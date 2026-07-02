## Summary

The paper proposes **PIRN**, a prototype-driven reconstruction framework for few-shot multimodal anomaly detection (RGB + surface normals). It introduces three components: Balanced Prototype Assignment (BPA) using optimal transport to prevent codebook collapse, Adaptive Prototype Refinement (APR) that dynamically updates prototypes at test time to capture unseen normal patterns, and Multimodal Normality Communication (MNC) that exchanges prototype-level normal information across modalities. Extensive experiments on MVTec 3D-AD, Eyecandies, and Real-IAD D3 show consistent gains over existing methods, especially under limited training data.

## Strengths

1. **Well-motivated problem and clear component design.** The paper identifies specific failure modes of existing MAD methods in few-shot settings (overfitting of cross-modal alignment, false positives from memory banks) and designs each of the three proposed components (BPA, APR, MNC) to directly address a distinct challenge: codebook collapse, train-test distribution gap, and lack of cross-modal collaboration.

2. **Strong empirical results under few-shot settings.** On MVTec-3D-AD and Eyecandies, PIRN outperforms the best baseline by +3.9 / +3.7 / +2.4 AUROC$_I$ at 5 / 10 / 50 shots, and these gains are consistent across three datasets and three metrics. Qualitative visualizations (anomaly maps, score distributions, t-SNE) further support the quantitative results.

3. **Computational efficiency.** The method achieves the best accuracy while requiring only 103.36 GFLOPs and 17.49 ms latency (85% fewer FLOPs and 4.35× faster than FIND), making it practical for deployment.

4. **Thorough ablation and analysis.** The paper studies the contribution of each component, the effect of prototype count, decoder depth, aggregation strategy, and single-modality vs. multimodal performance. The displacement visualization (Fig. 4) provides interpretable evidence that prototypes anchor normal features and anomalies are displaced further.

## Weaknesses

### Fatal

None.

### Major

1. **Unclear fairness of baseline comparisons.** The paper uses a frozen DINOv2 ViT-B/14 encoder for PIRN and adapts INP-Former to the same backbone, but it is not stated whether other baselines (M3DM, CFM, AST, BTF, 3D-ADNAS) were re-implemented with the same backbone or if their reported numbers are taken from original papers using different backbones (e.g., ResNet, WideResNet). If the latter, the performance gap may partly stem from the stronger backbone rather than the proposed method. The paper should clarify this and, ideally, re-evaluate all baselines with a consistent backbone.

2. **Lack of statistical significance reporting.** Results are presented as single numbers without error bars or multiple-run averages. Few-shot settings have high variance due to random sampling of training sets; reporting standard deviations or confirming that reported figures are averages over several runs (e.g., 3–5 random seeds) would substantially increase confidence in the claims.

3. **APR’s reliance on diffuse OT assignment for anomalous patches may not always hold.** The paper argues that anomalous patches receive diffuse weights in the OT plan and therefore do not corrupt prototype updates. However, when anomalies are globally subtle and similar to normal patterns (e.g., a small scratch on a uniformly textured surface), this assumption could break down. The paper does not discuss such failure cases or provide analysis of when APR might be less effective.

4. **Training loss not fully specified.** The paper mentions “a soft mining loss (Luo et al., 2025)” but does not define the loss function explicitly (e.g., equation, hyperparameters, how it operates on features from both modalities). This makes the method description incomplete and reproduction harder.

### Minor

1. **Ablation table formatting (Table 2) is ambiguous.** The checkmark pattern is unclear due to garbled formatting, though the accompanying text provides some explanation. The table header also contains a typo: “BFA” should be “BPA”.

2. **Dataset name inconsistency.** The paper uses “MVTec 3D-AD”, “MV Tec-3D-AD”, and “MVTec-3D-AD” interchangeably. While minor, consistent naming would improve readability.

3. **Prototype count sensitivity.** The ablation shows that $K=10$ works best, but the performance drops notably for $K=50$ or $100$. This sensitivity suggests that tuning $K$ per dataset may be necessary, but the paper does not discuss how to select $K$ in practice.

### Trivial

- The claim “first multimodal AD framework to integrate a vector-quantized prototype codebook into a ViT encoder-decoder” is narrow and not central to the paper’s contribution.

## Nice-to-Haves

- Provide a table comparing all baselines under the same frozen DINOv2 backbone for a fully controlled comparison.
- Include error bars or multiple-run statistics for few-shot experiments.
- Show a failure case analysis for APR, e.g., examples where test-time refinement degrades performance.
- Specify the reconstruction loss in more detail (formula, hyperparameters).

## Novel Insights

The paper demonstrates that in few-shot multimodal anomaly detection, optimal transport can be used not only for balanced prototype assignment (preventing collapse) but also for robustly extracting normal context from test samples to adapt prototypes online. The idea of communicating normality at the prototype level rather than the patch level avoids the brittleness of dense cross-modal alignment when data is scarce. This prototype-centric cross-modal design is a clean departure from existing alignment- or memory-based approaches.

## Suggestions

1. Clarify the backbone used for each baseline in Table 1 and, if possible, re-run comparisons with a consistent encoder to rule out backbone effects.
2. Report few-shot results averaged over multiple random training splits with standard deviations.
3. Provide a more detailed description of the loss function, including the exact formula and any hyperparameters.
4. Discuss potential limitations of the adaptive prototype refinement, especially for anomalies that are highly similar to normal patterns.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>