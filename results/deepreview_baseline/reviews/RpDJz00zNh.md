##Summary

The paper proposes ConciseHint, a framework that improves the reasoning efficiency of large reasoning models (LRMs) by injecting learnable hints (manually designed text or trained embeddings) *during* the token generation process, rather than before reasoning begins. The method adaptively controls hint intensity based on query complexity (using current reasoning length as a proxy) and dynamically selects injection positions to balance accuracy and computational cost. Experiments on GSM8K, AIME24, and GPQA-Diamond with Qwen3 and DeepSeek-R1 models show substantial token reduction while maintaining accuracy, and the approach can be combined with existing efficiency methods.

## Strengths

- **Novel in-reasoning intervention paradigm**: Unlike prior work that applies prompts or fine-tuning before reasoning, ConciseHint directly influences the model during generation. This is a conceptually clean and underexplored direction that opens new possibilities for efficiency control.
- **Adaptive complexity-aware design**: The injection interval grows with the current reasoning length (Equation 1), automatically providing stronger hints for easy queries and weaker hints for complex ones. Ablations (Table 3) convincingly show that fixed high-intensity injection harms accuracy on hard benchmarks (AIME24) while adaptive injection avoids this.
- **Dynamic position selection**: The injection position moves from head to tail as reasoning progresses (Equation 3), avoiding both accuracy degradation (tail injection) and excessive prefilling costs (head injection). Table 4 provides clear empirical support.
- **Training hint embeddings (ConciseHint-T)**: Learning hint embeddings on concise data further reduces token usage and provides controllable efficiency via interpolation (γ). The method generalizes to out-of-domain benchmarks (AIME24, GPQA-Diamond) reasonably well.
- **Comprehensive evaluation**: Experiments cover multiple model sizes (Qwen3-1.7B/4B/8B, DeepSeek-R1-14B), three diverse benchmarks, and integration with four existing baselines. The consistent token reduction across settings demonstrates robustness.

## Weaknesses

### Major

- **Practical overhead of multiple generation calls**: Algorithm 1 calls `client.completions.create` for each injection interval, meaning the model is invoked multiple times per query (e.g., for a 1000-token output with τ_k≈128, roughly 8 calls). This introduces significant latency and API cost that is not accounted for in the reported token usage. The paper claims extra costs are negligible (Section A.2, stripped), but wall-clock time or number of forward passes should be reported. A method that reduces token count but increases latency may not be practically efficient.

- **Overstated novelty regarding "during-reasoning" intervention**: The paper claims existing methods "do not dynamically intervene in the model during the token generation" (Section 2.2). However, Deer (early exit) and NoWait (removing transition tokens) both intervene during generation. The distinction is that ConciseHint injects external hints, but the claim of being the first to intervene during reasoning is inaccurate and should be clarified.

### Minor

- **Simplicity of complexity proxy**: Using current reasoning length as a proxy for complexity assumes a monotonic relationship, but some queries may be verbose without being complex (e.g., the model repeats itself). The paper acknowledges this as a prior but does not validate it or discuss failure cases. A more robust proxy (e.g., based on model confidence or semantic redundancy) could be explored.

- **Limited analysis of reasoning quality**: The paper reports accuracy and token counts but does not qualitatively examine whether the model skips important reasoning steps or produces less coherent chains after hint injection. The transition word analysis (Table 5) is a start, but a case study showing the full reasoning trace with and without hints would strengthen the paper.

- **Uneven effectiveness across models**: On DeepSeek-R1-14B, token reduction is modest (e.g., 17% on AIME24 vs. 10% for BeConcise). The paper does not discuss why the method is less effective on this model or whether hyperparameters (α, β) need adjustment.

### Trivial

- The paper uses "Ori." and "On" interchangeably in tables (Table 5 uses "On" instead of "Ori."). This is a minor inconsistency.

## Nice-to-Haves

- Report wall-clock time or number of generation calls alongside token usage to give a complete efficiency picture.
- Include results on commonsense reasoning (CommonsenseQA) and code generation (HumanEval) in the main paper, as they are mentioned in the appendix.
- Provide a qualitative example showing the full reasoning trace with and without ConciseHint to illustrate how the hint changes the model's behavior.
- Discuss the sensitivity of α and β more thoroughly, especially for different model families.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Measure and report the actual latency or number of API calls incurred by ConciseHint. If the overhead is small (e.g., because the model can be called with a large batch of tokens), provide evidence. If it is large, discuss trade-offs and potential optimizations (e.g., injecting hints in a single pass via logit manipulation).
- Clarify the novelty claim by explicitly comparing to Deer and NoWait, which also intervene during generation, and explain why ConciseHint's approach is distinct and valuable.
- Add a qualitative analysis of reasoning traces to show that the model does not sacrifice reasoning quality for conciseness.

## Score and Decision

**Score**: 6.0  
**Decision**: Accept

The paper presents a genuinely novel and well-motivated approach to improving reasoning efficiency. The adaptive injection mechanism is clever and empirically validated. However, the practical overhead of multiple generation calls is a significant concern that must be addressed before the method can be considered ready for deployment. The novelty claim is slightly overstated but does not invalidate the contribution. Overall, the paper brings sufficient value to the community and opens a promising new direction.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>