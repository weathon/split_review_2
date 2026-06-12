## Summary
This paper proposes Patch-wise and Keyword-Aware Attention (PKA) to address the computational bottleneck of multi-condition control in Diffusion Transformers. The method decomposes the costly full-attention mechanism into two efficient specialized modules—Position-Aligned Attention (PAA) for spatial conditions via one-to-one patch correspondence, and Keyword-Scoped Attention (KSA) for subject-driven conditions via keyword-guided relevance masking—plus an early-timestep sampling strategy for training. The method reports up to 10× inference speedup and 5.12× VRAM reduction for the attention module while maintaining or improving generation quality on three multi-condition tasks.

## Strengths
- **Clear and well-motivated problem**: The paper convincingly identifies the computational redundancy in the "concatenate-and-attend" paradigm through concrete attention visualizations (Figures 2, 3), establishing that spatial conditions are diagonal-dominant and subject conditions activate only sparse regions. This empirical grounding directly motivates the proposed solution.
- **Impressive and well-documented efficiency gains**: Figures 7 and 8 demonstrate consistent, scalable speedup (3.90× at 4 conditions to 10× at 16 conditions) and VRAM reduction (2.46× to 5.12×) over strong baselines. The scaling behavior is particularly compelling—PKA's cost grows nearly linearly while baselines grow quadratically.
- **Comprehensive ablation studies**: Each proposed component (PAA, KSA threshold, early-timestep sampling) is individually validated with both qualitative and quantitative evidence, providing clear insight into their individual contributions and trade-offs. The KSA threshold ablation (Figure 10) is especially well-designed, showing a graceful degradation curve.
- **Quantitative improvements across multiple tasks**: Table 1 shows that PKA achieves best or near-best results on generative quality (FID, SSIM) and subject consistency (CLIP-I, DINOv2) across all three evaluated tasks, suggesting the efficiency does not come at the cost of quality.
- **Clean architectural design**: The Condition Cache mechanism, enabled by the structural choice that condition tokens only self-attend, is elegant and eliminates redundant computation across denoising steps. The overall method adds minimal architectural complexity.

## Weaknesses
### Fatal
None.

### Major
- **Underspecified keyword extraction mechanism**: KSA relies on identifying a small set of keyword tokens K (1–2 tokens) from the text prompt, yet the paper never specifies how these keywords are identified. This is a critical component of the method—without a clear mechanism (e.g., noun phrase extraction, attention-based selection, or user annotation), reproducibility is compromised and the practical applicability of KSA is unclear.
- **Notable controllability regression on Subject-Canny task**: The paper claims "highly competitive" controllability with "minor exception," but the Subject-Canny F1 score gap is substantial: 0.414 vs. UniCombine's 0.551 (a 25% relative decrease). This is the primary controllability metric for spatial conditions, and this gap raises questions about whether PAA's one-to-one constraint loses important structural information for fine-grained edge adherence.
- **Condition Cache quality impact unjustified**: The KV cache for condition tokens is reused across all denoising steps after the first computation. While this is efficient, no ablation or analysis is provided to show this doesn't degrade quality. Condition representations may need to adapt as the noisy image evolves, and the paper should demonstrate this assumption is safe.

### Minor
- **No error bars or statistical significance**: All quantitative results in Table 1 are single-run numbers. Given the stochastic nature of diffusion models, variance estimates (e.g., across multiple seeds or prompt sets) are important for assessing whether differences—especially marginal ones—are meaningful.
- **Limited condition type diversity**: Only canny edges, depth maps, and subject images are evaluated. Segmentation maps, pose keypoints, or scribble maps would strengthen the claim that the method generalizes across spatial condition types.
- **Early-timestep sampling analysis is shallow**: The perturbation experiment (Figure 5) provides motivation, but only SSIM is measured, and only for a single example. A more systematic analysis across diverse images and metrics, or theoretical justification for why visual conditions matter more at early timesteps, would strengthen this contribution.
- **Practical speedup framing**: The 10× speedup at 16 conditions is dramatic but represents an extreme scenario. The more realistic 2–3 condition case yields 3.9× speedup, which is still good but less headline-grabbing. The paper could better contextualize practical usage scenarios.

### Trivial
- The paper refers to FLUX.1 as the backbone but doesn't specify which variant (e.g., FLUX.1-dev vs. FLUX.1-schnell), which matters for reproducibility.

## Nice-to-Haves
- A comparison with other efficient attention mechanisms for transformers (e.g., FlashAttention, Linformer) applied to the multi-condition setting, to better position the contribution relative to the broader efficient attention literature.
- Analysis of when the temporal consistency assumption in KSA might break down (e.g., cases where the subject location shifts significantly between denoising steps).
- User study or human evaluation to complement the automated metrics, especially given the qualitative differences shown in Figure 6 are described as "nuanced."

## Novel Insights
The paper's central novel insight is that multi-condition attention redundancy is condition-type-specific: spatial conditions exhibit diagonal-dominant attention (enabling position-aligned one-to-one correspondence), while subject-driven conditions exhibit keyword-correlated sparse activation (enabling mask-based pruning). This typology of redundancy is a useful conceptual contribution that could inform future work on multi-condition architectures beyond the specific PKA mechanism. The early-timestep sampling insight—that visual conditions disproportionately influence early denoising stages—also provides a practical and potentially generalizable training strategy for fine-tuning conditional diffusion models.

## Suggestions
- Add a clear, detailed description of how keyword tokens are identified from the text prompt for KSA (e.g., via NLP parsing, cross-attention peaks, or a learned selector). Without this, the method cannot be reproduced.
- Include an ablation study comparing generation quality with and without the Condition Cache to verify the reuse assumption does not harm output fidelity.
- Report standard deviations or confidence intervals for the quantitative metrics in Table 1.
- Provide a more nuanced discussion of the Subject-Canny F1 gap rather than characterizing a 25% relative decrease as a "narrow margin."

## Score and Decision
The paper presents a practical and well-motivated solution to a real computational bottleneck in multi-condition DiTs. The efficiency gains are substantial and convincingly demonstrated, the architectural design is clean, and the ablation studies are thorough. However, the underspecified keyword extraction mechanism, the notable controllability regression on the Canny task, and the unjustified condition cache assumption represent meaningful gaps that limit confidence in the method's completeness and generalizability. These are resolvable issues, and the core contribution is valuable enough to warrant consideration.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept