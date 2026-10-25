import ast
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'app.py').read_text(encoding='utf-8')
TREE = ast.parse(SOURCE)

class SecurityContracts(unittest.TestCase):
    def test_central_security_hooks(self):
        names = {node.name for node in TREE.body if isinstance(node, ast.FunctionDef)}
        for name in ('protect_medical_routes', '_can_access_medical_record', '_current_actor', 'prevent_personal_data_caching'):
            self.assertIn(name, names)
        self.assertIn('compare_digest', SOURCE)
        self.assertIn('SESSION_COOKIE_SECURE', SOURCE)

    def test_csrf_in_post_forms(self):
        for path in (ROOT / 'templates').glob('*.html'):
            html = path.read_text(encoding='utf-8')
            for match in re.finditer('<form[^>]*>', html, re.I | re.S):
                if 'method="post"' not in match.group(0).lower():
                    continue
                end = html.lower().find('</form>', match.end())
                self.assertNotEqual(end, -1, str(path))
                self.assertIn('name="_csrf_token"', html[match.end():end], str(path))

    def test_ajax_writes_include_token(self):
        self.assertIn('X-CSRF-Token', (ROOT / 'static/js/script.js').read_text(encoding='utf-8'))

if __name__ == '__main__':
    unittest.main()
