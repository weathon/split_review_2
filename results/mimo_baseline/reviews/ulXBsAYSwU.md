## Summary

MolMiner is a fragment-based autoregressive molecular generation model that combines dynamic 3D geometry awareness (via forcefield relaxation), symmetry-aware fragment attachments, order-agnostic rollouts, and multi-property conditioning over twelve physicochemical and structural properties. The paper also proposes improved benchmarking using Wasserstein distance and calibration plots for evaluating both unconditional and conditional generation.

## Strengths

- **Novel unification of features**: The paper combines several desirable design choices—fragment-based generation, dynamic 3D geometry via forcefield updates, order-agnostic rollouts, and symmetry-aware attachments—into a single framework. Each of these is individually motivated and the combination is architecturally coherent.

- **Multi-property conditional generation at scale**: Supporting simultaneous conditioning on twelve properties with any subset specified is a meaningful advance. The GMM-based property completion mechanism for partial conditioning is practical and well-motivated. The calibration plots (Figure 2) show reasonable diagonal alignment for most properties (logP, SAS, FractionCSP3, TPSA, HBD, HBA, ring count, rotatable bonds), demonstrating that the model does respond to conditioning signals.

- **Thoughtful evaluation methodology**: The use of 1D Wasserstein distance for distributional comparison and calibration plots for conditional evaluation are rigorous choices that go beyond standard metrics. The paper is also transparent about where performance falls short (e.g., QED, molWt, MR), which builds trust in the reported results.

- **Automatic validity guarantee**: As a fragment-based model operating with valence-respecting fragments and attachment rules, MolMiner consistently produces chemically valid molecules, eliminating a common failure mode of atom-level generative models.

## Weaknesses

### Fatal
None.

### Major

- **Insufficient baseline comparisons**: Only HierVAE is used for quantitative comparison. MoLR is excluded after a 7-day training run with poor results, and MARS is excluded because it uses oracle property evaluations at inference time. While these exclusions are individually justified, the net result is that MolMiner is compared against a single baseline from 2020. There are no comparisons with conditional generation methods (e.g., conditional VAEs, property-guided diffusion models, or other autoregressive baselines), making it impossible to assess whether the conditional generation performance is competitive with the state of the art. The calibration plots in Figure 2 lack any baseline context—without knowing how other models perform on the same task, the diagonal alignment is difficult to interpret as good or merely adequate.

- **Unconditional generation consistently below baseline**: Table 1 shows MolMiner underperforming HierVAE across most properties, with large gaps on molecular weight (15 vs. 47/65 Wasserstein distance), TPSA (2.3 vs. 7.6/10.9), and MR (3.8 vs. 11.9/16.3). The paper attributes this to early termination bias from order-agnostic rollouts and GMM approximation error, but MolMinerD (which uses ground-truth conditions) also shows large gaps, weakening this explanation. Since the model is primarily sold as a conditional generator, these gaps are not fatal, but they raise concerns about whether the core generation quality is sound.

- **No quantitative metrics for conditional generation quality**: The conditional generation evaluation relies entirely on visual inspection of calibration plots. No scalar metrics (e.g., mean absolute error between prompted and predicted properties, R² scores) are reported, and no comparison to other conditional generation methods is provided. This makes the central claim—that MolMiner achieves "calibrated conditional generation across most properties"—difficult to rigorously verify or compare.

- **Training-inference distribution shift**: Forcefield relaxation occurs during generation but training uses precomputed (pre-relaxed) geometries. This discrepancy means the model sees different geometric configurations at inference time than during training, and the impact of this shift is not analyzed or ablated.

### Minor

- **Termination action imbalance**: The paper identifies early termination bias as a key limitation but does not attempt any mitigation (e.g., termination balancing, RL fine-tuning). This is acknowledged but feels like an incomplete evaluation since it affects both unconditional and conditional performance.

- **Fragment vocabulary and scalability**: The fragment vocabulary derived from SSSR and isolated bonds is not characterized in terms of size or coverage. The impact of vocabulary design on generation capacity and the model's behavior on out-of-vocabulary structural motifs are not discussed.

- **No 3D property evaluation**: While the model incorporates 3D geometry during generation, all twelve evaluated properties are 2D descriptors computable from molecular graphs. The 3D-awareness is architecturally present but never shown to provide measurable benefit for any evaluated task.

### Trivial
None.

## Nice-to-Haves

- Quantitative conditional generation metrics (MAE, R²) alongside calibration plots
- Comparison with at least one conditional generation baseline
- Ablation of geometry-awareness contribution to conditional generation quality
- Analysis of fragment vocabulary statistics and their impact on molecular diversity

## Novel Insights

The paper's most interesting observation is that order-agnostic rollouts serve as effective data augmentation, exposing the model to diverse construction orders and reducing overfitting. Additionally, the approach of fitting a GMM to the empirical joint distribution of molecular properties to enable partial conditioning (specifying any subset of properties) is a practical and elegant solution that could be adopted by other conditional generation frameworks. The symmetry-aware fragment attachment protocol, while specific to this architecture, addresses a real problem in fragment-based generation that was previously underexplored.

## Suggestions

1. Add at least one quantitative metric for conditional generation (e.g., MAE across prompted properties) and compare against a conditional baseline to contextualize the calibration results.
2. Ablate the forcefield relaxation during generation—does using frozen (pre-relaxed) geometries degrade conditional generation quality? This would justify the training-inference mismatch.
3. Investigate and report termination action rates during generation, and consider simple mitigation strategies (e.g., temperature scaling of termination probability) to address the early termination bias.
4. Report validity rates explicitly even though the model guarantees valence-correct molecules, as this builds trust and follows community conventions.

## Score and Decision

The paper presents an architecturally coherent and novel combination of desirable features for molecular generation. The multi-property conditioning capability is genuinely useful, and the evaluation methodology (Wasserstein distances, calibration plots) is well-chosen. However, the experimental evaluation is significantly weakened by the absence of conditional generation baselines, the lack of quantitative conditional metrics, and consistently below-baseline unconditional performance. The core claim of "calibrated conditional generation" is supported only by visual inspection of calibration plots without comparative context. These gaps make it difficult to assess the true contribution relative to the existing literature, despite the promising architectural design.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject