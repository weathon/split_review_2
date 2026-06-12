## Summary

This paper investigates the effect of the L0 hyperparameter (average number of active features per token) in sparse autoencoders (SAEs) for LLM interpretability. Using toy models with known ground-truth features and experiments on Gemma-2-2b and Llama-3.2-1b, the authors show that setting L0 incorrectly—either too low or too high—causes the SAE to mix correlated features, producing polysemantic latents. They demonstrate that the common sparsity–reconstruction tradeoff is misleading because a ground-truth SAE can have worse reconstruction than an incorrect SAE at low L0. They propose a proxy metric, decoder pairwise cosine similarity (c_dec), which is minimized near the correct L0 and correlates with peak sparse probing performance. The paper argues that most currently used SAEs have L0 set too low.

## Strengths

- **Important and timely research question.** The paper addresses a critical hyperparameter choice in SAE training that has been largely overlooked. Showing that L0 must be set correctly for SAEs to learn correct features has direct implications for the interpretability community.
- **Clear toy model experiments with ground truth.** The controlled setting with known features convincingly demonstrates the mechanism of feature mixing at incorrect L0, and that MSE loss actively incentivizes incorrect solutions. The sparsity–reconstruction tradeoff plot (Figure 4) is a particularly striking illustration of the problem.
- **Validation on real LLMs.** The authors train SAEs on two different LLMs (Gemma-2-2b and Llama-3.2-1b) and show that the c_dec metric aligns with sparse probing performance, providing practical evidence that the phenomenon extends beyond toy models.
- **Practical diagnostic metric.** The proposed c_dec metric is simple to compute and provides a useful heuristic for identifying when L0 is too low, even if it is not a perfect guide. The paper also compares BatchTopK and JumpReLU SAEs, showing interesting differences at high L0.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **c_dec metric is not a complete solution.** The metric sometimes has a flat region over a wide range of L0 (e.g., Gemma-2-2b layer 5), making it difficult to pinpoint a single optimal L0. The paper acknowledges this but does not provide a principled way to resolve the ambiguity beyond using the "elbow" before the low-L0 jump.
- **Limited LLM evaluation.** The LLM experiments are conducted on only two models and a single layer per model (layer 5 for Gemma-2-2b, layer 7 for Llama-3.2-1b, plus layer 12 for Gemma-2-2b). The generalizability to other layers, larger models, and different training distributions is not established.
- **Claim about "most commonly used SAEs" is weakly supported.** The paper cites a "cursory search of open source SAEs on Neuronpedia" in Appendix A.13, but no systematic analysis is presented. This claim is not central to the paper's core contribution, but it is stated in the abstract and discussion without strong evidence.

### Trivial
- The paper uses "L0" and "L0" interchangeably; the notation is clear but could be standardized.

## Nice-to-Haves
- A method to automatically tune L0 during training (e.g., by incorporating c_dec or a related term into the loss) would greatly increase practical impact. The paper briefly mentions this as future work.
- More analysis of why JumpReLU SAEs perform better at high L0 than BatchTopK SAEs, and whether the per-latent threshold adaptation is the key factor.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the sparsity–reconstruction tradeoff, which is the standard way to evaluate SAEs, can be actively misleading: a ground-truth SAE can be *worse* at reconstruction than a cheating SAE that mixes correlated features. This challenges a fundamental assumption in the field and suggests that reconstruction quality alone is insufficient to judge SAE quality. The paper also provides a concrete mechanism (feature hedging due to insufficient L0) that explains why low-L0 SAEs underperform on downstream tasks, linking the toy model behavior to real LLM observations.

## Suggestions
- Provide a more systematic survey of L0 values used in existing open-source SAEs to substantiate the claim that most are too low.
- Test the c_dec metric on additional layers and models (e.g., larger models like Gemma-2-9b or Llama-3-8b) to assess generalizability.
- Investigate whether the c_dec metric can be used as a regularizer during training to automatically find a good L0, rather than requiring a sweep.

## Score and Decision

**Score:** 8  
**Decision:** Accept

The paper makes a significant and well-supported contribution to the SAE interpretability literature. The core finding—that L0 must be set correctly and that the sparsity–reconstruction tradeoff is misleading—is novel and important. The experiments are thorough, the toy model analysis is convincing, and the LLM validation provides practical relevance. The minor weaknesses (limited scope of LLM experiments, imperfect metric) do not undermine the main claims and are appropriately acknowledged. This work will likely influence how SAEs are trained and evaluated in the future.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>