Now let me write the final authoritative review.

## Summary

This paper investigates a timely and important question: whether translating benchmarks into Arabic can mask data contamination signals while still allowing models to benefit from contaminated data. The authors fine-tune four open-weight LLMs on varying proportions of Arabic-translated test data from MMLU, XQuAD, and MLQA (always alongside the full English test set), evaluate on the original English benchmarks, and probe memorization via a choice-reordering extension of TS-Guessing. They also propose a Translation-Aware Contamination Detection (TACD) framework. The paper is clearly written and addresses a genuine blind spot in current evaluation practices.

## Strengths

- **The research question is timely and well-motivated.** The paper correctly identifies that current contamination detection methods are overwhelmingly English-centric (Section 2). Whether translation into a lower-resource language can function as a contamination blind spot is a genuine concern for multilingual evaluation pipelines.

- **Multiple datasets and model families are used.** The experimental design covers both MCQ (MMLU) and extractive QA (XQuAD, MLQA) task types, and includes four model families (Llama, Mistral, Gemma, Qwen) of varying scales. This provides reasonable coverage beyond a single model or task.

- **The paper is transparent about TACD's scope.** Section 5.3 explicitly states that TACD is "a forward-looking blueprint rather than a complete implementation" and discusses limitations including multilingual resource requirements, translation noise, and compute demands.

## Weaknesses

### Major

1. **The experimental design cannot isolate the effect of translation on contamination dynamics.** The training set for every condition (including p=0) includes the full English test set (D_EN^d — see Section 3.1, lines 130–142: "where D_EN^d is the English split (MMLU: English test items formatted as MCQ; XQuAD/MLQA: English QA)"). At p=0, models are already trained on 100% of the English evaluation items they are later tested on. Adding Arabic translations on top of already-memorized English data does not test whether translation itself masks contamination — it tests whether additional Arabic data provides marginal gains beyond deliberate overfitting to the test set. Without a condition where the English test data is *not* seen during training (i.e., Arabic-only contamination vs. a clean baseline with no test-set exposure), the paper's central claim that translation "conceals" contamination cannot be supported.

2. **The TS-Guessing probe results (Table 3) are uniformly low but uncalibrated.** For MMLU, IDR values are mostly below 0.3 (with one outlier at 0.643 for LLaMA at 50%). For XQuAD, EM and RL-F1 are below 0.02 for most models. The paper attributes these low scores to translation "concealing contamination," but provides no calibration experiment showing the probe produces detectable signals on non-translated (English-only) contaminated data. Without this control, the low TS-Guessing scores could equally indicate that (a) the probe itself is ineffective on this setup, or (b) the models simply did not memorize the translated data in detectable ways. The paper assumes interpretation (a) without ruling out these alternatives.

### Minor

3. **The claim that performance is "approximately equal" across contamination levels is overstated.** Section 4.2 states that "across contamination levels p ∈ {10, 50, 100}%, the models exhibit approximately equal performance on all evaluated benchmarks." This is contradicted by the paper's own Table 2. Several model-dataset combinations show notable changes: Mistral MMLU jumps from 0.580 (10%) to 0.690 (50%) — a 19% relative increase; Gemma XQuAD rises from 0.481 (10%) to 0.606 (100%) — a 26% increase; LLaMA XQuAD rises from 0.459 (10%) to 0.569 (100%) — a 24% increase; Qwen MLQA collapses from 0.409 (10%) to ~0.155 (50–100%). These changes undermine the blanket "approximately equal" claim, though the paper's detailed discussion in Section 4.1 does acknowledge some of these trends.

4. **The claim about "stronger Arabic capabilities" is asserted without evidence.** The abstract and introduction state that models benefit from contaminated data "particularly those with stronger Arabic capabilities" (lines 9, 17). The paper provides zero evaluation of Arabic proficiency for any of the four models — no Arabic benchmark scores, language understanding evaluation, or tokenization analysis. This claim appears without any supporting measurement.

5. **No statistical analysis is reported.** All results appear to come from single fine-tuning runs without confidence intervals, standard deviations, or significance tests. Given that some reported differences are small (e.g., Qwen MMLU: 0.560 → 0.581 across the entire p range), the reader cannot distinguish genuine effects from noise.

6. **TACD is presented as a contribution but is not evaluated.** Section 5 describes a framework at a conceptual level with no experiments, implementation, or evaluation. While the paper is transparent about this being a blueprint (Section 5.3), the abstract nonetheless frames TACD as a contribution ("To address this, we propose a Translation-Aware Contamination Detection framework"). This creates a mismatch between framing and evidence.

### Trivial

None.

## Nice-to-Haves

- A control condition where models are trained on Arabic-translated test data *without* access to the English test set, compared against a clean (no test-set exposure) baseline, would directly test whether translation conceals contamination.
- Calibrating the TS-Guessing probe by running it on English-only contaminated models (where contamination signals should be strong) and comparing with Arabic-condition scores would make the TS-Guessing results interpretable.
- Reporting variance across multiple runs (at least 3 seeds) for key comparisons would add needed statistical grounding.
- The "stronger Arabic capabilities" claim should either be removed or substantiated with independent Arabic-language evaluation.
- TACD should either be implemented and evaluated experimentally, or reframed as a Discussion/Future Work section rather than a standalone contribution.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Criticism about the literature review being too long:** This is a subjective judgment about scope/emphasis, not a substantive evidential weakness.
- **Criticism about missing appendix details (hyperparameters, extended discussion):** The appendix was stripped by the PDF parser; the paper references it and commits to releasing code.
- **Criticism about the TS-Guessing XQuAD protocol being underspecified ("how is the 'critical' token chosen?"):** This is a reasonable clarification question but does not constitute a weakness — the description (masking a critical token in the question) is standard for the TS-Guessing approach and the paper provides a clear figure illustrating the process.
- **Formatting/style complaints:** These are PDF-to-text parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions. The input review correctly identifies several gaps between the paper's framing and its experimental evidence, but these are critiques rather than additive insights.

## Suggestions

1. Redesign the core experiment to include a condition where the English test set is held out entirely, and Arabic-translated data is the only source of contamination. Compare this against a clean baseline with no test-set exposure.
2. Calibrate the TS-Guessing probe by running it on models trained with English-only contaminated data, to confirm the probe produces detectable signals when translation is not a factor.
3. Report variance across multiple random seeds for all key comparisons.
4. Either substantiate or remove the "stronger Arabic capabilities" claim.
5. Either implement and evaluate TACD, or clearly frame it as Discussion/Future Work rather than a contribution.

## Score and Decision

**Calibration anchors considered:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `.../Nk1MegaPuG.md` (Evading Data Contamination Detection) | 4.25 | R1+B2 | Yes | Most topically similar; proposes rephrasing attack to evade detection. That paper had an implemented method (EAL) but suffered from poor clarity and incomplete settings. My paper is cleaner but has a weaker contribution (unimplemented framework). |
| `.../lwtaEhDx9x.md` (Elephants Never Forget) | 4.75 | R1 | Yes | Studies memorization of tabular data with multiple tests. Stronger methodology but limited by lack of ground-truth. My paper has a cleaner controlled setup but weaker evidence for its core claims. |
| `.../Nsms7NeU2x.md` (How much can we Forget) | 6.75 | R1 | Yes | Strong theoretical+experimental study on contamination forgetting. My paper is substantially weaker in both methodology and evidence. |
| `.../jOmk0uS1hl.md` (Training on the Test Task) | 8.00 | R1 | Yes | Very strong paper with clean experiments on task contamination confounding evaluation. My paper is not in this league. |
| `.../rAylWUIKtu.md` (Benchmark Inflation) | 4.25 | R2 | Yes | Retro-holdout methodology; had implemented, tested framework. Comparable in score range to my paper but with stronger validation. |
| `.../JL42j1BL5h.md` (All Languages Matter) | 3.50 | R2 | Yes | Multilingual safety benchmark. Had methodological concerns about translation quality and evaluation; comparable weakness profile. My paper is better structured but has more fundamental experimental design issues. |

**Round 1 bracket:** 3.5–5.5. The paper is clearly above papers scoring <2 (which have trivial or no contributions) and clearly below papers at 6.75+ (which have strong, well-supported evidence).

**Round 2 narrowing:** Comparison with the 4.25 anchors (Evading Detection, Benchmark Inflation) and the 3.50 anchor (All Languages Matter) places this paper in the range 3.5–4.5. The paper's worst-rated weaknesses (favorability -1.03, -0.16) are less severe than the 4.25 anchors' worst items (-3.49, -3.38, -1.20), suggesting a score slightly above 3.5. However, the paper's strengths (favorability 5.80–7.30) are comparable to the 4.25 anchors' strengths, and the paper lacks an implemented, tested contribution (unlike the 4.25 anchors which had working methods). The experimental design issue is structural — the setup cannot cleanly separate the effect of translation from the already-present English test data — which constrains the score below 5.0.

**Final score:** 4.0. The paper asks an important question and is clearly presented, but the experimental design does not adequately support the central claims. The TS-Guessing probe is uncalibrated, the "approximately equal performance" claim is contradicted by the paper's own data, and a key assertion ("stronger Arabic capabilities") is entirely unsupported. These issues are addressable with redesigned experiments but prevent acceptance in the current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>