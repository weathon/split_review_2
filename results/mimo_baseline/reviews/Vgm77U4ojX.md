## Summary
The paper introduces SIGMADOCK, a fragment-based SE(3) Riemannian diffusion model for molecular docking that decomposes ligands into rigid-body fragments, learns to reassemble them within the binding pocket via SE(3) diffusion, and achieves state-of-the-art performance on the PoseBusters benchmark—reporting 79.9% Top-1 success (RMSD < 2Å and PB-valid) compared to 12.7–32.8% by recent deep learning approaches, and being the first DL method to surpass classical physics-based docking under the intended train-test split.

## Strengths
- **Strong theoretical motivation with formal results.** Theorem 1 rigorously establishes why torsional models produce entangled, non-product induced measures, whereas fragment-based SE(3)^m diffusion factorises cleanly. This provides a principled justification for the core design choice rather than a purely empirical one. Theorem 2 proves coordinate-frame invariance, ensuring the model is well-defined regardless of local coordinate choices.

- **State-of-the-art empirical results with rigorous evaluation.** SIGMADOCK achieves 79.9% Top-1 PB-valid on PoseBusters, a ~6.3× improvement over DiffDock under fair comparison (same train-test split, same data). The paper also demonstrates consistent generalization across sequence similarity splits (Table 4), robustness to pocket size variations (Table 3), and systematic failure analysis by co-factor presence (Table 2), providing convincing evidence that the model learns meaningful physics rather than memorizing poses.

- **Well-designed fragmentation pipeline (FR3D) with clear ablations.** The stochastic merging strategy reduces fragments from k+1 to roughly ⅔(k+1), lowering degrees of freedom. The ablation study (Table 1) cleanly isolates contributions: removing triangulation conditioning drops PB-valid by ~13%, removing fragment merging drops it by ~6%, confirming each component's importance. The soft triangulation constraints via Lemma 1 provide additional geometric priors without restricting torsional freedom.

- **Data efficiency and computational advantages.** The authors highlight that SIGMADOCK reaches AF3-level performance (79.9% vs ~80.2% PB-valid) using only 19k training examples, with ~50× faster inference and significantly lower train-test leakage (Appendix J). This makes the method practical for high-throughput virtual screening, unlike co-folding models.

## Weaknesses
### Fatal
None identified.

### Major
- **Constrained experimental setting limits practical impact claims.** The method assumes rigid receptor, known binding pocket, and holo-conformation—substantially simpler than the blind docking and flexible receptor scenarios encountered in real drug discovery pipelines. While the authors are transparent about this choice and frame it as a deliberate first step, the paper's strong claims about "feasibility of deep learning for molecular modelling" and "accelerating drug discovery" need qualification. The 79.9% Top-1 result applies only to this restricted setting, and it is unclear how performance degrades when these assumptions are relaxed.

- **Reliance on RDKit conformers as the stationary distribution.** The method samples initial fragment poses from π_{Mc} (ETKDGv3 conformers). While the alignment analysis in Section 2.2.1 justifies this empirically, the quality of RDKit's conformer generation for diverse drug-like molecules is variable, and the model's performance is implicitly bounded by this upstream component. The paper does not quantify how sensitive final results are to the quality of the initial conformer ensemble.

### Minor
- **Heuristic ranking instead of a trained confidence model.** The paper proposes using pseudo binding energy and physicochemical checks to rank samples (Appendix F), which is simple and effective. However, this choice means the ranking quality depends on the fidelity of these heuristics, and a learned rescoring model (as used by DiffDock) might further improve Top-1 performance. The ablation showing 82.1% vs 79.9% with/without PB scoring (Table 1, rows E vs I*) suggests the heuristic contributes significantly, but it is unclear whether this generalizes to molecules outside the training distribution.

- **The right panel of Figure 4 appears inconsistent with Table 4.** The sequence similarity splits in Figure 4 show Top-1 values around 51–53%, while Table 4 shows PB-valid of 72–87% for similar splits. This likely reflects different metrics (RMSD-only vs PB-valid) or different split definitions, but the discrepancy could confuse readers.

### Trivial
None beyond parser artifacts.

## Nice-to-Haves
- A comparison of inference wall-clock time per complex against DiffDock and Vina would make the computational advantage claims more concrete.
- Analysis of how performance scales with ligand size/number of fragments would help assess practical boundaries of the approach.
- Discussion of failure cases with specific examples (beyond aggregate co-factor analysis) would strengthen the error analysis.

## Novel Insights
The paper's theoretical contribution—showing that torsional diffusion produces non-product induced measures while fragment-based SE(3)^m diffusion factorises (Theorem 1)—is a genuinely novel insight that goes beyond the empirical contribution. This observation suggests a fundamental reason why torsional models have underperformed despite their dimensional efficiency, and it reframes the design space for diffusion-based molecular generative models. The practical consequence—that simpler score functions and more stable sampling dynamics arise from fragment-space diffusion—is well-supported by the experimental results.

## Suggestions
- Expand the failure case analysis with visual examples showing when and why the model fails, particularly for the co-factor cases (natural ligands with 41.2% failure rate).
- Include a brief discussion of how the method would extend to blind docking (unknown pocket) and flexible receptor scenarios, with preliminary experiments if feasible.
- Clarify the discrepancy between Figure 4 right and Table 4 for readers unfamiliar with the metrics.

## Score and Decision
This is a well-executed paper with strong theoretical grounding, novel methodological contributions (FR3D, triangulation conditioning, fragment SE(3) diffusion), and impressive empirical results that establish a new state of the art under fair evaluation conditions. The main limitation is the constrained (rigid-receptor, known-pocket) experimental setting, but the authors are transparent about this and the contributions within this setting are substantial. The theoretical analysis of torsional vs. fragment diffusion is a valuable conceptual advance for the field. I recommend acceptance.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: Accept