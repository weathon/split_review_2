## Summary
# Final Review Report

## Summary

This paper introduces Purrception, a variational flow matching approach adapted for vector-quantized (VQ) image generation. The key idea is to use a categorical variational posterior over codebook indices within the Variational Flow Matching (VFM) framework, enabling the model to learn from discrete supervision (cross-entropy loss) while maintaining continuous transport dynamics in the embedding space. This hybrid design aims to combine the geometric awareness of continuous methods with the categorical structure of discrete approaches.

The paper evaluates Purrception on ImageNet-1k 256×256 using DiT-L/2 and DiT-XL/2 backbones. Empirical results show faster convergence compared to continuous flow matching (CFM) and discrete flow matching (DFM) baselines, and a competitive FID of 3.88 among VQ-based generative models. The method also enables temperature-controlled generation via softmax logit scaling at inference time.

**Overall assessment:** The paper presents a technically sound adaptation of VFM to the VQ latent setting and provides useful empirical evidence of faster convergence. However, several claims are imprecisely scoped (e.g., "state-of-the-art among VQ models" is contradicted by Open-MAGVIT2-L's superior FID), and the novelty relative to prior hybrid approaches (particularly CDCD, Dieleman et al. 2022) requires clearer differentiation. The convergence analysis lacks statistical rigor (single-run, no variance reported). The method's core theoretical contribution is incremental — adapting an existing framework (VFM) to a new domain (VQ image generation) — and several published baselines achieve substantially better FID scores. A major revision is needed to tighten claim boundaries, add statistical validation, and honestly position the contribution relative to related work. External literature verification was unavailable in this run (API unavailable); novelty conclusions are deferred for manual verification.

## Strengths
1. **Sound technical adaptation:** The paper correctly identifies the core tension in VQ latent modeling — discrete indices vs. continuous embeddings — and provides a principled adaptation of VFM to this setting. The derivation of the categorical posterior velocity field (Eq. 12-13) is clear and mathematically well-motivated.

2. **Empirical convergence advantage:** The convergence speed comparison (Figure 3) is the paper's strongest empirical contribution. Across two DiT backbones, Purrception consistently reaches target FID values in fewer training iterations than both continuous and discrete flow matching baselines, which is practically meaningful for reducing training compute.

3. **Temperature controllability:** The demonstration that inference-time softmax temperature tuning provides a quality-diversity tradeoff (Figures 4-5) is a practical advantage over pure CFM (which lacks logits) and is clearly attributable to the categorical posterior formulation. The U-shaped FID-vs-temperature curve is well-characterized.

4. **Reproducibility effort:** The paper provides pseudocode (Appendix B), detailed implementation settings (Appendix C), and a publicly released codebase, which supports reproducibility.

5. **Honest limitation discussion:** The Limitations section acknowledges the reliance on a fixed pretrained VQ autoencoder and the performance gap relative to top continuous diffusion models, which provides readers with a realistic view of the method's current scope.

## Weaknesses
### W1. Overclaiming "state-of-the-art" among VQ models (Major)
**Location:** Page 1 - Section 4.3, Table 1 commentary
**Evidence:** The text claims Purrception "firmly establishes [itself] as a novel, state-of-the-art approach, among VQ-based latent generative models." However, Table 1 shows Open-MAGVIT2-L achieves FID 2.51 with 804M parameters — substantially outperforming Purrception's FID 3.88 (750M params). The claim is factually incorrect as stated.
**Impact:** Overclaiming undermines scientific credibility and can mislead readers about the method's relative position.
**Repair:** Replace with bounded language: "Purrception achieves competitive results among VQ-based flow matching methods, outperforming several discrete diffusion and autoregressive VQ approaches." Remove the "state-of-the-art" characterization.

### W2. Insufficient statistical rigor in convergence analysis (Major)
**Location:** Page 1 - Section 4.1
**Evidence:** Convergence speed comparisons (1.65×, 3.0×, 2.3×, 3.5×) are based on single-run FID-10k curves without confidence intervals or multi-seed evaluation. The checkpoint comparisons (e.g., "1M iterations matches DFM's final score after ~325k iterations") do not clearly specify the baseline's reference iteration. FID-10k evaluation itself has variance, so single-curve convergence comparisons are unreliable.
**Impact:** Without variance reporting, readers cannot assess whether the observed speed advantage is statistically significant or within run-to-run noise.
**Repair:** Report FID-10k mean ± std over ≥3 seeds for at least one backbone setting. Clarify the exact baseline iteration used for speedup calculations. Consider reporting area-under-convergence-curve (AUC) as a holistic metric.

### W3. Equation (11) contains a conditioning direction error (Major)
**Location:** Page 1 - Section 3.2, Eq. (11)
**Evidence:** Eq. (11) reads $u_t(z_t) = \mathbb{E}_{p_t(z_t|z_1)}[u_t(z_t|z_1)]$, but comparing with Eq. (3) — which has $\mathbb{E}_{p_t(x_1|x)}[u_t(x|x_1)]$ — the conditioning should be $p_t(z_1|z_t)$, i.e., the posterior over endpoints given the current state. The current expression incorrectly conditions on the endpoint $z_1$ to predict $z_t$, which is the forward transition direction.
**Impact:** This typographical error in a critical equation could confuse readers about the theoretical foundation. While subsequent equations (12-14) correctly treat the posterior $q_t^\theta(c|z_t)$, the error should be corrected.
**Repair:** Replace $p_t(z_t|z_1)$ with $p_t(z_1|z_t)$ in Eq. (11). Verify that the surrounding text also reflects the correct conditioning direction.

### W4. Insufficient differentiation from CDCD (Moderate)
**Location:** Page 1 - Introduction P3, Section 5 (Related Work)
**Evidence:** The Introduction claims the VQ latent challenge is "not addressed by purely continuous or discrete methods," yet the Related Work acknowledges CDCD (Dieleman et al., 2022) "follows the same general spirit of combining categorical supervision with continuous transport." This creates a contradiction: the novelty framing in the Introduction is stronger than the Related Work admits. The paper does not clearly articulate what distinguishes Purrception from CDCD beyond domain (images vs. language) and framework (flow matching vs. diffusion).
**Impact:** Reviewers familiar with CDCD may view Purrception as an incremental domain transfer rather than a genuinely new method.
**Repair:** Add explicit comparison in Section 3 or 5: (a) CDCD uses learned embeddings vs. fixed VQ codebook, (b) CDCD targets 1D sequences vs. 2D grid latents, (c) Purrception's velocity-field formulation via VFM provides a different theoretical grounding than diffusion denoising.

### W5. Conclusion introduces unsupported claims (Moderate)
**Location:** Page 1 - Section 6, Limitations and Future Work
**Evidence:** The sentence "because the model remains a continuous flow, it supports distillation into highly efficient, few-step samplers and can incorporate guidance" is speculative — no distillation experiments are conducted or referenced. This violates the principle that conclusions should summarize validated findings.
**Impact:** Readers may mistakenly believe distillation performance has been demonstrated, leading to overestimation of practical readiness.
**Repair:** Move distillation and guidance claims to a dedicated "Future Work" paragraph. In the Limitations section, restrict to experimentally validated limitations only.

### W6. Single-dataset evaluation limits generalization claims (Moderate)
**Location:** Page 1 - Section 4
**Evidence:** All experiments are conducted on ImageNet-1k 256×256. While this is a standard benchmark, the paper's claims about training efficiency and FID competitiveness are dataset-specific. The method's behavior on other datasets (e.g., LSUN, FFHQ, or higher resolutions) is unknown.
**Impact:** The generality of the approach cannot be assessed from the current evidence.
**Repair:** Acknowledge this limitation explicitly in the abstract and conclusion. Consider adding at least one additional dataset experiment (e.g., FFHQ or a smaller-scale dataset) to demonstrate generality.

### W7. Missing baseline: VAE-latent version of Purrception (Minor)
**Location:** Page 1 - Section 4.3
**Evidence:** The paper attributes Purrception's FID gap relative to DiT/SiT to VAE vs. VQ tokenizer quality and longer training, but provides no controlled experiment to validate these explanations.
**Impact:** The causal explanation for the performance gap remains speculative.
**Repair:** Either train Purrception on VAE latents (removing quantization) and compare, or train Purrception for the same number of iterations as DiT-XL/2 (7M) and report the result. A negative result (gap persists) would strengthen the tokenizer-quality explanation; a positive result (gap narrows) would show training duration is the key factor.

### W8. Mean-field VFM assumption not discussed (Minor)
**Location:** Page 1 - Section 2.2
**Evidence:** The text states the variational approximation factorizes dimension-wise but does not discuss the limitations of this mean-field assumption. In standard variational inference, mean-field underestimates posterior correlations, which could affect sample quality for structured image latents.
**Impact:** Readers familiar with VI will notice the missing caveat.
**Repair:** Add one sentence acknowledging the mean-field approximation and its potential limitations, citing standard VI references.

## Score
**Final Score: 5.5/10**

**Rationale:** The paper presents a technically sound adaptation of Variational Flow Matching to vector-quantized image generation, with a clear motivation and a mathematically coherent formulation. The convergence speed advantage over CFM and DFM baselines is the most compelling empirical finding. However, the score is constrained by the following factors prioritized per the scoring policy (research value + novelty first):

1. **Incremental novelty (primary limiting factor):** The core idea — using a categorical variational posterior within VFM — is a direct application of existing VFM/CatFlow methodology to the VQ image domain. The paper acknowledges similarity to CDCD (Dieleman et al., 2022) in the Related Work but does not clearly differentiate beyond domain shift. The technical contribution is more of an adaptation than a conceptual advance.

2. **Overclaiming reduces credibility:** The "state-of-the-art among VQ models" claim is contradicted by the paper's own Table 1 (Open-MAGVIT2-L FID 2.51 vs. 3.88). The convergence speed claims lack statistical validation. These issues lower trust in the paper's self-assessment.

3. **Evidence sufficiency:** The method is evaluated only on ImageNet-1k at a single resolution, with no multi-seed variance reported. The explanations for underperformance against continuous diffusion models are speculative rather than experimentally validated.

4. **Positive aspects:** The hybrid discrete-continuous formulation is well-motivated, the temperature control property is practically useful and clearly demonstrated, and the convergence speed advantage (if statistically validated) would have practical value for reducing training cost. The paper is generally well-written and the code release supports reproducibility.

A revision addressing the major weaknesses (claim bounding, statistical rigor, error correction in Eq. 11, and clearer differentiation from CDCD) could raise this score to the 6.5-7.0 range.