## Summary

This paper formalizes the problem of critical KV cache entry selection in LLM inference from an output perturbation perspective (Definition 3.1). It derives an upper bound on the L₁ output perturbation (Theorem 3.3) showing that, beyond attention weights, the projected value states (‖VW^O‖₁) also matter. Based on this analysis, the paper proposes a two-stage greedy selection algorithm that constrains worst-case perturbation, and integrates it as a plug-and-play enhancement into three existing cache eviction methods (SnapKV, AdaKV, HeadKV). Evaluated across 3 LLM families and 29 datasets from Ruler and LongBench plus SCBench, the method consistently reduces compression loss, often substantially.

## Strengths

1. **Formal grounding of a previously heuristic problem.** Prior cache eviction methods rely on the intuition that higher attention weight = more critical. This paper is the first to formally define the problem (Definition 3.1) as minimizing output perturbation and derive what properties an optimal selection criterion should have. This reframes the conversation in the field.

2. **Theoretical derivation showing why attention weights alone are insufficient.** Theorem 3.3 derives an upper bound θ = C − (2 − 1/Σ) Σᵢ Nᵢ Aᵢ ‖V_{i,:}‖₁ that explicitly depends on both attention weights *and* the projected value state norms. This is a concrete, non-trivial result that explains *what* matters and *how* it enters the bound.

3. **Thorough and systematic empirical validation.** The evaluation covers 3 model families (Llama-3.1-8B, Mistral-7B-v0.3, Qwen2.5-32B), 3 distinct eviction methods (SnapKV, AdaKV, HeadKV), and 2 major benchmarks covering 29 datasets (Ruler + LongBench), plus SCBench multi-turn QA. The "w/ ours" variant wins in nearly every configuration — 88 out of 90 long-dependency-domain test cases (Section 4.3) — and the improvements are systematic, not cherry-picked.

4. **Negligible computational overhead.** The added computation (VW^O multiplication followed by L1 norm) is linear in sequence length. Measured overhead is 0.06s for batch-1 at 32K context (Section 4.6), making the method practically usable.

5. **Empirical validation of the theoretical mechanism.** Section 4.7 verifies that the algorithm actually reduces measured output perturbation (head-wise, layer-wise, across budgets), closing the loop between the theoretical bound and the method's practical behavior.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Framing overstates the algorithm's relationship to the bound.** The abstract claims the algorithm "optimizes the worst-case output perturbation," but the paper itself acknowledges that "directly minimizing the upper bound θ remains non-trivial" (Section 3.4). The two-stage greedy algorithm is a *heuristic designed to lower the bound*, not a direct optimizer of it. Theorem 3.5 only shows Stage 2 minimizes a conditional bound given Stage 1's selections; the overall selection is not shown to be optimal. The strong empirical results justify the method, but the framing should be more precise about what the theory does and does not guarantee.

2. **No variance or statistical significance reported.** The Ruler benchmark uses 100 sampled instances per task (Section 4.2), and the main tables (Tables 1, 2, 3) report only point estimates with no standard deviations, confidence intervals, or other measures of variability. Given that the improvements are large and consistent across all configurations, the overall conclusions are unlikely to be invalidated, but the absence of any variance information weakens the evidential rigor of the quantitative claims.

3. **Discrepancy in the stated value of α.** Algorithm 1 lists the input as "Hyper Parameter α = 0.25" (line 132), but the experiments consistently use α = 0.5 (Section 4.1, Section 4.5), and the theoretical discussion (Assumption 3.4) describes α in a 0.5 setting. The value 0.25 appears nowhere in the experimental discussion. This is a clear inconsistency that must be corrected.

4. **Pseudocode ambiguity in Algorithm 1.** Stage 1 (line 5) reads "for all K_i, V_i ∈ K, V that A_i ∈ Top_k(𝒜, b')". The text clearly states that Stage 1 selects by attention weights only (line 126), but the pseudocode references the combined score 𝒜 (attention × value norm) rather than the raw attention weights A. This appears to be a typo — the pseudocode should reference Top_k(A, b') for Stage 1 — but as written it is confusing.

### Trivial

- The "more than half" claim (abstract, Figure 1) averages over configurations that range from ~20% relative reduction (Mistral + SnapKV on Ruler) to ~84% (Llama + HeadKV on Ruler). While "on average" is an accurate qualifier, reporting the range or the worst-case improvement alongside the average would give readers a more complete picture.

## Nice-to-Haves

- **Tightness analysis of the bound.** The paper never examines how tight the upper bound θ is relative to the actual perturbation L. Showing θ/L ratios across heads and layers empirically would strengthen the claim that the bound is useful for guiding selection, and could be done with data already collected.
- **A more isolated ablation of the value-norm term.** The α sensitivity analysis (Table 4) partially addresses this, but a dedicated ablation comparing "Stage 2 with combined score" vs. "Stage 2 with attention only" across all methods and cache sizes would clarify the independent contribution of the value-norm signal.

## Removed Points

These points were raised in earlier reviews but are excluded or downgraded here with justification:

- **SCBench evaluation scope is narrow.** The main evaluation already covers 29 datasets × 3 models × 3 methods. The SCBench section is supplementary; demanding more models here is scope creep.
- **Table 1 column alignment issues.** These are parser-induced formatting artifacts, not problems in the original submission.
- **Missing ablation isolating value-norm term.** The α analysis (Table 4) already provides a partial ablation; the removed point is a stronger version of what is now listed as a Nice-to-Have.
- **Bound tightness analysis missing.** Downgraded to Nice-to-Have; not a standard requirement and the paper already provides empirical perturbation verification (Section 4.7).
- **"More than half" claim is misleading.** Downgraded to Trivial; the claim is accurate as stated with the qualifier "on average."
- **Generic concerns about confounders, metrics measuring proxies.** These were speculation-driven category sweeps, not specific verified problems.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface any perspective that the paper itself does not already present. The most useful observation — that the algorithm is better described as a heuristic that lowers the bound rather than one that optimizes it — is already partially acknowledged in the paper (Section 3.4).

## Suggestions

1. Correct the α default in Algorithm 1 from 0.25 to 0.5.
2. Fix the Stage 1 pseudocode to reference Top_k(A, b') instead of Top_k(𝒜, b').
3. Add standard deviations or confidence intervals to the main tables (especially Ruler, where 100 samples per task are already available).
4. Soften the abstract's language from "optimizes" to "constrains" or "lower bounds" the worst-case output perturbation.
5. Report the range of relative loss reductions alongside the average for the "more than half" claim.

## Score and Decision

**Score: 8 — Accept**

This is a strong paper with a genuine intellectual contribution: formalizing the critical cache selection problem, deriving a theoretically grounded bound, and operationalizing it into a practical algorithm with thorough empirical validation. The weaknesses are real but minor — none threaten the core contribution — and all are straightforward to address in a revision.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>