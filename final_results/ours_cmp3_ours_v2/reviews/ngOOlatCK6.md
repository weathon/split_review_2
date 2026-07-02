## Summary

This paper studies the problem of finding the minimal set of nodes guaranteed to contain the optimal conditional intervention in a single-node conditional causal bandit (where arms are conditional interventions, the causal graph is known but structural assignments are unknown). The authors establish a graphical characterization: the minimal globally interventionally superior set (mGISS) equals the LSCA closure of the parents of the target variable, equivalently the set of nodes forming Λ-structures over those parents. They also present the C4 algorithm, which computes this set in linear time O(|V|+|E|). Experiments on random and real-world graphs show substantial search-space pruning (>90% for large models), and integrating mGISS with a UCB-based algorithm improves regret.

## Strengths

- **Proposition 4 (conditional ≅ deterministic atomic superiority):** This equivalence is a genuinely non-obvious theoretical simplification. It allows the paper to analyze the much cleaner deterministic atomic case while the result carries over to the full probabilistic conditional-intervention setting. This result is properly proved (appendix), and it is the linchpin making the entire analysis tractable.

- **Λ-structure characterization (Theorem 12):** The observation that the mGISS can be characterized as the set of nodes forming Λ-structures over Pa(Y) provides a crisp, visualizable condition connecting the recursive LSCA-closure definition to a simple graph-theoretic property. This is elegant and clearly presented.

- **mGISS uniqueness (Proposition 6):** Many "minimal" sets in the causal literature are not unique; having a well-defined, unique target is important for downstream applications and is a genuine strength.

- **C4 algorithm:** The algorithm is clean and intuitive (using connectors, Definition 14). The linear-time proof (Theorem 16) is convincingly argued, and the connector concept naturally illuminates why certain nodes are included or excluded from the mGISS.

- **Real-world graph pruning statistics:** The paper reports >90% search-space reduction for some of the largest models from the `bnlearn` repository. Since real-world causal graphs tend to have low average degrees (all tested models have average degree <4.0), this provides concrete evidence that the theoretical characterization translates into practical value.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Regret baseline computed against an "estimated best arm" (footnote 11):** The regret is computed against "the arm that most runs concluded to be the best at the end of training." It is not clear whether this estimate is computed jointly across conditions or separately per condition. If the two bandit algorithms (brute-force vs. mGISS-pruned) converge to different nodes, the regret is computed relative to different targets, making the curves hard to interpret as clean evidence that the mGISS converges to the *truly* optimal node faster. The paper's theoretical contribution stands independently, but this weakens the empirical demonstration.

- **Missing alternative pruning baselines in bandit experiments:** The only comparison is mGISS vs. brute-force (all nodes). Since fewer arms *always* reduces regret in bandit problems (all else equal), the reader cannot distinguish whether the improvement comes from the *specific mGISS characterization* or simply from any reduction in arm count. The paper's own framing (Section 1) motivates the contribution as finding *which* nodes to prune, not just that pruning helps, making this gap notable. Comparisons against random pruning to the same set size or heuristic pruning (e.g., to Pa(Y) only) would substantially strengthen the empirical validation.

- **Experimental details are vague in places:** (a) The total number of rounds for the regret experiments is not stated explicitly — the paper says only "chosen as to observe (near) convergence." (b) The mGISS sizes for the four `bnlearn` datasets used in the regret experiments appear in the figure labels but are not reported in the main text prose, making it hard for a reader to gauge how much pruning actually occurred on those specific datasets.

### Trivial
None.

## Nice-to-Haves

- Comparing against alternative pruning strategies (random pruning to matched set size, pruning to Pa(Y) only) would directly test whether the *specific mGISS characterization* drives the improvement, rather than any reduction in arm count.
- Explicitly stating the number of rounds used in the regret experiments.
- Presenting the conditioning-set assumptions (An(X)\{X\} ⊆ Z_X ⊆ V\De(X) and the nesting condition) as an enumerated list for clarity.
- Reporting wall-clock time comparisons between brute-force and mGISS-pruned bandits would further illustrate the practical benefit.

## Removed Points

These points are flagged to be removed — treat them with caution:

- **Issue 3 from the harsh critic ("no policy optimization / worst-case set vs specific SCMs"):** The critic argued the experiments should verify whether the optimal node falls within mGISS for specific SCMs. This misunderstands the role of the theoretical guarantee: the mGISS is proven to contain the optimal node for *all* SCMs compatible with G. The experiments are meant to validate that using this set improves bandit performance, not to re-verify the theory. Removed.

- **Criticism about Proposition 4 proof being in the appendix:** Putting proofs in the appendix is standard practice at ICLR. The main text clearly states the equivalence and its consequences. Removed.

- **Criticism about not discussing computational cost of ancestor computation for C4:** The O(|V|+|E|) complexity is standard for a topological traversal, and the paper claims linear time. This is a standard assumption, not a missing analysis. Removed.

- **Criticism about strength 4 being generic ("addressed an important problem"):** Not present in this reviewer input.

## Novel Insights

None beyond the paper's own contributions. The harsh critic provides a competent but standard assessment: it correctly identifies the paper's theoretical strengths (Proposition 4, Λ-structure characterization, uniqueness, C4 algorithm) and raises valid concerns about the experimental methodology (regret baseline, missing baselines, vague round counts). The review does not surface any deep structural flaw that the authors would not already be aware of.

## Suggestions

1. For the regret experiments: compute regret against a fixed reference determined by exhaustive search in a separate evaluation phase, or at minimum clarify whether the "estimated best arm" is computed jointly or per-condition, and justify the choice.
2. Add at least one alternative pruning baseline (random pruning to same set size, or pruning to Pa(Y) only) to the bandit experiments. This would directly test whether the specific mGISS characterization outperforms naive pruning.
3. Explicitly state the number of rounds used in the bandit experiments and the mGISS sizes for each dataset in the main text.
4. Consider presenting the conditioning-set assumptions as an enumerated list rather than a single long paragraph.

---

### Calibration Report

**Round 1 bracket:** [6.0, 7.5]

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| IPayPEGwdE — Learning Good Interventions in Causal Contextual Bandits | 5.00 | 1 | Similar causal-bandit theory paper, but rejected. Less clean theoretical result, weaker experiments. Our paper is stronger. |
| MVpvyeVeyI — Causal Bayesian Optimization w/ Unknown Graphs | 3.40 | 1 | Wide score range (3–10); not a reliable comparator. |
| YcW8i9VCf5 — Adversarial Causal Bayesian Optimization | 6.00 | 1 | Similar theory+experiments structure; accepted. Our paper has cleaner theory but weaker experiments. Comparable quality. |
| pOoKI3ouv1 — Robust agents learn causal world models | 5.75 | 1 | Very different type of paper (causal representation learning theory). |
| u63OVngeSp — Deriving Causal Order from Single-Variable Interventions | 7.00 | 2 | Strong causal theory paper with experiments; accepted with scores 5,8,8,6,8. Our theory is comparably strong but experiments are sparser. |
| M0xK8nPGvt — Exploiting Causal Graph Priors with Posterior Sampling for RL | 7.50 | 2 | Stronger experiments (RL benchmarks); our paper is more theoretical. |

**Narrowing:** The paper sits between the 6.0 (YcW8i9VCf5, accepted with moderate experiments) and 7.0 (u63OVngeSp, strong theory + reasonable experiments) anchors. The theory is solid and non-trivial, comparable to u63OVngeSp, but the experiments are weaker — limited to 4 datasets, no alternative baselines, and a somewhat problematic regret baseline. This places the paper below u63OVngeSp's 7.0 but above YcW8i9VCf5's 6.0, yielding a final score of **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>