## Summary

This paper addresses a real problem in soft-robot co-design: when morphology mutates, a controller's I/O dimensions change, breaking fixed-topology MLP policies. The authors propose representing voxelized soft robots as graphs and using a Graph Attention Network (GAT) as the policy backbone, with a structured weight-inheritance procedure (MAPWEIGHTS) that maps parameters from parent to offspring controllers when morphology changes. The method is evaluated on four EvoGym tasks against two MLP-based baselines. While the core idea is well-motivated and the MAPWEIGHTS mechanism is clearly described, the experimental design has a significant gap between the paper's claims and the evidence provided.

## Strengths

1. **Well-motivated problem with a clear impediment identified.** The paper correctly pinpoints a genuine challenge: as robot morphology evolves, sensor/actuator layouts change, breaking the fixed-input assumption of MLP policies. This obstacle is acknowledged in prior work (Bhatia et al. 2021; Harada & Iba 2024) but not fully resolved there.

2. **Sensible architectural choice.** Representing voxelized robots as graphs and using a GAT as the policy backbone is a natural fit. The design — GAT → global pooling → lightweight MLP head → per-actuator outputs — is reasonable for handling varying node counts while maintaining permutation-aware processing.

3. **Clearly specified inheritance mechanism.** Algorithm 2 (MAPWEIGHTS) provides concrete, implementable rules for copying shared GAT layers, transferring MLP hidden layers intact, mapping matched actuators, and randomly initializing new ones. This is the paper's most tangible contribution.

4. **Standardized evaluation platform.** The paper evaluates on four tasks from EvoGym, a recognized benchmark, against two relevant baselines: GA-MLP-PPO (no transfer, Bhatia et al. 2021) and GA-MLP-PPO-Transfer (with inheritance, Harada & Iba 2024).

## Weaknesses

### Fatal
None.

### Major

1. **Claimed ablations do not exist as described, conflating architecture and inheritance effects.** The paper states as a contribution "Empirical validation … with ablations isolating the effects of graph policies and inheritance" (line 31). However, the experimental design compares:

   | Method | Policy Architecture | Inheritance |
   |--------|-------------------|-------------|
   | GA-GAT-PPO-{Global,Local}-Transfer (Ours) | GAT | MAPWEIGHTS |
   | GA-MLP-PPO-Transfer (baseline) | MLP | Harada & Iba (2024) |
   | GA-MLP-PPO (baseline) | MLP | none |

   This confounds two variables. There is no **GA-GAT-PPO without inheritance** (which would isolate the GAT architecture's effect) and no **MLP with MAPWEIGHTS-like structured transfer** (which would test whether the mapping procedure itself aids MLPs). The paper repeatedly attributes gains to "attention" and "graph-structured policies," but the evidence cannot uniquely support that attribution — the observed improvements could come from the GAT's inductive bias, the MAPWEIGHTS mapping rules, the GAT having different capacity, or any combination. This gap between the claimed contribution and the experimental design is the paper's most significant weakness.

### Minor

2. **Under-specified architectural details.** The paper states "the resulting graph is processed by a GAT layer" (line 140, singular — is this literally 1 layer?), with no specification of: number of attention heads, GAT hidden dimension, MLP head size/layers/width, learning rate, PPO clip parameter, number of PPO update steps per generation, or number of environment episodes per generation. Hyperparameters are deferred to Harada & Iba (2024), which specified MLP hyperparameters, leaving unclear whether GAT parameters were matched in capacity to the MLP baselines. This hinders both reproducibility and fair comparison.

3. **Node correspondence in Algorithm 2 is underspecified.** Line 117 reads "Compute node correspondence C: V_k → V_u ∪ {∅} by spatial matching" but does not state how this matching is computed — by grid coordinates? IoU of voxel positions? Nearest-neighbor in 2D? Since an incorrect correspondence would break the entire weight mapping, this detail is essential.

4. **Limited statistical support.** Results are averaged over 3 independent runs (lines 170, 174) with no statistical significance tests or effect sizes reported. The shaded regions in Figure 3 show non-trivial variance, especially for the MLP baselines. While 3 runs is not unusual in evolutionary robotics, the absence of any significance testing weakens the reliability of the comparisons, particularly when the variance bands overlap in parts of the Carrier-v1 and Catcher-v0 plots.

5. **Algorithm 1 pseudocode contains a typo in the loop header.** Line 83 reads `for g = 1 ... p` where `p` is the population size, but the Require statement (line 81) specifies max generations as `n`. The loop should iterate over generations (`g = 1 ... n`), not population size.

### Trivial

6. **Node feature description for Global-Transfer is ambiguous.** Line 136 says "node features are averaged and assigned uniformly to all nodes" without specifying what is being averaged (all sensor readings across the robot? some subset?), making this design choice unclear at first read.

## Nice-to-Haves

- **Add a GA-GAT-PPO (no transfer) baseline** — training GAT controllers from scratch on each new morphology — to isolate the GAT architecture's effect from the inheritance mechanism.
- **Apply MAPWEIGHTS-like structured transfer to an MLP baseline** to test whether the mapping procedure alone helps MLPs, which would clarify whether graph-structured policies are the driver.
- **Compare against a Transformer or other permutation-invariant architecture** (e.g., from Kurin et al. 2021) to test whether the graph inductive bias specifically matters.
- **Report statistical significance or confidence intervals** for the main results.
- **Specify the node correspondence method** in Algorithm 2 (grid coordinate matching, IoU, or other).
- **Provide a table of exact architectural dimensions** (GAT layers, heads, hidden sizes, MLP head widths, total parameter counts) for both GAT and MLP policies.
- **Report computational cost** (training time per generation or total).

## Removed Points

These points from the input are removed with brief justifications:

- **"No GAT-vs-other-graph-policy comparison"** — De-scoped as a nice-to-have. The paper's contribution is GAT-vs-MLP in this specific co-design setting, not GAT-vs-all-architectures. The critic's suggestion to compare against NeuroNet, Transformers, etc. demands work outside the paper's stated scope.
- **"Global-Transfer variant is not truly a graph-structured policy"** — The paper transparently presents both Global and Local variants and describes how each works. This is a design observation, not a weakness; it does not invalidate any result.
- **"Section 7 — GAT controllers don't converge as quickly means MLP baselines may be undertrained"** — Speculative claim by the reviewer, not a verifiable weakness in the paper. The paper honestly acknowledges this trade-off.
- **"Section 5.3 — morphology convergence raises questions about persistence under more diverse search"** — Speculative; the paper reports the observation factually.
- **"Section 6.2 — should compare against Transformer baseline"** — Scope creep; duplicate of the removed "no GAT-vs-other" point.
- **Section-by-section notes about mutation-only design, single-seed values in Section 5.2 (used for qualitative illustration), and parser artifacts** — Either factual notes with no evaluative force or parser issues that do not affect the paper's substance.
- **"3 runs is insufficient" stated as a definitive judgment** — Weakened to "limited statistical support" since 3 runs is standard practice in this sub-field; the valid concern is the absence of significance testing, not the run count itself.

## Novel Insights

None beyond the paper's own contributions. The reviewers' input does not surface a novel framing, alternative interpretation, or cross-connection that the paper itself does not already contain or imply.

## Suggestions

1. Add the two missing ablations (GAT-without-inheritance, MLP-with-structured-transfer) to genuinely isolate the effect of graph-structured policies from the inheritance mechanism, as claimed in contribution 3.
2. Provide a full architectural specification table and clarify the node correspondence matching in Algorithm 2.
3. Report confidence intervals or statistical significance for the main results to strengthen the empirical case.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>