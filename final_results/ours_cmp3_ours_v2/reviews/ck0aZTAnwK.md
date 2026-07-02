Now I have sufficient calibration. Let me produce the final review.

## Summary

This paper studies pre-training in the data-constrained, compute-unlimited regime — a timely problem given that web data grows at ~1.03×/year while compute grows at ~4×/year. The key findings are: (1) standard data-constrained recipes (epoching + parameter scaling) overfit; (2) tuning weight decay to ~30× higher than the standard 0.1 restores monotonic power-law scaling; (3) ensembling independently trained models achieves a lower loss asymptote than scaling single-model parameters; (4) the two strategies compose; and (5) distillation preserves most of the gain in smaller models. The headline quantitative claim is that the best recipe achieves the standard recipe's loss with 5.17× less data.

## Strengths

- **Timely, well-motivated problem framing.** The paper identifies a genuine tension (Section 1) — data is the bottleneck while compute is abundant — and frames the question clearly. This framing is novel and practically relevant as training runs grow.

- **Asymptote-based evaluation is a clean conceptual contribution.** The observation that FLOPs-anchored comparisons are inappropriate when compute is unconstrained, and the proposal to evaluate recipes by the limit of loss as parameters/ensemble members → ∞ (Section 3, Figure 1), directly matches the target regime and reframes the comparison in a useful way.

- **The weight decay finding is concrete, non-obvious, and actionable.** The paper finds that optimal weight decay under data-constrained, over-parameterized settings is ~30× larger than the standard 0.1 (Section 3, Figure 3 table). This specific result converts a non-monotonic loss curve into a monotonic power law and is immediately usable by practitioners.

- **Distillation validates practical relevance.** Showing that an 8-ensemble of 300M models can be distilled into a 300M student retaining 83% of the loss improvement (Section 6.1, Figure 8) directly addresses the objection that the asymptote benefits require impractically large models.

- **Disciplined evaluation protocol.** The paper deferred all downstream evaluation until after recipe selection was complete, using only validation loss to guide decisions (Section 7). This avoids cherry-picking or overfitting to specific benchmarks.

## Weaknesses

### Fatal

None.

### Major

1. **Precision of "5.17×" data efficiency is not supported by the evidence.** The headline multiplier is the product of a cascade of power-law fits, each from minimal data: 4 parameter counts for the regularized scaling law, 5 ensemble sizes (K=1–5) for ensemble scaling, then a three-step procedure (fit K→∞ asymptotes per N → fit N→∞ asymptote → fit D-scaling law) from 4 token counts. The paper acknowledges "the data scaling laws are expected to be noisy" (Section 5.3) but presents the number with two decimal places as if it carries that precision. A range (e.g., "~4×–6×") or qualitative framing would better reflect the underlying uncertainty. The *directional* claim is likely correct, but the precise multiplier is overclaimed.

2. **The joint scaling recipe's hyperparameter heuristic is unvalidated.** Section 4.3 states: "For the inner limit, we cannot fully find locally optimal hyperparameters due to experimental constraints. Instead, we use the heuristic of taking the optimal regularized hyperparameters with 2× epochs and 0.5× weight decay." This heuristic feeds directly into the "5.17×" number. The paper provides no analysis of how far this heuristic is from optimal or in which direction the error goes. Without this, the strongest quantitative claim rests on an unverified approximation.

### Minor

3. **Baseline comparison conflates tuning weight decay with the specific 30× finding.** The "standard recipe" tunes epoch count and learning rate but fixes weight decay at 0.1 (Section 2, Figure 2). The "regularized recipe" additionally tunes weight decay (Section 3). This means the reported gains combine two effects: (a) that tuning weight decay matters at all, and (b) that optimal weight decay is 30× larger than the default. Adding a "standard recipe with tuned weight decay" baseline would isolate contribution (b), which is the genuine novel finding. The current comparison is defensible (standard practice vs. improved practice) but the framing inflates the apparent novelty of the 30× result.

4. **Downstream evaluation is thin.** The paper validates on three accuracy-based multiple-choice benchmarks (PIQA, SciQ, ARC Easy) at 200M tokens (Section 7). While the paper is careful to defer evaluation and the results (9% improvement) are consistent with the claims, three similar tasks constitute a narrow test of generalization. The claim that interventions "generalize to downstream benchmarks" would be strengthened by more diverse tasks or generative evaluation.

### Trivial

- The abstract says "a 9% improvement for pre-training evals" without specifying the baseline; Section 7 clarifies this is relative to the best unregularized model. Should be explicit in the abstract.

## Nice-to-Haves

- Confidence intervals or bootstrap uncertainty estimates for the scaling-law asymptotes, given the small number of data points per fit.
- A small-scale study validating the joint scaling heuristic against a tuned search at one or two (N, K) combinations.
- Token-level perplexity on a standard corpus (e.g., WikiText-103) in addition to DCLM validation loss.
- Discussion of *why* the optimal weight decay scales with model size (currently provided only as an empirical finding).

## Removed Points

- *"Converging asymptotes at high data means the data efficiency advantage is a finite-data phenomenon"* — The paper directly addresses this (Section 5.3), showing that if asymptotes and exponents converge, a *constant* data efficiency gain persists determined by the numerator ratio (A₂/A₁)^(1/α). The reviewer misread this section.
- *"Self-distillation 'vastly outperforms its teacher' is a stretch"* — The improvement from ~3.57 to 3.43 is substantial (Figure 8); "vastly" is a reasonable characterization.
- *"Contradiction with Muennighoff et al. is overstated"* — The paper accurately describes the discrepancy and notes that Muennighoff et al. acknowledge it. Not overstated.
- *"Missing per-task breakdown"* — Deferred to Appendix G, which was stripped by the parser, not omitted by the authors.
- *"Only 300M used for ensemble comparison"* — Using a single base model size for the ensemble comparison is a standard experimental design choice; the paper's claim is conditional on that size.
- *"Missing discussion of why WD scales with model size"* — This is a nice-to-have, not a weakness. The empirical finding stands.
- *Formatting nitpicks, missing appendix references, reproducibility style concerns* — Removed per hard rules.

## Novel Insights

The harsh review's most pointed observation — that the "5.17×" number emerges from a fragile cascade of low-N power-law fits and an unvalidated hyperparameter heuristic — is both correct and important. It does not undermine the paper's substantive contributions (the 30× WD finding, the ensemble > parameter insight, the distillation preservation), but it does mean the paper's headline quantitative claim is substantially weaker than its presentation suggests. The other criticisms (thin downstream evaluation, baseline comparison framing) are real but secondary. The paper's core value lies in the directional findings and the asymptote evaluation framework, not in the precise multipliers.

## Suggestions

1. Replace "5.17×" with a range (e.g., "~4×–6×") or add explicit uncertainty quantification for all scaling-law asymptotes. At minimum, hedge the precision in the abstract and Figure 1.
2. Validate the joint scaling heuristic with a small tuned search at one (N, K) combination to bound the error.
3. Add a "standard recipe with tuned weight decay" baseline to isolate the contribution of *how much* WD helps beyond *any* WD tuning.
4. Broaden downstream evaluation (even at a single scale) to include a generative task or a non-multiple-choice benchmark.

## Score and Decision

**Round 1 bracket: 5.5–7.0.** The paper clearly outranks the 1–3 range (papers with no real contribution or fundamental flaws) and falls below the 7.5+ range (top-tier papers with cleaner experiments and stronger evidence). It is most comparable to papers scoring 5.2–6.75 in the calibration corpus.

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Systematic Review of LLMs | 1.00 | R1 | Much weaker — no novel contribution |
| Role of Task Complexity | 3.00 | R1 | Weaker — narrower scope, less actionable findings |
| A Hitchhiker's Guide to Scaling Law Estimation | 5.20 | R1 | Similar methodological concerns about scaling law fitting, but less novelty |
| Scaling Laws for Multilingual LMs | 5.25 | R1 | Similar — interesting findings but overclaimed precision |
| Scaling Laws for Predicting Downstream Perf. | 4.25 | R1 | Weaker — less novel framing |
| Language Models Scale Reliably w/ Over-training | 6.50 | R1 | Stronger experimental validation (104 models), less conceptual novelty |
| Bayesian Scaling Laws for ICL | 6.00 | R1 | Comparable — interesting framing but limited scope |
| Dynamic Loss-Based Sample Reweighting | 6.00 | R2 | Similar score — clear contribution but limited validation |
| How much can we Forget about Data Contamination? | 6.75 | R2 | Stronger empirical methodology, similar experimental scale |
| Synergy and Diversity in CLIP Ensemble | 6.25 | R2 | Similar — ensemble analysis in a different domain |

The paper's core contributions (asymptote metric, 30× WD finding, ensemble > parameter scaling, distillation preservation) are real and practically useful. However, the headline "5.17×" multiplier is built on a fragile chain of extrapolations and an unvalidated heuristic, making its precision misleading. The paper would be stronger if it honestly communicated this uncertainty.

**Score:** 6.0 — Borderline accept. The paper makes a meaningful contribution but must substantially qualify its central quantitative claim.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>