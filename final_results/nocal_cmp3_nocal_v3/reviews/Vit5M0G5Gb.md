Now I will write the final consolidated review.

## Summary

This paper develops a theoretical framework connecting saddle-to-saddle learning dynamics to simplicity bias in neural networks. The framework has three pillars: (1) a unified geometric characterization of embedded fixed points (Theorem 1, extending Fukumizu & Amari 2000) and invariant manifolds (Theorem 3) that applies to fully-connected, convolutional, and attention-based architectures through a general unit formulation (Equation 1); (2) heuristic dynamics analyses for two-layer linear networks (data-driven timescale separation → low-rank weights) and two-layer quadratic networks (initialization-driven timescale separation → sparse weights); and (3) testable predictions about how width, data distribution, and initialization affect learning, validated on synthetic data. The core theoretical contributions—the extension of embedded fixed points (Equations 6–7) and the invariant manifold characterization—are rigorous and genuinely novel.

## Strengths

- **Unified geometric framework across architectures (Theorems 1 and 3).** By formulating architectures via the general unit structure in Equation (1), the paper shows that embedded fixed point construction (Theorem 1, with new categories in Equations 6–7 beyond Fukumizu & Amari) and invariant manifolds (Theorem 3) apply generically across fully-connected, convolutional, and attention-based networks. Theorem 3's identification of invariant manifolds (equal weights, zero weights, proportional weights under homogeneity, linear dependence under linearity) as corresponding to effectively narrower networks provides a formal geometric mechanism connecting saddle structure to progressive complexity increase.

- **Disentangling two distinct sources of timescale separation.** The paper cleanly distinguishes data-induced timescale separation (linear case, Section 5.1: growth along singular vectors of Σ_{yz}) from initialization-induced timescale separation (quadratic case, Section 5.2: rich-get-richer across units). This yields differentiated predictions about weight structure (low-rank vs. sparse) and about the effects of data distribution vs. initialization. The prediction that increasing width speeds up learning in the quadratic case but not the linear case (Section 6, Figure 2A) is a sharp, testable consequence.

- **Original invariant manifold analysis.** Theorem 3 is genuinely new. The observation that escape from a saddle corresponds to "breaking exactly one constraint" on an invariant manifold (Section 4) provides a clear conceptual picture connecting the loss landscape geometry to the dynamics.

- **Honest about limitations and conditions for saddle-to-saddle dynamics.** The Discussion (Section 7) explicitly states that the dynamics analysis only applies to two-layer networks, that exhaustiveness of fixed points is open, and that tanh networks violate conditions for saddle-to-saddle dynamics. The falsifiable conditions for saddle-to-saddle dynamics (lines 222-226) are a valuable contribution.

## Weaknesses

### Fatal
None.

### Major

- **Abstract/title framing significantly oversells the scope of the dynamics analysis.** The abstract claims "we show" that "linear networks learn solutions of increasing rank, ReLU networks learn solutions with an increasing number of kinks, convolutional networks learn solutions with an increasing number of convolutional kernels, and self-attention models learn solutions with an increasing number of attention heads." However, the rigorous dynamics analysis (Section 5) covers only **two-layer linear networks** (Section 5.1) and **two-layer quadratic networks** (Section 5.2, which includes linear self-attention in the scalar-output two-layer case). No dynamics analysis is provided for ReLU activations (beyond noting they fall under Theorem 3(iii)), deep networks, convolutional networks beyond the linear case, or actual multi-head self-attention. While the paper is transparent about this limitation at lines 122 and 228 ("the analysis of dynamics in Section 5 only applies to two-layer networks"), the abstract and introduction are not scoped to match what is actually delivered. The paper's genuine contribution—a unified loss-landscape framework (Sections 3–4) plus two concrete two-layer dynamics case studies—is still substantial, but the framing should be adjusted to reflect it accurately.

- **The dynamics analysis (Section 5) is heuristic and leaves a gap between the geometric framework and the claim of "explaining" simplicity bias.** The paper explicitly calls its arguments "heuristic" (line 118) but the central claim that saddle-to-saddle dynamics *explains* simplicity bias depends on bridging this gap. Specifically:
  - Theorem 4 analyzes the linearized dynamics (Equation 10), not the actual gradient flow (Equation 9). The approximation replaces (Σ_{yz} - WΣ_{zz}) with Σ_{yz}, justified by small initialization. The paper provides the approximation order (O(ε²), line 138) but no bound on the approximation error, no analysis of how long the approximation remains valid, and no guarantee that the true trajectory stays close to the linearized system.
  - Proposition 5 analyzes the simplified system (Equation 14) which retains only the quadratic terms from the full gradient flow, not the full dynamics. The scalar intuition \dot{v}_i = v_i² (Equation 15) illustrates the mechanism but elides coupling between v_i and u_i.
  - The argument that "subsequent iterations operate similarly" (line 154, Equation 12) relies on a projected version of Σ_{yz} with the claim deferred to Appendix G.3 (stripped by parser). Whether earlier approximation errors compound at each stage is not addressed in the main text.
  - For architectures beyond linear/quadratic two-layer networks, the paper relies on simulations (Figures 1, 3–5) to demonstrate saddle-to-saddle behavior, without providing dynamics analysis. This creates a gap between the paper's title-level claim of "explaining a simplicity bias across architectures" and what is analytically established.

### Minor

- **Experimental validation is limited to synthetic data with no quantitative measures.** The experiments in Section 6 validate theoretical predictions using synthetic data with controlled power-law spectra, which is appropriate for a theory paper. However, the results are described qualitatively ("shortens the plateaus") without quantitative measures such as plateau duration as a function of singular value gaps or initialization scale compared to theoretical predictions (e.g., O(ε^{1-s_{r+1}/s₁}) from Theorem 4). No variance or error bars are reported for any simulation. These are not fatal omissions for a theory paper, but they weaken the link between theory and evidence.

- **The treatment of "subsequent iterations" is compressed.** The argument that dynamics near each saddle is analogous to the first transition (line 154–158 and line 188) is presented too briefly in the main text. The claim that the projected Σ_{yz} in Equation (12) captures the relevant dynamics needs more justification, as the structure of the dynamics at a rank-r saddle may differ qualitatively from the initial escape from zero.

### Trivial
None.

## Nice-to-Haves

- **Provide error bounds for the linearization in Section 5.1.** A perturbation bound showing that the trajectory of the true gradient flow (Equation 9) stays near the linearized system (Equation 10) for a controlled duration would significantly strengthen the dynamics analysis.
- **Quantitative experimental measures** (e.g., measured vs. predicted plateau duration as a function of singular value gaps or initialization scale) would tighten the connection between theory and simulations.
- **A dedicated discussion of what the existing analysis predicts for ReLU dynamics** (and where it breaks down) would help bridge the gap between the abstract's claims about ReLU networks and the actual analysis, which covers only linear and quadratic activations.
- Sharper differentiation from prior work on simplicity bias (Saxe et al., Arpit et al., Kalimeris et al.)—in particular, explicitly stating which aspects are newly explained—would help readers assess the contribution.

## Removed Points

- "The central mechanism is unproven" — **Kept but integrated** into the Major weakness about the heuristic nature of the dynamics analysis; the paper explicitly calls it "heuristic" at line 118, so this is not a surprise but remains a genuine limitation.
- "No experiments on real datasets" — **Moved to Nice-to-Haves**; for a theory paper focused on mechanism, synthetic experiments that directly test theoretical predictions are the appropriate standard.
- "Simulations use gradient flow with squared loss, a substantial simplification" — **Removed**; this is standard practice for theory papers studying gradient flow dynamics and does not constitute a weakness.
- "The connection to prior work on simplicity bias needs sharper differentiation" — **Moved to Nice-to-Haves**; it is a suggestion for improvement, not a weakness.
- "The claim that 'subsequent iterations operate similarly' glosses over non-trivial questions" — **Kept but demoted to Minor**; the paper references Appendix G.3, so it is not ignored, but the main-text treatment is too brief.
- Criticisms framed as general area-of-concern sweeps ("could the metric be measuring a proxy?", "are confounders controlled?") — **Removed**; none were present in the input review.

## Novel Insights

The review surfaces a recurring tension in this type of theory paper: the gap between a rigorous geometric framework (loss landscape results that apply broadly) and a heuristic dynamics analysis (that applies only to specific two-layer cases). This gap is partially structural—dynamics is genuinely harder than geometry—but the review correctly identifies that the abstract's "we show" language papers over this gap. A more interesting observation is that the paper's own "conditions for saddle-to-saddle dynamics" (Section 7) could be used to self-criticize its own scope: by the paper's own criteria, the ReLU, deep convolutional, and multi-head attention cases are not actually shown to satisfy condition (i) (escape paths follow invariant manifolds) because no dynamics analysis is provided for them. This suggests a concrete path for strengthening the paper: prove that one specific non-linear, non-quadratic architecture satisfies both conditions.

## Suggestions

1. **Rescope the abstract and introduction** to accurately reflect what is analyzed: a unified loss-landscape framework (Theorems 1, 3) with heuristic dynamics for two-layer linear and two-layer quadratic networks, supported by simulations for other architectures. Remove the implication that a full dynamics analysis exists for all listed architectures.
2. **Add at least one quantitative comparison** between theory and experiment, e.g., measured plateau duration vs. the predicted O(ε^{1-s_{r+1}/s₁}) scaling, to demonstrate the explanatory power of the framework.
3. **Provide a perturbation bound** for the linearization in Theorem 4—even a simple one—to show when the linearized dynamics remains predictive.
4. **Expand the main-text justification** for the "subsequent iterations" argument (Equation 12), or add a brief sketch of why the projected Σ_{yz} captures the relevant dynamics.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>