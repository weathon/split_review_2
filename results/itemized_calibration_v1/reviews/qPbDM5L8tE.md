Now let me produce the final consolidated review.

## Summary

CoRAL proposes a modular framework for contact-rich robotic manipulation that separates perception (FoundationPose + GPT-4o-as-VLM), reasoning (GPT-4o-as-LLM), and control (MPPI). The LLM generates symbolic cost functions and contact strategies that guide MPPI trajectory optimization, with an outer loop for online adaptation based on execution feedback and a memory unit for experience reuse. Experiments on six simulated contact-rich tasks compare against OpenVLA, π₀.₅, and human-designed cost baselines.

## Strengths

**1. A conceptually clean modular architecture with explicitly separated roles.** The paper carves out a well-defined design space distinct from monolithic VLA policies: the VLM handles perception and physical parameter estimation, the LLM handles strategic cost-function design and contact reasoning, and MPPI handles reactive control. The rationale for this separation is articulated clearly in §3.

**2. The ablation of unified vs. separated VLM/LLM roles is informative.** The "Unified VLM" variant (single GPT-4o for both perception and planning) fails catastrophically — 0/10 on 4 of 6 tasks (Table 1). While the ablation design is not perfect (it conflates role separation with prompt engineering), the result does suggest that forcing one model to handle both geometric perception and strategic planning degrades performance sharply. This is a genuine finding supporting the modular design thesis.

**3. The online parameter correction demonstration is compelling.** Figure 4 and §4.1.4 show the LLM iteratively correcting an initially wrong mass estimate (~1.0 kg → ~0.85 kg, with ground truth 0.1 kg) and friction estimate based on observed execution failures. This capability — online world-model correction mid-task — distinguishes the approach from static-policy VLAs and from one-shot LLM planners.

**4. The memory unit for reusing cost functions and contact strategies shows consistent although modest benefit.** Using RAG to retrieve previously successful plan tuples improves success rates across tasks (e.g., T1: 2/10 → 4/10; T5: 7/10 → 9/10; T6: 5/10 → 7/10) and reduces completion time. This is a practical addition that bootstraps performance without additional training.

**5. The guided vs. unguided contact strategy comparison is a clean experiment.** The analysis on T6 shows the LLM's symbolic contact strategy reduces task steps by 83.9% and end-effector path length by 63.9% (Figure 5/appendix). This directly demonstrates the mechanism's value.

## Weaknesses

### Fatal
None.

### Major

**1. The VLA comparison does not support the claimed "significant outperformance" as cleanly as asserted.** The paper compares CoRAL against OpenVLA-OFT and π₀.₅ using their official **LIBERO checkpoints** — models fine-tuned on pick-and-place tasks. However, T1, T4, T5, and T6 are custom tasks that the paper itself describes as "designed to be difficult for purely vision-based, collision-avoidant planners" (§4). The baselines are evaluated zero-shot on out-of-distribution tasks that the authors deliberately designed to challenge the very class of methods being compared. As Table 1 shows, the VLA baselines perform well on in-distribution LIBERO tasks (T2: 10/10, T3: 8-9/10) but poorly on custom tasks. This finding is uninformative — it tells us that a model fine-tuned on pick-and-place cannot solve novel contact-rich tasks without retraining, which is expected. The paper claims "CoRAL significantly outperforms both state-of-the-art baselines" (§4.1.1), but this conflates architecture choice (modular vs. end-to-end) with training distribution (LIBERO pick-and-place vs. custom contact-rich tasks). A controlled comparison would require fine-tuning the VLA baselines on the same tasks or ablating the backbone capacity.

**2. The LLM-to-controller interface is critically underspecified, harming reproducibility.** The paper states that the LLM generates a "structured cost functional" (Eq. 2) and is "free to introduce any cost terms constructible from the available state, pose, and action variables" (§3.2). But no details are provided on how the LLM's output is parsed into a cost function usable by the MPPI optimizer. Is the output LaTeX, JSON, Python code, or a structured API call? The same applies to the contact strategy (Eq. 3) — how does the LLM specify surface regions on arbitrary 3D meshes? No prompt template, output schema, or parsing mechanism is described in the paper (the appendix is stripped, so some details may be there, but the main text must stand on its own for a core methodological contribution). Since LLM-generated cost functions are the paper's central innovation, this omission is a serious reproducibility gap.

### Minor

**3. Performance claims are mismatched with the results against human-designed baselines.** The Human Expert (FSM) baseline achieves equal or higher success rates on **all six tasks** (Table 1): T1: 8/10 vs. 4/10; T2–T4: ties; T5: 10/10 vs. 9/10; T6: 9/10 vs. 7/10. The paper §4.1.2 correctly frames this as "narrowing the gap" and "approaching expert-level performance," but the abstract and introduction emphasize performance improvement over monolithic approaches without clarifying that the best-performing comparison system is a hand-designed one, not an automated one. The paper's genuine contribution — **automating cost-function design to reduce human engineering effort** — would be better served by leading with this framing rather than claiming performance superiority.

**4. No uncertainty quantification for 10-trial experiments.** Each condition uses N=10 trials. Key ablation differences are small (e.g., memory benefit on T1: 2/10 → 4/10; on T6: 5/10 → 7/10). The paper uses language like "significantly boosted" (§4.1.3) and "dramatic performance drop" (§4.1.3) without confidence intervals, error bars, or statistical tests. With N=10 and randomized parameters (mass, friction, dimensions), a difference of 2/10 may be within random variation. While N=10 is common in robotics, the strength of the claims warrants honest uncertainty reporting.

**5. No analysis of failure modes.** The paper does not characterize what causes the remaining failures (e.g., 3/10 on T6, 6/10 on T1). Are they perception errors (FoundationPose tracking failure), reasoning errors (GPT-4o generates a poor cost function), or control errors (MPPI cannot optimize the given cost)? Understanding this distribution would strengthen the contribution and guide future work. The paper does not discuss which component is the current bottleneck.

**6. Internal inconsistency in the w/o Pose Tracking results.** The paper states this ablation "resulted in a catastrophic failure across all tasks (0/10 success)" (§4.1.3), but Table 1 shows 9/10 success on T2. This discrepancy between the text and the table should be corrected.

### Trivial
None.

## Nice-to-Haves

- Provide the exact prompt template and output schema used for the LLM-to-MPPI interface, including how the LLM's cost terms are parsed and validated.
- Report Clopper-Pearson confidence intervals for the success rates given N=10.
- Include an analysis of GPT-4o API cost and wall-clock time per task, especially given completion times in Table 1 show CoRAL is substantially slower than VLA baselines on T2/T3 (45-49s vs. 5-12s).
- Discuss the practical implications of requiring known 3D CAD models for all objects (FoundationPose requirement).
- Extend the limitations section to discuss: reliance on known 3D models, API cost/latency, simulation-only results, and the fact that human experts outperform the automated system.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Simulation-only evaluation for a paper about contact-rich manipulation"** — Demoted to Minor/Nice-to-Have. Simulation papers are standard at ICLR; the paper's core contribution (online cost-function generation with LLM) can be evaluated in simulation. The reactive control augmentation (Eq. 7) motivated by sim-to-real does not make the paper fatally incomplete without real experiments.
- **"No analysis of GPT-4o API cost or latency"** — Moved to Nice-to-Have; useful context but not a core flaw that undermines the contribution.
- **"Section-by-section notes about the introduction and related work"** — These were observational commentary rather than specific, actionable weaknesses. The key observations have been folded into the weaknesses above where relevant.

## Novel Insights

The reviews surface a tension that the paper does not fully resolve: the core technical contribution (LLM-generated cost functions for MPPI with online closed-loop adaptation) is genuinely novel and well-motivated, but the paper's evaluation narrative tries to claim performance superiority over end-to-end VLAs with a comparison that cannot cleanly separate architecture from training distribution. The strongest evidence in the paper is not the VLA comparison but (a) the guided-vs-unguided contact strategy ablation (83.9% faster, 63.9% shorter path on T6), (b) the online parameter correction (Figure 4), and (c) the catastrophic failure of the unified VLM ablation. These demonstrate the mechanism working as intended. The paper would be strengthened by centering its contribution around **automated cost-function design with demonstrable benefits in adaptability and explainability** rather than around claiming state-of-the-art performance.

## Suggestions

1. **Reframe the contribution.** Lead with "automated cost-function design that reduces human engineering effort while approaching expert-level performance" rather than claiming performance superiority over end-to-end methods. Restructure the VLA comparison as a zero-shot generalization study rather than a direct performance comparison.

2. **Provide full interface details.** Include the prompt template, output schema (e.g., JSON specification of cost terms with weights, contact surface parameters), and parsing mechanism for the LLM-to-MPPI interface.

3. **Add statistical grounding.** Report Clopper-Pearson intervals for all binomial success rates to honestly communicate uncertainty given N=10.

4. **Add a failure-mode breakdown.** For each task, report what fraction of failures are attributable to perception, reasoning, or control errors.

5. **Fix the internal inconsistency** between the text (claiming 0/10 for w/o Pose Tracking on all tasks) and Table 1 (showing 9/10 on T2).

## Score and Decision

**Calibration Anchors (Retrieval-based):**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/WtHKqtHVXo.md` — "Generating Robot Policy Code for High-Precision and Contact-Rich Manipulation Tasks" | 4.00 | R1 | Yes | Very similar topic (LLM generating policies for contact-rich tasks), had real-robot validation but was scored 4.00 due to being called "ad-hoc" and "not general enough." Our paper has a more principled architecture but lacks real-robot experiments. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/JWrl5pJCnl.md` — "Instruct2Act" | 5.00 | R1 | Yes | Similar modular LLM pipeline; had similar comparison-fairness concerns (-5 weight) and real-robot experiments. Our paper has stronger ablations and online adaptation but no real robots. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iTsHStJKcm.md` — "Make a Donut" | 5.25 | R1/R2 | Yes | Language-guided zero-shot manipulation; had real-robot validation but weaknesses about open-loop planning and error recovery. Our paper's closed-loop adaptation is an advantage but we lack real-robot validation they had. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lvDHfy169r.md` — "Automated Rewards via LLM-Generated Progress Functions" | 5.75 | R2 | No | LLM generating reward functions; more rigorous evaluation across diverse tasks. Our paper is tackling a harder problem (contact-rich manipulation) but with weaker evaluation. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RQDuFF1rOn.md` — "Wonderful Team" | 3.67 | R2 | No | Multi-agent VLLM for zero-shot robotics; scored low for insufficient novelty and weak evaluation. Our paper is more principled and novel. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/IEduRUO55F.md` — "Eureka" | 6.25 | R2 | No | LLM reward design with evolutionary optimization; scored higher due to rigorous evaluation across 29 environments and outperforming human rewards. Our paper's evaluation is less comprehensive. |

**Round 1 Bracket:** After filtering the harsh critic's review and drafting, the paper's plausible score range is 4.0–5.5. The core architecture is more principled than the 4.0 anchor (WtHKqtHVXo) — stronger ablations, online closed-loop adaptation, clean modular separation — but the evaluation is not as rigorous as the 5.75–6.25 anchors which had real-robot validation, multiple environments, or statistical rigor.

**Final Placement:** The paper shares heavy-weight negative items with the 4.0–5.0 anchors: comparison fairness concerns (shared with JWrl5pJCnl at -5 weight), missing interface details (shared with WtHKqtHVXo at -5 weight), and no real-robot validation (shared with none of the positive-strength items from higher-scored papers, all of which had real experiments as a positive factor). The paper's genuinely positive items — clean ablations, online adaptation loop, informative unified VLM ablation — push it above the 4.0 anchor but the evaluation shortcomings prevent it from reaching the 5.75+ range. This puts the paper at **5.0**, between borderline reject and borderline accept.

**Score: 5.0** — The paper presents a well-motivated architecture and informative ablations, but the evaluation's structural limitations (unfair VLA comparison, underspecified core interface, no statistical uncertainty, no real-robot validation despite real-world framing) prevent the paper from supporting its stronger claims. The contribution is real — LLM-generated cost functions with online closed-loop adaptation for contact-rich tasks — but the current evidence is not sufficient for acceptance at ICLR.

**Decision: Reject**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>