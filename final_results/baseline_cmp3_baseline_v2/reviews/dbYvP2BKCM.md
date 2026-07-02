## Summary

The paper proposes ZNet, a deep learning method for automatically constructing instrumental variable (IV) representations from observed covariates to enable causal effect estimation under unobserved confounding. ZNet learns a decomposition of the observed data into a confounder representation \(C=f(X)\) and an instrument representation \(Z=g(X)\) via neural networks, using a multi-part loss that enforces the IV conditions of relevance, exclusion restriction, and unconfoundedness. The learned representations can be plugged into standard downstream IV estimators (TSLS, DeepIV, DFIV). Experiments on semi-synthetic IHDP-based datasets show that ZNet recovers ground-truth instruments when they exist and produces valid instrument representations that reduce confounding bias in diverse scenarios.

## Strengths

- **Novel formulation**: ZNet explicitly encodes the IV structural causal model into a neural architecture with loss terms that correspond to the three IV conditions, differing from prior work that relies on variational autoencoders. This gives a transparent and modular framework.
- **Comprehensive evaluation**: The paper tests ZNet across eight data generation scenarios (varying instrument existence, linear/nonlinear, presence/absence of unobserved confounders) and with three downstream estimators, providing a thorough empirical comparison against multiple IV generation baselines (AutoIV, VIV, GIV) and a standard causal inference method (TARNet).
- **Ablation and diagnostic analysis**: The authors include ablation studies (showing the contribution of each loss term) and verify IV-relevant diagnostics (F-statistics, correlation checks), which strengthens the evidence that the learned representation satisfies the intended conditions.

## Weaknesses

### Fatal
- **Lemma 1 and the unconfoundedness constraint are unsupported.** Lemma 1 claims that if \(Z\sim\mathcal{N}(0,\sigma^2)\) and \(\text{Cov}(Z, e_Y - \mathbb{E}[e_Y|X,T])=0\) then \(\text{Cov}(Z, e_Y)=0\). The proof contains a critical error: it incorrectly replaces \(\mathbb{E}[Z \cdot \mathbb{E}[e_Y|X,T]]\) with \(\mathbb{E}[Z]\cdot\mathbb{E}[e_Y|X,T]\). Since \(Z=g(X)\), \(Z\) is a function of \(X\), so \(\mathbb{E}[Z \cdot \mathbb{E}[e_Y|X,T]] = \mathbb{E}[Z\,\mathbb{E}[e_Y|X,T]]\) is generally not equal to \(\mathbb{E}[Z]\mathbb{E}[e_Y|X,T]\). Therefore, the loss \(L_{Z \not\leftrightarrow \epsilon_Y}^{PC}\) that minimizes covariance between \(Z\) and the residuals \(Y-\hat{Y}\) does **not** guarantee \(\text{Cov}(Z,e_Y)=0\) as claimed. The entire justification for relaxing the assumption that unobserved confounders do not influence the observed data collapses. This invalidates a core theoretical claim of the paper and undermines the reliability of the unconfoundedness enforcement. Without a correct argument, the method is no different from arbitrarily minimizing a correlation that may not correspond to the intended causal condition.

### Major
- **Sufficiency of constraints**: The losses enforce only pairwise correlations (or mutual information via KDE approximations) between scalar quantities. The IV conditions require full conditional independence (e.g., \(Z \perp e_Y \mid C\)), not just zero correlation or low mutual information. The empirical checks (Figure 6b) test only linear predictability in a regression, which is insufficient to verify the exclusion restriction and unconfoundedness for general nonlinear causal models. The paper does not discuss this gap or provide evidence that the learned representations satisfy the stronger independence requirements.
- **Hyperparameter sensitivity and complexity**: The method requires Bayesian optimization over many loss coefficients (\(\alpha_1\)–\(\alpha_7\)), choice of correlation vs. MI losses, gradient surgery, and pretraining stages. While hyperparameter tuning is acceptable, the heavy reliance on multi-objective optimization and the need to select Pareto-front points by F-statistic introduces degrees of freedom that make the method difficult to apply robustly in practice. The performance differences between ZNet and baselines in Table 1 are often small, and it is unclear whether ZNet’s wins are statistically significant beyond the reported averages (no confidence intervals or significance tests are provided for most entries).
- **Limited comparison with related IV-generation methods**: The paper only compares ZNet against AutoIV, VIV, and GIV. Several recent methods (e.g., GDIV Chou et al., 2024, DVAE-CIV Cheng et al., 2023) are cited in related work but not empirically evaluated. Given that these are directly competitive and appeared after or simultaneously, the evaluation feels incomplete.

### Minor
- The data generation process is based on IHDP covariates but uses synthetic outcomes and treatments. While this allows controlled evaluation, the realism of the scenarios (especially the “no candidate” cases where no observed variable is a valid instrument) is limited. The paper would benefit from at least one real-world or more realistic semi-synthetic benchmark.
- The description of the training pipeline could be clearer: the three-stage training is described, but it is not stated how the gradient surgery (Yu et al., 2020) is applied exactly or when it is used. The hyperparameter tuning details (e.g., search ranges for \(\alpha\) weights) are deferred to the appendix (removed), so reproducibility is hampered.

### Trivial
- Figure 6a shows calibration plots for relevance but the p-values reported are from an F-test; the test split F=1.83, p=0.081 suggests weak relevance in the test set, which contradicts the claim of strong relevance. This deserves a brief discussion.

## Nice-to-Haves
- A theoretical result that justifies why minimizing correlation (or MI) between \(Z\) and the residuals, under the specific architecture and data assumptions, can still yield approximately unconfounded instruments even if Lemma 1 is flawed. Alternatively, a different, provably correct approach to enforce unconfoundedness.
- Experiments with continuous treatments to demonstrate the claimed generality of ZNet.
- A sensitivity analysis showing how ATE estimation quality varies with the strength of unobserved confounding.

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
1. **Fix or remove Lemma 1.** If the unconfoundedness constraint cannot be theoretically justified, the paper should clearly state that the loss is a heuristic and discuss its limitations. Alternatively, derive a correct condition (e.g., using orthogonalization or doubly robust ideas).
2. **Strengthen empirical validation of IV conditions** by testing not just linear dependence but also nonlinear dependence (e.g., using kernel-based independence tests). Provide evidence that the learned \(Z\) is conditionally independent of \(Y\) given \(C\) and \(T\) beyond simple F-tests.
3. **Provide confidence intervals or standard errors** for the ATE errors in Table 1 (e.g., bootstrap intervals) to allow the reader to assess statistical significance of the differences.
4. **Include at least one real-data benchmark** or a more realistic simulation (e.g., using existing observational datasets with known instruments, such as the Health and Retirement Study or the CPS) to increase external validity.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>