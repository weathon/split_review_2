## Summary

This paper proposes a framework to enhance 3T BOLD fMRI data to approximate 7T quality, enabling improved retinotopic decoding. The method maps cortical surfaces to 2D parametric disks via conformal mapping and then applies an unpaired Brain Disk Schrödinger Bridge (BDSB) diffusion model to translate low-resolution 3T fMRI signals toward the distribution of high-resolution 7T signals. The approach is evaluated on synthetic, cross-dataset, and paired real-data experiments, showing improvements in signal-to-noise ratio, structural similarity, and downstream population receptive field (pRF) analysis compared to several baselines.

## Strengths

- **Addresses an important and practical problem:** Enhancing widely available 3T fMRI data using scarce 7T data has clear value for the neuroscience and BCI communities.
- **Novel combination of techniques:** The use of conformal mapping to bring brain surfaces from different subjects and datasets into a common 2D domain, followed by a Schrödinger Bridge for unpaired image translation, is a creative and well-motivated design.
- **Comprehensive evaluation:** The paper tests the method on three distinct public datasets (synthetic, cross-dataset real, and paired TDM) using multiple metrics (SSIM, PSNR, FID) and downstream pRF decoding (R²), with comparisons against five baselines.
- **Ablation study clarifies contributions:** The ablation study (Table 3) convincingly demonstrates the importance of conformal mapping over simpler slicing/harmonic mapping and the value of the proposed regularization terms.

## Weaknesses

### Major

1. **Missing ground-truth comparison in synthetic experiment:** The synthetic experiment has a known ground truth (original 7T fMRI), yet Table 2 does not report the average R² of the ground truth. Without this, it is impossible to assess the claim that the enhanced data is “comparable to 7T quality”—the table only compares raw LQ and enhanced R². The paper should include the ground truth R² for a direct and quantitative validation of the core claim.
2. **Cross-dataset experiment lacks ground truth:** In the cross-dataset real experiment (3T NOD → 7T NSD), there is no ground truth 7T data for the test subjects, so the evaluation relies entirely on FID and self-consistent pRF R² improvement. While this demonstrates that the enhanced data leads to better pRF fits, it does not verify that the outputs actually match the distribution of true 7T scans. The claim of “approximating 7T quality” is therefore partially supported.
3. **TDM experiment is very limited:** The paired TDM experiment involves only two subjects and a single eccentricity session each, which severely limits statistical power and generalizability. The results here are also weaker (SSIM is not the best), and the small sample size makes it difficult to draw robust conclusions.

### Minor

- **Novelty is somewhat incremental:** The BDSB framework is adapted from existing Schrödinger Bridge models (Kim et al. 2023; Dong et al. 2024) and applied to a new domain with the addition of conformal mapping. While the application is novel, the core technical contribution beyond the application is limited.
- **Baselines are general-purpose 2D models:** The comparison baselines (CycleGAN, OTT-GAN, etc.) are generic image translation methods not specialized for fMRI data. A baseline that directly operates on surface data or uses 3D fMRI-specific architecture would strengthen the evaluation.
- **Potential overclaim on being “first”**: The paper states it is “the first approach to improve fMRI SNR and retinotopic map quality using unpaired learning.” Given the existence of some related work on fMRI enhancement (e.g., deep learning super-resolution), this claim should be more carefully qualified, though it is plausible in the specific unpaired setting.

### Trivial

- None.

## Nice-to-Haves

- Include the ground truth average R² in Table 2 for the synthetic experiment, and ideally also for the cross-dataset experiment if feasible (e.g., by using a held-out subject from NSD as a simulated test).
- Provide visual comparisons of pRF parameter maps (center, size) in addition to R² to more thoroughly evaluate the quality of enhancement for downstream decoding.
- Consider including a baseline that performs super-resolution directly on the cortical surface or uses a 3D generative model to further demonstrate the advantage of the proposed pipeline.

## Novel Insights

The key insight is that mapping 3T and 7T fMRI data from different subjects and datasets onto a shared 2D parameterized brain disk via conformal mapping enables effective unpaired translation using a Schrödinger Bridge. The work underscores that preserving cortical geometry through the mapping—rather than treating the data as generic images—is critical for maintaining functional interpretability in downstream decoding tasks like pRF modeling. This integration of surface-based neuroimaging preprocessing with modern generative models is a useful contribution.

## Suggestions

- Report the average R² of the ground truth 7T data in the synthetic experiment to enable direct comparison with the enhanced results.
- Add a discussion or a figure showing the distribution of R² values for the enhanced, LQ, and ground truth data (e.g., box plots) to give a clearer picture of the improvement.
- If possible, apply the method to a larger paired dataset (even if synthetic or from a different modality) to further demonstrate generalizability.

## Score and Decision

The paper tackles a relevant problem and combines conformal mapping with a Schrödinger Bridge in a novel way. However, the most critical claim—that the enhanced 3T data is comparable to 7T quality—is not sufficiently supported because the ground truth R² is omitted from the synthetic experiment results. This major weakness, together with the limited paired-data validation, prevents the paper from fully substantiating its conclusions. The work is methodologically sound and shows clear improvements over baselines, but the missing evidence weakens the overall contribution.

Score: 4

Decision: Reject

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>