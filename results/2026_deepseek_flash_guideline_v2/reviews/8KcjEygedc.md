Now I have confirmed the critical claims from both reviewers. Let me produce the final consolidated review.

## Summary

This paper develops a random-matrix-theory framework for data curation in high-dimensional binary classification with ridge regression. It derives exact asymptotic formulas for test error under label-agnostic and label-aware pruning strategies (Theorem 1) and proves that "keep hard" is optimal when the data generator is strong while "keep easy" is optimal when it is weak (Theorem 2). The theory is validated on synthetic data, connected to ImageNet experiments, and used to explain recent contradictory findings in LLM reasoning (LIMO/s1 vs. Sun et al.). The paper also presents empirical results on model collapse mitigation through strategic pruning.

## Strengths

- **Exact asymptotic characterization of test error under pruning (Theorem 1).** The paper derives a closed-form expression for test error captureable by four scalar constants (p, γ, β, β̃) that fully determine the pruning strategy's effect. Prior work (Sorscher et al., 2022) studied pruning empirically; this paper provides the first exact analytical scaling laws that map from pruning parameters to test error in a tractable setting.

- **Provable phase transition in optimal strategy type (Theorem 2).** The theorem pins down analytically when "keep hard" vs. "keep easy" is optimal as a function of generator quality ρ and oracle quality ρ_*, giving a testable, analytical condition. This goes beyond heuristic comparisons in the LIMO/s1 literature.

- **Clean synthetic validation (Figure 1).** The theoretical error curves closely match empirical simulations across all four regimes (large/small n × strong/weak generator), including the precise location of the "less is more" optimum at p ≪ 1 in the bottom-left quadrant — a nontrivial quantitative match.

- **Qualitative confirmation on ImageNet (Figure 2).** The ImageNet experiments show the predicted crossover: "keep easy" outperforms "keep hard" with a weak generator (160K examples) but the ranking flips with a strong generator (1.2M examples), confirming the core qualitative prediction.

- **Unified explanation of contradictory LLM reasoning results (Tables 1–2).** The framework resolves the apparent conflict between LIMO/s1 (curation improves average AIME performance) and Sun et al. (2025) (more data helps on hard AIME questions) by showing that the same LLM acts as a strong generator on average problems but a weak generator on hard problems — a single-parameter (ρ) distinction.

## Weaknesses

### Fatal
None.

### Major

- **The model collapse contribution is advertised as analytical but is entirely empirical.** The Contributions section states: *"We show analytically that data curation can avert model collapse under label shift, establishing phase boundaries where uncurated training diverges while curated training remains stable."* No theorem, proposition, or corollary in the paper establishes such phase boundaries. The closest theoretical connection is a qualitative remark after Theorem 2(B) saying the result is "relevant for mitigating model collapse." The actual model collapse evidence (Figure 3) is entirely a simulation experiment. This is a clear gap between what the paper advertises and what it delivers and should be corrected by honest reframing.

### Minor

- **The "less is more" claim (p<1 beats p=1) is not established as a clean analytical condition.** Theorem 2 determines the optimal *type* of pruning (keep-hard vs. keep-easy) *at a fixed pruning ratio p*. It does not establish when pruning itself (p<1) outperforms not pruning (p=1). The paper's central narrative — that small curated datasets can outperform full datasets — is demonstrated by evaluating the Theorem 1 formula in simulations (Figure 1, bottom-left quadrant), not by a theorem. The theoretical machinery is there, but the headline claim is supported by computation/simulation rather than by a standalone analytical condition.

- **Theorem 2 Part (B) has limited practical applicability when the pruner and generator are the same model.** Part (B) requires ρ_*→1 (excellent pruner) even when ρ<1 (weak generator). In the common practical scenario where the pruner and generator are the same model (as in the LIMO/s1 examples), we have w_o = w_g, so ρ_* = ρ. Thus when ρ<1, the precondition ρ_*→1 fails. This means Part (B)'s "keep easy is optimal" regime requires an external oracle that is substantially better than the generator — a meaningful restriction on its direct applicability that the paper does not discuss.

- **ImageNet validation is qualitative, not quantitative.** The experiments test directional predictions (which strategy wins under strong vs. weak generators) rather than the exact formulas from Theorem 1. The synthetic experiments validate the theory under its own assumptions (Gaussian, isotropic, linear). This is standard practice for theory papers and not a flaw per se, but the paper's framing of "empirical confirmation on ImageNet" slightly oversells what is, in practice, a qualitative consistency check.

- **The model collapse experiment (Figure 3) lacks a clear description of how the pruner is maintained across rounds.** The flow diagram suggests iterative training → pruning → re-training, but the text does not specify whether the pruner at each round is the model from the previous round (which degrades) or a fixed initial model. This detail is critical for interpreting whether the result is driven by the pruning strategy or by an artifact of the experimental setup.

### Trivial

None.

## Nice-to-Haves

- A concrete example computing the constants p, γ, β, β̃ for "keep hard" and "keep easy" threshold rules in the main text would make the theory more tangible.
- The LLM reasoning analysis (Section 4.2) is currently post-hoc interpretation; a forward prediction (e.g., predicting on a held-out dataset before seeing results) would strengthen the claim that the theory has explanatory power.

## Removed Points

The following points from the inputs were removed with justification:

1. **"LLM reasoning analysis is interpretive, not evidential"** (Harsh Critic Point 4) — REMOVED because the paper explicitly frames this as interpretation ("Our framework can interpret and unify"), not as evidence for the theory. Asking a theory paper to predict novel outcomes rather than explain existing ones sets a higher bar than what the paper promises.

2. **"Missing comparison against alternative baseline pruning strategies"** — REMOVED because the paper's contribution is a theoretical framework, not an empirical benchmark. The scope is demonstrating how theory explains the behavior of keep-hard/keep-easy strategies, not surveying all possible curation heuristics.

3. **"Constants in Eqn (8) and (13) are not fully expanded in the main text"** — REMOVED as a minor presentation preference; the appendix is the appropriate place for full expansions.

4. **"The paper assumes isotropic covariance"** — REMOVED as the paper explicitly states this is for exposition and general results are in the appendix; this is standard practice.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the model collapse overclaim.** Revise the Contributions bullet to read something like: "We demonstrate empirically that data curation can avert model collapse under label shift, and provide theoretical motivation through our analysis of pruning with weak generators." Remove the "analytically" and "phase boundaries" language unless a specific theorem is added.
2. **Discuss the applicability scope of Theorem 2(B) explicitly.** Add a remark noting that when the pruner equals the generator (common in practice), ρ_* = ρ, so Part (B)'s precondition (high ρ_* with low ρ) may not hold, and explain what this means for practical scenarios.
3. **Clarify the model collapse experiment setup.** Specify whether the pruner is the model from the previous round or a fixed initial model, and how pruning quality is maintained across rounds.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>