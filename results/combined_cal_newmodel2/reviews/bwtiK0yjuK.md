Now I have all the information I need. Let me compile the final review.

## Summary

The paper studies offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs). It proposes a two-stage algorithm (seeded binary segmentation + low-rank tensor estimation via TH-PCA), establishes consistency guarantees for both the number and locations of change points, and derives limiting distributions for refined estimators — claimed to be the first such results for network data. A data-driven confidence interval construction procedure is also provided.

## Strengths

- **Novel problem formulation.** The paper tackles offline change point detection in D-MRDPGs, a setting genuinely unaddressed in prior work — the closest predecessors study the online setting for the same model (Wang et al., 2025) or the offline setting for single-layer networks (Wang et al., 2021). This is a clearly identified and occupied gap in the literature.

- **Theoretical depth.** The paper provides consistency guarantees for both the number and locations of change points (Theorem 1) and, notably, derives limiting distributions for the refined change point estimators (Theorem 2) in both vanishing and non-vanishing jump regimes. The claim that Theorem 2 is the first result of its kind for network data is credible. This is a substantial theoretical contribution that goes beyond the high-probability bounds typical in this area.

- **Method design coherence.** The two-stage architecture (seeded binary segmentation for coarse candidates, low-rank tensor estimation via TH-PCA for refinement) is well-motivated by the structure of the problem. Stage I is computationally efficient and handles multiple change points at multiple scales; Stage II leverages the low-rank Tucker decomposition of the expected CUSUM tensors to improve localization. The link between the tensor structure and the D-MRDPG model (equations (2)–(4)) is clearly laid out.

- **Confidence interval construction.** Section 3.1 provides a fully data-driven procedure for constructing CIs for change point locations — a practically useful capability that comparison methods do not offer, when the theory holds.

## Weaknesses

### Fatal
None.

### Major

1. **The baseline comparison in the main text is inadequate for the paper's headline empirical claim.** Table 1 compares only against gSeg and kerSeg — generic change point detection methods not designed for network data, multilayer networks, or the D-MRDPG model. Their poor performance is expected and does not demonstrate superiority over "state-of-the-art algorithms" as claimed in Section 1.1. The paper mentions comparisons against the relevant methods (Wang et al., 2025; Li et al., 2024) but defers these to Appendix G.1. The strong comparative claim in the abstract and contributions list is therefore unsupported by the evidence presented in the main text. *Verification: Section 4.1, lines 249-255: "we compare it to gSeg (Chen and Zhang, 2015) and kerSeg (Song and Chen, 2024)… We further conduct additional simulations…compare our approach with existing dynamic multilayer network approaches (Wang et al., 2025)…All results are reported in Appendix G.1."*

2. **The confidence intervals reported in the real-data analysis contain an anomaly that undermines the inference demonstration.** For the 2005 change point (time index 20), the 95% CI is (17.97, 18.05); for the 2013 change point (time index 28), the CI is (25.99, 26.06). Neither interval contains the detected change point. Since the CI construction formula (Step 4 in Section 3.1) is symmetric around the estimate η̂_k (CI = [η̂_k − q̂_{1−α/2}/κ̂_k², η̂_k − q̂_{α/2}/κ̂_k²], and by construction q̂_{α/2} = −q̂_{1−α/2} for the symmetric limiting distribution), this should not happen under a correct implementation. The CI widths (~0.04–0.08 time units) are also narrower than any CI in the simulation study (Table 2), despite the real data having fewer observations (T=35, n=75) than the simulations. This suggests either a computational error or a failure of the asymptotic approximation at this sample size. *Verification: Table 4 in Section 4.2; CI formula in Section 3.1 Step 4.*

3. **There is a structural gap between the theoretical guarantees and the practical implementation.** Algorithm 1 requires four mutually independent adjacency tensor sequences for its theoretical analysis. The paper states that in practice (and in all numerical experiments) the method uses "the same two split tensor sequences via the odd-even splitting approach" (line 89). Odd-even splitting of a single observed sequence produces dependent subsamples, and the paper does not establish that its theoretical guarantees (consistency, limiting distributions) hold under this scheme. *Verification: Algorithm 1 input (line 111); line 89; Theorem 1 condition.*

### Minor

4. **Table 1 reports all metrics as means over 100 Monte Carlo trials with no standard deviations, standard errors, or any measure of variability.** For metrics where competitors produce "Inf" values, variance is clearly high, but without any variability quantification for the proposed method, the reader cannot assess whether observed differences are meaningful relative to estimation noise.

5. **The coverage failure in Scenario 3 (76.67% at n=100, Table 2) receives an incomplete explanation.** The paper attributes this to "violations of Model 1 and relatively small, layer-specific changes," but Scenario 2 also violates Model 1 (changes community structure and number of communities) yet achieves 100% coverage. The inconsistency suggests the explanation is incomplete, and the practical utility of the CI procedure is unclear when coverage can drop well below nominal level without a clear diagnostic.

6. **No multiplicity adjustment is discussed for the confidence intervals.** Each CI is constructed at level 1−α independently for K detected change points; the joint coverage probability is substantially lower (for K=4, (0.95)^4 ≈ 81.5%).

7. **The assumption Δ = Θ(T) (Model 1(i))** requires the minimal spacing between change points to grow proportionally with T, ruling out settings with frequent change points (K growing with T). The paper acknowledges this in Section 5, but the main theoretical results depend on it.

### Trivial
None.

## Nice-to-Haves

- Validate the CI procedure on a simulation with parameters matching the real-data setting (n=75, T=35) to assess whether the narrow CI widths reported in Table 4 are plausible.
- Acknowledge the circular dependence in the CI procedure (CI width depends on κ̂_k, which depends on the estimated change points) explicitly.
- Report wall-clock times for the proposed method to complement the asymptotic complexity analysis.

## Removed Points

These points are flagged to be removed, treat them with caution:
- The criticism about the Stage I truncation factor of 64 being unexplained: valid but minor and not central to the evaluation; removed to keep the weakness list focused on substantive issues.
- The criticism that the real-data narrative is "post-hoc" and "forced": providing geopolitical context for detected change points is standard practice in this literature; removed as subjective.
- The criticism about Definition 5 not being fully specified in the main text (deferred to appendix): standard for papers with appendices.
- The "no comparison against simple threshold baseline" criticism: removed as a generic scope-creep request.
- The "computational cost not measured" criticism (only asymptotic complexity reported): wall-clock time is not a standard requirement for this type of theoretical paper.
- The criticism that the SNR condition's L^{1/2} term is unexplained: removed as a narrow technical detail about a derivation detail that space constraints naturally limit.
- Table 1 "empty cells" noted by reviewer: these are parser artifacts, not paper errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Move the relevant comparisons front and center.** Bring the comparisons against Wang et al. (2025) and Li et al. (2024) from the appendix into the main text, or alternatively, moderate the empirical claims in the abstract/introduction to match the evidence actually shown in the main paper.

2. **Investigate and correct the CI anomaly in Table 4.** If this is a computational error, it must be fixed. If the asymptotic approximation fails at T=35, acknowledge this limitation explicitly. Either way, add a simulation matching the real-data configuration (n=75, T=35).

3. **Address the theory-practice gap.** Either provide heuristic justification for why the odd-even splitting scheme preserves the theoretical guarantees, or reframe the theoretical results as applying to a cleaner (but idealized) data scenario, with the practical implementation treated as a heuristic extension.

4. **Add standard deviations or error bars to Table 1** to allow readers to assess the significance of performance differences.

5. **Discuss the multiplicity issue** for the confidence intervals, and consider a Bonferroni or simultaneous confidence band correction.

---

## Score and Decision

**Calibration summary:**

| Path | Avg score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| I5MquO1g7R.md (TV-HMM) | 4.75 | 1 | Yes | Weaker theory, similar experimental limitations |
| vjHCyOWc7h.md (MSBM) | 4.40 | 1 | Yes | Similar baseline issues, weaker theory |
| fwHVclv0ij.md (LLM detection) | 5.25 | 1 | Yes | No baselines, weaker theory |
| tra8ktyk0E.md (Dynamic similarity) | 5.50 | 2 | Yes | Cleaner experiments, less novel theory |
| i3T0wvQDKg.md (Conformal pred.) | 5.80 | 1 | No | Different domain, comparable rigor |

**Round 1 bracket:** The paper sits between 4.5 and 6.5 — stronger in theory than the 4.40–4.75 anchors but with empirical issues that prevent it from reaching the 6+ range of papers with cleaner evaluations.

**Round 2 narrowing:** Comparing to the dynamic similarity graphs anchor (5.50, tra8ktyk0E.md), our paper has stronger theoretical novelty (strength favorability 15.67 vs 14.10) but more problematic empirical issues (weakness favorability −2.78 for baselines vs −3.23 for incremental novelty). The CI anomaly (−2.78 favorability) is the dominant concern that prevents a score above 6.0.

**Final score justification:** The paper's theoretical contribution is genuinely strong and novel — the first limiting distribution results for change point estimators in network data, plus consistency guarantees for a new problem setting. However, the empirical evaluation has two significant problems: (1) the headline empirical claim is supported only by comparisons against generic baselines in the main text, and (2) the real-data confidence intervals contain an anomaly (CIs that don't contain their point estimates) that suggests either a computational error or a failure of asymptotic approximation at small sample sizes. The theory-practice gap regarding the independence assumption further limits the immediate applicability of the theoretical guarantees. These issues are fixable but as presented they prevent the paper from being accepted in its current form.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>