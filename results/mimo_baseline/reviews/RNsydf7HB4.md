## Summary

The paper proposes GAMA, a learning-to-improve (L2I) framework for the Capacitated Vehicle Routing Problem (CVRP) that formulates adaptive operator selection as a Markov Decision Process. The key contribution is a Dual-GCN encoder that separately encodes the problem instance graph and the evolving solution graph, followed by self- and cross-attention layers with a gated fusion mechanism to produce rich state representations for a PPO-based operator selection policy. Experiments on synthetic CVRP instances (N=20, 50, 100) and out-of-distribution benchmarks show improvements over neural baselines, with ablation studies validating each architectural component.

## Strengths

- **Well-motivated problem and clear framework**: The paper clearly identifies two limitations of existing AOS methods for VRP—coarse-grained state representations and naive feature concatenation—and proposes a structured solution. The MDP formulation is complete, with well-defined states, actions, rewards, and transitions (Section 3.2).

- **Comprehensive experimental evaluation**: The paper compares against a broad set of baselines including classical solvers (LKH3, HGS, VNS), L2C methods (POMO, LEHD, ReLD), and L2I methods (DACT, L2I), across three problem sizes with 30 independent runs and Wilcoxon rank-sum significance testing. The results on CVRP100 with T=20k are particularly strong: GAMA achieves 15.6510 avg cost vs. 15.6925 for DACT and 15.7334 for L2I, beating even HGS (15.6994).

- **Well-designed ablation studies**: Table 2 cleanly isolates the contribution of cross-attention (GAMA vs. GENIS) and gated fusion (GAMA vs. GAMA_NG), with statistical significance testing. Figure 2 further shows that GAMA exhibits lower variance and better median performance across all inference budgets, supporting the stability claims.

- **Generalization results**: Table 3 demonstrates meaningful zero-shot generalization to the Uchoa et al. benchmark (N=100–1000) without retraining, achieving 4.956% avg gap vs. 5.018% for ReLD and much worse for DACT (25.305%) and L2I (13.557%). This is a practical and important capability.

## Weaknesses

### Fatal
None.

### Major

- **Incremental novelty over existing work**: The individual components—GCN encoding, self-attention, cross-attention, and gated fusion—are all well-established in the deep learning literature. The paper's nearest relative, GENIS (Guo et al., 2025), already employs dual-GCN encoding for the same problem setting. GAMA's primary additions are cross-attention between the two GCN branches and a gated fusion mechanism. While these additions yield empirical improvements, the paper does not provide a compelling argument for why this particular assembly of standard components constitutes a significant conceptual advance rather than an engineering refinement. The "multi-modal" framing is somewhat stretched, as the two graph representations are different views of the same data rather than truly heterogeneous modalities.

- **Name inconsistency / possible copy-paste error**: Section 4.1 states "Table 5 in the appendix gives the parameter settings of the proposed **GENIS**," but GENIS is the baseline from Guo et al. (2025), not the proposed method. This should read "GAMA." This error, while likely typographical, raises concerns about care in manuscript preparation.

- **Missing baseline in results**: The compared algorithms section lists GIRE (Ma et al., 2023) as a baseline, but GIRE does not appear in Table 1. If results were obtained, they should be reported; if not, the mention should be removed. Similarly, Hottung et al. (2025) is referenced but not compared. This weakens the claim of comprehensive evaluation.

### Minor

- **Marginal improvements on small instances**: On CVRP20 with T=20k, GAMA achieves 6.0810 avg vs. L2I's 6.0820—a difference of 0.001, which is practically negligible. The paper would benefit from discussing where the approach provides the most value (i.e., larger instances) rather than uniformly claiming superiority.

- **Coarse reward signal**: All operators within an improvement phase receive the identical reward (the cost reduction over the entire phase), which provides no credit assignment to individual operator selections. While this follows prior work (Lu et al., 2019), a discussion of how this affects learning efficiency—especially given the long training times (7 days for N=100)—would strengthen the paper.

- **Computational cost discussion**: Training requires 1–7 days depending on problem size, and inference at T=20k takes ~19 minutes for CVRP100. The paper could more explicitly discuss the practical trade-off between solution quality improvement and computational overhead, particularly compared to fast L2C methods like ReLD (0.72s for N=100).

- **Sensitivity to hyperparameter L**: The shake procedure triggers after L consecutive non-improving iterations, but no sensitivity analysis is provided for this parameter. Given that it directly controls the exploration-exploitation balance, understanding its impact would be valuable.

### Trivial
None beyond parser artifacts.

## Nice-to-Haves

- A wall-clock time vs. solution quality Pareto analysis comparing GAMA against baselines would help practitioners assess the practical value of the approach.
- Analysis of which operators are selected most frequently and how the policy adapts across different problem instances.
- Extension to other VRP variants (e.g., VRPTW, MDVRP) to demonstrate broader applicability.

## Novel Insights

The paper's most notable observation is that encoding the problem instance and evolving solution as separate graph modalities and explicitly modeling their cross-modal interactions via attention yields substantially better state representations for operator selection than either treating them independently (GENIS) or fusing them naively. The gated fusion mechanism further demonstrates that adaptive, learned integration of cross-modal signals outperforms simple summation, particularly on larger and out-of-distribution instances. While these are incremental insights relative to the broader attention and GNN literature, the empirical demonstration of their effectiveness in the AOS context for VRP is a genuine contribution.

## Suggestions

- Resolve the GENIS/GAMA naming error in Section 4.1 and include or remove the GIRE baseline from the compared algorithms.
- Add a dedicated subsection discussing computational cost trade-offs and scenarios where GAMA is most practically useful.
- Consider including a reward shaping or per-operator reward assignment mechanism to improve learning efficiency and reduce training time.

## Score and Decision

The paper presents a technically sound method with solid experimental results, particularly on larger instances and out-of-distribution generalization. The ablation studies are well-designed and convincing. However, the novelty is incremental—primarily assembling well-known attention components into a coherent framework for a specific problem setting—without a deep conceptual insight that would significantly advance the field. The improvements, while consistent, are sometimes marginal on small instances. The editorial issues (naming error, missing baseline) are concerning but not disqualifying. Overall, the paper sits at the borderline: it would be a reasonable contribution to a workshop or second-tier venue, but the incremental novelty makes it a stretch for ICLR.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>