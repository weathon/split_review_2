## Summary

This paper introduces SIGMADOCK, an SE(3) Riemannian diffusion model for molecular docking that decomposes ligands into rigid-body fragments and learns to reassemble them within a protein binding pocket. The key innovation is a fragmentation scheme (FR3D) that reduces the degrees of freedom relative to both torsional and naïve fragment approaches, combined with soft triangulation constraints and an SE(3)-equivariant architecture. The authors claim state-of-the-art performance on the PoseBusters benchmark (79.9% Top-1 PB-valid), surpassing both prior deep learning methods and classical physics-based docking for the first time under the standard train-test split.

## Strengths

- **Strong empirical results**: The reported 79.9% Top-1 PB-valid success rate substantially outperforms prior deep learning methods (12.7-32.8% range) and even exceeds classical docking. The ablation studies systematically decompose contributions from key components.

- **Principled theoretical grounding**: The paper provides rigorous justification for fragment-based diffusion over torsional models, including Theorem 1 about non-product measures in torsional models, Lemma 1 about triangulation constraints, and Theorem 2 about equivariance. The analysis of why torsional models underperform (non-local Cartesian displacements, ambiguous extrinsic gauge, lever effect) is insightful.

- **Strong generalization evidence**: The breakdown by sequence similarity (Figure 4, right) and co-factor analysis (Table 2) convincingly demonstrates that the model learns genuine physics rather than memorizing training complexes. The performance on proteins with ≤30% sequence similarity (72% PB-valid) is particularly compelling.

- **Data efficiency**: Achieving AF3-level performance with only 19k training datapoints (versus AF3's massive dataset) is a meaningful practical contribution, especially for resource-constrained research groups.

## Weaknesses

### Major

- **Overclaiming relative to AlphaFold3**: The paper repeatedly claims "AF3-level performance" (e.g., "we reach AF3-level performance (Top-1 of 84%)"), but AF3 solves a fundamentally harder problem—co-folding with unknown protein structure and flexible receptor. SIGMADOCK uses the holo protein conformation (known bound structure) and a specified pocket. Comparing a rigid-receptor redocking method to a full co-folding method is apples-to-oranges. The paper acknowledges this briefly but continues to use the comparison as a headline result.

- **Missing computational cost analysis for inference**: The paper claims "50× faster sampling" than AF3 but does not report actual wall-clock times, GPU hours, or computational budget for SIGMADOCK inference. Given that 40 seeds are generated per complex, the actual cost may be non-trivial. Without concrete numbers, the speed advantage claim is unverifiable.

- **Unexplained discrepancy in sequence similarity results**: The right panel of Figure 4 reports Top-1 of 51%, 53%, and 53% across sequence similarity bins, yet Table 4 reports PB-Val of 72%, 79%, and 87% respectively. The paper does not explain why the Figure 4 values are dramatically lower than both the main result and Table 4. This inconsistency undermines confidence in the reported numbers.

- **Limited novelty in architecture**: The architecture is described as "EquiformerV2 augmented with virtual nodes," which is an incremental modification of existing work. The claimed innovations (hierarchical topology, tailored featurization, smooth distance cutoffs) are standard practices in graph neural networks for molecular modeling.

### Minor

- **The fragment reduction (FR3D) algorithm is under-explained**: While Figure 3 provides intuition, the actual algorithm (relegated to Appendix D.4) lacks crucial details: how merging decisions are made, how the stochastic search works, and how the irreducible set size $m$ is determined. The claim that $m \approx \frac{2}{3}\hat{m}$ is presented without statistical support.

- **Ranking heuristic not fully validated**: The paper uses a "simple and cheap heuristic" (pseudo binding energy + physicochemical checks) to rank samples, claiming it doesn't require a separately trained confidence model. However, the ablation (Table 1, Config D and E) shows removing either energy or PB scoring significantly degrades performance (67.2% and 70.8% PB-Val respectively, vs 79.9% full). This suggests the ranking heuristic is critical and not necessarily simpler than trained confidence models.

### Trivial

- The paper states "SIGMADOCK is the *first deep learning approach* to surpass classical physics-based docking under the PB train-test split," but this is difficult to verify definitively and may depend on which classical docking software and parameters are used as the baseline.

## Nice-to-Haves

- Reporting inference wall-clock time per complex (with GPU specification) would substantiate the speed claims.
- Including failure case analysis beyond co-factor presence (e.g., ligand flexibility, pocket size extremes) would strengthen the characterization of limitations.
- Providing the full distribution of RMSD values (not just Top-1 success rate) would give a more complete picture of performance.

## Novel Insights

Beyond the paper's own contributions, an interesting insight is that the failure mode analysis (Table 2) reveals the critical role of co-factors in docking performance. Complexes with natural ligands fail at 41.2%, while those with no co-factors succeed at 84.2%. This suggests that current deep learning docking benchmarks may systematically overestimate performance because many test complexes involve multi-body interactions that are treated as pairwise protein-ligand problems. The paper's hypothesis that these failures are due to partial observability is well-supported and has implications for how the community should design future benchmarks.

## Suggestions

- Resolve the discrepancy between Figure 4 (right) sequence similarity results and Table 4. If these measure different things (raw RMSD vs. PB-valid), state this clearly and explain why they differ so dramatically.
- Remove or substantially qualify the AF3 comparison, or add a co-folding variant of SIGMADOCK to make the comparison fair.
- Report actual compute times for SIGMADOCK inference (e.g., seconds per complex on an A100) and clearly state the total compute required for 40 seeds.

## Score and Decision

The paper presents a well-motivated and technically sound approach that achieves strong empirical results. The theoretical justification for fragment-based diffusion over torsional models is compelling, and the generalization analysis is thorough. However, the overclaiming relative to AlphaFold3 (which solves a harder problem) and the unexplained discrepancy in sequence similarity results are significant issues that undermine confidence. The architectural contributions are incremental.

Given the genuine empirical advances but the presence of concerning overclaims and data inconsistencies, this is a borderline case that could go either way depending on the author response.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>