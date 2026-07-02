## Summary

SIGMADOCK proposes a fragment-based SE(3)⁵ Riemannian diffusion model for molecular docking. Rather than operating over torsional angles (as in DiffDock and similar methods), it decomposes ligands into rigid-body fragments via a novel fragmentation scheme (FR3D) and learns to reassemble them within the binding pocket. The method achieves 79.9% Top-1 PB-valid on PoseBusters, substantially outperforming prior deep learning methods and competitive with classical docking tools. Key innovations include the FR3D reduction algorithm, soft triangulation conditioning, an SO(3)-equivariant EquiformerV2-based architecture, and a Newton-Euler-based prediction head that resolves local-coordinate ambiguity.

## Strengths

1. **Conceptually novel and well-motivated formulation.** Replacing torsional-angle parametrization with SE(3)⁵ fragment diffusion is a genuine advance. The argument for why torsional models suffer from non-product induced measures, ambiguous gauge choices, and lever effects (Theorem 1, Section 2.2.2) is structurally sound and grounds the approach in a clear limitation of prior work.

2. **Compelling empirical results.** The headline result (79.9% Top-1 PB-valid on PoseBusters) substantially exceeds prior DL methods on the same split (e.g., DiffDock at 38.0%). The ablation study (Table 1) isolates the contributions of fragment merging, triangulation conditioning, protein-ligand interactions, and the ranking heuristic. The sequence-similarity stratification (Figure 4, right) shows consistent generalization (~51–53% Top-1) across all similarity bands. The co-factor analysis (Table 2) provides a diagnostic sanity check — failure rates jump from 16.2% (no co-factors) to 41.2% (natural ligands) — supporting the claim that the model learns physics rather than memorizing.

3. **Careful evaluation hygiene.** The paper deliberately uses the correct PB train-test split (Footnote 1), restricts training to PDBBind(v2020) alone to avoid data-leakage confounds (Footnote 8), and notes that DiffDock-L was trained on a superset (PDBBind ∪ BindingMOAD). This careful treatment is a strength relative to much of the existing literature.

4. **Coherent and well-motivated architecture.** The EquiformerV2 backbone, virtual nodes for hierarchical information flow, the Newton-Euler-based SO(3)-equivariant prediction head (resolving the local-coordinate orientation ambiguity, Theorem 2), and the soft triangulation distance conditioning (Lemma 1) are individually justified and form a principled system.

## Weaknesses

### Fatal

None.

### Major

1. **Missing classical docking baselines in the main comparison table weaken the headline claim.** The abstract and conclusion claim SIGMADOCK is "the first deep learning approach to surpass classical physics-based docking under the PB train-test split." Yet the main comparison table (Figure 4, left) includes only one entry marked as classical docking — "PDBBind" at 15.9%. PDBBind is a database, not a docking algorithm; the entry is confusingly labeled and is not a representative classical baseline. The paper mentions Vina (line 256) with Top-1 RMSD of 57.2%, but this is relegated to a side comment about pocket sensitivity and uses RMSD-only rather than PB-valid. Widely-used classical tools (Vina, Glide) are absent from the main comparison. Since Vina's 57.2% is well below SIGMADOCK's 79.9% PB-valid, including it in the main table would *strengthen* the paper's claim — its absence leaves the central "surpassing classical docking" assertion less cleanly supported than it should be.

### Minor

2. **The AF3 comparison (Table 4) is framed as head-to-head despite acknowledged task differences.** The paper states "we cannot directly compare SIGMADOCK to co-folding methods" (line 256), yet Table 4 presents per-sequence-similarity PB-valid metrics for SIGMADOCK and AF3 side by side. AF3 performs blind co-folding from sequence with no knowledge of the pocket or holo protein; SIGMADOCK performs re-docking with the holo-conformation protein fixed and the pocket known. These are tasks of fundamentally different difficulty, and the disclaimer does not neutralize the implicit invitation to compare the numbers directly. The table should be restructured or its headers made to explicitly state the differing conditions.

3. **The headline "12.7–32.8%" range lacks an explicit citation at the point of use.** The abstract (line 9) states SIGMADOCK achieves "79.9% on the PoseBusters set, compared to 12.7-32.8% reported by recent deep learning approaches" without a reference for this specific range. The main text does not provide one either. This is a central quantitative claim that needs an explicit citation (e.g., to Butenschön et al. (2024), which is cited nearby in the introduction for a related point).

4. **Limited characterization of the ranking heuristic.** The heuristic (pseudo-binding energy + physicochemical checks) is responsible for a 13.3% PB-valid drop when removed (Table 1, D: 66.1% vs. I: 79.9%). Despite its large impact, the heuristic is described only at a high level with details deferred to Appendix F. More concrete characterization in the main text would help the reader assess how much of the method's success relies on this component versus the diffusion process itself.

### Trivial

5. **FR3D stochasticity is not characterized.** The FR3D algorithm is described as stochastic, but the paper does not report how much performance varies across different fragmentations of the same ligand. If different runs of FR3D produce meaningfully different fragment sets, this variance should be quantified.

6. **The fragment reassembly challenge is not discussed.** The paper argues that SE(3)⁵ diffusion is easier to learn than torsional diffusion, but does not discuss the converse challenge: at t=T, fragments are essentially randomly placed and the model must bring them together into a chemically valid ligand. Some analysis of the sampling trajectory would strengthen the claim that the process is well-conditioned.

## Nice-to-Haves

- Include Vina (and ideally Glide or GOLD) directly in the main comparison table (Figure 4) with PB-valid metrics. The paper already has Vina numbers; computing Top-1 PB-valid for Vina on the same split would cleanly settle the "surpassing classical docking" claim.
- Add an explicit citation for the 12.7–32.8% range at the point where it is stated.
- Restructure or relabel Table 4 to make the task asymmetry (re-docking vs. blind co-folding) explicit in the column headers.

## Removed Points

These points appeared in the reviewer input but were filtered:

- **"Theorem 1 framing is overblown"** — A style/substance judgment about presentation; the intuitive reasoning is clear and deferred proof is standard. Not a substantive weakness.
- **"Architecture description is brief and relies on Appendix G.4"** — Deferring architectural details to the appendix is standard practice. The main text conveys the key insight.
- **"FR3D description is a black box"** — The main-text characterization is appropriate given Algorithm 1 and analysis appear in Appendix D.4 (present in the original submission, stripped by the parser).
- **"Slow inference claim for co-folding models is not substantiated with numbers"** — A qualitative claim about well-known properties of AF3-style models; a precise runtime comparison in the introduction is not required.
- **"Conclusion would benefit from acknowledging limitations more concretely"** — The paper states limitations are discussed in Appendix J, which is standard practice.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add Vina (and one additional classical tool if feasible) to the main comparison table with PB-valid metrics. This directly strengthens the paper's central claim and requires no new experiments — the Vina numbers are already computed.
2. Add an explicit citation (e.g., Butenschön et al. (2024)) at the point where the 12.7–32.8% range is stated in the abstract.
3. Relabel Table 4's columns to explicitly state the differing conditions (e.g., "SIGMADOCK (re-docking, known pocket)" vs. "AF3 (blind co-folding from sequence)") so the task asymmetry is clear without needing the disclaimer.
4. Add a brief discussion or simple figure showing fragment positions at intermediate diffusion timesteps to address the reassembly-conditioning concern.
5. Quantify the variance of FR3D's stochastic fragmentation across multiple runs on the same ligand.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>