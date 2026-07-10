Now I have all the calibration data I need. Let me write the final consolidated review.

## Summary

This paper proposes Spherical Watermark, a lossless watermarking framework for diffusion models. The key idea is to construct a spherical 3-design from repeated watermark bits mixed with random padding, rotate it orthogonally, then scale by a chi-square-distributed radius to produce noise that is theoretically indistinguishable from standard Gaussian up to third-order moments. Compared to prior lossless methods (Gaussian Shading, PRC Watermark), the approach eliminates per-image key storage and reduces extraction time by roughly four orders of magnitude while maintaining or improving robustness.

## Strengths

- **A genuinely novel mapping from binary watermarks to Gaussian noise.** The core construction — forming a spherical 3-design via repeated watermark bits + binary embedding, rotating orthogonally, and scaling by a chi-square radius — is structurally different from stream-cipher-based (Gaussian Shading) and error-correcting-code (PRC) methods. The elimination of per-image key storage while maintaining losslessness is a concrete and meaningful practical advantage. [favorability=9.11]

- **Strong theoretical analysis with measurable guarantees.** The paper traces the distribution through each transform step (Theorems 3.1, 3.2, Lemmas 3.3, 3.4), establishing that the watermarked noise matches the standard Gaussian up to third-order moments. The connection to spherical t-design theory is apt and well-exploited, providing formal grounding uncommon in the watermarking literature. [favorability=10.42]

- **Empirical indistinguishability is convincingly demonstrated.** FID values for Spherical Watermark (e.g., 48.12 vs. Original's 48.13 on COCO SD v1.5) are essentially identical to the unwatermarked baseline. Binary classifier accuracy at both latent and image levels is at chance (~50%), meaning a trained ResNet-18 cannot distinguish watermarked from unwatermarked images. This goes well beyond typical PSNR-based evaluations. [favorability=8.50]

- **Computational advantage is large and well-measured.** Extraction is roughly four orders of magnitude faster than PRC Watermark, a genuinely practical improvement for deployment at scale. [favorability=10.22]

- **Robustness under adversarial attack is strong.** Against WEvade, Spherical Watermark achieves TPR=99.83% compared to PRC's 95.38% and Gaussian Shading's 99.23% (Table 2). This addresses a known failure mode of PRC (belief-propagation error floor under strong attacks). [favorability=10.41]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The fixed secret signature (T, C) security is not analyzed under multi-sample observation.** The paper notes that K = {T, C} is kept fixed and secret during runtime (Section 3.2), but never considers what an attacker who observes multiple watermarked images (with different messages m but the same T and C) could infer. Since each invocation uses a fresh random padding r, the threat is partially mitigated, but the paper should at minimum discuss whether an attacker can estimate T or C from a collection of watermarked images, or acknowledge this as a limitation. [favorability=5.29]

- **The theoretical guarantee (spherical 3-design) only covers moments up to degree 3, while full Gaussian indistinguishability requires all moments.** The paper acknowledges this in Section 5, and provides strong empirical evidence (FID, classifier accuracy) that the gap does not cause detectable artifacts. However, no argument is given for why the 3-design guarantee survives the nonlinear diffusion denoising process — this remains an open theoretical question (e.g., Lipschitz continuity of the ODE flow could bridge this gap). [favorability=6.65]

- **The inversion mismatch between generation and extraction is acknowledged but incompletely characterized.** Generation uses DPM-Solver++ with text prompts at CFG=7.5, while extraction uses DDIM inversion with empty prompts at CFG=1.0. The paper ablates different ODE solvers (Table 4) and timesteps (Table 5), but does not ablate (a) using the correct text prompt during inversion, (b) varying guidance scale during inversion, or (c) prompt complexity. While extraction accuracy is already ~99.99% under clean conditions despite this mismatch, understanding these sensitivities would strengthen the practical robustness analysis. [favorability=6.87]

- **The paper reports only final ACC after majority voting, not the pre-voting bit error rate (BER).** Understanding the BER before majority voting would help assess how much margin the repetition code provides and how close the method operates to its error-correction limit under strong attacks. [favorability=6.21]

### Trivial
None.

## Nice-to-Haves
- Report pre-majority-vote bit error rates to characterize the margin of the N=31 repetition code under various attacks.
- Add a formal argument (e.g., Lipschitz continuity of the ODE flow) connecting the spherical 3-design guarantee to post-diffusion noise indistinguishability.
- Ablate extraction accuracy when using the correct text prompt during inversion (vs. empty prompts), across different guidance scale values and prompt lengths.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **"Encryption-free" framing overstated** (removed): PRC also uses a fixed secret key, so the distinction is about per-image key management. The paper's framing is technically accurate (no encryption algorithms used) but could be clearer. This is an observation rather than a concrete weakness of the method's validity.
- **Figure 2 only shows two methods** (removed): Parser artifact from PDF extraction — the actual figure likely shows all four methods as described in the text.
- **Comparison with different watermark capacities** (removed): The paper acknowledges the 32-bit vs 512-bit distinction between traditional and latent-based methods. The meaningful comparisons (latent-vs-latent) are the paper's main focus.
- **Computational efficiency excludes diffusion steps** (removed): The paper explicitly states this scoping choice. Since diffusion steps are common across all methods, measuring only the transform time is appropriate for comparing methods.
- **Statistical significance tests** (removed): Nice-to-have but not standard practice in this literature. The paper reports means and standard deviations over 5 runs, which is standard.
- **Dimension sensitivity of spherical 3-design** (removed): The paper uses a fixed latent dimension (16,384) that matches standard Stable Diffusion architectures. How the approximation degrades at smaller dimensions is a niche concern.
- **Guidance scale ablation** (removed / moved to Nice-to-Haves): A reasonable suggestion but not a weakness given the already excellent results under the current setup.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
1. Analyze or discuss the security implications of the fixed signature (T, C) against an attacker who observes multiple watermarked images.
2. Report pre-majority-vote bit error rates to characterize the margin of the repetition code under various attacks.
3. Ablate the inversion mismatch: test extraction accuracy with correct prompts during inversion, and across different guidance scale values.
4. Consider adding a formal argument linking the spherical 3-design property to post-diffusion noise indistinguishability (e.g., via Lipschitz continuity of the ODE flow).

## Score and Decision

**Calibration anchors (all rounds):**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| PRC Watermark (Gunn et al.) | jlhBFm7T2J.md | 6.50 | R1 | Yes | Direct competitor. Spherical Watermark has better robustness (adversarial TPR 99.83% vs 95.38%), 4× faster extraction, comparable undetectability. PRC reviewers flagged robustness as a weakness; here it is a strength. |
| Shallow Diffuse | 1IwoEFyErz.md | 6.00 | R1 | Yes | Similar topic. Spherical Watermark has stronger theory (spherical 3-design), more comprehensive evaluation (more baselines, attacks), better presentation. |
| Hidden in the Noise (WIND) | ll2nz6qwRG.md | 5.83 | R1 | Yes | Similar topic. Spherical Watermark has broader evaluation (two backbone models, two datasets, adversarial attacks), and stronger theoretical guarantees. |
| A Recipe for Watermarking DMs | HexshmBu0P.md | 5.33 | R2 | Yes | Lower quality and novelty. Spherical Watermark is clearly stronger. |
| Spread them Apart | 9XEBFywIW7.md | 4.40 | R1 | Yes | Less relevant, lower quality. |

**Bracket reasoning (Round 1):** The paper is clearly above the PRC paper (6.50) — all favorability ratings for Spherical Watermark's strengths (8.50–10.42) exceed PRC's strength ratings, and Spherical Watermark's weaknesses (5.29–6.87) are far less damaging than PRC's low-favorability weaknesses (e.g., -0.89, 1.60). Initial bracket: 6.5–8.0.

**Narrowing (Round 2):** At the 6.5–8.5 range, no directly comparable diffusion watermarking papers exist at the upper end. TabWak (7.20, tabular diffusion) and Lightweight Deep Watermarking (7.60, non-diffusion) provide reference points. The Spherical Watermark paper matches these in evaluation rigor and exceeds them in theoretical novelty. Given that all weaknesses are minor (none below favorability 5.0, unlike PRC which had items at -0.89) and strengths are consistently high (8.50–10.42), the paper sits comfortably above 6.50.

**Final placement:** 7.5. The paper is a strong Accept. Key factors: the method is genuinely novel; the theoretical analysis is thorough; the empirical evaluation convincingly demonstrates undetectability, robustness, and efficiency gains; and the weaknesses are all minor (missing ablations, incomplete threat-model discussion) rather than fundamental. The comparison with the PRC paper (6.50) is particularly informative — Spherical Watermark addresses the very robustness weaknesses that PRC reviewers identified, while adding theoretical depth and computational efficiency.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>