## Summary

This paper proposes a theoretical framework for understanding saddle-to-saddle learning dynamics and simplicity bias across a broad class of neural network architectures. It presents three tiers of contribution: (1) general landscape results showing that fixed points of narrow networks are embedded in wider networks (Theorem 1, extending Fukumizu & Amari) and that invariant manifolds are preserved under gradient flow (Theorem 3), both valid for any architecture fitting the general form of Equation (1); (2) dynamical analysis for two specific cases — two-layer networks with linear-in-u activations (data-driven timescale separation, Theorem 4) and quadratic-in-u activations (initialization-driven timescale separation, Proposition 5); and (3) testable predictions about the effects of width, data distribution, and initialization on plateau structure, validated in simulation.

## Strengths

- **Theorems 1 and 3 are genuinely general.** Theorem 1 extends the classic Fukumizu & Amari (2000) fixed-point embedding result with two new constructions (Equations 6 and 7) that are necessary for explaining the specific saddle types visited during learning. Theorem 3 identifies invariant manifolds (equal weights, zero weights, proportional weights, linear dependence) that are preserved under gradient flow for any architecture fitting the general form of Equation (1). These results are not architecture-specific and constitute the paper's most solid theoretical contribution.

- **Clean separation of two timescale mechanisms.** The distinction between data-induced timescale separation (linear case, Section 5.1: different singular values of Σ_yz cause directions to grow at different rates) and initialization-induced timescale separation (quadratic case, Section 5.2: different initial values cause units to grow at different rates) is insightful and is one of the paper's genuinely new conceptual contributions. This directly explains why different architectures show different patterns (low-rank vs. sparse weights during plateaus) and why data and initialization interventions have different effects across architectures.

- **The predictions in Section 6 are specific, testable, and non-trivial.** The prediction about width having little effect on linear networks but shortening plateaus in architectures with quadratic-in-u activations (Figure 2A), the prediction about data spectrum controlling plateau structure (Figure 2B), and the observation about initializing on invariant manifolds away from saddles producing a previously unobserved regime (Figure 2C) are concrete, falsifiable claims that go beyond merely fitting prior observations.

- **Intellectual honesty about scope.** The paper is clear that the dynamical analysis (Section 5) covers only two-layer networks with linear or quadratic activations, and that the deeper analysis of deep networks and general nonlinear activations remains conjectural. Lines 122, 202-203, and 227-228 explicitly delineate what is proven and what is conjectural.

## Weaknesses

### Fatal
None.

### Major

- **Framing-claims mismatch.** The abstract and introduction claim a universal dynamical theory across all listed architectures ("we show that linear networks learn solutions of increasing rank, ReLU networks learn solutions with an increasing number of kinks…"), but the formal dynamical analysis (Section 5) is proven only for two-layer networks with linear or quadratic-in-u activations. For ReLU and standard convolutional networks, Theorems 1 and 3 provide general landscape results (embedded fixed points and invariant manifolds), and Figure 1 shows empirical evidence, but the dynamical mechanism explaining *why* saddle-to-saddle dynamics occurs in those architectures is not proven — it remains conjectural. The paper is transparent about this limitation in the Discussion, but the abstract and introductory framing imply a stronger level of theoretical support than has been established.

### Minor

- **Unexplained symmetry assumption in Proposition 5.** The proposition assumes "Σ_yZ is symmetric" without justification in the main text. In the linear self-attention context where this analysis is meant to apply, it is not obvious why this matrix would be symmetric, and the main text does not explain or motivate this restriction.

- **Approximate dynamics lack rigorous error bounds.** Both Theorem 4 and Proposition 5 analyze approximate dynamics (dropping higher-order terms from the full gradient). The paper describes the approximations and provides intuition, but does not provide a formal bound on the approximation error or a guarantee of when it breaks down. This is a common limitation in theoretical deep learning papers but remains a gap between the analysis and the full conclusions about the dynamics.

- **Experimental validation on low-dimensional synthetic data only.** The experiments in Figure 2 use only 3 non-zero singular values following a power law. While appropriate for illustrating the theoretical predictions in a controlled setting, this does not demonstrate that the predicted effects hold in realistic high-dimensional settings. The paper's claims about practical implications rest on circumstantial evidence.

### Trivial
None.

## Nice-to-Haves

- Justify the Σ_yZ symmetry assumption in Proposition 5 (or relax it) in the main text rather than only in the appendix.
- Add at least one experiment with non-synthetic data (e.g., features from CIFAR, a simple text task) to strengthen the claim that predicted effects hold beyond controlled settings.
- Provide explicit error bounds for the approximate dynamics, at least for the linear case where standard perturbation theory applies.

## Removed Points

- *"The paper does not address whether the fixed points constructed in Theorem 1 are all possible embedded fixed points"* — The paper explicitly addresses this in the Discussion (line 236), stating it remains an open question.
- *"The note about connecting paths between embedded fixed points (line 118) is not proved"* — This claim references Appendix F.4. Per meta-instructions, weaknesses about missing appendix content are removed.
- *"Standard self-attention with softmax is not covered"* — The paper explicitly studies *linear* self-attention; the scope is clearly stated.
- *"The quadratic-case dynamics is less rigorous; transition from scalar intuition to matrix case not fully justified"* — This overlaps with the symmetry assumption point already listed as Minor.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Revise the abstract and introduction to clearly separate two tiers of contribution: (a) the general landscape results (Theorems 1 and 3) which apply to all architectures fitting Equation (1), and (b) the proven dynamical mechanism which covers two-layer linear and quadratic-in-u cases. For architectures like ReLU where only the landscape theory and empirical evidence apply, this should be explicit in the abstract rather than only in the Discussion.

2. Justify the Σ_yZ symmetry assumption in the main text — either by showing why it holds for the architectures of interest (e.g., linear self-attention with specific parameterizations) or by relaxing the assumption with a more general analysis.

3. Add a single experiment on a non-synthetic dataset (e.g., a simple image classification task with extracted features) demonstrating that the predicted width and data-spectrum effects hold qualitatively beyond synthetic toy data. This would substantially strengthen the claim of practical relevance.

## Score and Decision

**Calibration anchors used across rounds:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4xWQS2z77v.md | 8.00 | R1 | Yes | Loss landscape stationary points via convex duality — stronger proofs, narrower focus; higher score |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wFD16gwpze.md | 7.33 | R1, R2 | Yes | Similar theoretical depth on two-layer nets with power-law spectra — cleaner framing, comparable contribution |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/QibPzdVrRu.md | 6.50 | R1, R2 | Yes | Narrower focus (ReLU alignment only); our paper has broader architectural scope |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/3ROGsTX3IR.md | 5.80 | R1 | Yes | Grokking phase transitions — less rigorous, weaker presentation |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tMzPZTvz2H.md | 7.00 | R2 | No | Mean-field ResNet analysis — similar tier |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/AbXGwqb5Ht.md | 7.00 | R2 | No | Implicit regularization of ResNets — similar tier |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tNn6Hskmti.md | 6.25 | R2 | No | One-step SGD analysis — narrower focus |

**Bracket identified (Round 1):** 6.0–8.0

**Narrowing (Round 2):** Comparing weighted items: the paper's top strengths (10.60, 10.86, 11.09) are comparable to the 7.33 anchor's top strengths (9.44–13.28). The paper's highest-weighted weakness (approximate dynamics: 5.38) is similar in magnitude to the 7.33 anchor's mid-range weaknesses (~5–6). The framing mismatch weakness (2.14) is relatively mild by the model's assessment but is a genuine concern. The paper has better-scoped experiments than the 6.50 anchor but a less clean framing than the 7.33 anchor. The absence of a fatal weakness and the presence of genuinely novel theoretical contributions (new embedded fixed point constructions, invariant manifold theory applied across architectures) place this paper above the 6.5 tier but below the 8.0 tier where proofs are more complete.

**Final score: 7.0**

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>