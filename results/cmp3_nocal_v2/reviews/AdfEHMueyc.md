## Summary

This paper proposes a graph-based approach for the co-design of morphology and control in soft robots. The key idea is to represent each robot as a graph and use a Graph Attention Network (GAT) as the policy architecture, which naturally accommodates varying numbers of sensors and actuators across generations. The MAPWEIGHTS inheritance procedure transfers learned parameters from parent to offspring morphologies by reusing shared GAT layers, copying matched actuator weights, and randomly initializing new ones. The method is evaluated on four EvoGym tasks against MLP-based baselines with and without inheritance.

## Strengths

- **Well-motivated problem framing.** The paper clearly identifies a structural limitation in prior co-design work: MLP policies have fixed input/output dimensions, so when morphology mutates (adding/removing actuators), inherited parameters become misaligned or unusable. Representing robots as graphs processed by GNNs is a natural and principled fix (Section 1, lines 15–16).

- **Clean inheritance mechanism (Algorithm 2).** The MAPWEIGHTS procedure is clearly described: shared GAT message-passing layers are copied in full, MLP hidden layers are transferred intact, and per-actuator output weights are matched, randomly initialized, or discarded based on correspondence. The critic inheritance is handled consistently. This gives a clean algorithmic specification of how knowledge transfers across changing morphologies.

- **Two node-feature variants (Global vs. Local).** The paper investigates both a shared mean representation and individualized node features, and finds that different tasks favor different designs (Section 5.1). This is a useful empirical observation that goes beyond a single "ours vs. baseline" comparison.

## Weaknesses

### Fatal
None.

### Major

- **Insufficient statistical evidence for strong comparative claims.** The paper reports results over only *three independent runs* per condition (lines 170, 174). No statistical significance tests are reported, and with three runs, standard deviation estimates are very noisy. Nonetheless, the paper makes definitive comparative claims: GAT variants "consistently match or surpass" MLP baselines, show "reduced variance," and achieve "higher peak fitness." For example, on Carrier-v1 all methods converge to similar fitness, yet the paper still claims GAT shows gains in "robustness" — a claim about variance that is precarious with n=3. At a top venue, this level of replication is too low to support the strength of the claims made.

- **Missing ablation: GAT without inheritance.** The paper's central claim involves two components: (i) GAT-based policies as a flexible architecture, and (ii) the MAPWEIGHTS inheritance mechanism. The paper claims to provide "ablations isolating the effects of graph policies and inheritance" (line 31), yet there is no condition where GAT policies are trained from scratch each generation (no inheritance). The comparison GA-GAT-PPO-* vs. GA-MLP-PPO-Transfer partially isolates architecture, but the comparison GA-GAT-PPO-* vs. a hypothetical GAT-without-inheritance would isolate the effect of inheritance *for GAT specifically*. This ablation is absent, making it impossible to determine how much of the improvement comes from the GAT architecture itself versus the inheritance mechanism.

- **Critical implementation details absent, hindering reproducibility.** Several details necessary to reproduce the method are missing or underspecified:
  - **Spatial matching (Algorithm 2, line 1):** The procedure "Compute node correspondence C by spatial matching" is the core of the inheritance mechanism, but the paper never explains how correspondences are determined when voxels are added, removed, or changed. This is not a minor detail — the quality of inheritance depends on it.
  - **GAT architectural hyperparameters:** Number of attention heads, hidden dimension sizes for GAT layers and the MLP head, number of MLP head layers, and the exact node feature vector dimensionality (beyond listing "coordinates, voxel type, and velocity" at line 71) are not reported.
  - **BUILDGRAPH procedure (Algorithm 1, line 15):** How a morphology is converted to a graph (node and edge construction from the 2D voxel grid) is never described.
  - While GA and PPO hyperparameters are cited from Harada & Iba (2024), the GAT-specific choices are the authors' own and must be specified.

- **Single GAT layer may limit receptive field for coordinated behaviors.** The paper states the graph is processed by "one attention-based message passing round" (line 140). With a single GAT layer, each node's representation is based only on its immediate neighbors. For tasks the paper itself describes as requiring "rapid, system-wide synchronization" (Catcher-v0, line 180), it is unclear how one-hop messages provide sufficient global coordination. The paper provides no analysis of receptive field or discussion of whether deeper GAT layers would improve results.

### Minor

- **No comparison against non-attention GNNs to support attention-specific claims.** The paper claims GATs offer "an additional advantage by learning attention weights that highlight the most relevant connections" (line 108), yet never compares against a simpler GNN variant (e.g., GraphConv, GCN). Without this comparison, the specific benefit of *attention* over generic message passing is not empirically supported.

- **Algorithm 1 contains an error.** Line 83: `for g = 1 ... p` should be `for g = 1 ... n` (the outer loop iterates over generations, not population size). While the intended meaning is clear, this error in a central algorithm description is concerning.

- **Single-seed visual comparison in Section 5.2.** The specific fitness scores (6.079, 6.258 vs. 3.268, 3.353) for Thrower-v0 are presented "under the same seed" (line 188), but only one seed is shown with no justification for why this seed is representative. This amounts to a single qualitative example.

- **Limited task scope.** The evaluation covers only 4 tasks from a single benchmark (EvoGym). While this is not a fatal limitation, it constrains the generality of the conclusions.

### Trivial
None.

## Nice-to-Haves

- **Computational cost comparison.** GATs are more expensive than MLPs. The paper acknowledges slower convergence (line 230) but provides no runtime, FLOPs, or wall-clock comparison — information that would help practitioners assess the practical trade-off.
- **Inheritance success rate analysis.** The paper could report what fraction of inherited controllers improve after fine-tuning versus regress, which would illuminate when MAPWEIGHTS works well.
- **Ablation of generations or population size.** The paper adopts these from prior work without investigating sensitivity.

## Removed Points

These points were raised in the input review but are removed per filtering rules:

- **"We address this by develop" grammatical issue (line 9):** This is a parser artifact, not an author error. Removed.
- **Missing appendix content:** The parser strips appendices; the original submission contains them. Removed.
- **Claims about "not yet released" references:** No such claims present in the input review. N/A.

## Novel Insights

Beyond the paper's own contributions, the reviews surface a few notable observations: (i) the honest finding in Section 5.3 that terminal morphologies are "broadly similar" across methods suggests the controller architecture mainly affects *how efficiently* the morphology is reached, not *which* morphology emerges — this somewhat qualifies the paper's framing but is candidly reported; (ii) the two-feature-variant analysis reveals a genuine task-dependent trade-off (local features for part-level coordination vs. global features for whole-body coordination) that could guide future GNN design in co-design settings.

## Suggestions

1. **Run at least 10–20 independent seeds per condition** and report confidence intervals or effect sizes to make the comparative claims statistically meaningful.
2. **Add the missing GAT-without-inheritance ablation** to isolate the effect of MAPWEIGHTS for GAT policies specifically.
3. **Add a non-attention GNN baseline** (e.g., GraphConv or GCN with the same inheritance procedure) to test whether attention-specific claims are supported.
4. **Specify all missing architectural details**: number of attention heads, hidden dimensions, node feature dimensionality, the spatial matching procedure, and the BUILDGRAPH construction. These are essential for reproducibility.
5. **Fix the Algorithm 1 loop bound** (`for g = 1 … n`).
6. **Consider analyzing whether one GAT layer provides sufficient receptive field**, or test deeper architectures.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>