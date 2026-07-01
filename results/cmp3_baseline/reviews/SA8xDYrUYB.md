## Summary

The paper introduces Purrception, which adapts Variational Flow Matching (VFM) to vector-quantized (VQ) image generation. Instead of purely continuous or purely discrete transport, the method learns a categorical posterior over codebook indices while computing velocity fields in the continuous embedding space. This hybrid approach provides explicit categorical supervision (cross-entropy over codes) while retaining smooth, geometry-aware flow dynamics. Experiments on ImageNet-1k 256×256 show faster convergence than both continuous and discrete flow matching baselines, competitive FID scores (3.88), and a temperature control mechanism that arises naturally from the categorical logits.

## Strengths

- **Well-motivated hybrid formulation:** The paper clearly identifies the core tension in VQ-latent generation (continuous vs. discrete trade-off) and proposes a principled solution via VFM with a categorical posterior. The motivation is presented concisely and convincingly.
- **Faster convergence demonstrated empirically:** Across two DiT backbones, Purrception reaches lower FID in fewer training iterations compared to continuous flow matching (CFM) and discrete flow matching (DFM). This training efficiency is a practically valuable contribution.
- **Temperature control via logits:** The categorical posterior naturally provides softmax logits, enabling inference-time temperature scaling. The paper shows a clear U-shaped FID vs. temperature curve and qualitative examples, highlighting a unique capability absent in continuous or discrete flow models.
- **Solid empirical scope:** Experiments include two VQ tokenizers (vq-f8, vq-ds8-c2i), two DiT backbones (L/2, XL/2), and comparisons against many autoregressive, diffusion, and masked generative baselines. Code release supports reproducibility.

## Weaknesses

### Fatal
None.

### Major
1. **Questionable DFM baseline implementation:** In Figure 3, DFM achieves FID-10k scores around 30–40, which is far worse than expected for a discrete flow model on VQ latents (e.g., VQ-Diffusion reports FID ~5.8 on ImageNet 256×256). This suggests the DFM baseline may be suboptimally tuned or implemented, undermining the fairness of the convergence comparison. Without a stronger DFM baseline or more implementation details, the claimed speed advantage over DFM (3.0–3.5×) is less convincing.

2. **Limited absolute performance:** The final FID of 3.88 (Table 1) trails behind top continuous diffusion models (DiT-XL/2: 2.27, SiT-XL/2: 2.06) and even some autoregressive models (ViT-VQGAN: 3.04, LlamaGen-XL: 3.39). The authors attribute this to VQ tokenizers and shorter training, but this gap diminishes the significance of the contribution relative to state-of-the-art image generation.

3. **Moderate novelty:** The core idea—using a categorical variational posterior in VFM—was already introduced in CatFlow (Eijkelboom et al., 2024) for discrete data. Applying it to VQ image generation is a natural and worthwhile extension, but the methodological novelty is incremental. The paper does not introduce new training objectives, architectures, or theoretical insights beyond the specific hybrid application.

### Minor
1. **No experimental comparison to CDCD:** The related work mentions Continuous Diffusion for Categorical Data (CDCD) as a similar spirit of combining categorical supervision with continuous transport, but no experimental comparison or discussion of differences is provided. This would strengthen the paper’s positioning.
2. **FID values missing from temperature plot:** Figure 4 shows a qualitative U-shaped curve but does not report the precise FID-50k numbers. A table with the exact values would make the result more concrete and reproducible.
3. **Inconsistent naming:** The paper inconsistently uses “Purrception” and “Purception” (e.g., Table 1 says “Purception” while the rest uses “Purrception”). This should be unified.

### Trivial
- The abstract and conclusion are slightly verbose; some sentences could be tightened.

## Nice-to-Haves

- Include wall-clock training time to complement iteration-based convergence comparison.
- Train Purrception for the same number of iterations as DiT (e.g., 7M) to see if the gap to continuous diffusion narrows further.
- Provide an ablation replacing the categorical posterior with a Gaussian (standard VFM) to directly isolate the benefit of categorical supervision.
- Discuss the impact of codebook size and embedding dimension on performance and convergence.

## Novel Insights

The key insight—that VQ latents possess a natural dual discrete-continuous structure that neither continuous-only nor discrete-only methods fully exploit—is clear and well-argued. The connection to VFM’s variational posterior allows the model to “have its cake and eat it too”: categorical cross-entropy provides a strong learning signal, while the expectation over embeddings yields smooth flows. The temperature knob is a clean consequence of this design and is demonstrated effectively. However, these insights are largely consistent with the prior VFM/CatFlow framework, and the paper does not produce a surprising or counterintuitive finding beyond the application domain.

## Suggestions

- For the camera-ready version, ensure the DFM baseline is properly tuned (e.g., use the same DiT backbone with a standard discrete flow objective like masking or multinomial diffusion). Consider adding a stronger discrete baseline such as VQ-Diffusion re-implemented in the DiT framework.
- Provide explicit FID-50k values for each temperature setting in a small table rather than relying solely on a plot.
- Add a brief experimental comparison to CDCD (Dieleman et al., 2022) on ImageNet, or at least discuss why a comparison is difficult and what the key differences are.
- Unify the paper’s naming to “Purrception” throughout.

## Score and Decision

The paper addresses a well-motivated problem with a clean method and demonstrates tangible benefits (faster convergence, temperature control). The writing is clear and the experiments are generally thorough. However, concerns about the DFM baseline’s validity and the modest absolute FID scores (despite the authors’ acknowledgement) prevent the paper from being a strong accept. The methodological novelty is moderate for ICLR.

**Score:** 6  
**Decision:** Accept

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>