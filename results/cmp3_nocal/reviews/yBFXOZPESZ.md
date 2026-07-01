Now let me finalize the review.

## Summary

This paper proposes Ano, a new optimizer that decouples update direction (using the sign of momentum) from update magnitude (using the instantaneous gradient norm), along with an extension Anolog that uses a logarithmic β₁ schedule. The paper provides non-convex convergence guarantees (Õ(K^{-1/4})) and empirically evaluates the method across CV (CIFAR-100), NLP (GLUE), and RL (MuJoCo SAC, Atari PPO), with the strongest gains appearing in the high-noise, non-stationary RL setting.

## Strengths

- **Well-motivated and clean design principle (Sections 1, 3).** The core idea of decoupling direction (momentum sign for stability) from magnitude (instantaneous gradient norm for responsiveness) is clearly motivated by diagnosing a limitation of Adam's coupled update in noisy regimes. The decomposition of Adam's update into |m_k|·sign(m_k) is pedagogically effective.

- **Consistently strong RL results with proper statistical methodology (Section 6.3, Tables 4-5, Figure 2).** Using 10 seeds, 95% CIs, and IQM metrics following Agarwal et al. (2021), Ano achieves mean rank 1.4 across 5 MuJoCo environments (SAC) and rank 2.2 across 5 Atari games (PPO). The improvements are substantial and consistent across two distinct RL algorithms and multiple environments.

- **Hyperparameter robustness analysis (Figure 3).** The head-to-head comparison of Ano vs. Adam across learning rate and β values on the HalfCheetah proxy shows Ano maintaining high reward over a substantially wider range of hyperparameters, demonstrating a genuine practical advantage not explained by cherry-picked settings.

- **Honest framing and clear limitations (Sections 6, 8).** The paper explicitly frames CV and NLP experiments as "diagnostic checks" rather than competitive evaluations. The Limitations section identifies three concrete weaknesses: the β₂-decay design helps RL but not supervised learning, larger step sizes can cause instability, and large-scale CV/NLP remains untested.

## Weaknesses

### Fatal
None.

### Major

- **Discrepancy between pseudocode and mathematical description of the core update (Section 3, Algorithm 1 line 60 vs. Equation at line 74).** The pseudocode gives `x_{k+1} = x_k - η_k/√(v̂_k+ε) · g_k · sign(m_k)`, while the mathematical description gives `x_{k+1} = x_k - (η_k/(√v_k+ε)) |g_k| · sign(m_k)`. These differ in more than notation: when g_k and sign(m_k) disagree in sign, `g_k · sign(m_k)` has the sign of g_k while `|g_k| · sign(m_k)` has the sign of sign(m_k). For example, when g_k = -5 and sign(m_k) = -1 (both negative, agreeing on direction), the pseudocode produces `-η·(-5)·(-1) = -5η` while the mathematical description produces `-η·5·(-1) = +5η` — opposite directions. Since the paper's central claim is that the update follows sign(m_k) for directional stability, the authors must clarify which formulation was actually implemented and ensure the pseudocode, equations, and source code agree. This does not invalidate the empirical results — the text formula is the clearly explained and intended formulation — but it makes the core algorithmic specification ambiguous.

- **Convergence theory does not directly apply to the evaluated algorithms (Section 5.1 vs. Sections 3-4).** The theoretical analysis assumes β₁,k = 1 - 1/√k (square-root schedule) and η_k = η/k^{3/4}. However, Ano (the main evaluated algorithm, line 84) uses constant β₁ = 0.92, and Anolog (line 90) uses β₁,k = 1 - 1/log(k+2). Neither matches the square-root schedule or the k^{-3/4} learning rate decay assumed in the proof. The theory therefore proves convergence for a variant that was not empirically evaluated. The authors should either frame the theory as analyzing a related variant with evidence of qualitatively similar behavior, or extend the analysis to the actual schedules used.

### Minor

- **Mislabeled schedules in the ablation table (Table 6, lines 311-313).** Per the paper's own definitions (Section 4), the square-root schedule is β₁,k = 1 - 1/√k and the harmonic schedule is β₁,k = 1 - 1/k. However, row "Ano √k" lists β₁,k = 1 - 1/k (harmonic) while "Ano log k" lists β₁,k = 1 - 1/√k (square-root). Only "Analog" with 1 - 1/log k is correct. The names and formulas are swapped, making it impossible to determine which schedule produced which result. The authors should correct these labels.

- **Duplicate optimizer label in GLUE table (Table 3, line 190).** The "Default" section shows two rows labeled "Adam" with different scores. One of these appears to be mislabeled for a different optimizer, making the table difficult to interpret.

- **Second-moment estimate can become negative without discussion (Section 3, line 78).** The Yogi-style update v_k = β₂ v_{k-1} - (1-β₂)·sign(v_{k-1} - g_k²)·g_k² can produce negative values for v_k when β₂ v_{k-1} < (1-β₂)·g_k². The paper does not explain how √(v̂_k+ε) handles this case (clipping? absolute value?), even though this matters for correctness of the step-size computation.

- **Baseline collapses in default RL comparisons (Table 4).** Lion achieves only 98.22 ± 32.33 on Humanoid under default settings (vs. 5357 for Adam), and Grams collapses on Hopper (1175.31 ± 927.22). While the "Best Version" comparison partially addresses this and Ano still leads there, the default comparisons inflate Ano's relative advantage partly due to poorly-performing baselines rather than Ano's strength alone.

### Trivial

- The variant name appears as "Analog" in several places in Tables 4-6 and surrounding text, while the correct name given in the paper is "Anolog." (e.g., Table 4 lines 234, 242; Table 5 lines 275, 283; Table 6 line 310)

## Nice-to-Haves

- Comparing Ano to at least one RL-specific optimization method (e.g., NaP) would better contextualize the RL results, since all current baselines are general-purpose optimizers.
- An empirical analysis of how often g_k and sign(m_k) disagree during training, and how each formulation of the update behaves in those cases, would directly test the claimed decoupling mechanism.

## Removed Points

The following points from the harsh critic review were removed with justification:
- **Reproducibility concern about missing code/contradictory release statement**: Per hard rules, we do not question the existence or availability of cited artifacts. The paper states the code and pip package exist.
- **Missing related works**: Per hard rules, we do not mention missing related works.
- **Assertion that Issue 1 is fatal**: Demoted to Major. The discrepancy is real and requires clarification, but the intended algorithm is clearly explained in the text, the empirical results are unaffected, and the issue is resolvable. A fatal flaw must be unambiguous from the paper as written.
- **"Ano √k" catastrophic failure narrative**: The attribution of collapse to β₁,₁ = 0 alone is speculative oversimplification; the empirical failure is correctly reported regardless of cause.
- **Generic evaluation rigor concerns**: Removed as they lacked concrete anchors to specific paper content.
- **Table 6 readability and formatting complaints**: The table is dense but functional; this is a presentation preference issue.
- **"Strengthening the Paper on Its Own Terms" suggestions**: These were either merged into Nice-to-Haves or already addressed by retained weaknesses.
- **"Grad. Norm." and "Mom. Norm." simultaneously checked**: The reviewer's confusion here reflects a misunderstanding of the table legend, which shows component ablation.

## Novel Insights

The harsh critic's observation that the pseudocode `g_k · sign(m_k)` and the text `|g_k| · sign(m_k)` produce different results when g_k and sign(m_k) disagree is a genuinely useful insight that goes beyond the paper's own analysis. The paper explains the decoupling conceptually but never examines this corner case. If the authors intended `|g_k| · sign(m_k)` (as the text suggests), the pseudocode is simply wrong. If they intended `g_k · sign(m_k)` (as the pseudocode suggests), the decoupling claim needs re-framing because the update would no longer consistently follow sign(m_k) for direction. This ambiguity is the single most important issue for the authors to resolve.

## Suggestions

1. **Resolve the pseudocode/text discrepancy immediately.** State which update rule matches the implementation. If the text formula (`|g_k| · sign(m_k)`) is correct, fix the pseudocode. If the pseudocode (`g_k · sign(m_k)`) was actually used, explain how the decoupling claim should be understood given that the update does not always follow sign(m_k).
2. **Correct the ablation table labels** so that the β₁,k formulas match their row names.
3. **Fix the duplicate "Adam" label** in Table 3 (determine which optimizer the scores correspond to) and the "Analog" → "Anolog" typo throughout.
4. **Either match the theory to the evaluated schedules** or explicitly frame the theory as analyzing a related variant, with supporting evidence that the convergence behavior is qualitatively similar.
5. **Add a brief note** about how the Yogi-style v_k update handles potentially negative values before the square root is applied.

## Score and Decision

The paper presents a well-motivated optimizer with a clean design principle and the strongest RL optimization results I have seen in a single paper, supported by proper statistical methodology. The core issues are (a) resolving the ambiguity between the pseudocode and the mathematical description of the update, and (b) clarifying how the theoretical analysis relates to the evaluated algorithms. Neither issue undermines the empirical findings — the intended algorithm is clear from the text explanation, and the RL results speak for themselves. With the identified corrections, this paper would make a solid contribution. I recommend conditional acceptance pending clarification of the algorithmic specification.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>