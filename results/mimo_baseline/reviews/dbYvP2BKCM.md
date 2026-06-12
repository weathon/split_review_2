## Summary

The paper proposes ZNet, a deep learning architecture that decomposes observed covariates into confounder and instrument representations satisfying standard IV assumptions (relevance, exclusion restriction, unconfoundedness). The method enforces these conditions through explicit loss constraints rather than variational distributions, and can recover existing instruments or construct proxy latent instruments when none exist. The paper evaluates ZNet across comprehensive semi-synthetic datasets and shows competitive performance against existing IV generation methods (AutoIV, GIV, VIV).

## Strengths

- **Novel architecture design with clear causal motivation**: ZNet's multi-armed architecture (Figure 3) directly mirrors the IV structural causal model, with separate networks f and g for learning confounder and instrument representations. The explicit constraint-based approach (Constraints 1–3) is a clear differentiator from prior variational approaches and offers more transparent control over IV validity.

- **Comprehensive evaluation across diverse settings**: The paper evaluates across 10 dataset configurations (linear/non-linear × disjoint/latent/mixed/no-candidate/no-U), 3 downstream estimators (TSLS, DeepIV, DFIV), and 4 IV generation methods. This is notably more thorough than prior work and demonstrates broad applicability.

- **Strong instrument recovery evidence**: ZNet successfully recovers existing instruments (Figure 5, R² up to 0.84) and latent categorical instruments (Figure 4, near-perfect confusion matrix). The ablation study (Figure 5c) convincingly demonstrates that each loss component contributes to instrument recovery, with ablating all constraints reducing R² to ~0.02–0.05.

- **Competitive treatment effect estimation**: In the "No Candidate" settings (both linear and non-linear), where no explicit instruments exist, ZNet frequently achieves the smallest ATE errors (e.g., Table 1: Linear No Candidate with DeepIV error 0.189, Non-linear No Candidate with DFIV error 0.049).

## Weaknesses

### Fatal
None.

### Major

- **Lemma 1 proof contains an algebraic error**: The proof claims that E[Z · (e_Y − E[e_Y|X,T])] = E[Z · e_Y] − E[Z] · E[e_Y|X,T]. This is incorrect because E[e_Y|X,T] is a random variable, not a constant. The correct expansion is E[Z · e_Y] − E[Z · E[e_Y|X,T]], and since Z = g(X), we have E[Z · E[e_Y|X,T]] = E[g(X) · E[e_Y|X,T]] ≠ E[Z] · E[e_Y|X,T] in general. This undermines the paper's key claim that the method handles the case where X may be influenced by U, which is presented as a distinguishing theoretical contribution over prior work.

- **Limited to semi-synthetic data**: All experiments use IHDP-based semi-synthetic data with author-controlled data-generating processes. The paper's strong claim that "ZNet can be used as a plug-in module for causal effect estimation in general observational settings" lacks real-world validation. Semi-synthetic evaluations, while useful, cannot fully capture the complexity of real observational data.

- **Mixed empirical results**: ZNet does not consistently outperform all baselines. In several settings, other methods achieve smaller errors: AutoIV+DeepIV in Linear Disjoint (0.038 vs. ZNet's 0.054), VIV+TSLS in Linear Latent (−0.082 vs. −0.125), and GIV+TSLS in Linear No Candidate no-U (0.137 vs. 2.718). The claim of "superior" performance is overstated relative to the evidence.

### Minor

- **Complex and opaque tuning procedure**: The two-stage Bayesian optimization with multi-objective Pareto front selection, using a nearest-neighbor ATE proxy, adds significant complexity. The sensitivity of results to tuning choices is not analyzed.

- **Binary treatment only**: Despite claiming generalizability, all experiments use binary treatments. The practical relevance for continuous treatment settings (common in economics and medicine) remains undemonstrated.

### Trivial
None.

## Nice-to-Haves

- Real-world experiments on observational datasets (e.g., using known IV settings from econometrics)
- Analysis of computational cost and scalability to high-dimensional data
- Sensitivity analysis of results to architectural choices (number of layers, dimensionality of Z and C)
- Extension to continuous treatments with empirical validation

## Novel Insights

The paper's genuinely novel insight is that IV conditions can be enforced through explicit, interpretable loss constraints in a purpose-built neural network architecture, rather than through variational inference. This constraint-based approach provides direct control over instrument validity—each IV assumption maps to a specific loss term that can be monitored during training. The combination of this transparency with the ability to construct instruments even when none exist in the observed data represents a meaningful conceptual advance over prior variational methods, which lack such direct interpretability of whether IV conditions are satisfied.

## Suggestions

- **Fix or replace Lemma 1**: Either provide a correct proof under additional explicit assumptions (e.g., if Z is constructed to be independent of X, or under specific distributional conditions on e_Y), or remove the claim about handling X influenced by U and focus the theoretical contribution on the standard setting where X ⊥ U.
- **Add at least one real-world experiment**: Even a simple application using a known IV setting (e.g., returns to schooling with geographic instruments) would significantly strengthen the practical relevance claims.
- **Provide failure mode analysis**: Under what conditions does ZNet fail to produce valid instruments? What diagnostic checks can practitioners use to assess instrument quality before downstream estimation?

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>