"""Regresje na pełnych lokalnych materiałach; testy nie wykonują żądań sieciowych."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import refresh_data as refresh
from refresh_parsers import history_tables, uew_durations


class RefreshTests(unittest.TestCase):
    def test_full_pwr_history_matches_audited_active_tables(self):
        html = (ROOT / 'docs/research/pwr/progi.html').read_bytes()
        tables = history_tables(html, [2026, 2025, 2024], 'pwr')
        expected = refresh.read_json(ROOT / 'docs/research/pwr/thresholds-active.json')['tables']
        self.assertEqual(tables, expected)
        self.assertEqual([t['year'] for t in tables], ['2026/2027', '2025/2026', '2024/2025'])

    def test_full_uew_plan_matches_all_twenty_offers_without_guessing(self):
        text = (ROOT / 'docs/research/curricula/uew/Programy-2026.txt').read_text(encoding='utf-8')
        programmes = refresh.read_json(ROOT / 'src/data/uew.json')['programmes']
        rows = uew_durations(text, programmes)
        self.assertEqual(len(rows), 20)
        self.assertEqual(len({r['programmeId'] for r in rows}), 20)
        self.assertTrue(all(r['duration'] in ['6 semestrów', '7 semestrów'] for r in rows))
        with self.assertRaises(ValueError):
            uew_durations(text.replace('Język kształcenia angielski', 'Język kształcenia polski'), programmes)

    def test_uew_archival_language_labels_are_matched_without_campus_merging(self):
        programme = refresh.read_json(ROOT / 'src/data/uew.json')['programmes']
        english = next(p for p in programme if p['name'] == 'Business Management')
        self.assertEqual(refresh.match_offer('Business Management (studia w j.angielskim)', programme, 'uew')['id'], english['id'])
        self.assertIsNone(refresh.match_offer('Zarządzanie w nowoczesnej gospodarce (Filia)', programme, 'uew'))
        self.assertIsNone(refresh.match_offer('Business Management (studia w j.angielskim)', [{**english, 'language': 'pl'}], 'uew'))

    def test_conflicts_and_rejected_claims_never_overwrite_previous_values(self):
        programme = {'id': 'uew-ekonomia', 'thresholds': [{'year': '2025/2026', 'round': None, 'value': 170, 'status': 'official', 'sourceId': 'old'}]}
        row = dict(year='2025/2026', round=None, value=180, raw='180')
        policy = refresh.read_json(ROOT / 'src/data/source-policy.json')
        with self.assertRaises(ValueError):
            refresh.add_observation(programme, row, 'portal', 'https://www.uczelnie.pl/progi-punktowe/ekonomia', policy, '2026-11-09')
        self.assertEqual(len(programme['thresholds']), 1)
        refresh.add_observation(programme, row, 'official-new', refresh.CORE['uew-thresholds'][1], policy, '2026-11-09')
        self.assertEqual([r['value'] for r in programme['thresholds']], [170, 180])
        self.assertFalse(refresh.add_observation(programme, row, 'official-new', refresh.CORE['uew-thresholds'][1], policy, '2026-11-09'))

    def test_failed_parser_keeps_real_active_data_and_has_no_proposal(self):
        before = refresh.input_hashes(ROOT)
        broken = b'<h2>2026/2027</h2><table><tr><th>Changed layout</th></tr></table>'
        with patch.object(refresh, 'download', return_value=(broken, {'status': 'changed'})):
            folder, report = refresh.run_refresh(ROOT, selected=['pwr-thresholds'])
        self.assertEqual(report['sources'][0]['status'], 'failed')
        self.assertEqual(report['files'], {})
        self.assertEqual(refresh.input_hashes(ROOT), before)
        with self.assertRaises(ValueError):
            refresh.apply_refresh(ROOT, folder)

    def test_apply_rejects_stale_and_modified_proposals_before_any_write(self):
        base = ROOT / 'output/data-refresh/runs'
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as name:
            folder = Path(name)
            report = dict(version=1, mode='core', applied=False, inputHashes={}, sources=[{'status': 'parsed'}], files={})
            (folder / 'report.json').write_bytes(refresh.json_bytes(report))
            with self.assertRaisesRegex(ValueError, 'zmieniły'):
                refresh.apply_refresh(ROOT, folder)
            report['inputHashes'] = refresh.input_hashes(ROOT)
            report['files'] = {'src/data/uew.json': {'before': refresh.digest((ROOT / 'src/data/uew.json').read_bytes()), 'after': 'fake'}}
            proposal = folder / 'proposal/src/data/uew.json'
            proposal.parent.mkdir(parents=True)
            proposal.write_text('{}', encoding='utf-8')
            (folder / 'report.json').write_bytes(refresh.json_bytes(report))
            with self.assertRaisesRegex(ValueError, 'Zmodyfikowano'):
                refresh.apply_refresh(ROOT, folder)

    def test_html_change_detection_includes_new_document_links_but_ignores_navigation(self):
        a = b'<main><p>Programme</p><a href="plan2026.pdf">Plan</a><nav>old</nav></main>'
        b = a.replace(b'<nav>old', b'<nav>new')
        c = b.replace(b'plan2026.pdf', b'plan2027.pdf')
        self.assertEqual(refresh.semantic_hash(a, 'text/html'), refresh.semantic_hash(b, 'text/html'))
        self.assertNotEqual(refresh.semantic_hash(a, 'text/html'), refresh.semantic_hash(c, 'text/html'))

    def test_policy_stops_redirect_before_requesting_excluded_host(self):
        from source_policy import guarded_get
        response = unittest.mock.Mock(status_code=302, headers={'Location': 'https://wroclaw.mapaakademicka.pl/'})
        with patch('source_policy.requests.get', return_value=response) as request:
            with self.assertRaisesRegex(ValueError, 'POMIŃ:'):
                guarded_get('https://rekrutacja.uwr.edu.pl/test')
        self.assertEqual(request.call_count, 1)

    def test_monitor_does_not_download_known_excluded_sources(self):
        item = dict(id='excluded', university='uwr', url='https://wroclaw.mapaakademicka.pl/', purpose='current')
        with patch.object(refresh, 'inventory', return_value=[item]), patch.object(refresh, 'download') as download:
            _, report = refresh.run_refresh(ROOT, mode='monitor')
        self.assertEqual(report['sources'][0]['status'], 'excluded')
        download.assert_not_called()

    def test_oversized_download_stops_stream_before_reading_the_rest(self):
        from source_policy import guarded_get
        response = unittest.mock.Mock(status_code=200, headers={})
        response.iter_content.return_value = iter([b'1234', b'5678', b'must not be consumed'])
        with patch('source_policy.requests.get', return_value=response):
            with self.assertRaisesRegex(ValueError, 'limit'):
                guarded_get('https://rekrutacja.uwr.edu.pl/test', max_bytes=6)
        self.assertEqual(next(response.iter_content.return_value), b'must not be consumed')
        response.close.assert_called_once()

    def test_all_pwr_plans_include_every_semester_and_hidden_elective_group(self):
        from pwr_curricula import parse_pwr_curriculum
        plans = refresh.read_json(ROOT / 'src/data/curricula-pwr.json')
        programmes = {p['id']: p for p in refresh.read_json(ROOT / 'src/data/pwr.json')['programmes']}
        links = refresh.read_json(ROOT / 'docs/research/pwr/syllabus-links.json')
        for plan in plans:
            url = next(s['url'] for s in plan['sources'] if 'sylabus.usos.pwr' in s['url'])
            cid = next(s['courseId'] for s in links if s['url'] == url)
            raw = (ROOT / f'docs/research/pwr/syllabi/{cid}.html').read_bytes()
            parsed, audit = parse_pwr_curriculum(raw, programmes[plan['programmeId']], url)
            self.assertEqual(parsed['completeness'], 'full-plan')
            self.assertGreater(audit['courseRows'], 20)
            self.assertEqual(audit['unresolvedTables'], 0)
            self.assertTrue(all(not s.startswith('Student/ka') for g in parsed['groups'] for s in g['subjects']))
        raw = (ROOT / 'docs/research/pwr/syllabi/54.html').read_bytes()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(raw, 'html.parser')
        target = soup.select_one('button.syl-group-head')['aria-controls'].split()[0]
        soup.find(id=target).decompose()
        with self.assertRaisesRegex(ValueError, 'koszyk'):
            parse_pwr_curriculum(str(soup).encode(), programmes['pwr-architektura'], plans[0]['sources'][-1]['url'])

    def test_european_cultures_audit_is_pinned_to_the_reviewed_document(self):
        from european_cultures import reviewed_plan
        original = next(r for r in refresh.read_json(ROOT / 'src/data/curricula-uwr-a.json') if r['programmeId'] == 'uwr-european-cultures')
        raw = (ROOT / 'docs/research/curricula/uwr-a/european-cultures-program-2023.pdf').read_bytes()
        plan = reviewed_plan(raw, original, ROOT, '2026-11-09')
        self.assertEqual(sum(len(g['subjects']) for g in plan['groups']), 59)
        self.assertEqual(len([g for g in plan['groups'] if g['title'].startswith('Do wyboru')]), 5)
        self.assertTrue(any(g['semester'] == 'II, III, IV, V' for g in plan['groups']))
        with self.assertRaisesRegex(ValueError, 'zmienił'):
            reviewed_plan(raw + b'changed', original, ROOT, '2026-11-09')


if __name__ == '__main__':
    unittest.main()
