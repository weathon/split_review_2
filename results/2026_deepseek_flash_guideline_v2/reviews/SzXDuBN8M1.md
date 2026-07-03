The calibration tool is unavailable due to a file path issue. I will proceed based on my judgment as an experienced area chair with knowledge of ICLR standards, using the verified evidence from the paper itself.

Let me write the final consolidated review.

---

## Summary

TD-JEPA introduces a temporal-difference (TD) variant of the latent-predictive (JEPA) loss for zero-shot unsupervised RL. The key innovation is replacing the on-policy Monte Carlo loss (which requires full trajectory rollouts) with a TD loss that only needs one-step transitions and actions sampled from target policies, enabling learning from offline, reward-free data. The method trains separate state and task encoders (φ and ψ) plus policy-conditioned predictors, with theoretical results connecting the loss to successor measure factorization. Empirically, TD-JEPA is evaluated across 65 tasks and 13 datasets, showing strong performance especially on pixel-based domains.

## Strengths

1. **Novel off-policy TD formulation for multi-policy latent prediction.** The TD loss (Eq. 7, Eq. 9) replaces the on-policy Monte Carlo loss (Eq. 5) that requires full trajectory rollouts, enabling learning from offline, reward-free data. This is a genuine algorithmic innovation that directly addresses the limitation stated in the abstract: "existing methods are typically limited to... on-policy trajectory data."

2. **Formal gradient-matching theorems connecting TD-JEPA to successor measure factorization.** Theorem 1 and Theorem 3 prove that the gradients of the TD-JEPA loss w.r.t. φ and ψ match those of forward/backward successor measure TD losses. Theorem 4 bounds policy evaluation error by the successor measure loss, linking the latent-predictive objective to downstream task performance. These results "generaliz[e] and imply all previous guarantees for latent-predictive representations" (Section 4), citing Tang et al. (2023), Khetarpal et al. (2025), Voelcker et al. (2024), and Lawson et al. (2025) as special cases.

3. **Strong empirical results on pixel-based domains, the most challenging setting.** TD-JEPA achieves 628.8 ± 5.5 on DMC_RGB (avg), substantially ahead of the next best BYOL-γ\* at 582.4 ± 9.8 — a clean ~8% improvement. The probability-of-improvement analysis (Figure 2) confirms TD-JEPA is "significantly better than [FB and HILP] in visual domains." Pixel-based zero-shot RL is identified by the paper as "one of the most challenging settings for unsupervised RL so far," and this is where TD-JEPA's advantage is clearest.

4. **Non-collapse guarantee for the doubly latent-predictive TD objective.** Theorem 2 proves that under a continuous-time relaxation with optimal predictors, the covariance matrices of φ and ψ remain constant, preventing collapse to trivial solutions. The paper honestly acknowledges the gap between this idealized setting and the practical algorithm.

5. **Demonstration that frozen pre-trained representations enable fast downstream adaptation.** Figure 4 shows that keeping the pre-trained state encoder frozen during offline or online fine-tuning allows rapid adaptation, often matching the performance of full fine-tuning and substantially outperforming training from scratch. This is a practical advantage for deployment where fine-tuning encoder weights may be costly.

6. **Broad evaluation across 65 tasks and 13 datasets with statistical rigor.** The evaluation covers locomotion, navigation, and manipulation with both proprioceptive and pixel inputs from ExoRL (DMC) and OGBench. The probability-of-improvement analysis (Figure 2) with bootstrap confidence intervals goes beyond simple point estimates.

## Weaknesses

### Fatal
None.

### Major
None. The paper's core contributions are solid and well-supported by theory and experiments.

### Minor

1. **Asymmetric encoder design shows marginal empirical benefit over the simpler symmetric variant.** The paper's own ablation (Figure 3, right; Section 6) reports that the symmetric variant "performs comparatively rather well, while relying on a single predictor-encoder pair. However, using distinct state and task embeddings tends to improve empirical performance more often than not" (lines 286-287). This is honest but weak evidence for what the paper presents as a distinguishing architectural contribution. The asymmetric design adds substantial complexity (two encoders, two predictors, two regularization terms, four target networks) for a modest average advantage. The paper would be strengthened by analyzing specific regimes where the asymmetry matters theoretically (e.g., when state and task spaces have very different dimensionalities or structure).

2. **Performance gains are concentrated in pixel-based settings; proprioception results are competitive but not dominant.** In DMC (proprioception), TD-JEPA's advantage over FB is modest (661.2 vs 648.2). In OGBench (proprioception), TD-JEPA ties HILP (37.98 each) and trails FB (39.04). Some individual-task gaps are notable and undiscussed: e.g., antmaze-me (proprioception) yields TD-JEPA 20.20 vs FB 51.60 (line 229) — a 2.5× gap. The paper's "matches or outperforms" claim is directionally correct in aggregate, but the advantage is clearly domain-dependent. The paper would benefit from explicitly characterizing the regimes where TD-JEPA helps and where it does not.

3. **Baseline comparison protocol mixes architectural and algorithmic contributions.** The paper adds an explicit state encoder to all baselines (line 247), reporting that this alone improves their performance by factors of 1.3×–2.4× over published results (line 271). Methods marked with an asterisk (BYOL\*, BYOL-γ\*, ICVF\*) are representation-learning methods whose instantiation in a zero-shot framework is novel (line 251), not established zero-shot algorithms. While the asterisk notation is transparent, the main empirical framing compares TD-JEPA against these augmented, re-purposed baselines. Reporting original unmodified baseline numbers alongside the enhanced ones would cleanly separate what each contribution buys.

4. **Theoretical guarantees rely on strong assumptions with a non-trivial gap from practice.** Theorems 1-4 assume linear predictors, uniform state distribution (A2), symmetric transition kernels (A3), and identity covariance (A1). The paper acknowledges these "can be relaxed" (line 157) and honestly notes the gap, but the practical algorithm relies on explicit orthonormality regularization, target networks, and EMA updates that do not appear in the theory. The theory validates the conceptual design of the loss but does not provide guarantees about the practical algorithm. This gap is typical for latent-predictive representation theory (Tang et al., 2023; Voelcker et al., 2024) and is not a fatal issue, but it limits the practical force of the theoretical claims.

### Trivial
None.

## Nice-to-Haves

- Report original unmodified baseline numbers alongside the enhanced ones to cleanly separate the benefit of TD-JEPA's method from the benefit of adding an explicit state encoder to everything.
- Analyze specific task properties (e.g., state vs. task dimension mismatch, reward nonlinearity, data coverage) that correlate with when the asymmetric design helps vs. hurts empirically.
- Provide an empirical analysis of reward projection error (how well ψ captures benchmark reward functions) to complement Theorem 4's theoretical bound.
- Report computational cost (wall-clock time, parameter counts) given the method trains five networks with four target networks.
- Discuss the antmaze-me (proprioception) gap to understand potential limitations.

## Removed Points

None. All retained weaknesses are factually grounded in the paper and verified against specific lines/sections.

## Novel Insights

The reviews surface a revealing tension in the paper: TD-JEPA's most novel algorithmic element (the TD-based latent-predictive loss enabling off-policy learning) is convincingly supported by both theory and experiments, while its most emphasized architectural choice (asymmetric encoders) is empirically marginal — the paper's own ablation shows the symmetric variant performs nearly as well. The pixel-based results are clearly the strongest evidence for acceptance, and they address a genuinely hard problem. The theoretical gradient-matching analysis (Theorems 1 and 3) is a meaningful advance that subsumes several prior analyses in a unified framework.

## Suggestions

1. Add a discussion section analyzing where TD-JEPA excels vs. struggles (e.g., why antmaze-me proprioception fails compared to FB).
2. Include a supplementary table of original (unmodified) baseline numbers to let readers cleanly separate architectural from algorithmic contributions.
3. Either provide stronger evidence that the asymmetric design matters in specific regimes or temper its emphasis as a contribution.
4. Report computational cost to help practitioners assess the trade-off.

## Score and Decision

Based on my assessment of the paper against ICLR standards:

The paper makes a clear algorithmic contribution (off-policy TD latent-predictive loss), backs it with novel theoretical analysis (gradient-matching theorems that generalize prior results), and provides extensive empirical validation with the strongest results in the most challenging setting (pixel-based zero-shot RL). The weaknesses identified are real but minor: the asymmetric encoder benefit is marginal, but this is honestly reported; the baseline comparison is transparent; the theory assumptions are strong but standard for this line of work. None of the weaknesses threaten the core claims.

The paper is clearly above the acceptance threshold. It is not a 10 (groundbreaking, flawless) — the asymmetric design is overclaimed relative to its evidence, and the domain-dependent performance pattern could be better characterized. But it is comfortably above the borderline.

**Score: 7.5** — solid accept. The paper brings sufficient value to the community through its algorithmic contribution, theoretical analysis, and empirical results on a challenging problem.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>