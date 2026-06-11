## Summary
# Final Review Report

## Summary

This paper introduces Count Bridges, a stochastic bridge process on $\mathbb{Z}^d$ using Poisson birth-death dynamics, providing a discrete-native generative modeling framework for integer-valued count data. The method extends diffusion-style models to the integer lattice with closed-form conditionals, enabling exact sampling and training. A key secondary contribution is an EM-style deconvolution framework that trains from aggregated measurements by treating unit-level counts as latent variables. The paper demonstrates the approach on synthetic benchmarks (comparing against continuous and discrete flow matching) and two biological applications: nucleotide-resolution single-cell RNA-seq modeling for bulk RNA-seq deconvolution, and reference-free spatial transcriptomic deconvolution.

The paper is well-structured, mathematically rigorous, and addresses an important gap—generative modeling of ordinal count data with principled deconvolution. The birth-death bridge construction, the slack-variable parameterization, and the connection to entropy-regularized optimal transport are elegant and theoretically sound. The biological applications are ambitious and relevant.

However, the paper has several significant weaknesses: (1) the EM-style deconvolution E-step uses an amortized, projection-guided sampling loop that creates a circular dependency (the model generates its own training latents), and convergence guarantees are absent; (2) the "state-of-the-art" and "outperform" claims are not fully supported by the evidence, as key baselines (Blackout Diffusion, reference-based spatial deconvolution methods) are discussed in the related work but not quantitatively compared; (3) the comparison to Enformer in Table 1 is fundamentally mismatched in terms of task and input information; and (4) several critical implementation details (gradient estimation for the discrete energy score, number of Monte Carlo samples, cell-type assignment procedure) are missing.

Retrieval-Disabled Mode was active during this review; novelty and positioning conclusions are based solely on manuscript evidence and should be verified through external literature search in a revision cycle.

## Strengths
1. **Novel and principled discrete bridge construction**: The Poisson birth-death bridge on $\mathbb{Z}^d$ with closed-form conditionals (Proposition 3.1) is an elegant and original contribution. The slack-variable parameterization using the Bessel distribution is mathematically sound and enables efficient training and sampling via Algorithms 1-2. The connection to entropy-regularized optimal transport (static Schrödinger bridge) provides useful theoretical grounding.

2. **Unified framework for generation and deconvolution**: The paper ambitiously unifies two typically separate problems—generative modeling of integer-valued distributions and deconvolution from aggregated observations—within a single framework. The EM-style extension in Section 4, while imperfect, represents a genuine attempt to tackle a practically important and methodologically challenging problem.

3. **Strong synthetic scaling results**: The high-dimensional scaling experiment (Fig. 3) shows that Count Bridges maintain near-zero W1 error as dimension increases to 512, while CFM and DFM degrade substantially. This is a compelling demonstration of the bridge's ability to leverage the intrinsic low-rank structure. The effect persists across different NFE budgets, suggesting robustness to discretization.

4. **Ambitious and relevant biological applications**: The application to nucleotide-resolution scRNA-seq modeling and spatial transcriptomic deconvolution addresses genuine needs in computational biology. The use of side information (cell-type embeddings, genomic context, nuclear images) within the bridge framework is practically motivated.

5. **Honest limitations section**: The paper candidly acknowledges three key limitations: the continuous-data regime where Euclidean models may be preferable, the identifiability problem in pure deconvolution, and the lack of theoretical support for the projection step. This transparency is commendable and helps manage reader expectations.

6. **Algorithmic clarity**: The paper provides clear pseudocode for training (Algorithm 1), sampling (Algorithm 2), guided sampling for deconvolution (Algorithm 3), and the EM training loop (Algorithm 4), which supports reproducibility.

## Weaknesses
### W1. Circular dependency in the EM-style deconvolution E-step [Critical]

**Location**: Page 1 - Section 4 (Deconvolution with Count Bridges), Algorithms 3-4

The proposed EM-style approach for training from aggregates has a fundamental methodological issue. The E-step (Algorithm 3) generates latent unit-level samples $\mathbf{x}_0^\infty$ using the model itself through projection-guided diffusion sampling, and these latents are then used in the M-step to train the same model (Algorithm 4). This creates a circular self-training loop: the model generates its own training targets. Without a separate initialization phase, a warm-start from unit-level data, or an explicit regularization mechanism, this procedure risks converging to degenerate solutions that reproduce the aggregate statistics without learning meaningful unit-level structure.

The paper acknowledges this partially in the Limitations ("the projection step we use is a first-order surrogate and lacks serious theoretical support") but this is a critical concern that affects the validity of the deconvolution results in Tables 2-5. Standard EM theory guarantees convergence to a (local) maximum of the observed-data likelihood only when the E-step computes the exact posterior expectation. Algorithm 3 uses an amortized approximation whose bias is uncharacterized.

**Required action**:
1. Add a controlled synthetic experiment comparing the amortized E-step against an oracle E-step (using ground-truth latents) to quantify the approximation error.
2. Provide convergence diagnostics showing that the EM objective increases over training iterations.
3. Discuss alternative approaches (variational EM, importance-weighted sampling) that could provide more principled E-step approximations.

---

### W2. Unsupported "state-of-the-art" and missing baselines [Major]

**Location**: Page 1 - Abstract; Section 5 (Related Work); Section 6.1 (Synthetic Distributions)

The abstract claims "state-of-the-art performance on integer distribution matching benchmarks," but the synthetic experiments compare Count Bridges against only two baselines: continuous flow matching (CFM) and discrete flow matching (DFM). Critically, the paper does not compare against:
- **Blackout Diffusion** (Santos et al., 2023): Described in Section 5 as "the only existing work that also deals with such a process" for count/ordinal data. The paper positions Count Bridges as generalizing Blackout Diffusion but provides no quantitative comparison.
- **CTMC-based discrete diffusion models** (Austin et al., 2021; Campbell et al., 2022; Lou et al., 2023): While designed for categorical data, these could be adapted to ordinal settings and serve as baselines.
- **Distributional diffusion models** (De Bortoli et al., 2025; Shen et al., 2025): The distributional loss is inspired by these works, but no comparison is provided.

Without this evidence, the term "state-of-the-art" is not empirically justified and should be replaced with bounded comparative language.

**Required action**: At minimum, add a comparison to Blackout Diffusion on the synthetic tasks. If adaptation is required, describe the procedure explicitly.

---

### W3. Task-mismatched comparison between Count Bridge and Enformer [Major]

**Location**: Page 1 - Section 6.2, Table 1

Table 1 compares Count Bridge (CB) against "Fine-tuned Enformer" on Bulk MSE and CT MSE. This comparison is fundamentally mismatched:
- Enformer is a sequence-to-expression model that predicts expression *from DNA sequence alone* (input: genomic sequence).
- Count Bridge takes the noisy count $x_t$ and diffusion time $t$ as primary inputs, augmented with a genomic context embedding $z$ from Enformer and a cell-type embedding. The noisy count $x_t$ already contains information correlated with the true count $x_0$.

The methods address different tasks with different input information, so a direct MSE comparison is not informative. Additionally, CB Bulk MSE is reported as $0.601 \pm 0.000$ — zero variance over 3 training seeds is suspicious and may indicate numerical underflow in reporting precision.

**Required action**: 
1. Clarify the task distinction: CB uses count observations as input, Enformer does not.
2. Report std with meaningful precision (e.g., 3 decimal places for $\pm$ values).
3. Either add a setting where both methods receive comparable input information, or reframe the comparison as demonstrating CB's ability to denoise/deconvolve (which Enformer cannot do) rather than as a direct performance contest.

---

### W4. Missing implementation details for reproducibility [Major]

**Location**: Page 1 - Section 3.2 (Distributional Scoring Loss); Algorithms 1-4

Several critical implementation details are omitted:

1. **Gradient estimation for the energy score**: The loss $\mathcal{L}(\theta)$ in Section 3.2 requires differentiating through samples $\hat{x}^{(j)} \sim q_\theta(\cdot | x_t, t)$. For discrete distributions, reparameterization gradients are not available. The paper must specify whether it uses score-function (REINFORCE) gradients, continuous relaxations (Gumbel-Softmax), or another approach. This affects training stability and convergence.

2. **Number of Monte Carlo samples $m$**: The plug-in estimator $\hat{S}_\rho$ uses $m$ samples from $q_\theta$, but $m$ is never specified. The variance of the energy score estimator scales with $1/m$, affecting gradient noise.

3. **Diffusion steps $K$**: Algorithms 2-3 use a reverse grid $t_K > \dots > t_0$ but the number of steps $K$ and the choice of grid schedule (linear, quadratic, etc.) are not reported for experiments.

4. **Cell-type assignment procedure**: The comparison against CIBERSORTx/MuSiC aggregates nucleotide-level predictions into gene counts and assigns cells to the "closest cell type" without specifying the distance metric or threshold.

**Required action**: Provide all missing hyperparameters ($m$, $K$, schedule, gradient method, assignment metric) in the main text or appendix.

---

### W5. Synthetic data realism for spatial transcriptomics [Major]

**Location**: Page 1 - Section 6.3 (Spatial Transcriptomic Deconvolution)

The spatial transcriptomic experiment artifically aggregates MERFISH single-cell data to simulate Visium spots. The paper does not describe:
- How neighborhoods are defined (spatial proximity, random assignment, cell-type-aware?)
- The number of cells per simulated spot and its match to real Visium (10-50 cells)
- The degree of spatial correlation in the MERFISH data vs. real Visium spots

Real Visium spots have complex mixture compositions due to tissue architecture, which the synthetic aggregation may not capture. The strong results (Table 4-5) could partly reflect the synthetic construction rather than genuine deconvolution capability.

Additionally, reference-based methods (cell2location, RCTD, DestVI) are deferred to Appendix F, which is not available in the main manuscript. Since these represent the current standard for spatial deconvolution, their absence from the main comparison table weakens the "outperform" claim.

**Required action**:
1. Describe the aggregation procedure in detail.
2. Add a sensitivity analysis showing how results vary with aggregation parameters.
3. Include reference-based method comparisons in the main table or explicitly justify their exclusion.

---

### W6. Related work reads as a list rather than thematic comparison [Minor]

**Location**: Page 1 - Section 5 (Related Works)

The related work section surveys five areas sequentially but does not organize papers by conceptual axes (e.g., state space type, forward process, training loss, deconvolution capability). The discrete diffusion subsection lists many citations without clearly differentiating their approaches. A comparison table organized by decision-relevant axes would be more informative for positioning the contribution.

**Action**: Add a structured comparison (table or thematic paragraphs) showing where Count Bridges fits relative to existing approaches across dimensions such as: state space (categorical/ordinal/continuous), forward process (masking/uniform/birth-death), training loss (cross-entropy/score/energy), and deconvolution support.

---

### W7. Minor technical and writing issues [Minor]

**Location**: Throughout

- Algorithm 3 title has a typo: "Guided Sampling for for $\mathbf{x}_0^\infty$" (double "for").
- The integration domain in Eq. (1) is unspecified (measure-theoretic ambiguity between $\mathbb{R}^d$ integrals and $\mathbb{Z}^d$ sums).
- The claim that Count Bridges "solve" the Schrödinger bridge problem should be qualified as the *static* (coupling-level) problem under the Poisson reference, not the dynamic (process-level) problem.
- The scaling experiment's near-perfect W1 values (Fig. 3) are striking but not discussed in terms of potential limitations of the synthetic data (low-rank Gaussian mixtures may favor the birth-death bridge structure).

## Score
**Final Score: 6/10**

The paper presents a mathematically elegant and practically motivated contribution — a discrete-native generative bridge framework for count data with a deconvolution extension. The core methodological contribution (the Poisson birth-death bridge with closed-form conditionals) is novel and technically sound. The potential impact on computational biology is significant if the method proves robust in practice.

However, the score is constrained by the following critical issues:

- **The EM-style deconvolution loop (W1)** has a circular dependency that undermines confidence in the deconvolution results. This is the most significant weakness because the biological applications are the paper's primary demonstration of real-world value. Without evidence that the E-step approximation is faithful, the deconvolution claims rest on uncertain ground.

- **The empirical evidence does not fully support the stated claims (W2, W3)**. Missing baseline comparisons (especially Blackout Diffusion) and a task-mismatched comparison against Enformer weaken the empirical positioning. The term "state-of-the-art" is not justified by the presented evidence.

- **Reproducibility gaps (W4)** in the training procedure (gradient estimation, Monte Carlo sample size, diffusion step count) reduce the paper's immediate utility to practitioners.

On the positive side, the mathematical framework is rigorous, the scaling results on synthetic data are impressive, the biological applications are ambitious and relevant, and the paper is honestly written with explicit acknowledgment of key limitations.

**The paper has the potential to be a solid contribution (7-8/10 range) after major revisions addressing the circular E-step concern, adding missing baselines, clarifying comparisons, and filling reproducibility gaps.** The core idea is worth pursuing; the main issues are in the execution and evidence presentation.

**Novelty assessment note**: Retrieval-Disabled Mode was active during this review; novelty conclusions relative to Blackout Diffusion, other discrete diffusion models, and existing deconvolution methods should be verified through dedicated literature search in revision.