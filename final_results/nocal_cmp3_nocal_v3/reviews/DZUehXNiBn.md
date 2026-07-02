Now let me write the final consolidated review.

## Summary

VISTA proposes a three-stage modular framework for causal structure learning: (1) decompose the graph into Markov Blanket neighborhoods, (2) aggregate local subgraph estimates using a weighted voting scheme with exponential confidence decay, and (3) enforce acyclicity via a greedy Feedback Arc Set heuristic. The framework is model-agnostic (any base learner and MB estimator can be plugged in), fully parallelizable, and requires only lightweight $\mathcal{O}(n^2)$ aggregation overhead. Experiments across six base learners and multiple graph families show substantial runtime reductions and competitive accuracy.

## Strengths

- **Clean, model-agnostic framework design.** The three-stage pipeline cleanly separates concerns. Any base learner and any MB estimator can be swapped without modifying the aggregation logic. This is a genuine practical improvement over prior work like DCILP (solver-based reconciliation) and heuristic fusion schemes tied to specific learners.

- **Substantial, well-documented runtime improvements.** Table 3 shows dramatic reductions across all base learners (e.g., NOTEARS at n=300: 12,515s → 2,136s; SCORE at n=100: 10,040s → 198s; GraN-DAG at n=300: 25,206s → 2,336s). These gains are real, stem from the divide-and-conquer design, and can be amplified further with additional parallelization. This is the paper's strongest and most cleanly demonstrated result.

- **Broad empirical coverage.** Experiments span six base learners (NOTEARS, GOLEM, DAG-GNN, GraN-DAG, SCORE, CAM) across Erdős–Rényi and scale-free graphs with sizes from n=30 to n=300 and two density levels. This breadth makes the model-agnostic claim more credible than it would be with only one or two learners.

- **Theoretical ambition.** The paper provides finite-sample error bounds (Theorem 3.2), a practical range for $\lambda$ (Theorem 3.4), and an asymptotic consistency result (Theorem 3.5). While these have important limitations (discussed below), the attempt at formal guarantees goes beyond purely heuristic fusion schemes like Shah et al. (2024).

## Weaknesses

### Fatal

None.

### Major

1. **The asymptotic consistency guarantee (Theorem 3.5) does not apply to the sparse-graph regime on which VISTA is evaluated.** Theorem 3.5 assumes $m = C\log n$, where $m$ is the number of subgraphs containing both endpoints of a candidate edge. In sparse graphs with bounded average degree ($h\in\{3,5\}$ in the experiments), an edge appears in the MB subgraphs of its two endpoints plus at most a few common children/spouses. This number is bounded by a small constant related to max degree, not growing with $n$. The paper does not discuss this gap or justify that the assumption holds in the experimental setting. The asymptotic consistency claim is therefore conditional on a condition that is not met.

2. **The MB estimator used in experiments is never specified.** The pseudocode (Figure 2) treats `MB_solver` as a black box, but the experiments never name which MB estimator was used, what hyperparameters were chosen, or how its accuracy was validated. Proposition 3.1 guarantees coverage only when MBs are *correctly* identified. Figure 1 reports MB F1 scores (~0.9) across graph sizes but without naming the method, these results are not reproducible. For a framework whose theoretical coverage guarantee and practical performance both depend on reliable MB identification, this is a significant omission.

3. **The evaluation on the real-world Sachs benchmark (Table 4) is weak.** Improvements are marginal and inconsistent: GOLEM+VISTA shows no SHD improvement (16→16, TPR drops from 0.26 to 0.18); SCORE+VISTA improves SHD from 18→15 but TPR drops from 0.18 to 0.12; DAG-GNN+VISTA improves SHD from 15→14; GraN-DAG+VISTA shows the largest SHD improvement (16→12) but TPR drops sharply from 0.53 to 0.29. SID values barely change (e.g., 50→48 for GOLEM). No standard deviations are reported, making significance assessment impossible. These results do not convincingly support the claim that VISTA "consistently" improves base learners.

4. **The comparison between VISTA-WV and standalone baselines confounds the effect of decomposition (smaller subgraphs) and the effect of aggregation (weighted voting).** The paper includes VISTA-NV (naive voting = keep all edges) as a control, which partially addresses this confound — WV's dramatic improvement over NV (e.g., FDR 0.87→0.08 for NOTEARS on ER5) shows the voting mechanism does useful filtering. However, NV is a degenerate baseline (FDR=0.87, SHD=3171) that cannot cleanly isolate whether the decomposition alone (e.g., base learner on MB subgraphs followed by simple edge intersection/consensus) already provides gains over the full-graph baseline. A cleaner ablation would compare VISTA-WV against the base learner run on MB subgraphs with a simple intersection or consensus rule to isolate the voting contribution.

### Minor

1. **The independence assumption in Theorem 3.2 is violated in practice.** The theorem models votes as independent Binomial($m$, $p$), but MB subgraphs heavily overlap and the base learner's errors on overlapping data are correlated. The paper acknowledges this limitation (lines 138–139) and frames the bound as "a qualitative guide." This is responsible, but it means the finite-sample error bound provides no quantitative guarantee about actual behavior, and combined with Issue 1 in the Major section, the theoretical contribution is largely heuristic.

2. **The fixed $\lambda = 0.5$ may violate Theorem 3.4's lower bound for edges with low support.** For $m=2$ and $t=0.7$, Theorem 3.4 requires $\lambda > -\frac{1}{2}\ln(1-0.7) \approx 0.602$, but the paper uses $\lambda = 0.5$ across all experiments. The paper does not check how often edges with $m\leq 2$ occur or whether this violation has empirical consequences.

3. **Sensitivity analysis is reported only for $\lambda$, not for the threshold $t$.** The threshold $t$ is fixed at 0.7 in all main experiments. Since $\lambda$ and $t$ jointly govern the precision–recall trade-off, a 2D sensitivity sweep would be informative. The paper notes that $\lambda$ sweeping is retraining-free (reusing cached votes), and the same property holds for $t$, so this would be straightforward to include.

4. **The runtime reporting does not separate MB identification time from base learner time.** The MB identification cost is a one-time overhead that the divide-and-conquer design requires. Reporting the breakdown would help practitioners understand where time is spent and how the framework scales for different MB estimators.

### Trivial

- **No discussion of boundary nodes with small MBs.** Edges involving nodes with few neighbors (graph periphery) appear in very few subgraphs (small $m$). The exponential weighting term $(1-e^{-\lambda m})$ aggressively down-weights such edges even if they are correct. The paper does not discuss how this affects structure recovery at graph boundaries.

## Nice-to-Haves

- A comparison where the standalone baseline is given the same parallelization budget as VISTA (i.e., subgraph-size problems) would help separate the effect of VISTA's framework from the trivial benefit of smaller problem instances, clarifying whether VISTA's contributions go beyond "just use a smaller graph."
- Reporting statistical significance (e.g., paired tests across runs) for the reported improvements would strengthen the empirical claims, especially given that some standard deviations in Table 1 are large relative to the reported differences.

## Removed Points

These points from the input review were removed with justifications:

- **"VISTA consistently reduces TPR relative to the base learner"**: Fact-checking Table 1 shows this is incorrect for most cases. For ER5 at n=100, VISTA-WV improves TPR for 4 of 5 methods (GOLEM: 0.35→0.50, DAG-GNN: 0.42→0.56, GraN-DAG: 0.05→0.10, SCORE: 0.58→0.65). Only NOTEARS shows a slight drop (0.74→0.68). The claim is not supported by the data.
- **"Bound should be interpreted as a qualitative guide" weakness**: The paper already acknowledges the independence limitation explicitly (lines 138–139). The weakness duplicates Issue 1 in Minor above but with no additional content not already in the paper's own discussion.
- **"Comparison on the same computational budget"** and **"Health of the related-work characterization"**: These were moved to Nice-to-Haves or removed as scope-creep or speculative concerns not verifiable from the paper.

## Novel Insights

The most interesting observation across the reviews is the tension between VISTA's theoretical framing and its empirical success. The theory relies on assumptions (independent votes, $m=\Omega(\log n)$ per edge) that are violated in the sparse-graph regime, yet the method works well empirically. This suggests the framework may be robust for reasons the theory does not capture — possibly because the FAS post-processing corrects residual errors that the voting stage misses, or because the weighted voting is effective even under dependence in ways that the Binomial concentration model does not predict. The runtime improvements are so dramatic (often 5–10×) that they are valuable even without clear theoretical guarantees, and the paper could lean more heavily on this engineering contribution rather than overclaiming the theory.

## Suggestions

1. **Specify the MB estimator** used in all experiments (name, hyperparameters, implementation), or provide an ablation across different MB estimators to demonstrate model-agnosticism.
2. **Add the proposed ablation**: compare VISTA-WV against a simple consensus baseline (intersection or majority-vote of edges across subgraphs) to cleanly isolate the weighted voting mechanism's contribution.
3. **Acknowledge the $m = C\log n$ assumption gap** in Theorem 3.5 explicitly, and discuss what the asymptotic consistency result implies (or does not imply) for the sparse-graph regime actually tested.
4. **Report standard deviations on the Sachs results** and tone down the "consistently improve" characterization given the mixed real-data outcomes.
5. **Add a 2D sensitivity analysis** ($\lambda \times t$) to show how the two parameters interact.

## Score and Decision

The paper has real engineering value: the runtime improvements are substantial, the modular design is practical, and the empirical coverage is broad. The core ideas (MB decomposition + weighted voting + FAS) are clean and well-motivated. However, the theoretical guarantees have significant gaps that are not acknowledged, the MB estimator is not specified (harming reproducibility), the real-data evidence is weak, and the evaluation confound between decomposition effects and voting effects is not fully resolved. The claims about accuracy improvements are somewhat overstated relative to what the evidence cleanly supports.

The primary contribution is a runtime-efficient, modular framework for causal discovery, not a method with fundamentally better accuracy. Treated as an engineering/systems contribution, the paper is solid. The weaknesses are addressable but nontrivial.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>