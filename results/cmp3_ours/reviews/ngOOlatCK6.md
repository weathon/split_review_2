Now I have a clear picture of calibration. Let me finalize the review.

Round 1 bracket: I place this paper between 5.5 and 7.0. It is stronger than the 5.00 "Learning Good Interventions in Causal Contextual Bandits" paper (which has restrictive binary assumptions and weaker theory) but not as strong as the 7.00 "Deriving Causal Order from Single-Variable Interventions" paper (which has broader experimental validation). The most directly comparable anchor is the 6.00 "Adversarial Causal Bayesian Optimization" paper, which has a similar mix of clean theory and moderately strong experiments.

Within this bracket, I narrow to 6.0. The estimated-best-arm issue in the bandit experiments is a real weakness that keeps the paper from being a 7+, but the core theoretical contribution is genuinely novel and well-executed, placing it clearly above the 5-range papers.

Here is the final consolidated review:

## Summary

This paper studies single-node conditional interventions in causal bandits, where the agent selects both which node to intervene on and what policy (a function of observed context) to use. The paper provides a graphical characterization of the minimal set of nodes guaranteed to contain the optimal intervention node (the mGISS), proving it equals the LSCA closure of the parents of the target variable Y. It also proposes the C4 algorithm (linear in |V|+|E|) to compute this set, and empirically demonstrates substantial search space pruning (up to 90% for real-world networks) and improved regret convergence when the mGISS is used with a UCB-based bandit algorithm.

## Strengths

1. **Novel problem formulation.** The paper formalizes a realistic and previously uncharacterized setting — single-node *conditional* interventions in causal bandits — that sits between the well-studied hard-intervention setting (Lattimore et al., 2016) and the multi-node hard-intervention setting (Lee & Bareinboim, 2018). The paper correctly argues why this combination makes the search-space problem more difficult than either dimension alone, and provides rigorous justification for why existing results do not apply.

2. **Elegant theoretical characterization.** The main result (Theorem 13) — that the mGISS equals the LSCA closure of the parents of Y — is clean, non-trivial, and well-motivated through the worked examples in Figure 1. The Λ-structure characterization (Theorem 12) provides a simple graphical test for membership in the closure, and the reduction to deterministic atomic interventions (Proposition 4) is a clever simplification that makes the analysis tractable while preserving applicability to the full probabilistic setting.

3. **Optimal linear-time algorithm.** The C4 algorithm (Section 5) runs in O(|V|+|E|) time, which is optimal. The connector concept is intuitive and the algorithm's logic (a node enters the closure iff its children have more than one distinct connector) is directly interpretable in terms of the paper's graph-theoretic machinery. The pseudocode is clear enough to implement directly.

4. **Substantial empirical pruning.** The search space reduction results — up to 90% pruning for real-world networks and from 70% down to 29% for sparse 500-node random graphs — are genuinely impressive and provide the paper's strongest empirical evidence for practical impact. The trend (sparser graphs → more pruning, larger graphs → more pruning) is well-documented and aligns with the theoretical intuition about Λ-structure formation.

## Weaknesses

### Fatal
None.

### Major

1. **Regret computed against an estimated best arm, not the true optimum.** Footnote 11 states: "For the computation of regret, we use the estimated best arm, defined as the arm that most runs concluded to be the best at the end of training." Standard regret is defined with respect to the true optimal arm μ* = max_a μ_a. By substituting an empirically estimated best arm, the paper measures convergence to the algorithm's own estimate rather than to the true optimum. This creates a risk of circularity: if both the brute-force and mGISS methods converge to the same (possibly wrong) estimate, their regret curves will converge to zero even if neither has found the true optimal node. The claim "better nodes are selected earlier" (Section 6) cannot be properly assessed from these curves alone. The paper's theory guarantees that the mGISS contains the optimal node, but the experiments neither verify this guarantee empirically nor demonstrate that CondIntUCB successfully identifies the true optimal node. A synthetic experiment with a known SCM (where the true optimum is known by exhaustive enumeration) would cleanly resolve this, but none is provided.

### Minor

2. **Weak baseline for regret comparison.** The "brute-force" baseline considers all ancestors of Y as candidates. Since the paper's theory already implies many of these can never be optimal, comparing against the full ancestor set is a low bar — any pruning method that removes *any* nodes will show an advantage because fewer arms means less exploration. A more informative comparison would be against intervening only on Pa(Y) (the parents of Y), which would measure how much value the LSCA closure adds over this simpler pruning. This does not invalidate the results but limits their informativeness.

3. **CondIntUCB's per-context UCB approach is not analyzed.** CondIntUCB maintains a separate UCB instance for each realization of Z_X (each context). With Z_X = An(X)\{X}, the number of contexts is the product of the ranges of all ancestor variables, which can grow exponentially. The paper gives no information about how many contexts arise for each dataset, how many rounds are needed for the inner UCB instances to converge, or whether any form of generalization or function approximation is used. The paper acknowledges that datasets were selected because their mGISS was "sufficiently small to allow experimentation" — but without context counts, it is hard to assess the practical feasibility of CondIntUCB or whether the regret results are driven by mGISS pruning or by pathological behavior of the per-context UCB approach.

4. **No statistical significance reported for regret curves.** The confidence bands (standard deviations) are shown, but no statistical tests are reported to assess whether the differences between brute-force and mGISS regret curves are significant across the 300–500 runs.

5. **Arm space size not reported.** The paper reports the reduction in the number of nodes (e.g., from 30 to 3), but does not report the reduction in the number of *arms* (distinct conditional interventions). Since each node X can have many policies depending on Z_X, the reduction in nodes may not translate linearly into reduction in arms. This matters for understanding the practical speedup.

### Trivial

6. **C4 algorithm complexity note.** The pseudocode uses Ch(V) ∩ An(U), which requires ancestor reachability from U to be precomputed. The O(|V|+|E|) claim is plausible only if this preprocessing is included. A brief confirming note would improve clarity.

## Nice-to-Haves

- Add a synthetic verification experiment: for randomly sampled SCMs with known structural assignments and noise distributions, enumerate all conditional interventions to identify the true optimal node, and verify that it always falls within the mGISS. This would directly validate the theoretical guarantee, which currently rests entirely on proofs.
- Compare against the Pa(Y)-only baseline to quantify the value added by the LSCA closure beyond simple parent-only pruning.
- Report the number of contexts per node and the number of arms in the full vs. pruned space for each dataset used in the bandit experiments.

## Removed Points

The following points from the harsh critic input were removed (with justification):

- **"Single-node more challenging not justified"** (Harsh Critic, Section-by-Section Notes, Abstract/Introduction): The paper explicitly justifies this on lines 98–99, explaining that multi-node interventions allow simply intervening on Pa(Y) (Lee & Bareinboim, 2018), while single-node interventions cannot, so the minimal search space is more complex. The criticism is factually incorrect.
- **"Z_W ⊆ Z_X assumption not motivated"** (Harsh Critic, Section-by-Section Notes, Preliminaries): The paper provides motivation and concrete examples (traffic controller and doctor examples) on line 86. The assumption is stated, contextualized, and given a clear mathematical formulation. This is a transparent design choice, not a weakness.
- **"Definition 1 quantifies over all conditioning sets — too strong"** (Harsh Critic, Section 3, Definition 1): This is by design. The definition is meant to provide a worst-case guarantee that holds regardless of the practitioner's choice of Z_X and Z_W. The criticism reflects a misunderstanding of the purpose of a global superiority relation.
- **"Proposition 4 proof in appendix"** (Harsh Critic, Section 3, Proposition 4): Per the hard rules, criticisms about missing appendix content are removed. The parser strips appendix content from all submissions; the proof exists in the original paper.
- **"Bar plot in appendix"** (Harsh Critic, Section 6, Experiments — real-world graph results): The main text gives the summary claim ("over 90% reduction") with specific numerical examples. The actual plot being in the appendix is standard practice; the criticism is a formatting nitpick.
- **"The paper does not report the size of the full arm space"** (Harsh Critic, Missing Parts): This is kept in Minor Weaknesses instead.

## Novel Insights

None beyond the paper's own contributions. The critical evaluation surfaces the estimated-best-arm issue and the weak baseline concern as the two most actionable areas for improvement, but these are standard review observations rather than novel analytical insights.

## Suggestions

1. **Fix the regret computation.** Replace the estimated-best-arm approach with oracle-optimal regret using a synthetic SCM where the optimal node is known by exhaustive enumeration. This would allow the regret curves to demonstrate genuine convergence to the true optimum and directly validate the theoretical guarantee that the mGISS contains the optimal node.

2. **Add synthetic verification experiments.** Even a small-scale experiment with random SCMs checking that the true optimal node always falls within the mGISS would provide direct empirical support for the core theoretical claim, which currently rests entirely on proofs.

3. **Strengthen the bandit baselines.** Compare against the Pa(Y)-only condition to measure how much the LSCA closure adds beyond trivial parent pruning. Report context counts and arm space sizes for each dataset.

4. **Report statistical significance.** Add a simple paired test to assess whether the regret differences are statistically reliable across runs.

## Score and Decision

<score>6.0</score>
<decision>Accept</decision>