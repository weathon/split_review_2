## Summary

This paper proposes a pipeline to enhance 3T BOLD fMRI signals to approximate 7T quality using unpaired data. The method first maps cortical surface meshes to 2D brain disks via conformal parameterization, then applies a Schrödinger Bridge diffusion model (BDSB) to translate the low-quality brain disks to high-quality ones while preserving geometry. The enhanced signals are evaluated on synthetic data, cross-dataset real data (unpaired), and a small paired 3T/7T dataset, showing improvements in standard image quality metrics and downstream pRF decoding variance explained (R²).

## Strengths

* **Addresses an important practical problem.** Improving widespread 3T fMRI to approach 7T quality could benefit many neuroscience labs without access to ultra-high-field scanners. The paper correctly identifies this gap and proposes a plausible learning-based solution.
* **Novel combination of conformal mapping and Schrödinger Bridge for fMRI.** Mapping 3D cortical surfaces to a shared 2D parametric space before applying an unpaired diffusion model is creative and geometrically principled. The BDSB model with structural regularization is well motivated.
* **Comprehensive experimental design with three settings.** The paper attempts to validate on synthetic (with ground truth), cross-dataset real (unpaired), and the only available paired TDM dataset, covering different levels of evaluation realism.

## Weaknesses

### Fatal
None.

### Major

1. **Cross-dataset real experiment lacks ground truth and uses mismatched stimuli.** The 3T NOD and 7T NSD come from different subjects, datasets, and potentially different pRF stimulus designs. Without ground-truth 7T for the test subjects, the reported R² improvement is not evidence that the enhanced signals are more *accurate*—only that they yield higher variance explained by a pRF model, which could result from learning dataset-specific smoothness or noise characteristics. This undermines the core claim of "enhancing 3T fMRI to approximate 7T quality."

2. **Synthetic experiment uses an unrealistic degradation model.** Down-sampling from 7T to 3T resolution and adding Gaussian noise does not capture real differences in scanner hardware, pulse sequences, physiological noise, or subject motion between 3T and 7T acquisitions. The strong results on synthetic data may not transfer to real scenarios, and the paper over-relies on this setting as a validation of the method.

3. **TDM paired experiment is too limited to support strong conclusions.** Only 2 subjects with one session each are available; the BDSB method does not consistently outperform baselines (e.g., SSIM and PSNR are comparable to OTT-GAN). Given the small sample size, statistical significance is not evaluated, and the claim of superiority is not convincing.

4. **Downstream evaluation relies solely on R², which is insufficient.** R² measures how well a pRF model fits the fMRI signal, but a higher R² does not necessarily mean more accurate retinotopic maps. The paper does not assess topological correctness, violation of known retinotopic organization, or compare to standard atlases. The enhancement could be producing smoother, more predictable signals that fit the pRF model better but contain artifact introduced by the translation.

5. **Incomplete baseline comparisons.** The paper omits unpaired diffusion models that could be applied to brain disks (e.g., CycleDiffusion, score-based Schrödinger bridge baselines like DSS). The claim that "only our approach can improve pRF R²" is not fully established because several baselines (e.g., OTT-GAN) may also yield R² improvements, but their downstream results are not shown for all experiments (e.g., only FID and R² are partially reported).

### Minor

* The paper states that they are the first to improve fMRI SNR and retinotopic map quality using unpaired learning, but they do not adequately discuss prior work on fMRI super-resolution (e.g., using CNNs or GANs within the same field strength) to contextualize the novelty.
* The ablation study (Table 3) shows that harmonic mapping alone achieves comparable FID to full conformal mapping, but the explanation for why conformal mapping yields better R² is brief and somewhat vague.

### Trivial

None.

## Nice-to-Haves

* For the cross-dataset experiment, the authors could perform a "face validity" check by examining whether the enhanced pRF maps exhibit known retinotopic features (e.g., foveal vs. peripheral organization, coherent angle maps) that are plausible for a given subject. This would partially compensate for the missing ground truth.
* Including a quantitative comparison of topological violation rates (e.g., using tools like Tu et al. 2021) would strengthen the claim that enhancement improves pRF quality.
* Validation on a larger paired dataset (if available) or a more realistic simulation that includes different noise profiles and acquisition parameters.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

* **Strengthen real-data evidence.** Either acquire or identify a more substantial paired dataset (even with simplified stimuli), or perform a rigorous validation on the TDM dataset showing that enhanced pRF maps are reliably closer to the 7T maps than any baseline.
* **Address the stimulation mismatch issue.** If cross-dataset test subjects lack ground truth, consider evaluating on the same subjects by holding out a subset of their 7T data as a hidden test (e.g., within NSD, split subjects for synthetic evaluation; for NOD, could use the paired TDM subjects in a leave-one-out manner).
* **Add topological evaluation of pRF maps.** Report the percentage of vertices that violate retinotopic organization (e.g., mirror reversals, discontinuities) for both raw 3T and enhanced maps.
* **Clarify the definition of "unpaired" in the TDM experiment.** Table 1 says training is unpaired even when paired data is available—confirm that the model never sees simultaneous 3T and 7T from the same subject and run during training. If true, the TDM evaluation is a weak test of the unpaired assumption.
* **Report R² for baselines in the cross-dataset and TDM experiments.** The current Table 2 only shows R² for the proposed method in those settings; baselines are missing, making it impossible to assess relative improvement.

## Score and Decision
4 (borderline reject). The paper addresses an important problem and introduces a novel combination of techniques, but the experimental validation has critical weaknesses: the cross-dataset real experiment lacks ground truth and uses mismatched stimuli, the synthetic experiment uses an unrealistic degradation model, and the paired real experiment is too small to draw strong conclusions. The downstream evaluation is narrow (R² only), and baseline comparisons are incomplete. These issues prevent the paper from convincingly supporting its core claim that 3T fMRI can be enhanced to 7T quality in practical settings.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>