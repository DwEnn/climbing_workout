from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MODULE_SPEC = importlib.util.spec_from_file_location(
    "validate_guides", ROOT / "scripts" / "validate_guides.py"
)
assert MODULE_SPEC and MODULE_SPEC.loader
validate_guides = importlib.util.module_from_spec(MODULE_SPEC)
sys.modules[MODULE_SPEC.name] = validate_guides
MODULE_SPEC.loader.exec_module(validate_guides)


class ValidateGuidesTest(unittest.TestCase):
    def test_current_repository_inventory_and_reference_targets(self) -> None:
        summary, findings = validate_guides.validate_guides(
            ROOT / "validation" / "spec.yaml",
            ROOT / "validation" / "source-audit.yaml",
        )

        self.assertEqual(summary["sessions"], 4)
        self.assertEqual(summary["exercises"], 18)
        self.assertEqual(summary["audit_exercises"], 21)
        self.assertEqual(summary["replacement_slots"], 11)
        self.assertEqual(summary["verified_replacements"], 7)
        self.assertEqual(summary["revised_currents"], 3)
        self.assertEqual(summary["removed_slots"], 1)
        self.assertEqual(summary["final_audit_exercises"], 18)
        self.assertEqual(summary["final_at_or_above_80"], 17)
        self.assertEqual(summary["final_below_80"], 1)
        self.assertEqual(summary["final_score_mean"], 84.8)
        self.assertEqual(summary["final_removed_after_rescore"], 2)
        self.assertEqual(summary["video_audit_exercises"], 18)
        self.assertEqual(summary["public_videos"], 18)
        self.assertEqual(summary["exact_video_matches"], 18)
        self.assertEqual(summary["retained_videos"], 8)
        self.assertEqual(summary["added_videos"], 3)
        self.assertEqual(summary["replaced_videos"], 7)
        self.assertGreater(summary["reference_links"], 0)
        self.assertFalse(
            any(item.code == "REFERENCE_TARGET_MISSING" for item in findings),
            "Every inline reference should resolve inside its guide.",
        )
        self.assertFalse(
            any(item.code.startswith("SOURCE_AUDIT_") for item in findings),
            "The source audit should cover every exercise with valid totals and sources.",
        )
        self.assertFalse(
            any(item.code.startswith("REPLACEMENT_") for item in findings),
            "Every replacement decision should independently pass the approval gate.",
        )
        self.assertFalse(
            any(item.code.startswith("FINAL_AUDIT_") for item in findings),
            "The final audit should match the active spec and current guide hashes.",
        )
        self.assertFalse(
            any(item.code.startswith("VIDEO_AUDIT_") for item in findings),
            "Every active exercise should have its exact audited video implemented.",
        )

    def test_high_score_does_not_override_replacement_hard_failure(self) -> None:
        policy = {
            "minimum_total_score": 80,
            "required_source_status": "verified",
            "require_no_hard_failures": True,
            "require_equipment_and_time_fit": True,
            "require_session_integration_pass": True,
        }
        candidate = {
            "source_status": "verified",
            "score": {"total": 95},
            "equipment_and_time_fit": "pass",
            "session_integration": "pass",
            "hard_failures": ["unavailable_required_equipment_without_safe_substitute"],
        }

        self.assertFalse(validate_guides.candidate_gate_pass(candidate, policy))

    def test_replacement_audit_is_linked_to_implemented_guide_title(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            replacement_path = Path(temp_dir) / "replacement-audit.yaml"
            replacement = yaml.safe_load(
                (ROOT / "validation" / "replacement-audit.yaml").read_text(encoding="utf-8")
            )
            replacement["slots"]["push.ex3"]["implemented_title"] = "다른 운동"
            replacement_path.write_text(
                yaml.safe_dump(replacement, allow_unicode=True),
                encoding="utf-8",
            )

            _, findings = validate_guides.validate_guides(
                ROOT / "validation" / "spec.yaml",
                ROOT / "validation" / "source-audit.yaml",
                replacement_path,
            )

            self.assertTrue(
                any(
                    item.code == "REPLACEMENT_IMPLEMENTATION_MISMATCH"
                    and item.exercise_id == "push.ex3"
                    for item in findings
                )
            )

    def test_final_audit_rejects_component_total_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            final_path = Path(temp_dir) / "final-audit.yaml"
            final_audit = yaml.safe_load(
                (ROOT / "validation" / "final-audit.yaml").read_text(encoding="utf-8")
            )
            final_audit["exercises"][0]["score"]["total"] = 99
            final_path.write_text(
                yaml.safe_dump(final_audit, allow_unicode=True),
                encoding="utf-8",
            )

            _, findings = validate_guides.validate_guides(
                ROOT / "validation" / "spec.yaml",
                ROOT / "validation" / "source-audit.yaml",
                ROOT / "validation" / "replacement-audit.yaml",
                final_path,
            )

            self.assertTrue(
                any(
                    item.code == "FINAL_AUDIT_SCORE_MISMATCH"
                    and item.exercise_id == "push.ex1"
                    for item in findings
                )
            )

    def test_final_audit_removed_slot_cannot_return_to_active_spec(self) -> None:
        spec = yaml.safe_load(
            (ROOT / "validation" / "spec.yaml").read_text(encoding="utf-8")
        )
        spec["sessions"]["core"]["exercises"].append(
            {
                "id": "ex7",
                "title": "글루트 브릿지",
                "slot": "posterior_chain",
                "page_declared_evidence": "principle",
            }
        )
        findings: list[validate_guides.Finding] = []

        validate_guides.validate_final_audit(
            spec,
            ROOT / "validation" / "source-audit.yaml",
            ROOT / "validation" / "final-audit.yaml",
            findings,
        )

        self.assertTrue(
            any(
                item.code == "FINAL_AUDIT_REMOVED_SLOT_STILL_ACTIVE"
                and item.exercise_id == "core.ex7"
                for item in findings
            )
        )

    def test_video_audit_must_match_implemented_card_video(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            video_path = Path(temp_dir) / "video-audit.yaml"
            video_audit = yaml.safe_load(
                (ROOT / "validation" / "video-audit.yaml").read_text(encoding="utf-8")
            )
            video_audit["videos"][0]["youtube_id"] = "YTAyc2uf_d0"
            video_audit["videos"][0]["youtube_url"] = (
                "https://www.youtube.com/watch?v=YTAyc2uf_d0"
            )
            video_path.write_text(
                yaml.safe_dump(video_audit, allow_unicode=True),
                encoding="utf-8",
            )

            _, findings = validate_guides.validate_guides(
                ROOT / "validation" / "spec.yaml",
                ROOT / "validation" / "source-audit.yaml",
                ROOT / "validation" / "replacement-audit.yaml",
                ROOT / "validation" / "final-audit.yaml",
                video_path,
            )

            self.assertTrue(
                any(
                    item.code == "VIDEO_AUDIT_IMPLEMENTATION_MISMATCH"
                    and item.exercise_id == "push.ex1"
                    for item in findings
                )
            )

    def test_workspace_output_path_rejects_escape(self) -> None:
        with self.assertRaises(ValueError):
            validate_guides.workspace_output_path("/tmp/outside-workspace.json")

    def test_documentation_drift_is_detected_with_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            guide_path = temp_path / "guide.html"
            guide_path.write_text("", encoding="utf-8")
            document_path = temp_path / "notes.md"
            document_path.write_text("old term", encoding="utf-8")
            spec = {
                "source_of_truth": {"disclaimer_policy": "none"},
                "sessions": {
                    "fixture": {
                        "guide": str(guide_path),
                        "exercises": [],
                    }
                },
                "documentation_drift_checks": [
                    {
                        "document": str(document_path),
                        "section": "fixture",
                        "stale_terms": ["old term"],
                        "missing_current_terms": ["new term"],
                    }
                ],
            }
            spec_path = temp_path / "spec.yaml"
            spec_path.write_text(yaml.safe_dump(spec), encoding="utf-8")

            _, findings = validate_guides.validate_guides(spec_path)
            self.assertTrue(any(item.code == "DOCUMENTATION_DRIFT" for item in findings))

    def test_detects_missing_reference_target_and_direct_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            guide = temp_path / "fixture.html"
            guide.write_text(
                """
                <section class="section fade-in" id="ex1">
                  <div class="section-header"><h2>테스트 운동</h2>
                    <p class="section-tagline">Test</p></div>
                  <div class="badge-row"><span class="badge badge-tier1">Tier 1</span></div>
                  <div class="media-grid">video</div>
                  <h3>원문 근거</h3><a href="#ref-9">[9]</a>
                  <h3>클라이밍 연관성</h3>
                  <div class="set-rest-card">sets</div>
                  <table class="prog-table"><tr><td>Lv.1</td></tr></table>
                  <h3>검증 수준</h3>
                </section>
                """,
                encoding="utf-8",
            )
            spec = {
                "source_of_truth": {"disclaimer_policy": "none"},
                "evidence_policy": {
                    "direct": {"required_card_marker": "✅"},
                    "principle": {"required_card_marker": "🔶"},
                    "mixed": {"required_card_markers": ["✅", "🔶"]},
                },
                "sessions": {
                    "fixture": {
                        "guide": str(guide),
                        "exercises": [
                            {
                                "id": "ex1",
                                "title": "테스트 운동",
                                "declared_evidence": "direct",
                            }
                        ],
                    }
                },
            }
            spec_path = temp_path / "spec.yaml"
            spec_path.write_text(yaml.safe_dump(spec, allow_unicode=True), encoding="utf-8")

            _, findings = validate_guides.validate_guides(spec_path)
            codes = {item.code for item in findings}
            self.assertIn("REFERENCE_TARGET_MISSING", codes)
            self.assertIn("EVIDENCE_MARKER_MISSING", codes)

    def test_minimal_fixture_uses_spec_relative_guide_and_default_policy(self) -> None:
        fixture_spec = (
            ROOT
            / "skills"
            / "workout-session-validator"
            / "evals"
            / "fixtures"
            / "invalid-spec.yaml"
        )
        summary, findings = validate_guides.validate_guides(fixture_spec)
        codes = {item.code for item in findings}

        self.assertEqual(summary["sessions"], 1)
        self.assertEqual(summary["exercises"], 1)
        self.assertIn("REFERENCE_TARGET_MISSING", codes)
        self.assertNotIn(
            "EVIDENCE_MARKER_MISSING",
            codes,
            "The fixture badge literally includes the direct marker.",
        )


if __name__ == "__main__":
    unittest.main()
