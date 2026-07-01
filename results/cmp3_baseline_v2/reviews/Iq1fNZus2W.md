## Summary

This paper tackles the computational inefficiency of multi-condition control in Diffusion Transformers (DiTs). The authors analyze attention patterns in the “concatenate-and-attend” paradigm and identify substantial redundancy, which they exploit via Patch-wise and Keyword-Aware Attention (PKA). PKA decomposes full attention into Position-Aligned Attention (PAA) for spatial conditions (one-to-one local attention) and Keyword-Scoped Attention (KSA) for subject conditions (attention restricted to keyword-activated regions), supplemented by a condition KV cache and an early-timestep sampling strategy for faster fine-tuning. Experiments on FLUX.1 demonstrate up to 10× inference speedup and 5.12× VRAM reduction for the attention module while maintaining or improving generative quality compared to OminiControl2 and UniCombine.

## Strengths

- **Clear problem identification and motivation:** The paper carefully analyzes attention patterns in multi-condition DiTs and provides concrete evidence (diagonal dominance for spatial conditions, localized activations for subject conditions) that full attention is highly redundant. This motivates the design of specialized, sparse attention modules.
- **Practical and effective efficiency gains:** PAA and KSA are intuitive and directly reduce computational complexity from O(N²) to O(N) for spatial conditions, and substantially prune query-key interactions for subject conditions. The reported 10× speedup and 5.12× VRAM reduction are impressive and address a real bottleneck in multi-condition DiTs.
- **Condition KV cache is a clean practical contribution:** By having condition tokens perform only self-attention (enabling a KV cache), the method eliminates redundant projections across denoising steps without architectural complexity.
- **Early-timestep sampling is well-motivated:** The perturbation analysis (Figure 5) provides empirical support that visual conditions matter most in early denoising stages, and the shifted logit-normal sampling accelerates training convergence.
- **Comprehensive evaluation:** The paper evaluates on three multi-condition tasks with multiple metrics (FID, SSIM, CLIP-I, DINOv2, F1, MSE) and includes ablation studies for each component (PAA vs. sliding window, KSA threshold, early-timestep sampling). Qualitative results also show consistent improvements over baselines.

## Weaknesses

### Fatal
None.

### Major
- **Unclear whether baselines use the same base model:** The paper fine-tunes FLUX.1 with LoRA and compares against OminiControl2 and UniCombine, but it does not explicitly state whether these baselines also use FLUX.1 as their backbone. If the baselines use a different architecture (e.g., SD3), then the efficiency and quality comparisons may be confounded by the base model rather than the conditioning mechanism. This is critical for a fair evaluation and must be clarified.

### Minor
- **KSA temporal consistency assumption is not quantitatively verified:** The mask computed at timestep t is reused at t+1, motivated by temporal consistency. The paper does not provide quantitative evidence (e.g., mask overlap across steps) that this assumption holds reliably across different subjects and noise levels. A failure of this assumption could lead to missing important regions or artifacts.
- **Early-timestep sampling ablation lacks quantitative metrics:** Figure 11 shows only qualitative convergence. Quantitative results (e.g., FID or CLIP scores at different iterations) would strengthen the claim that early-timestep sampling accelerates convergence and improves fidelity.
- **No comparison with general sparse attention baselines:** The paper compares PAA only to sliding window attention with small windows. It would be informative to compare against more general sparse attention methods (e.g., Reformer-style LSH attention, top-k sparse attention) to better contextualize the advantages of the condition-specific design.
- **Missing details on keyword extraction for KSA:** The paper mentions “a small set of keyword tokens K” (typically 1–2 tokens) but does not specify how these keywords are extracted from the prompt or whether this process is automated. The practical usability of KSA depends on this step.

### Trivial
- Figure 2 and Figure 3 captions contain duplicated text from the main text, making them slightly redundant.

## Nice-to-Haves
- A quantitative study of mask consistency across denoising steps for KSA would strengthen the temporal consistency argument.
- Including a baseline that uses full attention on the same FLUX.1 backbone (without any sparse modifications) would clarify the absolute efficiency gain of PKA.
- Ablation on the number of keyword tokens and automatic keyword selection methods.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

1. Clarify whether OminiControl2 and UniCombine baselines are built on the same base model (FLUX.1) and, if not, conduct a controlled experiment where all methods share the same backbone.
2. Provide quantitative evidence of mask temporal consistency for KSA (e.g., IoU between masks at consecutive timesteps averaged over many samples).
3. Add quantitative metrics (FID, CLIP scores) for the early-timestep sampling ablation to demonstrate convergence speed more rigorously.
4. Compare against a general sparse attention baseline (e.g., random masking or top-k attention) to isolate the benefit of the condition-specific design.
5. Describe the keyword extraction procedure in detail (e.g., from prompt parsing, using attention weights, or manual annotation).

## Score and Decision

The paper presents a well-motivated and practically effective solution to an important computational bottleneck in multi-condition DiTs. The efficiency gains are substantial, the ablations support the design choices, and the generation quality is competitive or better than existing methods. However, the lack of clarity about the base model used in baseline comparisons is a significant concern that could affect the fairness of the results. Assuming this can be clarified, the contribution warrants acceptance.

**Score:** 7

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>