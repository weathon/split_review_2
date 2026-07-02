## Summary
This paper introduces FASTer, a unified framework for efficient autoregressive Vision-Language-Action (VLA) modeling in robotics. The framework consists of two components: FASTerVQ, a neural action tokenizer that uses residual vector quantization with a patchification strategy to compress action sequences into compact discrete codes while preserving reconstruction fidelity, and FASTerVLA, an autoregressive policy that leverages block-wise autoregressive decoding and a lightweight action expert for faster inference. Extensive experiments across simulated and real-world benchmarks demonstrate that FASTer achieves state-of-the-art performance on LIBERO (97.9% success rate) and Simpler-Bridge (87.9%), while significantly reducing inference latency compared to prior autoregressive VLA methods.

## Strengths
- **Strong empirical results**: The paper demonstrates consistent state-of-the-art performance across multiple benchmarks (LIBERO, Simpler-Bridge, VLABench) and real-world platforms, with FASTerVLA achieving 97.9% on LIBERO and 87.9% on Simpler-Bridge, substantially outperforming prior methods.
- **Comprehensive evaluation**: The experimental setup is thorough, covering 9 benchmarks across 5 distinct embodiments in both simulation and real-world settings, including single-arm, bimanual, and whole-body control tasks.
- **Novel technical contributions**: The action patchifier that non-uniformly groups action dimensions based on physical semantics is a well-motivated design choice that addresses the distributional imbalance across action dimensions. The block-wise autoregressive decoding with coarse-to-fine codebook ordering is a principled approach to reducing inference latency.
- **Cross-backbone generalization**: The paper demonstrates that FASTerVQ can be effectively combined with different VLM backbones (PaliGemma, Qwen2.5, InternVL3.5), with particularly impressive gains on InternVL3.5 (17.3% improvement), showing the tokenizer's broad applicability.

## Weaknesses
### Fatal
None.

### Major
- **Limited novelty relative to prior work**: The paper's core technical components—residual VQ, transformer-based autoencoder, block-wise decoding, and lightweight action experts—are all well-established techniques from prior work (audio codecs, video generation, π₀). The primary novelty is the application of these techniques to action tokenization, but the paper does not clearly articulate what new technical insight or algorithmic contribution is being made beyond engineering integration. The action patchifier is the most novel component, but its design (non-uniform grouping based on physical semantics) is described at a high level without sufficient detail on how the grouping is determined or learned.

- **Insufficient analysis of the action patchifier**: The non-uniform partitioning of action dimensions is a key contribution, but the paper provides no ablation study or analysis of different grouping strategies. How are the groups determined? Is this done manually based on domain knowledge, or is there a learned component? The paper states dimensions are grouped "based on their physical characteristic" but does not specify the grouping for any of the evaluated embodiments, making the results difficult to reproduce.

- **Missing critical baselines and comparisons**: The paper compares against π₀ and π₀-FAST but does not include comparisons with other recent autoregressive VLA methods such as RT-2, RT-2-X, or other VQ-based approaches beyond those cited. Additionally, the paper does not compare against diffusion-based methods on the same benchmarks where they might excel (e.g., VLABench), making it difficult to assess the claim that autoregressive VLAs can "rival and even surpass diffusion-based approaches."

- **Incomplete reporting of experimental details**: The paper mentions "spacing augmentation" during training but does not specify the value of k used in experiments. The action expert architecture is described as "sharing the backbone architecture but with fewer parameters" without specifying the exact parameter count or architecture differences. These omissions hinder reproducibility.

### Minor
- **The VRR metric, while well-motivated, depends critically on the choice of σ**: The paper uses σ = 10⁻³ for the main results but does not justify this specific value or show how results change with different σ values. Since the metric is central to the tokenizer evaluation, this sensitivity should be explored.

- **Inference time comparisons are limited**: Table 2 provides inference times for FASTer but does not include direct comparisons with π₀ or π₀-FAST under the same hardware and implementation conditions. The paper mentions these comparisons in text but does not present them in a table, making it difficult to verify the claimed speedups.

- **The paper claims "near-lossless reconstruction" but does not provide quantitative evidence**: The VRR results show high reconstruction rates, but "near-lossless" is a strong claim that should be supported by additional metrics (e.g., PSNR, SSIM for trajectories, or task success rate with reconstructed vs. ground-truth actions).

### Trivial
- The paper uses "FASTer" and "FASTER" inconsistently throughout the text and figures.
- Figure 4 is presented as a bar chart but the underlying data is also given in a table, which is redundant.

## Nice-to-Haves
- An ablation study comparing different action patchification strategies (e.g., uniform vs. non-uniform grouping, different group sizes) would strengthen the paper.
- A comparison of FASTerVQ against a learned grouping approach (e.g., clustering action dimensions) would help validate the manual grouping design.
- Analysis of how the codebook utilization and entropy metrics correlate with downstream task performance across more benchmarks would be valuable.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Provide a detailed specification of the action patchifier grouping for each embodiment evaluated, including the exact dimensions assigned to each group.
- Add an ablation study comparing different grouping strategies (uniform, random, learned) to justify the manual non-uniform design.
- Include direct inference time comparisons with π₀ and π₀-FAST under identical hardware and implementation conditions in a table.
- Report the sensitivity of VRR to the tolerance parameter σ and justify the chosen value.
- Clarify the architecture of the lightweight action expert, including parameter count and architectural differences from the backbone.

## Score and Decision
The paper presents a well-engineered system that achieves strong empirical results across diverse robotic benchmarks. However, the technical novelty is limited—the core components (RVQ, transformer autoencoder, block-wise decoding) are all adapted from prior work without significant algorithmic innovation. The action patchifier is the most novel contribution, but it is insufficiently analyzed and specified. The evaluation is comprehensive and the results are compelling, but the lack of critical baselines and incomplete experimental details weaken the contribution. The paper is a solid engineering contribution that advances the state of the art in autoregressive VLA, but it does not introduce sufficient new knowledge or insight to warrant acceptance at a top venue.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>