Now I have sufficient anchoring. Let me compile my final review.

**Round 1 bracket:** Based on the calibration anchors, the paper sits between 5.5 and 7.0. The most comparable papers in this band are DiffDock-Pocket (5.0), Frag2Seq (5.75, Accept), VFDiff (6.0, Reject), DockGen (6.0, Accept), DynamicFlow (6.2, Accept), and IPDiff (6.25, Accept).

**Narrowing:** SIGMADOCK's strengths (+10.00 theoretical diagnosis, +9.99 strong results) are comparable to the strongest items of accepted papers like IPDiff (+10.00 SOTA) and Frag2Seq (+10.00 proofs). Its weaknesses (-10.00 to -8.97) are presentation/precision issues rather than fundamental methodological errors — similar in nature to the missing-baselines/notation issues that DynamicFlow and DockGen overcame at 6.0+. The paper's theoretical contribution (identifying why torsional models underperform and proposing fragment SE(3)^m diffusion) is more novel than the incremental concerns flagged for Frag2Seq (-9.98 lack of innovation) or VFDiff (-10.00 copying). However, the metric inconsistency and underspecified central claims prevent a score above 6.5. I place the paper at **6.0** — a borderline accept where the core contribution is strong but the presentation needs to be cleaned up.

**Anchor comparison table:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Illumination Harmonization | u1cQYxRI1H | 0.5 (irrelevant) | 1 | No | Topically irrelevant to docking |
| KL Div GFlowNets | Uj0h13lVrR | 1.0 | 1 | No | Weak reject, nothing in common |
| Ligand Conformation (singleton→pairwise) | m9zWBn1Y2j | 3.0 | 2 | No | Less comprehensive results than SIGMADOCK |
| TorSeq | G536mmC2HL | 3.0 | 2 | No | Torsion modeling, SIGMADOCK's weaknesses are less severe |
| Fragment-Augmented Diffusion | r0QqfaCkF8 | 4.33 | 3 | No | Similar fragment+diffusion but for conformer generation, not docking |
| DiffMaSIF | S4zpk61r6G | 4.67 | 3 | No | Protein docking diffusion, less strong results |
| **DiffDock-Pocket** | 1IaoWBqB6K | **5.0** | **3** | **Yes** | Directly comparable docking paper. SIGMADOCK has stronger novelty (fragment representation vs incremental DiffDock extension) and better PB-valid results |
| Frag2Seq | mMhZS7qt0U | 5.75 | 2 | Yes | Fragment-based approach; SIGMADOCK's theoretical diagnosis is stronger |
| Navigating Design Space | kzGuiRXZrQ | 5.75 | 2 | No | De novo generation, not docking |
| **VFDiff** | 5YLsnsjgeC | **6.0** | **2** | **Yes** | SE(3)-equivariant diffusion. SIGMADOCK has stronger theoretical motivation and cleaner evaluation |
| **DockGen** | UfBIxpTK10 | **6.0** | **2** | **Yes** | Docking generalization paper. SIGMADOCK's weaknesses are comparable magnitude to DockGen's -9.9 items |
| **DynamicFlow** | 9qS3HzSDNv | **6.2** | **2** | **Yes** | Protein dynamics + SBDD. SIGMADOCK has comparable strength profile; DynamicFlow had -10.00 reproducibility issue |
| **IPDiff** | qH9nrMNTIW | **6.25** | **2** | **Yes** | Interaction prior diffusion. SIGMADOCK's theoretical contribution is more novel |

---

## Summary

This paper introduces SIGMADOCK, an SE(3)^m Riemannian diffusion model for molecular docking that replaces the standard torsional representation with a fragment-based representation. The key insight is that torsional models induce a nonlinear, non-product measure that makes score learning poorly conditioned, whereas factorizing over SE(3)^m rigid fragments yields a product of Haar measures and a simpler learning problem. The paper contributes a fragmentation reduction algorithm (FR3D), soft triangulation constraints, and an EquiformerV2-based architecture. On the PoseBusters benchmark, SIGMADOCK achieves 79.9% Top-1 PB-valid, substantially above prior deep learning methods.

## Strengths

- **Well-motivated method with clear theoretical diagnosis (Sections 2.2.1–2.2.2).** The paper identifies a genuine limitation of torsional models — the nonlinear mapping from torsion angles to Cartesian coordinates produces an entangled, non-product induced measure (Theorem 1) — and proposes a principled fix by factorizing over SE(3)^m fragments. This is not an architecture tweak but a rethinking of the representation space itself. **[impact=+10.00]**

- **Strong quantitative results on a challenging benchmark.** The 79.9% Top-1 PB-valid rate on PoseBusters substantially exceeds prior deep learning methods. The ablation study (Table 1) confirms that triangulation conditioning, fragment merging, and the protein-ligand interaction graph each contribute meaningful improvements (4–12% relative). The failure-case analysis by co-factor type (Table 2) provides diagnostic value that most docking papers skip. **[impact=+9.99] combined**

- **Honest failure-case analysis (Table 2).** Breaking down performance by co-factor type (natural ligands, ions, etc.) helps the community understand where the method works (84.2% RMSD < 2Å on complexes with no co-factors) and where it does not (58.8% when natural ligands are present). **[impact=+5.05]**

- **Clean and transparent scope framing (Section 1).** The paper explicitly adopts the re-docking protocol, justifies it as standard practice and industrially relevant, and clearly leaves flexible-receptor docking and co-folding as future work. This avoids overclaiming. **[impact=+4.94]**

## Weaknesses

### Major

- **Metric inconsistency between abstract and main comparison table.** The abstract reports "Top-1 success rates (RMSD < 2 Å PB-valid) above 79.9% … compared to 12.7–32.8% reported by recent deep learning approaches." The main table (Figure 4) shows baselines at much higher rates (DiffDock 38.0%, G2G 58.1%, Vibe2 58.1%) under column "PB (%)". The paper states "6.3× higher PB-validity than DiffDock" (implying DiffDock's PB-valid rate ~12.7%), confirming the table's baseline numbers are RMSD-only, not PB-valid. This means the table compares SIGMADOCK's PB-valid rate against baselines' RMSD-only rates — a mixed-metric comparison — while the abstract uses a consistent PB-valid comparison but does not explain the source of the 12.7–32.8% range or how it relates to the table. This conflation prevents the reader from directly verifying the headline claim from the presented data. **[impact=-9.94]**

- **"Surpass classical physics-based docking" claim is underspecified.** The main comparison table (Figure 4) shows only PDBBind (15.9%) as a classical method — and PDBBind is a scoring function, not a docking tool. Vina, a standard classical docking tool achieving 57.2% Top-1 (from Table 3), appears only in the pocket-sensitivity analysis. The paper should explicitly state which classical methods it surpasses and include them in the primary comparison table to substantiate this central claim. **[impact=-9.91]**

- **The ranking heuristic contributes a large fraction of performance but is not characterized against alternatives.** Ablations D and E (Table 1) show that removing energy scoring drops Top-1 from 80.5% to 67.2% (13.3 pts) and removing PB scoring drops PB-valid from 79.9% to 70.8% (9.1 pts). These are enormous drops. The paper does not compare this heuristic against standard alternatives such as using the model's own log-probability as a ranker or a learned confidence model. Without this, it is unclear whether the reported gains come from better generation or better filtering. **[impact=-8.97]**

- **AF3 comparison conflates fundamentally different tasks.** The paper acknowledges "we cannot directly compare SIGMADOCK to co-folding methods" but then presents a comparison (Table 4) and claims "AF3-level performance." SIGMADOCK operates on re-docking (fixed receptor, known pocket), while AF3 predicts structure jointly from sequence — different problems with different difficulty profiles. Moreover, the per-sequence-similarity bin counts differ substantially between methods (e.g., 109 vs 38 in [0,30), 123 vs 187 in [95,100]) despite both totaling 308 complexes, suggesting different subset definitions that further undermine the comparison. **[impact=-10.00]**

### Minor

- **Two "Ours" rows in Figure 4 are unexplained.** The table shows two rows for SIGMADOCK (79.9% and 80.6% PB) with no explanation of whether these reflect different metrics, seeds, or configurations. **[impact=-0.00]**

- **No training computational cost reported.** The paper highlights 50× faster sampling than AF3 but does not report training GPU-hours, epochs, or wall time. **[impact=-0.00]**

- **Distribution of fragment counts (m) across the dataset is not analyzed.** The paper claims m ≈ (2/3)(k+1) empirically but does not show the distribution or how performance correlates with m. **[impact=-0.00]**

### Trivial

None.

## Nice-to-Haves

- A controlled ablation keeping architecture fixed while varying the representation (fragments vs. torsions) would directly test the central hypothesis that fragment-space diffusion yields a better-conditioned learning problem, rather than relying on cross-architecture comparisons.
- Compare the ranking heuristic to the model's own unconditional score (log-likelihood) as a ranker, to determine whether the heuristic genuinely improves upon the model's internal probability estimates.
- Provide a summary statistic (mean/median alignment RMSD, fraction below thresholds) for the conformer-to-bound alignment claim in the main text.

## Removed Points

These points were considered but removed with justification:

- **"No statistical significance or confidence intervals":** Removed — single-run evaluation is standard practice in the docking literature. This is not considered a methodological gap in this field.
- **"Empirical claim about aligned conformer RMSDs deferred to appendix":** Removed — the main text (lines 86–87) states the RMSDs are "substantially below 2Å" and references Appendix D.3. A summary statistic would strengthen the paper but the claim is present.
- **"Theorem 1 proof in appendix":** Removed — standard practice; the intuitive argument is in the main text.
- **"DoF analysis could be clearer about lower bound":** Removed — the paper explicitly states "k+6 ≤ DoF ≤ 6m" and discusses the bound. The critic's concern is about emphasis, not correctness.
- **"Missing related work":** Removed per instructions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the metric discrepancy.** In Figure 4, label the column for baselines as "PB RMSD-only (%)" and SIGMADOCK's as "PB-valid (%)", or else report PB-valid numbers for all baselines in the table. In the abstract, cite the source of the 12.7–32.8% range and make explicit that this is the PB-valid range for baselines.
2. **Substantiate the classical docking claim.** Add Vina (or other classical docking tools) to the main comparison table, or rephrase the claim to precisely match what is shown.
3. **Characterize the ranking heuristic.** Compare it against the model's own log-likelihood as a ranker. If the heuristic outperforms the model's own score, that is itself interesting and warrants analysis.
4. **Reframe the AF3 comparison.** Present it as a contextual observation ("our PB-valid rate on the re-docking task happens to match AF3's rate on the co-folding task") rather than a competitive benchmark. Explain the differing bin counts.
5. **Explain the two Ours rows** in Figure 4.
6. **Report training computational cost** (GPU-hours, epochs).

## Score and Decision

Based on calibration against 12 anchor papers in the molecular docking/diffusion domain (scores ranging from 0.5 to 8.0), with closest matches being DiffDock-Pocket (5.0), Frag2Seq (5.75), VFDiff (6.0), DockGen (6.0), DynamicFlow (6.2), and IPDiff (6.25):

The paper's strengths — a genuinely novel theoretical diagnosis of torsional model limitations, strong PB-valid results (+10.00 and +9.99 impact) — are comparable to the top strengths of accepted papers in the 5.75–6.25 range. Its weaknesses (-8.97 to -10.00) are similar in impact magnitude to those of Frag2Seq and DynamicFlow, but the nature of the weaknesses differs: SIGMADOCK's issues are about presentation precision and claim substantiation (fixable in revision), not about incremental novelty (Frag2Seq's main weakness at -9.98) or reproducibility (DynamicFlow at -10.00). The paper is more novel than DiffDock-Pocket (5.0), which was judged incremental. It has stronger theoretical grounding than VFDiff (6.0), which suffered from concerns about copying IPDiff. The metric inconsistency and underspecified central claims prevent a score above 6.5, but the core contribution solves a real problem with a principled approach and achieves compelling results.

Final score: **6.0** (borderline accept) — the paper should be accepted conditional on addressing the metric clarity, claim precision, and ranking heuristic characterization.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>