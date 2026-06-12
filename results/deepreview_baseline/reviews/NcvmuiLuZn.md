## Summary

This paper introduces the Noise-to-Process (N2P) paradigm for stochastic process modeling from a single trajectory without strong priors. The key idea is to learn a parameterized generator that maps a shared base-noise process to an entire trajectory in one pass, making projective consistency intrinsic by design. The authors instantiate this paradigm with Deconvolution-Based Process Transformation (DBPT), which uses a noise encoder and deconvolution-based decoder to capture inter-temporal dependencies, and demonstrate competitive performance across synthetic, time series, image completion, and black-box optimization tasks.

## Strengths

- **Novel and principled framework**: The N2P paradigm offers a clean theoretical formulation where projective consistency follows naturally from the shared-noise + single-generator structure, avoiding the need for post-hoc consistency constraints. The formal connection to Kolmogorov extension is a nice theoretical touch.

- **Addresses an important gap**: The paper targets the underexplored regime of single-trajectory stochastic process learning with weak priors, which is practically relevant for expensive simulation settings (e.g., CFD) where only one noisy trajectory is available.

- **Competitive empirical results**: DBPT achieves strong performance across diverse tasks, particularly in image completion where it significantly outperforms baselines (e.g., PSNR 21.65 vs. 16.58 for CNP on MNIST), and in black-box optimization where it converges faster than all competitors.

## Weaknesses

### Major

- **Limited theoretical contribution beyond formalism**: While the N2P representation is cleanly defined, the theoretical results (Propositions 2-3) are essentially standard measure-theoretic facts about pushforward measures and coordinate projections. The claim that this is "novel" is overstated—any generative model that maps noise to outputs in one pass has this property. The paper would benefit from non-trivial theoretical guarantees (e.g., sample complexity, approximation bounds, or convergence results).

- **Insufficient comparison with relevant baselines**: The paper omits several important baselines that are directly relevant: (1) Neural ODEs/SDEs trained on single trajectories, (2) Deep GP variants that can handle single trajectories, (3) Variational autoencoders with temporal structure, and (4) Simple interpolation methods (e.g., splines with uncertainty). The absence of these comparisons makes it difficult to assess whether DBPT's gains come from the N2P paradigm or from the specific architectural choices.

- **Unclear how DBPT differs from standard deconvolutional generative models**: The DBPT architecture (noise encoder + deconvolution decoder) is essentially a standard deep generative model (like a conditional VAE or GAN) applied to trajectory generation. The paper does not clearly explain what makes this specifically a "process transformation" rather than just a neural network that maps noise to outputs. The claim that deconvolution "captures inter-temporal dependence" is true of any convolutional architecture and is not unique to this work.

- **Missing ablation studies on key design choices**: The paper only ablates grid resolution. Critical ablations are missing: (1) What happens if you replace the deconvolution decoder with a simple MLP or transformer? (2) How does the choice of base-noise distribution affect results? (3) What is the effect of the noise encoder vs. directly feeding noise to the decoder? Without these, it's unclear which components drive performance.

### Minor

- **The masked MSE training objective is simple but potentially limiting**: Training only on observed indices with MSE may not capture complex uncertainty structures. The paper claims the decoder "propagates observational constraints" but provides no analysis of when or why this propagation works.

- **NLL values in Table 1 are extremely large (e.g., 602-2130)**: These values suggest potential numerical issues or that the predictive distributions are poorly calibrated in absolute terms. The paper should discuss what these numbers mean in context.

- **The image completion results, while strong, may partly reflect DBPT's architectural advantage**: Deconvolutional networks are known to be effective for image tasks, so the comparison with GP-based methods (which are not designed for images) may be somewhat unfair.

### Trivial

- Figure 1 is difficult to interpret and the caption is repetitive.

## Nice-to-Haves

- A theoretical analysis of when the N2P representation can approximate arbitrary stochastic processes (universality) would significantly strengthen the paper.
- Experiments on irregularly-sampled time series would better demonstrate the framework's generality.
- A discussion of computational complexity and training time compared to baselines would be helpful for practitioners.

## Novel Insights

None beyond the paper's own contributions. The core insight—that a shared noise source passed through a single generator yields projective consistency—is a useful reframing of existing ideas in generative modeling, but it does not constitute a fundamentally new theoretical discovery. The paper's main value is in identifying the single-trajectory weak-prior regime as an important problem and demonstrating that a carefully designed deconvolutional architecture can work well in this setting.

## Suggestions

1. Add comparisons with Neural ODEs, Deep GPs, and simple interpolation baselines to better contextualize DBPT's performance.
2. Include ablation studies that vary the decoder architecture (e.g., MLP, transformer) to isolate the contribution of deconvolution.
3. Provide theoretical analysis of approximation capabilities or sample complexity for the N2P framework.
4. Discuss the practical implications of the large NLL values in the time series experiments.

## Score and Decision

The paper presents a clean formulation and demonstrates promising empirical results on an important problem. However, the theoretical contribution is modest (standard measure-theoretic facts), the architectural contribution is incremental (deconvolutional generative model), and the experimental evaluation omits several relevant baselines. The work is solid but does not rise to the level of a top-venue acceptance in its current form.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>