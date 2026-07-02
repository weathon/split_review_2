Here is the final consolidated review:

---

## Summary

This paper investigates whether translating LLM evaluation benchmarks (MMLU, XQuAD, MLQA) into Arabic masks contamination signals. The authors fine-tune four open-weight models on varying proportions of Arabic-translated test data (p=0, 10%, 50%, 100%) alongside the original English test data, then evaluate on the English benchmarks. They extend the TS-Guessing memorization probe with a choice-reordering strategy for MCQs and propose a Translation-Aware Contamination Detection (TACD) framework as a blueprint for future work.

## Strengths

1. **Novel and well-motivated research question.** Contamination research is overwhelmingly English-centric. The question of whether translation into a lower-resource language acts as a natural barrier—or merely conceals contamination—is genuinely important and timely. The literature review (Section 2) competently identifies the gap in multilingual contamination research.

2. **Core empirical finding is real and worth communicating.** Table 2 shows that MMLU accuracy increases monotonically with Arabic-translated contamination across all four models (e.g., Mistral: 0.577→0.690, Gemma: 0.220→0.284, LLaMA: 0.332→0.431, Qwen: 0.553→0.581). This demonstrates that even when evaluation involves a language shift, exposure to translated benchmark content still inflates English scores—a concrete result with implications for multilingual evaluation practice.

3. **The TS-Guessing + choice-reordering extension (Section 3.3) is a reasonable adaptation.** Shuffling choices and masking one option to probe whether the model recalls the pre-shuffle index is a clean way to separate surface-form memorization from reasoning in MCQs. The idea is clearly described and represents a sound incremental extension of Deng et al. (2024).

## Weaknesses

### Fatal

None.

### Major

1. **The "stronger Arabic capabilities" claim in the abstract and introduction is entirely unsupported.** The abstract (line 9) states that models "benefit from exposure to contaminated data, particularly those with stronger Arabic capabilities." The introduction (line 17) repeats this. However, the paper **never evaluates the models' Arabic capabilities**—no Arabic benchmark, no Arabic proficiency metric, no cited Arabic performance scores. This claim appears in both the abstract and introduction as a key finding but has zero evidence in the paper. It should be removed or substantiated by evaluating the models on Arabic tasks (e.g., Arabic MMLU or QA benchmarks).

2. **Section 4.2 contains a factual inconsistency with Table 2.** The contamination analysis section (lines 201, 216–218) claims that "Across contamination levels p ∈ {10, 50, 100}%, the models exhibit approximately equal performance on all evaluated benchmarks" and that "The consolidated results in Tables 2 and 3a show that scores remain broadly stable as p increases." This is factually incorrect for Table 2: MMLU scores increase monotonically for every model (e.g., Mistral 0.577→0.690, LLaMA 0.332→0.431). The paper is internally inconsistent—it simultaneously reports that MMLU rises with contamination (Section 4.1, line 189) and claims the results are "broadly stable" (Section 4.2, line 216). This contradiction undermines the central narrative about translation "masking" contamination.

3. **The TS-Guessing probe results are over-interpreted as evidence of "masking."** Table 3 shows TS-Guessing scores are near-floor across all contamination levels (MMLU IDR mostly below 0.4, XQuAD EM below 0.02 for most models). The paper interprets flatness as evidence that "translation conceals traditional contamination signals." But the more parsimonious interpretation is that the probe, as adapted here, may simply be insensitive to Arabic-translated data. The paper never validates TS-Guessing on English-only contamination to confirm that the probe can detect known contamination in this setup. Without this control, the flat results are uninterpretable as evidence of masking.

4. **The translation methodology is completely undescribed.** The paper's central variable is translation, yet it never describes how the Arabic translations of MMLU, XQuAD, and MLQA were obtained. Were they human-translated? Machine-translated? Which system was used? What quality checks were applied? How might translation artifacts (fluency, register, dialect choice) affect results? This is a critical methodological gap for a paper whose entire argument depends on translation.

### Minor

1. **No clean (no fine-tuning) baseline.** The p=0 condition trains on the English test data only, which is itself a contaminated model. The paper never reports what the base models score without any fine-tuning, making it impossible to decompose inherent capability from English-contamination gain from Arabic-contamination gain. This would be straightforward to add.

2. **No confidence intervals or significance tests.** Results in Tables 2 and 3 are reported as point estimates. Given the small number of models (4), the noisy XQuAD/MLQA patterns, and the central claim about monotonic MMLU trends, some indication of variance or significance (e.g., bootstrapping across MMLU subjects) would substantially strengthen the claims.

3. **The experimental design does not control for the amount of training data.** The p=0 condition trains on less data (EN only) than p=100 (EN+AR). Performance gains could partly reflect having more training examples rather than contamination per se. A control condition training on an equal amount of non-benchmark Arabic text would disentangle these effects.

4. **Non-monotonic XQuAD/MLQA results are over-interpreted with post-hoc explanations.** Section 4.1 offers individual narratives for each model's pattern (Mistral collapses, Gemma/LLaMA rise, Qwen dips then recovers) without any systematic analysis or statistical testing. The claimed "peak-at-10%" pattern is not actually consistent across model/dataset combinations. This analysis should be shortened and clearly caveated as speculative.

5. **The TACD framework (Section 5) is an unimplemented blueprint.** The paper honestly states this (line 252: "a forward-looking blueprint rather than a complete implementation"), but presenting it as a named framework in the abstract inflates the contribution beyond what is delivered. It would be more appropriately framed as future work or a discussion paragraph rather than a separate contribution.

### Trivial

None beyond the issues listed above.

## Nice-to-Haves

- Validating the TS-Guessing probe on English-only contamination to establish a sensitivity baseline.
- Adding an Arabic-only contamination condition (training on D_AR^d only, no D_EN^d) to isolate whether translation alone provides a contamination benefit.
- Reporting per-subject MMLU breakdowns to examine which knowledge domains are most affected.

## Removed Points

These points were flagged by the harsh critic but are removed for the following reasons:
- *"The model set is too heterogeneous and too small (4 models, largest 7B)"* — Generic criticism that could apply to many empirical studies; the paper does not claim exhaustiveness and 4 models across 1B–7B is a reasonable coverage for a controlled experiment.
- *"Limitation about generalizability—models 1B-7B"* — The paper already cites Li (2023) showing larger models exploit contamination more, which indirectly acknowledges this.
- *Critic's Issue 1 (fine-tuning vs. pre-training conflated)* — The paper explicitly states it fine-tunes models (abstract line 9, introduction line 17), and the methodology is transparent about this. The conclusion (line 258) says "when fine-tuned on translated benchmark data," which correctly scopes the claim. While the literature review discusses pre-training contamination, the experimental framing is clear enough. This is a scope-caveat issue at most.

## Novel Insights

The harsh critic's review surfaces a useful meta-point: there is a tension between the paper's stated narrative ("translation masks contamination") and the evidence it presents. The MMLU scores *rise transparently* with contamination—they are the opposite of masked. What is "masked" is only the TS-Guessing probe signal, which may be an artifact of probe insensitivity rather than a property of contamination. This discrepancy between the evaluation results (clear signal) and the probe results (flat noise) is itself an interesting observation that the paper could reframe around. The paper would be stronger if it honestly centered its contribution on the finding that "translation ≠ decontamination" (MMLU scores still rise) and simply noted that standard probes fail under translation as a secondary limitation, rather than trying to spin this as evidence that contamination is "concealed."

## Suggestions

1. **Remove or substantiate the "stronger Arabic capabilities" claim.** This is the most urgent fix—either add Arabic benchmark evaluations for the four models, or remove the claim from the abstract and introduction entirely.
2. **Fix the internal inconsistency in Section 4.2.** Acknowledge that MMLU scores increase with contamination (Table 2) while the TS-Guessing probe scores are flat (Table 3). Do not claim that "all" results are stable.
3. **Describe the translation methodology.** State how translations were obtained (human vs. machine, which system), any quality assurance, and how translation artifacts are accounted for.
4. **Add a clean (no fine-tuning) baseline** for all models and benchmarks.
5. **Validate the TS-Guessing probe** on English-only contamination as a positive control, or explicitly caveat that the probe's flat results may reflect insensitivity rather than masking.
6. **Condense TACD into a future-work paragraph** rather than presenting it as a separate contribution.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>