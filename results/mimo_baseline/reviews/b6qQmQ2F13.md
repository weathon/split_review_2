## Summary

This paper conducts a large-scale empirical study (~1,700 configurations) on how to optimally allocate fixed memory budgets for reasoning model deployment, systematically varying model size, weight precision, token budget, parallel scaling group size, and KV cache compression method. The central finding is that the optimal memory allocation strategy is scale-dependent: small reasoning models (effective size below 8-bit 4B) benefit from investing memory in larger weights, while larger models benefit from investing in longer generations and parallel scaling. The paper also finds task-dependent weight precision requirements and that KV cache eviction outperforms quantization for small models.

## Strengths

- **Systematic and thorough empirical methodology.** The paper sweeps over five key factors (model size, weight precision, token budget, group size, KV compression) across 1,700+ configurations, covering multiple model families (Qwen3, DeepSeek-R1-Distill, OpenReasoning-Nemotron) and multiple benchmarks (AIME25, GPQA-Diamond, LiveCodeBench, MATH500). This breadth lends credibility to the generality of the findings.

- **Practically important and timely question.** The shift from non-reasoning to reasoning models fundamentally changes the memory landscape because KV cache grows with generation length. The paper convincingly argues that prior wisdom (e.g., "4-bit is always sufficient") does not transfer, and provides concrete, actionable guidelines for practitioners deploying reasoning models under memory constraints. The Pareto frontier analysis in Figures 1, 2, 5, and 8 is a clean and interpretable way to present these trade-offs.

- **Robustness across model families and quantization schemes.** The authors verify that their main findings hold for DeepSeek-R1-Distill and OpenReasoning-Nemotron (not just Qwen3), and that AWQ and FP8 yield similar conclusions to GPTQ (Appendix C.2). This significantly strengthens the generalizability claims.

- **Well-structured narrative with clear numbered findings.** Each finding is well-motivated by a specific question, supported by figures, and stated concisely. The paper is unusually well-organized for an empirical study of this scope.

## Weaknesses

### Fatal
None.

### Major

- **The "8-bit 4B" threshold is somewhat arbitrary and imprecisely justified.** The paper repeatedly invokes "effective size below 8-bit 4B" as the critical threshold, but this exact boundary emerges from one model family (Qwen3) on primarily one benchmark (AIME25). While DeepSeek-R1-Distill and OpenReasoning-Nemotron results are shown for parallel scaling (Figures 6, 16), the full Pareto frontier analysis for the weight-vs-KV trade-off (Finding 1) is not replicated for these families. The threshold could be an artifact of the specific parameter count granularity (0.6B, 1.7B, 4B, 8B, etc.) rather than a genuine phase transition. A brief discussion of why this particular threshold arises (e.g., relating it to KV cache-to-weight ratios) would strengthen the claim.

- **Single-run evaluation without confidence intervals or statistical tests.** Results are reported as averaged accuracy over 32 generations for serial scaling and 8 generations for KV compression experiments, but no confidence intervals, standard deviations, or statistical significance tests are provided. Given that the paper makes claims about which configurations are "more memory-efficient" than others, and that some differences on the Pareto frontier appear small (e.g., Figures 2, 9), quantifying uncertainty is important for readers to assess whether the observed differences are reliable.

- **The scale-dependent nature of findings 1 and 3 is presented as novel but is partially expected.** It is somewhat intuitive that very small models would benefit more from capacity than from generating many tokens (a weak model generating 30k tokens may not use them well), and that large models would benefit from test-time compute. The paper would benefit from a more careful framing of what is genuinely surprising versus what follows from basic scaling intuitions, and what the quantitative contribution is (i.e., where exactly the crossover occurs and why).

### Minor

- **Limited exploration of KV cache eviction methods.** Only R-KV and StreamingLLM are considered for eviction. R-KV is a recent method designed for reasoning models, but StreamingLLM is a simple sliding-window approach. The comparison would be strengthened by including more eviction methods (e.g., H2O, SnapKV) to assess whether the eviction-vs-quantization finding is robust across eviction strategies.

- **Budget forcing as the primary serial scaling mechanism.** The paper relies entirely on budget forcing (injecting "Wait" to continue generation) for controlling token budgets, following Muennighoff et al. This can produce degenerate outputs (repetitive or incoherent text) at very long budgets, which may confound the analysis of whether longer generations are truly beneficial. Some analysis of generation quality as a function of forced length would be informative.

- **The verifier experiment (Section 4.1) is shallow.** Only one PRM (ActPRM-X) is evaluated, and the conclusion that "self-contained strategies such as majority voting are preferable" is drawn from a single comparison. More importantly, the PRM memory is counted as a fixed overhead without exploring whether a smaller PRM or a quantized PRM could change the conclusion.

### Trivial
None.

## Nice-to-Haves

- A simple theoretical model or back-of-envelope calculation explaining *why* the 8-bit 4B threshold exists (e.g., relating the KV cache growth rate to the marginal accuracy gain from additional parameters versus additional tokens) would significantly elevate the paper from empirical to insightful.
- Analysis of latency/throughput trade-offs in the main text rather than just in an appendix, since practitioners care about memory *and* speed jointly.
- A concrete deployment recipe or decision flowchart summarizing the guidelines for practitioners.

## Novel Insights

The most genuinely novel insight is that the established wisdom from non-reasoning model compression—"4-bit quantization is generally sufficient"—fails for reasoning models in math and code tasks, and that this failure is task-dependent (knowledge-intensive tasks still favor 4-bit). This task-dependent sensitivity of weight precision is a non-obvious finding that challenges a widely-held assumption. The observation that KV cache eviction is preferable to quantization for small effective models is also interesting and somewhat surprising, as it suggests small models are more sensitive to per-token precision loss than to simply having fewer tokens. The scale-dependent crossover between weight investment and token investment, while partially expected, is concretely quantified and practically useful.

## Suggestions

- Add error bars or confidence intervals to key figures (especially Figures 1, 2, 5, 8) so readers can assess the reliability of the Pareto frontier positions.
- Provide a brief mechanistic explanation for why the 8-bit 4B threshold exists—is it driven by the ratio of KV cache growth rate to marginal accuracy improvement from additional tokens?
- Expand the verifier analysis to include at least one additional PRM and/or a quantized PRM to test robustness of the claim that verifiers are memory-inefficient.
- Replicate Finding 1 (weight vs. KV trade-off) for DeepSeek-R1-Distill and OpenReasoning-Nemotron to confirm the scale threshold generalizes beyond Qwen3.

## Score and Decision

This is a well-executed empirical study that addresses a timely and practically important question. The experimental scope is impressive (~1,700 configurations, multiple model families, multiple benchmarks), the analysis is clean and well-organized, and the findings are actionable. The main weaknesses—the somewhat imprecise threshold claim, lack of uncertainty quantification, and partial expectedness of findings—prevent it from being a strong accept, but the practical value, breadth of experiments, and genuinely novel observations about task-dependent precision requirements and eviction-vs-quantization trade-offs make it a solid contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>