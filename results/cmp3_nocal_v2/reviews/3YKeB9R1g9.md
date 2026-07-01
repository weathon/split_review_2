## Summary

This paper extends the "training loss curve collapse" phenomenon (previously observed only at small scale with vanilla Adam) to practical LLM training at 100M–3.9B scale under AdamW with weight decay, co-scaled depth, and realistic vocabularies. It identifies three controls that govern collapse—the AdamW timescale τ, the tokens-per-parameter ratio (TPP), and the learning-rate schedule—and shows that fixing τ and TPP while using a matched LR schedule produces collapsed normalized loss curves. Two applications are demonstrated: using deviation-from-collapse as an early diagnostic for training pathologies, and using collapsed-curve predictability for early stopping in hyperparameter tuning. The paper also releases the Celerity model family, trained under this collapse regime.

## Strengths

1. **Scale-up of collapse is a real and non-trivial contribution.** Figures 1 (middle) and 6 show normalized training loss curves collapsing across 300M–3.9B models at fixed TPP and matched τ. Prior work (Qiu et al., 2025) showed collapse only on small autoregressive tasks (<100M) with vanilla Adam and no weight decay. Demonstrating the effect holds at practical LLM scale with AdamW, weight decay, co-scaled depth, and realistic vocabularies is a genuine service to the community.

2. **Practical diagnostic case study is compelling.** The 1.8B numerical-instability example (Fig. 1 right, lines 204–206) is the paper's most viscerally concrete contribution: the collapse residual caught a problem at ~60% of training that was invisible in raw loss until ~90%. This is a clear and practical benefit.

3. **Early stopping via collapse is convincingly demonstrated.** Figure 9 shows the "predicted best" method selects the optimal hyperparameter with negligible loss gap after only 10–30% of training, while "current best" (common practitioner practice) is unreliable. The clean framing that τ-fixed sweeps preserve ordering (Fig. 7) provides a principled justification for why the method works.

4. **Clear synthesis of τ as a unified control.** The paper shows (Fig. 3) that the normalized AdamW timescale τ subsumes the individual effects of learning rate η, weight decay λ, and batch size B on TLC shape. This synthesis is well motivated and usefully demystifies why these three hyperparameters interact in shaping loss curves.

## Weaknesses

### Fatal

None.

### Major

None. The paper's core claims—that collapse scales to practical LLM regimes, that τ/TPP/LR-schedule controls govern it, and that collapse residuals enable useful diagnostics and early stopping—are supported by the evidence presented.

### Minor

1. **The early-align diagnostic's calibration window is not discussed as a limitation.** The paper normalizes in-progress curves by choosing the normalizer L(T) so that ℓ(t) best aligns with the smallest-scale reference over the 25–50% portion of training (line 194). This means any training pathology that begins before ~25% and persists through the calibration window can be partially normalized away, reducing the residual signal. The paper presents the 1.8B case study (problem at ~60%, after the window) as evidence of sensitivity, but does not disclose that divergences starting earlier could be masked. The alternative "Estimate" strategy (extrapolating via power law) is mentioned but not analyzed. This is a caveat that practitioners would need to know.

2. **Celerity's evaluation scope is too narrow to fully support the "compute-efficiency frontier" claim.** The claim (lines 33, 187, 210) rests on average accuracy across 7 commonsense reasoning tasks (arc-c, arc-e, boolq, hellaswag, piqa, siqa, winoqrande). Missing are coding (HumanEval, MBPP), math (GSM8K, MATH), and knowledge-intensive benchmarks (MMLU), so it is unclear whether the compute-efficiency advantage generalizes. Additionally, no error bars or variance estimates are provided for the evaluation points in Fig. 2, even though several of these tasks have high instance-level variance. The data-annealing confound raised by the reviewer is explicitly addressed in the paper (line 159) and reflects a methodological choice rather than a flaw.

3. **The parametric surrogate model (§5, Eq. 4–5) is not compared against simpler alternatives.** The paper introduces a 6-parameter functional form for normalized TLCs but never directly compares it against simply using the nearest empirical small-scale TLC as the reference. The paper explains that the surrogate can generate curves for control combinations not yet trained (lines 239–240), but the cost of this extra complexity vs. the empirical baseline is not quantified. Additionally, the early-stopping validation (Fig. 9) compares "predicted best" only against "current best" and "random" baselines; comparison against existing loss-curve prediction or early-extrapolation methods would help assess whether collapse-based prediction is a meaningful advance or merely another workable method.

4. **Architecture shift between analysis and deployment is not explicitly validated.** The experimental analysis in Section 3 uses GPT2-like models with SwiGLU, ALiBi, and µP. Celerity (Section 4) uses Squared ReLU, ALiBi, and CompleteP. The theoretical framework (noisy quadratic model, scale invariance) is derived under µP, and the paper does not run the τ-sweep experiments (Fig. 3) under CompleteP to verify that the same controls govern TLC shape under the different parameterization. The empirical results (Fig. 6) show that collapse still occurs, so the concern is not fatal, but the theoretical transfer is assumed rather than evidenced.

5. **Early-stopping validation is limited to λ sweeps.** The procedure in §5 is described generically (for "a hyperparameter"), but the main validation (Fig. 9) only sweeps weight decay λ. Validating on a sweep over learning rate η or batch size B would increase confidence in generalizability.

6. **No repeated-seed experiments.** All claims about collapse tightness and prediction accuracy rest on single runs. Reporting even 2–3 seeds for a subset of conditions would strengthen the evidence that deviations-from-collapse are meaningful signals rather than noise. (This is noted as a limitation rather than a fatal gap, since single-run evaluation is the norm at this training scale.)

### Trivial

- The abstract states collapse occurs "precisely when optimization hyperparameters are set optimally" (line 9); the paper's own Fig. 4 (right) shows collapse at non-optimal τ when τ is matched across scales. The conflation of "collapse" with "optimal τ" is a minor but persistent imprecision.

## Nice-to-Haves

- A direct comparison between the parametric surrogate (Eq. 4–5) and the simpler approach of using the nearest empirical small-scale TLC as the reference would help readers assess whether the parametric form earns its complexity.
- The "Estimate" strategy (extrapolating L(T) via power law) could be evaluated as an alternative normalization method, potentially complementing the early-align approach when divergences affect the calibration window.
- An explicit statement about whether the Celerity models will be publicly released would strengthen the paper's value to the community (this information may exist in the stripped appendix).

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Weakness about Celerity evaluation "size mismatch" (comparing 3.9B to 7B models).** The x-axis in Fig. 2 is FLOPs, not parameter count. Comparing a 3.9B model against 7B models on a per-FLOP basis is a valid compute-efficiency comparison; if the smaller model achieves comparable accuracy with fewer FLOPs, it *should* appear more compute-efficient. This is not a flaw but a design feature of the analysis. **Removed.**

- **Weakness about the normalization being "materially weaker" than Qiu et al.'s supercollapse.** The paper uses a simpler normalization (dividing by final loss only, with L̂=0) and achieves collapse. This is an empirically justified design choice, not a weakness. The paper clearly states its normalization method (line 101) and does not claim "supercollapse." **Removed.**

- **Weakness about "data-annealing confound."** The paper explicitly addresses this as a philosophical choice (line 159), stating that Celerity avoids task-specific data annealing to serve as a clean comparison baseline. This is a methodological choice, not an unrecognized confound. **Removed.**

- **Criticism about "model release not stated."** The appendix is stripped by the parser; this information likely exists in the original submission. Per hard rules, criticism about release status of the paper's own artifacts that may be documented in the stripped appendix is removed. **Removed.**

- **Strength about "this paper addressed an important problem"** — generic and lacks specific content. **Removed.**

## Novel Insights

The most insightful synthesis from the review is that the paper's diagnostic application (collapse residuals for early detection) and its early-stopping application pull in opposite directions: the diagnostic requires the collapse reference to be *sensitive* to deviations, while the early-stopping application requires it to be *predictive* (i.e., the reference must match observed curves well). The paper does not discuss this tension. A method that produces tight collapse (good for prediction) may be less sensitive to subtle divergences, and vice versa. Additionally, the review surfaces that the paper's strongest concrete result—the 1.8B diagnostic case study—is its most powerful advertisement, yet the simplicity of the early-align method means the diagnostic's reliability is directly tied to the quality of the alignment window, a point worth examining more carefully in future work.

## Suggestions

1. **Disclose the early-align calibration limitation explicitly.** Add 2–3 sentences acknowledging that normalization over the 25–50% window means divergences that affect this region may be partially normalized away, and note that the "Estimate" strategy (power-law extrapolation) is a complementary approach that avoids this issue.

2. **Broaden the Celerity evaluation or soften the claim.** Add coding and knowledge benchmarks if feasible. If the evaluation cannot be expanded, downgrade the "compute-efficiency frontier" framing to "competitive on a subset of commonsense reasoning tasks."

3. **Benchmark the parametric surrogate against the empirical baseline.** Compare the parametric form (Eq. 4–5) against simply using the nearest trained small-scale TLC as the reference. If the empirical baseline works as well, the parametric form can be presented as a convenience option rather than a core method.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>