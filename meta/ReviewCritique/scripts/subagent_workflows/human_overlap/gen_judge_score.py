"""Very original human-overlap AI judge (original guideline + original prompt), but the
output is a continuous reliability score in [0.0, 1.0] instead of a binary label, so we
can compute F1-max (best threshold) and AUROC. Judges all 815 unique overlapped segments."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUIDELINE = (HERE / "original_guideline_extracted.md").read_text()
segments = json.load(open(HERE / "ai_segments.json"))

TEMPLATE = """export const meta = {{
  name: 'human-overlap-ai-judge-score',
  description: 'Original judge, continuous reliability score in [0,1] for overlapped human weakness segments',
  phases: [{{ title: 'Judge' }}],
}}

const SCHEMA = {{
  type: 'object',
  properties: {{
    reliable_score: {{ type: 'number' }},
    error_type: {{ type: 'string' }},
    justification: {{ type: 'string' }},
  }},
  required: ['reliable_score', 'error_type', 'justification'],
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

log(`Judging ${{TASKS.length}} overlapped human weakness segments (continuous score)`)

function buildPrompt(t) {{
  return `You are an expert NLP/ML conference meta-reviewer. Judge whether ONE specific weakness/concern segment from a human review is reliable, USING THE PAPER TEXT as ground truth.

Error type table:
${{ERROR_TYPE_TABLE}}

Weakness reliability guideline (error type table + human-annotated examples):
${{GUIDELINE}}

First, use the Read tool to read the full paper text at: ${{t.paper_path}}

The SPECIFIC segment to judge:
=== SEGMENT START ===
${{t.segment_text}}
=== SEGMENT END ===

Task:
Judge whether THIS SPECIFIC segment is reliable BY CHECKING IT AGAINST THE PAPER TEXT.

Return:
- reliable_score: a number from 0.0 to 1.0 giving how reliable this segment is. 1.0 means the segment is genuinely supported by the paper (the flaw really exists, the omission is real, the critique is well-grounded). 0.0 means it clearly matches one of the error patterns in the guideline (Misunderstanding/Neglect/etc.). Use intermediate values to express uncertainty.
- error_type: if the score is low (unreliable), choose the single best-matching label from the error type table (exact label text). If the score is high (reliable), use an empty string.
- justification: 1-2 sentences citing the specific paper passage.

Be strict. If the segment's claim contradicts something explicitly in the paper, give it a low score (Neglect/Misunderstanding). If you cannot find supporting evidence in the paper for what the segment claims is missing, double-check the paper before giving a high score.

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
      pred_score: out.reliable_score,
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

tasks = [
    {
        "seg_id": s["seg_id"],
        "paper_idx": s["paper_idx"],
        "paper_path": s["paper_path"],
        "segment_text": s["segment_text"],
    }
    for s in segments
]
script = TEMPLATE.format(guideline_json=json.dumps(GUIDELINE), tasks_json=json.dumps(tasks))
(HERE / "judge_score_full.js").write_text(script)
print(f"judge_score_full.js: {len(tasks)} segments")
