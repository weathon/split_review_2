Now I have verified all claims against the paper. Let me write the final consolidated review.

---

## Summary

This paper proposes R-HORIZON, a method that constructs multi-horizon reasoning tasks by composing existing single-problem benchmarks with answer-dependent substitutions (linking one problem's answer as a key variable in the next). Using this approach, the authors build a benchmark spanning math, code, and agent tasks, evaluate ~25 LRMs, and further use composed data for reinforcement learning. Key findings: (1) even frontier models degrade severely as the number of composed problems increases; (2) LRMs have limited effective reasoning length, localized reflection, and poor thinking budget allocation; (3) RL training on composed data improves both multi-horizon and single-problem accuracy on a 7B model.

## Strengths

- **Well-motivated gap.** The paper correctly identifies that existing benchmarks evaluate reasoning on isolated, independent problems, while real-world use cases often require sequential interdependent reasoning. Section 1 makes this case clearly and concretely.

- **Composition method is clean, scalable, and leverages existing resources.** The key idea (Algorithm 1) — substituting a key integer in problem *i*+1 with a placeholder resolved by the answer to problem *i* — is simple, reproducible, requires no manual annotation, and can be applied at scale to any integer-answer dataset.

- **Broad model coverage in evaluation.** Table 1 (Figure 3) reports results for ~25 models from 1.5B to 235B parameters, including frontier closed-source models (o4-mini, Gemini-2.5-Pro, Claude-Sonnet-4) and open-weight reasoning models, lending credibility to the observed degradation trends.

- **Non-obvious RL training finding.** The result that training on composed problems (n=2) improves not only composed-task performance (+17.4 on AIME24 n=2) but also single-problem AIME24 accuracy (+7.5) is striking and practically useful. The associated finding that composed-data training reduces overthinking (shorter generations) is a genuinely interesting secondary result.

## Weaknesses

### Fatal

None.

### Major

- **Data error in the main evaluation table (Figure 3).** The row for "Qwen3-32B" (line 157) reports **127.6%** accuracy on MATH500 at n=4 — an impossible value for an accuracy metric. Additionally, "Qwen3-32B" appears **twice** in the same table block (lines 157 and 162) with entirely different results (e.g., 51.7 vs. 86.6 on MATH500 n=3). This makes it unclear which set of numbers is correct for this model. Since the main quantitative claim of the paper — that performance degrades with increasing reasoning horizon — depends on trusting this table, this error undermines confidence in the evaluation data. The authors must correct the impossible entry and clarify the duplicate before the numerical claims can be taken at face value.

- **"Effective" metric in the rollout efficiency analysis is undefined and the percentages are internally inconsistent.** The paper (lines 303–307) states it "compute[s] the proportion of Solve None, Solve All, and Effective samples" but never defines "Effective." The reported percentages do not sum to 100% or any consistent total across rows (e.g., for n=1 at step 100: 80+30+20=130; at step 600: 65+3+35=103). Without a clear definition and mutually exclusive categories, the central claim that "composed datasets yield more balanced reward signals" and that "n=4 obtains 20% more effective samples" cannot be verified from the data presented. This undermines a key supporting argument for the training benefit of R-HORIZON.

- **RL training experiments conducted on a single model only.** All RL training uses R1-Qwen-7B (line 215). The abstract and conclusion present the training benefit as a general property of R-HORIZON data ("promotes accuracy on standard reasoning tasks," "enhancing and evaluating the long-horizon reasoning capabilities"), but no evidence is provided that the results (improved single-task accuracy, reduced overthinking, better budget allocation) hold for larger models or different reasoning model families. Given that the evaluation analysis itself shows substantial behavioral differences between 7B and 32B models, there is no basis to assume transfer of the training benefit.

### Minor

- **Confound in the RL comparison.** The baseline "Naive Training Data (n=1)" uses the original Skywork-OR1 training data, while the composed conditions use a filtered data pool (D_filtered, constructed via seed filtering in Section 3.1). This means the comparison conflates composition with a different problem distribution. Some of the observed improvement could be due to the filtering step itself rather than composition.

- **Alternative explanation for token efficiency not discussed.** Training with composed data is claimed to "alleviate the overthinking phenomenon" (Section 5.2). However, the observed shorter generations could also be explained by the model learning to exploit the dependency structure (e.g., reusing computations across subproblems) rather than learning better reasoning per se. This alternative is not acknowledged.

- **Internal inconsistency: 25 vs. 26 models.** The introduction (line 28) states "evaluating 26 LRMs" while Section 4.1 (line 136) states "We select 25 advanced LRMs." The table has 26 entries but Qwen3-32B appears twice (likely a duplicate), so both numbers could be correct depending on whether entries or unique models are counted. This imprecision should be resolved.

- **Model naming inconsistency.** The evaluation results caption (line 140) refers to "Qwen3-235B-A22B-Thinking" while the table (line 149) lists "Qwen3-235B-Thinking." These appear to be the same model but the mismatch is confusing.

### Trivial

- No limitations section is included. Several should be acknowledged (narrow dependency structure limited to arithmetic substitution, RL training single-model, harsh all-or-nothing metric).
- No confidence intervals or variance estimates for key evaluation results.

## Nice-to-Haves

- Extending RL training to at least one additional model size (e.g., R1-Qwen-32B) would substantially strengthen the generalizability of the training claims.
- Clarifying whether the "Effective" metric is defined as "samples where at least one subproblem is solved but not all" or some other consistent definition, and ensuring mutual exclusivity of categories.
- Statistical significance or confidence intervals for the reported results, particularly for the key training comparisons at larger n where sample sizes may be small.
- A discussion of the verifier model *M* used in seed filtering (which model, reliability) — likely already in the (stripped) appendix; the main text would benefit from a brief note.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Verifier model details (asked "which model M?").** The paper mentions a model *M* for seed filtering (line 58) but does not specify which model. However, this detail is almost certainly in Appendix A, which was stripped by the parser. Per the instructions, missing appendix content should not be counted as a weakness.

- **"The paper does not control for whether base single-problem accuracy of larger models is higher."** The paper's expected accuracy metric (Equation 4) explicitly addresses this by computing the product of atomic pass rates. The reviewer partially acknowledged this. The remaining point (independence assumption) is a known limitation of decomposition-based metrics but is not a novel or paper-specific flaw.

- **Precision nitpick on "more than half of the problems lack long-range reflection."** The claimed quantification is supported by the visualization in Figure 7. The level of precision is appropriate for this type of analysis.

## Novel Insights

The reviews do surface a dimension not fully appreciated from the paper alone: the seed-filtering confound in the RL comparison (naive baseline vs. filtered pool) means the paper's central training claim — that *composition* specifically drives the improvement — has not been cleanly isolated. This is a genuine methodological blind spot rather than a scope limitation. No other novel insight emerges beyond the paper's own contributions.

## Suggestions

1. **Fix the data errors.** Correct the 127.6% entry and resolve the duplicate Qwen3-32B row. If one row corresponds to a different variant (e.g., Qwen3-32B-Instruct), rename it.
2. **Define "Effective" unambiguously.** Provide a clear definition and either ensure categories are mutually exclusive or explain why they are not.
3. **Add a controlled RL experiment.** Compare training on single problems from the *same filtered pool* vs. composed problems from that pool, to isolate the effect of composition from seed filtering.
4. **Acknowledge the single-model scope.** The abstract and conclusion should qualify the training claims as demonstrated on R1-Qwen-7B.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>