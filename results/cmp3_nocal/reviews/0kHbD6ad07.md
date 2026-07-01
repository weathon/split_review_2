## Summary

This paper proves that decoder-only Transformer language models are almost-surely injective: distinct prompts produce distinct last-token hidden representations. The proof exploits real-analyticity of the architecture to show that collisions are confined to a measure-zero parameter set, and that gradient descent training preserves this property. The authors validate the theory with large-scale collision searches (~5B pairwise comparisons across six model families, finding zero collisions) and introduce SIFT/SIPIT, an algorithm that provably recovers the exact input from per-position hidden states.

## Strengths

1. **Novel theoretical framing.** Reframing the prompt-to-representation map as a discrete-to-continuous map (rather than the usual continuous-to-continuous analysis of individual layers) is a genuine insight. Applying real-analyticity arguments to this discrete-domain map elegantly shows why non-injective components like LayerNorm and attention do not make the overall model lossy. This is a non-obvious contribution to the theoretical understanding of Transformers.

2. **Clean constructive argument in Theorem 2.2.** The proof constructs an explicit parameter setting that separates any two distinct prompts—by zeroing attention to collapse to the embedding layer for last-position differences, or by focusing one head on the first differing position. This avoids asymptotic or limit arguments and makes the measure-zero claim concrete.

3. **Large-scale and well-targeted empirical validation.** ~5 billion pairwise comparisons across GPT-2, Gemma 3, Llama-3.1, Mistral-7B, Phi-4, and TinyStories—with zero collisions observed and minimum L2 distances far above the collision threshold (10⁻⁶)—provides strong evidence the theoretical result is not vacuous. The inclusion of quantized models (FP4, INT8) and models with different normalizations (LayerNorm vs. RMSNorm) and activations (GELU, SiLU) broadens the validation.

4. **SIFT/SIPIT algorithm with provable guarantees.** The algorithm is straightforward and its correctness follows directly from injectivity. The linear-time worst-case bound (Theorem 3.1) and robustness guarantee (Theorem 3.2) are both clean and useful.

## Weaknesses

### Fatal
None.

### Major

- **Gap between proven training guarantee (GD) and tested models (Adam/AdamW).** Theorem 2.3 proves injectivity is preserved under gradient descent updates of the form φ(θ) = θ − η∇L(θ). The proof relies on the update map being real-analytic, which holds for GD. However, all pretrained models tested in Section 4 (GPT-2, Gemma 3, Llama-3.1, Mistral-7B, Phi-4) were trained with Adam-family optimizers, whose stateful moment-accumulation updates are not a simple analytic map from θₜ to θₜ₊₁. The paper does not acknowledge this discrepancy. The empirical collision search shows that these models *are* injective in practice, which is valuable positive evidence, but the theoretical training-preservation claim is proved for a narrower class of optimizers than what "standard training procedures" (line 31–33) suggests. The paper should either (a) explicitly state this limitation alongside the main result, or (b) discuss whether and how the proof could extend to adaptive optimizers.

### Minor

- **Naming inconsistency for the inversion algorithm.** The algorithm is called "SIFT" in the abstract (lines 9, 17) and in Section 4.2 (line 291), "SIPIT" at the start of Section 3 (lines 137, 139), "SIpIT" in Algorithm 1 (line 171) and Theorem 3.1 (line 202), and "SiPT" in Tables 4 and 5 (lines 309, 319). This is confusing and should be unified throughout the paper.

- **Unexplained discrepancy between Tables 1 and 2.** Table 1 reports the minimum L2 distance in the final layer (layer L) for Llama-3.1-8B as 0.620, and for Mistral-7B-v0.1 as 1.274. Table 2 reports the FP32 (unquantized) column for the same models in the final layer as 1.274 and 1.136, respectively. These should be the same measurement but differ by up to 2× (Llama-3.1-8B: 0.620 vs. 1.274). The paper does not explain this. If different prompts, seeds, or experimental conditions were used, this must be stated.

- **Framing overreach on "invertibility."** The title and abstract state that LMs are "injective and hence invertible." The injectivity theorem is about the *last-token* representation r(s; θ). The SIFT algorithm, however, requires access to the full per-position hidden-state matrix H^(ℓ)(s) at some layer ℓ (line 141: "here we assume access to all per-position states at a given layer ℓ"). The paper acknowledges this gap (lines 141–142: "recovery from only the final embedding is ... left to future work"), which is good, but the framing in the title and abstract suggests a stronger operational claim than what is currently delivered. The theoretical result is impressive as-is; the framing should match it.

- **Legal/discussion claims tied to SIFT access model.** Section 6 (lines 349–350) argues that hidden states "are not abstractions but the prompt in disguise" and that systems storing hidden states are "effectively handling the user's verbatim text." This argument relies on the SIFT access model (per-position states), whereas the paper's core theoretical object is the last-token state. The legal argument would be stronger if grounded in what can be recovered from the last-token state alone, or if it explicitly noted the access-model assumption.

### Trivial

- **Robustness condition (Theorem 3.2) may be hard to satisfy in practice.** The bound Δ_{π,t}/2 depends on the minimum distance between any two one-step states, which Figure 3 shows can be as small as ~10⁻⁵ in early layers. The theorem is correct, but the practical applicability of the robustness guarantee under realistic perturbations (e.g., adversarial noise) is limited.

## Nice-to-Haves

- **Adversarial prompt construction for collision search.** The current collision search uses naturalistic prompts from four datasets. A targeted search that iteratively optimizes prompts to minimize representation distance would provide even stronger evidence that collisions are genuinely absent, not just rare in natural data.
- **Statistical characterization of SIFT runtime variance.** The reported runtime for GPT-2 Small is 28.01 ± 35.87 seconds; the standard deviation exceeds the mean. Reporting the distribution (median, quartiles) and explaining what drives the variance would be more informative.

## Removed Points

These points were raised in the review but are not included as weaknesses. They are documented here for reference but should be treated with caution:

- **Training preservation proof sketch under-specified.** The reviewer notes the sketch does not fully justify the absolute-continuity preservation claim. However, the paper labels this as "Sketch of proof" and points to the full proof in Appendix C (Theorems C.1 and C.5). The appendix is stripped by the parser; per policy, missing appendix content is not a valid weakness.
- **SIFT policy not specified in main text.** The paper references Algorithms 2 and 3 (appendix) for the gradient-guided policy, which is standard practice for detailed algorithmic description. The appendix exists in the submission.
- **HARDPROMPTS comparison of questionable value.** The paper acknowledges that HARDPROMPTS is designed for a different task (prompt optimization for downstream performance, not exact inversion from hidden states). Showing that existing methods fail at this task is an informative negative result that motivates the new approach. This comparison serves a valid expository purpose.
- **Effect of layer depth not substantiated.** The paper phrases this as speculation ("likely, earlier layers need more iterations to converge"), not an empirical claim. No fix is needed.
- **Strawman weaknesses about missing code / reproducibility.** Not present in this review.

## Novel Insights

None beyond the paper's own contributions. The review identifies the GD/Adam gap as the most significant unresolved issue, but does not surface a deeper conceptual problem that the authors had missed.

## Suggestions

- Add an explicit paragraph in Section 2 or the introduction acknowledging that Theorem 2.3's training-preservation guarantee is proved for gradient descent (and its mini-batch variants), and that extending it to adaptive optimizers such as Adam is an open question. Note that the empirical results on Adam-trained models show the property nonetheless holds in practice.
- Unify the algorithm name throughout the paper (e.g., always "SIFT" for consistency with the abstract).
- Add a note explaining why Table 1 (layer L) and Table 2 (FP32) report different values for the same models, or consolidate them into a single table.
- Tone down the legal claim in Section 6 to clarify that it depends on the per-position access model, or strengthen it by discussing what can be inferred from the last-token state alone given injectivity.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>