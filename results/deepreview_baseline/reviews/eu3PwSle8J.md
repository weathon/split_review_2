## Summary

This paper proposes Augmented Intermediate Representations (AIR), a defense against indirect prompt injection attacks in LLMs. The key idea is to inject instruction hierarchy (IH) signals—which encode the privilege level of each token—not just at the input layer (as done by prior work using delimiters or segment embeddings) but at every decoder layer via small trainable embedding tables. Experiments across three model sizes (3B–8B), two training methods (SFT, DPO), and multiple attack types show that AIR consistently reduces attack success rates by 1.6× to 9.2× on gradient-based attacks compared to prior IH injection methods, with negligible utility degradation.

## Strengths

- **Clear identification of a limitation in prior defenses.** The paper provides empirical evidence (cosine similarity analysis across layers) that IH signals injected only at the input layer degrade as they propagate through the network, motivating the need for per-layer injection.
- **Simple and practical method with negligible overhead.** AIR adds only ~0.005% extra parameters (e.g., 0.4M for Llama-3.1-8B) and requires no architectural changes beyond adding per-layer embedding tables. The overhead during inference is minimal.
- **Comprehensive and well-designed evaluation.** The paper evaluates three base models (Llama-3.2-3B, Qwen2.5-7B, Llama-3.1-8B), two adversarial training techniques (SFT, DPO), multiple static and gradient-based attacks (GCG, Astra), and two evaluation datasets (AlpacaFarm, SEP). Results consistently show AIR outperforming delimiters and ISE, especially on strong gradient-based attacks.
- **Strong empirical results.** AIR achieves 1.6× to 9.2× reduction in ASR on GCG attacks compared to the next best defense, and up to 145× reduction on Astra attacks for SFT models. The utility (AlpacaEval win rate, SEP utility) remains comparable to or better than the non-adversarial baseline.
- **Conceptual connection to positional embedding research.** The paper draws an interesting parallel to RoPE, which injects positional information throughout layers rather than only at the input, providing a principled motivation for the approach.

## Weaknesses

### Major

- **Lack of ablation to isolate the effect of per-layer injection from extra parameters.** AIR adds trainable parameters at each layer. The paper does not compare against a baseline that adds the same number of per-layer parameters but without IH information (e.g., random or constant embeddings). Without this control, it is unclear whether the improvement comes from the IH signal being present at every layer or simply from the additional model capacity.
- **Cosine similarity analysis for delimiters is questionable.** For the delimiter method, tokens with different privilege levels are different token types (special tokens). Comparing the cosine similarity of their hidden representations may not be meaningful—the high similarity (1.0 across all layers) likely reflects that the special tokens themselves have similar representations, not that the IH signal is lost. The paper should clarify what exactly is being compared and whether the analysis is valid for delimiters.
- **Limited evaluation against adaptive attacks.** The gradient-based attacks (GCG, Astra) are white-box but optimize only over input tokens. An attacker aware of AIR could potentially design an attack that explicitly tries to neutralize the per-layer IH embeddings (e.g., by optimizing a loss that encourages the model to ignore the privilege signal). The paper does not discuss or evaluate such adaptive attacks, which is a significant gap for a security paper.
- **Robustness evaluation uses only one target phrase.** All attacks aim to make the model output exactly "hacked!". This is a simple, short target. The results may not generalize to more complex adversarial instructions (e.g., multi-sentence commands, data exfiltration). The paper should justify why this single target is sufficient or evaluate with more diverse targets.

### Minor

- **The hypothesis that input-level IH signals degrade is plausible but not rigorously proven.** The cosine similarity analysis shows that representations of tokens with different privilege levels become more similar in deeper layers for ISE and delimiters. However, similarity does not directly measure the model's ability to distinguish privilege levels—the model could still use attention patterns or other features. A more direct test (e.g., probing classifier accuracy on privilege level from hidden states) would strengthen the claim.
- **Utility sometimes improves over the non-adversarial baseline.** In several settings (e.g., Llama-3.2-3B DPO, Qwen-2.5-7B SFT), AIR achieves higher win rates than the model trained without any IH signal. The paper attributes this to "no significant degradation" but does not explain why utility can increase. This could be due to the extra parameters or training dynamics, and should be discussed.
- **The paper does not compare against the original implementations of prior defenses.** The delimiters and ISE baselines are re-implemented following the general recipe. While this is reasonable for a fair comparison, the paper could strengthen its claims by also evaluating against the exact models from prior work (e.g., SecAlign's released checkpoints) if available.

## Nice-to-Haves

- An ablation study comparing AIR against a baseline with per-layer random embeddings (same number of parameters) to isolate the effect of the IH signal.
- Evaluation against adaptive attacks that are aware of the per-layer IH injection (e.g., optimizing a prefix that minimizes the model's reliance on the privilege embeddings).
- Robustness evaluation with multiple target phrases of varying length and complexity.
- A probing experiment to directly measure how well the model can decode privilege level from hidden representations at each layer.

## Novel Insights

The paper's core insight—that injecting instruction hierarchy signals at every decoder layer (analogous to how RoPE injects positional information throughout the network) yields substantially better robustness than input-only injection—is both novel and well-supported by the experiments. This connection to positional embedding research provides a principled lens for understanding why prior defenses are limited and offers a clear design principle for future work on security in LLMs.

## Suggestions

1. Add an ablation with per-layer random embeddings (same dimensionality, trainable) to confirm that the improvement is due to the IH signal, not just extra parameters.
2. Clarify the cosine similarity analysis: specify exactly which token representations are compared for each method, and consider adding a probing classifier experiment to directly measure privilege-level separability.
3. Evaluate against an adaptive attack that optimizes a prefix to minimize the influence of the per-layer IH embeddings (e.g., by adding a term to the attack loss that encourages the model to treat all tokens uniformly).
4. Include robustness results with at least one additional target phrase (e.g., a longer instruction) to demonstrate generality.

## Score and Decision

The paper makes a clear, well-motivated contribution to an important security problem. The proposed method is simple, practical, and consistently outperforms prior approaches across a thorough set of experiments. The main weaknesses are the missing ablation to separate the effect of per-layer injection from extra parameters and the limited evaluation against adaptive attacks. These are significant but not fatal—the core claim is well supported, and the paper provides a strong foundation for future work. I recommend acceptance.

MY FINAL SCORE: 7.0</score>
MY FINAL DECISION: Accept</decision>