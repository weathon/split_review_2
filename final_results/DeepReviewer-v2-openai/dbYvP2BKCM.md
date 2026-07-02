## Summary
# Final Review Report

## Summary

This paper proposes ZNet, a deep learning architecture for learning instrumental variable (IV) representations from observed data without requiring pre-existing instruments. The method decomposes observed covariates X into confounder C and instrument Z representations by enforcing three soft constraints corresponding to the standard IV assumptions: unconfoundedness, exclusion restriction, and relevance. The key idea is to learn two neural networks f and g that produce C=f(X) and Z=g(X) such that the causal graph C→Y, Z→T, T→Y holds. The resulting Z representation can be plugged into downstream IV estimators (TSLS, DeepIV, DFIV) for treatment effect estimation.

The paper makes several valuable contributions: (1) a novel constraint-based approach to IV representation learning that differs from existing variational autoencoder methods, (2) empirical demonstration that ZNet recovers ground-truth instruments when they exist and constructs proxy instruments otherwise, and (3) a comprehensive set of semi-synthetic experiments (linear/nonlinear, with/without candidate instruments, with/without unobserved confounding) showing competitive ATE estimation. The method shows particular promise in settings with unobserved confounding where no explicit instruments are available—a practically important scenario.

However, the paper has several significant weaknesses: a gap in the theoretical justification for the unconfoundedness constraint (Lemma 1), overclaimed statements about guarantees and generalizability, evaluation on a single real-data benchmark (IHDP), and underspecified training details that hinder reproducibility. The novelty of the approach within the growing literature on learned IV methods is unclear without a formal retrieval-based comparison, though the constraint-based formulation provides a distinct alternative to VAE-based approaches.

## Strengths
1. **Novel constraint-based approach to IV learning**: ZNet's architecture directly encodes the three IV assumptions through differentiable loss terms, offering a transparent alternative to VAE-based black-box methods. The multi-objective loss design (Pearson correlation + mutual information + KL divergence) provides flexible control over which assumptions are enforced and how strongly.

2. **Comprehensive experimental design**: The paper evaluates across 8 distinct data configurations (linear/nonlinear, disjoint/mixed/latent/no candidate, with/without unobserved confounding), creating a thorough testbed. The 50-resample bootstrap evaluation for ATE provides statistical rigor that many causal inference papers lack.

3. **Practical motivation and framing**: The problem of learning instruments automatically from data is practically important—many real-world settings lack valid pre-specified instruments. The emergency department example in Section 3 effectively illustrates how latent instruments could arise naturally in healthcare data.

4. **Downstream estimator compatibility**: ZNet is designed to work with any two-stage IV estimator (TSLS, DeepIV, DFIV), which increases its utility as a modular component in existing causal inference pipelines.

5. **Ablation analysis**: The loss ablation study (Figure 5c) provides useful evidence that all three constraint terms contribute to instrument recovery, supporting the multi-loss design rationale.

## Weaknesses
### W1. Lemma 1 proof gap (Major)
The proof of Lemma 1 contains a logical gap that undermines the theoretical justification for the unconfoundedness constraint. The step $\mathbb{E}[Z \cdot \mathbb{E}[e_Y|X,T]] = \mathbb{E}[Z] \cdot \mathbb{E}[e_Y|X,T]$ implicitly assumes $\mathbb{E}[Z|X,T] = \mathbb{E}[Z]$, i.e., $Z$ is independent of $(X,T)$. However, since $Z = g(X)$ is a deterministic function of $X$, this independence does not hold generally. The KL divergence loss encourages $Z$ toward a standard normal but does not guarantee conditional independence of $Z$ from $X$. This means that the covariance-based loss $\text{Cov}(Z, Y - \hat{Y})$ may not actually enforce $\text{Cov}(Z, e_Y) = 0$ as claimed. The paper should either correct the proof with explicit assumptions or reframe Lemma 1 as heuristic motivation rather than a formal result. *(See annotation on Page 1 - Lemma 1)*

### W2. Overclaimed discussion and guarantee statements (Major)
The Discussion section makes several claims that exceed what the evidence supports: 
- "Our method learns SCMs" — ZNet learns representations $C=g(X), Z=f(X)$ consistent with an SCM, but the full structural equations remain unidentified.
- "Existing methods assume $U$ does not influence $X$, while our method relaxes this assumption" — The relaxation is only partial and relies on the gap-ridden Lemma 1.
- "Solutions to the ZNet loss minimization problem will always give a representation that serves as an instrument" — This is a strong guarantee that soft-constraint minimization cannot provide. A counterexample: if $\alpha_1 \gg \alpha_2$, the unconfoundedness constraint is effectively ignored.
These overstatements reduce the paper's scientific credibility and should be corrected with precise, bounded language. *(See annotation on Page 1 - Discussion)*

### W3. Single benchmark evaluation (Major)
All experiments are derived from the IHDP dataset (985 individuals, 25 covariates). While the paper varies functional forms and confounding structures, the underlying covariate distribution is the same across all configurations. This limits the generalizability claims in the abstract and discussion (e.g., "general observational settings," "broad utility"). Results could be dataset-specific. The paper would benefit from at least one additional real-data experiment (e.g., a standard economics IV dataset) and a clear acknowledgment of this limitation. *(See annotation on Page 1 - Experiment section)*

### W4. Undefined MSE operation in loss function (Major)
Equation (7) includes an MSE term $\text{MSE}(C, Y)$, but $C$ is a vector-valued learned representation while $Y$ is a scalar outcome. Computing MSE between a vector and a scalar is not well-defined without dimensionality reduction. The paper does not specify how this computation is performed (e.g., via a linear projection layer). This ambiguity directly affects reproducibility and should be clarified in a revised version. *(See annotation on Page 1 - ZNet Loss Terms)*

### W5. Underspecified training and hyperparameter details (Major)
Critical training details are missing: (a) the hidden dimensions of the four neural networks $f, g, \pi, \Phi$ are not specified; (b) the selected loss weights $\alpha_1,...,\alpha_7$ from Bayesian optimization are not reported; (c) the frequency and configuration of gradient surgery are not documented; (d) the dimensionality of the learned $Z$ representation is mentioned as 10 for one experiment but no general selection rule is provided. These omissions make independent reproduction difficult and raise concerns about hyperparameter sensitivity in such a complex multi-loss system. *(See annotation on Page 1 - Training)*

### W6. Overclaimed "on average best" performance (Major)
The paper claims ZNet is "on average the highest performing among IV generation methods," but Table 1 shows mixed results. ZNet does not consistently outperform competitors across all settings. For example, in the Linear Latent setting under TSLS, VIV achieves better ATE error (-0.082 vs -0.125 for ZNet). Under several DeepIV configurations, AutoIV matches or beats ZNet. A more precise statement quantifying win rates and statistical significance (e.g., paired tests) would be more appropriate than the sweeping "on average" claim. *(See annotation on Page 1 - Evaluation section)*

### W7. Constraint 2 over-identifies exclusion restriction (Major)
Enforcing $\text{Cov}(C, Z) = 0$ is a sufficient but not necessary condition for the exclusion restriction. Two variables can be correlated yet still satisfy exclusion if $Z$'s only path to $Y$ is through $T$. Conversely, uncorrelated $C$ and $Z$ could still violate exclusion if $Z$ has a direct effect on $Y$. This over-identification may force the model to discard useful predictive information for $T$, weakening the learned instrument. The paper should discuss this trade-off. *(See annotation on Page 1 - Constraints 1-3)*

### W8. Additive confounding assumption not discussed as limitation (Medium)
The SCM in Equation (1) assumes additive unobserved confounding: $e_Y(U)$ and $e_T(U)$ enter without interaction with $C$ or $T$. This restrictive assumption (inherited from Hartford et al., 2017) is not tested or discussed as a limitation. In many real-world settings (e.g., healthcare data with nonlinear interactions), non-additive confounding could violate the identification result in Equation (3). *(See annotation on Page 1 - Preliminaries)*

### W9. Related work is list-like without comparison axes (Medium)
The related work section summarizes papers sequentially rather than organizing them by thematic comparison axes (e.g., assumption about $U$, supervision type, identifiability guarantee, interpretability). A comparison table would help readers quickly understand how ZNet differs from the growing set of IV learning methods. The criticism that VAE methods "lack theory to guarantee learning the true causal model" also applies partially to ZNet, which uses soft constraints rather than hard identification conditions. *(See annotation on Page 1 - Related Work)*

### W10. Abstract overclaims plug-in capability (Minor)
The abstract concludes that ZNet "can be used as a plug-in module for causal effect estimation in general observational settings, regardless of whether the (untestable) assumption of unconfoundedness is satisfied." This implies a guarantee across all settings that the experiments cannot support (single benchmark, semi-synthetic data). A more bounded claim would improve scientific objectivity. *(See annotation on Page 1 - Abstract)*

## Score
**Final Score: 5/10**

**Rationale**: The paper addresses a practically important problem (learning IV representations automatically from data) and proposes a novel constraint-based architecture that is conceptually clean. However, the score is moderated by several significant weaknesses:

- **Research value (primary dimension)**: The problem is well-motivated and the constraint-based approach is a meaningful alternative to VAE-based methods. However, a single-benchmark evaluation limits the demonstrated value breadth. (6/10)
- **Novelty**: The approach differs from existing variational methods in its use of explicit differentiable constraints, but the theoretical contribution (Lemma 1) has a proof gap that weakens its novelty claim. Without external retrieval, the precise novelty position relative to the full literature cannot be definitively assessed. (5/10)  
- **Validity and soundness**: The multi-loss approach is reasonable but the Leamma 1 gap, the underspecified MSE(C,Y) operation, and the overclaimed guarantee statements reduce confidence in the method's theoretical foundations. The empirical work is sound but limited in scope. (4/10)
- **Reproducibility**: Missing architecture details, un-reported hyperparameter values, and underspecified gradient surgery configuration make independent reproduction difficult. (4/10)
- **Presentation**: The paper is generally well-written, but the Discussion section contains overclaims that should be corrected. The related work could be better organized thematically. (6/10)

The paper has potential as a conference publication after major revisions addressing the Lemma 1 gap, adding a second real-data evaluation, calibrating claim strength, and improving reproducibility reporting.

**Novelty/Comparison Note**: External literature search was unavailable in this run (Retrieval-Disabled Mode). Novelty and positioning conclusions relative to the full body of IV learning literature should be verified manually in a revision.