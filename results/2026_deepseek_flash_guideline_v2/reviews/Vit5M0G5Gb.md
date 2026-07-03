## Summary

This paper proposes a theoretical framework for understanding simplicity bias in neural networks, arguing that stage-like learning (saddle-to-saddle dynamics) across fully-connected, convolutional, and self-attention architectures arises from a nested hierarchy of embedded fixed points connected by invariant manifolds. The framework characterizes fixed points (extending Fukumizu & Amari), proves invariant manifold structure, and provides dynamics analyses for linear and quadratic activation cases that reveal two distinct timescale separation mechanisms (data-driven vs. initialization-driven). The theory generates testable predictions about how width, data distribution, and initialization affect learning, which the paper validates with simulations.

---

## Strengths

1. **New embedded fixed-point constructions (Eqs. 6, 7) that extend prior work and are empirically necessary.** Remark 1 (lines 87-89) explicitly states that prior work (Fukumizu & Amari, 2000) discovered only Eqs. (4) and (5), while this paper adds the homogeneity-based (Eq. 6) and linearity-based (Eq. 7) constructions. Crucially, the saddles actually visited during learning "turn out to fall under Equations (5) to (7) but not Equation (4)" — these extensions are not merely technical but necessary to capture the observed dynamics. This is a concrete, verifiable theoretical advance over the prior state of the art.

2. **Disentangling data-induced from initialization-induced timescale separation with distinct, validated predictions.** Sections 5.1 and 5.2 identify two qualitatively different mechanisms: in linear networks the timescale separation arises from the singular-value spectrum of the data (Theorem 4), while in quadratic networks it arises from the random spread of initial weights across units (Proposition 5). Section 6 then derives differential predictions — equalizing singular values eliminates plateaus in linear but not quadratic networks (Figure 2B), and increasing width shortens plateaus in quadratic but not linear networks (Figure 2A) — and validates both with simulations. This is a novel decomposition not present in prior work that cleanly separates two distinct sources of stage-like dynamics with contrasting empirical signatures.

3. **Novel prediction about large low-rank initialization producing saddle-to-saddle dynamics without an initial plateau (Figure 2C).** The paper predicts and demonstrates a previously unobserved regime: initializing near an invariant manifold but away from saddles still yields saddle-to-saddle dynamics, but with an initial exponential drop followed by later plateaus rather than a plateau at the start. The paper explicitly notes this regime "has not previously been observed" (line 214) and uses it to add nuance to the view that exponential loss curves are a hallmark of lazy learning. This is a falsifiable, experimentally validated prediction that goes beyond cataloging existing phenomena.

4. **Recursive embedding across deep networks (Corollary 2, line 91).** Corollary 2 extends the fixed-point embedding from two-layer to depth-\(L\) networks by repeated application of Theorem 1, explicitly covering architectures with multiple layers each defined by Equation (1). This goes beyond Fukumizu & Amari (2000), who studied only two-layer networks.

5. **Clear delineation of when saddle-to-saddle dynamics fails (Section 7, lines 222-226).** The Discussion identifies two necessary conditions (escape path must follow invariant manifolds with few additional units; initialization must be near an invariant manifold) and gives concrete counterexamples — tanh networks violate the first condition, and large random initialization violates the second. This delimits the theory's scope rather than claiming universality without qualification, which is good scientific practice.

---

## Weaknesses

### Fatal
None.

### Major

1. **Theoretical dynamics analysis does not cover ReLU networks despite the paper's framing claiming it does.** The abstract and introduction present ReLU networks as part of the paper's theoretical contribution: "we show that... ReLU networks learn solutions with an increasing number of kinks" (abstract). However, the rigorous dynamics analysis in Section 5 is explicitly restricted to two-layer networks where \(\phi(\mathbf{x}; \mathbf{u})\) is a homogeneous **polynomial** in the weights \(\mathbf{u}\) — specifically the linear (degree 1) and quadratic (degree 2) cases (line 122). ReLU is degree-1 homogeneous but is **not a polynomial** and is not linear in \(\mathbf{u}\), so neither the Section 5.1 analysis (linear dynamical system, Equation 10) nor the Section 5.2 analysis (quadratic dynamics, Equation 14) applies to ReLU. The paper provides no theoretical derivation of how the dynamical mechanism of saddle-to-saddle dynamics arises in ReLU networks specifically — it only shows the phenomenon empirically (Figure 1D-E). The fixed point analysis (Theorem 1(iii)) and invariant manifold analysis (Theorem 3(iii)) do apply to ReLU via its homogeneity, but the claim in the abstract conflates "theoretical explanation" with "empirical demonstration." This creates a gap between the paper's framing and its actual technical content. This is fixable — either narrow the abstract/introduction to accurately describe what is proven, or provide a dynamics analysis for ReLU.

### Minor

2. **Experimental validation is almost entirely qualitative despite the theory making specific quantitative predictions.** Theorem 4 predicts that the projection on the non-dominant subspace scales as \(O(\varepsilon^{1 - s_{r+1}/s_1})\). Proposition 5 makes quantitative predictions about unit growth scaling relative to initialization. Yet the experiments validate predictions only through visual inspection of loss curves — plateau duration is not measured as a function of spectral gaps, initialization scales, or width, and no error bars are reported. For a theoretical paper, qualitative consistency with key predictions is a reasonable first check, and the predicted *differential* effects (e.g., width shortens plateaus in quadratic but not linear networks) are genuinely demonstrated. However, the paper would be substantially stronger with even basic quantitative measurements (e.g., measured vs. predicted plateau duration scaling as a function of the spectral gap from Theorem 4). As it stands, the evidence that the theory captures the dynamics at a quantitative level is suggestive but not conclusive.

3. **Figure 1 panel labeling error.** Lines 97-99 list panel (E) under both the "Equation (6)" and "Equation (5)" categories. This needs correction.

### Trivial
None.

---

## Nice-to-Haves

- The paper mentions the NTK / lazy-learning literature in passing (lines 13-14, 214) but does not systematically discuss how the saddle-to-saddle framework relates to or differs from the rich-vs-lazy framework, which also addresses when networks learn simple features and how initialization scale matters. A brief discussion would strengthen the paper's positioning against alternative theoretical frameworks.
- The analysis uses gradient flow (infinitesimal learning rate); a comment on expected robustness to finite step sizes and different optimizers (SGD, Adam) would be useful, though this is standard practice for theoretical work.

---

## Removed Points

These points were raised by reviewers but are excluded from the final assessment for the reasons stated:

- **"Unified" framing overstates the nature of unification:** The critic argued that two mechanistically distinct cases (data-driven vs. initialization-driven) undermine the "unified" framing. However, the paper achieves genuine unification at the level of fixed points and invariant manifolds (Sections 3-4), which apply to all architectures in Equation (1) regardless of the specific dynamics. The distinction between two mechanisms is a *finding* of the analysis, not a failure of unification. Removed as a semantic disagreement not supported by the paper's actual technical achievement.
- **Missing comparison to rich-vs-lazy / NTK frameworks:** Per meta-review instructions, missing related works are not to be mentioned as weaknesses since I cannot independently verify the literature. The paper does cite this work. Level of engagement is a scope choice.
- **No discussion of optimization algorithm beyond gradient flow:** Standard practice for theoretical work at a venue like ICLR; not a weakness.
- **ReLU not covered by any theoretical analysis (strawman variant):** The critic's claim that the paper provides *no* theoretical explanation for ReLU is partially true for the dynamics analysis but false for the fixed point analysis (Theorem 1(iii)) and invariant manifold analysis (Theorem 3(iii)), both of which apply to ReLU via degree-1 homogeneity. The retained Major weakness (point 1 above) captures the genuine gap accurately without overstating it.

---

## Novel Insights

None beyond the paper's own contributions. The reviews do not identify a perspective or implication that the paper itself does not already articulate or implicitly contain.

---

## Suggestions

1. **Revise framing to match scope.** The abstract and introduction should clearly distinguish between: (a) what is proven theoretically for all architectures in Equation 1 (fixed point and invariant manifold structure), (b) what is proven for polynomial activations (dynamics analysis with timescale separation), and (c) what is demonstrated empirically with theoretical structural support (ReLU, convolutional, deep networks). The paper's genuine theoretical contributions stand on their own without overclaiming.

2. **Add quantitative validation of at least one prediction.** For instance, measure plateau duration as a function of the spectral gap in linear networks and compare against the \(O(\varepsilon^{1-s_{r+1}/s_1})\) scaling from Theorem 4. Even a single quantitative match (with error bars) would substantially strengthen the evidence that the theory captures the dynamics quantitatively.

3. **Correct the panel labeling error** in lines 97-99 where panel (E) appears under both Equation (5) and Equation (6) categories.

---

**Calibration note:** The calibration search tool was unavailable due to a database access error. Score is based on direct assessment of the paper and reviews against ICLR standards.

## Score and Decision

**Score: 6**

**Decision: Accept**

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>