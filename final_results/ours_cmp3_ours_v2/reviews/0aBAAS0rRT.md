Below is my final consolidated review. The draft was recorded; the calibration anchors and final score follow the review text.

---

## Summary

This paper proposes SigMap, a multimodal foundation model for wireless localization that introduces two domain-informed innovations: (1) a cycle-adaptive masking strategy for self-supervised pre-training on CSI data that disrupts periodic shortcuts, and (2) a map-as-prompt framework encoding 3D geographic information via GNN-generated soft prompts for parameter-efficient cross-scenario adaptation. Experiments on DeepMIMO and WAIR-D show improvements over OMP, CNN, SWiT, and LWLM baselines, with fine-tuning updating only 0.7% of parameters.

## Strengths

1. **Domain-informed cycle-adaptive masking.** The observation that standard MAE masking allows models to exploit the inherent periodicity of wireless signals as a shortcut is genuine and well-motivated. The cross-correlation-based adaptive mask (Equation 6) is a non-trivial, domain-appropriate adaptation of the MAE framework.

2. **Clean parameter-efficiency story.** Fine-tuning updates only 0.085M parameters (0.7% of an 11.73M backbone) and completes 1000 epochs in 30 minutes (Table 5). This level of specificity is valuable for deployment-oriented work and is clearly documented.

3. **Reasonable geographic prompt design with informative ablation.** The pipeline (3D mesh → Delaunay triangulation → 2-layer GCN → global pool → projection) in Algorithm 1 is clearly specified. Table 4's ablation showing 2-D bird's-eye view retains most of the benefit (1.692 vs 1.564 MAE) and that the map provides most gain over no-map (2.275 MAE) correctly identifies topological/LoS cues as the driver.

## Weaknesses

### Fatal
None.

### Major

1. **"Zero-shot" claim is contradicted by the paper's own experimental setup.** The abstract states "strong zero-shot generalization in unseen environments" and Contribution 3 claims "strong zero-shot generalization to unseen environments and base station configurations." However, Section 4.5 explicitly describes the setup as few-shot: *"only the downstream task heads are fine-tuned using limited target samples (approximately 100 instances per scenario), while the self-supervised backbone remains frozen. This few-shot learning setup..."* (lines 317–318). Fine-tuning on ~100 labeled samples per target environment is few-shot, not zero-shot. The few-shot results are still valuable, but the headline claim in the abstract and contributions section is inconsistent with the experiment design and must be corrected.

2. **NLoS-aware attention mechanism (Equation 11) is introduced in the experiments section without being specified in the method.** Equation 11 appears in Section 4.2 and is described as *"the key advantage"* for single-BS NLoS localization. However, the notation $\mathbf{o}_s^{(i)}$ and $\mathbf{W}_{\text{NLoS}}$ is never defined, the mechanism is absent from Section 3 (Methodology), and it is unclear whether this replaces or supplements the standard self-attention in the backbone or whether it is used during pre-training, fine-tuning, or both. A mechanism claimed as the key advantage for the most challenging scenario should be specified as part of the method, not dropped into the results section without context.

### Minor

3. **Missing comparisons against SSL baselines discussed in the paper's own related work.** The related work discusses CrowdBERT (Han et al., 2024), signal-guided masked autoencoders (Wang et al., 2025), and WirelessGPT (Yang et al., 2025) as SSL-based localization/representation learning methods but none appear in the experiments. While LWLM (Pan et al., 2025) is an SSL baseline that is included, the absence of these other explicitly discussed methods limits the reader's ability to assess whether SigMap improves on the full set of prior SSL approaches the paper positions itself against.

4. **No standard deviations reported despite 5-run averaging.** Section 4.1 states *"All results are averaged over 5 independent runs,"* yet every table presents only point estimates — no standard deviations, confidence intervals, or error bars. Given that some comparisons are close (Table 2: 0.673 vs 0.789 MAE for SigMap w/ and w/o map), variance information is needed to assess whether differences are meaningful.

5. **Numerical inconsistency in Section 4.5.** The text states *"SIGMAP reaches 1.026 m MAE on DeepMIMO O2 and 1.580 m on WAIR-D Scenario-2"* (line 340), but the WAIR-D result in the table shows **1.880 m** (line 336). This is a reporting error that must be resolved.

6. **Figure reference error in Section 4.4.** The text states *"Two-dimensional and three-dimensional map ablations are illustrated side-by-side in Figure 1,"* but Figure 1 (line 55) is a propagation diagram showing LoS/NLoS paths, not an ablation plot.

7. **Strip-masking achieves better RMSE than adaptive masking without discussion.** In Table 3, strip-masking attains an RMSE of 0.972 vs adaptive masking's 1.099, yet this anomaly is not discussed. A method that improves MAE but degrades RMSE may produce more variable predictions, which is relevant for practical deployment.

8. **Main results evaluated on a single simulated scenario.** All main results (Tables 1–4) use DeepMIMO O1_3p5. Generalization experiments (Table 4.5) compare SigMap only against LWLM, not against the full baseline suite (CNN, SWiT, OMP). It is unclear whether other baselines would also show improved generalization or whether SigMap's advantage is specific to the O1_3p5 training distribution.

### Trivial

9. **Backbone architecture details absent from main text.** The backbone is described only as *"a transformer-based backbone network"* (Section 3.1). Number of layers, hidden dimension, attention heads, and the embedding strategy for the 4D input tensor are not stated in the main paper. (Appendix B likely contains these details but was stripped by the parser. Including a brief summary in the main text would aid reproducibility.)

## Nice-to-Haves

- An analysis showing the cross-correlation patterns detected and how the resulting masks differ from fixed grid/strip masks for representative CSI samples would strengthen the motivation for cycle-adaptive masking.
- The paper claims the geographic prompt enables "interpretable fusion" (Section 1.2) but does not provide any interpretability analysis (e.g., attention weights over the prompt token). Addressing this would substantiate a stated contribution.

## Removed Points

- **"Incomplete architectural specification as a Major issue"** — downgraded to Trivial. The appendix (stripped by parser) presumably contains these details; including a brief summary in the main text is a minor presentation improvement.
- **"Method is not reproducible" framing** — removed. The paper provides substantial implementation detail (Algorithm 1, Equations 1–10, training configurations). Missing architectural specifics are addressable with a short addition.
- **Missing appendix / missing proof references** — removed per policy: the parser strips appendices from all papers.
- **Generic strengths about "addressing an important problem"** — removed as not specific enough.
- **Criticism about missing interpretability analysis** — demoted to Nice-to-Have. The paper claims the mechanism *enables* interpretable fusion, not that it *demonstrates* it; this is a forward-looking claim, not a broken promise.

## Novel Insights

The decomposition of gain contributions (backbone + masking does most of the work, the map provides incremental but meaningful benefit) is a useful quantification that the paper itself implies but could state more explicitly. The observation that strip-masking achieves better RMSE than adaptive masking (Table 3) is genuinely curious and points to a trade-off the authors should investigate. Beyond these, the reviews do not surface insights that the paper itself does not already contain or directly imply.

## Suggestions

1. Correct "zero-shot" to "few-shot" or "parameter-efficient cross-scenario generalization" in the abstract and contributions.
2. Move the NLoS-aware attention mechanism (Equation 11) to Section 3 (Methodology) with full specification of what $\mathbf{o}_s^{(i)}$ represents and how $\mathbf{W}_{\text{NLoS}}$ is trained.
3. Add standard deviations to all tables.
4. Resolve the WAIR-D numerical inconsistency (1.580 vs 1.880).
5. Correct the Figure 1 reference in Section 4.4.
6. Discuss the strip-masking RMSE advantage in the ablation analysis.
7. Add at least one more SSL baseline comparison from the methods discussed in related work, if feasible.

---

**Calibration summary.** Round 1 bracketing set the plausible range between 4.0 and 6.5. Anchor papers used:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 9TClCDZXeh (Differentiable Wireless Simulation) | 7.00 | R1 | More thorough evaluation; our paper has stronger novelty but more framing issues |
| lG9fjBLb6d (RFMamba) | 6.50 | R1 | Similar domain-application strength; our paper has clearer ablations but more major issues |
| NPNUHgHF2w (CBraMod) | 6.75 | R1 | Stronger evaluation breadth; similar baseline gaps and presentation issues |
| 7KDuQPrAF3 (Foundation Model for ECC) | 6.25 | R1 | Ambitious claim with limited validation; our paper has comparable claim-verification gap |
| t5LXyWbs5p (Freq-Aware MAE Biosignals) | 5.50 | R2 | Rejected; similar concept (signal-adaptive MAE) but weaker novelty and smaller gains |
| 7ipjMIHVJt (DASFormer) | 5.25 | R1 | Rejected; insufficient novelty and missing baselines; our paper has stronger methodological novelty |
| Iip7rt9UL3 (Lightweight Pre-trained Remote Sensing) | 4.75 | R2 | Weaker than our paper in technical depth and evaluation |

Our paper sits above the rejected signal-pretraining papers (5.25–5.50) due to genuinely novel methodological contributions and a clean parameter-efficiency story, but below the accepted wireless/signal foundation models (6.25–7.00) because of two major issues (zero-shot framing error, orphaned NLoS mechanism) and multiple minor gaps.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>