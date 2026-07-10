## Summary

The paper introduces Ano, a first-order optimizer that decouples update direction (from momentum sign) and magnitude (from instantaneous gradient norm), along with Anolog (a variant with a logarithmic momentum schedule). It provides a non-convex convergence guarantee (Õ(K^{-1/4})), a noise-robustness experiment, and evaluations across CV, NLP, and RL. The main empirical contribution is in RL, where Ano shows consistent and meaningful gains over Adam, Lion, Adan, and Grams.

## Strengths

- **Strong and consistent RL results.** On MuJoCo SAC (Table 4), Ano achieves mean rank 1.4 and normalized average 99.48 vs. Adam's 90.66. On Atari PPO (Table 5), Ano's normalized average is 95.99 vs. Adam's 87.54. The advantage holds across both off-policy and on-policy RL, 10 environments, and Figure 2 shows Ano reaches Adam-level performance in 50–70% fewer steps. The hyperparameter robustness analysis (Figure 3) further supports that gains are not solely due to better-tuned defaults.

- **Well-designed ablation study (Table 6).** The ablation systematically isolates each design choice — second-moment rule, gradient norm, momentum norm, momentum direction, decoupled weight decay, and momentum schedule — across four benchmarks. The comparison AnoWoTweak (plain Yogi second moment) vs. full Ano isolates the effect of the Yogi+β₂-decay, and Signum vs. Ano isolates the contribution of gradient magnitude. This is more thorough than most optimizer ablation studies.

- **Honest scope framing.** The paper explicitly states that CV and NLP experiments are "diagnostic checks" (Section 6), not claims of superiority. The limitations section (Section 8) acknowledges that Ano favors larger step sizes which can cause instability and that stationary supervised settings may be better served by Adam. This calibrated framing is a genuine strength.

## Weaknesses

### Major
- **The claimed β₂-decay modification to Yogi is not specified in the main text.** Lines 16 and 76 state that the paper "introduce[s] an additional decay factor" to Yogi, but the only explicit equation shown (Eq. 4, line 78) is standard Yogi (Zaheer et al., 2018). The ablation (Table 6) attributes a ~16% DRL improvement to "Yogi+β₂-decay" vs. plain Yogi, and the limitations section (line 321) refers to "the choice of β₂-decay" as if it is defined — yet no equation or reference to where the modified update is defined appears in the main text. The paper should at minimum cite the appendix location where this modification is specified, or provide the modified equation inline.

### Minor
- **Algorithm pseudocode does not match the formal update equation.** Algorithm 1 (line 60) specifies `x_{k+1} = x_k - η/√(v̂_k+ε) · g_k · sign(m_k)`, while Equation (3) (line 74) specifies `x_{k+1} = x_k - η/(√v_k+ε) · |g_k| · sign(m_k)`. These are mathematically different: `g_k·sign(m_k)` equals `|g_k|·sign(m_k)` only when gradient and momentum agree in sign, and produces the opposite direction when they disagree. Since the text (line 66) and Eq. (3) consistently describe the intended update as using `|g_k|·sign(m_k)`, the pseudocode likely contains a typo. The paper must clarify which update was actually implemented.

- **Convergence theory covers a different momentum schedule than recommended.** The theory (Section 5.1, line 102) assumes β_{1,k}=1-1/√k (square-root schedule), which is neither Ano's recommended fixed β₁=0.92 nor Anolog's logarithmic schedule β_{1,k}=1-1/log(k+2). The configuration with proven convergence empirically underperforms in Table 6 (DRL 8750 vs. Ano's 10520). While this gap is common in optimizer papers and the paper is transparent about the rate being Õ(K^{-1/4}), it weakens the connection between theory and practice.

- **Table 3 (GLUE) has an unexplained duplicate "Adam" row.** Both the Default and Tuned panels contain two rows labeled "Adam" with different scores (e.g., Default: 59.40 vs. 55.65 on CoLA). The paper provides no explanation of what distinguishes these rows, undermining interpretability.

- **Table 6 schedule naming is confusing.** The row "Ano √k" uses β₁=1-1/k (harmonic schedule) while "Ano log k" uses β₁=1-1/√k (square-root schedule). The names and formulas appear swapped relative to conventional naming.

### Trivial
- None beyond the table labeling issues noted above.

## Nice-to-Haves

- Adding a Yogi baseline to the RL experiments would help attribute gains specifically to the direction-magnitude decoupling vs. the second-moment choice.
- Presenting the 95% CIs for the noise robustness experiment (Table 1) inline rather than deferring them to the appendix would strengthen a central supporting experiment.

## Removed Points

These points from the input review were removed with justification:

- **"The algorithm/equation mismatch is a structural/fatal issue"**: Demoted to Minor because the text (line 66) and equation (Eq. 3) consistently describe the intended update (`|g_k|·sign(m_k)`); the pseudocode discrepancy is a presentation inconsistency, not a conceptual flaw. The core design motivation (decoupling direction and magnitude) is correctly stated and equation-supported.

- **"The convergence theory covers a variant that empirically fails"**: The theory honestly acknowledges the Õ(K^{-1/4}) rate and its assumptions. The gap between theoretical and recommended schedules is standard practice in optimizer papers (e.g., Lion's convergence proof uses different assumptions than its recommended configuration). Not a fatal issue.

- **Generic speculation about confounders and metric validity**: Removed per filtering rules — these were area-of-concern sweeps without specific anchors in the paper.

- **Missing Yogi baseline in RL, formatting/style nitpicks**: Removed per hard rules (formatting issues are parser artifacts; Yogi is not a standard RL baseline).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the pseudocode** (Algorithm 1, line 60): replace `g_k·sign(m_k)` with `|g_k|·sign(m_k)` to match the intended update in Eq. (3) and the text. Alternatively, if the implemented version actually uses `g_k·sign(m_k)`, explain why this is the correct form and update the text/equation accordingly.
2. **Define the β₂-decay modification** in the main text, or at minimum add a citation to the appendix equation where it is specified. Without this, the ablation's central comparison (AnoWoTweak vs. Ano) supports an unverifiable claim.
3. **Label the duplicate Adam rows** in Table 3 and fix the schedule name/formula swaps in Table 6.
4. **Add a note** explaining the theory-practice schedule gap and why convergence is expected to hold by continuity for the recommended configurations.
5. Consider adding a Yogi baseline to the RL experiments for completeness.

## Score and Decision

### Round-1 Bracket

From the first calibration pass, the closest comparable papers are in the 4.67–6.20 range: **Torque-Aware Momentum** (4.67, rejected), **SoftSignSGD (S3)** (6.20, rejected), **Do Stochastic, Feel Noiseless** (6.00, accepted), and **Adaptive Methods through SDEs** (7.00, accepted). The Ano paper sits between TAM and S3/μ²-SGD — it has stronger empirical evidence than TAM (which had marginal gains of ~0.1% on ImageNet and no convergence proof) but more presentation issues than the accepted theory papers. The initial bracket is **[5.5, 7.0]**.

### Round-2 Narrowing

Itemized comparison with **SoftSignSGD (S3)** (avg 6.20, rejected) — the most relevant anchor as both are sign-inspired optimizer papers with theory and experiments. S3's strengths have favorabilities 9.6–12.7 (ablation = 13.4, experiments = 12.7); its weaknesses have favorabilities mostly 1–5 (e.g., unclear component contributions at 1.6, typos at -1.8). Ano's strengths have similar favorabilities (RL results 10.4–10.9, ablation 12.4, honest scope 11.1); Ano's weaknesses have favorabilities 0.05–3.2. The key differentiator: S3's most damaging weakness (favorability -3.22, concerning Nesterov acceleration) is about an inflated claim, while Ano's most damaging weakness (favorability 0.47, undefined β₂-decay) is about an omission that is likely fixable from the appendix. Ano also has more favorable items overall (fewer items below 1.0). **However**, S3's top weakness has favorability 1.6 while Ano's top weakness has 0.47 — suggesting Ano's presentation issues are more distracting.

**Final score: 6.0**. The paper's core contributions (RL results, ablation design, honest scope) are real and well-supported. The weaknesses are addressable — the pseudocode is an inconsistency (not a fatal flaw), the β₂-decay definition is likely in the appendix, and the theory-practice gap is common. With revisions to fix the presentation issues, this would be a solid paper. The score positions it slightly below S3's average (6.20) because the undefined β₂-decay and pseudocode inconsistency make the method harder to evaluate than S3, but above TAM (4.67) because the empirical evidence is substantially stronger and a convergence proof is provided.

### Calibration Anchors Used

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/.../aF1jasJeRy.md (TAM) | 4.67 | R1 | Yes | Weaker: marginal improvements, no proof |
| /home/.../TBJCtWTvXJ.md (S3) | 6.20 | R1, R2 | Yes | Comparable: sign-based optimizer, similar theory/experiments, but fewer presentation issues |
| /home/.../zCZnEXF3bN.md (μ²-SGD) | 6.00 | R1, R2 | Yes | Different focus: theory-heavy, weaker experiments |
| /home/.../ww3CLRhF1v.md (Adaptive SDEs) | 7.00 | R1 | No | Higher: pure theory paper with rigorous analysis |
| /home/.../zfeso8ceqr.md (Deconstructing) | 6.00 | R2 | Yes | Different: empirical study, not new optimizer |
| /home/.../CYa4FKjYM9.md (NGN Step-size) | 6.00 | R2 | No | Comparable: optimizer stability focus |

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>