Now I'll finalize my review with the assessment.

## Summary

VISTA is a modular, model-agnostic framework for causal structure learning. It decomposes global DAG learning into Markov Blanket-centered subgraphs, runs any off-the-shelf base learner on each subgraph in parallel, and aggregates results via a weighted voting scheme with exponential confidence decay, followed by GreedyFAS-based acyclicity enforcement. The framework is empirically evaluated on 6 base learners across synthetic and real data, and is accompanied by finite-sample error bounds and an asymptotic consistency theorem.

## Strengths

1. **Model-agnostic and consistently improves accuracy across diverse base learners.** Tables 1-2 show VISTA-WV improves F1 over standalone baselines for NOTEARS (0.76→0.79), GOLEM (0.35→0.60), DAG-GNN (0.33→0.59), GraN-DAG (0.06→0.17), and SCORE (0.14→0.31) on ER5 n=100, with gains holding across ER and SF topologies. The improvements span differentiable and combinatorial learners, directly validating the model-agnostic claim.

2. **Substantial empirical runtime reductions (5-10×) through parallelizable decomposition.** Table 3 shows NOTEARS at n=300 drops from 12,516s to 2,137s (5.9×), DAG-GNN from 17,714s to 1,960s (9.0×), and GraN-DAG from 25,206s to 2,336s (10.8×). These are large efficiency gains supporting the scalability claim.

3. **Finite-sample error bounds with an explicit feasible interval for λ.** Theorem 3.4 derives a closed-form admissible range for λ (`-1/m ln(1-t) < λ ≤ -1/m ln ε`), providing principled theoretical guidance for the weighting parameter that goes beyond the uncalibrated heuristics used in prior modular approaches.

4. **Clean coverage guarantee (Proposition 3.1).** Proves every true edge appears in at least two MB subgraphs (sender's and receiver's), ensuring the decomposition does not discard correct edges before voting.

5. **FAS-before-thresholding ordering insight.** The paper identifies that removing cycles before filtering avoids unnecessary precision loss — a simple but non-obvious design detail that is explicitly justified and informs practical usage.

## Weaknesses

### Major

1. **Asymptotic consistency theory (Theorem 3.5) assumes a regime that the algorithm does not satisfy.** Theorem 3.5 proves consistency when `m = C log n` (number of subgraphs per candidate edge grows logarithmically with n). In VISTA's design, an edge (X,Y) appears only in subgraphs whose Markov Blankets contain both endpoints — for sparse graphs with bounded degree, this number is essentially constant (bounded by the degree of the two endpoints), not growing with n. The sufficient condition in the theorem therefore does not describe the algorithm's operating regime. This means the paper's asymptotic consistency claim, as stated in the abstract and conclusion, does not apply to the implemented procedure. The paper should either (a) prove consistency under the correct scaling regime or (b) clearly delineate that the asymptotic result establishes a sufficient condition that may not hold for the actual algorithm, and downgrade the consistency claim accordingly.

2. **Theory-practice gap for the λ selection (Theorem 3.4 vs. fixed λ=0.5).** Theorem 3.4's feasible λ range depends on per-edge m: `-1/m ln(1-t) < λ ≤ -1/m ln ε`. For t=0.7, the lower bound is ≈1.204/m and the upper bound depends on ε. The experiments use a single λ=0.5 for all edges, but whether λ=0.5 satisfies (5) depends on m and the unspecified ε; for m=1 or 2 (common for low-degree edges in sparse graphs), λ=0.5 is outside the guaranteed range, and for large m it may exceed the upper bound. The paper states λ=0.5 "lies within (5)" without specifying which ε is used or reporting the distribution of m values across edges, making the link between the theoretical guarantee and the experimental setup unclear.

### Minor

1. **The MB identification algorithm used in the main experiments is not named.** The paper refers to "MB_solver" in pseudocode and states the code provides a flexible interface, but never identifies which specific MB algorithm (e.g., IAMB, MMPC, PCMB) was used in the reported experiments. Since MB identification is the critical first pipeline step whose quality directly affects all downstream results, this is a reporting gap. The code is provided in supplementary material, so this is partially addressable, but the main paper should name the method.

2. **Absolute performance on the Sachs real-data benchmark is modest.** The best SHD is 12 on an 11-node, 17-edge graph (GraN-DAG+VISTA), but this comes at TPR=0.29 — most true edges are missed. While VISTA consistently improves over baselines (the paper's primary claim, which holds), readers should be aware that the enhanced graphs still recover substantially less than half the ground-truth structure.

3. **The subgraph learning step inherits known marginalization issues.** When a learner is applied to subset {V} ∪ MB(V), the true causal relationships under the marginal distribution may differ from the induced subgraph of the global DAG due to unobserved variables outside the subset. The paper acknowledges this briefly as "latent confounding" producing "redundant edges" in the limitations, but the issue cuts deeper: even a perfect local learner might not recover the correct global subgraph projection. This does not invalidate the approach (the FAS + thresholding post-processing is designed to mitigate it), but the issue deserves more prominent discussion.

### Trivial

None.

## Nice-to-Haves

- A per-edge m distribution plot across graph sizes would help clarify whether the algorithm operates in a regime where the theoretical λ bounds from Theorem 3.4 are meaningful.
- A sensitivity analysis for the threshold t (not just λ) would provide a more complete picture of the precision-recall trade-off.

## Removed Points

These points are flagged to be removed; treat them with caution:

- "NV results are consistently catastrophic" — NV is presented as an ablation to motivate the weighted voting; its poor performance is expected and not a weakness of the paper.
- "Variance collapse is suspicious" — Pure speculation that reduced standard deviations reflect rigidity rather than robustness; no evidence is offered for this interpretation.
- "No comparison with DCILP in main tables" — The paper states the comparison is in Appendix F.2, which exists in the original submission but was removed by the parser.
- "No error bars for Sachs" — Single-run evaluation on a small real dataset is standard.
- "No ablation for FAS vs. thresholding ordering" — The paper provides explicit reasoning for this design choice.
- "Sensitivity study only varies λ, not t" — The paper fixes t=0.7 and focuses on λ as the tunable parameter; this is a reasonable scoping choice.
- "The subgraph learning step is fundamentally ill-posed" — The paper acknowledges this limitation; the critic overstates it as a fatal issue when it is a known challenge shared by all modular causal discovery approaches.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Revise the asymptotic consistency framing.** Either prove consistency under the algorithm's actual m regime (bounded per edge in sparse graphs) or clearly state that Theorem 3.5 establishes a sufficient condition under idealized `m = C log n` growth and does not directly apply to the implemented algorithm. Downgrade the consistency claim in the abstract/conclusion accordingly.

2. **Name the MB identification algorithm used in the experiments.** This is the single most actionable fix for reproducibility. If multiple MB algorithms are supported in the code, specify which one was used for the reported results.

3. **Provide per-edge m diagnostics.** A simple histogram or summary of m values across edges for different graph sizes (n=30, 50, 100, 300) would help bridge the gap between the per-edge λ theory and the fixed λ=0.5 used in experiments.

4. **Discuss the marginalization issue more prominently.** Acknowledge that the divide step assumes local subgraphs correspond to global DAG projections, and explain why this assumption is reasonable (or what its limitations are) beyond the brief mention in the conclusion.

## Score and Decision

<score>6.0</score>
<decision>Accept</decision>