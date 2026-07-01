Now I have all the verification I need. Let me write the final consolidated review.

## Summary

This paper proves that decoder-only Transformer language models are almost-surely injective: the map from prompts to last-token hidden states is injective with probability one at random initialization (Theorem 2.2), and injectivity is preserved under gradient-based training (Theorem 2.3). The proof leverages real-analyticity of Transformer components and the measure-zero property of zero sets of non-identically-zero real-analytic functions. The paper introduces SIFT/SIPIT, an algorithm that reconstructs the exact input from per-position hidden states, and provides empirical collision search across six model families plus inversion experiments.

## Strengths

1. **Elegant theoretical framing that genuinely advances understanding.** The paper correctly identifies that injectivity of the discrete-to-continuous map (prompts → last-token hidden states) does not follow from the well-known non-injectivity of individual Transformer components. Using real-analyticity and the fundamental dichotomy of real-analytic functions (either identically zero or measure-zero zero set) is a mathematically sound and non-trivial approach. The construction in Theorem 2.2 to exhibit a parameter setting where two prompts yield different last-token states (thereby proving h(θ) is not identically zero) is carefully reasoned.

2. **Extension from initialization to training (Theorem 2.3) goes beyond prior work.** The paper explicitly credits Sutter et al. (2025) for proving injectivity only at initialization. The argument that gradient descent preserves absolute continuity of the parameter distribution is a meaningful advance, provided the full proof holds up.

3. **Large-scale collision search across multiple model families.** Testing 6+ model families (GPT-2, Gemma-3, Llama-3.1-8B, Mistral-7B, Phi-4, TinyStories) on ~100k prompts with billions of pairwise checks provides useful empirical support. The observation that minimum pairwise distances grow with depth and remain well-separated (Figure 3, Table 1) is a genuinely informative empirical finding.

## Weaknesses

### Fatal
None.

### Major

1. **Training-preservation argument (Theorem 2.3) has unresolved gaps in the main text.** The proof sketch states that the Jacobian determinant det Dφ(θ) of the GD update is "real-analytic and not identically zero (one can check this by evaluating at a simple parameter setting)," but the main text never specifies what that parameter setting is or why checking it is possible. Given the complexity of the Hessian of a cross-entropy loss through a full Transformer, this is a non-trivial claim that requires explicit verification. Further, the mini-batch SGD extension (Corollary 2.3.1) argues that "at the point θ\* from the single-sample proof (where the Jacobian determinant is sample-independent and nonzero) the batch Jacobian coincides with the single-sample one by linearity of differentiation, and its determinant is therefore also nonzero." This reasoning is insufficient as stated: Dφ_B = I − η·(1/|B|)·∑∇²L_i, which equals (1/|B|)·∑Dφ_i. Even if each Dφ_i(θ\*) has nonzero determinant, their average can have zero determinant (the determinant of a sum of matrices is not determined by the individual determinants). The full appendix may resolve these gaps, but the main-text argument is not self-contained. If the training preservation claim cannot be sustained, the paper's primary advance over Sutter et al. (2025) collapses.

2. **Inversion evaluation is far too limited to support the practical claims.** SIFT/SIPIT is advertised as the "first algorithm that provably and efficiently reconstructs the exact input text from hidden activations," but the main inversion experiment (Table 5) uses only **100 prompts of 20 tokens on GPT-2 Small** (85M parameters). The quantized-model experiments (Table 4) use 50 prompts of 10 tokens. This is a tiny evaluation for a method whose headline claim is enabling exact recovery in practice. We do not know whether SIFT scales to larger models like Llama-3.1-8B at full precision on realistic-length prompts. The accuracy metric is saturated at 100% and cannot discriminate. A stronger evaluation (more prompts, varying lengths, at least one larger model at full precision) is needed to substantiate the practical claims.

### Minor

3. **Framing gap between theory and algorithm.** The paper proves that the *last-token* hidden state almost-surely identifies the input prompt (injectivity). The SIFT algorithm, however, assumes access to *all per-position hidden states* at a given layer. The paper acknowledges this explicitly (Section 3: "designing an efficient algorithm for that setting is nontrivial and left to future work; here we assume access to all per-position states at a given layer ℓ"), which is commendably transparent. However, the abstract states that SIFT "reconstructs the exact input text from hidden activations" without distinguishing which hidden activations, and the discussion (Section 6) argues that "hidden states are not abstractions but the prompt in disguise: any system that stores or transmits them is effectively handling user text itself." This conflates the theoretical result (which applies to any single hidden state) with the algorithmic demonstration (which needs the full matrix). The framing could more carefully separate the two guarantees.

4. **HARDPROMPTS baseline is uninformative.** HARDPROMPTS was designed for a different task (discrete prompt optimization) and, unsurprisingly, achieves 0% accuracy on exact token recovery. The paper acknowledges this mismatch but includes it anyway. This comparison adds nothing to the evaluation.

5. **Collision threshold is not theoretically anchored.** The paper sets a collision threshold of 10⁻⁶ L2 distance and reports all minimum distances are above it. While the observed distances (0.001–20+) are orders of magnitude above this threshold and the threshold is practically reasonable, the paper frames this as confirming "no collisions" without discussing the relationship between this empirical check and the theoretical claim of exact injectivity. The actual minimum distances are reported and speak for themselves, but the threshold choice appears unmotivated.

### Trivial

6. **Naming inconsistency.** The algorithm is referred to as "SIFT" in the abstract and Section 1, "SIPIT" in the Section 3 heading and introduction, "SIpIT" in Algorithm 1, and "SiPT" in the experiment tables (Tables 4, 5, line 319). These should be unified.

## Nice-to-Haves

- Reporting the empirical minimum separation Δ_{π,t} (Theorem 3.2) across models and layers would directly connect the theoretical robustness guarantee to practice.
- Analyzing worst-case (rather than just mean) exploration rates for the gradient-guided policy would characterize when SIFT might approach the brute-force bound.
- The paper would benefit from more thorough discussion of which real-world deployment scenarios provide per-position hidden-state access (KV-cache leaks, shared inference) versus only last-token access (typical API endpoints).

## Removed Points

These points were flagged for removal in the filter pass; they are listed here for transparency:

- **"The empirical collision search does not test the claimed property"** (original Weakness 3 from the harsh critic): The critic demanded checking for exact (bit-identical) equality rather than using a threshold. This is not standard practice—floating-point arithmetic means exact equality is not expected even for mathematically injective functions, and the reported minimum distances (all well above 10⁻⁶, most above 10⁻¹) already speak to the claim. The critic's demand is unreasonable for numerical verification. **Removed.**

- **"SIFT is essentially brute-force"** and "not a deep algorithmic insight": This is a normative claim about contribution significance rather than a concrete weakness. The paper does not claim deep algorithmic novelty; it frames SIFT as an operationalization of the theoretical result. **Removed.**

- **Concerns about missing appendix, proofs, or references**: The parser strips these sections; they exist in the original submission. **Removed per instructions.**

- **"Missing related work"**: Cannot be verified without external sources. **Removed per instructions.**

- **Criticism that the paper should cover multimodal architectures, ReLU activations, etc.**: These are explicitly scoped out or acknowledged as failure cases by the paper (lines 125, 135). **Removed as scope creep.**

## Novel Insights

The most interesting meta-point that emerges from reading the reviews is the fundamental tension between the theoretical claim (last-token injectivity) and the algorithmic practice (per-position recovery). The paper's cleanest contribution is the injectivity theorem itself, which is genuinely surprising: despite non-injective components (LayerNorm, softmax, non-linearities), the composite prompt-to-last-token map is almost-surely injective. The SIFT algorithm is a straightforward consequence (causal structure + injectivity → sequential brute-force search works with a guarantee), and the paper could more honestly frame it as a demonstration rather than a co-equal contribution. The unresolved question is whether the training-preservation argument (Theorem 2.3) can be made fully rigorous; the sketched Jacobian-determinant argument is the paper's most technically delicate claim and also the least-verified part in the main text.

## Suggestions

1. **Tighten the training-preservation argument.** Provide an explicit construction for the "simple parameter setting" where det Dφ ≠ 0, or replace the Jacobian-determinant approach with a more rigorous argument accessible in the main text. The mini-batch extension needs a corrected justification.

2. **Expand the inversion evaluation.** At minimum, run SIFT on one larger model (e.g., Llama-3.1-8B) at full precision with more prompts and varying lengths. Report worst-case exploration rates and failure cases.

3. **Sharpen the framing.** Make the distinction between "injectivity (exists in theory)" and "SIFT (practical recovery with per-position access)" clearer in the abstract and conclusions. Consider leading with the injectivity theorem as the primary contribution and presenting SIFT as a corollary/demonstration.

4. **Unify the algorithm name** throughout the paper.

## Score and Decision

The paper's core contribution—proving that decoder-only Transformers are almost-surely injective using real-analyticity—is a genuine theoretical advance that challenges a common intuition. The collision search experiments provide reasonable empirical support. However, the training-preservation argument contains verification gaps in the main text that are not negligible, and the inversion evaluation is too small to support the practical claims made. The paper would benefit from a revision that closes these gaps and narrows its claims to match its evidence.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>