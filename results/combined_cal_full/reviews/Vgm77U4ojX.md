Now I'll produce the final consolidated review.

## Summary

SIGMADOCK introduces a fragment-based SE(3) Riemannian diffusion model for molecular docking. Rather than operating on torsional angles (the dominant paradigm), it decomposes ligands into rigid-body fragments via a novel fragmentation scheme (FR3D), diffuses on SE(3)^m, and learns to reassemble fragments within the binding pocket. The paper reports a Top-1 PB-valid rate of 79.9% on the PoseBusters set, substantially exceeding prior deep learning approaches and surpassing classical physics-based docking (Vina) under the re-docking protocol.

## Strengths

- **Clear empirical advance on PoseBusters.** The paper reports a Top-1 PB-valid rate of 79.9% on the PoseBusters set, substantially above the 12.7–32.8% range cited for prior deep learning approaches and above the ~57% reported for Vina. The result is supported by a reasonable ablation study (Table 1) showing that the main components contribute positively. This is a genuine step change in performance on this benchmark.

- **Well-motivated alternative to torsional diffusion with theoretical grounding.** The argument that torsional models suffer from non-local coupling and ambiguous gauge choices (Section 2.2.2) is clearly articulated. Theorem 1 shows that fragment-space diffusion yields a factorized product of Haar measures while torsional models produce entangled measures — a genuine theoretical insight that motivates why the learning problem is simpler in fragment space.

- **Honest failure analysis.** Table 2 breaks down performance by co-factor presence, showing that failure rates are substantially higher when co-factors are involved (41.2% for natural ligands vs 16.2% for none). The paper acknowledges this is expected since co-factors are excluded from the model's input. This diagnostic analysis builds trust in the method's understanding.

- **Clean experimental discipline.** Restricting training exclusively to PDBBind(v2020) rather than augmenting with additional data (as DiffDock-L does) is a principled choice that isolates the contribution of the method from the contribution of more data. The deliberate use of the PB train-test split and reporting of sequence-similarity breakdowns (Table 4) address legitimate concerns about memorization vs. generalization.

- **Robustness analysis with practical value.** Table 3 shows SIGMADOCK remains competitive across a range of pocket definitions, and the method does not require expensive post-hoc minimization or a separately trained confidence model to filter generations.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The degrees-of-freedom framing in the abstract and introduction is overstated.** The paper claims to "reduce the additional degrees of freedom introduced from fragmentation" (line 22), but the paper's own arithmetic shows: torsional models have k+6 DoF, the fragment model has between k+6 (triangulation lower bound) and 6m ≈ 4k+4 (upper bound, with m ≈ ⅔(k+1)). At best the fragment model matches the torsional model's DoF; at worst it has substantially more. The paper's real strength is the factorization argument (Theorem 1) — that the forward kernel in fragment space factorizes while torsional dynamics are entangled — not DoF reduction. The paper should lead with this factorization argument and drop the misleading DoF reduction framing.

- **The abstract's comparison against prior methods is not fully traceable to the paper's own tables.** The abstract claims "79.9%... compared to 12.7-32.8% reported by recent deep learning approaches." However, the paper's main comparison table (Figure 4) shows baseline Top-1 rates of 15.9%, 38.0%, and 58.1% — none of which fall within the 12.7-32.8% range. The 12.7-32.8% range appears to come from external evaluations of other methods' PB-valid rates (Butenschön et al., 2024; Harris et al., 2023). While these external numbers are cited, the paper's main comparison table does not report PB-valid rates for baselines in a directly comparable way to SIGMADOCK's combined RMSD<2+PB-valid metric. At line 192, the paper claims "6.3× higher PB-validity than DiffDock" — but DiffDock is listed at 38.0% in Figure 4, which would imply a PB-valid rate of ~12.7% for DiffDock if the 6.3× factor is correct. The table should be clearer about which metric (RMSD<2 only vs. PB-valid) is reported for each method.

- **The AF3 comparison (Table 4) is presented as showing "AF3-level performance" (79.9% vs 80.2% overall), but on the low-similarity regime ([0,30) sequence similarity) — the hardest generalization test — AF3 outperforms SIGMADOCK by 15 percentage points (87% vs 72%).** SIGMADOCK only catches up in aggregate because it has more samples in the high-similarity regime where it does better (123 vs 187 for [95,100]), and the per-bin sample counts differ between methods. The paper should prominently acknowledge this distributional difference and discuss its implications, regardless of the different task difficulty (AF3 solves a harder co-folding problem).

- **The "data efficiency" claim** in the conclusion ("principled inductive biases in enabling superior generalisation and data efficiency") is asserted without direct experimental evidence. The paper does not vary training set size. While achieving strong results with 19k complexes (the standard PDBBind size) is commendable and the claim about data efficiency relative to AF3 is reasonable (AF3 trains on much more data), a dedicated data-scaling experiment would substantiate the claim.

### Trivial
None.

## Nice-to-Haves

- **Re-center the motivation on factorization, not DoF reduction.** The paper's strongest theoretical argument is Theorem 1. The factorization argument is what genuinely distinguishes the method from torsional models; the DoF framing should be de-emphasized.

- **Report PB-valid rates for all baselines in the main comparison table.** The paper already distinguishes RMSD<2 from PB-valid in its own ablation (Table 1). The main results table should do the same for baselines.

- **Acknowledge the AF3 low-similarity deficit explicitly** in the main text (not just in the table), and discuss what this implies about the methods' relative generalization.

- **Add confidence intervals or bootstrap estimates.** Given the benchmark size (308 complexes), even a few percentage points of variance could change rankings. This is not standard practice in the field but would strengthen the evaluation.

## Removed Points

These points were filtered from the input review under the removal rules. They are listed here for transparency but should not be considered active weaknesses.

1. **Criticism about the re-docking scope limiting the "surpassing classical docking" claim.** *Removed because the paper already explicitly qualifies this at lines 24–26: "We adopt the standard re-docking protocol..." and "extensions to flexible-receptor docking and co-folding... we leave as future work." The paper clearly bounds its scope.*

2. **Criticism about FR3D stochastic merge process being underspecified.** *Removed because the paper references Algorithm 1 in Appendix D.4, which was stripped by the parser. Details exist in the original submission.*

3. **Criticism about the architectural description being brief.** *Removed because the paper references Appendix G for architectural details, which was stripped by the parser.*

4. **Criticism that the paper does not acknowledge a gauge issue in the fragment model.** *Removed because the paper addresses this directly with Theorem 2 and the Newton-Euler prediction head (Section 2.4), explicitly proving invariance to the choice of local coordinate axes.*

5. **Criticism about missing inference cost comparison with torsional diffusion methods.** *Demoted to Nice-to-Have. This would be informative but is not a core flaw.*

6. **Criticism about missing statistical significance / confidence intervals.** *Demoted to Nice-to-Have. Single-run evaluation is standard in this benchmark setting.*

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's strengths (strong empirical results, novel fragment-based approach, honest failure analysis) and surface some framing issues (DoF claims, AF3 comparison nuance, abstract traceability) that the authors should address. No reviewer identified a methodological flaw that would invalidate the core contribution.

## Suggestions

1. Re-center the theoretical motivation on the factorization argument (Theorem 1) rather than DoF reduction, which the paper's own arithmetic contradicts.
2. Report PB-valid rates explicitly in the main comparison table for all baselines, alongside RMSD<2 rates, so readers can directly verify the headline comparison.
3. In the AF3 discussion, prominently acknowledge the 15-point deficit on the low-similarity regime ([0,30)) and discuss what this implies about generalization.
4. Either add a data-scaling experiment (e.g., training on subsets of PDBBind) to substantiate the data efficiency claim, or remove the claim from the conclusion.

## Score and Decision

**Calibration anchors consulted:**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| DiffDock-Pocket (1IaoWBqB6K) | 5.00 | R1 | Yes | Docking diffusion paper criticized for incremental novelty over DiffDock; SIGMADOCK is substantially more novel (fragment-based approach) and has stronger empirical results |
| CompassDock (nWO75tVjfp) | 3.00 | R1 | Yes | Docking evaluation paper with fatal methodological flaw (non-gradient-tracked loss); SIGMADOCK has no comparable fatal issues |
| Deep Confident Steps (UfBIxpTK10) | 6.00 | R1 | Yes | Docking generalization paper with valuable new benchmark; SIGMADOCK has stronger empirical results but shares thorough experimental discipline |
| IPDiff (qH9nrMNTIW) | 6.25 | R2 | Yes | Ligand generation paper with novelty concern (-7.36 weight); SIGMADOCK's strongest negatives are -3.25 range, and its positive weights (+7.29, +6.29) are notably stronger |
| Protein SLM (OzUNDnpQyd) | 7.00 | R2 | Yes | Protein conformation paper with misleading presentation (-5.08) and novelty (-6.61) concerns. SIGMADOCK's negatives are milder |

**Weighted-item comparison:** SIGMADOCK's strongest positive weights — empirical advance (+7.29) and theoretical motivation (+6.29) — exceed those of the scoring 6.0–6.25 anchors. Its strongest negative weight (-3.25 for abstract traceability) is significantly milder than the -7.36 novelty concern of IPDiff (6.25) or the -5.08 misleading-table issue of SLM (7.0). The Round-1 bracket was [5.5, 8.5], and comparison with the itemized anchors narrows this to [6.5, 7.5]. The final score of **7.0** reflects a paper with a genuinely novel method and strong empirical results, held back from the 8+ range only by presentation-level framing issues that require revision.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>