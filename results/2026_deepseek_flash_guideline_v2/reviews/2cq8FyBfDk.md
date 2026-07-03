Here is the final consolidated review.

---

## Summary

ProteinVista introduces a full-atom 3D CNN that voxelizes protein structures into adaptive-density grids and is pre-trained on ~500K AlphaFold2 structures via contrastive alignment with ESM-2 sequence embeddings. It demonstrates competitive or superior performance to widely used sequence-based ESM-2 models on protein-ligand binding prediction tasks (TSP, ESP, and BindingDB IC50 regression) while using ~5× fewer parameters and ~1% of the GPU-hours for pre-training.

## Strengths

1. **Dramatically lower pre-training cost with competitive accuracy on structure-dependent tasks**: Pre-training used ~48 hours on 4 A100 GPUs (~500K structures) versus ESM-2 650M's ~7 days on 128 H100 GPUs (250M sequences). Despite this, ProteinVista achieves R²=0.69 vs ESM-2 650M's 0.61 on BindingDB IC50 regression (p < 10⁻³⁰⁴), and 90.8% vs 89.3% accuracy on the TSP classification task (Tables 1–2, Section 4.3).

2. **Adaptive boxing with continuous-density voxelization**: Each protein is embedded in the smallest of four grid sizes (64³, 96³, 128³, 160³) to minimize empty space, and atoms contribute Gaussian-blurred continuous density rather than binary occupancy (Section 2.1). This is a practical innovation that makes full-protein processing tractable at scale.

3. **Systematic stratified analysis of when structure information helps**: Section 4.1 partitions the test set by sequence identity, TM-score, and pLDDT, revealing that ProteinVista excels when structural templates exist in the training set while ESM-2 handles novel folds better. Across all similarity ranges the ensemble outperforms both single models, providing genuinely informative evidence for complementarity.

4. **Honest negative result on GO prediction**: ProteinVista underperforms ESM-2 on Gene Ontology molecular-function prediction (Fmax=0.57 vs 0.62, Section 3.4), demonstrating the authors did not cherry-pick benchmarks and appropriately scoping the model's applicability.

5. **Contrastive alignment of structure and sequence embedding spaces as a pre-training objective**: Using InfoNCE loss to align ProteinVista's structure embeddings with ESM-2's sequence embeddings yields a measurable improvement over multi-task regression on Rosetta scores (+1.0% R² on IC50, Section 4.2).

## Weaknesses

### Fatal
None.

### Major

1. **The compute comparison lacks sufficient transparency to support the efficiency claims as presented**: ProteinVista (415 GFLOPs) processes 1000 proteins in 20s on an A100 during training, while ESM-2_150M (140 GFLOPs, ~1/3 the FLOPs) takes 215s — a 10× runtime disparity. The paper attributes this to "parallelization efficiency" but does not specify whether the ESM-2 baselines used optimized implementations (FlashAttention, mixed precision, appropriate batch sizes) or whether the timing includes voxelization. Given that "compute-efficient" is a central framing claim and a named contribution, the comparison needs greater transparency about measurement conditions and baseline optimization levels.

### Minor

2. **The rotation robustness claim is stronger than the evidence supports**: The augmentation scheme covers only 90° rotations about Cartesian axes plus mirror reflections — at most 24 discrete orientations (the octahedral group). The abstract claims "rotation-robust representations" and Section 2.4 states the goal is "rotation-invariant predictions," but the model has not been tested on arbitrary rotations (e.g., 30° about an arbitrary axis). The 5-view inference ensemble mitigates this partially but does not establish rotation invariance. A proper evaluation on held-out continuous orientations is needed.

3. **The "outperforms sequence transformers" framing is slightly overstated for the individual model**: On the ESP task, ProteinVista alone achieves 91.8% vs ESM-2 650M's 91.9% — a statistical tie. On TSP, ProteinVista achieves 90.8% vs 89.3% — a modest 1.5 pp gain. The cleanest individual-model win is IC50 regression (R² 0.69 vs 0.61). The largest gains come from the ESM-ProteinVista ensemble, not ProteinVista alone. The title and abstract could more precisely distinguish individual-model from ensemble results.

4. **The IC50 ensemble underperformance is not fully explained**: The ESM-ProteinVista ensemble achieves R²=0.68 vs ProteinVista alone's 0.69 (Table 2). The explanation that "accurate affinity prediction relies strongly on fine-grained structural detail, leaving little additional information for the sequence model to contribute" does not account for why adding ESM-2 actively degrades performance. Whether this reflects miscalibration or a statistical artifact should be investigated.

5. **Potential data overlap between pre-training and evaluation is not addressed**: The pre-training set (500K Swiss-Prot/AlphaFold2 structures from Swiss-Prot) may contain proteins overlapping with downstream test sets. Section 4.1 analyzes similarity to the fine-tuning training set, not the pre-training set. Without a sequence-level decontamination analysis, the extent to which observed gains reflect generalization vs. memorization from pre-training is unclear.

6. **Inconsistencies between text and figure values in ablation results (Section 4.2)**: The text reports a 6.4% relative R² drop from single-view inference, a 0.9% gain from 10 vs. 5 views, a 1.0% drop from Rosetta pretraining, and a 1.1% drop from 1.5Å resolution. The figure (Figure 2e table) reports approximately 5.5%, 1.8%, 1.2%, and 0.8% respectively, with "no training augmentation" showing opposite sign (+0.4% in figure vs. -0.1% in text). These discrepancies need resolution.

### Trivial

7. Structures exceeding the 160³-voxel grid are "cropped at the bounding box" (Section 2.1), but the paper does not report how often this occurs or whether binding sites of cropped proteins are affected.

## Nice-to-Haves

- A comparison with or discussion of SE(3)-equivariant architectures (e.g., EGNN, NequIP) as alternative approaches that also process 3D coordinates would strengthen positioning.
- Main-text statistics for dataset sizes (currently referenced as Table S3 in the appendix).

## Removed Points

- Harsh Critic's claim that the compute comparison is "not credible" → Demoted to Major/needs-transparency. The paper provides a plausible explanation (parallelization efficiency of CNNs vs. transformers); the critic's assertion of "artificially slowed" baselines is speculative without evidence of suboptimal implementation.
- "SOTA gains are very small" → Removed. 0.8 pp on TSP and 0.2 pp on ESP are marginal but the main contribution is the architectural approach and compute efficiency, not SOTA-chasing.
- "The 'first compute-efficient full-atom 3D CNN' claim is debatable" → Removed. The paper qualifies this with "pretrained on large-scale AlphaFold-2 structures," distinguishing it from prior non-pretrained 3D CNNs (3DCNN_MQA, etc.).
- "No comparison to equivariant architectures" → Moved to Nice-to-Have. The paper scopes itself against sequence models and graph-based models; demanding an entirely different model family is scope creep.
- "Sources from 2020–2021 are dated" → Removed as a minor nitpick.
- Generic/foundational strengths from Strength Finder about "addressing an important problem" → Removed as generic and lacking specific content.

## Novel Insights

The most interesting finding that emerges from the review is the task-dependent nature of sequence-structure complementarity: on binary classification (TSP/ESP), the ensemble reliably beats both individual models, while on regression (IC50) the ensemble underperforms ProteinVista alone. This asymmetry — also reflected in the homology-stratified analysis where ProteinVista excels on high-similarity bins while ESM-2 holds its own on low-similarity ones — suggests that the marginal value of structural information shrinks as tasks shift from coarse classification to fine-grained regression, and as the test protein diverges from the training distribution. This is a nuanced observation worth deeper investigation.

## Suggestions

1. Provide per-configuration FLOPs and runtime breakdowns to make the compute comparison transparent. Report whether ESM-2 baselines used FlashAttention, mixed precision, and equivalent batch sizes.
2. Test the model on proteins rotated by continuous random angles (not just 90° increments) and report whether performance degrades. If it does, acknowledge the limitation.
3. Perform a sequence-level decontamination analysis between pre-training and test sets (e.g., remove test proteins with >30% identity to any pre-training protein).
4. Resolve the text/figure inconsistencies in Section 4.2 ablation values.
5. Report how many test proteins exceed each box size in the adaptive boxing scheme, and verify that binding sites of cropped proteins are intact.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>