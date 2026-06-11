## Summary
# Final Review Report

## Summary

This paper proposes DPG (Data and Process Guidance), a training-free unified framework for imperfect-label diffusion guidance covering both weak-label (style transfer) and degraded-label (super-resolution, deblurring) tasks. The core idea combines two knowledge sources: (1) **data knowledge** — diffusing the imperfect label and injecting noisy variants into early reverse-diffusion steps to enrich the generative process with label information, and (2) **process knowledge** — a progressive alignment loss that enforces each denoising step to produce an output more consistent with the label than the previous step, aiming to reduce error accumulation. Experiments on 40K WikiArt style-transfer samples and 1K FFHQ face images compare DPG against 10-11 baselines per task, showing improvements in Style Loss (0.631), CLIP Loss (4.233), PSNR (28.86 for SR), and SSIM (0.774 for deblurring). The paper makes a reasonable contribution in terms of task unification and the two-knowledge-source design, but several methodological details (computational cost, gradient backpropagation scope), statistical rigor (missing variance, identical LPIPS values across tasks), and writing precision (overclaims, catalog-style related work) require attention before the work can be considered fully validated.

## Strengths
1. **Novel unification perspective.** The paper is one of the first to explicitly formalize the gap between weak-label and degraded-label guidance tasks and to propose a single framework that handles both families without task-specific architectural changes. The analysis of data-information density asymmetry and objective misalignment (Section 1, lines 69-84) provides a useful conceptual contribution that could inform future unified diffusion frameworks.

2. **Elegant two-knowledge-source design.** The combination of data knowledge (noisy label injection) and process knowledge (progressive alignment loss) is conceptually clean and well-motivated. Unlike SDEdit, which uses the label as a one-time initialization, DPG's multi-step injection allows the model to adaptively select which label information to use at each denoising stage. The margin-based loss in Eq. (11) for enforcing monotonic alignment across steps is a technically interesting formulation.

3. **Strong empirical results on diverse tasks.** Across 11 baselines for style transfer and 10 baselines for super-resolution/deblurring, DPG achieves the best or second-best scores on 8 out of 12 metric-task combinations. The qualitative comparisons (Fig. 4) show visibly improved detail restoration (mole, temple hair, hat folds) and stylization quality, suggesting genuine practical benefits.

4. **Training-free framework.** DPG requires no task-specific fine-tuning or feature extractor training, working directly with a pre-trained LDM backbone. This makes it readily deployable for new tasks without additional data collection or computation for training, which is a practical advantage over methods like StyleDrop or DEADiff that require per-task adaptation.

5. **Architecture-agnostic formulation.** The method is described in terms of general diffusion operations (noise injection, predicted-clean-latent optimization) that can work with both U-Net and DiT backbones, as noted in Section 3.1.

## Weaknesses
### W1. Formula ambiguity and reproducibility risk (Major)
**Page 3 — Method: Eq. (3).** The PLMS reverse-diffusion formula contains an ambiguous square-root expression:
$$z_{t-1} = \sqrt{\alpha_{t-1}} z_{0|t} + \sqrt{1 - \alpha_{t-1} - \sigma_t^2 \epsilon_\theta(t) + \sigma_t z}$$
The radicand is not parenthesized — it is unclear whether $\sqrt{1 - \alpha_{t-1} - \sigma_t^2}$ multiplies $\epsilon_\theta(t)$ or whether the sqrt extends over the noise term. The standard DDIM/PLMS formulation uses $\sqrt{1 - \alpha_{t-1} - \sigma_t^2} \, \epsilon_\theta(t) + \sigma_t z$. Additionally, Eq. (3) uses $\sqrt{\alpha_{t-1}}$ while Eqs. (10) and (12) use $\sqrt{\bar{\alpha}_{t-1}}$, creating an inconsistency that could affect noise scaling in the sampling trajectory. **Impact:** Two independent implementations of DPG could produce different results, undermining reproducibility. **Fix:** Clarify parentheses and unify notation to $\sqrt{\bar{\alpha}_{t-1}}$.

### W2. Missing computational cost and gradient backpropagation analysis (Major)
**Pages 4-5 — Method: Eqs. (9)-(11).** The gradient update $\nabla_{z_{0|t}} f_{loss}(D(z_{0|t}), y)$ requires backpropagation through the full decoder $D$ (a VQGAN decoder in LDM). With $N_{iter}=5$ inner iterations and $T=50$ denoising steps, this amounts to up to 250 decoder backward passes per image — roughly a 5× overhead over standard DDIM sampling. The paper does not discuss this cost, nor does it clarify whether gradients for $\mathcal{L}_2$ (Eq. 11) flow through the U-Net or are stopped at $z_{0|t-1}$. **Impact:** Readers cannot assess the practical deployability of DPG. **Fix:** Add a computational cost paragraph; clarify gradient stopping points; report GPU time and memory in the experiment section.

### W3. Statistical rigor insufficient for claimed superiority (Major)
**Pages 7-8 — Experiments: Table 1.** All metric values are reported as point estimates without variance, confidence intervals, or significance tests. Several margins are critically thin: DPG's SSIM in super-resolution (0.8323) exceeds FPS-SMC (0.8283) by only 0.004; its Text Score in style transfer (0.2952) is *lower* than TFG (0.3092) and FreeDom (0.2933). Without multi-seed statistics, the claimed "superior accuracy and robustness" is unverifiable. Additionally, the Abstract states "highest PSNR" but Table 1(c) shows DPG's PSNR (27.58) is lower than DCDP (27.91). **Impact:** The core empirical claim is not statistically established. **Fix:** Report mean±std over ≥3 seeds; add paired significance tests; correct the Abstract claim.

### W4. Suspicious LPIPS duplication across tasks (Major)
**Page 8 — Experiments: Table 1(b) vs 1(c).** The LPIPS Loss for DPG is reported as **0.2236** in both super-resolution and deblurring. These are different degradation models (4× downsampling + noise vs. Gaussian blur + noise), making identical LPIPS values to four decimal places highly improbable. This strongly suggests a copy-paste or computation error. **Impact:** If erroneous, the claim of "superior perceptual quality" across both tasks is partially unsupported. **Fix:** Verify and correct LPIPS values; if genuinely identical, provide an explanation.

### W5. Ablation inconsistency not discussed (Minor)
**Page 8 — Ablation: Table 2.** Removing process knowledge (w/o P) *increases* Text Score (0.3008 vs. 0.2952 with full DPG) in style transfer. The paper claims "process knowledge is both essential and effective" but does not address this negative result. **Impact:** The paper misses an opportunity to discuss the trade-off between style fidelity and text alignment. **Fix:** Add a sentence explaining the observed trade-off and its implications.

### W6. Priority claim unverifiable (Major)
**Page 2 — Introduction.** The paper states: "To our knowledge, this paper is the first study to analyze the gap between weak-label and degraded-label guidance tasks and to propose a unified approach to bridge it." Without external literature verification (which is disabled in this run), this claim cannot be independently assessed. Moreover, prior unified loss-guidance methods (TFG, FreeDom) are acknowledged but dismissed — the paper does not discuss how DPG's "unified" nature differs from theirs beyond performance. **Impact:** If a reviewer identifies a prior unified framework, the paper's novelty positioning is weakened. **Fix:** Replace "first" with "to our knowledge, this paper provides a new analysis of..." and explicitly state the distinguishing factors from TFG/FreeDom.

### W7. Introduction narrative is a catalog, not a gap-driven story (Minor)
**Pages 1-2 — Introduction.** Paragraphs 2 and 3 read as mini-surveys with 6-8 citation mentions each, listing methods without clearly stating what common gap they share or why DPG resolves it. The narrative momentum stalls in catalog-style exposition. **Impact:** Reviewers must work harder to extract the paper's specific contribution. **Fix:** Restructure to follow: specific practical challenge -> why category A fails -> why category B fails -> how DPG's design avoids both failure modes.

### W8. Conclusion lacks limitations and future work (Minor)
**Page 9 — Conclusion.** The 4-sentence conclusion restates the unification claim without mentioning any scope boundaries, failure conditions, or computational trade-offs. No actionable future directions are proposed. **Impact:** Reduces the paper's perceived scientific completeness. **Fix:** Add validated findings (with metric anchors), bounded limitations, and 2-3 concrete next-step experiments.

### W9. Overclaiming and imprecise wording (Minor)
**Throughout the paper.** The Abstract uses "universal framework" and "optimal performance" without qualification. The phrase "paving the way for future innovations in unified frameworks" is promotional and unverifiable. The claim that loss functions are "blind to the valuable priors and granular details that exist within the data itself and are not reducible to a mathematical expression" overstates — texture information is mathematically representable (Gram matrices, perceptual losses). **Impact:** Inflated language reduces reviewer trust. **Fix:** Replace universal/optimal claims with bounded, evidence-grounded wording.

### W10. Limited evaluation scope (Minor)
**Page 7 — Experiment Settings.** Evaluation is limited to FFHQ (faces) and WikiArt (art). The paper does not test on standard natural-image benchmarks (e.g., ImageNet, COCO, or DIV2K for SR). Generalization claims to "imperfect-label guidance tasks" are therefore only validated on two restricted domains. **Fix:** Add results on at least one standard natural-image benchmark per task (e.g., DIV2K for SR, GoPro for deblurring).

## Score
**Final Score: 6/10**

**Score Rationale:** This score reflects an assessment where research value and novelty are primary dimensions, in accordance with the scoring policy.

**Strengths supporting the score:** The paper introduces a conceptually clean two-knowledge-source framework that bridges weak-label and degraded-label guidance tasks, a useful unification perspective. The empirical results show competitive or superior performance across 12 metric-task combinations against a diverse set of baselines. The training-free, architecture-agnostic design is practically attractive.

**Weaknesses constraining the score:** Several major issues prevent a higher score. First, the statistical rigor is insufficient — all metrics are point estimates without variance, several margins are thin, and the Abstract overclaims on PSNR ranking. Second, the suspicious LPIPS duplication across tasks requires verification and correction. Third, the computational cost of DPG's per-step gradient optimization is not discussed, making it impossible to assess practical trade-offs. Fourth, the formula ambiguity in Eq. (3) introduces reproducibility risk. Fifth, the priority claim ("first study") is unverifiable in this run and should be softened. The paper also exhibits catalog-style writing in the introduction and lacks a bounded conclusion with limitations.

**Overall assessment:** The core ideas are promising and the experiments demonstrate genuine quality improvements, but the current presentation lacks the statistical and methodological rigor needed for top-tier venues. With the identified weaknesses addressed — particularly variance reporting, LPIPS verification, computational cost analysis, and claim softening — the contribution could be suitable for publication.