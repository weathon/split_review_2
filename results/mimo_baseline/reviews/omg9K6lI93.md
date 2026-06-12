## Summary

This paper investigates whether translating benchmarks into Arabic can mask data contamination in LLMs. The authors fine-tune four open-weight models on varying proportions of Arabic-translated benchmark data (MMLU, XQuAD, MLQA), evaluate on the original English benchmarks, and extend the TS-Guessing method with choice reordering to probe memorization. They conclude that translation conceals traditional contamination signals while still benefiting models, and propose a conceptual Translation-Aware Contamination Detection (TACD) framework.

## Strengths

- **Important and timely research question.** The multilingual dimension of data contamination is genuinely understudied, and the core hypothesis—that translation could act as a camouflage for contamination—is well-motivated and practically relevant for evaluation integrity.

- **Systematic experimental design.** The use of four models across three datasets with four contamination levels (0%, 10%, 50%, 100%) provides a reasonable factorial design. The controlled fine-tuning setup (identical optimizer, schedule, and batch policy) is appropriate for isolating the effect of contamination proportion.

- **Extension of TS-Guessing with choice reordering.** The idea of shuffling multiple-choice options before masking to detect reliance on memorized index positions is a reasonable methodological addition for MCQ contamination probing.

## Weaknesses

### Fatal

None.

### Major

- **Internal contradiction between results and narrative.** Section 4.2 claims "the models exhibit approximately equal performance on all evaluated benchmarks" and that Tables 2 and 3a show "scores remain broadly stable as p increases." However, Table 2's MMLU column directly contradicts this: Mistral goes from 0.577 to 0.690, LLaMA from 0.332 to 0.431, Gemma from 0.220 to 0.284—clear, non-trivial increases. These are substantial gains, not "approximately equal" performance. This contradiction between the paper's own data and its central interpretive narrative significantly undermines the paper's credibility and makes it difficult to assess what the results actually demonstrate.

- **Inconsistent and hard-to-interpret TS-Guessing results.** The TS-Guessing data (Table 3) are highly variable across models: LLaMA's IDR peaks at 50% then drops; Gemma's IDR *decreases* monotonically with contamination; Mistral's IDR stays near zero throughout. For XQuAD, all EM scores are ≤ 0.103. With such heterogeneity, it is difficult to draw any generalizable conclusion about whether TS-Guessing reliably detects cross-lingual contamination. The paper does not adequately acknowledge or explain this variability.

- **TACD framework is purely conceptual with no validation.** Section 5 proposes a three-component detection framework (cross-translation benchmarking, TS-Guessing across variants, back-translation consistency) but provides no experiments, no preliminary results, and no concrete algorithmic specification. The authors themselves acknowledge it is "a forward-looking blueprint rather than a complete implementation." While the idea is sound, presenting an untested framework as a contribution limits the paper's actionable impact.

### Minor

- **Non-monotonic extractive QA trends are under-analyzed.** XQuAD and MLQA results frequently peak at 10% contamination then decline (e.g., Qwen's MLQA: 0.162 → 0.409 → 0.157). The paper notes this briefly as "fragile transfer" but does not offer a clear mechanistic explanation or controlled experiment to distinguish distributional overfitting from genuine cross-lingual degradation.

- **Missing embedding analysis in main text.** The paper references an "embedding figure" showing cosine similarity between Arabic→English translations and originals, but this evidence does not appear in the main paper content provided. This is central to the claim that "translation ≠ decontamination" yet the supporting evidence is absent from the presentation.

- **Dataset selection rationale is thin.** MMLU (knowledge MCQ), XQuAD (cross-lingual extractive QA), and MLQA (multilingual QA) serve different purposes and test different capabilities. The paper does not discuss why this particular combination was chosen or how findings might differ for other benchmark types (e.g., reasoning, code generation).

- **Table 3a caption says "Overall TS-Guessing (MCQ) on MMLU" but the columns list "IDR" and "RL-F1" without clearly connecting RL-F1 to the masked-choice text generation. The relationship between these two metrics and what each specifically captures is not explained.

### Trivial

None.

## Nice-to-Haves

- A baseline comparison using same-language contamination (English→English) to quantify how much translation specifically reduces detectability, rather than relying on cross-model variability alone.
- Statistical significance tests or confidence intervals for the reported metrics, given the small model sizes (1B–7B) and potential sensitivity to fine-tuning randomness.
- Analysis of whether the contamination benefits are proportionate to the Arabic capabilities of each model, as the abstract claims "models with stronger Arabic capabilities" benefit more, but this is not systematically validated.

## Novel Insights

The paper's core finding—that Arabic translation preserves semantic contamination signals while obscuring surface-level detection—is genuinely novel and practically important. The observation that MMLU (closed-book MCQ) benefits from contamination more consistently than extractive QA, combined with the non-monotonic behavior on XQuAD/MLQA, suggests that contamination through translation differentially affects task types depending on whether the task relies on option discrimination versus span grounding. However, the paper's internal contradictions and inconsistent TS-Guessing results prevent this insight from being established with the rigor needed for a strong contribution.

## Suggestions

1. **Resolve the central contradiction.** Either acknowledge the MMLU performance gains as evidence that contamination is *not* masked at the evaluation level (even if surface-level detection fails), or redefine what "masking" means precisely—e.g., masking of detection probes only, not of performance effects.
2. **Provide a clear same-language contamination baseline.** Fine-tune on English versions of the same benchmark data at the same proportions to establish the "unmasked" contamination effect, enabling a direct comparison of how much translation reduces detectability.
3. **Run TACD components on the existing data.** Even a minimal instantiation—e.g., checking whether TS-Guessing on Arabic versions of MMLU detects contamination that English TS-Guessing misses—would strengthen the conceptual framework with empirical grounding.

## Score and Decision

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>