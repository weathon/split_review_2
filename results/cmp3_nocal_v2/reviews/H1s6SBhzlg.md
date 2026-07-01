## Summary

This paper proposes two aggregation algorithms — Optimal Weight (OW) and Inverse Surprising Popularity (ISP) — for combining responses from multiple LLMs. The core idea is to move beyond simple majority voting (zero-order) by exploiting first-order information (agent accuracies) and second-order information (answer correlations between agents). The paper proves that OW is Bayesian-optimal among all aggregators under conditional independence (Theorem 1), and establishes the theoretical ordering ISP > MV > SP in expected advantage (Theorem 2). Experiments on synthetic data, UltraFeedback, MMLU, and a healthcare dataset (ARMMAN) show consistent improvements over majority voting.

---

## Strengths

1. **Bayesian optimality result (Theorem 1) is a genuinely non-trivial theoretical contribution.** Showing that a linear weighted rule — the OW algorithm — is optimal among *all* possible aggregators (not just linear ones) under the stated assumptions is a clean, strong result that goes beyond what most prior work in multi-LLM aggregation establishes. It also provides an interpretable connection to log-odds weighting.

2. **Principled ISP design grounded in theory, not ad hoc tuning.** The paper identifies *why* the standard Surprisingly Popular rule underperforms in the LLM setting (systematic biases are less pronounced than in human crowds) and proposes a counterfactual variant (ISP). Theorem 2's crisp ranking ISP > MV > SP is a clean theoretical statement that resolves which method to use.

3. **Empirical validation across diverse domains with per-question analysis.** The experiments span synthetic data (matching the model assumptions exactly), standard LLM benchmarks (UltraFeedback, MMLU), and a real-world healthcare application (ARMMAN). Table 4 provides per-question win/loss counts, giving a more informative picture than a single aggregate number. The t-statistics (12.53, 23.39, 3.22) confirm statistically significant improvements over MV.

---

## Weaknesses

### Fatal

None.

### Major

1. **σ_K defined inconsistently between the abstract and the main body.**  
   The abstract/overview (line 25) defines σ\_K(x) = x²/(K−1 + x²), while Section 3 (line 73) defines σ\_K(x) = eˣ/(K−1 + eˣ). These are mathematically distinct functions. The body of the paper (lines 73, 90) is internally consistent — Algorithm 1 and Corollary 1 both use the exponential form — so the intended definition is clearly the exponential one from Section 3. However, the conflicting definition in the abstract makes the paper appear ambiguous about its own core method. A reader who skims the abstract and turns to the algorithm will encounter two different weight functions. **This does not invalidate the theorem (the proof in the appendix presumably uses the exponential form that matches the body), but it is a significant presentation error that must be fixed.** The authors should state σ\_K unambiguously in one place and use it consistently throughout.

2. **OW-L and OW-I produce identically identical results across all three datasets, which is suspicious and unexplained.**  
   In Table 3, OW-L and OW-I achieve the exact same accuracy on every dataset (73.66%, 90.37%, 85.78%). In Table 4, the per-question counts for OW-L and OW-I are also identical (2545/1727, 1821/659, 264/195). These are two different estimation pipelines (ERM-based accuracy learning vs. ISP-based pseudo-label accuracy estimation) and should, in principle, produce different predictions on at least some questions. The paper provides no explanation for why they converge to identical results. This either indicates a reporting conflation, that the two methods collapse to the same accuracy estimates for an unarticulated reason, or that the methods are more similar than described. **The authors must explain this.** If the methods are genuinely different, showing diagnostic plots (estimated accuracies from both methods, or a breakdown of where they disagree) would resolve the concern.

### Minor

3. **The conditional independence assumption (Assumption 1) is central to all theorems but is acknowledged to be violated in practice.**  
   The paper states on line 63 that "this assumption may not hold perfectly in the LLM setting" and claims to extend results to a more general setting in Appendix C (which is stripped from the submission). The only robustness evidence is the real-dataset experiments, where gains over MV are modest (0.54%–1.45% absolute). This is a standard limitation for any work making conditional-independence assumptions, and the paper handles it better than most by acknowledging it explicitly. Still, the gap between the strong theoretical claims (optimality, dominance) and the modest empirical corroboration under violated assumptions should be discussed more transparently.

4. **The OW-L optimization pipeline (Equation 7) is under-specified.**  
   The objective minimizes the squared error between the true conditional probabilities (functions of the accuracies) and the empirical second-order information. The paper gives no detail about the optimization algorithm, initialization, convergence criteria, or whether the problem is convex. The expanded expressions are deferred to the stripped Appendix F.2. While deferring implementation details to the appendix is normal, the main text should at least state the nature of the optimization (e.g., closed-form? gradient-based? guaranteed to find the global optimum?).

### Trivial

5. **Theorem 3 uses a ≳ (greater-than-or-approximately) symbol and Õ notation without constants.**  
   While this presentation is standard in theoretical computer science, it would be more informative to provide a clean finite-sample inequality. This is a minor presentation preference.

---

## Nice-to-Haves

- **Ablation on the number of agents N.** The theory covers general N, but experiments fix N=4. Showing whether the gains persist, increase, or diminish with more/fewer agents would strengthen the practical guidance.
- **Cost-benefit discussion.** Running multiple LLMs and computing second-order information is more expensive than majority voting. A brief discussion of computational overhead and when the modest accuracy gains (0.5–1.5%) are worth it would help practitioners.
- **Confidence intervals** for the real-world accuracy numbers, beyond the t-statistics comparing against MV, would help assess whether differences between OW-L, OW-I, and ISP are meaningful.

---

## Removed Points

The following points from the input review were removed as invalid, speculative, or noise:

- **MMLU single-best gap:** The critic claimed the paper "groups" MMLU with datasets where aggregation beats all individual models. The paper explicitly states (line 301) "our aggregation methods outperform all participating models on **both UltraFeedback and ARMMAN**" — deliberately omitting MMLU — and calls Single Best a "clairvoyant oracle" (line 287). The paper is honest about this limitation; the criticism is factually incorrect.
- **SP formulas not depending on question difficulty:** The critic found it suspect that the expected advantage formulas depend only on accuracies and not on question difficulty. This is expected for expectation-averaged quantities — the per-question difficulty is integrated out. Not a genuine weakness.
- **Theorem 1's "for any ℙ" claim being too strong:** This is exactly the theorem statement; the critic provided no evidence it is incorrect. Speculative.
- **Position bias (Proposition 1):** The critic claimed the ordering-invariance assumption is "strong" but the paper already cites Guo & Vosoughi (2024) and acknowledges it. This is a standard assumption made explicit.
- **Generic requests** (e.g., larger ablation, failure mode analysis) that are reasonable extensions but not weaknesses of the current paper.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Fix the σ_K definition:** Use the exponential form (eˣ/(K−1+eˣ)) consistently in the abstract, main text, and algorithm box. Include a brief proof sketch (½ page) in the main text showing how the posterior odds computation leads to σ_K^{-1}(x_i) as the optimal weight.
2. **Explain the OW-L/OW-I identity:** Clarify whether the two methods genuinely produce different accuracy estimates. If so, explain why they yield identical predictions. If they converged to the same solution for the reported ensemble, say so and show diagnostic evidence (e.g., estimated accuracy vectors from both methods).
3. **Provide optimization details for Equation 7:** Specify whether the problem is convex, what solver was used, and how initialization was handled.
4. **Acknowledge the MMLU result more transparently:** While the paper already handles this honestly, a sentence in Section 5.4 discussing why aggregation underperforms the best single model on MMLU (e.g., ceiling effects, strong model dominance) would strengthen the discussion.

---

## Score and Decision

This paper has a strong core idea and genuinely non-trivial theory. The Bayesian optimality result (Theorem 1) and the ISP > MV > SP ordering (Theorem 2) are clean, well-motivated contributions that advance the multi-LLM aggregation literature. The empirical validation, while showing modest gains, is consistent across multiple domains.

However, two issues require attention: (a) the σ_K inconsistency between the abstract and the body, which is a significant presentation error even though the body is internally consistent, and (b) the suspiciously identical results from OW-L and OW-I, which need explanation. These are fixable issues that do not undermine the paper's core theoretical contributions, but they must be resolved before the paper can be accepted.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>