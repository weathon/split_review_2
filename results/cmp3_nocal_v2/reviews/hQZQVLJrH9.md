## Summary

This paper establishes a first-order equivalence between activation steering and influence functions—two previously disconnected techniques in interpretability. It proves that any steering vector can be represented as an influence weighting over training data (and vice versa), derives a geometric diagnostic (γ) that characterizes when steering can succeed, and provides constructive formulas including the Influence-Aligned Steering (IAS) vector, a spectral optimality theorem, and generalization bounds. The work is primarily a theoretical contribution: it formalizes the primal-dual relationship between the two methods and gives practitioners concrete tools for deciding when steering versus weight-space editing is appropriate.

## Strengths

1. **Genuinely novel theoretical unification.** The core insight—that activation steering and influence functions are, to first order, projections of the same sensitivity structure onto different subspaces—is non-obvious and advances conceptual understanding. The primal-dual formulation (Section 3) is elegant: the minimum-norm steering vector that replicates a given influence update is obtained by projecting the target logit displacement onto the activation-reachable subspace and lifting via the pseudoinverse.

2. **The γ diagnostic and no-free-lunch theorem (Theorems 5.1, 6.2).** The alignment bound—connecting the fidelity of steering to the smallest principal angle between two Jacobian subspaces—is the paper's most practically useful result. It provides a principled criterion for when steering *cannot* succeed, which is the kind of negative result that prevents wasted effort. Computing γ costs two small SVDs.

3. **Constructive formulas throughout.** The paper gives explicit, implementable constructions: the IAS vector (Δh* = J†_{h→y} J_{θ→y} Δθ), the signed measure ρ_s for mapping steering back to training data (Theorem 4.2), the spectral direction for optimal steering under a norm budget (Theorem 5.3), and the generalization bound for low-rank steering (Theorem 6.1). Each is a concrete tool, not just an abstract statement.

4. **Intellectually coherent narrative.** The "steer first, trace provenance, edit weights only when γ says you must" framing is well-motivated by the theory and gives the paper a clear throughline.

## Weaknesses

### Fatal

None. The theoretical core is sound and represents a meaningful advance.

### Major

1. **The slope discrepancy in the central empirical validation (Figure 1) is not explained or discussed.** The paper's first-order theory predicts that the logit shift from an influence update should match the shift from the corresponding IAS vector with a slope of 1.0. Figure 1 reports cosine 0.978 (high correlation, supporting the linear relationship) but slope 1.50 (the actual shift is 50% larger than predicted). The paper describes this as "consistent with the expected linear regime," but a slope of 1.5 is not consistent with the first-order prediction of 1.0. This discrepancy could arise from: (a) the steering magnitude α being large enough that second-order terms contribute systematically; (b) the damped Hessian inverse (H+λI)^{-1} systematically biasing the influence estimate; or (c) some other unmodeled nonlinearity. Without an explanation—or a demonstration that the slope approaches 1.0 as α → 0—the validation of the paper's central first-order claim is weaker than presented. The theory may still be correct, but the empirical evidence for it is incomplete.

2. **The paper's most distinctive practical claim—mapping steering vectors back to causal training examples—is never empirically validated.** Theorem 4.2 and Corollary 1 state that any steering vector yields a signed measure ρ_s over training examples whose L1 norm equals the steering magnitude, and the paper repeatedly frames this as a key payoff (abstract: "mapping undesired behaviors back to causal training examples"; line 130: "pinpoints the fewest training examples to relabel/remove/examine"; line 275: "trace provenance"). **No experiment tests this claim.** The detoxification experiment (Section 7.1) compares IAS with CAA on toxicity scores but never shows which training examples ρ_s points to, whether those examples are causally relevant, or whether removing/up-weighting them changes behavior as predicted. Influence functions alone already provide training-example attribution; the paper's advertised value-add is the *bidirectional* mapping from steering vectors back to data. Without evidence for this direction, the "trace provenance" framing overclaims relative to what is demonstrated.

### Minor

3. **Experiments are too narrow to support the claimed practical workflow.** All LM experiments use a single model (GPT-2 Medium), a single task (detoxification), and mostly a single layer (ℓ=8). The detoxification comparison (Table 1) shows IAS *underperforming* the simpler CAA baseline (toxicity 0.0164 vs. 0.0150). The ImageNet experiment (Section 7.4) tests one class (horse) with one model (ResNet-50) against random baselines. The paper frames IAS as an "integrated workflow for debugging, auditing, and aligning large neural models" (Conclusion), but the experiments only serve as proof-of-concept for the theory. They do not demonstrate the practical superiority or utility of the framework.

4. **The γ diagnostic's predictive power is never directly validated.** Figure 2 shows that γ increases with layer depth, but no experiment tests whether a layer with high γ actually yields better steering fidelity (as Theorem 5.1 predicts) or whether Theorem 6.2's no-free-lunch prediction holds (steering fails when γ is low). Without this validation, γ remains a plausible heuristic rather than a verified diagnostic.

5. **Theorem 6.1 models steering as a rank-k weight correction (f̃ = f_θ + α UV^T), but the paper's IAS is defined as activation-space steering (adding Δh* to h(x)).** The paper does not explain how activation steering translates to a rank-k weight change, or why the generalization bound applies to activation steering. The sketch claims "IAS changes only a rank-k submatrix of the layer weight" without justifying this claim. This connection needs to be spelled out.

6. **The spectral optimality experiment (Section 7.4) is under-described.** The experiment compares spectral radii under true vs. random labels, but it is not explained how this connects to Theorem 5.3 (which maximizes *expected first-order logit change* under a norm budget). The x-axis label "Spectral radius of Xc^T diag(y) Xc" uses notation not introduced in the paper. The connection between the theorem and the experiment is unclear.

7. **The influence magnitude and training example used for the first-order equivalence experiment (Figure 1) are not specified.** The paper reports results over 5000 prompt-token pairs but does not state which influence update Δθ is being matched, the perturbation magnitude ϵ, or the steering magnitude α. The reader cannot assess whether the slope of 1.5 arises from α being too large.

### Trivial

8. **The value of the damping parameter λ is not stated.** The paper mentions using a damped inverse (H+λI)^{-1} but does not report the λ value used in experiments. This parameter controls the bias-stability trade-off and can substantially affect influence estimates.

## Nice-to-Haves

- Show that the slope in Figure 1 approaches 1.0 as α → 0, which would confirm that the discrepancy is due to second-order effects at finite α rather than a systematic error in the theory.
- Validate the traceability claim on a controlled dataset (e.g., a small classification task with known "poisoned" examples): construct the IAS vector, compute ρ_s, and verify that the top-weighted training examples include the known causal example.
- Test the γ diagnostic by comparing steering fidelity at a high-γ layer versus a low-γ layer, directly validating Theorem 5.1's prediction.
- Discuss the practical limitations of influence functions for deep networks (e.g., Basu et al., 2021), since the IAS construction inherits their known instabilities.

## Removed Points

The following points from the input review are excluded or substantially modified:

- **Equation formatting issue (Section 3.2, Δh* formula on line 84):** The input reviewer noted that the equation appears to lack a pseudoinverse factor. This is a parser formatting artifact, not an author error. Removed per hard rules.
- **"Lemma 5.4 is not very informative":** This is an opinion about the lemma's usefulness, not a specific problem with the paper. Removed.
- **Influence-function fragility as a "structural" issue:** The paper cites Basu et al. (2021) and mentions the Gauss-Newton approximation. The omission is real but minor, not structural. Downgraded to a nice-to-have suggestion.
- **Generic "experiments too narrow" framing as a Major weakness:** Downgraded to Minor. The paper is primarily a theoretical contribution; proof-of-concept experiments are acceptable for a theory paper, though the framing should be tempered.
- **Claim that the paper "never specifies" the influence update:** Incorporated into a Minor weakness (point 7 above), not treated as a Major issue.

## Novel Insights

None beyond the paper's own contributions. The input review did not surface a genuinely novel observation about the paper that was not already in the paper itself. The key insight—the primal-dual equivalence between steering and influence—is the paper's own contribution.

## Suggestions

1. Directly address the slope of 1.5 in Figure 1: either show that it approaches 1.0 with smaller α, or provide a principled explanation (e.g., systematic bias from the damped Hessian inverse).
2. Reframe the paper's practical claims to match what is actually demonstrated. The "trace provenance" workflow is a theoretical promise that Appendix-level or follow-up experiments should validate; present it as such rather than as a demonstrated capability.
3. Add an experiment validating γ's predictive power (e.g., compare IAS fidelity at a layer with γ=0.9 vs. a layer with γ=0.6).
4. Clarify the connection between Theorem 6.1's rank-k weight correction formulation and the paper's activation-space steering construction.
5. Report the damping parameter λ value and ablate its effect on IAS.

## Score and Decision

**MY FINAL SCORE: <score>6</score>**
**MY FINAL DECISION: <decision>Borderline Accept</decision>**