## Summary

The paper presents PIRN, a framework for few-shot multimodal anomaly detection (MAD) that uses RGB and 3D surface-normal data. It introduces three core innovations: Balanced Prototype Assignment (BPA) via optimal transport to prevent codebook collapse, Adaptive Prototype Refinement (APR) with GRU to adapt prototypes during inference, and Multimodal Normality Communication (MNC) for cross-modal prototype exchange. Experiments on MVTec 3D-AD, Eyecandies, and Real-IAD D3 show consistent improvements over baselines in few-shot settings, with competitive full-shot performance and high computational efficiency.

## Strengths

- **Well-motivated problem**: The paper clearly identifies the limitations of existing cross-modal alignment and memory-based methods in few-shot MAD, and the proposed solution directly addresses these issues.
- **Technically sound components**: BPA uses balanced optimal transport to encourage diverse prototype usage; APR dynamically adapts prototypes at test time to handle unseen normal variations; MNC exchanges high-level normal knowledge across modalities without requiring dense patch-level alignment. Each component is justified and ablated.
- **Comprehensive experiments**: Evaluation spans three benchmarks (MVTec 3D-AD, Eyecandies, Real-IAD D3) under multiple few-shot regimes (5/10/50-shot), with image-level and pixel-level metrics, ablations on all components, codebook size, decoder depth, and modality availability. The efficiency comparison (FLOPs/latency) is a valuable addition.
- **Clear and reproducible**: The architecture is described in sufficient detail, and the training/inference procedure is well-specified. The use of frozen DINOv2 encoders and surface-normal maps from point clouds ensures a reproducible setup.

## Weaknesses

### Major

- **Overclaimed novelty**: The paper states it is "the first multimodal AD framework to integrate a vector-quantized prototype codebook into a ViT encoder-decoder architecture." Prototype-based reconstruction (e.g., HVQ-Trans, MemAE, INP-Former) and optimal transport for prototype assignment have been explored in 2D AD; the main novelty lies in the specific combination for the multimodal few-shot setting and the APR/MNC modules. The claim should be softened.
- **BPA vs. softmax assignment**: The comparison in Figure 1 (t-SNE) shows that BPA yields more uniformly distributed prototypes than softmax assignment, but no quantitative metric (e.g., entropy of prototype usage) is provided to measure codebook collapse. A more rigorous evaluation would strengthen the claim.
- **Potential test-time adaptation risk**: APR updates prototypes during inference based on the test sample's context. While the OT-based mechanism is designed to suppress anomalous contributions, there is no analysis of how much the prototypes can drift, or whether this adaptation could inadvertently incorporate rare normal patterns that are actually anomalies. The ablation (Table 7) shows APR helps, but a deeper diagnostic (e.g., prototype trajectory over test samples) would be reassuring.

### Minor

- **INP-Former adaptation fairness**: The paper adapts INP-Former to a two-stream architecture by processing RGB and surface-normal maps independently and fusing via element-wise summation. Given that INP-Former relies on extracting intrinsic normal prototypes per test image, this simple adaptation may not fully leverage its design. A more careful baseline or discussion of adaptation choices would strengthen the comparison.
- **Missing comparison with FIND on main results**: FIND (Li et al., 2025) is referenced in the efficiency table (Table 4) and achieves SOTA (AUROC_I 0.921) in the 10-shot setting, which is very close to PIRN's 0.922. Why is FIND not included in the main tables (Table 1)? This would provide a more complete picture.
- **GAT alignment sensitivity**: The MNC stage 1 uses a graph attention network with KNN edges between prototypes of different modalities. The number of nearest neighbors is not specified, and no ablation on graph construction is provided. The robustness of this alignment step is unclear.
- **Limited analysis of APR's gating**: The gated update uses a GRU with context vector. The paper does not analyze whether the gate values indeed prevent anomaly-contaminated updates (e.g., gate activations on normal vs. anomalous test samples).

### Trivial

- Minor formatting artifacts (e.g., "incoperates" in abstract) are likely parser errors.
- Figure 4 caption is garbled, but the figure content is understandable.

## Nice-to-Haves

- Provide a quantitative measure of codebook collapse (e.g., entropy of prototype assignments) for BPA vs. softmax.
- Include results on the 1-shot setting to better demonstrate the method's upper bound in data-scarce regimes.
- Add a discussion of failure cases, especially when the few normal training samples are highly similar (e.g., all bagels look alike) and the prototype codebook may under-generalize.
- Study the effect of APR on prototype drift over a sequence of test samples to understand stability.

## Novel Insights

Beyond its own contributions, the paper offers a useful insight: in few-shot multimodal anomaly detection, directly modeling normality through a compact set of balanced prototypes, combined with cross-modal communication at the prototype level, is more effective than dense cross-modal alignment or large memory banks. The use of optimal transport for both balanced prototype assignment and context extraction for refinement provides a principled way to avoid collapse and to robustly update prototypes even when test samples contain anomalies. This suggests that discrete bottleneck approaches can be key to generalization in low-data regimes.

## Suggestions

- Tone down the novelty claim in the introduction (e.g., "first" → "a novel" or "to the best of our knowledge, the first approach to combine prototype-based reconstruction with cross-modal communication for few-shot MAD").
- Include entropy of prototype assignment as an additional metric to demonstrate BPA's effect on codebook collapse.
- Add FIND to the main comparison table (Table 1) for a direct fairness check.
- Provide the number of nearest neighbors used in the GAT stage of MNC.
- Add an experiment showing prototype gate values on normal vs. anomalous samples to confirm that APR filters out anomalies.

## Score and Decision

The paper addresses an important problem, proposes a well-designed method with clear motivations, and backs it with extensive experiments. The weaknesses are not fatal; they primarily relate to overclaiming and missing minor ablations. The contribution is solid and the empirical results are convincing. The paper is clearly written and the codebook-based reconstruction approach for few-shot MAD is a valuable direction.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>