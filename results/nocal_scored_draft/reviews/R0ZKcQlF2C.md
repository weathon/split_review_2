Now let me write the final consolidated review.

## Summary

ARENABENCHER proposes a framework for automatically evolving static benchmarks by generating variants of test cases that preserve the original task ability while increasing difficulty. The pipeline extracts the core skill of each test case, generates candidate rewrites verified by an LLM judge, scores them using feedback from a sampled subset of models, and iteratively refines candidates using in-context demonstrations. Evaluated on GSM8K (math), CommonsenseQA (reasoning), and AdvBench Harmful Behaviors (safety), the framework produces benchmarks that are harder and maintain high alignment and fairness.

## Strengths

- **Well-motivated problem with a clear diagnosis** of benchmark saturation and data leakage threats (Section 1). The paper correctly identifies that static benchmarks lose diagnostic power as models improve and may reflect memorization.

- **Clean framework design with four well-reasoned desiderata** — difficulty, separability, fairness, alignment — that provide a coherent lens for evaluating benchmark quality (Section 3.5). This structuring of benchmark quality is a useful conceptual contribution.

- **Human evaluation on 100 GSM8K samples** with three expert annotators, reporting 95% alignment and 96% correctness (Section 4.2, Human Annotation). This provides credible evidence that the pipeline produces valid test cases for math reasoning.

- **Transparent case study (Figure 2)** that honestly documents a failure mode where the LLM verifier passed an unsolvable question. This disclosure is valuable for understanding the method's limitations and for future improvements.

- **Ablation of m=1 vs m=3 feedback models** (Table 1) showing that using more models consistently produces larger performance drops across all domains. This provides direct evidence that multi-model aggregation matters within the framework.

## Weaknesses

### Fatal

None.

### Major

- **No baseline comparisons against prior benchmark augmentation methods.** The paper discusses MATH-Perturb, ARITHMATTACK, Automatic Robustness Stress Testing, and gradient-based adversarial methods (Section 2) but implements none of them. Tables 1 and 2 compare only against the original benchmark. Without any baseline, the reader cannot determine whether ARENABENCHER's complex pipeline (ability extraction, multi-model scoring, iterative refinement) improves upon simpler perturbation strategies. The m=1 vs m=3 ablation is a good internal comparison but cannot substitute for external baselines.

- **Abstract claim that ARENABENCHER "improves model separability" is contradicted by the paper's own data.** For the default m=3 configuration, separability decreases on all three benchmarks: GSM8K (15.2→12.2), Harmful Behaviors (17.1→14.5), CSQA (8.5→7.2) (Table 2). While the body text acknowledges "slight variation," the abstract asserts the opposite of what the data show. This needs correction regardless of how the authors frame the acceptable trade-off between difficulty and separability.

- **Core framing around data contamination is never tested.** The abstract and introduction motivate the work entirely through data leakage ("Models can match memorized content rather than demonstrate true generalization"). Yet no experiments — n-gram overlap analysis, membership inference, controlled contamination tests — evaluate whether ARENABENCHER's updates are more resistant to contamination than the originals. The conclusion acknowledges this is a "first step," but the gap between the strong motivational framing and the absence of any evidence is large and risks misleading readers about what has been demonstrated.

- **The fairness metric is partially a tautology given the selection criterion.** Section 3.3 explicitly selects candidates that "consistently degrade performance across the sampled models." The fairness metric (Section 3.5) measures whether failures are evenly distributed across models. Selecting for uniform degradation mechanically inflates the fairness score. The high fairness values in Table 2 (87.8% for GSM8K, 85.47% for Harmful Behaviors) do not constitute independent evidence of fairness; they are in part a restatement of the selection criterion. A baseline that does not optimize for uniform degradation is needed to establish genuine improvement.

- **The same pool of 6 models is used for both candidate selection and final evaluation** (Section 3.3 and Table 1). Randomly sampling 3 out of 6 per iteration provides partial separation, but any candidate that exploits a quirk shared by the 3 sampled models will score highly and the result will be re-observed when evaluating on all 6. A held-out model set (models that never participated in feedback) is needed to support the claim of model-agnostic generalization.

### Minor

- **GPT-4o serves as the generator, verifier, and alignment judge** (Section 4.1), creating a self-reinforcing evaluation loop. The case study (Figure 2) concretely demonstrates this risk: the verifier passed an unsolvable question. The human annotation on 100 samples partially mitigates this, but using a different model for verification or as the alignment judge would strengthen the pipeline's validity.

- **Results in Tables 1 and 2 are reported as point estimates without variance or confidence intervals.** Given the stochasticity of LLM-based generation and the small model pool (K=6), it is difficult to assess whether observed differences are meaningful.

- **The model pool (K=6, 1B-7B, open-source, 3 families) lacks breadth.** No frontier or API-based models are included, which limits the generalizability of findings to the kinds of systems where benchmarks are most urgently needed.

- **The √K rule citation from Breiman (2001) and Chen & Guestrin (2016) (Section 3.3) is not a principled justification.** Random forest feature subsampling has no established connection to subsampling language models for benchmark generation. The heuristic may still be sensible, but the cited work does not support it in this context.

### Trivial

None.

## Nice-to-Haves

- Add at least one simple baseline (e.g., random LLM paraphrasing without multi-model scoring) to isolate the value of the feedback mechanism.
- Evaluate the updated benchmarks on a held-out model set (e.g., API-based models) to test generalization beyond the 6-model pool.
- Report the rejection rate from the verification step (fraction of candidates failing J(x_i^j, y_i^j) = Valid) to characterize the pipeline's efficiency.
- Systematically categorize failure modes beyond the single case study (e.g., from the human-annotated samples).
- Use a different LLM (e.g., Claude or Gemini) as the alignment judge and report cross-model agreement.

## Removed Points

These points from the input review were removed or substantially altered after verification against the paper:

- **"Full-benchmark results missing"** — The paper states all test cases are updated (Section 3.5, B' = {(x_i^†, y_i)}_{i=1}^N). The question of how many candidates were rejected per test case is a reasonable clarity request but the paper does report the final set size.
- **"No analysis of failure modes"** — Partially addressed by the case study and human annotation. A valid suggestion but not a core weakness.
- **"Separability consistently decreases"** — The reviewer's phrasing was slightly imprecise: for m=1, Harmful Behaviors and CSQA show minor increases (17.1→18.2 and 8.5→9.4). The corrected finding is that for the *default m=3 setting*, separability decreases uniformly.
- **"Strengthening the Paper" section** — Most suggestions are folded into Nice-to-Haves above.
- Various generic strengths (e.g., "well-motivated problem" just as a standalone statement) were merged into more specific strengths.

## Novel Insights

The most informative finding goes beyond the paper's own claims: the m=1 vs m=3 comparison (Table 1) empirically shows that aggregating feedback from multiple models yields consistently harder benchmarks than using a single model, providing non-trivial support for the multi-model design choice. The transparent failure case study (Figure 2) also yields an insight that the paper does not fully explore — the ability extraction step can capture surface-level scenario features (e.g., "fantasy scenario involving a dragon and a magical gemstone") rather than core reasoning structure, which is a concrete failure mode that future benchmark evolution methods need to guard against.

## Suggestions

1. Add at least one baseline from prior perturbation-based methods to substantiate the claim that multi-model feedback outperforms simpler alternatives.
2. Correct the abstract — replace "improves model separability" with an accurate description of the empirical finding (separability decreases slightly under increased difficulty but benchmarks remain diagnostic).
3. Report variance across multiple generation/evaluation runs, or at minimum note that single-run estimates are used.
4. Include a held-out evaluation on models not used in feedback to test for overfitting.
5. Disambiguate the fairness metric from the selection criterion, either by changing the metric or by including baselines that isolate the effect.

## Score and Decision

The paper addresses a timely and important problem with a well-structured framework, a transparent evaluation that includes human annotation, and an informative ablation showing the value of multi-model feedback. However, the experimental evaluation has significant gaps: no baseline comparisons against prior work, an abstract claim contradicted by the paper's own data, a core motivational premise (contamination resistance) left untested, a fairness metric that is partially a restatement of the selection criterion, and an evaluation design that does not separate the models used for selection from those used for scoring. These are not fatal — the framework itself is sound and the m=1 vs m=3 ablation provides real evidence — but they are serious enough that the paper's strongest claims are not fully supported. With revisions, particularly the addition of baselines and correction of overstated claims, the work would be considerably stronger.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Accept</decision>