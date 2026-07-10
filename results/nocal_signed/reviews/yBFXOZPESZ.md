## Summary

The paper proposes Ano, a new optimizer that decouples update direction (from momentum sign) from update magnitude (from instantaneous gradient norm), targeting improved robustness in noisy and non-stationary optimization landscapes such as reinforcement learning. A secondary variant, Anolog, replaces the fixed momentum coefficient with a logarithmic schedule. The paper provides RL experiments (SAC on MuJoCo, PPO on Atari-5), noise-robustness diagnostics, and a non-convex convergence analysis.

## Strengths

- **Clean noise-robustness experiment (Section 5.2, Table 1).** Synthetic gradient-noise injection on CIFAR-10 directly tests the core claim while controlling for all other variables. The widening accuracy gap between Ano and Adam as σ increases (from −1.43 to −7.08 points) provides the cleanest mechanistic evidence that the decoupling design works as intended.

- **Strong RL results with proper statistical practices (Section 6.3, Tables 4–5).** SAC on 5 MuJoCo tasks with 10 seeds and IQM+CI95 reporting shows Ano achieving the best mean rank (1.4 default, 1.6 best-version) and the highest normalized average across all baselines. PPO-on-Atari-5 independently replicates this pattern. Ano consistently places within or near the CI of the best baseline even on tasks where it does not rank first, which suggests the gains are genuine and not cherry-picked.

- **Thorough ablation (Table 6).** The ablation disentangles the contribution of each component (sign-magnitude decoupling, second-moment rule, gradient vs. momentum norm) across four benchmarks. The comparison of Ano (Yogi+β₂-decay) vs. AnoWoTweak (plain Yogi) attributes roughly 15% of the DRL gain to the β₂-decay specifically—informative and well-designed.

- **Honest scope calibration.** The paper explicitly frames CV and NLP experiments as "diagnostic checks" to verify Ano does not break in stable regimes rather than claiming superiority. The limitations section (Section 8) candidly acknowledges instability risks from larger step sizes and the restricted relevance of β₂-decay to stationary settings.

## Weaknesses

### Fatal
None.

### Major

- **Inconsistency between the mathematical description and algorithm pseudocode.** The text (line 74) and core motivation describe the update as `|g_k|·sign(m_k)` — direction always from momentum sign, magnitude always from the instantaneous gradient norm. However, Algorithm 1 (line 60) writes `g_k·sign(m_k)`. These differ when `sign(g_k) ≠ sign(m_k)`: the pseudocode produces `−|g_k|`, moving parameters opposite to `sign(m_k)`. The reader cannot determine which version was evaluated, making the paper's central claim ambiguous. If the pseudocode is correct, the optimizer does not do what the paper says it does. If the description is correct, the pseudocode has a substantive error. This must be clarified.

- **Theoretical analysis does not apply to either proposed algorithm.** The convergence proof (Section 5.1) assumes `β_{1,k} = 1−1/√k` and `η_k = η/k^{3/4}`, but Ano uses a fixed `β₁=0.92` and Anolog uses `β_{1,k}=1−1/log(k+2)`. Neither matches the theory. The ablation compounds this with confusing labels: "Ano √k" uses `1−1/k` (harmonic), and "Ano log k" uses `1−1/√k` (square-root, swapped). The variant that matches the theory scores 8750 on HalfCheetah — notably worse than Ano (10520) and Anolog (9472.73). The convergence guarantee as presented provides no evidence about the behavior of either proposed algorithm. The paper should either re-prove convergence for the actual algorithms or clearly frame the theorem as applying to a related family, not to Ano/Anolog directly.

### Minor

- **Anolog's value proposition is not convincingly demonstrated.** Anolog underperforms Ano with fixed default β₁=0.92 across every experiment. Since Ano's default already requires no tuning of β₁, Anolog does not demonstrably reduce tuning burden; it simply offers a different fixed choice that performs consistently worse. The paper does not show any scenario where Anolog outperforms Ano, which would be necessary to establish its claimed practical advantage.

- **GLUE table (Table 3) contains duplicate "Adam" rows** in both Default and Tuned sections with substantially different numbers (e.g., CoLA 59.40 vs. 55.65, Average 82.64 vs. 80.62). It is unclear which configuration corresponds to which baseline. This is a presentation error; however, Ano's average (82.92) exceeds both rows, so the overall comparison direction is unaffected.

- **Ablation table naming is inconsistent with formulas.** In Table 6, "Ano √k" uses `1−1/k` (harmonic schedule) and "Ano log k" uses `1−1/√k` (square-root schedule). These labels are swapped relative to their actual schedule forms, making the table confusing and misaligned with the prose description of the schedule comparisons.

### Trivial
None.

## Nice-to-Haves

- A fully symmetric comparison of Ano (tuned) vs. baselines (tuned) on the RL benchmarks would strengthen the "best version" analysis, though the current framing already addresses this fairly.
- Wall-clock timing data would confirm the step-count speedup claim, though per-step costs are nearly identical to Adam's.

## Removed Points

The following points raised in the original harsh review are removed with justification:

- **Concern about pip package / code release status**: Removed per policy — the paper cites the package; questioning its existence is not permitted.
- **Request for ImageNet-scale experiments**: Removed — the paper explicitly scopes large-scale CV/NLP as future work.
- **Request for wall-clock timing**: Removed — not a standard requirement given near-identical per-step cost; step-count comparisons are provided.
- **Speculation about v_k approaching zero**: This is a theoretical observation without demonstrated empirical impact in the paper; too speculative to retain as a weakness.
- **Criticism of hyperparameter sensitivity axis labels**: The figure caption is unclear, but the axis semantics cannot be verified from the embedded image alone.
- **Convergence rate being O(K^{-1/4}) vs. Adam's O(K^{-1/2})**: The paper explicitly acknowledges and explains this as a known limitation of sign-based methods (line 114). This is candid disclosure, not a weakness.
- **Section-by-section observations on the v_k update, Grams' low-noise improvement, etc.** : These are observations, not actionable weaknesses.

## Novel Insights

None beyond the paper's own contributions. The reviews raise no observation about the paper's mechanism or empirical patterns that the paper itself does not already discuss.

## Suggestions

1. **Resolve the `|g_k|` vs. `g_k` inconsistency.** Align Algorithm 1 with the mathematical description. If `g_k·sign(m_k)` is actually used, explain why and how this differs from the claimed mechanism, and correct the text.
2. **Clarify the scope of the theoretical analysis.** Either prove convergence for the actual Ano (fixed β₁) and Anolog (log schedule), or clearly frame the theorem as a proof for the `1−1/√k` scheduled variant (currently mislabeled "Ano log k") rather than for the proposed algorithms directly.
3. **Fix the duplicate "Adam" rows in Table 3** by distinguishing configurations (e.g., Adam vs. AdamW, different learning rates, or different β₂ values).
4. **Correct the swapped ablation labels** in Table 6: "Ano √k" (uses `1−1/k`) and "Ano log k" (uses `1−1/√k`) should be renamed to match their actual formulas.
5. **Reconsider Anolog's framing** — either demonstrate a scenario where it provides a practical advantage over default Ano, or acknowledge that it is a worse-performing variant introduced for theoretical completeness rather than practical benefit.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>