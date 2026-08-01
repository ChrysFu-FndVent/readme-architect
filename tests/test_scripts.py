"""Regression tests for the standard-library README Architect scripts."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANALYZER = ROOT / "scripts" / "analyze_project.py"
VALIDATOR = ROOT / "scripts" / "validate_readme.py"


class AnalyzeProjectTests(unittest.TestCase):
    def test_readme_architectignore_excludes_project_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "src").mkdir()
            (project / "internal").mkdir()
            (project / "nested").mkdir()
            (project / "package.json").write_text(
                '{"name":"demo","description":"Recipe nutrition planner"}', encoding="utf-8"
            )
            (project / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
            (project / "internal" / "secret.py").write_text("token = 'private'\n", encoding="utf-8")
            (project / "nested" / "config.yaml").write_text("nested: true\n", encoding="utf-8")
            (project / "config.yaml").write_text("root: true\n", encoding="utf-8")
            (project / ".readme-architectignore").write_text(
                "internal/\n*.py\n!src/app.py\n/config.yaml\n", encoding="utf-8"
            )
            output = project / "profile.json"

            result = subprocess.run(
                [sys.executable, str(ANALYZER), "--root", str(project), "--out", str(output)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            profile = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(profile["ignore_patterns"], ["internal/", "*.py", "!src/app.py", "/config.yaml"])
            self.assertNotIn("internal", profile["top_level"])
            self.assertEqual(profile["total_files"], 4)
            self.assertEqual(profile["language_counts"], {"Python": 1})
            self.assertEqual(profile["presentation_profile"]["key"], "food-health")
            self.assertEqual(profile["presentation_profile"]["matched_terms"], ["nutrition", "recipe"])


class ValidateReadmeTests(unittest.TestCase):
    def run_validator(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README.md"
            path.write_text(text, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), "--bilingual", str(path)],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_bilingual_contract_accepts_chinese_before_english(self):
        result = self.run_validator("""<div align=\"right\"><a href=\"#简体中文\">简体中文</a> | <a href=\"#english\">English</a></div>
<h1>Demo</h1>

<a id=\"简体中文\"></a>
## 简介
中文内容。

<a id=\"english\"></a>
## About
English content.

## License
MIT.
""")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_bilingual_contract_rejects_english_before_chinese(self):
        result = self.run_validator("""<div align=\"right\"><a href=\"#简体中文\">简体中文</a> | <a href=\"#english\">English</a></div>
<h1>Demo</h1>

<a id=\"english\"></a>
## About
English content.

<a id=\"简体中文\"></a>
## 简介
中文内容。

## License
MIT.
""")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Chinese body before the English body", result.stdout)


if __name__ == "__main__":
    unittest.main()
