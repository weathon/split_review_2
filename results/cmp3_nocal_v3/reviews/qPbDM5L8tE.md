Now let me write the final consolidated review.

## Summary

This paper proposes CoRAL, a modular framework for contact-rich robotic manipulation that separates perception (VLM for pose tracking and physical parameter estimation) from reasoning (LLM for generating cost functions and contact strategies), with plans executed by an MPPI controller and failures diagnosed via an LLM-driven outer loop. The core idea — using an LLM to symbolically formulate the cost structure of a model-predictive controller, avoiding the need for demonstration data — is well-motivated. The system is evaluated on six simulated manipulation tasks against OpenVLA-OFT, π₀.₅, human-expert-designed costs, and several ablations.

## Strengths

1. **Well-motivated modular architecture (Sections 3.1–3.4).** The separation of VLM (perception, physical parameter estimation) and LLM (cost function design, contact strategy, failure diagnosis) with MPPI for reactive control is clearly articulated. The ablation study directly tests this design choice — the "Unified VLM" variant fails on nearly all tasks — providing concrete support for the core architectural thesis.

2. **Genuinely zero-shot with respect to demonstration data.** The method requires no task-specific tele-operation data or imitation learning. The VLM estimates physical parameters from visual appearance, the LLM generates cost functions and contact strategies from task descriptions, and the MPPI controller executes them. If validated, this represents a meaningful reduction in data requirements compared to end-to-end VLA approaches.

3. **The online adaptation loop (outer loop) is a genuinely interesting capability (Section 3.4).** Using the LLM to diagnose execution failures, correct world model parameters, and reformulate the cost function mid-task goes beyond what most decoupled reasoning frameworks do. The qualitative example of cost function re-weighting illustrates a concrete advantage over black-box policies.

4. **Explainability is a real byproduct of the design.** The LLM's ability to produce natural-language diagnoses of failures and corrective actions is a genuine advantage that the paper correctly highlights.

## Weaknesses

### Fatal
None.

### Major

1. **Internal inconsistency in the mass correction experiment (Section 4.1.4, Figure 4) undermines the central evidence for online parameter adaptation.** The text (lines 220–221) states: "we intentionally initialized the Evaluation World with a severely overestimated mass (2.0 kg vs. a ground truth of 0.1 kg)." The Figure 4 caption (lines 244–246) describes a plot where both the "Corrected Mass" and "Initial Mass" start at ~1.0 kg, and the corrected value converges to ~0.85 kg. These numbers are irreconcilable: (a) the initial value is 2.0 kg in the text but 1.0 kg in the figure; (b) the claimed "ground truth" is 0.1 kg, yet the corrected value converges to 0.85 kg — an 8.5× error, not "remarkably close" as claimed; (c) if the true simulation mass is 2.0 kg (which the text says was used to initialize the Evaluation World), the Planning World estimate at 0.85 kg is not close to that either. The reader cannot determine what was actually measured or what the ground truth was. This is the paper's primary direct evidence for online physical parameter correction, and its self-contradiction substantially weakens confidence in that claim.

2. **Statistical evidence is too weak for the confidence of the claims.** All experiments use n=10 trials per condition. With binary success/failure outcomes, the 95% binomial confidence intervals are wide (e.g., 4/10 → [~12%, 74%]; 2/10 → [~3%, 56%]). The paper uses language like "significantly boosted" (2/10→4/10), "dramatic performance drop" (4/10→0/10), and "catastrophic failure" without reporting confidence intervals or statistical significance tests. For instance, the difference between 4/10 (full CoRAL) and 8/10 (Expert FSM) on T1, or between 2/10 (w/o Memory) and 4/10 (full CoRAL), falls within chance variation at n=10. The paper overstates the reliability of its quantitative results.

### Minor

3. **LLM-MPPI interface is underspecified for reproducibility.** The paper describes *what* the LLM outputs (cost function structure, contact strategy) but not *how* these outputs are produced or consumed. Missing details include: the prompt template for cost function generation, the output format (JSON? Python code? parsed natural language?), how the contact strategy (Eq. 3) is generated from an image and task description, how the RAG memory embeds and retrieves experiences (embedding model? similarity metric?), and how the outer loop's logged episode data is formatted for LLM diagnosis. This is the core technical contribution, and the interface specification is critical for reproducibility.

4. **VLA baseline comparison is framed too strongly.** The VLA models (OpenVLA-OFT, π₀.₅) are evaluated zero-shot using LIBERO checkpoints on custom-designed tasks that require force control, multi-contact reasoning, and long-horizon planning — capabilities these models were never designed or trained for. Their failure is informative (it demonstrates the limitations of the VLA paradigm on contact-rich tasks) but the more meaningful comparison is against the human expert-designed cost baselines, where CoRAL consistently underperforms (e.g., T1: 4/10 vs 8/10; T6: 7/10 vs 9/10). The paper's headline framing ("CoRAL significantly outperforms both state-of-the-art baselines") obscures this gap.

5. **Randomization ranges for physical parameters are not reported.** The paper states that object masses, surface friction coefficients, and box dimensions are randomized (line 155), but reports no ranges or distributions. Without this information, it is impossible to assess whether the randomization is meaningful (e.g., masses varying from 0.1–0.2 kg vs 0.1–10 kg produce very different difficulty levels).

6. **VLM physical parameter estimation accuracy is not evaluated.** The VLM estimates mass and friction from visual appearance, but the paper never reports how accurate these estimates are. This directly affects how important the outer loop's correction capability is, and whether failures stem from poor initial estimates or the MPPI controller.

7. **Reactive control augmentation (Eq. 7) conflates state and force feedback.** Equation 7 uses `x_des − x_measured` — a position/state error — but the description references "real-time sensors (e.g., force/torque)." It is unclear whether `K_f` maps state error to force commands, or whether the reactive term is intended as something else. The equation and description need to be reconciled.

### Trivial

8. The explainability demonstration (Section 4.1.4) is a single qualitative example with no quantitative evaluation of diagnosis correctness or recovery success rate.

9. No per-cycle timing or latency analysis is reported, which matters for a real-time control system.

## Nice-to-Haves

- **Fix, expand, and clarify the mass correction experiment.** Report corrected numbers consistently, show both mass and friction corrections across multiple seeds, and include the corresponding success-rate recovery. This experiment, properly executed, would provide the paper's strongest mechanistic evidence.
- **Specify the LLM-MPPI interface concretely** (prompt templates, example outputs, parsing code). This is not a tangential detail — it is the central technical contribution.
- **Increase trial counts and add statistical reporting.** At least 50 trials per condition on core comparisons, with binomial confidence intervals or a Fisher's exact test.
- **Replace the VLA comparison emphasis with a more informative baseline** such as CoRAL vs. MPPI with a fixed generic cost (isolating the LLM's contribution), or a time-constrained expert baseline.
- **Report VLM estimation accuracy** for mass and friction against ground-truth simulation values.
- **Real-robot validation** on even a single task would substantially strengthen claims about deployment in unknown environments.

## Removed Points
Weaknesses from the input review that were filtered out:
- "No real-world experiments" — The paper acknowledges simulation-only evaluation as a limitation (line 242). Demanding real-robot experiments for a method paper is scope creep. Moved to nice-to-have.
- "Ablation results are too catastrophic/uninformative" — The ablations are designed to test whether specific components are necessary; showing that removing them causes failure is the intended finding. The suggestion of intermediate variants is a nice-to-have, not a weakness.
- "VLA comparison is invalid/staged" — The comparison is informative even if the outcome is predictable; it is valid zero-shot evaluation. The criticism was retained in weakened form (Minor 4) about framing, rather than removed entirely. The "staged" framing was removed as it overstates the problem.
- "Missing appendix content / proofs" — The parser strips appendices; these exist in the original submission.
- Formatting, grammar, and presentation nitpicks — These are parser artifacts, not author errors.

## Novel Insights

The harsh review's most valuable observation is the mass correction experiment inconsistency — a specific, verifiable numerical contradiction between the main text and the figure caption that directly affects the paper's central evidence for online physical parameter adaptation. This is not a generic "evaluation could be stronger" criticism but a concrete flaw in the presented evidence. The reviewer also correctly identifies that the paper's statistical resolution (n=10, binary outcomes) is too low to support the confident language used, and that the core LLM-MPPI interface — the paper's main technical contribution — is described only at a conceptual level. These insights converge on a clear diagnosis: the paper has a promising architectural idea but insufficiently rigorous evidence in its current form.

## Suggestions

1. **Fix the mass correction experiment numbers immediately.** Ensure text, figure, and caption all report consistent values. Report the actual ground truth mass used in simulation, the initial estimate, and the corrected value with error bars across multiple runs.
2. **Run more trials.** n=10 is insufficient for binary success/failure metrics. Increase to at least n=50 for the core comparisons (full CoRAL vs w/o Refinement, full CoRAL vs Expert FSM) and report confidence intervals.
3. **Provide the prompt templates and parsing code** for the LLM-to-MPPI interface in an appendix or supplementary material.
4. **Report randomization ranges** for all randomized physical parameters.
5. **Report the VLM's parameter estimation accuracy** (mass, friction) against ground truth to establish the baseline that the outer loop is correcting from.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>