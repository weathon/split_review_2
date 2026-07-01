Now I have a clear picture. Let me write the final review.

## Summary

This paper studies offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs), a setting not previously addressed in the literature. It proposes a two-stage algorithm combining seeded binary segmentation with low-rank tensor estimation (TH-PCA), proves consistency for the number and locations of change points (Theorem 1), and derives limiting distributions enabling confidence interval construction (Theorem 2). The distributional results are genuinely novel for network change point inference, and the confidence interval methodology provides a practical deliverable beyond point estimation.

## Strengths

1. **Novel problem formulation.** The paper is the first to study offline change point detection in dynamic multilayer networks under the MRDPG model. Single-layer offline (Wang et al., 2021) and multilayer online (Wang et al., 2025) methods exist, but the offline multilayer setting is new, and the paper correctly positions itself relative to these.

2. **Substantive theoretical contributions.** Theorem 1 establishes consistency for both the number and locations of change points. Theorem 2 derives limiting distributions for refined estimators in the vanishing-jump regime — genuinely the first such distributional result for network change point inference, going well beyond the high-probability bounds common in this literature. The result covers both vanishing and non-vanishing regimes (the latter in Appendix A).

3. **Principled algorithm design.** The two-stage structure (seeded binary segmentation for coarse candidates, TH-PCA tensor estimation for refinement) is well-motivated. The use of CUSUM transformations and explicit Tucker decomposition of the probability tensor creates a clean connection between the statistical model and the algorithmic steps.

4. **End-to-end data-driven confidence interval methodology.** Section 3.1 provides a fully specified procedure for constructing confidence intervals from data, going beyond point estimation.

## Weaknesses

### Major

None.

### Minor

1. **CI coverage results need more transparency.** Table 2 reports 100% coverage for Scenarios 1, 2, and 4 (n=100) with average interval lengths as small as 0.003 on a T=200 discrete time scale — narrower than a single time point. While strong signal in these scenarios can produce tight CIs, 100% coverage across 100 Monte Carlo trials with sub-unit-length intervals is remarkable and the paper does not report standard errors or distributions of CI lengths across trials. The degradation in Scenario 3 (76.67% coverage, length 1.528), which violates Model 1, provides partial validation that the method is not trivially perfect, but the other scenarios warrant more detailed reporting for full credibility.

2. **Theory-practice gap in data splitting acknowledged but unaddressed.** Algorithm 1 and Theorems 1–2 assume four mutually independent tensor sequences {A(t), A'(t), B(t), B'(t)}. The paper states (line 89) that in practice the procedure uses two split sequences via odd-even splitting and that this is "for theoretical convenience." While this practice is common in the change point literature (e.g., Wang et al., 2021 uses similar data-splitting conventions), the paper provides no argument — formal or heuristic — that the theoretical guarantees carry over to the practical implementation.

3. **CI procedure tested outside its theoretical regime.** The confidence interval procedure (Section 3.1) is justified by Theorem 2 for the vanishing-jump regime (κ_k → 0). The simulation scenarios use fixed (non-vanishing) jumps, so the CI procedure is applied as a robustness check beyond its theoretical justification. The paper does not explicitly flag this mismatch, leaving ambiguity about whether the reported coverage rates are backed by the theory.

4. **Baseline comparisons in the main paper are not the most informative.** The main paper's Table 1 compares against gSeg and kerSeg — generic graph change point methods not designed for multilayer networks and not designed for offline multi-change-point estimation. Their poor performance is expected. The more relevant comparisons (Wang et al., 2025; Li et al., 2024) are in Appendix G.1. Since the appendix is part of the submission, the evidence exists, but the main paper's evaluation as presented (claiming "substantially outperform[ing] existing state-of-the-art algorithms") rests on uninformative baselines unless the reader consults the appendix.

### Trivial

None.

## Nice-to-Haves

- Move the Wang et al. (2025) comparison into the main paper. If space is tight, the Frobenius-norm variants of gSeg/kerSeg could be trimmed.
- Report standard deviations or empirical distributions of CI lengths alongside coverage rates.
- Provide a brief heuristic argument that the theoretical guarantees for the four-sequence construction are preserved under odd-even two-sequence splitting.
- Explicitly note in the discussion of Table 2 that the CI procedure operates beyond its theoretical vanishing-jump regime in those simulations.
- Include a simple flattening baseline (e.g., averaging over layers then applying Wang et al., 2021) to isolate the value of explicit multilayer modeling.

## Removed Points

These criticisms from the input review were removed:

1. **"Real data evaluation provides no evidence of correctness"** — This criticism (that post-hoc rationalization of detected change points is not a valid argument) applies to essentially every change point paper performing real data analysis. It is a universal limitation of the setting, not a specific weakness of this paper. The paper's narrative linking detected points to geopolitical events follows standard practice. Removed as it does not distinguish this paper from any other.

2. **"Section-by-section notes" about Theorem 2 being limited to vanishing jumps and Δ = Θ(T)** — These limitations are explicitly acknowledged by the authors (Section 5: "Second, our inference procedure is limited to vanishing jumps"; line 65: "This assumption can be relaxed"). The paper openly discusses both as future work. These are known scoping decisions, not weaknesses.

3. **"Implausible" framing of CI results** — The original review called the CI results "suspicious" and said they "undermine rather than support." This framing is too strong given that (a) Scenario 3 shows realistic imperfect results, validating the method, and (b) tight CIs are expected in high-SNR settings. The concern is retained as a transparency issue (Minor weakness 1) but the "implausible/undermine" rhetoric is removed.

4. **CUSUM notation being unreadable** — This is a PDF-to-text extraction artifact, not an issue in the actual submission.

5. **Formatting nitpicks about SNR condition complexity** — This describes the content rather than identifying an actual weakness.

6. **"Only one real dataset in the main paper"** — A second dataset exists in Appendix G.2, making this incorrect as stated.

## Novel Insights

The review surfaces a productive tension: the paper's strongest selling point — providing the first limiting distribution results for network change point inference — coexists with a CI evaluation whose reported perfect coverage and sub-unit-length intervals in high-SNR scenarios invite skeptical scrutiny. The graceful degradation in Scenario 3 (which violates Model 1) partly validates the method, but the paper would benefit from more comprehensive reporting of estimator variability (standard errors, per-trial CI distributions) to fully substantiate the inference claims. The data-splitting gap between theory and practice, while standard in this subfield, is another area where a brief justification would strengthen an otherwise solid theoretical contribution.

## Suggestions

1. Add a panel to Table 2 showing the standard deviation of CI lengths across trials, or a histogram of CI centers and lengths for representative scenarios.
2. In the main paper, dedicate at least one row or table to the Wang et al. (2025) comparison, even if space requires trimming the Frobenius-norm variants of gSeg/kerSeg.
3. Add a remark in Section 2.2 or in the proof appendix that odd-even splitting preserves the independence structure needed for the theorems, or state the specific additional condition under which the two-sequence implementation is valid.
4. Explicitly note in the discussion of Table 2 that the simulation scenarios use fixed (non-vanishing) jumps, so the CI procedure operates as a robustness check beyond its theoretical regime.

## Score and Decision

**Round 1 bracket (initial):** 6.0 – 7.5

**Calibration anchors consulted:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| I5MquO1g7R (TV-HMM change point) | 4.75 | 1 | Weaker: same area (change point detection) but our paper has stronger theory (limiting distributions), clearer problem novelty, and more decisive empirical results |
| ILqA09Oeq2 (Multi-view clustering tensor) | 6.20 | 1 | Comparable: similar level of theoretical contribution (tensor methods), similar evaluation depth; our paper has a novel problem + inference results |
| p1TBYyqy8v (Spreading OOD on graphs) | 6.60 | 1 | Weaker empirical/theoretical comparison: graph-based but different problem; our paper has more novel theoretical results |
| P7KIGdgW8S (Graph stability) | 8.00 | 1 | Stronger: cleaner theoretical framing, no evaluation gaps |

The paper under review has genuine theoretical novelty (first limiting distributions for network change point inference) and a principled algorithm, placing it well above reject-range papers (scores 1–4). The weaknesses are about evaluation transparency and presentation, not about the core theory being flawed. It does not reach the 8+ tier because the CI evaluation needs more thorough reporting and the main paper's baseline choices are suboptimal. A score of **6.5** captures a solid accept: a paper with clear theoretical contributions whose evaluation, while directionally supportive, could better serve the claims.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>