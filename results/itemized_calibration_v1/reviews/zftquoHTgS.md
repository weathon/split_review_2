Now I have all the calibration data I need. Let me finalize the review.

**Calibration bracket analysis (Round 1):**
- Strong rejects (score <1.5): Irrelevant papers — no similarity to SmartSwitch which has real experiments and results.
- Rejects/Borderline rejects (1.5–3.5): Papers like "Planning in Strawberry Fields" (3.00) lacked novel contributions. SmartSwitch has a genuinely novel method and large gains, well above this band.
- Weak rejects (3.5–5.5): Papers at this level (e.g., MathHay 4.17, Can LLMs Solve Long Math Word Problems? 4.75) are mostly benchmarks/analyses without novel methods. SmartSwitch proposes a novel inference framework with significant improvements, so it's above this band.
- Borderline to Clear Accepts (5.5–7.5): Key anchors here include:
  - IssPhpUsKt (6.80, accepted): Inference-time intervention for reasoning. Weaknesses: hyperparameter sensitivity (alpha), limited model scope, modest gains. SmartSwitch has larger gains, more models/benchmarks, but similar hyperparameter sensitivity.
  - OoNazl6T7D (6.50, accepted): MPC-based decoding for reasoning. Weaknesses: similarity to prior work, missing comparisons. SmartSwitch is more novel.
  - Tn5B6Udq3E (6.00, accepted): Mathematically rigorous but limited to synthetic data and small models. SmartSwitch has more practical impact.
  - DzKdjWe59v (5.75, rejected): Marginal gains (<1%), limited ablations. SmartSwitch dominates this anchor on every dimension.
- Strong accepts (7.5–8.5): Papers like FlexPrefill answer a crisp, well-scoped efficiency question with thorough engineering. SmartSwitch's broader scope and the test-set tuning concern keep it below this band.

**Narrowed bracket: 6.0–6.5.** SmartSwitch has stronger empirical evidence (large gains, many models/benchmarks, good ablations) than the 5.75 rejected anchor but the threshold-tuning issue prevents it from reaching the 6.80 level.

**Anchor comparison for final placement:**
- Shared heavy-weight items with IssPhpUsKt (6.80): Both have hyperparameter sensitivity concerns, both propose novel inference-time interventions. SmartSwitch adds more model scales, more benchmarks, and quantitatively larger gains, but has a more explicit test-set tuning concern. SmartSwitch is slightly below IssPhpUsKt.
- Above DzKdjWe59v (5.75) and 0JjsZC0w8x (5.75): SmartSwitch has far more convincing results, better ablations, and a clearer contribution.
- Comparable to Tn5B6Udq3E (6.00): Both have interesting findings and solid experiments. SmartSwitch's practical impact is higher.

**Final score: 6.5**

Here is the final review:

## Summary

This paper identifies the "underthinking" problem in LongCoT LLMs — where models prematurely switch reasoning paths without sufficient exploration. The authors propose SmartSwitch, a training-free, model-agnostic inference framework that detects thought switches via linguistic cues, uses an off-the-shelf Process Reward Model (PRM) to evaluate whether the abandoned thought was promising, and if so, backtracks and injects a "deepen prompt" to encourage further exploration. Experiments on five math benchmarks (AIME24, AIME25, AMC23, MATH-500, GaoKao2023en) across five model scales (1.5B–32B) show consistent and often large accuracy gains (e.g., +16.7 points on AIME25 for 1.5B, +23.3 for 7B) while also reducing inference time.

## Strengths

1. **Large and consistent accuracy gains, especially for small models.** The improvements are substantial (e.g., +16.7 points on AIME25 for 1.5B, +23.3 points for 7B) and hold across all five model scales and five benchmarks (Table 1). The gains are not isolated to a single configuration — the pattern is broad and systematic.

2. **Training-free and model-agnostic design is a genuine practical virtue.** The framework requires no fine-tuning or model modification — only an off-the-shelf PRM and a list of linguistic triggers. This lowers the adoption barrier considerably.

3. **Well-structured and extensive ablation studies.** The paper systematically ablates the process division strategy (Table 6) across five model scales, the PRM choice (Table 4), the process-to-thought score mapping (Table 7), and the score threshold (Table 8). The v4 adaptive paragraph strategy consistently outperforms alternatives across all model sizes, demonstrating careful engineering.

4. **The problem is well-motivated with concrete evidence.** The qualitative example in Figure 1(a) (74 thoughts with 150-token median leading to truncated output) and the quantitative survey across six models (Figure 1(b)) convincingly illustrate that underthinking is a real, widespread phenomenon. Figure 2's finding that wrong answers correlate with higher underthinking frequency further grounds the problem.

## Weaknesses

### Major

1. **Hyperparameter threshold tuned directly on a test benchmark without a validation split.** The potential score threshold (τ=0.70) is selected by sweeping values on AIME24 (Table 8, Section 5.5), and the same benchmark appears as a test set in the main results (Table 1). This constitutes tuning on the test set. For the 1.5B model, accuracy drops from 40.0% to 30.0% when the threshold moves ±0.01, which is a change of only 3 out of 30 problems — within the noise range of a small benchmark. Mitigating factors: (a) the paper is transparent about the sweep and reports all values; (b) the 0.70 optimum is consistent across all five model sizes (Table 8), which argues against pure overfitting; (c) the large gains on AIME25 (a separate, non-tuned benchmark) provide a de facto held-out signal. Still, the paper should either report results on a held-out test split after tuning on a development split, or provide bootstrapped confidence intervals so readers can assess whether the threshold sensitivity is within sampling noise.

### Minor

2. **The Underthinking Frequency metric (Eq. 1) is a heuristic proxy, not a direct measure of premature abandonment.** UF counts thoughts shorter than L=100 tokens as "underthinking." A short thought may legitimately reflect efficient pruning of a dead end, while a long thought could still represent circular reasoning. The paper is transparent about this being a heuristic ("Heuristically, we define…"), and the metric is mainly used for problem characterization rather than for validating the main accuracy results. However, the narrative about "detecting underthinking" would be strengthened by a small human annotation study validating that short thoughts correspond to premature abandonment, or by a different metric that checks whether an abandoned thought contained correct sub-steps.

3. **Comparison against TIP (the closest prior underthinking method) is limited to one model (1.5B) on one benchmark (AIME24).** Since the paper's own Figure 1 shows that underthinking patterns vary dramatically across model scales and model families, the TIP comparison should be extended to the same suite of models and benchmarks used in Table 1 to establish that SmartSwitch consistently outperforms the closest prior work.

4. **No confidence intervals or variance estimates for main results.** Results in Table 1 are reported as pass@1 averaged over 32 responses without error bars. On small-N benchmarks (30 problems for AIME24/25), a few correct answers can swing accuracy by several points. Reporting bootstrapped 95% confidence intervals would help distinguish real improvement from noise.

### Trivial

5. **PRM performance ordering (Table 4) lacks diagnostic analysis.** Universal-PRM-7B (36.7%) dramatically outperforms Qwen2.5-Math-PRM-72B (24.8%). The paper attributes this to long-context capability but does not provide diagnostic evidence (e.g., what fraction of thoughts the 72B model truncates). A brief analysis would substantiate the claimed explanation.

## Nice-to-Haves

- A breakdown of inference time into PRM scoring vs. generation vs. backtracking overhead (Tables 2, 3) would clarify the source of efficiency gains.
- Estimating the recall of the linguistic-cue-based switch detector on a manually annotated sample would bound the method's effective scope (the paper already acknowledges this limitation in the discussion).
- Comparing against Best-of-N using the same PRM would isolate whether the gain comes from PRM-guided selection or the backtracking+deepen mechanism specifically.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"PRM choice unexplained and context length alone cannot explain the gap"** — The paper does explain this (Universal-PRM-7B's 32K context window is critical; other PRMs have shorter limits). The critic's assertion that "context length alone cannot explain it" is speculative and unsupported.
- **"Threshold sensitivity indicates the results are fragile" in its most extreme framing** — Reframed above as Major weakness #1 with appropriate nuance, noting the mitigating factor of cross-model consistency.
- **"Linguistic cue detection coverage is unquantified"** — The paper acknowledges this limitation in the Discussion section. A quantified detection rate would be a nice-to-have, not a weakness.
- **"Missing comparisons to self-consistency, re-ranking, verifier-guided decoding"** — These methods target different problems (variance reduction, response selection) rather than underthinking mitigation. The paper's scope is underthinking-specific methods; demanding every possible inference-time technique is scope creep.
- **Formatting/style nitpicks and complaints about the stripped appendix** — Removed per hard rules (parser artifact).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. For the final version, split AIME24 into development (for threshold tuning) and test subsets, or provide bootstrapped confidence intervals for all main results.
2. Extend the TIP comparison to cover the full model and benchmark suite.
3. Add a brief diagnostic for the PRM performance gap (Table 4) showing truncation rates or score distributions.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>