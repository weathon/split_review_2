## Summary

This paper claims that decoder-only Transformer language models are almost surely injective: different prompts map to different last-token hidden states. It provides a theoretical proof using real-analyticity and measure theory, argues that this property is preserved under gradient-based training, and introduces SIFT, an algorithm that exactly recovers the input prompt from hidden states in linear time. Empirical collision searches on several models find no collisions, and inversion experiments show perfect recovery on small-scale tests.

## Strengths

- **Novel and important question.** The paper challenges the common intuition that Transformers are lossy and provides a rigorous theoretical perspective on injectivity of the prompt-to-representation map. This is a fundamental property with implications for interpretability, privacy, and safety.
- **Rigorous theoretical framework for initialization.** The use of real-analyticity to prove that collisions are measure-zero at initialization is elegant and well-executed. The proof sketch is clear and the reliance on standard initialization distributions is reasonable.
- **Extensive empirical collision search.** The paper performs billions of pairwise comparisons across multiple model families (GPT-2, Gemma-3, Llama-3.1, Mistral, Phi-4, TinyStories) and finds no collisions, strongly supporting the theoretical claim. The inclusion of quantized and large models adds robustness.
- **Clear writing and structure.** The paper is well-organized, with a logical flow from theory to algorithm to experiments. The figures and tables effectively communicate the key empirical findings.

## Weaknesses

### Major

- **Insufficient justification for training preservation of injectivity.** The proof sketch for Theorem 2.3 (injectivity preserved under training) relies on the claim that a single gradient descent step is a diffeomorphism that preserves absolute continuity of the parameter distribution. The argument that the update map φ(θ)=θ−η∇L(θ) has a non-zero Jacobian determinant almost everywhere and is therefore a "smooth, locally invertible change of coordinates" does not guarantee that the pushforward of an absolutely continuous measure remains absolutely continuous. Local invertibility is not sufficient; global injectivity or additional properties (e.g., properness) are needed to prevent the map from collapsing sets of positive measure onto lower-dimensional sets. The sketch does not address this gap, and the reliance on the Inverse Function Theorem alone is insufficient. Since the training preservation claim is central to the paper's main result, this is a significant weakness.

- **Limited empirical validation of the inversion algorithm.** The SIFT experiments are conducted on only 100 prompts of 20 tokens (GPT-2 Small) and 50 prompts of 10 tokens (quantized models). This scale is too small to convincingly demonstrate that the algorithm works reliably in practice, especially given the claim of "exact invertibility." The comparison with HARDPROMPTS is not meaningful because HARDPROMPTS addresses a different task (prompt optimization) and does not have access to hidden states. The ablation with BRUTEFORCE is trivial.

- **Assumption of access to all per-position hidden states.** The inversion algorithm requires the full hidden-state matrix at a given layer. The paper acknowledges this but does not discuss realistic threat models where only the last-token state or a subset of states might be available. This limits the practical applicability of the claimed "invertibility" and weakens the privacy implications drawn in the discussion.

### Minor

- **The worst-case linear-time guarantee is essentially brute force.** The bound O(T|V|) is linear but not efficient for large vocabularies (e.g., 128k). The paper's empirical observation that only ~0.2% of the vocabulary is explored is interesting, but the theoretical guarantee is weak.
- **The paper's title and abstract may overclaim.** The phrase "hence invertible" suggests that injectivity directly implies a practical inversion algorithm, but the algorithm requires additional assumptions (access to all per-position states) and is not guaranteed to be efficient in the worst case.

### Trivial

- The paper uses "SIFT" and "SIPIT" inconsistently (the algorithm is introduced as SIPIT but later referred to as SIFT in some places). This is a minor inconsistency.

## Nice-to-Haves

- A more rigorous treatment of the training preservation argument, possibly using tools from optimal transport or showing that the update map is a global diffeomorphism under the given assumptions.
- Larger-scale inversion experiments on longer prompts and more diverse models to strengthen the empirical claims.
- A discussion of how the inversion algorithm could be extended to settings where only the last-token state is available, or a proof that such extension is impossible.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Provide a complete and rigorous proof that gradient descent preserves absolute continuity of the parameter distribution, or relax the claim to only hold at initialization and empirically verify that trained models remain injective (which the collision search already supports).
- Clarify the threat model and the exact access assumptions needed for SIFT. If the goal is to demonstrate invertibility from hidden states, consider also evaluating a setting where only the last-token state is available (even if the algorithm is less efficient).
- Increase the scale of inversion experiments (more prompts, longer sequences, multiple models) to build confidence in the practical utility of the algorithm.

## Score and Decision

The paper addresses an important question and provides a compelling theoretical and empirical case for injectivity at initialization. However, the central claim that injectivity is preserved under training is not convincingly justified, and the inversion experiments are too limited to fully support the practical claims. Given that the training preservation argument is a core component of the paper's main result, this weakness is significant.

**Score**: 4

**Decision**: Reject

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>