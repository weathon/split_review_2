Now I have all the information needed. Let me write the final consolidated review.

---

## Summary

This paper proposes LDP, a lightweight denoising autoencoder plug-in (642K parameters) for single-image super-resolution that improves generalization to unseen degradations. LDP models the degradation process via patch-dependent noise addition and a convolutional denoiser, enforcing cycle consistency between SR outputs and LR inputs. It operates in two modes: as a training-time loss function and as an inference-time posterior sampling correction.

## Strengths

- **Training-time fine-tuning results (Table 3) are solid.** Across four architectures (FeMaSR, StableSR, SwinIR, MambaIR) and five synthetic degradation types, the +LDP variant consistently improves all metrics. StableSR gains are particularly notable (e.g., +2.16 PSNR, +0.1541 SSIM, -0.1266 LPIPS on Hybrid). These results convincingly demonstrate that the cycle-consistency loss and frequency-domain losses act as effective regularizers during fine-tuning.

- **Lightweight design with practical value.** At 642K parameters and ~16 hours training on a single A6000, LDP is genuinely lightweight. The plug-in design that can be dropped into arbitrary SR models during fine-tuning is a clear and well-communicated value proposition.

- **Clear architectural description.** The method is described with sufficient detail (patch-dependent noise scheduling with diffusion-style noise schedule, Condition Residual Blocks with Adaptive Layer Normalization, degradation prompts, DWT-based loss) that reproduction should be feasible.

- **Informative ablation study (Tables 6, 7).** The ablation of loss components and the τ hyperparameter is informative — LDPV7 (full loss) outperforms all partial variants, and the τ sweep (0.1–100) shows the method is not critically sensitive to this parameter.

## Weaknesses

### Major

- **Real-world fine-tuning results (Table 4) show systematic regressions that the paper does not adequately explain, and the claim of "consistently improves" is overstated.** FeMaSR+LDP degrades on 4 of 5 metrics on DPED (MANIQA −0.0393, MUSIQ −5.07, QAlign −0.167, NIQE +0.659) and on 4 of 5 metrics on RealSRSet. The paper's explanation that some metrics "favor visually striking but structurally inaccurate results" is post-hoc and could rationalize any negative outcome without a principled analysis. While StableSR, SwinIR, and MambaIR fare better, the overall pattern across Table 4 is better described as "often improves, sometimes degrades" than the claimed "consistently improves." The paper does not analyze *when* and *why* LDP helps or hurts.

- **The inference-time posterior sampling mode (Table 5) is claimed to show "improvements across nearly all metrics on most datasets," but the data do not support this.** LDM+LDP degrades on 3 of 5 metrics on RealSR; ResShift+LDP shows essentially no meaningful change across all datasets (differences on the order of 0.0001–0.0004); UPSR+LDP is mixed. Of the four models tested, only StableSR+LDP shows reasonably consistent gains. This mode is presented as a core contribution but the evidence is insufficient to support the paper's claims about it.

### Minor

- **No error bars, confidence intervals, or statistical significance measures are reported.** Several improvements are small (e.g., MambaIR +0.05 dB PSNR on the Down task), and synthetic test sets are generated using stochastic BSRGAN degradations. Without variance estimates, readers cannot assess whether differences are meaningful or within the noise of the evaluation.

- **No inference-time computational cost reported.** The paper emphasizes LDP's lightweight design (642K parameters) but never reports actual inference FLOPs or runtime overhead, which is essential for the practical deployment use case the paper targets.

- **The arrow directions for MANIQA and MUSIQ are inconsistent** between Table 4 (↑ for most entries) and Table 5 (↓), making it harder to interpret results correctly across tables.

### Trivial

None.

## Nice-to-Haves

- A direct quantitative comparison with Lway (Chen et al., 2024), cited in the paper and the source of the DWT-based loss, would strengthen the paper. Lway addresses the same problem, and without a comparison it is unclear whether LDP offers advantages beyond being smaller.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"ALL five metrics get worse for LDM+LDP on RealSR"** — This claim by the initial reviewer is factually incorrect when checked against Table 5's own arrow conventions (both MANIQA↓ and MUSIQ↓ show improvements for LDM on RealSR according to the table's arrow directions). This error inflated the perceived severity of the inference-time issue.
- **"DRN/DualSR comparison is staged against methods never designed for the task"** — The paper's stated purpose of Tables 1–2 is to demonstrate that LDP does not degenerate into simple downsampling (Table 2), not to claim multi-degradation superiority. The paper explicitly explains DRN's bicubic-only limitation, making the comparison meaningful for its stated purpose.
- **Criticisms about missing appendix content** — The parser strips appendix sections from all papers; they exist in the original submission.
- **"The connection to diffusion models is strained"** — This is a theoretical motivation observation rather than an empirically verifiable flaw and does not affect the validity of the experimental results.
- **Formatting and reproducibility nitpicks** — Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Tone down the claims to match the evidence.** Either strengthen the inference-time mode with a better experimental design or honestly characterize it as not yet effective and focus the paper on the training-time mode. Qualify the "consistently improves" claim for real-world data to reflect that improvements are model-dependent.
2. **Analyze the regression cases in Table 4 systematically** rather than using post-hoc rationalization. Determine whether LDP consistently harms certain types of degradations or images, and report this transparently.
3. **Add error bars or multiple-run statistics**, especially for small-magnitude improvements.
4. **Report inference-time FLOPs and runtime overhead** of the LDP module.
5. **Add a direct comparison to Lway (2024)**, or at minimum quantify the claimed "significant computational overhead" of Lway by reporting its parameter count and runtime.
6. **Fix the inconsistent arrow directions** between Table 4 (MANIQA↑, MUSIQ↑) and Table 5 (MANIQA↓, MUSIQ↓).

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>