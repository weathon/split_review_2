Let me read the remaining sections for completeness.Now I have the full paper. Let me draft the review based on my verification of the claims.Now let me run calibration search Round 1 to bracket the score.Let me read some of the most relevant anchor papers for calibration.Now I have enough context to calibrate. Let me formalize my **Round 1 bracket**.

**Round 1 Bracket Assessment:**
- **Score 1-3 (reject)**: PsiDiff (3.0), TorSeq (3.0), GNNAS-Dock (3.0) — all have fundamental novelty/contribution/methodology issues. SIGMADOCK is far stronger.
- **Score 3.5-5.5 (borderline reject)**: DiffDock-Pocket (5.0), DiffMaSIF (4.67) — incremental or with insufficient evaluation. SIGMADOCK clearly exceeds these.
- **Score 5.5-7.5 (borderline accept)**: DockGen (6.0, Accept), VFDiff (6.0, Reject), IPDiff (6.25, Accept) — SIGMADOCK has stronger theoretical grounding and stronger empirical results than all of these.
- **Score 7.5-8.5 (accept)**: FoldFlow (8.0), GeoBFN (8.0), ProtComposer (8.0) — strong theory + empirical papers with unanimous scores. SIGMADOCK has comparable theoretical depth, arguably stronger practical impact (first DL > classical docking on PB-valid), but has presentation issues.

**Initial bracket: 7.0–8.0**

Now let me write the final consolidated review.

---

## Summary
SIGMADOCK introduces a fragment-based SE(3) Riemannian diffusion model for rigid-receptor molecular docking. The key idea is decomposing ligands into rigid-body fragments via a novel FR3D fragmentation scheme, then performing diffusion in SE(3)^m rather than torsion space T^k × SE(3). This is theoretically motivated by Theorem 1, which shows the fragment formulation yields factorized product measures (avoiding the entangled non-product measures of torsional models). Evaluated under the stringent PoseBusters train-test split with PB-validity checks, SIGMADOCK achieves 79.9% Top-1 PB-valid on PoseBusters and 90.6% on Astex, making it the first deep learning method to surpass classical physics-based docking under these conditions.

## Strengths

- **Principled theoretical contribution (Theorem 1, Section 2.2.2).** The paper formally establishes that torsional models produce entangled, non-product induced measures in Cartesian space, while disjoint rigid fragments yield a factorized product of Haar measures on SE(3)^m. This directly maps to a real training difficulty (the lever effect creating geometric coupling along torsional chains) and provides genuine motivation for the fragment formulation — not handwaving. Theorem 2 further proves the training objective and sampling are invariant to choice of local coordinate axes.

- **Non-trivial domain-aware engineering (FR3D + triangulation, Section 2.2.3).** The recursive fragment merging reduces fragment count from k+1 to ~2/3(k+1), with dummy-atom pruning for over-constrained dihedrals (which would break the conformational manifold assumption). The triangulation conditioning (Lemma 1) uniquely determines cross-fragment bond angles without restricting dihedral freedom. These reflect genuine structural chemistry understanding.

- **State-of-the-art results under the most rigorous available evaluation (Figure 4, Tables 1–4).** Using the PoseBusters train-test split with PB-validity checks — the hardest standard re-docking evaluation — SIGMADOCK achieves 79.9% Top-1 PB-valid (PB) and 90.6% (Astex), substantially exceeding prior DL methods under the same split. Critically, no post-hoc energy minimization is used, which is a common but computationally expensive shortcut.

- **Thorough and informative ablation study (Tables 1–3).** Table 1 isolates triangulation conditioning (+12.8% PB-valid), fragment merging (+6.2%), PL interactions (+3.6%), and ranking heuristic contributions. Table 2's co-factor stratification confirms the expected pattern: SIGMADOCK fails more when co-factors (excluded by design) are present. Table 3 demonstrates robustness to pocket size variation.

- **Exemplary comparison practices.** DiffDock-L and AF3 are excluded from the main comparison figure because they use different training data (footnote 9), with a separate, appropriately caveated AF3 comparison in Table 4. Training is deliberately restricted to PDBBind(v2020) for fair comparison. This sets a high standard for the field.

## Weaknesses

### Fatal
None

### Major
- **Ambiguous metric labeling in Figure 4 and abstract creates confusion about improvement magnitude.** The abstract claims "12.7–32.8% reported by recent deep learning approaches" for the PB-valid metric, but Figure 4's table shows DiffDock at 38.0% and G2G/Vibe2 at 58.1% — these appear to be RMSD < 2Å rates, not PB-valid rates. The 12.7% figure is derivable (79.9% / 6.3× = 12.7%, matching the "6.3× higher PB-validity than DiffDock" claim in Section 3.2), but the reader must cross-reference multiple sections to reconcile the abstract with the main results figure. Figure 4's table does not explicitly label whether baseline numbers are RMSD-only or PB-valid, while SIGMADOCK's two rows (79.9% and 80.6%) presumably correspond to PB-valid and RMSD < 2Å respectively — but this is never stated. The underlying improvement is real and large, but the main evidence as presented requires detective work to parse.

### Minor
- **The M_c vs M_b conformer gap (5.5pp) deserves more characterization.** Table 1 row G shows sampling from M_b yields 85.4% vs 79.9% from M_c — a non-trivial gap indicating the rigid-fragment assumption introduces measurable error from RDKit conformers. The paper acknowledges this as "small but expected" (Section 3.2) and provides one alignment example (BFL in PDB 1Q4G, 0.11Å RMSD, Figure 2B), but does not characterize which types of molecules suffer most (e.g., by fragment count or flexibility). Turning this limitation into an informative analysis would strengthen the paper.

- **Language critiquing torsional models occasionally overstates practical implications.** Section 2.2.2 states torsional models "cannot guarantee consistency during sampling" and the framework is "unscalable" due to "combinatorial growth of possible extrinsic realisations." While the theoretical argument is sound, DiffDock does achieve 38% RMSD < 2Å on PB, indicating torsional models work, just less well. The paper hedges with "We hypothesise" in one sentence but the overall framing leans toward "fundamentally broken" rather than the more defensible "harder to train and more ill-conditioned."

- **Architecture innovations are not individually ablated.** Section 2.4 lists three innovations (virtual nodes/edges, tailored featurization, smooth cutoff decay) as a "significant contribution," but only the aggregate PL-interactions effect is ablated (Table 1 row B: +3.6pp). The individual impact of each architectural component remains unknown.

- **No wall-clock inference time comparisons against the baselines in Figure 4.** The paper claims "50× faster sampling" than co-folding models and motivates the approach partly through HTVS applicability, but provides no timing comparison against DiffDock, G2G, Vibe2, or classical methods — the actual baselines in the main evaluation.

### Trivial
None

## Nice-to-Haves
- A **direct torsional-vs-fragment ablation** using the same EquiformerV2 backbone and training setup would isolate the fragment formulation's contribution from other design differences with DiffDock/others. This would elevate the paper's central argument from "plausible and supported by cross-method comparison" to "demonstrated in controlled experiment."
- Reporting **Top-5 or oracle (best-of-N) rates** to separate generation quality from ranking heuristic quality (the heuristic contributes ~14pp per Table 1 rows D vs I*).
- **Bootstrap confidence intervals** on Top-1 PB-valid given the 308-complex PB set, where a few percentage points could be within noise.
- Stratifying the M_c vs M_b gap by molecule flexibility or fragment count.
- **Cross-docking experiments**, though the paper explicitly and appropriately scopes to re-docking (Section 1, paragraph 4).

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Right panel of Figure 4 shows 51/53/53% seemingly inconsistent with 79.9% headline.** This is almost certainly a PDF parsing artifact — the bar chart heights were misread by the parser. Table 4 provides the actual per-similarity-split PB-valid numbers (72/79/87%), which correctly average to 79.9%. Removed: parser error, not author error.
- **AF3 comparison extracted from Extended Data figures introduces potential inaccuracies.** This is standard practice in the field, and the paper appropriately caveats the comparison ("Values for AF3 are extracted from Extended Data 4c (Abramson et al., 2024)"). Removed: standard practice with appropriate caveat.
- **DoF overhead of fragmentation is understated (44 DoFs vs 16 for torsional model).** The paper explicitly discusses this trade-off in Section 2.2.3, explains how FR3D reduces m and how triangulation conditioning provides soft DoF reduction, and ablates both components (Table 1 rows A, C showing +12.8% and +6.2% contributions). The triangulation being "load-bearing" is expected — it is the whole point of the soft-constraint design. The reviewer's demand for a quantitative analysis of "simpler landscape in higher D vs. complex landscape in lower D" would be interesting but is not a weakness given the empirical evidence. Removed: paper addresses this adequately.
- **Only one alignment example (BFL) in main text for M_c/M_b claim.** Additional analysis is deferred to Appendix D.3, which exists in the original submission. Removed: appendix-deferred evidence.
- **No statistical significance measures.** Single-run evaluation is standard practice for benchmark evaluations in this field. Moved to nice-to-have.
- **Scope limited to re-docking, but claims extend beyond.** The paper explicitly scopes to re-docking (Section 1, paragraph 4) and explains why, though some conclusion language ("major leap forward") could be more tightly scoped. Moved to nice-to-have as scope creep concern.

## Novel Insights
The paper's central insight — that decomposing ligands into rigid fragments and diffusing in SE(3)^m yields a factorized product structure that avoids the geometric entanglement inherent in torsional-space diffusion — is theoretically grounded (Theorem 1) and empirically validated. The triangulation conditioning scheme (Lemma 1) elegantly soft-constrains inter-fragment geometry without restricting dihedral freedom, creating an effective inductive bias. The FR3D recursive merging with over-constrained dummy-atom pruning demonstrates that careful structural chemistry reasoning can substantially reduce degrees of freedom while preserving conformational coverage. The combination of these ingredients produces the first DL method to surpass classical docking under PB-valid evaluation, suggesting that inductive-bias engineering may be more productive than scaling data/compute alone for molecular docking.

## Suggestions
- **Clearly annotate Figure 4** with the specific metric (RMSD < 2Å vs PB-valid) used for each method, and ensure the abstract's comparison range maps directly to a visible table.
- **Add wall-clock timing** against baselines in Figure 4 to substantiate HTVS claims.
- **Stratify M_c vs M_b performance** by fragment count/flexibility to guide future conformer generation improvements.
- **Consider a controlled torsional-vs-fragment experiment** with the same backbone to strengthen the core theoretical argument.
- **Tighten conclusion language** ("major leap forward in … molecular modelling") to match the evaluated scope (re-docking with holo receptor and known pocket).

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to SIGMADOCK |
|-------|------|-----------|-------|------------------------|
| PsiDiff (ligand conf. gen.) | m9zWBn1Y2j | 3.0 | R1 | Weak novelty and baselines; SIGMADOCK far stronger |
| DynamicsDiffusion | kKXIYUi8ff | 3.0 | R1 | MD trajectory generation, limited results; not comparable in quality |
| TorSeq | G536mmC2HL | 3.0 | R1 | Torsional conformer gen., rejected for weak evaluation |
| GNNAS-Dock | An87ZnPbkT | 3.0 | R1 | Algorithm selection wrapper, fundamentally different scope |
| Toric varieties diffusion | FuXtwQs7pj | 4.5 | R1 | Novel math but limited practical impact |
| DiffDock-Pocket | 1IaoWBqB6K | 5.0 | R1 | Incremental DiffDock extension; SIGMADOCK is more novel and achieves stronger results |
| DiffMaSIF | S4zpk61r6G | 4.67 | R1 | Protein-protein docking diffusion; weaker evaluation |
| Protein inverse problems | UYZRaUCLAg | 5.33 | R1 | Different problem; mixed reception |
| VFDiff | 5YLsnsjgeC | 6.0 | R1 | SE(3) equivariant diffusion for SBDD; rejected despite 6.0 avg; SIGMADOCK has stronger empirical validation |
| IPDiff | qH9nrMNTIW | 6.25 | R1 | Interaction prior for diffusion docking; SIGMADOCK has stronger theory and results |
| DockGen/Deep Confident Steps | UfBIxpTK10 | 6.0 | R1 | Benchmark + confidence bootstrapping for docking generalization; accepted. SIGMADOCK has stronger theoretical contribution and achieves SOTA rather than improving generalization on a new benchmark |
| Equivariant diffusion design space | kzGuiRXZrQ | 5.75 | R1 | Design space exploration for molecular generation; accepted but lower impact |
| FoldFlow SE(3) | kJFIH23hXb | 8.0 | R1 | SE(3) flow matching for proteins; strong theory + clean presentation, unanimous 8s. Comparable theoretical depth but SIGMADOCK has more impactful empirical results (first DL > classical) though slightly less clean presentation |
| GeoBFN | NSVtmmzeRB | 8.0 | R1 | Bayesian flow networks for 3D molecules; strong but different domain |
| ProtComposer | 0ctvBgKFgc | 8.0 | R1 | Compositional protein generation; strong but different application |
| Protein Walk-Jump Sampling | zMPHKOmQNb | 8.0 | R1 | Discrete generative for antibodies; strong but different application |

**Round 1 bracket: 7.0–8.0**

SIGMADOCK clearly exceeds all score-6 papers: it has stronger theoretical grounding (Theorem 1 + Lemma 1 + Theorem 2), achieves a genuine milestone (first DL method to beat classical docking under PB-valid), and demonstrates exemplary evaluation practices. Compared to score-8 papers like FoldFlow, SIGMADOCK has comparable theoretical depth and arguably greater practical significance, but has a presentation issue in its main results figure that creates unnecessary confusion, and limited evaluation scope (re-docking only). The presentation issue is fixable and does not undermine the core contribution; the scope is explicitly stated and appropriate.

**Final score: 7.5** — The paper makes a significant, well-executed contribution with principled theory, careful engineering, and strong empirical results under rigorous evaluation. The presentation issue in Figure 4/abstract is the primary concern keeping it from a clear 8, alongside the absence of a controlled torsional-vs-fragment ablation. But the core contribution — demonstrating that fragment-based SE(3) diffusion with structural chemistry inductive biases can for the first time push DL docking past classical methods on PB-valid evaluation — is genuine and important.

**Decision: Accept.** The contribution is substantial, the methodology is sound, and the weaknesses are addressable. The paper advances the state of the art in its chosen setting and introduces ideas (FR3D, triangulation conditioning, SE(3)^m fragment diffusion) that are likely to influence future work in molecular docking.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>