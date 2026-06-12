## Summary

This paper investigates whether translating benchmark data into Arabic can mask data contamination signals in LLM evaluation. The authors fine-tune four small open-weight models on varying proportions (0%–100%) of Arabic-translated test data, evaluate on the original English benchmarks, and apply a TS-Guessing memorization probe with a choice-reordering extension. They find that MMLU accuracy shows monotonic increases with contamination, while TS-Guessing results are mostly flat or near floor. The paper interprets this as evidence that translation "conceals" contamination signals and proposes a Translation-Aware Contamination Detection (TACD) framework as a conceptual blueprint.

## Strengths

- **Sensible methodological extension of TS-Guessing (Section 3.3).** The choice-reordering strategy, where answer positions are shuffled before masking, targets a more specific memorization signal (index recall) than the original TS-Guessing method. This is a clean adaptation for the multiple-choice setting.

- **The TACD framework identifies a genuine gap (Section 5).** The idea that contamination checks should operate across multiple translated variants rather than English alone is well-motivated by the paper's framing. Even as a conceptual blueprint, this highlights an underexplored vulnerability in current evaluation practice.

## Weaknesses

### Fatal

None.

### Major

1. **Central claim contradicted by the paper's own MMLU evidence.** The paper asserts that Arabic translation "conceals traditional contamination signals" (abstract) and that "scores remain broadly stable" with "near-flat trend" across contamination levels (Section 4.2). However, **Table 2 shows clear, monotonic increases in MMLU accuracy for all four models** as contamination rises (e.g., Mistral: 0.577→0.690, a ~20% relative increase; LLaMA: 0.332→0.431, a ~30% relative increase; Gemma: 0.220→0.284; Qwen: 0.553→0.581). Section 4.1 itself states that "MMLU exhibits a generally monotonic increase as contamination rises from 0%→100%." The paper never reconciles these contradictory statements. If the primary evaluation metric (MMLU accuracy) rises detectably and monotonically with Arabic-translated contamination, then translation does **not** conceal contamination signals on the metric that matters most (benchmark accuracy). The claim of masking is only salvageable if restricted to the TS-Guessing probe — but the paper invokes "Tables 2 and 3a jointly" to support it, which is not justified by the data.

2. **TS-Guessing results are near floor and do not independently support the masking interpretation.** Table 3 shows that for MMLU (IDR), Mistral is 0.000 at every contamination level; Gemma drops from 0.350 (10%) to 0.005 (100%); Qwen hovers at 0.21–0.26 with no clear trend; only LLaMA shows notable signal at 50% (0.643), dropping to 0.410 at 100%. For XQuAD (Table 3b), EM and ROUGE-L F1 are essentially zero for all models except Mistral (0.07–0.11), and even those slightly *decrease* with contamination. The paper interprets this flatness as evidence that translation "masks" contamination. A more straightforward interpretation is that the TS-Guessing probe simply does not work well for these models/tasks — the metrics are at or near floor, providing no signal to interpret. Without a same-language control demonstrating that the probe detects contamination in non-translated settings (i.e., that the probe works), the masking claim is unsupported speculation.

3. **Missing critical baseline: same-language contamination.** The paper repeatedly invokes an implicit comparison: "In typical same-language settings, increasing p would be expected to induce noticeable shifts" (Section 4.2). But **no same-language experiment is ever run**. Without fine-tuning models on English-paraphrased versions of the same test data at the same contamination levels and measuring the same probes, there is no empirical basis for claiming that Arabic translation *specifically* alters contamination dynamics relative to same-language exposure. The observed patterns could equally be due to probe insensitivity, small-sample noise, or the inherent noisiness of extractive QA metrics. This baseline is essential to the paper's narrative and its absence is a major gap.

### Minor

4. **Framing gap: pre-training contamination vs. deliberate fine-tuning on test sets.** The introduction and literature review (Sections 1–2) discuss contamination in the context of incidental pre-training exposure (Common Crawl, The Pile, etc.). But the experiments fine-tune models on benchmark test-set translations — deliberate, multi-epoch, high-concentration exposure. The paper does not discuss whether contamination dynamics in these two settings are comparable, nor does it acknowledge this gap in the generalizability of its findings. This weakens the link from the experimental results to the sweeping claims about "contamination detection practices" in the abstract and conclusion.

5. **Ambiguity in the baseline condition (D_EN^d).** The paper describes D_EN^d as "the English split (MMLU: English test items formatted as MCQ; XQuAD/MLQA: English QA)" (Section 3.1). If D_EN^d includes MMLU *test* items (as the parenthetical suggests), then even the p=0 baseline involves fine-tuning on test data, making every condition "contaminated" and fundamentally changing the experimental setup from "clean vs. contaminated" to "English-contaminated vs. English+Arabic-contaminated." This requires clarification.

6. **No variance or significance estimates.** All results (Tables 2 and 3) are single point estimates with no confidence intervals, error bars, or significance tests. This is especially problematic for the small differences (e.g., Qwen MMLU: 0.553→0.560→0.562→0.581) and near-floor TS-Guessing values, where noise could dominate the observed patterns.

7. **IDR metric captures only position-based memorization, not content-based memorization.** The Index-Dependent Recall rate measures whether the model recalls the pre-shuffle answer letter. But if a model memorizes the answer text (e.g., "Paris"), shuffling choices should not affect its output — it would output "Paris" regardless of position. This narrow scope may explain why IDR is near zero for models that clearly benefit from contamination (as shown by their rising MMLU scores), and is a limitation the paper does not discuss.

8. **Translation provenance and quality are not reported.** The paper does not specify whether the Arabic translations are human-generated or machine-generated, or what quality metrics they satisfy. This matters because low-quality or unnatural translations might make contamination *more* detectable (via translation artifacts) or *less* detectable (via garbled semantics), confounding interpretation.

### Trivial

9. **Limited experimental scope.** The study uses 4 small models (only one above 1.7B parameters), 3 datasets, and 1 language. The conclusions are framed broadly but the evidence base is narrow.

## Nice-to-Haves

- The paper does not evaluate on the Arabic benchmarks themselves. If the claim is that models benefit from Arabic-translated contamination, showing Arabic benchmark performance would provide a useful comparison point.
- A same-language paraphrasing control (as described in Major Weakness 3) would directly test whether translation specifically alters contamination dynamics vs. any surface-form perturbation.

## Removed Points

- **Strength: "A genuinely important and understudied question"** — Removed as generic; the statement lacks concrete content specific to this paper.
- **Weakness about conflating pre-training and fine-tuning (originally "Critical Issue #4" by the harsh critic)** — Downgraded to Minor and retained as Weakness #4. The paper is transparent about its experimental design; the gap is in the framing and literature review, not a flaw in the experiments themselves.
- Various formatting/style nitpicks, speculation about missing appendix content, and criticisms about "not yet released" artifacts were removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's key observation — that the paper's MMLU results directly contradict its central masking claim while the paper never reconciles this — is an accurate diagnosis of the paper's structural flaw, not a novel research insight.

## Suggestions

1. **Address the internal contradiction head-on.** The MMLU trends (Section 4.1) and the "near-flat" claim (Section 4.2) are irreconcilable as written. The paper needs to explain why MMLU accuracy detects contamination while TS-Guessing does not, and what this divergence actually means for the paper's thesis.
2. **Run a same-language paraphrasing control.** Fine-tune models on English-paraphrased versions of test data at the same contamination levels. If the Arabic condition shows *flatter* performance curves than English paraphrasing, the claim that translation specifically masks contamination would be supported.
3. **Report variance estimates.** Provide multiple seeds, confidence intervals, or significance tests for all results, especially the small-magnitude differences in Table 2 and near-floor values in Table 3.
4. **Clarify D_EN^d.** Explicitly state whether the English baseline includes test-set items and, if it does, discuss how this affects interpretation.
5. **Specify translation provenance.** Report whether the Arabic translations are human or machine-generated and provide quality metrics.

---

### Calibration Report

Anchor papers retrieved across calibration rounds:

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| *Evading Data Contamination Detection is (too) Easy* | 4.25 | Bracket | Topically similar. That paper had clearer experimental evidence for its claim (evasion works) despite structural issues. The current paper's central claim is contradicted by its own data, making it weaker. |
| *Benchmark Inflation: Retro-Holdouts* | 4.25 | Bracket | Better executed with a clear methodology and validated holdout set. Current paper is weaker in experimental support. |
| *To the Cutoff... and Beyond?* | 6.75 | Bracket | Much stronger: longitudinal design, statistical rigor, clear evidence for contamination. Current paper is far below this quality. |
| *How much can we Forget about Data Contamination?* | 6.75 | Bracket | Strong empirical work with scaling laws. Current paper lacks comparable rigor. |
| *Language Models for Textual Data Valuation* | 2.00 | Narrow | Very different topic; not comparable. |
| *All Languages Matter: Multilingual Safety* | 3.50 | Narrow | Different topic but similar scale/scope. The current paper is roughly comparable in quality. |

**Bracket:** Round 1 placed the paper plausibly between 3.0 and 5.0. Round 2 narrowed this using topically similar anchors. The paper is clearly below the 4.25-level papers (Evading, Benchmark Inflation) because its central empirical claim is internally inconsistent — a more fundamental flaw than their structural or methodological weaknesses. It is above the 1–2 range because it has a coherent experimental design and addresses an important question.

**Final score:** 3.5 — The paper identifies an important question and makes a sensible methodological extension, but its central claim is contradicted by the paper's own best evidence (MMLU monotonic trends vs. the "masking" narrative), the probe results do not independently support the interpretation, and a critical control experiment is absent. The paper would require major revisions, new experiments, and a reframing of its claims before the evidence would be credible.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>