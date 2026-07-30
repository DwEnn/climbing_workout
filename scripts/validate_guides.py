#!/usr/bin/env python3
"""Validate workout guide structure against validation/spec.yaml."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE_POLICY = {
    "direct": {"required_card_marker": "✅"},
    "principle": {"required_card_marker": "🔶"},
    "mixed": {"required_card_markers": ["✅", "🔶"]},
}
SCORE_DIMENSIONS = (
    "evidence_accuracy",
    "goal_and_pattern_fit",
    "session_integration",
    "equipment_and_time_fit",
    "usability_and_progression",
)
YOUTUBE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")
VIDEO_ACTIONS = {"retained", "added", "replaced"}


@dataclass
class Finding:
    severity: str
    code: str
    path: str
    message: str
    exercise_id: str | None = None


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(html.unescape(value).split())


def section_for_id(document: str, exercise_id: str) -> str | None:
    match = re.search(
        rf'<section\b[^>]*\bid="{re.escape(exercise_id)}"[^>]*>(.*?)</section>',
        document,
        flags=re.DOTALL | re.IGNORECASE,
    )
    return match.group(1) if match else None


def has_heading(section: str, text: str) -> bool:
    return bool(re.search(rf"<h[23]\b[^>]*>.*?{re.escape(text)}.*?</h[23]>", section, re.DOTALL))


def youtube_id_from_url(value: str) -> str | None:
    """Extract a canonical 11-character YouTube video ID from a supported URL."""
    match = re.search(
        r"(?:youtube\.com/watch\?(?:[^\"']*&)*v=|youtu\.be/)([A-Za-z0-9_-]{11})",
        html.unescape(value),
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else None


def validate_card(
    findings: list[Finding],
    rel_path: str,
    section: str,
    exercise: dict[str, Any],
    evidence_policy: dict[str, Any],
    video_policy: dict[str, Any] | None = None,
) -> None:
    exercise_id = exercise["id"]
    title_match = re.search(r"<h2\b[^>]*>(.*?)</h2>", section, flags=re.DOTALL)
    actual_title = strip_tags(title_match.group(1)) if title_match else ""
    if actual_title != exercise["title"]:
        findings.append(
            Finding(
                "error",
                "TITLE_MISMATCH",
                rel_path,
                f"Expected title '{exercise['title']}', found '{actual_title or 'none'}'.",
                exercise_id,
            )
        )

    requires_video = bool((video_policy or {}).get("required_videos_per_exercise"))
    field_checks = {
        "subtitle": 'class="section-tagline"' in section,
        "evidence_badge": 'class="badge-row"' in section and 'class="badge ' in section,
        "reference_media": (
            'class="media-grid"' in section
            and (not requires_video or "youtube.com/watch" in section)
        ),
        "source_basis": has_heading(section, "원문 근거") or has_heading(section, "운동 방법"),
        "climbing_relevance": "클라이밍 연관성" in section,
        "sets_reps_rest": 'class="set-rest-card"' in section,
        "progression": 'class="prog-table"' in section,
        "validation_summary": "검증 수준" in section,
    }
    for field, present in field_checks.items():
        if not present:
            findings.append(
                Finding(
                    "error",
                    "CARD_FIELD_MISSING",
                    rel_path,
                    f"Required card field missing: {field}.",
                    exercise_id,
                )
            )

    badge_match = re.search(
        r'<div class="badge-row">(.*?)</div>',
        section,
        flags=re.DOTALL | re.IGNORECASE,
    )
    badge_text = strip_tags(badge_match.group(1)) if badge_match else ""
    evidence_kind = exercise.get("page_declared_evidence", exercise.get("declared_evidence"))
    if evidence_kind == "mixed":
        required_markers = evidence_policy["mixed"]["required_card_markers"]
    else:
        required_markers = [evidence_policy[evidence_kind]["required_card_marker"]]
    missing = [marker for marker in required_markers if marker not in badge_text]
    if missing:
        findings.append(
            Finding(
                "warning",
                "EVIDENCE_MARKER_MISSING",
                rel_path,
                f"Badge row is missing declared evidence marker(s): {', '.join(missing)}.",
                exercise_id,
            )
        )

    refs = re.findall(r'href="#(ref-\d+)"', section)
    if not refs:
        findings.append(
            Finding(
                "error",
                "CARD_REFERENCE_MISSING",
                rel_path,
                "Exercise card has no inline reference link.",
                exercise_id,
            )
        )


def validate_source_audit(
    spec: dict[str, Any],
    audit_path: Path,
    findings: list[Finding],
    replacement_outcomes: dict[str, str] | None = None,
    retired_keys: set[str] | None = None,
) -> int:
    """Check that the evidence audit is complete and internally consistent."""
    if not audit_path.exists():
        findings.append(
            Finding("error", "SOURCE_AUDIT_MISSING", str(audit_path), "Source audit does not exist.")
        )
        return 0

    audit = yaml.safe_load(audit_path.read_text(encoding="utf-8"))
    entries = audit.get("exercises", [])
    expected_keys = {
        f"{session_id}.{exercise['id']}"
        for session_id, session in spec["sessions"].items()
        for exercise in session["exercises"]
    }
    replacement_outcomes = replacement_outcomes or {}
    expected_keys.update(
        key for key, outcome in replacement_outcomes.items() if outcome == "remove_slot"
    )
    expected_keys.update(retired_keys or set())
    actual_keys = [entry.get("key") for entry in entries]

    duplicates = sorted({key for key in actual_keys if actual_keys.count(key) > 1})
    if duplicates:
        findings.append(
            Finding(
                "error",
                "SOURCE_AUDIT_DUPLICATE",
                str(audit_path),
                f"Duplicate exercise keys: {', '.join(duplicates)}.",
            )
        )
    missing = sorted(expected_keys - set(actual_keys))
    extra = sorted(set(actual_keys) - expected_keys)
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if extra:
            details.append(f"unexpected: {', '.join(extra)}")
        findings.append(
            Finding(
                "error",
                "SOURCE_AUDIT_INVENTORY_MISMATCH",
                str(audit_path),
                "; ".join(details) + ".",
            )
        )

    source_keys = set(audit.get("sources", {}))
    alternative_scorecards = audit.get("alternative_scorecards", {})
    regret_threshold = audit.get("scope", {}).get("selection_regret_threshold", 5)
    for entry in entries:
        key = entry.get("key", "unknown")
        score = entry.get("score", {})
        calculated_total = sum(score.get(dimension, 0) for dimension in SCORE_DIMENSIONS)
        if calculated_total != score.get("total"):
            findings.append(
                Finding(
                    "error",
                    "SOURCE_AUDIT_SCORE_MISMATCH",
                    str(audit_path),
                    f"Components total {calculated_total}, recorded {score.get('total')}.",
                    key,
                )
            )
        alternatives = entry.get("alternatives", [])
        if len(alternatives) != 2:
            findings.append(
                Finding(
                    "error",
                    "SOURCE_AUDIT_ALTERNATIVE_COUNT",
                    str(audit_path),
                    f"Expected two alternatives, found {len(alternatives)}.",
                    key,
                )
            )
        scorecards = alternative_scorecards.get(key, [])
        if len(scorecards) != len(alternatives):
            findings.append(
                Finding(
                    "error",
                    "SOURCE_AUDIT_ALTERNATIVE_SCORECARD_COUNT",
                    str(audit_path),
                    f"Expected {len(alternatives)} alternative scorecards, found {len(scorecards)}.",
                    key,
                )
            )
        for index, (alternative, scorecard) in enumerate(
            zip(alternatives, scorecards, strict=False),
            start=1,
        ):
            calculated = sum(scorecard.get(dimension, 0) for dimension in SCORE_DIMENSIONS)
            if calculated != scorecard.get("total") or scorecard.get("total") != alternative.get(
                "score"
            ):
                findings.append(
                    Finding(
                        "error",
                        "SOURCE_AUDIT_ALTERNATIVE_SCORE_MISMATCH",
                        str(audit_path),
                        (
                            f"Alternative {index} components total {calculated}, "
                            f"scorecard records {scorecard.get('total')}, "
                            f"alternative records {alternative.get('score')}."
                        ),
                        key,
                    )
                )
        referenced = set(entry.get("source_keys", []))
        referenced.update(
            alternative.get("source_key")
            for alternative in alternatives
            if alternative.get("source_key")
        )
        unknown_sources = sorted(referenced - source_keys)
        if unknown_sources:
            findings.append(
                Finding(
                    "error",
                    "SOURCE_AUDIT_SOURCE_UNKNOWN",
                    str(audit_path),
                    f"Unknown source keys: {', '.join(unknown_sources)}.",
                    key,
                )
            )
        hard_failures = set(entry.get("hard_failures", []))
        disposition = entry.get("disposition")
        final_outcome = replacement_outcomes.get(key)
        expected_disposition = {
            "verified_replacement": "replace",
            "revise_current": "revise",
            "remove_slot": "remove",
        }.get(final_outcome)
        if expected_disposition and disposition != expected_disposition:
            findings.append(
                Finding(
                    "error",
                    "SOURCE_AUDIT_FINAL_DISPOSITION_MISMATCH",
                    str(audit_path),
                    (
                        f"Final replacement outcome '{final_outcome}' requires disposition "
                        f"'{expected_disposition}', found '{disposition}'."
                    ),
                    key,
                )
            )
        selection_failures = hard_failures - {"unsupported_or_misattributed_direct_claim"}
        if hard_failures and disposition == "retain":
            findings.append(
                Finding(
                    "error",
                    "SOURCE_AUDIT_HARD_FAILURE_RETAINED",
                    str(audit_path),
                    "An exercise with a publication hard failure cannot be retained as-is.",
                    key,
                )
            )
        if selection_failures and disposition not in {"replace", "remove"}:
            findings.append(
                Finding(
                    "error",
                    "SOURCE_AUDIT_SELECTION_FAILURE_DISPOSITION",
                    str(audit_path),
                    "Equipment or safety hard failures require replace or remove.",
                    key,
                )
            )
        best_alternative = max(
            (alternative.get("score", 0) for alternative in alternatives),
            default=0,
        )
        if (
            best_alternative - score.get("total", 0) > regret_threshold
            and disposition not in {"replace", "remove"}
            and final_outcome is None
        ):
            findings.append(
                Finding(
                    "error",
                    "SOURCE_AUDIT_SELECTION_REGRET_DISPOSITION",
                    str(audit_path),
                    (
                        f"Best alternative wins by {best_alternative - score.get('total', 0)} "
                        f"points, above the {regret_threshold}-point threshold."
                    ),
                    key,
                )
            )
    return len(entries)


def candidate_gate_pass(candidate: dict[str, Any], policy: dict[str, Any]) -> bool:
    """Return whether a replacement candidate independently clears every gate."""
    return (
        candidate.get("score", {}).get("total", 0) >= policy.get("minimum_total_score", 80)
        and candidate.get("source_status") == policy.get("required_source_status", "verified")
        and (
            not policy.get("require_no_hard_failures", True)
            or not candidate.get("hard_failures", [])
        )
        and (
            not policy.get("require_equipment_and_time_fit", True)
            or candidate.get("equipment_and_time_fit") == "pass"
        )
        and (
            not policy.get("require_session_integration_pass", True)
            or candidate.get("session_integration") == "pass"
        )
    )


def validate_replacement_audit(
    spec: dict[str, Any],
    source_audit_path: Path,
    replacement_path: Path,
    findings: list[Finding],
) -> tuple[dict[str, str], dict[str, int]]:
    """Validate final replacement decisions after same-gate candidate review."""
    if not replacement_path.exists():
        findings.append(
            Finding(
                "error",
                "REPLACEMENT_AUDIT_MISSING",
                str(replacement_path),
                "Replacement audit does not exist.",
            )
        )
        return {}, {}

    source_audit = yaml.safe_load(source_audit_path.read_text(encoding="utf-8"))
    replacement = yaml.safe_load(replacement_path.read_text(encoding="utf-8"))
    slots = replacement.get("slots", {})
    reopened = {
        entry.get("key")
        for entry in source_audit.get("exercises", [])
        if entry.get("disposition") in {"replace", "remove"}
        or entry.get("screening_disposition") == "replace"
    }
    actual = set(slots)
    missing = sorted(reopened - actual)
    extra = sorted(actual - reopened)
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if extra:
            details.append(f"unexpected: {', '.join(extra)}")
        findings.append(
            Finding(
                "error",
                "REPLACEMENT_AUDIT_COVERAGE_MISMATCH",
                str(replacement_path),
                "; ".join(details) + ".",
            )
        )

    policy = spec.get("replacement_approval", {})
    allowed_outcomes = set(
        policy.get(
            "allowed_outcomes",
            ["verified_replacement", "revise_current", "remove_slot", "unresolved"],
        )
    )
    known_sources = set(source_audit.get("sources", {}))
    outcomes: dict[str, str] = {}
    outcome_counts = {outcome: 0 for outcome in allowed_outcomes}
    candidate_total = 0
    implemented_exercises = {
        f"{session_id}.{exercise['id']}": exercise["title"]
        for session_id, session in spec["sessions"].items()
        for exercise in session["exercises"]
    }

    for key, slot in slots.items():
        candidates = slot.get("candidates", [])
        candidate_total += len(candidates)
        if len(candidates) != 2:
            findings.append(
                Finding(
                    "error",
                    "REPLACEMENT_CANDIDATE_COUNT",
                    str(replacement_path),
                    f"Expected two candidates, found {len(candidates)}.",
                    key,
                )
            )

        passing_names: set[str] = set()
        for candidate in candidates:
            score = candidate.get("score", {})
            calculated = sum(score.get(dimension, 0) for dimension in SCORE_DIMENSIONS)
            if calculated != score.get("total"):
                findings.append(
                    Finding(
                        "error",
                        "REPLACEMENT_SCORE_MISMATCH",
                        str(replacement_path),
                        (
                            f"Candidate '{candidate.get('name')}' components total "
                            f"{calculated}, recorded {score.get('total')}."
                        ),
                        key,
                    )
                )
            unknown_sources = sorted(set(candidate.get("source_keys", [])) - known_sources)
            if unknown_sources:
                findings.append(
                    Finding(
                        "error",
                        "REPLACEMENT_SOURCE_UNKNOWN",
                        str(replacement_path),
                        f"Unknown source keys: {', '.join(unknown_sources)}.",
                        key,
                    )
                )
            passed = candidate_gate_pass(candidate, policy)
            recorded = candidate.get("gate_status")
            if recorded != ("pass" if passed else "fail"):
                findings.append(
                    Finding(
                        "error",
                        "REPLACEMENT_GATE_STATUS_MISMATCH",
                        str(replacement_path),
                        (
                            f"Candidate '{candidate.get('name')}' records gate status "
                            f"'{recorded}', calculated '{'pass' if passed else 'fail'}'."
                        ),
                        key,
                    )
                )
            if passed:
                passing_names.add(candidate.get("name"))

        correction = slot.get("corrected_current")
        correction_passes = False
        if correction:
            score = correction.get("score", {})
            calculated = sum(score.get(dimension, 0) for dimension in SCORE_DIMENSIONS)
            if calculated != score.get("total"):
                findings.append(
                    Finding(
                        "error",
                        "REPLACEMENT_CORRECTION_SCORE_MISMATCH",
                        str(replacement_path),
                        (
                            f"Corrected current components total {calculated}, "
                            f"recorded {score.get('total')}."
                        ),
                        key,
                    )
                )
            unknown_sources = sorted(set(correction.get("source_keys", [])) - known_sources)
            if unknown_sources:
                findings.append(
                    Finding(
                        "error",
                        "REPLACEMENT_SOURCE_UNKNOWN",
                        str(replacement_path),
                        f"Unknown source keys: {', '.join(unknown_sources)}.",
                        key,
                    )
                )
            correction_passes = candidate_gate_pass(correction, policy)
            if correction.get("gate_status") != ("pass" if correction_passes else "fail"):
                findings.append(
                    Finding(
                        "error",
                        "REPLACEMENT_GATE_STATUS_MISMATCH",
                        str(replacement_path),
                        "Corrected-current gate status does not match the calculated result.",
                        key,
                    )
                )

        outcome = slot.get("outcome")
        outcomes[key] = outcome
        if outcome not in allowed_outcomes:
            findings.append(
                Finding(
                    "error",
                    "REPLACEMENT_OUTCOME_INVALID",
                    str(replacement_path),
                    f"Invalid outcome: {outcome}.",
                    key,
                )
            )
            continue
        outcome_counts[outcome] += 1
        approved = slot.get("approved_candidate")
        if outcome == "verified_replacement" and approved not in passing_names:
            findings.append(
                Finding(
                    "error",
                    "REPLACEMENT_NOT_GATE_APPROVED",
                    str(replacement_path),
                    f"Approved candidate '{approved}' did not pass every gate.",
                    key,
                )
            )
        if outcome in {"verified_replacement", "revise_current"}:
            implemented_title = slot.get("implemented_title")
            expected_title = implemented_exercises.get(key)
            if implemented_title is None or implemented_title != expected_title:
                findings.append(
                    Finding(
                        "error",
                        "REPLACEMENT_IMPLEMENTATION_MISMATCH",
                        str(replacement_path),
                        (
                            f"Replacement audit records implemented title "
                            f"'{implemented_title}', spec records '{expected_title}'."
                        ),
                        key,
                    )
                )
        if outcome == "revise_current" and (approved is not None or not correction_passes):
            findings.append(
                Finding(
                    "error",
                    "REPLACEMENT_CORRECTION_NOT_APPROVED",
                    str(replacement_path),
                    "Revise-current requires a passing corrected_current and no replacement.",
                    key,
                )
            )
        if outcome == "remove_slot" and key in implemented_exercises:
            findings.append(
                Finding(
                    "error",
                    "REPLACEMENT_REMOVED_SLOT_STILL_ACTIVE",
                    str(replacement_path),
                    "A removed slot is still present in the active session spec.",
                    key,
                )
            )
        if outcome in {"remove_slot", "unresolved"} and (
            approved is not None or passing_names or correction_passes
        ):
            findings.append(
                Finding(
                    "error",
                    "REPLACEMENT_TERMINAL_OUTCOME_INVALID",
                    str(replacement_path),
                    f"Outcome '{outcome}' is only valid when no option passes every gate.",
                    key,
                )
            )

    recorded_summary = replacement.get("summary", {})
    for outcome, calculated in outcome_counts.items():
        if recorded_summary.get(outcome, 0) != calculated:
            findings.append(
                Finding(
                    "error",
                    "REPLACEMENT_SUMMARY_MISMATCH",
                    str(replacement_path),
                    (
                        f"Outcome '{outcome}' summary records "
                        f"{recorded_summary.get(outcome, 0)}, calculated {calculated}."
                    ),
                )
            )
    if replacement.get("scope", {}).get("candidates") != candidate_total:
        findings.append(
            Finding(
                "error",
                "REPLACEMENT_CANDIDATE_TOTAL_MISMATCH",
                str(replacement_path),
                (
                    f"Scope records {replacement.get('scope', {}).get('candidates')} candidates, "
                    f"calculated {candidate_total}."
                ),
            )
        )
    return outcomes, outcome_counts


def validate_video_audit(
    spec: dict[str, Any],
    video_audit_path: Path,
    findings: list[Finding],
) -> dict[str, int]:
    """Validate one exact, public YouTube demonstration per active exercise."""
    empty = {
        "exercises": 0,
        "public": 0,
        "exact": 0,
        "retained": 0,
        "added": 0,
        "replaced": 0,
    }
    if not video_audit_path.exists():
        findings.append(
            Finding(
                "error",
                "VIDEO_AUDIT_MISSING",
                str(video_audit_path),
                "Video audit does not exist.",
            )
        )
        return empty

    audit = yaml.safe_load(video_audit_path.read_text(encoding="utf-8"))
    entries = audit.get("videos", [])
    expected = {
        f"{session_id}.{exercise['id']}": {
            "session": session_id,
            "guide": session["guide"],
            "exercise_id": exercise["id"],
            "title": exercise["title"],
        }
        for session_id, session in spec["sessions"].items()
        for exercise in session["exercises"]
    }
    actual_keys = [entry.get("key") for entry in entries]
    duplicates = sorted({key for key in actual_keys if actual_keys.count(key) > 1})
    if duplicates:
        findings.append(
            Finding(
                "error",
                "VIDEO_AUDIT_DUPLICATE",
                str(video_audit_path),
                f"Duplicate exercise keys: {', '.join(duplicates)}.",
            )
        )
    missing = sorted(set(expected) - set(actual_keys))
    extra = sorted(set(actual_keys) - set(expected))
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if extra:
            details.append(f"unexpected: {', '.join(extra)}")
        findings.append(
            Finding(
                "error",
                "VIDEO_AUDIT_INVENTORY_MISMATCH",
                str(video_audit_path),
                "; ".join(details) + ".",
            )
        )

    policy = spec.get("video_policy", {})
    required_count = policy.get("required_videos_per_exercise", 1)
    required_availability = policy.get("required_availability", "public")
    required_match = policy.get("required_movement_match", "exact")
    allowed_host = policy.get("allowed_host", "www.youtube.com")
    documents: dict[str, str] = {}
    action_counts = {action: 0 for action in VIDEO_ACTIONS}
    public_count = 0
    exact_count = 0

    for entry in entries:
        key = entry.get("key", "unknown")
        expected_entry = expected.get(key)
        if expected_entry:
            for field in ("session", "guide", "exercise_id", "title"):
                if entry.get(field) != expected_entry[field]:
                    findings.append(
                        Finding(
                            "error",
                            "VIDEO_AUDIT_IMPLEMENTATION_MISMATCH",
                            str(video_audit_path),
                            (
                                f"Field '{field}' records '{entry.get(field)}', "
                                f"spec records '{expected_entry[field]}'."
                            ),
                            key,
                        )
                    )

        youtube_id = entry.get("youtube_id")
        youtube_url = entry.get("youtube_url", "")
        if not isinstance(youtube_id, str) or not YOUTUBE_ID_PATTERN.fullmatch(youtube_id):
            findings.append(
                Finding(
                    "error",
                    "VIDEO_AUDIT_ID_INVALID",
                    str(video_audit_path),
                    f"Invalid YouTube ID: {youtube_id}.",
                    key,
                )
            )
            continue
        if allowed_host not in youtube_url or youtube_id_from_url(youtube_url) != youtube_id:
            findings.append(
                Finding(
                    "error",
                    "VIDEO_AUDIT_URL_MISMATCH",
                    str(video_audit_path),
                    "YouTube URL host or video ID does not match the audited ID.",
                    key,
                )
            )
        if entry.get("availability") == required_availability:
            public_count += 1
        else:
            findings.append(
                Finding(
                    "error",
                    "VIDEO_AUDIT_NOT_PUBLIC",
                    str(video_audit_path),
                    (
                        f"Availability must be '{required_availability}', "
                        f"found '{entry.get('availability')}'."
                    ),
                    key,
                )
            )
        if entry.get("movement_match") == required_match:
            exact_count += 1
        else:
            findings.append(
                Finding(
                    "error",
                    "VIDEO_AUDIT_MOVEMENT_MISMATCH",
                    str(video_audit_path),
                    (
                        f"Movement match must be '{required_match}', "
                        f"found '{entry.get('movement_match')}'."
                    ),
                    key,
                )
            )
        if not entry.get("verified_title") or not entry.get("channel"):
            findings.append(
                Finding(
                    "error",
                    "VIDEO_AUDIT_METADATA_MISSING",
                    str(video_audit_path),
                    "Verified title and channel are required.",
                    key,
                )
            )
        action = entry.get("action")
        if action not in VIDEO_ACTIONS:
            findings.append(
                Finding(
                    "error",
                    "VIDEO_AUDIT_ACTION_INVALID",
                    str(video_audit_path),
                    f"Invalid video action: {action}.",
                    key,
                )
            )
        else:
            action_counts[action] += 1

        if not expected_entry:
            continue
        rel_path = expected_entry["guide"]
        if rel_path not in documents:
            guide_path = ROOT / rel_path
            if not guide_path.exists():
                continue
            documents[rel_path] = guide_path.read_text(encoding="utf-8")
        section = section_for_id(documents[rel_path], expected_entry["exercise_id"])
        if section is None:
            continue
        hrefs = re.findall(
            r'href="([^"]*(?:youtube\.com/watch|youtu\.be/)[^"]*)"',
            section,
            flags=re.IGNORECASE,
        )
        implemented_ids = [
            video_id
            for value in hrefs
            if (video_id := youtube_id_from_url(value)) is not None
        ]
        if len(implemented_ids) != required_count:
            findings.append(
                Finding(
                    "error",
                    "VIDEO_AUDIT_CARD_COUNT_MISMATCH",
                    rel_path,
                    (
                        f"Expected {required_count} YouTube video link(s), "
                        f"found {len(implemented_ids)}."
                    ),
                    key,
                )
            )
        if implemented_ids != [youtube_id]:
            findings.append(
                Finding(
                    "error",
                    "VIDEO_AUDIT_IMPLEMENTATION_MISMATCH",
                    rel_path,
                    (
                        f"Audited video ID is {youtube_id}; "
                        f"card links {implemented_ids or 'none'}."
                    ),
                    key,
                )
            )
        if policy.get("require_matching_thumbnail_id", True):
            thumbnail_ids = re.findall(
                r"img\.youtube\.com/vi/([A-Za-z0-9_-]{11})/",
                section,
                flags=re.IGNORECASE,
            )
            if youtube_id not in thumbnail_ids:
                findings.append(
                    Finding(
                        "error",
                        "VIDEO_AUDIT_THUMBNAIL_MISMATCH",
                        rel_path,
                        "Card thumbnail does not use the audited YouTube ID.",
                        key,
                    )
                )
        if policy.get("require_video_label", True) and 'class="video-label"' not in section:
            findings.append(
                Finding(
                    "error",
                    "VIDEO_AUDIT_LABEL_MISSING",
                    rel_path,
                    "Card does not include a video label.",
                    key,
                )
            )

    calculated_summary = {
        "linked_videos": len(entries),
        "public_videos": public_count,
        "exact_movement_matches": exact_count,
        "retained": action_counts["retained"],
        "added": action_counts["added"],
        "replaced": action_counts["replaced"],
        "unavailable": len(entries) - public_count,
        "mismatched": len(entries) - exact_count,
    }
    recorded_summary = audit.get("summary", {})
    for field, value in calculated_summary.items():
        if recorded_summary.get(field) != value:
            findings.append(
                Finding(
                    "error",
                    "VIDEO_AUDIT_SUMMARY_MISMATCH",
                    str(video_audit_path),
                    (
                        f"Summary '{field}' records {recorded_summary.get(field)}, "
                        f"calculated {value}."
                    ),
                )
            )
    if audit.get("scope", {}).get("active_exercises") != len(entries):
        findings.append(
            Finding(
                "error",
                "VIDEO_AUDIT_SCOPE_MISMATCH",
                str(video_audit_path),
                (
                    f"Scope records {audit.get('scope', {}).get('active_exercises')} "
                    f"active exercises, calculated {len(entries)}."
                ),
            )
        )

    return {
        "exercises": len(entries),
        "public": public_count,
        "exact": exact_count,
        **action_counts,
    }


def validate_final_audit(
    spec: dict[str, Any],
    source_audit_path: Path,
    final_audit_path: Path,
    findings: list[Finding],
) -> dict[str, Any]:
    """Validate the post-change rescore against the current spec and HTML."""
    empty = {
        "exercises": 0,
        "at_or_above_80": 0,
        "below_80": 0,
        "score_mean": 0.0,
        "removed_after_rescore": 0,
    }
    if not final_audit_path.exists():
        findings.append(
            Finding(
                "error",
                "FINAL_AUDIT_MISSING",
                str(final_audit_path),
                "Final post-change audit does not exist.",
            )
        )
        return empty

    final_audit = yaml.safe_load(final_audit_path.read_text(encoding="utf-8"))
    source_audit = yaml.safe_load(source_audit_path.read_text(encoding="utf-8"))
    entries = final_audit.get("exercises", [])
    removals = final_audit.get("removals", [])
    expected = {
        f"{session_id}.{exercise['id']}": {
            "session": session_id,
            "title": exercise["title"],
            "slot": exercise["slot"],
            "evidence": exercise["page_declared_evidence"],
        }
        for session_id, session in spec["sessions"].items()
        for exercise in session["exercises"]
    }
    actual_keys = [entry.get("key") for entry in entries]
    duplicates = sorted({key for key in actual_keys if actual_keys.count(key) > 1})
    if duplicates:
        findings.append(
            Finding(
                "error",
                "FINAL_AUDIT_DUPLICATE",
                str(final_audit_path),
                f"Duplicate exercise keys: {', '.join(duplicates)}.",
            )
        )
    missing = sorted(set(expected) - set(actual_keys))
    extra = sorted(set(actual_keys) - set(expected))
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if extra:
            details.append(f"unexpected: {', '.join(extra)}")
        findings.append(
            Finding(
                "error",
                "FINAL_AUDIT_INVENTORY_MISMATCH",
                str(final_audit_path),
                "; ".join(details) + ".",
            )
        )

    source_audit_keys = {
        entry.get("key") for entry in source_audit.get("exercises", [])
    }
    removal_keys = [removal.get("key") for removal in removals]
    removal_duplicates = sorted(
        {key for key in removal_keys if removal_keys.count(key) > 1}
    )
    if removal_duplicates:
        findings.append(
            Finding(
                "error",
                "FINAL_AUDIT_REMOVAL_DUPLICATE",
                str(final_audit_path),
                f"Duplicate removal keys: {', '.join(removal_duplicates)}.",
            )
        )
    for removal in removals:
        key = removal.get("key", "unknown")
        if key in expected:
            findings.append(
                Finding(
                    "error",
                    "FINAL_AUDIT_REMOVED_SLOT_STILL_ACTIVE",
                    str(final_audit_path),
                    "A post-rescore removal is still present in the active spec.",
                    key,
                )
            )
        if key not in source_audit_keys:
            findings.append(
                Finding(
                    "error",
                    "FINAL_AUDIT_REMOVAL_UNKNOWN",
                    str(final_audit_path),
                    "A post-rescore removal is not present in the initial source audit.",
                    key,
                )
            )
        if removal.get("outcome") != "remove_slot":
            findings.append(
                Finding(
                    "error",
                    "FINAL_AUDIT_REMOVAL_OUTCOME_INVALID",
                    str(final_audit_path),
                    f"Removal outcome must be 'remove_slot', found '{removal.get('outcome')}'.",
                    key,
                )
            )

    weights = spec.get("scoring", {}).get("weights", {})
    known_sources = set(source_audit.get("sources", {}))
    known_hard_failures = set(spec.get("scoring", {}).get("hard_failures", []))
    retain_threshold = spec.get("scoring", {}).get("thresholds", {}).get("retain", 80)
    revise_threshold = spec.get("scoring", {}).get("thresholds", {}).get("revise", 70)
    totals: list[int] = []
    disposition_counts = {"retain": 0, "revise": 0, "replace": 0, "remove": 0}
    session_values: dict[str, list[int]] = {
        session_id: [] for session_id in spec["sessions"]
    }

    for entry in entries:
        key = entry.get("key", "unknown")
        exercise_id = key
        expected_entry = expected.get(key)
        if expected_entry:
            for field in ("session", "title", "slot", "evidence"):
                if entry.get(field) != expected_entry[field]:
                    findings.append(
                        Finding(
                            "error",
                            "FINAL_AUDIT_IMPLEMENTATION_MISMATCH",
                            str(final_audit_path),
                            (
                                f"Field '{field}' records '{entry.get(field)}', "
                                f"spec records '{expected_entry[field]}'."
                            ),
                            exercise_id,
                        )
                    )

        score = entry.get("score", {})
        calculated_total = sum(score.get(dimension, 0) for dimension in SCORE_DIMENSIONS)
        recorded_total = score.get("total")
        if calculated_total != recorded_total:
            findings.append(
                Finding(
                    "error",
                    "FINAL_AUDIT_SCORE_MISMATCH",
                    str(final_audit_path),
                    f"Components total {calculated_total}, recorded {recorded_total}.",
                    exercise_id,
                )
            )
        for dimension in SCORE_DIMENSIONS:
            value = score.get(dimension)
            maximum = weights.get(dimension)
            if not isinstance(value, int) or maximum is None or not 0 <= value <= maximum:
                findings.append(
                    Finding(
                        "error",
                        "FINAL_AUDIT_SCORE_RANGE",
                        str(final_audit_path),
                        (
                            f"Dimension '{dimension}' records {value}; "
                            f"expected an integer from 0 to {maximum}."
                        ),
                        exercise_id,
                    )
                )
        if isinstance(recorded_total, int):
            totals.append(recorded_total)
            session = entry.get("session")
            if session in session_values:
                session_values[session].append(recorded_total)

        unknown_sources = sorted(set(entry.get("source_keys", [])) - known_sources)
        if unknown_sources:
            findings.append(
                Finding(
                    "error",
                    "FINAL_AUDIT_SOURCE_UNKNOWN",
                    str(final_audit_path),
                    f"Unknown source keys: {', '.join(unknown_sources)}.",
                    exercise_id,
                )
            )
        unknown_failures = sorted(set(entry.get("hard_failures", [])) - known_hard_failures)
        if unknown_failures:
            findings.append(
                Finding(
                    "error",
                    "FINAL_AUDIT_HARD_FAILURE_UNKNOWN",
                    str(final_audit_path),
                    f"Unknown hard failures: {', '.join(unknown_failures)}.",
                    exercise_id,
                )
            )

        disposition = entry.get("disposition")
        if disposition in disposition_counts:
            disposition_counts[disposition] += 1
        else:
            findings.append(
                Finding(
                    "error",
                    "FINAL_AUDIT_DISPOSITION_INVALID",
                    str(final_audit_path),
                    f"Invalid disposition: {disposition}.",
                    exercise_id,
                )
            )
        hard_failures = entry.get("hard_failures", [])
        if hard_failures and disposition == "retain":
            findings.append(
                Finding(
                    "error",
                    "FINAL_AUDIT_HARD_FAILURE_RETAINED",
                    str(final_audit_path),
                    "An exercise with a hard failure cannot be retained.",
                    exercise_id,
                )
            )
        elif not hard_failures and isinstance(recorded_total, int):
            expected_disposition = (
                "retain"
                if recorded_total >= retain_threshold
                else "revise"
                if recorded_total >= revise_threshold
                else "replace"
            )
            if disposition != expected_disposition:
                findings.append(
                    Finding(
                        "error",
                        "FINAL_AUDIT_DISPOSITION_MISMATCH",
                        str(final_audit_path),
                        (
                            f"Score {recorded_total} requires '{expected_disposition}', "
                            f"found '{disposition}'."
                        ),
                        exercise_id,
                    )
                )

    hashes = final_audit.get("basis", {}).get("guide_sha256", {})
    expected_guides = {session["guide"] for session in spec["sessions"].values()}
    if set(hashes) != expected_guides:
        findings.append(
            Finding(
                "error",
                "FINAL_AUDIT_GUIDE_HASH_INVENTORY",
                str(final_audit_path),
                "Guide hash inventory does not match the active session guides.",
            )
        )
    for rel_path, recorded_hash in hashes.items():
        path = ROOT / rel_path
        if not path.exists():
            continue
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != recorded_hash:
            findings.append(
                Finding(
                    "error",
                    "FINAL_AUDIT_GUIDE_CHANGED",
                    rel_path,
                    (
                        f"Current HTML hash {actual_hash} does not match final audit "
                        f"hash {recorded_hash}; rescore the changed guide."
                    ),
                )
            )

    calculated_summary = {
        "score_mean": round(sum(totals) / len(totals), 1) if totals else 0.0,
        "minimum_score": min(totals) if totals else 0,
        "maximum_score": max(totals) if totals else 0,
        "at_or_above_80": sum(total >= retain_threshold for total in totals),
        "below_80": sum(total < retain_threshold for total in totals),
        "hard_failures": sum(bool(entry.get("hard_failures", [])) for entry in entries),
        "removed_after_rescore": len(removals),
    }
    recorded_summary = final_audit.get("summary", {})
    if final_audit.get("scope", {}).get("active_exercises") != len(entries):
        findings.append(
            Finding(
                "error",
                "FINAL_AUDIT_SCOPE_MISMATCH",
                str(final_audit_path),
                (
                    f"Scope records {final_audit.get('scope', {}).get('active_exercises')} "
                    f"active exercises, calculated {len(entries)}."
                ),
            )
        )
    for field, value in calculated_summary.items():
        if recorded_summary.get(field) != value:
            findings.append(
                Finding(
                    "error",
                    "FINAL_AUDIT_SUMMARY_MISMATCH",
                    str(final_audit_path),
                    (
                        f"Summary '{field}' records {recorded_summary.get(field)}, "
                        f"calculated {value}."
                    ),
                )
            )
    if recorded_summary.get("dispositions", {}) != disposition_counts:
        findings.append(
            Finding(
                "error",
                "FINAL_AUDIT_SUMMARY_MISMATCH",
                str(final_audit_path),
                (
                    f"Disposition summary records "
                    f"{recorded_summary.get('dispositions', {})}, "
                    f"calculated {disposition_counts}."
                ),
            )
        )

    recorded_sessions = final_audit.get("session_summary", {})
    for session_id, values in session_values.items():
        calculated = {
            "exercises": len(values),
            "score_mean": round(sum(values) / len(values), 1) if values else 0.0,
            "below_80": sum(total < retain_threshold for total in values),
        }
        if recorded_sessions.get(session_id) != calculated:
            findings.append(
                Finding(
                    "error",
                    "FINAL_AUDIT_SESSION_SUMMARY_MISMATCH",
                    str(final_audit_path),
                    (
                        f"Session '{session_id}' records "
                        f"{recorded_sessions.get(session_id)}, calculated {calculated}."
                    ),
                )
            )

    return {
        "exercises": len(entries),
        "at_or_above_80": calculated_summary["at_or_above_80"],
        "below_80": calculated_summary["below_80"],
        "score_mean": calculated_summary["score_mean"],
        "removed_after_rescore": calculated_summary["removed_after_rescore"],
    }


def validate_guides(
    spec_path: Path,
    audit_path: Path | None = None,
    replacement_path: Path | None = None,
    final_audit_path: Path | None = None,
    video_audit_path: Path | None = None,
) -> tuple[dict[str, Any], list[Finding]]:
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    findings: list[Finding] = []
    totals = {"sessions": 0, "exercises": 0, "reference_links": 0}

    for session_id, session in spec["sessions"].items():
        totals["sessions"] += 1
        rel_path = session["guide"]
        root_candidate = ROOT / rel_path
        spec_candidate = spec_path.parent / rel_path
        path = root_candidate if root_candidate.exists() else spec_candidate
        if not path.exists():
            findings.append(Finding("error", "GUIDE_MISSING", rel_path, "Guide file does not exist."))
            continue

        document = path.read_text(encoding="utf-8")
        reference_ids = set(re.findall(r'\bid="(ref-\d+)"', document))
        reference_links = re.findall(r'href="#(ref-\d+)"', document)
        totals["reference_links"] += len(reference_links)
        for ref_id in sorted(set(reference_links) - reference_ids):
            findings.append(
                Finding(
                    "error",
                    "REFERENCE_TARGET_MISSING",
                    rel_path,
                    f"Inline reference target does not exist: {ref_id}.",
                )
            )

        expected_exercises = session["exercises"]
        totals["exercises"] += len(expected_exercises)
        actual_ids = re.findall(
            r'<section\b[^>]*class="section fade-in"[^>]*\bid="(ex\d+)"',
            document,
            flags=re.IGNORECASE,
        )
        expected_ids = [exercise["id"] for exercise in expected_exercises]
        if actual_ids != expected_ids:
            findings.append(
                Finding(
                    "error",
                    "EXERCISE_ORDER_MISMATCH",
                    rel_path,
                    f"Expected exercise order {expected_ids}; found {actual_ids}.",
                )
            )

        for exercise in expected_exercises:
            section = section_for_id(document, exercise["id"])
            if section is None:
                findings.append(
                    Finding(
                        "error",
                        "EXERCISE_SECTION_MISSING",
                        rel_path,
                        "Expected exercise section does not exist.",
                        exercise["id"],
                    )
                )
                continue
            validate_card(
                findings,
                rel_path,
                section,
                exercise,
                spec.get("evidence_policy", DEFAULT_EVIDENCE_POLICY),
                spec.get("video_policy"),
            )

    disclaimer_policy = spec.get("source_of_truth", {}).get("disclaimer_policy")
    if disclaimer_policy == "index_only":
        index_path = ROOT / "index.html"
        index_text = index_path.read_text(encoding="utf-8")
        if "개별 운동의 클라이밍 특화 효과" not in index_text:
            findings.append(
                Finding("error", "DISCLAIMER_MISSING", "index.html", "Index disclaimer is missing.")
            )

    for check in spec.get("documentation_drift_checks", []):
        path = ROOT / check["document"]
        text = path.read_text(encoding="utf-8")
        stale_found = [term for term in check.get("stale_terms", []) if term in text]
        missing_found = [term for term in check.get("missing_current_terms", []) if term not in text]
        if stale_found or missing_found:
            details = []
            if stale_found:
                details.append(f"stale terms present: {', '.join(stale_found)}")
            if missing_found:
                details.append(f"current terms absent: {', '.join(missing_found)}")
            findings.append(
                Finding(
                    "warning",
                    "DOCUMENTATION_DRIFT",
                    check["document"],
                    f"{check['section']}: {'; '.join(details)}.",
                )
            )

    audit_exercises = 0
    replacement_outcomes: dict[str, str] = {}
    replacement_counts: dict[str, int] = {}
    final_counts = {
        "exercises": 0,
        "at_or_above_80": 0,
        "below_80": 0,
        "score_mean": 0.0,
        "removed_after_rescore": 0,
    }
    video_counts = {
        "exercises": 0,
        "public": 0,
        "exact": 0,
        "retained": 0,
        "added": 0,
        "replaced": 0,
    }
    if audit_path is not None:
        if replacement_path is None:
            default_replacement = audit_path.with_name("replacement-audit.yaml")
            replacement_path = default_replacement if default_replacement.exists() else None
        if replacement_path is not None:
            replacement_outcomes, replacement_counts = validate_replacement_audit(
                spec,
                audit_path,
                replacement_path,
                findings,
            )
        if final_audit_path is None:
            default_final = audit_path.with_name("final-audit.yaml")
            final_audit_path = default_final if default_final.exists() else None
        if video_audit_path is None:
            default_video = audit_path.with_name("video-audit.yaml")
            video_audit_path = default_video if default_video.exists() else None
        final_removal_keys: set[str] = set()
        if final_audit_path is not None and final_audit_path.exists():
            final_data = yaml.safe_load(final_audit_path.read_text(encoding="utf-8"))
            final_removal_keys = {
                removal.get("key")
                for removal in final_data.get("removals", [])
                if removal.get("key")
            }
        audit_exercises = validate_source_audit(
            spec,
            audit_path,
            findings,
            replacement_outcomes,
            final_removal_keys,
        )
        if video_audit_path is not None:
            video_counts = validate_video_audit(
                spec,
                video_audit_path,
                findings,
            )
        if final_audit_path is not None:
            final_counts = validate_final_audit(
                spec,
                audit_path,
                final_audit_path,
                findings,
            )

    summary = {
        **totals,
        "audit_exercises": audit_exercises,
        "replacement_slots": len(replacement_outcomes),
        "verified_replacements": replacement_counts.get("verified_replacement", 0),
        "revised_currents": replacement_counts.get("revise_current", 0),
        "removed_slots": replacement_counts.get("remove_slot", 0),
        "final_audit_exercises": final_counts["exercises"],
        "final_at_or_above_80": final_counts["at_or_above_80"],
        "final_below_80": final_counts["below_80"],
        "final_score_mean": final_counts["score_mean"],
        "final_removed_after_rescore": final_counts["removed_after_rescore"],
        "video_audit_exercises": video_counts["exercises"],
        "public_videos": video_counts["public"],
        "exact_video_matches": video_counts["exact"],
        "retained_videos": video_counts["retained"],
        "added_videos": video_counts["added"],
        "replaced_videos": video_counts["replaced"],
        "errors": sum(item.severity == "error" for item in findings),
        "warnings": sum(item.severity == "warning" for item in findings),
        "status": "fail" if any(item.severity == "error" for item in findings) else "pass_with_warnings"
        if findings
        else "pass",
    }
    return summary, findings


def to_markdown(summary: dict[str, Any], findings: list[Finding]) -> str:
    lines = [
        "# Workout guide structural validation",
        "",
        f"- Status: **{summary['status']}**",
        f"- Sessions: {summary['sessions']}",
        f"- Exercises: {summary['exercises']}",
        f"- Audited exercises: {summary['audit_exercises']}",
        f"- Replacement-gated slots: {summary['replacement_slots']}",
        f"- Verified replacements: {summary['verified_replacements']}",
        f"- Revised current exercises: {summary['revised_currents']}",
        f"- Removed slots: {summary['removed_slots']}",
        f"- Final rescored exercises: {summary['final_audit_exercises']}",
        f"- Final scores at or above 80: {summary['final_at_or_above_80']}",
        f"- Final scores below 80: {summary['final_below_80']}",
        f"- Final score mean: {summary['final_score_mean']}",
        f"- Removed after final rescore: {summary['final_removed_after_rescore']}",
        f"- Video-audited exercises: {summary['video_audit_exercises']}",
        f"- Public videos: {summary['public_videos']}",
        f"- Exact movement video matches: {summary['exact_video_matches']}",
        f"- Retained videos: {summary['retained_videos']}",
        f"- Added videos: {summary['added_videos']}",
        f"- Replaced videos: {summary['replaced_videos']}",
        f"- Inline reference links checked: {summary['reference_links']}",
        f"- Errors: {summary['errors']}",
        f"- Warnings: {summary['warnings']}",
        "",
        "## Findings",
        "",
    ]
    if not findings:
        lines.append("No findings.")
    else:
        for item in findings:
            target = f" ({item.exercise_id})" if item.exercise_id else ""
            lines.append(
                f"- **{item.severity.upper()} · {item.code}** `{item.path}`{target}: {item.message}"
            )
    lines.append("")
    return "\n".join(lines)


def workspace_output_path(value: str) -> Path:
    """Resolve an output path and reject writes outside the repository."""
    output = (ROOT / value).resolve()
    try:
        output.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"Output must stay inside the repository: {value}") from exc
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", default="validation/spec.yaml")
    parser.add_argument("--audit", default="validation/source-audit.yaml")
    parser.add_argument("--replacement-audit", default="validation/replacement-audit.yaml")
    parser.add_argument("--final-audit", default="validation/final-audit.yaml")
    parser.add_argument("--video-audit", default="validation/video-audit.yaml")
    parser.add_argument("--skip-audit", action="store_true")
    parser.add_argument("--json-output")
    parser.add_argument("--markdown-output")
    parser.add_argument("--no-fail", action="store_true")
    args = parser.parse_args()

    spec_path = (ROOT / args.spec).resolve()
    audit_path = None if args.skip_audit else (ROOT / args.audit).resolve()
    replacement_path = (
        None if args.skip_audit else (ROOT / args.replacement_audit).resolve()
    )
    final_audit_path = None if args.skip_audit else (ROOT / args.final_audit).resolve()
    video_audit_path = None if args.skip_audit else (ROOT / args.video_audit).resolve()
    summary, findings = validate_guides(
        spec_path,
        audit_path,
        replacement_path,
        final_audit_path,
        video_audit_path,
    )
    payload = {"summary": summary, "findings": [asdict(item) for item in findings]}

    try:
        if args.json_output:
            output = workspace_output_path(args.json_output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        if args.markdown_output:
            output = workspace_output_path(args.markdown_output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(to_markdown(summary, findings), encoding="utf-8")
    except ValueError as exc:
        parser.error(str(exc))

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.no_fail:
        return 0
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
