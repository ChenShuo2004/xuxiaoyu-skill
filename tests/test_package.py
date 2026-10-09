import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'scripts'))
from check_package import check
from install import install

class PackageTests(unittest.TestCase):
    def test_relocated_offline_install(self):
        with tempfile.TemporaryDirectory(prefix='other-user-') as td:
            result=install(ROOT,Path(td)/'skills')
            target=Path(result['installed'])
            self.assertEqual(check(ROOT),check(target))
            for rel,digest in json.loads((ROOT/'manifest.json').read_text())['files'].items():
                self.assertEqual(hashlib.sha256((target/rel).read_bytes()).hexdigest(),digest)

    def test_existing_install_is_preserved_and_update_backed_up(self):
        with tempfile.TemporaryDirectory() as td:
            target=Path(install(ROOT,td)['installed'])
            (target/'local-note.txt').write_text('keep my edits')
            with self.assertRaises(ValueError):install(ROOT,td)
            result=install(ROOT,td,update=True)
            self.assertEqual((Path(result['backup'])/'local-note.txt').read_text(),'keep my edits')
            check(target)

    def test_do_not_overwrite_source(self):
        with self.assertRaises(ValueError):install(ROOT,ROOT,True)

    def test_detect_corrupted_resource(self):
        with tempfile.TemporaryDirectory() as td:
            target=Path(install(ROOT,td)['installed'])
            (target/'references/claims.jsonl').write_text('broken')
            with self.assertRaises(ValueError):check(target)

if __name__=='__main__':unittest.main()
