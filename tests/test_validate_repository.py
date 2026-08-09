#!/usr/bin/env python3
"""Regression tests for repository guidance validation."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidationTests(unittest.TestCase):
    def test_each_required_one_shot_guidance_section_is_enforced(self) -> None:
        required_sections = (
            (
                "docs/adventure-structure-guide.md",
                "## Pacing und sichere Kürzbarkeit",
                "adventure structure guide",
            ),
            (
                "docs/adventure-audit-guide.md",
                "## Spielerausgaben und Visuals",
                "adventure audit guide",
            ),
            (
                "docs/adventure-audit-guide.md",
                "## Pacing und sichere Kürzbarkeit",
                "adventure audit guide",
            ),
            (
                "docs/adventure-audit-guide.md",
                "## Übersichten und Navigationswege",
                "adventure audit guide",
            ),
            (
                "docs/adventure-audit-guide.md",
                "## Tischreife",
                "adventure audit guide",
            ),
        )

        with tempfile.TemporaryDirectory(
            prefix="dm-asset-forge-repository-test-", dir=ROOT.parent
        ) as temporary:
            repo = Path(temporary) / "repo"
            shutil.copytree(
                ROOT,
                repo,
                ignore=shutil.ignore_patterns("__pycache__", "adventure"),
            )

            for relative_path, heading, guide_name in required_sections:
                with self.subTest(path=relative_path, heading=heading):
                    path = repo / relative_path
                    original = path.read_text(encoding="utf-8")
                    self.assertIn(heading, original)
                    path.write_text(
                        original.replace(heading, f"## Removed: {heading[3:]}", 1),
                        encoding="utf-8",
                    )

                    result = subprocess.run(
                        ["python3", "scripts/validate_repository.py"],
                        cwd=repo,
                        capture_output=True,
                        text=True,
                    )

                    self.assertEqual(result.returncode, 1)
                    self.assertIn(
                        f"{guide_name} is missing section: {heading}",
                        result.stdout,
                    )
                    path.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
