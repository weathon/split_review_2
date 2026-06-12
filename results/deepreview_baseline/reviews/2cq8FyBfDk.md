## Summary

ProteinVista introduces a compute-efficient 3D convolutional neural network that voxelizes full atom-level protein structures and is pre-trained on ~500,000 AlphaFold-2 predicted structures via contrastive alignment with ESM-2 embeddings. The model demonstrates competitive or superior performance to sequence-based ESM-2 models on structure-dependent tasks (enzyme-substrate, transporter-substrate, and drug-target inhibition prediction) while using 5x fewer parameters and orders of magnitude less pre-training data, and shows that sequence and structure signals are complementary.

## Strengths

- **Novel and well-motivated approach**: The paper convincingly argues that existing structure-aware methods (GNNs on residue graphs) omit atom-level details, and demonstrates that full-atom 3D CNNs are tractable with modern hardware and adaptive boxing strategies. This fills a genuine gap in the literature.
- **Strong empirical results on structure-dependent tasks**: ProteinVista outperforms ESM-2_650M on the IC50 regression task (R² 0.69 vs 0.61) and matches/exceeds it on substrate classification, with the ensemble (ESM-ProteinVista) achieving state-of-the-art results on both TSP and ESP benchmarks. The statistical significance tests (p < 10^-13, p < 10^-304) provide confidence.
- **Compute efficiency is genuinely impressive**: Pre-training on 4 A100 GPUs for 48 hours vs. 128 H100 GPUs for 7 days for ESM-2_650M, with faster inference despite similar FLOPs, is a meaningful practical contribution. The adaptive boxing strategy is a clever engineering solution to the sparsity problem.
- **Thoughtful ablation and analysis**: The stratification by sequence identity, TM-score, and pLDDT (Figure 2) provides nuanced understanding of when structure helps vs. when it doesn't. The ablation on augmentation, pretraining objective, and resolution is informative and well-executed.

## Weaknesses

### Major

- **Limited architectural novelty and shallow exploration of 3D CNN design**: The 3D CNN architecture itself is quite standard (5 blocks of conv-bn-relu-maxpool with decreasing kernel sizes). The paper does not explore or compare with more modern 3D architectures (e.g., residual connections, attention mechanisms, sparse convolutions, or equivariant networks like SE(3)-transformers). Given that the paper claims to "introduce the first compute-efficient full-atom 3D CNN," the architectural contribution is modest.
- **The contrastive pretraining to ESM-2 embeddings is conceptually circular**: ProteinVista is pretrained to align its structure embeddings with ESM-2 sequence embeddings, yet the paper's main claim is that structure provides information beyond sequence. If the pretraining objective forces structure embeddings toward sequence embeddings, this could limit the model's ability to learn genuinely novel structural features. The ablation shows only a 1% difference from Rosetta-based pretraining, which suggests the contrastive objective is not critical, but the conceptual tension is worth addressing.
- **Missing comparison with other structure-aware methods**: The paper compares only against ESM-2 (sequence-only) and does not compare against GearNet, ESM-GearNet, or other structure-aware GNNs that also use AlphaFold structures. Given that these methods are cited as related work and also use 3D structure (albeit at residue level), a direct comparison is essential to substantiate the claim that atom-level detail provides additional value over residue-level structure.

### Minor

- **The GO term prediction experiment is underdeveloped**: The paper reports that ProteinVista underperforms ESM-2 on GO annotation (F_max 0.57 vs 0.62) and concludes that structure adds limited value for homology-based tasks. However, GO annotation is a multi-label problem with thousands of classes, and the paper does not describe the fine-tuning setup, evaluation protocol, or whether the same simple pipeline was used. This experiment feels like an afterthought rather than a rigorous analysis.
- **Storage cost is dismissed too quickly**: The paper notes that 5,800 proteins require 75 GB as float32 NumPy arrays. This is a substantial practical barrier for many labs, and the paper does not discuss potential mitigations (e.g., compression, on-the-fly voxelization from PDB files, or mixed-precision storage). For a paper emphasizing accessibility, this is a nontrivial limitation.
- **The ensemble method is simple averaging without analysis of complementarity**: The paper averages predictions from ProteinVista and ESM-2 but does not analyze which proteins benefit from which model, or whether a learned weighting would improve results. The claim of "complementary signals" would be stronger with case studies or error analysis.

### Trivial

- The paper states "123 million parameters" but Figure 3a shows approximately 120 million; minor inconsistency.
- The ablation table in the main text (Figure 2e) has slightly different numbers than described in the text (e.g., "1.0%" vs "1.2%" for Rosetta vs CL pretraining).

## Nice-to-Haves

- Comparison with residue-level GNNs (GearNet, ESM-GearNet) on the same benchmarks would significantly strengthen the paper.
- Analysis of which voxels/regions drive predictions (e.g., Grad-CAM visualization) would provide mechanistic insight into what the model learns.
- Discussion of how the model handles proteins with missing atoms or non-standard residues in PDB files.
- Exploration of whether the model benefits from ensembling multiple AlphaFold-2 predictions (e.g., top-5 models) rather than a single structure.

## Novel Insights

The paper's most interesting finding is that a simple 3D CNN on voxelized atoms, despite lacking any built-in rotation invariance, can match or exceed sequence transformers on structure-dependent tasks through data augmentation alone. The stratification analysis (Figure 2a-c) provides a nuanced picture: structure helps most when the test protein has a close structural neighbor in the training set, while sequence models are more robust to novel folds. This suggests that the two modalities capture genuinely different aspects of protein function, and the optimal approach depends on the specific prediction scenario. The finding that the ensemble consistently outperforms either model alone, even when one model individually underperforms, is practically valuable.

## Suggestions

- Add comparisons with at least one structure-aware GNN (e.g., GearNet or ESM-GearNet) on the same benchmarks to substantiate the claim that atom-level detail provides additional value over residue-level structure.
- Discuss the conceptual tension between pretraining via contrastive alignment to ESM-2 and the claim that structure provides information beyond sequence. Consider adding an experiment where ProteinVista is pretrained without any sequence-derived signal (e.g., pure masked voxel prediction) to test whether the model can learn useful structural features independently.
- Provide more detail on the GO term prediction experiment, including the number of classes, evaluation metric, and whether the same pipeline was used, to make the negative result more interpretable.

## Score and Decision

The paper presents a well-executed, practically useful contribution that convincingly demonstrates the value of full-atom 3D CNNs for structure-dependent protein prediction tasks. The compute efficiency and strong empirical results on binding prediction benchmarks are genuine strengths. However, the lack of comparison with structure-aware GNNs and the conceptual tension in the pretraining objective are significant gaps that prevent the paper from being a definitive advance. The paper is a solid contribution that merits acceptance but falls short of the highest tier.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>