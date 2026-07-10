Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper introduces the problem of single-node conditional-intervention causal bandits and provides a theoretical characterization of the minimal set of nodes (mGISS) guaranteed to contain the optimal intervention node. The authors prove that the mGISS equals the LSCA closure of the parents of the target variable Y, establish an elegant equivalence (Proposition 4) between conditional-intervention superiority and deterministic atomic-intervention superiority that simplifies the analysis, and present the C4 algorithm that computes the mGISS in O(|V|+|E|) time. The paper is primarily a theoretical contribution with supporting empirical demonstrations of search-space reduction and regret improvement.

## Strengths

- **Clean theoretical framing with a non-trivial simplification.** Definitions 1-3 establish the conditional-intervention superiority and deterministic atomic-intervention superiority relations, and Proposition 4 proves their equivalence — a non-trivial simplification that enables the graphical characterization to be analyzed through deterministic atomic interventions, which are easier to reason about.

- **Elegant graphical characterization.** The LSCA closure (Definition 9) and its equivalence to Λ-structures (Theorem 12) provide a clean, visualizable condition for whether a node belongs to the minimal search space. Theorem 13 proves this equals the mGISS. The characterization is principled and the Λ-structure viewpoint is insightful.

- **Efficient linear-time algorithm.** C4 (Algorithm 1) computes the mGISS in O(|V|+|E|) time using connectors (Definition 14). The algorithm is simple, the connector concept is clever, and linear-time complexity makes it practical as a preprocessing step for any causal bandit algorithm.

- **Well-motivated problem and honest scope definition.** The paper identifies a genuine gap in the causal bandits literature (single-node conditional interventions) and provides concrete motivating examples. It explicitly states its assumptions (no latent confounders, single-node only, Z_X must contain all ancestors of X) and acknowledges limitations, including that the setting is "non-comparable" to prior multi-node hard-intervention work and that latent confounders are left for future work.

## Weaknesses

### Major
None.

### Minor

- **Regret evaluation uses an empirically estimated best arm as reference.** Footnote 11 states that regret uses "the estimated best arm, defined as the arm that most runs concluded to be the best at the end of training." While this is standard practice in bandit experiments when ground truth is unknown, it means the experiments demonstrate that fewer arms → faster convergence without independently validating that the mGISS contains the true optimal node. The theory (Theorem 13) already proves this, but the experimental design misses an opportunity to directly verify the central claim against ground-truth SCMs where the optimal node is known analytically.

- **Experimental setup for the bandit evaluation is underspecified.** The paper uses bnlearn graphs as SCMs but does not describe how structural equations, noise distributions, variable ranges, or policy functions g are instantiated. While code is provided in the supplementary material, the paper itself lacks sufficient detail for a reader to assess the experimental design without running code.

- **No comparison against a random baseline of the same size as the mGISS.** The regret improvement from mGISS pruning is compared only against the full set of nodes. A random subset of the same size would help disentangle whether the benefit comes from the *specific* nodes selected by the mGISS or simply from reducing the number of arms.

- **No analysis of worst-case mGISS size.** The paper shows that dense graphs retain up to 77% of nodes but does not characterize conditions under which the mGISS is large (or equals the entire ancestor set), which would help practitioners understand when the method provides little benefit.

### Trivial

- The claim that "restricting to single-node interventions in fact makes the problem more challenging" (page 2) is asserted without a concrete complexity metric or comparison, making it feel rhetorical rather than precise.
- C4 pseudocode (Algorithm 1) filters children to those in An(U) at Step 6, but An(U) is not precomputed in the pseudocode — a minor presentation issue.

## Nice-to-Haves

- Construct synthetic SCMs where the optimal node is known analytically, and verify that the mGISS contains it while a random subset of the same size does not. This would directly validate the theory.
- Characterize the conditions under which the mGISS is large (or equals the entire ancestor set) to help practitioners assess when the method provides the most benefit.
- Provide more intuition for why "strictness" is needed in the LSCA definition (Definition 7), perhaps with a counterexample showing where ordinary LCAs fail.

## Removed Points

These points from the harsh critic were removed from the main review, treat with caution:

- **"The regret evaluation is circular"** — Removed and demoted to Minor. The evaluation follows standard bandit practice. The experiments are not designed to re-prove Theorem 13; they demonstrate convergence improvement. Calling this "circular" overstates the issue.
- **"The harder part of the problem is policy selection, not node selection"** — Removed as scope creep. The paper explicitly scopes its contribution to node selection: "In this paper, we find the minimal set of nodes that need to be considered by the agent in step (i)." Criticizing the paper for not solving policy selection is outside its stated scope.
- **"Random graph experiments conflate two effects"** — Removed. Choosing Y as the node with the most ancestors is a conservative experimental design choice, and using An(Y)\{Y} as denominator is natural since mGISS ⊆ An(Y).
- **Generic strengths** (e.g., "addressed an important problem") were removed for lacking specificity.
- Various formatting/style nitpicks removed per instructions.

## Novel Insights

None beyond the paper's own contributions. The reviews largely affirm the theoretical contribution while noting that the empirical validation could be strengthened, which the authors themselves could address in a revision.

## Suggestions

1. Add a synthetic SCM experiment where the optimal node is known analytically to directly validate that the mGISS contains the optimal node and that pruning to it does not exclude the optimal intervention.
2. Include a random-subset baseline of the same size as the mGISS in the bandit experiments to demonstrate that the specific node selection matters beyond arm-count reduction.
3. Provide a sketch of the SCM instantiation details (structural equations, noise distributions) for the bnlearn graphs in the appendix.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/IPayPEGwdE.md | 5.00 | R1 | Yes | Below this paper; that paper had weaker strengths and more negative weaknesses |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/YcW8i9VCf5.md | 6.00 | R1 | Yes | Below this paper; that paper had controversy about novelty and weaker empirical validation |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/qac43AwuL9.md | 6.00 | R2 | Yes | Below this paper; contributions seen as limited by some reviewers |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/l11DZY5Nxu.md | 6.50 | R1 | Yes | Comparable in score quality but had more severe weaknesses (some below -2.0) |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/MVpvyeVeyI.md | 6.50 | R1 | Yes | Comparable but with wide reviewer disagreement (3-10); paper under review is more consistent |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/u63OVngeSp.md | 7.00 | R2 | Yes | Slightly above this paper; had stronger empirical validation with benchmark comparisons |

**Round-1 bracket:** 5.5 – 7.5. **Round-2 narrowing:** The paper's strengths (favorability 11.44–12.70) are comparable to the 6.50 and 7.00 anchors, while its weaknesses (favorability -1.58 to 1.43) are milder than those anchors' weaknesses. The 7.00 anchor had stronger empirical validation with multiple baselines; the current paper's experiments are weaker, placing it just below 7.00. The paper is clearly above 6.00 anchors which had more significant methodological concerns. **Final score: 6.5.**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>