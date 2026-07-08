"""STAGE 3 — classifier over the weakness-validity dataset, via Claude Agent SDK.

For each dataset row the classifier is given:
  - the FILE PATH to the paper's full text (datasets/iclr2026_new/papers/<id>.txt); it reads the file
    itself with the Read tool (we pass a path, not the text, to avoid the SDK content-size limit).
  - the reviewer weakness item text.
It must predict VALID vs INVALID from the paper + weakness ALONE (it never sees the AC meta-review).
Ground truth is the AC-derived label from stage 2.

Concurrency: 2 (asyncio semaphore). Model: claude-sonnet-5.
Resumable: each prediction is written to meta/weakness_validity_out/stage3/<row_idx>.json; existing rows skipped.
After all rows, prints accuracy / precision / recall / F1 (per class + macro) and the confusion matrix.
Run: python meta/weakness_classify.py
"""
import asyncio
import json
import re
from pathlib import Path

from datasets import load_from_disk
from sklearn.metrics import classification_report, confusion_matrix

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
)

ROOT = Path(__file__).resolve().parent.parent
DS_PATH = Path(__file__).parent / "weakness_validity_out" / "dataset"
PAPERS = ROOT / "datasets" / "iclr2026_new" / "papers"
OUT = Path(__file__).parent / "weakness_validity_out" / "stage3_readonly"
OUT.mkdir(parents=True, exist_ok=True)

MODEL = "claude-sonnet-5"
CONCURRENCY = 2
MAX_TURNS = 8
# Read-only: the classifier may only read the paper file it is handed. Block every other general
# tool so it cannot Grep/Bash/Web its way around instead of reading the paper.
BLOCK = [
    "Task", "AskUserQuestion", "Bash", "CronCreate", "CronDelete", "CronList", "Edit",
    "EnterPlanMode", "EnterWorktree", "ExitPlanMode", "ExitWorktree", "Glob", "Grep", "Monitor",
    "NotebookEdit", "PushNotification", "RemoteTrigger", "ScheduleWakeup", "Skill", "TaskOutput",
    "TaskStop", "TodoWrite", "ToolSearch", "WebFetch", "WebSearch", "Write",
]

PROMPT = """You are judging whether a single reviewer weakness raised against a submitted paper is a VALID or INVALID concern.

Definitions:
- VALID: a genuine, blocking weakness. Satisfying it requires actually revising the paper (new experiments, added results, corrections, restructuring). The concern stands after considering the paper.
- INVALID: a non-blocking concern. It can be settled by clarification or argument WITHOUT editing the paper (e.g. the reviewer misunderstood something, the point is already addressed in the paper, or it is a debatable preference), so it should not block acceptance.

The full text of the paper is in the file: {paper_path}
Read that file, then judge the weakness below against the paper.

REVIEWER WEAKNESS:
{weakness}

Respond with ONLY a JSON object on a single line, no prose, no code fence:
{{"label": "valid"}} or {{"label": "invalid"}}
"""


async def classify(idx, row):
    out_path = OUT / f"{idx}.json"
    if out_path.exists():
        return

    paper_path = PAPERS / f"{row['paper_id']}.txt"
    prompt = PROMPT.format(paper_path=str(paper_path), weakness=row["review_item"])

    opts = ClaudeAgentOptions(
        model=MODEL,
        allowed_tools=["Read"],
        disallowed_tools=BLOCK,
        permission_mode="bypassPermissions",
        max_turns=MAX_TURNS,
        cwd=str(ROOT),
    )
    text = ""
    async with ClaudeSDKClient(options=opts) as sdk:
        await sdk.query(prompt)
        async for m in sdk.receive_response():
            if isinstance(m, AssistantMessage):
                for b in m.content:
                    if isinstance(b, TextBlock):
                        text += b.text

    match = re.search(r"\{[^{}]*\"label\"[^{}]*\}", text)
    pred = json.loads(match.group(0))["label"]
    if pred not in ("valid", "invalid"):
        raise ValueError(f"bad label {pred!r} for row {idx}")

    json.dump(
        {"idx": idx, "paper_id": row["paper_id"], "gold": row["label"], "pred": pred},
        open(out_path, "w"),
    )
    print(f"row {idx}: gold={row['label']} pred={pred}")


async def main():
    ds = load_from_disk(str(DS_PATH))
    sem = asyncio.Semaphore(CONCURRENCY)

    async def worker(idx, row):
        async with sem:
            await classify(idx, row)

    await asyncio.gather(*(worker(i, ds[i]) for i in range(len(ds))))

    gold, pred = [], []
    for i in range(len(ds)):
        r = json.load(open(OUT / f"{i}.json"))
        gold.append(r["gold"])
        pred.append(r["pred"])

    labels = ["valid", "invalid"]
    print("\n=== classification report ===")
    print(classification_report(gold, pred, labels=labels, digits=4))
    print("=== confusion matrix (rows=gold, cols=pred) order", labels, "===")
    print(confusion_matrix(gold, pred, labels=labels))


asyncio.run(main())
