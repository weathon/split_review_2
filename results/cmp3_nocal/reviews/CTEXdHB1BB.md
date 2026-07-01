## Summary

This paper proposes CANON (Conditional advaNtage estimatiON), a method for advantage estimation in RLVR (Reinforcement Learning with Verifiable Rewards) for LLM reasoning. The core idea is to split sampled responses into two groups based on a metric (e.g., entropy, response length), then compute both an inter-group advantage (which trend yields higher reward) and an intra-group advantage (which response is better within its group). The two are combined via a parameter μ. DR.GRPO is shown to be the special case μ=0.5. The paper evaluates CANON across 3 LLMs, 6 math benchmarks, and 3 logic reasoning difficulty levels, demonstrating performance gains and token-efficiency improvements.

## Strengths

1. **Clean, well-motivated core idea (Section 4).** Splitting sampled responses by a metric and letting the data decide which direction of that metric is beneficial is conceptually elegant. It directly addresses a real limitation of prior advantage-shaping methods (Cheng et al. 2025, Arora & Zanette 2025) that require the user to pre-specify whether a metric should be higher-is-better or lower-is-better.

2. **Theoretical unification of prior work (Eq. 7).** Showing that DR.GRPO is exactly the μ=0.5 special case of CANON is a concrete, non-trivial connection that cleanly situates the method in the literature.

3. **Thorough evaluation across multiple dimensions.** Experiments cover 3 LLMs (Qwen-7B, Qwen-1.5B, Llama-8B), 6 math reasoning benchmarks, 3 logic reasoning difficulty levels, and an efficiency analysis. This breadth is substantive and allows the paper to demonstrate that different μ settings benefit different tasks.

4. **Non-trivial efficiency Pareto improvement (Section 5.3, Table 3, Figure 4).** CANON-Eff (α=0.96) achieves 56.2% accuracy with 822 tokens vs. DR.GRPO's 56.6% with 1115 tokens — a 26% token reduction with negligible performance loss. The Pareto frontier in Figure 4c shows CANON-Eff dominating all baselines. This is practically meaningful for deployment.

## Weaknesses

### Fatal

None.

### Major

1. **No statistical significance or variance reporting.** All results (Tables 1, 2, 3) are reported as point estimates with no standard deviations, confidence intervals, or information about number of random seeds or runs. RL training for LLMs is notoriously noisy; reported gains of 1.9 points on average math accuracy (57.6 vs. 55.7, Table 1) or 5.2 points on the XLarge logic subset could fall within run-to-run variance. Without any measure of uncertainty, the reader cannot assess whether the central claims — that CANON outperforms prior methods — are reliable or noise. This is a structural weakness in the evaluation.

### Minor

2. **The comparison to DR.GRPO is partially within-family.** Eq. 7 shows DR.GRPO is exactly CANON with μ=0.5. The headline comparison (CANON-Inter vs. DR.GRPO) is therefore CANON at μ=1.0 vs. CANON at μ=0.5. The paper does benchmark against genuinely independent methods (ReMax, RLOO, GRPO, etc.) which partly addresses this, but the framing should be contextualized as "CANON at μ=1.0 outperforms CANON at μ=0.5 (DR.GRPO)" rather than treating DR.GRPO as an entirely external baseline.

3. **Radar chart values in Figure 3 are not transparently derived from the main tables.** The embedded table in Figure 3 gives values like Qwen-7B DR.GRPO Math=57.6, Logic=39.2. However, Table 2 reports DR.GRPO for Qwen-7B as Math=55.7, Logic=26.2. Similar discrepancies exist for Llama-8B and Qwen-1.5B. The paper does not explain whether these are normalized, rescaled, or computed differently, making it impossible to interpret the radar chart from the reported data.

4. **Theorem 2's guarantee is narrower than claimed.** The paper states that CANON based on c₁ "will not amplify the influence of another independent condition c₂" (line 132). What Theorem 2 actually proves is that the ratio |A_inter|/|A_DR.GRPO| is constant with respect to c₂. This means the *amplification factor* (relative to DR.GRPO) does not depend on c₂'s parameters, but the absolute advantage values — and thus the policy gradient — can still be influenced by c₂ through the rewards. The claim of "selective amplification" is somewhat over-interpreted.

5. **Different scheduling strategies used for different models (Section 5.2).** The paper selects *Cosin-First-Inter-Later-Intra* for Qwen-7B and Llama-8B, but *First-Inter-Later-Intra* for Qwen-1.5B. The paper acknowledges this is "acceptable in practice," but it weakens the claim of a single consistent scheduling principle working across models.

### Trivial

6. **Notation inconsistency.** Sets are defined as C_q^+ and C_q^- in Section 4.1, but Eqs. 3, 4, and 9 use G_q^+ and G_q^-.

## Nice-to-Haves

- Clarify whether the context expansion (rope theta modification from 4096 to 16384) was applied uniformly to all baselines, or whether the 33.8% token reduction claimed for CANON-Inter (Length) partly reflects a length advantage.
- Report training wall-clock time or compute overhead; the paper notes the overhead is negligible but should state this explicitly.
- The paper lacks a limitations section. Important points to acknowledge: CANON requires choosing which metric to group by; scheduling strategies require model-specific tuning; the method has not been tested on non-math/non-logic domains or tasks with dense rewards.

## Removed Points

- **"Acc column confusion"**: Removed because the reviewer used GRPO's numbers (22.3, 18.3, 47.3, 60.6, 83.8, 90.8) to compute the average for DR.GRPO. The actual Acc values are correct simple averages of each row's six math benchmarks.
- **Context expansion speculation**: Removed because there is no evidence the modification was applied unequally; the paper states it was done for all experiments.
- **Missing limitations section / compute cost / related works**: Removed per instructions — missing limitations sections and compute cost are not required weaknesses; missing related works cannot be verified.
- **Aroca vs. Arora typo**: Removed as a parser artifact / trivial formatting issue.
- **Table 1 "Acc" column organization confusion**: Removed — the Acc is clearly described as "average performance" (line 162), and values are consistent with simple averages.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Add variance estimates.** Run the main experiments (at minimum Table 1) with at least 3 random seeds and report mean ± std. This is the single highest-leverage improvement — without it, the core empirical claims are unverifiable given the noise in RL-based LLM training.
- **Reframe the DR.GRPO comparison.** Rather than presenting DR.GRPO as an external baseline, lean into the unified framework: frame CANON as a generalization of DR.GRPO, then show that the μ=0.5 default is suboptimal and CANON provides a principled way to depart from it.
- **Explain the Figure 3 radar chart values.** State explicitly whether the numbers are raw accuracy, normalized scores, or some other transformation, and show how they relate to Tables 1 and 2.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>