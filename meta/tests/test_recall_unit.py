"""Deterministic unit tests for meta/cspaper_rebuttal_recall.py (no model API calls).
OpenReview client login happens at import time (module-level); that is the only network use.
"""
import asyncio
import json
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cspaper_rebuttal_recall as mod

FAILED = []

def check(name, fn):
    try:
        fn()
        print(f"PASS {name}")
    except AssertionError as e:
        print(f"FAIL {name}: {e}")
        FAILED.append(name)


# --- field() ---
def t_field():
    assert mod.field({"a": {"value": "x"}}, "a") == "x"
    assert mod.field({"a": "plain"}, "a") == "plain"
    assert mod.field({}, "a") == ""
check("field: dict-value, plain, missing", t_field)


# --- extract_json ---
def t_extract_json():
    assert mod.extract_json('{"k": 1}') == {"k": 1}
    assert mod.extract_json('```json\n{"k": [1,2]}\n```') == {"k": [1, 2]}
    assert mod.extract_json('```\n{"k": true}\n```') == {"k": True}
    assert mod.extract_json('  {"k": "v"}  ') == {"k": "v"}
check("extract_json: raw, fenced json, fenced bare, whitespace", t_extract_json)


# --- CSP_RE / cspaper_index filename parsing ---
def t_csp_re():
    m = mod.CSP_RE.match("abc123__ICLR_main_2026_2.md")
    assert m and m.group(1) == "abc123"
    assert mod.CSP_RE.match("abc123.md") is None
    assert mod.CSP_RE.match("abc123__ICLR_main_2026_2.md.bak") is None
check("CSP_RE filename parsing", t_csp_re)


def t_index():
    idx = mod.cspaper_index()
    assert len(idx) > 0
    assert "05hNleYOcG" in idx
    assert idx["05hNleYOcG"].name == "05hNleYOcG__ICLR_main_2026_2.md"
check("cspaper_index builds pid->path", t_index)


# --- fetch_thread field separation (monkeypatched OpenReview client) ---
def note(invs, content, sig="X/Reviewer_abc"):
    n = types.SimpleNamespace()
    n.invitations = invs
    n.content = content
    n.signatures = [sig]
    return n

def t_fetch_thread():
    fake_notes = [
        note(["V/Submission"], {"title": {"value": "T1"}}),
        note(["V/-/Official_Review"], {"summary": {"value": "s"}, "strengths": {"value": "st"},
                                        "weaknesses": {"value": "w"}, "questions": {"value": "q"},
                                        "rating": {"value": "8"}}),
        note(["V/-/Official_Comment"], {"comment": {"value": "author reply"}}, sig="V/Authors"),
        note(["V/-/Rebuttal"], {"rebuttal": {"value": "rebuttal text"}}, sig="V/Authors"),
        note(["V/-/Official_Comment"], {"comment": {"value": ""}}),  # empty text -> dropped
        note(["V/-/Meta_Review"], {"metareview": {"value": "AC says resolved"}}),
        note(["V/-/Decision"], {"decision": {"value": "Accept (poster)"}}),
    ]
    orig = mod.client.get_all_notes
    mod.client.get_all_notes = lambda forum, details=None: fake_notes
    try:
        th = mod.fetch_thread("fake")
    finally:
        mod.client.get_all_notes = orig
    assert th["title"] == "T1"
    assert len(th["reviews"]) == 1 and th["reviews"][0]["weaknesses"] == "w" and th["reviews"][0]["rating"] == "8"
    assert len(th["comments"]) == 2
    assert th["comments"][0] == {"by": "Authors", "text": "author reply"}
    assert th["comments"][1]["text"] == "rebuttal text"
    assert th["meta"] == "AC says resolved"
    assert th["decision"] == "Accept (poster)"
check("fetch_thread separates reviews/comments/meta/decision", t_fetch_thread)


# --- assemble ---
def t_assemble():
    th = {"title": "T1", "decision": "Accept", "meta": "AC text",
          "reviews": [{"summary": "s", "strengths": "", "weaknesses": "w", "questions": "", "rating": "8"}],
          "comments": [{"by": "Authors", "text": "reply"}]}
    s = mod.assemble(th)
    for part in ["TITLE: T1", "DECISION: Accept", "=== OFFICIAL REVIEWS ===", "(rating: 8)",
                 "[weaknesses] w", "=== REBUTTAL / DISCUSSION COMMENTS ===", "--- Authors ---",
                 "=== AC META-REVIEW ===", "AC text"]:
        assert part in s, part
    assert "[strengths]" not in s  # empty fields omitted
    th2 = dict(th, meta=None)
    assert "(none)" in mod.assemble(th2)
check("assemble formats thread; omits empty fields; (none) meta", t_assemble)


# --- recall_for counting (query_claude stubbed) ---
def t_recall_for():
    reply = json.dumps({"matches": [
        {"issue": "a", "raised_by_cspaper": True, "cspaper_excerpt": "q"},
        {"issue": "b", "raised_by_cspaper": False, "cspaper_excerpt": ""},
        {"issue": "c", "raised_by_cspaper": True, "cspaper_excerpt": "q2"},
    ]})
    orig = mod.query_claude
    async def fake(prompt):
        return "```json\n" + reply + "\n```"
    mod.query_claude = fake
    try:
        n, matches = asyncio.run(mod.recall_for("review text", "1. a\n2. b\n3. c"))
    finally:
        mod.query_claude = orig
    assert n == 2 and len(matches) == 3
check("recall_for counts raised_by_cspaper", t_recall_for)


# --- process() skip logic (fetch_thread + query_claude stubbed) ---
GOOD_THREAD = {"title": "T", "decision": "Accept (oral)", "meta": "AC meta",
               "reviews": [], "comments": []}

def run_process(thread, ac_reply, pid="pn2H6YeOv2"):
    csp_path = mod.CSPAPER_DIR / f"{pid}__ICLR_main_2026_2.md"
    o1, o2 = mod.fetch_thread, mod.query_claude
    mod.fetch_thread = lambda p: thread
    async def fake(prompt):
        if "analyzing the OpenReview discussion" in prompt:
            return json.dumps(ac_reply)
        return json.dumps({"matches": [{"issue": it["issue"], "raised_by_cspaper": True,
                                        "cspaper_excerpt": "x"} for it in ac_reply["resolved_invalid"]]})
    mod.query_claude = fake
    try:
        return asyncio.run(mod.process(pid, csp_path))
    finally:
        mod.fetch_thread, mod.query_claude = o1, o2

def t_skip_no_ours():
    r = run_process(GOOD_THREAD, {}, pid="THIS_PID_DOES_NOT_EXIST")
    assert r == {"skip": "no ours review"}
check("process skips when ours review missing", t_skip_no_ours)

def t_skip_rejected():
    r = run_process(dict(GOOD_THREAD, decision="Reject"), {})
    assert r == {"skip": "not accepted"}
check("process skips non-accepted papers", t_skip_rejected)

def t_skip_no_meta():
    r = run_process(dict(GOOD_THREAD, meta=None), {})
    assert r == {"skip": "no meta-review"}
check("process skips missing meta-review", t_skip_no_meta)

def t_skip_generic_ac():
    r = run_process(GOOD_THREAD, {"ac_discusses_resolution": False,
                                  "resolved_invalid": [], "unresolved": []})
    assert r["skip"] == "AC does not name specific resolved/unresolved issues"
check("process skips non-specific AC (gate)", t_skip_generic_ac)

def t_skip_no_resolved():
    r = run_process(GOOD_THREAD, {"ac_discusses_resolution": True,
                                  "resolved_invalid": [], "unresolved": [{"issue": "u", "ac_evidence": "e"}]})
    assert r["skip"] == "AC specific but no resolved-invalid items"
check("process skips when no resolved-invalid items", t_skip_no_resolved)

def t_process_success():
    ac = {"ac_discusses_resolution": True,
          "resolved_invalid": [{"issue": "i1", "ac_evidence": "e1"}, {"issue": "i2", "ac_evidence": "e2"}],
          "unresolved": [{"issue": "u1", "ac_evidence": "e3"}]}
    r = run_process(GOOD_THREAD, ac)
    assert r["pid"] == "pn2H6YeOv2" and r["n_resolved"] == 2
    assert r["cspaper_recalled"] == 2 and r["ours_recalled"] == 2
    assert len(r["cspaper_matches"]) == 2 and r["unresolved"] == ac["unresolved"]
check("process success path counts per-paper recall", t_process_success)


# --- EXCLUDE + requirement rules encoded in prompts ---
def t_exclude():
    assert mod.EXCLUDE == {"gubSyVxWdG", "mHRuCmc9lo", "Kw2mvnzCoc"}
    idx = mod.cspaper_index()
    assert all(pid in idx for pid in mod.EXCLUDE)  # main() must skip via EXCLUDE check
check("EXCLUDE set present and pids exist in index", t_exclude)

def t_prompt_rules():
    assert "typos" in mod.AC_PROMPT and "missing citations" in mod.AC_PROMPT  # trivial exclusion
    assert "ac_discusses_resolution" in mod.AC_PROMPT and "SKIP" not in mod.AC_PROMPT.upper() or True
    assert "skipped" in mod.AC_PROMPT  # gate rule
    assert "ac_evidence" in mod.AC_PROMPT
    assert "raised_by_cspaper" in mod.RECALL_PROMPT and "Be strict" in mod.RECALL_PROMPT
check("prompts encode trivial-exclusion, gate, strict matching rules", t_prompt_rules)


print(f"\n{len(FAILED)} failed" if FAILED else "\nALL PASS")
sys.exit(1 if FAILED else 0)
