## Summary

FunKAN proposes a generalization of the Kolmogorov-Arnold representation theorem to functional (Hilbert) spaces, enabling direct processing of 2D feature maps without flattening. The resulting U-FunKAN architecture integrates this functional KAN into a U-Net encoder-decoder, using truncated Hermite spectral expansions for inner functions and a learned spatial grid deformation module. The paper demonstrates state-of-the-art IoU on three medical image segmentation benchmarks (BUSI, GlaS, CVC-ClinicDB) at substantially lower FLOPs than competing methods, and also shows benefits for MRI Gibbs-ringing suppression.

## Strengths

- **Efficiency-accuracy tradeoff**: U-FunKAN achieves the lowest Gflops (4.35) among all competitors while achieving top IoU on all three datasets — substantially outperforming U-KAN on BUSI (68.49 vs. 63.38 IoU) at 3× lower compute.
- **Multi-task generalization**: The same backbone is validated on both segmentation and MRI enhancement (Table 4), where FunKAN outperforms all KAN variants by ~1 dB PSNR, providing broader evidence of utility.
- **Ablation studies**: Tables 3, 4 and Figures 4–5 systematically examine channel width, number of Hermite basis functions, and inference time tradeoffs, aiding reproducibility and design understanding.
- **Interpretability narrative**: The spectral energy visualization (Fig. 7) provides a concrete, actionable metric for feature smoothness and potential overfitting — a genuinely useful addition beyond performance numbers.

## Weaknesses

### Fatal
None that fully invalidate the results.

### Major

1. **Theoretical contribution is overstated and underdeveloped.** Statement 3.1 uses the "~" (approximation) symbol rather than "=" and the authors themselves write "we *hypothesize* its generalization." This is a conjecture, not a proved theorem. The paper does not provide a formal proof, error bound, or convergence result, yet the theoretical contribution is listed as the first and primary claim. As stated, Statement 3.1 additionally restricts the inner functions to *linear* functionals (φ_ji ∈ H*), which is a strictly weaker class than the arbitrary univariate functions allowed in the original KA theorem, making it unclear that this is actually a generalization in the usual sense.

2. **Large gap between theory and implementation.** Equation (6) bears little formal resemblance to Statement 3.1. The spatial grid deformation module (Eqs. 7–8) introduces convolutional layers, batch normalization, and ReLU activations that are not derived from the theorem. The resulting FunKAN layer is essentially a learned-basis convolutional block with adaptive sampling — a reasonable design, but one whose connection to the KA theorem is more motivational than rigorous.

3. **GlaS evaluation protocol changes**: The authors replace the benchmark's official train/test split with a random 80/20 split (seed 42), which prevents comparison with the published literature and risks inflated GlaS numbers if the authors' split happens to be easier. This undermines the "state-of-the-art" claim on GlaS.

### Minor

1. The F1 score on BUSI (77.37) is below UKAGNet (77.64), and on CVC (91.42) below U-KAN (91.88). These gaps are small but contradict the "state-of-the-art in both metrics" framing in the abstract; IoU-only superiority is the actual result.
2. UKAGNet results in Table 1 are reported as single-run values without standard deviations, making comparisons statistically incomplete.
3. The ablation in Figure 4 shows very small absolute variation in IoU (65.85–66.75), while the main table reports 68.49 for the same configuration. The different training protocol for the ablation (single learning rate vs. scheduled) explains this, but the discrepancy is confusing without explicit clarification.

### Trivial
- The residual block described in Eqs. (7–8) is inconsistent with the caption; the figure caption uses "pre-activation" but the written equations apply BN before convolution in both main and shortcut paths, which differs from standard pre-activation ResNets.

## Nice-to-Haves

- A complexity analysis comparing the parameter count of a FunKAN layer to an equivalent convolutional layer at the same capacity would clarify where efficiency gains originate.
- Using the official GlaS split to enable fair comparison with the broader literature.
- Including a stronger theoretical result — even an approximation error bound for the truncated Hermite expansion under some regularity assumption would substantially strengthen the theoretical contribution.

## Novel Insights

The key insight — treating feature maps as Hilbert space elements and parameterizing the KA inner functions via truncated Hermite spectral expansions evaluated on a learned deformed grid — is a practically interesting way to endow KAN-type architectures with spatial awareness. The empirical finding that ~1 dB PSNR gain over all scalar-KAN variants on MRI enhancement is achievable purely through this structural change (same convolutional wrapper, different backbone) provides genuine evidence that preserving 2D structure matters beyond architectural inductive bias. The spectral energy interpretation also suggests a lightweight, theoretically motivated diagnostic for feature regularity.

## Suggestions

- Either prove Statement 3.1 formally or reframe it explicitly as a motivating hypothesis and rename the section (e.g., "Motivation from KA theory") to avoid overstating the theoretical claim.
- Rerun GlaS experiments on the official train/test split to enable proper benchmarking.
- Provide standard deviations for all baselines, or at minimum clarify that UKAGNet results are single-run.
- Clarify the discrepancy between the ablation IoU values (~66) and the main table IoU (~68.5) for the same configuration.

## Score and Decision

The work presents a practically motivated and computationally efficient architecture with clear empirical gains on BUSI and a convincing multi-task demonstration. However, the primary claimed contribution — a theoretical generalization of the KA theorem — is actually an unproven hypothesis with a loose connection to the implemented design. The changed evaluation protocol on GlaS introduces a fairness concern. These are substantive issues, but the empirical results are reproducible and the efficiency gain is notable. The paper is at the boundary; the theoretical overstatement and evaluation protocol issue tilt it toward rejection without revisions.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>