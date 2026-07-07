Now I'll produce the final consolidated review.

## Summary

This paper presents PIRN, a prototype-driven reconstruction framework for few-shot multimodal anomaly detection (MAD). It addresses three identified challenges of few-shot MAD — codebook collapse, static prototypes missing novel normal variations, and lack of cross-modal collaboration — through three corresponding modules: Balanced Prototype Assignment (BPA via optimal transport), Adaptive Prototype Refinement (APR via GRU-based gated updates), and Multimodal Normality Communication (MNC via graph attention and cross-attention). Experiments on MVTec-3D-AD, Eyecandies, and Real-IAD D3 show consistent improvements over baselines, particularly in few-shot settings, with substantial computational efficiency gains (85% fewer FLOPs than FIND).

## Strengths

- **Well-motivated problem with coherent method design.** The paper identifies three specific challenges of few-shot MAD (codebook collapse, static prototypes, lack of cross-modal collaboration) and directly ties each to a corresponding module (BPA, APR, MNC). This internal coherence between the problem framing in Section 1 and the method in Section 3 is a genuine strength.

- **Consistent empirical gains under few-shot settings.** Across Tables 1 and 3, PIRN shows clear improvements over strong baselines in the 5-shot, 10-shot, and 50-shot settings on both MVTec-3D-AD and Eyecandies. Gains include +3.9 AUROC_I at 5-shot on MVTec-3D-AD and +4.0 at 10-shot on Eyecandies over the best-performing baseline (INP-Former, adapted with the same frozen DINOv2 backbone). These are meaningful improvements in a regime where most baselines struggle. Weight from scoring model: +5.35 — the strongest positive signal in the draft.

- **Computational efficiency is genuinely impressive.** Table 4 shows PIRN achieves the best AUROC_I (0.922) with 103.36G FLOPs and 17.49ms latency — roughly 5× fewer FLOPs than the next-best-performing FIND and 4.35× faster. This accuracy-efficiency combination is uncommon and provides a concrete practical advantage. Weight: +4.36.

- **Clean evaluation across three datasets with multiple metrics.** The paper evaluates on MVTec-3D-AD, Eyecandies, and Real-IAD D3, reporting AUROC_I, AUROC_P, and AUPRO across 5/10/50/all-shot settings. The ablation study (Tables 5, 6, 7, and modality ablation in Table 3) covers codebook size, decoder depth, aggregation method, and modality contribution. Weight: +4.23.

## Weaknesses

### Fatal
None.

### Major

- **No variance or statistical significance reporting.** Every result in every table is a single number with no standard deviation, confidence interval, or mention of multiple random seeds or data splits. For few-shot anomaly detection where only 5 or 10 normal training samples are available, the particular samples drawn can substantially affect performance. A 3.7-point AUROC improvement could fall within the noise of a single split. The paper does not specify how few-shot splits were constructed, whether results are averaged over multiple splits, or whether the same splits were used across all baselines. This is the most significant evidential gap. (Weight: -4.30)

- **No quantitative evidence supporting the codebook collapse mitigation claim.** The paper motivates BPA by claiming softmax assignment leads to codebook collapse (Section 1, Section 3.2), but provides only qualitative t-SNE visualizations (Fig. 1 Right) as evidence. There are no quantitative metrics — entropy of the assignment distribution, percentage of active prototypes, variance of prototype usage over training, or reconstruction fidelity per prototype — that would directly demonstrate that (a) codebook collapse actually occurs in this setting, and (b) the balanced OT constraint materially changes prototype utilization. Without such measurements, the connection between the BPA mechanism and the observed performance gains remains plausible but unsubstantiated. (Weight: -5.17)

### Minor

- **Mixed results on Real-IAD D3 are discussed but warrant more candid treatment.** On Real-IAD D3 (Table 8), PIRN achieves the best AUROC_P (0.961) but is second-best on the primary detection metric AUROC_J (0.873), behind D³M (0.890). While the paper acknowledges this and notes D³M uses tri-modal inputs versus PIRN's two modalities, the main text frames the result primarily as a success ("highly competitive performance"). The image-level detection gap deserves more direct discussion, including an analysis of categories where PIRN underperforms.

- **The APR OT-weighting claim is not quantitatively verified.** Section 3.3 states that anomalous patches "tend to be assigned more diffusely across prototypes … thereby contributing weakly to each prototype context." This is a plausible but untested heuristic. No analysis of OT weight distributions for anomalous vs. normal patches is provided. A quantitative examination (e.g., average OT entropy per patch for normal vs. anomalous inputs) would significantly strengthen this claim.

- **Backbone specifications not provided for all baselines.** While INP-Former is adapted to use the same DINOv2 ViT-B/14 backbone as PIRN, the paper does not clarify whether M3DM, CFM, AST, BTF, and 3D-ADNAS also use equivalent backbones or potentially weaker alternatives. If they do not, some of the performance gap may partly reflect backbone quality.

### Trivial

- **CFM/CTM naming inconsistency.** The method is referred to as "CFM (Costanzino et al., 2024)" in the introduction, related work, and computational efficiency analysis, but as "CTM (Costanzino et al., 2024)" in Table 1. These appear to be the same method.

- **Loss function specification is imprecise.** The paper states the model is trained using "e.g., a soft mining loss (Luo et al., 2025)" (Section 4). The phrase "e.g." makes it unclear whether the authors used exactly the referenced soft mining loss or a different formulation.

## Nice-to-Haves

- An ablation of whether the sigmoid-based purification step in MNC Stage 2 is necessary, or whether cross-attention alone would suffice.
- An analysis of the OT weight distributions for anomalous vs. normal patches to substantiate the APR claim.
- Clarification of how the few-shot splits were constructed and whether they are fixed across all baseline methods.

## Removed Points

- **Table 2 row 4 (0.967 vs. 0.922):** The reviewer flagged this as an unexplained anomaly. However, Table 2 is visibly parser-corrupted (all rows show identical checkmarks despite the text stating the baseline row excludes all modules). The 0.967 value is likely also a parser artifact. Removed because this is a formatting corruption, not a content error by the authors.

- **MNC purification step not ablated:** The reviewer questioned whether the sigmoid purification in Stage 2 of MNC is necessary. However, the ablation study (Table 2) is designed to test component contributions, and the parser corruption makes it impossible to evaluate this claim from the available text.

- **General codebook collapse speculation beyond quantitative evidence:** The broader speculative framing about codebook collapse being an untested assumption is subsumed by the specific request for quantitative metrics (retained as a Major weakness above); the more speculative framing is removed.

- **Strength about "well-motivated problem" from input review:** The original strength about the problem being important is generic and removed; the coherent method-design mapping is concrete and retained.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface observations that go beyond what the paper already articulates about its design and results.

## Suggestions

1. **Add variance reporting** over at least 3 random few-shot splits for Table 1. This is the single highest-leverage improvement.
2. **Provide quantitative metrics of prototype utilization:** entropy of assignment distribution and fraction of active prototypes with vs. without BPA over training.
3. **Add a quantitative analysis** of OT weight distributions for anomalous vs. normal patches to substantiate the APR claim.
4. **Replace "e.g., a soft mining loss"** with the exact loss formulation used.
5. **Harmonize the CFM/CTM naming** throughout the paper.
6. **Add a candid discussion** of the Real-IAD D3 AUROC_J gap, including per-category analysis of where PIRN underperforms D³M.

## Score and Decision

**Calibration Anchors Considered (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| bESxQeXTlo.md (CLIP-LAD) | 3.00 | R1 | Yes | Limited novelty, simple pipeline. Much weaker than PIRN. |
| Vi6p2TeujL.md (PTAD) | 4.25 | R1 | Yes | Prototype-based tabular AD. Similar evidential gaps (no statistical testing, weight -5.24) but much weaker positive weights (+2-4 vs PIRN's +4-5). |
| J2we1sVd9m.md (Prototype-OT OOD) | 4.60 | R2 | Yes | OT for OOD detection. Theoretical concerns and unclear methodology. PIRN is stronger. |
| 8TBGdH3t6a.md (H-PAD) | 5.60 | R2 | Yes | Prototype-based time series AD. Marginal gains (-4.81), reproducibility issues (-3.89). PIRN has clearer gains and superior efficiency. |
| Zzs3JwknAY.md (One-for-All) | 6.40 | R1 | Yes | Few-shot AD with prompt learning. Had more severe weaknesses (clarity -7.44, missing baselines -6.88) than PIRN's worst (-5.17). |
| cJs4oE4m9Q.md (Deep Orthogonal Hypersphere) | 8.00 | R1 | Yes | Strong theoretical contributions and minimal weaknesses. PIRN lacks this theoretical depth. |

**Round 1 bracket:** 5.5–7.0. **Narrowing:** PIRN sits above H-PAD (5.60) and PTAD (4.25) because its strongest positive weights (+5.35 empirical gains, +4.36 efficiency) exceed anything in those anchors, while its worst weaknesses (-5.17, -4.30) are comparable in magnitude. It sits below Deep Orthogonal Hypersphere (8.00) which has theoretical proofs and minimal weaknesses. The closest comparable is One-for-All (6.40) whose most severe weaknesses exceed PIRN's, but PIRN lacks that paper's task novelty. **Final score:** 6.5.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>