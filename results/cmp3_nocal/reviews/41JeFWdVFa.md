## Summary

This paper proposes LDP (Lightweight Denoising Plugin), a 642k-parameter denoising autoencoder module that improves the generalization of single-image super-resolution (SISR) models to unseen degradations. LDP works in two modes: as a training-time auxiliary loss enforcing LR cycle consistency, and as an inference-time posterior-sampling correction for diffusion models. It conditions degradation modeling on LR high-frequency components and uses patch-dependent noise injection within a DAE framework. Experiments cover 8 base SR architectures across synthetic and real-world benchmarks.

## Strengths

1. **Clean dual-mode design (Sections 3.2–3.3).** LDP operates as both a training-time loss and an inference-time posterior-sampling correction. A single lightweight module (642k parameters) serving two purposes is practically useful for deployment.

2. **Broad model coverage (Tables 3–5).** The paper evaluates LDP across 8 base methods spanning CNN, GAN, diffusion, transformer, and state-space architectures (FeMaSR, StableSR, LDM, ResShift, UPSR, SwinIR, MambaIR). This breadth makes the results informative even where gains are modest.

3. **Explicit conditioning on LR high-frequency components (Section 3.2).** Using \(y_{hf}\) (the residual after \(s^2\)-fold down/upsampling) as a degradation-discriminating condition is a reasonable choice that avoids shortcut learning. The three design criteria motivating this choice are clearly stated.

## Weaknesses

### Fatal
None.

### Major

1. **Missing control condition confounds the main experimental comparison (Table 3).** The paper fine-tunes pre-trained SR models on DF2K using BSRGAN degradations *with* LDP as an auxiliary loss, but compares against the original pre-trained checkpoints (not fine-tuned). As stated in Section 4.1: "We fine-tune existing SR models on the DF2K dataset... using BSRGAN degradation patterns, *with our LDP employed as an auxiliary loss*." No "fine-tuned on the same data without LDP" baseline exists anywhere in the paper. Since BSRGAN-style data augmentation alone is known to improve generalization to unseen degradations (Zhang et al., 2021a), the observed gains (e.g., StableSR +2.16 PSNR on Hybrid) cannot be attributed specifically to LDP's cycle-consistency mechanism. The ablation in Table 6 uses the original pre-trained SwinIR as baseline (23.52 PSNR, matching Table 3 Hybrid), not a fine-tuned-only version, so the same confound persists. This is the single most significant weakness: the paper's central claim is not supported by a controlled experiment.

2. **Claim of "consistent improvement" is contradicted by the paper's own results (Tables 4–5).** The abstract and contributions state that LDP "consistently improves all baseline models." However, Table 4 contains numerous regressions on real-world benchmarks:
   - FeMaSR: CLIPIQA drops from 0.5645→0.4482 (−21%) on RealSR, MUSIQ drops 49.14→44.07 on DPED, CLIPIQA drops 0.6874→0.5683 on RealSRSet
   - StableSR: CLIPIQA drops 0.3968→0.3363 on DPED
   - SwinIR and MambaIR: NIQE worsens on RealSR
   
   Table 5 is even more problematic: LDM+LDP regresses on *all 5 metrics* on RealSR and on 3 of 5 on DPED, with no explanation offered. The paper's speculation about FeMaSR's CLIPIQA drop ("metrics may favor visually striking but structurally inaccurate results") does not explain why four different metrics simultaneously disagree, nor why other models do not show the same pattern. The actual result is that LDP helps some models on some metrics while hurting others — this should be reported honestly rather than as "consistent improvement."

3. **No experimental comparison against the closest prior work (Lway).** The paper adopts Lway's (Chen et al., 2024) DWT-based high-frequency supervision loss directly (Section 3.3: "Following Lway...") and cites Lway as the most relevant self-supervised approach (Section 2.1–2.2). Yet no experiment compares LDP-augmented training against Lway-based fine-tuning, or even against training the base model with BSRGAN data augmentation alone (the control from Issue 1). Without these comparisons, the paper cannot substantiate its claim that LDP's approach is *better* than existing generalization techniques — only that it is *compatible* with various architectures. This is a significant gap for a methods paper.

### Minor

4. **High-noise-level alignment is invoked but not validated.** LDP samples timesteps from [500, 1000] (Section 4.1) "to align the noisy HR and LR features." At these noise levels, both HR and LR features are dominated by Gaussian noise — their "alignment" is trivial (both nearly isotropic). The paper does not ablate this design choice (e.g., using lower noise levels or removing noise injection altogether) to demonstrate that the diffusion-alignment property meaningfully contributes to degradation modeling rather than being incidental within the DAE framework.

5. **No error bars or statistical testing.** Given that many gains are small (e.g., MambaIR +0.05 PSNR on Down, +0.23 on Noise), single-run results are unconvincing. Standard practice in SR would be to report at least 3 runs with standard deviation, or justify why a single run is sufficient.

6. **No inference-time overhead measurement.** The paper emphasizes that LDP is "lightweight" (642k parameters) but does not report inference-time FLOPs, latency, or memory overhead in posterior-sampling mode, where gradient computation through LDP at each denoising step could be substantial.

7. **Patch-dependent noise schedule is not empirically motivated.** Section 3.2 assigns each 16×16 patch a random timestep to "better capture spatially varying corruption." No experiment demonstrates that real-world degradations vary spatially in a way that per-patch random noise levels actually capture, nor does an ablation compare patch-dependent noise against uniform noise.

8. **"Unseen" degradations are drawn from the same BSRGAN family used in training.** Synthetic test sets are generated with BSRGAN/Real-ESRGAN-style degradations, which are in-distribution relative to the training data. The generalization claim is therefore about unseen *combinations* of known degradation types, not genuinely out-of-distribution scenarios. This tempers the significance of the claimed generalization improvement.

### Trivial
- Notation inconsistency: Section 3.1 uses \(s^l\) while Section 3.2 uses \(s^2\) for the down/upsampling factor in the \(y_{hf}\) computation (lines 76 vs. 90–92).

## Nice-to-Haves
- An ablation isolating the core DAE design choices (patch-dependent vs. uniform noise, the DAE framework vs. a direct HR→LR regression network, \(y_{hf}\) vs. other conditioning signals) would be more informative than the current loss-component toggling in Table 6.
- Comparing LDP's degradation module against a simple learned downsampler (e.g., a CNN trained end-to-end without the DAE framework) would help isolate what the DAE architecture adds.

## Removed Points
- *"Comparison in Tables 1–2 is misleadingly staged"* — The paper acknowledges DRN's design limitations (Section 2.2: "DRN handles only bicubic downsampling") and the comparison serves to illustrate LDP's architectural advantage. This is informative, not misleading.
- *"Table 6 column headers are corrupted"* — Parser artifact, not author error.
- *"Contribution list over-extends framing"* — Overly pedantic; the dual-mode description is sufficiently accurate.
- *"Patch-dependent noise is unmotivated"* and *"s^2 vs s notation"* — These specific criticisms are partially addressed by the paper's design rationale or are minor notation issues; the substantive point about missing ablation is covered in Minor Weakness 7.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's main structural insight — that the missing fine-tuning-only control prevents clean attribution of results — is the key observation. The remaining points largely restate verification issues that follow from reading the tables carefully.

## Suggestions

1. **Add the missing control experiment.** Fine-tune each base model on the same DF2K+BSRGAN data *without* the LDP loss, and compare against fine-tuning *with* LDP. This directly addresses the attribution confound in Table 3.
2. **Report results honestly by model/metric.** Replace blanket "consistent improvement" claims with a transparent breakdown of which models, metrics, and degradation types benefit and which regress. Provide evidence-based explanations for regressions rather than post-hoc speculation.
3. **Include a comparison against Lway** under the same experimental conditions. Since LDP adopts Lway's DWT loss, this is the most natural and informative baseline.
4. **Report error bars** (at least 3 runs with std) for the main results, especially where gains are small.
5. **Include throughput/latency numbers** for posterior sampling to support the "lightweight" claim.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>