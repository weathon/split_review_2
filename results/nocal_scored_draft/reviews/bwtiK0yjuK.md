Now let me write the final consolidated review.

## Summary

This paper studies offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs), where at each time point a multilayer network is observed with shared node latent positions and time-varying layer-specific weight matrices. The authors propose a two-stage algorithm combining seeded binary segmentation with low-rank tensor estimation (TH-PCA), establish consistency for estimating the number and locations of change points, and derive the first limiting distributions for change point estimators in any network model. A data-driven confidence interval construction procedure is also provided.

## Strengths

- **Novel problem formulation (Section 2.1).** Offline change point detection in dynamic multilayer networks is genuinely underexplored. Prior work on D-MRDPGs (Wang et al., 2025) addresses only the online setting, and existing offline results are for single-layer networks. The D-MRDPG model (Definition 2, Model 1) cleanly separates shared latent positions from layer-specific weight matrices, making the change point problem well-posed.

- **Two-stage algorithm design (Section 2.2, Algorithm 1).** The architecture—seeded binary segmentation for coarse candidates, then refinement via TH-PCA—is natural and well-motivated. The overall computational cost O(T n² L r log²(T ∨ n)) is reasonable for the setting.

- **Theoretical depth and novelty.** Theorem 1 provides consistency for both the number and locations of change points. Theorem 2 derives limiting distributions for the refined estimators under both vanishing and non-vanishing jump regimes—as the paper correctly notes, the first such result in the network change point literature. The confidence interval construction (Section 3.1) is a practical deliverable that follows from this theory in a non-trivial way.

- **Empirical performance in simulations (Table 1).** Across all four scenarios, CPDmrdpg achieves lower error than gSeg and kerSeg on essentially every metric. The method remains competitive even in Scenarios 2 and 3 where Model 1 is violated, demonstrating robustness to model misspecification.

## Weaknesses

### Fatal
None.

### Major

- **Confidence intervals in the real-data example (Table 4) require clarification.** The table reports detected change points from Algorithm 1 (Stage II) alongside 95% confidence intervals constructed via Section 3.1. For the 2005 change point (t=20), the CI is (17.97, 18.05); for 2013 (t=28), the CI is (25.99, 26.06). These CIs do not cover the Stage II point estimates. The CI procedure (Step 4) constructs intervals around the *refined* estimator η̂_k from Equation (5), not the Stage II output, so a discrepancy is possible. However, the roughly 2-unit shift between the Stage II estimates and the CI midpoints, combined with very narrow interval widths (~0.06–0.08), is unusual and requires explanation. The paper should report the refined estimates explicitly alongside the Stage II estimates and verify that the CI construction is correct for this data. Since the CI procedure is presented as a headline contribution, this needs to be resolved.

- **Gap between theoretical independence assumptions and practical implementation (Lines 89, 111, 187, 211).** The theoretical guarantees (Algorithm 1, Theorems 1 and 2) require four mutually independent tensor sequences {A(t)}, {A'(t)}, {B(t)}, {B'(t)}. In practice, the paper acknowledges (Line 89) that only two sequences are used via odd-even splitting. This gap is described as "imposed for theoretical convenience," but the paper does not analyze whether the guarantees degrade gracefully under this relaxation. While such gaps are common in statistics papers, the absence of any theoretical or simulation-based analysis (e.g., comparing 2-split vs. 4-split implementations) is a limitation that weakens the link between theory and the reported experimental results.

### Minor

- **Baseline selection in the main paper is limited.** The main paper compares against gSeg and kerSeg—general-purpose change point detection methods for graph-valued or high-dimensional data. The closest network-specific competitor (Wang et al., 2025, operating on the same D-MRDPG model) and a deep-learning approach (Li et al., 2024) are mentioned but relegated to Appendix G.1. While the paper does include these comparisons (the appendix was stripped during PDF extraction), the main paper's claim of "substantially outperform[ing] existing state-of-the-art algorithms" relies primarily on comparisons against methods not designed for the multilayer network setting. Including the network-specific comparison briefly in the main paper would strengthen the empirical claims.

- **Suspiciously high CI coverage with narrow intervals in simulations (Table 2).** For Scenarios 1, 2, and 4 at n=100, the 95% CIs achieve 100% coverage with average lengths as small as 0.003. The combination of perfect coverage and extremely narrow intervals over 100 Monte Carlo trials is unusual for a nominal 95% procedure (under perfect calibration, P(coverage=100%) ≈ 0.006). While this could reflect very high SNR making the estimator near-deterministic, the paper does not report the actual SNR values realized in each simulation setting (the quantity under Assumption 2). Reporting these would help readers assess the difficulty level and interpret the coverage results.

- **Simulation results are near-perfect across multiple scenarios (Table 1).** Scenarios 1, 2, and 4 are essentially flawless at both n=50 and n=100. While Scenario 3 (n=50) shows meaningful error (|ΔK|=0.19, d(Ĉ,C)=9.64) indicating the method can be stressed, the paper would benefit from showing performance under systematically varied SNR to establish the practical boundary of applicability.

### Trivial
None.

## Nice-to-Haves

- An ablation study comparing Stage I alone vs. Stage I+II would empirically demonstrate the contribution of tensor-based refinement and verify the rate improvement claimed in Remark 1.
- Reporting standard errors (or standard deviations) alongside the means in Table 1.
- A sensitivity analysis for the TH-PCA rank parameters (r₁, r₂) would strengthen the practical guidance for users.

## Removed Points

These points from the input review were removed per filtering rules:

1. **CUSUM notational issue in Eq. (1):** "u ∈ [t][s]" and "u ∈ [e][t]" — This is a PDF parsing artifact, not an author error. Removed per formatting-artifact rule.

2. **"First" appearing three times is "unusually emphatic"** — A stylistic observation, not a substantive weakness. Removed.

3. **Criticism about gSeg's Inf values indicating poor fit rather than method strength** — The paper simply reports the comparison results as they are; this is a restatement of the data, not a misleading claim.

4. **Claim about competitors detecting "spurious change points" (Line 306) being misleading for gSeg** — The paper's statement at Line 306 refers to "their higher reverse distances d(C, Ĉ)" which applies to kerSeg (non-Inf values) as well. The characterization is imprecise for gSeg but not misleading enough to retain as a standalone weakness.

5. **Missing ablation for Stage I alone, rank sensitivity, variance reporting** — These are nice-to-have suggestions, not weaknesses. Moved to Nice-to-Haves.

6. **Missing related work** — Removed per hard rule (no external sources to verify).

## Novel Insights

Beyond the paper's own contributions, the reviews surface two observations. First, the gap between requiring four independent tensor sequences for theory and using two in practice is a recurring tension in change point detection: papers often prove results under data-splitting assumptions that are relaxed in implementation without formal robustness analysis. Second, the combination of 100% coverage and sub-unit interval lengths in Table 2 is unusual enough to warrant scrutiny—it either indicates that the estimator variance is essentially zero at these SNRs, or reveals a gap between the asymptotic approximation and finite-sample behavior that the authors should explicitly discuss.

## Suggestions

1. In Table 4, explicitly report the refined estimates (η̂_k from Equation 5) alongside the Stage II estimates and the CIs, and clarify whether the refinement substantially shifted the estimates.
2. Add a focused simulation or theoretical discussion addressing the 4-sequence vs. 2-sequence independence gap.
3. Report the realized SNR values (the quantity under Assumption 2) for each simulation scenario.
4. Include a brief comparison with Wang et al. (2025), adapted to the offline setting, in the main paper.
5. Show performance under systematically decreasing SNR (e.g., reducing jump sizes) to establish where the method begins to degrade.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>