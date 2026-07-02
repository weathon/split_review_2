## Summary

This paper investigates data contamination in LLMs from a multilingual perspective, specifically examining whether translating English benchmarks into Arabic can mask contamination effects. The authors fine-tune four open-weight LLMs on varying proportions of Arabic-translated benchmark data (MMLU, XQuAD, MLQA) and evaluate on original English benchmarks, using TS-Guessing with choice-reordering to detect memorization. They find that while translation obscures traditional contamination signals, models still benefit from contaminated data, particularly those with stronger Arabic capabilities. The paper proposes a Translation-Aware Contamination Detection (TACD) framework as a forward-looking blueprint for multilingual contamination detection.

## Strengths

- **Novel and timely research question**: The investigation of how translation affects contamination dynamics in multilingual contexts is genuinely underexplored in the literature, and the finding that translation can mask but not eliminate contamination is practically important for the evaluation community.
- **Well-designed experimental setup**: The use of multiple models (4), datasets (3), and contamination proportions (0%, 10%, 50%, 100%) provides a reasonably comprehensive investigation. The extension of TS-Guessing with choice-reordering is a clever methodological contribution.
- **Clear and actionable main finding**: The paper convincingly demonstrates that translation ≠ decontamination, which has direct implications for how the community should approach multilingual evaluation pipelines.

## Weaknesses

### Major

- **Insufficient statistical rigor**: The paper reports single-point accuracy numbers without confidence intervals, standard errors, or multiple runs. Given the small model sizes (1B-7B parameters) and the relatively modest performance differences between contamination levels (e.g., MMLU 0.577→0.580 for Mistral at 10%), it is impossible to assess whether observed differences are statistically significant or simply noise. This is particularly problematic for the non-monotonic trends in XQuAD/MLQA, which the paper interprets substantively.

- **Contradiction between core claims and evidence**: The paper's central claim is that translation "conceals traditional contamination signals" (Section 4.2), yet Table 2 shows clear monotonic improvements on MMLU for all models as contamination increases (e.g., Mistral: 0.577→0.690, LLaMA: 0.332→0.431). These are substantial gains that are detectable even through translation. The paper's argument that translation masks contamination is weakened by its own evidence showing contamination effects are clearly visible.

- **The TACD framework is underspecified**: The proposed Translation-Aware Contamination Detection framework is presented as a "forward-looking blueprint" with no implementation, no experimental validation, and no concrete algorithmic details. It reads as a discussion section rather than a contribution. The paper would be stronger without claiming this as a contribution or by providing even a preliminary implementation.

- **Missing critical experimental details**: The paper does not specify which Arabic translation was used (machine translation? human translation? which service?), the quality of translations, or whether translations were verified for semantic fidelity. Given that the entire experiment hinges on translation quality, this omission is significant. The Appendix is referenced but not available in the provided content.

### Minor

- **Model selection rationale is unclear**: The paper uses models ranging from 1B to 7B parameters but does not explain why these specific models were chosen or how their Arabic capabilities were assessed (beyond a vague reference to "stronger Arabic capabilities").
- **The TS-Guessing results in Table 3 are very low**: Most IDR and EM scores are near zero (e.g., 0.001, 0.005), which raises questions about whether the probe is actually detecting anything meaningful. The paper interprets these as contamination signals, but near-zero rates could also indicate the probe is too difficult or poorly designed.
- **Limited scope of datasets**: Only three datasets are used, and MMLU is the only multiple-choice benchmark. The findings may not generalize to other task formats or languages.

### Trivial

- The paper uses "terra bytes" instead of "terabytes" (Section 2.3).
- Table 1 is presented without clear explanation of its provenance or how it relates to the paper's experiments.

## Nice-to-Haves

- Running experiments with multiple random seeds and reporting confidence intervals would substantially strengthen the statistical claims.
- Including a baseline with English-only contamination (without translation) would help quantify how much translation actually "masks" versus simply reduces contamination effectiveness.
- Providing qualitative examples of model outputs under TS-Guessing would help readers understand what the near-zero detection rates actually mean.

## Novel Insights

The paper's key insight—that translation can obscure surface-level contamination signals while preserving semantic-level memorization—is genuinely novel and important. This challenges the implicit assumption in much of the contamination literature that detection methods operating on English text are sufficient. The finding that models with stronger Arabic capabilities benefit more from translated contamination (though not rigorously demonstrated) points toward an important interaction between language proficiency and contamination susceptibility that deserves further study. However, the paper's own evidence partially undermines this claim by showing that contamination effects are still detectable through standard evaluation metrics even after translation.

## Suggestions

1. **Add statistical rigor**: Report results over multiple runs (at least 3-5 seeds) with confidence intervals or standard deviations. This is essential given the small performance differences being interpreted.
2. **Reconcile the central claim with the evidence**: The paper should either acknowledge that MMLU shows clear contamination effects despite translation, or reframe the claim to focus on specific scenarios where masking occurs (e.g., extractive QA tasks).
3. **Provide translation details**: Specify the translation method, quality metrics, and any validation of semantic preservation. Without this, the experimental foundation is unclear.
4. **Either implement TACD or remove it as a contribution**: The framework as presented is too vague to be evaluated. Either provide a concrete implementation with experimental results, or reframe it as future work/discussion.
5. **Include an English-only contamination baseline**: Train models on English contaminated data at the same proportions to directly compare how translation affects contamination detectability.

## Score and Decision

The paper addresses a genuinely important and underexplored question with a reasonable experimental design. The core finding—that translation can mask contamination—is valuable to the community. However, the paper is weakened by insufficient statistical rigor, a partial contradiction between its central claim and its own evidence, and an underspecified proposed framework. The lack of confidence intervals and the absence of translation quality details are significant methodological concerns. The paper would benefit from substantial revision before acceptance.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>