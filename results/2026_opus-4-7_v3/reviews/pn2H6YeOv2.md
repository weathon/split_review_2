Now let me verify specific claims about Figure 3, Table 1, and other details more carefully:Now I have a thorough understanding of the paper. Let me draft my review.Now let me run calibration search Round 1 — Bracketing:Let me read some of the most relevant anchor papers to calibrate my score:Now let me read the LVLM-CL paper (avg 2.50) to understand what a low-scoring paper in this area looks like:Now I have enough to calibrate. Let me form my assessment.

**Round 1 Bracket Assessment:**

Comparing PI-CCA to the anchors:
- **LVLM-CL (2.50)**: PI-CCA is far stronger — clear mathematical framework, thorough evaluation, multiple baselines.
- **CLIP Online CL (3.80)**, **VL Task Codebook (4.67)**, **VL Synergy (5.00)**: PI-CCA has stronger methodology, broader evaluation, and more thorough analysis.
- **PROOF (5.67)**: PI-CCA has stronger mathematical framework and broader evaluation across 4 benchmarks.
- **TiC-CLIP (6.25)**: Different focus (benchmark vs method), but similar quality level.
- **C-CLIP (6.50)**: Most direct comparison — C-CLIP is a baseline PI-CCA outperforms. PI-CCA has more thorough analysis (ablations, stress tests, 20-permutation order sensitivity) and more principled framework. But improvements are modest.

**Initial bracket: 6.0–7.5**

PI-CCA sits at or slightly above C-CLIP quality (6.50). The mathematical novelty and thorough analysis push it above, but the modest improvements and the Figure 3 analysis concern prevent it from reaching the 8.0 tier. No anchors were found above 8.5 in this specific topic.

Now let me write the final review:## Summary
PI-CCA proposes a replay-free continual learning framework for vision-language models that reframes forgetting as alignment-geometry drift. It introduces a compact "CCA certificate" capturing the top-*k* canonical correlations and subspaces of the whitened cross-covariance matrix, with losses for spectral preservation, subspace-angle preservation, and prompt invariance via projector averaging. Evaluated across four VL-CL benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL), PI-CCA achieves state-of-the-art among replay-free methods while maintaining constant memory and compatibility with parameter-efficient (LoRA) adaptation.

## Strengths

- **Novel and well-specified mathematical framework (§3.1–3.4).** The CCA certificate (Eq. 4) is a compact, interpretable object. The spectral preservation loss (Eq. 8, with permutation-invariant sorted surrogate and Ky-Fan-*k* alignment), subspace-angle loss (Eq. 10, via sketched Gram projectors), and prompt invariance loss (Eq. 11, with mean-projector alignment and dispersion contraction) are precisely defined. The streaming EMA estimation (Eq. 12–13) and stable whitening procedures (eigendecomposition with floor, Newton–Schulz iteration) are detailed enough for reimplementation. This is a genuinely novel use of CCA in VL-CL — prior work (e.g., Raghu et al., 2017; Kornblith et al., 2019) used CCA-family measures only diagnostically; PI-CCA uses them prescriptively as a training objective.

- **Thorough ablation and robustness analysis (Table 3, Figs. 2, 4, 5).** Table 3 systematically removes each component, quantifying degradation: spectral (−2.5 MTIL Avg) and subspace (−2.2) terms cause the largest drops, establishing that both are necessary. The Pareto analysis (Fig. 2) sweeps (k, h) over 35 configurations and identifies a broad plateau near (64, 256). The prompt invariance stress test (Fig. 4) shows +2.44pp R@1 improvement at perturbation strength s=1.0 under both ID and OOD templates. The task-order sensitivity study over 20 permutations (Fig. 5) shows narrow IQRs — a robustness check rarely provided by CL papers.

- **Breadth of evaluation (§4.1, Tables 1–2).** Four distinct VL-CL protocols covering classification (MTIL, X-TAIL), retrieval (VLCL), and structured concept matching (ConStruct-VL) are evaluated against 10+ recent baselines. Consistent improvements across all four tracks make the claimed generality credible.

- **Prompt invariance mechanism is principled and empirically validated.** Averaging projectors over prompt perturbations (Eq. 5–6) elegantly sidesteps sign/rotation ambiguity without Procrustes alignment. Figure 4 demonstrates clear benefits under both ID and OOD template shifts, with the gap widening at higher perturbation strengths.

## Weaknesses

### Fatal
None.

### Major

1. **Figure 3 correlation analysis is potentially circular and insufficiently transparent.** Two panels report Pearson r=1.00 and two report r=0.99, with Spearman ρ=1.00 in all four. Since the training loss (Eqs. 8, 10) directly minimizes the drift metrics being correlated with performance (D_ang = Σ sin²θ_i and D_ρ = ‖ρ̂−ρ*‖₂), a strong correlation is at least partly tautological: settings that minimize the CCA losses will by construction have low drift. The paper presents this as evidence that "preserving CCA geometry predicts retention" (§4.3, Fig. 3 caption: "Clear positive trends with realistic scatter"), but does not discuss how many data points are plotted, which experimental settings each point represents, or the degree to which the near-perfect correlation is mechanistically expected given the loss design. The caption's mention of "realistic scatter" is inconsistent with r=0.99–1.00 values. This analysis is central to the paper's thesis and its current form invites skepticism rather than providing convincing evidence.

2. **Missing variance reporting for MTIL/X-TAIL weakens the headline improvements.** Table 1 reports no standard deviations for MTIL or X-TAIL, while the gains over the next-best methods are modest: +1.6% Avg on MTIL (over C-CLIP), +0.7% Avg on X-TAIL (over DIKI). Table 2 appropriately reports standard deviations for VLCL and ConStruct-VL. Without variance estimates in Table 1, it is impossible to determine whether the improvements on the two main classification benchmarks are statistically meaningful or within noise.

### Minor

1. **The "invariants vs. proxies" framing is overstated (§1, §2, abstract, conclusion).** The paper repeatedly frames CCA quantities as "the alignment object itself" versus prior methods' "proxy signals" (e.g., §1: "they regularize outcomes... rather than directly controlling the alignment object"; §2: "consolidation still targets proxy signals, not invariants"). However, the CCA decomposition of the whitened cross-covariance is itself a summary statistic of the feature geometry. Contrastive off-diagonals (Mod-X), similarity distributions (ZSCL), and CCA spectra (PI-CCA) are all summary statistics at different levels of abstraction. The paper should argue that CCA captures *better-chosen* invariants rather than claiming a categorical difference — this is a framing issue, not a methodological flaw.

2. **Certificate initialization requires reference data, creating tension with the "no reference corpus" framing.** The reference certificate (Eq. 4) requires computing CCA on the pre-continual model using paired image-text data. Section 3.2 states the certificate is "constructed from a diverse anchor prompt set." Yet the paper criticizes prior methods for depending on "reference corpora" (§1, §2). The paper should acknowledge this requirement explicitly and clarify how it differs from competitors' reference data needs (e.g., scale, diversity, privacy implications).

3. **CLIP backbone not specified in main text.** The backbone (ViT-B/16 vs ViT-L/14) is not stated in the main paper — the reproducibility statement defers to Appendix A.2. Since baseline performance varies substantially with backbone choice, this is relevant information for assessing comparison fairness.

### Trivial
None.

## Nice-to-Haves

- A **contrastive diagnostic** showing a specific case where a proxy-based method (e.g., ZSCL or C-CLIP) maintains its own proxy metric but still suffers alignment-geometry drift and downstream degradation, while PI-CCA preserves both. This would make the "invariants vs. proxies" argument empirical rather than conceptual.
- **Wall-time comparison table** against top baselines. The method requires per-batch SVD, eigendecomposition, and multiple forward passes for prompt perturbations; knowing the overhead relative to simpler distillation methods would help practitioners.
- Softening the certificate EMA (α > 0) means the certificate drifts across tasks, creating tension between the "preservation" framing and actual controlled plasticity. A brief discussion of when this drift helps vs. hurts would strengthen the narrative.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Comparison fairness — unclear whether all baselines use LoRA."** The paper categorizes baselines into "Regularization/Distillation" and "Parameter-efficient/Architecture" groups (§4.1), and the reproducibility statement mentions adapter details in Appendix A.2. This is an appendix-deferred detail, not a core methodological problem.
- **"TiC-YFCC/RedCaps mentioned in §4.1 but results not in main text."** The paper states results are reported for this study; they are likely in the appendix, which was stripped by the parser. Cannot penalize for missing appendix content.
- **Concerns about undisclosed hyperparameters/implementation details.** The reproducibility statement explicitly lists all key hyperparameters, EMA rates, sketch dimensions, and power-iteration settings in Appendix A.1–A.2. This is a reproducibility nitpick about stripped appendix content.

## Novel Insights
The core insight of treating continual VL learning as preserving CCA geometry (canonical spectrum + subspaces) of the whitened cross-covariance is genuinely novel in this field. While CCA-family measures have been used diagnostically in representation learning (Raghu et al., 2017; Kornblith et al., 2019), PI-CCA is the first to use them prescriptively as a continual learning objective. The random sketching for constant-memory certificate storage and the projector-averaging approach for prompt invariance are clean technical contributions. The 20-permutation task-order sensitivity study sets a useful methodological precedent for VL-CL evaluation.

## Suggestions
- Report standard deviations for MTIL and X-TAIL in Table 1, matching Table 2's rigor.
- In Figure 3 analysis, disclose the number of data points, identify which setting each point represents, and explicitly discuss why the correlation is expected to be strong given that the loss directly minimizes these drift metrics — then argue what additional information the near-perfect fit provides beyond the loss design.
- Soften the "invariants vs. proxies" framing: argue CCA captures better-chosen quantities rather than a categorically different object.
- State the CLIP backbone in the main text for comparison transparency.
- Clarify what data is used for initial certificate computation and how its scale/privacy profile compares to competitors' reference data.

## Score and Decision

### Anchor Papers Retrieved

| Paper | Avg Score | Round | Comparison to PI-CCA |
|-------|-----------|-------|---------------------|
| LVLM-CL (JIlIYIHMuv) | 2.50 | 1 | Far weaker: lacks baselines, unclear method, limited evaluation |
| Multimodal CIL Benchmark (gNoqEdT2wO) | 2.33 | 1 | Benchmark-only, no strong method contribution; PI-CCA is clearly stronger |
| Projected Subnetworks (WM5G2NWSYC) | 2.00 | 1 | Weaker method and evaluation; PI-CCA is clearly above |
| Task-Specific Adapters (TxIrMD6lAN) | 3.00 | 1 | Limited evaluation and contribution; PI-CCA is stronger |
| VL Synergy / LEAPGen (9aZ2ixiYGd) | 5.00 | 1 | Mixed reviews (3–8); PI-CCA has more consistent evaluation and novel framework |
| VLM Task Codebook (EKfcngSxwD) | 4.67 | 1 | PI-CCA has broader benchmarks and more principled approach |
| CLIP Online CL (G9Ea7mlqGO) | 3.80 | 1 | Weaker methodology; PI-CCA is clearly above |
| Replay-free CL (gCYFtUKXSc) | 4.00 | 1 | Limited scope; PI-CCA is above |
| PROOF / VLM-CIL (k9NYnsC4Mq) | 5.67 | 1 | PI-CCA has stronger mathematical framework, broader evaluation |
| **C-CLIP (sb7qHFYwBc)** | **6.50** | **1** | **Most direct comparison — C-CLIP is a baseline PI-CCA outperforms. PI-CCA has more thorough analysis and novel mathematical framework, but improvements are modest.** |
| TiC-CLIP (TLADT8Wrhn) | 6.25 | 1 | Different focus (benchmark vs method), similar quality level |
| Spurious Forgetting (ScI7IlKGdI) | 6.33 | 1 | Different focus (analysis paper); PI-CCA has stronger methodological contribution |
| VDT Understanding (WyEdX2R4er) | 8.00 | 1 | Different topic (data-type identification); PI-CCA doesn't reach this quality tier |
| Modality Gap Analysis (uAFHCZRmXk) | 8.00 | 1 | Different topic; strong analysis paper, PI-CCA doesn't match this depth |
| Hyperbolic VLM (3i13Gev2hV) | 8.00 | 1 | Different topic; PI-CCA is below this quality tier |
| Clothing-Irrelevant ReID (5lUdTogEL3) | 1.00 | 1 | Far weaker; PI-CCA is clearly above |

**Round 1 bracket:** 6.0–7.5

**Narrowing rationale:** PI-CCA is clearly above the 5.0–5.67 papers (PROOF, VL Synergy) due to its novel mathematical framework, broader evaluation, and more thorough analysis. It sits at or slightly above C-CLIP (6.50), the most direct anchor: PI-CCA outperforms C-CLIP empirically, has a more principled framework, and provides substantially more thorough analysis (ablations, stress tests, 20-permutation robustness). However, the improvements are modest (1–2pp without error bars on main benchmarks), the Figure 3 analysis has circularity concerns, and the paper doesn't reach the 8.0 tier which requires cleaner evidence or more substantial impact. The major weaknesses (missing variance reporting, questionable correlation analysis) prevent scoring above 7.0, while the genuine novelty and thorough evaluation prevent scoring below 6.0.

**Final score: 6.5**

This is a solid borderline-accept paper. The CCA certificate framework is genuinely novel, the evaluation is thorough and spans four benchmarks, and the ablation/robustness analyses are exemplary. The weaknesses — modest improvements without statistical significance testing on the main benchmarks, a potentially circular key analysis, and somewhat overstated framing — are real but not fatal. The contribution is sufficient for acceptance, contingent on the authors addressing the variance reporting and Figure 3 transparency in a revision.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>