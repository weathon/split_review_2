## Summary

This paper studies the Kernel Density Estimation (KDE) problem for the Gaussian kernel and proposes a data structure that leverages asymmetric Locality Sensitive Hashing (LSH) to achieve a tradeoff between query time and space. The main result is a data structure with expected query time roughly \(1/\mu^{0.05}\) and space \(1/\mu^{4.15}\), improving the previous best query exponent of 0.173 (data-dependent) and 0.25 (data-independent). The paper also gives a version with linear space (\(1/\mu\)) and query exponent 0.1865, which improves on the prior data-independent bound and nearly matches the data-dependent bound with a simpler analysis. More generally, the authors present the first time-space tradeoff curve for KDE, parameterized by a space exponent \(\delta\).

## Strengths

- **Novel application of asymmetric LSH to KDE.** The paper shows, for the first time, that asymmetric LSH (Andoni et al., 2017) can be used to break the symmetric LSH bottleneck in the KDE framework of Charikar et al. (2020). This is a clever and non-trivial extension that yields improved query exponents.
- **Formal tradeoff analysis.** The paper provides a clean optimization-based framework that characterizes the query exponent \(\xi(\delta,x)\) for each distance scale and derives the overall KDE query exponent \(\xi(\delta)\) as a function of the space exponent \(1+\delta\). This tradeoff is new to the KDE literature.
- **Concrete numerical results.** The paper reports specific query exponents (0.05 and 0.1865) backed by numerical evaluation of the optimization. The plots in Figure 1 clearly illustrate the behavior and the plateau, helping the reader understand the limits.
- **Clear and well-structured exposition.** The technical overview (Section 1.2) is particularly helpful: it explains the source of improvement and why constant query time is not possible with current ANN technology. The paper is accessible to readers familiar with LSH and KDE.

## Weaknesses

### Fatal
None.

### Major
- **High space requirement for the best query time.** The \(1/\mu^{4.15}\) space exponent is very large; for typical \(\mu = n^{-\Theta(1)}\), this would be prohibitive in practice. While the paper acknowledges this, the linear space version gives only a modest improvement (0.1865 vs 0.25) over the prior data-independent bound and is slightly worse than the data-dependent bound (0.173) of Charikar et al. (2020). The practical impact of the tradeoff regime is therefore limited.
- **Dependence on numerical optimization without analytical closed forms.** The query exponent \(\xi(\delta)\) is defined through a min-max optimization (Equation 10) that is solved numerically. While this is acceptable for a theoretical paper, it makes the results less transparent and harder to verify exactly. The paper does not provide bounds that are analytically tight, which would strengthen the contribution.
- **The “constant query not possible” argument is heuristic.** Section 1.2 gives an intuitive high-level explanation for why constant query time is not achievable, but this is not a rigorous lower bound. The paper does not prove that the plateau near 0.05 is inherent; it only shows that their specific construction cannot go below it. A formal lower bound or a more complete characterization would be valuable.

### Minor
- **Assumptions on parameters.** The paper uses standard but strong assumptions (e.g., \(\mu^* = n^{-\Theta(1)}\), \(d = \tilde{O}(1)\)). While these are typical in the literature, they restrict the generality of the results. For instance, when \(\mu\) is very small the exponents matter most, but the polynomial in \(d\) and \(\log n\) factors dominate asymptotic notation.
- **The improvement for linear space is incremental.** The query exponent moves from 0.25 to 0.1865, which is a noticeable but not dramatic improvement. Moreover, the data-dependent scheme of Charikar et al. (2020) achieved 0.173 with linear space and a more complex analysis; the paper’s claim of “nearly matching” is accurate but the gap is small.
- **Missing discussion of practical scalability.** The paper does not compare to other high-dimensional KDE methods such as discrepancy-based approaches (Phillips & Tai, 2020; Charikar et al., 2024) that achieve \(1/\epsilon\) instead of \(1/\epsilon^2\). The focus is entirely on the dependence on \(1/\mu\), but the \(\epsilon\) dependence could matter in practice.

### Trivial
- Some notation is overloaded (e.g., \(\mu\) used both as baseline approximation and exponent base), but this is clarified in the text.

## Nice-to-Haves
- A more detailed explanation of why the tradeoff plateau occurs, possibly with a closed-form lower bound for the achievable query exponent under the ANN constraint.
- A discussion of whether the asymmetric LSH construction could be combined with data-dependent techniques to achieve even better tradeoffs.
- A comparison with the reduction to ANN and note that the analysis yields exact recovery, not just approximate near neighbor retrieval.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the bottleneck in KDE via ANN arises from intermediate distance scales, not just the near and far ends. The asymmetric LSH framework naturally allows shifting the computational burden between space and query time at different scales, leading to a non-trivial optimization problem whose solution reveals a plateau. This suggests that further improvements may require fundamentally new ANN constructions or different KDE reduction strategies.

## Suggestions
- Provide a tighter analytical bound (or a more rigorous numerical verification) for the main query exponent 0.05, perhaps by showing that the optimization is convex and the stationary point is captured.
- Consider adding a small table summarizing the exponents for key prior works and the new results, to make the improvement clearer.
- Clarify how the reduction to ANN on the sphere (Lemma 8) interacts with the subsampling step; a concrete example or diagram would help.

## Score and Decision

**Score:** 8  
**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>