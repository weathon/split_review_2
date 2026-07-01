Now let me write the final review.

## Summary

SIGMADOCK proposes a fragment-based SE(3) diffusion model for molecular docking. Instead of operating in torsion space (the dominant paradigm), the method decomposes ligands into rigid-body fragments and diffuses over their SE(3) poses. A novel fragmentation reduction scheme (FR3D) and soft triangulation constraints reduce the degrees of freedom, while an EquiformerV2-based architecture with a Newton-Euler rigid-body prediction head provides SO(3)-equivariance. The paper reports a Top-1 PB-valid success rate of 79.9% on PoseBusters, substantially outperforming prior deep learning methods trained on the same split and matching AF3-level performance with far less data and compute.

## Strengths

- **Principled theoretical motivation for fragment-based diffusion (Section 2.2.2).** Theorem 1 identifies a concrete pathology of torsional models: the induced measure in Cartesian space is a non-product distribution, creating entangled score dynamics that complicate learning. The fragment approach yields a factorised product of Haar measures on SE(3)^m. This is a genuine insight that goes beyond engineering convenience. Lemma 1's triangulation constraints provide inductive biases on bond lengths/angles without freezing dihedrals — an elegant middle ground between full flexibility and rigid constraints.

- **Strong empirical results with clean ablations (Section 3.2, Table 1).** The 79.9% Top-1 PB-valid on PoseBusters is a substantial advance over prior methods trained on the same split (6.3× improvement over DiffDock in PB-validity). The ablation study is informative and well-structured: triangulation conditioning (+6.7%), fragment merging (+6.2%), and protein-ligand interactions (+3.6%) each contribute meaningfully, validating the design choices. The result is consistently reported across abstract, main text, and Table 1.

- **Careful experimental protocol.** Training exclusively on PDBBind(v2020) and using the PoseBusters train-test split avoids the data-leakage confounds that plague many comparisons in this area. Footnote 9 explicitly states which baselines are on the same split, and the paper correctly excludes methods trained on larger corpora from the main comparison.

- **Informative generalization diagnostics (Tables 2–4).** The co-factor analysis (Table 2: 58.8% with natural ligands vs. 84.2% without) provides meaningful evidence that the model learns physical interactions rather than memorizing training complexes. The pocket-size sensitivity (Table 3) shows graceful degradation.

## Weaknesses

### Fatal
None.

### Major

- **Internal inconsistency between the overall Top-1 success rate and the per-sequence-similarity breakdown (Figure 4, right).** The right panel of Figure 4 reports Top-1 rates of ~51–53% across sequence-similarity bins. Weighted by bin counts (109, 76, 123), this gives an average of ~52.3%. However, the paper's headline result is 79.9% (PB-valid) / 80.5% (RMSD < 2Å) — a gap of >27 percentage points. The paper never acknowledges or explains this discrepancy. Even the most degraded ablation in Table 1 (Configuration D, without energy scoring) reports 67.2% RMSD and 66.1% PB-valid, well above 52%. The per-seq-sim panel may use a different metric, a different number of seeds, or a different ranking heuristic, but none of this is stated. This is the single most important issue for the authors to address: it does not invalidate the core claim (79.9% is consistently reported elsewhere), but it is a significant reporting gap that undermines confidence in the paper's internal consistency.

- **Table 4's per-sequence-similarity comparison with AF3 is not a valid per-bin comparison.** SIGMADOCK and AF3 have dramatically different bin counts across the same sequence-similarity intervals: [0,30) has 109 vs 38; [30,95) has 76 vs 83; [95,100] has 123 vs 187 (both sum to 308 total). This indicates different definitions or implementations of sequence similarity. Presenting a "per-sequence-similarity comparison" under these conditions is misleading — the per-bin values evaluate different subsets and are not directly comparable. Only the aggregate comparison (79.9% vs 80.2%) is valid. The authors should either recompute AF3's performance on identical bins or clearly state that per-bin comparisons are not meaningful.

### Minor

- **The abstract's "12.7–32.8%" baseline range lacks sufficient context.** This range evidently refers to PB-valid numbers of methods trained on the same PB train-test split (DiffDock's PB-valid is ~12.7% given the 6.3× factor stated in the text). However, the abstract does not clarify this, and readers familiar with Figure 4's left table (which shows G2G and Vibe2 at 58.1% on "PB (%)") may reasonably be confused about what metric the range covers and which baselines are included. The comparison is not wrong, but the framing could be more transparent.

- **Classical docking baselines are not prominently displayed in the main comparison table.** The paper claims to be "the first deep learning approach to surpass classical physics-based docking," which is a strong claim. Vina (~57%) is mentioned only in the pocket-sensitivity discussion (Table 3 context), and the footnote "(*) Denotes classical docking" refers to markers not visible in the main table. The evidence likely supports the claim, but the reader cannot verify it at a glance.

- **No statistical uncertainty reported.** Top-1 success rates are reported as point estimates without confidence intervals, standard deviations, or statistical tests. On a 308-complex benchmark, a 3–4% difference could fall within sampling noise. This is common practice in docking papers, but given the strong SOTA claims, bootstrapped confidence intervals would strengthen the empirical case.

- **The impact of FR3D stochasticity is not evaluated.** FR3D performs a stochastic search over possible fragment mergings. The paper does not ablate how different fragmentations of the same ligand affect downstream performance, leaving open the question of sensitivity to the fragmentation outcome.

### Trivial
None.

## Nice-to-Haves

- Reporting wall-clock sampling time for SIGMADOCK alongside the "50× faster than AF3" claim would make the efficiency comparison concrete.
- A quantitative summary of the alignment experiment in Section 2.2.1 (e.g., fraction of complexes with aligned RMSD < 0.5Å, < 1Å) would strengthen the justification for treating fragment internal geometries as fixed.
- Including Vina directly in the main comparison table with aligned metrics would cleanly validate the "first to surpass classical docking" claim.

## Removed Points

These points from the input review are removed or downgraded because they are factually incorrect, speculative, or violate the filtering guidelines:

- **"Abstract's 12.7-32.8% contrast is misleadingly selective due to metric mismatch"** — The harsh critic claimed the abstract compares SIGMADOCK's PB-valid number against other methods' RMSD-only numbers. This is incorrect: the paper states "6.3× higher PB-validity than DiffDock," confirming DiffDock's PB-valid is ~12.7%. The range refers to PB-valid numbers of methods on the same split. The clarity concern is retained as a Minor weakness, but the metric-mismatch accusation is removed.

- **"AF3 comparison claim of 'AF3-level performance' is not supported"** — The aggregate totals (79.9% vs 80.2%) support the claim; the problem is specifically with the per-bin display. The per-bin display issue is retained as Major; the stronger claim that the evidence is unsupported is removed.

- **"Sampling cost not quantified"** — Demoted to Nice-to-Have (generic request, not a core flaw).

- **"No confidence model needed" claim not costed** — Same as above, demoted to Nice-to-Have.

## Novel Insights

The most useful observation emerging from the review is the verifiable ~27 percentage point gap between the per-sequence-similarity breakdown (~52%) and the headline result (~80%) in Figure 4. This is not a speculation — it is directly calculable from the paper's own table. The gap is wider than any ablation condition in Table 1, strongly suggesting a different evaluation protocol (e.g., fewer seeds, no ranking heuristic) is used in the per-seq-sim panel without being disclosed. This is the single issue that most needs clarification. The AF3 per-bin comparison issue (Table 4) is also noteworthy: the different bin counts are visible from the paper itself and make clear that what is presented as per-slice comparison is actually two different binnings side by side.

## Suggestions

1. **Reconcile the per-sequence-similarity breakdown with the overall result.** State explicitly what metric, number of seeds, and ranking heuristic (if any) are used in the right panel of Figure 4. If it uses a different protocol, say so clearly. If it is wrong, fix it.
2. **Make the AF3 comparison honest.** Either recompute AF3's numbers on identical sequence-similarity bins, or state clearly that only the aggregate is comparable and the per-bin display uses different bin definitions.
3. **Clarify the abstract's baseline range** with a brief parenthetical note (e.g., "PB-valid, methods on the same train-test split").
4. **Add Vina (or the relevant classical methods) to the main comparison table** with matched metrics, so the "surpassing classical docking" claim can be verified at a glance.
5. **Report bootstrapped confidence intervals** for the main Top-1 results.
6. **Ablate FR3D stochasticity** to quantify sensitivity to the fragmentation outcome.

## Score and Decision

The core contribution — fragment-based SE(3)^m diffusion with soft triangulation constraints — is genuinely novel, theoretically well-motivated, and supported by strong empirical results (79.9% PB-valid). The method is a clear advance over prior torsional models, and the experimental protocol is more careful than is typical for this field. The major weaknesses (the per-seq-sim inconsistency and the AF3 per-bin comparison) are real reporting gaps that must be addressed, but they do not invalidate the central contribution: the 79.9% figure is consistently reported across multiple instances in the paper, and the methodological novelty stands apart from these presentation issues. I recommend acceptance conditional on the authors resolving the identified gaps.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>