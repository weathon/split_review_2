## Summary

This paper proposes a method for evaluating unsupervised anonymous record linkage without requiring labeled training data. The authors derive observable lower bounds on precision and relative recall by exploiting a structural constraint that limits how many positive outcomes a single individual can have (e.g., one first-lien mortgage per person). They demonstrate the method on HMDA mortgage data using hierarchical clustering to detect "cross-applicants" (individuals submitting multiple applications), achieving an estimated 92.3% precision at their preferred specification.

## Strengths

- **Novel theoretical contribution**: The derivation of observable lower bounds on precision and recall without labeled data is genuinely novel and practically valuable. The key insight—that the rate of multiple originations within clusters provides an upper bound on false positives—is clever and well-justified theoretically.

- **Practical relevance**: The mortgage application setting is a high-impact domain where person-level identifiers are unavailable due to privacy constraints. The ability to detect cross-applicants with quantifiable precision guarantees has direct applications for fairness measurement, lending standard monitoring, and consumer behavior research.

- **Method-agnostic framework**: The bounds depend only on predicted labels, making them applicable to any algorithm that generates such labels. This enables principled hyperparameter tuning and cross-model comparisons without ground truth, which is a significant practical advantage.

- **Clear exposition of the core idea**: The paper does a good job explaining the intuition behind the bounds (e.g., the simplified two-application case) and illustrating the trade-off between precision and sample size through figures.

## Weaknesses

### Major

- **Assumption 1 (independence of origination decisions across borrowers) is strong and likely violated in practice**: Mortgage origination decisions are correlated across borrowers due to common macroeconomic factors (interest rates, housing market conditions), lender-specific policies, and geographic clustering. While the authors acknowledge this assumption, they do not discuss how violations would affect the bounds. If origination decisions are positively correlated (e.g., during a housing boom), the bound could be overly optimistic (i.e., the true precision could be lower than the bound suggests).

- **The bound relies on estimating p (unconditional origination probability) from the data, but this estimate may be biased**: The empirical origination rate in the dataset reflects the observed sample, not the true population rate. If the clustering algorithm systematically selects certain types of applications (e.g., those with higher origination probabilities), the bound could be misleading. The paper does not address this potential selection bias.

- **Limited validation of the core theoretical claim**: The simulation provides some evidence that the bound works, but the simulation is relatively simple (one million census tracts with a specific distribution). The paper would benefit from more extensive simulations that test the robustness of the bounds under various violations of Assumptions 1 and 2, different cluster sizes, and different correlation structures.

- **The 92.3% precision claim is an estimate, not a guarantee**: The paper states "we successfully identify cross-applicants with an estimated 92.3% precision," but this is a lower bound estimate, not a validated precision. The bound could be loose, and the actual precision could be lower. The paper should be more careful about how it frames this result.

### Minor

- **The paper focuses exclusively on clusters of size two**: The authors note they drop all clusters with more than two applications. This is a significant restriction that limits the applicability of the method. Many real-world cross-applicants may submit more than two applications, and the theoretical bounds would need to be extended to handle larger clusters.

- **The choice of categorical variables for partitioning is somewhat arbitrary**: The paper uses nine categorical variables (census tract, property type, occupancy, etc.) to create partitions. While the authors acknowledge this is application-specific, they do not provide guidance on how to select these variables or what happens if a variable is incorrectly assumed to be constant across an individual's applications.

- **The computational complexity of O(ℓ²) may still be prohibitive for very large datasets**: While the paper uses an efficient algorithm, the largest partition size ℓ could still be large in practice. The paper does not discuss computational bottlenecks or provide runtime statistics for the HMDA application (65.5 million applications).

### Trivial

- The paper uses "cross-applicants" to refer to individuals who submit multiple applications, but this term is not standard in the mortgage literature. "Multiple applicants" or "serial applicants" might be more descriptive.

## Nice-to-Haves

- A sensitivity analysis showing how the bounds change under different assumptions about the correlation structure of origination decisions would strengthen the paper.
- A comparison with alternative approaches (e.g., using credit bureau data or other external validation) would provide additional confidence in the method.
- Discussion of how to handle clusters of size greater than two, perhaps with a generalization of the theoretical bounds.

## Novel Insights

The paper's core insight—that structural constraints on positive outcomes (e.g., one mortgage per person) can be exploited to derive observable performance bounds for unsupervised record linkage—is genuinely novel and has broad applicability beyond mortgages. The idea that the rate of "impossible" outcomes (multiple originations in a cluster) provides an upper bound on false positives is elegant and practically useful. This insight could be applied to any domain where individuals can have at most one positive outcome, including insurance, education, and employment settings.

## Suggestions

- Provide a more thorough discussion of how violations of Assumption 1 (independence) would affect the bounds, and consider deriving bounds that are robust to positive correlation.
- Validate the method on a dataset where ground truth labels are available (e.g., a synthetic dataset with known cross-applicants) to directly measure the tightness of the bounds.
- Extend the theoretical analysis to handle clusters of arbitrary size, not just pairs.
- Include runtime statistics and discuss scalability to datasets with millions of observations.

## Score and Decision

The paper makes a novel theoretical contribution with clear practical relevance. The core idea is clever and well-executed. However, the strong independence assumption and the lack of validation on data with ground truth labels are significant concerns. The paper would benefit from addressing these issues before acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>