## Summary

The paper introduces Purrception, which adapts Variational Flow Matching (VFM) to vector-quantized latent spaces for image generation by using a categorical posterior over codebook indices while computing velocity fields in continuous embedding space. The method is evaluated on class-conditional ImageNet-1k 256×256, demonstrating faster convergence than continuous and discrete flow matching baselines, competitive FID within the VQ model class, and a natural temperature control mechanism arising from the categorical logits.

## Strengths

- **Well-motivated hybrid formulation.** The paper clearly identifies a real tension in existing approaches: continuous flow matching ignores categorical structure while discrete flow matching discards geometric information. The VFM framework provides a principled resolution via categorical posteriors over codebook indices with velocities in continuous space (Eq. 13–14). This is a clean, theoretically grounded design.

- **Substantial convergence speed improvements.** The convergence experiments (Figure 3) are well-designed with consistent baselines. Purrception converges 1.65–3.0× faster than CFM variants and 3.0–3.5× faster than DFM across both DiT-L/2 and DiT-XL/2 backbones. The fair comparison against CFM-endpoint (same continuous space, different objective) isolates the contribution of the categorical supervision signal.

- **Temperature control as a natural property.** The softmax temperature mechanism (Figure 4, 5) is not artificially imposed but emerges from the categorical formulation. The U-shaped FID curve across temperatures is clearly demonstrated and provides practical controllability absent in continuous flow matching. Finding that τ ≈ 0.8–0.9 outperforms τ = 1.0 (the training temperature) is a useful practical insight.

- **Competitive within the VQ model class.** In Table 1, Purrception (FID 3.88) outperforms all discrete diffusion/masked models (VQ-Diffusion at 5.84, Implicit Timestep Model at 5.30) and most autoregressive methods, while using fewer parameters than several of them. This establishes the hybrid approach as effective within its natural comparison class.

- **Clear presentation.** The paper is well-written with a logical flow from motivation through derivation to experiments. The pipeline diagram (Figure 2) and the synthesis of contributions in the conclusion effectively communicate the approach.

## Weaknesses

### Fatal
None.

### Major

- **Incomplete comparison with continuous diffusion baselines.** Table 1 compares against DiT-XL/2 (FID 2.27) and SiT-XL/2 (FID 2.06), acknowledging the gap. However, the paper attributes this to (1) better VAE tokenizers and (2) longer training (DiT/SiT use ~6.4M iterations vs. Purrception's 3.5M). This creates a confounded comparison: Purrception uses vq-ds8-c2i tokenizer while DiT/SiT use continuous VAEs. The paper would be significantly stronger if it provided results with the same backbone under matched training budgets, or at minimum a clear ablation isolating tokenizer quality from method quality. As stated, the reader cannot determine whether the gap is due to the method, the tokenizer, or training duration.

- **Narrow experimental scope.** All experiments are on a single dataset (ImageNet-1k) at a single resolution (256×256) with a single autoencoder configuration. The paper acknowledges this in the limitations but does not provide even preliminary evidence on other datasets, resolutions, or different VQ codebook sizes. This limits confidence in the generalizability of the reported convergence advantages.

### Minor

- **CFM-endpoint convergence fairness on DiT-XL/2.** The paper reports Purrception converges 2.3× faster than CFM-endpoint on DiT-XL/2. However, convergence is measured at the final FID of CFM-endpoint, which may not reflect what CFM-endpoint would achieve with extended training. Figure 3b suggests CFM-endpoint is still improving at 2M iterations, so the "2.3× faster" claim depends on the comparison endpoint.

- **Temperature analysis could be deeper.** The temperature experiments fix τ during training at 1.0 and vary only at inference. It would be valuable to know: (a) whether jointly training with a temperature schedule improves final quality, (b) how temperature interacts with classifier-free guidance scale, and (c) whether the optimal temperature is consistent across different class conditioning scales. The paper acknowledges some of these as future work but even one more ablation would strengthen the contribution.

- **Two different tokenizers across experiments.** Convergence experiments use Stable Diffusion's vq-f8 (Section 4.1), while the main results use LlamaGen's vq-ds8-c2i (Section 4.3). While this is likely driven by availability of baseline numbers, it means the convergence speed findings don't directly apply to the reported FID of 3.88.

### Trivial
None.

## Nice-to-Haves

- A comparison of inference speed (wall-clock sampling time) against autoregressive baselines would strengthen the efficiency argument.
- Exploring whether the convergence advantage scales with larger models (e.g., DiT-XXL) or higher resolutions would be valuable future work.
- A comparison with CDCD-style approaches adapted to image generation would more clearly delineate the contribution.

## Novel Insights

The paper's genuinely novel insight is that the dual discrete-continuous nature of VQ latents maps naturally onto VFM's framework: the posterior over endpoints is inherently categorical (since endpoints are codebook vectors), which means categorical supervision and continuous transport are not competing objectives but complementary aspects of a single formulation. This is a clean theoretical observation that turns what is normally seen as a modeling challenge (the discrete-continuous tension) into a feature. The temperature control mechanism is not an ad-hoc addition but falls out directly from this formulation, providing a principled quality-diversity knob that is unique to this hybrid setting.

## Suggestions

- Provide results with a matched training schedule and tokenizer comparison to isolate the method's contribution from confounds. At minimum, train Purrception for 6.4M iterations with the same tokenizer as the continuous baselines.
- Add at least one experiment on a different resolution (e.g., 512×512) or dataset to demonstrate generalizability of the convergence advantage.
- Explore the interaction between temperature τ and classifier-free guidance scale, which is likely the most practically relevant aspect of the temperature mechanism.

## Score and Decision

The paper presents a theoretically well-motivated and practically useful contribution: applying VFM to VQ latent spaces yields faster convergence than both continuous and discrete alternatives, and temperature control emerges naturally from the formulation. The method is clearly described and the convergence experiments are well-designed with fair baselines. However, the main FID results are not state-of-the-art relative to continuous diffusion, the experimental scope is narrow (single dataset, single resolution), and the comparison with top methods is confounded by different tokenizers and training durations. Within the VQ model class, the results are competitive. This is a solid incremental contribution that advances the understanding of how to handle VQ latents in flow-based generative models, though it does not yet demonstrate clear superiority over the best existing approaches.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept