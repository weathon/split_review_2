## Summary

This paper proposes using Graph Attention Networks (GATs) as the policy representation for co-evolving morphology and control in soft robots within the EvoGym benchmark. The key contributions are: (a) a graph-based policy representation that naturally handles variable-size inputs caused by morphological mutations, (b) a MAPWEIGHTS procedure for transferring trained controllers across morphological changes via topology-consistent weight mapping, and (c) empirical comparisons against MLP-based co-design baselines on four EvoGym tasks.

## Strengths

1. **Well-motivated problem.** The paper correctly identifies that morphological mutation breaks fixed-size MLP policies, making controller inheritance fragile (Section 1). This is a genuine obstacle that limits the scalability of evolutionary robot co-design.

2. **Principled inheritance scheme.** The MAPWEIGHTS procedure (Algorithm 2) cleanly handles parameter transfer: GAT message-passing layers are fully inherited, the MLP output head is remapped actuator-by-actuator based on spatial correspondence, and new actuators get random initialization. This is more structured than the ad-hoc transfer rules required by MLP-based approaches.

3. **Clear presentation of algorithms.** Algorithm 1 (co-design loop) and Algorithm 2 (MAPWEIGHTS) are presented clearly, and the relationship to prior work (Bhatia et al. 2021; Harada & Iba 2024) is explicitly stated.

## Weaknesses

### Fatal
None.

### Major

1. **Missing ablation: GAT without inheritance.** The paper compares four methods: GA-GAT-PPO-Global-Transfer, GA-GAT-PPO-Local-Transfer, GA-MLP-PPO-Transfer (Harada & Iba 2024), and GA-MLP-PPO (Bhatia et al. 2021, no inheritance). There is no GA-GAT-PPO without inheritance (training from scratch each generation). The paper's contribution bullet claims "ablations isolating the effects of graph policies and inheritance" (line 31), but this critical ablation is absent. Without it, the source of improvement is ambiguous: gains could come from (a) the GAT encoder's ability to handle variable input sizes, (b) the MAPWEIGHTS inheritance scheme being more effective than the MLP inheritance scheme from Harada & Iba (2024), or (c) both. This is the most consequential gap in the evaluation.

2. **Weak statistical evidence.** All results are averaged over only 3 independent runs (line 170), with no statistical significance tests reported. In evolutionary robotics, variance across seeds is typically high due to randomness in GA mutation, PPO training, and environment interactions. With n=3, confidence intervals on the reported standard deviations are wide. On Carrier-v1, all methods reach similar fitness, so the headline claim of superiority rests on the other three tasks with n=3 per task. This level of evidence is insufficient for confident conclusions.

### Minor

3. **Architecture/narrative mismatch.** The paper frames the GAT controller as enabling "actuators to act locally" with a "decentralized structure" (line 108). However, the actual architecture (lines 140–141) pools all per-node GAT outputs into a single averaged vector before a lightweight MLP head produces all actuator commands. Every actuator command is decoded from the same global pooled vector, not from local per-node representations. The controller is best described as a global policy with a graph-based encoder, not a decentralized one. The real advantage over MLPs is that the GAT encoder handles variable-size inputs naturally — this is the correct framing, and the "decentralized" narrative overstates the architecture.

4. **Underspecified node correspondence in MAPWEIGHTS.** Algorithm 2 (line 117) states "Compute node correspondence by spatial matching" without explaining how this matching is done. In EvoGym, robots are defined on a 2D grid; it matters whether matching is by grid coordinates, by voxel index, or by some other criterion, and what happens when voxels shift positions or are inserted/deleted. This needs a concrete description for reproducibility.

5. **Fitness definition may conflate speed and quality.** Line 87 defines fitness as the "best episodic return" during PPO training rather than final or mean performance. A method that spikes early could appear better than one that converges to a higher stable performance. This choice is not discussed or justified.

6. **Missing GAT-specific hyperparameters.** The paper adopts GA/PPO hyperparameters from Harada & Iba (2024) (line 160) but does not specify GAT-specific architectural details: hidden dimension, number of attention heads, MLP head depth/width, or whether these were re-tuned for the GAT architecture. These are not inherited from an MLP-based prior work and are needed for reproducibility.

### Trivial

7. **Algorithm 1 typo:** Line 83 loops `g = 1 ... p` (population size) where it should be `g = 1 ... n` (max generations).

---

## Nice-to-Haves

- A GCN (without attention) baseline would isolate the contribution of the attention mechanism; a Transformer policy motivated by the paper's own discussion of Kurin et al. (2021) would further strengthen the evaluation.
- Quantifying the convergence speed differences that the paper qualitatively acknowledges in Section 7 would be informative.

## Removed Points

- The reviewer's criticism about attention being "effectively uniform" in the Global variant is weakened: edge features include relative offsets (Δx, Δy), which could differentiate edges even when node features are identical, depending on the GAT implementation. The broader point about unclear naming stands and is retained as Minor #3.
- The criticism about a missing Transformer baseline is moved to Nice-to-Haves, as the paper's stated scope is comparing GNN-based vs MLP-based co-design.
- The criticism about slow convergence not being quantified is removed; the paper honestly acknowledges this limitation and quantifying it is a secondary concern.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a GA-GAT-PPO-no-transfer condition** to disentangle the contribution of the GAT encoder from the MAPWEIGHTS inheritance scheme. This is the single highest-leverage improvement.
2. **Run experiments over at least 10 seeds** and report confidence intervals or statistical significance tests.
3. **Specify the node correspondence procedure** in Algorithm 2 concretely, and report all GAT-specific hyperparameters (hidden dim, number of attention heads, MLP head architecture).
4. **Reframe the contribution** around handling variable-size graph-structured inputs rather than "decentralized control," which better matches the actual architecture.
5. **Justify the "best episodic return"** fitness measure or switch to final/mean return.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>