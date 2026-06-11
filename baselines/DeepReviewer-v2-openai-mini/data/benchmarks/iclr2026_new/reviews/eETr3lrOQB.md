## Summary
This paper proposes **VQ-Transplant**, a framework that enables plug-and-play replacement of vector quantization (VQ) modules within pre-trained visual tokenizers without costly end-to-end retraining. The framework operates in two stages: (1) VQ module substitution, where the native VQ module of a frozen pre-trained tokenizer (specifically VAR) is replaced with a new VQ module trained via a codebook alignment loss, and (2) lightweight decoder adaptation (5-20 epochs on ImageNet-1k) to realign the decoder's priors with the new quantized latent space. The paper also introduces **MMD-VQ**, a quantization method using Maximum Mean Discrepancy (MMD) for distribution alignment between feature and codebook vectors, designed for compatibility with the framework.

The key empirical claims are: VQ-Transplant with MMD-VAR achieves 0.81 r-FID (vs 0.92 for baseline VAR) while requiring only 44 GPU-hours (vs 960 GPU-hours for full VAR training), representing a ~21.8× speedup. The framework shows consistent improvements across multi-scale and fixed-scale VQ variants, and demonstrates generalization to out-of-domain datasets (FFHQ, CelebA-HQ, LSUN-Churches).

**Novelty note:** External literature verification was unavailable in this run (Retrieval-Disabled Mode). Novelty and comparison conclusions are explicitly deferred for manual verification. The following assessment is based solely on manuscript-internal evidence.

## Strengths
**1. Practical problem framing with high impact potential.** The paper addresses a genuine bottleneck in visual tokenization research: the prohibitive computational cost of training state-of-the-art VQ-based tokenizers from scratch. Decoupling VQ module development from full encoder-decoder training could accelerate iteration in quantization research. The proposed two-stage framework (substitution + lightweight adaptation) is straightforward and well-motivated.

**2. Comprehensive empirical evaluation.** The experiments cover five VQ methods (Vanilla, EMA, Online, Wasserstein, MMD) under both multi-scale and fixed-scale quantization configurations, across multiple codebook sizes (K=4096 to 65536), and on four datasets (ImageNet-1k, FFHQ, CelebA-HQ, LSUN-Churches). The ablation on adaptation epochs (5 to 20) and comparison against from-scratch training (Table 6) provide useful insights into the framework's behavior. The inclusion of both multi-scale (VAR-style) and fixed-scale VQ demonstrates generalizability across quantization paradigms.

**3. Clear identification of decoder-quantization mismatch.** A key analytical contribution is the explicit demonstration that lower quantization error does not automatically translate to better reconstruction after VQ module substitution (Table 3, Phase I vs Phase II). The paper convincingly shows that decoder adaptation is essential to bridge this gap, and that adversarial training in the adaptation phase effectively converts quantization error reduction into perceptual quality gains. This finding has practical value for future modular tokenizer design.

**4. Reproducibility-friendly details.** The paper commits to releasing code and models, specifies the discriminator architecture (frozen DINO-S), and documents practical training stabilizers (DiffAug, consistency regularization, LeCAM). The computational budget is reported transparently (Table 1), enabling readers to assess feasibility.

## Weaknesses
### W1. Non-apples-to-apples efficiency comparison (Major)

The paper's central efficiency claim — "reducing the training cost by 95%" (Abstract) and "21.8× faster training" (Table 1) — compares VQ-Transplant (2× A100, 22 hours, ImageNet-1k) against the VAR tokenizer (16× A100, 60 hours, OpenImages). These configurations differ in three confounded factors: (1) dataset size (ImageNet-1k ~1.3M images vs OpenImages ~9M images), (2) GPU count (2× vs 16×), and (3) training epochs/objective. The speedup factor mixes the benefit of training on a smaller dataset with the benefit of the framework itself. A fairer comparison would normalize by dataset size, GPU-hours, or convergence quality. The paper should report GPU-hours explicitly (44 GPU-hours vs 960 GPU-hours) and acknowledge the dataset discrepancy. [(Annotation: Abstract 95% cost claim, Page 1 - Abstract)]

### W2. Baseline comparisons are not fully controlled (Major)

The "Main Results" claim of outperforming competing baselines (Section 5, Table 2) is undermined by uncontrolled factors. VQ-Transplant methods use more tokens (512 or 680) and larger codebooks (K up to 65536) than most baselines (256 tokens, K=16384). Token count and codebook size directly affect reconstruction quality. The baselines were also trained from scratch with different protocols, while VQ-Transplant leverages a pre-trained backbone. These confounds make it impossible to attribute gains solely to the framework or MMD-VQ. The paper would benefit from controlled comparisons holding token count, codebook size, and backbone initialization constant. [(Annotation: Main results uncontrolled comparison, Page 1 - Experiment: Main Results)]

### W3. Speedup/savings metric is inconsistently defined (Major)

The Abstract claims "95% training cost reduction" but Table 1 reports "21.8× Speedup" for VAR. A 21.8× speedup corresponds to ~95.4% reduction, so the numbers are arithmetically consistent. However, the Speedup column for VQ-Transplant is intentionally left blank ("-"), and the speedup is computed as a ratio of raw training hours without normalizing by GPU count or dataset size. This selective reporting could mislead readers about the true computational savings. The paper should use a consistent, well-defined efficiency metric (e.g., GPU-hours, normalized by training samples seen).

### W4. Internal contradiction on adversarial training stability (Major)

The Introduction motivates the framework by stating that adversarial training is "inherently unstable" (Page 1 - Introduction), yet the decoder adaptation stage (Stage II) uses adversarial training (GAN loss through a DINO-S discriminator). If adversarial training is inherently unstable, the proposed method inherits that instability. The paper does not discuss why adversarial training is acceptable in Stage II but not in full training. The authors should either (a) provide empirical evidence that decoder adaptation is more stable (e.g., training loss curves, gradient norms), or (b) revise the motivational framing to focus on computational cost rather than instability. [(Annotation: Adversarial training instability, Page 1 - Introduction paragraph 2)]

### W5. Cross-dataset "SOTA" claims lack controlled baselines (Major)

Section 5.3 claims "state-of-the-art reconstruction performance" on FFHQ, CelebA-HQ, and LSUN-Churches. However, the baselines cited from Zhu et al. (2024) were trained from scratch on each dataset, while VQ-Transplant benefits from the pre-trained VAR backbone (trained on OpenImages). The comparison conflates framework advantage with transfer learning from pretraining. The "record r-FID of 1.21" on FFHQ (Table 8) uses 512 tokens and K=32768, while the closest baseline VQGAN-LC uses 256 tokens and K=100000. A controlled comparison (matching tokens, pre-training condition, or comparing fine-tuned backbones) is needed before making SOTA claims. [(Annotation: Cross-dataset SOTA overclaim, Page 1 - Section 5.3)]

### W6. MMD-VQ contribution novelty needs clarification (Moderate)

MMD is a well-established kernel-based divergence measure widely used in domain adaptation and generative modeling. The paper's novelty claim for MMD-VQ rests on applying MMD to codebook learning in VQ. However, the paper does not clearly state whether MMD has been previously applied to codebook or codebook learning in the signal processing or neural compression literature. The Related Work section criticizes Wasserstein VQ's Gaussian assumption but does not survey kernel-based or non-parametric approaches to VQ. Without this context, readers cannot assess the incremental contribution of MMD-VQ. The paper should explicitly clarify the novelty boundary and, if MMD for codebook learning is novel, state this directly. [(Annotation: MMD-VQ novelty differentiation, Page 1 - Introduction; Page 1 - Related Work)]

### W7. Reproducibility gaps in experimental reporting (Moderate)

The Experiment Setup paragraph does not report critical hyperparameters for reproducibility: learning rates, optimizers, batch sizes, number of training epochs for Stage I, loss weight coefficients ($\gamma$, $\lambda_P$, $\lambda_G$), data augmentation used, and whether the full ImageNet-1k training set or a subset was used for decoder adaptation. These details are essential for other researchers to apply VQ-Transplant to their own models. The paper should add a hyperparameter table (potentially in Appendix A) covering both stages. [(Annotation: Missing hyperparameters, Page 1 - Experiment Setup)]

### W8. Conclusion lacks synthesis and limitation disclosure (Minor)

The Conclusion (2 sentences) restates the contributions without quantitative summary, limitation disclosure, or future work directions. It misses an opportunity to bound the framework's scope (e.g., reduced compatibility with continuous tokenizers like LDM-16, dependency on a suitable pre-trained backbone). A stronger conclusion would consolidate validated findings, acknowledge boundaries, and suggest concrete next steps. [(Annotation: Conclusion too brief, Page 1 - Conclusion)]

### W9. Redundancy across multi-scale and fixed-scale sections (Minor)

Section 5.1 and Section 5.2 present nearly identical narrative structures and conclusions for multi-scale and fixed-scale VQ. While consistency is valuable, the redundancy could be reduced by presenting one detailed analysis and a shorter confirmation paragraph for the other. [(Annotation: Fixed-scale redundancy, Page 1 - Section 5.2)]

### W10. Missing confidence intervals and significance tests (Moderate)

All reported metrics (r-FID, PSNR, SSIM, LPIPS, r-IS) are presented as point estimates without variance, confidence intervals, or significance tests. For metrics like r-FID (where differences of 0.01-0.05 can change rankings), the statistical reliability of comparisons is unclear. The paper should report results over multiple seeds (at least 3) with standard deviations, or explain why variance is negligible for the reported settings.

## Score
**Final Score: 6.5/10**

The paper addresses a practically important problem (efficient VQ module development) with a well-motivated framework (VQ-Transplant) and comprehensive experiments. The two-stage approach is conceptually clean, and the empirical demonstration of decoder-quantization mismatch is a useful analytical contribution. The efficiency gains (44 GPU-hours vs 960 GPU-hours for comparable reconstruction quality) are promising.

However, several major weaknesses reduce confidence in the current claims: (1) the central efficiency comparison is not apples-to-apples (different datasets, GPU counts, and training protocols), (2) baseline comparisons in Table 2 mix uncontrolled factors (token count, codebook size, backbone pretraining), (3) the SOTA claims on cross-dataset generalization lack controlled baselines, (4) the internal contradiction regarding adversarial training instability is unresolved, and (5) MMD-VQ's novelty over existing kernel methods needs clarification (deferred due to Retrieval-Disabled Mode). The paper would benefit from controlled comparisons, explicit GPU-hours reporting, and a more nuanced positioning of its claims.

The framework's core idea — modular VQ replacement with lightweight decoder adaptation — has genuine practical value and could become a useful tool for the community if the claims are tightened and the evaluation is made more rigorous.