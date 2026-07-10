## Summary

This paper studies how to aggregate answers from multiple LLMs by leveraging higher-order information beyond simple majority voting. The authors propose two methods: Optimal Weight (OW), a Bayesian-optimal linear weighting scheme that requires knowing per-model accuracies, and Inverse Surprising Popularity (ISP), which uses second-order information (answer correlations) to avoid needing ground-truth labels. Theoretically, they prove ISP's advantage function exceeds MV's in expectation. Empirically, they evaluate on simulated data, UltraFeedback, MMLU, and a real healthcare dataset (ARMMAN), showing consistent small but statistically significant improvements over majority voting.

## Strengths

- **Clear theoretical framing with an elegant preprocessing trick.** The paper roots LLM aggregation in the economics information aggregation literature (Prelec et al., Austen-Smith & Banks). The random-shuffle preprocessing (Proposition 1) converts an unknown label distribution into a uniform one, making the Bayesian-optimal derivation tractable. **[favorability=12.86]**

- **The ISP construction is a genuine adaptation of existing ideas.** The paper identifies that the classic Surprisingly Popular rule underperforms MV in LLM settings (Theorem 2) and constructs a modified version (ISP) that reverses the conditioning intuition. This non-trivial adaptation has a theoretical proof of advantage over MV. **[favorability=12.61]**

- **Solid empirical breadth.** Evaluation covers simulated data with controlled heterogeneity, two standard LLM benchmarks (UltraFeedback, MMLU), and a real healthcare application (ARMMAN). Across all settings, proposed methods consistently outperform majority voting, with t-tests confirming statistical significance. **[favorability=12.27]**

- **Honest about limitations.** The paper acknowledges that the conditional independence assumption may not hold in practice (line 63), notes SP underperforms MV in LLM settings, and discusses when ISP's advantage diminishes as K grows. **[favorability=11.76]**

## Weaknesses

### Major

- **σ_K function is defined inconsistently.** The Overview of Results (line 25) defines σ_K(x) = x²/(K−1+x²), but the OW algorithm definition (line 73) defines σ_K(x) = eˣ/(K−1+eˣ). Corollary 1 for K=2 confirms the logistic/exponential form (σ(x)=eˣ/(1+eˣ)). Since OW weights are σ_K^{-1}(x_i), these definitions yield different weight vectors — e.g., for x_i=0.8, K=2, the quadratic form gives inverse weight ≈ 2.0 while the exponential form gives ≈ 1.39. The methods section and corollary are internally consistent (exponential form throughout), so the overview appears to contain an error rather than the method being ambiguous. However, this must be resolved: a reader cannot tell which function the overview intends, and the mismatch undermines confidence in the presentation of Theorem 1's key object.

- **OW-L and OW-I produce identical accuracy on all three real-world datasets, which is unexplained.** In Table 3, OW-L and OW-I both achieve exactly 73.66% on UltraFeedback, 90.37% on MMLU, and 85.78% on ARMMAN. Table 4 shows identical per-question discrepancy counts (2545/1727, 1821/659, 264/195) across all datasets. OW-L learns accuracies by minimizing a squared-error objective over second-order information (Equation 7), while OW-I uses ISP predictions as pseudo-ground-truth. These are fundamentally different estimation pipelines; producing indistinguishable results requires explanation. Until resolved, this reduces confidence in the evaluation pipeline.

### Minor

- **The ISP derivation (Section 4.2) transitions from Equation (3) to Equation (4) without adequate justification.** Equation (4) swaps conditioning events inside the probability terms, presented as "a natural alternative," but the logical motivation connecting the two expressions is not explained. The formal definition of ISP (Equation 5) then averages over non-observed answers with a 1/(K−1) factor, presented as a definition rather than derived from the preceding intuition. A clearer step-by-step derivation would strengthen the paper.

### Trivial

None.

## Nice-to-Haves

- Show empirically that the advantage ordering predicted by Theorem 2 (not just accuracy) holds on real datasets, to bridge the theoretical and empirical halves more directly.
- Include a simple baseline weighting each model by validation-set accuracy as a controlled comparison for the OW-L/OW-I results.

## Removed Points

The following points from the input review were removed with justification:

1. **"Theorem 2 is about advantage, not accuracy — logical gap"** — REMOVED. The theorem explicitly states its claim is about E[Adv(s*)]. The paper does not claim Theorem 2 directly proves accuracy; the empirical evaluation (Section 5) tests accuracy and confirms the predicted ordering. The theory provides motivation; the experiments validate accuracy separately. No logical gap exists because the claims concern different quantities.

2. **"Position bias assumption is questionable"** — REMOVED. The paper explicitly states this as an assumption (line 51), cites supporting work (Guo & Vosoughi, 2024), and notes random shuffling is standard practice. Every theoretical model makes assumptions; this one is clearly scoped.

3. **"Conditional independence may not hold"** — REMOVED. The paper acknowledges this limitation (line 63), states it "may not hold perfectly in the LLM setting," and points to Appendix C for extensions. Experiments run on real data where this assumption is violated, and the methods still work.

4. **"Missing baselines (weighted voting, confidence-based)"** — REMOVED. OW itself is a principled weighted voting scheme. The paper's baselines (MV, SP, Single Best, OPT) are adequate for its core comparison.

5. **"Missing confidence intervals"** — REMOVED. The paper reports t-statistics establishing statistical significance (line 303). Large-scale benchmark evaluations with the reported setup are standard.

6. **"Small practical improvements"** — REMOVED. 0.54–1.45 pp gains are modest but statistically significant and consistent across three datasets. Small gains can be practically meaningful, especially in high-stakes settings like healthcare.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Resolve the σ_K inconsistency: the overview must match the methods section (exponential form σ_K(x) = eˣ/(K−1+eˣ)).
- Explain why OW-L and OW-I produce identical results across all datasets — is this due to the 4-model ensemble structure, rounding, or something else?
- Provide a clearer step-by-step derivation from SP to ISP, showing why Equation (4) follows from the intuition about prediction bias.

---

### Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| LLM aggregation majority voting (strong reject) | 8QTpYC4smR.md | 1.00 | R1 | No | Systematic review; our paper is substantially stronger conceptually and empirically. |
| LLM aggregation majority voting (strong reject) | 5kMwiMnUip.md | 1.40 | R1 | No | Jailbreaking paper; not comparable in contribution. |
| Information aggregation theory (1.5–3.5) | E2CR6hmV1I.md | 3.00 | R1 | No | Multi-agent learning paper; our paper has more rigorous theory. |
| Information aggregation theory (1.5–3.5) | PQrkWvQSL0.md | 2.50 | R1 | No | Drug discovery multi-agent; our paper has cleaner problem framing. |
| LLM weighted voting (3.5–5.5) | yCEf1cJDGh.md | 5.25 | R1 | Yes | Truthful aggregation paper; our paper has stronger theory and more comprehensive experiments. |
| LLM weighted voting (3.5–5.5) | obYDlJN0oU.md | 4.25 | R1 | No | Multi-agent market simulation; less relevant to aggregation. |
| Multi-agent LLM reasoning (5.5–7.5) | JtGPIZpOrz.md | 6.67 | R1 | Yes | Multiagent finetuning paper; our paper has more theoretical depth but a narrower experimental scope. |
| Multi-agent LLM reasoning (5.5–7.5) | Yol6nUVIJD.md | 6.00 | R1 | Yes | ReConcile multi-agent debate; our paper has cleaner theory but the ReConcile paper has more extensive evaluations. |
| Multi-agent LLM reasoning (5.5–7.5) | QAwaaLJNCk.md | 6.00 | R1 | No | Multiagent debate; similar scope to ReConcile. |
| Optimal weight aggregation (5.0–7.0) | grM2Yv49cI.md | 6.00 | R2 | Yes | Model aggregation paper; our paper has stronger theoretical guarantees but the σ_K and OW-L/OW-I issues are more salient. |
| Optimal weight aggregation (5.0–7.0) | ecIvumCyAj.md | 5.75 | R2 | Yes | LLM mixture via filtering; comparable score band but different methodology; our paper has cleaner presentation. |

**Bracket after Round 1:** 5.0–7.0. The paper clearly outperforms the 1–3 band papers and is stronger than the 5.25 "Truthful Aggregation" paper. It is comparable to the 6.00–6.67 band papers but held back by unresolved issues (σ_K inconsistency and unexplained OW-L/OW-I identity).

**Narrowing (Round 2):** Comparing rated items against anchors: the paper's strengths (favorability 12.86, 12.61, 12.27) are notably strong, similar to the 6.00 anchors' strongest items. However, its two Major weaknesses — σ_K inconsistency (favorability 1.27) and OW-L/OW-I identity (favorability 2.01) — are concretely identifiable problems, unlike the more methodological concerns in the anchors (e.g., "insufficient experiments" with favorability −1.79 in grM2Yv49cI). The paper's issues are presentation/verification problems rather than fundamental methodological flaws, which places it slightly below the 6.67 "Multiagent Finetuning" anchor but comparable to the 6.00 "Model aggregation" and 6.00 "ReConcile" anchors.

**Final score:** 6.0. The theoretical contribution and empirical breadth are solid, but the two unresolved issues must be addressed before the paper can be a clear accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>