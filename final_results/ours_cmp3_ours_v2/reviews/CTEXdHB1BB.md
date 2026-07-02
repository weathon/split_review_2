## Summary

This paper introduces CANON (Conditional advaNtage estimatiON), a regrouping-based advantage estimation method for RLVR in large reasoning models. Rather than imposing directional priors (higher-is-better or lower-is-better) on training metrics like entropy or response length, CANON splits sampled responses into two groups by a metric's value and computes inter-group (cross-group comparison) and intra-group (within-group comparison) advantages. The method is evaluated across three model families (Qwen-7B, Qwen-1.5B, Llama-8B) on six math benchmarks and three ZebraLogic difficulty tiers. A weighted variant (CANON-Eff) targets token-efficiency and produces a superior Pareto frontier.

## Strengths

1. **Clean, well-motivated conceptual formulation (Sections 4.1–4.2).** The core idea — regrouping sampled responses by a metric's value and computing inter-group vs. intra-group advantages — genuinely avoids prescribing which direction of the metric is beneficial. This is a non-trivial and useful design choice that addresses a real limitation of prior advantage-shaping methods.

2. **Theoretical unification (Eq. 7, Theorem 1).** Proving that DR.GRPO with equal-sized groups is a special case of CANON with μ=0.5 provides a clean theoretical connection. Theorem 2 (selective amplification) also usefully formalizes that CANON amplifies only the grouping metric's influence, not independent factors.

3. **Comprehensive evaluation scope.** The paper evaluates across three model families (Qwen-7B, Qwen-1.5B, Llama-8B), six math benchmarks, and three ZebraLogic difficulty tiers. The inclusion of high-complexity logic reasoning subsets (>10³, >10⁶, >10⁹ solution spaces) goes beyond standard math-only evaluation and provides a differentiated picture of when inter-group vs. intra-group advantages matter.

4. **Strong efficiency results (Section 5.3).** The Pareto frontier analysis (Figure 4c) is the most compelling part of the empirical evaluation. CANON-Eff maintains stable performance across a range of α values while baselines collapse (e.g., Length Reward (+) drops from 54.8 to 22.5 when the coefficient moves from 0.004 to 0.005). The finding that CANON-Eff with α=0.96 Pareto-dominates baselines is a genuine practical advantage.

## Weaknesses

### Major

1. **Figure 3 data values do not match Tables 1–2, with no explanation.** The embedded table in Figure 3 reports numerical values that systematically disagree with Tables 1–2. For example, Qwen-7B DR.GRPO logic accuracy is listed as 39.2 in Figure 3 vs. 26.2 in Tables 1–2; CANON-Dynamic math is listed as 45.0 vs. 56.7 in Table 2. The values appear to have undergone some transformation (possibly per-task normalization for the radar chart), but no procedure is described. The caption says "Performance is measured on a scale from 0 to 100," which is ambiguous since Tables 1–2 already report percentages. This inconsistency undermines the visual evidence for the claim that "CANON-Dynamic achieves the highest performance across both tasks for all models." The primary quantitative claims are supported by Tables 1–2 (which are internally consistent), but the discrepancy must be resolved.

2. **Scheduling strategies selected post-hoc per model.** The paper tries four scheduling strategies and selects the best one per model (Section 5.2), with selection tested on the same benchmarks used for the main comparison. This is a mild form of test-set hacking. While Table 2 reports all strategies, the main visual (Figure 3) only shows the selected strategy per model. The authors should report whether a single fixed strategy works across models, or present a principled selection rule.

### Minor

1. **No variance or statistical significance reported.** None of the tables report standard deviations, confidence intervals, or multiple seeds. For small benchmarks like AIME 24 (30 problems) and AIME 25 (30 problems), the claimed 1.9–5.2 point improvements may not be statistically significant. Single-seed evaluations are common in this literature, but given the paper's central claims are empirical (CANON outperforms DR.GRPO), variance quantification would substantially strengthen the evidence.

2. **Baseline re-implementation needs clarification.** The paper states it applies length bias correction, clip-higher strategy (ε_high=0.28), and removes KL/entropy loss "for all experiments" (Section 5.1), but does not explicitly confirm that all baselines (ReMax, R++, RLOO, GRPO, DR.GRPO) were re-run under these modified conditions. The phrase "unified setting" in table captions implies this, but explicit confirmation would remove ambiguity about whether CANON's improvements reflect the regrouping mechanism or the auxiliary modifications.

3. **"Reflection gain" metric not operationally defined.** The analysis in Figure 2f and line 192 divides responses "by counting reflection patterns" without specifying how a reflection pattern is identified (specific tokens like "Wait," "Alternatively"? Structural properties?). This affects reproducibility of the training dynamics analysis.

4. **"No directional prior" framing slightly overstated.** The paper's unifying rhetorical emphasis on "amplifying the impact of the target metric without presuming its direction" is accurate for CANON with α=1, but the headline efficiency results (Section 5.3) come from CANON-Eff where α<1 explicitly imposes a directional prior on length (shorter-is-better). The paper does distinguish these cases (Section 4.3 vs. Section 5.3), but the framing could mislead casual readers.

### Trivial

None.

## Nice-to-Haves

- Run main comparisons with at least 2–3 seeds and report mean ± std, especially for small benchmarks.
- Clarify the Figure 3 normalization procedure or correct the values to match Tables 1–2.
- Provide an operational definition of "reflection pattern" for the reflection gain metric.
- Report all four scheduling strategies for each model (not just the best) in the main results.
- Discuss sensitivity to the choice of group size (currently fixed at 8 per group via median split).

## Removed Points

These points from the harsh critic are removed with brief justifications:

- **"Figure 3 discrepancy is the most serious problem / structural issue"** → Demoted from fatal to major. The primary quantitative claims (CANON outperforming DR.GRPO on math and logic) are supported by Tables 1–2, which are internally consistent. Figure 3 is a visualization that likely uses a per-task normalization for radar chart display; the discrepancy is a presentation gap, not a data fabrication concern. But it remains a significant issue that must be addressed.
- **"Abstract claim about 2.63× is presented without qualification"** → The abstract says "In low-token-budget scenarios for math tasks, it achieves 2.63× higher performance," which does qualify the scope. Removed as the reviewer slightly misread this.
- **"The 'no directional prior' claim is overstated for the efficiency variant"** → Merged into Minor #4. The rhetorical framing could be cleaner, but the paper does distinguish CANON (α=1) from CANON-Eff (α<1) in separate subsections. Demoted to minor.
- **"Equal-sized groups by median split discards information"** → This is a design choice with a stated motivation (Theorem 1). A valid discussion point but not a weakness.
- **"Section 4.2 Theorem 1 statement is difficult to parse"** → Presentation issue, not a substantive weakness.
- **"Asymmetric formulation of Eq. 9 not clearly justified"** → The paper states the form and provides an example (α=0.9 for length reduction). This is an implementation choice.
- **"Table 1 aggregation method unspecified"** → The paper says "average performance" which is a simple mean across benchmarks. Minor at best.
- **"Training dynamics budget-performance curves unclear"** → The paper points to Appendix C.2 (removed by parser). Not verifiable.

## Novel Insights

None beyond the paper's own contributions. The harsh critic raised useful points about the method's behavior (e.g., inter-group advantage reinforcing rather than discovering metric direction) but these are clarifications of the paper's own analysis, not novel external observations.

## Suggestions

1. **Resolve the Figure 3 discrepancy as the highest priority.** Either state explicitly that the radar chart uses a per-task min-max normalization (and describe it), or replace the table with the raw accuracy values from Tables 1–2.
2. **Add variance reporting** for the main DR.GRPO vs. CANON comparisons — even 2 seeds with bootstrapped confidence intervals would substantially improve the evidentiary basis.
3. **Explicitly state** whether all baselines were re-implemented under the identical training setup (KL/entropy loss removal, clip-higher strategy) or, if not, discuss the confound.
4. **Pre-specify a single scheduling strategy** or report all four strategies for each model to show robustness rather than selecting the best per model.

## Score and Decision

**Calibration procedure:** I retrieved anchors from a corpus of human-reviewed ICLR papers. Round 1 bracketing searched across six score bands for topics related to "reinforcement learning for large language models advantage estimation GRPO RLVR." The strongest reject anchors (scores 1.0–1.4) were papers with fundamental methodological errors or near-empty contributions. The 1.5–3.5 band captured papers that proposed incremental alignment methods with limited evaluation (avg 2.5–3.0). The 3.5–5.5 band included papers with solid ideas but significant evaluation gaps, such as "Fine-Tuning Language Models with Advantage-Induced Policy Alignment" (5.25, rejected; scored 5,8,3,5 — similar domain but narrower evaluation than CANON). The 5.5–7.5 band included accepted papers like "Vanishing Gradients in Reinforcement Finetuning" (6.25) and "Improving Reasoning Performance via Representation Engineering" (6.80) — papers with genuine contributions but non-trivial weaknesses.

Round 2 narrowed with a focused query on "conditional advantage estimation regrouping RLVR LLM reasoning" in the 4.0–7.0 band. The representation engineering paper (6.80, accepted) had significant concerns about task simplicity and overclaimed interpretations but was still accepted, while the APA paper (5.25, rejected) was weaker in both evaluation breadth and contribution clarity. CANON sits between these: its contribution is clearer and its evaluation broader than APA, but the Figure 3 inconsistency and missing variance prevent it from reaching the 6.8 level. The fair score range is 5.5–6.5, anchored at 6.0.

**Score: 6.0 — Accept.** The paper has a genuine, well-motivated contribution (the regrouping mechanism and its theoretical connection to DR.GRPO), comprehensive evaluation across models and tasks, and compelling efficiency results. The main issues (Figure 3 inconsistency, missing variance) are significant but addressable and do not invalidate the core claims.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>