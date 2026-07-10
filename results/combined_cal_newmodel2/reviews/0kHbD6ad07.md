Now let me compile the final review with the calibration comparison.

**Round 1 Bracketing**: After reviewing the paper and the initial calibration results, I determined the paper sits between 5.5 and 7.5 because: (a) papers below 5.5 (like "Complexity of Injectivity" avg 5.0 and "When Can Transformers Count to n?" avg 5.6) had more severe issues with proof correctness, missing empirical support, or oversimplified settings, while the current paper has a clean theoretical proof and a practical algorithm; (b) papers above 7.5 (like "On the Hölder Stability" avg 8.0) had strong theory plus extensive experiments and new architectures, which the current paper lacks.

**Round 2 Narrowing**: I examined "Minimum width for universal approximation" (avg 7.0, accepted) and "Transformers are Universal In-context Learners" (avg 6.67, accepted) as upper-band anchors, and "Provable In-context Learning" (avg 5.0, rejected) and "Complexity of Injectivity" (avg 5.0, rejected) as lower-band anchors. The current paper's theory is more original than "Minimum width" (which was criticized as incremental) and has a practical algorithm unlike the pure-theory "Universal In-context Learners" paper. However, it has more presentation issues and weaker experiments than those accepted papers. This places it between the lower anchors (~5.0 rejected) and upper anchors (~6.67-7.0 accepted).

The favorability ratings from my draft show the strengths are all high (8.86-15.00) while the weaknesses range from strongly negative (HARDPROMPTS comparison at -4.01) to mildly negative. Compared to anchors: "Minimum width" had a -4.16 point for incremental contribution (similar magnitude to my HARDPROMPTS point at -4.01) and still got accepted at 7.0, but its strengths were rated higher (14.21, 12.30 for theoretical contributions). "Complexity of Injectivity" at 5.0 had severe presentation issues (favorability as low as -1.01 for sketch completeness). My paper's most negative item (-4.01 for HARDPROMPTS) is comparable but the overall favorability profile is better than the 5.0 anchors and worse than the 7.0 anchors. Final score: **6.0**.

Here is my final consolidated review.

---

## Summary

This paper proves that standard decoder-only Transformer language models are almost surely injective — i.e., different prompts almost surely yield different last-token representations. The proof uses real-analyticity of Transformer components (embeddings, LayerNorm, attention, MLPs with analytic activations) to show that collisions can only occur on a measure-zero set of parameters, and that gradient descent preserves this property. Building on this, the authors introduce an algorithm (variously named SIFT/SIPIT/SiPT) that recovers the exact input from per-position hidden states with linear-time guarantees.

## Strengths

- **A genuinely counterintuitive theoretical claim, clearly articulated.** The paper identifies a real tension in the community's intuition — Transformer components (LayerNorm, softmax attention, residual connections) appear lossy, yet the paper argues the map from discrete prompts to last-token representations is almost surely injective. This is a substantive and non-obvious result that, if correct, meaningfully advances our theoretical understanding of these architectures. The framing in Section 1 accurately captures this tension.

- **Clean proof structure leveraging real-analyticity.** The overall approach — showing the model is real-analytic in its parameters (Theorem 2.1), applying the dichotomy that a non-identically-zero real-analytic function has a measure-zero zero set (Theorem 2.2), then arguing gradient descent preserves absolute continuity (Theorem 2.3) — is elegant and well-motivated. The authors correctly identify the key technical ingredients.

- **Honest about failure cases and limitations.** Section 2 explicitly acknowledges that collisions can be manufactured (identical embedding vectors, identical positional encodings, quantized weights). The threat model in Section 3 is transparent about the access assumption (all per-position states at a given layer). The paper also correctly identifies that designing an efficient algorithm for inversion from only the last token state is left to future work.

- **Noise-robustness theorem (Theorem 3.2).** The guarantee of exact recovery under bounded perturbations of hidden states is a genuine addition beyond the basic injectivity claim, connecting the theory to practical robustness.

## Weaknesses

### Major
None.

### Minor

1. **The comparison against HARDPROMPTS is uninformative.** HARDPROMPTS (Wen et al., 2023) is designed for prompt optimization — finding prompts that optimize a downstream objective — not for prompt inversion from hidden states. Reporting 0% accuracy (Table 5) does not establish anything about the proposed method. The paper itself identifies Thomas et al. (2025) as the closest prior work (§5) but does not compare against it, which is a missed opportunity for meaningful comparison.

2. **The inversion experiments are too small to be informative.** Table 5 reports results on 100 prompts of 20 tokens for GPT-2 Small (the smallest model tested), and Table 4 uses 50 prompts of 10 tokens for quantized models. While the theoretical correctness guarantee means these experiments serve as sanity checks rather than confirmations, the scale is limited relative to what the community would expect for claiming practical invertibility. Larger prompt sets, multiple lengths, and more model families would strengthen the demonstration.

3. **The tolerance ε in Algorithm 1 is never specified or discussed.** Algorithm 1 requires a tolerance ε ≥ 0 (line 175), and the paper notes that "in practice, we accept matches if the observed hidden state is within an ε-ball around the predicted one" (footnote 4). However, the actual ε value used in experiments, how it was chosen, and how sensitive results are to this choice are never reported. This is a gap in experimental reporting.

4. **The empirical collision search (§4.1) tests near-equality within a 10⁻⁶ threshold rather than exact equality.** The theoretical claim is about exact injectivity (with probability one), and the experiments provide a useful sanity check but cannot falsify or confirm the "with probability one" claim because they test finitely many pairs from finitely many prompts. The paper slightly overclaims the evidential value (abstract: "confirm this result empirically"; §4: "extensive empirical evidence supporting our theory"), when the experiments are better framed as sanity checks consistent with the theory.

5. **The proof sketch for Theorem 2.3 (training preservation of injectivity) is somewhat terse.** The claim that gradient descent preserves absolute continuity relies on the map φ(θ) = θ − η∇L(θ) being real-analytic with non-identically-zero Jacobian determinant. The sketch does not fully justify why local invertibility (via the Inverse Function Theorem) suffices to guarantee that the pushforward measure stays absolutely continuous with respect to Lebesgue measure. The full proof is in the appendix, but the sketch as presented would benefit from additional detail.

### Trivial

1. **The algorithm name is inconsistent throughout the paper.** The algorithm is called SIFT (abstract, §1, §4.2), SIPIT (§3 header, §3), SIpIT (Algorithm 1, Theorem 3.1), SiPT (Tables 4, 5), and SiPIT (Discussion). The expansion "Sequential Inverse Prompt via ITerative updates" does not clearly match any single variant. This is a basic presentational flaw that should be fixed.

## Nice-to-Haves

- Provide statistical variability information (error bars, confidence intervals) for the collision distance measurements.
- Discuss how different tokenization schemes might affect the injectivity result (this is outside the current scope but would strengthen practical relevance).
- Add a comparison against Thomas et al. (2025), which operates in the same setting and is identified as the closest prior work.

## Removed Points

These points from the harsh critic input were removed with justification:

- **Issue about Theorem 2.3 proof gap (properness concern):** The critic raised a specific technical concern about whether the GD map preserves absolute continuity. However, the paper states "full proof in Theorems C.1 and C.5" — the appendix was stripped by the parser, so we cannot verify whether this concern is addressed. A softened version is retained as Minor weakness #5 above.
- **Privacy discussion overclaimed:** The critic claimed §6 elides the distinction between last-token and per-position access. The paper's §3 clearly states the access assumption, and §6's claim that hidden states encode the prompt is conceptually valid. Not a genuine weakness.
- **Title overstatement:** The critic said the title overstates the result. The abstract and introduction clearly qualify with "almost-surely" and "with probability one." Standard rhetorical practice in theoretical papers.
- **Theorem 2.2 existential construction described informally:** This is a proof sketch; the full proof is in the appendix. Not a weakness.
- **Quantized models showing larger distances:** The paper explicitly comments on this observation (line 287), so the concern is addressed.
- **Missing related works:** Per hard rule, not mentioned.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Fix the algorithm naming inconsistency throughout (pick one name and use it consistently).
2. Either remove the HARDPROMPTS comparison or add a meaningful baseline operating in the same setting (e.g., Thomas et al. 2025).
3. Report the ε tolerance value used, how it was chosen, and analyze sensitivity.
4. Reframe the collision search as a sanity check consistent with theory rather than "empirical confirmation."
5. Increase the scale of inversion experiments or honestly reposition them as implementation sanity checks.
6. Expand the proof sketch for Theorem 2.3 to more clearly justify the absolute continuity preservation claim.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>