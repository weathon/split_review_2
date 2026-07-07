Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proves that decoder-only Transformer language models are almost-surely injective: distinct prompts map to distinct last-token hidden states under standard initialization and GD/SGD training. The proof uses real-analyticity to show collision sets are measure-zero and that training preserves this property. Empirically, a collision search across ~5B pairwise comparisons on six model families (GPT-2, Gemma-3, Llama-3.1, Mistral-7B, Phi-4, TinyStories) finds zero collisions. The paper also introduces SIFT/SIPIT, an algorithm that exploits injectivity to provably recover the exact input text from hidden states in linear time.

## Strengths

- **Well-motivated and significant question.** Whether LLM representations preserve input information is a foundational question with direct implications for interpretability, privacy, and transparency. The paper reframes this from a folklore assumption ("Transformers are lossy") into a concrete mathematical claim and offers a crisp answer backed by formal proof.

- **Elegant proof strategy.** The core idea — that real-analyticity forces collisions onto measure-zero parameter sets — is mathematically clean. The proof decomposes into three manageable parts (real-analyticity of the architecture, initialization avoids collision sets, GD/SGD preserves avoidance), each following from standard results in real analysis.

- **Consistent empirical support across diverse models.** The collision search covers six model families with ~5B pairwise comparisons finding zero collisions. Experiments on quantized models (FP4, INT8) and large models (up to 70B parameters) extend the findings to practically relevant settings. This level of empirical validation is rare for theory papers and strengthens confidence in the result.

- **Honest limitation disclosure.** The paper is upfront about what SIFT/SIPIT requires (access to all per-position hidden states at a given layer, not just the final embedding) and acknowledges deliberate failure cases (tied embeddings, quantization, non-smooth activations).

## Weaknesses

### Fatal
None.

### Major

1. **Training preservation theorem (Theorem 2.3) is proved only for GD/SGD, while all empirical models were trained with Adam(W).** The paper proves that gradient descent and SGD preserve injectivity because their update maps are real-analytic. However, all tested models (Gemma-3, Llama-3.1, Mistral-7B, Phi-4, etc.) were trained with Adam(W), whose elementwise scaling by inverse square roots of gradient moments introduces non-analyticities (square-root and division operations near zero). The paper does not acknowledge this gap between its theoretical guarantee and its empirical validation. The abstract and introduction state that injectivity is "preserved during training" and that "common training procedures" avoid collisions, without specifying the optimizer limitation. While the injectivity-at-initialization result (Theorem 2.2) stands independently and the empirical findings are consistent, the formal training guarantee applies to a different optimizer class than the one used to produce the tested models.

2. **Naming inconsistency across the paper.** The abstract and introduction introduce "SIFT"; Section 3 renames it "SIPIT" and Algorithm 1 uses "SIpIT"; the experiments section uses "SIpT", "SiPT", and "SIFT" interchangeably (Tables 4–5, Figures 6 caption, Section 4.2 text). This is not merely cosmetic — a reader trying to understand or reproduce the algorithm faces an unnecessary obstacle in tracking which variant is being discussed.

### Minor

3. **The proof sketch for Theorem 2.3 contains a nontrivial gap.** The sketch asserts that det(I − η∇²L) "is not identically zero (one can check this by evaluating at a simple parameter setting)" without constructing or even indicating what that setting is. Verifying that the Hessian has a non-degenerate region is nontrivial for a Transformer with cross-entropy loss, and the sketch leaves the reader to fill in this step. While the full proof resides in the appendix (stripped by the parser), the main-text sketch should at least indicate a plausible construction.

4. **SIFT/SIPIT's practical efficiency relies on an opaque gradient heuristic.** The gradient-based candidate policy (Algorithms 2–3) is referenced in Algorithm 1 but described only in the appendix. The main text reports that the algorithm explores ~0.2% of the vocabulary per token, but does not explain how the policy works, whether it requires differentiation through the full model for each candidate, or how sensitive it is to prompt length, model size, or quantization. With 50–100 test prompts and high runtime variance (28±36s for GPT-2 Small, 549±266s for Llama-3.1-8B), the efficiency claims would benefit from more analysis of when and why the heuristic succeeds.

5. **The step size bound η ∈ (0,1) in Theorem 2.3 is stated without justification.** It is unclear whether this bound is necessary for the proof, what breaks for η ≥ 1, or whether it is a proof artifact.

### Trivial
None.

## Nice-to-Haves

- A brief description of the gradient-based candidate policy (Algorithms 2–3) in the main text would help readers assess the efficiency claims without consulting the appendix.
- A paragraph acknowledging the GD/SGD versus Adam gap — explaining why the empirical consistency is still informative (e.g., the architecture result at initialization is optimizer-independent, and the training result may extend heuristically) — would strengthen the paper's framing.
- Justifying the η ∈ (0,1) bound or clarifying whether it is a proof artifact would improve the theoretical presentation.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Empirical collision search covers negligible fraction of input space**: The paper's claim is theoretical, not empirical; the experiments are supporting evidence. The scoring model assigned this criticism a positive weight (+3.36), confirming it is not a valid weakness. However, the paper could frame the empirical results as a "consistency check" rather than "confirming local injectivity" (Figure 4 caption) for precision.
- **HARDPROMPTS comparison is of questionable value**: The paper explicitly acknowledges the comparison is imperfect (lines 293–311), noting HARDPROMPTS addresses a different setting. This transparency is appropriate.
- **Threat model is vague**: The paper explicitly states "we do not define a full adversarial model" (line 141) and gives concrete scenarios (leaked KV-cache, shared-inference pipeline). This is transparent scoping, not an oversight.
- **Privacy implications underdeveloped**: The privacy discussion (Section 6) scopes its claim to systems that "store, cache, or transmit hidden states," which is consistent with the threat model.
- **Framing overstatement relative to Sutter et al. (2025)**: The paper correctly positions itself in Section 5, noting Sutter et al. proved injectivity at initialization for the full hidden-state matrix, while this paper extends to the last-token state and persistence under training.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface an angle the paper itself misses.

The reviews surface a useful observation that the paper could benefit from: the real gap between the GD/SGD training guarantee and the Adam-trained empirical models is not just a scope footnote but a genuine tension that the paper should address explicitly, even if only by acknowledging it and explaining why the empirical consistency is still meaningful.

## Suggestions

1. **Unify the algorithm name** throughout: pick one consistent name (e.g., SIFT or SIPIT) and use it in every section, table, and figure caption.
2. **Acknowledge the GD/SGD versus Adam gap** explicitly in the main text. Explain that Theorem 2.3 covers GD/SGD, that the empirical models were trained with Adam, and that the architecture-level injectivity result (Theorem 2.2) is optimizer-independent. If the argument plausibly extends to Adam heuristically, say so.
3. **Include a brief description of the gradient-based policy** from Algorithms 2–3 in the main text, or at minimum give the high-level intuition (e.g., "the policy uses the gradient of the reconstruction loss with respect to token embeddings to rank candidates").
4. **Justify the η ∈ (0,1) bound** or clarify whether it is a proof artifact that could be relaxed.
5. **Tighten the proof sketch for Theorem 2.3** by providing a concrete example of a parameter setting where det(I − η∇²L) ≠ 0, or by stating more precisely where in the appendix the construction appears.

## Score and Decision

**Calibration report:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| 10kBEqYKKN.md | Impact of Prompt on Latent Repr. in LLMs | 3.00 | 1 | Yes | Pervasive writing issues, no clear insights — much weaker than this paper |
| nxQ0Bjp8zD.md | Provable ICL for Mixture of Linear Regressions | 5.00 | 1 | Yes | Similar theoretical style but derivative results (-7.30), limited significance (-7.11); our paper has stronger novelty |
| 1lFZusYFHq.md | How Transformers Implement Induction Heads | 6.20 | 2 | Yes | Strong strengths (+8.64) but severe weaknesses about simplified models (-7.77) and writing (-7.51); our paper tests real models |
| SfNmgDqeEa.md | Looking Beyond Top-1 | 6.40 | 1 | Yes | Novel concept but insufficient evidence for main claim (-9.79); our paper's evidence is stronger |
| 6S4WQD1LZR.md | Transformers are Universal ICL Learners | 6.67 | 2 | Yes | Very high strengths (+6.47, +7.42) with very mild weaknesses; purely theoretical, no experiments on real models |
| NHhjczmJjo.md | On the Learn-to-Optimize Capabilities | 7.00 | 1 | No | Strong theory with mild weaknesses; no real-model experiments |
| hwSmPOAmhk.md | Understanding Factual Recall via Assoc. Memories | 7.33 | 2 | Yes | High impact potential, solid theory, very mild weaknesses (all near zero); synthetic tasks only |
| STUGfUz8ob.md | When can transformers reason with abstract symbols | 7.60 | 1 | Yes | Very strong theoretical + empirical; mild concerns about architecture simplification |

**Bracket reasoning (Round 1):** The paper falls between 5.5 and 7.0. Its strengths (+4.23 to +5.41) are above the 5.00 anchor's (whose main weaknesses were derivative results and limited significance) but below the 6.67 anchor's (whose strengths reached +7.42 with near-zero weaknesses). The paper's main negative items (Adam gap at -3.19, naming at -4.73) are more substantial than the near-zero weaknesses of the 6.67 and 7.33 anchors, but the paper benefits from testing on real, large-scale models (Gemma-3, Llama-3.1-70B) — a strength most theory anchors lack.

**Narrowing (Round 2):** Compared to the 6.20 anchor (induction heads), this paper's weaknesses are less severe (not about simplified toy models or incremental contribution) and its empirical validation is substantially stronger. Compared to the 6.67 anchor (universal ICL), this paper's weaknesses are more negative but its experiments are on real deployed models rather than purely theoretical. The 7.33 anchor (associative memories) has very mild weaknesses but only tests on synthetic tasks.

**Final placement:** The paper has a genuinely novel theoretical contribution with clean proofs and unusually strong empirical validation on real deployed models. The two main weaknesses (Adam gap, naming inconsistency) are real but fixable. It is clearly above the 5.00 and 6.20 anchors and sits near the lower end of the 6.5–7.5 band, below the cleanest theory papers that have near-zero weaknesses.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>