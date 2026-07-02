Now I will write the final consolidated review.

## Summary

This paper introduces CANON (Conditional advaNtage estimatiON), a method for reinforcement learning with verifiable rewards (RLVR) that incorporates metric signals (entropy, response length) without imposing hand-crafted directional priors. CANON regroups sampled responses into two groups by a target metric, then computes inter-group advantages (which metric trend correlates with correctness) and intra-group advantages (identifies better responses within the same trend). The method is evaluated on three LLMs (Qwen2.5-Math-7B/1.5B, Llama3.1-8B) across six math benchmarks and three logic reasoning tasks, showing consistent gains over DR.GRPO and other baselines, as well as improved token efficiency via weighted advantages.

## Strengths

1. **Clean, conceptually novel idea (Sections 1, 4):** The core insight — letting the data reveal which metric trend (higher or lower) correlates with correctness through regrouping — is genuinely elegant. It avoids the brittleness of hand-crafted penalties (e.g., length reward with coefficient 0.004 vs 0.005) and is not an incremental tweak to existing advantage estimation methods.

2. **Non-trivial theoretical grounding (Section 4.2):** Theorem 1 establishes that inter-group advantage amplifies the grouping signal relative to DR.GRPO when groups are equally sized. Theorem 2 shows this amplification is selective to the grouping metric and does not bleed into independent confounders. These results directly support the paper's central claim that CANON's advantage comes from *selective* amplification, not merely larger gradients.

3. **Thorough multi-model, multi-benchmark evaluation (Section 5, Tables 1–3):** The paper evaluates on three base models across six math benchmarks and three difficulty levels of logic reasoning. The inclusion of both entropy-based and length-based variants, and the separate analysis of inter vs intra advantages, allows the reader to see where the method helps most and where gains are marginal.

4. **Informative training dynamics (Figures 2, 5, 6):** The analysis showing CANON-Inter drives rapid math improvement with decreasing entropy, while CANON-Intra drives exploration that eventually pays off on complex logic, directly validates the method's mechanism. Figure 6's decomposition of "gain of rethinking" is insightful.

5. **Practical efficiency results (Section 5.3, Table 3):** The Pareto frontier analysis for CANON-Eff is the strongest empirical contribution. The stability of CANON-Eff across α values, contrasted with Length Reward (+) collapsing from 54.8 to 22.5 when its coefficient moves from 0.004 to 0.005, demonstrates a concrete practical advantage.

## Weaknesses

### Fatal
None.

### Major

1. **Radar chart (Figure 3) values are inconsistent with Table 1 and Table 2.** The radar chart's accompanying table reports DR.GRPO for Qwen-7B as Math=57.6, Logic=39.2, while both Table 1 and Table 2 consistently report DR.GRPO as Math=55.7, Logic=26.2. For CANON-Dynamic on Qwen-7B, the radar chart shows Math=45.0, Logic=45.0, but Table 2 shows the same method achieving Math=56.7, Logic=29.2. The discrepancy extends to Llama-8B: the radar chart shows CANON-Dynamic at Math=35.2, Logic=35.2, but Table 2 shows Math=22.6, Logic=18.9. The paper's only explanation — "We draw a radar chart with the average performance of the two scenarios for visualization" — does not account for these differences. Until this is resolved, the radar chart figure cannot be trusted, and confidence in the paper's quantitative reporting is reduced.

### Minor

2. **No variance or uncertainty reporting across all experiments.** Results are reported as single numbers with no error bars, multiple seeds, or significance tests. Given that several gains over strong baselines are modest (e.g., 1.9 points on math, 2.9 points on logic), the reader cannot assess whether improvements are reliable. While this is common in RLVR literature, the paper's claims of consistent superiority would be strengthened by variance information.

3. **Theorem 1 phrasing is ambiguous as presented.** The statement reads: "|Â^{inter}|/|Â^{DR.GRPO}| > 1, only when |C_q^+| = |C_q^-| if |C_q^+| is a constant." The logical connection between the two conditions ("only when... if...") is unclear. The paper would benefit from clarifying the quantifiers and the exact regime where amplification holds (and where it does not).

4. **The entropy metric used for regrouping is not formally defined.** The paper mentions "per-token generation entropy" (Section 5.1) but does not specify whether this is average per-token entropy, the entropy of the token probability distribution at each step, or some other formulation. This is needed for reproducibility.

5. **The "2.63× higher performance" claim uses an aggressive comparison point.** This compares CANON-Eff (α=0.88) against DR.GRPO at a specific low-token budget where DR.GRPO performs especially poorly. While the comparison is valid at equal budget, the framing glosses over that at unconstrained budgets the gap is about 3 points (53.6 vs 56.6). The accompanying "45.5% token reduction" claim (comparing to Length Reward (*) at comparable performance) is more carefully framed.

### Trivial

6. **The handling of ties during regrouping is not discussed.** When multiple responses share the same metric value, the paper does not specify how they are assigned to groups. This can arise with discrete or quantized metrics.

## Nice-to-Haves

- The ablation in Table 4 tests only one form of direct numerical amplification (multiplying by 2). Testing additional controls (e.g., amplifying only responses in a specific metric quartile) would strengthen the claim that selective amplification is key.
- A limitations section discussing when CANON may not help (e.g., metric uncorrelated with reward, highly imbalanced groups) would improve the paper.

## Removed Points

These points were raised by the harsh critic but are removed with justification:

- **"Table 1 vs Table 2 inconsistency (53.8 vs 55.7)":** Removed (factually wrong). The critic claimed Table 1 shows DR.GRPO as 53.8/17.2. These are actually GRPO values (a different baseline). DR.GRPO is consistently 55.7/26.2 in *both* Table 1 and Table 2. The tables are internally consistent.
- **"CANON-Dynamic results selected from multiple schedules inflates advantage":** Removed (paper is transparent). The paper explicitly states it tried 4 strategies and reports 2 of them in Table 2. Both reported strategies outperform DR.GRPO. The model-specific selection is acknowledged, and the gains over DR.GRPO are robust across strategies. This is adequately handled.
- **"Missing related work context":** Removed per policy (no external sources to verify).
- **"Section-by-section notes about appendix content":** Removed per policy (appendix stripped by parser).
- **"Formatting and style nitpicks":** Removed per policy.

## Novel Insights

The harsh critic's analysis surfaces one genuinely novel observation beyond the paper's own contributions: the radar chart discrepancy reveals that the paper has a data integrity issue that is not acknowledged. The critic's framing of this as a "Table 1 vs Table 2" problem is incorrect (the tables agree), but the radar chart's divergence from both tables is real and needs author explanation. The critic also correctly notes that Theorem 1's phrasing is ambiguous, though the underlying concept is sound.

## Suggestions

1. **Resolve the radar chart inconsistency.** Clearly explain what the Figure 3 radar chart values represent — are they normalized/scaled? From a different checkpoint or evaluation protocol? Correct any reporting errors. Without this fix, the paper's quantitative claims are undermined.

2. **Formally define the entropy metric** used for regrouping. Provide the formula for "per-token generation entropy."

3. **Clarify Theorem 1's statement.** Restate the condition for amplification with precise quantifiers, and discuss regimes where amplification does not hold.

4. **Add variance information** for at least the main comparison (DR.GRPO vs CANON-Inter/Intra) on the primary benchmarks.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>