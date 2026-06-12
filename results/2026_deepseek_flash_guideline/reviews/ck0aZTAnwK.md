Let me write the final consolidated review.

## Summary

This paper studies language model pre-training under a novel regime: fixed, limited data (200M tokens baseline) but unlimited compute. The authors find that standard data-constrained recipes (epoching, scaling parameters) overfit, and propose three interventions—heavy regularization (optimal weight decay up to 30× standard), ensembling independently trained models, and their composition—to improve data efficiency. They introduce the scaling-law asymptote (limit as N→∞ or K→∞) as a metric for comparing recipes under no compute constraints, and estimate that their joint scaling recipe achieves 5.17× data efficiency at 200M tokens. The paper also shows distillation preserves most gains, and that validation loss improvements transfer to downstream benchmarks.

## Strengths

1. **Empirical discovery that optimal weight decay is ~30× larger than the standard default for large models.** Figure 3 (lines 97–102) shows tuned weight-decay values of 0.8 (150M), 1.6 (300M), and 3.2 (600M, 1.4B), versus the standard 0.1 from Brown et al. (2020). This directly challenges a widely used default and is shown to be necessary for achieving monotone power-law scaling at parameter-to-token ratios 140× larger than Chinchilla.

2. **Ensembling achieves a lower asymptotic loss (3.34) than parameter scaling (3.43), establishing that under infinite compute, many small models beat one large model.** Figure 4 (lines 125–133) shows this concretely: even a K=3 ensemble of 300M models outperforms the parameter-scaling asymptote. This is a testable, counterintuitive finding that contradicts the typical assumption that scaling a single model's parameters is the optimal use of extra compute.

3. **Proposal of the scaling-law asymptote as a metric for comparing recipes under unlimited compute.** Rather than comparing at fixed compute budgets (standard since Hoffmann et al., 2022), the paper evaluates lim_{N→∞} L(D,N) via power-law fits (line 91: L(D,N) = A_D/N^α_D + E_D). This framework is well-motivated by the paper's premise and enables meaningful comparison of recipes whose ordering may differ at small vs. asymptotic scales.

4. **Ensemble distillation compresses gains into an 8× smaller model while retaining 83% of the improvement.** Section 6.1 (lines 199–213): a 300M student distilled from an 8-ensemble achieves loss 3.36, outperforming the regularized recipe's asymptote (3.43). This shows practical applicability even under inference-parameter constraints.

5. **Self-distillation of a same-size teacher improves performance without ever training a larger model.** Section 6.2 (lines 215–219): a 300M student trained on the teacher's generations mixed with real data matches the regularized asymptote (3.43), contrary to prior work predicting collapse from self-generated data.

## Weaknesses

### Fatal
None.

### Major

1. **The quantitative precision of the headline claims (5.17× data efficiency, asymptotic loss values) exceeds what the underlying evidence supports with confidence.** The regularized recipe's asymptote (3.43) is fit on just 4 parameter counts (150M–1.4B, line 91). The joint scaling recipe's 5.17× figure involves a triple cascade of power-law fits (16 fits of L vs. K → 4 fits of asymptote vs. N → 1 fit of meta-asymptote vs. D, Section 5.2/Figure 7), each with few degrees of freedom. The paper reports only seed variance (at most 0.02 loss, line 113)—not model specification uncertainty (whether the functional form is correct or would change with additional data at larger N or K). The abstract and Figure 1 present 5.17× as a headline result without the caveats the body acknowledges. The paper would be strengthened by presenting the concrete best-achieved numbers (3.75× from five 1.4B models, 2.09× from the best 1.4B regularized model, line 185) as primary evidence alongside the extrapolations.

2. **The distillation experiment does not specify D' (the amount of synthetic data generated), making the "data efficiency" framing difficult to interpret.** Section 6.1 (lines 203–204) states that the teacher generates D' tokens and the student trains on a mixture of D real tokens and D' synthetic tokens, but D' is never reported. The claim "retains 83% of the ensembling benefit" compares the student's loss to the ensemble's loss at D tokens, but if D' is comparable to or larger than D, the student operates under a different effective token budget. The paper should report D' or clarify the exact data budget under which the student was evaluated.

### Minor

1. **The downstream evaluation is limited to three benchmarks (PIQA, SciQ, ARC Easy) without confidence intervals.** The paper reports "over 9% improvement" (line 235) comparing a specific best ensemble against a specific best unregularized model, without per-task breakdowns or error bars. While the paper cites Thrush et al. (2025) for standard benchmarks at this scale, the thin evaluation weakens the generalization claim, especially since evaluation variance on 2,000–5,000-example benchmarks can be non-trivial at this model scale.

2. **The data scaling laws for both recipes rely on only 4 token counts (200M–1.7B, an 8× range) without reporting fit quality metrics.** The standard recipe's data scaling law (Section 5.1) is built from the best loss at each of 4 token counts—since this recipe overfits, there is no systematic family of fits. No R² or similar measure is reported for any of the power-law fits, making it difficult for the reader to assess extrapolation reliability. The data efficiency ratios (2.29×, 5.17×) depend on interpolating these laws.

3. **The "30× larger weight decay" claim is model-size-dependent and should be qualified in the abstract/text.** The optimal weight decay for the 150M model is 0.8 (8×), not 30×. The 30× figure applies to the 600M and 1.4B models (3.2 vs. 0.1, lines 97–102). While the table in Figure 3 provides exact values, the abstract and line 87 state "30× larger" without qualification.

### Trivial
None.

## Nice-to-Haves
- Even one additional parameter count (e.g., 3B) or larger ensemble size (K=7–10) would substantially strengthen the asymptotic fits.
- A brief analysis of ensemble member diversity (e.g., predicted token distribution divergence) would strengthen the mechanistic explanation for why ensembling helps (Section 4 references Allen-Zhu and Li 2023, but does not verify the "multi-view" mechanism in its own setting).
- Reporting fit quality (R²) for power-law fits would help readers assess extrapolation reliability.

## Removed Points
- *Criticism about the paper contradicting Muennighoff et al. (2023):* The paper explicitly acknowledges this discrepancy and notes that Muennighoff et al. also removed overfit runs from their law (line 58). This is not a contradiction; it is a correct identification of a gap in prior work.
- *Criticism that the "heuristic hyperparameters" (2× epochs, 0.5× weight decay) for joint scaling are not fully optimized:* The paper is transparent about this (line 143: "cannot fully find locally optimal hyperparameters due to experimental constraints"). This is an honest limitation, not a flaw.
- *Criticism about the standard recipe data scaling law being "not from a systematic scaling law":* The paper explicitly states that it searches for the best parameter count and hyperparameters at each data scale (Section 5.1, line 173), which is the appropriate procedure given that the standard recipe does not admit a monotone scaling law.
- *Strength Finder claims about the paper "addressing an important problem" or being "well-written":* These are generic/superficial and lack specific anchors in the paper. Removed. All other strengths in the final review are concrete and verified against specific figures/sections.

## Novel Insights
The reviewers' analyses highlight a meta-observation not centered in the paper's own narrative: the paper's success with simple, decades-old techniques (regularization, ensembling, distillation) in a regime where compute is abundant and data is scarce suggests that many design decisions in current pre-training practice are implicitly optimized for the compute-constrained regime. The fact that optimal weight decay scales with model size (0.8→1.6→3.2→3.2 as N goes 150M→300M→600M→1.4B) and that self-distillation without a larger teacher works (Section 6.2) are both results pointing to significant "low-hanging fruit" that the field may have overlooked due to historically focusing on compute-optimal scaling. Additionally, the paper's asymptotic framework effectively reformulates the scaling law question: instead of asking "what's the best loss at this compute budget?", it asks "given this data, what's the best loss achievable with unlimited compute?"—shifting the optimization target in a way that could influence how future data-constrained pre-training research is designed.

## Suggestions
1. Qualify the headline quantitative claims (5.17×, 9%) as estimates with clear caveats about extrapolation uncertainty, and present concrete best-achieved numbers (3.75×, 2.09×) more prominently.
2. Report D' (synthetic token count) for distillation experiments and clarify the data budget under which the student operates.
3. Add per-task breakdowns and confidence intervals for the downstream evaluation (Appendix G is referenced but stripped).
4. Report fit quality (R² or similar) for power-law fits used in asymptotic estimation.

## Calibration Anchors

| Anchor Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| Language models scale reliably with over-training and on downstream tasks | iZeQBqJamf.md | 6.50 (Accept) | R1, R2 | Similar topic (scaling laws, downstream), more models (104 vs ~20) but less novel framing. Our paper has a more creative contribution but fewer data points. Roughly comparable quality. |
| Scaling Laws for Downstream Task Performance in Machine Translation | vPOMTkmSiu.md | 6.60 (Accept) | R2 | Also studies scaling laws for downstream performance. Similar thoroughness. |
| Scaling Law with Learning Rate Annealing | o9YC0B6P2m.md | 6.75 (Reject) | R1 | Novel scaling law but theoretical gaps. Our paper is more empirically grounded. |
| No Free Lunch from Random Feature Ensembles | 7rzA6aEASo.md | 5.60 (Reject) | R1, R2 | Also studies ensembling vs parameter scaling, but in a different (negative) direction. Our paper's finding (ensembling wins under infinite compute) is orthogonal and more novel in the data-constrained LM setting. |
| Why Has Predicting Downstream Capabilities...Remained Elusive? | zpBamnxyPm.md | 5.75 (Reject) | R2 | Studies why downstream predictions are hard; our paper actually shows positive transfer. Less directly comparable. |
| Investigating Pre-Training Dynamics of In-Context Learning | htDczodFN5.md | 6.50 (Accept) | R2 | Accepted paper at similar score; studies pre-training dynamics with careful empirical design. Comparable rigor level. |
| Need a Small Specialized Language Model? Plan Early! | aP3OBwf8dk.md | 6.00 (Reject) | R2 | Studies specialized SLMs with limited data. Less novel framing than our paper. |

Round-1 bracket: 5.5–7.5. Based on anchor comparison, the paper sits closest to the 6.5–6.6 range: it has a more novel framing than the scaling-law papers at 6.5, but fewer experimental data points and less statistical rigor. The qualitative findings are solid; the main weakness is that the quantitative precision claimed in the abstract exceeds what the evidence supports.

**MY FINAL SCORE:** <score>6.5</score>
**MY FINAL DECISION:** <decision>Accept</decision>