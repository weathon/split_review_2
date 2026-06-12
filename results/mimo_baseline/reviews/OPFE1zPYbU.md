## Summary

This paper argues that diffusion models do not learn the statistical quantities (posterior, score, velocity field) they are theoretically assumed to learn. The authors claim that in high-dimensional sparse settings, the posterior mean "degrades" from a weighted sum of samples to essentially a single nearest sample, preventing effective learning of these quantities. They propose a "Natural Inference" framework that unifies most existing sampling methods (DDPM, DDIM, Euler, DPM-Solver, DPM-Solver++, DEIS) by expressing all inference as autoregressive x₀ prediction with signal and noise coefficient matrices, offering a statistics-free perspective on diffusion model operation.

## Strengths

- **Empirical measurement of posterior concentration**: Tables 1 and 2 provide concrete measurements of how concentrated the posterior p(x₀|x_t) becomes on ImageNet-256 and ImageNet-512, showing that for low-to-moderate t values (especially with Flow Matching), the posterior overwhelmingly peaks at a single training sample. This is a useful empirical observation about high-dimensional behavior.

- **Unified inference framework**: The Natural Inference framework provides a clean algebraic structure for expressing diverse sampling methods. Showing that DDPM, DDIM, Euler, DPM-Solver, DPM-Solver++, DEIS, and Flow Matching solvers can all be cast as linear combinations of predicted x₀ values and noise terms with specific coefficient matrices is a useful organizational contribution. The connection between self-guidance operations and classifier-free guidance is an interesting observation.

- **Frequency-domain interpretation of training**: Section 3.3's frequency-domain perspective—viewing the objective as learning to predict submerged (higher-frequency) components based on SNR at each noise level—provides an intuitive and practically resonant understanding of what diffusion models learn at different timesteps, consistent with the well-known coarse-to-fine generation pattern.

## Weaknesses

### Fatal

None.

### Major

- **The manifold hypothesis is entirely ignored, undermining the core claim.** The entire argument about "curse of dimensionality" and sparsity treats the data as living in the full ambient space (4096 or 16480 latent dimensions). However, it is well-established that natural images and other structured data lie on much lower-dimensional manifolds. The diffusion model operates on this manifold, not the ambient space. The paper's claim that high dimensionality prevents learning statistical quantities is therefore built on a fundamentally incomplete analysis. Without addressing this, the central thesis remains unsubstantiated.

- **Overclaiming what degradation implies.** The paper shows that p(x₀|x_t) concentrates on a single sample but then jumps to claiming this means the model "cannot effectively learn" posterior, score, or velocity field. This is a non sequitur. Even when the posterior is concentrated, it has a well-defined mean, score, and velocity field—they are just concentrated in particular ways. Furthermore, the objective function ∫∫ p(x₀,x_t) ‖f_θ(x_t) - x₀‖² dx₀dx_t still has the correct expected value regardless of posterior shape. The paper needs to demonstrate that concentration actually impairs learned quantities, not merely assert it.

- **No experimental validation of the alternative mechanism.** The paper claims diffusion models operate via "a different mechanism" (information enhancement/filtering) but provides no experiments comparing this interpretation against the standard one. No ablation, no prediction of novel phenomena from the new framework, no demonstration that the Natural Inference framework leads to better sampling algorithms. The contribution remains purely interpretive without empirical consequences.

- **The "Natural Inference" framework's novelty and non-triviality are unclear.** Any iterative method that predicts x₀ via linear updates can be unfolded into a linear combination of predicted x₀ values and noise terms—this is algebraic bookkeeping, not a deep structural insight. The paper does not demonstrate that this framework leads to any new sampling methods, theoretical insights, or practical improvements beyond reorganizing existing knowledge.

### Minor

- **The 0.9 threshold for degradation is arbitrary and unanalyzed.** The paper defines degradation as p(x₀=x₀'|x_t) > 0.9 but provides no sensitivity analysis for this threshold. Different thresholds would yield different degradation statistics. Without robustness analysis, the quantitative claims in Tables 1-2 are less compelling than they appear.

- **Only degradation rates are measured, not downstream impact.** The paper shows degradation occurs but never measures whether it actually impairs model quality, score estimation accuracy, or sample generation. This missing link weakens the argument considerably.

- **The claim of "first rigorous analysis" is overstated.** The posterior concentration phenomenon in high-dimensional spaces with Gaussian likelihood is well-known and discussed in Karras et al. (2022) (which the paper itself cites). The analysis, while more detailed, is not fundamentally novel.

### Trivial

- The frequency-domain discussion (Section 3.3) conflates two different things: the model learning to predict submerged frequencies versus the objective function naturally causing this behavior. These are the same thing viewed from different angles, not separate insights.

## Nice-to-Haves

- A direct experiment measuring score/velocity estimation quality as a function of dimensionality to test whether degradation actually impairs learning.
- Application of the Natural Inference framework to design a novel sampler that outperforms existing methods.
- Analysis of how the manifold dimensionality (as opposed to ambient dimensionality) affects the degradation phenomenon.
- Comparison with empirical studies of diffusion model features at different noise levels (e.g., Park et al. 2023, Balaji et al. 2022) to test the frequency-filtering interpretation.

## Novel Insights

The observation that the diffusion model's objective can be viewed as a frequency-domain filtering operation—where at each noise level, the model learns to predict the submerged frequency components, effectively functioning as a progressive information enhancement operator—is a genuinely appealing perspective that aligns well with practical observations about coarse-to-fine generation. The connection drawn between classifier-free guidance and image sharpening operations (unsharp masking) via the "Self Guidance" concept also provides a useful conceptual bridge between classical image processing and modern generative modeling. However, whether these insights amount to a fundamentally new understanding or merely a repackaging of existing intuitions remains debatable.

## Suggestions

- Address the manifold hypothesis directly: analyze degradation as a function of intrinsic dimensionality rather than ambient dimensionality, or provide evidence that the manifold is high-dimensional.
- Provide an experiment where the Natural Inference framework enables a new sampling strategy that demonstrably improves upon existing methods.
- Add robustness analysis for the 0.9 degradation threshold and report how the statistics change across a range of thresholds.
- Connect the paper's claims to the broader empirical evidence: if diffusion models truly cannot learn scores, explain the success of score-based methods in practice.

## Score and Decision

The paper raises an interesting question about how diffusion models operate in high-dimensional spaces, and the empirical measurement of posterior concentration is valuable. However, the central claim that this concentration prevents learning of statistical quantities is overstated and not properly substantiated—particularly because the manifold hypothesis is unaddressed. The Natural Inference framework, while cleanly presented, amounts to algebraic reformulation without demonstrated practical or theoretical payoff. The paper identifies a real phenomenon (posterior concentration) but draws overly strong conclusions from it and fails to validate the alternative interpretation it proposes.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject