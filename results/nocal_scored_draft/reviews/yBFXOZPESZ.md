Now let me write the final consolidated review.

---

## Summary

This paper introduces Ano, an optimizer that decouples update direction from magnitude: momentum sign provides directional smoothing while the instantaneous gradient norm scales the step size, with a modified Yogi-style second-moment estimate for variance adaptation. The goal is improved robustness in noisy/non-stationary regimes (especially RL). The paper provides a non-convex convergence rate of $\tilde{\mathcal{O}}(K^{-1/4})$ and evaluates Ano across CV, NLP, and RL, with the strongest gains appearing in RL.

## Strengths

- **Well-motivated direction-magnitude decoupling.** The paper identifies a concrete mechanism by which Adam degrades in noisy settings — momentum coupling conflates direction and magnitude, so a noise spike that perturbs the magnitude also corrupts the directional signal. The proposed fix (momentum sign for direction, instantaneous gradient norm for scale) is clean, intuitive, and directly addresses the stated problem. This is the paper's core intellectual contribution, clearly explained in Section 3.

- **Consistent and often large RL improvements.** In MuJoCo SAC (Table 4), Ano achieves mean rank 1.4 (default) and 1.6 (best version) across five environments, outperforming Adam, Adan, Lion, RMSprop, and Grams with approximately 9–10% higher normalized average. The Atari PPO results (Table 5) show a similar pattern: Ano ranks first with a 6–10% higher normalized average than the next-best method, with results reported using 95% CIs and 10 seeds — meeting RL best-practice standards.

- **Hyperparameter robustness evidence.** Figure 3 demonstrates that Ano's performance on the HalfCheetah proxy is less sensitive to learning rate and momentum coefficient choices than Adam. This is a genuine practical advantage, especially in RL where hyperparameter tuning is expensive.

- **Honest scope delimitation.** The paper repeatedly and clearly states that CV and NLP experiments serve as "diagnostic checks" rather than attempts to claim superiority. The limitations section (Section 8) candidly acknowledges that Ano can be unstable in stationary settings and that Adam sometimes performs better in long-horizon supervised training, which makes the RL claims more credible.

## Weaknesses

### Fatal
None.

### Major

- **Convergence theory does not cover either proposed algorithm.** The proof (Section 5.1, line 102) assumes $\beta_{1,k} = 1 - 1/\sqrt{k}$, but Ano uses a **constant** $\beta_1 = 0.92$ (line 84) and Anolog uses $\beta_{1,k} = 1 - 1/\log(k+2)$ (line 90). Neither matches the theoretical assumption. The ablation (Table 6) confirms that the theoretically analyzed variant (Ano log k with $1 - 1/\sqrt{k}$, DRL score 8750) empirically underperforms Ano (score 10520), creating a disconnect where the variant with theoretical coverage is empirically weaker while the best empirical variant lacks theoretical support. The paper needs to either provide convergence guarantees for the actual algorithms or be explicit about this gap rather than claiming the theory applies to Ano/Anolog as stated.

- **GLUE benchmark table contains a labeling error.** In Table 3, the optimizer "Adam" appears twice in both the Default section (lines 189–190) and the Tuned section (lines 196–197) with different scores. Since Adan and RMSprop are used in other experiments but absent from the GLUE table, one of the duplicate entries is almost certainly mislabeled. This renders a key experimental table partially uninterpretable and must be corrected.

### Minor

- **Inconsistency between algorithm pseudocode and mathematical description.** Algorithm 1 (line 60) specifies the update as $g_k \cdot \text{sign}(m_k)$, while the mathematical description (Eq. 74) uses $|g_k| \cdot \text{sign}(m_k)$. These are not equivalent when the gradient and momentum disagree on sign. The text (line 66) clearly states the intended design ("replaces the momentum magnitude with the instantaneous gradient norm $|g_k|$"), so the pseudocode appears to contain a typo ($g_k$ instead of $|g_k|$). However, the discrepancy must be resolved so readers know what was actually implemented.

- **Table 1 (CIFAR-10 noise experiment) omits 95% CIs from the main text.** The CIs are relegated to a footnote and appendix (line 131), despite this table being the primary evidence for noise robustness. These should be in the main paper.

- **Yogi is not included as a baseline in main experiments.** Ano's second-moment update directly extends Yogi (Yogi + $\beta_2$ decay factor), yet Yogi is absent from the main experimental tables — it appears only in the ablation as "YogiTweaked." Given the close relationship, readers would benefit from seeing how Ano compares to standard Yogi with matched hyperparameters to isolate the benefit of the modification.

- **Grams' anomalously low performance at $\sigma=0$ is unexplained.** In Table 1, Grams achieves only 71.34% at $\sigma=0$, roughly 10 points below Ano (82.10%), Adam (80.67%), and Lion (81.04%). While the paper hypothesizes about Grams' improvement with noise, it does not address this baseline degradation.

### Trivial
None.

## Nice-to-Haves

- Report wall-clock training throughput to complement the sample-efficiency claims (Ano reaching Adam's final performance in 50–70% fewer steps).
- Explicitly state the learning rate schedule used in each experimental domain (the theory uses $\eta_k = \eta/k^{3/4}$, but it is unclear what schedule the experiments use).

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Convergence rate comparison "misleadingly framed":** Removed because the paper already addresses this at line 114: "our $\tilde{\mathcal{O}}(K^{-1/4})$ rate stems from a fundamental limitation of sign-based methods: ensuring stable updates requires decaying step sizes $\eta_k = \mathcal{O}(k^{-3/4})$ which, in turn, constrains the overall convergence rate." The paper does acknowledge the source of the rate gap.
- **Missing learning rate schedule / appendix content:** Removed per policy (the parser strips appendices; these details exist in the original submission).
- **Formatting nitpicks and speculation about unavailable resources:** Removed per policy.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Resolve the convergence theory gap: either prove convergence for constant-$\beta_1$ Ano or the logarithmic Anolog schedule, or clearly state that the theory covers a related idealized schedule while the empirical results stand on their own.
2. Fix the duplicated "Adam" entries in Table 3 with correct optimizer labels.
3. Correct Algorithm 1 to use $|g_k| \cdot \text{sign}(m_k)$ consistently with Eq. (74) and the surrounding text.
4. Move the 95% CIs for Table 1 into the main paper.
5. Include Yogi as a baseline in the main experiments.
6. Report wall-clock throughput to substantiate the sample-efficiency claims.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>