Now I have all the information needed. Let me compile the final review.

---

## Summary

This paper proposes LS-Merge, a framework for encoding LLM weights into a latent space via a transformer-based VAE, performing merging operations (interpolation, soup) in that space, and decoding back to weights. Key contributions include: (1) an analysis of LLM weight statistics showing heavy-tailed distributions that motivate encoder design, (2) a latent-space merging framework with Optimal Transport alignment for cross-architecture merging, and (3) empirical demonstrations on self-merging, LoRA expert merging, and heterogeneous (cross-family) merging.

## Strengths

- **Weight distribution analysis (Section 3.1, Table 1):** The paper provides concrete empirical evidence that LLM weights have low variance, near-zero means, and markedly high excess kurtosis (up to ~15 in early attention layers). This is a genuinely useful observation that directly motivates encoder design choices and goes beyond generic "weights are heavy-tailed" intuition.

- **Optimal Transport alignment for heterogeneous merging (Section 3.3, Eq. 2):** The observation that heterogeneous models produce disjoint latent manifolds and the use of a closed-form affine OT map under a Gaussian assumption to register them is principled. Algorithm 1 clearly lays out the per-layer pipeline. This is the paper's most technically distinct contribution.

- **PCA vs. VAE comparison (Table 8):** The dramatic collapse of PCA-reconstructed models (MMLU: 41.44 → 25.50 at r=1.6) while the VAE retains ~96% of performance is a striking result that demonstrates pretrained weights do not lie on a linear subspace. This finding has implications beyond this paper.

## Weaknesses

### Fatal
None.

### Major

- **VAE training confound in self-merging experiment (Section 4.1, line 183):** The VAE is trained jointly on weights from *both* Gemma-3-1B-it and Gemma-3-4B-it. The self-merging experiment encodes a single model and samples multiple latents from its posterior. Because the decoder has jointly learned the distribution of both architectures, it may reconstruct patterns from the larger model when decoding the smaller model's latents. The observed improvement over the base model (Table 2: 32.20 → 35.13 MMLU for the 1B model) could therefore stem from information leakage across architectures rather than the latent-space operation itself. A control experiment training the VAE on a single model's weights only is needed to isolate the effect.

- **VAE reconstruction alone outperforms the base model without explanation (Table 2):** For Gemma-3-4B-it, the VAE single-reconstruction baseline scores *higher* than the original base model on MMLU (54.10 vs. 53.10), HellaSwag (49.03 vs. 47.40), and GSM8k (31.27 vs. 29.90). A lossy compression (compression ratio 2) that improves a pretrained model's task performance is surprising and the paper offers no explanation. The downstream merging improvements may simply inherit this unexplained gain, and the paper's silence on this point undermines confidence in the subsequent comparisons.

### Minor

- **Cross-architecture merging gains are marginal (Section 4.4, Table 5):** At λ=0.1 (90% target, 10% source), improvements over the base model are 0.92 (WinoGrande), 0.56 (ARC-C), and 1.03 (HellaSwag) percentage points. While this demonstrates that cross-architecture merging is *possible*, the practical benefit is thin. The "OT only" baseline (alignment without interpolation) crashes performance (WinoGrande drops from 56.83 to 51.13), indicating nearly all benefit comes from staying close to the target model rather than from genuinely integrating source knowledge.

- **Comparison with representation-merging methods is limited to one setting (Section 4.3, Table 4):** The comparison with Task Arithmetic and AIM uses only one model family (Llama-2-13B) and one fine-tuning setup (code + instruct). The paper claims to "match the performance of prominent methods," but the evidence is insufficient to draw general conclusions.

- **PCA vs. VAE comparison confounds linearity with data-driven learning (Section 5.3, Table 8):** PCA is applied per-matrix (no cross-layer learning), while the VAE is a data-driven model trained across layers. Although a linear autoencoder with L2 loss would converge to the PCA solution (partially justifying the comparison), the confound means the experiment does not cleanly isolate linear vs. non-linear compression. A linear autoencoder trained on the same data would be a cleaner ablation.

### Trivial

- **VAE training details are underspecified:** The paper states "Training data consist of pretrained weight snapshots" but does not specify how many snapshots, training steps, or the VAE's parameter count relative to the encoded models. This limits reproducibility.

## Nice-to-Haves

- Train the VAE on a single model's weights and verify that the self-merging improvement over the base model persists.
- Add a "reconstruct-then-merge" control for LoRA expert experiments: encode each expert, immediately decode it, then apply weight-space merging.
- Replace the PCA baseline with a linear autoencoder trained on the same data to cleanly test linearity vs. non-linearity.
- Report the source model's standalone performance alongside cross-architecture merging results and systematically evaluate at multiple λ values.

## Removed Points

These points were flagged during review filtering and are not included as weaknesses in the main review:

- "Algorithm 1 and Algorithm 2 are both referenced but only one is shown" — The reference to Algorithm 2 is likely in the appendix (stripped by the parser); not a verifiable issue.
- "The 'dimensionality-matching projection' is straightforward" — Subjective opinion, not a verifiable weakness.
- "No variance from VAE training seeds" — Single training run is standard practice in this setting.
- Various Section-by-Section notes (e.g., "the theoretical compressibility argument adds little") — Subjective assessments, not concrete problems.
- Missing related works — Cannot be confirmed without external sources per policy.
- Formatting/style nitpicks — Parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The most impactful improvement would be to cleanly separate the VAE's reconstruction effect from the latent-space merging effect by: (a) training the VAE on a single model for the self-merging control, and (b) adding a reconstruct-then-merge baseline for the expert merging experiments. Additionally, providing explicit numbers for training data size, steps, and VAE parameter count would improve reproducibility. Consider comparing against a simpler alignment baseline (e.g., z-score normalization + linear interpolation without OT) to clarify whether the full OT machinery is necessary.

## Score and Decision

The paper introduces a genuinely novel framework (latent-space merging with OT alignment for heterogeneous architectures) and provides useful empirical characterization of LLM weight statistics. However, the experimental evidence has two significant issues: the VAE training confound in self-merging and the unexplained finding that a lossy VAE reconstruction already outperforms the base model. These concerns weaken confidence that the observed improvements are attributable to latent-space operations rather than to properties of the VAE itself. The cross-architecture results, while technically novel, show only marginal gains. On balance, the paper has real contributions that merit further development but needs cleaner experimental design to fully support its claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>