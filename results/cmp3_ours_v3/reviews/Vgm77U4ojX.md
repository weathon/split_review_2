Here is the final consolidated review.

---

## Summary
SIGMADOCK proposes a fragment-based SE(3)^m Riemannian diffusion model for molecular docking. Unlike prior torsional diffusion approaches that operate over dihedral angles, the method decomposes ligands into rigid-body fragments, diffuses over their independent SE(3) poses, and learns to reassemble them within the binding pocket. The paper introduces a fragmentation reduction scheme (FR3D), soft triangulation constraints to preserve bond geometry, and an SE(3)-equivariant architecture. Empirically, SIGMADOCK achieves 79.9% Top-1 PB-valid on PoseBusters, significantly outperforming prior deep learning methods, with evidence of generalization to unseen proteins.

## Strengths

- **Genuinely novel methodological contribution.** The fragment-based SE(3)^m diffusion paradigm is a principled departure from torsional diffusion. The theoretical argument (Theorem 1) that torsional models produce non-product induced measures in Cartesian space — leading to ill-conditioned learning — is concrete and falsifiable, not just hand-wavy motivation. This provides a clear explanation for why prior torsional models underperform despite their theoretical appeal.

- **Thorough and honest ablation study (Table 1).** The paper includes Configuration G (sampling from the bound manifold M_b, 86.4% RMSD<2) as an explicit upper-bound ablation, telling the reader exactly how much performance comes from the method's components vs. the fragment representation itself. Ablations A-D cleanly isolate the contributions of triangulation conditioning, protein-ligand interaction modeling, fragment merging, and the ranking heuristic.

- **Co-factor analysis (Table 2) provides genuine evidence against memorisation.** The finding that failure rates are highest when natural ligands or other co-factors are present (41.2% failure for natural ligands vs. 16.2% for complexes with no co-factors) is a specific, non-trivial pattern supporting the claim that the model learns physics rather than memorising training data.

- **Sequence-similarity breakdown (Figure 4 right) shows consistent generalisation.** Performance across all similarity splits (51-53% Top-1) is unusual for deep learning docking methods and provides meaningful evidence of generalisation to unseen proteins.

- **The FR3D reduction scheme** reduces fragments from k+1 to approximately 2/3(k+1), addressing the key concern that fragmentation introduces more degrees of freedom than torsional models.

## Weaknesses

### Fatal
None.

### Major

- **The main comparison table (Figure 4) conflates different metrics, creating a misleading impression in the abstract and preventing apples-to-apples verification of the headline claims.** The abstract states: "reaching Top-1 success rates (RMSD < 2 Å PB-valid) above 79.9% … compared to 12.7-32.8% reported by recent deep learning approaches." However, Figure 4's table shows DiffDock at 38.0%, G2G at 58.1%, and Vibe2 at 58.1% — numbers that are almost certainly RMSD-only (not PB-valid). The paper itself acknowledges (line 192) that DiffDock's PB-valid rate is ~12.7% (79.9/6.3). The table's column header "Top-1 (%)" does not specify whether the numbers are RMSD-only or PB-valid, and the metric labeling is inconsistent between the abstract (which uses PB-valid) and the table (which mixes metrics across methods). A reader looking at Figure 4 would reasonably conclude that G2G (58.1%) is much closer to SIGMADOCK than the 12.7-32.8% range in the abstract suggests. The paper should present all methods on the same metric in a single table, or clearly label which metric each column uses.

### Minor

- **The ranking heuristic drives ~13 percentage points of performance but is critically underspecified in the main text.** The ablation (Table 1, Config D) shows that removing "energy scoring" from the ranking heuristic drops Top-1 (RMSD<2) from 80.5% to 67.2% — the single largest ablation effect. Yet the main text devotes only one sentence to describing this heuristic (line 176): "evaluating both the (pseudo) binding energy of the generated protein-ligand system, as well as a set of physicochemical checks (such as, bond angles, bond lengths, internal energy)." What is the "pseudo binding energy"? Is it a classical scoring function (Vina, etc.), a learned network, or a simple physics-based potential? This matters because 40 seeds are generated and the heuristic selects among them — comparison with methods using different selection strategies (e.g., DiffDock's confidence model) is incomplete without understanding what the heuristic is. The paper references Appendix F, but the main text should provide at minimum a brief description of how the pseudo binding energy is computed.

- **The AF3 comparison overstates the case.** The paper claims "AF3-level performance," but Table 4 shows AF3 substantially outperforming SIGMADOCK on the low-sequence-similarity regime ([0,30): AF3 87% vs. SIGMADOCK 72% PB-valid). This is precisely the regime that matters most for drug discovery (unseen proteins). SIGMADOCK leads only in the [95,100] band (87% vs. 78%) where train-test leakage is highest. The framing should be adjusted to acknowledge that AF3 remains stronger on the most practically relevant subset.

- **The conformational manifold alignment claim lacks aggregate statistics in the main text.** The paper asserts that RDKit conformers can be aligned to bound poses with "negligible error" (RMSD ≪ 2Å), but provides only a single example (Figure 2b, 0.11 Å). What is the mean, median, and 90th percentile of alignment RMSD across the 19k training complexes? If even a small fraction have alignment RMSD > 1Å, the rigid-fragment assumption weakens for those cases. The paper references Appendix D.3, but summary statistics in the main text would substantially strengthen this crucial assumption.

- **The "PDBBind" row in the main comparison table is confusing.** While the figure caption annotates it with (*) for classical docking, a reader unfamiliar with the field conventions would see "PDBBind" (the dataset name) listed as a method achieving 15.9%. The presentation could be clearer by using a more descriptive method label.

### Trivial
None.

## Nice-to-Haves
- Report confidence intervals or perform significance tests. The PB set has 308 complexes; a Top-1 rate of 79.9% has a 95% CI of roughly ±4.5pp. Many ablation differences fall within this range.
- Report per-ligand-size (rotatable bond count) breakdown to test whether the fragment approach actually solves the "lever effect" problem that motivates it.
- Report median RMSD or fraction of seeds correct per complex, not just Top-1 across seeds.
- Clarify in Config D whether the energy-scoring ablation still uses a ranking heuristic (e.g., just the physicochemical checks) and with how many seeds.

## Removed Points
These points are flagged to be removed; treat them with caution:

- **Critical Issue #3 (classical docking comparison inconsistency):** The reviewer claims the PDBBind (15.9%) and Vina (57.2%) numbers are inconsistent. These are from different experimental setups — the 15.9% is a classical docking baseline under the standard protocol, while Vina at 57.2% is from a pocket-sensitivity experiment with a specific autobox setting. The paper's claim about surpassing classical methods is supported by the 15.9% comparison. **REMOVED as based on a misunderstanding.**

- **Critical Issue #4 (abstract's 12.7-32.8% vs table numbers):** This is the same underlying issue as the metric conflation in the main comparison table, and is merged into the Major weakness above.

- **Theorem 1 "no proof given in main text":** The paper states "For further details and a proof of Theorem 1, see Appendix C.2." Proofs in appendices are standard. **REMOVED (presentation choice, not a weakness).**

- **Section-by-section notes about missing appendix content (FR3D algorithm, architecture details, etc.):** The parser strips these sections from all papers; they exist in the original submission. **REMOVED per policy.**

- **Critique that the introduction overstates limitations of co-folding models:** This is a matter of opinion and does not affect the paper's core claims. **REMOVED.**

## Novel Insights
The harsh critic's most insightful observations are: (1) the metric mismatch between the abstract's "12.7-32.8%" and the table's "58.1%" for G2G/Vibe2 is not merely a presentation infelicity — it actively prevents a reader from verifying the paper's central comparative claim from the primary exhibit; and (2) the ranking heuristic, which the reviewer correctly identifies as the largest single ablation effect, is described in insufficient detail given its importance. Both issues are independently verifiable from the main text alone. The paper's own strength — the co-factor analysis as evidence against memorisation — was correctly highlighted as a particularly strong piece of evaluation design.

## Suggestions
1. Reorganize the main results table (Figure 4) to report all methods on the same metric. Ideally, report PB-valid for all methods. If baseline PB-valid numbers are unavailable, clearly label the table columns as "RMSD-only" vs. "PB-Val" and add a second row for each baseline.
2. Add at least a one-sentence specification of the pseudo binding energy computation in the main text (e.g., "We use the Vina scoring function to compute binding energy" or "We train a lightweight MLP…").
3. Adjust the AF3 comparison framing to acknowledge AF3's stronger performance on low-similarity proteins, which is the most practically relevant regime.
4. Add summary statistics (mean, median, 90th percentile) for the RMSD alignment between RDKit conformers and bound poses across the training set.

## Score and Decision

**Calibration anchors used (all rounds):**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Uj0h13lVrR | 1.00 | R1 | Weak paper; not comparable |
| 5lUdTogEL3 | 1.00 | R1 | Weak paper; not comparable |
| m9zWBn1Y2j | 3.00 | R1 | Low-quality docking paper; SIGMADOCK stronger |
| G536mmC2HL | 3.00 | R1 | Torsion modeling paper; SIGMADOCK stronger |
| 1IaoWBqB6K (DiffDock-Pocket) | 5.00 | R1 | Incremental extension of DiffDock; SIGMADOCK more novel |
| FuXtwQs7pj | 4.50 | R1 | Diffusion on toric varieties; weaker evaluation |
| 5YLsnsjgeC (VFDiff) | 6.00 | R1/R2 | SE(3) diffusion for molecules; similar tier, SIGMADOCK stronger novelty |
| qH9nrMNTIW (IPDiff) | 6.25 | R2/R3 | Interaction priors in diffusion; SIGMADOCK more novel |
| uNomADvF3s (Lift Your Molecules) | 6.50 | R2/R3 | Latent Euclidean space framework; similar quality, cleaner evaluation |
| RyWypcIMiE (SBDD metrics) | 6.50 | R3 | Evaluation meta-paper; different contribution type |
| kzGuiRXZrQ | 5.75 | R2 | Design space exploration; less novel |
| UfBIxpTK10 (Deep Confident Steps) | 6.00 | R2 | Scaling analysis; less methodological novelty |
| kJFIH23hXb (SE(3) flow matching) | 8.00 | R1 | Exceptional clarity and contribution; stronger than SIGMADOCK |

**Bracket:** Round 1 bracket 6.0–7.0; narrowed to **6.5** after comparing the above anchors.

**Rationale:** SIGMADOCK has stronger core methodological novelty than any anchor in the 5.0–6.5 range — the fragment-based approach is a genuine paradigm shift from torsional diffusion. The experiments are thorough and include unusually informative analyses (co-factor breakdown, Config G upper bound ablation). However, the evaluation presentation has material problems: the main comparison table conflates RMSD-only and PB-valid metrics without labeling, making the abstract's comparative claims unverifiable from the primary exhibit, and the largest single ablation component (the ranking heuristic) is underspecified. These are fixable presentation issues, not fatal methodological flaws, and the underlying contributions are solid.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>