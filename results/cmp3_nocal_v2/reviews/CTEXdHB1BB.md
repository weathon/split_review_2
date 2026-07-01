## Summary

This paper proposes CANON (Conditional advaNtage estimatiON), a modification to group-based advantage estimation for RLVR that splits sampled responses into two groups by a training metric (entropy or length) and computes inter-group and intra-group advantages separately. The key idea is to amplify the impact of a metric without presuming its directional preference (higher-is-better or lower-is-better). CANON is evaluated on 6 math benchmarks and 3 ZebraLogic subsets across three LLMs (Qwen2.5-Math-7B, Qwen2.5-Math-1.5B, Llama3.1-8B), demonstrating consistent gains over DR.GRPO and other baselines.

## Strengths

1. **Clean and well-motivated formulation.** The paper correctly identifies a limitation of prior approaches—hand-crafted directional priors (higher-is-better or lower-is-better for metrics like entropy)—and designs CANON to avoid presuming direction by decomposing advantage into inter-group (which trend leads to higher reward?) and intra-group (which responses in the same trend are better?) components. The unification with DR.GRPO as the special case μ=0.5 (Eq. 7) is a clean formal result.

2. **Broad evaluation across models and task types.** The paper evaluates on 6 math benchmarks and 3 high-complexity ZebraLogic subsets, across three models. This goes beyond single-model evaluation and shows consistent patterns.

3. **Informative training dynamics analysis (Figure 2).** The analysis showing that CANON-Inter (μ=1.0) improves math rapidly with decreasing entropy, while CANON-Intra (μ=0.0) eventually captures reflection-driven gains on logic tasks, provides grounded insight into why the two extremes behave differently and motivates the scheduling approach.

4. **Selective amplification verified via ablation (Table 4).** The paper includes a clean ablation showing that direct numerical scaling of the advantage (A = A×2) does not reproduce CANON's benefits, confirming that CANON's mechanism is selective amplification rather than simple magnitude increase.

## Weaknesses

### Fatal
None.

### Major

1. **Data values in Figure 3's table do not match Tables 1 and 2, without explanation.** For Qwen2.5-Math-7B (the primary model):

   | Method | Table 1 Math Acc | Figure 3 Math | Table 1 Logic Acc | Figure 3 Logic |
   |---|---|---|---|---|
   | DR.GRPO | 55.7 | 57.6 | 26.2 | 39.2 |
   | CANON-Inter (Entropy) | 57.6 | 45.0 | 25.7 | 35.0 |
   | CANON-Intra (Entropy) | 54.7 | 35.0 | 29.1 | 45.0 |
   | CANON-Dynamic (Table 2: 56.7 / 29.2) | — | 45.0 | — | 45.0 |

   DR.GRPO's Figure 3 math value (57.6) matches CANON-Inter's Table 1 value. DR.GRPO's Figure 3 logic value (39.2) matches the Mid-subset score from Table 1, not the average across Mid/Large/XLarge (26.2). CANON-Dynamic's values in Figure 3 (45.0/45.0) differ substantially from Table 2 (56.7/29.2 for the chosen strategy). For Qwen-1.5B and Llama-8B, similar mismatches occur: Figure 3's "DR.GRPO" values correspond to the *First-Inter-Later-Intra* row in Table 2 rather than the actual DR.GRPO row. The paper does not state whether the radar chart uses a different evaluation protocol, normalization, or experimental run. This is the paper's central visualization for its headline claim that "CANON-Dynamic achieves the highest performance across both tasks for all models." **This issue must be resolved before the empirical claims can be trusted.**

### Minor

2. **Post-hoc selection of scheduling strategy per model inflates apparent reliability of CANON-Dynamic.** The paper tries 4 scheduling strategies and selects the best per model (Cosin-First-Inter-Later-Intra for Qwen-7B/Llama-8B, First-Inter-Later-Intra for Qwen-1.5B). The text acknowledges this ("A specifically designed strategy is acceptable for better performance in practice"), but CANON-Dynamic is presented as a single method when it is actually a family with per-model strategy selection. Only 2 of the 4 attempted strategies appear in Table 2; the failing strategies (First-Intra-Later-Inter, Cosin-First-Intra-Later-Inter) are never discussed. Reporting all four would clarify whether the advantage over DR.GRPO is robust to strategy choice.

3. **Theorem 1's "clearer advantage signal" framing is at odds with the paper's own evidence.** Theorem 1 shows |A^inter|/|A^DR.GRPO| > 1 under equal-sized groups and frames this as a "clearer advantage signal." However, Table 4 shows that directly scaling the advantage magnitude (A = A×2) produces negligible gains on math (55.7→56.1) and harms logic (26.2→25.1), demonstrating that larger magnitude alone is not beneficial. The paper already distinguishes "direct numerical amplification" from CANON's selective amplification (lines 100, 291), so the Theorem 1 framing could be sharpened to avoid implying that magnitude is the mechanism.

4. **No measures of variance or statistical significance.** All results are from single runs without standard deviations, confidence intervals, or multiple seeds. The main math improvement (CANON-Inter: 57.6 vs DR.GRPO: 55.7, +1.9 points) is modest. Given that AIME 24/25 use Avg@10 and some variance is expected, it is unclear whether reported gaps exceed noise. While single-seed evaluation is standard in this computationally expensive setting, the paper should at minimum acknowledge this limitation.

### Trivial
- The figure caption for Figure 5 has "mu=0.5 (CANON-Intra)" but μ=0.0 corresponds to CANON-Intra per Eq. 5; this appears to be a typo in the extracted caption.

## Nice-to-Haves
- Reporting all four scheduling strategies' results (including the two that were attempted but not shown) would improve transparency.
- An ablation on what happens when the grouping metric is uncorrelated with reward (does CANON degenerate to DR.GRPO as Theorem 2 suggests?) would strengthen the analysis.

## Removed Points
These points from the input review were removed with justification:

- **"CANON-Eff comparison stacks advantages"** — Removed because CANON(μ=0.5) is mathematically equivalent to DR.GRPO (Eq. 7) when groups are equal-sized. The α-weighting is the sole modification, making the comparison one-modification vs. one-modification, not two vs. one. The criticism is based on a misunderstanding of the μ=0.5 equivalence.
- **"Unstated assumption about metric computability"** — Not a meaningful weakness; all metrics used (entropy, length) are standard and computable per-response at training time.
- **"Some CANON variants perform worse than DR.GRPO"** — Not a weakness; the paper transparently shows all results including negative ones.
- **"Llama3.1-8B results are very low"** — An observation about task difficulty, not a flaw in the method.
- **"Missing comparison to DAPO"** — DAPO is cited in the training setup; its absence as a baseline is worth noting but the paper's baseline set is already thorough.
- Generic concerns about metric normalization, scope creep, and speculation about missing appendix content were removed per filtering rules.

## Novel Insights
The training dynamics analysis (Figure 2) revealing the distinct roles of inter-group vs. intra-group advantages—where CANON-Inter drives rapid math improvement with decreasing entropy while CANON-Intra captures delayed reflection-driven gains on complex logic—is the paper's most insightful finding and goes beyond typical method comparisons. The ablation showing that direct numerical amplification (A×2) does not reproduce CANON's benefits (Table 4) cleanly demonstrates that selective, not scalar, amplification is the operative mechanism.

## Suggestions
1. **Resolve the Figure 3 data discrepancy** — Either correct the values to match Tables 1/2, or explicitly state that the radar chart uses a different evaluation protocol/normalization and describe what it shows. This is the most impactful fix.
2. **Report all four scheduling strategies** — Show results for First-Intra-Later-Inter and Cosin-First-Intra-Later-Inter alongside the two already reported. If they fail, that finding is itself informative.
3. **Add at least a brief discussion of variance** — Even noting that single-seed evaluation is standard due to computational cost, and acknowledging the limitation, would improve transparency.
4. **Sharpen Theorem 1's framing** — Clarify that the theorem establishes when the advantage magnitude is amplified, but that CANON's success relies on selective (not scalar) amplification as shown in Table 4.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>