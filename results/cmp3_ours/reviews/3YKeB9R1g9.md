Now I have sufficient calibration data. Let me write the final review.

**Calibration Assessment:**
- **Bracket round 1**: Papers most similar to this one (loss curve prediction/practical scaling) score between 5.2 and 8.0. The strongest match is "Scaling Law with Learning Rate Annealing" (6.75) which had a similar mix of genuine empirical contributions and heuristic modeling gaps, and "A Multi-Power Law for Loss Curve Prediction" (6.00, accepted). The "Small-scale proxies for large-scale Transformer training instabilities" (8.00) sets a higher bar for systematic validation that this paper does not reach.
- **Final range**: 6.0–7.0. The paper's core collapse demonstration is more novel than the loss-curve-fitting anchors, supporting the upper end; but the single-incident diagnostic and limited surrogate validation prevent it from reaching the 7.5+ tier.

Let me produce the final review.

## Summary

This paper demonstrates that training loss curves (TLCs) from LLMs of different sizes (111M–3.9B parameters) collapse onto a single universal trajectory after normalization, provided three controls are matched: AdamW timescale τ, tokens-per-parameter ratio (TPP), and learning-rate schedule. The authors introduce the Celerity model family trained with this collapse property, show that collapse residuals serve as an early diagnostic for training pathologies (via a real 1.8B numerical instability case), and propose a method for early stopping in hyperparameter tuning by fitting a small-scale parametric surrogate. The core empirical finding—that collapse persists at LLM scale under practical training recipes—is novel and well-supported.

## Strengths

1. **Clean identification of collapse conditions at meaningful LLM scale (Sec. 3, Figs. 3–4).** The paper systematically sweeps η, λ, and B independently to show that τ is the unifying variable (Fig. 3). The scale-invariance demonstration at fixed TPP/τ spans from 111M to 3.3B parameters—a 1000× FLOPs range—and goes substantially beyond Qiu et al. (2025), which was limited to small models without weight decay. This is a genuine empirical advance.

2. **Concrete diagnostic case study with a complete causal chain (Fig. 1 right, Sec. 4).** The 1.8B numerical instability example traces from observation (collapse residual divergence at ~60% of training) through diagnosis (a kernel bug triggered at specific microbatch sizes) to repair (training tracks the reference after fix). This provides a compelling proof-of-concept for the practical value of collapse monitoring.

3. **Principled early stopping procedure with clean baselines (Sec. 5, Fig. 9).** The "predicted best" method (aligning partial TLCs to a small-scale reference to infer final loss) demonstrably outperforms both "current best" (the practitioner heuristic used by Falcon) and random baselines at early stopping points (10–30% of training). The comparison is fair because the baselines mirror actual practice.

4. **Honest self-assessment of limitations.** The paper acknowledges Celerity's weaker parameter efficiency (line 189), small early deviations from perfect collapse at 20 TPP (line 202), and larger-model divergences at 234 TPP on training data (line 202). This transparency strengthens credibility.

## Weaknesses

### Fatal

None.

### Major

1. **The diagnostic application (collapse residuals for detecting training pathologies) rests on a single incident with no systematic validation.** The paper claims that "deviations from collapse provide a sensitive, early diagnostic of training pathologies" (abstract, contribution list) but demonstrates this on exactly one real incident (the 1.8B numerical instability). There is no systematic evaluation: no injected perturbations with known timing, no measurement of false positive rate (what fraction of normal runs show residual excursions of comparable magnitude?), and no comparison to alternative monitoring methods (e.g., gradient norms, loss spike detectors). While the single case is compelling as an anecdote, it does not support a general claim about diagnostic value. The paper would be substantially stronger with even two or three additional examples or a controlled perturbation study.

2. **The Celerity compute-efficiency frontier claim lacks uncertainty quantification (Fig. 2).** The paper states Celerity models "form the accuracy/compute Pareto frontier" based on a single accuracy point per model with no error bars, multiple seeds, or statistical significance assessment. The paper also acknowledges Celerity uses a curated data mix emphasizing math and code (line 163), making it unclear whether the frontier position reflects the training recipe or data quality differences. However, this weakness is bounded: the core contributions (collapse conditions, diagnostics, early stopping) do not depend on Celerity being on the Pareto frontier. The authors should either add uncertainty estimates or soften the claim from "frontier" to "competitive with contemporary open models."

3. **The parametric surrogate (Eq. 4–5) is heuristic with limited validation scope.** The surrogate is central to the early stopping application, but its functional form is empirically motivated without convergence analysis, initialization sensitivity study, or justification of the alternating fitting procedure. Critically, the early stopping evaluation only tests λ sweeps at two specific (model size, TPP) combinations (1.7B/20TPP and 3.3B/30TPP). The paper motivates the method by showing sweeps with varying τ are problematic (Fig. 7 left) and fixing τ solves this (Fig. 7 right), but then only evaluates on λ sweeps where τ is already naturally controlled. Testing on B or η sweeps would better demonstrate the surrogate's general value.

### Minor

1. No variance or seed information is reported for any downstream evaluation in Fig. 2—it is not stated whether numbers are single-run or averaged.
2. The diagnostic narrative for the 1.8B incident stops at "tracked the reference TLC closely" without confirming whether the repaired run completed successfully and whether its final loss matched expectations.
3. The surrogate fitting procedure's convergence is not described: how many alternations between fitting b and q were needed? Does the procedure give the same result from different initializations?
4. No discussion of what magnitude of collapse residual constitutes a signal vs. normal variation in the monitoring application, which is needed for any practical deployment.

### Trivial

None.

## Nice-to-Haves

- Systematic validation of the diagnostic application via controlled perturbations (injected gradient noise, LR schedule corruption) across multiple model sizes, measuring detection latency and false positive rate.
- Testing the early stopping surrogate on batch size (B) and learning rate (η) sweeps, not just λ sweeps.
- Reporting whether the repaired 1.8B run completed successfully and matched its expected final loss.

## Removed Points

- "The paper asserts the Celerity compute-efficiency claim without uncertainty quantification" — RETAINED AS MAJOR WEAKNESS 2 (verified against Fig. 2).
- "The parametric surrogate and its fitting procedure are heuristic with limited validation" — RETAINED AS MAJOR WEAKNESS 3, but softened from the original framing: the surrogate works empirically on the tested configurations, which is sufficient at the proof-of-concept level.
- "Missing parts: no variance/seed info, no false positive rate discussion" — DEMOTED TO MINOR (these are real but secondary to the paper's core claims).
- Strengths about the paper addressing an important problem or targeting an interesting question — REMOVED (generic/superficial). Only strengths with specific content anchors were retained.
- The critic's "Strengthening the Paper on Its Own Terms" suggestions about systematic diagnostic validation and testing on B/η sweeps — MOVED TO NICE-TO-HAVES (constructive but not required for the contributions as stated).

## Novel Insights

None beyond the paper's own contributions. The harsh critic's analysis is thorough and well-calibrated but does not introduce novel analytical observations not already present in or derivable from the paper.

## Suggestions

1. Add uncertainty quantification (multiple seeds or confidence intervals) for the Celerity compute-efficiency plot, or soften the "Pareto frontier" claim to "competitive with contemporary open models."
2. Validate the diagnostic application with at least 2–3 additional examples or a controlled perturbation study to substantiate the generality claim.
3. Test the early stopping surrogate on batch size and learning rate sweeps beyond λ sweeps to demonstrate generality.
4. Describe the convergence behavior and initialization sensitivity of the alternating fitting procedure for the surrogate.
5. Report whether the repaired 1.8B run completed successfully and matched its expected final loss.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>