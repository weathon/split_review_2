## Summary

This paper proposes a Dynamics Feature Representation (DFR) framework for RL-based Dynamic Path Planning (DPP) on urban road networks. DFR uses a two-stage hierarchical refinement: (1) a pre-trained static-distance "policy attention" selects top-k shortest paths to extract a task-relevant subgraph, and (2) an n-hop neighborhood method further decouples this subgraph into node-local features. The goal is to produce a state representation that is both compact and informationally sufficient for RL agents. Experiments on three urban road networks compare DFR-enhanced DQN, PPO, and GCN+DQN against "All Dynamics" (AD) baselines.

## Strengths

- **Well-motivated problem framing (Section 4.1, lines 89–101).** The paper clearly articulates the completeness-efficiency trade-off in state representation for RL-based DPP — that global dynamics are informationally complete but prohibitively high-dimensional, while local dynamics risk non-Markovian suboptimality. This framing is precise and establishes why the "sufficient yet compact" goal is a legitimate design challenge.

- **Conceptually clean two-stage hierarchy (Equations 5–7, lines 107–117).** The decomposition into task-relevant features (Ψ) and then node-local features (Φ) is intuitive and well-structured. The idea of using a pre-trained static-distance policy as a structural attention mechanism to identify relevant subgraphs before the RL agent begins learning is creative and grounded in the observation that distance is a stable, topology-dependent signal.

- **Comprehensive ablation study on k and n (Section 5.3, lines 206–253).** The ablation covers six values of k and five values of n, presented in heatmaps with numerical data. The observation that k has "a more complex and less predictable impact" (line 253) than n is an honest finding, and the recommendation to prefer moderate k with smaller n is a useful practical takeaway.

## Weaknesses

### Fatal
None.

### Major

- **The AD (All Dynamics) baseline is too weak to validate the specific DFR design.** DFR is compared against feeding every edge weight of the full graph into a small MLP (64 hidden units). Given the subgraph sizes (thousands of nodes/edges, per Figure 4 legends), any dimensionality-reduction method — including random subsampling at the same compression rate — would likely outperform AD because a 64-unit network cannot process that many inputs. The ablation does include a k=-1.0 condition (no policy attention), which provides some internal signal, but the paper lacks comparisons against **(a) random subgraph selection at matched compression rates** (to isolate whether the *specific* policy-attention selection matters or just *any* reduction), and **(b) simple dimensionality-reduction baselines** such as PCA on edge weights. Without these, the experiments demonstrate only that compressing a large vector helps a small MLP, not that DFR's particular selection mechanism is responsible for the gains.

- **The static-distance policy attention has an unexamined structural limitation (lines 141–150).** The policy attention pre-computes the top-k shortest paths by *static distance* and restricts the RL agent's view to this subgraph *before* any traffic dynamics are observed. Since the objective is travel *time* and congestion factors range from 0.1 to 1.5 (a 15× variation, line 159), the optimal time-based path may use roads that are longer in distance but faster due to low congestion. The distance filter can systematically exclude such paths. The paper's defense — "distance naturally serves as one of the most fundamental constraints" (line 149) — does not address whether the *only* paths worth considering are among the top-k shortest by distance. The paper never tests whether the optimal dynamic path (under its own congestion model) is actually contained within the filtered subgraph. This is a gap that directly concerns the method's core filtering premise.

- **The radar-chart metric conflates a design property with a performance outcome (Figure 5, lines 189–200).** The paper plots 1−GAP, SR, and 1−CR on a radar chart and uses the triangle area as "a summary of overall performance" (line 189). CR (Compactness Rate) measures how much compression DFR achieves — a property of the method's design, not a task-performance outcome. Since AD achieves no compression (CR=1.0, so 1−CR=0), the triangle area for DFR is systematically inflated by its design alone, independent of whether it routes better. A method with moderate GAP/SR but extreme compression could have a larger area than one with excellent GAP/SR but moderate compression. This metric conflates "performs well on the routing task" with "compresses the input well" and does not support the claim that DFR achieves "superior overall performance" (line 200).

### Minor

- **No variance or statistical significance reported for the main metrics (Section 5.2).** Only planning time is reported with error bars (8.18 ± 1.74 ms, line 202). Mean GAP, SR, and CR are given as single-point estimates. The ablation heatmaps (Figure 6) show considerable variation across (k, n) configurations — e.g., SR ranging from 0.672 to 0.905 — making it unclear whether the reported differences between DFR and AD are meaningful or within noise. Multiple random seeds and confidence intervals would substantially strengthen the empirical claims.

- **The PSR "theoretical basis" is invoked but not operationalized (Section 4.2, lines 129–135).** The paragraph connects DFR to Predictive State Representations but does not derive any design constraint, algorithm, or guarantee from PSR theory. The claim that grounding DFR in PSR "guarantees that the resulting representations are compact, temporally predictive, and theoretically sufficient" (line 135) is an overstatement — mentioning a theoretical framework does not confer its properties onto a specific implementation. This passage reads more as motivation than as a rigorous foundation.

- **The dynamics model is simple relative to the practical claims made.** Traffic dynamics are modeled as a congestion factor β ∈ [0.1, 1.5] multiplied by base travel time (line 159–161). Real urban traffic exhibits spatiotemporally correlated congestion, cascade effects, and time-of-day patterns. The paper's claims about "practical urban transportation" (abstract, line 9) and "real-world traffic scenarios" (line 153) are not fully supported by this simulation model. This is a common limitation in simulation-based RL work, but it should be acknowledged more explicitly.

- **Manual tuning of k and n is a practical limitation (Section 6, lines 256–258).** The ablation shows that k in particular has a "complex and less predictable impact" (line 253), and performance varies noticeably across settings (SR from 0.672 to 0.905). The paper acknowledges that manual selection "may limit its practical applicability" but understates the challenge: without a principled way to set these hyperparameters, deployment in a new city requires costly re-tuning.

### Trivial
None.

## Nice-to-Haves

- **Comparison against non-RL baselines (D\* Lite, A\* with predicted costs).** Footnote 3 (line 165) scopes the paper to evaluating DFR within RL, which is a legitimate choice. However, since the paper frames DPP as a routing problem and makes practical claims, showing that DFR+RL is at least competitive with standard routing algorithms would broaden the paper's impact.
- **An experiment directly testing the static-distance filter assumption:** measuring what fraction of optimal dynamic paths (under the paper's own congestion model) fall within the top-k shortest paths by distance. If the fraction is high, this would directly address the structural limitation concern.
- **Automatic or adaptive selection of k and n,** or a discussion of how these parameters might scale to city-wide networks with millions of nodes.

## Removed Points

The following points from the input review were removed after verification against the paper:

1. **"GNNs dismissed without evidence or citation"** (critique of lines 29–30). The paper *does* cite Wu et al., 2020 immediately after the claim about computational/memory overhead scaling with graph size. This criticism is factually incorrect.
2. **"Abstract wording suggests adaptation to traffic dynamics"** (critique of line 9). The abstract says "progressively refines high-dimensional global dynamics into compact, decision-relevant features." This is consistent with the paper's hierarchical refinement (static-distance task filter → dynamic-position local filter). The concern about non-adaptation to traffic dynamics is the same as the structural-limitation weakness already listed under Major; separating it here would duplicate.
3. **"Section 5.2 concedes that AD failure is an architectural capacity issue"** (critique of lines 200–202). The paper's entire motivation is that high-dimensional global dynamics are problematic for RL; observing that a small MLP cannot process them is consistent with this framing, not a concession that undermines it.
4. **Missing related works.** Cannot be verified without external sources per the review guidelines.

## Novel Insights

None beyond the paper's own contributions. The reviews do surface a synthetic observation that the static-distance filter's structure creates a tension with the paper's dynamic-routing claims, but this is a critique of a limitation, not a novel discovery from the reviews.

## Suggestions

1. **Add fair compression baselines.** Compare DFR against: (a) random subgraph selection at matched CR, and (b) a simple PCA-reduced version of the full edge-weight vector. This is essential to isolate whether DFR's specific policy-attention mechanism adds value beyond generic dimensionality reduction.
2. **Test the static-distance filter assumption directly.** Measure, under the paper's own congestion model, the fraction of tasks where the optimal dynamic path falls within the top-k shortest paths by distance. Report results across a range of k values.
3. **Report all main metrics with variance across multiple seeds.** This is standard practice in RL research and would address the significance concern without requiring major re-experimentation.
4. **Remove CR from the radar-chart "overall performance" visualization**, or clearly separate compression metrics from task-performance metrics. The triangle area claim should not mix design properties with routing outcomes.
5. **Tone down the PSR claims** (line 135). Replace "guarantees" with language about inspiration or motivation, since no PSR-derived design constraints are enforced in the implementation.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>