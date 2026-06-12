## Summary

This paper investigates the safety implications of activation steering in LLMs, demonstrating that adding steering vectors—even random ones or those derived from benign SAE features—systematically compromises model alignment safeguards. The authors show that random steering can increase harmful compliance from 0% to 2-27% across models, that SAE features exhibit comparable or greater jailbreaking potential, and that averaging just 20 random vectors that jailbreak a single prompt creates a universal attack generalizing to unseen harmful requests. The work challenges the assumption that interpretable, precise control over model internals guarantees safe outcomes.

## Strengths

- **Important and timely research question**: The paper addresses a critical gap in the literature—whether benign activation steering, widely promoted as a safe and interpretable control method, can inadvertently compromise safety. This is highly relevant given the growing deployment of steering-based APIs and tools.

- **Comprehensive experimental design**: The authors systematically sweep across multiple model families (Llama-3, Qwen2.5, Falcon3, FalconH1), model sizes (3B-70B), steering depths, scaling coefficients, and vector types (random vs. SAE features). The use of 1,000 random vectors per configuration provides statistical robustness.

- **Clear and alarming findings**: The demonstration that random steering alone can induce 2-27% harmful compliance, that SAE features are comparably dangerous, and that a universal attack can be constructed from just 20 vectors without model weights or gradients, are all compelling and practically significant results.

- **Practical validation via case study**: The case study using the public Goodfire API to jailbreak a production model with a benign "brand identity" feature provides concrete, real-world evidence of the vulnerability, strengthening the paper's practical relevance.

- **Well-structured presentation**: The paper is clearly organized, with a logical flow from single-prompt probing to full-dataset evaluation to universal attack construction. Figures and tables effectively communicate key results.

## Weaknesses

### Major

- **Limited analysis of why steering compromises safety**: The paper documents the phenomenon thoroughly but provides minimal mechanistic analysis. The authors mention in passing (Section 4.1) that "preliminary analysis...suggests this safety compromise is not due to simple alignment with known refusal directions nor general capability degradation," but this analysis is relegated to an appendix (App. E) that is not included in the main text. Understanding the mechanism is crucial for developing mitigations.

- **SAE experiments limited to a single model and layer**: SAE-based steering is tested only on Llama3.1-8B at layer 19 using Goodfire's SAE. While the authors acknowledge this limitation, it significantly constrains the generalizability claims about SAE feature dangers. The paper would be stronger with SAE experiments on at least one additional model family or layer.

- **The universal attack construction is somewhat underspecified**: The authors state that 20 vectors are selected from 100-500 random trials, but do not explore how the number of aggregated vectors affects attack potency. Is 20 optimal? Would 5 or 50 work better? The sensitivity of the attack to this hyperparameter is not examined.

- **No discussion of potential mitigations or defenses**: The conclusion briefly mentions adversarial training and automated audits, but the paper provides no experimental evaluation of any defense. Given the paper's focus on safety vulnerabilities, some exploration of countermeasures would strengthen the contribution.

### Minor

- **The LLM-as-judge evaluation, while practical, has known limitations**: The authors use Qwen3-8B as the judge and report that incoherent responses are classified as SAFE, which is reasonable. However, no human validation or inter-rater agreement statistics are provided for the judge's classifications beyond a reference to Appendix B.

- **The "random direction" baseline may conflate multiple effects**: Adding random noise to activations could degrade model performance generally, not specifically compromise safety mechanisms. The paper does not fully disentangle general capability degradation from targeted safety failure.

- **Cross-category generalization analysis (Fig. 4b) is somewhat difficult to interpret**: The heatmap shows conditional probabilities, but the baseline compliance rates for each category are not clearly indicated in the same figure, making it hard to assess how much generalization exceeds chance.

### Trivial

- Figure 2's caption and table are somewhat redundant; the table could be simplified.

## Nice-to-Haves

- An ablation study varying the number of aggregated vectors in the universal attack (e.g., 5, 10, 20, 50) to show the scaling behavior.
- A comparison with other inference-time intervention methods (e.g., activation patching, representation engineering) to contextualize whether this vulnerability is unique to steering.
- A brief analysis of whether certain SAE feature categories (e.g., "brand identity") are systematically more dangerous than others, beyond the histogram in Fig. 4a.

## Novel Insights

Beyond the paper's own contributions, the most striking insight is that the very property that makes activation steering useful—its ability to linearly shift model behavior in a predictable direction—is also what makes it dangerous. The fact that averaging 20 random vectors, each individually weak and prompt-specific, produces a universal attack suggests that the safety mechanism occupies a relatively low-dimensional subspace that can be disrupted by any sufficiently large perturbation in a random direction. This implies that safety alignment may be fundamentally fragile to linear interventions, regardless of whether those interventions are semantically meaningful or random. The paper thus raises a deeper question: can any inference-time linear intervention be made safe, or is the very architecture of residual stream steering inherently at odds with robust safety guarantees?

## Suggestions

- Provide mechanistic analysis (even preliminary) in the main paper rather than relegating it to an appendix, as it is central to understanding the phenomenon.
- Add SAE experiments on at least one additional model (e.g., Qwen2.5-7B with a different SAE) to strengthen generalizability claims.
- Include a sensitivity analysis for the number of vectors used in the universal attack construction.
- Consider adding a small-scale human evaluation of the LLM judge's accuracy on a random subset of 100-200 responses.

## Score and Decision

This paper makes a clear, well-supported, and practically important contribution to understanding the safety risks of activation steering. The experimental design is thorough, the findings are consistent across multiple models, and the practical case study demonstrates real-world relevance. The main weaknesses are the limited mechanistic analysis and the restriction of SAE experiments to a single model, but these do not invalidate the core claims. The paper is likely to have significant impact on how the community thinks about the safety of interpretability-based control methods.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>