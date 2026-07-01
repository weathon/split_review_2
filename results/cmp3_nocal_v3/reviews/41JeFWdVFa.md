Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper proposes LDP, a lightweight denoising autoencoder plug-in that improves SR model generalization by enforcing cyclic consistency between the SR output and the LR input. LDP operates in two modes: as a training-time loss during fine-tuning, and as an inference-time post-processing step for diffusion models. The core idea — repurposing a DAE as a degradation-model regularizer — is conceptually clean and practically lightweight (642k parameters).

## Strengths

- **Novel and principled conceptual framing.** Repurposing a denoising autoencoder as a cyclic-consistency plug-in that wraps existing SR models without architectural changes is a genuine contribution. The two-mode design (training loss and inference post-processing) adds versatility.

- **Broad architectural coverage in fine-tuning evaluation.** Experiments span GAN-based (FeMaSR), diffusion-based (StableSR), Transformer-based (SwinIR), and Mamba-based (MambaIR) architectures (Table 3), demonstrating model-agnostic applicability.

- **Genuinely lightweight.** With 642k parameters and ~16 hours of training on a single A6000, LDP is computationally inexpensive — a meaningful practical advantage over test-time adaptation methods.

- **Informative ablation of loss components.** Table 6 systematically decomposes the loss terms, showing that combining symmetric and frequency losses (LDPV5–LDPV7) yields the best results, and that each component contributes.

## Weaknesses

### Fatal
None.

### Major

- **Fine-tuning evaluation conflates LDP with additional training data, preventing clean attribution.** In Section 4.3 (Tables 3–4), baseline models are evaluated from their original checkpoints, while the "+LDP" variants are fine-tuned on DF2K with BSRGAN degradation patterns **using the LDP loss** (line 160: "We fine-tune existing SR models on the DF2K dataset... using BSRGAN degradation patterns, with our LDP employed as an auxiliary loss"). The comparison therefore mixes two factors: (a) additional training on BSRGAN-degraded data, and (b) the LDP loss itself. Without a control condition where each baseline is fine-tuned on the same BSRGAN data *without* LDP, the reported gains cannot be attributed to LDP. The ablation study (Table 6) does not resolve this: even the "frequency loss only" variant (LDPV1) involves fine-tuning on BSRGAN data. This is the most consequential weakness in the paper — the central empirical claim (that LDP improves generalization) is not interpretable from the evidence presented.

- **Inference-time (posterior sampling) results do not support the claimed improvements.** Table 5 is the primary evidence for the inference-time mode, and the results are unpersuasive:
  - **LDM + LDP on RealSR:** most metrics degrade (CLIPIQA 0.4564→0.4319, QAlign 2.685→2.610, etc.).
  - **ResShift + LDP:** changes are effectively zero across all datasets (e.g., CLIPIQA 0.5353→0.5354, MUSIQ 56.85→56.85).
  - **UPSR + LDP:** mixed, with tiny positive and negative changes (e.g., DPED CLIPIQA drops 0.4094→0.4026).
  - **StableSR + LDP** shows consistent improvements, but this is one of four baselines.

  The paper's claim that "after applying LDP, the baselines show improvements across nearly all metrics on most datasets" (line 274) is contradicted by LDM (systematic degradation) and overstated for ResShift and UPSR (changes near noise level). Since the inference-time mode is listed as a core contribution (lines 29–31), this weak evidence is a significant gap.

- **FeMaSR + LDP degrades on multiple real-world metrics, contradicting the "consistently improves" claim.** On DPED, FeMaSR + LDP drops MANIQA by 12.6% (0.3102→0.2710) and MUSIQ by 10.3% (49.14→44.07). On RealSRSet, CLIPIQA drops 17.3% (0.6874→0.5683) and NIQE worsens (5.236→5.952). The paper's statement that LDP "consistently improves the performance of existing blind SR models across almost all datasets and metrics" (line 240) is inaccurate for FeMaSR on real-world benchmarks. While the paper offers an explanation (GAN artifact suppression lowering no-reference metrics), this does not change the fact that the quantitative data contradicts the unqualified claim.

### Minor

- **Table 4 contains an inconsistent arrow annotation for MANIQA** (RealSR: ↓, but DPED and RealSRSet: ↑). Since MANIQA is standardly higher-is-better, the ↓ on RealSR is likely a typo, but it undermines the reliability of the table's presentation.

- **The degradation-modeling evaluation (Tables 1–2) compares LDP against DRN, which the paper itself acknowledges "handles only bicubic downsampling" (line 45).** Using a method that was never designed for non-bicubic degradations as a primary baseline on noise, blur, JPEG, and hybrid scenarios is not a stringent test. A more informative comparison would include methods designed for multi-degradation settings or a simple "downsample SR by the ground-truth degradation" baseline.

- **Several design choices lack ablation or justification:** (a) The $s^2$ factor in Eq. 4 for computing $y_{hf}$ (why $s^2$ rather than $s$?) is not explained, and the motivation section uses $s^l$ (line 76) inconsistently. (b) The noise timestep range [500, 1000] (line 158) is justified only as "to align the noisy HR and LR features" with no ablation showing sensitivity to this choice. (c) The Degradation Prompt $P_D$ is introduced as a learned embedding but never ablated to verify whether it meaningfully captures degradation information beyond being a learned constant.

### Trivial
None.

## Nice-to-Haves

- **Add a fine-tuning control:** Fine-tune each baseline on the same BSRGAN/DF2K data without the LDP loss and report these as the proper baselines for Table 3. This is the single highest-leverage improvement for the paper.

- **Add variance reporting** (e.g., 3 random seeds) for the fine-tuning experiments, especially for small-magnitude improvements (e.g., MambaIR Down PSNR +0.05 dB).

- **Direct experimental comparison against Lway (Chen et al., 2024)** — cited as the method LDP follows for training (line 130) — would strengthen the positioning.

- **Ablate the patch-dependent noise** (vs. global noise) and **analyze what the denoiser learns** (e.g., visualize the learned blur kernels).

## Removed Points

- *"DR2 connection is decorative"* — The reviewer claimed the DR2 property is not meaningfully used. In fact, the paper uses the DR2 alignment insight (Section 3.1, line 59) to motivate why denoising noisy HR features is equivalent to denoising noisy LR features, which is the theoretical basis for the DAE framework. This is a valid motivational link, not decorative.

- *"Both values bolded in some cells (Table 4)"* — Likely a PDF-extraction artifact; not attributable to the authors.

- *"No analysis of what the denoiser actually learns"* — While useful, this is a nice-to-have analysis, not a weakness.

- *"Missing comparison against more recent degradation models (e.g., Lway, 2024)"* — Lway is cited but its approach (test-time adaptation with large models) differs in use case from LDP (lightweight plug-in). A comparison would be welcome but the omission is not a flaw.

- *"The paper should add the baseline of downsampling SR with the actual degradation"* — This is a reasonable suggestion but the paper's evaluation (Tables 1–2) compares multiple methods on the same task; the suggested baseline would not invalidate the relative comparisons shown.

- *"No variance/statistical significance reported"* — Single-run evaluation is standard practice in this benchmark setting. While variance reporting would strengthen the paper, its absence is not a weakness unique to this submission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the fine-tuning confound** by adding a "fine-tuned without LDP" control for each baseline in Table 3. If LDP still shows consistent gains over this control, the core claim would be supported.
2. **Honestly characterize the inference-mode results:** either add evidence that LDP improves LDM and produces meaningful (not near-zero) changes for ResShift/UPSR, or explicitly limit the claim to the fine-tuning mode and treat the inference mode as preliminary.
3. **Fix the MANIQA arrow annotation** in Table 4 for consistency.
4. **Ablate or justify** the $s^2$ factor in Eq. 4, the [500, 1000] timestep range, and the Degradation Prompt $P_D$.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>