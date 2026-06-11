## Summary
This paper proposes BDSB (Brain Disk Schrödinger Bridge), a framework for enhancing 3T BOLD fMRI signals to approximate 7T quality for visual retinotopic decoding. The key idea is to map 3D cortical surfaces into a shared 2D parametric domain via conformal mapping (producing "Brain Disks"), then apply an unpaired Schrödinger Bridge diffusion model to translate 3T-quality brain disks toward the distribution of 7T data. The enhanced fMRI signals are then re-sampled back to the cortical surface for downstream pRF analysis.

The method is evaluated on three experimental settings: (1) synthetic data with known ground truth (down-sampled NSD 7T data), (2) cross-dataset real data (3T NOD → 7T NSD), and (3) paired TDM real data (3T/7T from the same subjects). Quantitative comparisons against five baselines (Cycle-GAN, OTT-GAN, OTE-GAN, SCR-Net, fast-DDPM) show BDSB achieving competitive or superior results on SSIM, PSNR, FID, and downstream pRF $R^2$ metrics. The ablation study confirms that conformal mapping outperforms direct slicing and harmonic mapping, and that the proposed regularization terms (PatchNCE and BD-SSIM) improve structural fidelity at a cost in distribution-level quality.

The paper addresses a practically important problem—making 3T fMRI more useful for retinotopic mapping without requiring costly 7T scanning—and demonstrates a technically sound pipeline combining conformal geometry with Schrödinger Bridge diffusion. However, several weaknesses in evidence presentation, claim scoping, and evaluation validity temper the overall contribution.

**Contribution Claims (C1-C3):**
- **C1:** A robust fMRI enhancement pipeline with BDSB model applied across subjects/datasets.
- **C2:** First approach to improve fMRI SNR and retinotopic map quality using unpaired learning across public datasets.
- **C3:** Validation on real and synthetic experiments demonstrating improved downstream neural decoding performance.

**Novelty Status (Retrieval-Disabled Mode):** Due to the unavailability of external paper search in this run, novelty verification for C2 (the "first approach" claim) is deferred for manual literature verification. The authors should independently verify that no prior work has applied unpaired generative models for fMRI-to-fMRI enhancement with retinotopic evaluation and adjust the claim scope accordingly.

## Strengths
1. **Addresses an important practical problem.** The scarcity of 7T fMRI scanners limits retinotopic mapping research. Developing methods to enhance 3T data toward 7T-like quality has genuine scientific and clinical value, potentially democratizing access to high-quality functional neuroimaging.

2. **Technically well-motivated pipeline design.** The combination of conformal mapping (to handle cross-subject cortical geometry variation) with a Schrödinger Bridge diffusion model (to perform unpaired distribution alignment) is a sensible and novel synthesis of existing techniques. The use of a shared 2D parametric domain via brain disks is a clean way to avoid direct 3D surface-to-surface translation.

3. **Multi-setting evaluation.** The paper evaluates on three distinct experimental setups—synthetic (with ground truth), cross-dataset real (no ground truth), and paired TDM real (limited paired data)—which demonstrates awareness of the data limitations and provides complementary evidence. The inclusion of five baselines (Cycle-GAN, OTT-GAN, OTE-GAN, SCR-Net, fast-DDPM) offers a reasonable comparison landscape.

4. **Comprehensive ablation study.** Table 3 systematically decomposes the contribution of brain mapping strategy (slice vs harmonic vs conformal) and regularization components (PatchNCE, BD-SSIM). This allows readers to understand the relative importance of each design choice.

5. **Honest limitations discussion.** The "Lack of Paired Data" and "Synthetic Data" paragraphs in the Conclusion acknowledge the fundamental challenge of missing paired 3T/7T datasets and the limitations of synthetic down-sampling. This transparency strengthens the paper's scientific credibility.

## Weaknesses
### W1. Overclaiming and Imprecise Scope (Multiple Sections)

**W1a.** The Abstract states that results are "comparable to 7T quality," but the reported metrics tell a more nuanced story. On synthetic data (where ground truth is available), SSIM=0.855 (versus 1.0 for perfect match), PSNR=25.05 (typically 7T scans achieve much higher SNR), and on real TDM data SSIM=0.718 and PSNR=19.24. While these are meaningful improvements over raw 3T, they do not demonstrate equivalence to 7T quality. This overclaim weakens scientific credibility and sets unrealistic expectations.

**W1b.** The Future Work section claims the method "has the potential to set a new standard for improving 3T or 1.5T fMRI quality" and asserts broad applicability to "fMRI-based segmentation, classification, and visual reconstruction" without any supporting evidence or experiments. These statements are promotional rather than evidence-based.

**W1c.** Introduction Paragraph 3 makes the imprecise claim that HCP/NSD 7T resolution "is not concentrated in the occipital lobe, where retinotopic maps are studied primarily." HCP 7T provides whole-brain coverage at 1.6mm isotropic, including excellent occipital coverage. The actual limitation is more nuanced (e.g., pulse sequence optimization, coil design, or stimulus protocols) and should be stated more precisely.

**Action:** Replace all "comparable to 7T quality" wording with bounded claims (e.g., "substantially narrows the gap" or "consistently improves across metrics"). Remove promotional language from Future Work and replace with testable hypotheses. Revise the occipital lobe resolution claim with a precise justification.

### W2. Missing Variance and Statistical Reliability in Table 2

All metrics in Table 2 are reported as single point estimates without standard deviations, confidence intervals, or significance tests. Given the small test sets (2 subjects for synthetic, 2 for cross-dataset, 2 for TDM), subject-specific variability could substantially influence the reported rankings. For instance, on the TDM Real experiment, the proposed method achieves SSIM=0.718 versus OTT-GAN's 0.727 — a difference that is almost certainly within measurement noise, yet no uncertainty is reported. Furthermore, the text states "Across all real and synthetic experiments, our pipeline achieves the best performance," which is factually contradicted by the TDM SSIM result where OTT-GAN scores higher (0.727 vs 0.718).

**Action:** Report all metrics as mean ± std over multiple runs or bootstrap resampling. Add a statistical significance test (e.g., paired Wilcoxon) for the primary comparisons. Correct the sweeping "best performance" claim to acknowledge that OTT-GAN achieves marginally higher SSIM on TDM.

### W3. pRF $R^2$ as Evaluation Metric — Risk of Circularity

The pRF decoding evaluation (Sec 2.4, Eq. 6-7) estimates pRF parameters from the enhanced fMRI signals and then computes $R^2$ as a goodness-of-fit of the same model to the same signal. This is an internal consistency check, not an external validation. If the enhancement model introduces systematic structure that the pRF model can fit (e.g., by sharpening temporal dynamics), $R^2$ may increase even if the enhanced signal does not better represent true neural population responses. This risk is especially acute for the cross-dataset experiment (where no ground truth 7T data exists) and for the TDM experiment (where the paired ground truth is available but $R^2$ is not reported — only image similarity metrics).

The synthetic experiment partially addresses this by comparing $R^2$ between enhanced and ground-truth signals, but a direct parameter comparison (estimated vs ground-truth pRF centers and sizes) would be a stronger validation. The scatter plots in Fig. 7(b) show this for top-40 vertices but not comprehensively.

**Action:** (Must) Add a direct pRF parameter comparison (center $c_v$ and size $\sigma_v$ error against ground truth) for the synthetic experiment. (Must) Report $R^2$ on TDM real data where ground truth is available, to complement the image similarity metrics. (Nice-to-have) For cross-dataset experiments, add a control analysis showing that $R^2$ improvements are not simply from increased signal variance in the enhanced data.

### W4. Ablation Study Reveals Unacknowledged Trade-offs

Table 3 shows a clear and important conflict: adding PatchNCE and BD-SSIM regularization improves SSIM (0.849→0.858→0.855) and PSNR (24.26→24.88→25.05) but substantially *worsens* FID (34.23→42.64→42.88). A 25% relative worsening in FID is a meaningful distribution-level quality degradation that the text completely ignores, instead describing the regularization as providing "modest gains" and playing a "critical role." Furthermore, the ablation does not include a harmonic mapping + regularization condition. Since harmonic mapping alone achieves FID=35.56 (better than any conformal configuration), adding regularization to harmonic mapping could potentially outperform the full conformal pipeline, but this condition is missing.

**Action:** (Must) Explicitly acknowledge the FID-regulariation trade-off in the Ablation Study text. (Must) Add the harmonic + regularization ablation condition. (Nice-to-have) Provide a Pareto-style analysis showing which configuration is optimal under different priority regimes (image quality vs distributional fidelity vs downstream performance).

### W5. Cross-Subject Alignment Not Quantified

The conformal mapping framework is central to the pipeline, ensuring that 3T and 7T brain disks from different subjects are "spatially consistent." However, the precision of this cross-subject alignment is never quantified. Registration errors between subjects could introduce spatial mismatch that propagates into the unpaired Schrödinger Bridge training. Without measuring vertex displacement or overlap metrics, readers cannot assess whether residual misalignment is small enough to be negligible for the translation task.

**Action:** Report the mean vertex displacement between corresponding fsaverage vertices across subject pairs in the ROI. Show that the displacement is substantially smaller than the receptive field size of pRF estimates. Alternatively, provide a sensitivity analysis showing that small perturbations in the alignment do not materially change enhancement results.

### W6. "First Approach" Claim Needs Verification

Contribution (b) states: "To our knowledge, it's the first approach to improve fMRI SNR and retinotopic map quality using unpaired learning across public datasets." While the hedging "to our knowledge" is appropriate, the claim requires explicit literature verification against prior fMRI super-resolution, denoising, and cross-field-strength translation methods. Given the popularity of unpaired image translation (CycleGAN, etc.) and their known application to medical imaging, the novelty claim would be strengthened by a brief discussion of why prior works do not cover this specific combination.

**Note:** External literature search was unavailable in this review run, so this claim could not be independently verified. The authors should add a thorough related-work comparison to substantiate the "first" claim.

### W7. Introduction Narrative Structure

The introduction has an imbalanced structure: Paragraph 1 opens with BCI applications (tangential to the paper's core focus on fMRI enhancement), Paragraph 5 is an overly dense literature survey with 25+ citations packed into a single paragraph, and the key gap ("limited focus on enhancing fMRI signals for downstream decoding") is buried near the end of that paragraph. The narrative would benefit from a clearer arc: importance of high-quality fMRI for retinotopy → limited access to 7T → gap in existing enhancement methods → proposed approach and contributions.

**Action:** Restructure introduction paragraphs as suggested in the per-paragraph annotation guidance.

### W8. Missing Implementation Details

Several critical details needed for reproducibility are relegated to the appendix (B.1), which was not available for review in this run. From the main text, the following are unclear: (a) the exact architectural details of the generator $q_\phi$, (b) the training hyperparameters (batch size, learning rate, number of steps $N$, optimization details), (c) how the weight parameters $\lambda_{\text{SB}}, \lambda_{\text{Reg}}$ in Eq. (5) were chosen, and (d) the specific values of $\tau$ and $\epsilon_\mu$ used. The authors should ensure the appendix contains all details necessary for independent reproduction.

### W9. Marginal Quality Gain on Real Paired Data

On the TDM Real experiment (the only setting with true paired 3T/7T data), the proposed method achieves PSNR=19.24, which is only 1.18 dB higher than the best baseline (OTE-GAN, 19.06) and only 0.06 dB higher than OTT-GAN (19.18). The SSIM is actually slightly lower than OTT-GAN (0.718 vs 0.727). While FID shows a more substantial improvement (62.09 vs 84.45), the marginal gains on the two primary image-quality metrics over existing methods are small. The authors should discuss this limitation and clarify whether the primary advantage lies in downstream task improvement rather than image quality alone.

## Score
**Final Score: 5.5/10**

The paper addresses an important practical problem with a technically well-motivated pipeline combining conformal mapping and Schrödinger Bridge diffusion. The multi-setting evaluation and ablation study demonstrate methodological rigor. However, the score is tempered by several weaknesses:

- The primary evaluation metric ($R^2$ on pRF fit) has circularity risks that are not adequately addressed, reducing confidence in the claimed improvements.
- The "best performance" claim is contradicted by the data (TT-GAN achieves higher SSIM on TDM Real), and the absence of variance estimates prevents reliable ranking.
- Overclaiming (abstract claiming "comparable to 7T quality," future work making unsupported broad applicability claims) weakens scientific credibility.
- The ablation study reveals an unacknowledged trade-off where regularization improves pixel-level metrics but substantially degrades distribution-level quality (FID).
- The cross-subject alignment precision, which is fundamental to the pipeline's validity, is not quantified.

The novelty of applying unpaired Schrödinger Bridge to cross-field-strength fMRI enhancement is promising, but the "first approach" claim requires external literature verification that was unavailable in this review run. The paper has solid technical foundations but needs tighter claim scoping, better statistical reporting, and additional validation to support its stronger assertions.