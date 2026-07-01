## Summary

The paper proposes ZNet, a deep learning method that learns instrument (Z) and confounder (C) representations from observed covariates X for causal effect estimation with instrumental variables (IV). The architecture encodes the structural causal model of IVs through a multi-part loss enforcing relevance, exclusion restriction, and unconfoundedness. The learned representations can be plugged into downstream IV estimators (TSLS, DeepIV, DFIV). Experiments on semi-synthetic datasets with varying instrument existence scenarios show that ZNet can recover ground-truth instruments when present and construct proxy instruments that reduce confounding bias, with competitive performance against existing IV generation methods (AutoIV, VIV, GIV).

## Strengths

- **Important problem**: Automating instrument construction from observed data could broaden the applicability of IV methods in settings where valid instruments are unavailable or unknown to the analyst.
- **Comprehensive evaluation**: The paper tests across multiple data generation scenarios (disjoint, mixed, latent, no candidate instruments) with both linear and nonlinear structural equations, and with/without unobserved confounding. This is the most extensive evaluation of IV generation methods I have seen.
- **Ablation studies**: The paper includes ablation experiments (Figure 5c) showing that each constraint in the loss function contributes to recovering true instruments, which helps validate the design choices.
- **Simple and transparent architecture**: The ZNet architecture directly encodes the SCM structure, making the approach more interpretable than variational autoencoder-based alternatives.

## Weaknesses

### Fatal
None.

### Major

1. **Insufficient theoretical justification for causal validity**: The paper enforces IV conditions through correlation-based constraints (Pearson correlation and mutual information). These are necessary but not sufficient for causal validity. For example, relevance is enforced by maximizing correlation between Z and T, but this could be achieved by Z capturing confounder variation that also affects T, violating exclusion restriction. The paper does not provide any identification guarantees or show that the learned representation satisfies the IV conditions in a causal sense (e.g., conditional independence of Z and potential outcomes). Lemma 1 only ensures zero covariance between Z and the residual, not full independence from unobserved confounders.

2. **Overstated claims of superiority**: The paper claims "superior performance" and "on average the highest performing among IV generation methods," but the results in Table 1 are mixed. ZNet is often the best or second best, but not consistently. In many settings, the differences are small and the significance testing is unclearly reported (what do single/double asterisks mean exactly?). For example, in the "Linear No Candidate (no U)" setting, ZNet's ATE error with TSLS is 2.718, which is much worse than GIV (0.137) and VIV (0.279). The paper's claims do not match the empirical evidence.

3. **Limited to semi-synthetic evaluation**: All experiments are on semi-synthetic data derived from IHDP covariates. While this is common, the paper would be significantly stronger with at least one real-world application where ground truth is known (e.g., a well-studied IV problem) or where the method provides new insights. The paper's claim that "ZNet can serve as a plug-in causal inference estimator" in real-world settings is not supported by real-world evidence.

4. **Missing comparisons to relevant baselines**: The paper compares only to AutoIV, VIV, GIV, and TARNet. Missing comparisons include: (a) DeepIV with oracle instruments (to show the gap between learned and true instruments), (b) methods that do not use IVs but adjust for observed confounders (e.g., propensity score methods, doubly robust estimation) to demonstrate the benefit of IV generation, (c) other recent IV generation methods from 2024 (e.g., DVAE.CIV, GDIV mentioned in related work but not compared).

5. **Unclear practical utility**: The method requires careful hyperparameter tuning via Bayesian optimization with multi-objective acquisition functions and gradient surgery for stability. The paper does not discuss the computational cost or sensitivity to hyperparameters. This limits the "plug-in" claim and practical adoption.

### Minor

- The loss term in Equation (7) includes MSE(C, Y), but C is a learned representation (vector) and Y is a scalar. It is unclear how MSE is computed here (per-dimension? averaged?).
- The paper uses both Pearson correlation and mutual information losses but does not clearly justify when to use which. The ablation studies only use PC, so the MI variant is not validated.
- Figure 4 shows a perfect diagonal confusion matrix for latent categorical instrument recovery, which seems too clean and may be an artifact of the specific data generation or evaluation procedure.
- The paper claims to "relax the assumption that unobserved confounders do not influence the observed data," but the method still assumes X is not influenced by U (standard in IV literature). Lemma 1 only addresses covariance with residuals, not full independence.

### Trivial

- The term "instrumental unconfoundedness" is non-standard; the usual term is "instrument exogeneity" or "independence of instrument and potential outcomes."
- The ethics statement mentions using LLMs for code production, which is unusual but not problematic.

## Nice-to-Haves

- A real-world case study (e.g., using genetic instruments or the classic college proximity example) would greatly strengthen the paper.
- Theoretical analysis of when the learned representation is guaranteed to satisfy IV conditions (e.g., under what functional form assumptions).
- Analysis of the sensitivity of results to the dimensionality of Z and C.
- Comparison to a simple baseline that uses all observed covariates as instruments (which would violate exclusion restriction but is a natural naive approach).

## Novel Insights

None beyond the paper's own contributions. The idea of learning instrument representations via constrained neural networks is novel, but the theoretical and empirical support is not strong enough to yield deeper insights about causal inference with learned instruments.

## Suggestions

1. Provide a clearer theoretical statement: under what conditions does the learned Z satisfy the three IV assumptions in a causal (not just correlational) sense? At minimum, discuss the gap between correlation-based constraints and causal validity.
2. Add a real-world experiment or a more realistic simulation (e.g., based on a known IV application) to demonstrate practical utility.
3. Include comparisons to additional baselines, especially DeepIV with oracle instruments and non-IV causal inference methods.
4. Clarify the significance testing in Table 1: what do the asterisks mean, and are the comparisons across methods or within methods?
5. Discuss the computational cost and hyperparameter sensitivity of the method.

## Score and Decision

The paper addresses an important problem and proposes a novel architecture with a comprehensive evaluation. However, the theoretical justification for causal validity is weak, the empirical results do not consistently support the claimed superiority, and the evaluation is limited to semi-synthetic data. These issues are major enough to weigh against acceptance at a top venue like ICLR. The paper has value but would need stronger theoretical grounding or more convincing empirical evidence (e.g., real-world validation) for acceptance.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>