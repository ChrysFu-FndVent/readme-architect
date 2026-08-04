"""Tests for release and skill packaging helpers."""

from __future__ import annotations

import os
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.package_skill import build_archive
from scripts.stage_binary import main as stage_binary


class SkillArchiveTests(unittest.TestCase):
    def test_archive_contains_skill_resources_but_not_project_readme(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "source"
            root.mkdir()
            (root / "SKILL.md").write_text("---\nname: readme-architect\n---\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "README.md").write_text("project documentation\n", encoding="utf-8")
            (root / "assets/readme").mkdir(parents=True)
            (root / "assets/readme/banner.png").write_bytes(b"project artwork")
            (root / "references").mkdir()
            (root / "references" / "rules.md").write_text("rules\n", encoding="utf-8")
            output = Path(temp_dir) / "skill.zip"

            build_archive(output, root)

            with zipfile.ZipFile(output) as archive:
                names = set(archive.namelist())
            self.assertIn("readme-architect/SKILL.md", names)
            self.assertIn("readme-architect/references/rules.md", names)
            self.assertNotIn("readme-architect/README.md", names)
            self.assertNotIn("readme-architect/assets/readme/banner.png", names)


class StageBinaryTests(unittest.TestCase):
    def test_stage_binary_copies_and_marks_executable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source"
            output = Path(temp_dir) / "release" / "readme-architect"
            source.write_bytes(b"binary")

            result = stage_binary(["--source", str(source), "--output", str(output)])

            self.assertEqual(result, 0)
            self.assertEqual(output.read_bytes(), b"binary")
            if os.name != "nt":
                self.assertTrue(output.stat().st_mode & 0o111)


if __name__ == "__main__":
    unittest.main()
