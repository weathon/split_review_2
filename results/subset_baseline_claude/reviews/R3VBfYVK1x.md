## Summary

This paper presents an empirical evaluation of 12 frontier LLMs on 464 binary forecasting questions from Metaculus, comparing their Brier scores against a human crowd and a group of expert forecasters hired by Metaculus. It also tests a "narrative" prompting strategy inspired by jailbreaking techniques, finding that models perform worse under this framing than with direct prompting.

## Strengths

- **Timely and comprehensive model coverage**: The study evaluates the most recent frontier models (o3, o3-pro, GPT-4.1, Qwen3-235B, etc.) as of 2025, meaningfully extending prior benchmarks like Halawi et al. (2024) and Karger et al. (2025) which tested older models.
- **Credible data leakage control**: The hold-out set (130 questions with news collected in real time on the question open date) provides a principled check on whether the main dataset results are contaminated by post-resolution article edits. The consistency of results across both datasets is reassuring.
- **Novel narrative prompting experiment**: Testing whether fictional framing elicits better latent knowledge is a legitimately interesting research question; the finding that it hurts rather than helps has practical implications for LLM deployment and robustness.
- **Ensemble methodology**: Running five independent predictions per question and reporting both mean and median ensembles is a good design that reduces noise from individual stochastic outputs.

## Weaknesses

### Fatal
None that fully invalidate the study.

### Major

- **Uncontrolled expert–model comparison**: The core claim—that expert forecasters "significantly outperform" models—is undermined by a critical confound. Experts predicted on only 47% of questions (157/334), almost certainly self-selecting to questions in their domains of expertise. The paper never computes model Brier scores on the same 157 expert-predicted questions. Without this apples-to-apples comparison, the 0.023 vs. 0.135 gap conflates question difficulty/selection bias with forecasting skill. This is the most important methodological gap in the paper.

- **Speculative linear extrapolation**: Figure 1 plots superforecaster performance at "September 2027" based on a linear trend in Brier score versus release date, treating the superforecaster score as a future data point. This framing is scientifically problematic—improvement curves for LLMs are not guaranteed to be linear, and placing human expert performance on the same axis conflates a fixed human performance level with a moving LLM trend.

- **Ambiguous cross-dataset Brier score comparisons**: The paper repeatedly compares its Brier scores with those from Halawi et al. (0.149) and Karger et al. (0.121), acknowledging that "Brier scores are not directly comparable across different question sets," yet then makes the comparison anyway as a "general indicator." The differing question difficulty distributions make this comparison potentially misleading.

### Minor

- The narrative prompting experiment conflates two different effects: (1) fictional framing changing probability elicitation behavior and (2) reasoning mode differences. There is no ablation that holds the chain-of-thought structure constant while varying only the framing.
- Category-level analysis (Table 4) relies on very small samples for arts & recreation (n=16) and sports (n=32), and the author acknowledges this. The claim that "models do better on healthcare" for newer OpenAI models (n=31) should be disclaimed more strongly as likely noise.
- The description of o3-pro achieving a median Brier score of 0.0225 on 157 questions for *expert forecasters* (Table 8 header says "Expert forecasters") while o3-pro the *model* is scored on 334 questions is confusing and deserves clearer presentation.

### Trivial
- The paper uses "Brier score" and "score" interchangeably in different tables; standardizing terminology would aid clarity.

## Nice-to-Haves

- A regression or matching analysis restricting model evaluation to the exact 157 questions the expert forecasters chose to predict on would substantially strengthen the expert comparison.
- Analyzing whether model calibration errors are systematic (e.g., persistent overconfidence on specific categories) would be more informative than the current qualitative description.
- Comparing the LLM-ensemble Brier score with the raw crowd median on this specific dataset (not from other papers) would provide an internally consistent crowd baseline.

## Novel Insights

The narrative prompting result is the most novel contribution: fictional framing consistently degrades forecasting accuracy across all tested models, including reasoning models, suggesting that stylistic scaffolding that activates "story completion" mode systematically biases probability outputs. This observation, if replicated more rigorously, has direct implications for prompt injection and jailbreak robustness—fictional framing may elicit fluent but less calibrated output.

## Suggestions

- Restrict the expert vs. model comparison to the shared 157-question subset and report model Brier scores on that subset alongside expert scores.
- Replace the linear extrapolation in Figure 1 with confidence intervals or a range of trend assumptions, and remove the expert score from the trend line.
- Add statistical significance tests (e.g., paired Wilcoxon or bootstrap confidence intervals) for key model-vs-model and model-vs-expert comparisons.

## Score and Decision

The paper addresses a real and important question, employs a credible experimental setup, and includes useful empirical results. However, it is essentially an incremental empirical update to a well-established line of work (Halawi et al., Karger et al.), the primary novel finding (expert gap) suffers from a fundamental confound that is not addressed, and the writing and framing are informal. The narrative prompting experiment is interesting but underdeveloped. For ICLR, this sits below the bar for acceptance.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>