## Summary

This paper introduces Count Bridges, a stochastic bridge process on the integers built from independent Poisson birth-death dynamics. The process yields closed-form conditionals that satisfy the bridge consistency and projective posterior properties, enabling efficient training and sampling analogously to continuous diffusion models. The authors extend this framework to deconvolution from aggregated observations via an EM-style procedure that treats unit-level counts as latent variables. They demonstrate state-of-the-art performance on synthetic integer distribution benchmarks and on two large-scale biological applications: nucleotide-resolution single-cell RNA-seq modeling for deconvolution of bulk RNA-seq, and reference-free deconvolution of spatial transcriptomic spots into single-cell count profiles.

## Strengths

* **Novel and principled framework.** Count Bridges are a natural extension of diffusion/flow matching to integer-valued data using a Poisson birth-death process. The theoretical development—including closed-form bridge kernels, the Bessel slack formulation, and the connection to Schrödinger bridges/entropy-regularized optimal transport—is mathematically sound and provides a firm foundation for generative modeling of counts.
* **Addresses an important, under-explored problem.** While discrete diffusion models for categorical data have flourished, the ordinal integer-valued case has received little attention. Blackout Diffusion (pure-death) is the only prior count-specific generative model, and it cannot transport between arbitrary distributions. Count Bridges fill this gap with a general, tractable approach.
* **Practical biological applications with strong results.** The paper demonstrates two realistic, large-scale applications: (1) nucleotide-resolution single-cell expression modeling outperforming a fine-tuned Enformer baseline, and (2) reference-free spatial transcriptomic deconvolution outperforming STDeconvolve. The deconvolution results are validated on held-out ground truth and show meaningful gains on distributional metrics.
* **Extensibility to deconvolution from aggregates.** The EM-style training procedure for aggregate observations is a novel and useful extension, enabling the model to be trained directly on aggregated data (e.g., bulk RNA-seq or spatial spots) while learning unit-level count distributions. The projection-guided sampling provides a practical approximation.
* **Rigorous evaluation.** The paper uses proper scoring rules (energy score) for training and evaluates with multiple distributional metrics (Wasserstein, MMD, Energy). Comparisons against both continuous and discrete flow matching baselines on synthetic tasks, and against domain-specific deconvolution methods, are appropriate and thorough.

## Weaknesses

### Fatal
None.

### Major
1. **Weak theoretical support for the deconvolution projection step.** The projection operator (Proposition 4.1) is justified only as a “first-order approximation” to the true aggregate-conditional distribution, and the authors explicitly state that the projection step “lacks serious theoretical support.” Since deconvolution is a core contribution of the paper, this is a significant gap. The practical effectiveness of the method is demonstrated, but the theoretical grounding is thin.

2. **Biological validation is on simulated aggregates, not real data.** The spatial transcriptomic deconvolution experiments use MERFISH data that is artificially aggregated to simulate Visium spots. While this enables ground-truth evaluation, it limits the strength of claims about real-world applicability. The paper would be substantially stronger if it included at least one experiment on real Visium data with some form of validation (e.g., comparison to histological annotations or independent spatial measurements).

3. **Unfair or insufficient baselines in some comparisons.**  
   * The comparison to fine-tuned Enformer (Table 1) is questionable: Enformer predicts a point estimate (mean expression), while Count Bridges predict a full conditional distribution. The MSE comparison likely favors a distributional model that can output the conditional mean; a more appropriate comparison would involve probabilistic metrics (e.g., negative log-likelihood) or a larger-scale ablation.  
   * On synthetic benchmarks, CB is compared to continuous flow matching (CFM) and discrete flow matching (DFM). While these are natural baselines, a discretized Gaussian diffusion (round continuous samples) would be a more direct competitor for integer data. The paper would benefit from such a baseline to isolate the advantage of the count-native bridge.

### Minor
1. **Exposition is dense and occasionally unclear.** The notation for bridges (e.g., \(K_{s|0,t}\), \(K_{s|t}\)) is introduced at a fast pace, and the crucial sampling algorithms (Algorithms 1 and 2) use variable names derived from the slack formulation that are difficult to follow without carefully studying the appendix. The paper would benefit from a more intuitive walkthrough of the generative process before diving into the algebra.

2. **No ablation studies.** The paper does not isolate the contributions of individual components: the energy score vs. a cross-entropy loss, the effect of the projection module vs. simple rescaling, or the impact of the number of EM iterations. Such ablations would clarify which design choices are most important.

3. **Claims of “state-of-the-art” are somewhat diluted by the novelty of the problem.** Count Bridges are compared against methods that are not designed for integer data (CFM, DFM) or against methods that solve a different task (Enformer predicts bulk, not single-cell). While the paper does outperform these baselines, the “state-of-the-art” claim would be stronger if the problem setup were more standard or if more directly related methods existed.

### Trivial
None.

## Nice-to-Haves
* An experiment on real Visium data (e.g., human breast cancer or mouse brain) with some form of external validation (e.g., matching to scRNA-seq reference or histological cell-type annotations).
* An ablation comparing the energy score loss to a standard cross-entropy loss for the count bridge, to empirically motivate the choice of scoring rule.
* A sensitivity analysis of the deconvolution performance versus the number of EM iterations.

## Novel Insights
The paper offers a genuinely novel connection between birth-death processes and generative modeling: by treating the marginals of a Poisson bridge as the training distribution and deriving closed-form conditionals via a Bessel-distributed slack variable, the authors create a fully tractable diffusion-style model on the integers. This framework further reveals that Count Bridges solve an entropy-regularized optimal transport problem on integers with cost \(|x_1 - x_0|\), analogous to how Gaussian bridges solve the quadratic-cost OT. The extension to deconvolution via an EM algorithm with projection-guided sampling is also novel, though less theoretically grounded. Beyond the paper’s own contributions, the insight that count data need not be rounded or categorized to be modeled generatively, and that the ordinal structure can be preserved through a birth-death mechanism, is valuable for any domain dealing with discrete integer measurements.

## Suggestions
* Add a real spatial transcriptomics experiment (e.g., Visium data from 10x Genomics) with evaluation against histological annotations or a reference-based deconvolution method. This would significantly strengthen the deconvolution claims.
* Include an ablation comparing the energy score loss to the cross-entropy loss on a synthetic task to empirically justify the choice of training objective.
* Provide a more intuitive explanation of the sampling algorithms (Algorithms 1 and 2) in the main text, perhaps with a diagram or a simpler pseudo-code version, to improve readability.
* Consider adding a baseline of a discretized Gaussian diffusion (train continuous diffusion, round to integers at generation) on the synthetic benchmarks to better isolate the advantage of the count-native approach.

## Score and Decision

MY FINAL SCORE: <score>7</score>  
MY FINAL DECISION: <decision>Accept</decision>