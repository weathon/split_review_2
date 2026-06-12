## Summary

This paper proposes SCaSML, a framework that combines a pre-trained surrogate model (PINN or GP) with Multilevel Picard (MLP) Monte Carlo simulation to correct the surrogate's error at inference time without retraining. The core idea—the "Structural-preserving Law of Defect"—derives a defect PDE for the error that retains the original semi-linear structure, enabling existing stochastic solvers to refine the surrogate. Theoretical analysis proves a product-form error bound that yields an improved convergence rate, and experiments on four PDE families up to 160 dimensions show consistent error reductions.

## Strengths

1. **Well-motivated and technically sound core idea.** The observation that the defect PDE inherits the semi-linear structure of the original PDE (Fact 2.3) is an exact analytical identity, not an approximation. This cleanly separates surrogate training (coarse global approximation) from inference-time correction (targeted local refinement), and Section 2.2 explains this clearly.

2. **Meaningful theoretical error bound.** Theorem 2.5's product-form bound—final error ≤ (MLP simulation error) × (surrogate error)—is a clean structural result implying multiplicative improvement from either component. The improved scaling law (Corollary 2.6, from O(m^{-γ}) to O(m^{-γ-1/2})) is the paper's most distinctive theoretical contribution, backed by a proof sketch and rigorous appendix.

3. **Broad experimental scope.** Experiments span four PDE families (linear convection-diffusion, viscous Burgers, HJB/LQG, oscillatory diffusion-reaction) in dimensions up to 160, with two surrogate types (PINN and GP). Violin plots of error distributions and inference-time scaling curves provide more granular insight than aggregate tables alone.

## Weaknesses

### Major

1. **The "20-80%" error reduction claim in the abstract is not supported by the reported data.** Computing relative L² improvements from Table 1: LCD ranges 33-52%, VB-PINN 16-66%, VB-GP 43-58%, LQG 11-31%, and DR 7-21%. Several configurations fall below 20% (e.g., DR 160d at ~7%, LQG 160d at ~11%, VB-PINN 80d at ~16%), and no configuration reaches 80% (best is VB-PINN 20d at ~66%). The abstract and contribution list claim "20-80%" which overstates the results.

2. **The MLP baseline comparison uses different clipping thresholds without adequate justification for fairness.** Across three of four problem settings, the naive MLP and SCaSML use substantially different clipping thresholds (VB: 1.0 vs 0.01, 100×; LQG: 10 vs 0.1, 100×; DR: 10 vs 0.01, 1000×). The paper justifies this by noting the defect has smaller magnitude (lines 250-251, 296), which is physically plausible—but it still means the LQG naive MLP (relative L² error ~5.3-5.6) is essentially a failed solver due to under-stabilization. The paper states its *primary* comparison is SR vs SCaSML (line 224), and the MLP baseline is supplementary. Nevertheless, presenting a baseline whose clipping is an order of magnitude different from the proposed method's while claiming "SCaSML outperforms naive MLP" is misleading as presented.

### Minor

3. **No variance/error bars in the main results table.** Table 1 reports point estimates without standard deviations or confidence intervals. Since MLP and SCaSML are Monte Carlo methods, the variability of the estimates is essential information. The paper mentions "p ≪ 0.001" (deferred to Appendix G.4) but the main table should include error bars.

4. **Claimed experiment on "smaller PINN outperforming larger PINN" (contribution list, line 33) does not appear in the main text.** This is stated as a key finding but no corresponding experiment is presented in Sections 3.1–3.4. If present in the appendix, the main text should preview or summarize it.

5. **The scaling law experiment (Figure 4) has unclear budget accounting.** The x-axis is described as "number of collocation points (m)" for both the GP surrogate and SCaSML. The theory assumes 2m total evaluations (m training + m inference). If SCaSML uses 2m total while the GP uses m, the comparison is on unequal total budget. The slope comparison is about convergence rate—a structural claim—but the presentation should clarify the budget allocation.

6. **No sensitivity analysis for key hyperparameters.** The method depends on clipping threshold, number of MLP levels, and basis sample size M. The paper does not explore how results vary with these choices, which would help assess robustness.

### Trivial

- The LLM inference-time scaling analogy in the introduction (lines 15-21) is motivationally helpful but the parallel is loose—LLM inference-time compute (chain-of-thought, search) differs qualitatively from Monte Carlo path sampling. The paper does not rely on this analogy for its technical contributions.

## Nice-to-Haves
- Equalize clipping thresholds between MLP and SCaSML (or tune MLP separately with its own optimal clipping) and report the comparison, to strengthen the baseline discussion.
- Add standard deviations alongside point estimates in Table 1.
- Include the "smaller PINN outperforms larger PINN" experiment in the main text or clearly reference where it appears.
- Clarify the budget accounting in Figure 4 (is x-axis m training points or total 2m?).
- Add a sensitivity analysis for key parameters (clipping, M, number of levels).

## Removed Points
These points are flagged to be removed from consideration; treat them with caution:
- "SCa²SM¹ formatting is confusing" — this is a PDF parser artifact, not an author issue.
- "Section 2.3 is difficult to follow without the appendix" — structural feature of the submission; the appendix is stripped in parsing.
- "The MLP baseline on LQG with error > 5 does not provide useful information" — it is informative to show that pure simulation fails where the hybrid approach succeeds; this is a standard comparison in hybrid method papers.
- "The paper does not discuss when Assumption 2.4's regularity conditions are violated" — this is a reasonable scope choice; few papers discuss every possible assumption violation.
- The critic's speculation about the defect derivation being "overstated" as a contribution — while the algebraic step is straightforward, the contribution is in the *pairing* with MLP simulation, which is clearly stated. The paper acknowledges classical defect correction. This framing criticism is too harsh given the paper's stated contributions.

## Novel Insights
None beyond the paper's own contributions. The reviews converge on the paper's stated contributions (defect correction for PDE surrogates with MLP simulation, product-form error bound) and surface evidential concerns about the experimental evaluation rather than producing novel analytical observations about the method.

## Suggestions
1. Correct the "20-80%" claim in the abstract and contribution list to reflect the range actually observed (e.g., "7-66%" or "up to 66%"), or add experiments that reach higher improvements.
2. Add standard deviations or confidence intervals to Table 1—these are Monte Carlo methods and variance is essential information for the reader.
3. Either tune the naive MLP clipping threshold separately on each problem (with justification) or explicitly reframe the MLP comparison as illustrative and move the primary claims to the SR vs SCaSML comparison.
4. Provide a brief algorithmic sketch of MLP in the main text so Section 2.3 is more self-contained.
5. Clarify the budget allocation in Figure 4 and ensure the scaling law verification is on equal footing.

**Calibration anchors used:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| wUaOVNv94O (Auto Neural Spatial Integration) | 4.00 | R1 | Similar hybrid neural+MC control variate idea but simpler setting (integration, not PDEs), weaker theory. This paper is stronger. |
| 3ep9ZYMZS3 (HyPER surrogate correction) | 5.00 | R1, R2 | Similar hybrid surrogate+simulator correction, RL-based without comparable theory. Roughly comparable overall. |
| wVADj7yKee (SINGER high-dim PDE) | 6.33 | R1, R2 | Strong theory + high-dim PDE solving but cleaner experiments. This paper has comparable theory but weaker empirical validation. |
| 5rfj85bHCy (HyResPINNs) | 5.00 | R2 | PINN architecture modification, different type of contribution. |
| EP09OGPRzk (L-PINN) | 6.00 | R2 | PINN sampling method with theory, had similar experimental gaps (missing hyperparams, no error bars) but received 6.00. This paper's experimental issues are more substantive (overstated claims). |
| q4AEBLHuA6 (High-Freq PDE with GP) | 5.75 | R1, R2 | Comparable empirical scope. |

**Round 1 bracket: 4.0–6.5. Round 2 narrowed to 5.0–6.0.**

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>