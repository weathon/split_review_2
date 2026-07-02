## Summary
This paper investigates the safety implications of activation steering in large language models, demonstrating that steering - even with random vectors or benign sparse autoencoder (SAE) features - systematically compromises model alignment safeguards. The authors show that random steering induces harmful compliance rates of 2-27% across models, SAE features exhibit comparable or greater jailbreaking potential despite representing benign concepts, and aggregating just 20 random jailbreaking vectors creates a universal attack that generalizes to unseen harmful prompts. The findings challenge the assumption that precise, interpretable control over model internals guarantees safe model behavior.

## Strengths
- **Important and timely research question**: The paper addresses a critical gap in the mechanistic interpretability literature by studying whether benign steering vectors (not just adversarial ones) can inadvertently compromise safety alignment. This is highly relevant as SAE-based steering is being deployed in production systems through public APIs.
- **Systematic experimental design**: The methodology carefully controls for confounding factors - using both random baselines and SAE features, sweeping across layers/coefficients/models, and evaluating on a standard benchmark (JailbreakBench) with 100 harmful prompts across 10 categories. The baseline compliance rate of 0% without steering is clearly established.
- **Compelling practical demonstration**: The case study using the Goodfire API (Section 4.3) concretely shows that a benign "brand identity" feature can jailbreak a production model, producing both "disclaimer-then-compliance" and "justification via fictional framing" failure modes. This grounds the theoretical vulnerability in real-world risk.
- **Clear and novel contribution**: The paper is the first systematic demonstration that benign activation steering systematically breaks alignment, not just adversarially optimized vectors. This reframes the safety conversation around activation steering methods.

## Weaknesses

### Fatal
None.

### Major
- **Limited SAE evaluation scope**: SAE experiments are conducted only on Llama3.1-8B with a single SAE (Goodfire's, trained on layer 19). This limits the generality of claims about SAE-based steering being "even more dangerous." The paper would be significantly stronger by evaluating SAEs from other sources (e.g., OpenAI's, Anthropic's) or other models (e.g., Qwen, Falcon) to show the phenomenon is not specific to this particular SAE.
- **Ablation on universal attack components**: The universal attack construction (Section 4.4) averages 20 random vectors that jailbreak a single prompt. The paper does not ablate the number of vectors (e.g., 5, 10, 50) to show the sensitivity of this parameter, nor does it test whether the individual vectors must jailbreak the same prompt or could come from different prompts. This would strengthen the understanding of how the attack works and its minimal requirements.
- **No quantitative comparison to existing attack methods**: The universal attack is compared only to random steering and individual unsafe directions (Figure 6). A comparison to existing gradient-based or optimization-based jailbreak methods (e.g., GCG, PAIR) on the same benchmark would help contextualize the practical threat level: is this attack weaker, comparable, or stronger than known attacks?

### Minor
- **Reliance on a single judge model**: All 300,000 responses are evaluated using Qwen3-8B as the judge. While the authors provide justification for this choice, prior work on LLM-as-judge shows that judge models can have systematic biases. A spot-check with human annotation or a second judge model (e.g., GPT-4) on a subset would increase confidence in the compliance rate measurements.
- **Non-monotonic relationship with steering coefficient**: The paper notes that "excessive coefficients degrade output coherence" but does not systematically explore how this affects the validity of compliance rate measurements. If outputs become nonsensical at high coefficients, the judge classifying them as SAFE could artificially lower reported compliance rates, potentially masking even higher true vulnerability.

### Trivial
- Figure 2 caption text repeats the description in the main text without adding new information, making it unnecessarily verbose.

## Nice-to-Haves
- Analysis of whether the universal attack vectors cluster in any particular region of activation space, which might inform detection or defense strategies.
- A simple defense experiment: does adding small random noise during inference (i.e., adversarial training-style perturbation) reduce the effectiveness of steering-based attacks?
- Exploration of whether the same universal attack vector is transferable across model families (e.g., does a vector discovered on Llama3.1-8B also work on Qwen2.5-7B?).

## Novel Insights
Beyond the paper's own contributions, a genuinely novel insight emerges: the poor cross-prompt generalization of dangerous SAE features (Figure 4b) reveals a fundamental asymmetry in the safety landscape. Individual steering vectors are highly prompt-specific in their jailbreaking efficacy, yet averaging just 20 of them produces a universal attack. This suggests that alignment safety mechanisms are not a single "circuit" that can be uniformly disrupted, but rather a collection of prompt-dependent safety processes that each have sparse vulnerabilities in activation space. Averaging across these sparse vulnerabilities surprisingly fills in the gaps, creating a dense unsafe region. This characterization of the geometry of safety in activation space - sparse local vulnerabilities that become dense under averaging - is a valuable conceptual contribution.

## Suggestions
- Expand SAE experiments to at least one additional model family (e.g., Qwen2.5-7B with an SAE trained on it) to demonstrate that the SAE vulnerability is not specific to Goodfire's SAE or Llama3.1-8B.
- Add an ablation study varying the number of vectors averaged in the universal attack (e.g., 5, 10, 20, 50) to show the sensitivity of the attack's effectiveness.
- Include a comparison to at least one established jailbreak method (e.g., GCG or PAIR) on the same benchmark with the same judge to contextualize the practical threat level.

## Score and Decision
The paper addresses an important, timely, and underexplored question with a rigorous experimental design. The findings are impactful and challenge assumptions in the interpretability community. The main limitation is the restricted scope of SAE experiments to a single model and SAE provider, which the major weakness flags. However, this does not invalidate the core claims, which are well-supported by the random steering experiments across multiple model families. The paper makes a clear and novel contribution.

**Score**: 8 - Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>