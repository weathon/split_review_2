Now I have thorough calibration data. Let me write the final consolidated review.

## Summary

This paper introduces ProteinVista, a 3D CNN that voxelizes full-atom protein structures at 1Å resolution across five atom-type channels, uses adaptive boxing to handle varying protein sizes, and is pre-trained on ~500K AlphaFold2 structures via contrastive alignment to ESM-2 embeddings (123M parameters). It is evaluated on three protein-ligand prediction benchmarks (transporter-substrate prediction TSP, enzyme-substrate prediction ESP, and drug-target IC50 regression) plus GO annotation. The core claims are: (1) dramatic compute savings vs. sequence transformers, (2) competitive or superior accuracy, and (3) sequence-structure complementarity when ensembled with ESM-2.

## Strengths

- **Genuinely compute-efficient design.** Pre-training on 4 A100 GPUs for 48 hours vs. 128 H100 GPUs for ~7 days for ESM-2-650M is more than a 100× reduction in GPU-hours. The adaptive boxing (choosing among four grid sizes to minimize empty voxels) is a practical engineering choice that makes the approach feasible for real use. This is the paper's clearest and most concrete contribution (Section 4.3, Figure 3). [impact=+9.96]

- **Ablation study with informative findings.** Showing that disabling multi-view ensembling at inference drops R² by 6.4% while disabling augmentation during fine-tuning costs only 0.1% is a concrete, non-obvious result that reveals where the model actually learns its orientation robustness (Section 4.2, Figure 2e). [impact=+9.99]

- **Sequence-structure complementarity convincingly demonstrated.** Across multiple analyses (Table 1 ensemble rows, Figure 2a–c stratified by sequence/structural similarity), the ensemble of ProteinVista and ESM-2 consistently outperforms either alone. This is a meaningful empirical finding regardless of whether one accepts the paper's stronger claims. [impact=+9.96]

- **Honest negative result on GO annotation.** The paper reports that ProteinVista's Fmax on molecular-function GO term prediction (0.57) is substantially below ESM-2's (0.62), and explicitly states "structure encoders add limited value" when function depends on conserved motifs or overall homology (Section 3.4). This willingness to delineate where the method does *not* work strengthens credibility. [impact=+8.04]

## Weaknesses

### Fatal
None.

### Major

- **No variance or confidence intervals reported for the core comparisons.** Every number in Tables 1 and 2 is a point estimate from a single run with no standard deviations, multiple seeds, or confidence intervals. On ESP, ProteinVista is actually behind ESM-2-650M on 3 of 4 metrics (Accuracy 91.8% vs 91.9%, ROC-AUC 0.951 vs 0.955, MCC 0.78 vs 0.79). On TSP the accuracy gap is 1.5 percentage points (90.8% vs 89.3%). Without variance estimates, these small differences could be within single-run noise. The McNemar test reported in the paper tests whether the ensemble and ESM-2 produce *different predictions* on individual samples — it does not test whether the accuracy gap itself is reproducible across training runs. The IC50 result (0.69 vs 0.61, p < 10⁻³⁰⁴) is more robust due to the larger gap, but the paper's central comparative claims hinge on all three benchmarks, and two of them lack adequate statistical support. [impact=-10.00]

- **Title and abstract overclaim relative to the paper's own data.** The title states ProteinVista "OUTPERFORMS SEQUENCE TRANSFORMERS IN PROTEIN-LIGAND PREDICTION" and the abstract claims superiority on "three benchmarks." However, on the Enzyme-Substrate Prediction (ESP) task — which is a protein-ligand prediction benchmark — ProteinVista underperforms ESM-2-650M on three of four reported metrics (Accuracy, ROC-AUC, MCC) and only surpasses it on Precision (0.89 vs 0.86). The body text hedges with "surpasses or equals" (Section 3.2) and the conclusion says "outperforms or matches" (Section 5), but the title and abstract do not. This mismatch between the strong headline and the mixed results is a significant presentation issue. [impact=-9.98]

- **Rotation augmentation covers only the octahedral (cubic) symmetry group, not full SO(3).** The augmentations are restricted to 90° rotations and mirror reflections (Section 2.4), yielding 24 discrete orientations. The model's "rotation-robust" claims (abstract: "learns rotation-robust representations") have only been tested on augmentations drawn from this same discrete set. Real protein structures from PDB or AlphaFold DB can appear at arbitrary orientations. Whether the model generalizes to continuous rotations (e.g., a 45° rotation) is untested and unknown. This matters because one claimed advantage over graph-based methods is not requiring orientation canonicalization. [impact=-3.27]

### Minor

- **The SOTA comparison in Section 3.3 bundles multiple modeling improvements without isolating ProteinVista's contribution.** The optimized pipeline (OP) involves: fine-tuning with updated MolFormer weights, extracting and freezing embeddings, training a separate contrastive network on those embeddings, and ensembling with both ProteinVista and ESM-2. The final ESM-ProteinVista_OP is an ensemble of two protein encoders plus a separately trained classifier. Comparing this to individual models (SPOT, ProSmith-ESP) does not reveal how much of the gain comes from ProteinVista vs. the pipeline improvements. The paper should report what the OP gives for ProteinVista alone and for ESM-2 alone before ensembling. [impact=-7.08]

- **Contrastive pre-training to ESM-2 partially confounds the complementarity finding.** ProteinVista is pre-trained with a contrastive loss that explicitly aligns its embeddings to ESM-2's embedding space (Section 2.3). The model is trained to produce representations close to ESM-2's for the same protein, so the ensemble complementarity may partly reflect the design choice rather than truly orthogonal structure information. The ablation showing Rosetta regression yields similar results (+1.0% difference) partly mitigates this, but the paper does not discuss the interpretive cost. [impact=-5.19]

- **No direct statistical test comparing ProteinVista alone vs. ESM-2 alone on the binary tasks (TSP, ESP).** The McNemar test compares the ESM-ProteinVista *ensemble* vs. ESM-2, not ProteinVista alone vs. ESM-2. Given the small and mixed metric differences on ESP, this omission is notable. [impact=-1.07]

### Trivial

- **Inconsistent Rosetta score count:** Section 2.3 and the ablation (Section 4.2) state "23 Rosetta scores" while the Discussion (Section 5) states "33 Rosetta scores." This should be resolved.

## Nice-to-Haves

- The 5-atom-type encoding (C, N, O, S, P) loses chemically important distinctions (e.g., carbonyl vs. hydroxyl oxygen) that could matter for binding tasks. Using more fine-grained atom typing or adding chemical features could be beneficial.
- The timing analysis attributes the 20× speedup over ESM-2-650M to parallelization efficiency despite similar FLOPs, but provides no detailed breakdown (convolution vs. attention, GPU utilization metrics). A brief analysis would strengthen the compute claims.
- Reporting dataset statistics (split sizes, homology reduction status) in the main text rather than deferred to Table S3 would help readers interpret results.

## Removed Points

These points from the input review were filtered out per the consolidation guidelines:

1. **Missing related works (equivariant networks like SE(3)-transformers, NequIP, MACE)** — Removed as "DO NOT mention missing related works" per instructions.
2. **Parser-garbled density formulation in Section 2.1** — Removed as a known parser artifact, not an author error.
3. **"5 heavy atom types loses distinctions"** — Moved to Nice-to-Haves as a design scope choice, not a weakness.
4. **Lack of GPU utilization analysis for speedup** — Removed as a nitpick; the paper provides a reasonable explanation.
5. **Dataset statistics in appendix** — Moved to Nice-to-Haves as a presentation preference.
6. **Abundance of single-view test vs. 5-view** — Already covered in Strengths (the paper reports this clearly).
7. **Speculation about timing being "forward-pass" not "training"** — The paper explicitly says "during training" (Section 4.3). The reviewer's speculation is not grounded.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report results from 3–5 random seeds with standard deviations for the main comparisons (Tables 1, 2). This is essential for the TSP and ESP results where metric differences are small.
2. Recalibrate the title and abstract to emphasize compute efficiency and complementarity as the headline contributions, rather than a blanket "outperforms" claim that is contradicted by the ESP results.
3. Test rotation robustness on continuously rotated structures (not just 90° increments) to validate the "rotation-robust" claim.
4. In Section 3.3, report what the optimized pipeline achieves for ProteinVista alone and for ESM-2 alone before combining them, to enable proper attribution.
5. Resolve the 23 vs. 33 Rosetta scores inconsistency.

## Score and Decision

### Calibration Analysis

All anchors retrieved across rounds:

| Anchor | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| ProteinAdapter (jqx5XI4Yr3) | 3.40 | R1 | Yes | Adapter-based protein representation, rejected for limited novelty and marginal improvements. ProteinVista has stronger novelty (full 3D CNN) but worse evaluation rigor (no variance). |
| ProteiNexus (iBAWiEjogY) | 3.67 | R1 | Yes | Structural pre-training, rejected for unclear experiments and data leakage. ProteinVista has better experimental design but similar issues with claim-evidence alignment. |
| MiniFold (SjgfWbamtN) | 4.25 | R1,R2 | Yes | Compute-efficient structure prediction (100× speedup), rejected. Shares similar strength-profile (clear efficiency contribution, some evaluation gaps). ProteinVista's evaluation gaps are more severe (no variance at all). |
| RapidDock (0sU4myabw1) | 4.25 | R1,R2 | Yes | Compute-efficient molecular docking (100× speedup), rejected. Similar contribution style, but ProteinVista has the additional issue of title/abstract overclaiming. |
| E³former (QKywN4BbqA) | 5.25 | R1 | Yes | Equivariant protein representation, rejected despite strong results. Significantly stronger empirical validation than ProteinVista. |
| Pre-training Seq/Struct/Surface (BEH4mGo7zP) | 5.75 | R1 | Yes | Multimodal protein pretraining, accepted. Stronger experimental rigor despite marginal gains. |
| ProteinWorkshop (sTYuRVrdK3) | 6.25 | R1 | No | Benchmark suite, accepted. Different contribution type. |
| AtomSurf (ARQIJXFcTH) | 6.75 | R1 | No | Surface representation benchmark, accepted. Different contribution type. |

**Round 1 bracket**: 3.5–5.5, anchored by ProteiNexus (3.67) below and E³former (5.25) above.

**Narrowing**: Within this bracket, ProteinVista sits below MiniFold (4.25) and RapidDock (4.25) because its evaluation gaps are more fundamental: those papers had specific missing baselines or scope limitations, whereas ProteinVista has no variance reporting at all for its main comparative claims. The title/abstract overclaim on ESP (where the model is actually behind ESM-2 on most metrics) is also a uniquely clear presentation error. The strongest itemized comparison is with MiniFold (4.25): MiniFold's top impact weaknesses were about missing code (-9.96), incorrect kernel analysis (-9.99), and missing baselines (-9.59). ProteinVista's top weaknesses (-10.00 for no variance, -9.98 for overclaiming) are similarly decisive. Given that ProteinVista's evaluation gap is more central to its core claims than MiniFold's issues, a slightly lower score is warranted.

**Final score**: 4.0.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>