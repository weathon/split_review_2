Now I have a clear calibration picture. Let me write the final consolidated review.

## Summary

This paper investigates whether generative (decoder-based) or non-generative (encoder-based) approaches are better suited for compositional generalization in visual perception, with a focus on data efficiency. The authors formalize perception as inverting a generator, building on the function class ℱ_int (additive slot-wise functions with bounded polynomial interactions). They prove (Theorem 3.2) that when the ambient image dimension d_x ≥ d_z³ — the practical setting for images — the first and second derivatives of inverse generators g ∈ 𝒢_int can be arbitrary at a point, making it infeasible to constrain an encoder to 𝒢_int via practical means. In contrast, constraining a decoder to ℱ_int is straightforward via architecture or regularization. The paper proposes gradient-based search and generative replay to invert a decoder out-of-domain. Experiments on PUG datasets with controlled ID/OOD splits show that non-generative methods need large-scale pretraining to generalize compositionally, while generative methods with search/replay improve OOD accuracy without additional data.

## Strengths

- **Theorem 3.2 is a genuine theoretical contribution.** The result that when d_x ≥ d_z³ the first and second derivatives of inverse generators g ∈ 𝒢_int can be arbitrary at a point is non-trivial and provides a formal basis for why the constraints natural to impose on a forward generator (block-diagonal higher-order derivatives) do not transfer in any simple way to its inverse in high-dimensional ambient spaces. The contrast with Lemma 3.1 (where d_x = d_z the inverse retains structure) sharpens the point.

- **Clean experiment-design link.** The PUG datasets with three controlled splits (Background, Texture, Object) respectively probe n > 0 interaction cases and the n = 0 non-interacting case. The empirical pattern — non-generative methods fail on interacting splits unless heavily pretrained, and succeed on the non-interacting split — is consistent with the theory and genuinely informative. The fact that PUG-Object (n=0) yields near-perfect OOD accuracy for all methods serves as a useful sanity check that the task itself is not insurmountable.

- **Clear exposition of the formal framework.** Sections 2 and 3 are well-structured, with the mathematical setup (perception as inversion up to slot-wise reparameterizations, OOD identifiability via Eq. 2.5–2.6, the ℱ_int class) laid out with appropriate precision.

## Weaknesses

### Fatal

None.

### Major

1. **The headline claim is materially stronger than what the evidence and theory support.** The title asserts that "generation is required" for data-efficient perception, but the paper's own findings are more qualified. The theory (Theorem 3.2) shows that *explicitly guaranteeing* compositional generalization via constraints on an encoder is infeasible — not that generation is strictly *required*. The paper acknowledges this internally: "whether compositional generalization occurs depends on whether the optimization process happens to avoid converging to such a solution" (Sec. 3 Takeaways). The experiments corroborate this qualification: non-generative SigLIP2 reaches ~80% OOD accuracy on PUG-Background and ~85% on PUG-Texture, showing that non-generative methods *can* succeed with sufficient data. The paper's contribution is better captured by "generation enables stronger guarantees and better data efficiency for compositional generalization" rather than "generation is required." This is a framing issue, not a flaw in the science, but it misrepresents what the paper actually demonstrates.

2. **Missing statistical information undermines the experimental comparisons.** The paper reports OOD accuracy as point values in bar charts with no error bars, no mention of variance across runs, and no discussion of the number of random seeds or trials. For experiments comparing many models (six base encoders, multiple slot encoders, supervised vs. unsupervised), the reported "best-performing combination" (line 213) introduces selection bias whose magnitude is unknown. Without variance information, the reader cannot assess whether the observed differences between methods are meaningful. This is a significant omission for an empirical study that makes comparative claims.

### Minor

1. **The cubic condition d_x ≥ d_z³ lacks intuition.** Theorem 3.2's threshold is stated without explanation of where the cubic comes from. The reader is asked to take this condition on faith. A brief proof sketch or intuition (likely tied to a parameter-counting argument about degrees of freedom in the function class vs. constraints imposed by the derivative structure) in the main text would help readers assess the theorem's scope.

2. **PUG-Texture replay limitation and the role of search.** The paper acknowledges that replay cannot be applied to PUG-Texture (slots are designed to capture objects/backgrounds, not textures), meaning the generative advantage on this split comes *only* from gradient-based search — a general optimization procedure, not specific to generative models. The paper does not discuss whether analogous test-time refinement could be applied to non-generative encoders (e.g., optimizing encoder input latents to satisfy a consistency objective), or why it would not be feasible. This would help clarify whether the asymmetry is fundamental or incidental.

3. **The scope restriction to ℱ_int is more consequential for the central claim than acknowledged.** The paper assumes ground-truth generators belong to ℱ_int (Eq. 2.7) — additive slot-wise functions with bounded-degree polynomial interactions. While characterized as "the largest function class shown to enable OOD identifiability," this remains a specific structural assumption that excludes many real visual phenomena (occlusion, transparency, lighting, shadows, reflection). The limitations section (line 231) does acknowledge this, but the title and abstract do not carry this caveat. If real generators are not in ℱ_int, the theoretical guarantees for generative methods also vanish, and the argument for generation being required loses part of its foundation.

### Trivial

None.

## Nice-to-Haves

- Train an encoder with a regularizer that approximates the tangent-space constraint (Eq. 3.4) on 𝒳_ID, and measure whether this improves OOD generalization. The theory predicts it should not (because the constraint is manifold-dependent and OOD geometry is unknown), but a negative result would be stronger evidence than the current comparison.
- Provide intuition for the d_x ≥ d_z³ condition with a brief proof sketch in the main text.
- Discuss whether test-time optimization could be applied to non-generative encoders for OOD refinement, and if not, why the asymmetry is fundamental.

## Removed Points

The following points from the input review were removed per filtering rules:

1. **"The empirical comparison is structurally confounded"** — This argued that non-generative methods are compared against generative ones without controlling for decoder architecture, test-time computation, and synthetic data. However, the paper's unsupervised non-generative baseline (VAE) and generative method share the *same* decoder; the difference is solely whether the encoder output is used directly or the decoder is inverted via search/replay. Architecture is thus controlled. Test-time computation and synthetic data are definitional components of the "generative approach" being tested, not confounds. This criticism is not a valid weakness.

2. **Criticism about Figure 1 being confusing** — The confusion stems from a parser artifact in the extracted figure description. The original figure is described clearly in the surrounding text (lines 25–26, 29–31).

3. **Observation about Eq. (2.7) assuming polynomial interactions** — This is a transparent assumption inherited from prior work (Brady et al., 2025), not a weakness of this paper.

4. **Observation about generative replay circularity** — The fact that the ℱ_int-constrained decoder enables replay, and replay then validates the decoder, is a coherent design choice, not a logical flaw.

5. **Criticism about limitations section placement** — This is a presentation/style nitpick.

6. **Various points about missing appendix content** — The appendix is stripped by the parser; these are not author errors.

## Novel Insights

None beyond the paper's own contributions. The reviewer's suggestion to directly test whether encoder-side tangent-space regularizers fail (confirming the theory's prediction) — and conversely, whether the ℱ_int decoder architecture is necessary for search/replay gains — identifies a gap between the theory and experimental design that the paper does not fully bridge. The current experiments compare end-to-end systems rather than isolating the specific asymmetry the theory predicts.

## Suggestions

1. **Calibrate the central claim.** Reframe the title and abstract to match what is actually shown: that generative methods enable stronger *guarantees* and better *data efficiency* for compositional generalization, rather than asserting that generation is strictly *required*.
2. **Add statistical reporting.** Include error bars or confidence intervals for all reported OOD accuracies. Report the number of random seeds/trials. Clarify what "best-performing combination" means and how selection over slot encoder and fine-tuning choices is accounted for.
3. **Provide intuition for the cubic condition.** Add a brief explanation or proof sketch for why d_x ≥ d_z³ is the relevant threshold in Theorem 3.2.
4. **Discuss test-time optimization for non-generative encoders.** Address whether gradient-based search could be applied to refine encoder predictions on OOD data, and if not, why the asymmetry is fundamental rather than incidental.
5. **Surface the ℱ_int limitation more prominently.** Ensure the title and abstract reflect the scope of the theoretical assumptions.

## Score and Decision

**Calibration methodology.** I performed two rounds of RAG retrieval over a corpus of human-reviewed ICLR papers.

**Round 1 (bracketing):** Searched for papers on "compositional generalization generative vs non-generative perception" and "theoretical analysis of compositional generalization in visual perception OOD identifiability" across all score bands. This yielded the following relevant anchors:

- **Strong reject band** (< 3.5): "Compositional World Models with Interpretable Abstractions" (3.00, Reject), "Beyond Finite Data" (3.00, Reject), "Non-Parameterized Randomization" (2.33, Reject) — These papers either lacked theoretical contributions or had fundamentally flawed experimental designs. The current paper is clearly stronger than all of these.

- **Mid band (3.5–5.5):** "On Provable Length and Compositional Generalization" (5.25, Reject) — A theoretical paper on compositional generalization for seq-to-seq models that was rejected due to highly simplified models and strong assumptions. The current paper has more realistic experiments and a more grounded theoretical contribution. "Image Background Serves as Good Proxy for OOD" (5.33, Accept) — A more applied OOD detection paper. The current paper has a stronger theoretical component.

- **Upper-mid band (5.5–7.5):** "Provable Compositional Generalization for Object-Centric Learning" (7.33, Accept) — Very closely related: same area (compositional generalization via identifiability theory on autoencoders), similar approach (structural decoder assumptions). Accepted despite synthetic-only experiments and restrictive assumptions. "Interaction Asymmetry" (7.00, Accept) — Directly builds on the same ℱ_int framework the current paper uses; accepted with scores 6,8,6,8. "Dynamics of Concept Learning and Compositional Generalization" (6.50, Accept) — Accepted despite significant criticism about abstraction quality. "Discovering modular solutions that generalize compositionally" (6.50, Accept).

- **High band (7.5+):** "When can transformers reason with abstract symbols?" (7.60, Accept), "Compositional Entailment Learning" (8.00, Accept) — Papers with broader scope or more comprehensive evaluation. The current paper is not at this level.

**Initial bracket:** 5.5–7.5.

**Narrowing:** The most directly comparable anchors are "Provable Compositional Generalization for Object-Centric Learning" (7.33, Accept) and "Interaction Asymmetry" (7.00, Accept). Both are accepted papers with genuine theoretical contributions in the same area as the current paper. The current paper has more realistic experiments (PUG photorealistic images vs. purely synthetic) but also has two clear weaknesses those papers do not share: (1) a title/central claim that overstates what the evidence supports, and (2) a complete absence of statistical reporting (no error bars, variance, or seeds). These are fixable but real shortcomings.

I place the paper slightly below the 7.00–7.33 anchors, settling at 6.5. This reflects a genuine theoretical contribution and well-designed experiments, tempered by overclaiming that needs correction and missing statistical rigor that prevents the empirical findings from being fully interpretable.

**Final score:** 6.5
**Decision:** Accept (contingent on the authors addressing the two major weaknesses — claim calibration and statistical reporting — in revision).

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>