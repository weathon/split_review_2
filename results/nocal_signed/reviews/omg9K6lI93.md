Now let me write the final consolidated review.

## Summary

This paper investigates whether translating benchmark data into Arabic can obscure data contamination in LLM evaluation. The authors fine-tune four open-weight LLMs on varying proportions of Arabic-translated test data (alongside English data) and evaluate on the original English benchmarks. They extend the TS-Guessing method with a choice-reordering strategy to probe for index-level memorization in MCQs, and propose a Translation-Aware Contamination Detection (TACD) framework. The core finding is that models still show performance gains from exposure to translated contaminated data, even when surface-form contamination signals are weak.

## Strengths

1. **The research question is genuinely important and underexplored.** The contamination literature is overwhelmingly English-centric, and the question of whether multilingual translation alters contamination detectability addresses a real blind spot in current evaluation practice. The paper is grounded in a thorough literature review (Section 2) that documents the fragmentation and English-centricity of existing detection methods.

2. **The TS-Guessing extension with choice reordering for MCQs (Section 3.3, Figure 1) is a sensible and well-motivated methodological adaptation.** Masking one choice and checking whether the model recovers the pre-shuffle letter index provides a cleaner probe of index-level memorization than standard n-gram overlap checks, which is particularly relevant for studying MCQs.

3. **The paper is clearly structured** and the limitations of the TACD proposal are honestly acknowledged (Section 5.3: "forward-looking blueprint rather than a complete implementation").

## Weaknesses

### Fatal
None.

### Major

1. **Unsupported claim about Arabic capabilities.** The abstract and introduction state that contamination benefits are "particularly [for] those with stronger Arabic capabilities" (lines 9, 17), but the paper provides no evaluation, measurement, or ranking of any model's Arabic proficiency. No Arabic benchmark scores or multilingual capability metrics are presented anywhere in the manuscript. This claim should either be removed or empirically supported.

2. **The TS-Guessing probe results are weakly supportive and the discrepancy is unaddressed.** Table 3 shows MMLU IDR values mostly below 0.4 and XQuAD EM values mostly below 0.02, yet Table 2 shows accuracy improvements with increasing contamination (e.g., Mistral MMLU: 0.577→0.690, LLaMA MMLU: 0.332→0.431). If models were strongly benefiting from memorization, one would expect the probes to detect it at higher rates. The paper does not discuss this discrepancy or explain why the probes show such limited sensitivity relative to the claimed contamination effects.

3. **The claim that translation "evades standard detection tools" (conclusion, line 258) is untested.** The paper never applies any standard detection method (n-gram search, Min-K% Prob, guided prompting) to the Arabic-trained models. Only the paper's own TS-Guessing probe is used. Asserting that existing tools are evaded without running them is an overclaim unsupported by experimental evidence.

4. **Scope mismatch between the framing and the experiments.** The paper motivates its work through the broader problem of pre-training contamination (Section 2) but conducts experiments involving deliberate fine-tuning on test data. These are qualitatively different phenomena (direct gradient supervision on the test set vs. passive exposure at massive scale during pre-training). The paper does not discuss how its findings might or might not generalize to pre-training contamination, which limits the applicability of its conclusions.

### Minor

1. **No statistical rigor.** Table 2 reports single-point estimates without variance, confidence intervals, or multiple seeds. Given model- and dataset-specific fluctuations (e.g., Mistral XQuAD: 0.455→0.114; Qwen MLQA: 0.162→0.409→0.153), it is unclear which trends are reliable and which are single-run artifacts.

2. **Missing embedding analysis.** Section 4.3 (line 224) references "the embedding figure" showing that Arabic→English translations remain close to their English originals with high cosine similarity, but this figure is not presented in the paper, making the supporting analysis inaccessible to readers.

3. **MMLU training data provenance is ambiguous.** The paper states D_EN^d for MMLU is "English test items" (line 132). Since MMLU has no standard training split, the source and size of this English data should be explicitly stated and its implications for the experimental design discussed. The paper does clarify that all conditions intentionally use test data (the experiment is about contamination by design), but the provenance should be transparent.

4. **TACD is presented as a contribution but is entirely conceptual.** The paper acknowledges this (line 252) but still lists it as part of the contribution. It has no implementation or validation.

### Trivial

1. XQuAD/MLQA are evaluated with ROUGE-L F1 (line 153), which is less common for span-extraction QA than token-overlap F1. The choice is not justified, and it creates an unaddressed asymmetry with the TS-Guessing probe for XQuAD, which uses Exact Match.

## Nice-to-Haves
- An Arabic-only training condition (without English data) would strengthen the "masking" comparison by directly isolating the effect of translation on contamination signals.
- Applying standard contamination detectors (Min-K% Prob, guided prompting) to the Arabic condition would directly test whether they are evaded.
- Evaluating each model's Arabic proficiency (e.g., on Arabic NLP benchmarks) would substantiate the claim about "stronger Arabic capabilities."

## Removed Points

1. **"The experimental design does not support the paper's central claim (missing Condition A vs. Condition B comparison)"** — Removed. The paper does include an English-only baseline (p=0). The critic's proposed comparison (English-only vs. Arabic-only) is a different design from what the paper runs (English-only vs. English+Arabic). The current design is valid for testing whether adding Arabic-translated data changes contamination patterns relative to English-only contamination. An Arabic-only condition would strengthen the paper but its absence is not a fatal flaw.

2. **"TACD is not a contribution" (framed as fatal)** — Removed as overstatement. The paper acknowledges it as a blueprint. Downgraded to minor.

3. **"Critical ambiguity in training data invalidates the entire experiment"** — Removed as overstatement. The experiment is intentionally about contamination (training on test data is by design). The ambiguity about source specification does not invalidate the core experimental design. Downgraded to minor.

4. **"Section 4.2 is too brief"** and other presentation/style nitpicks — Removed as not substantive.

5. **"No analysis of representation overlap"** (as a separate point) — Merged into Minor weakness #2 (missing embedding figure), which is the concrete manifestation of this concern.

## Novel Insights

None beyond the paper's own contributions. The core finding — that models fine-tuned on Arabic-translated test data show performance gains on English benchmarks even when surface-form probes detect weak memorization signals — is potentially interesting but is weakened by the overclaims and evidentiary gaps identified above.

## Suggestions

1. Remove or substantiate the claim about Arabic capabilities with actual Arabic evaluation data.
2. Apply at least one standard contamination detector (e.g., Min-K% Prob) to the Arabic-trained models to directly test whether existing tools are evaded.
3. Add multiple seeds with variance reporting for the key comparisons (Tables 2 and 3).
4. Clarify the provenance of D_EN^d for MMLU and discuss implications of training on test data.
5. Address the TS-Guessing discrepancy directly: explain why accuracy improves while the memorization probe shows low detection rates.
6. Scope the claims more carefully to the fine-tuning contamination setting studied.

## Score and Decision

The paper tackles a genuinely important and underexplored question, and the TS-Guessing extension is a reasonable methodological contribution. However, the paper makes several unsupported claims (about Arabic capabilities, about evading standard detection tools), fails to address a significant discrepancy between its accuracy results and its probe results, and frames its conclusions in terms broader than its experimental design supports. These issues collectively undermine the confidence that can be placed in the paper's central narrative. With substantial revisions — particularly removing overclaims, adding an Arabic-only control, applying standard detectors, and addressing the probe discrepancy — the work could become a solid contribution.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>