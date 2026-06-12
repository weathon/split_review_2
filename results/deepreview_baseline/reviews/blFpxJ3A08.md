## Summary

The paper presents LPFQA, a benchmark for evaluating LLMs on long-tail professional knowledge, built by automatically extracting question-answer pairs from screenshots of technical forum discussions across 20 fields. The pipeline uses MLLMs for QA generation with LLM-based quality control, followed by expert verification and difficulty calibration. 12 mainstream LLMs are evaluated on the 505-question benchmark, revealing performance disparities and ablations on code interpreter and search tool integration.

## Strengths

- **Relevant problem identification**: The paper correctly identifies that existing benchmarks insufficiently cover long-tail professional knowledge grounded in real-world user needs, and the forum-sourcing approach is a reasonable attempt to address this gap.
- **Practical evaluation methodology**: The expert verification step (Phase 3) provides quality assurance that many fully automated benchmark construction pipelines lack, and the empirical difficulty testing adds practical discriminative value.
- **Interesting ablation findings**: The observation that search tool integration *decreases* performance on long-tail knowledge (Section 4.2.2) is a non-obvious result worth reporting, suggesting that retrieval on rare topics can introduce noise rather than help.

## Weaknesses

### Major
- **Factual contradiction in main analysis**: The paper states that "DeepSeek-V3 demonstrates the most balanced and consistent performance across disciplines, with no apparent weaknesses, and can thus be regarded as the overall best-performing model." Table 1 shows DeepSeek-V3 scores **32.60**, second-lowest among all 12 models, while GPT-5 leads at **47.28**. This is not a matter of interpretation—it is a direct contradiction of the paper's own data and severely undermines the credibility of the analysis section.
- **Claimed evaluation dimensions are never used**: The paper repeatedly highlights "four fine-grained evaluation dimensions: knowledge depth, reasoning, terminology comprehension, and contextual analysis" as a key innovation. However, all experimental results are reported only by field breakdowns (Physics, Math, etc.). No evaluation is conducted along these four proposed dimensions, making this a stated contribution that is entirely unrealized in the experiments.
- **Insufficient scale relative to scope**: 505 questions across 20 fields (some fields have as few as 3–8 items, e.g., Data Science: 3, AI: 8, Aerospace: 8) raises concerns about per-field statistical reliability. After filtering out non-discriminative questions (Section 4.2.1), only 421 items remain. A benchmark meant to evaluate "long-tail professional knowledge" across 20 diverse domains with fewer than 30 questions per field on average has limited representativeness.
- **Post-hoc filtering reveals design limitations**: The paper's own analysis shows that a non-trivial fraction of questions are either unsolvable by any model or solvable by all models, requiring post-hoc removal to improve discriminative power. This suggests the difficulty calibration pipeline (Phase 3) did not fully achieve its stated goal, and the benchmark design could have been validated more rigorously before evaluation.

### Minor
- **The long-tail nature of the questions is asserted, not demonstrated**: The paper discusses long-tail distribution conceptually and claims the benchmark tests long-tail knowledge, but provides no quantitative analysis (e.g., frequency of topics in common corpora, rarity estimates) to support this characterization.
- **No comparison or correlation with existing benchmarks**: The paper argues that existing benchmarks are insufficient but never compares LPFQA to MMLU, HLE, or Arena-Hard in terms of what it measures differently or how model rankings correlate. This limits the ability to assess whether LPFQA provides genuinely new signal.
- **Ablation interpretations are under-supported**: The code interpreter ablation showing decreased performance is interpreted as "LPFQA primarily reflects domain knowledge mastery rather than reasoning ability." This is a strong conclusion from a single experiment with potential confounders (e.g., integration quality, models' ability to decide when to invoke CI).

### Trivial
- The abstract says "502 tasks" while the paper consistently uses "505 questions" elsewhere.
- The y-axis in Figures 2 and 5 is labeled "Quality of items" but the data shown are counts, not quality scores.

## Nice-to-Haves
- An analysis of how LPFQA model rankings correlate with rankings on MMLU, HLE, or Arena-Hard would help establish whether the benchmark captures distinct information.
- Reporting per-question variance or confidence intervals across the three trials would strengthen the reliability of the results.
- A breakdown of model performance by the four claimed evaluation dimensions (knowledge depth, reasoning, terminology, contextual analysis) would demonstrate that these dimensions are operationalizable.

## Novel Insights

The observation in Section 4.2.2 that search tool integration *hurts* rather than helps performance on long-tail knowledge is genuinely interesting and non-obvious, though it is reported as a single ablation with limited analysis of *why* this occurs (e.g., does the retrieved information contradict the correct answer, or does the model become over-reliant on noisy search results?). Beyond this, the paper does not produce a novel insight that extends beyond its own benchmark construction and evaluation.

## Suggestions

- Correct the DeepSeek-V3 analysis error: either fix the factual mistake in the text or provide evidence that the authors meant a different model.
- Conduct and report evaluation along the four proposed dimensions (knowledge depth, reasoning, terminology, contextual analysis) or remove the claim as a contribution if it is not operationalized.
- Add correlation analysis with at least one existing benchmark (e.g., MMLU or HLE) to demonstrate what new signal LPFQA provides.
- Provide quantitative evidence for the long-tail nature of the questions (e.g., occurrence frequency in pretraining corpora or in web-scale data).
- Report per-field confidence intervals or statistical significance for model comparisons, especially for fields with very few questions.

## Score and Decision

This paper tackles a relevant problem and presents a reasonable construction methodology, but it has significant execution issues. The factual contradiction in the main results analysis (misidentifying the worst-performing model as the best) and the complete absence of evaluation along the claimed four dimensions are major flaws that weaken the paper's core claims. The small per-field sample sizes and lack of validation against existing benchmarks further limit the contribution's impact. The idea has merit, but the paper in its current form does not sufficiently support its conclusions.

**Score**: 4

**Decision**: Reject

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>