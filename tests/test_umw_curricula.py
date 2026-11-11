import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from umw_curricula import parse_umw_curriculum

class UmwCurriculaTests(unittest.TestCase):
    def test_all_16_documents_match_canonical_partial_lists(self):
        folder=ROOT/'docs/research/umw'
        manifest=json.loads((folder/'manifest.json').read_text(encoding='utf8'))
        programmes=json.loads((ROOT/'src/data/umw.json').read_text(encoding='utf8'))['programmes']
        records=json.loads((ROOT/'src/data/curricula-umw.json').read_text(encoding='utf8'))
        self.assertEqual(len(records),16)
        for entry in manifest['plans']:
            p=next(p for p in programmes if p['id']==entry['programmeId'])
            record,audit=parse_umw_curriculum((folder/entry['planFile']).read_bytes(),p,entry['planUrl'])
            self.assertEqual(record,next(r for r in records if r['programmeId']==p['id']))
            self.assertEqual(record['completeness'],'listed-subjects')
            self.assertGreater(audit['rows'],30)
            self.assertEqual(audit['rows'],entry['rows'])
            self.assertTrue(all(g['semester'] is None for g in record['groups']))
        self.assertEqual(sum(len(g['subjects']) for r in records for g in r['groups']),1244)
        # Załącznik z tej samej strony BIP, ale innego kierunku i poziomu, musi zostać odrzucony.
        with self.assertRaisesRegex(ValueError,'Inny kierunek'):
            parse_umw_curriculum((folder/'plan-psychologia.docx').read_bytes(),next(p for p in programmes if p['id']=='umw-psychologia'),'https://bip.umw.edu.pl/attachments/download/19558')
