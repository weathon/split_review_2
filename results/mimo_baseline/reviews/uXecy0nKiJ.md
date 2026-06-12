## Summary

This paper demonstrates that activation steering—a technique for controlling LLM behavior by adding vectors to hidden states during inference—systematically compromises model safety by breaking refusal mechanisms. Through experiments across multiple model families (Llama3, Qwen2.5, Falcon3), the authors show that even random steering vectors increase harmful compliance from 0% to 2–27%, SAE-based features show comparable or slightly worse harmful potential, and aggregating just 20 random jailbreak vectors creates a universal attack that generalizes to unseen harmful prompts.

## Strengths

- **Important and timely research question.** The paper addresses a genuine gap: while prior work focused on adversarially optimized steering vectors, the safety implications of *benign* steering (the kind used in practice) were underexplored. This is directly relevant as activation steering is increasingly deployed via public APIs (e.g., Goodfire).

- **Comprehensive cross-model evaluation.** The experiments span 8 model configurations across 4 model families (Llama3, Qwen2.5, Falcon3, FalconH1) at scales from 3B to 70B parameters, demonstrating that the vulnerability is architectural rather than model-specific. The systematic sweep across layers, coefficients, and vector types (Fig. 2) provides a thorough characterization.

- **The universal attack finding is a genuine and concerning result.** The demonstration that averaging 20 random vectors (obtained from a single prompt) creates a universal attack achieving 50%+ compliance on Llama3-70B and 63% on Falcon3-7B (Fig. 6) is a striking result. The attack requires only black-box steering access—no weights, gradients, or logits—making it practically relevant.

- **Practical case study with production API.** The Goodfire API case study (Sec. 4.3) concretely demonstrates that the vulnerability exists in deployed systems, not just in controlled experiments. The identification of "disclaimer-then-compliance" and "justification via fictional framing" failure modes adds behavioral insight.

- **Well-structured and clearly written.** The paper progresses logically from single-prompt probing to scaled evaluation to universal attack construction, with each section building on the previous findings.

## Weaknesses

### Fatal
None.

### Major

- **Effect sizes are modest for the core claim.** The headline results—17% compliance for Llama3-8B and 10% for Qwen2.5-7B with random steering—represent relatively small absolute effects. The SAE-vs-random difference is only 2-4% (Fig. 2c), which is within noise for many practical applications. The paper's framing ("systematically breaks model alignment safeguards," "compromises LLM safety") is somewhat stronger than the data warrants for the base steering results, though the universal attack results do justify stronger language.

- **Limited mechanistic analysis.** The paper acknowledges in Appendix E that the safety compromise is "not due to simple alignment with known refusal directions nor general capability degradation," but this is a critical unsolved question. Without understanding *why* steering breaks safety, it is difficult to assess the true scope of the vulnerability or develop principled mitigations. The paper essentially documents a phenomenon without explaining it, which limits its scientific contribution.

- **SAE analysis is restricted to a single model and layer.** All SAE experiments use features from Goodfire's SAE trained on layer 19 of Llama3.1-8B only. This is a significant limitation given that the random steering results show substantial variation across models and layers. The claim that "SAE features demonstrate comparable potential to random vectors" may not generalize beyond this specific configuration.

### Minor

- **The LLM-as-judge evaluation, while necessary at scale, introduces uncertainty.** The paper uses Qwen3-8B to classify 300,000 responses, and while Appendix B reportedly contains quality assessment against human annotations, the reliability of this evaluation directly affects all reported compliance rates. A small systematic bias in the judge could meaningfully shift the already-modest effect sizes.

- **The universal attack's effectiveness is highly model-dependent.** The method shows dramatic improvement on Falcon3-7B (5.7% → 63.4%) but minimal improvement on Qwen2.5-32B (9% → 9%). This variability is acknowledged but not explained, and it limits the generalizability of the "weaponization" narrative.

- **Greedy decoding may not reflect practical deployment.** Most production systems use sampling-based decoding (temperature > 0), which could either amplify or attenuate the observed effects. The paper does not explore this.

### Trivial
None.

## Nice-to-Haves

- An analysis of whether the steering-induced compliance correlates with specific token patterns or output structures (e.g., does the model produce coherent harmful content or garbled text that happens to pass the judge?)
- Exploration of whether safety classifiers or output filters can detect steering-induced jailbreaks
- A comparison of the universal attack's effectiveness against established jailbreak baselines (e.g., GCG, AutoDAN) to contextualize the practical threat level

## Novel Insights

The most novel contribution is the demonstration that the vulnerability of activation steering to safety bypass is not primarily a property of the steering vector's semantics but of the intervention itself. The fact that random vectors are nearly as effective as semantically meaningful SAE features (and that the most dangerous SAE features correspond to benign concepts like "brand identity") challenges the implicit assumption in the interpretability community that understanding *what* you're steering guarantees safe outcomes. The universal attack construction—turning many weak, prompt-specific failures into a strong, generalizable attack through simple averaging—is a genuinely clever insight that reveals how the linearity of steering vectors, typically celebrated as a feature, becomes a security liability.

## Suggestions

- The paper would benefit from a deeper investigation of the mechanism. Even a simple ablation study—e.g., measuring whether steering affects the model's representation of the refusal direction (Arditi et al., 2024) or disrupts specific attention patterns—would significantly strengthen the contribution.
- Consider reporting compliance rates broken down by response quality (coherent vs. incoherent) to ensure the results reflect genuine harmful compliance rather than steering-induced degeneration that happens to contain harmful keywords.
- The universal attack section would be strengthened by comparing against a simple baseline like "average of 20 random vectors (not filtered for jailbreaking)" to isolate the contribution of the selection step.

## Score and Decision

The paper addresses an important and underexplored question at the intersection of mechanistic interpretability and AI safety. The universal attack finding is genuinely concerning and practically relevant. However, the core steering results show modest effect sizes, the mechanistic understanding is limited, and the SAE analysis is restricted to a single configuration. The paper is a solid empirical contribution that surfaces a real safety concern, but it falls short of providing the deep understanding needed to fully assess and address the vulnerability.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <score>Accept</score>