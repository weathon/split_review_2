Now I have enough information to finalize my review and score. Let me compile everything.

## Summary

This paper introduces Dual-level Noisy Correspondence (DNC) in Multi-modal Entity Alignment (MMEA), where noise exists in both intra-entity (entity-attribute) and inter-graph (entity-entity, attribute-attribute) correspondences. The proposed RULE framework addresses DNC through uncertainty-based reliability estimation (Dempster-Shafer Theory + consensus), three-way pair division with tailored loss strategies, reliability-weighted attribute fusion, and a test-time correspondence reasoning (TTR) module using a 72B MLLM. Experiments on five benchmarks with seven baselines demonstrate strong performance across multiple noise settings.

## Strengths

- **Well-grounded reliability estimation principle**: The two-fold principle combining uncertainty (Dempster-Shafer Theory, Definition 1, Eq. 3) with consensus (Definition 2, Eq. 5) is theoretically principled. Theorem 1 formally justifies why uncertainty alone is insufficient, providing clear motivation for the consensus component.

- **Clean three-way pair division with empirical validation**: The partition into S_U (high uncertainty, excluded), S_I (low consensus, blended), and S_C (clean, trusted) is conceptually well-designed. Figure 4 empirically confirms these subsets are well-separated in uncertainty-consensus space, directly validating the design.

- **Comprehensive experimental evaluation**: Five benchmarks, seven SOTA baselines, three noise levels (inherent, 20%, 50%), and two evaluation protocols (Non-name and All-attributes). RULE achieves best or second-best results in every setting. On ICEWS-WIKI Non-name with inherent DNC, RULE achieves 64.2 H@1 vs. next-best 52.6 (PMF), a +11.6 gap.

- **Training-time methods are independently effective in the harder Non-name setting**: Table 3 shows w/o TTR achieves 56.5 H@1 on Non-name ICEWS-WIKI, already exceeding all baselines (best: PMF at 52.6 from Table 1). This demonstrates the training-time robustness framework has genuine standalone value, particularly for the harder evaluation protocol that excludes entity names.

- **Effective robust fusion visualization**: The DRF module (Eq. 14) uses inter-graph reliability weights to suppress noisy attributes during fusion. Figure 5 visualizes that correctly associated attributes receive high reliability while injected noise attributes receive significantly lower scores, confirming the mechanism works as intended.

## Weaknesses

### Fatal
None.

### Major

- **Asymmetric use of 72B MLLM in headline results**: The method uses Qwen2.5-VL-72B-Instruct at test time (Section 2.5, Eq. 15–16; Section 3.1, line 224), while all seven baselines use only CLIP-based feature extraction. The paper states "For fair comparisons, we adopt the same backbone (i.e., CLIP) for all baselines and our method" (Section 3.2), but this only addresses the feature extraction stage. Table 3 ablation reveals that on All-attributes ICEWS-WIKI: w/o TTR = 94.0, MLLM Enhance = 97.6, Default = 97.7 — the MLLM alone nearly matches the full model. On this specific setting, w/o TTR (94.0) actually slightly underperforms PMF (94.6 from Table 2), meaning the headline 97.7 result is driven primarily by the MLLM rather than the training-time innovations. While the training-time methods are independently effective in the harder Non-name setting (56.5 vs. best baseline 52.6), the headline Tables 1–2 blend both contributions, making it impossible for readers to evaluate the genuine contribution of the proposed training-time methods versus the 72B VLM. The paper should present main results for the training-time framework alone (w/o TTR) and discuss TTR as a separate contribution, or at minimum include w/o TTR results alongside in the main tables.

- **Ablation restricted to one dataset**: Table 3 is reported exclusively on ICEWS-WIKI (Section 3.3, line 304: "we conduct analysis and ablation studies on the ICEWS-WIKI dataset"). The relative importance of components varies notably across settings — TTR contributes +1.7 H@1 on Non-name but +3.7 on All-attributes — and the lack of ablation on DBP15K or ICEWS-YAGO limits confidence in the generality of conclusions about component contributions.

### Minor

- **No standard deviations or confidence intervals**: Given that noise injection is stochastic and the method has many components, no variance is reported for any result. Running at least 3 seeds and reporting mean±std would increase confidence, especially for the closely-spaced All-attributes results.

- **Missing computational cost analysis for TTR**: The paper does not report the size of the candidate set T_i^m (Eq. 16), the number of MLLM calls per entity, or total wall-clock inference time. For DBP15K with ~15K entity pairs and 3 modalities, this could require tens of thousands of 72B MLLM inference calls, which has major practical implications that should be disclosed.

- **Bootstrapping concern in pair division**: The S^TP set (Eq. 8) uses the current model's similarity predictions to identify "true positives" for threshold determination. Early in training, when the model is unreliable, this estimated true positive set may itself be noisy, creating a circular dependency. A brief discussion or warm-up strategy would strengthen confidence in the pair division design.

### Trivial
None.

## Nice-to-Haves

- Test whether a smaller MLLM (e.g., 7B) could achieve similar TTR gains, to clarify whether benefits come from reasoning capability or model scale.
- Provide at least one strong baseline (e.g., PMF or MEAformer) augmented with the same TTR module, to directly disentangle the training-time methods' contribution from the MLLM's.
- Discuss failure modes of Assumption 1 (marginal contribution, Eq. 6–7) when attributes are correlated or redundant.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Harsh critic's claim that Theorem 1 is "trivial"**: The formalization serves a valid motivational role for the consensus principle and is standard practice in evidence theory papers. Not a substantive weakness.
- **Criticism about appendix content being unavailable**: Stripped by parser, not a paper problem. The original submission contains these sections.
- **Harsh critic's framing that the paper "should not be accepted in its current form"**: Overstated given that the training-time methods are independently effective in the harder Non-name setting, with w/o TTR (56.5) exceeding all baselines (best: 52.6) by +3.9 points.

## Novel Insights

The paper's most genuinely novel observation is the identification of Dual-level Noisy Correspondence as a distinct problem in MMEA — prior work on noisy correspondence has addressed inter-graph or intra-entity noise separately, but not their simultaneous interaction. The finding that both uncertainty and consensus are needed (Theorem 1: low uncertainty does not guarantee correct belief assignment) provides a principled foundation for noise identification that goes beyond simple confidence thresholding. The paper also makes a valuable empirical contribution by quantifying noise levels in real-world MMEA benchmarks (e.g., >50% in ICEWS), establishing that DNC is not merely a theoretical concern but a practical one that significantly degrades existing methods.

## Suggestions

- Add w/o TTR results to Tables 1–2 so readers can evaluate the training-time methods' independent contribution across all datasets.
- Expand Table 3 ablation to at least one DBP15K dataset to confirm component generalizability.
- Report TTR computational cost (number of MLLM calls, wall-clock time per entity).
- Consider giving at least one strong baseline access to TTR to directly answer whether headline gains are from training-time methods or the 72B MLLM.

## Calibration Report

**Anchors retrieved across all rounds:**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| a4O528mek9 (Multiple2Vec, multimodal incomplete data) | 3.00 | R1 | Much weaker paper, generic method with limited evaluation |
| YrxhSkfHh0 (UniFast HGR, multimodal feature extraction) | 3.33 | R1 | Weaker paper, less comprehensive experiments |
| rwdeKOdAwY (RetFormer, multimodal retrieval) | 3.00 | R1 | Much weaker paper with noisy labels |
| ky2JYPKkml (Explainable multi-modality) | 3.00 | R1 | Much weaker, limited evaluation |
| DWWwGlPMFr (LEMoN, multimodal label errors) | 5.25 | R1 | Weaker paper, narrower scope |
| er7VhmqZEA (Noisy multi-view contrastive) | 4.00 | R1 | Weaker paper, limited novelty |
| HhP9bgCugr (Align-VL, vision-language alignment) | 4.75 | R1 | Weaker paper with similar noise motivation |
| 20mMK8UlFh (One-step noisy label mitigation) | 5.00 | R1 | Comparable noise-handling topic but narrower |
| z3dfuRcGAK (GEEA, generative entity alignment) | 6.67 | R1, R2 | **Directly comparable**: entity alignment, theoretical grounding, Accept. Our paper has more comprehensive experiments but MLLM fairness concern. |
| NNUiUwQWx6 (NeuSymEA, neuro-symbolic entity alignment) | 5.75 | R1, R2 | **Directly comparable**: entity alignment with theoretical framework. Our paper is clearly stronger in experiments and problem novelty. |
| 5BXWhVbHAK (Synergize modality training) | 6.33 | R1 | Multimodal learning, less directly comparable |
| QQYpgReSRk (MOFI, noisy entity images) | 6.25 | R1 | Noisy data handling, Accept |
| 9Cu8MRmhq2 (Norton, noisy video correspondence) | 8.00 | R1 | Similar problem (noisy correspondence) but more polished evaluation — aspirational comparison |
| TPZRq4FALB (READ, multi-modal TTA) | 8.00 | R1 | Multi-modal robustness, different task |
| ue1Tt3h1VC (MoMK, MMKG representation learning) | 6.60 | R2 | **Directly comparable**: MMKG learning, Accept. Our paper addresses a more practical noise problem. |
| ftGnpZrW7P (GRAM, multimodal alignment) | 7.00 | R2 | Multimodal alignment with novel metric, Accept |
| uSz2K30RRd (Weighted point cloud contrastive) | 7.33 | R2 | Multimodal contrastive learning |

**Round 1 bracket**: 6.0–7.0. Our paper is clearly above NeuSymEA (5.75, Reject) in experiments and problem novelty, comparable to GEEA (6.67, Accept) and MoMK (6.60, Accept) in contribution level, but below Norton (8.00) due to the MLLM evaluation fairness concern.

**Round 2 narrowing**: The paper sits between GEEA (6.67) and GRAM (7.00). The MLLM fairness issue and single-dataset ablation prevent a score above 7.0, while the genuine novelty of the DNC problem, strong theoretical grounding, and comprehensive experiments (including independently effective training-time methods) keep it clearly above the 5.75 NeuSymEA reject threshold.

**Final score**: 6.5. The paper makes genuine contributions — identifying a novel practical problem, providing a principled theoretical framework, and demonstrating effectiveness across comprehensive experimental settings. The training-time methods alone outperform all baselines in the harder Non-name setting. However, the headline results in Tables 1–2 blend training-time contributions with a 72B MLLM that baselines are not given access to, and the ablation is limited to one dataset. These are addressable issues that could elevate this to a stronger paper.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>