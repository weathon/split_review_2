Now I have enough calibration data. Let me write the final consolidated review.

**Bracket reasoning:**
- Round 1 range: Score 6–8 (comparing to DiffDock-Pocket at 5.0, IPDiff at 6.25, GroupBind at 6.75 vs FoldFlow at 8.0)
- Round 2 narrowing: Score 6.5–7.5 (Stiefel Flow Matching at 7.0, DrugFlow at 6.67, MAGNet at 7.25)
- Final: 7.0 — the paper has a genuinely novel method and strong results, but presentation/framing issues (abstract number discrepancy, classical docking not in main comparison table, AF3 table bin mismatch) prevent it from reaching the 7.5+ level of papers like FoldFlow.

Here is the final review.

---

## Summary

SIGMADOCK proposes a fragment-based SE(3) Riemannian diffusion model for molecular re-docking. The key idea is to decompose a ligand into rigid-body fragments by breaking rotatable bonds, then learn to reassemble them within a known binding pocket via diffusion on SE(3)^m. The paper reports 79.9% Top-1 (RMSD < 2Å + PB-valid) on PoseBusters, substantially exceeding prior deep learning methods, and claims to be the first deep learning approach to surpass classical physics-based docking under the PB train-test split.

## Strengths

1. **Novel and well-motivated representation.** The fragment-based SE(3)^m decomposition is a genuine departure from torsional models. Theorem 1 provides a principled argument that torsional updates produce entangled, non-product induced measures in Cartesian space, whereas fragment SE(3)^m yields factorised Haar measures. This is a real conceptual advance in the design space for generative docking, not an incremental modification.

2. **Strong empirical results with thorough ablations.** The headline 79.9% Top-1 (RMSD + PB-valid) on PoseBusters substantially exceeds prior DL methods under comparable conditions (e.g., DiffDock at 38.0%). The ablation study (Table 1) systematically isolates the contributions of triangulation conditioning, fragment merging, protein-ligand interactions, and the ranking heuristic. The generalization across sequence similarity splits (Figure 4, right) suggests the model learns physics rather than memorizing training complexes. The co-factor failure analysis (Table 2) provides additional insight into failure modes.

3. **Data efficiency.** Training only on PDBBind v2020 (~19k complexes) and reaching performance competitive with AF3 (trained on orders of magnitude more data) is a genuine achievement. The paper correctly frames this as a meaningful contribution that demonstrates the value of principled inductive biases over scale alone.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Abstract's 12.7-32.8% claim is not tied to the results table.** The abstract states prior deep learning approaches achieve "12.7-32.8%" Top-1, but the main comparison table (Figure 4, left) shows DiffDock at 38.0%, G2G at 58.1%, and Vibe2 at 58.1% — all above 32.8%. The paper never explains where the 12.7-32.8% range comes from or whether it refers to a different metric (e.g., PB-valid vs RMSD-only). If prior methods' PB-valid numbers are substantially lower than their RMSD-only numbers, stating this distinction explicitly in the abstract and the table caption would resolve the confusion. As written, a reader cannot reconcile the paper's headline number with its own results.

2. **Classical docking baselines missing from the main comparison table despite being central to a key claim.** The paper advertises being "the first deep learning approach to surpass classical physics-based docking" (abstract and line 192), yet Figure 4's left panel includes no classical docking methods. The only classical result — Vina's 57.2% Top-1 — appears in the pocket-sensitivity discussion (line 256) rather than the main benchmark table. The figure caption states "(*) Denotes classical docking" but no such markers appear in the table rows. For a flagship claim, the evidence should be front and center.

3. **Table 4's per-bin AF3 comparison uses different bin definitions.** The count distributions across sequence-similarity bins differ between SIGMADOCK (109/76/123 complexes) and AF3 (38/83/187), indicating different bin definitions or similarity metrics. This means per-bin comparisons (e.g., "72% vs 87% in [0,30)") compare different sets of complexes and are not directly interpretable. The paper does not discuss whether the total average difference (79.9% vs 80.2%) is statistically significant. While the paper does not make strong per-bin claims, the table as presented invites misleading comparisons.

4. **The ranking heuristic accounts for substantial performance but is under-described in the main text.** The ablation (Table 1, config D) shows removing energy scoring drops Top-1 from 79.9% to 67.2% — a 12.7 point swing. Yet the main text describes the heuristic only as "pseudo binding energy" and "physicochemical checks" (line 176) and defers details to the appendix. A reader of the main paper alone cannot assess what fraction of the reported performance comes from the generative model versus the post-hoc selection rule. Providing a concise summary of the heuristic's components in the main text would significantly strengthen the paper.

5. **The AF3-level performance claim spans different task settings.** The paper states "we achieve AF3-level performance" (line 194), but SIGMADOCK operates in the re-docking setting (holo-conformation, known pocket) while AF3 solves co-folding without a specified receptor conformation — a fundamentally harder task. The paper acknowledges this once ("Although we cannot directly compare SIGMADOCK to co-folding methods," line 256), but the surrounding framing ("AF3-level performance," "50× faster sampling") invites apples-to-apples comparisons that do not hold. This should be more prominently caveated.

### Trivial
None.

## Nice-to-Haves

- Adding confidence intervals or variance estimates for the main results (79.9%, 90.6%) would help assess whether differences between configurations are significant, though single-run Top-k benchmarking is standard in this field.
- Reporting actual wall-clock inference times for SIGMADOCK and baselines would substantiate the "50× faster sampling" claim, which currently lacks concrete numbers.
- Comparing the ranking heuristic against learned confidence models (e.g., DiffDock's confidence model) would strengthen the argument that a simple heuristic suffices.

## Removed Points

- **"Figure 4 caption says (*) denotes classical docking but no markers appear"** — Partially a parser artifact (the original image may have markers). The substantive point (classical methods absent from the main text table) is retained in Weakness #2.
- **"Confidence intervals / variance are missing"** — Moved to Nice-to-Haves since single-run Top-k evaluation is standard practice in this field.
- **"Inference time not reported"** — Moved to Nice-to-Haves since the paper does not claim to provide detailed timing benchmarks.
- **"The introduction conflates co-folding and re-docking"** — A presentation suggestion that does not affect the core claims.
- **"Architecture description is terse"** — Standard for conference papers with appendix space; does not affect evaluation.
- **"Table 1 mixes train-time and test-time ablations"** — A minor presentation choice, not a weakness.
- **Strength "Strong empirical results" (from harsh critic)** — Retained as Weakness #1 caveat: the numbers are strong, but the abstract's framing is confusing.
- **Strength "Data efficiency"** — Retained as Strength #3 with specific evidence.
- **Section-by-section notes about conformational manifold evidence and torsional model critique** — These are presentation suggestions that don't impact core claims or could reasonably be in appendices.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's main novel observation — the framing inconsistency between the abstract's 12.7-32.8% range and the results table — is already captured in Weakness #1.

## Suggestions

1. Add a column to the main comparison table (Figure 4) for classical docking baselines (Vina, Glide) and annotate each method's metric (RMSD-only vs PB-valid) clearly. This directly substantiates the flagship claim of surpassing classical docking.
2. State explicitly in the abstract and main text what the 12.7-32.8% range refers to (e.g., "PB-valid results for prior DL methods under the same split") and ensure the numbers are consistent with cited sources.
3. In Table 4, either harmonize bin definitions with AF3 or explain why they differ, and add a caveat that per-bin numbers should not be directly compared across methods.
4. Provide a concise description of the ranking heuristic's components (pseudo-binding energy calculation, specific physicochemical checks) in the main text with a pointer to the appendix for full detail.
5. When comparing to AF3, include a prominent caveat in the comparison text that SIGMADOCK uses the holo-conformation and known binding pocket while AF3 solves a harder co-folding task.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| DiffDock-Pocket (1IaoWBqB6K) | 5.00 | R1 | Lower novelty; missing baselines; weaker results |
| IPDiff (qH9nrMNTIW) | 6.25 | R1 | Comparable novelty but methodological concerns about SE(3) equivariance |
| GroupBind (zDC3iCBxJb) | 6.75 | R1 | Clearer presentation; less novel idea (grouping vs fragment SE(3)^m) |
| Stiefel Flow Matching (84WmbzikPP) | 7.00 | R2 | Similar novelty level; comparable empirical thoroughness |
| DrugFlow (g3VCIM94ke) | 6.67 | R2 | Broader scope (de novo design); similar methodological rigor |
| FoldFlow (kJFIH23hXb) | 8.00 | R1 | Stronger theoretical framing; cleaner presentation; protein backbone generation |

**Round 1 bracket:** 6–8 → **Round 2 narrowing:** 6.5–7.5 → **Final score:** 7.0

SIGMADOCK makes a genuinely novel methodological contribution (fragment-based SE(3)^m diffusion with a principled critique of torsional models) and backs it with strong empirical results. The presentation issues (abstract number discrepancy, classical docking not in the main table, AF3 table bin mismatch) are real but fixable and do not undermine the core contribution. The paper sits comfortably alongside other solid-accept papers like GroupBind (6.75) and Stiefel Flow Matching (7.0), with a slightly more novel method but somewhat less polished presentation.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>