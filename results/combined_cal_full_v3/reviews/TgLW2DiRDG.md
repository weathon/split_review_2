## Summary

This paper studies the connectivity graph of polyhedral complexes defined by fully-connected ReLU networks—where nodes are linear regions and edges connect regions sharing a face. The main result (Theorem 3.4) is that the average degree of this graph is at most 2d (twice the input dimension), a clean non-asymptotic bound that holds for any architecture regardless of width, depth, or total neuron count. The paper also provides a matching lower bound (Theorem 3.5), monotonicity (Theorem 3.6), convergence for shallow networks (Theorem 3.7), and diameter bounds (Theorem 3.8). Experiments on synthetic and real-world data validate the theoretical predictions.

## Strengths

1. **Theorem 3.4 (average degree ≤ 2d) is a genuine improvement over prior work.** Prior bounds (Fan et al., 2024) required no-bias or low-rank assumptions and were asymptotic; this paper proves a non-asymptotic bound that is fully general. The bound is crisp and surprising: the average degree is controlled by the input dimension alone, independent of network width, depth, or total neuron count.

2. **The proof technique is elegant and likely of independent interest.** The induction on the number of bent hyperplanes using iterative neuron removal from the last layer backward (Lemma 3.3), combined with the three-way cell categorization (Lemma 3.2), provides a clean reduction from deep to shallower problems. This is a genuine methodological contribution to analyzing ReLU complexes.

3. **The lower bound (Theorem 3.5) and monotonicity (Theorem 3.6) complement the upper bound well.** Together they characterize the average degree as lying between min(n₁, d) and 2d, with monotonic growth as neurons are added—a relatively complete picture.

4. **The synthetic experiments (Section 5.1) are well-scoped and directly validate the theory.** For small networks (up to d=5, width 16, depth 4), exhaustive enumeration confirms that average degree stays below 2d, the distribution is unimodal and right-skewed, and diameter does not grow with d. The scope is appropriately matched to computational limitations.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The Introduction overclaims the scope of the convergence result.** Claim #2 under "Theoretical Properties" (line 46) states "This average approaches the upper bound as the size of the network increases" in the same register as the fully general Theorem 3.4. However, Theorem 3.7 proves convergence to 2d only for shallow (single hidden layer) networks; for deep networks the paper states only that it "appears to approach 2d" as an empirical observation (Section 3.1, line 149). The Introduction should clearly delineate which claims are proven for all architectures versus only for shallow networks versus empirically observed.

2. **The empirical observation about data-containing regions (Section 5.2) relies on uncharacterized partial enumeration.** For CIFAR10 and California Housing, traversal was terminated after 8 million polyhedra. The sampling bias introduced by this truncation is not discussed, nor is it clear how retroactively adding data-point polyhedra to the 8-million set affects the distributional comparisons.

### Trivial

3. **Table 1 does not report total neuron count n**, on which the lower bound (Theorem 3.5) and the diameter bound depend—only width and depth are given.

4. **The diameter estimation method** (Magnien et al., 2009) is cited but the estimation error or precision of the upper/lower bounds used to compute midpoints is not described.

## Nice-to-Haves

- Discuss the computational complexity of Algorithm 1 (O(N_d · n · LP_cost)) to clarify its scalability limitations for practitioners.
- Add a brief remark reconciling the diameter lower bound Ω(ln(N_d)/ln(n)) with the experimental observation of near-d-independence for d=2–5; the bounds are ~1.2–3.7 while observed diameters are 5–76, so no conflict exists, but a note would preempt confusion.

## Removed Points

- **Harsh Critic's Critical Issue 1 (diameter bound O(m^ℓ) is loose, trivial bound exists)**: REMOVED. The critic claimed a trivial bound of n (total neurons) from Hamming distance in the sign-sequence representation. This is incorrect because the connectivity graph is an *induced subgraph* of the hypercube on valid d-cells; intermediate Hamming-path vertices may not correspond to valid d-cells, so the claimed trivial bound is not guaranteed. The paper's O(m^ℓ) bound is non-trivial and its d-independence is genuinely interesting even if the bound is loose.
- **Critic's concern about experiments using hidden representations rather than the input**: REMOVED. The subnetwork formed by the last few layers is itself a ReLU network, so the theory applies directly with the appropriate input dimension (5 for MNIST, 10 for CIFAR10).
- **Critic's concern about bounded/unbounded confounding not controlled for**: The paper explicitly discusses this relationship (Figure 7 and accompanying text) and does not claim to control for it; it reports the observation transparently.
- **Critic's concern about proof induction step depending on h_i**: This comments on detail deferred to Appendix B (which exists in the submitted paper). The proof sketch provided is reasonable.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. In the Introduction's contribution list, mark theoretical claims that are proven for all architectures, proven only for shallow networks, or empirically observed.
2. Characterize the potential sampling bias from the 8-million-polyhedron truncation in Section 5.2.
3. Add total neuron count n to Table 1.

## Score and Decision

**Calibration**: Round 1 bracketed the paper in the 5.5–7.5 range. Round 2 compared against anchors averaging 5.80 (IQdlPvj4dX, "On the Local Complexity of Linear Regions") and 5.67 (sq5gkjC9jv, "Topological Expressive Power"), both of which have structural weaknesses (bound tightness doubts, practical relevance gaps) that this paper does not share, as well as the 7.25 anchor (vVCHWVBsLH, "Decomposition Polyhedra") which is technically deeper but less directly impactful. The paper's core strengths (favorability 8.97–10.03) are well above the 5.80-anchor's strength profile, and its weaknesses (favorability 2.23–5.90) are trivial-to-minor presentation issues rather than structural flaws. The paper sits between the 5.80 and 7.25 anchors.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>