##Summary

This paper revisits the idea of using an off-the-shelf LLM to detect and remove prompt injection attacks. While prior work (using older, weaker LLMs) found this approach ineffective, the authors show that with modern LLMs possessing strong reasoning capabilities (e.g., GPT-4o, GPT-4.1), the method achieves very low false positive and false negative rates (below 1% on AgentDojo) and reduces attack success rates from 54.5% to near zero. The paper proposes PromptArmor, a modular guardrail that detects injected prompts and sanitizes the input via fuzzy matching, and provides extensive evaluations across three benchmarks, comparisons with existing defenses, and ablation studies on prompting strategies, model size, reasoning, and adaptive attacks.

## Strengths

- **Clear and well-motivated problem.** The paper addresses a timely and important security concern for LLM agents, and the motivation for revisiting a simple baseline in light of improved LLM reasoning is compelling.
- **Thorough and rigorous evaluation.** The experiments cover three diverse benchmarks (AgentDojo, Open Prompt Injection, TensorTrust), compare against seven representative baselines from different defense categories, and include ablation studies on prompting strategies, model size/reasoning, data contamination, and adaptive attacks. The results consistently support the main claims.
- **Strong empirical results.** PromptArmor with GPT-4.1 achieves FPR 0.56% and FNR 0.13% on AgentDojo, and reduces ASR to 0.00%. These results convincingly demonstrate that the previously dismissed approach is now highly effective.
- **Practical insights.** The study of model size and reasoning (using Qwen3 models) provides useful guidance for practitioners: sufficient model capacity (≥32B) is the primary factor, and reasoning helps but is not sufficient for very small models.
- **Reproducibility focus.** The paper provides detailed experimental settings, model checkpoints, system prompts, and fuzzy matching code, supporting reproducibility.

## Weaknesses

### Fatal
None.

### Major
- **Limited adaptive attack evaluation.** The adaptive attack evaluation uses only one automated red-teaming method (AgentVigil). While the results show robustness, a more diverse set of adaptive attacks (e.g., manually crafted attacks targeting the guardrail’s detection logic, or attacks that obfuscate the injection to evade the guardrail) would strengthen the claim of robustness. The paper’s conclusion that PromptArmor is “robust against adaptive attacks” is somewhat overstated given this limitation.

### Minor
- **Practical cost and latency considerations are not discussed.** PromptArmor requires an additional LLM call (to the guardrail) for every data sample. The paper does not discuss the computational cost, latency overhead, or API pricing implications, which are important for real-world deployment. This does not invalidate the results but limits the practical guidance.
- **Fuzzy matching removal may be fragile.** The paper uses a simple fuzzy matching (regex with arbitrary characters between words) to remove the extracted injection. If the guardrail LLM extracts a slightly different phrasing (e.g., paraphrased injection), the removal might fail. The low FNR suggests this is not a major issue in practice, but the paper does not analyze failure cases or discuss robustness of the removal step.
- **The paper claims “essential baseline” but the concept is not novel.** The contribution is primarily empirical validation rather than a new algorithmic idea. This is acceptable for a baseline paper, but the novelty is limited.

### Trivial
None.

## Nice-to-Haves

- A discussion of the cost/latency trade-off and potential optimizations (e.g., using a smaller guardrail model when resources are constrained, or caching).
- An analysis of cases where the guardrail LLM fails (e.g., qualitative examples of false negatives) to understand the limitations.
- Evaluation on a wider range of guardrail LLMs, including other strong models (e.g., Claude, Gemini) to demonstrate generality.

## Novel Insights

None beyond the paper’s own contributions. The key insight is that the effectiveness of prompting-based prompt injection defense is not inherently limited, but was previously masked by the weak reasoning capabilities of older LLMs. The paper provides a clear empirical demonstration of this shift and offers practical guidance on model size and reasoning requirements.

## Suggestions

- Expand the adaptive attack evaluation to include manually crafted attacks or multiple red-teaming methods to strengthen the robustness claim.
- Add a brief discussion of the computational overhead and potential deployment strategies (e.g., batching, using a cheaper model for initial screening).
- Consider analyzing the failure cases of the fuzzy matching removal to understand its limitations and propose improvements.

## Score and Decision

**Score:** 6  
**Decision:** Accept

The paper is a well-executed empirical study that convincingly demonstrates that a simple, previously dismissed baseline is now highly effective with modern LLMs. The evaluation is thorough, the results are strong, and the paper provides useful insights for practitioners. The main limitation is the narrow adaptive attack evaluation, but this does not undermine the core contribution. The paper is a valuable addition to the literature on prompt injection defenses and will serve as an important baseline for future work.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>