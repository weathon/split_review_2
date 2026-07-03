Now I have thoroughly verified all claims against the paper. Let me write the final consolidated review.

## Summary

This paper proposes IterRef, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) with a noising-denoising transition kernel to iteratively refine intermediate states during reward-guided generation. The method is evaluated across three backbones (MDLM, LLaDA-8B, MaskGIT) on text and image tasks.

## Strengths

1. **Clever adaptation of MTM to discrete diffusion.** The tailored transition kernel K and balancing function λ (Eq. 2) yield uniform importance weights and a simplified acceptance ratio β = min(1, exp((r(x_t')−r(x_t))/α)) (Eq. 3), which eliminates the need for backward-proposal resampling and reduces per-iteration cost by nearly half (Section 3.3). This is a concrete algorithmic contribution.

2. **Strong quantitative evidence of efficient scaling.** On MDLM with Toxicity, IterRef at 4T NFEs matches FK steering at 32T NFEs (~8× faster); on Sentiment, CoLA, and Perplexity, IterRef at 2T NFEs surpasses all baselines at 32T NFEs (Section 4.2, Figure 2). The per-NFE comparison is a fair compute-controlled evaluation.

3. **Insightful ablation revealing that later denoising stages matter more.** Table 2 systematically sweeps application timesteps and shows that later stages (0.1T) consistently outperform earlier ones, directly contrasting with continuous diffusion dynamics. This is a genuine empirical contribution to understanding discrete diffusion.

4. **Iteration count k beats particle count N.** Table 3 holds total compute constant and shows (k=8, N=4) achieves 85.3 CoLA vs. (k=1, N=32) achieving 8.7 CoLA, directly validating the core thesis that iterative refinement drives gains more than brute-force particle enumeration.

5. **Cross-modality generalization.** Consistent improvements on MDLM, LLaDA-8B (text), and MaskGIT (image) with qualitatively different reward functions (classifier-based, CLIPScore, toxicity, perplexity) demonstrate that the benefit is not domain-specific (Table 1).

## Weaknesses

### Major

1. **Convergence guarantee rests on an unverified and likely unsatisfied reversibility assumption.** Proposition 1 explicitly conditions convergence on the assumption that "q and p_θ form a reversible Markov kernel." This assumption is never checked, and for the absorbing-state formulation used by all three backbones (MDLM, LLaDA-8B, MaskGIT), there is no reason to believe it holds — the forward noising process (adding mask tokens) and the learned reverse denoising (predicting original tokens) are not jointly reversible by design. Since the theoretical claims (detailed balance, convergence as k→∞, simplification of importance weights and acceptance ratio) flow from this assumption, the practical relevance of the convergence guarantee is unclear. **Why it matters:** The paper claims in the conclusion (Section 6) that the method is "theoretically well-founded," but the foundation rests on an assumption that is transparently stated but neither justified nor plausibly satisfied by any model tested.

2. **Internal inconsistency between Algorithm 2 and the described practical implementation.** Line 8 of Algorithm 2 includes generating N−1 backward auxiliary proposals (standard MTM). However, Section 3.3 states the implementation "eliminates the resampling step" and reduces cost by nearly half, claiming the balancing function makes backward proposals unnecessary for evaluating the acceptance ratio. The paper does not reconcile which version was actually run in experiments — if the full Algorithm 2 was used, the cost savings claim is inaccurate; if the simplified version was used (as Section 3.3 asserts), Algorithm 2 is misleading. Either way, the divergence undermines both the theoretical claims (which rely on the full MTM procedure for detailed balance) and the empirical interpretation.

### Minor

3. **No uncertainty quantification for any result.** All main results (Figure 2, Tables 1–3) report only point estimates (mean scores) without standard deviations, confidence intervals, or statistical tests. The evaluation uses 15 prompts × 20 samples = 300 generations per task (Section 4.1). On such a modest evaluation set, the "8× faster" and "2× improvement" claims cannot be assessed for stability — observed gaps could be driven by prompt selection rather than method superiority.

4. **Figure 5(a) baseline naming ambiguity.** The parser-extracted figure legend shows baselines named "SLP", "SR", "SVTOD" — none of which match the baselines defined in Section 4.1 (BoN, SoP, SVDD, FK Steering). Section 4.5 does not specify which baselines were used in the detoxification experiment, making it impossible for the reader to determine what is being compared.

5. **Critical hyperparameter α receives no analysis.** The acceptance probability β = min(1, exp((r(x_t')−r(x_t))/α)) is controlled by α, which directly determines how selective the chain is. Despite being listed in Algorithm 2's input, no ablation, default value, or sensitivity study is reported for any experiment. The same applies to the composition of the effective timestep set U.

6. **No discussion of limitations or failure modes.** The paper lacks any discussion of when the method might underperform (e.g., noisy reward models, poor denoising quality on specific tasks, or the impact of the reversibility assumption violation in practice).

### Trivial

7. Eq. 3 has a minor parenthesis formatting issue: `β = min(1, exp((r(x_t') - r(x_t)/α)))` — the closing parentheses are ambiguous, which could confuse readers.

## Nice-to-Haves

- Sensitivity analysis for α and the composition of the effective timestep set U.
- Clarify whether Algorithm 2 Line 8 (backward proposals) was actually executed in experiments or omitted as Section 3.3 describes.
- Add error bars or confidence intervals to all main results.
- A brief discussion of how the marginal p(x_t) in Eq. 2's balancing function is handled in practice (the derivation is deferred to the stripped appendix).

## Removed Points

These points from the reviews were removed for the following reasons:

1. **Pool reuse introduces bias (Harsh Critic):** The claim that reused candidates are "no longer an i.i.d. sample from K(x_t,·)" is valid in a strict sense, but the paper's defense (candidates were originally i.i.d. and rejection does not change that) is reasonable for practical purposes. This is nitpicking a reasonable engineering approximation.

2. **p(x_t) estimation not addressed (Harsh Critic):** The derivation is in Appendix D.2, which is stripped by the parser. Cannot verify as a weakness from the main text.

3. **"8× faster" not caveated (Harsh Critic):** The paper clearly states in Section 4.2 and Figure 1 that this applies to the Toxicity/MDLM setting. The claim is properly situated.

4. **Missing related works / reproducibility nitpicks / formatting issues / missing appendix content:** All removed per hard rules (parser artifacts, not author errors).

5. **Criticisms that are factually wrong or based on speculation:** Removed per filtering rules.

## Novel Insights

The harsh critic's most valuable observation is that the reversibility assumption in Proposition 1 is not merely an untightened theoretical bolt but is structurally implausible for absorbing-state discrete diffusion models, making the convergence guarantee largely decorative. This is a genuinely novel insight that goes beyond the paper's own self-assessment and points to a meaningful weakness in how the theoretical contribution is framed. The nitpicks about pool reuse bias and missing p(x_t) handling, by contrast, are standard concerns that the paper's appendix would likely address.

## Suggestions

1. **Reconcile Algorithm 2 with the actual implementation.** Either remove Line 8 from Algorithm 2 (if backward proposals are truly not generated) or, if they are generated, acknowledge the cost and remove the "eliminates the resampling step" claim in Section 3.3. Add a brief justification for why the practical modifications do not break the theoretical guarantees.

2. **Acknowledge the reversibility assumption limitation.** Add a sentence or paragraph discussing whether the reversibility assumption is reasonable for absorbing-state models and whether the method degrades gracefully when it is violated. If empirical evidence (even approximate) exists that the chain still targets a reasonable distribution, include it.

3. **Add uncertainty quantification.** Report standard deviations or confidence intervals for all main results (Figure 2, Tables 1–3). This is standard practice for the benchmarks used.

4. **Clarify Figure 5 baselines.** State explicitly which baselines are compared in the detoxification case study, or correct the figure legend if it is erroneous.

5. **Add an α ablation or at minimum report the values used.** Even a single appendix table showing sensitivity to α across a plausible range would substantially strengthen the paper.

## Score and Decision

**Bracket analysis (calibration unavailable due to tool error):** I attempted calibration search but the index was inaccessible. Based on my knowledge of ICLR reviewing standards, this paper has a novel, well-motivated contribution and generally positive empirical results, but its theoretical claims are weaker than advertised (externally conditioned on an unverified assumption) and its evaluation lacks standard uncertainty reporting. Papers in the 5–6 band at ICLR typically present novel methods with clean evaluations and honest scoping of limitations. This paper's strengths match that band but the theory-practice gap and missing error bars tilt it downward.

**Scoring rationale:** The core idea is clever and the empirical trends are consistent across domains. However, two Major weaknesses (unverified reversibility assumption underlying the convergence guarantee, and an internal inconsistency between Algorithm 2 and the described implementation) prevent the paper from meeting the bar for acceptance. The evaluation gaps (no error bars, missing α analysis, Figure 5 baseline ambiguity) further weaken confidence but are addressable. Score 5 reflects a borderline paper with real contributions that needs significant improvements in presentation and rigor.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>