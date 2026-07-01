## Summary

This paper proposes ConciseHint, a framework that improves the reasoning efficiency of large reasoning models (LRMs) by injecting hints (either manually designed text or learned continuous embeddings) *during* the token generation process, rather than before reasoning (prompting) or after fine-tuning. The method adaptively controls hint injection intensity based on query complexity and dynamically selects injection positions to balance accuracy and computational cost. Experiments on GSM8K, AIME24, and GPQA-Diamond with Qwen3 and DeepSeek-R1 models show substantial token reduction while maintaining accuracy, and the approach can be combined with existing efficiency methods for further gains.

## Strengths

- **Novel paradigm**: The paper introduces a genuinely new direction for reasoning efficiency—in-reasoning intervention—which is orthogonal to existing before-reasoning (prompting, fine-tuning) approaches. This opens a promising research avenue.
- **Well-motivated adaptive design**: The complexity-adaptive hint intensity (Eq. 1) and dynamic injection position (Eq. 3) are clearly motivated by the need to avoid harming accuracy on complex queries while maximizing conciseness on easy ones. Ablation studies (Tables 3, 4) convincingly justify these design choices.
- **Comprehensive empirical evaluation**: Experiments cover multiple state-of-the-art LRMs (Qwen3-4B/8B, DeepSeek-R1-14B) and three diverse benchmarks (GSM8K, AIME24, GPQA-Diamond). The method is tested both individually and in combination with four existing baselines, consistently showing token reduction with minimal accuracy loss.
- **Flexibility and compatibility**: ConciseHint can be seamlessly integrated with existing methods (BeConcise, Prompt, Deer, NoWait) to further push efficiency, demonstrating its value as a plug-in module.
- **Controllability via learned embeddings**: ConciseHint-T shows that training hint embeddings on concise data yields additional token reduction and provides a controllable trade-off via interpolation (γ parameter), with reasonable generalization to out-of-domain data.

## Weaknesses

### Fatal
None.

### Major
1. **Lack of latency/wall-clock time analysis**: The method requires multiple generation interruptions, hint injection, and re-prefilling of modified text. The paper claims "negligible extra costs" but provides no empirical evidence (e.g., time per query, FLOPs, or throughput). Token count reduction alone does not guarantee actual speedup if the overhead of repeated API calls or re-prefilling is significant. This is a critical gap for a method whose core claim is improving efficiency.
2. **Heuristic design choices with limited justification**: The adaptive interval formula (τ_k = α + β·l_k) and the dynamic position formula (p = τ_k * min((τ_k - α)/1024, 0.8)) rely on fixed constants (α=128, β=0.2, denominator 1024, cap 0.8) that appear arbitrary. While ablation shows they work on the tested settings, there is no theoretical grounding or sensitivity analysis across diverse tasks. The paper states performance is "not sensitive to β" but does not show this systematically.

### Minor
1. **Limited evaluation diversity**: The main results focus on math and science benchmarks. CommonsenseQA and HumanEval are mentioned in the appendix but not presented in the main paper, weakening the claim of general applicability.
2. **Overhead of re-prefilling not fully quantified**: Table 4 reports "prefilling ratio" but does not translate this into actual computational cost or latency. The dynamic strategy reduces prefilling but still incurs some cost; the paper should compare total compute (including prefilling) against baselines.
3. **Comparison with baselines could be stronger**: Some baselines (e.g., "Prompt" is a custom prompt, not a standard method) are relatively weak. The paper would benefit from comparing with more recent or stronger efficiency methods, such as budget forcing or adaptive computation time.

### Trivial
None.

## Nice-to-Haves

- Provide wall-clock time or FLOPs measurements to demonstrate that token reduction translates to actual speedup.
- Analyze the sensitivity of α and β more thoroughly, perhaps with a grid search or theoretical motivation.
- Test on a broader set of tasks (e.g., code generation, multi-step reasoning) to strengthen generality claims.
- Explore more sophisticated hint designs (e.g., task-specific hints) or learned hints that adapt per query.

## Novel Insights

Beyond the paper's own contributions, the key insight is that *continuous intervention during generation* can effectively steer reasoning models toward conciseness without requiring retraining or altering the model's weights. This contrasts with the dominant before-reasoning paradigm and suggests that efficiency can be treated as a dynamic control problem rather than a static optimization. The complexity-adaptive mechanism further highlights that a one-size-fits-all compression strategy is suboptimal; the model's own generation length serves as a useful proxy for query difficulty.

## Suggestions

- **Provide latency measurements**: Run a timing comparison (e.g., seconds per query) for ConciseHint vs. baselines, including the overhead of hint injection and re-prefilling. This is essential to validate the efficiency claim.
- **Clarify implementation details**: Explain how hint injection is performed in practice (e.g., via API calls with prompt modification, or by manipulating the model's internal state). Discuss the computational cost of each injection step.
- **Add sensitivity analysis for hyperparameters**: Show how accuracy and token usage vary with α and β across different benchmarks, and justify the chosen values more rigorously.
- **Include more diverse benchmarks in the main paper**: Move CommonsenseQA and HumanEval results to the main text to demonstrate broader applicability.

## Score and Decision

**Score**: 6  
**Decision**: Accept

The paper presents a novel and well-executed idea with solid empirical support. The main weakness—lack of latency analysis—is significant but addressable; the core contribution is valuable enough to warrant acceptance at a borderline level. If the authors can convincingly demonstrate that the overhead is negligible in practice, the score could be raised.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>