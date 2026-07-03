"""ACTUAL-PIPELINE test for meta/cspaper_rebuttal_recall.py on ONE paper.
Real OpenReview fetch + real Claude Agent SDK calls (sonnet-5). Asserts the shape of
each stage's output and saves intermediates to meta/tests/pipeline_run_output.json.
Never touches meta/cspaper_rebuttal_recall_test.json.
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cspaper_rebuttal_recall as mod

PID = "pn2H6YeOv2"  # known accepted paper that previously passed all gates
OUT = Path(__file__).resolve().parent / "pipeline_run_output.json"


async def main():
    saved = {"pid": PID}

    # Stage 1: fetch_thread
    thread = mod.fetch_thread(PID)
    assert set(thread) == {"title", "reviews", "comments", "meta", "decision"}
    assert thread["title"], "no title"
    assert len(thread["reviews"]) > 0, "no reviews"
    for r in thread["reviews"]:
        assert set(r) == {"summary", "strengths", "weaknesses", "questions", "rating"}
    assert len(thread["comments"]) > 0 and all(set(c) == {"by", "text"} for c in thread["comments"])
    assert thread["meta"], "no meta-review"
    assert "accept" in thread["decision"].lower(), thread["decision"]
    saved["stage1_fetch_thread"] = {
        "title": thread["title"], "decision": thread["decision"],
        "n_reviews": len(thread["reviews"]), "n_comments": len(thread["comments"]),
        "meta_chars": len(thread["meta"]),
        "review_ratings": [r["rating"] for r in thread["reviews"]],
    }
    print("STAGE 1 fetch_thread:", json.dumps(saved["stage1_fetch_thread"], indent=2))

    # Stage 2: assemble
    text = mod.assemble(thread)
    for sect in ["=== OFFICIAL REVIEWS ===", "=== REBUTTAL / DISCUSSION COMMENTS ===", "=== AC META-REVIEW ==="]:
        assert sect in text
    saved["stage2_assembled_chars"] = len(text)
    print(f"STAGE 2 assemble: {len(text)} chars, all sections present")

    # Stage 3: AC extraction (real Claude call)
    ac = mod.extract_json(await mod.query_claude(mod.AC_PROMPT.format(thread=text)))
    assert set(ac) >= {"ac_discusses_resolution", "resolved_invalid", "unresolved"}, ac.keys()
    assert isinstance(ac["ac_discusses_resolution"], bool)
    assert isinstance(ac["resolved_invalid"], list) and isinstance(ac["unresolved"], list)
    for it in ac["resolved_invalid"] + ac["unresolved"]:
        assert set(it) >= {"issue", "ac_evidence"}, it
        assert it["ac_evidence"].strip(), f"empty ac_evidence for {it['issue']}"
    saved["stage3_ac"] = {
        "ac_discusses_resolution": ac["ac_discusses_resolution"],
        "n_resolved_invalid": len(ac["resolved_invalid"]),
        "n_unresolved": len(ac["unresolved"]),
        "resolved_issues": [it["issue"] for it in ac["resolved_invalid"]],
        "unresolved_issues": [it["issue"] for it in ac["unresolved"]],
    }
    print("STAGE 3 AC extraction:", json.dumps(saved["stage3_ac"], indent=2))
    assert ac["ac_discusses_resolution"], "gate failed on a paper that previously passed"
    assert ac["resolved_invalid"], "no resolved-invalid items"

    # Stage 4: recall (real Claude call, cspaper review only to limit cost)
    issues_txt = "\n".join(f"{i+1}. {it['issue']}" for i, it in enumerate(ac["resolved_invalid"]))
    csp_path = mod.CSPAPER_DIR / f"{PID}__ICLR_main_2026_2.md"
    n, matches = await mod.recall_for(csp_path.read_text(), issues_txt)
    assert isinstance(matches, list) and len(matches) == len(ac["resolved_invalid"])
    for m in matches:
        assert set(m) >= {"issue", "raised_by_cspaper", "cspaper_excerpt"}, m
        assert isinstance(m["raised_by_cspaper"], bool)
        if m["raised_by_cspaper"]:
            assert m["cspaper_excerpt"].strip(), f"raised but empty excerpt: {m['issue']}"
    assert n == sum(1 for m in matches if m["raised_by_cspaper"])
    saved["stage4_recall"] = {
        "n_issues": len(matches), "cspaper_recalled": n,
        "matches": [{"issue": m["issue"], "raised_by_cspaper": m["raised_by_cspaper"]} for m in matches],
    }
    print("STAGE 4 recall:", json.dumps(saved["stage4_recall"], indent=2))

    OUT.write_text(json.dumps(saved, indent=2))
    print(f"\nALL PIPELINE STAGES PASS — intermediates saved to {OUT}")


asyncio.run(main())
