## Summary
# Final Review Report

## Summary

This paper presents **SpatialBoost**, a training framework that enhances the 3D spatial awareness of pre-trained vision encoders by injecting dense spatial knowledge expressed in natural language. The core idea is to convert 3D spatial information extracted from 2D images (via off-the-shelf depth, segmentation, and reconstruction models) into structured linguistic descriptions, then use these descriptions to fine-tune the vision encoder through a Large Language Model (LLM) decoder. To prevent catastrophic forgetting, the authors introduce a **dual-channel attention** mechanism that preserves original features while learning new spatial representations. A **multi-turn Chain-of-Thought reasoning** dataset is constructed with pixel-level, object-level, and scene-level QA pairs, enabling hierarchical spatial understanding.

The method is evaluated on four vision encoders (OpenCLIP, SigLIPv2, DINOv2, DINOv3) across depth estimation, semantic segmentation, 3D scene understanding, robotic control, image classification, and retrieval. Results show consistent gains: e.g., DINOv3 improves from 51.4% to 54.9% on SQA3D (3D scene understanding) and from 88.4% to 90.2% on ImageNet linear probing.

**Strengths**: The core idea of using language as the supervision medium for spatial knowledge injection is original and well-motivated. The multi-turn CoT dataset design and dual-channel attention mechanism are technically sound. The evaluation is broad and covers diverse tasks.

**Key weaknesses**: (1) All main results lack variance/statistical significance, making it impossible to assess gain reliability. (2) The conclusion is incomplete and lacks any limitations discussion. (3) The dual-channel attention's novelty over existing approaches is insufficiently clarified. (4) The introduction narrative can be restructured for stronger motivation. (5) Novelty and comparison with related methods cannot be fully verified due to the absence of external literature retrieval in this run.

**Novelty verdict (deferred, retrieval unavailable)**: Contribution claims C1 (language-guided spatial injection), C2 (dual-channel attention), and C3 (multi-turn CoT spatial reasoning dataset) appear technically sound from manuscript evidence, but external literature comparison is pending manual verification. All novelty conclusions in this report are marked as deferred.

**Recommendation**: Major revision. The paper has a promising core idea and extensive evaluation, but the missing variance reporting, incomplete conclusion, and insufficient comparison with related work require attention before acceptance.

## Strengths
1. **Original core idea with clear motivation**. Using language as the medium to inject 3D spatial knowledge into vision encoders is a genuinely novel approach. The insight that language naturally composes spatial information sequentially (pixel → object → scene) is well-articulated, and the pipeline converting 3D point clouds into hierarchical QA pairs is technically coherent. This contrasts favorably with existing multi-view approaches that require expensive 3D-annotated or simulated data.

2. **Broad and systematic evaluation**. The paper evaluates across 4 vision encoders (OpenCLIP, SigLIPv2, DINOv2, DINOv3) on a diverse set of 8 task categories including depth estimation, segmentation, 3D scene understanding, robotic control, image classification, and retrieval. This breadth convincingly demonstrates transferability of the learned spatial representations. The inclusion of robot learning tasks (CortexBench, 4 domains) is particularly valuable for showing practical downstream utility.

3. **Technically sound dual-channel attention design**. The proposed dual-channel attention mechanism (Eq. 1, Fig. 3) is a principled solution to the catastrophic forgetting problem. The use of a learnable per-channel mixture factor α = sigmoid(a) with zero initialization ensures the fine-tuning starts from the pre-trained state and smoothly transitions. The ablation (Fig. 6) shows that dual-channel outperforms both full fine-tuning and LoRA on classification, providing evidence that the design choice is justified.

4. **Multi-turn CoT reasoning dataset is well-designed**. The hierarchical QA structure (pixel → object → scene) with explicit CoT rationales at each level is a thoughtful dataset design. The ablation (Table 7) shows that the forward order (pixel→object→scene) outperforms reverse and random orders, demonstrating that the hierarchical structure matters — a meaningful empirical finding.

5. **Strong ablation and component analysis**. The paper includes thorough ablations: effect of LLM vs. pixel-level supervision (Table 6), multi-turn ordering (Table 7), single vs. multi-view data (Table 7), naive post-training comparison (Table 8), dual-channel vs. other tuning methods (Fig. 6), and dataset scalability (Fig. 5). These ablations collectively support the design choices and strengthen confidence in the method.

6. **Demonstrated resistance to spatial overfitting**. Table 5 shows that SpatialBoost improves ImageNet classification and retrieval, not just spatial tasks. This suggests that spatial knowledge injection does not degrade general visual representations — a non-trivial result given the risk of catastrophic forgetting.

## Weaknesses
### W1. Missing statistical significance and variance across all core results [Major]

Every main result table (Tables 1, 2, 3, 5) reports point estimates without any measure of variance, confidence intervals, or statistical significance. Only the robot learning results (Table 4) include standard deviations. This is a serious omission because:
- Many improvements are modest (e.g., DINOv3 ImageNet +1.8%, ScanQA BLEU-1 +2.7 points). Without variance, readers cannot assess whether gains are within noise range.
- The paper performs 28+ comparisons across 4 encoders × 7+ tasks, raising multiple-testing concerns.
- Table 4 shows that some standard deviations are large relative to gains (e.g., Adroit: DINOv3 63.9±1.5 → 71.8±3.4, the ±3.4 overlaps with the baseline range).

**Required action**: Report mean±std over at least 3 random seeds for all main results. For key comparisons (e.g., DINOv3 ± SpatialBoost), add a paired significance test (t-test or Wilcoxon) or confidence intervals. This is a Must requirement for the next revision.

### W2. Incomplete conclusion with no limitations discussion [Major]

The Conclusion (Section 5) is a single incomplete sentence followed by figures and references. It does not:
- Summarize what was validated and what remains open.
- Acknowledge any limitations of the approach.
- Discuss failure modes, scope boundaries, or threats to validity.

Key limitations that should be discussed include: (1) dependence on off-the-shelf depth/segmentation/reconstruction models whose errors propagate, (2) reliance on GPT-4o for QA generation (bias, cost, reproducibility), (3) evaluation limited to static scenes and simulated environments, (4) computational cost of the three-stage training pipeline.

**Required action**: Rewrite the conclusion with three clear subsections: validated findings, bounded limitations, and future work. This is a Must requirement.

### W3. Dual-channel attention novelty insufficiently differentiated from prior work [Major]

The paper attributes the dual-channel attention illustration to (Hong et al., 2023a) in the Figure 3 caption but does not explain how SpatialBoost's mechanism differs from or extends that work. The approach of adding a parallel attention branch with learned interpolation resembles adapter-based tuning and residual attention. The ablation compares against LoRA (Fig. 6), which is helpful, but several questions remain unanswered:
- How does dual-channel attention compare to simply adding learnable bias terms to attention outputs?
- What is the additional parameter cost of Attn⁺ vs. the original Attn?
- Is the gradient signal from a frozen LLM rich enough to meaningfully update the vision encoder through the projector and dual-channel layers?

**Required action**: Add a paragraph explicitly comparing dual-channel attention with LoRA, adapters, and (Hong et al., 2023a), stating parameter counts and computational overhead. Add an analysis of gradient flow from frozen LLM to vision encoder.

### W4. Introduction narrative structure weakens impact [Moderate]

The introduction has four paragraphs but lacks a clean Big Picture → Gap → Solution → Evidence → Contribution arc:
- Paragraph 1 is a generic success recitation without establishing the paper's specific motivation.
- Paragraph 2 conflates data types and misses the true differentiator (language as supervision, not less data).
- Paragraph 3 (hypothesis) breaks mid-sentence across a page boundary and uses vague claims about language's advantages.
- Paragraph 4 front-loads implementation details (dual-channel attention) before explaining the core intuition.

**Required action**: Restructure the introduction following the suggested rewrites in annotations 2-5. Ensure each paragraph has a single clear role and builds toward the contribution.

### W5. Overclaiming and insufficiently bounded language [Moderate]

Several statements over-extend the evidence:
- "SpatialBoost even improves the performance of the vision encoders across all benchmarks" (Introduction) — the paper has not shown "all" benchmarks; some results are in the appendix.
- "Our method eliminates the need for joint text-image representation learning by using LLM, thereby enhancing pre-trained models with relevant linguistic information efficiently" (Related Work) — the word "efficiently" has no computational cost evidence.
- "Dual-channel attention uniquely preserves and even enhances pre-trained knowledge" (Ablation) — "uniquely" is too strong given the limited set of baselines compared.

**Required action**: Replace absolutes with bounded language. Remove "efficiently," "uniquely," and "across all benchmarks" unless directly evidenced. Use "consistently improves on the evaluated tasks" instead.

### W6. Limited discussion of training cost and reproducibility [Moderate]

The paper reports model architectures (Qwen-2.0-7B, 2-layer MLP projector) and data volumes (100K single-view + 200K multi-view) but does not report:
- Training GPU hours for each of the three stages.
- Number of trainable parameters in the dual-channel attention module.
- Peak GPU memory usage.
- Inference latency comparison before/after SpatialBoost fine-tuning.

Without these, reviewers cannot assess the practical cost of the proposed method or compare it fairly with alternatives.

**Required action**: Add a table reporting training cost (GPU hours per stage), parameter count (frozen vs. trainable), and inference throughput for representative encoders.

### W7. Novelty and comparison with related work not fully verifiable [Deferred]

Due to Retrieval-Disabled Mode in this run, external literature search was not available. The paper's contribution claims (C1: language-guided spatial injection, C2: dual-channel attention, C3: multi-turn CoT dataset) appear technically sound from manuscript evidence, but verifying whether prior work already covers similar ideas under comparable settings requires manual literature verification. The following questions need resolution:
- Have prior works used LLM-based decoders to inject spatial knowledge into vision encoders (e.g., SpatialVLM [Chen et al., 2024a] listed in the paper's own references)?
- Is the dual-channel attention mechanism significantly different from the approach in Hong et al. 2023a?
- Are there existing spatial VQA datasets with multi-turn hierarchical structure?

**Required action**: Authors should expand the Related Work section to include explicit comparison with the most closely related methods (SpatialVLM, MV-MWM, Hong et al.), stating overlap axes and residual novelty clearly. This weakness is noted as deferred for this review.

### W8. Notation inconsistency in multi-turn conversation definition [Minor]

The formal notation $(x_1^1, x_1^2, \dots, x_4^T, x_4^T)$ contains a typo (repeated $x_4^T$) and ambiguous indexing. It is unclear whether $i$ indexes the reasoning level and $j$ indexes the turn number, or vice versa. The total of 12 turns is stated but not clearly derived from the notation.

**Required action**: Replace with a clearer schema: describe the 4 levels with $k_t$ QA pairs per level, or remove the formal notation in favor of Figure 2's illustration.

### W9. Missing analysis of failure cases and negative results [Minor]

The paper reports only positive results. No failure cases, qualitative analysis of when SpatialBoost underperforms, or discussion of which spatial tasks benefit most vs. least. Including such analysis would significantly strengthen the paper's scientific rigor.

**Required action**: Add a qualitative analysis section (or paragraph) showing examples where SpatialBoost helps most and where gains are marginal, with visual comparisons.

## Score
**Final Score: 6/10**

**Rationale**: The paper presents a creative and well-executed core idea (language-guided spatial knowledge injection), with broad evaluation across diverse tasks and thorough ablations. However, the score is constrained by:

1. **Missing statistical rigor** (W1): Without variance or significance tests on any main result, the empirical claims cannot be verified as reliable. This is a must-fix issue for any publication venue.

2. **Incomplete conclusion** (W2): The current conclusion is not publishable in its present form. A scientific paper requires proper closure with validated findings, limitations, and future directions.

3. **Novelty uncertainty** (W7): Due to the absence of external literature retrieval in this run, novelty claims cannot be fully verified. The authors should strengthen comparison with closest related methods.

4. **Overclaiming** (W5): Several statements exceed the evidence boundary, which reduces overall credibility.

The paper has significant strengths (original idea, broad evaluation, strong ablations) that justify a mid-range score. With proper statistical reporting, expanded conclusion, and bounded claims, the score could reach 7-8/10 in revision.

**Post-Revision Target**: [7, 8]/10