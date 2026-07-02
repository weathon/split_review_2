## Summary

ProteinVista introduces a 3D convolutional neural network that voxelizes full-atom protein structures at 1.0 Å resolution and is pre-trained on ~500 k AlphaFold-2 structures via contrastive alignment with ESM-2 embeddings. The model outperforms ESM-2 on three structure-sensitive benchmarks (transporter-substrate, enzyme-substrate, and drug-target IC₅₀ prediction) while using fewer parameters, less pre-training data, and faster inference. An ensemble with ESM-2 further improves accuracy, demonstrating that sequence and structure signals are complementary.

## Strengths

- **Novel and timely approach**: Full-atom 3D CNNs for proteins have been largely abandoned in favor of sequence transformers and graph networks. ProteinVista shows that, with modern hardware and large-scale predicted structures, this class of models is not only tractable but can outperform sequence-only models on tasks requiring fine geometric detail.
- **Strong empirical results on structure-dependent tasks**: On the IC₅₀ regression benchmark, ProteinVista achieves R²=0.69 vs. 0.61 for ESM-2₆₅₀M, a substantial and statistically significant improvement. On transporter-substrate prediction, the optimized ensemble (ESM-ProteinVistaOP) reaches 93.2% accuracy and MCC=0.83, exceeding the previous state-of-the-art.
- **Compute and data efficiency**: ProteinVista uses 123 M parameters (vs. 650 M for ESM-2₆₅₀M), pre-trains on 500 k structures (vs. 250 M sequences), and processes 1 k proteins in 20 s on an A100 (vs. 426 s for ESM-2₆₅₀M). These efficiency gains are clearly documented and practically important.
- **Thorough analysis of complementarity**: The paper systematically examines how performance varies with sequence identity, structural similarity, and structure quality (pLDDT), and shows that the ESM-ProteinVista ensemble consistently outperforms either model alone. This provides actionable insight for practitioners.
- **Ablation studies**: Key design choices (pre-training objective, voxel resolution, number of augmented views, augmentation during fine-tuning) are ablated on the IC₅₀ task, giving clear guidance on what matters most.

## Weaknesses

### Fatal
None.

### Major
- **Pre-training relies on ESM-2 embeddings**: The contrastive objective aligns ProteinVista’s representations with ESM-2, which may limit the model’s ability to learn structural features that are not captured by the sequence model. While the paper shows that ProteinVista adds complementary information, a purely structure-based pre-training objective (e.g., masked voxel prediction) would be a stronger demonstration of the 3D CNN’s independent representational power.
- **No comparison with other structure-aware methods**: The paper compares only with ESM-2 (sequence-only) and specialized substrate-prediction models (SPOT, ProSmith-ESP). It does not compare with graph-based structure models such as GearNet, ESM-GearNet, or other 3D CNNs (e.g., DeepSite, EnzyNet, 3DCNN_MQA). Without such comparisons, it is unclear whether the advantage comes from the full-atom 3D CNN architecture or simply from using any structure-aware encoder.
- **Rotation invariance is not fully achieved**: The model relies on test-time averaging over five random rotations; a single view reduces R² by 6.4%. This indicates that the learned representations are not truly rotation-invariant, which is a practical limitation for deployment and a conceptual weakness compared to equivariant architectures (e.g., SE(3)-transformers, EGNNs).

### Minor
- **Limited atom-type channels**: Only five heavy-atom types (C, N, O, S, P) are used. Hydrogen atoms and other elements (e.g., halogens in drug molecules) are omitted, which may be relevant for binding affinity prediction. The impact of this choice is not discussed.
- **Storage cost is high**: 3D coordinate arrays require ~75 GB for 5 800 proteins, compared to 3 MB for sequences. This is acknowledged but could be a barrier for large-scale applications.
- **State-of-the-art comparison uses an optimized pipeline**: The ESM-ProteinVistaOP results involve fine-tuning the small-molecule encoder and training a separate contrastive network, making it difficult to isolate the contribution of ProteinVista. The simple-pipeline comparisons (Table 1, Table 2) are fair, but the OP results should be interpreted with caution.

### Trivial
- The abstract claims “outperforms sequence transformers” but only ESM-2 is tested; other PLMs (ProtT5, Ankh) are not evaluated.
- Figure 2e (ablation) reports relative changes in R², but the text in section 4.2 gives slightly different numbers (e.g., “6.4%” vs. “~5.5%” in the figure). This inconsistency should be resolved.

## Nice-to-Haves

- Compare with at least one graph-based structure model (e.g., GearNet) on the same benchmarks to contextualize the advantage of full-atom voxelization.
- Explore a purely structure-based pre-training objective (e.g., masked voxel reconstruction) to demonstrate that the 3D CNN can learn useful representations without distillation from a sequence model.
- Evaluate on additional structure-sensitive tasks such as mutation effect prediction or protein-protein interaction prediction, as suggested in the discussion.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that full-atom 3D CNNs, long considered impractical for proteins due to sparsity and memory constraints, can be made efficient through adaptive boxing and modern GPU parallelization, and that they capture geometric information that is complementary to—and in some tasks superior to—sequence-based representations. The finding that the gap between sequence and structure models widens on fine-grained regression tasks (IC₅₀) compared to coarse classification (substrate prediction) provides a useful heuristic for when to invest in structure-based encoders.

## Suggestions

- Add a comparison with a graph-based structure model (e.g., GearNet or ESM-GearNet) on at least one benchmark to strengthen the claim that full-atom 3D CNNs are superior to residue-level graph methods.
- Clarify the inconsistency between the ablation values in the text (section 4.2) and Figure 2e.
- Discuss the potential impact of omitting hydrogen atoms and other atom types, and consider adding them in future work.

## Score and Decision

**Score**: 8  
**Decision**: Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>