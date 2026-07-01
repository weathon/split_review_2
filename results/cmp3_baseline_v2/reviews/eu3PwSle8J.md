## Summary

This paper addresses indirect prompt injection attacks in LLMs by improving how instruction hierarchy (IH) signals are injected into the model. The authors identify that prior methods inject IH signals only at the input layer, causing the signal to degrade through deeper layers. They propose Augmented Intermediate Representations (AIR), which injects trainable IH embeddings at every decoder layer. Experiments across multiple models (3B–8B) and training methods (SFT, DPO) show that AIR reduces attack success rates by 1.6× to 9.2× against gradient-based attacks compared to prior methods, with minimal utility degradation.

## Strengths

- **Clear problem identification and motivation**: The paper provides empirical evidence (Figure 3) that IH signals from input-only injection methods become less distinguishable as they propagate through layers, directly motivating the need for layer-wise injection.
- **Simple yet effective solution**: AIR adds only a small number of parameters (0.005% increase for Llama-3.1-8B) and requires negligible inference overhead, making it practical for deployment.
- **Comprehensive evaluation**: The experiments cover three model sizes, two training paradigms (SFT and DPO), multiple attack types (static and gradient-based), and two evaluation datasets (AlpacaFarm and SEP). The consistent improvement across all settings is convincing.
- **Strong empirical results**: Against gradient-based attacks (GCG, Astra), AIR consistently achieves the lowest ASR, often by a large margin (e.g., 145× lower for Astra on SFT models). The utility impact is minimal (<2% degradation in most cases).

## Weaknesses

### Fatal
None.

### Major
- **Causal link between signal degradation and vulnerability is not directly established**: The paper shows that cosine similarity between privilege-level representations increases in deeper layers for input-only methods, and that AIR maintains lower similarity. While this correlation is plausible, the paper does not provide a causal analysis (e.g., ablation where IH is injected only at certain layers) to confirm that the degradation is the primary reason for higher ASR. The method’s success provides indirect evidence, but a more rigorous demonstration would strengthen the claim.

### Minor
- **Utility evaluation is limited to two datasets**: The paper measures utility only on AlpacaFarm and SEP. While these are standard for instruction-following and instruction-data separation, the claim that AIR “does not significantly degrade the model’s utility” would be stronger with additional benchmarks (e.g., MMLU, GSM8K, or general language understanding tasks) to rule out unintended side effects on broader capabilities.
- **Limited model diversity**: The three models (Llama-3.2-3B, Qwen-2.5-7B, Llama-3.1-8B) are all from the same architectural family (decoder-only transformers). Testing on models with different architectures (e.g., encoder-decoder, mixture-of-experts) would increase generalizability.

### Trivial
- The paper reports “1.6× to 9.2× reduction in ASR” but the exact factor varies across settings; this is a minor imprecision that does not affect the overall conclusion.

## Nice-to-Haves

- An ablation study injecting IH signals at a subset of layers (e.g., only first half, only last half) to directly test the hypothesis that deeper-layer injection is critical.
- Evaluation against adaptive attacks where the adversary is aware of the defense mechanism (e.g., optimizing the adversarial prefix to also fool the layer-wise IH embeddings).
- Analysis of whether AIR provides benefits against other security threats such as jailbreak attacks or data poisoning.

## Novel Insights

Beyond the paper’s own contributions, the analogy to positional embeddings (RoPE) is a valuable insight: just as injecting positional information at every layer (via rotary attention) improved model performance over input-only positional encodings, injecting privilege information at every layer improves security. This connection suggests a broader design principle for encoding structural information in transformers.

## Suggestions

- To strengthen the causal claim, consider an experiment where IH signals are injected only at a subset of layers (e.g., layers 0–5, layers 10–15, all layers) and compare ASR. This would directly test whether the number of layers with IH injection correlates with robustness.
- Add a few standard NLP benchmarks (e.g., MMLU, HellaSwag) to the utility evaluation to reassure readers that AIR does not harm general model capabilities.

## Score and Decision

The paper makes a clear, well-motivated contribution to an important security problem. The proposed method is simple, efficient, and consistently outperforms prior defenses across a thorough experimental setup. The weaknesses are minor and do not undermine the core claims. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>