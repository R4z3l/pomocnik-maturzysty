import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from upwr_curricula import parse_upwr_curriculum


class UpwrCurriculaTests(unittest.TestCase):
    def test_all_real_plans_match_reviewed_records_including_hidden_baskets(self):
        folder=ROOT/'docs/research/upwr'
        data=json.loads((ROOT/'src/data/upwr.json').read_text(encoding='utf-8'))
        canonical=json.loads((ROOT/'src/data/curricula-upwr.json').read_text(encoding='utf-8'))
        manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(len(canonical),28)
        index=json.loads((folder/'plan-index.json').read_text(encoding='utf-8'))
        for item in manifest['offers']:
            programme=next(p for p in data['programmes'] if p['id']==item['programmeId'])
            source=next(p for p in index if p['url']==item['planUrl'])
            html=(folder/(source['file']+'.html')).read_text(encoding='utf-8')
            record,audit=parse_upwr_curriculum(html,programme,item['planUrl'])
            self.assertEqual(record,next(r for r in canonical if r['programmeId']==programme['id']))
            self.assertEqual(audit['semesters'],item['semesters'])
            self.assertEqual(audit['subjectRows'],item['subjectRows'])
            self.assertGreater(audit['subjectRows'],40)
            with self.assertRaises(ValueError):
                parse_upwr_curriculum(html.replace('2026/27','2025/26'),programme,item['planUrl'])

    def test_instructions_and_hours_are_never_course_names(self):
        data=json.loads((ROOT/'src/data/curricula-upwr.json').read_text(encoding='utf-8'))
        subjects=[s for r in data for g in r['groups'] for s in g['subjects']]
        self.assertGreater(len(subjects),3000)
        self.assertTrue(any(g['title'].startswith('Pula wyboru:') for r in data for g in r['groups']))
        self.assertFalse(any(s.startswith(('student realizuje','Student wybiera','Punkty ECTS:')) for s in subjects))
