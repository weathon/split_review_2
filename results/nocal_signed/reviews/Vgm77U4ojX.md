Now I have all the information I need. Let me construct the final review based on the per-item impact scores from the model.

The strengths consistently score very high (+8.3 to +10.0), while the most impactful weakness is a moderate -4.7 (classical docking framing). All other weaknesses score -1.5 or below, indicating they are minor. The core contribution is genuinely novel and backed by strong empirical evidence. The weaknesses are about framing and clarity, not methodological flaws.

---

## Summary

This paper proposes SIGMADOCK, a fragment-based SE(3) diffusion model for molecular docking. Instead of modeling torsional angles (the standard approach), it decomposes ligands into rigid-body fragments and diffuses them independently in SE(3)^m, then reassembles them via a learned score. The theoretical motivation is that fragment-based diffusion yields a factorized product of Haar measures, avoiding the ill-conditioned learning problem of torsional models where independent torsional perturbations produce non-local Cartesian coupling. Empirically, SIGMADOCK achieves 79.9% Top-1 PB-valid on PoseBusters — substantially above prior deep learning methods on the same split.

## Strengths

- **A genuinely novel and well-motivated methodological idea (Section 2.2.2, Theorem 1).** The paper identifies a real weakness in torsional diffusion models — that independent torsional perturbations produce non-local, coupled Cartesian displacements — and replaces the torsional parameterization with a fragment-based SE(3)^m parameterization that cleanly factorizes the diffusion kernel. This is a conceptually different and well-argued approach.

- **Strong empirical results validated with appropriate physicochemical filters (Table 1, Figure 4).** The reported 79.9% Top-1 PB-valid success rate on PoseBusters substantially exceeds prior deep learning methods on the same split. Using PB-valid RMSD (passing PoseBusters' physicochemical sanity checks) rather than raw RMSD directly addresses the critique from Butenschön et al. (2024) and raises the bar for evaluation.

- **Clean ablations isolating key components (Table 1, Configs A-C, re-trained from scratch).** Triangulation conditioning, protein-ligand interactions, and fragment merging each contribute measurable (4-12% relative) improvements.

- **Co-factor failure analysis (Table 2).** Stratification by co-factor presence is diagnostic: the failure rate drops to 16.2% on complexes with no co-factors versus 41.2% for natural ligands, revealing a specific, bounded limitation and making the core results more credible.

- **Careful experimental discipline (Section 3.1).** Training only on PDBBind(v2020) without augmentation enables fair comparison — many prior papers compared models trained on different data mixtures without assessing overlap.

## Weaknesses

### Fatal
None.

### Major
- **The headline claim of surpassing "classical physics-based docking" is not supported by the comparisons shown in the main results table (Figure 4).** The paper asserts this centrally (abstract, introduction, conclusion), yet the main comparison table includes only one entry that could be classical (PDBBind at 15.9%). The well-known classical method Vina — whose Top-1 of 57.2% is reported in the pocket-sensitivity discussion (line 256) — is absent from the main comparison. Since 79.9% > 57.2% the claim is likely true, but the evidence that would validate it is not prominently displayed alongside the core results. The paper should either add Vina (and ideally Glide/Gold) to Figure 4, or qualify the claim to reference only prior deep learning methods, which the data cleanly supports.

- **The "AF3-level performance" claim (Section 3.2, line 194) is overstated relative to the disaggregated evidence in Table 4.** While the average PB-valid rates are close (79.9% vs. 80.2%), on the hardest generalization split ([0,30%) sequence similarity), SIGMADOCK achieves 72% versus AF3's 87% — a 15-percentage-point gap. The aggregate average is driven by SIGMADOCK's higher score on the [95,100%] split (87% vs. 78%), where train-test leakage is most likely to inflate scores. The claim should be qualified to acknowledge this gap.

### Minor
- **The abstract states "12.7-32.8% reported by recent deep learning approaches"** for Top-1 PB-valid rates, but the main table (Figure 4) shows DiffDock at 38.0% and G2G at 58.1% under the PB column. It is unclear whether these baseline numbers are RMSD-only or PB-valid, making the abstract's range difficult to reconcile with the table. The paper should clarify which metric each baseline number reflects.

- **The main comparison table (Figure 4) presents two rows for "Ours" (79.9% and 80.6%)** both under "Pocket Specified" with no explanation of what differs between them. Additionally, the right chart in Figure 4 shows sequence-similarity breakdowns (51%, 53%, 53%) that disagree substantially with the corresponding PB-valid numbers in Table 4 (72%, 79%, 87%) without clarifying which metric is being plotted.

- **The conformational alignment assumption (Section 2.2.1)** — that conformers from M_c align to bound states with RMSD ≪ 2Å — is stated but the distribution of alignment errors is not summarized in the main text. Only a single example (0.11Å for BFL in PDB 1Q4G) is shown, with details deferred to Appendix D.3. Reporting mean ± std and the 95th percentile in the main paper would strengthen the theoretical foundation.

- **Inference cost is not reported for SIGMADOCK itself.** The paper claims "50× faster sampling than AF3" (line 194) but provides no wall-clock time or number of function evaluations for its own method, making the efficiency claim unverifiable.

- **The number of seeds used for baseline methods (DiffDock, G2G, Vibe2) is not stated,** only N_seeds=40 for SIGMADOCK. Since Top-1 success rate increases with the number of samples, this matters for fairness of comparison.

### Trivial
None.

## Nice-to-Haves
- A single sentence in Section 2.2.1 reporting the alignment RMSD distribution (mean, std, 95th percentile) would address the main methodological concern without new experiments.
- Explicit labelling of which methods in Figure 4 report PB-valid vs. RMSD-only rates.

## Removed Points
These points from the input review are removed with justification:

- **"SIGMADOCK appears under both Holo Specified and Pocket Specified conditions"** — REMOVED as factually incorrect. Both "Ours" entries are under "Pocket Specified" in the text table. The observation about unexplained rows is kept as a minor weakness.
- **"Without the appendix it is difficult to assess the architecture"** — REMOVED per hard rule (the parser strips appendices; they exist in the original submission).
- **"Training data curation/PDBBind filtering question"** — REMOVED as a minor detail that does not affect the paper's claims.
- **"Alignment efficiency, FR3D quantification histogram, ablation table structure"** — REMOVED as minor implementation clarifications typical of deferred appendix content, not weaknesses.
- Any formatting/style nitpicks — REMOVED per hard rules.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Add Vina (and ideally Glide or Gold, if numbers are obtainable) to the main comparison table in Figure 4 with clear source annotation.
- Qualify the AF3 comparison: explicitly report the disaggregated sequence-similarity breakdown and acknowledge the gap on [0,30%).
- Add one sentence in Section 2.2.1 reporting the alignment RMSD distribution across the dataset.
- Report wall-clock inference time and NFE for SIGMADOCK alongside the 50× efficiency claim.
- Clarify in the table caption whether each baseline number is RMSD-only or PB-valid, and state the number of seeds used.

## Score and Decision

The paper presents a genuinely novel fragment-based SE(3) diffusion framework with a well-argued theoretical motivation, strong empirical results (79.9% PB-valid), and clean ablations. The weaknesses are primarily about framing and presentation — the classical docking comparison is missing from the main table, the AF3 claim is slightly overstated, and several expositional details are deferred or unclear. None of these undermine the core contribution, which is novel and well-supported. With the clarifications suggested above, the paper would be substantially strengthened.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>