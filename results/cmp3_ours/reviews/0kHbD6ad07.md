Good — I now have all the verification I need. Let me write the final consolidated review.

## Summary

This paper proves that decoder-only Transformer language models are almost-surely injective: distinct prompts map to distinct last-token hidden states, with collisions confined to a Lebesgue-measure-zero set of parameters. The proof uses real-analyticity of the parameter-to-representation map, arguing that injectivity holds at initialization and is preserved under gradient-based training. It then introduces SiPIT, an algorithm that exploits injectivity to recover the exact input prompt from per-position hidden states in provable linear time. Experiments on several models find no collisions and achieve exact recovery on small test sets.

## Strengths

1. **Elegant use of real-analyticity to establish injectivity (Section 2).** The proof framework is genuinely clever and well-structured. Treating the parameter-to-representation map as real-analytic and leveraging the dichotomy that a non-identically-zero real-analytic function has a measure-zero zero-set is a clean and appropriate mathematical approach. The finiteness of the prompt space 𝒱^{≤K} makes the union-over-pairs argument work.

2. **Surprising and non-trivial thesis.** The claim that standard decoder-only Transformers are injective (different prompts → different hidden states) runs counter to widely held intuitions about LayerNorm non-injectivity, attention's many-to-one structure, and residual cancellation. Framing this as a provable property is a genuine contribution.

## Weaknesses

### Major

1. **The training-preservation argument (Theorem 2.3) has a gap in the main-text sketch that the paper does not adequately resolve.** The sketch argues that the GD update map φ(θ)=θ−η∇ℒ(θ) is a local diffeomorphism almost everywhere (where det Dφ≠0) and therefore "pushing forward an absolutely continuous distribution through φ yields another absolutely continuous distribution" (line 107). The step from "local diffeomorphism almost everywhere" to "absolute continuity preserved" requires additional justification (e.g., invoking the Lusin N property via local Lipschitzness of C¹ maps) that the sketch omits. The paper states the full proof is in Appendix C (Theorems C.1, C.5), which the parser strips, so this gap may be resolved there. **However, as presented in the main text, the argument is incomplete.** This matters because the claim that injectivity persists under training is the paper's primary differentiator from prior work (Sutter et al., 2025, which covers initialization only). If the appendix proof closes this gap cleanly, this weakness is addressable; if not, the paper's contribution over prior work is substantially reduced.

### Minor

2. **The "probability one" guarantee does not directly transfer to floating-point arithmetic.** The proof operates in ℝᴺ with Lebesgue measure, but actual deployment uses discrete IEEE 754 parameters. A set of Lebesgue measure zero in ℝᴺ can contain many — or even all — representable float32 points. The paper acknowledges that quantization can break injectivity ("Failure cases," line 125) and tests quantized models, but the unqualified "probability one" / "almost surely" language throughout the abstract, theorems, and conclusions creates an impression that overstates what the mathematics guarantees for real systems.

3. **Empirical validation is too thin to support the confirmatory framing.** The collision search uses 100k prompts from an astronomical space (|𝒱|≈32K, K=2048); finding no collisions on 100k prompts is consistent with both injectivity and near-injectivity. The inversion experiments use 100 prompts (20 tokens each) for the main result and 50 prompts for the quantization result — far too few to constitute meaningful confirmation. The paper's core contribution is theoretical, so this does not threaten the main result, but the abstract and conclusion frame the experiments as "confirm[ing] this result empirically" (abstract), which the data do not support.

4. **Missing baseline: no comparison with Thomas et al. (2025).** The paper identifies Thomas et al. (2025) as "most closely related" work on prompt recovery from hidden states, yet provides no experimental comparison. Including this baseline would meaningfully situate the algorithmic contribution.

5. **The legal/privacy discussion (Section 6) draws conclusions that assume the algorithm is practical for the realistic threat model.** The paper acknowledges that recovering from only last-token states (which the injectivity theorem covers) is "left to future work" (line 141), and SiPIT requires per-position hidden states. Yet the discussion states that "any system that stores, caches, or transmits hidden states is effectively handling the user's verbatim text" (line 349). Since the algorithm requires per-position states — a stronger assumption than the theorem's guarantee about last-token states — this conclusion overreaches relative to what the paper's results currently support.

6. **Inversion experiments use only 20-token prompts (Table 5).** For the main inversion result, all prompts are 20 tokens long, which is very short. The mean inversion time of 28.01±35.87 seconds also has a standard deviation exceeding the mean, indicating a highly skewed distribution that is not discussed.

### Trivial

7. **The algorithm name is inconsistent throughout the paper.** It appears as "SIFT" (abstract, introduction, Figure 1, Section 4.2), "SIPIT" (Section 3 heading), "SIpIT" (Algorithm 1, Theorem 3.1), and "SiPT" (Tables 4 and 5, Section 4 body). This does not affect technical content but signals poor manuscript preparation.

## Nice-to-Haves

- The collision-search threshold of 10⁻⁶ for L2 distance should be justified. Why 10⁻⁶ rather than machine epsilon for the representational range?
- A larger-scale inversion study (hundreds to thousands of prompts) would make the empirical demonstration more persuasive.
- The paper could more explicitly discuss the relationship between the embedding layer and potential near-collisions (the minimum L2 distance between distinct token embeddings).

## Removed Points

These points from the input review are flagged for removal; treat them with caution:

- **"SiPIT requires per-position states, not just last-token"** — Removed: the paper explicitly acknowledges this limitation (line 141: "designing an efficient algorithm for that setting is nontrivial and left to future work; here we assume access to all per-position states"). This is honest scoping, not a flaw.
- **"Abstract overstates scope from 'last-token' to 'sequence of representations'"** — Removed: injectivity of the last-token map implies injectivity of the full hidden-state matrix map (since the matrices differ in the last row), so the abstract's phrasing is technically correct.
- **"Related work distinction unclear"** — Removed: the paper clearly differentiates itself from Sutter et al. (2025) by noting Sutter proves injectivity "at initialization" while this work claims it "persists under training," and distinguishes last-token injectivity from full-matrix injectivity.
- **"Loss being real-analytic not argued explicitly"** — Removed: Theorem 2.1 establishes the map as real-analytic in parameters; the loss is a composition of this with softmax and cross-entropy, which are real-analytic. This is adequately covered for a sketch.
- **"Theorem 2.2 construction too brief / LayerNorm concern"** — Removed: this is a sketch; the full proof is in the appendix. Per policy, complaints about missing appendix content are removed.
- **"Embedding layer role not discussed"** — Removed: the paper discusses exactly this possibility in the "Failure cases" section (line 125: "if two vocabulary items v_i≠v_j are assigned exactly the same embedding vector...").
- **"HARDPROMPTS baseline is uninformative"** — Removed: the paper acknowledges the comparison is imperfect (lines 293-311). While the comparison adds limited value, its inclusion is not a meaningful weakness.
- **"Standard deviation exceeding mean suggests skewed distribution"** — Merged into Minor weakness #6.

## Novel Insights

The input reviews surface one genuinely subtle point beyond the paper's own contributions: the training-preservation argument's sketch relies on the claim that a local diffeomorphism (where det Dφ≠0) preserves absolute continuity of pushforward measures. This is not trivial — it requires that φ has the Lusin N property, which holds for C¹ maps (since they are locally Lipschitz). The sketch does not mention this reasoning, creating a gap that, while likely bridgeable, undermines confidence in the paper's primary distinguishing claim. This nonlinear dynamical subtlety — that one cannot infer global measure-preservation from local invertibility alone — is a genuinely nuanced point worth flagging.

## Suggestions

1. Either (a) provide a rigorous justification in the main text that φ(θ)=θ−η∇ℒ(θ) preserves absolute continuity under the GD flow (e.g., by noting C¹ maps are locally Lipschitz and thus have the Lusin N property, so the pushforward of an absolutely continuous measure is absolutely continuous), or (b) honestly reposition the contribution as covering only initialization and clearly state the distinction from Sutter et al. (2025).

2. Replace unqualified "probability one" statements with precise qualifications ("with probability one over the random initialization in the Lebesgue-measure sense over ℝᴺ") and add a paragraph discussing the real-to-float transition and why the result remains practically relevant despite it.

3. Restructure the empirical section as illustrative rather than confirmatory, drop strong confirmatory language in the abstract and conclusion, and add the Thomas et al. (2025) baseline.

4. Resolve the algorithm-name inconsistency (SIFT/SIPIT/SIpIT/SiPT) throughout the manuscript.

## Score and Decision

**Score: 5.5**

**Decision: Borderline Accept**

**Rationale:** The paper's core theoretical contribution — establishing injectivity of decoder-only Transformers via real-analyticity — is genuinely clever and novel. However, the training-preservation argument (Theorem 2.3) is presented with an incomplete sketch in the main text, which is concerning because this claim is the paper's primary differentiator from prior work (Sutter et al., 2025 covers initialization only). The empirical evaluation is too thin to support the confirmatory framing. The paper's contribution is real but the presentation of its central technical claim needs to be strengthened. If the appendix closes the proof gap and the overclaiming is addressed, the paper would be a solid accept.

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Induction Heads (1lFZusYFHq) | 6.20 | R1, R2 | Similar theoretical-transformers paper, rejected for simplified setup; current paper is more novel but has a proof gap |
| VICL Transformers (YE6N8htoFQ) | 6.00 | R2 | Rejected due to unfixable proof gap; current paper's gap may be fixable in appendix |
| LM Are Implicitly Continuous (SMK0f8JoKF) | 5.75 | R2 | Accepted despite thin experiments; current paper has stronger theory but a more significant gap |
| When Can Transformers Count (WULjblaCoc) | 5.60 | R1, R2 | Rejected; similar mix of theory + modest experiments |
| Transformer Encoder SAT (VVO3ApdMUE) | 5.50 | R2 | Accepted; complexity analysis, comparable score |
| Multi-Round Reasoning (MRPCIForrE) | 4.75 | R1, R2 | Rejected; incomplete proofs, less novel than current paper |
| Factual Recall via Associative Memories (hwSmPOAmhk) | 7.33 | R1 | Accepted; rigorous theory but on toy models — current paper is more ambitious but less polished |
| Transformers Reason with Abstract Symbols (STUGfUz8ob) | 7.60 | R1 | Accepted; rigorous theory with experiments — current paper's theory is less complete |

**Round 1 bracket:** 4.5–6.5. **Narrowing (Round 2):** The paper is above 4.5 (more novel than the Multi-Round Reasoning paper), but below 6.5 (the Induction Heads paper at 6.2 was rejected despite rigorous proofs; the current paper's main-text proof gap makes it weaker as presented). The most natural anchor is the "LM Are Implicitly Continuous" paper (5.75, accepted), which had interesting theory and thin experiments — the current paper has stronger theory but a more significant proof gap, roughly balancing to 5.5.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>