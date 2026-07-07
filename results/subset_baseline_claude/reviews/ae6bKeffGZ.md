## Summary

Arithmetic-Bench is a dynamically generated benchmark designed to evaluate LLMs' multi-step reasoning by testing basic arithmetic operations (addition, subtraction, multiplication, division) over numbers of varying digit lengths, along with subtasks like copying, reversing, counting, and base conversion. The paper argues that arithmetic serves as a reliable proxy for general reasoning ability because it is deterministic, infinitely scalable, and resistant to memorization. Experiments across ~20 models show that accuracy drops sharply beyond 10 digits and that no model achieves robust length generalization.

## Strengths

- **Clean, practical benchmark design**: The dynamic generation scheme (sampling new random numbers for each evaluation run) is a genuine advantage over static benchmarks, making memorization-based cheating effectively impossible. The evaluation protocol (`a in b`) is elegantly simple and avoids formatting-related evaluation noise.
- **Breadth of model coverage**: The paper evaluates a large set of models spanning open-source and proprietary, instruction-tuned and reasoning-specialized, across model sizes from 0.5B to 671B. The resulting dataset of observations (Table 4) is genuinely useful for the community to assess where models stand on basic computation.
- **Concrete memorization experiment**: Section 4.4's demonstration that training on AIME 2024 for ~100 epochs achieves ~90% accuracy — and still fluctuates — is a concrete, compelling illustration of the finite-benchmark cheating problem.

## Weaknesses

### Fatal
None.

### Major

- **Critical underpowering for key models**: DeepSeek and GPT models are evaluated with n=1 problem per digit length (100 digit lengths × 1 sample = 100 total problems per task). With binary outcomes and n=1, a single lucky or unlucky guess shifts reported accuracy by 1%. The paper acknowledges this ("due to resource limitations") but still draws comparative conclusions from these numbers (e.g., "GPT-4's performance falls between Qwen2.5 and Qwen3"). The variance for n=1 is so large that many claims in Section 4.2 are statistically unsupportable for these models.

- **Weak theoretical contributions**: Theorem 1 ("a container cannot hold more than its capacity") is a definitional tautology, not a theorem — it introduces no new insight. Theorem 2's "proof" reduces to: if you can encode any reasoning task as arithmetic, then arithmetic capacity lower-bounds reasoning capacity. This mapping is claimed but never formalized — the proof is one paragraph of hand-waving with no concrete reduction. These are presented as mathematical theorems with notation, which overstates their rigor.

- **Correlation analysis is severely underpowered**: Table 5, which is supposed to demonstrate that arithmetic performance correlates with AIME performance, contains only 6 data points. No correlation coefficient, p-value, or confidence interval is reported. Observing a rough trend in 6 points is insufficient to claim a "positive correlation" between Arithmetic-Bench and general reasoning ability.

### Minor

- **Proxy metric claim is speculative**: The analogy to text rendering in image generation (Section 1.4) is intuitive but not empirically verified. The paper shows that reasoning models score higher on multiplication than non-reasoning models, but does not demonstrate that improving arithmetic performance causally improves performance on other reasoning tasks.
- The distinction between the benchmark's "sub tasks" (copy, reverse, space, box) is underexplored experimentally — Table 4 only covers main tasks; sub-task results appear only in Section 4.2's qualitative summary without a dedicated results table.

### Trivial
None.

## Nice-to-Haves

- Including confidence intervals or at least error bars (even bootstrap estimates) for the n=1 model evaluations would substantially strengthen the experimental section.
- A correlation plot with more data points — e.g., including all models in Table 4 against their known AIME/MATH scores — would make the proxy-metric claim far more credible.
- Reporting sub-task accuracy in a table (not just prose) would improve completeness.

## Novel Insights

The clearest novel insight is the empirical finding that reasoning-specialized models (DeepSeek-R1, QwQ, Qwen3-think) outperform instruction-tuned models on high-complexity arithmetic (multiplication) but underperform on low-complexity tasks (addition, copy). This is consistent with findings from Shojaei et al. (2025) and the paper's acknowledgment of that work is fair. The demonstration that LLMs approach a hard cliff around 10 digits for multiplication — and that this cliff appears across model families and sizes — is a useful empirical contribution, though not surprising given prior work on length generalization failure.

## Suggestions

- Increase n to at least 30–50 per digit length for all models evaluated, or clearly mark results with n=1 as "preliminary" and restrict comparative claims to models with adequate sample sizes.
- Formalize or remove Theorem 2; as currently written it contributes little beyond a verbal argument. If retained, at minimum provide an explicit algorithmic reduction.
- Include a full sub-task results table (e.g., copy, rev, count, len, b2d, d2b) analogous to Table 4 for the main tasks.

## Score and Decision

The core benchmark contribution — dynamic, scalable, memorization-resistant arithmetic evaluation — is genuinely useful and the paper is clearly written. However, the two major weaknesses substantially undermine the reliability of the reported results and the theoretical framing: the n=1 evaluations make model comparisons unreliable for half the evaluated models, and the theoretical "theorems" add little. The paper needs a more careful experimental design and either strengthened or removed theoretical claims.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>