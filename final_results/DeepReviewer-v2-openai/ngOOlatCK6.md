## Summary
# Final Review Report

## Summary

This paper studies the **conditional causal bandit problem**, where a decision-maker chooses single-node conditional interventions (do(X = g(Z_X))) on a known causal graph to maximize an expected reward variable Y. The authors' core theoretical contribution is a graphical characterization of the **minimal globally interventionally superior set (mGISS)** — the smallest set of nodes guaranteed to contain the node with the optimal conditional intervention, regardless of the specific structural equations. They prove that the mGISS equals the LSCA (Lowest Strict Common Ancestor) closure of the parents of Y, and they provide the **C4 algorithm** that computes this closure in O(|V|+|E|) time.

A key theoretical insight is Proposition 4, which shows that conditional-intervention superiority coincides with deterministic atomic-intervention superiority, allowing the analysis to be reduced to a simpler deterministic setting. Empirical results on random DAGs and real-world Bayesian networks (bnlearn repository) show that C4 can prune 60–90% of the search space for large sparse graphs. When integrated with a UCB-based conditional bandit algorithm (CondIntUCB), mGISS pruning yields lower cumulative regret compared to brute-force search over all nodes.

The paper is well-structured, the theoretical development is rigorous (proofs deferred to appendix), and the C4 algorithm is elegantly simple. However, the experimental evaluation has several methodological limitations: no comparison against a baseline with equal arm-count reduction, potential circularity in optimal-arm estimation for regret computation, selection bias in target node choice, and lack of variance reporting for random-graph experiments. Additionally, the novelty claims cannot be independently verified in this run due to disabled external retrieval. The assumption of no latent confounders, while acknowledged as a limitation, significantly bounds the applicability of the results.

## Strengths
1. **Novel problem formulation.** The conditional causal bandit problem is a meaningful extension of standard causal bandits that bridges the gap between causal inference and contextual decision-making. The formulation captures realistic settings (e.g., personalized treatment, dynamic pricing) where intervention values depend on observed context.

2. **Clean theoretical reduction.** Proposition 4 (equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority) is a clever insight that simplifies the analysis considerably. By reducing the probabilistic conditional case to a deterministic atomic case, the paper makes the graphical characterization more tractable and the proofs more transparent.

3. **Elegant graphical characterization.** The LSCA closure and its equivalence to the mGISS (Theorem 13) provide a complete, checkable condition for node optimality. The Λ-structure characterization (Theorem 12) is intuitive and well-illustrated through the running examples in Figure 1.

4. **Simple, linear-time algorithm.** The C4 algorithm (Algorithm 1) is remarkably simple—a single reverse-topological pass with connector propagation. Its O(|V|+|E|) complexity ensures scalability to large causal graphs, which is essential for practical deployment.

5. **Strong pruning results on real-world graphs.** The empirical results on bnlearn networks demonstrate that C4 can reduce the search space by 60–90% for large models, with better performance on sparser graphs (which are common in real-world causal models). This practical effectiveness is arguably the paper's strongest empirical finding.

6. **Reproducibility consideration.** The paper provides a code repository and references to standard benchmark datasets (bnlearn), making the empirical results verifiable.

## Weaknesses
### W1. Experimental evaluation lacks a baseline controlling for arm-count reduction (Major)
The regret experiment (Section 6, CondIntUCB) compares mGISS pruning against brute-force search over all nodes. This is not a fair comparison because any reduction in the number of arms will trivially reduce regret (fewer arms to explore). The appropriate baseline would be a **random subset of nodes of the same size as the mGISS** (or a heuristic alternative such as parents of Y plus a random ancestor). Without this control, it is impossible to tell whether mGISS selects the *right* nodes or whether the observed improvement is simply due to a smaller arm set. 

**Impact:** Undermines the central practical claim that C4 "substantially accelerates convergence rates." The improvement could be an artifact of reduced arm count rather than a property of the mGISS selection.

**Required fix:** Add experiments comparing mGISS against (a) a random subset of |mGISS| nodes from An(Y)\{Y\}, and (b) a heuristic baseline (e.g., Pa(Y) plus their ancestors one step up). Show that mGISS yields statistically significantly lower regret.

### W2. Regret computation uses an estimated (potentially circular) optimal arm (Major)
Footnote 11 states that the optimal arm for regret computation is "the arm that most runs concluded to be the best at the end of training." This creates a **circular dependency**: the benchmark is derived from the same algorithm being evaluated. If the algorithm converges to a suboptimal arm, the "estimated best arm" will also be suboptimal, understating the true regret. Standard practice is to use either (a) the true optimal intervention (which could be computed by exhaustive enumeration in a synthetic SCM) or (b) the best arm identified by a substantially longer run.

**Impact:** The absolute regret values in Figure 3 are not interpretable, and the relative improvement between mGISS and brute-force is potentially biased because both conditions use the same estimated optimal arm.

**Required fix:** For the bnlearn-based experiments, generate synthetic SCMs with known structural equations and compute the true optimal intervention by enumeration. Alternatively, run the brute-force condition for a much longer horizon and use its final recommendation as the reference.

### W3. Target-node selection bias in pruning experiments (Major)
Both random-graph and real-world experiments select Y as "the node with the most ancestors." This is a favorable case—nodes with many ancestors have more opportunities for Λ-structures and thus more aggressive pruning. For nodes with few ancestors, the mGISS may be close to the full ancestor set, yielding minimal benefit. The paper does not report pruning rates for other nodes.

**Impact:** The paper overstates the typical pruning benefit. A practitioner applying C4 to an arbitrary target node may see much less than the advertised 90% reduction.

**Required fix:** Report the distribution of |mGISS|/|An(Y)\{Y\}| across all nodes for 2–3 representative graphs. Include median and interquartile range.

### W4. Missing variance reporting in random-graph experiments (Minor)
The random-graph experiment reports only point estimates ("17%, 29%, 62% and 77%") for mean retention fractions aggregated over 1000 graphs per configuration. No standard deviations, confidence intervals, or percentile ranges are provided. Given that Erdős-Rényi graphs with the same expected degree can have widely varying structures, the variance across runs matters for assessing the reliability of the findings.

**Impact:** Limits the statistical interpretability of the results. The reader cannot judge whether the differences between degree settings are significant.

**Required fix:** Add error bars (standard deviation or 10/90 percentiles) to the bar plot in Figure 5 (Appendix H), or include a table with mean ± std.

### W5. Novelty positioning relies on unverifiable first-claim (Unresolved — deferred)
The paper claims "This is the first time the minimal search space for a causal bandits problem with non-hard interventions is fully characterized." Due to disabled external retrieval in this review run, this claim cannot be independently verified against the literature. The paper's own related-work section cites several lines of work (Sen et al., 2017; Yabe et al., 2018; Lu et al., 2020; Lee & Bareinboim, 2018, 2019, 2020) that address overlapping settings. 

**Impact:** If a reviewer identifies prior work that partially characterizes the search space for soft or conditional interventions, the novelty claim would need to be substantially narrowed.

**Required fix:** Add qualifying language: "To our knowledge, this is the first complete graphical characterization..." and explicitly discuss the closest prior works on soft-intervention causal bandits, explaining why their results do not directly imply the mGISS characterization. This verification is deferred to the authors' revision phase.

### W6. Latent confounder assumption limits applicability (Major)
The paper assumes **no latent confounders**, which is acknowledged as a limitation. However, in many real-world causal bandit applications (e.g., epidemiology, gene networks), unobserved confounding is the norm rather than the exception. The assumption is used to justify the observability of all ancestors (An(X)\{X\} ⊆ Z_X), which is central to the Λ-structure analysis. Without this assumption, the mGISS characterization may not hold.

**Impact:** The practical applicability of the results is significantly narrower than the paper's motivational examples might suggest. The mGISS provides no guarantee when latent confounders are present.

**Required fix:** The paper already acknowledges this limitation. Strengthen the discussion by adding a brief sketch of how latent confounding would affect the characterization: e.g., "Under latent confounding, the conditioning sets Z_X may not include all ancestors of X, breaking the observable-conditioning-set assumption. The Λ-structure criterion would need to be augmented to account for unobserved common causes, potentially requiring the mGISS to include additional nodes."

### W7. Missing discussion of Z_X specification (Minor)
The paper assumes "conditioning sets Z_X are specified in advance" but provides no guidance on how a practitioner should choose them. The only constraint is An(X)\{X\} ⊆ Z_X ⊆ V\De(X), which leaves significant freedom. The choice of Z_X affects both the policy class and, potentially, the mGISS (since Z_X appears in the definition of conditional-intervention superiority). 

**Impact:** A practitioner using C4 may not know which Z_X to use, and the choice may affect whether the mGISS guarantee applies.

**Required fix:** Add a remark clarifying that the mGISS characterization is valid for any Z_X satisfying the observable-conditioning-set assumption. Also note that if Z_X is chosen to be minimal (An(X)\{X\}), the policy class is most restricted, which may affect optimality but does not change the mGISS.

## Score
**Final Score: 6/10**

**Rationale:** The paper's primary contribution is theoretical—a clean graphical characterization of the minimal search space for conditional causal bandits, accompanied by a linear-time algorithm. This theoretical work is rigorous and well-presented. However, the score is constrained by three factors. First, the experimental evaluation has significant methodological weaknesses (lack of proper baselines controlling for arm-count reduction, circular optimal-arm estimation, target-node selection bias) that prevent the empirical claims from being fully trusted. Second, the paper's applicability is substantially limited by the no-latent-confounders assumption, which restricts the practical relevance for many real-world settings. Third, the novelty claim ("first characterization") cannot be independently verified in this review due to disabled external retrieval. The paper would benefit from a revised experimental methodology and a more measured presentation of empirical results. With these improvements, the research value could increase substantially, as the theoretical framework is solid and addresses a genuine gap in the literature.