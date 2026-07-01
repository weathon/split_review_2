## Summary

The paper introduces Purrception, which adapts Variational Flow Matching (VFM) to vector-quantized (VQ) image generation by learning a categorical variational posterior over codebook indices while computing velocity fields in the continuous embedding space. This hybrid approach combines the geometric awareness of continuous flow matching with the discrete supervision of categorical methods. On ImageNet-1k 256×256, Purrception converges 1.65×–3.5× faster than continuous and discrete flow matching baselines, achieves a competitive FID of 3.88, and provides a practical temperature control mechanism at inference.

## Strengths

- **Well-motivated hybrid formulation (Section 3.1, Eqs. 11–14).** The paper clearly identifies the tension between continuous methods (which ignore categorical structure) and discrete methods (which discard embedding geometry), and shows how a categorical variational posterior within VFM resolves it. The derivation from Eq. 11 through Eq. 14 is sound and directly follows from prior VFM theory. The velocity field is computed as an expectation over codebook embeddings weighted by the predicted posterior (Eq. 13), naturally blending discrete supervision with continuous transport.

- **Convergence speed advantage is demonstrated with consistent evidence (Figure 3, Section 4.1).** Across two backbone sizes (DiT-L/2, DiT-XL/2) and three baselines (CFM, CFM-endpoint, DFM), Purrception reaches lower FID-10k scores in substantially fewer iterations (1.65×–3.5× faster). The advantage is visible, consistent across settings, and practically meaningful for reducing training cost.

- **Temperature provides a principled and controllable quality-diversity knob (Section 4.2, Figures 4 & 5, Eq. 15).** Because the model outputs logits over codebook indices, the softmax temperature can be varied at inference time to trade off fidelity and diversity. The U-shaped FID-50k curve in Figure 4 demonstrates measurable impact, and qualitatively the progression from simplistic (low τ) to detailed but noisier (high τ) generations is visually compelling. This control is unique to the hybrid formulation and absent in both CFM (no logits) and DFM (collapsed indices).

## Weaknesses

### Fatal
None.

### Major

1. **The textual characterization of quantitative results in Table 1 is overstated.** The paper states Purrception "firmly establishes [it] as a novel, state-of-the-art approach, among VQ-based latent generative models" and "shows stronger performance against most autoregressive methods" (Section 4.3, p.7). Table 1 tells a different story: Purrception (FID 3.88) is outperformed by multiple VQ-based methods — ViT-VQGAN (3.04), RQTransformer (3.80), LlamaGen-XL (3.39), and Open-MAGVIT2-L (2.51). Among clearly autoregressive methods (VQGAN, ViT-VQGAN, RQTransformer, LlamaGen-XL), Purrception beats only one (VQGAN, 5.20). The claim of "state-of-the-art among VQ-based latent generative models" is not supported by the paper's own data. The paper would be markedly stronger if it reframed its quantitative positioning around competitiveness (which is fair) rather than superiority. The convergence speed advantage (Figure 3) and temperature controllability are the paper's genuine differentiators; these should be the headline claims.

2. **Classifier-free guidance (CFG) is used but never described.** Table 1 reports Purrception with cfg=1.3, but the paper contains zero explanation of how CFG is applied to a model that outputs a categorical distribution over codebook indices rather than a velocity or score. Is the velocity field extrapolated before computing the expectation in Eq. 13? Are the logits extrapolated? The guidance mechanism is central to the reported FID of 3.88, and omitting it makes the primary quantitative result difficult to reproduce or verify. This is the single most important missing methodological detail.

### Minor

3. **Convergence comparison uses FID-10k rather than the standard FID-50k, and final FID-50k for baselines is not reported (Section 4.1, Figure 3).** FID-10k has higher variance and is less standard in the ImageNet generation literature. More importantly, the paper shows that Purrception reaches lower FID-10k *earlier* but does not report the final FID-50k that the CFM and DFM baselines would achieve with extended training. This makes it unclear whether the convergence claim is about training efficiency (reaching a given quality level faster) or model capacity (reaching a fundamentally better final quality). The claim is still meaningful in the former sense, but the evidence is weaker than it could be.

4. **No variance or confidence intervals reported for any quantitative result.** FID-10k is known to have nontrivial variance, and no multiple-seed statistics or error bars are provided for any of the reported FID scores in Table 1, Figure 3, or Figure 4.

### Trivial
None.

## Nice-to-Haves

- **Report wall-clock sampling time.** The convergence experiment uses 100 Euler steps while the Table 1 result uses 250 steps, but no sampling cost comparison is provided. This would help practitioners evaluate the practical trade-off.
- **Ablate the categorical posterior vs. hard endpoint prediction.** An ablation replacing the soft categorical distribution with hard argmax decoding during training would isolate whether the benefit comes from the categorical objective itself or from the continuous relaxation.
- **Ablate codebook size or embedding dimension.** The method's behavior likely depends on how well the codebook embeddings capture geometry; this is not explored.

## Removed Points

- *Novelty relative to CatFlow is modest.* — **Removed.** The paper properly cites CatFlow as prior work (lines 15, 76, 123) and frames Purrception as "an adaptation of VFM to vector-quantized latents" (line 32). The positioning is appropriate; applying CatFlow's framework to large-scale VQ image generation with DiT backbones, CFG integration, and temperature control is a nontrivial extension.
- *"CFM cannot use temperature at all" is overstated.* — **Removed.** The paper states CFM "cannot use temperature at all, since it lacks logits" (line 30). This is factually correct for flow matching models.
- *Missing appendix details about per-patch posterior computation, linear head, etc.* — **Removed.** These details are stated to be in Appendix C, which is stripped by the parser.
- *Eq. 6 notation could be clearer.* — **Removed.** Pure presentation nitpick.
- *Purrception has more parameters than DiT-XL/2 but parameter argument cuts both ways.* — **Removed.** The paper's parameter comparison is specifically to autoregressive methods (where it genuinely has fewer parameters), not to DiT.

## Novel Insights

The harsh review surfaces one genuinely insightful observation that goes beyond the paper's own contributions: the central tension between how the paper frames itself and what the evidence actually supports. The paper's strongest empirical claim — convergence speed — is largely independent of its most impressive-looking table entry (FID 3.88 with CFG). This means the paper has two separable contributions (training efficiency and final quality), and the evidence for the first is much stronger than for the second. A reframed paper that leads with the convergence result and positions Table 1 as evidence of competitiveness (rather than superiority) would be more accurate and more convincing.

## Suggestions

1. **Reframe the quantitative claims.** Replace "state-of-the-art among VQ-based models" and "stronger performance against most autoregressive methods" with honest characterizations such as "competitive FID" and "outperforms all discrete diffusion and masked generative models while being competitive with autoregressive approaches." Let the convergence speed and temperature control be the headline contributions.
2. **Describe the CFG mechanism explicitly.** Show how guidance is applied — whether to the velocity field, the logits, or the posterior probabilities — and justify the choice of cfg=1.3. Without this, the FID in Table 1 is not reproducible.
3. **Report final FID-50k for all convergence baselines** or clearly state that the convergence claim is about reaching a given quality earlier, not about achieving a better final quality.
4. **Add error bars or confidence intervals** for the main FID results.

## Score and Decision

**MY FINAL SCORE: <score>6.0</score>**
**MY FINAL DECISION: <decision>Accept</decision>**