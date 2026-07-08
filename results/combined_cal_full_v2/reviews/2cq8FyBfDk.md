Here is the final consolidated review.

---

## Summary

ProteinVista introduces a full-atom 3D CNN for protein representation learning that makes the architecture computationally tractable through adaptive boxing, continuous density voxelization, and large-scale pre-training on ~500K AlphaFold-2 structures. The model is evaluated on three protein-ligand prediction benchmarks (transporter-substrate classification, enzyme-substrate classification, and drug-target IC50 regression) where it matches or exceeds ESM-2 while using 5× fewer parameters, ~1% of the GPU-hours for pre-training, and two orders of magnitude less data. The paper also demonstrates complementarity with sequence models via an ensemble.

## Strengths

- **A genuine architectural contribution:** ProteinVista demonstrates that a full-atom 3D CNN for proteins — which the community has largely abandoned as computationally infeasible — can be made tractable through adaptive boxing (four grid sizes: 64³, 96³, 128³, 160³), continuous density voxelization, and large-scale pre-training. The fact that a 123M-parameter 3D CNN can be pre-trained on ~500K structures in 48 hours on four A100s meaningfully challenges the conventional wisdom that 3D CNNs are too expensive for proteins. **[weight=9.38]**

- **Compute efficiency is convincingly demonstrated with concrete numbers:** 20s vs 426s per 1k proteins on an A100 for training throughput, ~1% of the GPU-hours for pre-training, and 123M vs 650M parameters. The paper also transparently acknowledges the storage trade-off (75GB vs 3MB for the TSP dataset) rather than hiding it. **[weight=9.93]**

- **Honest negative result on GO term prediction:** Section 3.4 reports that ProteinVista reaches an Fmax of 0.57 vs ESM-2's 0.62, and the ensemble only marginally improves to 0.63. The paper explicitly states that "structure encoders add limited value" for homology-driven tasks, which provides calibrated expectations for when to use ProteinVista. **[weight=6.45]**

- **Informative ablation studies:** Section 4.2 isolates multiple factors — single vs multi-view inference (−6.4% R²), augmentation during fine-tuning (−0.1%, negligible), pre-training objective (−1.0% for Rosetta vs contrastive), and voxel resolution (−1.1% at 1.5Å). These allow the reader to understand which design choices matter and by how much. **[weight=9.60]**

- **Complementarity analysis by sequence and structural similarity bins:** Figure 2 (panels a-c) partitions the test set by sequence identity, TM-score, and pLDDT. This reveals that ProteinVista's advantage is concentrated in high-identity/high-confidence regimes, consistent with the claim that it genuinely captures structural detail that sequence models miss. **[weight=7.95]**

## Weaknesses

### Fatal
None.

### Major

- **The "outperforms" claim is overstated for the ESP benchmark.** The abstract states that ProteinVista "outperforms sequence transformers on three benchmarks: enzyme-substrate classification; transporter-substrate classification; and drug-target inhibition prediction." However, on the ESP benchmark (Table 1), ESM-2_650M scores higher on 3 of 4 metrics: Accuracy 91.9% vs 91.8%, ROC-AUC 0.955 vs 0.951, MCC 0.79 vs 0.78. ProteinVista only wins on Precision (0.89 vs 0.86). While the TSP and IC50 results genuinely favor ProteinVista, the ESP result is at best a tie. The paper body (line 115) uses the more accurate phrasing "surpasses or equals," but the abstract and title use "outperforms" without qualification. This discrepancy needs to be resolved by qualifying the claim (e.g., "outperforms or matches on three benchmarks") or explicitly stating which benchmarks show improvement. **[weight=3.50]**

- **The comparison against ESM-2 is not an independent test of structure vs. sequence.** ProteinVista's main results all use weights pre-trained with a contrastive objective (Section 2.3) that aligns its embeddings with ESM-2 via symmetric InfoNCE loss. The model's representations were explicitly trained to be close to ESM-2's embeddings for the same protein and far from those of different proteins. The paper frames the results as "structure beats sequence," but the structural encoder's best-performing version was trained using a sequence transformer's embeddings as targets. This concern is partially mitigated by the Rosetta-based pre-training ablation (only −1.0% R² on IC50), suggesting the structure encoder can work well without ESM-2 alignment. However, the Rosetta-pre-trained results are only shown for IC50, not for TSP or ESP. The paper should either (a) present Rosetta-pre-trained results on all three benchmarks to demonstrate ESM-independent performance, or (b) reframe the central claim around complementarity rather than independent superiority. **[weight=3.63]**

### Minor

- **Statistical significance for ProteinVista vs. ESM-2 alone is incomplete.** For IC50, a one-sided Wilcoxon test (p < 10⁻³⁰⁴) is reported for ProteinVista vs. ESM-2_650M, which is appropriate. However, for the TSP and ESP classification tasks, significance is only reported for the *ensemble* vs. ESM-2_650M (McNemar's test), not for ProteinVista alone vs. ESM-2_650M. Given that the absolute differences on TSP are small (90.8% vs 89.3% accuracy) and on ESP they favor ESM-2 on most metrics, significance tests for these direct comparisons would clarify whether the observed differences are meaningful or just noise. **[weight=5.68]**

- **Potential data leakage between pre-training and downstream sets is not discussed.** The pre-training set (~500K Swiss-Prot proteins) contains well-characterized proteins that may overlap with the downstream test sets (BindingDB, enzyme-substrate, transporter-substrate). The paper should state whether any measures were taken to avoid overlap or discuss the potential impact. **[weight=4.51]**

- **The optimized pipeline (OP) comparison confounds multiple changes.** The OP comparison against SPOT and ProSmith-ESP introduces several changes simultaneously (updating MolFormer embeddings, extracting fine-tuned embeddings, training a separate contrastive network, ensembling with ESM-2). While the pipeline is clearly described, it is difficult to attribute the improvement to any specific component, and the baselines do not benefit from the same multi-stage optimization. **[weight=2.51]**

### Trivial
None.

## Nice-to-Haves
1. Presenting Rosetta-pre-trained ProteinVista results on all three benchmarks (not just IC50) would cleanly separate the structural contribution from the ESM-2 alignment contribution.
2. A brief qualitative analysis (e.g., 3D Grad-CAM visualization of important voxels) would help demonstrate that the model's performance derives from structural reasoning rather than spurious correlations.
3. Adding McNemar's test results for ProteinVista alone vs. ESM-2_650M on TSP and ESP.

## Removed Points
These points are flagged to be removed, treat them with caution:
- *"Missing comparison to other 3D structure-based methods (DeepSite, EnzyNet, VoroCNN, etc.)"* — REMOVED. These methods address fundamentally different tasks (pocket detection, EC number prediction, structure quality assessment) from different eras. The paper's benchmarks use SPOT, ProSmith-ESP, and Fusion_ESP as relevant SOTA baselines, which are the correct comparisons for these specific tasks. Requiring experimental comparison against methods designed for different tasks is scope creep.
- *"Runtime numbers unclear whether forward pass or forward+backward"* — REMOVED. The paper clearly states "during training" in the main text (line 174), and this is standard reporting.
- *"Global average pooling over different voxel sizes"* — REMOVED. The paper explicitly states this yields a "fixed 1,024-dimensional representation for every protein, independent of the input box size" (line 67-68). The concern about different numbers of voxels is a theoretical curiosity, not an identified problem.
- *"Rotation augmentation limited to 90° rotations"* — Move from Weaknesses to Removed. The ablation shows the impact is negligible (−0.1% during fine-tuning). While a theoretical limitation, there is no evidence it harms empirical performance.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Qualify the "outperforms" claim in the abstract and title to accurately reflect the ESP results (e.g., "outperforms or matches on three benchmarks").
2. Present the Rosetta-pre-trained version's results on all three benchmarks alongside the contrastive-pre-trained results, to demonstrate that the structural encoder works independently of ESM-2 alignment.
3. Add McNemar's test results for ProteinVista alone vs. ESM-2_650M on TSP and ESP.
4. Add a data leakage analysis section discussing potential overlap between the Swiss-Prot pre-training set and the downstream test sets.

---

**Calibration Anchor Report:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| ProteinAdapter | jqx5XI4Yr3.md | 3.40 | R1 | Yes | Weaker contribution (gluing existing models); weaknesses had negative weights (−2.89, −3.72). This paper is clearly stronger. |
| ESMGain | vVlNBaiLdN.md | 3.00 | R2 | No | Similar topic (ESM-2 transfer learning); score 3. This paper is stronger. |
| PPBind | xNDydjYBmC.md | 4.60 | R1 | Yes | Similar weaknesses (data leakage, missing baselines) but also had missing figures. This paper has better evidence. |
| Deep Learning for Protein-Ligand Docking | ZuU4mZILBB.md | 4.38 | R3 | Yes | Benchmark paper with mixed scores (3-6). Different contribution type. |
| Protein-ligand binding rep learning | AXbN2qMNiW.md | 5.67 | R2 | Yes | Accepted with similar concerns (data leakage, missing baselines). Weighted items show strong positives. This paper has comparable quality. |
| ProteinWorkshop | sTYuRVrdK3.md | 6.25 | R1 | Yes | Benchmark suite with high-quality evaluation. Cleaner claims than this paper. |
| AtomSurf | ARQIJXFcTH.md | 6.75 | R2 | Yes | Accepted with strong positive weights (8.72-11.81). Cleaner presentation and no overclaim issues. |

**Bracket reasoning:** Round 1 placed the paper between ProteinAdapter (3.4, Reject) and AtomSurf (6.75, Accept). The draft's weakness weights are all positive (2.51 to 7.26), meaning they are moderately damaging but not critically so — unlike ProteinAdapter whose weaknesses carried negative weights. The closest anchor is the protein-ligand binding paper (5.67, Accept) which shares similar concerns (data leakage, missing comparisons) but was accepted. This paper has slightly more severe framing issues (the overstated "outperforms" claim and ESM confound), placing it just below that anchor. The final score of **5.0** reflects a paper with genuine contributions whose headline claims need reframing before acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>