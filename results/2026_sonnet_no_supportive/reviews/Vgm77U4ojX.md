Now I have a thorough understanding of the paper. Let me draft the review.Let me look at one or two of the 8-band papers more closely to calibrate.**Round 1 bracket: 7 to 8.** SIGMADOCK's decisive empirical milestone (first DL to beat classical docking on PB split), 6.3× improvement over DiffDock, and strong theoretical grounding (Theorems 1 & 2) put it clearly above the 6-7 band (FABFlex 7.0, GroupBind 6.75). The missing same-architecture torsional ablation—while a real evidential gap—doesn't invalidate the contribution and keeps it just below the 8-band papers (FoldFlow 8.0, GeoBFN 8.0) that have clean, complete validation. **Final score: 7.5.**

---

## Summary
SIGMADOCK is a fragment-based SE(3) Riemannian diffusion model for molecular docking that decomposes ligands into rigid-body fragments via the FR3D fragmentation scheme and learns to reassemble them in the binding pocket. Combining soft triangulation constraints, a gauge-invariant SO(3)-equivariant architecture built on EquiformerV2, and energy-based sample ranking, the model achieves 79.9% Top-1 PB-valid on PoseBusters—the first deep learning method to surpass classical physics-based docking under the strict PB train-test split, representing a 2.4–6.3× gain over prior generative baselines.

## Strengths

- **Decisive and well-documented empirical advance (Table 1, Figure 4, Section 3.2):** 79.9% Top-1 PB-valid vs. 12.7–32.8% for prior DL methods under identical training conditions; 6.3× over DiffDock. Performance holds on the separate Astex benchmark (90.6% Top-1) and under low sequence similarity, countering memorization concerns. The gains survive both RMSD and PB-validity checks, ruling out chemical-plausibility artifacts.

- **Theoretically grounded motivation (Section 2.2.2, Theorem 1):** Theorem 1 formally establishes that torsional models induce non-product, entangled distributions in Cartesian space, while fragment SE(3)^m diffusion yields a factorized product structure. This is a principled, non-heuristic argument for why the fragment parametrization simplifies the learning problem.

- **Conformational manifold validation (Section 2.2.1, Figure 2B):** The paper explicitly justifies its core assumption—that bound poses are reachable via rigid-body assembly from conformational space—by aligning conformers to crystal poses and empirically confirming RMSD residuals well below 2Å, providing necessary support for the approach.

- **Gauge-invariance resolution (Section 2.4, Theorem 2):** The paper identifies and solves a non-trivial correctness problem: the local coordinate orientation for each fragment is not canonical, creating an ambiguity in SE(3) parametrization. Using Newton-Euler equations from rigid-body mechanics for the score prediction head, Theorem 2 proves full invariance to this orientation choice.

- **Specific, retrained ablations (Table 1):** Configurations A–C are retrained from scratch (not post-hoc), isolating triangulation conditioning (+12% PB-valid), fragment merging (+6%), and energy scoring (+12%). The ablation separates RMSD-only and PB-valid metrics, making chemical plausibility contributions transparent.

- **Co-factor stratification and pocket sensitivity (Tables 2–3):** Failure rate drops to 16.2% with no co-factors vs. 41.2% for complexes with natural ligand co-binding events—a mechanistic, coherent story. Pocket-sensitivity experiments (Table 3) show gains are not attributable to smaller pocket definitions.

## Weaknesses

### Fatal
None.

### Major

- **Missing fragment-vs.-torsional ablation under identical architecture (Section 2.2.2, Table 1):** The paper's central claim is that SE(3)^m fragment diffusion is preferable to torsional diffusion. The best supporting evidence is the gap over DiffDock, but DiffDock uses a different backbone (EGNN vs. EquiformerV2), different training pipeline, and different fragmentation scheme. Table 1's ablations do not include a variant of SIGMADOCK with a torsional parametrization in place of SE(3)^m fragments. Without this, the gain over DiffDock conflates at least three simultaneous changes: parametrization, architecture, and training improvements. Theorem 1 is valid, but whether the parametrization specifically accounts for a material fraction of the measured gain is untested. The contribution stands regardless, but the attribution of the gain to the fragment parametrization specifically is not cleanly established.

- **AF3 comparison framing (Abstract, Section 3.2, Table 4):** The abstract states "we reach AF3-level performance" without qualification. AF3 solves a strictly harder problem (co-folding from sequence with flexible receptor), while SIGMADOCK uses the crystal receptor structure and known pocket. The paper does include a caveat in Section 3.2 ("we cannot directly compare SIGMADOCK to co-folding methods"), but this caveat is not present in the abstract or conclusion where "AF3-level performance" dominates. Table 4's comparison (79.9% vs. 80.2%) is scientifically creditable given data efficiency, but the unqualified phrase in the abstract will be read as a direct capability comparison and needs explicit task-difficulty conditioning.

### Minor

- **Figure 4 right-panel values inconsistent with headline numbers (Figure 4, Table 4):** The parsed right panel of Figure 4 shows Top-1 values of ~51–53% across all three sequence-similarity bins, while Table 4 reports PB-valid values of 72–87% for the same bins and the headline is 79.9%. If Figure 4 right is showing a different metric (e.g., with fewer seeds), this needs to be stated explicitly in the caption. This may be a PDF parsing artifact, but if these numbers appear in the actual submission, they require a clarifying note.

- **FR3D stochastic fragmentation sensitivity not characterized (Section 2.2.3):** FR3D performs a stochastic search yielding multiple valid fragmentations. The paper notes this "provides a promising stream for data augmentation" but does not assess the variance across stochastic fragmentation choices at test time. If results are stable, this should be stated; if they are not, it is a methodological detail relevant to reproducibility.

### Trivial
None.

## Nice-to-Haves
- A direct torsional variant of SIGMADOCK (same EquiformerV2 backbone, same training, only replacing SE(3)^m with torsional parametrization) would decisively test whether the parametrization itself drives the gain—and given Theorem 1, it would likely reinforce rather than undermine the conclusion.
- Reporting variance across stochastic FR3D fragmentation seeds would confirm robustness of the fragmentation step.

## Removed Points
*These points are flagged as removed — treat with caution.*

- **W (Harsh Critic): Section-by-section note about Introduction framing of DiffDock-L** — Minor presentation precision concern; Section 3.2 already distinguishes DiffDock (same split) from DiffDock-L (larger dataset), so the paper does address this.
- **W (Harsh Critic): Footnote 9 inconsistency (AF3 in Table 4, excluded from Figure 4)** — Merged into the AF3 framing major weakness; treating as duplication.
- **W (Harsh Critic): Section 2.4 note about EquiformerV2 contribution being unknown** — Merged into the major missing-ablation weakness.
- **S (Generic): "Addresses an important problem in drug discovery"** — Too generic; not included as a concrete, evidence-backed strength.

## Novel Insights
The paper's most distinctive architectural insight is recognizing that the gauge-invariance problem in fragment-space parametrization—the non-canonical choice of local coordinate axes for each rigid-body fragment—is a fundamental correctness issue requiring explicit resolution, and that pseudo-force prediction via Newton-Euler rigid-body mechanics (Theorem 2) provides a natural solution that is both geometry-consistent and architecturally clean. Separately, the triangulation conditioning scheme—feeding cross-fragment distance mismatches as edge features to softly encode bond-angle geometry without hard-constraining dihedral angles—is an elegant inductive bias the ablations show contributes materially to chemical plausibility. Together, these represent a more systematic approach to incorporating structural chemistry priors into diffusion-based docking than prior work.

## Suggestions
- Add a qualifying clause to the abstract's "AF3-level performance" (e.g., "AF3-level PB-valid accuracy on the re-docking task, where the receptor structure is known") — this is a framing fix, not a results fix.
- Clarify or relabel Figure 4 right panel to match the metric reported in Table 4.
- As future work, include a same-architecture torsional variant in a follow-up study; this would definitively validate Theorem 1's empirical consequences.

---

## Score and Decision

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| m9zWBn1Y2j (PsiDiff ligand conformation) | 3.0 | 1 | Weaker: incremental ligand generation, no strong empirical milestone |
| kKXIYUi8ff (DynamicsDiffusion MD) | 3.0 | 1 | Weaker: limited evaluation, no docking benchmark |
| G536mmC2HL (TorSeq torsional conformation) | 3.0 | 1 | Weaker: narrower contribution, no SOTA breakthrough |
| An87ZnPbkT (GNNAS-Dock) | 3.0 | 1 | Weaker: algorithm selection, not a generative model |
| FuXtwQs7pj (toric varieties diffusion) | 4.5 | 1 | Weaker: interesting geometry but limited scope and no SOTA results |
| IARgA4HqjJ (Lie group score-based) | 5.4 | 1 | Weaker: theoretical extension, no strong docking empirics |
| 1IaoWBqB6K (DiffDock-Pocket) | 5.0 | 1 | Weaker: good but incremental extension of DiffDock, no milestone |
| FWsGuAFn3n (PromptDiff) | 3.75 | 1 | Weaker: prompt-based generation, limited empirical gains |
| qH9nrMNTIW (IPDiff) | 6.25 | 1 | Weaker: good contribution but no milestone, accepted borderline |
| 5YLsnsjgeC (VFDiff) | 6.0 | 1 | Weaker: energy-guided SE(3) model, no PB benchmark |
| kzGuiRXZrQ (EQGAT-diff) | 5.75 | 1 | Weaker: design-space exploration, no hard-to-beat milestone |
| uNomADvF3s (LiftMol) | 6.5 | 1 | Comparable scope, accepted, but no comparable breakthrough |
| kJFIH23hXb (FoldFlow SE3-SFM) | 8.0 | 1 | Strong: clean SE(3) theory + empirics on protein backbone; similar profile but protein not docking |
| NSVtmmzeRB (GeoBFN) | 8.0 | 1 | Strong: unified modeling, SOTA; cleanly validated without major missing ablations |
| iezDdA9oeB (FABFlex flexible docking) | 7.0 | 2 | Close: docking-specific, good empirics, accepted; SIGMADOCK has stronger milestone |
| g3VCIM94ke (DrugFlow) | 6.67 | 2 | Weaker: SBDD, good contribution but less decisive empirical gap |
| zDC3iCBxJb (GroupBind) | 6.75 | 2 | Weaker: group docking extension, no PB benchmark comparison |
| 5FXKgOxmb2 (MAGNet) | 7.25 | 2 | Weaker: molecule generation, not docking; SIGMADOCK's docking milestone is more impactful |
| jkvZ7v4OmP (DiffCSP++) | 7.33 | 2 | Comparable: crystal generation with constrained diffusion; SIGMADOCK more impactful milestone |

**Round 1 bracket:** Between 7 and 8.

**Round 2 narrowing:** SIGMADOCK's empirical advance (first DL to surpass classical docking, 6.3× over DiffDock) is more decisive than FABFlex (7.0) or GroupBind (6.75). The missing torsional ablation under identical architecture is a real major weakness that prevents a clean 8, which is where papers like FoldFlow and GeoBFN sit—those papers have complete experimental validation of their central claims. SIGMADOCK sits between these bands at **7.5**.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>