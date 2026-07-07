## Summary
DISCO (Diffusion-free SCORE matching) proposes learning a single, time-independent score function rather than the time-indexed family of score fields used in standard diffusion models. The core insight is that diffusion models' latent noise variables make exact conditional sampling intractable, whereas a single score field for the slightly perturbed data distribution makes conditioning trivially exact (clamping observed coordinates in Eq. 5). The authors derive the DISCO loss from a weighted mixture of q-weighted Fisher divergences, prove its consistency, and demonstrate competitive FID on CIFAR-10/FFHQ-64 while dramatically outperforming diffusion-based conditional sampling heuristics on inpainting tasks.

## Strengths
- **Principled theoretical framework**: The q-weighted Fisher divergence construction (Def. 1) and the DISCO loss (Theorem 1) are clean, the derivation is rigorous, and the proof that the global minimizer recovers the true perturbed data score is sound. The masked DISCO variant is also shown to share the same global minimum.
- **Correctly identifies and fixes an error in prior work**: The paper analytically shows that Li et al. (2023)'s MDSM does *not* learn the data score but a posterior-averaged diffusion score (Appendix A.2), which is a non-trivial and valuable correction to a published claim.
- **Strong empirical validation across scales**: The W1-distance evaluation on 2D distributions (Table 1) shows near-perfect conditional inference with DISCO vs. large errors for all diffusion heuristics. At image scale, DISCO achieves FID 2.65 on FFHQ-64 (close to EDM's 2.39) while outperforming all heuristic conditional samplers on most inpainting tasks (Table 2).
- **Competitive unconditional generation quality**: Achieving FID 3.58 on CIFAR-10 and 2.65 on FFHQ-64 with a *time-independent* single score field—using the same EDM backbone—is impressive and validates the claim that the diffusion hierarchy is not necessary for high-quality generation.

## Weaknesses

### Fatal
None.

### Major
- **Mini-batch approximation bias for large datasets**: The DISCO training requires sampling from the posterior p₀(x|x_t) over the training set. For large datasets (CIFAR-10, FFHQ), this is approximated via mini-batch sampling. The theoretical guarantees hold for the empirical distribution, but the mini-batch approximation introduces bias whose impact on the quality of the learned score—particularly at low noise levels where the posterior is concentrated—is not systematically analyzed. Given that the entire claim of learning the true data score rests on this step, quantifying this bias is important.
- **EDM Masked dominates DISCO on most inpainting metrics**: Despite DISCO's theoretical advantage, "EDM Masked" (a time-indexed diffusion model with masked training) outperforms DISCO on the majority of LPIPS/SSIM comparisons in Table 2. DISCO only clearly beats the heuristics applied to *unconditionally* trained models, raising the question of whether its advantage over EDM Masked is primarily principled or primarily due to the masked training objective (which EDM Masked also uses). This makes the headline claim about "outperforming standard heuristic samplers" somewhat qualified.

### Minor
- The practical accuracy of conditional sampling depends on the number of SMC particles. The claim of "asymptotically exact" sampling is theoretically valid, but there is no study of how particle count trades off against inference quality in the high-dimensional image setting. For a practitioner, this is non-trivial.
- The masked training introduces a hyperparameter γ and a mask distribution p(m). A sensitivity analysis of these choices is absent from the main text (it may be in the appendix).

### Trivial
None worth noting.

## Nice-to-Haves
- An ablation studying mini-batch size for the p₀(x|x_t) approximation against learned score quality would substantially strengthen the theoretical claims.
- Particle-count vs. conditional inference quality curves for at least one image task would make the "asymptotically exact" guarantee more practically actionable.

## Novel Insights
DISCO's central conceptual contribution is the reinterpretation of diffusion-level noise distributions p_t not as targets to be learned, but merely as proposal distributions in q-weighted Fisher divergences. This reframing is elegant and non-obvious: it preserves the beneficial coverage properties of diffusion training (learning scores outside the data manifold) while discarding the time-indexing that makes conditional inference intractable. The identification that existing "time-independent" approaches (MDSM, Sun et al.) learn unwanted weighted averages of diffusion scores—rather than the true data score—further sharpens what DISCO achieves uniquely. The masked training variant, which provably preserves the global optimum while improving learning of mixed clean/noisy configurations, is a practically important addition.

## Suggestions
- Add a mini-batch size ablation for p₀(x|x_t) to quantify how far the implementation deviates from the theoretical ideal.
- Include a direct comparison against EDM Masked in Table 1-style conditional quality metrics on image data (e.g., using held-out pixel values as ground truth), to clearly demonstrate whether DISCO's principled conditioning translates to image-scale gains over masked diffusion training.

## Score and Decision
The paper makes a genuine and clean theoretical contribution, identifies an error in prior work, and demonstrates that diffusion-free single-score training is both viable and practically advantageous for conditional inference. The FID gap on CIFAR-10 versus EDM and the partial dominance of EDM Masked on inpainting prevent a higher score, but neither undermines the core contribution. This is a solid borderline-accept paper.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>