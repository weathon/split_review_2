Now let me write the final consolidated review.

## Summary

This paper proposes SIGMADOCK, a diffusion-based generative model for molecular docking that replaces the standard torsional-angle parametrization with a fragment-based SE(3) representation. Ligands are decomposed into rigid-body fragments via a novel fragmentation reduction scheme (FR3D), and the generative process operates over SE(3) transformations of each fragment. The paper contributes soft triangulation constraints, an EquiformerV2-based architecture with SO(3)-equivariant prediction head, and extensive empirical evaluation showing 79.9% Top-1 PB-valid on PoseBusters — surpassing both prior deep learning methods and classical physics-based docking in the re-docking setting.

## Strengths

- **The fragment-based SE(3) formulation is well-motivated and tackles a genuine limitation of torsional models.** Section 2.2.2 clearly identifies that the induced Cartesian measure in torsional models is non-product, creating entangled dynamics and ambiguous gauge choices. Moving to SE(3) fragments gives a factorized product space, which is architecturally cleaner and should yield simpler score functions.

- **The quantitative results are genuinely strong.** Under the re-docking protocol with holo protein and PB train-test split, SIGMADOCK achieves 79.9% Top-1 PB-valid on PoseBusters. The ablation study (Table 1) is well-designed: each component (triangulation conditioning, protein-ligand interactions, fragment merging) is stripped out and shown to matter with clear relative improvements of 4-12%.

- **The per-sequence-similarity comparison with AF3 (Table 4) is genuinely informative.** SIGMADOCK achieves comparable overall PB-validity (79.9% vs 80.2%) with a fraction of the training data, and notably outperforms AF3 on the high-similarity bin (87% vs 78%) where memorization concerns are most relevant.

- **The ablation comparing sampling from M_b (bound fragments) vs M_c (RDKit conformer fragments) is honest and informative.** Config G (86.4% RMSD) vs the default (80.5%) quantifies exactly how much performance is lost to the RDKit approximation — a meaningful gap that future work could try to close.

- **The co-factor analysis (Table 2) provides a valuable sanity check:** failure rates are lowest on complexes with no co-factors (16.2%) and highest when natural ligands are present (41.2%), consistent with the model learning genuine physics rather than memorizing patterns.

## Weaknesses

### Fatal
None.

### Major

- **The Right Chart in Figure 4 reports Top-1 values of 51%, 53%, and 53% for the three sequence-similarity splits (≤0, 30-95, 95-100) of the PB set, yet Table 4 reports PB-Val values of 72%, 79%, and 87% for the same splits (with identical counts of 109, 76, 123).** The Right Chart values average to approximately 52%, which contradicts the stated overall Top-1 of 79.9% (PB-Val) or 80.5% (RMSD-only) from Table 1. The 20+ percentage point gap between the Right Chart and Table 4 for each bin cannot be explained by the difference between RMSD-only and PB-Val metrics (which differ by only 0.6 points in Table 1). This is a direct numerical inconsistency in the paper's central results that must be resolved. Either the Right Chart reports a different metric than advertised, or one set of numbers contains an error. Without resolution, the quantitative foundation of the per-sequence-similarity analysis is uncertain.

### Minor

- **The abstract's comparison statement is ambiguous about metrics.** The abstract compares SIGMADOCK's clearly stated PB-valid metric (79.9%) against "12.7-32.8% reported by recent deep learning approaches" without specifying whether those baseline numbers use PB-valid or RMSD-only. The 12.7% appears to be DiffDock's PB-valid rate, but the 32.8% is not clearly sourced, and the Left Chart in Figure 4 shows RMSD-only values for baselines (e.g., DiffDock at 38.0%, G2G at 58.1%) that fall outside this range. The body text partially clarifies, but the abstract is misleading in isolation.

- **No error bars or variance estimates are reported** despite multiple sources of stochasticity (diffusion sampling, stochastic FR3D fragmentation, Gaussian pocket jitter during training). While single-run evaluation is standard for large-scale docking benchmarks and the margins over baselines are large, variance estimates would strengthen the quantitative claims.

- **The "50× faster sampling" claim (line 194)** compares a docking model (SIGMADOCK) to a co-folding model (AF3) that generates full protein structures. These are very different inference pipelines, and the speed advantage is partly attributable to the different problem settings rather than architectural efficiency alone. This should be contextualized.

- **The RDKit conformer gap is described as "a small but expected decrease."** The 5.9-point gap between M_b (86.4%) and M_c via RDKit (80.5%) is meaningful — it defines how much performance is lost to the conformer proxy. While not the largest individual effect (triangulation conditioning contributes 8.6 points, fragment merging 6.1), this direction deserves more prominent discussion as an avenue for future work.

### Trivial
None.

## Nice-to-Haves
- Confidence intervals or variance estimates for Tables 1-4 and Figure 4 would further strengthen the paper.
- A more precise scope qualifier on the "first DL to surpass classical docking" claim could avoid potential misinterpretation (the paper already notes the re-docking setting, but the claim's framing in the abstract is quite broad).

## Removed Points
- **"RDKit gap is the largest source of error"** — REMOVED because factually incorrect. Triangulation conditioning (8.6-point drop) and fragment merging (6.1-point drop) are both larger effects than the M_b improvement gap (5.9 points). A corrected version is retained as a minor weakness.
- **Theorem 1 labeling criticism** — REMOVED as a style nitpick. The proof is provided in the appendix.
- **"First DL to surpass classical docking" scope critique** — REMOVED because the paper already qualifies this claim with "under the PB train-test split" (abstract) and "using the intended train-test split on the re-docking task" (body).
- **FR3D data augmentation determinism question, N_seeds for baselines, formatting nitpicks** — REMOVED as speculative, unverifiable, or parser artifacts.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Resolve the numerical inconsistency** between the Right Chart of Figure 4 (51/53/53) and Table 4 (72/79/87). Clarify what metric the Right Chart reports and ensure consistency with the stated overall Top-1 of 79.9%.
2. **Clarify the abstract's comparison range** (12.7-32.8%) by specifying the metric for both endpoints.
3. **Discuss the RDKit conformer gap more prominently** as a direction for future work rather than characterizing it as "a small but expected decrease."
4. **Contextualize the 50× speed comparison** by noting that it compares different inference pipelines (docking vs. co-folding).

## Score and Decision

This is a strong paper with a genuinely novel method, sound theoretical motivation, and impressive empirical results. The fragment-based SE(3) diffusion formulation is a meaningful departure from the torsional-model paradigm, and the ablation study, co-factor analysis, and AF3 comparison provide thorough support. However, the numerical inconsistency in Figure 4's Right Chart (51/53/53 vs. Table 4's 72/79/87) is a serious reporting issue that must be resolved before the results can be taken at face value. Given the strength of the method and the overall evidence, this is fixable, and the paper deserves acceptance conditional on this resolution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>