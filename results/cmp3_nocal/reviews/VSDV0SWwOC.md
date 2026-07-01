## Summary

LS-Merge proposes encoding LLM weights into a learned latent space via a Transformer-VAE, performing merging (interpolation) in that space, and decoding back to weights. The method aims to enable cross-architecture merging (models with different widths/depths/families) and single-model "self-merging." The core idea—shifting merging from weight space to a learned latent space—is conceptually interesting and tackles a real limitation of prior work.

## Strengths

- **Novel and well-motivated core idea.** The paper correctly identifies that weight-space merging requires homogeneous architectures, and encoding weights into a fixed-dimensional latent representation is a principled way to relax this constraint (Section 1, lines 27–29). Cross-architecture merging is the right problem to target.

- **Weight statistics analysis (Section 3.1, Table 1) is a concrete empirical contribution.** Documenting the heavy-tailed, high-kurtosis nature of LLM weights (e.g., kurtosis > 5 and up to ~15 in self-attention layers) and showing that this contradicts Gaussian assumptions used in prior work is informative and can inform future weight-space modeling efforts.

- **PCA vs. VAE comparison (Section 5.3, Table 8) convincingly demonstrates that linear projections fail.** PCA-reconstructed models regress to near-random accuracy (MMLU ~25.5%) even at mild compression (r=1.6), while the VAE preserves ~96% of base performance—a clean empirical justification for non-linear encoding.

- **Using Optimal Transport for latent distribution alignment (Section 3.3)** is a principled response to the geometric mismatch between heterogeneous models, and the closed-form Gaussian OT solution keeps it tractable. Figure 3 provides visual evidence that OT alignment brings source and target latents into shared support.

## Weaknesses

### Fatal
None.

### Major

- **Inconsistent evaluation frameworks prevent cross-experiment comparison.** The same base model (Gemma-3-1B-it) reports MMLU scores of **32.20** (Table 2), **40.76** (Tables 6 and 7), and **41.44** (Table 8)—a ~25% range. While the paper acknowledges switching between the "subset dataset used by Feng et al. (2024b)" (line 151) and `lm-eval` (lines 191, 234), it never reconciles these numbers. A reader cannot determine whether claimed improvements reflect genuine gains or different evaluation conditions. For example, the "self-merging" gain in Table 2 (32.20 → 35.13, Feng subset) uses a different evaluation framework than the cross-architecture results in Table 5 (baseline 40.76, `lm-eval`). The paper should normalize all experiments to a single consistent framework or explicitly document which framework each table uses and provide a conversion analysis.

- **The cross-architecture merging results (Table 5) show marginal gains without error bars, and the OT-only baseline degrades sharply.** The "OT + interp." strategy yields improvements of +0.92 (WinoGrande), +0.56 (ARC-C), and +1.03 (HellaSwag)—all <1.5 points—with no variance estimates reported. Meanwhile, the "OT only" row drops ARC-C from 42.78 to 34.25, indicating that the alignment itself is harmful and the recovery via interpolation is fragile. Given the overhead of training a VAE, encoding/decoding weights, and computing OT alignment, these marginal gains do not yet make a compelling case for the method's practical value in cross-architecture settings.

- **The LoRA expert merging comparison (Table 3) gives LS-Merge an unfair methodological advantage.** The paper states that LS-Merge "sampl[es] multiple latent codes for each expert before merging" (Section 4.2, line 187), while all weight-space baselines use single-point estimates. This conflates the benefit of latent representations with the benefit of ensembling over multiple stochastic samples. A controlled comparison where both methods use the same number of samples is needed before claiming that "latent-space fusion consistently outperforms all weight-space baselines" (line 187).

### Minor

- **"Self-merging" (Section 4.1) is posterior averaging / ensembling, not model merging as standardly understood.** The procedure—encoding a single model, sampling multiple latents from its posterior, averaging them, and decoding—is a form of Bayesian variance reduction, not the combination of information from distinct checkpoints. The gains in Table 2 (e.g., Gemma-3-1B-it: 32.20 → 35.13) may be attributable to variance reduction from averaging, which is a different phenomenon from merging. The paper frames this as "enabling single-model augmentation" (abstract, line 29), but it should explicitly discuss whether the improvement is an ensemble effect.

- **The VAE reconstruction sometimes outperforms the uncompressed base model (Table 2).** Gemma-3-4B-it's VAE reconstruction yields MMLU 54.10 vs. base 53.10, and GSM8k 31.27 vs. 29.90. A lossy autoencoder with compression ratio 2 improving over the original, uncompressed model warrants explanation. Possible causes include (a) the VAE acting as a denoiser on heavy-tailed weights, (b) training on both models' weights providing beneficial information, or (c) different evaluation conditions for the base vs. VAE rows (the base row reports no variance). The paper does not discuss this.

- **VAE reconstruction loss at r=2 is substantial under `lm-eval` (Table 7), and the self-merging gains may partially reflect compression recovery.** Under `lm-eval`, VAE reconstruction at r=2 drops Gemma-3-1B-it MMLU from 40.76 to 32.22 (a ~21% loss). The self-merging experiment (Table 2) uses r=2, and while the base reference there is 32.20 (Feng subset, a different scale), the paper does not disentangle how much of the self-merging improvement is genuine enhancement vs. partial recovery of compression-induced degradation. An experiment at a near-lossless compression ratio would clarify this.

- **Figure 4 reports intra-family cross-architecture results only as bar charts without precise numerical values** (Section 4.4, line 226). The paper states "small injections from the source (λ ∈ [0.05, 0.20]) deliver the best improvements" but does not report the actual numbers. Given that these are the paper's main cross-architecture results, raw numbers should be reported.

### Trivial
None.

## Nice-to-Haves
- Report the computational cost (GPU-hours, data requirements) of VAE training and encoding/decoding. The paper claims scalability but provides no basis for this.
- Report error bars or statistical significance measures on the cross-architecture results (Table 5), where gains are small and no variance is reported.
- For the OT alignment, provide evidence that the VAE's latent space is approximately Gaussian (to justify the closed-form Gaussian OT solution). The paper's own finding of heavy-tailed weights doesn't automatically contradict this, but empirical verification would strengthen the method.

## Removed Points
These points were flagged by the harsh critic but are removed for the following reasons:
- **The OT Gaussian assumption contradicts the heavy-tailed finding:** The critic conflates the *weight* distribution (heavy-tailed) with the *latent* distribution, which is regularized toward a Gaussian via the VAE's KL term. The VAE is explicitly designed to produce approximately Gaussian latents. This criticism misunderstands the method.
- **Theoretical compressibility argument is merely existence-based:** The existence bound is standard motivation for this type of work. Demanding quantitative connection to the VAE design is beyond typical expectations for a motivation section.
- **Algorithm numbering mismatch (Algorithm 1 vs. Algorithm 2):** This is a minor formatting artifact likely resolved in the (stripped) appendix.
- **Various missing appendix contents, reproducibility nitpicks about hyperparameters, and formatting/style notes:** These are parser artifacts or issues standardly addressed by reference to the appendix.

## Novel Insights

The most useful insight from the reviews is that the paper's evaluation suffers from an unreconciled dual-framework problem. The same Gemma-3-1B-it base model is evaluated at MMLU values of 32.20 (Feng subset), 40.76 (lm-eval), and 41.44 (lm-eval), and these numbers cannot be directly compared. This means the self-merging experiment (Table 2, Feng subset) and the cross-architecture ablation (Table 5, lm-eval) exist in separate evaluation universes—a fact that the paper acknowledges procedurally but never addresses analytically. The VAE reconstruction at r=2 produces ~32.22–32.60 MMLU regardless of framework, but whether this represents minimal loss (vs. base 32.20 on Feng subset) or massive loss (vs. base 40.76 on lm-eval) depends entirely on which table you read. Until the paper adopts a single framework or provides explicit cross-walk numbers, its empirical claims cannot be coherently assessed.

## Suggestions

1. **Adopt a single evaluation framework across all experiments** and re-run all models under it. At minimum, provide a cross-walk table showing base model scores under both frameworks so the reader can mentally calibrate across experiments.
2. **Disentangle VAE reconstruction loss from merging gains** by running the self-merging experiment at a near-lossless compression ratio (e.g., r=1.0 or r=1.1) and showing that the merging improvement persists.
3. **Control for the multi-sample advantage in the LoRA comparison** by also reporting LS-Merge with a single latent sample per expert, ensuring an apples-to-apples comparison with weight-space baselines.
4. **Report the precise numerical values for Figure 4** (intra-family cross-architecture merging) rather than only bar charts.
5. **Report error bars for Table 5** (cross-architecture results), given that the gains are small and the base model MMLU itself shows variance across different evaluations.

## Score and Decision
MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>