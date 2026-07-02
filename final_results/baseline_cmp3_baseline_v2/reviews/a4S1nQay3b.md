## Summary
This paper tackles noisy correspondence (NC) in multi-view clustering, identifying two harmful types: category-level mismatch (same-class samples treated as negatives) and sample-level mismatch (misaligned or missing cross-view pairs). The authors propose **CorreGen**, a generative framework that formulates correspondence learning as maximum likelihood estimation over latent correspondences, solved via an Expectation-Maximization algorithm. In the E-step, they infer soft correspondence distributions using GMM-guided marginals and optimal transport with virtual samples to handle noise; in the M-step, they update the encoder by maximizing expected log-likelihood. Experiments on four datasets with synthetic and real-world noise show consistent improvements over seven baselines.

## Strengths
- **Principled generative formulation**: Shifting from discriminative contrastive objectives to a generative MLE framework for noisy correspondence is novel and well-motivated. The EM approach elegantly handles both category-level and sample-level mismatches without relying on pre-defined positive/negative pairs.
- **Theoretical contribution**: The proof that standard InfoNCE is a special case of the proposed objective (Proposition 2) provides a clean connection to existing methods and anchors the work in the broader contrastive learning literature.
- **Effective technical design**: The E-step solution combining GMM-guided marginals (which naturally down-weight noisy/unalignable samples) with optimal transport augmented by virtual samples is principled and addresses both types of noise simultaneously. The visualization in Figure 3 convincingly shows progressive recovery of class-level correspondences.
- **Strong empirical results**: The method achieves consistent improvements across all four datasets and noise levels, including substantial gains on the real-world noisy UMPC-Food101 dataset (e.g., +13.6 ACC at 0% MR, +15.4 ACC at 80% MR over the best baseline). The degradation under high noise is graceful, demonstrating robustness.
- **Clear problem formalization**: Definitions 1 and 2 clearly distinguish category-level and sample-level mismatches, which helps situate the work and justifies the need for a generative approach.

## Weaknesses
### Fatal
None.

### Major
1. **Estimation of the noise ratio ρ**: The method introduces a virtual sample with marginal mass ρ to absorb unalignable samples. The paper does not explain how ρ is set in practice—especially on real-world datasets like UMPC-Food101 where the true noise ratio is unknown. The sensitivity analysis (referenced in Appendix E) is not provided, and without guidance on choosing ρ, the method’s practical applicability is unclear. If ρ is tuned per dataset, it becomes a significant hyperparameter that limits ease of use.

2. **GMM-guided marginal estimation has several free parameters**: The formula in Eq. (13)–(14) introduces non-standard shaping parameters ε and m, plus the momentum update. The motivation for the specific shaping function is not well justified, and it is unclear how sensitive results are to these choices. Given that the GMM itself is fitted to potentially noisy embeddings early in training, the reliability of these marginals is questionable—yet this step is central to the E-step.

3. **Mini-batch versus full-dataset optimal transport**: The paper does not specify whether the OT problem is solved over the full dataset or within mini-batches. For large datasets, full OT would be prohibitively expensive. If mini-batches are used, the marginal constraints become local approximations, which could distort the estimated posterior. This practical consideration is not discussed.

### Minor
- The claimed “10% accuracy improvements” is actually an understatement (e.g., UMPC-Food101 improvement at 0% MR is 13.57 points absolute). The claim is conservative, which is fine, but it could be more precise.
- Table 1 has duplicate “Ours” rows with different formatting—likely a formatting artifact, but it is confusing.
- The GMM is fitted per view. The paper does not discuss whether the same number of Gaussian components is used as the number of clusters, or whether this is treated as a hyperparameter.

### Trivial
- In Table 2, one baseline is misspelled as “GCFAGg” while in Table 1 it is “GCFAGG”.
- Figure 2 is described in the caption but the text references it only briefly; the figure itself is somewhat dense and could benefit from a cleaner layout in the actual submission.

## Nice-to-Haves
- An ablation study isolating the effect of the virtual sample (ρ) and the GMM-guided marginals would strengthen the paper.
- A discussion on how to set ρ automatically (e.g., by estimating the corruption rate from data) would improve practical utility.
- The sensitivity of the method to the number of GMM components and the regularization parameter λ would be informative.

## Novel Insights
Beyond the paper’s own contributions, a notable insight is that contrastive InfoNCE implicitly assumes uniform marginals and one-to-one instance-level correspondence. When these assumptions are violated (as they are under noisy correspondence), the generative EM framework that relaxes them is a natural generalization. This perspective unifies several lines of work—contrastive learning, optimal transport, and mixture models—under a single probabilistic objective.

## Suggestions
- Include a practical heuristic or a simple validation-based method for estimating ρ, or at least discuss how sensitive results are to this choice (even if briefly in the main paper).
- Clarify whether the OT problem is solved on mini-batches or the full dataset, and if on mini-batches, discuss the effect on marginal consistency.
- Provide standard deviations for the reported means across the five runs to allow statistical significance assessment.

## Score and Decision
The paper presents a novel generative framework for a practically important problem (noisy correspondence in multi-view clustering). The EM derivation is sound, the E-step design is technically creative, and the experimental results consistently demonstrate strong improvements. The main concerns—estimation of the noise ratio and sensitivity to several hyperparameters—do not invalidate the core contribution but should be addressed to strengthen the paper. The work is a meaningful advance over existing discriminative approaches and will be of interest to the ICLR community.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>