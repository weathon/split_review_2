Now I have sufficient calibration data. Let me finalize the review.

## Summary

This paper proposes a plug-and-play ADMM framework (ADMM-PnP) that integrates score-based denoisers via a novel three-stage "AC-DC" denoiser design: (1) auto-correction (AC) by adding Gaussian noise, (2) directional correction (DC) via conditional Langevin dynamics, and (3) score-based Tweedie/ODE denoising. The AC-DC design explicitly addresses the manifold mismatch between ADMM iterates and the noisy data manifolds on which score functions are trained. The paper provides convergence analysis (weak nonexpansiveness → δ-ball convergence, and boundedness → fixed-point convergence under adaptive step sizes) and evaluates the method on six inverse problems across FFHQ and ImageNet.

## Strengths

- **Principled denoiser design (AC-DC).** The three-stage structure has clear internal logic: the AC step adds Gaussian noise to push ADMM iterates toward the score's training manifolds; the DC step uses conditional Langevin dynamics to refine manifold alignment; and the final Tweedie/ODE denoising operates on an iterate that is actually on or near the score's operating manifold. This is more thoughtful than the simple noise injection used in prior work (DiffPIR, Li et al. 2024) and is grounded in a well-articulated problem diagnosis (Sec. 2, "Challenges — Manifold Mismatch and Convergence").

- **Non-trivial convergence analysis.** Extending the ADMM-PnP convergence theory of Ryu et al. (2019) and Chan et al. (2016) to a score-based denoiser is a genuine theoretical contribution. Proving that the AC-DC denoiser satisfies a weakly nonexpansive property (Theorem 2) and establishing boundedness (Theorem 3) within the fixed-point convergence framework is non-trivial and extends the known theory to a new class of denoisers.

- **Breadth of experimental validation.** The method is tested on six inverse problems (super-resolution, random inpainting, box inpainting, Gaussian deblurring, motion deblurring, phase retrieval) across two datasets (FFHQ 256×256, ImageNet 256×256) with multiple baselines (DPS, DAPS, DDRM, DiffPIR, RED-diff, DCDP, PMC). This is a thorough evaluation compared to many PnP papers.

## Weaknesses

### Major

- **Theory-practice gap in the DC Langevin step.** The DC step (Algorithm 1, lines 3–6) approximates the conditional score $p(\mathbf{z}_{\text{ac}}^{(k)}|\mathbf{z}_{\sigma^{(k)}})$ using a Gaussian distribution. The paper acknowledges (line 135) that the exact conditional likelihood is "unavailable" and gives only a vague condition ($\text{Var}(\mathbf{s}^{(k)})^{1/2} \ll \sigma^{(k)}$) for the approximation to be valid, without bounding or quantifying this approximation error. Theorems 2 and 3 explicitly assume "the DC step reaches the stationary distribution for each $k$," but the actual algorithm runs only $J=10$ Langevin steps with an approximate score — it does not converge to the true stationary distribution. A footnote (line 207) claims counterparts removing this assumption exist in Appendix E.2, but as presented in the main text, the theorems analyze an idealized denoiser while the experiments test a practical approximation, creating a disconnect that the paper does not resolve.

- **No variance or statistical significance reported.** Table 1 reports mean PSNR/SSIM/LPIPS over 100 images without any standard deviations, confidence intervals, or measures of variance. Across 6 tasks × 2 datasets × 3 metrics with many baselines, it is impossible to tell which differences are meaningful. For example, DCDP beats Ours-tweedie on box inpainting FFHQ (25.230 vs 24.025 PSNR), and many of Ours-tweedie's margins over DAPS are small (e.g., super-resolution FFHQ: 30.439 vs 29.529). Without variance estimates, the robustness of the claimed improvements cannot be assessed.

- **Computational cost is unreported, undermining comparison fairness.** Each ADMM iteration requires the AC step, $J=10$ Langevin steps (each one score evaluation), and a Tweedie or 10-step ODE denoiser. Additionally, each ADMM iteration solves an inner optimization subproblem (7a) with up to 1000 Adam steps (line 297). With $K = W+10$ total iterations and $W$ unspecified, the total score evaluations per image could exceed 1000. The paper reports no NFEs, wall-clock time, or any compute cost. Without controlling for computational budget, it is unclear whether the reported improvements reflect algorithmic superiority or simply higher compute.

### Minor

- **Missing baseline DPIR.** DPIR is listed in the baselines (line 295) but never appears in Table 1. No explanation is given for its absence.
- **Table 1 contains several inconsistencies.** "DiPIR" is used instead of the correctly spelled "DiffPIR" from the baselines list; "DDPM" appears in the Gaussian blur section (while the baselines list DDRM, not DDPM); PMC rows have duplicate entries with empty cells; DCDP is missing from the motion deblur section.
- **The window size $W$ is never specified numerically** (line 297), making the total iteration count $K = W+10$ ambiguous and the computational cost unquantifiable.
- **The ablation study is incomplete.** Fig. 5 only varies the number of DC steps $J$ on a single task (phase retrieval) with visual comparison only — no quantitative metrics. The AC step is not ablated at all. A proper ablation would test configurations with and without each component across multiple tasks and report metrics.
- **The abstract lists HDR as a validation application** (line 28), but the only HDR mention in the experiments (line 293) is a scaling factor within random inpainting. There is no dedicated HDR experiment with reported results.

### Trivial

- **Inconsistent notation.** The algorithm output is called $\mathbf{z}_{\text{rw}}^{(k)}$ (line 109) but Theorems 2 and 3 refer to $\mathbf{z}_{\text{lw}}^{(k)}$ (lines 183, 205).

## Nice-to-Haves

1. Characterize or empirically estimate the DC approximation error — e.g., bound the KL divergence between the stationary distribution of the approximate Langevin chain and the true conditional distribution of $\mathbf{z}_{\sigma^{(k)}}|\mathbf{z}_{\text{ac}}^{(k)}$.
2. Report NFEs per image and wall-clock time for all methods, ideally including an NFE-controlled comparison.
3. Add standard deviations (or other variance estimates) to all quantitative results in Table 1.
4. Add a quantitative ablation isolating each component (no denoiser, AC-only, DC-only, full AC-DC) across multiple tasks.
5. State the numerical value of $W$ and the total iteration count $K$.
6. Clean up Table 1: fix DiPIR→DiffPIR, resolve DDPM/DDRM, remove duplicate PMC rows, include/exclude DPIR transparently.
7. Either add dedicated HDR results or remove HDR from the abstract's list of validation applications.

## Removed Points

The following criticisms from the input review were removed:

- **DiffPIR description garbled (line 64), garbled equation (9) at line 129 ($\mathbf{z}_\sigma^{(k)} = \mathbf{z}_\sigma^{(k)} + \sigma^{(k)}\mathbf{n}_1$), undefined $\sigma_{z_t}$ in Algorithm 1.** These are likely PDF parsing artifacts (self-referential equation, broken subscript notation) that do not appear in the original submission. Removed per formatting/parser artifact rules.
- **Learned score approximates the true score (Assumptions 2–3).** This is a standard assumption across all score-based methods, not specific to this paper's analysis.
- **$R_\sigma$ subscript without superscript.** Trivial notation point that does not affect understanding.
- **Notation of $(\zeta(\tilde{\mathbf{x}}^{(k)} - \mathbf{x}^{(k+1)}))_{\sigma^{(k)}}$ is unclear.** Partially a formatting artifact; also could be clarified but does not affect the paper's core claims.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The paper's core algorithmic contribution (the AC-DC denoiser) is well-motivated and the convergence analysis is non-trivial. However, to be convincing for publication, the authors must: (1) reconcile the theory-practice gap by either relaxing the stationarity assumption in the main theorems or characterizing the DC approximation error; (2) report variance estimates and computational costs to ground the experimental claims; and (3) complete the ablation study to isolate each component's contribution.

## Score and Decision

**Round 1 bracket (5.5–7.5).** The most topically similar anchor is "Prior Mismatch and Adaptation in PnP-ADMM with a Nonconvex Convergence Analysis" (avg 6.25, Reject), which has stronger theory (explicit error bounds for denoiser mismatch) but narrower experiments (SR and deblurring only, noise 0.01) and missing comparisons. Our paper's theory is weaker (δ-ball convergence with uncharacterized radius; assumptions not matched by implementation) but experiments are broader. Other anchors in this range: "Restoration Network as Implicit Prior" (6.25, Accept), "Decomposed Diffusion Sampler" (6.50, Accept), "DiffStateGrad" (6.75, Accept), "PnP-Flow" (5.50, Accept). 

**Narrowing.** Comparing itemized impact scores: our paper's strongest weaknesses (theory-practice gap -9.99, no variance -10.00, compute unreported -9.84) have magnitudes comparable to the most severe weaknesses in the accepted anchors (e.g., Learned Proximal Networks: "convergence proof not true" -10.00, accepted at 5.75). However, unlike that paper, our paper's core theoretical claim (convergence of the ADMM-PnP algorithm with AC-DC) is directly impacted by the theory-practice gap — the theorems assume exact Langevin stationarity, but the algorithm uses an approximate Gaussian conditioned score for only 10 steps. This places our paper closer to the 5.5 anchor (PnP-Flow, Accept) in overall assessment: meaningful contributions with significant unresolved concerns.

**Final score: 5.5, Decision: Reject.** The paper has a genuinely novel algorithmic idea and broad experimental work, but the disconnect between the convergence theory (which assumes Langevin stationarity with exact conditional scores) and the practical algorithm (which uses 10 steps with an uncharacterized Gaussian approximation) is a structural gap that undermines the paper's central claim of a "convergent framework." The absence of variance estimates and computational cost reporting further weakens the experimental contribution. The paper could become a strong 6–7 after addressing these issues.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>