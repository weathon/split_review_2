## Summary

This paper investigates whether translating benchmark data into Arabic masks contamination signals in LLM evaluation. The authors fine-tune four open-weight models on varying proportions of Arabic-translated test data from MMLU, XQuAD, and MLQA, then evaluate on English benchmarks. They extend the TS-Guessing memorization probe with a choice-reordering strategy and propose a Translation-Aware Contamination Detection (TACD) framework as a forward-looking blueprint. The core empirical finding is that English MMLU accuracy rises monotonically with exposure to Arabic-translated test items, while extractive QA shows non-monotonic patterns.

## Strengths

- **The research question is important and understudied.** The concern that translation could create a blind spot for contamination detection in multilingual evaluation is well-motivated, and the paper correctly identifies that existing detection methods are overwhelmingly English-centric (Section 2).

- **The dose-response experimental design is structurally sound.** Varying the proportion of Arabic-translated test data (0%, 10%, 50%, 100%) across four models and three datasets is a reasonable way to look for monotonic relationships between exposure and performance.

- **TS-Guessing with choice reordering (Section 3.3) is a thoughtful methodological addition.** Extending the TS-Guessing probe to handle shuffled multiple-choice options is a sensible adaptation for the MMLU setting.

## Weaknesses

### Major

1. **The central claim that translation "conceals traditional contamination signals" is asserted without testing those methods.** The paper reviews Min-K% Prob (Shi et al., 2023), guided instruction probing (Golchin & Surdeanu, 2023a,b), and corpus-level search tools (Section 2.3–2.4) as existing detection approaches, but **none of them are run on the Arabic-translated data.** The claim that "standard English-only checks fail to capture this" (line 234) and that Arabic translations "evade standard detection tools" (line 258) is an empirical assertion that the paper does not support with evidence. Only the authors' own TS-Guessing extension is used as a probe, making the argument circular: the claim that translation masks detection is supported only by a probe that happens to show no signal.

2. **The TS-Guessing results are uninterpretable without a positive control.** Table 3 reports near-floor detection rates (MMLU IDR mostly 0.000–0.643; XQuAD EM <0.02 for all models except Mistral). The paper interprets this as evidence that "translation masks contamination," but several alternative explanations are equally consistent: (a) TS-Guessing may be insufficiently sensitive even for English-only contamination; (b) fine-tuning on Arabic translations may not produce the verbatim memorization that TS-Guessing targets; (c) probing with Arabic-trained inputs on English prompts may introduce a mismatch. Without a positive control condition (e.g., running TS-Guessing on models fine-tuned on English-paraphrased test items at equivalent exposure levels), the negative result cannot be attributed to translation specifically.

3. **The "stronger Arabic capabilities" claim is entirely unsupported.** The abstract states that models benefit from contamination "particularly those with stronger Arabic capabilities" (line 9). **No Arabic-language evaluation is conducted anywhere in the paper.** There is no Arabic proficiency metric, no cross-model Arabic capability ranking, and no correlation analysis. The reader cannot determine which of the four models (if any) has "stronger Arabic capabilities" or on what basis this claim rests.

4. **The experimental setup differs fundamentally from real-world contamination.** The paper fine-tunes models directly on the Arabic-translated **test set** of each benchmark (lines 130–142), then evaluates on the original English test set. Real contamination occurs when benchmark content appears incidentally in **pre-training corpora** among billions of tokens — the signal-to-noise ratio is vastly different. The paper's setup guarantees concentrated exposure to exact test items (in translated form), which does not model how pre-training contamination would manifest. The paper does not acknowledge or justify this gap between the studied phenomenon and the experimental operationalization.

### Minor

1. **No statistical rigor.** All results (Tables 2, 3) are reported as point estimates with no confidence intervals, standard errors, or information about multiple seeds. Given that differences between contamination levels are sometimes very small (e.g., LLaMA MMLU: 0.332 → 0.381 between 0% and 10%; Qwen MMLU: 0.553 → 0.560), it is impossible to assess whether these are meaningful effects or noise.

2. **Key interpretive evidence is deferred to the stripped appendix.** The paper's interpretation of non-monotonic XQuAD/MLQA results depends on claims about "low context-question lexical overlap" and "short yet non-trivial answer spans" (line 222), with dataset statistics delegated to Appendix B. Readers of the main paper cannot verify these claims.

3. **The choice of Arabic as the target language is not motivated beyond a simplified "low resources" label.** Arabic has substantial NLP resources and is not typically grouped with genuinely low-resource languages. The paper does not discuss whether findings would generalize to other languages with different typological properties or resource levels.

### Trivial

None.

## Nice-to-Haves

- Apply Min-K% Prob and guided instruction probing to the Arabic-translated benchmarks. If these methods return lower detection rates than on English equivalents while models still show performance gains, the core claim would be directly supported.
- Add a positive control: fine-tune on English-paraphrased (same-language, perturbed surface form) test items and run TS-Guessing to establish whether the probe detects contamination at all before claiming translation specifically masks it.
- Actually measure Arabic capability using Arabic-language benchmarks to support the "stronger Arabic capabilities" claim.
- Run multiple seeds and report confidence intervals or effect-size measures.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Reviewer claim that hyperparameters are under-specified (missing optimizer, LR, batch size, etc.):** Removed because the paper states that "All hyperparameters and training/evaluation settings required to reproduce our results are enumerated in Appendix A" (line 264), which the parser strips from all submissions.
- **Criticism that the paper does not engage with prior work on multilingual contamination:** Removed per the rule that missing related works cannot be confirmed as existing without external sources.
- **Reviewer's "Section-by-Section Notes" on presentation and framing:** These are restatements of the major weaknesses already addressed above.
- **Criticism about the paper not addressing generalizability to other languages:** This is outside the paper's stated scope (Arabic as a case study) and fits better as a nice-to-have.
- **Formatting nitpicks and speculation about the appendix:** Removed per parser/stripping rules.

## Novel Insights

None beyond the paper's own contributions. The reviewer provides a clear diagnosis of claim-evidence gaps but does not surface a novel scientific insight about the paper's findings or methodology that the authors themselves missed.

## Suggestions

1. **Test existing detection methods on the Arabic data.** This is the single most important missing piece. Without it, the paper's headline claim about translation "concealing traditional contamination signals" remains an assertion, not a finding.
2. **Add a positive control for TS-Guessing** (English-paraphrased data at the same exposure levels) to establish that the probe can detect contamination when it exists, before attributing negative results to translation.
3. **Either remove the "stronger Arabic capabilities" claim or support it** with actual Arabic-language evaluation data.
4. **Acknowledge the gap** between fine-tuning on test-set translations and real-world pre-training contamination, and discuss what the current setup can and cannot tell us.
5. **Add statistical measures** (multiple seeds, variance estimates) to at least a subset of conditions to establish the reliability of the reported trends.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>