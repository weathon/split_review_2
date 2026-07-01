Now I have a thorough understanding of the paper. Let me produce the draft review.Now let me proceed to calibration. The paper is about change point detection/inference in dynamic multilayer networks with tensor methods and limiting distributions.Let me read a few key anchors to calibrate more precisely.Now I have enough information to finalize the calibration and produce the final review. Let me summarize my findings:

**Round 1 Bracket:**
- The paper is clearly above the 4.75 rejected change point detection paper (I5MquO1g7R), which showed no improvement over competitors and had limited theoretical novelty.
- The paper is comparable to or stronger than the 6.20 accepted tensor theory paper (ILqA09Oeq2), which had good theory but less practical impact.
- The paper has genuine first-of-its-kind results, strong empirics, and a well-designed practical method.
- The theory-practice gap is the main concern but is standard in the literature and doesn't invalidate the core results.

**Initial bracket: 6.5–7.5**

The paper's main strength (first limiting distributions for network CP estimators + practical CI procedure + decisive empirical advantage) puts it firmly above borderline accept, but the theory-practice gap for its headline CI contribution and limited simulation diversity prevent it from reaching a clear 8.

---

## Summary
This paper proposes a two-stage algorithm for offline change point detection in dynamic multilayer random dot product graphs (D-MRDPGs), combining seeded binary segmentation with tensor-based low-rank estimation. Its primary novelty is deriving the first limiting distributions for change point estimators in network data (Theorem 2), enabling confidence interval construction via a data-driven procedure.

## Strengths
- **First limiting distributions for network change point estimators (Theorem 2, Section 3):** The derivation showing convergence to the argmin of a two-sided Brownian motion process with heterogeneous variance parameters σ_{k,k} and σ_{k,k+1} is a genuinely novel result in network statistics. No prior work has established such distributional results for change point estimators in network data.
- **Strong empirical dominance (Table 1):** CPDmrdpg achieves near-perfect localization across all four scenarios (e.g., |K̂ − K| = 0.00 in Scenarios 2 and 4 at n=100), while gSeg fails catastrophically (Inf Hausdorff distances, |K̂ − K| ≈ 5 in Scenario 4) and kerSeg consistently produces higher localization errors.
- **Theoretically justified algorithm design (Equations 2–4):** The Tucker decomposition structure naturally justifies TH-PCA in Stage II—expected CUSUM tensors factor through the shared latent position matrix X and time/layer-varying weight matrices, making the tensor estimation structurally principled rather than heuristic.
- **Robustness beyond stated assumptions:** The method performs excellently in Scenarios 2 and 3 which violate Model 1, demonstrating practical robustness beyond the theoretical guarantees.
- **Interpretable real-data analysis (Section 4.2):** Detected change points (1991, 1999, 2005, 2013) align with well-documented geopolitical events (Soviet dissolution, WTO conferences, Bali Package), and the paper convincingly argues that competitor detections are less plausible.

## Weaknesses

### Fatal
None

### Major
- **Theory-practice gap for independence assumption** — Theorem 2 formally requires four mutually independent adjacency tensor sequences, but the implementation uses only two sequences via odd-even splitting (Section 2.2: "imposed for theoretical convenience"). Since the limiting distribution is the paper's primary novel contribution and confidence intervals depend on it, the CIs are justified only under a stronger independence condition than what the procedure satisfies. No heuristic argument or empirical validation of this gap's impact on coverage is provided. This matters because the CI procedure is the headline contribution.

### Minor
- **CI undercoverage in Scenario 3 (Table 2)** — Coverage drops to 76.67% at n=100, nearly 20 points below nominal 95%. The paper's explanation (model violations and small layer-specific changes) is incomplete, since Scenario 2 also violates Model 1 yet achieves 100% coverage. This suggests the CI procedure may be fragile when signal is concentrated in a small part of the tensor structure, but this regime is not characterized.
- **Single time horizon (T=200) in all simulations** — It is impossible to assess how performance scales with T or whether the theoretical rate O(κ_k^{-2} log T) manifests empirically. Varying T is standard practice for validating asymptotic theory.
- **Main-text comparisons limited to general-purpose methods** — Only gSeg and kerSeg (which don't exploit multilayer tensor structure) appear in the main text. Comparisons with the more relevant network-specific methods (Wang et al., 2025; Li et al., 2024) are in Appendix G.1, making it harder to assess the method's relative contribution against appropriate baselines.

### Trivial
None

## Nice-to-Haves
- Empirically validate the two-sequence vs. four-sequence gap (e.g., a simulation comparing CI coverage under both implementations).
- Relax Δ = Θ(T) with formal theoretical guarantees for growing K.
- Vary T systematically (e.g., {100, 200, 500, 1000}) to demonstrate convergence rates empirically.
- Provide more intuition for the extremely narrow real-data CIs (width ~0.06 for T=35) so practitioners can assess when such precision is realistic.
- Characterize empirically which signal structures (dense vs. sparse in the tensor) lead to CI undercoverage.

## Removed Points
These points are flagged to be removed, treat them with caution:

- **Δ = Θ(T) as a structural flaw:** The paper explicitly scopes this (Model 1(i)) and acknowledges it as a limitation in Section 5, noting relaxation via narrowest-over-threshold with simulations in Appendix G.1. This is a stated scope limitation, and the current theory is correct under its stated conditions. Removed because criticizing a paper for not also solving a harder problem it explicitly scopes out is scope creep.
- **Assumptions 1(ii)-(iii) not directly verifiable:** The paper acknowledges this ("common in tensor-based models") and provides context for what the conditions mean. This is standard practice in the tensor literature and not a specific deficiency of this paper.
- **1/64 trimming constant unmotivated:** This is a minor algorithmic constant common in seeded interval methods; it does not affect the core contribution.

## Novel Insights
The paper's central novel insight is that change point inference in dynamic multilayer networks admits a two-sided Brownian motion limiting distribution with heterogeneous variance parameters that capture the asymmetry between pre- and post-change regimes. This connection—from multilayer network tensor structure through Tucker decomposition to a practical confidence interval procedure—has not been established before in the network statistics literature. The result bridges a gap between the well-developed theory of limiting distributions for change points in classical settings and the network change point detection literature, where previously only consistency results existed.

## Suggestions
- Provide a simulation comparing four-sequence vs. two-sequence implementations to empirically validate that the CI coverage is not substantially affected by the independence assumption violation.
- Bring at least a summary of the Wang et al. (2025) and Li et al. (2024) comparisons into the main text—these are the most relevant prior works.
- Vary T across multiple values in simulations to demonstrate that the theoretical localization rate O(κ_k^{-2} log T) matches observed behavior.
- Add a brief discussion characterizing when the CI procedure performs poorly (e.g., as a function of signal structure across layers), guiding practitioners on reliability.

## Score and Decision

**Calibration Anchors:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| I5MquO1g7R (CPD via TV-HMM) | 4.75 | 1 | Rejected CPD paper with no empirical advantage over competitors and limited novelty; paper under review is substantially stronger on both theory and experiments |
| e0bdvNsgcF (A-Loc tensor methods) | 2.50 | 1 | Rejected tensor paper; not comparable in quality |
| t5kThOYtxn (Stable batched bandit) | 4.20 | 1 | Rejected inference paper with weak contributions; paper under review has much stronger novel results |
| ILqA09Oeq2 (Multi-view clustering tensor) | 6.20 | 1 | Accepted tensor theory paper with good but narrow contribution; paper under review has comparable or greater impact with both theory and practice |
| O6znYvxC1U (Bayesian neural kernel) | 6.33 | 1 | Accepted theory paper; paper under review is comparable in novelty |
| xljPZuprBA (Edge probability graphs) | 5.75 | 1 | Rejected graph model paper; paper under review is stronger with clear practical utility |
| sIcPMMhl9W (Shuffled regression) | 5.80 | 1 | Rejected theory paper; paper under review has stronger experimental validation |
| EUSkm2sVJ6 (Dataset usage inference) | 7.60 | 1 | Accepted paper with strong experimental validation; paper under review has more theoretical depth but slightly weaker experimental diversity |

**Round-1 bracket:** 6.5–7.5

**Final reasoning:** The paper makes a genuinely novel first-of-its-kind theoretical contribution (limiting distributions for network CP estimators), demonstrates decisive empirical superiority, and provides a practical methodology. It clearly exceeds the 6.2 tensor theory paper in scope (theory + method + experiments). The main weakness (theory-practice gap for CIs) is real and affects the headline contribution, but is a common pattern in statistics papers and is addressable. The limited experimental diversity (single T, general-purpose baselines in main text) is minor. Overall, this is a solid contribution that sits at 7.0—above borderline accept but not quite at clear accept (8) due to the unresolved CI reliability question.

**Score: 7.0**

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>