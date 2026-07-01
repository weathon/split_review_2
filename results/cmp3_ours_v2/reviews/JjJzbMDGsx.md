Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper introduces the Language Confusion Gate (LCG), a lightweight MLP that intervenes at decoding time to dynamically filter tokens from unintended language families in multilingual LLM generation. The method is motivated by a novel mechanistic finding — that output token embedding norms are larger for high-resource languages (CJ, Latin), biasing sampling toward them — and uses norm-adjusted self-distillation to train the gate on the model's own debiased predictions. Evaluated across four "no-think" and three "thinking" models on translation and reasoning benchmarks, LCG reduces confusion rates substantially (especially CJ confusion, often by ~10×) with minimal overhead (0.4% latency increase).

## Strengths

1. **The norm imbalance analysis (Section 3.2, Table 1, Figure 2) is a genuine mechanistic contribution.** The decomposition of logits into ‖h‖·‖e_i‖·cos_sim(h, e_i) and the finding that CJ/Latin tokens disproportionately occupy the top-5% of embedding norms (e.g., 10.74% CJ vs. 0.14% Low-Res in Qwen3-8B) provides a clean, testable explanation for one source of language confusion. This goes beyond observing that confusion happens and offers a concrete mechanism that LCG then addresses.

2. **The gate is genuinely lightweight with measured overhead.** The intervention rate of 0.33–0.38% of tokens and measured latency increase of 0.4% (15.95ms → 15.99ms per step) are concrete, directly reported evidence of practicality.

3. **The paper takes the code-switching vs. confusion distinction seriously.** The FLORES-NO-LATIN / FLORES-WITH-LATIN partitioning, the human-annotated code-switch preservation test, and the explicit design choice to never mask Symbols or Low-Res tokens show thoughtful engagement with the hard part of this problem.

4. **Evaluation breadth across model families and scales** — Qwen3-8B/30B, Llama3.1-8B, Gemma3-12B, GPT-OSS-20B — plus both standard and thinking-mode setups, strengthens the generality of the findings.

## Weaknesses

### Major

1. **ORPO baseline comparison lacks sufficient detail to support the "outperforms training-based methods" claim.** The paper reports that ORPO causes accuracy drops on INCLUDE (61.4→57.3 for Qwen3-8B, 46.1→43.2 for Llama3.1-8B) but provides no hyperparameters, training steps, learning rate, or data composition details beyond "a multilingual dataset with synthesized confusion samples similar to Lee et al. (2025)" (Section 5.3). ORPO's effectiveness is highly sensitive to preference data quality and training budget. The accuracy degradation could reflect a poorly tuned ORPO run rather than a fundamental trade-off. The comparison as presented does not support the claim of superiority over training-based alternatives.

2. **The code-switching preservation analysis has an unresolved off-policy confound.** The 86.7% preservation test (Section 5.3) checks whether LCG *would have* allowed human-validated English tokens *on the original (no-LCG) generation path*. When LCG is active during actual generation, earlier token choices differ, so the set of confusion points changes. Whether the 86.7% rate holds on-policy is unknown. The paper does not discuss this limitation.

### Minor

3. **No variance or confidence intervals reported for any confusion rate or task metric.** All results in Tables 1–5 are point estimates. Given that confusion rates are small fractions (0.0–12.1%) where a single misclassified generation can shift rates measurably, the reader cannot assess whether the reported reductions are stable or within noise. While the qualitative pattern (large reductions in CJ confusion) is almost certainly robust, individual numbers like 0.12%→0.00% for Qwen3-30B CJ confusion (Table 4) need variance bounds to be interpretable.

4. **The "Low-Res" family is a black box: cross-low-resource confusion is neither measured nor addressed.** The gate classifies all non-CJ, non-Latin, non-Symbol tokens as a single family. Confusion *between* different low-resource scripts (e.g., generating Korean characters in Thai text, or Cyrillic in Arabic) cannot be detected. The paper acknowledges this in the limitations (Section 6, line 320) but does not quantify how frequent such confusion is, so the reader cannot gauge how much of the problem remains unaddressed.

5. **"Order of magnitude" framing is uneven across results.** CJ confusion consistently drops by ~7–45× (genuine order-of-magnitude). But Latin confusion drops by only 2–6× for Llama3.1-8B (8.4%→2.9%), Gemma3-12B (1.0%→0.5%), and Qwen3-8B (12.1%→2.0%). The abstract's "often by an order of magnitude" is qualified but could mislead a casual reader into expecting uniformly larger reductions. The paper would benefit from explicitly distinguishing CJ and Latin confusion in the abstract.

6. **Training hyperparameters k and p for pseudo-target generation (Section 4.2) are not reported.** The pseudo-targets are constructed using "top-k/p filtering" of norm-adjusted logits, but the specific k and p values are omitted. Since these control how permissive or strict the gate's training signal is, they are necessary for reproducibility.

### Trivial

7. **Table 4 header says "No-Think Models" when the content and surrounding text describe thinking-model results.** This is clearly a copy-paste typo and should be corrected.

8. **The rationale for not using LCB (Section 5.2) is stated without examples.** The paper says "some LCB queries require natural code-switching" and "its language detector sometimes produces wrong results" but provides no concrete instances. Since LCB is the only prior standardized benchmark for this phenomenon, supporting the decision with at least one example would strengthen the exposition.

## Nice-to-Haves

- Bootstrap confidence intervals (or Clopper-Pearson intervals for confusion rates) would substantially strengthen the evidential value of all tables.
- An ablation of individual intervention rules (Section 4.3), particularly Rule (2) where the gate defers to high-confidence model output, would clarify how much autonomy the gate actually has.
- A breakdown of confusion reduction by individual target language in the FLORES-NO-LATIN evaluation would reveal whether some languages benefit more than others.
- If the ORPO comparison is retained, full training details (hyperparameters, data size, steps, validation curves) should be reported.

## Removed Points

These points were identified in the input review but removed or demoted after cross-checking:

- **GPT-OSS availability concern** — REMOVED (hard rule: cannot question existence or release status of cited entities; the paper cites "OpenAI, 2025" and this must be treated as real).
- **Figure 2 norm analysis criticism** — Partially inaccurate. The reviewer claimed the top-10 after norm adjustment are all Latin tokens. In fact, the *top-1* token is the Hebrew character "נ״" (43.75%), followed by nine instances of "n". The paper's claim that norm adjustment "provides a signal for correct next-token language family" is supported by the top-1 being correct. Demoted from weakness.
- **Reasoning length increase counterintuitiveness** — REMOVED. A 34-token increase (3327→3361) on a generation of thousands of tokens is negligible and plausibly noise; masking tokens can change the generation path in ways that either increase or decrease total length.
- **Generic scope-creep concerns** (e.g., "should use more languages", "should study more baselines") — REMOVED as unfocused speculation.

## Novel Insights

The input review's most valuable observation is the unresolved tension between the off-policy 86.7% code-switch preservation test and the on-policy code-switch rate reductions (Table 5). The paper reports both numbers but does not reconcile them: if LCG allows English at 86.7% of confusion points from the original generation, why does the overall code-switch rate drop from 46.34% to 25.90%? The answer likely involves a shifted distribution of confusion points under LCG-guided generation — but this is not analyzed or discussed. This gap is the single most important unresolved issue in the evaluation.

## Suggestions

1. Add bootstrap confidence intervals to all confusion-rate and task-metric tables (the paper's central claims rest on small-rate comparisons).
2. Report the specific k and p values used during pseudo-target construction (Section 4.2).
3. Either fully document the ORPO training setup or soften the "outperforms training-based methods" claim to acknowledge the baseline's limited tuning.
4. Run the code-switch preservation test on-policy: generate with LCG active and have human annotators judge whether the retained/lost English tokens were legitimate.
5. Fix the Table 4 header typo.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gwZ90hFSL2.md | 1.00 | Round 1 (strong reject) | Poor-quality survey paper; not comparable — this paper has real experiments and analysis |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/fSbPwHjdDG.md | 3.00 | Round 1 (reject band) | "Llamas (mostly) think in English" — single-task study with too-strong intervention; our paper is significantly stronger |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/eznTVIM3bs.md | 5.25 | Round 1 (borderline band) | "Rise and Down of Babel Tower" — interesting hypothesis but missing details; our paper has more thorough evals and clearer practical contribution |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BCyAlMoyx5.md | 5.67 | Round 1 (borderline band) | "Crosslingual Capabilities" — limited set of similar languages; our paper covers more diverse language families and a practical method |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4z3IguA4Zg.md | 6.00 | Round 1 (accept band) | "MLLM can see?" — structurally similar decoding-time intervention with mechanistic insight; comparable quality |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NCrFA7dq8T.md | 6.60 | Round 1 (accept band) | "The Same but Different" — clean mechanistic interpretability with narrow scope (2 tasks, 2 languages); our paper has broader scope |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/vf5aUZT0Fz.md | 8.00 | Round 1 (strong accept band) | Top-tier work with more originality and rigor; our paper is not at this level |

### Initial Bracket

The paper sits between score 5.5 and 7.5. It is clearly stronger than reject-range papers (3.00) and low-borderline papers (5.25–5.67) due to its concrete mechanistic contribution, breadth of models, and thoughtful evaluation design. It is comparable to decoding-time intervention papers in the 6.00–6.60 range ("MLLM can see?" at 6.00, "The Same but Different" at 6.60), but not at the level of high-impact papers (8.00). Narrowing from the weaknesses — the ORPO comparison gap and the off-policy code-switch confound are real but fixable, and do not threaten the core method.

### Final

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>