Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper introduces SWIREASONING, a training-free framework that dynamically switches between explicit (CoT) and latent (soft-embedding) reasoning based on block-wise confidence estimated from entropy trends in next-token distributions. A switch count controller further bounds the number of mode transitions to suppress overthinking. The method is evaluated on 11 benchmarks across math, STEM, coding, and general reasoning domains using 4 model scales (1.7B–32B). The core idea is clean and well-motivated, and the evaluation breadth is commendable. However, three major evidential gaps — missing variance reporting, no comparison against a naive hybrid switching baseline, and conflated token efficiency measurements — prevent the paper from convincingly demonstrating that its entropy-guided switching mechanism is the source of the reported improvements.

## Strengths

- **A clean, well-motivated method.** The core idea — switching between explicit and latent reasoning based on entropy-based confidence — is intuitive and clearly explained in Section 3.3. The asymmetric dwell window design (immediate latent→explicit switch when confidence rises, but a delay for explicit→latent) is well-justified by the differing roles of exploration and convergence.
- **Broad evaluation across models and domains.** The paper tests on 11 benchmarks (math, STEM, coding, general reasoning) across 4 model scales (1.7B–32B) from two model families (Qwen3, DeepSeek-R1-Distill). SWIR consistently achieves accuracy at or near the top in Table 1, and the pattern holds across sizes and families.
- **Reasonable hyperparameter analysis.** The ablations on window size (Table 3) and mixing coefficients (α₀, β₀ in Table 2) are systematic, and the paper acknowledges limitations (e.g., that a fixed window size is suboptimal and could be adaptive).

## Weaknesses

### Fatal
None.

### Major

- **No variance reporting despite modest accuracy gains.** The reported accuracy improvements are 0.4–2.5% absolute on individual benchmarks with a 2.17% average headline (Table 1). The paper reports no standard deviations, confidence intervals, or number of independent runs for any experiment. Given the small margins and that baselines themselves use stochastic decoding (CoT with sampling), readers cannot assess whether improvements are statistically significant or within sampling noise. This is a structural evidential gap for the paper's central accuracy claims.

- **No comparison against a naive hybrid baseline.** The paper's core contribution is that entropy-guided switching improves over either mode alone (Section 3.3). Yet the experimental design (Section 4) only compares against single-mode baselines (pure CoT, pure Soft Thinking). Without evaluating a simple hybrid — e.g., random switching at the same frequency, or fixed-block alternation — we cannot determine whether the gains come from the entropy criterion or merely from alternating between modes at all. This omission weakens the central claim of Section 3.3.

- **Token efficiency gains conflate switching with forced early stopping.** The claimed 57%–79% token efficiency improvements (Section 4.3) are driven predominantly by the switch count controller (Section 3.4), which forcibly terminates reasoning at block boundaries by injecting an answer prefix. This is functionally a form of early stopping. The paper does not compare against a simple baseline of "CoT with early stopping at the same token budget." Without this control, the efficiency improvement cannot be attributed to the hybrid reasoning mechanism itself, making the framing that "SWIREASONING improves token efficiency" potentially misleading.

### Minor

- **Unlimited-budget Cₘₐₓ value not reported in main text.** For the "unlimited token budget" setting (Section 4.2), the paper states that Cₘₐₓ is incremented "until further increases in Cₘₐₓ no longer alter generation results" (Section 4.5), i.e., saturation. However, the specific Cₘₐₓ saturation values per model/benchmark are deferred to the (stripped) appendix. This is a reproducibility gap for the main accuracy results.

- **Pass@k evaluation is scope-limited.** Section 4.4 evaluates Pass@k only on AIME24/25 with a single model (Qwen3-8B). The claim that SWIR "reaches its maximal accuracy with significantly smaller k" would be strengthened by evaluation on more benchmarks and models.

- **α₀ ablation suggests entrance signal mixing is unnecessary.** The ablation in Table 2 shows α₀=1.0 (no mixing at all) achieves the best average accuracy at 61.85% — barely different from other values. The paper acknowledges this but presents the mixing mechanism as part of the method without clear evidence of benefit.

- **Computational overhead not quantified.** The entropy computation, switching logic, and injection queue (Section 3.4) add per-step overhead. Even if negligible, stating this explicitly would aid practical adoption and reproducibility.

### Trivial
None.

## Nice-to-Haves

- The α₀ and β₀ schedulers (Equations 4–5) could be made difficulty-aware rather than using fixed schedules, as the paper itself suggests.
- The pass@k analysis could be extended to additional benchmarks and models beyond AIME24/25 with Qwen3-8B.

## Removed Points

These points from the input are removed per filtering rules:

- **Soft Thinking baseline configuration concern**: The critic speculated Soft Thinking might be poorly configured because it sometimes underperforms greedy CoT. The paper explicitly states "Baseline hyperparameters follow the recommendations from their original papers" (line 255). Details are in the stripped appendix. Inconsistent performance across architectures is a reported finding, not necessarily a configuration error.
- **"Distribution collapse" motivation criticism**: The critic argued the soft embedding in Eq. 1 "averages over hypotheses" rather than preserving distinct branches. This critiques the training-free latent reasoning paradigm (prior work), not SWIREASONING. The paper's motivation is consistent with the cited literature.
- **Missing Wu et al. (2025b) comparison**: This is concurrent work; the paper explicitly notes this. Quantitative comparison may not be feasible.
- **Static reference entropy simplicity**: The paper's conclusion already characterizes the approach as "conceptually straightforward." This does not threaten any core claim.
- **Token injection disruption concern**: The critic asked whether overwriting autoregressive tokens could degrade accuracy. The empirical results (Tables 1, 4, 5) show accuracy improves, so this theoretical concern is addressed by the evidence.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add variance reporting.** Report standard deviations or confidence intervals (e.g., across 3–5 independent runs with different seeds) for all main accuracy tables. The modest gains (2.17% avg) cannot be interpreted without this.
2. **Include a naive hybrid baseline.** Add a control experiment with random or fixed-block mode switching at the same effective switch frequency. This directly tests whether the entropy criterion adds value beyond any hybrid alternation.
3. **Disentangle efficiency gains.** For the token efficiency analysis, include a "CoT with early stopping at equivalent token budget" baseline. This separates the effect of forced termination from the hybrid reasoning mechanism.
4. **Report Cₘₐₓ saturation values in the main text.** Specify the per-model/per-benchmark Cₘₐₓ values used to reach the "unlimited budget" saturation point.
5. **Quantify computational overhead.** Report the wall-clock or FLOP overhead of the entropy computation, switching logic, and injection queue to aid practical adoption.

## Score and Decision

The paper proposes a well-motivated, clean idea and evaluates it across an impressive range of models and benchmarks. The consistent direction of results is encouraging. However, **three major evidential gaps** substantially weaken the paper's central claims: (1) no variance quantification for modest accuracy improvements, (2) no comparison against a naive hybrid baseline to isolate the entropy criterion's contribution, and (3) conflated token efficiency measurements that cannot be attributed to the switching mechanism rather than forced early stopping. These issues are fixable with additional controlled experiments, but in the current form the evidence does not convincingly demonstrate that the entropy-guided switching mechanism is what drives the reported gains.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>