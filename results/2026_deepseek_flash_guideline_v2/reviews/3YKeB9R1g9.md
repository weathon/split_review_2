Now let me finalize the review based on my verification.

## Summary

This paper extends the phenomenon of training loss curve (TLC) collapse — previously shown only in small-scale μP setups — to practical LLM training (300M–3.9B parameters). It identifies τ (normalized AdamW timescale) and TPP (tokens-per-parameter) as key controls of TLC shape, shows that collapse holds when these are matched across model sizes, and demonstrates two applications: (1) using collapse residuals for diagnosing training pathologies (with a documented 1.8B debugging case), and (2) early stopping in HPO via a parametric surrogate fit at small scale. The paper also introduces Celerity, a model family trained in the collapse regime.

## Strengths

1. **Extends loss-curve collapse to practical LLM scales with AdamW, weight decay, and practical scaling.** Prior work (Qiu et al., 2025) validated collapse only on small autoregressive tasks without weight decay. The paper demonstrates collapse across Celerity models spanning 300M–3.9B parameters at 20 TPP and 80 TPP (Fig. 6), providing the first evidence that the phenomenon persists under realistic LLM training conditions with co-scaled width, depth, batch size, and weight decay.

2. **Identifies τ as the unifying control of TLC shape, subsuming η, λ, and B individually.** Figure 3 cleanly demonstrates that sweeping η, λ, or B produces near-identical normalized TLCs whenever τ matches — even when the individual hyperparameters differ by large factors. This is a concrete advance that unifies several prior threads (τ scaling from Bergsma et al., 2025a; TLC shape from Qiu et al., 2025) under a single explanatory variable.

3. **Collapse residuals provide a practical diagnostic for training pathologies, with a documented debugging case.** The 1.8B run (Sec. 4, lines 204–206) shows collapse residuals flagged divergence starting at ~60% of training (Fig. 1, right), while the raw TLC showed no visible upward trend until after 90% (Fig. 6, right). The paper traces the root cause to a specific numerical bug in a loss kernel triggered at certain microbatch sizes and shows the repaired run tracked the reference TLC closely. This goes beyond generic monitoring claims by providing a quantitative, scale-normalized intervention criterion.

4. **Celerity models on the compute-efficiency frontier.** Figure 2 positions Celerity models on the Pareto frontier against public families (Gemma, Llama, OLMo, SmolLM, etc.), with comparable accuracy to BTLm using 75% fewer training FLOPs (line 187). This demonstrates that the collapse-inducing recipe does not sacrifice model quality.

## Weaknesses

### Major

1. **Mismatch between theoretical framework (μP) and implementation (CompleteP).** Section 3 derives the conditions for collapse under μP, leveraging μP-specific properties for scale stability and hyperparameter transfer. However, line 164 states that Celerity uses **CompleteP**, "which enables hyperparameter transfer over width *and* depth, was more efficient/reliable than μP (Fig. 15)." The paper never explains whether CompleteP preserves the μP properties that the collapse theory depends on (e.g., scale-invariant curvature, the cancellation of the curvature factor *h* in the noisy quadratic model). The collapse observed in Celerity could have a different mechanism than the one the paper theorizes. At minimum, the paper should either show that the theoretical results hold under CompleteP or explicitly decouple the theory (motivation) from the Celerity implementation (independent empirical finding).

2. **The "optimal τ" central to the collapse-efficiency link is not independently verified for Celerity's setup.** The paper claims that "setting τ optimally for a given TPP" produces collapse and that collapse is a "signature of compute-efficient training" (lines 31, 38). The τ values are taken from Bergsma et al. (2025a)'s finding that optimal τ depends only on TPP (lines 76, 139). The paper does not independently verify that these τ values are optimal for the Celerity-specific architecture (CompleteP), tokenizer (Llama-3 vocabulary), data mix (educational/math/coding), and LR schedule (linear decay). If the τ values used are simply the ones that produce match across model sizes rather than independently verified optima, the claim that collapse "emerges as a signature of compute-efficient training" becomes circular: collapse and optimality may be coincident rather than causally linked. A sweep of τ at each TPP band with final loss reported would substantiate the optimality claim.

3. **The abstract overstates the collapse claim relative to the evidence.** The paper asserts "loss curves collapse across scales precisely when optimization hyperparameters are set optimally" (line 9) — but the paper's own results show this is clean only at 80 TPP. At 20 TPP "we see small early deviations" (line 202); at 234 TPP (the primary operating point), "divergences appear late in training for larger models" (line 202). The paper acknowledges these deviations but does not discuss whether they undermine the diagnostic at the settings most heavily emphasized. The late-phase divergence at 234 TPP is particularly relevant because it is the regime used for the compute-efficiency frontier claim and the diagnostic case study.

4. **Weak baselines for early stopping evaluation.** The early stopping procedure (Sec. 5) is compared only against "Random" and "Current best" baselines. The paper cites the loss-curve prediction literature (Tissue et al., 2024; Luo et al., 2025; Schaipp et al., 2025) in Related Work but does not compare against any of these methods or against standard HPO approaches (Bayesian optimization with early stopping, learning curve extrapolation). While the proposed use of collapse for this purpose is novel, the lack of comparison against reasonable alternatives limits assessment of its practical added value.

### Minor

1. **No statistical uncertainty.** All TLCs shown are single runs. While multiple seeds are expensive at LLM scale, the paper would benefit from at minimum 2–3 seeds for a representative subset of configurations to demonstrate that collapse is not an artifact of a particular initialization or data ordering.

2. **Parametric surrogate has limited justification and validation range.** The surrogate (Eq. 4) fixes ε₁=0.001, ε₂=0.1, and m=0.05 with only brief justification. The alternating fitting procedure for b and q reduces the grid search but convergence properties are not discussed. The surrogate is fit at 111M scale and validated up to 3.3B (30× scale-up) — respectable but far from the frontier-scale LLM setting the paper aims at. These choices do not invalidate the results but limit confidence in the surrogate's generality.

3. **Scale-invariance condition not empirically checked.** The theoretical claim that normalized TLCs depend only on τ and t̂ (line 131) relies on "residual bias at end-of-training is negligible relative to the variance floor." This assumption is not empirically verified, and the late-phase divergence at 234 TPP (which could be bias-related) suggests it may not hold universally.

### Trivial

None.

## Nice-to-Haves

- Sensitivity analysis of the early-align method (aligning partial curves over 25–50%) to the chosen alignment window — how does it perform when collapse is imperfect (e.g., at 234 TPP)?
- A quantitative measure of collapse quality (e.g., maximum pairwise divergence between normalized curves) would bound claims across TPP regimes more precisely than visual assessment.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Critical Issue" about the switch from Qiu et al.'s normalization to simple division by final loss:** The paper explains this was found empirically to result in better alignment (line 101: "simply dividing by the final training loss... resulted in optimal alignment"). A scientific choice, not a flaw.
- **"Celerity compute estimates not fully specified":** The paper provides a FLOPs comparison methodology and places Celerity in context of public models. The comparison is adequately documented for the qualitative frontier claim.
- **Speculation about the early-stop surrogate's convergence issues:** The alternating fitting procedure is described as "iterating to convergence" (line 252). Without evidence of non-convergence, this is a speculative concern, not a verified weakness.
- **Missing appendix content or references:** Parser strips appendix from all papers; these exist in the original submission.
- **Generic "no comparisons to learning curve extrapolation methods" framing as fatal:** This is already listed as Major weakness #4 with appropriate severity.
- **Formatting/style nitpicks:** Parser artifacts, not author errors.

## Novel Insights

Beyond the paper's own contributions, the most notable observation from cross-examining the reviews is that the paper's two strongest contributions — the τ-control finding (Fig. 3, well-evidenced) and the practical debugging case (1.8B, compelling) — are largely independent of the paper's more ambitious claims about collapse as a universal signature of optimality. The τ-control result would stand as a useful empirical finding even without the collapse framing. The debugging case demonstrates a concrete practical benefit regardless of whether the τ values are "provably optimal." This suggests the paper could be strengthened by foregrounding these robust findings and treating the optimality-collapse link as a hypothesis rather than a demonstrated conclusion.

## Suggestions

1. **Resolve the μP/CompleteP disconnect.** Either (a) show that CompleteP preserves the μP properties needed for the theoretical collapse derivation, or (b) explicitly state that the theory (Sec. 3) and the Celerity results (Sec. 4) are parallel contributions — the theory providing mechanistic intuition under μP, and Celerity providing an independent empirical demonstration under CompleteP — and discuss how the two relate.

2. **Independently verify τ optimality for Celerity's setup** by showing a sweep of τ at a representative TPP band with final loss reported, or at minimum soften the causal claim from "collapse is a signature of compute-efficient training" to "collapse is empirically observed under the conditions where compute-efficient training occurs."

3. **Add quantitative collapse metrics** (e.g., maximum pairwise normalized-curve divergence) across TPP bands to bound where collapse holds cleanly and where it degrades, informing when the downstream applications can be relied upon.

4. **Add at least one comparison baseline** for the early stopping method from the loss-curve prediction or HPO literature.

5. **Add statistical replicates** for at least one representative configuration to demonstrate robustness.

## Score and Decision

The calibration search was unavailable due to a persistent database error, so I proceed from first principles. 

Anchoring against what I would expect from venue calibration: papers at this venue that merely iterate an existing finding (collapse from μP small-scale → practical LLM scale) would score ~3–4. Papers that contribute a genuinely new empirical phenomenon plus a validated application would score ~6–8. This paper sits between these: the τ-control finding (Fig. 3) is a genuine advance beyond prior work, and the debugging case study is a compelling application. However, the theory-implementation disconnect (μP vs. CompleteP), the unverified τ-optimality link, the overclaiming in the abstract, and the weak baselines for early stopping prevent it from being a clear accept. These are real weaknesses that require major revisions but do not invalidate the core empirical contributions. The paper is a solid borderline accept: the contributions are real and useful, but the framing needs to be honest about limitations.

**Score: 5.5**

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>