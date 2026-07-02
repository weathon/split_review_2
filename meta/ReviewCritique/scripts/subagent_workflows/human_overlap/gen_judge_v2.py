"""Regenerate the human-overlap AI-judge workflow embedding the REVISED guideline
(reduced unreliable examples + added reliable examples). Produces a subset script
(for the cheap first pass) and a full script (all 815 segments)."""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUIDELINE = (HERE.parents[2] / "outputs" / "weakness_reliability_guideline.md").read_text()
segments = json.load(open(HERE / "ai_segments.json"))
assigns = json.load(open(HERE / "ai_assignments.json"))
strict_ids = set(json.load(open(HERE / "strict_pair_ids.json")))

seg_by_id = {s["seg_id"]: s for s in segments}

# seg_ids that participate in strict-subset pairs (the AI judges the judged side)
strict_seg_ids = sorted({a["seg_id"] for a in assigns if a["pair_id"] in strict_ids})

# subset: 60 strict pairs -> their unique judged seg_ids
rng = random.Random(0)
strict_pairs = [a for a in assigns if a["pair_id"] in strict_ids]
sub_pairs = rng.sample(strict_pairs, 60)
subset_seg_ids = sorted({a["seg_id"] for a in sub_pairs})

TEMPLATE = """export const meta = {{
  name: 'human-overlap-ai-judge-v2',
  description: 'AI (revised guideline) judges reliability of overlapped human weakness segments',
  phases: [{{ title: 'Judge' }}],
}}

const SCHEMA = {{
  type: 'object',
  properties: {{
    reliable: {{ type: 'integer', enum: [0, 1] }},
    error_type: {{ type: 'string' }},
    justification: {{ type: 'string' }},
  }},
  required: ['reliable', 'error_type', 'justification'],
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

const GUIDELINE = {guideline_json}
const TASKS = {tasks_json}

log(`Judging ${{TASKS.length}} overlapped human weakness segments (revised guideline)`)

function buildPrompt(t) {{
  return `You are an expert NLP/ML conference meta-reviewer. Judge whether ONE specific weakness/concern segment from a human review is reliable, USING THE PAPER TEXT as ground truth.

Error type table:
${{ERROR_TYPE_TABLE}}

Weakness reliability guideline (error type table + human-annotated examples of BOTH unreliable and reliable weaknesses):
${{GUIDELINE}}

First, use the Read tool to read the full paper text at: ${{t.paper_path}}

The SPECIFIC segment to judge:
=== SEGMENT START ===
${{t.segment_text}}
=== SEGMENT END ===

Task:
Judge whether THIS SPECIFIC segment is reliable BY CHECKING IT AGAINST THE PAPER TEXT.

Return:
- reliable: 1 if this segment is a genuine, well-grounded criticism of the paper (the flaw really exists, the omission is real, the concern is legitimate). 0 ONLY if it clearly matches one of the error patterns in the guideline (Misunderstanding/Neglect/Vague/Out-of-scope/etc.).
- error_type: if reliable=0, choose the single best-matching label from the error type table (exact label text). If reliable=1, use an empty string.
- justification: 1-2 sentences citing the specific paper passage.

Do NOT mark a segment unreliable merely because it is a criticism or because you could imagine a rebuttal. Most genuine weaknesses raised by reviewers ARE reliable (see the reliable examples in the guideline). Only mark reliable=0 when the segment clearly matches an error pattern -- e.g. it contradicts something explicitly in the paper, misreads a claim, is vague/generic, or asks for something out of scope. When in doubt, mark reliable=1.

Return your result via the required structured output only.`
}}

const CONCURRENCY = 2
const results = []
for (let i = 0; i < TASKS.length; i += CONCURRENCY) {{
  const chunk = TASKS.slice(i, i + CONCURRENCY)
  const chunkResults = await parallel(chunk.map((t) => async () => {{
    const out = await agent(buildPrompt(t), {{
      label: `seg${{t.seg_id}}_p${{t.paper_idx}}`,
      schema: SCHEMA,
      model: 'sonnet',
    }})
    if (!out) return null
    return {{
      seg_id: t.seg_id,
      paper_idx: t.paper_idx,
      segment_text: t.segment_text,
      pred_reliable: out.reliable,
      pred_error_type: out.error_type,
      pred_justification: out.justification,
    }}
  }}))
  results.push(...chunkResults)
  log(`chunk ${{i / CONCURRENCY + 1}}/${{Math.ceil(TASKS.length / CONCURRENCY)}} done`)
}}

const flat = results.filter(Boolean)
log(`${{flat.length}} segments judged`)
return flat
"""


def build(seg_ids, out_name):
    tasks = [
        {
            "seg_id": sid,
            "paper_idx": seg_by_id[sid]["paper_idx"],
            "paper_path": seg_by_id[sid]["paper_path"],
            "segment_text": seg_by_id[sid]["segment_text"],
        }
        for sid in seg_ids
    ]
    script = TEMPLATE.format(
        guideline_json=json.dumps(GUIDELINE),
        tasks_json=json.dumps(tasks),
    )
    (HERE / out_name).write_text(script)
    print(f"{out_name}: {len(tasks)} segments")


build(subset_seg_ids, "judge_v2_subset.js")
build(strict_seg_ids, "judge_v2_full.js")
json.dump(subset_seg_ids, open(HERE / "subset_seg_ids.json", "w"))
print(f"subset pairs: {len(sub_pairs)}, strict pairs total: {len(strict_pairs)}")
