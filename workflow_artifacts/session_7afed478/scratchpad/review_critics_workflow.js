export const meta = {
  name: 'review-critics-subagent',
  description: 'Judge weakness reliability for one method\'s reviews against final_results papers using Claude subagents',
  phases: [
    { title: 'Judge', detail: 'one subagent per paper: extract weaknesses, judge reliability against paper text' },
  ],
}

const SCHEMA = {
  type: 'object',
  properties: {
    items: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          weakness: { type: 'string' },
          reliable: { type: 'integer', enum: [0, 1] },
          error_type: { type: 'string' },
          justification: { type: 'string' },
        },
        required: ['weakness', 'reliable', 'error_type', 'justification'],
      },
    },
  },
  required: ['items'],
}

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

phase('Judge')

const method = args.method
const guideline = args.guideline
const tasks = args.tasks

log(`Judging ${tasks.length} papers for method=${method}`)

function buildPrompt(t) {
  return `You are an expert NLP/ML conference meta-reviewer. Extract each weakness claim in a review and judge whether it is reliable, USING THE PAPER TEXT as ground truth.

Error type table:
${ERROR_TYPE_TABLE}

Weakness reliability guideline (error type table + human-annotated examples):
${guideline}

Paper id: ${t.paper_id}

First, use the Read tool to read the full paper text at: ${t.paper_path}
Then, use the Read tool to read the review to evaluate at: ${t.review_path}

Task:
Extract every weakness claim that the review makes about the paper, then judge whether each weakness is reliable BY CHECKING IT AGAINST THE PAPER TEXT.

Ignore any item that is explicitly labeled as "Nice-to-Have" / "Nice-to-Haves" (e.g. items under a Nice-to-Have section or explicitly marked as nice-to-have) — do not extract those as weakness items. Only apply this to items explicitly said to be nice-to-have; do NOT infer or reclassify weakness items as nice-to-have.

For each weakness, return:
- weakness: one specific weakness, flaw, limitation, or criticism of the paper that appears in the review.
- reliable: 1 if this weakness is genuinely supported by the paper (the flaw really exists, the omission is real, the critique is well-grounded). 0 if it matches one of the error patterns in the guideline (Misunderstanding/Neglect/etc. -- e.g., the reviewer overlooked something explicitly in the paper, misread a claim, asked for something out-of-scope, or made a vague/generic/excessive criticism).
- error_type: if reliable=0, choose the single best-matching label from the error type table (exact label text). If reliable=1, use an empty string.
- justification: 1-2 sentences. If reliable=0, cite the specific paper passage that contradicts the weakness or explain why it is vague/excessive/generic. If reliable=1, point to the gap in the paper that supports the weakness.

Be strict. The paper is available to you -- if the reviewer's claim contradicts something explicitly in the paper, mark it Neglect/Misunderstanding. If you cannot find supporting evidence in the paper for what the reviewer claims is missing, double-check the paper before marking reliable=1.

Return your result via the required structured output only.`
}

const results = await parallel(tasks.map((t) => async () => {
  const out = await agent(buildPrompt(t), {
    label: `${method}:${t.paper_id}`,
    schema: SCHEMA,
    model: 'sonnet',
  })
  if (!out || !Array.isArray(out.items)) return []
  return out.items.map((it) => ({
    method,
    paper_id: t.paper_id,
    weakness: it.weakness,
    reliable: it.reliable,
    error_type: it.error_type,
    justification: it.justification,
    status: 'ok',
  }))
}))

const flat = results.filter(Boolean).flat()
log(`method=${method}: ${flat.length} weakness rows from ${tasks.length} papers`)
return flat
