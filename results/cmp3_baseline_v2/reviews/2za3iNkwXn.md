## Summary

The paper systematically investigates how three compression methods (quantization, distillation, pruning) affect the reasoning capabilities of Large Reasoning Models (LRMs), focusing on DeepSeek-R1 and its distilled variants. The authors benchmark compressed models across four reasoning datasets and use mechanistic interpretability techniques (difference of means + attribution patching) to compute fine-grained weight importance scores, revealing which weight matrices are critical for reasoning and how compression shifts their importance. Key findings include that weight count affects knowledge memorization more than reasoning, that the MLP up-projection in the final layer of distilled LRMs is the most important component, and that current quantization methods over-compress final-layer modules and MLP gate projections—protecting just 2% of weights yields a 6.57% average accuracy improvement.

## Strengths

- **Timely and important research question**: Understanding how compression affects reasoning in LRMs is crucial for efficient deployment and democratization of large models. The paper addresses a clear gap in the literature (compression studies focused on general LLMs, not specifically on reasoning models).
- **Comprehensive benchmarking**: The paper evaluates three compression paradigms (quantization, distillation, pruning) across multiple methods (dynamic quantization, AWQ, GPTQ, GPTAQ, ANY4/3, SparseGPT, AlphaPruning) on four diverse reasoning benchmarks (AIME 2024, FOLIO, Temporal Sequences, MuSiQue), with multiple model sizes (7B to 671B). This provides a useful empirical landscape.
- **Empirically validated findings with practical implications**: The core findings about the importance of the final-layer up-projection and the over-compression of gate projections are validated through selective quantization and protection experiments. The demonstration that protecting only ~2% of weights (final-layer MLP modules) can improve accuracy by 6.57% and surpass existing 3-bit methods by up to 23.17% is practically actionable.
- **Generalization across model families**: The paper provides evidence that key findings extend beyond R1 to non-R1 models (e.g., Llama-3.1-8B, Qwen-2.5-7B), increasing the impact of the results.

## Weaknesses

### Fatal
None.

### Major
1. **Methodological novelty is limited**: The interpretability approach (difference of means + attribution patching) is directly adapted from prior work (Venhoff et al., 2025; Arditi et al., 2024; Syed et al., 2023) without significant methodological innovations. The contribution lies in the *application* to compressed LRMs and the empirical findings, not in the method itself. The paper claims "fine-grained interpretation" as a distinguishing factor, but the adaptation is relatively straightforward.

2. **Validation of importance scores is somewhat circular**: The validation in Section 4.2 selectively quantizes a component identified as important and measures accuracy drop. While this confirms correlation, it is an expected outcome—quantizing any critical component should degrade performance. The validation would be stronger if compared against an alternative importance measure (e.g., weight magnitude, gradient-based sensitivity, or random component selection) to demonstrate that the identified component is *uniquely* critical. The fact that "1_up" (last row) causes the lowest accuracy on AIME 2024 while being ranked last overall undermines the consistency of the ranking.

3. **Lack of mechanistic explanation for *why* the final-layer up-projection is important**: The paper identifies the empirical finding but provides limited analysis of the functional role of this component in reasoning. Why does distillation concentrate importance in the final-layer up-projection? What computational role does this projection play in the reasoning process? Without deeper mechanistic understanding, the finding remains a correlation rather than a causal explanation.

4. **The "protection" experiment (Section 5.2) is a crude mixed-precision approach**: Keeping 2% of weights at 16-bit while quantizing the rest to 3-bit is a well-known mixed-precision strategy. The paper presents this as a "validation" of the bottleneck finding, but it more directly demonstrates that higher precision helps on important weights—a known fact in quantization literature. The experiment is a reasonable sanity check but not a novel intervention.

5. **Generalization claims are not fully substantiated in the main text**: The paper states findings "generalize to non-R1 families" but only references Appendix J (which is stripped from the provided content). Without concrete evidence in the main body, the generalization claim feels under-supported. Key results from non-R1 models should be included in the main paper.

### Minor
1. **MuSiQue results are very low (EM 0-17%)**, even for uncompressed R1 (EM 17.0). While the paper acknowledges this is due to the closed-book setting, the low scores limit the informativeness of MuSiQue-based analyses and conclusions about knowledge retention.
2. **The annotation of reasoning behaviors relies on GPT-4o**, which introduces potential noise and dependence on a proprietary model. The paper references Appendix G for robustness, but details are not in the main text.
3. **Statistical uncertainty is not reported**: Scores are averaged over three runs but standard deviations or confidence intervals are not provided. Given performance variability in LLMs, this would strengthen the conclusions.
4. **The "collapse point" analysis is informal**: The paper describes collapse points qualitatively (e.g., "between 40% and 50% sparsity") without a formal definition or statistical test for when collapse occurs.

### Trivial
- In Figure 1, "POUO" appears instead of "FOLIO" in the task list.
- Some notation inconsistencies (e.g., `RI_{m\ell}^c` vs `RI^c_{m\ell}`).

## Nice-to-Haves
- Include error bars or confidence intervals for all reported scores.
- Compare the proposed importance measure with simpler baselines (e.g., weight magnitude, Fisher information) to demonstrate added value.
- Provide a mechanistic analysis of *why* the final-layer up-projection is critical for reasoning (e.g., by examining its role in the residual stream or in output token prediction).
- Report results for the protection experiment on more models (e.g., Qwen variants) and more quantization methods.

## Novel Insights

Beyond the paper's own contributions, the most striking finding is that **current state-of-the-art quantization methods systematically over-compress precisely the weights that distillation makes most critical for reasoning** (final-layer modules and MLP gate projections). This reveals a fundamental misalignment between how compression methods distribute error and where the model is most sensitive. The implication is that generic calibration-based quantization (like AWQ) may be insufficient for reasoning-optimized models, and that post-distribution importance analysis should guide mixed-precision allocation. The finding that distillation creates a sharp concentration of importance in a single weight matrix (the final-layer up-projection) rather than distributing importance across layers is also noteworthy, as it suggests that the "reasoning capability" of distilled LRMs may be surprisingly localized.

## Suggestions

1. **Strengthen the validation of importance scores** by comparing against alternative importance metrics (e.g., random baseline, weight magnitude) to demonstrate that the identified component is uniquely critical.
2. **Include key generalization results in the main text** (from Appendix J) to substantiate the claim that findings apply to non-R1 models.
3. **Add statistical uncertainty measures** (standard deviations or confidence intervals) for all main results.
4. **Provide a clearer definition of "collapse point"** with a quantitative criterion rather than qualitative description.
5. **Discuss limitations of the GPT-4o annotation pipeline** explicitly in the main text, including potential biases.

## Score and Decision

This paper makes a solid empirical contribution by systematically benchmarking and interpreting compression effects on reasoning models. The findings are practically useful and validated through targeted experiments. However, the methodological novelty is limited (adaptation of existing interpretability techniques), the validation has some circularity, and the generalization claims are not fully substantiated in the main text. The paper is above the acceptance threshold but not at the level of a top-tier contribution. 

MY FINAL SCORE: 6.0</score>
MY FINAL DECISION: Accept</decision>