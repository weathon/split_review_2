## Summary

This paper formalizes the problem of assessing dataset reliability without ground truth access, where auxiliary observations from an unknown statistical experiment are available. The authors propose the Gram determinant score—measuring the volume of the parallelepiped spanned by joint distribution vectors of reported data and observations—and show it preserves several ground-truth-based reliability orderings (exact match, Blackwell dominant, and approximate Hamming/dist) under near-tight conditions, while being experiment-agnostic and unique up to scaling.

## Strengths

- **Elegant theoretical framework with near-tight impossibility results.** The paper establishes impossibility results (Proposition 3.1) showing that no score can preserve reliability orderings under broad conditions (e.g., Q_dom for Hamming ordering), and then shows the Gram determinant score works under Q_{L,δ} with δ ≤ 1/64L²d², which is close to the boundary. The key algebraic insight—det(Q^T P^T P Q) = det(P^T P) det(Q)²—cleanly decouples the experiment from the misreport matrix.

- **Experiment agnosticism and uniqueness.** Proposition 4.3 shows the Gram determinant score is the unique (up to scaling) experiment-agnostic reliability score under mild coherence assumptions. This is a strong characterization result that justifies the specific choice of score function.

- **Well-motivated problem with practical relevance.** The paper clearly motivates the problem with real-world examples (insurance, financial regulation, COVID data) and provides a clean formalization with multiple natural reliability orderings (exact match, Blackwell, Hamming/dist) that form a refinement chain (Proposition 2.1).

- **Diverse experimental validation.** Experiments span synthetic categorical data with six corruption policies, CIFAR-10 image embeddings using the kernelized variant, and real BLS employment data with naturally occurring revisions, demonstrating the score's effectiveness across different domains and observation types.

## Weaknesses

### Fatal

None.

### Major

- **No baseline comparisons.** The paper does not compare the Gram determinant score against any alternative approaches to data quality assessment (e.g., mutual information estimators, correlation-based measures, or other general-purpose dependency scores mentioned in the related work). Without baselines, it is difficult to assess the practical added value of the proposed method, even if the theoretical properties are unique.

- **Significant gap between impossibility and sufficient conditions for Hamming ordering.** The impossibility result holds for Q_dom (diagonally dominant), but the sufficient condition requires Q_{L,δ} with δ ≤ 1/64L²d², meaning the Hamming error must be very small relative to d². The paper does not empirically explore or discuss when this condition is violated in practice, leaving open how robust the method is in higher-noise regimes.

- **Limited scalability discussion.** The method requires |Y| ≥ d for the experiment to be linearly independent (P_indep). The experiments use d=5 (synthetic) and d=10 (CIFAR-10), which are small label spaces. For problems with large label sets, the d×d Gram matrix computation and determinant become expensive, and the requirement for linearly independent experiments becomes harder to satisfy. The paper acknowledges this in the conclusion but provides no concrete analysis or experiments.

### Minor

- **Employment data experiment is underdeveloped.** The claim that "revisions substantially improve reliability" is somewhat expected and could be seen as a sanity check rather than a rigorous validation. The experiment uses only N=209 data points with 4 quantile buckets, and the interpretation relies on the assumption that tax withholding data is a faithful proxy for true employment—this assumption is not validated.

- **The kernel extension's theoretical guarantees are entirely in the appendix.** The kernelized variant is essential for the CIFAR-10 experiment (the paper's most compelling real-data demonstration), yet the analogous ordering result (Theorem 4.2 for kernels) is stated only as existing in Appendix F without any summary of the conditions or proof sketch in the main text.

- **Single-source assumption.** The model assumes a single data source (one agent), which limits applicability to settings with multiple reporters. The paper does not discuss how to extend the framework to multiple sources or how the score behaves when data comes from heterogeneous sources.

### Trivial

None.

## Nice-to-Haves

- A comparison against at least one baseline (e.g., a mutual information estimator or a simple correlation-based score) to contextualize the practical gains.
- Experiments exploring the method's behavior as corruption rates approach or exceed the theoretical threshold δ ≤ 1/64L²d².
- A brief discussion or experiment on scalability to larger label spaces (e.g., d=100 or d=1000).

## Novel Insights

The experiment agnosticism property (Proposition 4.3) is a genuinely novel contribution: the idea that a reliability score should produce the same ranking of datasets regardless of the unknown experiment, and that the Gram determinant is the unique such score (up to scaling), provides a strong axiomatic justification. The geometric interpretation—reliability as volume of the parallelepiped spanned by joint distribution columns—is also a fresh perspective that connects data quality to a well-understood algebraic quantity. The near-tight impossibility results (Section 3) are valuable in delineating the fundamental limits of reliability scoring, a problem that has not been formally studied before.

## Suggestions

- Add at least one baseline comparison (e.g., a mutual information or correlation-based score) in the experiments to demonstrate the practical advantage of the Gram determinant score.
- Include a brief proof sketch or key conditions for the kernelized ordering result (Theorem 4.2 analogue) in the main text, since the kernel variant is central to the CIFAR-10 experiments.
- Discuss or experimentally evaluate the method's behavior when the linearly independent condition is approximately rather than exactly satisfied (e.g., near-singular P).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept