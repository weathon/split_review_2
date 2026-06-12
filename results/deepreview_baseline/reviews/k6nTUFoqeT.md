## Summary

The paper introduces FASTer, a unified framework for autoregressive Vision-Language-Action (VLA) models comprising a neural action tokenizer (FASTerVQ) and an efficient policy (FASTerVLA). FASTerVQ uses action patchification and residual vector quantization with temporal and frequency-domain losses to achieve high compression ratios while preserving reconstruction fidelity. FASTerVLA incorporates block-wise autoregressive decoding and a lightweight action expert to reduce inference latency and improve task performance. Extensive experiments across simulated and real-world benchmarks demonstrate that FASTer consistently outperforms prior state-of-the-art VLA models in both speed and success rate.

## Strengths

- **Novel and well-motivated tokenizer design**: The action patchifier that non-uniformly groups action dimensions based on physical semantics and the use of residual VQ with both time-domain and DCT-based frequency losses are principled innovations. This design explicitly addresses the unique properties of robot action sequences (non-uniform distribution across dimensions, temporal redundancy) and achieves a superior compression–fidelity trade-off compared to prior tokenizers like FAST and VQ-BeT.

- **Solid empirical validation across diverse settings**: The evaluation spans 9 benchmarks, 5 distinct embodiments, simulated and real-world environments, and multiple VLM backbones. FASTerVLA sets new state-of-the-art on LIBERO (97.9%) and Simpler-Bridge (87.9%), and demonstrates strong out-of-distribution generalization and cross-backbone transferability. The systematic comparison of tokenization methods and the VRR metric provide valuable insights for the community.

- **Inference efficiency gains are clearly demonstrated**: The block-wise autoregressive decoding reduces the number of autoregressive forward passes (e.g., from 21 to 3 on LIBERO), and the timing breakdown in Table 2 verifies that the added cost from BAR is modest. The total inference time (112ms on LIBERO) is competitive with or faster than diffusion-based π0 (176ms) and significantly faster than prior autoregressive π0-FAST (197–556ms).

## Weaknesses

### Fatal

None.

### Major

- **Limited novelty of the action expert and block-wise AR relative to existing literature**: The lightweight action expert shares architectural ideas with adapters used in prior VLA work (e.g., π0), and block-wise generation has been explored in video, speech, and language modeling. While the paper adapts these ideas to action token sequences and demonstrates practical benefits, the conceptual novelty is incremental. The paper would benefit from a clearer discussion of what specific challenges in the action domain make these adaptations non-trivial and how they differ from prior block-wise approaches.

- **Potential comparison fairness concerns**: Several baselines (e.g., π0, OpenVLA) are evaluated under different training recipes (e.g., initialized from π0-FAST checkpoints for FASTerVLA, while others may be trained from scratch or different pretrained weights). The paper states that all baselines and FASTerVLA are initialized from large-scale robotics checkpoints, but the exact data, compute, and hyperparameter parity are not fully controlled across all benchmarks. A few comparisons (e.g., VLABench in Figure 4) show only marginal gains over π0, and the “FASTer w/o BAR” ablation already achieves strong results, suggesting the tokenizer contributes most of the improvement. The paper should more explicitly disentangle gains from the tokenizer vs. the BAR and action expert.

### Minor

- **The VRR metric, while useful, depends on an arbitrary threshold σ and the paper does not provide a principled way to choose σ for different tasks.** The claim of “nearly lossless reconstruction at σ=10⁻³” is not directly connected to downstream task performance—it would be stronger to show that VRR correlates with policy success rate.

- **The description of the attention mask in Figure 3(c) is somewhat ambiguous**: the block-wise causal mask is described but the exact masking pattern (e.g., whether tokens within a block attend to all previous tokens in the same block or only a subset) is not clearly specified in the main text.

- **The spacing augmentation for positional encoding is introduced but not ablated**—its individual contribution to performance is unclear relative to the other components.

### Trivial

- Some figure captions (e.g., Figure 4) repeat the same description twice due to formatting artifacts, but this does not affect comprehension.

## Nice-to-Haves

- An analysis of how the codebook entropy and VRR correlate with downstream policy success rates would further strengthen the claim that balanced codebook utilization leads to better generalization.
- A comparison with end-to-end trained (non-tokenizer-based) autoregressive VLAs that directly regress continuous actions (without discretization) would help contextualize the benefits of tokenization.

## Novel Insights

Beyond its own contributions, the paper provides evidence that action tokenizers share critical design principles with audio codecs: both involve continuous time-series with non-uniform information density and require coarse-to-fine decomposition. The demonstration that a VQ tokenizer trained solely on single-arm delta end-effector trajectories can generalize to joint-space actions and bimanual embodiments suggests the existence of a transferable “action prior” that can be captured through proper normalization and structured quantization. This insight could guide future work on universal action representation learning.

## Suggestions

- Clarify the attention masking scheme for block-wise autoregression: specify whether intra-block attention is full or constrained, and whether the mask is causal within a block.
- Provide a direct comparison of tokenizer training data sizes and model sizes for FASTerVQ variants vs. baselines to strengthen the scaling argument.
- Include a brief discussion of limitations: e.g., when does BAR hurt performance (if ever), or what types of tasks require the full sequential AR modeling?

## Score and Decision

**Score**: 8

**Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>