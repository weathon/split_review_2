Here is the final consolidated review.

---

## Summary

SIGMADOCK proposes a fragment-based SE(3) diffusion model for molecular docking. The key idea is to decompose ligands into rigid-body fragments via a novel FR3D scheme and define diffusion in SE(3)^m, bypassing the complications of torsional parameterization. The paper provides a theoretical critique of torsional models (Theorem 1), introduces triangulation constraints to encode geometric priors, and demonstrates strong empirical results on PoseBusters (79.9% PB-valid Top-1) and Astex (90.6%), substantially surpassing prior deep learning methods and becoming the first deep learning approach to exceed classical physics-based docking on the intended PB train-test split.

## Strengths

1. **Novel and physically well-motivated fragmentation scheme (FR3D).** The decomposition of ligands into rigid-body fragments with diffusion in SE(3)^m is genuinely new. The paper provides a clear physical rationale (Section 2.2.1): bond lengths and angles are effectively fixed by thermodynamic constraints, making roto-translations of rigid fragments the relevant degrees of freedom. This is a clean inductive bias.

2. **Theoretical diagnosis of a real problem with torsional models (Theorem 1).** The observation that torsional models induce non-product measures in Cartesian space, creating entangled implicit dynamics, is a genuine insight. The paper correctly identifies that independent noise in torsion space becomes correlated in Cartesian space, producing ill-conditioned learning. The discussion of gauge ambiguity (Section 2.2.2) — the need to choose which side of the bond to rotate — is also insightful and well-articulated.

3. **Strong empirical results.** SIGMADOCK's PB-valid Top-1 of 79.9% represents a large jump over prior methods — roughly 6.3× higher PB-validity than DiffDock (~12.7%). Even comparing RMSD-only metrics (80.5% vs 58.1% for G2G/Vibe2), the improvement is ~22 percentage points. This is the kind of leap that could change practice in computational drug discovery.

4. **Well-structured ablation study (Table 1).** The ablations isolate triangulation conditioning, fragment merging, protein-ligand interactions, energy scoring, and PB scoring. Each ablation produces meaningful drops, confirming the contribution of multiple components. Retraining for architectural ablations (A-C) follows correct protocol.

5. **Co-factor failure analysis (Table 2) adds credibility.** The finding that failure rates are highest when co-factors are present (41.2% for natural ligands) and lowest without co-factors (16.2%) supports the claim that the model learns genuine protein-ligand physics rather than memorizing spurious correlations.

6. **Pocket-size sensitivity analysis (Table 3).** Systematic variation of the pocket definition cutoff provides a useful robustness check that many docking papers omit.

## Weaknesses

### Fatal

None.

### Major

1. **Metric ambiguity in the main comparison table (Figure 4).** The table column "PB (%)" mixes different metrics without clear annotation. SIGMADOCK's 79.9% is explicitly PB-valid (the paper states "Top-1 (RMSD & PB validity) of 79.9%"). However, the baselines' numbers (e.g., DiffDock at 38.0%, G2G at 58.1%) are RMSD-only — DiffDock's actual PB-validity is ~12.7% (derivable from the paper's own "6.3× higher PB-validity than DiffDock" claim: 79.9/6.3≈12.7). The abstract's 12.7-32.8% range refers to baseline PB-validity, which is not directly readable from the table. Presenting all values under a single "PB (%)" header without distinguishing RMSD-only from PB-valid makes the comparison ambiguous. The actual improvement is even larger than the table visually suggests, but the presentation undermines reader trust. The authors should report the same metric for all methods or clearly annotate each entry. *(Anchored in: Figure 4 table, lines 192, 200-209)*

2. **AF3 per-bin comparison (Table 4) is not interpretable as presented.** The per-bin counts differ substantially between SIGMADOCK and AF3 (109 vs 38 for [0,30), 76 vs 83 for [30,95), 123 vs 187 for [95,100]) despite both totaling 308 complexes. This indicates different sequence similarity definitions, binning thresholds, or evaluation protocols for AF3 (values extracted from Abramson et al., 2024). The per-bin breakdowns therefore cannot be meaningfully compared. The total averages (79.9% vs 80.2%) are still valid and support the claim of competitive performance, but the granular evidence used to discuss generalization to novel proteins does not hold up. *(Anchored in: Table 4, lines 267-274)*

### Minor

3. **Unsupported "50× faster sampling than AF3" claim.** The paper states "50× faster sampling" (line 194) without any supporting wall-clock time data, throughput comparison, or setup description. Given that AF3 is a co-folding model solving a different (harder) task, the comparison also mixes problem definitions. This quantitative claim should be substantiated with timing data or qualified appropriately.

4. **Foundational alignment evidence absent from main text.** The claim that conformers from M_c align to bound poses with RMSD ≪ 2Å is foundational to the approach (it justifies the entire fragment assumption). Yet the main text shows only one example (Figure 2b: PDB 1Q4G, RMSD 0.11Å), with systematic analysis deferred to Appendix D.3. Summary statistics (mean/median/P99 alignment error across the dataset) should be in the main text. *(Anchored in: lines 86-90, Figure 2b)*

5. **Two rows for "Ours" in Figure 4 are unexplained.** The table shows "Ours" twice (79.9% and 80.6%, both with AX 90.6%) without clarifying whether these represent different metrics (PB-valid vs RMSD-only), different configurations, or different numbers of seeds. This adds to the metric confusion. *(Anchored in: lines 208-209)*

6. **Fragmentation stochasticity at test time is not specified.** FR3D performs "stochastic search" characterized as data augmentation (Section 2.2.3). The paper does not state whether test-time fragmentation is deterministic (e.g., via fixed seed) or stochastic, which affects reproducibility. *(Anchored in: lines 106-112, Figure 3 caption)*

### Trivial

7. **Architecture description is brief.** Section 2.4 describes the architecture at a high level (EquiformerV2 backbone, virtual nodes, SO(3)-equivariant prediction head) with key details deferred to appendices. Acceptable for main text but notable since the architecture is described as "a significant contribution."

## Nice-to-Haves

- **Controlled comparison: torsional vs. fragment diffusion under matched conditions.** The paper criticizes torsional models theoretically but does not build a torsional variant of SIGMADOCK for direct comparison. A controlled experiment holding architecture, data, and training constant while varying only the parameterization would directly and convincingly isolate the benefit of the fragment approach.
- **Confidence intervals or variance estimates.** All results are point estimates without error bars. Given the use of 40 seeds and stochastic fragmentation, reporting standard errors would strengthen the reliability of claims.
- **Comparison of the ranking heuristic to a trained confidence model.** The paper claims no trained confidence model is needed (Section 2.5), but removing energy scoring drops Top-1 from 79.9% to 66.1% (Table 1, config D). A direct comparison to DiffDock's trained confidence model on the same data would contextualize how much the heuristic contributes to the gap.
- **Inclusion of Vina in the main comparison table.** Vina (57.2% Top-1) appears only in the pocket-sensitivity analysis (Table 3 discussion). Including it in the main table would strengthen the claim of surpassing classical methods.

## Removed Points

These points were flagged by the harsh critic but removed after verification against the paper:

- **"Torsional-space baselines claim is unsupported"** — REMOVED. The claim (line 192) is supported by the data in Figure 4 (DiffDock at 38.0%, G2G at 58.1%, Vibe2 at 58.1% vs SIGMADOCK at 79.9-80.6%). The evidence for the claim is presented in the same section.
- **"Theorem 1 is not mathematically precise"** — REMOVED. The theorem is stated at an appropriate level for the main text with proof deferred to Appendix C.2, which is standard practice.
- **"Introduction unfairly lumps AF3 limitations"** — REMOVED. Comparing to AF3 on re-docking is a legitimate framing choice; the paper acknowledges AF3 solves a different (co-folding) task.
- **"Missing related work"** — REMOVED per policy: external literature verification cannot be performed.
- **Formatting and grammatical nitpicks** — REMOVED per policy (parser artifacts are not author errors).
- **"Architecture description too brief / details in appendix"** — Demoted to Trivial per policy (missing appendix sections are a parser artifact).

## Novel Insights

None beyond the paper's own contributions. The reviews did not uncover a perspective on the work that the authors themselves have not already articulated.

## Suggestions

1. **Fix the metric reporting in Figure 4.** Clearly annotate whether each value is RMSD-only or PB-valid. Better yet, report both metrics for all methods where the data is available, or add a footnote explaining the discrepancy with the abstract's range.
2. **Fix the AF3 per-bin comparison (Table 4).** Either recompute the per-bin breakdowns using matching definitions, or replace with total averages only and qualify the comparison as approximate (different binning between studies).
3. **Add summary statistics** (mean/median/P99) of the M_c-to-bound alignment error to Section 2.2.1 main text, rather than deferring entirely to Appendix D.3.
4. **Substantiate or remove the "50× faster sampling" claim** — provide wall-clock timing data under comparable hardware settings.
5. **Clarify test-time fragmentation determinism** — state whether FR3D uses a fixed seed at inference or if fragmentation is stochastic.

## Score and Decision

**Calibration anchors retrieved across rounds:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| DiffDock-Pocket | 5.00 | R1 lower | Weaker method and results, less thorough analysis |
| CompassDock | 3.00 | R1 mid-low | Focused on data assessment, not generative method |
| IPDiff | 6.25 | R1 mid | Weaker theoretical contribution, comparable novelty |
| GroupBind | 6.75 | R1 mid-high | Less novel method, comparable acceptance quality |
| Deep Confident Steps | 6.00 | R1 mid | Stronger on benchmark contribution, weaker on novel method |
| FoldFlow | 8.00 | R1 high | Protein backbone generation (different sub-area), very strong |

**Round-1 bracket:** 6.0 – 8.0 (based on comparison to docking papers scoring 5-7 and protein generation papers scoring 8).

**Final score:** 7.5. The paper's core contributions (novel FR3D fragmentation, SE(3)^m diffusion framework, theoretical critique of torsional models, and SOTA empirical results with thorough analysis) place it clearly above the docking papers scoring 5-7. The presentation issues (metric table ambiguity, AF3 per-bin comparison) are genuine weaknesses that prevent a higher score but do not undermine the core scientific contribution, which is substantial.

**Decision:** Accept

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>