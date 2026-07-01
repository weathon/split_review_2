## Summary

This paper proposes **Copy-Paste**, a generation paradigm that mitigates RAG hallucinations by directly embedding contextual fragments into responses. The authors observe an inverse correlation between copying degree and hallucination density, and instantiate the paradigm through a two-stage pipeline: (1) three prompting methods (CP-Order, CP-Link, CP-Refine) generate high-copying responses, and (2) DPO training internalizes a preference for contextual trust into **CopyPasteLLM**. Using only 365 training samples (50× fewer than baselines), CopyPasteLLM achieves 12.2%–24.5% accuracy improvements on FaithEval counterfactual subsets and strong results on ConFiQA and PubMedQA. A mechanistic analysis (Context-Parameter Copying Capturing) reveals that the model recalibrates confidence in parametric knowledge rather than enhancing contextual representations.

## Strengths

- **Simple, well-motivated idea with strong empirical support.** The inverse correlation between copying degree and hallucination (Figure 1) provides a clear, intuitive motivation. The three prompting methods (CP-Order, CP-Link, CP-Refine) are carefully designed to trade off copying strength, fluency, and relevance, and Table 2 shows they consistently outperform baselines across models and datasets.
- **Remarkable data efficiency.** CopyPasteLLM is trained on only 365 query-context pairs, yet outperforms Context-DPO (18,000 samples), Canoe (10,000), and ParamMute (32,580) on counterfactual benchmarks (Table 1). This is a significant practical advantage.
- **Comprehensive evaluation across multiple settings.** The paper tests both counterfactual (Table 1) and non-counterfactual (Table 3) scenarios, on three diverse benchmarks (FaithEval, ConFiQA, PubMedQA), and reports multiple metrics (accuracy, hit rate, faithfulness, hallucination, fluency). The results are consistent and convincing.
- **Mechanistic interpretability.** The Context-Parameter Copying Capturing algorithm (Section 3.3) provides token-level analysis of knowledge source reliance during CoT generation. Figures 3 and 4 offer novel insights: CopyPasteLLM suppresses parametric knowledge confidence while preserving contextual representations, explaining its improved faithfulness.
- **Clear and well-structured presentation.** The problem formulation, methodology, and experimental design are easy to follow. The two-stage pipeline is illustrated effectively in Figure 2.

## Weaknesses

### Fatal
None.

### Major
- **Use of FaithEval for both training and testing.** The paper removes 241 samples used for training CopyPasteLLM from FaithEval and tests on the remaining samples. While this is acknowledged, it is non-standard to partition a benchmark in this way. The test set may no longer be representative of the full benchmark, and comparisons with baselines that were not trained on any FaithEval data (e.g., Attributed, CoCoLex) are not perfectly fair. The authors should report results on the full FaithEval (without training on it) or justify why the subset is still a valid evaluation.
- **Missing hallucination metrics for CopyPasteLLM in counterfactual settings.** Table 2 reports hallucination (Twist, Causal) for prompting methods, but Table 1 (CopyPasteLLM counterfactual) only reports Accuracy and Hit Rate. Including hallucination metrics would strengthen the claim that CopyPasteLLM reduces hallucinations, not just improves accuracy.
- **Potential bias in preference data construction.** The Elo-style LLM-as-Judge tournament (Section 3.2) introduces a subjective component. The paper does not analyze the quality or consistency of these judgments, nor does it compare against simpler ranking strategies (e.g., direct metric-based ranking). This is a key step in the pipeline and deserves more scrutiny.

### Minor
- **The term "Copy-Paste" is slightly misleading.** The methods (especially CP-Refine) involve iterative refinement and limited generation, not pure verbatim copying. The paper acknowledges this (e.g., "discourse glue" for CP-Link), but the name may overstate the degree of extraction.
- **Comparison with GPT-4o is in the appendix and not central**, but the claim "remarkably outperforming GPT-4o’s reported 47.5%" (Appendix Table 6) is an apples-to-oranges comparison (different model scale, training data, and evaluation setup). This should be toned down or contextualized.
- **The Context-Parameter Copying Capturing algorithm** compares runs with and without context, but the "without context" run may produce entirely different responses, making token-level logit comparisons noisy. The paper acknowledges this limitation but does not discuss potential confounds (e.g., different response lengths, topic shifts).

### Trivial
- None.

## Nice-to-Haves

- An ablation study comparing different preference data construction strategies (e.g., direct metric-based ranking vs. Elo tournament) would strengthen the pipeline design.
- Analysis of CopyPasteLLM’s performance on the full FaithEval benchmark (without training on any part of it) would make the evaluation more standard.
- A discussion of when high copying might be harmful (e.g., when context contains errors or biases) would add nuance, though the ethics statement touches on this.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that **explicit lexical copying can serve as a proxy for contextual faithfulness**, and that this behavior can be internalized through preference optimization with remarkably little data. The mechanistic finding—that CopyPasteLLM suppresses parametric knowledge confidence rather than enhancing contextual representations—is non-trivial and suggests that hallucination mitigation may be more about reducing competition from internal knowledge than about improving context processing. This could inspire future work on targeted parametric knowledge suppression.

## Suggestions

- Report results on the full FaithEval benchmark (without training on any part of it) to enable direct comparison with published baselines.
- Include hallucination metrics (Twist, Causal) for CopyPasteLLM in counterfactual settings (Table 1) to directly demonstrate hallucination reduction.
- Provide an analysis of the LLM-as-Judge ranking consistency (e.g., inter-rater agreement if multiple judges are used, or correlation with automatic metrics).
- Tone down the GPT-4o comparison or provide a more controlled setting (e.g., same prompt, same context).

## Score and Decision

**Score:** 8  
**Decision:** Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>