## Summary

This paper proposes DPG, a unified framework for imperfect-label diffusion guidance tasks (style transfer, super-resolution, deblurring). It introduces two components: (1) *data knowledge* — injecting noisy versions of the imperfect label into early reverse diffusion steps, and (2) *process knowledge* — a margin-based constraint enforcing that each denoising step produces an output closer to the target than the previous step. The paper evaluates on three tasks against a broad set of recent baselines.

## Strengths

- **Empirical breadth.** Evaluated on three distinct tasks (style transfer, super-resolution, deblurring) against 10+ recent baselines per task (2023–2025), providing a broad comparison landscape.
- **Task categorization is useful.** The framing into weak-label vs. degraded-label guidance, and the analysis of why unification is challenging (partial vs. near-complete information in labels), provides a helpful conceptual organization.
- **Qualitative results are visually competitive.** The shown outputs (Fig. 4) display fewer artifacts and better detail recovery than many baselines on visual inspection.
- **The data knowledge injection mechanism is novel.** Diffusing the processed label and blending it into the latent path (Eqs. 6–7) goes beyond standard loss-gradient guidance and meaningfully differs from prior approaches like SDEdit.

## Weaknesses

### Fatal

- **Identical LPIPS values across super-resolution and deblurring (Tables 1b and 1c).** The LPIPS row is numerically identical down to four decimal places for *every* method that appears in both tables (DPG: 0.2236; PSLD: 0.2675; FPS-SMC: 0.2540; SITCOM: 0.3100; DMAP: 0.5541; FlowDPS: 0.4887; FlowChef: 0.4934; DOC: 0.2448; TTG: 0.2869; FreeDom: 0.6764 — see lines 279 and 287). Even the first entries (InvSR at 0.2325 vs. DCDP at 0.2325) match exactly despite being different methods for different tasks. PSNR and SSIM *do* differ across the two tables, making this an isolated LPIPS-specific anomaly rather than a wholesale table duplication. Nevertheless, it is not credible that two image restoration tasks with different physics (4× downsampling+noise vs. Gaussian blur+noise) produce identical perceptual similarity scores for every method. This indicates a data processing error in the LPIPS evaluation pipeline for at least one of the two tasks. Since the paper's central claim of cross-task effectiveness depends on quantitative validation across all three tasks, the evidence for super-resolution and deblurring is compromised.

### Major

- **No computational cost evaluation despite substantially higher inference cost and efficiency claims.** The abstract claims "elevating the precision and efficiency of outputs" and "accelerating convergence." Yet DPG requires per timestep: two U-Net forward passes (Eq. 7), gradient optimization of $z_{0|t}$ via L1 (Eq. 9), and gradient optimization of $z_{0|t-1}$ via L2 (Eq. 11). This is significantly more expensive than standard sampling (one U-Net eval per step). The paper reports zero runtime measurements, zero FLOP comparisons, and zero wall-clock times. Without this data, the efficiency claims are unverifiable, and the comparisons with baselines are uninformed about the cost–quality tradeoff.

### Minor

- **Ablation results provide only mixed support for both components.** In the style transfer ablation (Table 2), removing process knowledge *improves* Text Score (0.3008 vs. 0.2952 for full DPG) — a result the paper does not mention. In super-resolution, removing data knowledge barely changes SSIM (0.8224 vs. 0.8233) and LPIPS (0.1574 vs. 0.1573). While other metrics show clearer benefits, these results suggest the two components contribute unequally across tasks. A more nuanced discussion of when each component helps (and when it does not) is needed.

- **DPS (Chung et al., 2022) is cited in references but never discussed in the body.** Diffusion Posterior Sampling is arguably the most influential posterior-sampling method for diffusion-based inverse problems and is structurally closest to what DPG does (latent optimization with a measurement loss). The omission is notable and leaves the paper's positioning relative to this important prior work unclear.

- **No confidence intervals or error bars.** Given the fine-grained metric differences (e.g., SSIM 0.8323 vs. 0.8283 for DPG vs. FPS-SMC in super-resolution), the absence of any uncertainty quantification makes it impossible to assess whether reported advantages are statistically meaningful.

- **Evaluation domain is narrow.** Super-resolution and deblurring are evaluated only on 1,000 FFHQ face images. Generalization to non-face domains (e.g., ImageNet, natural scenes) is untested.

### Trivial

- The super-resolution column headers in the qualitative comparison caption say "ImSR" while Table 1(b) says "InvSR" — minor inconsistency.
- Figure 2 caption text is garbled by the parser but likely contains inconsistencies in the original figure description.

## Nice-to-Haves

- Report wall-clock time or U-Net evaluations per image for DPG and all baselines to support or retract the efficiency claims.
- Correct the LPIPS evaluation for the affected tasks and report all quantitative results with error bars.
- Add a discussion of the relationship to DPS and clarify how DPG's approach differs from measurement-gradient-guided posterior sampling.
- Include a limitations section acknowledging failure cases or conditions where DPG underperforms.

## Removed Points

These points from the input review are excluded with justification:

- **"Unified framework overclaim"** — The paper's claim is about the framework structure (data knowledge + process knowledge) being applicable across tasks, not about being entirely task-agnostic. The paper transparently states that M(y) is task-specific. DPG genuinely introduces components that previous loss-guided methods do not have. The claim is appropriately scoped. *Removed: overstates the problem.*

- **"Process knowledge logical tension"** — The paper motivates process knowledge as addressing cumulative error in sequential optimization, not as solving L1's coarseness. The mechanism (margin constraint across time steps, Eq. 11) is logically consistent with this motivation — it adds a temporal structure that standard stepwise L1 lacks. *Removed: conflates two separate issues in the paper's argument.*

- **"False dichotomy about method categories"** — The paper categorizes existing methods into feature-mapping, feature-exploitation, strict-constraint, flexible-sampling, and loss-guided groups. The "either/or" phrasing in the abstract is a simplification but the full paper acknowledges multiple categories. *Removed: misreading of the full text.*

- **"M, N_iter, hyperparameters deferred to appendix"** — The appendix is stripped by the parser; these details exist in the original submission. *Removed: per policy, appendix-stripped content is not a valid criticism.*

- **"Qualitative fairness with pixel-space methods"** — The paper marks these methods with asterisks and is transparent about the distinction. *Removed: the paper already handles this appropriately.*

- **"No code release/reproducibility details"** — Not required for the paper itself and not a standard criticism for conference submissions at this stage. *Removed: not a paper weakness.*

- **"Notational inconsistency in Eq. 7"** — This is a trivial formatting artifact. *Removed: formatting nitpick.*

- **General speculative concerns** — Framings like "could the metric be measuring a proxy?" or "are confounders controlled?" that lack a specific anchor in paper content are removed.

## Novel Insights

None beyond the paper's own contributions. The reviewer's main novel observation — that the LPIPS duplication indicates a data error — is confirmed from the paper text, but this is an empirical finding about a flaw in the paper, not a conceptual insight that improves on the paper's own ideas.

## Suggestions

1. **Fix the LPIPS evaluation issue.** This is non-negotiable: re-run LPIPS for the affected tasks and verify the pipeline. Provide corrected tables.
2. **Report compute cost.** Add wall-clock time per image or number of U-Net evaluations for DPG and baselines, or remove efficiency claims from the abstract.
3. **Add statistical uncertainty.** Report confidence intervals or error bars for all quantitative metrics.
4. **Discuss DPS.** Clarify how DPG relates to and differs from Diffusion Posterior Sampling.
5. **Acknowledge ablation nuances.** Discuss the cases where components show marginal benefit (Text Score without process knowledge, SSIM/LPIPS without data knowledge in SR).

## Score and Decision

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>