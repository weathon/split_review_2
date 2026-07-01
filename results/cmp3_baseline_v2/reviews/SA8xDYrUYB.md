## Summary

The paper introduces Purrception, a variational flow matching approach for vector-quantized (VQ) image generation. The key idea is to use a categorical posterior over codebook indices while computing velocity fields in the continuous embedding space, thereby combining discrete supervision with continuous transport dynamics. This hybrid formulation provides explicit categorical learning signals, uncertainty quantification over plausible codes, and temperature-controlled generation. Experiments on ImageNet-1k 256×256 show that Purrception converges faster than both continuous flow matching (CFM) and discrete flow matching (DFM) baselines, and achieves competitive FID scores among VQ-based generative models.

## Strengths

- **Novel and well-motivated hybrid formulation.** The paper clearly identifies the core trade-off in VQ latent modeling—continuous methods ignore categorical structure while discrete methods discard geometry—and proposes a principled solution via VFM with a categorical posterior. This is a clean and original contribution.
- **Strong convergence speed results.** Purrception consistently reaches lower FID in fewer training iterations than CFM, CFM-endpoint, and DFM across two DiT backbones (L/2 and XL/2). The reported speedups (up to 3.5×) are practically significant for reducing training cost.
- **Temperature control as a natural byproduct.** The categorical logits enable inference-time temperature scaling, which provides a simple knob to trade off fidelity and diversity. The U-shaped FID curve in Figure 4 and the qualitative examples in Figure 5 convincingly demonstrate this capability, which is absent in continuous flow matching.
- **Clear exposition and thorough baselines.** The paper compares against a wide range of autoregressive, diffusion, masked, and flow-based models in Table 1, and includes two CFM variants (velocity and endpoint prediction) to isolate the effect of the objective. The method is described with sufficient detail for reproducibility.

## Weaknesses

### Fatal
None.

### Major
- **Overstated claim of “competitive with state-of-the-art.”** The final FID of 3.88 (Table 1) is notably higher than top continuous diffusion models (DiT-XL/2: 2.27, SiT-XL/2: 2.06) and some VQ-based methods (Open-MAGVIT2-L: 2.51, LlamaGen-XL: 3.39). While the paper acknowledges this gap, the abstract and introduction still claim “competitive FID scores with state-of-the-art models,” which is misleading. The contribution should be framed more precisely as competitive among VQ-based generative models.
- **Missing ablation to isolate the benefit of categorical supervision.** The comparison with CFM-endpoint is helpful but not a clean ablation because CFM-endpoint uses MSE on continuous embeddings. A direct ablation would compare Purrception (categorical posterior) against a version using a Gaussian posterior (continuous VFM) on the same VQ latents, holding everything else fixed. Without this, it is unclear how much of the gain comes from the categorical objective versus other aspects of the VFM framework.
- **Inconsistent tokenizer usage across experiments.** Convergence experiments (Figure 3) use Stable Diffusion’s vq-f8 tokenizer, while the final FID (Table 1) uses LlamaGen’s vq-ds8-c2i. This makes it difficult to assess whether the convergence advantage transfers to the higher-quality tokenizer. The paper should either use the same tokenizer throughout or justify the choice and show convergence results for both.

### Minor
- **Convergence analysis uses FID-10k instead of the standard FID-50k.** While FID-10k is acceptable for monitoring trends, the final results use FID-50k. The paper should confirm that the convergence trends hold for FID-50k or explain why FID-10k is sufficient.
- **Temperature comparison with DFM is missing.** The paper argues that DFM’s temperature only produces stochastic “hops” while Purrception’s temperature is geometry-aware, but no quantitative comparison is provided (e.g., FID vs. temperature for DFM). Such a comparison would strengthen the claim that Purrception’s temperature control is uniquely beneficial.
- **Limited discussion of CDCD (Dieleman et al., 2022).** The related work mentions CDCD as a similar spirit but does not clearly differentiate Purrception. CDCD also combines categorical supervision with continuous transport (via diffusion) and uses cross-entropy loss. The paper should explicitly state what Purrception adds beyond CDCD (e.g., flow matching formulation, application to VQ latents, temperature scaling analysis).

### Trivial
None.

## Nice-to-Haves

- An ablation study comparing categorical posterior vs. Gaussian posterior on VQ latents.
- Convergence experiments using the same tokenizer as the final FID table.
- A quantitative comparison of temperature scaling between Purrception and DFM.
- Experiments on additional datasets (e.g., LSUN, FFHQ) or higher resolutions to test generalization.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that VFM’s variational view naturally unifies the discrete and continuous aspects of VQ latents: the posterior over endpoints is inherently categorical, yet the resulting velocity field is a continuous expectation over embeddings. This perspective reveals that the “discrete vs. continuous” dichotomy in VQ modeling is artificial—the two can be reconciled by learning a categorical posterior and using it to compute a geometry-aware transport. The temperature scaling analysis further shows that the logits from the categorical posterior provide a principled way to control the bias-variance trade-off in generation, which is not available in purely continuous or purely discrete flow models.

## Suggestions

1. Tone down the claim of “competitive with state-of-the-art” and instead state “competitive among VQ-based generative models” or “approaching the performance of top continuous diffusion models.”
2. Add an ablation study comparing Purrception (categorical posterior) with a continuous VFM variant (Gaussian posterior) on the same VQ latents to isolate the benefit of categorical supervision.
3. Use FID-50k for convergence experiments or at least verify that the trends match FID-50k.
4. Include a comparison of temperature scaling between Purrception and DFM (e.g., FID vs. temperature curves for both).
5. Clarify the distinction from CDCD (Dieleman et al., 2022) in the related work section, highlighting the flow matching formulation and the specific application to VQ latents.

## Score and Decision

**Score:** 6  
**Decision:** Accept

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>