## Summary

The paper introduces SCaSML, a framework that improves pre-trained PDE surrogate models (PINNs, GPs) at inference time without retraining by deriving a "Structural-preserving Law of Defect"—a new PDE governing the surrogate's error that retains the original semi-linear structure—and solving it via Multilevel Picard Monte Carlo simulation. The authors prove the final error is bounded by the product of surrogate and simulation errors, yielding an improved convergence rate, and demonstrate 20–80% error reduction on PDEs up to 160 dimensions across multiple surrogate types.

## Strengths

- **Novel and well-motivated framework.** The key insight—that the defect PDE for semi-linear parabolic equations preserves the semi-linear structure, enabling efficient Monte Carlo simulation—is elegant and non-obvious. This structural preservation (Fact 2.3) is what makes the approach tractable in high dimensions where classical grid-based defect correction fails, and the paper clearly explains why this property holds.

- **Sound theoretical contribution with practical implications.** Theorem 2.5 establishes that the final error scales as the product of the MLP simulation error and the surrogate error, and Corollary 2.6 derives the improved convergence rate. The proof sketch in Section 2.4 provides clear intuition: a better surrogate reduces the variance of the Monte Carlo estimator for the defect, creating a virtuous cycle. This is a genuine theoretical contribution that extends classical defect-correction convergence results to the Monte Carlo/high-dimensional setting.

- **Comprehensive and convincing experiments.** The paper evaluates SCaSML across four distinct PDE types (linear convection-diffusion, viscous Burgers, HJB, diffusion-reaction), two surrogate types (PINN, GP), dimensions up to 160, and multiple error norms. Table 1 shows consistent improvement across nearly all settings. The inference-time scaling plots (Figure 3b) and the empirical verification of the improved scaling law (Figure 4) provide strong evidence for the framework's effectiveness.

- **Practical relevance and flexibility.** The "elastic compute" paradigm—trading inference time for accuracy on demand—is genuinely useful for applications like financial pricing and optimal control where high precision is needed at specific query points. The framework is surrogate-agnostic, working with both PINNs and GPs, which demonstrates its plug-and-play nature.

## Weaknesses

### Fatal
None.

### Major

- **Insufficient computational cost fairness analysis.** The central practical question is whether the inference-time compute is better spent on SCaSML's correction step versus training a larger or better surrogate. Table 1 shows SCaSML's runtime is often 10–100× larger than the base surrogate (e.g., LCD 60d: 0.28s vs 37.59s). The abstract claims "a smaller base PINN can outperform a larger PINN under the same inference-time compute budget," but this experiment is not clearly presented in the main text. Without a controlled comparison showing that the same total compute budget allocated to SCaSML outperforms allocating it entirely to surrogate training, the practical value proposition remains incomplete. This is the most significant gap in the experimental evaluation.

- **Clipping thresholds as a confounding factor.** Different clipping thresholds are used for different methods (e.g., LQG: threshold 10 for naive MLP vs. 0.1 for SCaSML; DR: 10 vs. 0.01). These choices significantly affect the results, and the naive MLP's poor performance may partly reflect unfavorable threshold settings rather than fundamental limitations. The paper should provide sensitivity analysis showing how results vary with clipping threshold, and ideally use a principled method for selecting these thresholds.

### Minor

- **The "first" claims are overstated.** The paper claims to be "the first physics-informed inference time scaling framework" and to establish the improved convergence result "at the first time." While the specific combination is novel, defect correction is a well-established technique, and the analogy to LLM inference-time scaling is somewhat loose (LLM inference-time scaling involves search/planning over discrete outputs, while this involves continuous numerical simulation). More measured language would strengthen the paper.

- **Limited PDE class.** The framework is restricted to semi-linear parabolic PDEs. While this is a broad and important class, the paper should more explicitly discuss which common PDE types fall outside this scope (e.g., fully nonlinear PDEs, hyperbolic PDEs, elliptic PDEs without time dependence) and whether extensions are possible.

- **The α(1) term in Corollary 2.6 is not defined in the main text.** The improved scaling law O(m^{-γ-1/2+α(1)}) contains an unspecified correction term, making it difficult to assess the tightness of the bound from the main paper alone.

### Trivial
None.

## Nice-to-Haves

- A wall-clock comparison plot showing error vs. total compute budget (training + inference) for SCaSML versus a surrogate trained with the same total budget would be very informative.
- Discussion of how the method performs when the surrogate is poor (large error), which would stress-test the framework's robustness.
- Analysis of how the number of MLP levels and samples should be chosen in practice as a function of the estimated surrogate quality.

## Novel Insights

The paper's most novel insight is that the defect PDE for semi-linear parabolic equations preserves the semi-linear structure, which is the key enabler for applying Monte Carlo methods in high dimensions. This structural preservation is non-trivial: one might expect the defect equation to involve complicated coupling between the surrogate and the true solution, but the subtraction procedure yields a clean semi-linear form with a modified nonlinearity. The connection to inference-time scaling in LLMs, while somewhat loose as an analogy, provides a useful conceptual framework for thinking about allocating computation between training and inference. The observation that Monte Carlo is particularly well-suited for correcting neural network surrogates—because it handles the high-frequency residual that surrogates struggle with, independent of integrand smoothness—is also insightful.

## Suggestions

- Add a controlled experiment comparing SCaSML (small surrogate + correction) against a larger surrogate trained with the same total compute budget, to directly validate the "elastic compute" claim.
- Include sensitivity analysis for the clipping threshold hyperparameter, which currently varies across experiments and could confound results.
- Provide a practical guideline or heuristic for choosing MLP parameters (number of levels, samples per level) based on estimated surrogate quality.

## Score and Decision

The paper presents a genuinely novel framework with solid theoretical grounding and comprehensive experiments. The core idea of structural-preserving defect correction via Monte Carlo simulation is elegant and practically relevant. The major weakness—insufficient computational cost fairness analysis—is significant but addressable, and does not invalidate the paper's core contributions. The theoretical results are sound, the experiments are thorough, and the framework opens a promising research direction at the intersection of scientific computing and machine learning.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>