## Summary
This paper establishes a first-order equivalence between activation steering (injecting vectors into intermediate layers) and training-data influence functions (re-weighting examples), showing they are projections of the same sensitivity tensor. The authors construct an Influence-Aligned Steering (IAS) vector via a minimum-norm pseudoinverse, introduce a principal-angle diagnostic γ for feasibility, derive spectral optimality for steering directions, and provide generalization bounds for low-rank interventions.

## Strengths
- **Novel theoretical unification.** Connecting activation steering and influence functions through a shared first-order sensitivity tensor is a genuinely original insight. The primal-dual formulation (Section 3) and the closed-form IAS construction are clean and well-motivated. This bridges two previously disconnected interpretability communities.
- **Practical diagnostic via γ.** The principal-angle cosine γ(x) provides a cheap, interpretable feasibility check (two SVDs) that tells practitioners whether steering can match influence at a given layer. The layer-depth ablation (Figure 2) showing γ increasing monotonically with depth is a useful empirical finding that supports the theory.
- **Impossibility result (Theorem 6.2).** The no-free-lunch bound showing that poor alignment (small γ) fundamentally limits steering fidelity is a valuable negative result that gives practitioners clear guidance on when to abandon steering.
- **Generalization bounds.** The Rademacher complexity analysis (Theorem 6.1) showing that low-rank IAS incurs only an O(αL√(2k/dn)) excess complexity term is a useful theoretical guarantee.

## Weaknesses
### Fatal
None.

### Major
- **IAS underperforms CAA in the main task.** Table 1 shows IAS achieves worse toxicity reduction (0.0164 vs. 0.0150) and worse perplexity (13701 vs. 13291) than CAA on the detoxification benchmark. The paper does not discuss this or explain why the theoretically-motivated method loses to the heuristic baseline. This undermines the practical value proposition.
- **Slope discrepancy in first-order validation.** Figure 1 reports a slope of 1.50 between predicted and actual logit shifts, not the expected 1.0. A 50% systematic deviation from the first-order theory is significant and inadequately explained. The paper calls this "consistent with the expected linear regime" but a slope of 1.50 suggests either the perturbations are not truly infinitesimal or there is a systematic bias. This is the paper's central empirical claim and it does not hold cleanly.
- **No end-to-end workflow demonstration.** The paper's key practical promise is a workflow: "steer first, trace provenance, edit weights only when the geometry demands it." Yet no experiment demonstrates that ρ_s (the signed measure from Theorem 4.2) successfully identifies causal training examples, or that the γ diagnostic correctly predicts steering success/failure in practice. The causal tracing claim (Section 4.1) remains entirely theoretical.
- **Limited experimental scope.** All language experiments use only GPT-2 Medium (a 355M model), and the vision experiment uses only ResNet-50 on a single class. The paper claims the framework "scales to billion-parameter models" but provides no evidence for this. The spectral optimality experiment (Figure 3) compares against random directions—a very weak baseline—rather than against principled alternatives.

### Minor
- **The ℓ₁-minimality proof sketch (Corollary 1) appears incomplete.** The argument that "if another measure achieved the same shift with smaller ℓ₁ norm, one could scale ρ_s down" does not logically follow—scaling down ρ_s would change the shift. The actual argument should rely on the structure of the minimum-norm solution, not a scaling argument.
- **The spectral direction recipe (Theorem 5.3) is expensive.** Computing J_{θ→h}^T H^{-1} ∇_θ ℓ(z, θ) for each training example in a batch requires Hessian-vector products over the full parameter space, which is prohibitive for large models. The paper does not discuss computational cost or provide timing results.
- **Layer choice heuristic is ad hoc.** The suggestion to "pick the smallest layer index with γ ≥ 0.7" (Section 4.2) is not validated empirically. Why 0.7? What happens at different thresholds?

### Trivial
None.

## Nice-to-Haves
- An experiment on a larger model (e.g., Llama-7B or GPT-2-XL) to support the scalability claims.
- A demonstration of the causal tracing workflow: apply IAS, compute ρ_s, inspect top-weighted training examples, and verify they are semantically related to the steered behavior.
- Analysis of when/why IAS underperforms CAA—is it a rank limitation, a first-order approximation error, or something else?
- Timing benchmarks for the full IAS pipeline (Jacobian computations, pseudoinverse, γ estimation).

## Novel Insights
The paper's central insight—that activation steering and influence functions are first-order duals sharing the same sensitivity tensor—is genuinely novel and has not appeared in prior work. The geometric framing through principal angles (γ) and the resulting impossibility theorem provide a principled way to reason about when steering can substitute for weight-space interventions. The spectral optimality result (Theorem 5.3), connecting the optimal steering direction to the top eigenvector of an influence-weighted Fisher matrix, is also a new contribution that could guide future steering vector design.

## Suggestions
- Address the slope-1.50 discrepancy directly: run the linearity experiment at multiple perturbation magnitudes to verify the first-order regime and identify where the approximation breaks down.
- Add a causal tracing experiment: compute ρ_s for a known steering vector (e.g., toxicity suppression), retrieve top-weighted training examples, and qualitatively/quantitatively verify they are causally relevant.
- Compare IAS against CAA more thoroughly—vary the layer, magnitude, and number of contrast pairs—to understand when IAS's theoretical advantages translate to empirical gains.
- Provide computational cost analysis, including wall-clock times for the Jacobian computations and pseudoinverse operations.

## Score and Decision
The theoretical contribution is novel and elegant, providing a clean mathematical bridge between two important interpretability techniques. However, the experimental validation is insufficient: IAS underperforms the baseline it should improve upon, the central linearity claim shows a 50% slope error, and the practical workflow (causal tracing via ρ_s) is never demonstrated empirically. The experiments feel preliminary rather than thorough. The theory deserves publication, but the paper needs substantially stronger empirical support to justify acceptance at ICLR.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject