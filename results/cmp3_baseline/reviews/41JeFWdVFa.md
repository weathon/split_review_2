## Summary
The paper proposes LDP, a lightweight denoising autoencoder plug-in for single-image super-resolution (SISR). LDP models the SR degradation process within a DAE framework, using patch-dependent noise and LR high-frequency components as a condition. It can be applied as a training-time loss to enforce cyclic consistency (improving generalization) or as an inference-time posterior sampling correction for diffusion models. Experiments on multiple SR architectures (SwinIR, MambaIR, FeMaSR, StableSR, etc.) across synthetic and real-world benchmarks show consistent, sometimes substantial, improvements.

## Strengths
- **Practical and timely problem**: Improving SR model generalization to unseen, complex degradations is a key challenge for real-world deployment. The paper directly addresses this.
- **Lightweight and model-agnostic design**: LDP has only 642k parameters and can be integrated with any SR model without architectural changes, adding minimal overhead during fine-tuning or inference.
- **Comprehensive and well-conducted experiments**: The evaluation spans four SR architectures, five degradation types, multiple datasets (synthetic + real), and both reference and no-reference metrics. The ablation studies (loss components, \(\tau\) weight) are informative and justify design choices.
- **Consistent improvements across settings**: LDP boosts performance on nearly all metrics and degradation types, with especially notable gains on challenging degradations (e.g., StableSR +2.16 dB on Hybrid). The qualitative results show visible artifact reduction.

## Weaknesses
### Fatal
None.

### Major
- **Limited novelty**: The core idea of using a degradation model to enforce LR cycle consistency for SR has been explored in prior works (DRN, DualSR, Lway). LDP’s innovation—a DAE with patch-dependent noise and LR high-frequency conditioning—is an incremental combination of existing concepts (diffusion noise scheduling, degradation prediction from LR features). The paper does not clearly articulate a new principle that distinguishes it from the broader cycle-consistency line.
- **Overstated “plug-in” versatility**: LDP is presented as a plug-in that operates in two modes, but for non-diffusion models (SwinIR, MambaIR) it is only used during fine‑tuning, not at inference. For diffusion models, the inference‑time use requires posterior sampling, which is not a standard inference pipeline. The claim of a seamless plug‑and‑play module is therefore qualified.
- **Modest gains on strong baselines**: While LDP consistently improves results, the absolute gains on the best-performing models (e.g., MambaIR: +0.05 dB on Down, +0.23 dB on Noise; SwinIR: +0.42 dB on Down) are small. The practical impact for already strong models may be limited, and the paper does not discuss the practical significance of such gains.
- **Missing comparisons with alternative generalization methods**: The fine‑tuning experiments only compare each baseline with and without LDP. There are no comparisons against other approaches that improve generalization, such as test‑time adaptation (ZSSR, CorrectFilter, Lway itself), advanced data augmentation (BSRGAN-style training), or self‑supervised fine‑tuning. This makes it difficult to gauge where LDP stands relative to the state of the art in generalization.

### Minor
- **Inconsistent no-reference metrics on real‑world datasets**: For FeMaSR on RealSR, CLIPIQA and NIQE degrade despite PSNR gains. The paper attributes this to GAN artifacts being suppressed, which may lower certain metrics. While plausible, a more rigorous analysis of when and why no‑reference metrics disagree would strengthen the claim.
- **Ablation limited scope**: The ablation of \(\tau\) and loss terms is conducted only on SwinIR on the Hybrid dataset. Tests on additional architectures or degradation types would increase confidence in the hyperparameter choices.

## Nice-to-Haves
- Compare LDP with other plug‑in generalization methods (e.g., Lway, test‑time adaptation) in the same experiment setting.
- Include inference‑time results of LDP for non‑diffusion models (e.g., running LDP as a post‑processing step after SwinIR) to fully verify the “inference‑time correction” claim.
- Provide a more detailed analysis of the computational overhead of LDP during fine‑tuning (e.g., additional time vs. baseline).

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- Clarify in the abstract and introduction that LDP’s inference-time use is limited to diffusion models, and that for other SR models it serves only as a training loss.
- Add comparisons with at least one strong generalization baseline (e.g., retraining the same SR model with BSRGAN-style data augmentation, or applying Lway test‑time adaptation) to contextualize the improvements.
- Discuss the practical significance of the reported PSNR/SSIM gains, perhaps by including user studies or perceptual evaluation for cases where gains are small.

## Score and Decision
The paper presents a well‑executed, lightweight solution to an important problem, supported by extensive experiments. However, the novelty is incremental relative to prior degradation‑modeling work, and the claimed plug‑and‑play versatility is narrower than suggested. The contributions are solid enough for acceptance, but the paper does not represent a major breakthrough. 

**MY FINAL SCORE: <score>6.0</score>**  
**MY FINAL DECISION: Accept**