## Summary
This paper introduces Count Bridges, a stochastic bridge process on the integers using Poisson birth-death dynamics, providing closed-form conditionals for exact sampling and an EM-based framework for deconvolving aggregated count data into unit-level profiles. The method respects the ordinal and integer nature of counts, is connected to entropy-regularized optimal transport, and is demonstrated on synthetic benchmarks and two large-scale biological applications: nucleotide-resolution single-cell RNA-seq modeling / bulk deconvolution and spatial transcriptomic spot deconvolution.

## Strengths
- **Novel and principled framework**: Count Bridges provide a clean, analytically tractable bridge process for integer-valued data using Poisson birth-death dynamics, with closed-form conditionals (Bessel slack distribution, binomial/hypergeometric sampling) that enable efficient training and exact reverse sampling. This fills a clear gap, as existing discrete diffusion models focus on categorical data and the only previous count-specific work (Blackout Diffusion) uses a restrictive pure-death process.
- **Theoretical grounding**: The paper establishes connections to Schrödinger bridges and entropy-regularized optimal transport, showing that the birth-death bridge parameter $\kappa$ plays an analogous role to the noise scale in Gaussian diffusion. The distributional scoring loss is properly justified for discrete spaces, avoiding the pitfalls of cross-entropy.
- **Practical deconvolution pipeline**: The EM-style approach with projection-guided sampling is a natural extension to handle aggregated observations, and the authors demonstrate it on two challenging real-world biological tasks (bulk RNA-seq deconvolution and spatial transcriptomic deconvolution) with credible improvements over existing methods.
- **Strong empirical results on synthetic benchmarks**: Count Bridges significantly outperform both continuous flow matching (CFM) and discrete flow matching (DFM) on integer transport tasks, especially in higher dimensions, and the scaling experiment (Fig. 3) is convincing.

## Weaknesses
### Fatal
None.

### Major
- **Missing baseline comparison to Blackout Diffusion**: The paper identifies Blackout Diffusion as the only existing count-specific generative model and notes its limitations, but does not include it in any experimental comparison. Without this comparison, the claim of “state-of-the-art” on integer distribution matching is incompletely supported.
- **Ad-hoc projection step with limited theoretical justification**: The projection operator used in the EM-style deconvolution (Prop. 4.1) is acknowledged as a first-order surrogate, and the paper states it “lacks serious theoretical support.” This weakens the deconvolution contributions, especially for real-world applications where the approximation may be poor.
- **Baseline choices in biological applications**: For single-cell sequence-to-expression modeling, the baseline is a fine-tuned Enformer, which is not a generative model (it predicts a continuous mean) — this comparison does not directly assess generative quality. For spatial deconvolution, the paper uses a synthetic aggregation of MERFISH data; while reasonable for a proof-of-concept, real spatial transcriptomics validation would be more convincing.

### Minor
- **Ablation on loss function**: The paper argues that cross-entropy has limitations for count data and uses an energy score instead, but no ablation comparing these losses is presented in the main text (it is mentioned only in an appendix that is removed).
- **High technical density**: The paper packs a great deal of theory and multiple experiments into a dense presentation; some readers may find the flow of ideas difficult to follow, especially the derivation of the bridge and the deconvolution algorithms.

### Trivial
None.

## Nice-to-Haves
- An empirical comparison to Blackout Diffusion on the synthetic benchmarks.
- An ablation study contrasting cross-entropy vs. energy score for Count Bridges.
- A real spatial transcriptomics dataset (e.g., Visium data with paired single-cell references) for deconvolution validation.
- Theoretical analysis of when the first-order projection is accurate (e.g., large-sample or high-signal regimes).

## Novel Insights
Beyond the paper’s own contributions, the most novel insight is that a birth-death process on the integers can be cast as a Schrödinger bridge problem, with the jump intensity $\kappa$ controlling the strength of entropy regularization and recovering discrete optimal transport with an $\ell_1$-like cost in the limit $\kappa \to 0$. This perspective unifies integer-valued generative modeling with the rich theory of optimal transport and bridges, and suggests that similar constructions could be derived for other discrete state spaces.

## Suggestions
- Add Blackout Diffusion as a baseline in the synthetic distribution experiments (at least for lower-dimensional tasks where it is tractable) to substantiate the claim of state-of-the-art.
- Include a small ablation comparing cross-entropy loss to the energy score on one of the synthetic tasks, to empirically justify the choice of scoring rule.
- For the deconvolution experiments, consider evaluating on a real spatial transcriptomics dataset where paired single-cell profiles are available (e.g., a Visium dataset with a matching scRNA-seq reference) to strengthen external validity.
- Clarify in the main text how the learned projection module in the single-cell application (Sec. 6.2) differs from the default first-order projection, and report its added value.

## Score and Decision
MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: Accept