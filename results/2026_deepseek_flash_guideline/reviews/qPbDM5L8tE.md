Now let me write the final consolidated review.

## Summary

CoRAL presents a modular neuro-symbolic framework for zero-shot contact-rich robotic manipulation. It integrates a VLM (GPT-4o) for physical parameter estimation, FoundationPose for 6-DoF object pose tracking, an LLM for generating MPPI cost functions and contact strategies, and an outer-loop adaptation mechanism with a memory unit for experience reuse. The core architectural claim is that explicitly separating VLM perception from LLM reasoning outperforms monolithic VLA approaches on contact-rich tasks. Experiments on six simulated manipulation tasks compare against OpenVLA-OFT, π₀.₅, human-expert-designed cost functions, and ablations.

## Strengths

1. **Controlled ablation quantifies the value of the LLM-provided contact strategy in pruning search (Section 4.1.4).** On the "Flip with Wall" task, the variant receiving only the cost function (no contact strategy) required 199 steps and 3.69 m of end-effector travel, while the full system needed 32 steps and 1.33 m — 83.9% fewer steps and 63.9% shorter path. This is direct, quantitative evidence that the LLM's symbolic contact regions transform an otherwise intractable search into a tractable one.

2. **Separating VLM from LLM roles is shown to be decisive through a clean ablation (Table 1, Section 4.1.3).** The "CoRAL (Unified VLM)" variant — using a single VLM prompt for both perception and planning — achieves 0/10 on four tasks and only 2/10 on the simplest pick-and-place. The full system with separated roles achieves 9–10/10 on those same tasks (T2–T5). This directly validates the paper's central design choice.

3. **Human-expert cost baselines provide a calibrated upper bound (Section 4.1, Table 1).** The Expert (FSM) variant achieves 8–10/10 on five of six tasks, showing CoRAL reaches 9–10/10 on T2–T5 and 7/10 on T6 — close to the expert ceiling on most tasks — while identifying where the framework still falls short (T1: 4/10 vs. 8/10).

4. **Ablating FoundationPose confirms a dedicated pose estimator is non-negotiable (Section 4.1.3).** The "w/o Pose Tracking" variant achieves 0/10 on five of six tasks. The VLM produced "physically impossible pose estimations ('hallucinations')" that rendered the planner's output useless.

## Weaknesses

### Major

1. **Mass-correction experiment has a verified internal inconsistency (Section 4.1.4, Figure 4).** The text states the evaluation world was initialized "with a severely overestimated mass (2.0 kg vs. a ground truth of 0.1 kg)" and that the agent's belief "converged remarkably close to their true values." However, Figure 4 shows a "Corrected Mass" starting at 1.00 kg and dropping to approximately 0.85 kg on a y-axis ranging from 0.75 to 1.00 kg, with an "Initial Mass" constant at 1.00 kg. These numbers are irreconcilable with the text: the initial estimate in the figure is 1.00 kg (not 2.0 kg), and the corrected value of ~0.85 kg is 8.5× the stated ground truth of 0.1 kg — not "remarkably close." No friction correction figure is shown. This inconsistency undermines a central robustness claim and must be resolved before the paper's evidence can be taken at face value. (Note: if this is a figure or text error, it is fixable; as presented, the claims do not match the data.)

### Minor

2. **VLA comparison framing oversells the finding (Section 4.1.1).** The paper calls the VLA outperformance a "critical finding," but the comparison is between fundamentally different architectures with different information access — CoRAL uses FoundationPose, a dynamics model, force feedback, and GPT-4o API calls. The VLA baselines receive only RGB(-D) images. The result that end-to-end models fail on contact-rich tasks while a system with pose tracking, a dynamics model, and online GPT-4o adaptation succeeds is not surprising. The paper appropriately includes human-expert cost baselines (which provide a more controlled comparison), but the abstract and introduction emphasize the VLA comparison too heavily. Reframing contributions around the ablation and expert comparisons would strengthen the paper.

3. **No statistical testing or variance reporting (Section 4).** All experiments use 10 trials per condition with a binary success metric, but no confidence intervals, standard deviations, or significance tests are reported. With n=10 and binary outcomes, the 95% Clopper-Pearson confidence interval for a 4/10 success rate spans approximately 12% to 74%. Several ablation differences are small (e.g., 2/10 vs. 4/10 on T1) and could arise from random variation. Completion times are reported as point estimates without variance despite substantial variation across conditions.

4. **No quantitative evaluation of VLM physical parameter accuracy.** The VLM estimates mass and friction from visual appearance (Section 3.1), which is a genuinely hard inverse problem. The paper never evaluates how accurate these estimates are across randomized trials, nor does it ablate the sensitivity of overall performance to the quality of these estimates. The mass-correction experiment attempts this but is muddled by the inconsistency above.

### Trivial

5. **LIBERO tasks are not clearly identified.** The paper mentions incorporating "two benchmark tasks from the LIBERO suite" (line 151) but the task descriptions T1–T6 do not map to standard LIBERO task names. It is unclear which tasks are LIBERO and which are custom.

6. **Explainability claim not systematically evaluated.** The paper cites explainability as a benefit (Section 4.1.4) and provides an anecdotal example of an LLM diagnosis, but no user study or systematic analysis is conducted.

## Nice-to-Haves

- Reporting computational budget/wall-clock control frequency. Table 1 shows CoRAL is 3–9× slower than VLA baselines, but this is not discussed as a limitation.
- A clean comparison: MPPI with a generic (non-expert, non-LLM) fixed cost function, to isolate what the LLM's cost generation adds beyond a reasonable default.
- Real-robot validation would substantially strengthen the claims.

## Removed Points

- **"Comparison to VLAs is structurally unfair and uninformative"**: Demoted from the critic's "Critical Issue" to Minor. The comparison is between different paradigms with different information access, which is common practice in ML papers. The paper also includes controlled human-expert and ablation baselines. The critic's framing overstated the problem; the real issue is that the paper oversells the VLA comparison, not that it is invalid to include it.

- **"Non-smooth cost function term (indicator in Eq. 2) would make optimization difficult"**: Removed. MPPI is a sampling-based method that does not require gradient information from the cost function; discontinuous terms are handled naturally by the weighted importance sampling framework.

- **"Contact strategy underspecification"**: Removed. Eq. (3) clearly defines the mathematical form of the contact point generation from surface regions, and the text explains that {R_j} are specified by the LLM. The mechanism is adequately described for the paper's scope.

- **"Missing related work on Eureka/Text2Reward"**: Removed per instructions (no external sources to confirm).

- **"Limitations section too brief"**: Removed. The paper identifies the key limitations (vision model fidelity, computational latency) and refers to the appendix for more detail. This is adequate for a conference paper.

- **Strength about online adaptation recovering from mis-initialized parameters**: Moved here because the specific evidence (Figure 4) contains the verified inconsistency. The adaptation mechanism itself is still supported by other evidence (the w/o Refinement ablation), but the flagship quantitative evidence is not credible as presented.

## Novel Insights

The harsh critic rightly identifies that the paper's most valuable comparison is not against VLAs but against the human-expert cost baselines and ablations. The Strength Finder correctly highlights that the contact strategy ablation (T6, 83.9% fewer steps) and the Unified VLM ablation (0/10 on complex tasks) are the paper's strongest pieces of evidence — they directly test the architectural claims rather than comparing against fundamentally different systems. The mass-correction inconsistency is the single most damaging point because it undercuts the paper's flagship evidence for online adaptation. Beyond these, the reviews do not surface genuinely novel insights beyond what the paper itself contributes.

## Suggestions

1. **Fix the mass-correction experiment.** Reconcile the numbers in the text with Figure 4. If the figure is correct, rewrite the text to describe the actual correction magnitude (1.00 kg → 0.85 kg against a ground truth of 0.1 kg) and honestly discuss what this means for the system's robustness. If the text is correct, replace or correct the figure. Either way, remove the phrase "converged remarkably close to their true values" unless the data supports it.

2. **Report confidence intervals or per-trial breakdowns** for the binary success metrics. With n=10, readers need to assess whether differences are meaningful.

3. **De-emphasize the VLA comparison** and reframe contributions relative to the human-expert cost baselines and ablations, which are more informative and controlled.

4. **Evaluate the VLM's physical parameter estimation accuracy** quantitatively, and show how performance varies with estimation quality.

5. **Identify which LIBERO tasks correspond to which T1–T6 labels** for clarity.

## Score and Decision

**Initial bracket (Round 1):** Based on retrieved anchors, the paper sits between the "borderline reject" cluster (avg 4.0–5.25, e.g., "Generating Robot Policy Code..." at 4.00 and "Make a Donut" at 5.25) and the "accept" cluster (avg 6.0+, e.g., HAMSTER at 6.00). CoRAL has a clearer architecture and better ablations than the 4.0 papers, but the mass-correction inconsistency, simulation-only evaluation, and overclaimed VLA comparison prevent it from reaching the 6.0 level.

**Narrowing (Round 2):** Direct comparison with "Make a Donut" (5.25, Reject) — both are zero-shot LLM-guided manipulation systems with simulation-only evaluation. CoRAL has stronger ablations but also has the verified mass-correction inconsistency, which is a more concrete flaw. The paper by "Generating Robot Policy Code for Contact-Rich Manipulation Tasks" (avg 4.00, scores 1,5,5,5) is the most topically similar: same LLM-for-contact-rich-manipulation problem. CoRAL is substantially stronger in architectural design and experimental breadth, justifying a higher score.

**Final score: 5.0** — The paper presents a well-motivated architecture with informative ablations, but a verified inconsistency in a core experiment and the simulation-only evaluation are significant weaknesses. The contribution is real but does not yet meet the acceptance bar.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>