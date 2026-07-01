## Summary

This paper investigates memory-accuracy trade-offs for reasoning LLMs, challenging the universal applicability of 4-bit quantization established for non-reasoning models. Through extensive experiments on the Qwen3 family (0.6B–32B) across mathematical, code, and knowledge-intensive reasoning tasks, the authors identify a scale-dependent optimal strategy: for models with effective size below ~8-bit 4B, memory is better allocated to larger/higher-precision weights, while larger models benefit more from longer generation sequences. The paper provides actionable guidelines covering weight precision choice, KV cache compression (eviction vs. quantization), and parallel scaling, supported by over 1,700 experimental configurations.

## Strengths

- **Timely and practically important research question**: The paper addresses a genuine gap—most prior memory optimization work focuses on non-reasoning models with short outputs, whereas reasoning models generate 10-100x more tokens, making KV cache a dominant memory bottleneck. The question of how to allocate a fixed memory budget across model size, weight precision, token budget, and KV cache compression is directly relevant to deploying reasoning models.
- **Systematic and comprehensive experimental design**: The study spans 5 factors (model size, weight precision, token budget, parallel scaling group size, KV cache compression method) across 3 model families (Qwen3, DeepSeek-R1-Distill, OpenReasoning-Nemotron) and 4 benchmarks. The paper controls for confounds carefully (e.g., verifying GPTQ findings with AWQ and FP8, evaluating serial vs. parallel scaling, comparing eviction and quantization).
- **Clear, non-obvious findings with actionable implications**: The central finding that the memory-optimal strategy flips at an effective size threshold (~8-bit 4B) is interesting and practically useful. The discovery that 4-bit weights are suboptimal for mathematical reasoning but optimal for knowledge-intensive tasks is a concrete, actionable insight that contradicts prior universal recommendations.
- **Methodological rigor in Pareto analysis**: The paper uses Pareto frontiers appropriately to identify memory-optimal configurations, making the trade-offs visually and quantitatively interpretable. The inclusion of a latency analysis (Appendix C.1) adds practical depth.

## Weaknesses

### Major

- **The effective size threshold is presented as a concrete guideline but lacks theoretical grounding or rigorous justification**: The paper repeatedly states thresholds like "8-bit 4B" (~4.2 GB) and "8-bit 8B" as inflection points, but these appear to be empirical observations from a specific family (Qwen3) on specific tasks. The thresholds are derived from a discrete set of model sizes (0.6B, 1.7B, 4B, 8B, 14B, 32B) with specific architectural choices (e.g., number of layers, hidden dimension, attention heads). It is unclear whether the threshold is fundamentally about weight memory (GB), parameter count, or something architecture-dependent. The paper would benefit from either a theoretical analysis explaining why this threshold emerges or a more explicit caveat about its limited generalizability.
- **The paper claims to study "reasoning models" but the primary analysis is on Qwen3, which is not primarily a reasoning model**: Qwen3 is a general-purpose instruction-tuned model family. While the paper also evaluates DeepSeek-R1-Distill and OpenReasoning-Nemotron, the core experiments and all fine-grained Pareto analysis (Figures 1, 2, 5, 8, 9) use Qwen3. The extent to which Qwen3 exhibits reasoning behavior (e.g., extended chain-of-thought, reflection) is not validated. The paper relies on budget forcing to induce longer generations, but this is an external intervention, not an inherent property of the model. The title and framing suggest the findings are about reasoning models generally, but the evidence is strongest for Qwen3 with budget forcing.

### Minor

- **The comparison between KV cache eviction and quantization is limited to one method each**: The paper uses R-KV for eviction and symmetric per-channel quantization (HQQ backend) for quantization. There are many other KV cache compression methods (e.g., KIVI, GEAR, CacheGen, SnapKV, PyramidKV) that might alter the conclusions. The paper acknowledges this in limitations but the strength of Findings 4 and 5 would be increased by a broader comparison.
- **The external verifier analysis (Section 4.1) is too brief to be conclusive**: The paper evaluates only one PRM (ActPRM-X) with one configuration. PRM-based scaling is a large and active area, and the single data point showing it is memory-inefficient under the paper's specific setup is not sufficient to draw general conclusions. The paper's own caveat about limited verifier evaluation is appropriate.
- **Memory accounting for parallel scaling is somewhat artificial**: The paper assumes a setting where all parallel samples are generated independently within the same memory budget (model weights shared, KV cache multiplied by group size). While this is valid for batched inference, many practical deployments use sequential generation or model-parallel settings where the trade-off is different. The paper acknowledges different batch sizes in Appendix C.3 but the main analysis uses fixed assumptions.

### Trivial

- The paper uses "effective size" interchangeably with "weight memory (GB)" but also refers to "8-bit 4B" as a threshold. This terminology could be clarified—8-bit 4B is not a model that exists (4B models are used at 4-, 8-, or 16-bit precision), it is a hypothetical construct for the threshold.
- The abstract claims "models with an effective size below 8-bit 4B parameters" which is a dense phrase.

## Nice-to-Haves

- A theoretical model or scaling law that predicts the inflection point from architectural parameters (e.g., number of layers, hidden dimension, head dimension) would greatly strengthen the paper.
- A practical decision tree or flow chart summarizing the guidelines would make the paper more accessible to practitioners.
- Analysis of how the optimal strategy changes under latency constraints (not just memory) would be valuable, though the paper does provide some latency analysis in Appendix C.1.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel observation is that the *task type* mediates the optimal weight precision even before considering KV cache: knowledge-intensive tasks tolerate 4-bit weights better than mathematical reasoning tasks, even at the same model size and memory budget. This suggests that different reasoning sub-skills (factual retrieval vs. multi-step symbolic manipulation) have different sensitivity to weight quantization, which is not explained by simple number of parameters or compute. This could motivate future work on task-adaptive quantization strategies for reasoning models.

## Suggestions

- Clarify the status of Qwen3 as a reasoning model. Provide evidence (e.g., average generation lengths, chain-of-thought patterns) that Qwen3 with budget forcing is representative of reasoning model behavior, or reframe the paper as being about "budget-forced instruction-tuned models" rather than "reasoning models."
- Add a section or paragraph explaining what factors determine the effective size threshold and why it might shift across model families or architectures. At minimum, discuss the limitations of the discrete model sizes used to derive the threshold.
- Expand the KV cache compression comparison to include at least one additional eviction method and one additional quantization method to strengthen the claim that the findings are about the *type* of compression, not specific implementations.

## Score and Decision

This paper addresses an important, under-explored problem with a systematic and rigorous experimental design. The findings are novel (challenging the universal 4-bit prescription) and practically actionable. The main weaknesses are the limited evaluation on true reasoning models (reliance on Qwen3) and the lack of theoretical grounding for the effective size threshold, but these do not invalidate the paper's core contributions. The paper is clearly written, well-organized, and the experimental methodology is sound. I recommend acceptance.

**Score**: 8

**Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>