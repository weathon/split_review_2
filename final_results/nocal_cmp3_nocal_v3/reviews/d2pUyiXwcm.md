Here is the final consolidated review.

---

## Summary

This paper proposes SCaSML, a framework that combines pre-trained surrogate models (PINNs, GPs) with a Monte Carlo defect-correction step for solving high-dimensional semi-linear parabolic PDEs. The core idea is to derive a new PDE (the "Structural-preserving Law of Defect") that describes the surrogate's error, then solve that defect PDE using Multilevel Picard (MLP) iteration. The paper proves a product-form error bound and demonstrates empirical results on PDEs up to 160 dimensions.

## Strengths

- **Mathematically clean derivation of the defect PDE (Fact 2.3, Section 2.2).** Subtracting the surrogate's approximate equation from the original semi-linear parabolic PDE yields a new PDE for the defect ũ that retains semi-linear structure. While algebraically straightforward, this is the correct foundation for the method and is clearly presented.

- **Demonstration on genuinely high-dimensional problems (up to 160D).** The experimental suite includes HJB and diffusion-reaction equations at 100–160 dimensions, which are genuinely challenging for traditional numerical methods. This sets the paper apart from work that stops at 10–20 dimensions.

- **Clear exposition of the MLP mechanism (Section 2.3).** The explanation of Multilevel Picard iteration, variance reduction through correlated levels, and why fewer expensive samples are needed at fine levels is accessible and well-structured.

- **Empirical verification of improved scaling (Figure 4).** The paper shows log-log plots of error vs. collocation points for GP and SCaSML across multiple dimensions, with SCaSML consistently exhibiting a steeper slope, providing empirical support for the claimed convergence acceleration.

## Weaknesses

### Major

**1. Uncontrolled baseline comparison (naive MLP).** The primary comparison against the "naive MLP" baseline uses asymmetric hyperparameters that undermine the fairness of the comparison:

- For 3 of 4 problems (VP-PINN, LQG, DR), different clipping thresholds are used for the naive MLP vs. SCaSML (e.g., LQG: clipping threshold 10 for MLP vs. 0.1 for SCaSML, lines 250, 242, 296). The paper acknowledges the asymmetry but does not justify why this is a fair comparison or provide a sensitivity analysis.
- The naive MLP is uniformly run with 2 levels and M=10 base samples — while SCaSML additionally benefits from the surrogate's preconditioning. The computational cost of SCaSML is consistently higher (2–12× for most problems, Table 1), yet the comparison is presented as error-at-fixed-hyperparameters rather than error-at-fixed-budget.
- LQG results show naive MLP errors >500% (relative L² of 5.27–5.63, lines 205–208). While this demonstrates that the method can succeed where naive MLP cannot, the different clipping thresholds and lack of computational budget control make it unclear whether a better-tuned or better-budgeted MLP would perform differently.

**2. Missing uncertainty quantification for Monte Carlo results.** Table 1 reports all errors as single point estimates with no error bars, confidence intervals, or variance information. For a method whose correction step is a Monte Carlo estimator, this is a significant omission. The paper references statistical significance tests (p ≪ 0.001) in Appendix G.4, but the main text provides no variance information, making it impossible for the reader to assess whether the observed error reductions are statistically reliable or within the noise of the estimator.

**3. Unsubstantiated claim about the MLP error term's independence from the surrogate (Theorem 2.5).** The paper states (line 214) that the MLP error term E(M,N) is "independent of the surrogate." However, the MLP solver operates on the defect PDE (7), whose modified nonlinearity F̃ depends explicitly on û through F(û+ũ, σᵀ(∇û+∇ũ)) − F(û, σᵀ∇û). The Lipschitz constant of F̃ — which controls MLP convergence — generally depends on û and its derivatives. The claim that E(M,N) factors out cleanly from the surrogate's influence requires justification not provided in the main text.

**4. Heuristic convergence rate conflates training points and Monte Carlo paths (Section 2.1, lines 105–106).** The heuristic analysis assumes that (a) the surrogate error scales as m^{−γ} using m training points, (b) m additional Monte Carlo paths are used at inference, and (c) the total cost is "2m function evaluations." A PINN training point (one collocation point evaluation during training) and a Monte Carlo MLP path (simulating an SDE trajectory with many time steps, evaluating the surrogate and its derivatives at each step) have vastly different computational costs. The "2m" framing is therefore not a meaningful cost metric. The empirical validation in Figure 4 uses collocation points rather than wall-clock time, and so inherits this limitation.

### Minor

**5. The "inference-time scaling" LLM analogy is a poor fit for the method's computational profile.** The paper frames SCaSML as "inference-time scaling" by analogy to LLMs (lines 15–21, 328). In LLMs, inference-time scaling means the same model allocates more computation (e.g., chain-of-thought tokens) at inference. In SCaSML, the "inference-time" step involves running a full Multilevel Picard Monte Carlo solver — simulating SDE paths, computing nested expectations, and evaluating surrogate derivatives — which costs 10–200× the surrogate evaluation (Table 1). This is better described as a surrogate-accelerated Monte Carlo solver. The framing does not invalidate the method but sets up expectations the paper does not meet and should be revised.

**6. The abstract's "20-80%" improvement claim is broader than the results support.** The DR problem improves only 6.6–10.9% (line 302), which falls below the 20% lower bound advertised in the abstract. While the 20-80% range may hold for other problems in aggregate, the abstract should be precise about which problems yield which improvement levels.

**7. Claim about "smaller PINN outperforming larger PINN" is stated as a contribution but has no supporting evidence in the main text.** Line 33 states this as one of the paper's main contributions, but no experiment comparing different-sized surrogates or compute-budget scaling appears in the main text. For a claimed contribution, at least a summary figure or table should appear in the main body.

**8. Novelty claims are somewhat oversold.** The derivation of the defect PDE (Fact 2.3) is a direct algebraic manipulation that necessarily preserves semi-linear structure because F(û+ũ,...) is still a nonlinear function of ũ. Claiming this as the "first derivation" (line 31) overstates the novelty. Defect correction for PDEs is classical (Stetter 1978; Bank & Weiser 1985); the genuine novelty is using Monte Carlo to solve the defect equation, not the defect PDE itself.

### Trivial

None.

## Nice-to-Haves

- A computational cost breakdown showing where SCaSML's 10–200× overhead goes (surrogate derivative evaluations, SDE path simulation, MLP level nesting) would help readers understand scaling behavior.
- A sensitivity analysis for MLP hyperparameters (number of levels, base samples, clipping threshold) would strengthen the empirical claims.
- A discussion of the threshold of surrogate quality below which SCaSML offers no benefit (or hurts) would be useful for practitioners.

## Removed Points

These points were flagged in the input review but are removed or downgraded for the indicated reasons:

- **The "inference-time scaling" analogy as a "Critical Issue":** The input review treated this as one of the most critical flaws. It is retained as a Minor weakness (issue 5 above) because the paper does clearly describe the computational procedure; the issue is presentation framing, not methodological validity.
- **"Principled connection between surrogate accuracy and Monte Carlo variance" listed as a Strength:** The input review listed this as a strength, but the same review's critique of the convergence heuristic (Section 2.1, lines 105–106) shows that the specific analysis conflates incomparable cost metrics. Per filtering rules, strengths that conflict with verified weaknesses are removed from the strengths list. The general principle (better surrogate → lower variance) is sound, but the paper's specific rate analysis is flawed.
- **Criticism about missing appendix content (fixed-budget comparisons in G.7, p-values in G.4):** The parser strips appendix content from all papers. Per instructions, papers are not penalized for content that exists in the original but is removed during parsing. The broader criticism about the main-table design not controlling for compute budget is retained (Major issue 1), as this concerns the experimental design presented in the main text.
- **Pure formatting artifacts (Table 1 notation inconsistencies):** The Table 1 formatting issues (SCa²SM¹, SCSML, etc.) are parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface any observation about the paper that the paper itself does not make.

## Suggestions

1. Reframe the paper as a "surrogate-accelerated Monte Carlo solver" or "hybrid defect-correction method" and drop the LLM inference-time analogy, which invites unfair comparisons and distracts from the technical contribution.
2. Report error bars (mean ± std over multiple random seeds) for all Monte Carlo results in Table 1, or at minimum include a variance summary in the main text.
3. Fix the baseline comparison: either (a) compare all methods at matched total compute budgets (wall-clock time), or (b) include a sensitivity study showing how the naive MLP's error changes with its hyperparameters (levels, samples, clipping). The current asymmetric clipping thresholds and uncontrolled budgets weaken an otherwise interesting demonstration.
4. Justify or remove the claim that E(M,N) is "independent of the surrogate" in Theorem 2.5, or clarify the conditions under which this holds.
5. Either include the "smaller PINN outperforming larger PINN" experiment as a main-text figure/table, or remove the claim from the contributions list.
6. Be precise about the per-problem improvement ranges in the abstract rather than aggregating to a single "20-80%" range.

## Score and Decision

The paper's core method — framing surrogate correction as solving a defect PDE with a Monte Carlo solver that exploits the surrogate's small residual — is sound, and the experiments reach genuinely high dimensions. However, the experimental comparison is weakened by uncontrolled baselines and missing uncertainty quantification for Monte Carlo results. The theoretical analysis has unresolved gaps (the "independent of the surrogate" claim, the conflated cost metric in the convergence heuristic). The framing and novelty claims are somewhat oversold. The method has genuine merit, but in its current form the gap between the claims and the supporting evidence is too wide for acceptance at ICLR.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>