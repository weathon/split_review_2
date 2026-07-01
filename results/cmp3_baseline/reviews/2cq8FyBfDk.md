## Summary

ProteinVista introduces a compute-efficient 3D convolutional neural network that voxelizes full-atom protein structures and is pre-trained on ~500k AlphaFold2 structures via contrastive alignment with ESM-2 embeddings. The model achieves competitive or superior performance to sequence-only transformers (ESM-2) on three protein-ligand prediction benchmarks while using substantially fewer parameters and less pre-training data, demonstrating that full-atom 3D CNNs are a viable and complementary alternative to sequence-based models for structure-sensitive tasks.

## Strengths

- **First large-scale pre-trained full-atom 3D CNN for proteins.** The paper shows that a carefully designed 3D CNN with adaptive bounding boxes and strong data augmentation can be trained efficiently on predicted structures at scale, challenging the prevailing reliance on sequence-only or graph-based approaches.

- **Thorough and fair experimental design.** The comparison to ESM-2 uses an identical simplified pipeline (fixed MolFormer embeddings, same prediction head) to isolate the effect of the protein encoder, and statistical significance tests (McNemar’s, Wilcoxon) are provided to substantiate the gains.

- **Insightful analysis of complementarity and failure modes.** The stratification by sequence identity, TM-score, and pLDDT clearly shows when structure information helps and when it does not, and the ensemble results confirm that sequence and structure signals are partially complementary.

- **Detailed ablation studies.** The impact of pre-training objective, voxel resolution, number of augmentation views, and augmentation during fine-tuning are all quantified on the IC50 regression task, providing practical guidance for future work.

- **Compute efficiency analysis.** The paper reports FLOPs, training time, epoch counts, and pre-training resources, showing that ProteinVista is faster per-iteration and requires far fewer GPU-hours for pre-training than ESM-2.

## Weaknesses

### Fatal  
None.

### Major  

- **Missing comparison to structure-aware graph neural networks (GNNs).** The paper claims to outperform sequence transformers, but the most relevant baseline class is structure-aware models like GearNet, ESM-GearNet, or GPS-Fun, which also leverage 3D coordinates (at residue or near-atom level).  Without such comparisons, it is unclear whether 3D CNNs offer advantages over graph-based structure encoders, which are the current standard for structure-conditioned protein learning.  This omission weakens the claim that ProteinVista is superior for structure-dependent tasks.

- **Title and abstract overstate the individual model’s superiority.** On transporter-substrate and enzyme-substrate prediction, ProteinVista alone is comparable to or only slightly better than ESM-2; the largest gains come from the ensemble (ESM-ProteinVista).  The claim "outperforms sequence transformers" is task-dependent and often requires ensemble averaging.  The paper is transparent in the results but the rhetoric in the title and abstract could mislead readers.

- **Pre-training relies on ESM-2 as the teacher.** The contrastive objective aligns ProteinVista embeddings with ESM-2 sequence embeddings, meaning the structure encoder is learning directly from a sequence model’s representations.  This blurs the distinction between “structure-only” and “sequence-informed” learning and raises the question of whether the downstream gains would hold if ProteinVista were pre-trained entirely without sequence knowledge (e.g., with a purely structural objective).  The Rosetta score regression ablation partially addresses this but the final model still uses ESM-2 distillation.

### Minor  

- **Limited architecture depth and spatial resolution.** The model uses only five convolutional blocks with aggressive max-pooling, followed by global average pooling that discards all spatial information.  While this keeps compute low, it may limit the ability to capture fine-grained geometric features such as pocket shapes or subtle atom arrangements that are only a few voxels wide.  The 1.0Å voxel resolution is modest for atomic details (typical bond lengths ~1.5Å), and the ablation shows only a 1.1% drop at 1.5Å, suggesting room for improvement.

- **GO term prediction evaluation is too brief.** Only molecular-function GO terms are tested, and the reported Fmax of 0.57 is modest.  Without also evaluating biological process and cellular component, or comparing to structure-aware GNNs on this task, the conclusion that structure encoders add limited value for homology-driven tasks is not strongly supported.

- **Optimized pipeline (OP) includes ESM-2 in the ensemble for SOTA comparison.** In Section 3.3, the state-of-the-art comparison uses ESM-ProteinVista_OP, which averages predictions from both encoders.  The individual ProteinVista performance under the OP is not reported, so it is unclear how much of the SOTA gain is attributable to ProteinVista alone versus the combination with ESM-2.

### Trivial  

- The bar chart in Figure 3 shows inference time for 1000 samples, but the absolute values (20s for ProteinVista vs 426s for ESM-2) should be contextualized as GPU-specific and implementation-dependent.  This is not a flaw, but a minor point for reproducibility.

## Nice-to-Haves  

- Compare against at least one graph-based structure model (e.g., GearNet or a vanilla protein GNN) on the same tasks to directly evaluate the value of atom-level voxelization over residue-level graphs.
- Report individual ProteinVista performance under the optimized pipeline (OP) to disentangle the effect of the encoder from the effect of the training pipeline.
- Experiment with a deeper or wider 3D CNN to explore whether scaling laws hold for this class of models, as suggested in the Discussion.

## Novel Insights

The paper demonstrates that a 3D CNN operating on full-atom density grids can learn representations that are complementary to sequence models, with the degree of complementarity varying systematically with task demands (classification vs. regression) and with structural similarity to the training set.  The finding that the advantage of structure information is most pronounced for high-confidence predicted structures and for closely related proteins, while sequence models handle remote homologs better, provides a clear roadmap for combining both modalities.  This is practically useful: practitioners can decide whether to incur the storage cost of 3D grids based on the expected structural novelty of their test set.

## Suggestions  

- Add a comparison to a simple residue-level 3D CNN or a GNN that operates on predicted structures to isolate the benefit of atom-level resolution over residue-level resolution.
- In the title and abstract, qualify the outperformance claim (e.g., “outperforms or complements sequence transformers” or “achieves superior performance on structure-sensitive benchmarks”).

## Score and Decision

**Score:** 6  
**Decision:** Accept

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>