## Summary

This paper investigates memory-accuracy trade-offs for reasoning LLMs under fixed memory budgets, challenging the universal 4-bit quantization prescription established for non-reasoning models. Through systematic experiments across model sizes (0.6B-32B), weight precisions, token budgets, parallel scaling, and KV cache compression strategies, the authors identify a scale-dependent inflection point at approximately 8-bit 4B effective model size: smaller models benefit more from allocating memory to higher-precision weights, while larger models benefit more from longer generation and parallel scaling. The paper provides actionable guidelines for practitioners deploying reasoning models under memory constraints.

## Strengths

- **Timely and practically important research question**: As reasoning models with long generation chains become increasingly deployed, understanding memory-accuracy trade-offs under realistic constraints is highly valuable to the community. The paper correctly identifies that prior work on non-reasoning models does not transfer directly.

- **Comprehensive and systematic experimental design**: The study spans over 1,700 configurations across model sizes (0.6B-32B), multiple weight precisions (4/8/16-bit), token budgets (2k-30k), parallel scaling (G=1-16), and KV cache compression methods. The inclusion of multiple model families (Qwen3, DeepSeek-R1-Distill, OpenReasoning-Nemotron) and diverse benchmarks (AIME25, GPQA-Diamond, LiveCodeBench, MATH500) strengthens the generality of findings.

- **Clear, actionable findings with practical guidelines**: The paper distills complex trade-offs into five concrete findings with clear thresholds (e.g., 8-bit 4B effective size as inflection point). The finding that 4-bit weights are memory-optimal for knowledge tasks but not for mathematical reasoning is a nuanced and useful insight.

- **Rigorous Pareto frontier analysis**: The use of Pareto-optimal frontiers to compare strategies is appropriate and well-executed. The analysis of which configurations lie on the frontier (Figure 2) provides clear visualization of the strategic shift between small and large models.

## Weaknesses

### Major

- **Limited exploration of KV cache compression methods**: The paper evaluates only two eviction methods (R-KV, StreamingLLM) and one quantization backend (HQQ). Given that Finding 5 (eviction vs. quantization) is a core contribution, the paper would benefit from broader validation across more KV cache compression techniques (e.g., KIVI, KVQuant, or other recent methods). The claim that eviction is "better" for small models may be specific to the particular methods tested.

- **The 8-bit 4B threshold is not rigorously justified**: The paper repeatedly cites "8-bit 4B" as the inflection point, but this threshold appears to emerge from the specific model sizes tested (0.6B, 1.7B, 4B, 8B, 14B, 32B). With only one model near the threshold (4B), it is unclear whether the threshold is truly at 4B parameters or somewhere between 1.7B and 8B. The paper would benefit from finer-grained analysis or a more principled justification for this specific threshold.

- **Limited analysis of latency and throughput trade-offs**: The paper focuses almost exclusively on memory-accuracy trade-offs, but practical deployment also depends on latency and throughput. While Appendix C.1 is mentioned, the main text does not adequately address how the recommended strategies affect inference speed. For example, recommending higher-precision weights for small models may increase memory bandwidth requirements and latency.

### Minor

- **The external verifier analysis is too limited**: The paper evaluates only one PRM (ActPRM-X) and concludes that external verifiers are "consistently memory-inefficient." This is a strong claim based on a single verifier. Different verifiers have different memory footprints and accuracy characteristics, and the conclusion may not generalize.

- **Budget forcing methodology may introduce artifacts**: The paper uses prompt injection ("Wait") to force longer generations, which may affect generation quality differently across model sizes. The paper does not analyze whether budget forcing introduces systematic biases that could affect the scale-dependent findings.

- **The paper does not discuss the computational cost of quantization itself**: GPTQ requires a calibration set and inverse-Hessian computation, which has non-trivial computational overhead. For practitioners, the cost of applying quantization may be relevant to the overall deployment decision.

### Trivial

- The paper uses "effective size" to mean both "parameters × bits per weight" and "memory footprint of weights" in different places, which could cause confusion.

## Nice-to-Haves

- A practical decision flowchart or table summarizing the recommended strategy for different model sizes, task types, and memory budgets would increase the paper's utility for practitioners.
- Analysis of whether the findings hold for mixture-of-experts (MoE) architectures, which have different memory characteristics.
- Discussion of how the findings interact with emerging inference optimization techniques like speculative decoding or prefix caching.

## Novel Insights

The paper's key insight is that memory optimization for reasoning models is fundamentally scale-dependent, with an inflection point where the optimal strategy flips from prioritizing model weights to prioritizing test-time compute. This challenges the prevailing assumption that 4-bit quantization is universally optimal and provides a principled framework for reasoning about memory allocation. The finding that task type (mathematical vs. knowledge-intensive) affects the optimal weight precision is also novel and practically important. The observation that parallel scaling only becomes memory-efficient above a certain model size threshold provides useful guidance for practitioners considering majority voting strategies.

## Suggestions

- Provide a more rigorous characterization of the inflection point, either through finer-grained model size experiments or through theoretical analysis relating effective model size to KV cache memory ratio.
- Expand the KV cache compression comparison to include additional methods (e.g., KIVI, KVQuant) to strengthen Finding 5.
- Include latency measurements for the recommended configurations to provide a more complete picture of deployment trade-offs.
- Clarify whether the findings hold when using different budget forcing strategies or when models generate naturally (without forced continuation).

## Score and Decision

The paper makes a solid empirical contribution to an important and timely problem. The experimental design is comprehensive, the findings are clearly presented and actionable, and the paper identifies genuine limitations in prior work. However, the reliance on a single threshold derived from a coarse grid of model sizes, the limited evaluation of KV cache compression methods, and the insufficient treatment of latency trade-offs prevent the paper from being a definitive reference. The paper is a valuable contribution that will be of interest to practitioners and researchers working on reasoning model deployment.

MY FINAL SCORE: 6.0</score>
MY FINAL DECISION: Accept</decision>