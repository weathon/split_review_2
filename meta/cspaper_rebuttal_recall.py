"""TEST (few papers): for ACCEPTED ICLR-2026 papers, pull the OpenReview thread
(reviews + author rebuttal comments + AC meta-review), have Claude extract the set of
reviewer-raised issues that were RESOLVED in rebuttal (treat these as "invalid" — they
turned out not to block acceptance), then measure how many of those resolved issues
CSPaper's automated review also raised (recall).

Claude Agent SDK (not Workflow). Run: python meta/cspaper_rebuttal_recall.py
"""
import asyncio
import json
import os
import re
from pathlib import Path

import dotenv
import openreview

ROOT = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(ROOT / ".env")
CSPAPER_DIR = ROOT / "final_results" / "cspaper"
JUDGE_MODEL = "claude-sonnet-5"
N_PAPERS = 3

client = openreview.api.OpenReviewClient(
    username=os.environ["OPENREVIEW_USERNAME"],
    password=os.environ["OPENREVIEW_PASSWORD"],
    baseurl="https://api2.openreview.net",
)

CSP_RE = re.compile(r"^(.+)__ICLR_main_2026_2\.md$")


def cspaper_index():
    idx = {}
    for f in CSPAPER_DIR.iterdir():
        m = CSP_RE.match(f.name)
        if m:
            idx[m.group(1)] = f
    return idx


def field(content, key):
    v = content.get(key, "")
    return v.get("value", "") if isinstance(v, dict) else v


def fetch_thread(pid):
    notes = client.get_all_notes(forum=pid, details=None)
    reviews, comments, meta, decision, title = [], [], None, None, None
    for n in notes:
        invs = n.invitations or []
        tail = [i.split("/")[-1] for i in invs]
        c = n.content
        if "Submission" in tail or "Full_Submission" in tail:
            title = field(c, "title") or title
        if "Official_Review" in tail:
            reviews.append(
                {k: field(c, k) for k in ["summary", "strengths", "weaknesses", "questions", "rating"]}
            )
        elif "Official_Comment" in tail or "Rebuttal" in " ".join(tail):
            txt = field(c, "comment") or field(c, "rebuttal")
            sig = (n.signatures or [""])[0].split("/")[-1]
            if txt:
                comments.append({"by": sig, "text": txt})
        elif "Meta_Review" in tail:
            meta = field(c, "metareview") or field(c, "recommendation") or json.dumps(c)
        elif "Decision" in tail:
            decision = field(c, "decision")
    return {"title": title, "reviews": reviews, "comments": comments, "meta": meta, "decision": decision}


def assemble(thread):
    out = [f"TITLE: {thread['title']}", f"DECISION: {thread['decision']}", "", "=== OFFICIAL REVIEWS ==="]
    for i, r in enumerate(thread["reviews"], 1):
        out.append(f"\n--- Reviewer {i} (rating: {r.get('rating','')}) ---")
        for k in ["summary", "strengths", "weaknesses", "questions"]:
            if r.get(k):
                out.append(f"[{k}] {r[k]}")
    out.append("\n=== REBUTTAL / DISCUSSION COMMENTS ===")
    for cm in thread["comments"]:
        out.append(f"\n--- {cm['by']} ---\n{cm['text']}")
    out.append("\n=== AC META-REVIEW ===")
    out.append(thread["meta"] or "(none)")
    return "\n".join(out)


async def query_claude(prompt):
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

    opts = ClaudeAgentOptions(
        model=JUDGE_MODEL,
        allowed_tools=[],
        permission_mode="bypassPermissions",
        disallowed_tools=["Read", "Glob", "Grep", "Bash", "Edit", "Write", "WebSearch", "WebFetch"],
        max_turns=1,
        cwd="/tmp",
    )
    text = ""
    async with ClaudeSDKClient(options=opts) as sdk:
        await sdk.query(prompt)
        async for m in sdk.receive_response():
            if isinstance(m, AssistantMessage):
                for b in m.content:
                    if isinstance(b, TextBlock):
                        text += b.text
    return text


def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return json.loads(text)


AC_PROMPT = """You are analyzing the OpenReview discussion of an ICLR paper that was ACCEPTED. The paper PDF under review is the POST-rebuttal version, and the AC meta-review below assesses THAT version.

{thread}

Follow these rules EXACTLY. Do NOT use your own judgement about whether the rebuttal resolved a concern. Decide ONLY from the AC meta-review's explicit statements.

Step 1 — gate. Does the AC meta-review explicitly discuss resolution status of reviewer concerns? That means it EITHER (a) explicitly states that certain concerns were resolved/addressed by the rebuttal, AND/OR (b) lists the remaining / still-open / unresolved concerns (or the concerns motivating its assessment). If the AC meta-review does NEITHER, set "ac_discusses_resolution": false and return empty lists — the paper will be skipped.

Step 2 — reviewer issues. Extract the SUBSTANTIVE issues reviewers raised (in reviews and discussion). EXCLUDE trivial items entirely: typos, grammar, wording, formatting, notation, missing citations, presentation/clarity nits.

Step 3 — classify each substantive issue using ONLY the AC meta-review:
- "resolved"  ONLY IF: the AC explicitly says that concern was resolved/addressed, OR the AC gave a list of remaining/unresolved concerns and this issue is NOT in that list.
- "unresolved" if the AC lists it among remaining/open concerns.
- "unknown"   if the AC statements do not let you decide by the two rules above.
For every "resolved" and "unresolved" item, quote the exact AC sentence you relied on in "ac_evidence".

Return ONLY JSON, no prose, no code fences:
{{"ac_discusses_resolution": true/false, "resolved_invalid": [{{"issue": "<short desc>", "ac_evidence": "<exact AC quote>"}}], "unresolved": [{{"issue": "<short desc>", "ac_evidence": "<exact AC quote>"}}]}}"""

RECALL_PROMPT = """Below is an automated reviewer's ("CSPaper") review of a paper, followed by a list of issues that HUMAN reviewers raised about the same paper but which were RESOLVED in rebuttal (i.e., they turned out not to block acceptance).

=== CSPAPER REVIEW ===
{review}

=== RESOLVED (NON-BLOCKING) ISSUES ===
{issues}

For each resolved issue, decide whether the CSPaper review ALSO raises essentially the same issue (same specific concern about the same aspect of the paper). Be strict: same specific point, not merely same topic.

Return ONLY JSON, no prose, no code fences:
{{"matches": [{{"issue": "<the resolved issue>", "raised_by_cspaper": true/false, "cspaper_excerpt": "<short quote from CSPaper review if raised, else empty>"}}]}}"""


async def process(pid, path):
    thread = fetch_thread(pid)
    dec = (thread["decision"] or "").lower()
    if "accept" not in dec:
        return {"skip": "not accepted"}
    if not thread["meta"]:
        return {"skip": "no meta-review"}
    ac = extract_json(await query_claude(AC_PROMPT.format(thread=assemble(thread))))
    if not ac.get("ac_discusses_resolution"):
        return {"skip": "AC does not discuss resolution"}
    issues = ac["resolved_invalid"]
    if not issues:
        return {"skip": "AC discusses resolution but no resolved-invalid items"}
    review = path.read_text()
    issues_txt = "\n".join(f"{i+1}. {it['issue']}" for i, it in enumerate(issues))
    rec = extract_json(await query_claude(RECALL_PROMPT.format(review=review, issues=issues_txt)))
    matches = rec["matches"]
    n_rec = sum(1 for m in matches if m["raised_by_cspaper"])
    return {"pid": pid, "title": thread["title"], "decision": thread["decision"],
            "n_resolved": len(issues), "n_recalled": n_rec,
            "resolved_invalid": issues, "unresolved": ac.get("unresolved", []), "matches": matches}


async def main():
    idx = cspaper_index()
    results = []
    scanned = 0
    MAX_SCAN = 40
    for pid, path in idx.items():
        if len(results) >= N_PAPERS or scanned >= MAX_SCAN:
            break
        scanned += 1
        try:
            r = await process(pid, path)
        except Exception as e:
            print(f"  skip {pid}: {type(e).__name__}: {e}")
            continue
        if r.get("skip"):
            print(f"  skip {pid}: {r['skip']}")
            continue
        results.append(r)
        print(f"\n### {pid} — {r['title']}  [{r.get('decision')}]")
        print(f"resolved(invalid) issues: {r['n_resolved']} | recalled by CSPaper: {r['n_recalled']} "
              f"({100*r['n_recalled']/r['n_resolved']:.0f}%)" if r["n_resolved"] else "no resolved issues")
        for m in r["matches"]:
            mark = "RAISED" if m["raised_by_cspaper"] else "  -   "
            print(f"  [{mark}] {m['issue'][:110]}")

    out = ROOT / "meta" / "cspaper_rebuttal_recall_test.json"
    out.write_text(json.dumps(results, indent=2))
    tot_r = sum(r["n_resolved"] for r in results)
    tot_rec = sum(r["n_recalled"] for r in results)
    print(f"\n=== TOTAL over {len(results)} accepted papers ===")
    print(f"resolved(invalid) issues: {tot_r} | recalled by CSPaper: {tot_rec} "
          f"({100*tot_rec/tot_r:.0f}%)" if tot_r else "none")
    print(f"wrote {out}")


if __name__ == "__main__":
    asyncio.run(main())
