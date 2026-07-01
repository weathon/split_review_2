Now let me produce the final consolidated review.

## Summary

This paper reframes pre-training from compute-optimal scaling to a data-constrained, compute-abundant regime, asking what recipes work best when data is fixed but compute is not. Using a 200M-token DCLM seed corpus, the authors show that standard recipes (increasing epochs and parameters) overfit, and demonstrate that tuning weight decay to ~30× larger than default enables monotonic loss improvement following a 1/N power law. They then show ensembling (K independently trained 300M models) achieves a lower loss asymptote (3.34) than parameter scaling (3.43), and that composing both via a joint scaling recipe is estimated to yield 5.17× data efficiency over the standard baseline. The paper further shows distillation can compress these gains and that validation loss improvements transfer to downstream benchmarks (PIQA, SciQ, ARC Easy) with a 9% average improvement.

## Strengths

- **Well-motivated and timely problem framing.** The paper explicitly identifies the tension between compute scaling (4×/year) and web data growth (1.03×/year) and reframes pre-training around the question "how should one pre-train under fixed data and no compute constraints?" This asymptotic evaluation framework is novel and likely to become increasingly relevant.
- **Actionable finding about weight decay (Section 3, Figure 3).** The discovery that optimal weight decay is ~30× larger than the default 0.1 for over-parameterized, data-constrained models is specific, clearly demonstrated, and practically useful. The tuning enables monotonic loss improvement in N (Figure 3, purple line) where the standard recipe plateaus, with the power law fit (0.05/N^1.02 + 3.43) exhibiting exponent ~1, notably different from Chinchilla's 0.34.
- **Ensembling beats parameter scaling at the asymptote (Section 4, Figure 4).** The finding that an ensemble of small models achieves a lower loss asymptote (3.34) than a single large model (3.43) under infinite total parameters, and that even a 3-ensemble outperforms the regularized asymptote, is a non-trivial empirical result with direct implications for compute allocation under fixed data.
- **Self-distillation works without collapse (Section 6.2, Figure 8).** The result that self-distillation (300M teacher → 300M student) improves loss over the teacher, matching the regularized asymptote (3.43) without ever training a large model, is genuinely surprising given the recent "model collapse" literature, and is well-supported by the theoretical framing in Allen-Zhu and Li (2023).
- **Downstream validation (Section 7, Figure 9).** The paper verifies that validation loss improvements transfer to PIQA, SciQ, and ARC Easy with a 9% average improvement, and notably evaluated on benchmarks only after selecting recipes by validation loss — a strong methodological choice that strengthens the validity of the downstream results.

## Weaknesses

### Fatal
None.

### Major

- **Precision of asymptote estimates is overstated given limited data points and no uncertainty quantification on extrapolation.** The paper's central quantitative claims (3.43, 3.34, 3.17 asymptotes; 5.17× data efficiency) depend on fitting power laws of the form A/N^α + E to only four data points (N = 150M, 300M, 600M, 1.4B). This is a 3-parameter fit with 1 degree of freedom per regression. The asymptote E is the most uncertain parameter because it extrapolates far beyond the observed range — the data span about one order of magnitude in N, while the asymptote is the limit at N → ∞. The only uncertainty analysis mentioned (Appendix I.1, 0.02 variance across 3 seeds) measures run-to-run variance of the observed points, not the uncertainty in the functional form or extrapolation. The 5.17× figure compounds uncertainty through a cascade of three nested fits (K → ∞ per N → power law in N → data scaling law in D) with no error propagation reported. **The directional findings are robust** (regularization helps, ensembling helps further, they compose) — and indeed the paper already reports non-extrapolated data efficiency numbers of 2.09× and 3.75× (Section 5) that do not rely on asymptote extrapolation. But the precise magnitudes, especially the headline 5.17× figure, carry substantially more uncertainty than the paper conveys.

### Minor

- **Joint scaling recipe asymptote (3.17) uses heuristic rather than optimally tuned hyperparameters.** Section 4.3 acknowledges that "we cannot fully find locally optimal hyperparameters due to experimental constraints" and instead uses the heuristic of taking the optimal regularized hyperparameters with 2× epochs and 0.5× weight decay. This means the 3.17 asymptote and derived 5.17× data efficiency figure are estimates of a *specific heuristic recipe's* performance, not the best possible joint scaling under optimal tuning. The paper does not quantify how far this heuristic is from optimal. A validation against a small grid search for even one (N, K) combination would help bound this gap.
- **Framing of Muennighoff "contradiction" and "standard recipe" is slightly overstated.** The paper claims to "contradict" the scaling law in Muennighoff et al. (2023) (line 58), but Muennighoff's law was fit to epoch counts up to 4, while overfitting in Figure 2 becomes severe at 128 epochs — far outside the law's applicable range. Additionally, the "standard recipe" comparison excludes weight decay tuning entirely (weight decay of 0, per Table 3), making the comparison partially about tuning vs. not tuning rather than a fundamental failure of existing approaches. Softening this language would better reflect the evidence.
- **Convergence rate to asymptote is not contextualized for finite compute budgets.** The paper evaluates recipes by their asymptotic loss (N → ∞), which is the correct framing for its stated scope. However, a recipe with a lower asymptote but slower convergence could be worse at any given finite budget. For the regularized recipe (exponent ≈ 1), getting from the 1.4B-model loss of ~3.46 to within 0.01 of the 3.43 asymptote requires N ≈ 4B+ parameters. A brief discussion of convergence rates (e.g., "the regularized recipe reaches within 0.01 of its asymptote at N = X") would help readers calibrate practical tradeoffs.

### Trivial

- **Limited downstream benchmarks.** Three relatively simple benchmarks (PIQA, SciQ, ARC Easy) are appropriate for the model scale, but the paper could acknowledge that correlation with more complex tasks at this scale is not guaranteed.
- **No discussion of actual compute costs (GPU-hours).** While the paper studies "infinite compute," reporting compute costs for the largest runs would help readers calibrate what "infinite" means in practice.

## Nice-to-Haves

- Add bootstrap confidence intervals or leave-one-out analysis for all power law fit parameters, especially the asymptotes. Propagate uncertainty through the nested fit cascade for the 5.17× data efficiency figure.
- Validate the joint scaling heuristic (2× epochs, 0.5× weight decay) against a small grid search for at least one (N, K) combination.
- Expand the discussion section to briefly address how quickly each recipe approaches its asymptote at finite budgets, with concrete examples.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"40× larger than Chinchilla" needs clarification** — The paper consistently uses 140× (verified via grep; the critic appears to have misread). Factually incorrect criticism; removed.
- **General speculative concerns about whether the metric measures a proxy** — Purely hypothetical concerns without specific textual anchor in the paper; removed.
- **Criticisms about missing appendix content (proofs, details)** — The parser strips the appendix from all papers; this content exists in the original submission; removed per hard rule.
- **Weaknesses that question whether cited models/tools exist or are released** — Paper references DCLM (Li et al., 2025), Muennighoff et al. (2023), etc. Per hard rules, these are assumed to exist; removed.
- **"No error propagation for the 5.17× figure"** — Already subsumed under the Major weakness about precision of asymptote estimates; merged rather than listed separately.

## Novel Insights

The merger of the two review lenses surfaces an important nuance: the paper's headline quantitative claims involve more epistemic uncertainty than the presentation suggests, yet the core empirical phenomenon — that simple regularization and ensembling yield large, reliable improvements under data constraints — is robust and demonstrable even without any extrapolation. The most actionable insight for authors is not that any finding is wrong, but that the *precision* of the headline numbers could be meaningfully improved with standard uncertainty quantification methods. The self-distillation result (Section 6.2) stands out as the most surprising and theoretically interesting finding, and its connection to Allen-Zhu and Li (2023) is well-articulated.

## Suggestions

1. **Add uncertainty quantification.** Bootstrap confidence intervals on all power law asymptotes (and propagate through the nested cascade for the 5.17× figure) would transform the headline numbers from "precise but unverifiable" to "estimates with known uncertainty." The infrastructure (3 seeds in Appendix I.1) already exists.
2. **Validate the joint scaling heuristic.** A small grid search over hyperparameters for at least one (N, K) combination would bound the gap between heuristic and optimal tuning for the 3.17 asymptote.
3. **Softens the Muennighoff framing.** Replace "contradict" with a more nuanced description that acknowledges the boundary condition on the law's applicable range.
4. **Add convergence rate discussion.** Briefly show how far from the asymptote each recipe sits at the largest tested parameter count, with a concrete example of the compute required to approach the asymptote.

## Score and Decision

**Calibration anchors used:**

| Anchor Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/xGM5shdGJD.md` (Hitchhiker's Guide) | 5.20 | R1 | Similar topical area (scaling law estimation methodology). The hitchhiker's guide paper is purely methodological; current paper has stronger empirical findings and a clearer novel contribution but shares similar concerns about evidential rigor. Current paper is stronger. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iZeQBqJamf.md` (Language models scale reliably with over-training) | 6.50 | R1 | Similar in character: both study scaling laws in a practically relevant regime (over-training / data-constrained), both have clear motivation and solid empirical work, both have addressable methodological concerns. Very comparable quality. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/o9YC0B6P2m.md` (Scaling Law with LR Annealing) | 6.75 | R2 | Novel scaling law formulation with theoretical concerns about invariance properties. Rejected despite high avg score due to split opinions. Current paper's weaknesses are less fundamental. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wg1PCg3CUP.md` (Scaling Laws for Precision) | 8.00 | R1 | Cleaner methodology and fewer concerns. Current paper has more surprising findings but less methodological rigor in one key area (uncertainty quantification). Current paper is weaker. |

**Round 1 bracket:** 5.5–7.5

**Round 2 narrowing:** The paper is clearly above the Hitchhiker's Guide (5.20) — it has a genuinely novel problem framing and more actionable empirical findings. It is comparable to the over-training paper (6.50), both in quality and in the nature of its weaknesses (both have addressable methodological concerns). It is below "Scaling Laws for Precision" (8.00), which had cleaner execution. The most appropriate range is 6.0–7.0.

**Final score:** 6.5 — The paper makes a genuine contribution with a timely problem framing, novel asymptotic evaluation framework, and robust directional empirical findings. The main weakness (overstated precision of asymptotic estimates) is real and non-trivial but does not invalidate the core claims, and is addressable in revision. The paper sits at a solid borderline-accept level: it has the novelty and empirical substance to warrant acceptance, with the expectation that the authors add proper uncertainty quantification to the headline numbers.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>