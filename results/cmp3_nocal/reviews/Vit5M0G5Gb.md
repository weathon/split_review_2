Now I will write the final consolidated review.

## Summary

This paper develops a theoretical framework for understanding saddle-to-saddle dynamics and simplicity bias across neural network architectures. The key contributions are: (1) extending the theory of embedded fixed points (Fukumizu & Amari, 2000) to a broader class of architectures, adding two new constructions (Theorem 1); (2) proving that invariant manifolds corresponding to effectively narrower networks exist under gradient flow (Theorem 3); (3) analyzing gradient flow dynamics for two-layer linear and quadratic networks, showing that distinct singular values of the input-output correlation induce data-driven timescale separation (Theorem 4), while distinct initializations across units induce initialization-driven separation (Proposition 5); and (4) experimentally validating predictions about the effects of width, data distribution, and initialization.

## Strengths

1. **A unified notational framework spanning multiple architectures.** Equation (1) captures fully-connected, convolutional, and self-attention layers in a single formalism. The self-attention mapping (Equation 2) is non-standard but correctly shows that all three architectures fit within the same layer definition. This enables a genuinely cross-architectural treatment of fixed points and invariant manifolds that goes beyond the prior work of Fukumizu & Amari (2000), who studied only fully-connected networks.

2. **Extension of embedded fixed points beyond prior work.** Theorem 1 adds two new constructions (Equations 6-7) to the two from Fukumizu & Amari (Equations 4-5). Remark 1 explains that the saddles actually visited during learning fall under the new constructions rather than the old ones — a self-contained empirical finding that gives this extension significance. Corollary 2 extends this inductively to deep networks.

3. **Clean conceptual separation of two timescale-separation mechanisms.** The distinction between data-induced timescale separation (linear case → low-rank weights) and initialization-induced timescale separation (quadratic case → sparse weights) is clearly motivated, formally stated in Theorem 4 and Proposition 5, and experimentally demonstrated. This gives the field a usable classification for reasoning about when stage-like dynamics will arise and what structural form it will take.

4. **Specific, falsifiable predictions validated experimentally.** Section 6 contains predictions about the effect of width (increasing H has little effect on linear networks but shortens plateaus in linear self-attention), data distribution (flattening singular values eliminates plateaus in linear but not quadratic networks), and initialization (large low-rank initialization produces saddle-to-saddle dynamics without an initial plateau). These predictions are non-obvious and are supported by simulations. The large low-rank initialization regime (Figure 2C) is genuinely novel.

5. **Intellectual honesty about limitations.** The paper explicitly states where the dynamics analysis is heuristic rather than rigorous (line 118: "we develop heuristic arguments"), where the analysis is limited to two-layer networks (lines 122, 228-229), and where conclusions are conjectural (deep networks, higher-order polynomial activations, general nonlinear activations). This transparency is commendable.

## Weaknesses

### Fatal
None.

### Major

1. **Framing gap between the general-architecture claims and the actual dynamics analysis.** The title ("across neural network architectures"), abstract, and introduction claim a universal theoretical framework, but the rigorous dynamics analysis (Section 5) covers only two-layer networks where φ is linear or quadratic in the weights. ReLU networks, convolutional ReLU networks, and general nonlinear activations appear in Figure 1 and are discussed as empirical demonstrations, but are not covered by the dynamics theory. The paper acknowledges this at lines 122 and 228-229, which is commendable, but the abstract's phrasing—"we show that linear networks learn solutions of increasing rank, ReLU networks learn solutions with an increasing number of kinks, convolutional networks learn solutions with an increasing number of convolutional kernels"—mixes theoretical results (linear case) with experimentally-observed phenomena (ReLU, convolutional) under a single "we show" claim without distinguishing the epistemic status of each. A reader may reasonably conclude the theory covers all architectures shown. The paper would be stronger if the title and abstract specified which claims are proven results vs. empirical observations vs. conjectures.

2. **The connection between invariant manifold theory (Theorems 1, 3) and the dynamics analysis (Section 5) is heuristic, not rigorous.** The paper honestly acknowledges this at line 118 ("heuristic arguments"), but it remains a structural gap in the paper's central narrative. Theorem 3 guarantees that **exact** satisfaction of a constraint is preserved under gradient flow, but the dynamics analysis (Theorem 4, Proposition 5) only shows that weights become **approximately** rank-r (linear case) or that one unit dominates while others are **approximately** zero (quadratic case). These are not exact invariant manifold conditions. The claim that the network "evolves near the invariant manifold and approaches a fixed point on it" (line 152) requires a perturbation analysis—showing that approximate satisfaction of the condition is approximately preserved, or that the true dynamics converges to a point near the manifold. This analysis is not provided. The paper's core thesis—that saddle-to-saddle dynamics arises from the interplay of embedded saddles and invariant manifolds—remains a well-motivated explanation rather than a proven theorem, even for the linear case where the analysis is most complete.

### Minor

1. **Theorem 4 analyzes a linearized system, and the gap from the approximation to the conclusion is not bridged.** Theorem 4 analyzes the linear system in Equation (10), obtained from Equation (9) by dropping the O(ε²) term (WΣ_zz). This approximation is valid when weights are small (‖W‖ = O(ε²)). But the theorem's conclusion concerns what happens "when the projection of the weights on the span of the top r singular vectors reaches O(1)" — i.e., when weights are no longer small. At that point, the dropped term is O(1) and the approximation is no longer valid. The paper uses Theorem 4 to characterize the *escape direction from the saddle*, which is a plausible argument, but it does not analyze whether the actual nonlinear dynamics remains on the trajectory suggested by the linearized analysis once weights leave the small-initialization regime. Engaging with center manifold theory or stable manifold theory could potentially formalize this transition.

2. **Remark 1's claim about which saddle constructions are "visited during learning" is an empirical observation, not a theorem.** The remark states that the saddles visited during learning "turn out to fall under Equations (5) to (7) but not Equation (4)." This is presented as part of the theoretical framework but is in fact an observation from the paper's own experiments. It should be explicitly prefaced as an empirical finding, which would not diminish its value but would improve precision.

### Trivial

1. The notation in Equation (9)—(Σ_yz − WΣ_zz)_{ii}—is ambiguous when N_v ≠ N_u, as the "(ii)-th element" of a non-square matrix requires clarification.

## Nice-to-Haves

1. **Error bars / multiple seeds** for the experimental loss curves in Figures 1 and 2. Showing that the qualitative behavior is reproducible across random initializations would strengthen the empirical claims.

2. **Quantitative comparison between theory and experiment.** Theorem 4 suggests that plateau duration scales with log(1/ε)/s₁. Testing this prediction quantitatively against simulations would be far more convincing than the qualitative loss-curve plots currently provided.

3. A more precise title and abstract that distinguish between architectures covered by the dynamics theory (two-layer linear and quadratic networks) and those demonstrated empirically (ReLU, convolutional, general nonlinear). This would not reduce the paper's value but would improve scholarly precision.

## Removed Points

These points from the input review are removed with justification:

- **"The paper does not discuss the role of the loss function"** — The paper explicitly states the loss function requirements on line 49 ("ℓ is second order differentiable with respect to f(x), including common choices like squared error loss"). The dynamics analysis in Section 5 uses squared loss. The mention of RL/SSL in the introduction is contextual motivation, not a claim to have analyzed those settings. This criticism misreads the paper's scope.

- **"The self-attention mapping obscures actual structure"** — The paper acknowledges this on line 47: "We note that this is not a common notation for self-attention; we present it solely to show that Equation (1) incorporates self-attention." The paper already addresses this concern.

- **"Proof deferred to appendix" complaints** — The hard rules for this review remove criticisms about proofs or material being deferred to the appendix, as those sections are stripped from the submission by the parser.

- **"The analysis of subsequent saddle-to-saddle iterations (lines 154-158) is sketchy"** — This criticism references material that is deferred to Appendix G.3, which is stripped. The main text provides a sketch and references the appendix; per the review guidelines, this is removed.

- **"The scalar ODE v̇ = v² blows up in finite time, which is qualitatively different from gradient flow on a quadratic network"** — This misreads the paper's intent. The scalar ODE is explicitly presented as giving "a flavor of such dynamics" (line 178), not as a rigorous derivation. The paper states that the general case is "analyzed in Appendix H.2" (line 186). This is an illustrative example, not a flawed proof.

- **"The paper should have cited center manifold theory"** — The absence of a specific reference is not a weakness per se; this is a suggestion for strengthening, not a flaw.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's stated contributions and identify a framing gap between the general-architecture claims and the actual scope of the dynamics analysis, but raise no genuinely novel observation about the paper's content that the paper itself does not already articulate.

## Suggestions

1. Revise the title and abstract to clearly distinguish which claims are proven theoretically, which are empirically demonstrated, and which are conjectured. For example, replace "across neural network architectures" with a more precise formulation.
2. Add error bars or multiple-seed visualizations to the experimental figures.
3. Provide at least one quantitative test of a theoretical prediction (e.g., plateau duration as a function of initialization scale or singular value gap).
4. Formalize the "near the invariant manifold" argument — even a conjecture about why approximate satisfaction of an invariant manifold condition is approximately preserved would strengthen the link between Sections 4 and 5.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>