## Summary

This paper proposes STBP, a framework for continual spatio-temporal forecasting (CSTF) that combines a frozen frequency-domain backbone (FreNet + Dual-Stream Linear Graph Attention) with an expandable contextual pattern bank. The backbone captures stable spatio-temporal patterns via frequency analysis and models dynamic spatial correlations with O(N) linear attention; the pattern bank is incrementally expanded and fine-tuned while the backbone stays fixed, addressing the stability-plasticity trade-off. Experiments on three real-world streaming datasets show STBP outperforming existing CSTF methods.

## Strengths

1. **DLGA is a genuine architectural contribution.** Incorporating the pattern bank embedding P<sub>τ</sub><sup>(2)</sup> as an additional key stream within a linear attention mechanism (Eq. 9) is elegant: it lets the model attend to stored knowledge without quadratic complexity. The reformulation φ(Q)(φ(K)ᵀV + φ(P<sub>τ</sub><sup>(2)</sup>)ᵀV) preserves O(N) complexity while adding the pattern-stream term — a clean integration of continual learning and efficient spatial modeling.

2. **Strong empirical results against CSTF baselines.** On PEMS-Stream and CA-Stream, STBP reduces MAE by **21.44%** and **21.93%** over the best CSTF baseline (EAC). Critically, these percentage claims are computed against *CSTF methods*, not against retrained STGNNs. The few-shot results (Table 2) are also impressive: STBP (13.58 MAE) notably outperforms EAC (16.13 MAE) on PEMS-Stream 10%.

3. **Architecturally principled design.** The separation of a frozen backbone (general, stable patterns via frequency-domain extraction) from an expandable pattern bank (node-level adaptation via gating and dual-stream attention) is clean and well-motivated. The paper correctly targets the stability-plasticity dilemma that prior CSTF methods address less effectively.

4. **Qualitative evidence for pattern bank structure.** The t-SNE analysis (Figure 6) shows the pattern bank evolving from chaotic initialization to well-separated clusters, with new nodes assigned to existing clusters — supporting the claim that the pattern bank captures meaningful node-level heterogeneity rather than mere overfitting.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **No analysis of AIR-Stream's marginal improvement.** The improvement on AIR-Stream is only 2.35% (MAE) — an order of magnitude smaller than on the two traffic datasets. AIR-Stream has different temporal dynamics (hourly sampling vs. 5-minute), different periodicity structure, and a different domain (air quality vs. traffic). The claim of "strong continual learning capabilities" is weakened when one of three datasets shows only marginal gains, yet the paper offers no discussion of why. The paper should analyze potential reasons: does the frequency-domain approach underperform on data with less pronounced periodicity? Does the pattern bank interact differently with hourly sampling?

2. **EAC presented alongside ablation variants.** Figure 4 and the ablation table include EAC as one of six variants alongside "Retrain," "Online," "w/o Backbone," and "w/o DLGA." The text (line 244) explains it is included "for comparison in the ablation study," but visually grouping a separate published method with component-removal variants is misleading. EAC already appears in the main results (Table 1); it should be clearly separated from the component ablations.

3. **Efficiency analysis lacks concrete numbers.** Figure 8 does show average training time (s/period) on the x-axis and GPU memory (GB) in the toy-dataset bar chart, so some quantitative data exists in the figure. However, the text reports no specific numbers — only qualitative statements ("minimal overhead," "maintains SOTA even under drastic graph expansion"). Reporting exact training time and peak memory for real datasets would make the efficiency claim evaluable.

4. **"Privacy protection" claim is unsupported.** Line 104 states the method "offer[s] advantages in privacy protection" because the pattern bank encodes abstractions rather than raw data. This is a plausible logical consequence but is not validated by any experiment or analysis. Either demonstrate it or remove the claim.

5. **Limited hyperparameter sensitivity.** The only sensitivity analysis is on the feature dimension d (Figure 5). Sensitivity to learning rate during the fine-tuning-only phase, number of gradient steps per incremental period, or other training hyperparameters is not discussed — these matter for reproducibility.

### Trivial

- The gating function in Eq. 5 uses elementwise multiplication without specifying broadcasting semantics for P<sub>τ</sub><sup>(0)</sup> and P<sub>τ</sub><sup>(1)</sup> relative to H<sub>τ</sub>.
- The linear attention description says "Softmax used for approximation" (line 130) without specifying the exact random feature map φ in the main text (deferred to appendix).

## Nice-to-Haves

- Include a version of conventional STGNNs (GWNet/STID) with a reasonable continual learning adaptation (e.g., fine-tuning with weight initialization from the previous period or a small replay buffer) to confirm the performance gap is not solely an artifact of the evaluation protocol. This is not a current weakness — the paper follows the established protocol from prior work (Chen & Liang, 2025) — but it would strengthen the narrative.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **Criticism that STGNN comparison is structurally unfair (from Harsh Critic's "Critical Issue #1").** REMOVED — verified against the paper. The 21.44% and 21.93% improvement claims are computed against EAC (the best CSTF baseline), not against retrained STGNNs. The paper clearly states "STGNNs... rely on static graph assumptions and are not designed for continual learning" (line 187) and follows the evaluation protocol established by prior work (Chen & Liang, 2025). The STGNN results are contextual motivation, not the primary competitive comparison. The critic conflated two separate comparisons.

2. **"No statistical comparison of CSTF variants."** REMOVED — standard deviations from 3 seeds are reported, which is standard practice. Statistical significance testing is not standard for these benchmarks.

3. **Criticism about missing appendix content or proofs.** REMOVED per instructions — appendix sections exist in the original submission; the parser strips them.

4. **Strength about "well-defined problem" or "important problem."** REMOVED — generic praise about problem importance, not specific to this paper's contribution.

5. **"Weak ST modeling" framing from harsh critic's section notes.** REMOVED — the critic acknowledged some CSTF methods use non-trivial backbones, but this is a minor framing issue that does not affect the paper's validity.

6. **Request for more baselines (2023-2024).** REMOVED — the paper already compares against state-of-the-art CSTF methods including EAC (2025). This is a generic request without specific missing baselines identified.

## Novel Insights

None beyond the paper's own contributions. The reviews surface no contradiction, alternative interpretation, or overlooked implication that changes how the contribution should be understood.

## Suggestions

1. Add a brief analysis section discussing why the AIR-Stream improvement is modest — domain differences, sampling rate, periodicity structure.
2. Move EAC out of the ablation figure/table and present it only in the main results. Replace with a proper component ablation (e.g., removing the gating mechanism).
3. Report concrete training time (seconds/period) and peak GPU memory (GB) numbers in the efficiency study text rather than relying solely on the figure.
4. Either validate or remove the "privacy protection" claim.
5. Add hyperparameter sensitivity analysis for learning rate and gradient steps per period.

## Score and Decision

**Calibration anchor papers used:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| FRzCIlkM7I.md (EAC) | 6.75 | Bracketing, Narrowing | Direct baseline; STBP improves upon EAC by ~21% on 2/3 datasets with more sophisticated architecture. Accepted. |
| rjuZyMfLSd.md | 6.25 | Narrowing | Continual learning for system dynamics. Accepted. Less directly related. |
| rLlDt2FQvz.md | 6.25 | Narrowing | Open temporal graph learning with continual learning. Accepted. |
| vJGKYWC8j8.md (MoE) | 4.00 | Bracketing | Only 1 dataset, mostly existing techniques. Rejected. STBP is clearly stronger. |
| URCfZ2NgaR.md (SKI-CL) | 5.33 | Bracketing | MTS continual learning. Rejected. Concerns about novelty. STBP has more architectural novelty. |
| 5IvTw0qMKj.md (C²INet) | 4.67 | Bracketing | Trajectory prediction with continual learning. Rejected. |

**Bracket (Round 1):** 5.5 – 7.5, based on comparison with EAC (6.75, accepted) at the upper end and SKI-CL (5.33, rejected) at the lower end.

**Narrowing (Round 2):** The paper is stronger than SKI-CL (rejected at 5.33) and MoE (rejected at 4.00) in terms of architectural novelty, experimental scope, and result magnitude. It directly extends and improves upon EAC (accepted at 6.75) with ~21% better performance on traffic datasets, a more sophisticated architecture (FreNet + DLGA + pattern bank with gating/attention), and evaluation on 3 datasets across 2 domains. The weaknesses (AIR-Stream analysis, EAC in ablation, qualitative efficiency) are all minor and addressable. No fatal or major flaws exist. Final score calibrated to 7.0.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>