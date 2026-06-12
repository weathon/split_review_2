## Summary

This paper proves that decoder-only Transformer language models are almost surely injective—different prompts map to distinct last-token hidden representations—under standard initialization and training. The authors provide rigorous mathematical proofs using real-analyticity arguments, confirm the absence of collisions empirically across billions of comparisons on six models, and introduce SIFT, an algorithm that provably recovers the exact input text from hidden activations in linear time. The work establishes injectivity as a fundamental structural property of Transformers with direct implications for interpretability, transparency, and privacy.

## Strengths

- **Novel theoretical contribution**: The paper provides rigorous mathematical proofs that decoder-only Transformers are almost surely injective, challenging the common intuition that non-linearities and normalization make representations lossy. The use of real-analyticity to establish measure-zero collision sets is elegant and technically sound.

- **Strong empirical validation**: The collision search experiments are extensive (billions of pairwise comparisons across six models), and the results consistently show no collisions with large margins. The experiments across different model families (GPT-2, Gemma-3, Llama-3.1, Mistral, Phi-4), sizes (33M to 70B), and quantization levels (FP4, INT8, FP32) demonstrate robustness.

- **Practical algorithmic contribution**: SIFT provides the first provable exact inversion algorithm with linear-time guarantees, and the empirical results show it works efficiently in practice (28 seconds average for 20-token prompts). The comparison against baselines (HARDPROMPTS, brute-force) clearly demonstrates the advantage.

- **Clear significance**: The paper identifies important practical implications for privacy and data protection, showing that hidden states are lossless encodings of user input and should be treated accordingly under regulatory frameworks.

## Weaknesses

### Fatal
None.

### Major

- **The training preservation proof (Theorem 2.3) has a critical gap**: The argument that gradient descent preserves absolute continuity relies on the Jacobian determinant of the update map being non-zero almost everywhere. However, the update map is θ - η∇L(θ), and its Jacobian is I - η∇²L(θ). The claim that det(I - η∇²L(θ)) is not identically zero is not adequately justified. The Hessian of a deep Transformer loss is highly degenerate (many zero eigenvalues due to overparameterization), and it is entirely possible that det(I - η∇²L(θ)) = 0 for all θ in practice. The sketch mentions "evaluating at a simple parameter setting" but this is not provided in the main text, and the referenced appendix is stripped. This is a serious gap in the core theoretical claim.

- **The practical relevance of the threat model is unclear**: The algorithm assumes access to all per-position hidden states at a given layer. In realistic deployment scenarios (API access, shared inference), attackers typically only get the final logits or next-token probabilities, not intermediate hidden states. The paper acknowledges this but does not address how to bridge this gap, significantly limiting the practical impact of SIFT.

- **The comparison with prior inversion work is misleading**: The paper dismisses prior work (Morris et al., Nazir et al.) as "complementary but not directly comparable" because they use different settings. However, these works address the more realistic black-box setting. The paper should either provide a fair comparison in a common setting or be more upfront about the limitations of their threat model.

### Minor

- **The proof sketch for Theorem 2.2 relies on constructing a parameter setting where two prompts differ, but this construction assumes the ability to "freeze the network" or "set one attention head" in specific ways. It is not obvious that such parameter settings exist within the standard Transformer parameterization without violating architectural constraints (e.g., attention weights must sum to 1). The full proof in the appendix might address this, but the sketch is insufficient.**

- **The empirical collision search uses 100k prompts, which is a tiny fraction of the possible prompt space (vocabulary^K). While the theoretical guarantee covers all prompts, the empirical validation is necessarily limited. The paper should acknowledge this limitation more explicitly.**

- **The inversion experiments only test on 100 prompts (20 tokens each) for GPT-2 Small, and 50 prompts (10 tokens each) for quantized models. These are small-scale tests. The paper would benefit from larger-scale inversion experiments.**

### Trivial
None.

## Nice-to-Haves

- An analysis of how the minimum pairwise distance scales with vocabulary size and embedding dimension would strengthen the theoretical understanding.
- A discussion of whether injectivity holds for encoder-decoder architectures or non-causal models would broaden the contribution.
- An investigation of whether SIFT can be extended to work with only the final logits (the more realistic threat model) would significantly increase practical impact.

## Novel Insights

The paper's key insight is that viewing Transformers as maps from discrete sequences to continuous representations, rather than as maps within the embedding space, fundamentally changes the injectivity analysis. While individual components (LayerNorm, attention) are non-injective as functions on ℝ^d, the composition of these components with the discrete embedding lookup creates a map that is almost surely injective. This reconciles the apparent contradiction between the "lossy" nature of Transformer components and the empirical observation that representations preserve input information. The real-analyticity framework provides a clean mathematical tool for analyzing such properties, and the extension to training preservation (though the proof has gaps) represents a novel approach to understanding how architectural properties persist through optimization.

## Suggestions

- **Fix the training preservation proof**: Provide a rigorous argument that the Jacobian determinant of the GD update map is not identically zero, or relax the claim to hold only under additional assumptions (e.g., non-degenerate Hessian, small enough step sizes). Alternatively, provide empirical evidence that training does not create collisions by checking injectivity before and after training on real models.

- **Clarify the practical setting**: Be more explicit about which deployment scenarios allow access to per-position hidden states (e.g., leaked KV-cache, shared inference pipelines) and which do not (e.g., standard API access). Discuss whether SIFT can be adapted to work with only final-layer representations or logits.

- **Expand empirical validation**: Test SIFT on more models (especially larger ones like Llama-3.1-70B) and longer prompts. Report the distribution of inversion times more thoroughly (e.g., histogram, not just mean/std).

- **Address the construction in Theorem 2.2**: Provide a concrete example of a parameter setting that separates two specific prompts, showing that it respects all architectural constraints (e.g., attention weights sum to 1, LayerNorm with ε > 0).

## Score and Decision

The paper makes a genuinely novel theoretical contribution and provides strong empirical support for the injectivity claim. However, the critical gap in the training preservation proof (Theorem 2.3) undermines one of the paper's central claims—that injectivity persists under training. Without a rigorous proof or strong empirical evidence that training preserves injectivity, the paper's main theoretical contribution is weakened. Additionally, the practical relevance of SIFT is limited by the unrealistic threat model. Despite these issues, the core insight and the initialization injectivity proof are valuable contributions that warrant acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>