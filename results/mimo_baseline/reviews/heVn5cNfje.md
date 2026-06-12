## Summary

This paper introduces High-Entropy Sum (HES), a training-free metric that sums the entropy of the top 0.5% highest-entropy tokens in each reasoning sample to quantify reasoning quality. The key insight is that high-entropy tokens correspond to critical "forking points" in reasoning where the model considers multiple options, and their cumulative entropy better distinguishes high- from low-quality samples than global metrics like average entropy. HES is validated across SFT, RFT, and RL paradigms, demonstrating that selecting data by HES improves efficiency (20% of data matches full-dataset performance) and that pruning low-HES data can actually exceed full-dataset training.

## Strengths

- **Simple, effective, and broadly applicable metric.** HES is computationally cheap (no additional model training), and the paper demonstrates consistent improvements across three training paradigms (SFT, RFT, RL), multiple base models (Qwen3-8B-Base, DeepSeek-R1-Distilled-Qwen-7B, DeepSeek-R1-Distilled-Qwen-1.5B), and three domains (math, code, STEM). The SFT results are particularly striking: Table 1 shows Highest-HES-80% achieves 35.36% average, surpassing the Full-Dataset baseline of 32.61% on the 8B model, and on DeepSeek-R1-Distilled-Qwen-7B (Table 2), Highest-HES-20% achieves 34.61% vs. 30.22% for Full-Dataset.

- **Well-designed experimental methodology.** The paper includes comprehensive comparisons against multiple baselines (difficulty-based, length-based, average entropy, entropy sum, forking-only training), cross-model transferability (0.6B proxy for 8B training), per-query vs. global pool RFT settings, and sensitivity analyses for both the data selection ratio and high-entropy token ratio. The ablation that Lowest-HES-20% scores only 14.90% (Table 1) provides strong evidence that HES captures a meaningful quality signal.

- **Novel RL sampling strategy with practical value.** The asymmetric RL approach—selecting highest-HES positive trajectories paired with random negatives—achieves 21.30% average accuracy, outperforming the Full-Batch baseline of 20.63% while using only half the training data per step (Table 6). The finding that constraining negative samples (Neg-Low strategies) hurts performance is a valuable practical insight about maintaining negative diversity.

## Weaknesses

### Fatal

None.

### Major

- **Incomplete explanation for why high-entropy tokens indicate quality.** The paper's core premise is that high entropy at forking tokens reflects the model navigating complex reasoning rather than being confused, but this causal link is not rigorously established. It is plausible that some high-entropy tokens reflect genuine uncertainty or errors rather than valuable decision points. The paper does not analyze the semantic content of the selected high-entropy tokens—do they correspond to actual reasoning decision points (e.g., "however," "let me reconsider," choice points in multi-step problems), or are they spread across various token types? Some form of token-level qualitative analysis would substantially strengthen the core claim.

- **Limited diversity in evaluation domains.** Despite claims of generality, the evaluation is heavily weighted toward mathematical reasoning (6 of 7 primary benchmarks). The code and STEM extensions (Tables 3-4) are welcome but use a smaller set of benchmarks and fewer experimental conditions. It remains unclear whether HES would work for tasks where the reasoning structure differs fundamentally (e.g., open-ended creative writing, dialogue, summarization), or whether the "top 0.5%" heuristic holds across substantially different sequence length distributions.

- **The 0.5% percentile choice lacks thorough justification.** While sensitivity analysis (Figures 3-4) shows that 0.005 performs best, the paper does not provide strong intuition for why this specific value works well. Is it related to the fraction of truly critical tokens in typical CoT sequences? How does this interact with sequence length? The sensitivity analysis shows that for some benchmarks (MMLU STEM, LiveCodeBench), the choice barely matters, while for others (AIME 2024) it makes a significant difference—the paper does not discuss this heterogeneity.

### Minor

- **RFT improvements are modest.** In the per-query RFT setting (Table 5), the gains of Highest-HES over Random are relatively small (e.g., +1.01 for k=2, +1.69 for k=4, +0.97 for k=8). The paper acknowledges this but could better contextualize whether these gains are practically significant at this scale.

- **Potential confound with response length.** Although the paper compares against a length-based baseline, the analysis does not explicitly disentangle the relationship between HES and length. Longer responses likely have more high-entropy tokens and higher HES sums. The relative percentile threshold partially addresses this, but a correlation analysis between HES and length would clarify how much of the signal is truly attributable to the entropy distribution versus response length.

- **The AvgHE metric is underexplored.** The paper introduces AvgHE (Eq. 3) but presents it primarily as a negative control. A brief discussion of why averaging over high-entropy tokens performs worse than summing would provide additional insight into the mechanism—does the number of forking points (numerator of HES) matter independently of their average intensity?

### Trivial

- The paper states "AvgHE is defined as HES_relative normalized by |T_high|, the number of tokens in the set. It is designed to isolate the average complexity of key-fork tokens, different from AvgHE" — this appears to be a typo where the last "AvgHE" should be "AvgE".

## Nice-to-Haves

- A qualitative analysis showing example reasoning paths with their high-entropy tokens highlighted, demonstrating that HES-selected samples indeed contain more insightful reasoning strategies (e.g., productive backtracking, exploration of alternative approaches) compared to low-HES samples.
- Analysis of whether HES quality rankings are stable across different models (i.e., does a sample have high HES under model A and also under model B?), which would further support the claim that HES captures intrinsic data properties.
- Experiments on smaller-scale or non-reasoning tasks to establish the boundary conditions of the method.

## Novel Insights

The observation that training on 80% of data ranked by HES (with the bottom 20% pruned) actually outperforms training on 100% of the data is a genuinely valuable finding. It provides strong evidence that certain training samples are not merely uninformative but actively harmful—a "less is more" result that has significant practical implications for data curation. The asymmetric RL sampling insight (high-quality positives + diverse negatives) is also a useful and somewhat counterintuitive finding that extends beyond simple data filtering.

## Suggestions

- Add a section analyzing the semantic properties of tokens selected by HES. For instance, report what fraction of top-0.5% entropy tokens correspond to connective words, mathematical operators, digits, or other categories, and how this differs between correct and incorrect samples.
- Investigate whether a length-normalized variant of HES (e.g., HES divided by sequence length) could provide an even cleaner signal, or whether the current formulation already adequately handles this.
- Consider expanding the RL experiments to a larger model (e.g., 7B) to confirm that the findings scale, as the current RL experiments use only the 1.5B model.

## Score and Decision

This paper presents a simple, well-validated metric with clear practical value across multiple training paradigms. The experimental design is thorough, the results are consistent, and the findings about harmful data are genuinely useful. However, the lack of deeper mechanistic understanding (why do high-entropy tokens indicate quality?) and the narrow domain focus prevent a higher score. The contribution is solid but falls in the "good incremental work" category rather than a major conceptual advance.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>