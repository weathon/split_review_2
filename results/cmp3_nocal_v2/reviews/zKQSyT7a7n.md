## Summary

This paper introduces Visuo-Tactile World Models (VT-WM), the first multi-task world model that fuses exocentric vision with fingertip tactile sensing (Digit 360 sensors) for contact-rich robot manipulation. The core idea is that tactile signals provide direct measurements of contact that vision alone cannot disambiguate (e.g., whether the hand is touching an object or not), which the model leverages through a transformer-based predictor that autoregressively generates both visual and tactile next-step latents. The paper evaluates VT-WM against a vision-only counterpart (V-WM) on imagination quality (object permanence, causal compliance with Fréchet distance metrics and statistical tests) and zero-shot real-robot planning across five tasks, reporting consistent gains for the visuo-tactile model.

## Strengths

1. **Well-motivated and specific problem framing.** The paper identifies a concrete failure mode of vision-only world models — hallucinating object states under occlusion and visual aliasing in contact-rich manipulation — and makes a principled argument (Section 3.1, "hand around a cup" example) for why tactile sensing directly addresses this. This goes beyond a generic "multimodal is better" claim.

2. **Quantitative imagination evaluation with statistical rigor.** Rather than showing only qualitative rollouts, the paper uses CoTracker-based normalized Fréchet distance to measure object permanence and causal compliance, and reports paired t-tests with p-values (Section 4.1). This is a more rigorous evaluation than typical in this area, even if the metrics have limitations.

3. **Real-robot zero-shot planning across multiple contact-rich tasks.** The paper evaluates CEM-based planning on a real robotic system across five tasks of varying difficulty (Section 4.2, Fig. 8). The largest gains (Reach&Push: +35%, Wipe Cloth: +31%) appear on multi-step contact-rich tasks where the mechanistic argument for tactile grounding is strongest, lending credibility to the results.

4. **Clean central comparison design.** The comparison between VT-WM and V-WM on identical action sequences isolates the effect of adding tactile input within a shared architectural family, which is the correct design for answering "does touch help?"

## Weaknesses

### Fatal
None.

### Major

1. **V-WM baseline construction is not described in the main text.** The paper's central quantitative claims (33% object permanence gain, 29% causal compliance gain, up to 35% higher planning success) all rest on the comparison between VT-WM and V-WM. However, the paper never explicitly states how V-WM is constructed: is it the same 12-layer transformer with tactile tokens/encoder removed and retrained from scratch? Is it VT-WM with tactile inputs masked at inference? Is it a separately trained architecture? This matters because differences in parameter count, training procedure, or initialization could confound the comparison. The reader cannot tell whether the reported gaps reflect tactile information or simply a different model. While the appendix (not available here) may contain implementation details, the main text should at minimum state the relationship between the two models. This is the most significant weakness because it directly affects interpretability of the headline claims.

### Minor

2. **Limited trial counts for real-robot planning experiments.** The planning results (Section 4.2, Fig. 8) report success rates from 5 trials per task. With n=5, a single trial outcome shifts the reported rate by 20 percentage points. The differences for Push Fruits (83%→92%, ~0.4 successes) and Stack Cubes (75%→83%, ~0.4 successes) are within the noise floor of a 5-trial Bernoulli experiment. The larger gaps (Reach&Push: 69%→93%, Wipe Cloth: 70%→92%) are more robust. The paper does not report confidence intervals or exact binomial tests for these planning results, unlike the Fréchet distance experiments. The directional conclusion is likely correct, but the evidence is weaker than the point estimates suggest.

3. **The data efficiency experiment conflates multiple factors.** Section 4.3 compares VT-WM (fine-tuned on 20 demos + pre-trained multi-task data + CEM planning) against a BC policy (ACT, trained from scratch on 20 demos). The BC policy also receives tactile inputs (line 245: "receives the latest RGB and tactile inputs"), so the comparison is not about touch vs. no-touch. The experiment instead compares "pre-trained multi-task world model + planning" against "single-task imitation learning." The paper's framing in the abstract — "VT-WM shows data efficiency when targeting a new task, outperforming a behavioral cloning policy by over 3.5×" — attributes the gain to VT-WM specifically, but the role of tactile grounding in this particular comparison is incidental. The experiment is still informative, but the claim should be calibrated to what is actually tested.

4. **Causal compliance metric scope is narrower than the headline claim.** The metric measures Fréchet distance of *static* object keypoints (objects that should not move under applied forces). The companion object permanence metric tracks *moving* objects, but together these do not fully capture "compliance with the laws of motion" (abstract). For instance, they would not detect a model that moves objects in the wrong direction but at the right speed, or that violates Newton's third law. The headline claims are slightly broader than what the metrics actually measure.

5. **Non-significant degradation on one causal compliance task.** On the "scribble with marker" task, VT-WM performs worse than V-WM on causal compliance (normalized Fréchet distance ~0.50 vs ~0.35, p=0.23, not significant). The paper transparently reports this and correctly includes it in the 29% average, but the aggregate framing ("29% better compliance") somewhat overstates the consistency of the benefit.

### Trivial
None.

## Nice-to-Haves

- Validate tactile prediction quality quantitatively. The paper references Appendix B-fig. 13 for qualitative tactile visualizations, but the mechanism story (tactile grounding improves rollouts) would be strengthened by showing that predicted tactile latents correlate with ground-truth contact states (e.g., force magnitude, binary contact/no-contact).
- Report confidence intervals or exact binomial tests for the 5-trial real-robot planning results to calibrate the reader's uncertainty.
- Include a failure mode analysis for planning (e.g., do VT-WM and V-WM fail on different types of contact misjudgments?).

## Removed Points

- **"Tactile prediction quality is never evaluated"** — Removed because the paper explicitly references Appendix B-fig. 13 for tactile prediction visualization. The claim that evaluations are "never" performed is incorrect given the appendix content (which is stripped by the parser, not absent from the original submission).
- **"Related work on existing visuo-tactile dynamics models insufficiently positioned"** — The paper clearly cites the relevant prior works (Sutanto et al., Tian et al., Ai et al.) and states they are task-specific, which is a valid distinction. The reviewer's request for "explicit evidence of cross-task transfer" is a nice-to-have, not a weakness.
- **Various pure nitpicks about parameter values, frame rates, etc. being deferred to appendix** — Per policy, missing appendix details are parser artifacts, not author errors.
- **Insufficient hyperparameter disclosure** — Per policy, these are trivial implementation details.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. In a revision, state explicitly: "V-WM is [identical architecture with tactile encoder and tactile tokens removed / separately trained / etc.], trained on the same data with the same hyperparameters." This single sentence would resolve the main concern about the central comparison.
2. Reframe the data efficiency experiment (Section 4.3) as a comparison of "pre-trained multi-task world model + planning vs. single-task imitation learning" rather than claiming it demonstrates tactile-specific data efficiency. Alternatively, include an ablation comparing VT-WM vs. V-WM for data efficiency to isolate the touch modality's role.
3. For the real-robot planning results, either increase trial counts or report exact binomial 95% confidence intervals alongside point estimates.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>