"""Generates per-method Workflow scripts that judge weakness reliability using Claude
subagents (Sonnet 5) instead of an OpenRouter-hosted judge model, for when the
OpenRouter account is out of credits. Each generated script embeds the guideline text
and the paper/review task list as JS literals -- passing them via Workflow's `args`
parameter was found to arrive as a raw JSON string, not a parsed object, in this
harness, so embedding as literals is the workaround.

Run this, then feed each output file to the Workflow tool via scriptPath.
"""
import json
import random
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
FINAL = REPO_ROOT / "final_results"
PAPER_DIR = REPO_ROOT / "datasets" / "iclr2026_new" / "papers"
GUIDELINE_PATH = Path(__file__).resolve().parent.parent / "outputs" / "weakness_reliability_guideline.md"
SUBSET_IDS_PATH = Path(__file__).resolve().parent.parent / "outputs" / "final_results_subset_ids.json"
OUT_DIR = Path(__file__).resolve().parent / "subagent_workflows"

SEED = 0
CONCURRENCY = 5  # per-workflow parallel agent() calls -- lowered from the harness
                 # default (~14) after that concurrency triggered heavy rate-limiting

METHODS = {
    "ours_cmp3_ours_v2": {"dir": FINAL / "ours_cmp3_ours_v2" / "reviews", "kind": "single_md"},
    "nocal_cmp3_nocal_v3": {"dir": FINAL / "nocal_cmp3_nocal_v3" / "reviews", "kind": "single_md"},
    "baseline_cmp3_baseline_v2": {"dir": FINAL / "baseline_cmp3_baseline_v2" / "reviews", "kind": "single_md"},
    "cspaper": {"dir": FINAL / "cspaper", "kind": "cspaper_md"},
    "DeepReviewer_14B": {"dir": FINAL / "DeepReviewer_14B", "kind": "deepreviewer_json"},
    "DeepReviewer-v2-openai": {"dir": FINAL / "DeepReviewer-v2-openai", "kind": "single_md"},
}

TEMPLATE = """export const meta = {{
  name: 'review-critics-subagent',
  description: 'Judge weakness reliability for one method using Claude subagents',
  phases: [{{ title: 'Judge' }}],
}}

const SCHEMA = {{
  type: 'object',
  properties: {{
    items: {{
      type: 'array',
      items: {{
        type: 'object',
        properties: {{
          weakness: {{ type: 'string' }},
          reliable: {{ type: 'integer', enum: [0, 1] }},
          error_type: {{ type: 'string' }},
          justification: {{ type: 'string' }},
        }},
        required: ['weakness', 'reliable', 'error_type', 'justification'],
      }},
    }},
  }},
  required: ['items'],
}}

const ERROR_TYPE_TABLE = `| Error Type | Explanation |
|---|---|
| Misunderstanding | The reviewer misinterprets claims or ideas presented in the paper, leading to inaccurate or irrelevant comments. |
| Neglect | The reviewer overlooks important details explicitly stated in the paper, resulting in unwarranted questions or critiques. |
| Vague Critique | The review lacks specificity, claiming missing components without clearly identifying what is missing. |
| Out-of-scope | The reviewer suggests additional methods, experiments, or analyses that are beyond the intended scope of the paper. |
| Invalid Criticism | The reviewer's criticism is considered invalid, especially when suggesting impractical experiments or trivializing results. |
| Superficial Review | The reviewer appears to have only skimmed the paper, providing generic or unsupported comments about the presence or absence of weaknesses. |
| Unstated statement | Statements made in the review are not supported by content in the paper. |
| Excessive demands | if the weaknesses are just asking for excessive things that are not necessary for a good paper. |
| Generic comment | weaknesses are just generic comments that can apply to any paper, without really pointing out the specific problems of the paper. |`

const METHOD = {method_json}
const GUIDELINE = {guideline_json}
const TASKS = {tasks_json}

log(`Judging ${{TASKS.length}} papers for method=${{METHOD}}`)

function buildPrompt(t) {{
  return `You are an expert NLP/ML conference meta-reviewer. Extract each weakness claim in a review and judge whether it is reliable, USING THE PAPER TEXT as ground truth.

Error type table:
${{ERROR_TYPE_TABLE}}

Weakness reliability guideline (error type table + human-annotated examples):
${{GUIDELINE}}

Paper id: ${{t.paper_id}}

First, use the Read tool to read the full paper text at: ${{t.paper_path}}
Then, use the Read tool to read the review to evaluate at: ${{t.review_path}}

Task:
Extract every weakness claim that the review makes about the paper, then judge whether each weakness is reliable BY CHECKING IT AGAINST THE PAPER TEXT.

Ignore any item that is explicitly labeled as "Nice-to-Have" / "Nice-to-Haves" (e.g. items under a Nice-to-Have section or explicitly marked as nice-to-have) -- do not extract those as weakness items. Only apply this to items explicitly said to be nice-to-have; do NOT infer or reclassify weakness items as nice-to-have.

For each weakness, return:
- weakness: one specific weakness, flaw, limitation, or criticism of the paper that appears in the review.
- reliable: 1 if this weakness is genuinely supported by the paper (the flaw really exists, the omission is real, the critique is well-grounded). 0 if it matches one of the error patterns in the guideline (Misunderstanding/Neglect/etc. -- e.g., the reviewer overlooked something explicitly in the paper, misread a claim, asked for something out-of-scope, or made a vague/generic/excessive criticism).
- error_type: if reliable=0, choose the single best-matching label from the error type table (exact label text). If reliable=1, use an empty string.
- justification: 1-2 sentences. If reliable=0, cite the specific paper passage that contradicts the weakness or explain why it is vague/excessive/generic. If reliable=1, point to the gap in the paper that supports the weakness.

Be strict. The paper is available to you -- if the reviewer's claim contradicts something explicitly in the paper, mark it Neglect/Misunderstanding. If you cannot find supporting evidence in the paper for what the reviewer claims is missing, double-check the paper before marking reliable=1.

Return your result via the required structured output only.`
}}

const CONCURRENCY = {concurrency}
const results = []
for (let i = 0; i < TASKS.length; i += CONCURRENCY) {{
  const chunk = TASKS.slice(i, i + CONCURRENCY)
  const chunkResults = await parallel(chunk.map((t) => async () => {{
    const out = await agent(buildPrompt(t), {{
      label: `${{METHOD}}:${{t.paper_id}}`,
      schema: SCHEMA,
      model: 'sonnet',
    }})
    if (!out || !Array.isArray(out.items)) return []
    return out.items.map((it) => ({{
      method: METHOD,
      paper_id: t.paper_id,
      weakness: it.weakness,
      reliable: it.reliable,
      error_type: it.error_type,
      justification: it.justification,
      status: 'ok',
    }}))
  }}))
  results.push(...chunkResults)
  log(`method=${{METHOD}}: chunk ${{i / CONCURRENCY + 1}}/${{Math.ceil(TASKS.length / CONCURRENCY)}} done`)
}}

const flat = results.filter(Boolean).flat()
log(`method=${{METHOD}}: ${{flat.length}} weakness rows from ${{TASKS.length}} papers`)
return flat
"""


def build_task_list(method, ids, dr14b_review_dir):
    cfg = METHODS[method]
    d = cfg["dir"]
    tasks = []
    for pid in ids:
        if cfg["kind"] == "single_md":
            review_path = d / f"{pid}.md"
        elif cfg["kind"] == "cspaper_md":
            review_path = d / f"{pid}__ICLR_main_2026_2.md"
        elif cfg["kind"] == "deepreviewer_json":
            review_path = dr14b_review_dir / f"{pid}.md"
        else:
            raise ValueError(cfg["kind"])
        paper_path = PAPER_DIR / f"{pid}.txt"
        if not review_path.exists() or not paper_path.exists():
            continue
        tasks.append({"paper_id": pid, "review_path": str(review_path), "paper_path": str(paper_path)})
    return tasks


def extract_deepreviewer_reviews(ids, out_dir):
    """DeepReviewer_14B stores 4 simulated reviewers per paper in one JSON; pick one
    deterministically (seeded by paper id) and materialize it as a .md file so it can
    be treated like every other method's single_md review."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for pid in ids:
        p = METHODS["DeepReviewer_14B"]["dir"] / f"{pid}.txt.json"
        if not p.exists():
            continue
        data = json.load(open(p))
        reviews = data["results"][0]["reviews"]
        if not reviews:
            continue
        rng = random.Random(f"{SEED}-DeepReviewer_14B-{pid}")
        text = rng.choice(reviews)["text"]
        (out_dir / f"{pid}.md").write_text(text)


def main():
    guideline = GUIDELINE_PATH.read_text(encoding="utf-8")
    ids = json.load(open(SUBSET_IDS_PATH))
    dr14b_review_dir = OUT_DIR / "dr14b_reviews"
    extract_deepreviewer_reviews(ids, dr14b_review_dir)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for method in METHODS:
        tasks = build_task_list(method, ids, dr14b_review_dir)
        script = TEMPLATE.format(
            method_json=json.dumps(method),
            guideline_json=json.dumps(guideline),
            tasks_json=json.dumps(tasks),
            concurrency=CONCURRENCY,
        )
        out_path = OUT_DIR / f"critics_workflow_{method}.js"
        out_path.write_text(script)
        print(f"{method}: {len(tasks)} tasks -> {out_path}")


if __name__ == "__main__":
    main()
