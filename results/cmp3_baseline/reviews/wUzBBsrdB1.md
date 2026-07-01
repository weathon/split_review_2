## Summary

This paper studies the role of the L0 sparsity hyperparameter in Sparse Autoencoders (SAEs) for LLM interpretability. Through toy model experiments with ground-truth features, it demonstrates that setting L0 too low causes the SAE to "cheat" by mixing correlated and anti-correlated features to improve reconstruction, while too high L0 also degrades feature monosemanticity. The authors propose a proxy metric—decoder pairwise cosine similarity—that can help identify the correct L0, and validate their findings on Gemma-2-2B and Llama-3.2-1B SAEs, showing that the metric's "elbow" aligns with peak performance on sparse probing tasks.

## Strengths

- **Important and timely question**: The paper addresses a critical hyperparameter choice in SAEs that is often treated as arbitrary. It makes a convincing case that L0 is not a free parameter and that incorrect L0 leads to corrupted features.
- **Clean toy model experiments**: The synthetic setup with known ground-truth features provides clear, interpretable evidence that low-L0 SAEs mix correlated features to game the MSE loss, and that sparsity-reconstruction tradeoff plots can be misleading.
- **Practical metric with empirical validation**: The decoder pairwise cosine similarity (c_dec) is simple to compute and correlates well with ground-truth L0 in toy models and with downstream probing performance in LLMs. The experiments span BatchTopK and JumpReLU SAEs and two different LLMs.
- **Clear practical implications**: The paper convincingly argues that most commonly used open-source SAEs likely have L0 set too low, which is directly actionable for practitioners.

## Weaknesses

### Fatal
None.

### Major
(**M1**) The c_dec metric is not a perfect guide: the paper acknowledges that it can be nearly flat over a range of L0 values (e.g., Gemma-2-2B layer 5). The method still requires sweeping L0 and visually identifying an "elbow", which limits its practical automation. A more principled or automatic selection procedure would strengthen the contribution.

(**M2**) The toy model assumes perfectly orthogonal features and simple Bernoulli correlations. Real LLM features may not satisfy the linear representation hypothesis perfectly, may have non-linear interactions, and may exhibit more complex correlation structures. The paper does not discuss how deviations from these assumptions might affect the conclusions or the c_dec metric.

### Minor
(**m1**) The paper claims that "most commonly used SAEs have an L0 that is too low" but only supports this with a cursory reference to Neuronpedia in the appendix. A more systematic survey (e.g., tabulating L0 values from popular open-source SAEs) would strengthen this claim.

(**m2**) The explanation for why JumpReLU SAEs behave better at high L0 (ability to adjust threshold per latent) is plausible but not deeply investigated. The paper could have included additional analysis (e.g., comparing latent L0 distributions between BatchTopK and JumpReLU).

### Trivial
None.

## Nice-to-Haves

- Automating the selection of L0 from the c_dec curve (e.g., detecting the elbow algorithmically) would make the method more practical.
- Extending the toy model to include non-orthogonal features or non-linear generative processes would test the robustness of the findings.

## Novel Insights

The central insight—that reconstruction quality alone cannot be trusted when L0 is too low because the SAE can exploit feature correlations to cheat—is both novel and important. It explains prior observations that low-L0 SAEs underperform on downstream tasks, and it directly challenges the common practice of using sparsity-reconstruction tradeoffs as the primary evaluation tool for SAE architectures. The paper also shows that the problem is asymmetric: low L0 harms nearly all latents, while high L0 can still preserve many correct latents.

## Suggestions

- Include a quantitative analysis of L0 values from a broader set of publicly available SAEs to substantiate the claim that most SAEs have too low L0.
- Provide guidance on how to select L0 in practice using c_dec, perhaps by suggesting a heuristic (e.g., choose L0 at the point where c_dec first reaches a minimum or an elbow).

## Score and Decision

Score: 8

Decision: Accept

The paper presents a clean, well-motivated, and empirically sound study of a previously underappreciated hyperparameter in SAE training. The contribution is significant for the interpretability community and directly actionable for practitioners. The weaknesses (lack of automatic L0 selection, limited realism of toy models) are acknowledged by the authors and do not undermine the core claims.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>