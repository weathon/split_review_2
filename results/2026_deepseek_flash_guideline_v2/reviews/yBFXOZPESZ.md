Good — this confirms the key finding. The critic's "critical" claim #2 is based on a misreading of Table 6. The √k schedule (1-1/√k) achieves DRL 8750, NOT the catastrophic -221.45 claimed by the critic. The failing schedule is 1-1/k (harmonic), which is a different schedule entirely.

Now let me produce the final consolidated review.

---

## Summary

This paper proposes Ano, a per-parameter optimizer that decouples update direction (taken from the momentum sign) from update magnitude (taken from the instantaneous gradient norm), along with a variant Anolog using logarithmic momentum scheduling and a Yogi-based second-moment update with β₂ decay. The design targets noisy/non-stationary optimization landscapes. The paper provides non-convex convergence guarantees (Õ(K^{-1/4})), and evaluates empirically across CV (CIFAR-100), NLP (GLUE), and RL (MuJoCo SAC, Atari PPO), with the strongest gains in RL.

## Strengths

1. **Controlled noise-injection experiment shows monotonic benefit (Table 1, Section 5.2)**: Gaussian noise is injected at five levels (σ=0 to 0.20). Ano's accuracy advantage over Adam grows monotonically from 1.43pp to 7.08pp, and over Lion from 1.05pp to 2.72pp. This systematic sweep directly supports the claim that direction–magnitude decoupling becomes more valuable as gradient noise increases.

2. **Strong RL results with statistical rigor (Table 4, Figure 2, Section 6.3)**: On SAC/MuJoCo with 10 seeds and IQM+95%CI reporting, Ano achieves mean rank 1.4 (default) and normalized average 99.48%, outperforming Adam (rank 3.4, 90.66%), Lion (4.4, 71.74%), Grams (6.4, 65.88%), and Adan (5.6, 78.38%). Ano also reaches Adam's final performance with 50–70% fewer training steps. These gains replicate on Atari PPO (Table 5, mean rank 2.2 default vs 4.4 Adam).

3. **Hyperparameter robustness evidence (Figure 3, Section 6.3)**: Heatmaps comparing Ano and Adam across learning rate and momentum values show Ano maintains high reward across a substantially wider region, addressing concerns about cherry-picked hyperparameters.

4. **Convergence analysis with honest discussion of limitations (Section 5.1)**: The paper provides a non-convex convergence rate of Õ(K^{-1/4}) and explicitly acknowledges this is worse than Adam's O(K^{-1/2}) due to the step-size constraint required by sign-based methods.

5. **Systematic ablation isolating each component (Table 6, Section 7)**: 12 variants across four benchmarks show that removing gradient magnitude (YogiSignum) collapses DRL to near-random (-285.58), and removing momentum direction (SignumGrad) also collapses (53.93% CIFAR-100 vs >70%). This provides direct evidence that both halves of the decoupling are necessary.

6. **Honest scoping and limitations (Section 8)**: The paper frames CV/NLP experiments as diagnostic checks rather than claiming superiority, and candidly discusses stability concerns, the scale limitation of supervised experiments, and settings where Adam may be preferable.

## Weaknesses

### Fatal
None.

### Major

1. **Algorithm specification inconsistency between pseudocode and equation (Section 3, Algorithm 1 vs Equation 4)**: The paper's conceptual description (line 66) and equation (line 74, top of page 3) both state that Ano uses the instantaneous gradient norm |g_k| for magnitude, giving the update `|g_k|·sign(m_k)`. However, the pseudocode in Algorithm 1 (line 60) writes `g_k · sign(m_k)` without the absolute value. When sign(g_k) and sign(m_k) disagree, these two formulations produce updates in opposite directions. The text and equation consistently describe |g_k|·sign(m_k), so the intended algorithm is discernible, but the pseudocode as printed implements something different. The authors must unambiguously specify which formulation is correct and ensure Algorithm 1 matches the prose and equation. This is the most significant issue and must be resolved before the contribution can be reliably evaluated.

2. **Empirical evidence beyond RL is modest (Sections 6.1–6.2)**: The paper honestly acknowledges this, but the fact remains that the core empirical support for Ano's benefits relies almost entirely on RL experiments. On CIFAR-100, Ano is within 1% of Adam/Adan — showing non-degradation rather than improvement. On GLUE, gains are concentrated on small tasks (RTE +2.58pp, MRPC +0.90pp) within typical variance. A skeptical reader could reasonably question whether the claimed benefits generalize beyond the RL setting. Strengthening the non-RL evidence or more clearly delimiting the scope of claims would improve the paper.

### Minor

1. **Theory–practice gap (Section 5.1 vs Sections 3–4)**: The convergence proof assumes β_{1,k}=1-1/√k and η_k=η/k^{3/4}, but Ano (the primary algorithm) uses fixed β₁=0.92, and Anolog uses β₁=1-1/log(k+2). The paper acknowledges this inspiration (line 88). Notably, the 1-1/√k schedule achieves reasonable empirical results (DRL 8750, CIFAR-100 67.26% in Table 6), so the critic's claim that it "catastrophically fails" is factually incorrect (the catastrophic failure is for the 1-1/k harmonic schedule). Nevertheless, the analyzed configuration matches neither recommended variant exactly. The authors should either extend the analysis or clearly delimit the theory's scope relative to the practical recommendations.

2. **Duplicate "Adam" entries in GLUE table (Table 3, lines 189–190, 196–197)**: Both the "Default" and "Tuned" sections contain two rows labeled "Adam" with different numerical values and no distinguishing subscript or footnote. The reader cannot tell which configuration each represents. This is a clear presentation error that undermines interpretability of the main comparison table.

3. **"Best Version" presentation in RL tables (Tables 4–5)**: The paper reports per-optimizer "Best Version" by taking the max of default/tuned configurations, then uses this framing in the abstract and summary discussion. This conflates tuning advantage with algorithmic merit and is non-standard. The "Default" rows are more informative for fair comparison, and the best-version framing should be de-emphasized.

4. **Denominator inconsistency between equation and pseudocode**: The equation (line 74) uses √v_k + ε, while Algorithm 1 uses √(v̂_k + ε) with bias correction. This is a secondary inconsistency alongside the g_k vs |g_k| issue.

### Trivial

1. **Table 6 row-label confusion**: The row named "Ano √k" uses β=1-1/k (harmonic), while the row named "Ano log k" uses β=1-1/√k (square root). The names appear swapped relative to the formulas they contain, making the table harder to parse.

## Nice-to-Haves

- Adding learning rate schedule details for the CIFAR-100 experiment (only the GLUE linear schedule with warmup is specified).
- Extending the convergence analysis to cover the fixed-β₁ or log-schedule cases would strengthen the connection between theory and practice, even if at a worse rate.

## Removed Points

These points from the reviewer inputs are removed or substantially weakened after verification:

- **Critic's claim that the √k schedule "catastrophically fails"** (DRL -221.45): FACTUALLY INCORRECT. The -221.45 result is for the 1-1/k (harmonic) schedule, labeled "Ano √k" but actually using 1-1/k. The 1-1/√k schedule achieves DRL 8750 (Table 6). The paper's ablation table has confusing row labels but the formulas are unambiguous.
- **Critic's claim about ablation table being "difficult to interpret"**: The checkmark scheme is a standard binary indicator for component presence. The column headers and β₁,k formulas provide all necessary information.
- **Critic's speculation about "the V100/RTX 5090 anachronism"**: Per the Hard Rules, all cited references and hardware are treated as real. This is not a scientific concern.
- **Critic's criticism that the second-moment modification is "marginal"**: This is subjective framing, not a verifiable weakness. The ablation study (Table 6) shows performance differences between second-moment variants.
- **Strength finder claims that are generic** (e.g., "the problem is important"): Removed as they lack specific evidence or conflict with verified weaknesses.

## Novel Insights

The most interesting observation emerging from the reviews is the asymmetry in Ano's empirical profile: the controlled noise injection shows monotonic gains as noise increases (exactly what the theory predicts), yet the GLUE results show Ano's best relative performance is on the smallest, noisiest tasks (RTE with ~2.6k training examples) while it matches baselines on large stable tasks (MNLI with ~393k examples). This pattern reinforces the paper's central claim that direction–magnitude decoupling specifically helps in high-variance regimes, but it also raises the question — unanswered by the current paper — of whether Ano provides any benefit in large-scale settings where gradient variance is moderate but non-stationarity is still present (e.g., continual learning, fine-tuning across distributions).

## Suggestions

1. **Resolve the g_k vs |g_k| discrepancy** between Algorithm 1 and Equation 4. Ensure the pseudocode, prose, and equation all describe the same update. If |g_k|·sign(m_k) is correct (as the prose suggests), add the absolute value to the pseudocode.
2. **Fix the duplicate "Adam" rows** in Table 3 by adding distinguishing labels (e.g., "Adam (lr=...)" or a footnote).
3. **Clarify the theory–practice relationship**: Either extend the convergence analysis to cover fixed-β₁ or log-schedule, or explicitly state that the theory applies to a related variant and is provided as formal analysis corroborating the design direction.
4. **De-emphasize "Best Version"** in the RL presentation. Default-configuration results should be the primary comparison.
5. **Fix the swapped row labels in Table 6** so that "Ano √k" correctly uses 1-1/√k and "Ano harmonic" uses 1-1/k, or similar.
6. **Add learning rate schedule details** for the CIFAR-100 experiments.

## Score and Decision

Based on my thorough verification of the reviewer inputs against the paper, the paper makes a genuine contribution (a well-motivated optimizer design) with strong supporting evidence in its target domain (RL). The main weakness is a real but fixable algorithm specification error in the pseudocode. The critic's most serious claim (that the √k schedule empirically fails, invalidating the theory) is factually incorrect — it was the harmonic schedule that fails, not the √k schedule. The theory-practice gap exists but is modest.

The paper is above the reject threshold: the central idea is clear, the RL evidence is convincing, and the honest scoping is commendable. However, the algorithm inconsistency and the modest CV/NLP evidence prevent it from reaching a clear accept level. Score: **6**.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>