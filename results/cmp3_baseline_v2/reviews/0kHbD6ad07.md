## Summary

The paper claims that decoder-only Transformer language models are almost surely injective: distinct prompts (within a finite vocabulary and context length) yield distinct last-token hidden representations. This property is argued to hold at random initialization and to persist under gradient-based training. Building on this, the authors introduce SIPIT (also referred to as SIFT), an algorithm that reconstructs the exact input prompt from intermediate hidden states with provable linear-time guarantees. Empirical collision searches and inversion experiments on several models (GPT-2, Gemma-3, Llama-3.1, etc.) are presented as supporting evidence.

## Strengths

- **Addresses an important question** – Whether transformer representations are lossy or lossless has direct implications for interpretability, transparency, and privacy. The paper challenges the common intuition that non-linearities and normalization destroy information.
- **Novel theoretical perspective** – Using real-analyticity to analyze the discrete-to-continuous mapping from prompts to hidden states is a creative and rigorous approach. The connection to measure-zero collision sets is well motivated.
- **Extensive empirical validation** – The paper tests for collisions across 100k prompts (≈5 billion pairs) on a variety of models and layers, consistently observing no collisions. Inversion experiments on quantized and large models further illustrate the practical utility.
- **Clear practical takeaway** – The demonstration that hidden states are lossless encodings of the input has concrete legal and regulatory implications, which the paper discusses.

## Weaknesses

### Fatal

**Insufficient justification for injectivity preservation under training (Theorem 2.3).**  

The core argument is that the gradient descent update map φ(θ)=θ−η∇ℒ(θ) is real-analytic, its Jacobian determinant is non-zero almost everywhere, and therefore the pushforward of an absolutely continuous parameter distribution remains absolutely continuous – implying the collision set (measure zero) is never hit. Several gaps undermine this:

1. **From det Dφ ≠ 0 a.e. to absolute continuity preservation is non-trivial.** The Inverse Function Theorem only guarantees local invertibility near points where det Dφ ≠ 0. The paper asserts that this prevents “collapsing regions of positive volume onto lower-dimensional sets”, but no theorem is cited or proved that a locally invertible a.e. map with non-vanishing Jacobian a.e. preserves absolute continuity of the pushforward measure. This is not a standard corollary; additional conditions (e.g., the map being a global diffeomorphism, Lipschitz, or proper) are typically required. Without a rigorous argument, the claim that training cannot map parameters into the measure-zero collision set is unsupported.

2. **The extension to SGD / mini-batch GD (Corollary 2.3.1) is even weaker.** The proof states that at a particular “simple parameter setting” the batch Jacobian determinant is non-zero because it “coincides with the single-sample one by linearity of differentiation.” This is false: the gradient of the batch loss is the average of per-sample gradients, and its derivative is the average of per-sample Hessians. There is no reason this average should have the same determinant as any single-sample Hessian at that point. The argument is insufficient.

Because the paper’s central theoretical claim – that injectivity is preserved during training – rests on this reasoning, the flaw is fatal. Without a correct proof, the main contribution is unsubstantiated. The empirical collision search, while supportive, cannot prove injectivity over the exponentially large space of all possible prompts up to context length K.

### Major

- **Algorithm name inconsistency** – The abstract introduces “SIFT” but the detailed description and Algorithm 1 refer to “SIPIT”. This suggests a lack of care in the manuscript.
- **SIPIT requires access to all per-position hidden states at a given layer.** The authors acknowledge that inversion from only the final representation is left to future work, which limits the practical scope. Many realistic threat models (e.g., leaked KV‑cache) provide only certain states, but the paper does not fully characterize which settings are covered.
- **The “collision threshold” (10⁻⁶) is arbitrary.** In floating point arithmetic two different prompts could produce bitwise identical representations only in extreme cases, but the threshold has no theoretical grounding. The empirical “no collisions” result is consistent with the theory, but does not itself prove injectivity.

### Minor

- The experiments, while large-scale, only test a finite (though large) set of prompt pairs. The theoretical proof is essential for the claimed certainty, and its flaw leaves the central assertion unsupported.
- The discussion of legal/privacy implications, while interesting, is speculative and not directly tied to the technical results in a quantitative way.

## Nice-to-Haves

- A more rigorous treatment of how gradient descent updates affect the parameter distribution would significantly strengthen the paper. This might involve proving that the update map is a global diffeomorphism (or at least that the pushforward of an absolutely continuous measure remains absolutely continuous) under realistic assumptions.
- Clarifying the threat model and specifying exactly which hidden states (e.g., last-token only, all positions at a given layer, or KV‑cache) are needed for SIPIT would help practitioners understand the algorithm’s applicability.

## Novel Insights

None beyond the paper’s own contributions – the real-analytic approach and the empirical confirmation that collisions do not occur in practice are the main novelties. If the theoretical guarantee were correctly established, it would be a significant insight.

## Suggestions

1. **Fix the training preservation proof.** Provide a correct argument that the distribution of parameters after any finite number of gradient descent steps remains absolutely continuous (or that the set of initial parameters leading to collision after training has measure zero). This may require stronger assumptions (e.g., that the update map is a diffeomorphism almost everywhere and that the parameter space is compact).
2. **Align the algorithm name** throughout (pick either SIFT or SIPIT and use it consistently).
3. **Clarify the limitation** that the inversion algorithm requires all per-position states at a given layer, and discuss whether alternative access (e.g., only last-token state) could still be exploited.

## Score and Decision

**Score:** 3 – reject. The paper’s main theoretical contribution (injectivity preserved during training) is not convincingly proved, and the flaw is fatal to the core claims. The empirical work is strong but cannot substitute for the missing theoretical guarantee. Without a correct proof, the paper does not meet the standard for acceptance at a top venue.

MY FINAL SCORE: 3</score>  
MY FINAL DECISION: Reject</decision>