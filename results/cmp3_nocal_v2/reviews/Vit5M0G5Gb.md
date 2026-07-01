## Summary

This paper develops a theoretical framework for understanding stage-like learning (saddle-to-saddle dynamics) across neural network architectures. It presents three contributions: (1) a unified treatment of embedded fixed points in the loss landscape, extending prior constructions (Fukumizu & Amari, 2000) to convolutional and self-attention layers (Theorem 1); (2) invariant manifolds that correspond to effectively narrower networks (Theorem 3); and (3) a dynamics analysis showing how timescale separation—from either data structure or initialization—can drive gradient flow along these manifolds, producing the characteristic staircase-like loss curves. The framework yields testable predictions about how width, data distribution, and initialization affect the duration and number of plateaus.

## Strengths

1. **A genuinely unified geometric treatment across architectures (Theorems 1 and 3).** Prior work studied fixed-point hierarchies in two-layer fully-connected nonlinear networks. This paper extends those constructions to convolutional layers, self-attention, and homogeneous activations in a clean, architecture-agnostic formalism (Equation 1). Theorem 1's four-part construction cleanly separates what holds for any activation from what requires specific algebraic structure (zero, homogeneity, linearity). Theorem 3's invariant manifolds are a novel addition that connects the landscape geometry to the simplicity of the network's input-output map. These are rigorous results with proofs in the appendix.

2. **The distinction between data-induced and initialization-induced timescale separation (Sections 5.1 vs. 5.2).** The paper identifies two qualitatively different mechanisms that produce saddle-to-saddle dynamics: one where singular value gaps in the data drive sequential rank increase (linear networks), and one where random initial-weight gaps drive sequential unit recruitment (quadratic networks / linear self-attention). This distinction is novel, physically meaningful, and leads to distinct predictions (e.g., width helps in one case but not the other).

3. **Concrete, testable predictions (Section 6).** The predictions about how width, data power-law exponent, initialization structure, and initialization scale affect plateaus are specific and non-trivial. The prediction that increasing width shortens plateaus in linear self-attention but not in linear fully-connected networks (Figure 2A) is particularly sharp and is supported by simulations.

## Weaknesses

### Fatal

None.

### Major

1. **The dynamics analysis (Section 5) is substantially less rigorous than the landscape analysis (Sections 3–4), creating a gap between the paper's central explanatory claim and the evidence provided.** The paper transparently describes Section 5 as "heuristic arguments" (line 118). Nevertheless, the title and abstract frame the paper as *explaining* saddle-to-saddle simplicity bias, and this explanation depends critically on the dynamics analysis:

   * For the linear case (Section 5.1): Theorem 4 analyzes the *linearized* dynamics (Equation 10), which drops the \(- \mathbf{W}\boldsymbol{\Sigma}_{zz}\) term from the full gradient flow (Equation 9). The paper acknowledges this is valid only "near small initialization" (line 138), but no bound is given on how long the approximation remains valid or how close the trajectory stays to the invariant manifold. The conclusion that weights align with top singular vectors is proven for the linearized system, but it is not proven that the full nonlinear dynamics follows the same trajectory long enough to reach the invariant manifold.

   * For the quadratic case (Section 5.2): The key intuition is illustrated with the scalar model \(\dot{v}_i = v_i^2\), which decouples the units entirely. The paper acknowledges "the general case, analyzed in Appendix H.2, is more complicated" (line 186), but the claim that "the timescale separation between units essentially comes from the same mechanism" (line 186) is stated as intuition rather than derived from the coupled dynamics of Equation (14).

   * The "higher-order polynomial" and "general nonlinear activation" subsections (lines 192–202) are explicitly conjectural (the paper says "we conjecture," line 192) and serve as discussion of extensions rather than analysis.

   **Why this matters**: The rigorous Theorems 1 and 3 establish the landscape geometry (fixed points exist, invariant manifolds exist). They do not by themselves prove that gradient flow traverses these points in order. The dynamics analysis bridges this gap, and its heuristic nature means the central claim — that saddle-to-saddle dynamics *explains* the simplicity bias — is less fully supported than the rigorous landscape results would suggest. This is not fatal: the heuristic analysis makes specific, testable predictions that the simulations support. But the framing overstates the level of theoretical closure the paper achieves.

### Minor

2. **The abstract and introduction claim broader scope than the dynamics analysis delivers.** The abstract states the paper "show[s]" that linear, ReLU, convolutional, and self-attention networks learn solutions of increasing complexity (e.g., "increasing rank," "increasing number of kinks"). The rigorous dynamics analysis (Section 5) is only worked out for two-layer networks with polynomial activations (linear and quadratic). For ReLU, convolutional, and deep networks, the dynamics analysis is not carried out — the paper relies on the landscape results (Theorems 1, 3) plus empirical demonstration. Section 7 appropriately scopes this ("the analysis of dynamics in Section 5 only applies to two-layer networks," line 228), but the abstract and introduction would better serve readers by matching this measured tone. The phrase "a universal mechanism" (line 27) is also too strong given that the paper's own Section 7 identifies non-trivial conditions for saddle-to-saddle dynamics and acknowledges the tanh case as a counterexample.

3. **The conditions under which embedded fixed points are saddles (rather than local minima) are referenced but not stated.** The paper states (line 93): "They are guaranteed to be saddles in deep linear networks... and, under mild conditions, are saddles in general architectures (Fukumizu & Amari, 2000; Fukumizu et al., 2019)." Since the entire saddle-to-saddle narrative requires these points to have unstable directions for escape, stating the "mild conditions" explicitly would let readers assess applicability to specific architectures without consulting external references. This is a self-containedness gap.

### Trivial

None.

## Nice-to-Haves

1. **Quantitative evidence for the mechanism in simulations.** The paper shows loss curves and final weight configurations but does not quantitatively track whether the trajectory follows the predicted invariant manifolds (e.g., effective rank over time, cosine similarity between weight trajectory and invariant manifold tangent space). Such measurements would strengthen the claim that the heuristic dynamics analysis correctly captures the mechanism.
2. **State the "mild conditions" for embedded fixed points to be saddles explicitly** (from Fukumizu & Amari, 2000; Fukumizu et al., 2019) in the main text.
3. **A summary table mapping each architecture** to whether Theorem 1 applies, Theorem 3 applies, the dynamics analysis is rigorous or heuristic, and whether saddle-to-saddle dynamics is empirically observed, would clarify scope at a glance.
4. **A brief discussion of whether the results extend to discrete gradient descent** (vs. gradient flow) would be useful, since practical training uses finite step sizes that can escape saddles differently.

## Removed Points

These points from the input review are removed or demoted per filtering rules:

- **Criticism that the "higher-order polynomial activation" and "general nonlinear activation" subsections are "entirely speculative."** The paper explicitly says "we conjecture" (line 192) and is transparent about the exploratory nature. This is standard practice in theory papers and not a weakness.
- **Criticism about lack of discussion of batch normalization, LayerNorm, or normalization layers.** These modify the architecture in ways that break Equation (1)'s structure; discussing them is outside the paper's stated scope.
- **Criticism about non-standard notation for self-attention (Equation 2) reducing readability.** The paper acknowledges this, and the reviewer notes it is "not a flaw." Removed as not a weakness.
- **Criticism about missing comparison to alternative mechanisms or baselines.** Demanding baselines for a theory paper's supporting simulations is scope creep; the paper's predictions are architecture-specific and the simulations test them directly.
- **Criticism about missing discussion of discrete gradient descent.** This is a nice-to-have, not a weakness. Moved to Nice-to-Haves.
- **Strength 4 ("intellectual honesty about scope").** Conflicts with verified weakness #2 (abstract overclaims relative to what the dynamics analysis delivers). When a strength and weakness disagree, the weakness wins.
- **Criticism about simulations being only on small synthetic problems.** The paper is primarily theoretical; small-scale simulations that test the qualitative predictions are standard and appropriate for a theory paper.

## Novel Insights

The most penetrating insight from the review process is that the paper's contribution is fundamentally two-tiered: the landscape geometry (Theorems 1, 3) is rigorous and broadly applicable, while the dynamics analysis (Section 5) is heuristic and architecture-specific. The paper would be stronger if it more sharply marked this boundary in its front matter, rather than using "show" uniformly across both tiers. A reader who evaluates only the rigorous tier gets a clean geometric characterization of where simple solutions sit in weight space; a reader who accepts the heuristic tier gets a mechanistic story for how gradient flow finds them. The gap between these tiers is the paper's central vulnerability but also its most interesting open direction.

## Suggestions

1. Reword the abstract and introduction to match the paper's actual scope — specifically, state that the rigorous dynamical analysis is carried out for two-layer networks with polynomial activations, and that extensions to other architectures are supported by the landscape results, heuristic reasoning, and empirical validation.
2. State the "mild conditions" for embedded fixed points to be saddles explicitly (this is a quick fix).
3. Add a quantitative plot of effective rank over training time for at least one architecture (e.g., linear network) to directly show the stepwise rank increase predicted by the theory.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>