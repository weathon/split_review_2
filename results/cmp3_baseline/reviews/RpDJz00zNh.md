## Summary

This paper proposes ConciseHint, a framework that improves the reasoning efficiency of large reasoning models (LRMs) by injecting hints (manually designed text or learned embeddings) *during* the token generation process, rather than before reasoning (e.g., prompting or fine-tuning). The method adaptively controls hint injection intensity based on query complexity via a dynamic interval that grows with reasoning length, and dynamically selects the injection position to balance accuracy and computational cost. Experiments on GSM8K, AIME24, and GPQA-Diamond with Qwen3 and DeepSeek-R1 models show substantial token reduction while maintaining accuracy, and the method can be combined with existing baselines for further gains.

## Strengths

- **Novel paradigm**: The paper identifies and explores an underexplored direction—intervening *during* reasoning generation to encourage conciseness—which is orthogonal to the dominant before-reasoning approaches (prompting, SFT, RL). This is a clear conceptual contribution.
- **Simple yet effective design**: The complexity-adaptive injection interval (Equation 1) and dynamic position selection (Equation 3) are intuitive, require minimal hyperparameter tuning, and are well justified through ablation studies.
- **Strong empirical results**: ConciseHint consistently reduces token usage across multiple models (Qwen3-4B/8B, DeepSeek-R1-14B) and benchmarks, often by 30–65%, with minimal or no accuracy loss. The method also improves upon strong baselines (BeConcise, Prompt, Deer, NoWait) and can be combined with them.
- **Flexibility and controllability**: The training-free version (ConciseHint) is immediately applicable, while the trained version (ConciseHint-T) further reduces tokens and provides controllable efficiency via interpolation (γ). The method generalizes to out-of-domain data.
- **Thorough ablation studies**: The paper convincingly demonstrates the necessity of adaptive interval control (Table 3) and dynamic position selection (Table 4), showing that fixed strategies either harm accuracy or increase computational cost.

## Weaknesses

### Fatal
None.

### Major
- **No wall-clock time or computational cost measurement**: The paper reports only token usage as the efficiency metric. Since ConciseHint requires multiple generation calls (one per injection interval), the actual latency and FLOP overhead could offset token savings. Without time or cost measurements, the practical efficiency gain is unverified.
- **Arbitrary design choices in position selection**: The formula for injection position (Equation 3) uses constants 1024 and 0.8 without clear justification. The paper references an appendix for theoretical and empirical analysis, but the appendix is not available for review. This makes it impossible to verify the claim that extra costs are negligible.
- **Overhead of multiple API calls**: The algorithm stops generation, injects a hint, and resumes generation repeatedly. This introduces latency from repeated model calls and context re-prefilling. The paper discusses prefilling costs but does not quantify the total overhead or compare end-to-end time against single-generation baselines.

### Minor
- **Limited model scale**: Experiments use models up to 14B parameters. It is unclear whether the method scales to larger models (e.g., 70B+) where verbose reasoning is more pronounced and computational savings matter most.
- **Accuracy degradation on some settings**: On DeepSeek-R1-14B, ConciseHint (Ori) reduces accuracy on AIME24 (63→61) and GPQA-Diamond (56→54.65). The paper does not analyze these failure cases or discuss when the method might hurt performance.
- **Weak justification for length as complexity indicator**: The paper assumes reasoning length is positively correlated with query complexity, citing prior work. While plausible, this assumption may fail for some queries (e.g., a complex problem solved quickly by a confident model). The adaptive mechanism partially mitigates this, but the paper does not discuss edge cases.

### Trivial
- The paper uses "state-of-the-art LRMs" but evaluates on Qwen3 and DeepSeek-R1, which are open-source but not the largest available models. This is acceptable for a research paper.

## Nice-to-Haves

- Report wall-clock time or inference cost (e.g., FLOPs, latency) alongside token usage to demonstrate practical efficiency gains.
- Provide a more detailed analysis of when ConciseHint fails (e.g., accuracy drops) and potential remedies.
- Explore alternative complexity indicators beyond current reasoning length (e.g., entropy of token probabilities, confidence scores).
- Evaluate on larger models (e.g., Qwen3-32B, DeepSeek-R1-67B) to test scalability.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Measure and report end-to-end inference time (or at least the number of generation calls) to validate that token reduction translates to real speedup.
- Clarify the derivation of constants in Equation 3 (1024 and 0.8) or provide empirical justification in the main text.
- Discuss potential failure modes (e.g., when the model becomes "lazy" and skips necessary reasoning) and how the adaptive mechanism prevents them.
- Add a comparison with a simple baseline that uses a fixed injection interval tuned per benchmark to better highlight the advantage of adaptivity.

## Score and Decision

**Score**: 6.5  
**Decision**: Accept

The paper presents a novel and well-motivated approach to improving reasoning efficiency, with solid empirical support across multiple models and benchmarks. The main concerns are the lack of wall-clock time measurement and the reliance on an unavailable appendix for key design justifications. These issues are addressable and do not invalidate the core contribution. The paper is likely to stimulate further work on in-reasoning intervention, a promising direction.

MY FINAL SCORE: <score>6.5</score>  
MY FINAL DECISION: <decision>Accept</decision>