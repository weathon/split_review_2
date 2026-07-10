Now I have all the data I need. Let me compile the final consolidated review.

---

## Summary

This paper addresses the challenge of integrating score-based denoisers (from diffusion models) into ADMM-based plug-and-play frameworks for solving inverse problems. The authors identify a genuine "manifold mismatch" problem: ADMM iterates, especially their dual variables, distort the noise geometry that pre-trained score functions expect. They propose a three-stage AC-DC denoiser (Auto-Correction by adding Gaussian noise, Directional Correction via conditional Langevin dynamics, and Tweedie/ODE denoising) to bridge this gap. The paper provides convergence analyses under both fixed and adaptive step-size schedules and evaluates the method on seven inverse problems across two datasets.

## Strengths

- **Well-motivated problem identification (Section 1, Section 2).** The manifold mismatch between score-training distributions and ADMM-iterate distributions—further complicated by dual variables—is a genuine obstacle that the paper articulates concretely. This framing correctly distinguishes the challenge from prior score-based PnP methods (DiffPIR, RED-diff, SNORE) in primal-only settings.

- **The AC-DC pipeline is a reasonable architectural idea (Algorithm 1, Figure 1).** Adding Gaussian noise (AC) to push iterates toward score-trained manifolds, then using conditional Langevin dynamics (DC) to refine alignment before applying Tweedie/ODE denoising, is logically coherent. The use of Langevin dynamics targeting $p(z_{\sigma^{(k)}}|z_{\text{ac}}^{(k)})$ — whose support lies within $\mathcal{M}_{\sigma^{(k)}}$ — addresses the manifold gap beyond naive noise injection.

- **Broad experimental coverage (Table 1).** Seven inverse problems (super-resolution, random/box inpainting, Gaussian/motion deblurring, phase retrieval, HDR) across two datasets (FFHQ, ImageNet) with multiple baselines (DPS, DAPS, DDRM, DiffPIR, RED-diff, DCDP, PMC) provide a solid evaluation scope.

## Weaknesses

### Major

- **Convergence theory requires the denoiser to vanish, but experiments use a non-vanishing denoiser.** Theorem 2(b) requires $\lim_{k\to\infty} (\sigma^{(k)})^2 \nu_k = 0$, and Theorem 3(b) explicitly requires $\lim_{k\to\infty} \sigma^{(k)} = 0$ and $\lim_{k\to\infty} \sigma_{s^{(k)}} = 0$. However, the experimental schedule (Section 6) uses $\sigma^{(k)} = \max(0.1, 10 - (10-0.1)\cdot k/W)$, clamped at 0.1 — it never approaches zero. The convergence guarantees therefore apply to a regime where the denoiser has vanishing effect, but the method is evaluated with a permanently active denoiser ($\sigma=0.1$). The paper does not flag this gap in the limitations section. Since "convergence guarantees" is a headline contribution, this mismatch between theory and practice is significant. The asymptotic analysis is still meaningful, but the scope of what is actually proven versus what is claimed should be explicitly delineated.

- **The main theorems assume the DC Langevin dynamics reach their stationary distribution — implausible given the experimental setup.** Theorems 2 and 3 state: "assume that the DC step reaches the stationary distribution for each $k$." In practice, $J=10$ Langevin steps in a $256\times256 = 65536$-dimensional image space with step size $\eta^{(k)} = 5\times10^{-4}\sigma^{(k)}$ cannot plausibly mix to stationarity. Footnote 1 references Appendix E.2 (removed by the parser) as containing "counterparts removing this assumption," but the main text's theorems depend on it. This is a strong idealized assumption whose violation in practice is orders of magnitude.

### Minor

- **Table 1 has formatting issues that undermine trust.** (a) "PMC" appears as duplicate entries with inconsistent/blank scores under Super-resolution (twice), Motion Deblur (twice, second blank), Gaussian Blur (four times, blank), and Inpainting Box (three times, mostly blank). (b) "DiPIR" appears in four rows (lines 321, 331, 351, 361) but the baselines list (Section 6) references "DiffPIR." (c) "DDPM" appears under Gaussian Blur (line 352) where "DDRM" is presumably intended. These are fixable but damage readability and trust.

- **No variance reporting.** Table 1 reports averages over 100 images without standard deviations, confidence intervals, or any measure of variability. Given the known variability of diffusion-based methods across random seeds and measurement realizations, this omission makes it difficult to assess whether reported improvements are meaningful.

- **DPS baseline numbers are notably below published values.** DPS achieves PSNR 24.828 on FFHQ 4× super-resolution in Table 1, while the original DPS paper reports ~27–28 dB under similar settings — a ~3 dB gap. If different experimental conditions (noise level, diffusion steps, checkpoint) apply, they should be stated to ensure fair comparison.

## Nice-to-Haves

- Add an ablation comparing AC-only (with extra compute matched to AC-DC) vs. AC-DC to isolate the benefit of the DC stage beyond additional compute.
- Report NFEs or wall-clock time per method, since the 10 DC Langevin steps + inner Adam loop per ADMM iteration likely incur higher computational cost than DPS or DiffPIR.
- Clarify the $W$ (decay window length) hyperparameter, as $K = W + 10$ is otherwise undefined.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. Criticism about equation (9) being "conceptually confused" and "self-referential" notation — this may be a parser-induced formatting artifact; the original submission may not have these issues.
2. Criticism about missing $W$ (decay window length) — standard tunable hyperparameter; not a substantive issue.
3. Criticism that "score-based denoising has rarely been combined with primal-dual methods" is overstated — the paper acknowledges DiffPIR uses variable splitting; this is a framing choice, not a weakness.
4. Criticism that Gaussian approximation for $\nabla\log p(z_{\text{ac}}|z_\sigma)$ is unjustified — the paper provides a condition ($\text{Var}(\mathbf{s}^{(k)})^{1/2} \ll \sigma^{(k)}$) and references an appendix; the justification is terse but present.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Explicitly state that convergence theorems require $\sigma^{(k)}\to0$ while experiments use $\sigma^{(k)}\ge 0.1$, and discuss why the constant-$\sigma$ regime is expected to behave similarly.
2. Either prove convergence with non-vanishing $\sigma$ (even a constant $\sigma>0$), or characterize the approximation error from the $\sigma=0.1$ floor.
3. Add variance reporting (standard deviations or confidence intervals) to Table 1.
4. Fix the duplicated PMC entries, method name typos ("DiPIR" → "DiffPIR", "DDPM" → "DDRM"), and blank cells in Table 1.
5. Explain the DPS baseline discrepancy or clearly state the experimental conditions that differ from the original DPS paper.

## Score and Decision

**Calibration Anchors Considered (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/HXjXPQU3yJ.md` (Prior Mismatch PnP-ADMM) | 6.25 | R1, R2 | Yes | This paper has stronger experiments (7 tasks vs. 2) but its theory-practice gap (σ→0 vs. σ≥0.1) is more fundamental than that anchor's presentation issues |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/66arKkGiFy.md` (PnP-ULA Mismatch) | 5.75 | R2 | Yes | Similar structure (theory + experiments for PnP under mismatch); both have negative-favorability weaknesses, but this paper's two major weaknesses are more consequential for the claimed contributions |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/kRBQwlkFSP.md` (DiffStateGrad) | 6.75 | R1 | Yes | Stronger paper overall; well-executed experiments with clear comparisons; this paper is weaker due to the theory-practice gap |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Z9Odi09Rv9.md` (Fast Noise-Robust Diffusion) | 4.75 | R1, R2 | Yes | This paper is stronger (no fundamental misunderstandings of core concepts like Tweedie's formula) |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5AtHrq3B5R.md` (PnP-Flow) | 5.50 | R2 | No | Similar tier; this paper's strengths are comparable but its major weaknesses are more damaging |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/x7d1qXEn1e.md` (Restoration Network as Implicit Prior) | 6.25 | R1, R2 | No | Stronger; cleaner theoretical contribution with verifiable assumptions |

**Bracketing:** Round 1 bracketed this paper between 3.5 and 6.5 based on topical similarity. Round 2 narrowed it to 4.0–5.5 by comparing favorability distributions. The two major weaknesses have negative favorability (−0.54, −1.45), which is more severe than the 5.75–6.25 anchor papers' weakest items. The strengths (9.50, 11.51, 12.89) are comparable to the 5.75 anchor's strengths but cannot compensate for the theory-practice gap because that gap directly undermines the paper's central claim of "convergence guarantees."

**Final score:** The paper identifies a real problem and proposes a reasonable architectural solution with broad experiments. However, the convergence guarantees — a headline contribution — are proven only for a regime (vanishing denoiser) that does not match the experimental regime (permanently active denoiser at σ=0.1), and the main theorems rest on an implausible stationary-distribution assumption. These are not fatal individually but together significantly weaken the paper's core claims. The experimental table issues compound the concern.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>