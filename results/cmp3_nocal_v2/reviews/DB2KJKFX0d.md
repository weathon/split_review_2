## Summary

This paper proposes BDSB (Brain Disk Schrödinger Bridge), a pipeline that enhances 3T fMRI signals to approximate 7T quality by (1) conformally mapping cortical surface meshes to 2D disks for cross-subject alignment, and (2) applying an unpaired Schrödinger Bridge diffusion model for 3T→7T translation. The method is evaluated on synthetic data, a cross-dataset experiment (3T NOD → 7T NSD), and a paired 3T/7T benchmark (TDM), with downstream pRF retinotopic decoding as the key application. The problem is genuine and the pipeline design is motivated, but the empirical evidence does not fully support the central claims.

---

## Strengths

- **The conformal-mapping-to-2D-disk preprocessing solves a nontrivial alignment problem.** The ablation study (Table 3) provides concrete evidence: direct slicing without conformal mapping yields catastrophic results (SSIM 0.237, FID 226.8), while conformal mapping recovers meaningful structure (SSIM 0.849, FID 34.23). This demonstrates that the parameterization itself is critical.

- **Three evaluation tracks with complementary trade-offs.** The paper designs a synthetic experiment (known ground truth, controlled degradation), a cross-dataset real experiment (practical use case with no ground truth), and a TDM paired experiment (small but genuine paired data). This triangulation shows awareness of the data limitations and is more informative than relying on a single setting.

---

## Weaknesses

### Major

- **The cross-dataset real experiment conflates field-strength enhancement with dataset translation, undermining interpretability of its results.** The Schrödinger Bridge is defined with the assumption that \(p_0\) and \(p_1\) represent "3T and 7T BD distributions viewing the same pRF stimuli" (line 94). However, the cross-dataset experiment uses 3T NOD subjects viewing natural objects as source and 7T NSD subjects viewing natural scenes as target — differing in subjects, stimulus content, and acquisition protocol. While the paper acknowledges "no ground truth" (line 45), it does not address that the model could be learning dataset-style transfer rather than field-strength enhancement. The reported improvements in FID (183.83 → 70.65) and \(\bar{R}^2\) (20.26 → 25.91) could partly reflect adaptation to the target dataset's distribution, not necessarily better neural encoding.

- **On the only real paired benchmark (TDM), the proposed method does not clearly outperform baselines, and the paper overstates its standing.** From Table 2 (TDM Real): SSIM is 0.718 vs. OTT-GAN 0.727 (OTT-GAN wins), PSNR is 19.24 vs. OTT-GAN 19.18 (margin of 0.06 dB, essentially a tie), and only FID shows a clear advantage (62.09 vs. 84.45). The paper claims "our pipeline achieves the best performance" (line 176), which is contradicted by the SSIM column. Furthermore, no uncertainty estimates are reported — the TDM experiment uses only 2 subjects with 3 test runs each, and single numbers without variance cannot support claims of superiority. The 0.06 dB PSNR margin and the SSIM deficit could easily be within measurement noise.

### Minor

- **Large gap between synthetic and real performance weakens support for the headline claim.** The synthetic degradation (down-sampling + Gaussian noise) is simpler than real 3T/7T differences, which involve different hardware, pulse sequences, and physiological noise profiles. The performance drop from synthetic (SSIM 0.855, PSNR 25.05, FID 42.88) to TDM real (SSIM 0.718, PSNR 19.24, FID 62.09) is substantial. The paper acknowledges this limitation (line 226) but only in the Discussion, while the abstract's claim "making it comparable to 7T quality" is stated without qualification about which experiment supports it.

- **Ablation study shows regularization terms worsen FID without discussion.** From Table 3: adding PatchNCE and BD-SSIM to conformal mapping improves SSIM (+0.006), PSNR (+0.79 dB), and \(\bar{R}^2\) (+1.98 pp) but increases FID from 34.23 to 42.88 — a 25% relative degradation. This trade-off is not discussed. The paper describes BD-SSIM as playing a "critical role in maintaining structural integrity" (line 218), but does not address why a core metric moves in the opposite direction.

- **No uncertainty estimates or statistical testing anywhere in the paper.** Terms like "significantly improves" (Abstract, line 176) are used without standard deviations, confidence intervals, or p-values. For a paper whose empirical results are its primary contribution, this is a substantive omission.

- **The \(\bar{R}^2\) metric in the cross-dataset experiment could reflect signal smoothing rather than genuine neural enhancement.** \(R^2\) measures how well the pRF model's predictions fit the enhanced signal. If enhancement produces smoother signals that are easier to fit (without improving neural information content), \(R^2\) can increase artifactually. The cross-dataset experiment lacks ground truth to rule this out, and no control analysis (e.g., split-half reproducibility of pRF parameters, topological fidelity of retinotopic maps) is provided.

### Trivial

None.

---

## Nice-to-Haves

- Report uncertainty on the TDM results (multiple random seeds, mean ± std) to clarify whether the small margins are meaningful.
- Add a "self-supervised" sanity check for the cross-dataset setting: create synthetic "3T-like" versions of NSD data from held-out NSD subjects, preserving the cross-subject nature while providing ground truth.
- Include a control analysis showing that pRF parameter estimates (center, size) from enhanced data are more reproducible across split-half trials, directly addressing the concern that \(R^2\) gains could come from signal smoothing.

---

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"Baseline configurations are not described — deferred to supplementary material"* — Removed per hard rule: the parser strips supplementary material; details exist in the original submission.
- *"No analysis of failure cases"* — The paper does discuss failure cases at line 194 (inert vertices show weaker alignment). A systematic analysis would be nice-to-have but is not a missing requirement.
- *Strength: "The problem is well-chosen and practically motivated"* — Removed per rule: this is a generic scope justification, not a concrete strength specific to the paper's execution.
- *"Methodological novelty not explicitly stated"* — The paper frames itself as a pipeline contribution; this is an accurate characterization, not a weakness.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

- Revise the headline claim in the abstract to reflect which experiments support it — specifically, separate what the synthetic experiment (where "comparable to 7T" is most plausible) shows from what the real experiments show.
- Add error bars or standard deviations to all quantitative results, especially the TDM experiment where the effective test size is very small.
- Discuss the FID/SSIM trade-off observed in the ablation study: acknowledge that regularization improves pixel-level and downstream metrics but worsens distribution-level similarity.
- In the cross-dataset experiment, include some control (e.g., split-half reproducibility of pRF parameters) to distinguish genuine neural enhancement from signal smoothing.

---

## Score and Decision

**MY FINAL SCORE:** <score>4.5</score>
**MY FINAL DECISION:** <decision>Reject</decision>