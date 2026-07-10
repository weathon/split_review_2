Here is my final consolidated review.

---

## Summary

This paper proves that decoder-only Transformer language models are almost-surely injective — different prompts map to different last-token hidden representations — using a real-analyticity argument showing collisions are confined to measure-zero parameter sets. It further claims this injectivity persists under gradient-based training, and introduces SIFT/SIPIT, an algorithm that exploits injectivity for exact prompt recovery from hidden states. The paper is primarily a theoretical contribution (injectivity theorems) with supporting empirical validation.

## Strengths

- **Counterintuitive theoretical claim (Section 2).** The widely-held intuition is that nonlinearities, normalization, and attention mechanisms cause information loss. The paper argues the opposite — that the map from prompts to last-token representations is almost-surely injective. The use of real-analyticity to argue that collisions are confined to measure-zero parameter sets is a clever and mathematically natural framework.

- **Clean use of the real-analytic dichotomy (Theorems 2.1, 2.2).** The core technical move — showing that the squared-distance function between two prompts' representations is real-analytic, and therefore either identically zero or zero on a measure-zero set — is elegant. The construction of a witness parameter setting where h(θ) ≠ 0 for each prompt pair (freezing the network so that the last state reduces to embedding plus position) is explicit and convincing. This part of the argument is well-structured and appears sound.

- **The injectivity result has genuine implications (Section 6).** If hidden states are lossless encodings of the full input, then systems that cache or transmit hidden states are effectively handling user text. The paper correctly distinguishes this implication from questions about training data in weights, and does not overreach in its practical claims.

## Weaknesses

### Major

- **The proof sketch for Theorem 2.3 (injectivity preserved under training) is incomplete in the main text.** The argument (lines 105–109) claims that pushing an absolutely continuous parameter distribution through a GD update map φ(θ) = θ − η∇L(θ) yields another absolutely continuous distribution because det(Dφ) ≠ 0 a.e. and φ is locally invertible via the Inverse Function Theorem. The property that a map with non-vanishing Jacobian almost everywhere preserves absolute continuity under pushforward is non-trivial for non-injective maps and is not rigorously justified in the sketch. The paper directs to Appendix C for the full proof, but the main text's reasoning is insufficient as a standalone argument. Since the persistence-under-training claim is what differentiates this work from Sutter et al. (2025), this gap is significant. If the appendix contains a rigorous proof, the core reasoning should be presented in the main text.

### Minor

- **The SIFT/SIPIT algorithm is essentially a sequential search over the vocabulary enabled by the injectivity guarantee.** Given injectivity and access to per-position hidden states, enumerating candidates and checking for a match is the natural approach. The comparison against HARDPROMPTS (0% accuracy) is not especially informative because HARDPROMPTS is designed for continuous prompt optimization, not exact prompt recovery from hidden states. The more relevant baseline (Thomas et al., 2025) is discussed qualitatively in related work but not compared numerically.

- **The collision-search experiments (Section 4.1) serve primarily as sanity checks rather than independent evidence.** 10⁵ prompts represent a tiny fraction of the input space, and the theory already predicts no collisions with probability 1. Additionally, the "collision threshold" of 10⁻⁶ used in Figures 3–5 is presented without derivation or justification for why this specific value is appropriate.

- **The paper does not address how floating-point arithmetic interacts with the injectivity claim.** Injectivity requires exact equality in ℝ^d, but computations use finite precision. A theoretically injective model could produce two representations differing by 10⁻¹⁵ due to numerical non-associativity — the paper should discuss how this affects the practical interpretation of the guarantee.

- **The step-size assumption η ∈ (0,1) in Theorem 2.3 is stated without justification.** Many practical training setups use learning rates outside this range. The proof should clarify whether this restriction is necessary or an artifact of the argument.

### Trivial

- **Naming inconsistency across the paper.** The algorithm is introduced as "SIFT" in the Abstract, renamed "SIPIT" in Section 3, appears as "SIpIT" in Algorithm 1, "SIpT" in the experiments introduction, and "SiPT" in Table 4. This inconsistent naming is confusing.

## Nice-to-Haves

- Include a direct empirical comparison with Thomas et al. (2025), the most closely related inversion method (hidden states, sequential recovery). This would meaningfully ground the efficiency claim.
- Provide a derivation or empirical justification for the 10⁻⁶ collision threshold used in the experiments.
- Address floating-point precision and its interaction with the theoretical exact-equality guarantee.

## Removed Points

- **Gradient-guided search not described (Algorithms 2, 3):** These algorithms are referenced in the main text but reside in the appendix, which the parser strips. Removed per rule that missing appendix content is not assessable.
- **"Actual domain narrower than it first appears":** The reviewer initially raised this concern but walked it back, noting Corollary 2.3.2 handles it correctly. Removed as self-resolved.
- **Generic/superficial strengths about "important problem":** Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- If the gap in Theorem 2.3's proof can be closed, present the core reasoning more rigorously in the main text, or at minimum state what additional conditions are required. If it cannot be made fully rigorous, honestly reframe: injectivity holds at initialization and is empirically observed to persist, but a fully rigorous training-time guarantee may require additional assumptions.
- Include a direct empirical comparison with Thomas et al. (2025).
- Unify the algorithm name throughout the paper (SIFT/SIPIT/SIpIT/SiPT).
- Address floating-point precision issues explicitly.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>