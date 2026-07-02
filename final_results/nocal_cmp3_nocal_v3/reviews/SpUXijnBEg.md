Here is my final consolidated review.

---

## Summary

This paper introduces Direct Optimal Action Learning (DOAL), a framework for extracting policies from Q-value functions in offline RL. Rather than backpropagating through the full BRAC objective, DOAL computes a single-step gradient-based target action from the data point and then learns to imitate it using efficient, policy-native behavior cloning losses (e.g., flow-matching loss). The paper also proposes a batch-normalized reparameterization of the step-size hyperparameter and identifies the importance of tuning `n_sample` in MaxQ sampling — a previously underappreciated trade-off between coverage and maximization bias. Experiments span three Q-value functions (IQL, Q-learning, ReBRAC), three policy classes (Gaussian, flow, diffusion), and two benchmarks (OGBench, D4RL).

## Strengths

1. **Clean theoretical reinterpretation of BRAC (Proposition 1).** The observation that the BRAC policy gradient is equivalent to the gradient of a squared-error loss targeting an "optimal action" is genuinely insightful. It provides a simple, principled motivation for decoupling target-action computation from the policy itself. The conceptual inconsistency the paper identifies — BRAC evaluates the Q-gradient at the policy's output rather than at the data action — is a real subtlety, and DOAL's resolution (evaluating at the data action) is well-motivated and rigorously derived.

2. **Proposition 3 on MaxQ sampling bias is a useful formalization.** The informal proposition that increasing `n_sample` leads to maximization bias from noisy Q-estimators is a practical insight. The literature has treated larger `n_sample` as uniformly better (Ghasemipour et al., 2021), and this paper correctly identifies the trade-off. This observation yields stronger baselines, which is a non-trivial empirical contribution even before evaluating DOAL itself.

3. **The framework is genuinely versatile.** DOAL is evaluated with three policy classes (Gaussian, flow, diffusion) and three Q-value functions (IQL, Q-learning, ReBRAC). The method subsumes all its baselines by setting δ=0. This structural property is elegant, and the breadth of the evaluation across 15 tasks (9 OGBench + 6 D4RL) is appropriate for a framework paper.

4. **Efficiency analysis is well-executed.** The time complexity breakdown (Figure 2) shows that DOAL adds only one extra forward+backward call through the Q-network, and the runtime regression analysis convincingly demonstrates that the overhead is modest compared to alternatives like BPTT (37 total calls for MFQL-BPTT vs. 10 for DIFQL). This is strong supporting evidence for the "efficient" part of the paper's claims.

## Weaknesses

### Fatal
None.

### Major

1. **No comparison to existing methods that also use ∇_a Q for policy extraction.** The paper compares DOAL only to baselines that do **not** use the Q-gradient (MaxQ sampling, AWR). Yet the Related Work (Section 6.2) lists QGPO (Wang et al., 2023), SFBC (Chen et al., 2023), EDA (Chen et al., 2024a), QVPO (Ding et al., 2024), and the paper's Section 6.3 discusses DAC (Fang et al., 2025) and BDPO (Gao et al., 2025) — all methods that also extract policies from Q-values using gradients. If DOAL is claimed to be "an efficient, effective, and versatile framework for policy extraction from Q value functions," it should be compared to at least one representative gradient-using method. Without this comparison, the reader cannot assess whether DOAL's simple single-step target-matching approach is competitive with classifier-free guidance or gradient-based resampling at similar computational cost. Even a comparison showing DOAL is worse-but-cheaper would be informative; the complete absence leaves a critical gap in the evaluation.

2. **The marginal improvement from DOAL over the strong baselines is modest and inconsistent, and the bulk of the gain over prior work comes from an orthogonal contribution (`n_sample` tuning).** On OGBench with IQL (Table 1), tuning `n_sample` yields a +111 point gain (IFQL* 218 → IFQL 329), while DOAL adds +30 points on top (IFQL 329 → DIFQL 359). The paper itself notes that "those [gains] are due to one or two tasks" — meaning on most tasks DOAL and baseline are within noise. On D4RL with IQL, DOAL is flat or slightly worse (IFQL 592 vs DIFQL 584). On D4RL with Q-learning (Table 2), DOAL is likewise flat (MFQL 623 vs DMFQL 614). The only setting where DOAL clearly helps is with regularized Q-learning on both benchmarks (DMFReBRAC 630 vs MFReBRAC 614 on D4RL; 466 vs 425 on OGBench). The `n_sample` tuning insight is a legitimate contribution, but the paper's framing could more clearly separate it from DOAL's marginal contribution. A reader could easily attribute the headline gains to DOAL when most are due to `n_sample` tuning.

### Minor

1. **The batch-normalizing optimizer is presented as a contribution but reduces to a fixed scalar in practice.** The paper concedes (lines 154, 329) that when gradient norms are stable — which Figure 3 shows they are — one can equivalently use a fixed scalar and "avoid the batch-normalization. The performance would be equivalent." The remaining claimed benefit is that δ is "easier to search for" than α. Table 3 shows that within OGBench, δ ranges from 0.03–0.3 (factor of ~10) versus α ranging from 10–1000 (factor of ~100), so δ is indeed more stable *within a domain*. However, δ requires per-domain tuning that spans two orders of magnitude between OGBench (0.03–0.3) and D4RL (0.0003–0.003), and the paper's own Table 3 shows the implied effective step size (δ/‖∇Q‖) still varies substantially. This weakens the claim that the batch-normalizing optimizer is a substantive methodological contribution beyond a convenient reparameterization.

2. **DOAL's effectiveness is contingent on Q-function quality, which limits its practical applicability.** The paper honestly observes that on D4RL with IQL "there is no performance gain from either DOAL model" and attributes this to "unreliability of IQL learned function gradient" (line 224). On D4RL with Q-learning, DOAL only helps with the regularized (ReBRAC) variant. This suggests that DOAL's core operation — taking a gradient step on the Q-function — only produces useful signal when the Q-function is already well-regularized. The paper acknowledges this limitation, but it substantially narrows the method's operating range.

3. **No statistical significance testing.** With 8 seeds and many overlapping error bars (e.g., on D4RL Table 1, IFQL 592 vs DIFQL 584 with similar stds), it is unclear which improvements are statistically meaningful. The paper relies on task aggregation (total scores), which conflates tasks with different scales and can mask both failures and noise-dominated results.

### Trivial
None.

## Nice-to-Haves

- A systematic analysis of *when* DOAL helps (e.g., correlation with Q-function smoothness, gradient norm magnitude, or dataset quality) would turn the paper's scattered observations into actionable knowledge.
- The role of α in the DOAL loss (Eq. 16) is unnecessary if the ablation study shows α=1 is fine. Removing it would simplify the method.
- Adding tanh output squashing (as used by ReBRAC) to flow/diffusion policies is noted as future work but could be tested directly.

## Removed Points

These points from the input review are excluded from the main weaknesses:

1. **"Suspiciously round standard deviations"** — Removed. The values (±24, ±23, etc.) may reflect genuine multi-seed variation or parsing artifacts. The paper's own explanation ("two seeds that have very low performance") accounts for large stds, and roundness alone is not a substantive criticism.

2. **"Abstract creates a misleading overall impression"** — Removed. The abstract's claims are individually true ("baseline models outperformed the previous best models" — true; "DOAL improves over strong baseline models" — true on OGBench). The phrasing is not misleading enough to warrant a separate weakness.

3. **"Proposition 1 doesn't discuss when evaluating at π_θ(s) vs. a matters"** — Removed. This demands an analysis beyond the paper's stated scope. The paper correctly identifies the conceptual difference and positions DOAL as a reasonable alternative objective.

4. **"MaxQ analysis is loosely connected to practice"** — Removed. The paper labels Proposition 3 as "Informal" and positions it as intuition. The idealized assumptions are appropriate for providing practical guidance about a trade-off.

5. **"The role of α is unclear"** — Moved to Nice-to-Haves, as the paper already addresses this in the ablation study (α=1 is fine; it is kept for consistency with prior work FQL).

6. **"Paper omits some OGBench tasks"** — Removed. The paper provides a valid reason ("as no current algorithms can work well") and is transparent about the omission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Include at least one representative gradient-using method** (e.g., QGPO or a guided-diffusion baseline) in the experimental comparison. This is the single highest-leverage improvement: it would establish whether DOAL's simple single-step target approach is competitive with more sophisticated sampling-time guidance, and it would directly address the core claim that DOAL is an effective framework for gradient-based policy extraction.

2. **Restructure the narrative** to explicitly separate the `n_sample` tuning contribution (which is valuable in its own right and deserves clear credit) from DOAL's marginal contribution. Present per-task effect sizes and a discussion of where DOAL helps versus where it is within noise.

3. **Reduce emphasis on the batch-normalizing optimizer**, presenting it as a convenient reparameterization rather than a core methodological contribution, given the paper's own admission that it reduces to a fixed scalar when gradient statistics are stable.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>