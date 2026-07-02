Now I'll write the consolidated final review.

## Summary

This paper studies language model pre-training under a fixed data budget with unlimited compute, motivated by the observation that compute grows faster than web text availability. The authors show that standard data-constrained recipes overfit, and that heavy regularization (weight decay 30× larger than standard) enables monotone parameter scaling. They propose evaluating recipes via the asymptote of their scaling law, and find that ensembling independently trained models achieves a lower loss asymptote than scaling a single model. Combining parameter and ensemble scaling yields a 5.17× estimated data efficiency improvement. The paper further shows that distillation retains most of these gains in smaller models, and that improvements on validation loss transfer to downstream benchmarks.

## Strengths

1. **Well-motivated problem framing.** The paper tackles a clean, underexplored regime (pre-training when data is the bottleneck and compute is abundant) with concrete motivation (compute growing ~4×/year vs. web text at ~1.03×/year). The asymptote evaluation metric — loss limit rather than performance at a fixed compute budget — is a natural and novel response to this regime, and is the paper's strongest conceptual contribution.

2. **Non-trivial, actionable discovery about weight decay.** The finding that optimal weight decay is 0.8–3.2 (30× larger than the default 0.1) for data-constrained settings is empirical and specific. This result is documented through systematic hyperparameter search (Section 3, Figure 3 table) and is immediately actionable by practitioners in data-constrained settings.

3. **Ensemble beats parameter scaling is concretely demonstrated, not just claimed.** The result that a K=3 ensemble of 300M models outperforms the regularized recipe's asymptote (Section 4.2, Figure 4) is a clean empirical finding. Both sides use the same regularized hyperparameters, so the advantage is attributable to ensembling structure, not tuning differences.

4. **Distillation results ground the theoretical findings in practical benefit.** Distilling an 8-ensemble into a 300M student retains 83% of the ensembling gain (Section 6.1), and self-distillation enables a 300M student to match the regularized asymptote without ever training a larger model (Section 6.2). These results directly address the objection that the asymptote framework requires impractically large models.

5. **Downstream validation is held out until the end.** The authors state (Section 7) that they did not evaluate on any benchmark until after selecting recipes based on validation loss. This experimental discipline makes the 9% downstream improvement more credible as a genuine signal rather than a selected-in-hindsight result.

## Weaknesses

### Fatal

None.

### Major

1. **Headline quantitative claims (5.17× data efficiency) depend on nested power-law extrapolations from very few data points, with no uncertainty propagation.** The regularized recipe asymptote (3.43) is fitted from 4 parameter counts (150M, 300M, 600M, 1.4B — a 3-parameter fit with 1 degree of freedom). The ensemble member scaling law uses K ∈ {1, 2, 3, 5} (4 values), and the joint scaling recipe compounds this with a three-layer nested fitting procedure. The paper reports only run-to-run variance ("asymptotes vary by at most 0.02 loss across 3 seeds," footnote 2), which is not equivalent to confidence intervals on the fitted asymptote parameters themselves. If the asymptote estimates shift by even 0.02–0.05, the derived data efficiency ratios (2.29×, 5.17×) change noticeably. The paper does not bound this uncertainty, making the precise numbers look more precise than the evidence supports. **Why it matters:** The 5.17× figure is the most prominent number in the abstract and Figure 1, yet it is the product of speculative nested extrapolations. The paper's qualitative findings are robust, but the quantitative framing overstates precision.

2. **Ensemble member scaling extrapolation (K → ∞ from K ∈ {1,2,3,5}) is uncontrolled.** The paper fits a power law in K with only 4 values (K=1,2,3,5) to estimate the K→∞ loss asymptote. Since K=1 represents a qualitatively different regime (no ensembling), and there is no theoretical guarantee the power law holds at large K, the extrapolated asymptote (3.34) is speculative. The finding "even the K=3 ensemble outperforms the regularized recipe's asymptote" is robust and does not need this extrapolation, but the data efficiency numbers that depend on the K→∞ asymptote (3.03× for the ensembling recipe alone, and the joint 5.17× figure) are on weaker ground. **Why it matters:** The paper's headline quantitative claims depend on this extrapolation, while its qualitative claims do not. The paper should more clearly distinguish between direct measurements and extrapolations.

### Minor

1. **Experimental scale gap between the motivating regime and the evidence.** The paper motivates the problem with a future of trillions of tokens but conducts experiments at 200M–1.6B tokens. The paper acknowledges this and attempts to address it via data scaling laws (Section 5.3), but those laws themselves are fitted from only 4 token budgets (200M–1.7B) and then extrapolated. The claim that "our data efficiency wins will not disappear across all data scales" relies on the fitted asymptotes being similar across recipes, but with only 4 data points per fit and near-identical curves, the data cannot distinguish between constant efficiency and narrowing efficiency at larger scales. The paper should soften this claim.

2. **Joint scaling recipe uses heuristic hyperparameters rather than a tuned search.** Section 4.3 notes that for the ensemble members in the joint scaling recipe, the paper uses 2× epochs and 0.5× weight decay as a heuristic rather than a full hyperparameter search ("we cannot fully find locally optimal hyperparameters due to experimental constraints"). This means the estimated joint scaling asymptote may not represent the true optimum for the ensemble case. The paper acknowledges this but should flag it more prominently when presenting the 5.17× figure.

3. **Narrow downstream evaluation.** The downstream evaluation covers 3 benchmarks (PIQA, SciQ, ARC Easy). While these are appropriate for models at this scale per Thrush et al. (2025), the paper's claims about "generalization to downstream benchmarks" would be strengthened by a broader evaluation including, e.g., HellaSwag or WinoGrande at comparable scales. Additionally, the 9% improvement is relative to the best unregularized model, not the best regularized single model — this should be clarified.

4. **No accounting for the enormous compute cost of the proposed recipes.** The paper frames the setting as "no compute constraints," but the recipes are extremely compute-intensive: training a 1.4B model for 8 epochs on 200M tokens costs ~15× the compute of a Chinchilla-optimal model, and an ensemble of 5 such models costs 75×. The paper should acknowledge that these recipes impose substantial wall-clock and hardware requirements even if compute is not budget-constrained.

### Trivial

None.

## Nice-to-Haves

- **Add explicit uncertainty quantification for all power-law fits.** Reporting confidence intervals on asymptote parameters (A, α, E) — standard practice in scaling law papers — would allow readers to assess the precision of the headline 5.17× number.
- **Test ensemble scaling with at least one larger K value** (e.g., K=10 for the 300M ensemble) to validate whether the power-law extrapolation from K ∈ {1,2,3,5} holds or saturates.
- **Promote directly measured results to equal prominence with asymptote estimates.** The paper already has robust non-asymptote numbers (2.09× from the best 1.4B model at 200M tokens; 3.75× from the best 5-ensemble of 1.4B models) that could serve as the primary quantitative claims, with asymptote-based numbers presented as extrapolations.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"The hyperparameter search method is referenced only to the appendix"** (from the harsh critic's Missing Parts). The paper references Appendix C.1 for full details, which is standard practice for papers with space constraints. REMOVED because this is a common and acceptable formatting choice, not a weakness.
- **"The paper does not discuss why extreme weight decay works" / "Are there training stability issues?"** (from Section-by-Section Notes). The paper's contribution is empirical; a mechanistic explanation is beyond its scope, and there is no evidence of training instability in the reported results. REMOVED as speculative.
- **"The contradiction with Muennighoff et al. is not deeply analyzed"** (from Section-by-Section Notes). The paper notes the discrepancy and a likely cause (removal of overfit runs). A full reconciliation is a separate research question. REMOVED as scope creep.
- **"The abstract should flag the speculative nature of the 5.17× number"** — This is a presentation suggestion, now addressed in the Major weaknesses above. DEMOTED from standalone weakness.
- **"No compute cost accounting"** — The paper does acknowledge the setting is "no compute constraints"; the concern about wall-clock time is a practical note, not a methodological flaw. KEPT as Minor weakness 4 with softened framing.

## Novel Insights

None beyond the paper's own contributions. The reviewer's key observations — that the paper's qualitative claims are robust while the quantitative extrapolations are uncertain, and that the headline 5.17× figure would benefit from being reframed as an extrapolation with error bars — are well-taken but follow logically from the paper's methodology and do not constitute a novel analysis beyond what the authors and the review process produced.

## Suggestions

1. Reframe the abstract and Figure 1 to give equal or greater prominence to the directly measured data efficiency numbers (2.09× from the best 1.4B model, 3.75× from the best 5-ensemble) alongside the asymptote-based extrapolations.
2. Add confidence intervals or posterior predictive checks for all fitted scaling law parameters.
3. Soften the claim in Section 5.3 that data efficiency wins "will not disappear" given the limited token budgets used to fit the data scaling laws.
4. Clarify in Section 7 that the 9% downstream improvement is versus the best unregularized model, and consider adding 1–2 additional benchmarks.

## Score and Decision

<score>8</score>
<decision>Accept</decision>