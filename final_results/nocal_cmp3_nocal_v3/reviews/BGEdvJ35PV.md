## Summary

This paper identifies a structural problem in molecular diffusion models: molecular data distributions have narrow, densely packed probability peaks (dense-concentrated structure, formalized in Definition 3.1), making diffusion fragile because even small errors can overshoot valid regions (Equation 7) and become unrecoverable. The authors propose **DIST**, a model-agnostic corrective sampling method that runs a pilot inference on candidate batches, filters out trajectories likely to produce invalid molecules, and steers the intermediate distribution toward valid regions. Experiments across EDM, GeoLDM, and RADM on QM9 and GEOM-Drugs show consistent improvements in stability and validity, with reduced computational cost.

## Strengths

- **Well-motivated problem with clear analysis.** The paper identifies a genuine structural property — narrow, densely packed probability peaks in molecular configuration space — and connects it to a concrete failure mode of diffusion models via the overshoot condition in Equation 7 (`β_t · Δ/σ_*² > cσ_*`). Figure 1 provides an intuitive illustration contrasting molecular vs. image distributions, and the analysis around overlap regions and score-field ambiguity is grounded and sensible.

- **Universal and convincing empirical improvements.** Table 2 shows DIST improves atom stability, molecule stability, validity, and validity×uniqueness across all three backbone models on QM9, with standard deviations reported over three runs. The gains on molecule stability are substantial (EDM: 82.0→89.9, GeoLDM: 89.4→93.4, RADM: 87.3→91.4). Demonstrating improvement across GNN-based, Transformer-based, equivariant, and latent-space models supports the claim that the DC-structure issue is architecture-independent.

- **Transparent efficiency reporting.** The average timestep counts in Table 3 (e.g., 556.1 for EDM+DIST on QM9) reflect the actual aggregate cost including pilot-run overhead, not just a best-case theoretical reduction. The ablation in Table 4 further reports quality–cost tradeoffs across different pilot sizes, providing practical guidance.

## Weaknesses

### Fatal
None.

### Major

- **Theory–method disconnect.** The theoretical apparatus (Definition 3.1, Corollary 3.1, Proposition 3.1) establishes that *if* batches close to the true marginal can be identified, the final distribution error is bounded. However, Proposition 3.1's bound depends on `sup_j TV(q_{t,j}, p_{t,j})` — the conditional discrepancy within each batch — yet the paper provides no argument connecting the pilot score `s_j` to this quantity. The filtering mechanism (computing `s_j` and thresholding) and the theoretical bound coexist without the method being derived from or justified by the theory. The theory motivates *why* filtering could help but does not formally ground *how* DIST's specific decision rule operates.

### Minor

- **Pilot score underspecified in the main text.** The paper states that `s_j` can be "round-trip residual, self-consistency, ensemble variance, or chemistry-based penalty" (line 150), listing four qualitatively different options without indicating which was used in the experiments, how it is computed, or whether it is a learned quantity or a handcrafted rule. Appendix F is referenced for detailed settings, and likely clarifies this, but the main text leaves the core decision criterion of the method ambiguous.

- **Missing distribution-level metrics.** The backbone papers (EDM, GeoLDM) standardly report property prediction MAEs (energy U0, dipole moment μ, heat capacity Cv) and/or Fréchet ChemNet Distance (FCD) on QM9. These metrics assess whether generated molecules match the *distribution* of physical properties, not just satisfy valence constraints. Since DIST claims to steer toward the true data distribution, showing that property distributions are preserved (not just validity improved) would substantiate this claim. The current evaluation covers only coarse chemical validity.

- **GEOM-Drugs results lack standard deviations.** The paper reports three-run standard deviations for QM9 but none for GEOM-Drugs, making it impossible to determine whether the more modest improvements there (e.g., atom stability 81.3→82.2 for EDM) are statistically significant.

- **Novelty claim overstated.** Line 27 states "We are the first to highlight that molecular data distributions are highly concentrated and dense that makes diffusion-based generative processes fragile." The observation that molecular validity imposes narrow constraints is well-recognized in prior work, including the backbone papers cited by the authors. The contribution lies in the *formalization* (Definition 3.1) and its connection to a specific diffusion failure mode, not in discovering the phenomenon itself.

### Trivial

- The condition `‖m_k − m_ℓ‖ ≤ O(Δ)` in Definition 3.1 is imprecise — `O(Δ)` with respect to what? The definition would benefit from separating the "concentration" (small σ_*) and "denseness" (peak separation) properties more cleanly.

## Nice-to-Haves

- **Comparison against DDIM or similar accelerated sampling.** The paper claims DIST reduces computation by nearly half but does not compare against the backbone models with DDIM sampling at equivalent or lower step counts. Without this control, it is difficult to separate the benefit of DIST's selective correction from the benefit of simply redistributing sampling steps. This comparison would strengthen the efficiency claim.

- **Comparison with other sampling-time correction methods.** A brief discussion of classifier guidance, classifier-free guidance, or RePaint-style resampling and why they are not applicable or are outperformed would help situate the contribution.

## Removed Points

These points were present in the input review but are removed per filtering rules:

- **"The corrective sampling is circular"** — Removed because it misunderstands the method. The pilot inference is used as a diagnostic (run the model on a subset, check if output is chemically valid) to assess whether the current batch is in a valid region, not as ground truth. This is standard rejection-sampling logic, not circular.

- **"The paper does not state the specific timestep t"** — Removed because the paper explicitly gives t=300 as an example in Section 4.3 (line 221) and refers to Appendix H for ablation on this hyperparameter.

- **"Missing related works"** — Removed per policy; the reviewer cannot verify existence of missing references.

- **Missing appendix claims** — Removed per policy; the parser strips appendix content, which exists in the original submission. The paper references Appendices F (implementation details), H (hyperparameter ablation), B (comparison with corrective methods), C (derivations), D (molecule-specific analysis), E (proofs), and G (cost quantification).

- **Formatting and style nitpicks** — Removed per policy.

## Novel Insights

None beyond the paper's own contributions. The reviewer's primary insight is the theory–method gap (that Proposition 3.1 depends on quantities not formally connected to the practical pilot score), which is incorporated above as a major weakness.

## Suggestions

1. **Specify the pilot score explicitly** in the main text — a single sentence stating exactly what `s_j` is (e.g., "the percentage of atoms in the pilot sample that violate valence rules") and how it is computed would eliminate ambiguity and allow readers to understand the method without consulting the appendix.

2. **Add property prediction metrics** (energy MAE, dipole MAE, FCD) for QM9 to demonstrate that DIST preserves distributional fidelity, not just chemical validity.

3. **Include a DDIM baseline** comparing the backbone models at matched or lower step counts to isolate DIST's benefit from the effect of fewer function evaluations.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>