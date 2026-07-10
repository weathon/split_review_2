Based on the scoring model's assessment, I can now write the final consolidated review.

## Summary

This paper identifies and characterizes a novel safety vulnerability specific to Masked Diffusion Language Models (MDLMs): the *priming vulnerability*, where affirmative tokens appearing at intermediate denoising steps can steer generation toward harmful responses even in aligned models. The authors present a theoretical analysis motivating First-Step GCG, an efficient attack that exploits this vulnerability without requiring intervention in the denoising process. They then propose Recovery Alignment (RA), which trains models to produce safe responses from contaminated intermediate states. Experiments across three MDLMs show that RA dramatically reduces attack success rates compared to existing alignment methods (SFT, DPO, MOSA) with minimal degradation in general capabilities.

## Strengths

- **Novel vulnerability identification** — The priming vulnerability in MDLMs is a genuinely new safety problem, clearly characterized via the anchoring attack (Section 4.1). Figure 2 shows even a single affirmative token at step 1 raises ASR from 2% to 21% on LLaDA Instruct, a striking and well-documented finding.
- **Theoretical connection to practical attack design** — Theorem 4.1 provides a clean lower bound on the full denoising likelihood via the first-step likelihood, and First-Step GCG (Section 4.2) operationalizes this insight. Table 1 shows First-Step GCG achieves 58% ASR vs. 20% for MC GCG on LLaDA Instruct with a 20× speedup.
- **Principled, well-motivated mitigation** — Recovery Alignment (RA, Section 5) directly addresses the root cause: standard alignment only trains from fully masked initial states. The linear curriculum for t_inter is a sensible design, and the RA w/o inter ablation in Table 2 cleanly isolates the effect of training on contaminated states.
- **Consistently strong empirical results** — Across three MDLMs, four attack types, two datasets, and three evaluators, RA dramatically reduces ASR compared to all baselines (e.g., LLaDA at t_inter=4: RA achieves 1.3% ASR vs. 42.7% for SFT, 20.0% for DPO, 24.0% for MOSA). General capability evaluation (Table 4) shows no substantial degradation.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Model name error in Tables 2 and 3** — The model column headers read "LLaMA" and "LLaMA1.5" (lines 218, 224, 250, 256) instead of the correct names "LLaDA" and "LLaDA1.5" that appear correctly in Table 4 and Section 6.1. While experienced readers can infer the intended mapping from context, this is confusing and could mislead readers. The results themselves are unaffected.

- **Numerical inconsistency between Section 4.1 and Table 2** — Section 4.1 (line 110) states that the Anchoring Attack at t_inter=1 raises ASR for LLaDA Instruct "from 2% to 21%", but Table 2 reports 17.3% for the same condition (same attack, dataset, and evaluator). The ~4 pp gap is not explained. This does not affect the paper's overall conclusions but erodes trust in the specific numbers and should be clarified.

- **Theorem 4.1's monotonicity assumption is heuristically motivated** — The theorem assumes log π_θ(𝐫̃_{t+1}=𝐫 | 𝐪, 𝐫_t) ≥ log π_θ(𝐫̃_1=𝐫 | 𝐪, 𝐫_0) for all t. The paper's justification ("richer context" → "probability mass concentrates") is a heuristic, not a formal guarantee. The paper defers to Appendix C.2 for empirical validation. Since First-Step GCG works well empirically regardless, this does not undermine the paper's conclusions but weakens the theoretical framing relative to what a strict reading of the theorem suggests.

- **Monte Carlo GCG baseline lacks sampling detail** — First-Step GCG outperforms MC GCG substantially (58% vs 20% ASR, Table 1), but the paper provides no details on MC sampling hyperparameters (number of samples per gradient estimate, variance-reduction techniques) in the main text. Without this context, it is unclear whether the comparison reflects a genuinely superior method or an undertuned MC baseline.

### Trivial
None.

## Nice-to-Haves

- Specify the exact HuggingFace identifier for the DeBERTaV3 reward model checkpoint to improve reproducibility.
- Add statistical significance tests (e.g., paired bootstrap) for the main RA vs. baseline comparisons in Tables 2 and 3, though the reported means and standard deviations over three runs are already informative.

## Removed Points

These points are flagged to be removed; treat them with caution:

- *Reward model specificity* (from "Strengthening the Paper"): Requesting the exact DeBERTaV3 checkpoint is a reproducibility nice-to-have, not a weakness. The paper's stated use of "DeBERTaV3 without additional fine-tuning" is sufficient for evaluation.
- *RA w/o inter reward model discrepancy* (from "Missing Parts"): The suggestion that the reward model may be miscalibrated for contaminated states is speculative and unsupported by evidence.
- *MMaDA distinct behavior* (from "Missing Parts"): The observation that MMaDA benefits more from RA is an honest reporting of results, not a weakness.
- *Statistical testing* (from "Missing Parts"): Requesting formal significance tests on top of three-run means and standard deviations goes beyond typical practice for this type of empirical evaluation.

## Novel Insights

None beyond the paper's own contributions. The identified weaknesses are surface-level presentation/consistency issues that do not reveal deeper structural problems. The reviews converge on the paper being strong and well-supported.

## Suggestions

1. Fix the LLaMA→LLaDA naming error across Tables 2 and 3.
2. Explain the 21% vs. 17.3% discrepancy between Section 4.1 and Table 2 (e.g., whether it reflects different random seeds, evaluation subsets, or is a reporting error).
3. Add the MC GCG sampling hyperparameters (sample count, variance reduction techniques) in the main text or explicitly reference the appendix section.
4. Consider adding the specific HuggingFace identifier for the DeBERTaV3 reward model checkpoint.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>