## Summary

This paper identifies three fundamental limitations of static pre-training in Supervised Causal Learning (SCL): fragility to distribution shifts, failure in compositional generalization, and a significant performance gap between synthetic benchmarks and real-world data. To address these issues, the authors propose Test-Time Training for Supervised Causal Learning (TTT-SCL), a framework that dynamically generates training data aligned with each test instance. They instantiate this framework with TACTIC, which uses an Alignment of Distribution (AD) metric combined with sparsity constraints to search for causally-aligned training graphs at test time, and demonstrate strong empirical performance across synthetic, pseudo-real, and real-world datasets.

## Strengths

- **Clear identification of a fundamental problem in SCL:** The paper systematically demonstrates three critical limitations of static SCL pre-training (distribution shift fragility, compositional generalization failure, and synthetic-to-real transfer gap) through well-designed experiments. This analysis is valuable and convincingly shows that the current SCL paradigm has serious practical limitations.
- **Novel and well-motivated framework:** The TTT-SCL framework is a creative and principled solution to the identified problems. The shift from diversity-seeking pre-training to test-time concentration is well-motivated by the empirical findings, and the framework elegantly addresses the core issue of distribution mismatch.
- **Strong empirical results:** TACTIC achieves state-of-the-art performance on multiple datasets, including real-world Sachs and pseudo-real Syntren, where static SCL methods fail. The ablation study and stage-wise analysis convincingly demonstrate the contribution of each component (AD, sparsity, and the SCL learning phase).
- **Clear and well-structured presentation:** The paper is well-organized, with a clear problem statement, systematic empirical demonstration of limitations, a principled framework, and thorough experimental validation. The figures and tables effectively communicate the key findings.

## Weaknesses

### Fatal
None.

### Major
- **Computational cost and scalability are not adequately addressed:** The TTT-SCL framework requires, for each test instance, generating 200 training graphs, regressing mechanisms, forward-sampling datasets, and training an SCL model from scratch. The paper only briefly mentions complexity analysis in Appendix F but does not provide concrete runtime numbers, memory requirements, or a comparison of computational cost against baselines. For a method that requires per-instance training, this is a critical practical concern. Without understanding the computational overhead, it is difficult to assess whether the method is feasible for real-world applications, especially as the number of variables or dataset size grows.
- **The AD metric's reliance on likelihood may be problematic for high-dimensional or complex data:** The AD metric (Equation 3) uses log-likelihood based on regressed mechanisms from the candidate graph. This requires fitting a regression model for each variable given its parents, which becomes computationally expensive and potentially unstable as the number of variables grows or when the true mechanisms are highly complex. The paper does not discuss the choice of regression model, its sensitivity to hyperparameters, or how it handles non-identifiable settings where multiple graphs yield similar likelihoods.
- **Limited discussion of identifiability conditions:** The paper states that TTT-SCL is "applicable to any assumption that guarantees the identification of the underlying causal graphs" but does not discuss how the method behaves when identifiability conditions are violated. In practice, many real-world datasets may not satisfy the assumptions required for unique identification (e.g., additive noise models with Gaussian noise). The paper would benefit from a discussion of when the method might fail or produce unreliable results.

### Minor

- **The AD metric's likelihood formulation (Equation 3) is somewhat underspecified:** The paper states that $f_i^k$ is the "fitting function of $X_i$ according to $\text{Pa}_{train}^k(X_i)$ based on $G_{train}^k$ and $D_{test}$ by SIM," but does not specify what class of functions is used for fitting (e.g., linear regression, neural networks, Gaussian processes) or how the likelihood is computed. This makes the implementation details unclear and the results potentially sensitive to this choice.
- **The sparsity hyperparameter $\lambda$ is not discussed:** The paper introduces $\lambda$ in Equation 5 but does not discuss how it is chosen, whether it is tuned per dataset, or how sensitive the results are to its value. This is important for reproducibility and practical application.
- **Limited comparison with other test-time adaptation approaches:** While the paper compares against traditional causal discovery methods and static SCL, it does not compare against other test-time adaptation or meta-learning approaches that could be applied to causal discovery. The related work section mentions test-time adaptation in general ML but does not discuss how TTT-SCL relates to or differs from these approaches in practice.

### Trivial
None.

## Nice-to-Haves
- A discussion of the computational cost (runtime, memory) of TACTIC compared to baselines, perhaps with a table or figure showing scaling with number of variables and sample size.
- An analysis of the sensitivity of results to the choice of $\lambda$ and the regression model used for AD computation.
- A comparison against a simple baseline that uses the seed graph directly (without the SCL training phase) to more clearly isolate the benefit of the SCL component.

## Novel Insights

The paper's key insight is that the failure of SCL is not merely about insufficient diversity in pre-training data, but a more fundamental issue of compositional generalization: models memorize specific configurations rather than learning modular causal representations. This motivates a paradigm shift from static diversity-seeking pre-training to dynamic test-time concentration. The idea of using distributional alignment (AD) as a proxy for causal similarity between candidate graphs and test data, combined with sparsity constraints to enforce causal minimality, is a novel and principled approach to generating causally-aligned training data at test time.

## Suggestions

- Provide concrete runtime measurements and scaling analysis for TACTIC across different numbers of variables and sample sizes, comparing against baseline methods.
- Specify the regression model used for AD computation and discuss its sensitivity to hyperparameters and data characteristics.
- Discuss the choice of $\lambda$ and provide guidance or a sensitivity analysis for this hyperparameter.
- Add a discussion of identifiability conditions and when the method might be expected to fail.

## Score and Decision

The paper makes a significant contribution by identifying a fundamental limitation of static SCL and proposing a novel, well-motivated framework (TTT-SCL) with a concrete instantiation (TACTIC) that demonstrates strong empirical results. The problem is important, the approach is creative and principled, and the experiments are thorough. The main weakness is the lack of discussion about computational cost and scalability, which is important for practical applicability but does not invalidate the core contribution. The paper is clearly written and makes a compelling case for a paradigm shift in SCL.

MY FINAL SCORE: 8.0score</score>
MY FINAL DECISION: Accept</decision>