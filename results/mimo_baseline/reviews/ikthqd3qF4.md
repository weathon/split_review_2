## Summary

This paper develops a methodological framework for evaluating unsupervised anonymous record linkage algorithms without labeled training data. The key insight is that structural constraints—such as each person originating at most one first-lien mortgage—allow the derivation of observable lower bounds on precision and relative recall by examining the rate at which predicted clusters contain multiple originations. The authors apply this framework using hierarchical agglomerative clustering on 65.5 million HMDA mortgage applications, achieving an estimated 92.3% precision in identifying cross-applicants.

## Strengths

- **Novel theoretical contribution with broad applicability.** The derivation of observable precision/recall bounds using structural constraints (Theorem 1 and its corollaries) is elegant and genuinely novel. The observation that multiple originations in a cluster serve as a sufficient statistic for bounding false positive rates is a clean and useful insight. The framework is both domain-agnostic and method-agnostic—it applies to any label-generating algorithm as long as the structural constraint holds.

- **Well-validated simulation study.** The simulation closely mirrors the real data structure and demonstrates that the theoretical lower bound closely tracks actual precision (Figures 3a vs. 4a), providing strong evidence that the bounds are tight in practice. The comparison between "with date" and "without date" specifications clearly shows how additional covariates improve clustering quality.

- **Substantial empirical application.** The application to 65.5 million HMDA mortgage applications demonstrates real-world scale and utility. The precision-sample-size frontier (Figure 5) provides a principled way to select tuning parameters, and the identified cross-applicants enable concrete downstream applications (fairness measurement, lending standard monitoring, shopping behavior analysis).

- **Clear and well-structured exposition.** The paper explains the methodology incrementally—intuitive examples, formal definitions, theorem statements, and practical implementation—making it accessible to a broad audience.

## Weaknesses

### Fatal
None.

### Major

- **Restriction to size-2 clusters discards potentially valuable signal.** Footnote 4 states that all clusters with more than two applications are dropped. This is a significant choice that limits recall and may exclude many genuine cross-applicants who submit 3+ applications. The paper does not quantify how much data is lost through this restriction or discuss how the theoretical bounds would extend to larger clusters (where the assumption P[Mult|False] = p² becomes less defensible). This seems like an important limitation that deserves more explicit treatment.

- **Limited discussion of Assumption 1's robustness.** The independence assumption (origination decisions are independent across borrowers) could be violated in practice due to correlated economic shocks, shared lenders, or regional market conditions. The paper does not explore sensitivity to violations of this assumption, either theoretically or empirically. Even a brief analysis of how correlated origination decisions would affect the bound's tightness would strengthen the paper.

### Minor

- **No ground-truth validation on real data.** While the simulation provides convincing validation, there is no attempt to validate the method against any ground-truth in the real mortgage data (e.g., using a small hand-labeled sample or an alternative dataset with identifiers). The Appendix diagnostics mentioned on page 8 could be more prominently discussed in the main text.

- **Distance function normalization is underspecified.** The paper considers 96 combinations of distance functions and tolerance parameters but does not clearly explain how the five continuous variables (date, income, loan size, FICO, LTV) are normalized or weighted. Since these variables have very different scales and units, normalization choices can substantially affect clustering outcomes. This should be more explicit.

### Trivial
None.

## Nice-to-Haves

- A brief analysis of how the method performs on clusters of size 3+ would be valuable, even if the paper's preferred specification restricts to size-2 clusters.
- Comparison with alternative unsupervised record linkage methods (e.g., probabilistic record linkage à la Fellegi-Sunter) would contextualize the clustering approach within the broader literature.
- Discussion of how the bounds degrade as the structural constraint becomes probabilistic rather than deterministic (e.g., if some individuals can originate multiple loans through refinancing).

## Novel Insights

The paper's most novel insight is that structural constraints present in many real-world datasets (one origination per person per property) create an observable test statistic—multiple originations in a predicted cluster—that enables principled evaluation of unsupervised classification without labels. This transforms an inherently unverifiable problem into one with computable performance guarantees. The observation that this framework is simultaneously domain-agnostic (any setting with structural constraints) and method-agnostic (any label-generating algorithm) makes it a broadly useful tool for the research community.

## Suggestions

- Provide more detail on variable normalization in the distance function, as this is critical for reproducibility and for understanding which specifications dominate.
- Discuss the sensitivity of Theorem 1's bound to violations of the independence assumption, even qualitatively.
- Expand the discussion of the size-2 cluster restriction to quantify its cost in terms of recall and to discuss how the theoretical framework would need to be modified for larger clusters.

## Score and Decision

The paper presents a genuinely novel and practically useful contribution: observable bounds on precision and recall for unsupervised record linkage using structural constraints. The theoretical framework is clean, well-motivated, and broadly applicable. The simulation validates the approach convincingly, and the empirical application at scale demonstrates real utility. The major weaknesses—restriction to size-2 clusters and limited robustness analysis—are meaningful but do not invalidate the core contribution. For an ICLR audience, the domain-agnostic nature of the evaluation framework and the methodological novelty around unsupervised evaluation without labels are the primary contributions, and they are solid.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept