## Summary

SIGMADOCK introduces a fragment-based SE(3)⁴ Riemannian diffusion model for molecular docking. Instead of operating on torsional angles (the dominant paradigm), the paper decomposes ligands into rigid-body fragments, diffuses over their independent SE(3) poses, and learns to reassemble them within the binding pocket. A fragmentation reduction scheme (FR3D), soft triangulation constraints, and an EquiformerV2-based architecture are developed to close the degrees-of-freedom gap with torsional models. The method achieves 79.9% Top-1 PB-valid on PoseBusters—a substantial gain over prior deep learning methods—and shows generalization across sequence-similarity splits and co-factor conditions.

---

## Strengths

1. **Novel fragment-based diffusion paradigm with clear theoretical motivation (Theorem 1, Sections 2.2.2–2.2.3).** The paper identifies a concrete weakness in torsional diffusion: the induced Cartesian measure is non-product, creating entangled dynamics that complicate score learning. Replacing the torsional parameterization with SE(3)ᵐ diffusion over rigid-body fragments (where the forward kernel factorizes as a product of Haar measures) is a well-motivated design choice, not an incremental tweak. The FR3D merging scheme and soft triangulation constraints (Lemma 1) are clever additions that reduce the DoF gap between the fragment and torsional formulations.

2. **Strong empirical results (Figure 4, Table 1).** The headline 79.9% Top-1 PB-valid on PoseBusters is a substantial jump over prior deep learning methods (e.g., DiffDock at 38.0%). The ablation study cleanly isolates the contributions of fragmentation merging, triangulation conditioning, protein–ligand interaction edges, and the energy scoring heuristic—each with measurable effect sizes (4–12% relative improvements).

3. **Rigorous experimental design.** Training only on PDBBind(v2020) and evaluating on the PoseBusters temporal split (proteins from 2021+) reduces train–test leakage, a common confound in the literature. Reporting PB-validity (not just RMSD) follows best practices (Butenschön et al., 2024). The analysis across sequence-similarity splits (Figure 4 right) and co-factor presence (Table 2) provides genuine evidence of generalization rather than memorization.

4. **Clean theoretical architecture (Theorem 2, Section 2.4).** The paper resolves a subtle gauge ambiguity (non-unique local coordinate orientation for fragments) via a Newton-Euler-based prediction head, proving invariance to the choice of local axes. This is a principled solution to a concrete architectural problem.

---

## Weaknesses

### Fatal
None.

### Major

1. **The AF3 comparison conflates different tasks and the evidence is not directly comparable.** The paper repeatedly claims "AF3-level performance" (abstract, Section 1, Section 3.2, Conclusion). But AF3 solves a strictly harder problem: joint protein–ligand co-folding *without* a known holo-receptor structure. SIGMADOCK operates in the re-docking setting with a fixed holo-receptor and known pocket. The paper acknowledges this difference (line 256: "Although we cannot directly compare SIGMADOCK to co-folding methods…") yet continues to use the comparison as a headline claim. Table 4 compounds the issue: the per-sequence-similarity counts between SIGMADOCK and AF3 differ substantially (e.g., the [0,30) bin has 109 vs. 38 complexes), indicating different split criteria or databases, making the column directly unreadable as a valid comparison. The paper's results are already strong enough (79.9% PB-valid on re-docking with clean ablations) to stand on their own without this conflated comparison.

### Minor

2. **The 12.7–32.8% range in the abstract has no clear provenance in the paper.** The abstract states performance is "compared to 12.7–32.8% reported by recent deep learning approaches." This range does not appear in any table or figure in the main text. The main comparison table (Figure 4) shows deep learning baselines ranging from 15.9% to 58.1% on PB—neither matching the abstract's range. The 12.7–32.8% range presumably refers to PB-valid rates of prior methods (from Butenschön et al., 2024), but the paper never states this explicitly or anchors the numbers to a specific table entry.

3. **The energy scoring / ranking heuristic is underspecified, despite being a critical component.** The paper states it uses a "simple and cheap heuristic" of evaluating "(pseudo) binding energy" plus physicochemical checks (line 176). Removing this heuristic drops Top-1 from ~80% to ~67% (Table 1, row D)—the single largest ablation effect in the paper. Yet the paper never specifies what this scoring function is (a classical physics potential? a learned model? which exact function?), whether it is retrained per dataset, or whether it would generalize to new protein families. This degrades reproducibility on a component that materially affects results.

4. **SIGMADOCK's own inference cost is not reported.** The paper claims "50× faster sampling" versus AF3 (line 194) and "faster inference" over torsional models (line 20), but does not provide wall-clock time, number of diffusion steps, steps per second, or total inference time per complex for SIGMADOCK itself. The speed claim relative to AF3 is unverifiable without the absolute numbers for the proposed method.

5. **Ambiguity about whether the main table's "PB (%)" column reports RMSD-only or PB-valid for baselines.** The abstract states SIGMADOCK's 79.9% is "RMSD < 2 Å PB-valid." The table column is labeled "PB (%)" without clarifying whether prior methods' numbers are also PB-valid or just RMSD-only. If the latter, the comparison is unfair to baselines. The text (line 192–193) says SIGMADOCK "achieve[s] a 6.3× higher PB-validity than DiffDock," suggesting DiffDock's 38.0% is PB-valid, but this should be unambiguous from the table alone.

### Trivial

6. **Two "Ours" rows in the main table (Figure 4) are unexplained.** The table shows "Ours" at 79.9% and another at 80.6%, both at 90.6% AX. The text does not explain what distinguishes them (different seeds? variant configuration?). The difference is small (~0.7 pp) but the presence of two unlabeled rows is confusing.

7. **The claim of surpassing classical physics-based docking is supported but could be presented more transparently.** The paper states this in the abstract and Section 3.2, and the figure caption notes "(*) Denotes classical docking" among the baselines. Vina is also mentioned in the pocket-robustness analysis (line 256: 57.2% Top-1). The claim is not unsupported, but the main comparison table would benefit from explicitly naming at least one well-known classical tool (e.g., Vina) in the primary results rather than burying the comparison in a secondary analysis.

---

## Nice-to-Haves

- Add a classical docking baseline (e.g., AutoDock Vina) to the main comparison table with both RMSD and PB-valid rates on the same PB split.
- Include wall-clock inference time (seconds per complex, diffusion steps) for SIGMADOCK under the default sampling configuration.
- Specify the exact scoring function used for the energy-based ranking heuristic.

---

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **"FR3D main text description too terse"** — The reviewer criticized the main text for insufficient detail about the FR3D merge criteria. The text is relatively brief but refers readers to Appendix D.4, which is standard practice for a conference paper. This is a presentational preference, not a genuine weakness.

2. **"Classical docking claim is not supported at all"** — The reviewer argued no classical methods appear in the main table and the claim rests on absent evidence. However, the figure caption explicitly states "(*) Denotes classical docking" among the listed baselines, and Vina is compared elsewhere (line 256). The claim IS supported, just less prominently than ideal. This has been demoted to a trivial presentation point (Weakness #7 above).

3. **"All baselines are deep-learning or scoring-function methods"** — The reviewer asserted this without evidence. The figure caption's explicit notation of classical docking means some baselines are classical. Since the parser strips visual markers (asterisks) from the rendered table, this criticism may stem from incomplete rendering rather than the paper's content.

4. **"PB-valid range from Butenschön — should include citation"** — Moved to Weakness #2 but stripped of the speculation about the exact source. The core concern (unanchored abstract number) is retained.

---

## Novel Insights

The main novel insight from the reviews is that the paper's strongest evidence—the clean ablation isolating the energy-scoring heuristic's 13 pp impact—receives the least discussion, while the weakest evidence (the AF3 comparison and the abstract's unanchored 12.7–32.8% range) receives the most prominent placement. The paper would be more robust if it inverted this emphasis.

---

## Suggestions

1. Remove or substantially reframe the AF3 comparisons. The paper's results on the re-docking task are strong enough not to need a conflated cross-task comparison. If kept, state clearly: "SIGMADOCK's 79.9% PB-valid on re-docking approaches the 84% Top-1 that AF3 reports on the harder co-folding task, despite using a fraction of the data and 50× faster inference."
2. Cite the source of the 12.7–32.8% range in the abstract and include those same PB-valid baselines in the main comparison table.
3. Specify what scoring function is used for the energy-based ranking heuristic.
4. Report wall-clock inference time (seconds per complex) for the default configuration (N_seeds=40).

---

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>