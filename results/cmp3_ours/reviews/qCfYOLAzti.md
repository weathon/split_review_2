## Summary

This paper identifies a failure mode of gradient-ascent-based LLM unlearning methods — the "squeezing effect," where probability mass shifts into semantically related rephrasings rather than being truly removed. The authors propose a bootstrapping framework (BS-T at token level, BS-S at sequence level) that jointly suppresses both target responses and the model's own high-confidence generations ("beliefs"). The method is motivated by mechanistic analysis, supported by theoretical analysis within an AKG learning-dynamics framework, and validated on TOFU, WMDP, and MUSE benchmarks.

## Strengths

1. **Concrete problem diagnosis with reproducible case studies.** Section 3.1 presents two clear failure cases (GA-induced syntactic collapse and NPO-driven semantic rephrasing) with actual model outputs, directly demonstrating why ROUGE, Truth Ratio, and probability metrics can misreport unlearning success. Case 2 (NPO rephrasing "She mainly writes in English" while metrics show low scores) is effective evidence that is more than a conceptual argument — it is a reproducible demonstration.

2. **Clean logical chain from analysis to method design.** The paper traces a well-motivated path: (a) GA/NPO suppress target responses → (b) softmax normalization squeezes probability mass into semantically similar high-likelihood regions → (c) these regions correspond to the model's own high-confidence predictions ("beliefs") → (d) suppressing those beliefs counters the squeezing effect. The two-level instantiation (BS-T for token-level local beliefs, BS-S for sequence-level global beliefs) follows naturally from this chain rather than being tacked on.

3. **Theoretical analysis expresses the mechanism concisely.** Theorem 5.2 cleanly shows G_BST[v] = G_GA[v] + λ q^i[v], making precise how BS-T adds suppression pressure on high-likelihood alternatives relative to standard gradient ascent. This is simple but informative.

## Weaknesses

### Fatal
None.

### Major

1. **No measures of variance or significance on core results.** The TOFU results in Table 1 report only point estimates without standard deviations, confidence intervals, or statistical significance tests across multiple runs. With many memorization improvements as small as 0.01–0.03 (e.g., FORGET 10% 1B: Mem. 0.59 vs 0.58; FORGET 5% 3B: Mem. 0.55 vs 0.55 — a tie), it is impossible to determine whether these differences represent genuine improvement or random variation. This is the most significant empirical gap and undermines the paper's central claims of "superior performance."

2. **Memorization gains are modest, and utility improvements often outpace forgetting gains.** The paper frames its contribution as achieving "more thorough forgetting" (abstract) and "superior performance" (contributions). However, the memorization improvements over NPO are frequently 0.01–0.03, with larger gains (0.04–0.06) only emerging at 1% forget settings with larger models (8B). In many configurations, utility improvements are substantially larger than memorization improvements (e.g., FORGET 5% 1B: Util. +0.08 vs Mem. +0.01; FORGET 10% 1B: Util. +0.05 vs Mem. +0.01). This pattern suggests the primary benefit may be better utility preservation at comparable forgetting levels, rather than "more thorough forgetting" — a distinction the paper does not discuss or acknowledge.

3. **WMDP forget scores are near the random floor and do not discriminate between methods.** On WMDP (Table 2), random guessing produces 0.25 accuracy. BS-S gets Bio 0.26 and Cyber 0.27; NPO gets 0.27/0.30; RMU gets 0.29/0.27. All methods converge to near-random, making differences of 0.01–0.03 uninformative as evidence of better forgetting. The paper's WMDP evidence for better forgetting is not meaningful; the real differentiator is MMLU retention (utility), which the paper does acknowledge but does not highlight as the primary WMDP contribution.

### Minor

4. **LLM judge evaluation lacks calibration reporting.** The paper uses Gemini 2.5 Flash as an LLM judge for the Naturalness and Similarity evaluation (Fig. 4c) — the same class of metric whose unreliability the paper criticizes in §3.1. No inter-rater reliability, human correlation, position bias analysis, or calibration checks are reported. While the LLM judge is used as an auxiliary probe (not the primary metric), and this practice is common in the community, the specific claim that the method "mitigates spurious unlearning" relies partly on this evaluation and would benefit from validation.

5. **BS-T's top-k design may miss mid-likelihood knowledge.** BS-T only suppresses the top-k tokens at each position. The paper's own Fig. 2a shows that mid-likelihood responses (20–60%) have non-trivial semantic similarity (~2.8 on a 0–5 scale), indicating some related knowledge persists outside the top-k window. The paper does not discuss whether the squeezing effect could shift mass into these mid-likelihood regions that BS-T would not address.

6. **Theoretical analysis characterizes rather than explains the performance advantage.** Theorem 5.2 is a definitional consequence of how BS-T is constructed — it shows what the method does (adds λq^i[v] to the GA residual) but does not go further to explain why this residual change leads to better unlearning outcomes. The eNTK/lazy-training assumption (Lemma 5.1) is also strong for unlearning, where the model can undergo significant distribution shifts; the paper acknowledges this for on-policy BS-S (line 292) but not for BS-T.

7. **Gap to the retrain baseline is not discussed.** The Retrain row in Table 1 represents the gold standard (training from scratch without forget data). BS-S never reaches Retrain levels, and the gap is non-trivial in several settings (e.g., FORGET 1% 8B: Retrain Agg. 0.62 vs BS-S 0.49; FORGET 5% 1B: Retrain 0.64 vs BS-S 0.58). The paper does not acknowledge or discuss this gap.

### Trivial
None.

## Nice-to-Haves

- **Disaggregated analysis of where gains come from.** The paper could strengthen its mechanistic claim by showing that BS methods specifically outperform baselines on metrics that detect semantic rephrasing (e.g., the Similarity score from LaaJ) while keeping standard memorization metrics comparable — directly tracing improvement to the claimed mechanism.
- **Qualitative comparisons of generated outputs.** Extending the case studies in §3.1 to show, for a set of prompts, what NPO generates (semantically related rephrasing) versus what BS-S generates (truly different/refusal), would provide complementary evidence beyond aggregate metrics.
- **Hyperparameter sensitivity analysis** in the main paper rather than deferred to appendix.
- **MUSE results** in the main paper rather than entirely relegated to the appendix (currently Appx. F.3).

## Removed Points

The following points from the input review were removed:

1. **Criticism that the aggregate metric (Agg.) conflates forgetting and retention (Issue 2).** The paper explicitly reports both Agg. AND Mem. separately and makes the claim about "best aggregate AND memorization scores" — the data supports the claim that BS-S achieves the best Mem. scores in most configurations. The criticism is not factually supported by the paper's reporting.

2. **Criticism about the "code merged to [OpenUnlearning](#)" placeholder reference.** This is a formatting artifact from PDF extraction; the original submission likely has a proper reference.

3. **Generic speculation about LLM judge biases** without checking whether the paper's specific judge might have been validated or whether the evaluation is robust to known biases. The point about missing validation is kept (Weakness #4), but the speculative framing is removed.

## Novel Insights

The insight that gradient-ascent-based unlearning suffers from a "squeezing effect" — where suppressing target responses causes probability mass to redistribute into semantically related high-likelihood regions that the model already confidently predicts — is a concrete, testable characterization of why standard unlearning metrics can mislead. The connection to the model's own "beliefs" as the natural region where squeezed mass accumulates, and using those beliefs as auxiliary forgetting targets, is a well-motivated design principle. None of the reviews surfaces a perspective that goes significantly beyond what the paper itself lays out.

## Suggestions

1. Report means and standard deviations across multiple random seeds (3–5 runs) for all main experiments.
2. Acknowledge the utility-vs-forgetting benefit pattern explicitly and reframe claims about "more thorough forgetting" to match what the memorization metrics actually show (the method primarily preserves utility while achieving comparable or marginally better forgetting).
3. Either validate the LLM judge with human correlation or inter-annotator agreement, or treat the LaaJ results explicitly as illustrative rather than primary evidence.
4. Discuss the gap to the retrain baseline and the limitations of the top-k design choice.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>