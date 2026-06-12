## Summary

ProteinVista introduces a compute-efficient 3D CNN that voxelizes full-atom protein structures at 1.0Å resolution and pre-trains on ~500K AlphaFold-2 predicted structures using contrastive alignment to ESM-2 embeddings. The model outperforms sequence-only ESM-2 (both 150M and 650M parameter variants) on three structure-dependent benchmarks—transporter-substrate classification, enzyme-substrate classification, and IC50 drug-target affinity prediction—while using far less pre-training data and compute, and the complementary information is further demonstrated via simple ensembling.

## Strengths

- **Well-motivated and clearly articulated research question**: The paper convincingly argues that residue-level graph representations miss atom-level details critical for binding site chemistry, and that despite the perceived inefficiency of 3D CNNs on sparse protein structures, modern hardware and large predicted-structure databases now make this feasible. This fills a genuine gap in the literature.

- **Rigorous and fair experimental comparison**: All models (ProteinVista, ESM-2_150M, ESM-2_650M) are fine-tuned under identical conditions with the same prediction head architecture and identical small-molecule embeddings. This deliberate control isolates the effect of the protein encoder, making the comparison interpretable and fair. Statistical significance testing (McNemar's test, Wilcoxon signed-rank test) is properly applied.

- **Comprehensive analysis and ablation studies**: The paper provides stratified analyses by sequence identity, structural similarity (TM-score), and AlphaFold-2 confidence (pLDDT), which reveal clear and interpretable patterns about when and why structure-based representations help. The ablation study on augmentation strategy, pre-training objective, number of inference views, and voxel resolution provides actionable design insights.

- **Efficient design with practical impact**: With 123M parameters, ~1% of ESM-2's pre-training GPU-hours, and faster training/inference than ESM-2_650M, ProteinVista demonstrates that 3D CNNs need not be prohibitively expensive. The adaptive boxing strategy (64³ to 160³ Å³) is a practical solution to memory efficiency that handles variable protein sizes well.

- **Balanced presentation of limitations**: The discussion honestly acknowledges when ProteinVista underperforms (GO annotation, low-confidence structures, low-sequence-identity regime) and identifies concrete directions for improvement (conformational ensembles, deeper architectures, alternative pre-training objectives).

## Weaknesses

### Fatal
None.

### Major

- **Limited diversity of benchmarks**: All three binding tasks (transporter-substrate, enzyme-substrate, IC50) test a similar capability—protein-small molecule interaction. The GO annotation experiment confirms the expected limitation but doesn't extend the positive case. Including additional structure-dependent tasks such as protein-protein interaction prediction, binding site residue prediction, or mutation effect prediction would significantly strengthen the generality of the claims. The paper explicitly mentions these as future work, but the current evidence base is narrow relative to the broad claim that "full-atom 3D CNNs are both tractable and superior than protein transformers for structure-dependent tasks."

- **Contrastive pre-training creates a dependency on ESM-2**: The pre-training objective aligns ProteinVista embeddings to ESM-2 embeddings, which means the structure encoder's learned representations are partly shaped by and entangled with a sequence model. This raises a conceptual concern: when ProteinVista outperforms ESM-2 on downstream tasks, some of that improvement may stem from the pre-training distillation rather than purely from structural information. The comparison with the Rosetta-based pre-training (1% R² drop) partially addresses this but does not fully resolve the concern, as the Rosetta scores are also sequence-derivable in principle. A pre-training objective purely based on 3D structure (e.g., masked voxel prediction) without any sequence-model dependency would more cleanly demonstrate the value of structural information.

- **IC50 ensemble result is puzzling**: On IC50 prediction, the ESM-ProteinVista ensemble performs *worse* than ProteinVista alone (R² 0.68 vs 0.69). The paper explains this by noting "little additional information for the sequence model to contribute," but if the signals are complementary in classification tasks, it is unexpected that ensembling hurts on regression. This suggests potential issues with the simple averaging strategy on regression targets, or that the ESM-2 signal is actually somewhat noisy for this task. A more nuanced fusion strategy (e.g., learned weighting) or a clearer investigation would strengthen this point.

### Minor

- **Rotation augmentation strategy is limited to 90° rotations and axis-aligned mirrors**: While this is a practical choice, it means the model is only partially invariant—structures at 45° rotations are not covered by augmentation. The ablation shows that training augmentation has little effect (-0.1%), suggesting the model may already be overfit to augmentation-similar orientations. More diverse rotation strategies (e.g., SO(3) sampling) could improve robustness.

- **Cropping at 160³ Å for large proteins**: The paper states that structures exceeding the largest grid are simply cropped, which could lose critical binding-site information for large proteins. The fraction of affected proteins and the impact on performance for these cases is not discussed.

- **Storage cost discussion could be more actionable**: The 75 GB for ~5,800 proteins is noted as a limitation, but the paper does not discuss practical mitigation strategies (e.g., compression, sparse representations) that could make large-scale deployment feasible.

- **The comparison with state-of-the-art substrate models (Section 3.3) uses an optimized pipeline (OP) that differs from the controlled comparison in Section 3.2**: This makes it harder to attribute the gains—some come from the optimized training pipeline (joint fine-tuning, contrastive network) rather than from ProteinVista itself. The gains over SOTA are also modest (e.g., 93.2% vs 92.4% accuracy on TSP).

### Trivial
None worth noting beyond parser artifacts.

## Nice-to-Haves

- A Grad-CAM or similar visualization applied to a concrete example (e.g., a known binding site) would powerfully demonstrate that ProteinVista learns physically meaningful features, rather than being purely predictive.

- Comparing against other structure-aware baselines (e.g., GearNet, GPS-Fun) under the same experimental protocol would contextualize ProteinVista's gains more clearly.

- Reporting confidence intervals or standard deviations across multiple random seeds would strengthen the reproducibility and statistical rigor of the results.

## Novel Insights

The paper's most valuable insight is empirical: despite widespread belief that 3D CNNs on full-atom protein structures are computationally infeasible, ProteinVista demonstrates that with adaptive boxing, modern GPUs, and large-scale predicted structures, this approach is not only tractable but can match or exceed sequence transformers with orders-of-magnitude less pre-training data and compute. The stratified analysis revealing that ProteinVista excels when test proteins have close structural neighbors in the training set, while ESM-2 is better in the low-similarity regime, provides a practical guide for when to use which representation. The complementarity between sequence and structure encoders, while not surprising conceptually, is quantitatively demonstrated and actionable.

## Suggestions

- Add at least one additional structure-dependent benchmark (e.g., protein function prediction at the residue level, protein-protein interaction, or mutation effect prediction) to broaden the evidence base for the claims.
- Include a pre-training variant using masked voxel prediction (a purely structural objective) to disentangle the contribution of 3D information from ESM-2 distillation.
- Investigate learned fusion (e.g., a small MLP or attention layer combining ProteinVista and ESM-2 embeddings) instead of simple averaging, especially for the regression task where averaging hurts.
- Report performance broken down by protein size to assess whether the 160³ Å cropping affects results on large proteins.

## Score and Decision

The paper presents a well-executed study with a clear research question, fair experimental comparisons, and thorough analysis. The core contribution—demonstrating that full-atom 3D CNNs are tractable and competitive with protein LMs using far less data and compute—is genuine and practically important. However, the benchmark diversity is limited (all three positive results are protein-small-molecule binding tasks), the contrastive pre-training creates a dependency on ESM-2 that complicates interpretation, and the improvements over existing optimized methods (Section 3.3) are modest. These factors temper enthusiasm without invalidating the contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept