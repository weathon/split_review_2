Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper investigates whether translating benchmarks into Arabic can mask data contamination signals in LLM evaluation. It fine-tunes four open-weight models on varying proportions of Arabic-translated test data from MMLU, XQuAD, and MLQA, then evaluates on the original English benchmarks. The authors extend TS-Guessing with a choice-reordering strategy to probe memorization and propose a Translation-Aware Contamination Detection (TACD) framework. The paper identifies a genuinely important and underexplored problem — whether multilingual evaluation creates a blind spot for contamination detection.

## Strengths

- **Addresses a genuinely underexplored problem.** The gap between English-centric contamination detection and multilingual evaluation is real and practically important. The question of whether translation into lower-resource languages can mask contamination signals is timely as multilingual evaluation grows. *(weight: +2.30)*

- **The TS-Guessing extension with choice reordering (Section 3.3) is a concrete, non-trivial methodological adaptation.** Shuffling answer choices and checking whether the model recovers pre-shuffle index patterns is a clever way to probe memorization of answer-position mappings rather than content reasoning. This is a reusable technique. *(weight: +2.89)*

- **Honest limitations discussion.** Section 5.3 transparently acknowledges that TACD is a "forward-looking blueprint rather than a complete implementation" and candidly discusses the resource, quality, and noise challenges of cross-translation evaluation. The paper does not oversell this component. *(weight: +3.54)*

## Weaknesses

### Major

1. **Internal contradiction between Sections 4.1 and 4.2 undermines the core empirical claim.** Section 4.1 (lines 187-197) carefully documents substantial, often non-monotonic performance changes across contamination levels: Mistral XQuAD collapses from 0.455→0.272→0.114 (a 75% drop from peak); LLaMA XQuAD rises 0.459→0.558→0.569; Gemma XQuAD rises 0.481→0.577→0.606. Yet Section 4.2 (line 201) asserts that "the models exhibit approximately equal performance on all evaluated benchmarks" and describes a "near-flat trend." This directly contradicts Table 2's data for most model-dataset combinations. The paper's central argument — that translation creates a flat performance surface that hides contamination — is undermined by its own reported results. *(weight: -2.17)*

2. **The central claim that Arabic translations "evade standard detection tools" is asserted but never tested.** The abstract states translations "conceal traditional contamination signals" and the conclusion (line 258) claims translations "obscure exact string matches and evade standard detection tools." However, the paper never applies any standard contamination detection method (e.g., n-gram search, Min-K% Prob, guided prompting) to the Arabic-translated data to demonstrate that these methods fail to flag contamination. The empirical study evaluates models on English benchmarks and uses TS-Guessing, but neither of these constitutes applying a standard detection tool to the translated data. This claim is the paper's most concrete practical message but has no supporting evidence. *(weight: -3.72)*

3. **Missing English-only contamination baseline.** The experiment fine-tunes models on Arabic-translated test data at proportions p ∈ {10, 50, 100}% but has no condition where the same proportion of English test data is added to the training set. Without this control, it is impossible to attribute the observed effects to translation specifically. If English-only contamination produces similar or larger performance gains, then translation is not "masking" anything — it is simply a weaker form of the same effect. This control is essential to distinguish between "translation specifically conceals contamination" and "any form of test-set overlap helps performance." *(weight: -3.68)*

### Minor

4. **TS-Guessing results lack a positive control.** Most TS-Guessing scores are very low (EM near 0, RL-F1 below 0.1 for XQuAD). The paper interprets this as evidence that translation masks contamination signals. However, without demonstrating that TS-Guessing clearly fires on a known-contaminated English-only condition, the near-zero scores could simply mean the probe does not work well for these models/tasks, rather than that contamination is present but hidden. The negative results are uninterpretable without a positive control. *(weight: -3.36)*

5. **Translation methodology is underspecified.** The paper does not clarify how Arabic translations of MMLU (which has no standard Arabic split) were obtained. Were they machine-translated? By whom? What quality assurance was performed? For XQuAD/MLQA, are these the official Arabic splits or newly produced translations? The paper simply states "MMLU: Arabic translations of the test items" (line 142) with no details on the translation process, quality, or potential artifacts. This matters because translation quality directly affects whether observed effects are due to "masking" or simply poor translations. *(weight: -0.69)*

6. **No statistical testing.** Results are reported as point estimates without confidence intervals, standard deviations, or significance tests. Given that the paper makes comparative claims (e.g., "MLQA spikes at 10% then collapses," "Qwen XQuAD dips at 10% then recovers"), the absence of error bars makes it impossible to assess whether observed differences are meaningful or noise. *(weight: -3.57)*

7. **Pre-existing contamination of base models is not assessed.** The four open-weight models (LLaMA-3.2, Mistral, Gemma, Qwen) may already be contaminated with the original English benchmarks from pre-training. The paper does not check this baseline, making it difficult to attribute observed behaviors specifically to the Arabic fine-tuning rather than pre-existing contamination. *(weight: -1.91)*

### Trivial

None.

## Nice-to-Haves

- The TACD framework (Section 5) is acknowledged as a forward-looking blueprint, which is honest. Even a small-scale validation — e.g., showing that on one translated benchmark, the proposed cross-translation check flags contamination that English-only checks miss — would significantly strengthen the paper's practical contribution.
- The embedding similarity analysis mentioned in Section 4.3 would benefit from reporting actual cosine similarity values rather than the qualitative "high" characterization.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Critique that the experimental design does not model "real contamination":** Removed. The paper is transparent about its setup (deliberate fine-tuning on translated test data). Many contamination studies use controlled injection of benchmark data; this is a standard experimental paradigm. The more serious issue (missing English-only baseline, kept above) captures the empirical concern.
- **TACD is a blueprint, not a contribution:** Removed as a formal weakness. The paper explicitly acknowledges this limitation (Section 5.3). Criticizing it for being unimplemented is fair as a nice-to-have but not as a core weakness.
- **Claim that the literature review is disproportionately long:** Removed. This is a subjective judgment about presentation balance, not a substantive flaw.
- **Claim that the paper uses "contamination" in two different senses:** Removed. The paper consistently uses "contamination" to refer to training on evaluation data, whether incidental or deliberate. The distinction the critic draws is orthogonal.
- **Section-by-section notes about missing figures from appendix stripped by parser:** Removed. Parser artifacts are not author errors.
- **Formatting, style, and grammar nitpicks:** Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The review's primary contribution is identifying the concrete internal contradiction between Sections 4.1 and 4.2 — the paper's own data shows substantial performance variation across contamination levels while the text claims "approximately equal" and "near-flat" behavior. This is not a standard missing-experiment critique but a logical inconsistency in how the paper interprets its reported results. The second key insight is the gap between the practical claim about detection methods failing and the complete absence of any test of those methods.

## Suggestions

1. **Resolve the 4.1/4.2 contradiction.** Either acknowledge the clear performance changes in Table 2 as evidence that translation does not fully mask contamination (the monotonic MMLU increases and substantial XQuAD changes contradict "near-flat"), or redefine what "masking" means in a way that is consistent with the data (e.g., "changes are compressed relative to same-language contamination controls").
2. **Add an English-only contamination baseline** at the same p levels. This is the single most important missing experiment — it is necessary to attribute effects to translation specifically.
3. **Apply at least one standard detection method** (Min-K% Prob, n-gram search, guided prompting) to the Arabic-translated data to test whether it would flag contamination. This is currently asserted but not demonstrated.
4. **Add a positive control for TS-Guessing** by testing it on a model known to be contaminated with English benchmark data, so that the near-zero TS-Guessing scores can be interpreted as "masking" rather than "probe doesn't work."
5. **Specify the translation methodology** (source, quality, procedure) for each benchmark, particularly MMLU which has no standard Arabic split.

## Score and Decision

The calibration search identified several relevant anchors for comparison. The most topically similar is "Evading Data Contamination Detection for Language Models is (too) Easy" (avg 4.25, Reject), which shares the theme of claiming evasion without adequate experimental support, but with more severe execution flaws. "Elephants Never Forget: Testing Language Models for Memorization of Tabular Data" (avg 4.75, Reject) and "Benchmark Inflation: Revealing LLM Performance Gaps Using Retro-Holdouts" (avg 4.25, Reject) are also relevant contamination/memorization studies that were judged to have genuine contributions but significant limitations. "To the Cutoff... and Beyond?" (avg 6.75, Accept) represents the stronger end of contamination papers — well-executed longitudinal analysis with rigorous methodology.

This paper's draft receives moderate positive weights (+2.30 to +3.54) for its problem framing and TS-Guessing adaptation, but substantial negative weights (-2.17 to -3.72) for the internal contradiction, untested central claim, missing baseline, and lack of positive controls. Compared to the Evading paper (4.25) which had more extreme negative weights (-8+) for its experimental failures, this paper's weaknesses are moderately severe but multiple. Compared to "Benchmark Inflation" (4.25), this paper's empirical gaps are larger. The paper does not reach the methodological rigor of accept-level contamination papers (6.75+).

Round-1 bracket: 3.0–5.0. Within this range, the weighted-item comparison places this paper below the "Elephants Never Forget" anchor (4.75) which, despite critiques about novelty, had more comprehensive and validated methodology. The contradiction between the paper's own data and its claims, combined with the untested central claim, pushes the score toward the lower end of the bracket.

**Score: 4.0** (Borderline Reject) — The paper identifies a genuinely important problem and contributes a useful methodological adaptation (choice-reordered TS-Guessing). However, it contains a verifiable internal contradiction in how it interprets its own results, makes a central practical claim (that standard detection methods fail on translated data) without testing it, and lacks essential experimental controls. The gap between what is claimed and what is demonstrated is too wide for acceptance in current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>