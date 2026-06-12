## Summary

This paper proposes Augmented Intermediate Representations (AIR), a method for defending LLMs against indirect prompt injection attacks by injecting instruction hierarchy (IH) signals into every decoder layer rather than only at the input layer. The key observation is that existing defenses (delimiters, instruction segment embeddings) suffer from signal degradation as representations propagate through layers, and AIR addresses this by adding layer-specific trainable embedding tables indexed by privilege level. Experiments across three models (3B–8B), two training methods (SFT, DPO), and multiple attack types demonstrate 1.6×–9.2× reductions in attack success rate on gradient-based attacks with minimal utility loss.

## Strengths

- **Well-motivated problem identification with direct evidence.** The paper identifies a concrete limitation in existing IH defenses and supports it with Figure 3, which shows cosine similarity between different-privilege representations increasing (converging) through decoder layers for Delim and ISE, while AIR maintains better separation. This is a clear, falsifiable claim backed by empirical measurement.

- **Simple, elegant, and practical method.** AIR adds a trainable embedding table per layer (K entries × hidden_dim), resulting in only 0.005% parameter overhead for an 8B model. The analogy to the evolution from input-only sinusoidal embeddings to layer-wise RoPE is well-articulated and provides strong conceptual grounding.

- **Comprehensive and rigorous experimental evaluation.** The paper evaluates a full matrix of 3 IH injection mechanisms × 2 training methods × 3 model sizes, tested against 4 static attacks and 2 recent gradient-based attacks (momentum-GCG and Astra) across 2 evaluation datasets (AlpacaFarm, SEP). This is thorough and allows readers to draw nuanced conclusions.

- **Consistently strong empirical results.** AIR achieves the lowest ASR across nearly all gradient-based attack settings. For example, on Qwen-2.5-7B with DPO, GCG ASR drops from 32% (Delim) to 1.6% (AIR), and Astra ASR drops from 19.9% to 0.9%. These improvements are large and consistent across models and training methods.

- **Favorable utility-robustness tradeoff.** Figure 6 shows AIR maintains win rates comparable to or exceeding the non-adversarially trained baseline, and Figure 8 demonstrates the best utility × separation scores for DPO-trained models.

## Weaknesses

### Fatal
None.

### Major

- **Limited mechanistic analysis of why AIR works.** While the cosine similarity analysis is a good start, the paper lacks deeper investigation. Key unanswered questions include: (a) Do the learned embeddings at different layers encode qualitatively different information? (b) Is there a point of diminishing returns—do early layers matter more than later ones? (c) An ablation varying which layers receive IH injection (e.g., first N layers only, last N layers only, every other layer) would substantially strengthen the paper by clarifying the mechanism and guiding future work.

- **Asymmetric attack evaluation methodology.** Gradient-based attacks use 50 optimization steps for SFT models but 200 for DPO models. This asymmetry complicates direct comparison and raises the question of whether SFT models' ASR would increase substantially with more steps. The paper should justify this choice and ideally show convergence curves or results with matched step counts.

### Minor

- **Narrow gradient-based attack configuration.** All gradient-based attacks use 100-token adversarial prefixes. It would be informative to understand how the AIR advantage scales with different prefix lengths and attack budgets, as this affects practical relevance.

- **The privilege level design (P0 = system/user, P1 = data, P2 = response) is used without ablation.** The paper does not discuss sensitivity to the number of privilege levels or alternative hierarchies, which would help practitioners.

- **No evaluation against adaptive attacks.** An attacker aware of the AIR mechanism might craft attacks that exploit the layer-wise injection pattern. While this is a common limitation in defense papers, acknowledging it and ideally providing preliminary adaptive attack results would strengthen the work.

### Trivial
Some figure captions are duplicated in the extracted text (likely a parser artifact).

## Nice-to-Haves

- An ablation study on which layers benefit most from IH injection, potentially revealing that only a subset of layers is critical.
- Visualization or analysis of the learned embedding vectors across layers to understand what the model learns at each stage.
- Evaluation with matched optimization steps across SFT and DPO for cleaner comparison.
- Discussion of potential failure modes and limitations of the approach.

## Novel Insights

The paper's core insight—that IH signals degrade through decoder layers and should be re-injected at each layer—is genuinely novel and well-supported empirically. The connection to the evolution of positional embeddings (from input-only sinusoidal to layer-wise RoPE) provides a compelling architectural principle: critical structural information should be distributed across all processing stages, not confined to the input. The magnitude of the improvement (up to 9.2× ASR reduction) from such a simple modification is surprising and suggests that the information bottleneck at the input layer is a more significant limitation than previously recognized. This finding likely generalizes beyond prompt injection defense to other settings where auxiliary structural signals must be preserved through deep networks.

## Suggestions

- Add an ablation study varying which layers receive IH injection to understand the contribution of early vs. late layer injection and to potentially reduce overhead further.
- Justify the asymmetric optimization steps (50 for SFT, 200 for DPO) and show convergence behavior for both.
- Analyze the learned per-layer embeddings—e.g., are they similar across layers or do they learn layer-specific patterns?
- Consider a brief adaptive attack evaluation where the attacker has knowledge of the AIR mechanism.

## Score and Decision

The paper presents a clear, well-motivated contribution with strong and consistent empirical results across a comprehensive experimental matrix. The core idea is simple but effective, and the practical implications for LLM security are significant. The main weakness is the lack of deeper mechanistic analysis and some evaluation methodology concerns, but these do not invalidate the contribution. The paper would benefit from ablation studies and more analysis, but the empirical evidence is convincing enough to warrant acceptance.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>