Now I will produce the final consolidated review.

## Summary

This paper proposes FASTer, a framework for efficient autoregressive Vision-Language-Action (VLA) models. It consists of FASTerVQ — a neural action tokenizer using patchification, hybrid transformer encoder, and residual vector quantization (RVQ) — and FASTerVLA, which uses block-wise autoregressive (BAR) decoding and a lightweight action expert. The tokenizer achieves high compression ratios while maintaining reconstruction quality, and the full system demonstrates strong inference speed improvements and competitive task performance across diverse simulated and real-world robotic benchmarks.

## Strengths

1. **Comprehensive evaluation across diverse embodiments (Table 1, Figure 4, Section 4).** The paper evaluates on four real-robot platforms (xArm, R1Lite bimanual, R1Lite WBC, WidowX) and multiple simulated environments (LIBERO, VLABench, GalaxeaManisim), covering single-arm, bimanual, and whole-body control. This breadth goes beyond most prior VLA papers.

2. **Meaningful inference efficiency improvements (Table 2, Section 4.3).** The paper provides a careful breakdown of inference latency: 112 ms for FASTerVLA on LIBERO vs. 176 ms for π₀ and 197–556 ms for π₀-FAST. On the high-dimensional WBC setting, π₀-FAST takes 1,100–3,000 ms while FASTerVLA takes 237 ms. This brings autoregressive VLA inference into a practically usable regime and is the paper's clearest concrete achievement.

3. **Cross-backbone generalization (Figure 7).** FASTerVQ improves performance across three different VLM backbones (PaliGemma2-3B, Qwen2.5-3B, InternVL3.5-2B), most dramatically lifting InternVL3.5-2B from 79.35% to 96.65%. This suggests the tokenizer provides a genuine representational benefit rather than being tied to a specific architecture.

4. **Tokenizer analysis (codebook utilization, VRR, scaling trends, Section 4.2).** The analysis of codebook utilization (100% of 4096 codes vs. 48–57% for baselines), the VRR metric, and the data-scaling experiments (FASTerS/L/XL in Figure 5) go beyond surface-level benchmarking and provide genuine insight into why the tokenizer works.

## Weaknesses

### Fatal
None.

### Major
None. The issues below are real but do not threaten the paper's core contributions.

### Minor

1. **Policy evaluation results lack reported variance in the main text (Table 1, Section 4.3).** The main text reports single success-rate numbers without confidence intervals, standard deviations, or explicit trial counts per task. This makes it difficult to assess whether the claimed performance gaps (e.g., the 1.1% gap over π₀.5 on LIBERO, or the 12.9% gap on Simpler-Bridge) are stable. While the appendix (stripped from the extracted text) may contain evaluation protocol details, including variance information in the main results would substantially strengthen the empirical contribution.

2. **The "single-channel images" claim in the abstract is not substantiated in the method (Abstract line 9 vs. Section 3.1).** The abstract states "FASTerVQ encodes action chunks as single-channel images," but the method describes only an action patchifier performing 2D partitioning followed by a hybrid transformer encoder — never an image encoder or explicit single-channel image representation. The 2D grid treatment is conceptually analogous to an image, but the method section does not explain this framing or implement any image-specific processing. This is a framing disconnect that should be resolved.

3. **The lightweight action expert is underspecified (Section 3.2, line 72).** The paper describes it as "sharing the backbone architecture but with fewer parameters" and cites π₀ as inspiration, but does not state: how many fewer parameters, the architectural relationship to the backbone (shared attention heads, feedforward layers, or neither), or whether it is trained jointly with the backbone or in stages. Given that the baseline π₀ already uses a separate action module, these specifics are needed to assess novelty.

4. **An unexplained performance regression with BAR on one task (Table 1, Simpler-Bridge "Spoon").** FASTer w/o BAR achieves 97.5% while full FASTer achieves only 91.7% — a decrease of 5.8 percentage points when BAR is added. This is not discussed in the paper. Understanding when BAR helps vs. hurts would strengthen the contribution.

5. **The spacing augmentation inference-time offset is not justified (Section 3.2).** The paper uses a fixed offset of 2 at inference time (p_i = p_{i-1} + 2) without explaining why 2 was chosen. No ablation is provided for this hyperparameter.

### Trivial
None.

## Nice-to-Haves
- Report inference times on a more widely accessible GPU (e.g., RTX 4090) in addition to the RTX 5090.
- Add a limitations/discussion paragraph acknowledging settings where the tokenizer may lose critical information or where the patchifier grouping may be suboptimal.
- Provide an ablation of the spacing augmentation offset value.
- Include a runtime comparison of the full BAR model vs. the AR (no BAR) variant with the FASTerVQ tokenizer to disentangle the speed contributions of the tokenizer and the decoding strategy.

## Removed Points

These points were raised in the input review but are removed for the following reasons:

1. **"No statistical reliability" as a fatal/structural issue** — Downgraded to Minor. The rule about stripped appendices means evaluation protocol details may exist in the original submission. Single-number reporting is common in robotics VLA evaluations, and the core improvements (e.g., 12.9% on Simpler-Bridge) are large enough that they are unlikely to be within noise. Valid as a reporting gap but not structural.

2. **"BAR is a known approach overclaiming novelty"** — Removed. The related work section (line 36) explicitly cites prior block-wise generation work across modalities. Applying a known technique to the VLA domain with demonstrated benefit is a valid systems contribution. The paper does not claim to have invented block-wise decoding wholesale.

3. **VRR σ hyperparameter not specified** — Removed. The paper does specify that σ differs by dimension type: "for end-effector translation, σ corresponds to Euclidean distance error measured in meters, whereas for end-effector rotation and joint positions, σ represents angular error in radians" (line 222).

4. **Naming inconsistency ("FASTerVLQ")** — Removed as a typo nitpick per the formatting/typo rule.

5. **Missing related work** — Removed per policy (no external verification available).

6. **Reproducibility nitpicks (hyperparameters, implementation details)** — Removed per policy; these are standard details likely in the stripped appendix.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
- Clarify the relationship between the "single-channel images" framing and the actual method implementation, or remove the claim from the abstract.
- Specify the action expert's parameter count relative to the backbone and its training procedure.
- Add confidence intervals or at minimum trial counts to the main results table.
- Discuss the BAR performance regression on Simpler-Bridge Spoon.
- Justify or ablate the spacing augmentation inference offset.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>