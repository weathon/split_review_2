Now I have a clear picture. Let me write the final consolidated review.

## Summary
This paper investigates whether translating benchmarks into Arabic masks data contamination in LLM evaluation. The authors fine-tune four open-weight models on varying proportions of Arabic-translated benchmark data (MMLU, XQuAD, MLQA) plus corresponding English data, then evaluate on the original English benchmarks. They extend the TS-Guessing memorization probe with a choice-reordering strategy for multiple-choice questions. The paper claims translation conceals traditional contamination signals while models still benefit from exposure, and proposes a Translation-Aware Contamination Detection (TACD) framework as a forward-looking blueprint.

## Strengths
- **Well-motivated and genuinely under-explored research question.** The paper correctly identifies that contamination detection has overwhelmingly focused on English, and asks whether translation can act as a "natural barrier" — a legitimate and timely gap (Section 1, Section 2.4).
- **TS-Guessing extension with choice reordering is a sensible methodological adaptation.** Shuffling answer options and checking whether the model recalls the pre-shuffle index letter is a clean way to isolate memorization of surface form from genuine content reasoning in the MCQ setting (Section 3.3, Figure 1).

## Weaknesses

### Fatal
None.

### Major
- **Contradiction between Section 4.2's "near-flat" claim and the paper's own data.** Section 4.2 asserts that "across contamination levels p ∈ {10, 50, 100}%, the models exhibit approximately equal performance on all evaluated benchmarks" and describes a "near-flat trend." This directly conflicts with Table 2. For example: Mistral's XQuAD drops 75% (0.455→0.114), Mistral's MMLU jumps 19% (0.580→0.690), and most other models show clear upward trends (Gemma XQuAD +26%, LLaMA XQuAD +24%, Qwen XQuAD +31%). Section 4.1 separately acknowledges this variation in detail, making the flatness claim in Section 4.2 internally inconsistent with the paper's own analysis.

- **Claim that translations "evade standard detection tools" is tested nowhere in the paper.** The abstract and conclusion assert that Arabic translations "evade standard detection tools" and "obscure exact string matches" (Section 1, Section 6). The paper surveys Min-K% Prob, guided prompting, and n-gram overlap methods in Section 2.3 but never applies any of them to the Arabic-translated data. This claim is an assertion with no experimental support.

- **TS-Guessing probe yields null results that the paper interprets as confirmatory without justification.** Table 3 shows that the TS-Guessing probe — the paper's own instrument for detecting memorization — produces near-zero values across nearly all models and conditions (MMLU IDR mostly ≤0.01–0.35, ROUGE-L F1 ≤0.12, XQuAD EM ≤0.10). The paper interprets these null results as evidence that translation "masks" contamination. However, an equally (if not more) parsimonious explanation is that fine-tuning on Arabic translations does not produce detectable memorization of English content, and the performance changes in Table 2 reflect other mechanisms (e.g., additional in-domain training data, distributional interference). The paper provides no positive control showing that TS-Guessing detects memorization when it occurs (e.g., by fine-tuning on English test items directly), so the "masking" interpretation of the null results is unsupported.

- **Ambiguity about whether training data includes the evaluation set.** The paper states that D_EN^d for MMLU consists of "English test items formatted as MCQ" (Section 3.1). If this refers to the MMLU test set itself (which is also the standard evaluation split), then every model including the p=0 baseline has seen the evaluation data during training. The paper does not clarify whether training and evaluation splits are distinct. The fact that p=0 scores (e.g., Mistral MMLU 0.577) are not near-perfect suggests the relationship is not straightforward, but the paper's failure to specify this unambiguously is a significant clarity gap that affects the interpretation of all results.

- **No uncertainty quantification.** All experiments are reported as single runs with no confidence intervals, standard errors, or statistical significance tests (Table 2, Table 3). With no measure of variance, small differences (e.g., Qwen MMLU ranging 0.553–0.581) cannot be assessed for meaningfulness, and strong claims about performance trends are unsupported.

### Minor
- **Translation provenance unspecified.** The paper does not state how Arabic translations of MMLU items were produced (machine translation, human translation, or existing resource). Translation quality is central to interpreting whether "translation" is the mechanism behind the observed patterns (Section 3.1).
- **Unsupported claim about same-language settings.** Section 4.2 asserts "in typical same-language settings, increasing p would be expected to induce noticeable shifts" without a citation or a same-language control experiment. This claim is asserted rather than demonstrated.
- **Fine-tuning paradigm vs. real-world contamination.** The paper studies deliberate fine-tuning on translated test data, which differs fundamentally from the incidental contamination during web-scale pretraining that motivates the work. This disconnect is not acknowledged or discussed.
- **TACD is an unimplemented blueprint.** Section 5 presents TACD as a contribution but explicitly acknowledges it as "a forward-looking blueprint rather than a complete implementation" (Section 5.3). While honestly stated, this means the framework provides no empirical evidence of its effectiveness.

### Trivial
None.

## Nice-to-Haves
- A same-language control condition (fine-tuning on English-only data at varying proportions) would strengthen the claim that translation specifically — rather than data quantity — is responsible for the observed patterns.
- Testing on additional languages beyond Arabic would probe the generality of the claim.
- Probing what models actually learned (e.g., evaluating on Arabic-language benchmarks or analyzing internal representations) would clarify the mechanism behind the performance changes.
- Positive controls demonstrating TS-Guessing detects memorization when it occurs (e.g., after fine-tuning on English test items directly).

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- *"All models are already contaminated with English test items (fatal confound)"* — Demoted from Fatal to Major (see Major weaknesses, point 4). The ambiguity about training/evaluation splits is a real concern, but calling it fatal overstates the case: p=0 scores are not inflated relative to expected model performance, suggesting the confound, if present, does not straightforwardly undermine the experiment's main comparisons.
- *"Reproducibility / code release upon acceptance"* — Removed per instruction (standard practice; parser strips appendix with hyperparameters).
- *"No analysis of sampling strategy for D_AR subsets"* — Removed as a minor implementation detail that does not threaten the paper's core claims.

## Novel Insights
None beyond the paper's own contributions. The review surfaces a contradiction between the paper's flatness claim and its own data, and highlights that the null TS-Guessing results undermine rather than support the core narrative — the paper lacks the positive controls needed to distinguish "translation masks contamination" from "the fine-tuning did not cause measurable memorization."

## Suggestions
- Resolve the contradiction between Section 4.2 (claims of flatness) and Section 4.1 / Table 2 (acknowledged variation) by revising the text to accurately describe the observed patterns.
- Either run standard contamination detectors (Min-K% Prob, n-gram overlap, guided prompting) on the Arabic-translated data, or remove the untested claim that translations "evade standard detection tools."
- Add positive controls: show that TS-Guessing detects memorization when models are fine-tuned on English test items directly, so the null results under Arabic translation can be meaningfully interpreted.
- Clarify the exact relationship between the D_EN^d training data and the evaluation splits for each dataset.
- Report confidence intervals or use multiple seeds to quantify experimental uncertainty.

---

**Calibration anchors used:**

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| Evading Data Contamination Detection (Nk1MegaPuG) | 4.25 | 1 | Similar topic (evading detection). That paper had an implemented method with experiments; this paper raises a more interesting question but has weaker execution (contradictory claims, untested assertions, null probe results). |
| To the Cutoff... and Beyond (m2NVG4Htxs) | 6.75 | 1 | Rigorous longitudinal contamination analysis with statistical evidence. The current paper is substantially less rigorous and well-executed. |
| How much can we Forget about Data Contamination? (Nsms7NeU2x) | 6.75 | 1 | Strong theoretical + empirical contamination work. The current paper lacks comparable depth and methodological rigor. |

**Round 1 bracket:** 3.0 – 4.5.

The most directly comparable anchor ("Evading Data Contamination Detection," avg 4.25) had a concrete implemented method with experiments evading detectors, but was criticized for overclaimed contributions and limited technical depth. The current paper has a more interesting question but weaker execution: an internal contradiction between its flatness claim and its own data, an unsupported claim about evading standard detectors, null probe results interpreted as confirmatory without positive controls, and ambiguous specification of training/evaluation splits. These issues collectively lower it below the Evading Detection anchor.

**Final score: 3.5** — between Reject and Borderline Reject. The question is genuinely interesting and the TS-Guessing adaptation is sensible, but the experimental reporting is internally inconsistent, the central interpretive claim is unsupported, and several strong assertions are untested. Substantial revision of the claims, addition of positive controls, and clarification of the experimental setup would be needed before the paper's thesis could be properly evaluated.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>