Now let me write the final consolidated review.

## Summary

This paper introduces the Language Confusion Gate (LCG), a lightweight MLP-based decoding intervention that reduces language confusion in multilingual LLMs. LCG is trained via norm-adjusted self-distillation—using the frozen model's own debiased top-k/p predictions as pseudo-targets—to predict permissible language families at each generation step, then dynamically masks disallowed tokens. Evaluated across 7 model variants (Qwen3, Llama3.1, Gemma3, GPT-OSS) on translation and reasoning benchmarks, LCG reduces CJ and Latin confusion rates by roughly an order of magnitude (e.g., Qwen3-30B CJ confusion 1.0%→0.0%, Latin confusion 4.4%→0.4%) with minimal computational overhead (0.4% per step) and no degradation in task metrics.

## Strengths

1. **Method is tightly motivated by mechanistic analysis.** Section 3 provides three concrete observations (confusion is rare, correct tokens are in the top-5 99.29% of the time, embedding norm bias favors high-resource languages), each of which directly informs a design choice (sparse intervention, masking based on language families, norm-adjusted self-distillation). This analysis-to-method chain is unusually clean.

2. **Norm-adjusted self-distillation (Section 4.2) is a principled and clever training signal.** Using the frozen model's own debiased logits as pseudo-targets avoids the need for any human-annotated confusion labels, and the ablation in Table 3 confirms that norm adjustment provides a meaningful improvement (e.g., Llama3.1-8B Latin confusion drops from 5.7% to 2.9% when norm adjustment is added). The connection back to the embedding-norm analysis in Section 3.2 gives the design internal coherence.

3. **Evaluation breadth is substantial and results are consistent.** The paper evaluates on 7 model variants (standard and thinking modes), two task types (translation with BLEU, reasoning with accuracy/Pass@k), and reports confusion reductions across all settings. Consistency across diverse architectures (Qwen, Llama, Gemma, GPT-OSS) provides reasonable evidence that the method generalizes.

4. **Practical efficiency is convincing.** The 0.4% overhead per generation step, the sparse intervention rate (0.33–0.38% of tokens), and the plug-in nature (no model modification) make a credible case for real-world deployment.

## Weaknesses

### Fatal

None.

### Major

1. **The FLORES+ dataset is used in both training and evaluation, which weakens generalization evidence.** The gate is trained on a composite dataset that includes the FLORES+ Dataset (Section 5.1, line 221), and the main evaluation uses FLORES-NO-LATIN and FLORES-WITH-LATIN, which are subsets of the same FLORES+ source (Section 5.2, line 231). Because the gate learns via self-distillation from the model's own predictions on FLORES+ data, there is a risk that the gate's behavior is specialized to patterns present in FLORES+ that may not hold for other text distributions. The INCLUDE evaluation partially mitigates this concern (it is a separate dataset), but INCLUDE only measures CJ confusion on a knowledge-and-reasoning task, not Latin confusion on a translation-like task. A held-out evaluation on a dataset with no source-level overlap with the training data would substantially strengthen the paper's generalization claims.

2. **No statistical significance or variance is reported for any result.** All confusion rates and task metrics in Tables 3–5 are reported as point estimates without confidence intervals, standard deviations, or multiple-run statistics. This matters because: (a) some confusion rates are very small (0.0%, 0.1%, 0.07%) and whether a change of this magnitude is meaningful depends on the number of samples; (b) accuracy differences between LCG-adjusted and No LCG on INCLUDE are sometimes tiny (e.g., Qwen3-30B: 71.12→70.83; Qwen3-8B: 61.43→61.76), and without variance estimates it is impossible to tell whether these reflect genuine task preservation or sampling noise; (c) the thinking model CJ% differences in Table 4 are as small as 0.06%, where a single token could determine the value. This is a standard expectation for empirical ML papers.

3. **The decision to not evaluate on the established Language Confusion Benchmark (LCB) is inadequately justified.** The paper provides a two-sentence rationale (Section 5.2, line 233): some LCB queries require code-switching and its language detector can produce false positives. These concerns may be valid, but without quantification (e.g., what fraction of LCB queries are affected, what is the detector's false-positive rate on relevant languages), the decision to opt out of the benchmark makes it difficult to compare results with prior work (Marchisio et al., 2024; Nie et al., 2025; Ji et al., 2025; Lee et al., 2025). The paper's evaluation on self-constructed FLORES subsets is reasonable on its own terms, but the absence of a direct link to the existing benchmark is a limitation.

### Minor

4. **The ORPO comparison lacks sufficient detail to be assessed as a fair baseline.** The paper states (Section 5.3, lines 298–299) that for ORPO they "prepare a multilingual dataset, and synthesize samples with language confusion as rejected samples similar as Lee et al. (2025)," but gives no specifics about the number of training steps, the ratio of preference pairs, hyperparameter tuning, or how many synthetic confusion samples were generated. Since ORPO is a training-based method that the paper positions as disadvantaged, and since the observed accuracy drop (e.g., Qwen3-8B INCLUDE from 61.4→57.3) is large enough to suggest possible suboptimal configuration, more detail is needed.

5. **The code-switch preservation evaluation in the first experiment is partially conditioned on the model's own behavior.** The first experiment (Section 5.3, line 284) selects code-switch examples from the *model's own outputs* (without LCG) that human annotators deemed natural, then checks whether LCG preserves those tokens. This evaluates preservation on the model's *natural* code-switching behavior, which is informative but is an upper bound: it does not test whether LCG would suppress a code-switch the model would *not* naturally produce but that a user might want. The second experiment (Table 5) partially addresses this, and the paper is transparent about the baselines being "just references for comparison" — but the framing still overstates what can be concluded.

6. **No analysis of the gate's false positive rate or precision/recall.** The paper reports confusion reduction and code-switch suppression rates, but does not evaluate the gate's accuracy directly (e.g., on a small annotated set with ground-truth language-family labels). Reporting the gate's precision and recall would help characterize its behavior beyond the downstream confusion metrics.

7. **The discussion of within-script confusions that LCG cannot correct is not quantified.** Section 6 (line 320) acknowledges the script-level granularity limitation, but the paper does not analyze what fraction of confusion errors are *within* the same script family (and thus fundamentally uncorrectable by LCG). This would help calibrate expectations.

### Trivial

8. In Table 3, Qwen3-8B shows BLEU 12.1 (No LCG), 11.9 (LCG-unadjusted), and 12.1 (LCG-adjusted). This is the only case where LCG-unadjusted degrades BLEU relative to baseline. A brief comment on whether this is random variation or a systematic effect of norm adjustment would be helpful.

## Nice-to-Haves

- Train the gate on a FLORES-free subset of the composite data and verify that confusion reductions on FLORES-NO-LATIN still hold. This would directly address the train/eval overlap concern.
- Report binomial confidence intervals for the confusion rate percentages given the number of generated tokens, or run multiple decoding seeds with variance.
- Provide a quantitative audit of LCB (e.g., "X% of LCB sentences have code-switching in the reference" or "the LCB detector has Y% false-positive rate on our testbed") to justify the decision to not use it.

## Removed Points

- The "Section 3.2" critique that norm-adjusted sampling should be used directly was removed because the paper explicitly addresses this ("can't be directly used for intervention... can't explain English↔Chinese confusion," line 155). The reviewer acknowledges this is "briefly mentioned"; it is a clarification request, not a weakness.
- The reviewer's suggestion that "No Rule" ablation results are "only mentioned in passing" was removed because the paper explicitly includes "No Rule" in Figure 3 and states the result in text (line 312). The request for a more detailed breakdown is a nice-to-have, not a weakness.
- The "code-switch preservation" concern about the first experiment being "partially circular" was kept (weakness #5) because the reviewer's characterization is accurate, but it was downgraded from the reviewer's framing as "Critical Issue" to Minor, since the paper acknowledges the limitations and provides a second experiment that partially addresses the issue.
- The reviewer's "Strengthening the Paper on Its Own Terms" section items are subsumed into Nice-to-Haves and the existing weaknesses.

## Novel Insights

None beyond the paper's own contributions. The reviews primarily surface methodological rigor concerns (data overlap, variance reporting, benchmark selection) that are standard evaluative observations rather than novel analytical insights about the paper's subject matter.

## Suggestions

- Add a single experiment where the gate is trained on the composite dataset *excluding* FLORES+, then evaluated on FLORES-NO-LATIN. If results hold, the generalization concern is resolved; if they degrade, the paper still gains insight into what training data is necessary.
- Report binomial confidence intervals for the confusion percentages in Tables 3–5 using the known number of generated tokens (provided for two models in Section 5.3). This is a low-effort fix with high evidential value.
- Expand the LCB rationale to include quantitative analysis, or report LCB results alongside the FLORES-based evaluation.

## Score and Decision

This paper presents a clean, well-motivated method with consistent empirical results across diverse models. The core ideas—norm-adjusted self-distillation for language-family prediction and lightweight decoding-time masking—are sound and practically valuable. The primary weaknesses (FLORES train/eval overlap, no variance reporting, thin LCB justification) are meaningful but addressable and do not invalidate the paper's central contribution.

I recommend acceptance.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>