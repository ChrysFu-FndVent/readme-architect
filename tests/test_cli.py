"""End-to-end tests for the offline CLI and deterministic renderer."""

from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

from readme_architect import cli
from readme_architect.renderer import render_readme
from scripts import validate_readme
from scripts.analyze_project import analyze


class OfflineCliTests(unittest.TestCase):
    def make_project(self, root):
        project = Path(root)
        (project / "src").mkdir()
        (project / "tests").mkdir()
        (project / "pyproject.toml").write_text(
            """[project]
name = "evidence-demo"
version = "1.2.3"
description = "A verified command-line demonstration"
requires-python = ">=3.9"

[project.scripts]
evidence-demo = "demo:main"
""",
            encoding="utf-8",
        )
        (project / "src" / "demo.py").write_text("def main():\n    return 0\n", encoding="utf-8")
        (project / "tests" / "test_demo.py").write_text("import unittest\n", encoding="utf-8")
        (project / "LICENSE").write_text("MIT License\n", encoding="utf-8")
        (project / "README.md").write_text("# Original\n\nKeep this text.\n", encoding="utf-8")
        return project

    def run_cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = cli.main(list(args))
        self.assertEqual(result, 0)
        return output.getvalue()

    def test_default_writes_candidate_and_isolated_banner_only(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = self.make_project(temp_dir)
            original = (project / "README.md").read_text(encoding="utf-8")

            self.run_cli(str(project))

            self.assertEqual((project / "README.md").read_text(encoding="utf-8"), original)
            candidate = project / "README.generated.md"
            banner = project / ".readme-architect/generated/evidence-demo-banner.svg"
            self.assertTrue(candidate.is_file())
            self.assertTrue(banner.is_file())
            generated = candidate.read_text(encoding="utf-8")
            self.assertLess(generated.index("Table of Contents"), generated.index('<a id="简体中文">'))
            self.assertLess(generated.index('<a id="简体中文">'), generated.index('<a id="english">'))
            self.assertIn("evidence-demo --help", generated)

    def test_custom_output_in_subdirectory_uses_valid_banner_reference(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = self.make_project(temp_dir)
            candidate = project / "previews/README.preview.md"

            self.run_cli(str(project), "--output", "previews/README.preview.md")

            generated = candidate.read_text(encoding="utf-8")
            self.assertIn('../.readme-architect/generated/evidence-demo-banner.svg', generated)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(validate_readme.main(["--bilingual", str(candidate)]), 0)

    def test_absolute_output_outside_project_uses_valid_banner_reference(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            project = workspace / "project"
            project.mkdir()
            self.make_project(project)
            candidate = workspace / "previews/nested/README.preview.md"

            self.run_cli(str(project), "--output", str(candidate))

            generated = candidate.read_text(encoding="utf-8")
            expected_banner = project / ".readme-architect/generated/evidence-demo-banner.svg"
            reference = os.path.relpath(expected_banner, start=candidate.parent).replace(os.sep, "/")
            self.assertIn(reference, generated)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(validate_readme.main(["--bilingual", str(candidate)]), 0)

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = self.make_project(temp_dir)

            output = self.run_cli(str(project), "--dry-run")

            self.assertIn("No files written", output)
            self.assertFalse((project / "README.generated.md").exists())
            self.assertFalse((project / ".readme-architect").exists())

    def test_diff_previews_without_writing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = self.make_project(temp_dir)

            output = self.run_cli(str(project), "--diff")

            self.assertIn("--- ", output)
            self.assertIn("+++ ", output)
            self.assertFalse((project / "README.generated.md").exists())
            self.assertFalse((project / ".readme-architect").exists())

    def test_write_replaces_readme_without_prompt(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = self.make_project(temp_dir)

            self.run_cli(str(project), "--write")

            generated = (project / "README.md").read_text(encoding="utf-8")
            self.assertNotIn("Keep this text", generated)
            self.assertTrue((project / "assets/readme/evidence-demo-banner.svg").is_file())
            self.assertFalse((project / "README.generated.md").exists())

    def test_suggest_only_json_is_machine_readable_and_read_only(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = self.make_project(temp_dir)

            output = self.run_cli(str(project), "--suggest-only", "--json")
            payload = json.loads(output)

            self.assertEqual(payload["project"], "evidence-demo")
            self.assertEqual(payload["facts"]["languages"], ["Python"])
            self.assertTrue(payload["facts"]["tests"])
            self.assertFalse((project / "README.generated.md").exists())


class RendererEvidenceTests(unittest.TestCase):
    def test_mermaid_nodes_come_from_detected_top_level_entries(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = OfflineCliTests().make_project(temp_dir)
            profile = analyze(project)

            rendered = render_readme(profile)

            self.assertIn('N0["src"]', rendered.text)
            self.assertIn('N1["tests"]', rendered.text)
            self.assertNotIn("Database", rendered.text)
            self.assertNotIn("Cloud", rendered.text)
            self.assertIn("<svg", rendered.banner)


if __name__ == "__main__":
    unittest.main()
