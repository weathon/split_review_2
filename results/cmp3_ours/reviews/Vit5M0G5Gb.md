## Summary

This paper develops a theoretical framework for understanding the simplicity bias in neural networks through saddle-to-saddle dynamics. It proves two main results: (1) Theorem 1 extends the classic Fukumizu & Amari (2000) embedded fixed point result with two new constructions (Equations 6 and 7) that are dynamically relevant; (2) Theorem 3 shows that weight relationships corresponding to effectively narrower networks (equal weights, proportional weights, linear dependence) are invariant under gradient flow. The paper then provides a dynamics analysis for two-layer linear (degree-1 homogeneous polynomial) and quadratic (degree-2 homogeneous polynomial) networks, showing how timescale separation—data-driven between directions or initialization-driven between units—guides trajectories along these invariant manifolds. Experiments across linear, ReLU, convolutional, quadratic, and linear self-attention networks validate predicted effects of width, data distribution, and initialization on learning dynamics.

## Strengths

1. **Theorems 1 and 3 are genuine theoretical contributions.** Theorem 1 extends the classic embedded fixed point result (Fukumizu & Amari, 2000) with two new constructions (Equations 6 and 7) beyond the original two (Equations 4 and 5). As Remark 1 correctly notes, the saddles visited during learning fall under the new constructions rather than the original ones, making this extension essential for the dynamics story. Theorem 3 (invariant manifolds) is arguably stronger: it shows that the same weight relationships that produce embedded fixed points are *dynamically preserved* under gradient flow, applying to the full class of networks defined by Equation (1). Together these provide a clean geometric picture: the loss landscape of a wide network contains nested substructures corresponding to narrower networks, and these substructures are dynamically attracting.

2. **The data-induced vs. initialization-induced distinction is conceptually illuminating.** The paper identifies two distinct mechanisms for timescale separation—between directions (driven by the singular value spectrum of the data) and between units (driven by random initialization). This cleanly explains why linear networks learn low-rank weights (Figure 1B,C) while quadratic networks learn sparse weights (Figure 1F,G), and makes testable predictions about how width and data structure affect dynamics (Figure 2A,B). This is a genuine synthesis that organizes disparate observations in the literature under a single geometric framework.

3. **The paper is unusually clear about its own limitations.** Section 7 explicitly discusses where the dynamics analysis applies (two-layer linear and quadratic homogeneous networks) and does not (tanh networks, large initialization), and which questions remain open (exhaustiveness of fixed points, deep networks). The "Condition for saddle-to-saddle dynamics" subsection provides a crisp characterization that helps readers assess when the theory applies.

## Weaknesses

### Fatal

None.

### Major

1. **Framing gap between the general geometric theory and the dynamical analysis.** The abstract claims the paper "explains a simplicity bias arising from saddle-to-saddle learning dynamics for a general class of neural networks" and the introduction states there is "a universal mechanism, saddle-to-saddle dynamics, driving stage-like learning" (line 27). However, the rigorous dynamics analysis (Section 5) is limited to two-layer networks where φ is a homogeneous polynomial of degree 1 or 2 in the weights. The general theorems (1 and 3) describe the *geometry* of the loss landscape—fixed points and invariant manifolds—which applies broadly to networks defined by Equation (1). But the *dynamical explanation* of how gradient descent actually follows saddle-to-saddle paths is only rigorously established for the specific cases analyzed in Section 5. For ReLU networks, convolutional networks with nonlinear activations, and general nonlinearities (all shown in Figure 1), the paper provides experimental evidence but no formal dynamics analysis. While Section 7 transparently states "the analysis of dynamics in Section 5 only applies to two-layer networks" (line 228), the abstract and introduction do not convey this scope, creating a misleading impression of the theory's breadth. The paper would be more honest—and stronger—if it presented itself as offering general *geometric foundations* for saddle-to-saddle dynamics, with detailed dynamical analysis for two illuminating special cases.

2. **The self-attention analysis conflates distinct architectural variants in a way that undermines the quadratic claim.** The paper claims linear self-attention fits into the quadratic framework (Equation 13) with "φ(x; u) a quadratic function of the key and query weights" (line 170). However, the definition of the self-attention unit in Section 2 (line 43) includes the softmax operation: φ(Z; K, Q) = I ⊗ smax(Z Q K^T Z^T) Z. The softmax involves exponentials of functions of K and Q and is not quadratic in these weights. The paper uses "linear self-attention" as a label but includes smax(·) in the formal definition without clarifying whether the experimental or theoretical analysis uses a softmax-free variant. This inconsistency raises real questions about whether the quadratic dynamics analysis genuinely applies to the standard self-attention mechanism or only to a simplified variant without softmax. The derivation in Equation (2) showing how self-attention fits Equation (1) does not resolve this—it shows the *structural* form but does not verify the *quadratic-in-weights* property claimed in Section 5.2.

### Minor

3. **The dynamics analysis is acknowledged as heuristic but the main-text language overstates its rigor.** While the paper flags Section 5 as developing "heuristic arguments" (line 118), the surrounding prose uses definitive language throughout. Theorem 4 analyzes an *approximate* linearized system (Equation 10), not the full dynamics (Equation 9); the justification that the full dynamics tracks this approximation is a heuristic order-of-magnitude argument (the O(ε²) terms are dropped because weights are initialized small). Subsequent iterations are described as "again approximately a linear dynamical system" (Equation 12) with the projection onto a subspace described but the approximation error not bounded. In the quadratic case (Section 5.2), Proposition 5 analyzes a simplified system (Equation 14) and the mechanism is illustrated with a scalar toy model (dv_i/dt = v_i²), with the leap to the full dynamics stated as "the timescale separation between units essentially comes from the same mechanism" (line 186). The connection between each approximate analysis and the actual full dynamics is not rigorously justified. This is common practice in deep learning theory, but the paper would benefit from more prominently distinguishing where rigorous proof ends and heuristic argument begins.

4. **Validation of predictions is qualitative rather than quantitative.** The paper's predictions about how width, data distribution, and initialization affect plateau lengths (Figure 2) are validated by visual comparison of loss curves. A more quantitative validation—e.g., measuring plateau lengths as a function of singular value gaps (linear case) or initialization variance (quadratic case) and comparing against a theoretical prediction—would substantially strengthen confidence that the approximate dynamics faithfully tracks the true dynamics. For a theoretical paper, qualitative validation is acceptable, but the claims about "predicting the effects of data distribution and weight initialization on the duration and number of plateaus" (abstract) would be better supported by a quantitative match.

### Trivial

None.

## Nice-to-Haves

- Quantitative validation of predicted plateau lengths as a function of singular value gaps or initialization variance.
- Clarification in the abstract and introduction that the general geometric results (Theorems 1, 3) apply broadly while the detailed dynamical analysis is specific to two-layer linear and quadratic homogeneous networks.
- A self-attention derivation that either omits the softmax (consistent with "linear attention" as used in parts of the literature) or clarifies that the quadratic analysis applies only to a softmax-free variant, with the experiments using the same variant.

## Removed Points

These points from the input review are not included as weaknesses:

- "Section 4's saddle-to-saddle connection relies on a 'carefully chosen small perturbation'" — The paper is transparent that Section 5 develops heuristic arguments for how this emerges naturally; this is the paper's intended structure, not a flaw.
- "Higher-order polynomial and general nonlinear activation subsections are purely speculative" — The paper explicitly labels these with "we conjecture" and "our intuition is"; speculation is appropriately flagged.
- "Experiments are small-scale synthetic simulations" — Acceptable for a theoretical paper; not a weakness in itself.
- "The paper should move the 'Condition for saddle-to-saddle dynamics' earlier" — Presentational preference, not a substantive weakness.
- Notes about missing appendix content — These sections exist in the original submission but were stripped by the parser.
- "The paper's Section 5 language reads as more definitive than warranted" — Merged into weakness 3 above with specific quotes.

## Novel Insights

The reviews raise a useful tension that the paper's own structure does not fully resolve: the general theorems (1 and 3) are about loss landscape *geometry* and hold for a broad class of architectures, but the *dynamics* analysis is necessarily architecture-specific. The paper's core intellectual move—using invariant manifolds to bridge geometry and dynamics—is clever and under-exploited in the current literature. A sharper insight is that the same weight relationships that define embedded fixed points (static) also characterize invariant manifolds (dynamic), meaning the geometric hierarchy is not just a curiosity but has dynamical consequences when combined with timescale separation. The paper would be strengthened by making this bridging argument more explicit: geometry provides the *scaffolding* (where the saddles are and which trajectories are dynamically constrained), while timescale separation provides the *steering* (why trajectories actually follow those constraints).

## Suggestions

1. Recalibrate the abstract and introduction to distinguish the general geometric results (Theorems 1 and 3, applicable to a broad class) from the dynamics analysis (Section 5, worked out rigorously for two specific cases with heuristic arguments for broader applicability). The paper as written says "we present a theoretical framework that explains..." when it would be more accurate to say "we present a geometric framework that characterizes the loss landscape across architectures, and show in two concrete cases how this geometry, combined with timescale separation, produces saddle-to-saddle dynamics."

2. Clarify the self-attention definition. Either: (a) state explicitly that the analysis applies to softmax-free linear attention (consistent with the "linear self-attention" label) and remove smax from the definition, or (b) if the analysis applies to standard softmax attention, provide a derivation showing that the quadratic structure still holds—this is non-trivial given the exponential in softmax.

3. Add a brief quantitative validation for one prediction (e.g., plateau length vs. singular value gap for linear networks) to demonstrate that the approximate dynamics faithfully captures the true dynamics. Even a single figure panel comparing predicted vs. observed plateau lengths would substantially strengthen the paper.

## Score and Decision

**Score anchors used:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| KNQJtoPZmz.md (Simplicity Bias in Overparameterized ML) | 3.00 | R1 | Much weaker—vague claims, no clear theoretical contribution. Our paper is clearly stronger. |
| CQF8mTF7qx.md (Simplicity Bias of SGD via Sharpness Minimization) | 6.00 | R1, R2 | Similar scope and limitations; our paper has broader architectural scope and more novel geometry results. |
| eQggPqESBr.md (Simplicity Bias and Optimization Threshold) | 5.50 | R1, R2 | Narrower focus; our paper has broader geometric contributions. |
| QibPzdVrRu.md (Early Neuron Alignment in Two-layer ReLU Networks) | 6.50 | R1, R2 | More rigorous dynamics analysis but narrower scope. |
| wFD16gwpze.md (Analyzing Neural Scaling Laws) | 7.33 | R1 | More comprehensive theoretical treatment; our paper's dynamics analysis is more limited. |
| 3Pn24GOcQ1.md (Geometry of Loss Landscape in Invariant Deep Linear Networks) | 5.80 | R2 | Similar geometric contribution type; our paper has broader architectural coverage. |
| J4Dvxv7WnG.md (Learning Dynamics of Deep Matrix Factorization Beyond EOS) | 7.00 | R2 | More rigorous dynamics analysis; our paper's dynamics is more heuristic. |

**Round 1 bracket:** 5.5 – 6.5  
**Final score:** 6.0 — narrows the bracket to the middle, reflecting that the paper's theoretical contributions (Theorems 1, 3) are strong and its breadth is impressive, but the framing gap, self-attention inconsistency, and heuristic dynamics analysis prevent it from reaching the 6.5-7.0 range of more rigorous theoretical papers.

The paper makes genuine contributions—the extended fixed-point embedding theorem, the invariant manifold theorem, and the clean conceptual distinction between data-driven and initialization-driven timescale separation. These are non-trivial and organize a significant body of observations in the literature. However, the gap between the paper's framing (which implies a unified dynamical theory across architectures) and what is actually proved (general geometry + specific-case dynamics) is significant. The self-attention inconsistency is a concrete technical concern. With revision to address the framing and the self-attention derivation, the paper would be stronger, but in its current form it is a borderline accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>