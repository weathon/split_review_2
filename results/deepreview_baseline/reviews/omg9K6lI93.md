## Summary

This paper investigates data contamination in LLMs from a multilingual perspective, specifically examining whether translating English benchmarks into Arabic can mask contamination effects. The authors fine-tune several open-weight LLMs on varying proportions of Arabic-translated benchmark data and evaluate them on original English benchmarks, using an extended TS-Guessing method with choice-reordering to probe memorization. Their key finding is that while translation into Arabic conceals traditional contamination signals, models still benefit from exposure to contaminated data, particularly those with stronger Arabic capabilities, revealing a dangerous blind spot in current evaluation practices. The paper proposes a Translation-Aware Contamination Detection (TACD) framework as a forward-looking blueprint for addressing this issue.

## Strengths

- **Timely and important research question**: The paper addresses a genuine gap in the contamination literature—how contamination manifests in multilingual contexts—which is increasingly relevant as LLMs are evaluated across languages.
- **Novel experimental design**: The idea of using translation as a potential "natural barrier" to contamination and systematically testing this hypothesis through controlled fine-tuning experiments is creative and well-motivated.
- **Extension of TS-Guessing with choice-reordering**: The methodological contribution of extending TS-Guessing with a choice-reordering strategy for MCQ tasks is a practical improvement that helps disentangle genuine reasoning from memorization of index patterns.
- **Clear demonstration of a critical finding**: The paper convincingly shows that translation can mask contamination signals while preserving memorization benefits, which has direct implications for evaluation practices.

## Weaknesses

### Fatal
None.

### Major
- **The core experimental setup has a fundamental confound**: The paper fine-tunes models on Arabic-translated test sets and evaluates on English benchmarks, but this setup conflates two effects: (1) contamination from seeing the test data, and (2) cross-lingual transfer learning from Arabic to English. The performance gains observed could partially reflect improved cross-lingual capabilities rather than pure memorization. The paper does not adequately control for this by, for example, including a condition where models are fine-tuned on Arabic translations of *different* (non-evaluation) datasets to measure the cross-lingual transfer baseline.

- **The TACD framework is presented as a contribution but remains entirely conceptual**: Section 5 describes TACD as a "forward-looking blueprint" with no implementation, no experiments, and no empirical validation. This is essentially a discussion/suggestion section rather than a methodological contribution. The paper would be stronger if it either implemented TACD or reframed it as future work rather than presenting it as a core contribution.

- **Limited scope of models and datasets**: The experiments use only four relatively small models (1B-7B parameters) and three datasets (MMLU, XQuAD, MLQA). The paper's claims about "multilingual contamination dynamics" would be substantially stronger with a broader range of model sizes, architectures, and languages beyond Arabic. The choice of Arabic is motivated but the paper does not demonstrate that the findings generalize to other non-English languages.

- **The "flat trend" claim in Section 4.2 is not well-supported**: The paper states that "across contamination levels, the models exhibit approximately equal performance" and that this "near-flat trend indicates that Arabic→English translation is effectively masking contamination effects." However, Table 2 shows substantial variation across contamination levels for many model-dataset combinations (e.g., Mistral MMLU: 0.577→0.690, LLaMA MMLU: 0.332→0.431, Gemma XQuAD: 0.364→0.606). These are not "flat" trends. The paper's interpretation seems to contradict its own data.

- **Missing statistical rigor**: The paper reports single runs without confidence intervals, standard deviations, or statistical significance tests. Given the variability in the results (especially the non-monotonic patterns), it is unclear which differences are meaningful versus noise. This is particularly problematic for the TS-Guessing results in Table 3, where many values are very close to zero.

### Minor
- **The literature review is disproportionately long** (Sections 2.1-2.4) relative to the paper's own contributions. Much of this material is standard knowledge in the field and could be significantly condensed.
- **The paper's framing of "translation as concealment" is somewhat overstated**: The results show that models *do* benefit from contaminated data (MMLU increases monotonically), which is itself a contamination signal. The claim that translation "conceals" contamination is more about the difficulty of *detecting* it through surface-form matching rather than about contamination being truly hidden.
- **The TS-Guessing results in Table 3 are very weak**: Most EM and ROUGE-L F1 scores are near zero, and the IDR values show inconsistent patterns across contamination levels. The paper does not adequately discuss why these probes appear to be ineffective for these models/datasets.

### Trivial
- The paper uses "terra bytes" instead of "terabytes" (Section 2.3).
- Table 1 is presented without clear context for how it relates to the paper's own experiments.

## Nice-to-Haves

- A control experiment where models are fine-tuned on Arabic translations of non-evaluation datasets to isolate cross-lingual transfer effects from contamination effects.
- Confidence intervals or error bars on all reported metrics.
- Analysis of whether the findings replicate with larger models (e.g., 13B, 70B) or with other languages (e.g., French, Chinese, Swahili).
- An actual implementation and evaluation of the TACD framework, even on a small scale.

## Novel Insights

The paper's most genuinely novel insight is that translation can serve as a "contamination camouflage"—it disrupts surface-form detection methods while preserving the semantic content that models can memorize. This is a non-obvious finding because one might intuitively expect translation to be an effective decontamination strategy. The paper demonstrates that this intuition is false, and that current English-centric contamination detection methods have a systematic blind spot. This insight has practical implications for how the community should design evaluation pipelines and contamination detection tools in an increasingly multilingual LLM landscape.

## Suggestions

1. **Add a control condition**: Fine-tune models on Arabic translations of *different* (non-evaluation) datasets matched for domain and difficulty, then compare performance gains. This would help disentangle contamination from cross-lingual transfer.

2. **Provide statistical measures**: Report results with confidence intervals (e.g., bootstrap) or standard deviations across multiple runs. This is essential given the variability in the data.

3. **Reframe the TACD contribution**: Either implement and evaluate TACD, or clearly label it as "Future Work" rather than presenting it as a core contribution of the paper.

4. **Address the "flat trend" contradiction**: Reconcile the claim that trends are "near-flat" with the substantial variations visible in Table 2. Consider whether the claim should be revised to something more nuanced, such as "translation reduces the *detectability* of contamination through surface-form methods, even though performance effects remain measurable."

5. **Expand the language scope**: Even a small additional experiment with one other language (e.g., French or Spanish) would substantially strengthen the claim that the findings are about multilingualism generally rather than Arabic specifically.

## Score and Decision

The paper addresses a genuine and important gap in the contamination literature with a creative experimental design. However, the core experimental setup has a confound that is not adequately addressed, the TACD framework is presented as a contribution without implementation, and the results do not fully support some of the paper's interpretive claims. The paper has value as a demonstration of a potential blind spot in contamination detection, but the methodological limitations prevent it from being a definitive study.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>