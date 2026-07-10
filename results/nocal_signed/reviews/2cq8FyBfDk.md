Now I have the impact-weighted signals. Let me write the final consolidated review.

## Summary

This paper introduces ProteinVista, a 3D convolutional neural network that processes full-atom protein structures via voxelization at 1.0 Å resolution. It is pre-trained on ~500K AlphaFold2 structures using a contrastive objective aligned with ESM-2 embeddings, then fine-tuned on downstream tasks. The paper demonstrates that ProteinVista outperforms ESM-2 variants of comparable and larger size on three binding-prediction benchmarks (TSP, ESP, IC50), does so with dramatically lower pre-training cost (48 hours on 4 A100s vs. 7 days on 128 H100s), and includes an honest failure analysis on GO term prediction where the structure-based model falls short. The core claim — that a well-engineered full-atom 3D CNN is computationally tractable and effective for structure-dependent protein tasks — is convincing.

## Strengths

- **Well-motivated architecture with practical solutions to the sparsity problem.** Adaptive boxing (choosing among four grid sizes to enclose each protein) and continuous-density voxelization (instead of one-hot occupancy) directly address the conventional critique that 3D CNNs for proteins waste memory. The five-channel heavy-atom encoding preserves chemical identity without excessive channel depth. (Section 2.1)

- **Statistically rigorous within-protocol comparisons.** The controlled experiments where ProteinVista and ESM-2 variants share the same prediction head, the same MolFormer embeddings, and the same hyperparameter search are the fairest and most informative comparisons in the paper. McNemar tests (p < 10^{-13}, p < 10^{-17}) and Wilcoxon test (p < 10^{-304}) provide strong evidence that observed differences are not noise. (Section 3.2)

- **Honest failure analysis strengthens credibility.** The GO term prediction experiment (Section 3.4) shows ProteinVista underperforming ESM-2 (Fmax 0.57 vs 0.62), confirming the paper's own framing that structure-aware models add value primarily on geometry-dependent tasks. The stratification by sequence identity, TM-score, and pLDDT (Section 4.1) further delineates *when* the structural representation helps.

- **Compute efficiency claims are concrete and well-supported.** Pre-training on four A100 GPUs for 48 hours vs. 128 H100 GPUs for 7 days is a dramatic efficiency difference. The FLOPs and wall-time comparisons (Figure 3) are concrete and reproducible, demonstrating that the conventional wisdom about 3D CNNs being too expensive for proteins was grounded in outdated constraints. (Section 4.3)

## Weaknesses

### Fatal
None.

### Major

- **The SOTA comparison (Section 3.3) is uncontrolled and the margins are narrow.** The optimized pipeline (joint fine-tuning of MolFormer, contrastive post-processing, ensemble averaging) is compared against published SOTA numbers (SPOT, ProSmith-ESP, Fusion_ESP) that used different pipelines. On the ESP benchmark, the margin over prior methods is only 0.2 percentage points (94.4% vs 94.2%), which is within any reasonable variance bound and could reflect pipeline differences rather than encoder quality. The paper's strongest evidence is the controlled comparison against ESM-2 (Section 3.2); the SOTA claims in the abstract and Section 3.3 are overstated relative to the support.

- **Missing comparison against structure-aware GNN baselines.** The paper compares ProteinVista against sequence-only ESM-2 models, but not against structure-aware graph neural networks such as GearNet or ESM-GearNet — which the paper itself cites (Section 1, lines 17–23) and critiques for omitting atom-level details. Without this comparison, the reader cannot tell whether the gains come from using structure *at all* (vs. sequence) or from full-atom voxelization *specifically* (vs. residue-level graphs). This is a significant gap given the paper's central argument about atom-level detail.

### Minor

- **Rotational invariance is not achieved; the model relies on test-time averaging.** Section 4.2 shows that reducing inference from 5 views to 1 reduces R² by 6.4%, indicating the model remains strongly orientation-dependent. The data augmentation covers only 90° rotations around Cartesian axes and mirror reflections (48 discrete orientations), not arbitrary continuous rotations. While the paper acknowledges that vanilla 3D CNNs are orientation-dependent (Section 2.4), the practical cost of multi-view inference (5× FLOPs for inference) should be more explicitly discussed in the compute efficiency narrative.

- **Main results lack confidence intervals.** Tables 1 and 2 report only point estimates. The claim that the ESM-ProteinVista ensemble performs *worse* than ProteinVista alone on IC50 (R² 0.68 vs 0.69, a 1.4% relative difference) would benefit from error bars or a direct statistical comparison, as it is unclear whether this difference is meaningful.

- **Dataset statistics relegated to the appendix.** The size of each benchmark (number of proteins, complexes, train/val/test splits) is in Table S3 rather than the main text, making it hard for the reader to assess whether results are based on hundreds or tens of thousands of examples.

### Trivial

- **Kernel density formula notation.** Section 2.1 (line 57) uses $\|\vec{v} - \vec{r}\|$ (not squared) in the exponent, which corresponds to a Laplacian kernel rather than a Gaussian. This should be clarified or corrected.

- **Storage cost acknowledged but not mitigated.** The 25,000× disk-space increase (75 GB vs 3 MB for 5,800 proteins) is a practical limitation. The paper should briefly discuss whether float16/int8 storage or on-the-fly voxelization from compressed coordinates is feasible.

## Nice-to-Haves

- Present the Rosetta-pretrained results (which do not use ESM-2 at all) alongside the contrastively-pretrained results in the main comparison tables, to decouple the structural representation claim from ESM-2 alignment.
- Reimplement prior SOTA methods within the same pipeline for a fairer SOTA comparison, or simply let the controlled experiments speak for themselves without SOTA claims.
- Discuss whether a structure-based ligand encoder (e.g., 3D CNN on ligand conformers) could further improve protein-ligand interaction prediction.

## Removed Points

These points from the input review are removed or modified for the following reasons:

- **"Contrastive pre-training undermines independent structural reasoning":** The paper uses the word "complementary" (not "independent") throughout. The Rosetta ablation (only 1% worse) shows the model works without ESM-2 alignment. The underlying concern is kept as a Minor weakness above about presentation clarity.
- **"Fusion_ESP is ESM-2-only":** Factually imprecise — Fusion_ESP explicitly fuses protein and chemical knowledge (Du et al., 2025). The uncontrolled-comparison concern stands without this characterization.
- **Section-by-section notes about kernel size schedule lacking ablation, data distribution differences (Swiss-Prot vs UniRef50), and whether 5-view inference was used in main results:** These are either partially addressed by the paper, minor presentation concerns, or speculation. Not substantive weaknesses.
- **GO task uses "independent test set":** This is the paper's own phrasing and not a weakness.

## Novel Insights

The review process surfaces that the paper's SOTA claims (Section 3.3) rest on uncontrolled comparisons with narrow margins (0.2 pp on ESP), while its strongest evidence comes from the well-controlled comparisons against ESM-2. The paper would benefit from repositioning its contribution around the controlled experiments — which are genuinely strong and well-executed — rather than the weakly-supported SOTA outperformance narrative. Additionally, the absence of any structure-aware GNN baseline leaves a significant gap in the evaluation: the paper's argument that atom-level detail matters cannot be evaluated relative to the most relevant alternative approach.

## Suggestions

1. Add a GearNet or ESM-GearNet comparison to the controlled experiments (Section 3.2) to establish whether full-atom voxelization provides gains over residue-level structure-aware methods.
2. Tone down the SOTA outperformance claims or reimplement prior methods within the same pipeline for a fair comparison.
3. Report confidence intervals on all main metrics.
4. Discuss practical mitigations for the storage cost (float16/int8, on-the-fly voxelization).
5. Explicitly state in the main results that 5-view averaging is used during inference.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>