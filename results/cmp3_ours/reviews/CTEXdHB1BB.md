Now I have a solid calibration picture. Let me write the final review.

**Calibration Summary:**

Round 1 anchors (bracketing):
- Strong reject band (<1.5): Papers at 1.0-1.4 — clearly flawed or not real papers (not applicable here).
- Low band (1.5-3.5): ZK1NnjpjEs (3.00) — incremental PPO application to NLU, found lacking in novelty. The current paper is clearly stronger.
- Middle-low (3.5-5.5): gdzpnRBP4F (4.50, rejected), F0GNv13ojF (5.17, rejected), OD9pwKQzXl (5.25, rejected), D23JcXiUwf (5.50, rejected).
- Middle-high (5.5-7.5): DpFeMH4l8Q (5.67, accepted), O0sQ9CPzai (6.33, accepted).
- High (7.5-8.5): mMPMHWOdOy (8.00), rfdblE10qm (8.00) — clearly stronger papers.

Round 2 narrowing (4.0-7.0): Confirms the pattern — papers around 5.0-5.5 are typically rejected due to evidential or methodological issues; papers above ~5.7 tend to be accepted.

**Bracket:** The paper sits in the 4.5–5.5 range. The core idea is cleaner than most papers in the 3.5–5.0 range, but the radar chart data discrepancy is a genuine presentation issue that depresses confidence. My final score is **5.0**.

Here is the final review:

---

## Summary

This paper proposes CANON (Conditional advaNtage estimatiON), a modification to group-relative advantage estimation (GRPO/DR.GRPO) for RLVR training of LLMs. The key idea is to split sampled responses into two equal-sized groups based on a metric (entropy, length), then compute inter-group and intra-group advantages separately. This amplifies the metric's influence on the policy gradient without requiring a directional prior (higher-is-better or lower-is-better). The paper shows DR.GRPO is a special case, evaluates across three LLMs on math and logic tasks, and demonstrates efficiency improvements via length-based weighting.

## Strengths

1. **Clean, theoretically grounded idea.** The inter/intra-group decomposition is simple and well-motivated. Equation (7) showing DR.GRPO = (1/2)(inter + intra) when groups are equal-sized elegantly grounds the method in a known baseline. Theorem 1 provides principled justification for the median-split design. These theoretical connections are stronger than what most RLVR papers provide.

2. **Comprehensive evaluation across models and tasks.** Experiments span three LLMs (Qwen2.5-Math-7B, Qwen2.5-Math-1.5B, Llama3.1-8B), six math benchmarks, and three complexity levels of ZebraLogic. The inclusion of small/weak models is informative. The efficiency results (Section 5.3) are practically compelling, with CANON-Eff at α=0.96 achieving comparable accuracy to DR.GRPO while using 26.3% fewer tokens (Table 3), and the Pareto frontier in Figure 4c dominates all baselines.

3. **Training dynamics analysis adds insight.** Figure 2 and the associated discussion provide real analysis of why inter-group and intra-group advantages behave differently: inter-group drives rapid math improvement with entropy reduction, intra-group enables exploration that pays off on hard logic tasks through increased reflection. This behavioral analysis is valuable and uncommon.

## Weaknesses

### Major

1. **Radar chart data inconsistency (Figure 3).** The numerical values presented alongside the radar chart (lines 212-225) are systematically inconsistent with the tabular results in Tables 1 and 2. Key examples:

   | Model | Method | Table Value (Math/Logic) | Radar Value (Math/Logic) |
   |-------|--------|------------------------|------------------------|
   | Qwen-7B | DR.GRPO | 55.7 / 26.2 (Table 1) | 57.6 / 39.2 |
   | Qwen-7B | CANON-Inter (Entropy) | 57.6 / 25.7 (Table 1) | 45.0 / 35.0 |
   | Llama-8B | DR.GRPO | 22.0 / 14.9 (Table 2) | 22.6 / 18.9 |
   | Qwen-1.5B | DR.GRPO | 46.4 / 12.8 (Table 2) | 46.8 / 17.0 |

   The values 45.0, 35.0, 30.0 are suspiciously round, and CANON-Inter/Intra values are exact mirror images (45.0/35.0 vs 35.0/45.0). For Llama-8B, the radar's "DR.GRPO" values (22.6/18.9) match the Cosin-First-Inter-Later-Intra row in Table 2, not the actual DR.GRPO row (22.0/14.9), suggesting a possible labeling error. The paper must clarify whether Figure 3 is empirical or schematic, and if empirical, reconcile the numbers.

### Minor

2. **No uncertainty estimates reported.** Results are point estimates with no standard deviations, confidence intervals, or multi-seed runs. For small benchmarks (AIME 24/25: ~30 problems; AMC: ~40), a few-point difference can arise from a single problem. The flagship 1.9-point accuracy gain masks per-benchmark variability (CANON-Inter wins by 5.0 on AIME 24 but loses by 1.6 on AIME 25). While single-seed runs are common in this area, variance estimates would substantially strengthen the central quantitative claims.

3. **CANON-Dynamic involves model-specific strategy selection.** The paper tries four scheduling strategies and selects the best per model (Cosin-First-Inter-Later-Intra for Qwen-7B and Llama-8B; First-Inter-Later-Intra for Qwen-1.5B). Results for unselected strategies are not reported. The abstract's claim that "CANON...consistently outperforms prior methods across three LLMs" conflates a family of approaches with model-specific selection. The paper is transparent in Section 5.2, but the framing is imprecise.

4. **"Without hand-crafted priors" framing is overstated.** The direction-agnostic property (not needing to know whether higher/lower metric values are better) is valid. However, CANON introduces its own tunable parameters (μ, α, scheduling strategy). In Section 5.3, α is tuned across 0.5, 0.7, 0.8, 0.88, 0.96 — comparable to the tuning of baseline coefficients criticized for requiring careful selection. The paper's narrative should more carefully distinguish between "direction-agnostic" and "free of hyperparameters."

### Trivial

5. **Theorem 1 clarity.** The condition "if |C_q^+| is a constant" in the theorem statement (line 94) is ambiguous. Since Eq. 7 shows DR.GRPO = 0.5(inter + intra) when groups are equal-sized, amplification of the inter-group advantage implies corresponding de-amplification of the intra-group advantage — this trade-off should be acknowledged in the theorem statement.

6. **CANON-Dynamic in Table 1.** CANON-Dynamic appears in Table 1 (line 126) under "Entropy" methods, but the scheduling concept is only introduced in Section 5.2. This mixes single-μ results with scheduled results without clear labeling.

## Nice-to-Haves

- Running multiple seeds (at least 3) for the main CANON-Inter vs DR.GRPO comparison would substantially strengthen the evidential basis for the 1.9-point gain claim.
- An ablation comparing equal vs. unequal group sizes would validate Theorem 1's theoretical prediction.
- Reporting results for all tried scheduling strategies would help assess how robust the CANON-Dynamic advantage is.

## Removed Points

- **Missing variance/statistical significance for any result** — This was kept as Minor (weakness 2) since it's a real concern but contextualized to the field's norms.
- **The "Length Reward (*)" misspelling "Aroca"** — Removed as a trivial formatting issue; parser may have introduced the artifact.
- **"Headline numbers are context-dependent"** — The paper does specify "In low-token-budget scenarios" in the introduction (line 30); the criticism was partially based on a misreading. The relevant observation about context-dependence is retained implicitly through weakness 4 (framing overstatement).
- **"CANON requires the grouping metric to be computable per response"** — This is inherent to the method's setup and not a meaningful limitation; removed.
- **Strength about "addressing an important problem"** — Generic/superficial; removed.
- **Strength about "comprehensive evaluation"** — Kept because it's specific (names models, benchmarks, tasks).

## Novel Insights

The consistent pattern in the Figure 3 radar chart data — where Llama-8B DR.GRPO values (22.6/18.9) match the Cosin scheduling row in Table 2 rather than the DR.GRPO row — and the perfectly symmetric CANON-Inter/Intra mirror values suggest a possible systematic labeling or data assignment error in the radar visualization that the paper does not acknowledge.

## Suggestions

1. **Resolve the Figure 3 data discrepancy.** If the radar chart is empirical, correct the values to match Tables 1/2 and explain any differences in aggregation. If it is a schematic illustration, label it clearly as such and remove the numerical table that presents the values as data.
2. Add uncertainty estimates (multi-seed runs or confidence intervals) for the main CANON-Inter vs DR.GRPO comparison.
3. Reframe CANON-Dynamic results with explicit caveats about model-specific strategy selection, and report results for all tried strategies.
4. Clarify Theorem 1's "if |C_q^+| is a constant" condition and acknowledge the inter/intra trade-off.
5. In the abstract and introduction, be precise that CANON is direction-agnostic (not "free of hand-crafted priors"), and note that the efficiency claims (2.63×, 45.5%) are for low-token-budget scenarios.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>