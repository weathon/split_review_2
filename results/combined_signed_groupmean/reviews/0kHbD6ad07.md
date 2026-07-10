Now I have a thorough understanding of the calibration landscape. Let me produce the final consolidated review.

## Summary

This paper proves that decoder-only Transformer language models are almost-surely injective (different prompts → different last-token hidden states) using real-analyticity arguments, and shows this property persists at initialization and during training. It introduces SIFT/SIPIT, an algorithm that reconstructs exact input prompts from per-position hidden states with linear-time guarantees. Empirical collision searches across six model families find no collisions.

## Strengths

- **Elegant theoretical proof framework (Theorems 2.1–2.2).** Using real-analyticity to show collision sets have measure zero at initialization is a genuinely counterintuitive and non-obvious claim, made rigorous through a clean proof strategy.
- **Large-scale empirical collision search.** ~5B pairwise comparisons across six model families (GPT-2, Gemma-3, Llama-3.1, Mistral-7B, Phi-4, TinyStories) at multiple layers and under quantization, confirming no collisions with distances far above machine epsilon.
- **Clear articulation of practical and regulatory implications (§6).** The discussion connecting injectivity to privacy and data-protection obligations when hidden states are cached or transmitted is a valuable contribution to the policy conversation.

## Weaknesses

### Fatal
None.

### Major

1. **Corollary 2.3.1 contains a mathematical error in the main text.** The argument claims the batch-update Jacobian determinant is nonzero because the single-sample Jacobian determinant is nonzero at θₐ, "by linearity of differentiation." The batch Jacobian is Dφ_B(θ) = I − η·(1/|B|)·Σᵢ ∇²Lᵢ(θ); even if each individual det(I − η∇²Lᵢ(θₐ)) is nonzero, it does NOT follow that det(I − η·(1/|B|)·Σᵢ ∇²Lᵢ(θₐ)) is nonzero. The determinant of a sum is not the sum of determinants, and the batch Hessian does not "coincide" with any single-sample Hessian without additional justification. This is a genuine mathematical error in a core argument that distinguishes the paper's novelty from prior work (Sutter et al., 2025). Whether the appendix contains a correct argument cannot be assessed from the main text.

2. **Theorem 2.3 (GD preservation) sketch leaves critical steps unsubstantiated.** (a) The claim that det(I − η∇²L(θ)) is "not identically zero" is hand-waved ("one can check this by evaluating at a simple parameter setting") with no justification in the main text. (b) The argument that a local diffeomorphism a.e. preserves absolute continuity of a pushforward measure conflates local invertibility (Inverse Function Theorem) with the measure-theoretic properties needed. These gaps matter because the training preservation claim is central to the paper's novelty over prior work.

3. **The empirical inversion evaluation is too small to be persuasive under the paper's own claims.** The main experiment uses 100 prompts of 20 tokens each on GPT-2 Small (Table 5); the quantized-model experiment uses 50 prompts of 10 tokens each (Table 4). For an algorithm whose abstract promises "demonstrating exact invertibility in practice," these sample sizes are inadequate to demonstrate robustness across diverse or challenging inputs, even as a sanity check for a theoretically-guaranteed algorithm.

### Minor

4. **The inversion algorithm's framing overstates its practical scope.** The abstract says SIFT "reconstructs the exact input text from hidden activations" without foregrounding that it requires access to all per-position hidden states at a given layer. While §3 honestly acknowledges this limitation and notes that recovery from only the final embedding is "left to future work," the abstract and introduction do not reflect this, potentially misleading readers about real-world applicability.

5. **The HARDPROMPTS baseline comparison is uninformative.** HARDPROMPTS is a prompt-optimization method, not designed for hidden-state inversion. Reporting 0.00 accuracy adds no useful information and may damage the paper's credibility. The paper would be stronger by omitting this comparison or replacing it with a genuinely comparable baseline.

6. **The BRUTEFORCE ablation is insufficiently described to interpret the 140× speedup.** The paper does not clarify whether the gradient-guided policy benefits from caching or other computational advantages unavailable to the uniform random policy, making it unclear how much of the speedup comes from better candidate ordering versus engineering optimizations.

7. **No discussion of numerical precision.** The theoretical result concerns exact equality in ℝᵈ, but computation uses floating-point arithmetic. Two mathematically distinct values could collide under finite precision, and the paper does not address this gap between theory and numerics.

8. **The collision threshold (10⁻⁶) and step-size constraint η ∈ (0,1) are stated without justification in the main text.**

### Trivial

9. **The algorithm name is used inconsistently throughout:** SIFT (abstract, §1, §4.2), SIPIT (§1, §3), SIpIT (Algorithm 1), SIpT (§4), SiPT (Tables 4, 5), SiPIT (§6). This harms readability.

## Nice-to-Haves

- Scaling the inversion experiments to thousands of prompts across varied domains and sequence lengths would strengthen the empirical claims without requiring any change to the algorithm.

## Removed Points

These points are flagged to be removed, treat them with caution:
- *Table captions inconsistency*: Removed as a formatting/presentation nitpick that does not affect scientific evaluation.
- *Critic's point about the measure-theoretic gap in Theorem 2.3 being conflated with local invertibility*: While the sketch is indeed informal, the conclusion is standard for C¹ maps with a.e.-nonzero Jacobian on bounded domains (Lipschitz maps satisfy Lusin's (N) property, which suffices). The gap is a presentation issue rather than an actual error, so this is subsumed into Major point 2 at a lower severity than the critic implied.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's analysis validated the paper's core theoretical framework while correctly identifying the mathematical error in Corollary 2.3.1 — this latter point is the most novel observation surfaced by the review process.

## Suggestions

1. **Fix the Corollary 2.3.1 argument.** Either provide a correct proof that the batch-update Jacobian determinant is nonzero (showing the claim holds without relying on the flawed "coincides" argument), or clearly limit the result to full-batch GD and remove the claim about SGD/mini-batch from the main result.
2. **Substantiate the Theorem 2.3 sketch.** Provide a concrete parameter setting where det(I − η∇²L(θ)) ≠ 0, and give a proper measure-theoretic justification for the pushforward argument.
3. **Substantially scale the inversion experiments** to match the strength of the claimed guarantees (e.g., thousands of prompts across varied lengths and domains).
4. **Remove or reframe the HARDPROMPTS comparison.** It is not informative.
5. **Add a discussion of finite-precision arithmetic** and how the measure-zero theoretical guarantee relates to floating-point collisions.
6. **Standardize the algorithm name** throughout.
7. **Justify the η ∈ (0,1) constraint and the 10⁻⁶ collision threshold.**

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8QTpYC4smR.md | 1.00 | R1 | No | Survey paper, strong reject — not comparable |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/fSbPwHjdDG.md | 3.00 | R1 | No | Empirical interpretability paper, weak theory |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/b5lXUwZiD3.md | 5.25 | R1 | Yes | Transformer limitations paper — rejected due to limited impact; sound theory but no mathematical errors. Our paper has a stronger core contribution but a mathematical error they lack. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1lFZusYFHq.md | 6.20 | R2 | Yes | Induction heads theory — rejected due to incremental contribution and simplified setting. Theory was sound. Our paper has a more novel claim but a mathematical error. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8p3fu56lKc.md | 6.00 | R2 | Yes | Linear self-attention theory — accepted despite limited significance and no experiments. The theory was sound. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6S4WQD1LZR.md | 6.67 | R3 | Yes | Universal approximation — accepted. Rigorous theory without mathematical errors. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NHhjczmJjo.md | 7.00 | R1 | Yes | L2O capabilities — accepted. Strong theory + experiments, no mathematical errors. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/STUGfUz8ob.md | 7.60 | R1 | Yes | Abstract reasoning — accepted. Rigorous theory, practical insights, no errors. |

**Round 1 bracket**: 4.5 – 6.5. The paper has genuine novel contributions (Theorem 2.2, collision search) that place it above pure-reject territory, but the mathematical error in Corollary 2.3.1 and undersized inversion experiments prevent it from reaching the 6+ band where accepted theoretical papers sit.

**Round 2 narrowing**: The paper is weaker than the 6.0 anchor (8p3fu56lKc.md, accepted despite limited significance) because that anchor's theory was sound while this paper contains a genuine mathematical error. It is comparable to the 5.25 anchor (b5lXUwZiD3.md, rejected) and the 6.2 anchor (1lFZusYFHq.md, rejected) in overall quality, but its error is more severe than those papers' weaknesses. The high-magnitude items that pull this paper down (−10.00 for the Corollary error, −9.97 for small experiments, −9.99 for HARDPROMPTS) are absent from accepted anchors. Conversely, the strengths (+10.00 for the core theory, +9.90 for collision search) are comparable to accepted papers' strengths. The balance places the paper just below the acceptance threshold.

**Final score: 4.5** — borderline reject. The core theoretical insight (Theorem 2.2) and collision-search experiments are valuable contributions, but the mathematical error in the SGD/mini-batch argument and the gaps in the GD preservation sketch undermine the paper's central novelty claim over prior work (Sutter et al., 2025). The inversion experiments are too small for the strength of the claimed guarantees. These issues are potentially fixable, but the paper in its current form does not meet the acceptance bar.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>