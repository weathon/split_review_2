## Summary

This paper introduces SIGMADOCK, a diffusion model for molecular docking that decomposes a ligand into rigid-body fragments by breaking rotatable bonds, then performs SE(3) diffusion on the fragment poses to generate bound conformations. The authors propose a fragmentation reduction scheme (FR3D) to reduce degrees of freedom, soft triangulation constraints to preserve bond geometry, and an architecture based on EquiformerV2 with virtual nodes and a Newton-Euler-style prediction head. They report state-of-the-art Top-1 success rates (RMSD<2Å PB-valid) above 79.9% on the PoseBusters benchmark, outperforming other deep learning methods trained on the same split.

## Strengths

- **Novel and well-motivated approach**: Decomposing a ligand into rigid fragments and diffusing over their SE(3) poses is a clever way to exploit chemical priors while avoiding the ill-conditioned inverse mapping from torsional angles to Cartesian coordinates. The motivation in Theorem 1 and the discussion of torsional-model drawbacks are conceptually sound.
- **Strong empirical results**: The Top-1 PB-valid success rate of 79.9% is substantially higher than the 58.1% reported for G2G and Vibe2, the next-best methods in the same figure, and represents a significant advance on the PoseBusters benchmark under the intended train-test split.
- **Comprehensive ablations**: Table 1 clearly shows the contribution of triangulation conditioning, fragment merging, protein-ligand interactions, and the ranking heuristic, helping to validate the design choices.
- **Data efficiency and generalisation**: The method achieves competitive performance with AlphaFold3 while using far less training data, and results across sequence-similarity splits demonstrate good generalisation beyond memorisation.

## Weaknesses

### Fatal

1. **False claim about being the first to surpass classical docking**. The paper states that SIGMADOCK is “the first deep learning approach to surpass classical physics-based docking under the PB train-test split.” However, Figure 4 shows that G2G and Vibe2 achieve 58.1% Top-1 on the same split, which already exceeds the 54.5% reported for the classical Vina baseline (Butenschoen et al. 2024). The paper omits classical docking results from its main comparison, making the claim unsubstantiated and likely incorrect. This misrepresentation undermines a core selling point of the paper.

2. **Inconsistent and misleading baseline numbers in the abstract**. The abstract states that prior deep learning approaches achieve 12.7–32.8% Top-1, yet Figure 4 reports 38.0% for DiffDock and 58.1% for G2G and Vibe2. The abstract’s range appears to cherry-pick only the weakest baselines, giving a false impression of the gap that SIGMADOCK closes.

### Major

3. **Ranking heuristic is not specified**. The paper uses a “simple and cheap heuristic” involving “pseudo binding energy” and “physicochemical checks” to rank samples. The exact form of the pseudo-energy, which checks are applied, and how they are combined are not described, making it impossible to assess the contribution of this ranking step to the reported Top-1 performance. Without this information, the results are difficult to reproduce or verify.

4. **Fragmentation reduction algorithm (FR3D) is under-described in the main text**. The stochastic search for merging fragments is described only at a high level; the algorithm itself is relegated to the appendix. Given that fragmentation is a core component of the method, the main paper should provide enough detail for readers to understand its operation and potential failure modes.

5. **Missing explicit comparison to classical physics-based docking**. The paper repeatedly claims to surpass classical docking but never includes Vina, Glide, or Smina in any figure or table in the main text. The only classical entry, labeled “PDBBind” (which is a dataset, not a docking engine), is ambiguous and uninformative.

### Minor

6. The label “PDBBind” in Figure 4 is misleading; PDBBind is a dataset, not a docking method. The authors should clarify which classical method is actually represented.
7. The claim that SIGMADOCK “does not require the use of a separately trained confidence model” is overstated, because the ranking heuristic effectively serves as a confidence model, even if it is simpler.
8. The term “soft triangulation constraints” could be confused with hard constraints; the description in Section 2.4 makes clear they are input features, but this distinction should be emphasised earlier.

### Trivial

None.

## Nice-to-Haves

- Provide a direct head-to-head table with classical methods (Vina, Glide) on PoseBusters alongside the deep learning baselines.
- Release the exact scoring heuristic for sample ranking to ensure reproducibility.
- Consider providing a deterministic variant of FR3D to guarantee replicability of the fragmentation step.

## Novel Insights

Beyond the paper’s own contributions, the analysis of why torsional diffusion models underperform—specifically the non-product induced measure and the non-local Cartesian displacements caused by local torsional changes—is a valuable conceptual insight. The idea of replacing that entangled representation with a product of independent fragment SE(3) spaces and letting the score model learn inter-fragment correlations is a clean architectural principle that may influence future molecular generative models.

## Suggestions

- Correct the false historical claim: SIGMADOCK is not the first deep learning method to surpass classical docking; G2G and Vibe2 already do. Instead, claim that SIGMADOCK achieves the highest Top-1 success rate on PoseBusters among methods trained on the same split.
- Revise the abstract baseline range to accurately reflect the numbers shown in Figure 4 (e.g., 38–58% for recent deep learning approaches).
- Move a succinct description of the ranking heuristic into the main text, or at least clearly state its components in the paper.

## Score and Decision

**Score**: 4

**Decision**: Reject

The paper presents a novel and empirically strong method, but the two fatal weaknesses—the false claim about being the first to surpass classical docking and the misleading baseline range in the abstract—undermine its credibility and cannot be overlooked. The contribution is otherwise significant, and with corrections to the claims and added clarity on the ranking heuristic, this work could become a strong accept. As submitted, however, these inaccuracies are severe enough to recommend rejection.

MY FINAL SCORE: 4.0</score>
MY FINAL DECISION: Reject</decision>