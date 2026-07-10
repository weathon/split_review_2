Now let me write the final review.

## Summary

ProteinVista introduces a 3D CNN that operates on voxelized full-atom protein structures, pre-trained on ~500K AlphaFold2 structures. The model is compared to ESM-2 on three binding prediction benchmarks (transporter-substrate, enzyme-substrate, IC50 regression) and one GO annotation task. The key results are: (1) ProteinVista matches or exceeds ESM-2 on two of the three binding tasks while using 5× fewer parameters and dramatically less pre-training compute; (2) an ensemble with ESM-2 yields further improvements, demonstrating complementarity; (3) compute efficiency is well-documented with concrete FLOPs and wall-clock measurements. The paper honestly reports that ProteinVista underperforms ESM-2 on a homology-driven GO annotation task.

## Strengths

- **Clearly motivated architectural choice.** The introduction makes a tight argument: existing residue-graph methods (GearNet, ESM-GearNet) abstract away side-chain geometry, positioning ProteinVista specifically against that limitation rather than making a generic "structure is better" claim (Section 1).

- **Honest failure case reporting.** Section 3.4 shows ProteinVista underperforms ESM-2 on GO annotation (F_max 0.57 vs. 0.62), a homology-driven task. This negative result helps delimit where the method does and does not work.

- **Stratified analysis by structure quality.** Section 4.1 breaks down performance by pLDDT confidence bins (Fig 2c-d), showing that ProteinVista's advantage concentrates in the high-confidence regime (pLDDT > 90) where most test proteins lie. This gives a practical guide for when to apply the method.

- **Compute efficiency is well-demonstrated.** Section 4.3 provides concrete FLOPs, wall-clock time, and GPU-hour comparisons. Pre-training cost (48 hrs on 4 A100s vs. ~7 days on 128 H100s for ESM-2_650M) and the observation that the 5-block CNN parallelizes better than deep transformer layers (20s vs. 426s per 1000 proteins on the same GPU) are genuine practical advantages.

## Weaknesses

### Fatal
None.

### Major

- **Missing comparison to the residue-graph encoders the paper critiques.** The introduction (Section 1) explicitly targets GearNet and ESM-GearNet as inadequate — operating at residue level and missing atom-level detail — and positions ProteinVista as the improvement. However, the experimental evaluation (Section 3) never compares against these methods. The SOTA comparisons (SPOT, ProSmith-ESP, Fusion_ESP) are task-specific methods, not general structure-aware encoders. Without a head-to-head comparison on the same benchmarks and prediction pipeline, the claim that atom-level 3D CNNs are superior to residue-graph methods is asserted but not demonstrated.

- **The optimized pipeline (OP) SOTA comparison is confounded by pipeline complexity.** ESM-ProteinVista_OP adds joint MolFormer weight updates, a separately trained contrastive network, and prediction averaging — substantially more complexity than the published baselines (SPOT, ProSmith-ESP, Fusion_ESP) use. An ablation applying the same OP pipeline to ESM-2_650M alone (without ProteinVista) would be needed to attribute the gains specifically to ProteinVista's encoder rather than the more elaborate pipeline.

### Minor

- **Rotation robustness claims are only tested at discrete 90° orientations.** The augmentation strategy (Section 2.4) is limited to 90° rotations and mirror reflections along Cartesian axes. The paper claims "rotation-robust representations" (abstract) and that the model is "less affected by arbitrary rotations" (Section 2.4), but never tests invariance to arbitrary continuous rotations (e.g., rotating test proteins by a non-90° angle). The ablation confirms that multiple discrete views help (single view → -6.4% R²), but this does not substantiate robustness to arbitrary orientations.

- **Pre-training objective is conceptually in tension with the paper's central claim.** The contrastive pre-training (Section 2.3) aligns ProteinVista's embeddings with ESM-2's sequence embeddings — potentially incentivizing the structure encoder to discard information not already captured by the sequence model. The Rosetta-score regression (a structure-only objective with no access to sequence embeddings) achieves nearly identical downstream performance (only 1.0% relative R² worse, Section 4.2), yet the paper presents contrastive pre-training as the default without discussing this tension.

- **The abstract's outperformance claim is overstated for the ESP benchmark.** The abstract states ProteinVista "outperforms sequence transformers on three benchmarks," but on the ESP task (Table 1), the single ProteinVista model matches ESM-2_650M on accuracy (91.8% vs 91.9%) and scores slightly lower on ROC-AUC (0.951 vs 0.955). The claim is supported on TSP and IC50, but should be qualified.

### Trivial

- **Rosetta score count inconsistency:** Section 2.3 says "23 *in silico* computed Rosetta scores," while the Discussion (Section 5) says "33 Rosetta scores."

- **No analysis of the 160Å cropping impact.** The paper notes that structures exceeding 160Å are cropped (Section 2.1) but does not report what fraction of test proteins this affects or whether performance degrades on cropped structures.

## Nice-to-Haves

- Providing Grad-CAM-style 3D visualizations showing that the model attends to binding pockets (mentioned as future work in Section 5) would strengthen the claim about encoding binding site geometry.
- Discussing mitigations for the large storage requirement of voxelized structures (compression, lower precision, on-the-fly voxelization from mmCIF) would improve practical utility.
- Testing explicitly with arbitrary continuous rotations (e.g., 37°) would cleanly address the rotation robustness question.

## Removed Points

- The garbled density formula in Section 2.1 is a parser artifact, not an author error, per the hard filter rules.
- The criticism about the storage barrier (13 MB per protein) and absence of mitigation discussion: the paper openly acknowledges this as a trade-off (Section 4.3); this is a known practical limitation rather than an omission.
- Generic "Strengthening the Paper on Its Own Terms" suggestions that duplicate points already captured in the weaknesses section above (e.g., controlled comparison to GearNet, reframing pre-training, testing rotation invariance) are subsumed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add a controlled comparison to GearNet or ESM-GearNet using the same prediction pipeline and benchmarks. This is the single most important missing experiment given the paper's positioning.
- Ablate the OP pipeline by applying the same procedure (joint MolFormer updates + contrastive network + averaging) to ESM-2_650M alone, to isolate ProteinVista's contribution.
- Test rotation robustness explicitly by evaluating on proteins rotated by non-90° angles (e.g., 37°) and reporting whether the multi-view ensemble maintains performance.
- Calibrate the abstract and title claims: specify that ProteinVista "outperforms sequence transformers on two of three benchmarks and matches on the third."
- Resolve the 23 vs. 33 Rosetta score inconsistency.

## Score and Decision

The paper makes a genuine contribution by demonstrating that a compute-efficient 3D CNN on voxelized full-atom structures can match or exceed ESM-2 on structure-dependent tasks, with impressively lower pre-training costs. The honest failure case reporting and stratified pLDDT analysis are marks in its favor. However, the two major weaknesses — the missing comparison to the residue-graph methods the paper explicitly critiques, and the uncontrolled OP pipeline comparison — mean the paper's strongest claims (superiority over structure-aware encoders, SOTA results) are not adequately supported. These are addressable but require meaningful additional experimental work.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Borderline Reject</decision>