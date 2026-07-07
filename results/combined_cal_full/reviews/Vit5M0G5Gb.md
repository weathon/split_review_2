## Summary

This paper develops a theoretical framework for understanding saddle-to-saddle dynamics and simplicity bias across neural network architectures. It establishes two general structural results — Theorem 1 (embedded fixed points: fixed points of narrow networks persist as fixed points in wider networks) and Theorem 3 (invariant manifolds: weight relationships that make a wide network behave like a narrow one are preserved under gradient flow) — that apply to any network of the form in Equation (1), covering fully-connected, convolutional, and attention layers. The paper then provides a dedicated dynamical analysis for two-layer linear networks (showing data-driven timescale separation between directions leading to low-rank weights) and two-layer quadratic networks (showing initialization-driven timescale separation between units leading to sparse weights). These dynamical mechanisms are validated through simulations, and the paper makes specific testable predictions about the effects of width, data distribution, and initialization on learning dynamics.

## Strengths

- **Clean, general structural results (Theorems 1 and 3).** Theorem 1's characterization of embedded fixed points and Theorem 3's identification of invariant manifolds are genuinely architectural — they apply to any network fitting Equation (1), covering fully-connected, convolutional, and attention layers. The systematic treatment of four cases (any φ, zero, homogeneous, linear-additive) goes beyond Fukumizu & Amari (2000), and the paper explicitly notes that Equations (6) and (7) are new and crucial because the saddles visited during learning fall under these (Remark 1).

- **Novel disentanglement of data-induced vs. initialization-induced timescale separation (Section 5).** The linear case (Section 5.1) shows that distinct singular values of Σ_yz drive a timescale separation *between directions across all units*, leading to low-rank weights. The quadratic case (Section 5.2) shows that distinct initial weights drive a timescale separation *between units*, leading to sparse weights. This is a crisp theoretical distinction that unifies previously separate observations in the literature and traces the difference to the degree of the activation function in the weights.

- **Specific, testable predictions validated by simulations (Section 6).** The paper makes four concrete predictions about the effects of width, data distribution, initialization structure, and initialization scale — each grounded in theory — and validates them with controlled simulations (Figure 2). The prediction that equalizing singular values eliminates plateaus in linear networks but only shortens them in quadratic networks (Figure 2B) is sharp and discriminating, and the observation about initialization near invariant manifolds but away from saddles (Figure 2C) appears to be a novel finding.

- **Honest discussion of limitations (Section 7).** The paper explicitly acknowledges that the dynamical analysis applies only to two-layer networks, that the deep network discussion is conjectural, that the fixed points and invariant manifolds may not be exhaustive, and that the conditions for saddle-to-saddle dynamics can fail (tanh, large initialization). This level of candor is commendable.

## Weaknesses

### Fatal
None.

### Major

- **Gap between framing and actual theoretical scope.** The abstract claims to "show that ReLU networks learn solutions with an increasing number of kinks" and "convolutional networks learn solutions with an increasing number of convolutional kernels," and the title claims the framework "explains a simplicity bias across neural network architectures." However, the dynamical analysis that *produces* saddle-to-saddle behavior (Section 5) covers only two-layer networks with linear or quadratic activations. ReLU networks are not analyzed dynamically — ReLU is positively homogeneous (degree 1, case (iii) of Theorems 1 and 3) but not additive/linear (case (iv)), and the paper provides no theorem for ReLU analogous to Theorem 4 or Proposition 5. The ReLU demonstration is purely empirical (Figure 1D-E). The paper acknowledges this limitation indirectly ("the analysis of dynamics in Section 5 only applies to two-layer networks," line 228), but the abstract and introduction frame the contribution as a unified theoretical explanation *across architectures*. The structural results (Theorems 1 and 3) do apply broadly, but the core dynamical mechanism — timescale separation driving the system along invariant manifolds — is not theoretically established for ReLU networks or nonlinear convolutional networks. The paper would benefit from recalibrating its claims to match the proven scope, or extending the dynamical analysis to cover ReLU.

- **Approximate dynamics without formal error bounds.** Theorem 4 analyzes Equation (10), which is an approximation of the true gradient flow dynamics (Equation 9) obtained by dropping the O(ε²) term. Similarly, Proposition 5 analyzes an approximate dynamics (Equation 14). The paper does not provide formal bounds on the approximation error between the true and approximate dynamics, proofs that the true dynamics stays close to the approximate dynamics for the relevant timescales, or analysis of whether the approximation remains valid through saddle escape where weights grow substantially. The central claim — that "saddle-to-saddle dynamics operates by iteratively evolving near an invariant manifold, approaching a saddle, and switching to another invariant manifold" — is established rigorously only for the *approximate* linearized/quadratic dynamics. The link to true gradient flow is supported by simulations but not by proof. Adding even a heuristic error estimate would strengthen the argument considerably.

### Minor

- **Vague conditions for when embedded fixed points are saddles vs. local minima.** The paper states that embedded fixed points "are guaranteed to be saddles in deep linear networks... and, under mild conditions, are saddles in general architectures" (line 93), citing Fukumizu & Amari (2000) and Fukumizu et al. (2019). The "mild conditions" are never specified, and the paper does not indicate where in the cited works they appear. Since the paper's mechanism requires these fixed points to be saddles, this underspecification weakens the self-containedness of the theory.

- **The "universal mechanism" claim (line 27) overreaches.** The paper states "there is a universal mechanism, saddle-to-saddle dynamics, driving stage-like learning" but then identifies multiple cases where it fails (tanh networks, large initialization, architectures with full expressivity in a single unit). Given the paper's own discussion of conditions and failure cases, labeling the mechanism "universal" is imprecise and inconsistent with the paper's otherwise careful hedging.

### Trivial
None.

## Nice-to-Haves

- A dedicated dynamical analysis for ReLU networks would substantially strengthen the paper. Since ReLU is positively homogeneous of degree 1, it sits between the linear case (degree 1, additive) and the general nonlinear case — perhaps homogeneity properties could be leveraged directly.
- Formal error bounds connecting the approximate dynamics (Equations 10/14) to the true gradient flow (Equations 9/44), even if heuristic, would transform the mechanism from a plausible argument into a theorem.
- An explicit catalog in the paper of what is proved theoretically vs. shown empirically vs. conjectured would help readers calibrate the claims.

## Removed Points

These points were flagged by the harsh critic but are removed here with justification:

1. **Criticism that the simplicity concept is architecture-dependent / circular.** The paper transparently defines simplicity as "expressible with few hidden units" and explicitly notes that a "unit" means different things per architecture (neurons, kernels, heads). This is by design — it reflects the architecture's inductive bias. The abstract's "simplicity bias across architectures" refers to the same *principle* (recruiting fewer units) applying across architectures, not the same numerical measure. **Removed: not a real weakness; transparent and intentional design choice.**

2. **Criticism about self-attention notation being unusual.** The paper acknowledges "this is not a common notation" and uses it only to show that Equation (1) incorporates self-attention. **Removed: notation choice acknowledged by authors; not a substantive weakness.**

3. **Criticism that the scalar toy example for Proposition 5 doesn't cover the matrix case.** The paper explicitly states the general case is in Appendix H.2. Deferring proofs to an appendix is standard. **Removed: addressed in the paper.**

4. **Criticism about "initially developed rank-one weights" for tanh networks being a weakness.** The paper discusses this as a *violation case* (tanh networks do not exhibit saddle-to-saddle dynamics), not as a claimed success. This is the paper's own limitation analysis. **Removed: misattributed as a weakness; it is the paper's own admission of a limitation.**

5. **Criticism about missing analysis of when embedded fixed points are saddles (separate from the Minor weakness above).** The minor weakness about "mild conditions" is retained; the broader criticism that the paper should independently prove when fixed points are saddles rather than citing prior work is scope creep. **Removed: secondary point; citations to prior work are appropriate.**

## Novel Insights

None beyond the paper's own contributions. The reviewer's insights largely recapitulate the paper's own framing and limitations, which the paper itself acknowledges.

## Suggestions

1. Recalibrate the abstract's framing to match the proven scope: for ReLU and nonlinear convolutional networks, replace "show that" with "empirically demonstrate that" or "provide evidence that," and clarify that the dynamical analysis covers linear and quadratic two-layer networks while the structural framework applies more broadly.
2. Add a remark or table cataloging what is proved theoretically (Theorems 1, 3, 4, Proposition 5) vs. shown empirically (ReLU, nonlinear conv nets) vs. conjectured (deep networks, higher-order polynomial activations).
3. Consider adding a perturbation bound connecting the approximate dynamics (Equations 10 and 14) to the true dynamics, even if heuristic, to strengthen the link between the proven mechanism and actual gradient flow.

## Score and Decision

**Round 1 bracket:** 5.5–6.5

**Calibration anchors retrieved:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Aq35gl2c1k.md` (avg 5.00, critical learning periods in deep linear networks) — similar theoretical framing (linear networks, learning dynamics), but my paper has stronger structural results extending beyond linear networks and more specific testable predictions. Itemized: the 5.00 anchor's top weakness (-4.58, biological connection not supported) is comparable to my paper's top weakness (-4.99, framing gap), but my paper's top strengths (+6.06, +5.41) exceed that anchor's typical strength weights (+3.25–+5.29). My paper sits clearly above this anchor.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lYQLwP9c9S.md` (avg 6.00, 2-homogeneity & implicit bias) — similar in being a theory paper with structural results and some assumptions. Itemized: this anchor has stronger top positive weights (+7.18, +6.92) but also much more severe negative weights (-6.52, -6.07 questioning novelty and result coherence). My paper's negative weights are shallower (-4.99, -2.90) and the positive weights (+6.06, +5.41) are comparable. My paper is in a similar band but with a cleaner weakness profile.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iEfdvDTcZg.md` (avg 6.25, feature learning strength) — empirical-theoretical mixed paper. Itemized: this anchor has severe negatives (-7.21 questioning significance, -6.18 questioning practical relevance) that are absent from my paper, while my paper's top negative (-4.99) is more moderate. My paper's positives (+6.06, +5.41) are comparable to this anchor's (+5.98, +5.66).
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/STUGfUz8ob.md` (avg 7.60, transformers & symbolic reasoning) — stronger empirical validation and more ambitious scope. My paper does not reach this level; its weaknesses (framing gap, approximate dynamics) prevent it from sitting in this band.

**Final calibration rationale:** The paper's strongest contributions (Theorems 1 and 3, the timescale separation distinction) are genuinely novel and well-supported. The empirical validation (Section 6) is clean and the predictions are specific. However, the framing overreach about ReLU networks and nonlinear convolutional networks not backed by dedicated dynamical analysis (top weakness, weight -4.99), combined with the reliance on approximate dynamics without formal error bounds (-2.90), places the paper solidly in the 6 range. It clearly exceeds the 5.0 anchor's typical profile but lacks the scope and rigor of a 7+ paper. The paper would benefit from recalibrating its claims more carefully.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>