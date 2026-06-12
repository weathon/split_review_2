## Summary
This paper proposes BDSB, a framework that enhances 3T fMRI data toward 7T quality using unpaired learning. The method maps cortical surfaces to 2D parametric "brain disks" via conformal mapping, then applies a Schrödinger Bridge diffusion model to translate low-quality (3T) brain disk distributions to high-quality (7T) distributions, evaluated through downstream population receptive field (pRF) retinotopic decoding on three real fMRI datasets and synthetic data.

## Strengths
- **Important and well-motivated research question.** Enhancing widely available 3T fMRI to approximate scarce 7T quality is practically significant for neuroscience and BCIs. The scarcity of 7T scanners makes this a high-impact problem.
- **Creative pipeline design.** The combination of conformal mapping for cross-subject/domain alignment and Schrödinger Bridge diffusion for unpaired translation is technically sound and novel in this application context. The conformal mapping preserves geometric properties of the cortical surface while enabling 2D processing.
- **Thorough experimental design.** The paper evaluates on three distinct real datasets (NSD, NOD, TDM) plus synthetic data, covering paired, cross-dataset, and simulated settings. Five baseline methods are compared, and an ablation study isolates the contribution of each component (mapping strategy, regularization terms).
- **Downstream task evaluation.** Rather than only reporting image-level metrics, the paper validates improvements through pRF decoding, including R² values and receptive center stability across random stimulus intervals (Fig. 7b), which directly demonstrates practical utility.

## Weaknesses
### Fatal
None.

### Major
- **Missing ground-truth HQ reference metrics.** For the synthetic experiment, the paper reports raw LQ and enhanced metrics but does not report the original HQ 7T R² values. Without this reference, it is impossible to assess whether the enhancement is calibrated or potentially hallucinating signals beyond 7T quality. Figure 7(a) shows scatter plots but no summary HQ R² is provided in Table 2.
- **No statistical significance testing or confidence intervals.** All results are point estimates. For pRF R² values that vary across hundreds or thousands of vertices, the lack of error bars, standard deviations, or statistical tests makes it difficult to assess whether improvements (e.g., R² from 20.26 to 25.91) are statistically reliable or driven by outliers.
- **Hallucination vs. genuine enhancement is unaddressed.** In a scientific context where enhanced signals will be used for brain function inference, it is critical to establish that the model denoises rather than fabricates plausible-looking neural signals. The paper provides no analysis of spatial specificity, correlation with anatomical priors, or tests that would distinguish genuine signal recovery from hallucination.
- **Unfair baseline for fast-DDPM.** In the cross-dataset real experiment, fast-DDPM is marked "No pair data" and excluded, while other GAN-based baselines are included. This suggests an implementation asymmetry rather than a methodological limitation, weakening the comparison.

### Minor
- **Small test sets.** Only 2 NOD subjects and 2 NSD subjects are reserved for testing in cross-dataset and synthetic experiments respectively. The TDM experiment uses a single session per subject with a 3/6 run train/test split. These small evaluation sets limit generalizability claims.
- **Cross-dataset evaluation lacks ground truth.** For the cross-dataset real experiment (the primary intended use case), only FID and R² are reported with no ground-truth comparison. FID reliability with limited samples is also not discussed.
- **TDM results show OTT-GAN outperforming BDSB on SSIM (0.727 vs 0.718).** While BDSB wins on PSNR and FID, the mixed results on this paired dataset reduce the strength of the claim that the method consistently outperforms all baselines.
- **Stimuli mismatch across datasets.** NSD uses natural images and pRF-fLOC stimuli while NOD uses different visual stimuli, yet these are treated as comparable LQ/HQ pairs. The effect of stimuli differences on the learned translation is not analyzed.

### Trivial
None.

## Nice-to-Haves
- Report the HQ 7T R² values in Table 2 for the synthetic experiment as a ceiling reference
- Add vertex-wise R² distribution plots (e.g., histograms or violin plots) rather than only mean R²
- Include a qualitative or quantitative test for signal hallucination (e.g., correlating enhanced signals with anatomical boundaries, or testing in regions expected to have no visual response)
- Discuss the choice of the number of diffusion steps N and its effect on enhancement quality

## Novel Insights
The paper's core insight—that conformal parameterization of cortical surfaces enables cross-subject/cross-dataset fMRI translation in a shared 2D domain—is genuinely valuable and could enable other cross-subject neuroimaging analyses beyond retinotopy. The observation that structural regularization (BD-SSIM) is critical for preserving brain disk geometry during enhancement (Table 3 ablation) highlights an important consideration for any surface-based neuroimaging translation method: unconstrained distribution matching can distort cortical topology even when it improves pixel-level metrics.

## Suggestions
- Add HQ ground truth R² to Table 2 and include vertex-wise R² distribution comparisons
- Include error bars or confidence intervals on all reported metrics, computed across vertices or test subjects
- Add a section analyzing whether the model introduces artifacts, e.g., by examining enhanced signals in non-visual cortical regions where no visual response is expected
- Clarify why fast-DDPM cannot be applied in the cross-dataset real setting and ensure all baselines are evaluated on equal footing

## Score and Decision
The paper addresses a valuable research question with a creative approach and shows promising results across multiple experimental settings. However, the missing ground-truth reference metrics, absence of statistical testing, and unaddressed hallucination concern represent significant gaps for a paper whose practical value depends on the reliability of the enhanced signals for scientific inference. The improvements over baselines are meaningful but not uniformly decisive, and the evaluation would benefit from substantially more rigor.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject