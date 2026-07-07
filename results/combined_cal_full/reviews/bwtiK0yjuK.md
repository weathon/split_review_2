Now I have all the information needed. Let me write the final consolidated review.

---

## Summary

This paper studies offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs), a setting that is genuinely underexplored relative to single-layer or online counterparts. It proposes a two-stage algorithm combining seeded binary segmentation (Stage I) with low-rank tensor estimation via TH-PCA (Stage II), proves consistency for both the number and locations of change points (Theorem 1), derives limiting distributions in the vanishing-jump regime (Theorem 2), and gives a data-driven confidence interval construction procedure. Simulation studies against generic single-layer baselines show strong performance, and a real-data application to agricultural trade networks is presented.

## Strengths

- **Novel problem formulation.** Offline change point detection in dynamic multilayer networks (D-MRDPGs) is a genuine gap in the literature. Existing work focuses on single-layer networks (Wang et al., 2021; Padilla et al., 2022) or online settings (Wang et al., 2025), making the offline multilayer problem both underexplored and practically relevant. The paper correctly identifies this niche.

- **Well-motivated two-stage architecture.** The design of seeded binary segmentation for coarse candidate generation followed by low-rank tensor estimation (TH-PCA) for refinement is natural and computationally justified. The overall complexity \(O(T n^2 L r \log^2(T \vee n))\) is clearly stated.

- **Substantial theoretical analysis.** The paper provides consistency guarantees (Theorem 1), localization error rates, limiting distributions in the vanishing-jump regime (Theorem 2), and a data-driven confidence interval construction procedure. Deriving distributional theory for change point estimators in structured network models is technically demanding, and the paper makes a serious effort on this front.

- **Strong simulation results against generic baselines.** In Tables 1–2, CPDmrdpg substantially outperforms gSeg and kerSeg across nearly all metrics in four scenarios. The inclusion of Scenarios 2 and 3, which violate Model 1, demonstrates robustness beyond exact model assumptions. Near-perfect detection (e.g., \(|\hat{K}-K|=0\), 100% coverage) is achieved for several settings with \(n=100\).

## Weaknesses

### Major

- **Real-data confidence intervals are implausibly narrow without explanation.** In Table 4, the 95% CIs for change points in annual agricultural trade data span roughly 0.06–0.08 time units (e.g., time point 6: CI (5.97, 6.03); time point 20: CI (17.97, 18.05)). With only \(T=35\) annual observations and \(n=75\), claiming sub-annual localization precision is suspicious. It suggests either downward bias in the variance estimates from the multi-stage CI procedure (Step 2, Section 3.1), or a mismatch between asymptotic theory and the small \((T,n)\) of the real data. The paper provides no diagnostic — such as Monte Carlo calibrated coverage on synthetic data matched to these dimensions — to validate that the nominal 95% coverage is actually achieved under conditions resembling the real application.

### Minor

- **Mainline empirical comparison is against methods not designed for the problem, while the most relevant competitor is deferred to the appendix.** The paper compares against gSeg and kerSeg — generic single-layer graph change point detection methods. The closest competitor, Wang et al. (2025), addresses change point detection in the *same* D-MRDPG model (albeit online) and is compared against only in the non-visible Appendix G.1. While the offline/online distinction is genuine and the paper is transparent about this deferral, the claim of "substantially outperforming existing state-of-the-art algorithms" would be better supported by showing at least a summary of this comparison in the main text.

- **No theoretical guarantee that the CI procedure's variance estimators are consistent.** The confidence interval construction (Section 3.1) uses plug-in estimates \(\hat{\sigma}_{k,k'}^2\) computed from residuals within estimated segments. Given the multi-stage pipeline (change points estimated → probability tensors estimated within estimated segments → residuals computed → variances estimated), the potential for bias amplification is real. No theorem establishes consistency of these variance estimators, and the paper does not discuss this limitation. Table 2 already hints at trouble: coverage drops to 76.67% for Scenario 3 with \(n=100\).

- **The simulation study is limited in scope in the main text.** Only two node sizes (\(n=50,100\)), one time horizon (\(T=200\)), and one layer count (\(L=4\)) are tested. Since the theory allows all parameters to diverge, demonstrating scaling behavior over a wider range (e.g., varying \(T\) or \(L\)) in the main paper would strengthen the empirical case.

### Trivial

- Table 1 reports only means over 100 Monte Carlo trials without standard errors or other variability metrics.

## Nice-to-Haves

- Include a diagnostic for the real-data CIs: run the CI procedure on synthetic data matched to the real-data dimensions \((T=35, n=75, L=4)\) and report calibrated coverage.
- Either prove consistency of the variance estimators in Section 3.1, or explicitly state the absence of such a guarantee and discuss practical implications.
- Report standard errors alongside means in Table 1.

## Removed Points

These points from the original harsh review were removed per the filtering rules:

- **Equation (5) formula error.** The first sum in Eq. (5) reads \(\sum_{u=t+1}^t\), which is mathematically empty as printed. This is a PDF-parser formatting corruption — the intended form (almost certainly \(\sum_{u=\tilde{s}_k+1}^t\)) is clear from context and standard in the change-point inference literature. Removed as a parser artifact per hard rules.

- **Garbled notation in Definitions 4 and 5.** The nonstandard notations "\(u \in [t][s]\)" and the garbled scan statistic in Definition 5 are PDF-parser formatting corruptions. Removed per hard rules.

- **"First limiting distributions" claim weakened by vanishing-jump regime.** The reviewer argued the vanishing-jump regime is "arguably uninteresting," but this regime is standard in the change point literature — CUSUM-based inference typically requires vanishing jumps to obtain nondegenerate limits. The paper also explicitly defers non-vanishing results to Appendix A. This criticism is too harsh and does not reflect standard practice in this subfield.

- **Threshold selection criticism.** The remark that \(\tau\)'s theoretical upper bound depends on unknown \(\kappa^2\Delta\) is true but minor; the paper picks \(c_{\tau,1}=0.1\) and defers sensitivity analysis to Appendix G.1, which is common practice in change point papers.

- **Section-by-section notation nitpicks.** Nearly all are PDF-parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a diagnostic for the real-data confidence intervals: run the CI procedure on synthetic data matched to \((T=35, n=75, L=4)\) and report calibrated coverage. If coverage is far below 95%, discuss the implications and consider tempering the CI claims for small samples.

2. Move the comparison against Wang et al. (2025) from Appendix G.1 to the main text, or at minimum include a summary paragraph (e.g., a sentence reporting the key metrics) so that readers can evaluate the method against the closest prior work without accessing the appendix.

3. Either prove that the variance estimators \(\hat{\sigma}_{k,k'}^2\) in Section 3.1 are consistent (or cite conditions under which consistency holds), or explicitly acknowledge this gap and discuss how practitioners should interpret the resulting CIs.

4. Include standard errors or interquartile ranges in Table 1 to convey Monte Carlo variability.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| nSDOkm0SKo.md | 1.00 | R1 | No | Unrelated topic (financial news impact) |
| P49gSPmrvN.md | 1.00 | R1 | No | Unrelated topic (UMAP word embeddings) |
| bEgDEyy2Yk.md | 1.00 | R1 | No | Unrelated topic (minimax path problem) |
| 5lUdTogEL3.md | 1.00 | R1 | No | Unrelated topic (person re-identification) |
| 2NwHLAffZZ.md | 2.33 | R1 | No | Unrelated topic (linearization of learning systems) |
| kz78RIVL7G.md | 2.60 | R1 | No | Unrelated topic (adversarial attack detection) |
| Y93F5eNmZG.md | 3.00 | R1 | Yes | LPPLS critical points. Had core methodological flaws: weak architecture, unconvincing experiments, heavy negatives (-10.62, -11.06). This paper is substantially stronger. |
| S3zKrEQpRr.md | 3.00 | R1 | Yes | GNN communication channels. Had severe flaws: unrealistic assumptions, unfair comparisons, negative weights up to -13.74. This paper is substantially stronger. |
| xw3fStKCwm.md | 3.75 | R1 | No | Unrelated topic (tensor-train point cloud compression) |
| I5MquO1g7R.md | 4.75 | R1 | Yes | TV-HMM change point detection. Had heavy negatives: no improvement over competitors (-5.70), limited experiments (-5.48), unclear writing (-6.33). This paper has stronger theory and no comparable severity of weakness. |
| SJ9lqUalq1.md | 5.25 | R1 | No | Tensor deflation — different problem but similar theoretical depth |
| l18hiEXRJS.md | 4.50 | R1 | No | Data shift detection via activation graphs |
| ILqA09Oeq2.md | 6.20 | R1 | Yes | Multi-view clustering under nested matrix-tensor model. Strong theory (+7.18 on top item). Had moderate negatives: insufficient comparisons (-3.81, -3.24), no real data (-0.70). Comparable in theoretical ambition; this paper has real data but with suspicious CIs. |
| eN0RyRVbSm.md | 6.50 | R1 | No | Double descent — unrelated topic |
| p1TBYyqy8v.md | 6.60 | R1 | No | Graph OOD detection — different problem |
| sIcPMMhl9W.md | 5.80 | R1 | No | Shuffled regression — unrelated |
| A3YUPeJTNR.md | 8.00 | R1 | No | Prediction-driven allocations — unrelated |
| EUSkm2sVJ6.md | 7.60 | R1 | No | Data usage inference — unrelated |
| KbetDM33YG.md | 8.00 | R1 | No | Online GNN evaluation — unrelated |
| cJs4oE4m9Q.md | 8.00 | R1 | No | Anomaly detection — unrelated |

**Round 1 bracket:** 5.0 – 6.5.

**Score justification:** The paper's two heaviest positive weighted items (theoretical depth +4.68, simulation results +5.04) are genuine strengths that the TV-HMM anchor (4.75) does not match — that anchor had no comparable positive weights and had multiple severe negatives. However, this paper is weaker than the tensor clustering anchor (6.20), which had a top strength item at +7.18 and whose negatives (insufficient comparisons -3.81, -3.24) are similar in magnitude to this paper's top negative (real-data CIs -3.30). The real-data CI issue is a genuine concern that prevents a higher score, as the implausibly narrow intervals are not adequately explained or diagnosed. The paper's core theoretical contribution is solid, but the empirical validation has gaps that need addressing before the paper's claims about inference reliability can be fully trusted.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>