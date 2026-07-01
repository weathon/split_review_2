Now I have sufficient calibration data. Let me produce the final consolidated review.

## Summary

CoRAL proposes a modular neuro-symbolic framework for contact-rich robotic manipulation that separates VLM (perception, physics estimation) and LLM (strategy, cost-function generation) roles, integrated with an MPPI controller in an inner-loop (high-frequency re-planning) / outer-loop (low-frequency LLM-driven adaptation) architecture. The LLM generates both the structure and weights of the MPPI cost function and proposes focused contact regions, while a memory unit stores and retrieves successful experience episodes.

## Strengths

1. **Well-motivated and clean architectural design.** The separation of VLM (perception/physics estimation) from LLM (reasoning/strategy formulation) is clearly motivated, and the inner/outer loop structure connecting these modules to an MPPI controller is intuitive. The ablation study (Table 1) demonstrates this empirically: the "Unified VLM" variant, which collapses these roles into a single model, fails catastrophically (0/10 on 4 of 6 tasks, 10/10 → 2/10 on T2). This is the paper's strongest empirical contribution.

2. **A genuinely interesting technical idea.** Using an LLM to generate the structure and weights of an MPPI cost function (Eq. 2) and to propose focused contact regions (Eq. 3) is a creative departure from prior LLM/MPC integrations (IMPACT, VLMPC) that use the LLM only as a perceptual guide or sub-goal identifier. The idea that the LLM can "program" the optimization objective itself is worth exploring and goes substantially beyond what prior work has attempted.

3. **Paper is clearly written and well-organized.** The figures (architecture diagram and task illustrations) are informative, and the reasoning about why each component matters is transparent.

## Weaknesses

### Fatal
None.

### Major

1. **No comparison against the most relevant baselines — other LLM/MPC integration methods.** The paper cites IMPACT, VLMPC, ThinkAct, and Inner Monologue in Related Work (§2, lines 37–45) as the closest related approaches—methods that "integrate foundation models with motion planners"—yet evaluates against none of them. Instead, the primary comparison is against OpenVLA and π₀.₅, which are end-to-end VLA models that directly output actions. While this comparison is not useless (it shows that end-to-end VLAs fail on contact-rich tasks), it is insufficient to support the paper's central claim that the proposed approach advances the state of the art in LLM/MPC integration. The paper would need to show that CoRAL outperforms or is competitive with the methods it positions itself against in the Related Work section.

2. **The mass correction experiment (Section 4.1.4, Figure 4) contains a discrepancy between the evidence presented and the paper's claim.** The text states: "we intentionally initialized the Evaluation World with a severely overestimated mass (2.0 kg vs. a ground truth of 0.1 kg)… the agent's belief about both mass and friction converged remarkably close to their true values." However, Figure 4 shows the "Corrected Mass" plateauing at approximately 0.85 kg, which is 8.5× the true mass of 0.1 kg. The y-axis scale (0.75–1.00 kg) does not even include the true value. The claim of convergence "remarkably close to their true values" is not supported by the presented evidence. This undermines the robustness claim that is a central part of the paper's narrative. Either the figure, the text, or the claim needs to be reconciled.

3. **Absolute success rates on the paper's flagship multi-stage task are low, and the expert FSM baseline consistently outperforms CoRAL.** On T1 (Push and Pick Cutting Board), CoRAL with Memory achieves only 4/10 success. More importantly, the Expert (FSM) baseline—a human-designed cost function—outperforms CoRAL on *every* task (8/10 vs. 4/10 on T1, 10/10 vs. 9/10 on T4, 10/10 vs. 9/10 on T5, 9/10 vs. 7/10 on T6). The paper frames this as "narrowing the gap," which is accurate, but the framing obscures that the gap remains large on contact-heavy tasks (T1: 40% vs. 80%). If the paper's core claim is that an LLM can substitute for expert effort in designing cost functions, the evidence shows it is currently a poor substitute.

### Minor

1. **No statistical significance or variance reported for any result.** All results are based on 10 trials per condition. On several tasks the differences across ablations are small (e.g., T4: 9/10 vs. 9/10 between CoRAL and w/o Memory; T5: 9/10 vs. 7/10). With 10 trials, a difference of 1–2 successful trials can arise from random seed variation. Without confidence intervals, standard deviations, or any significance test, the reader cannot assess which reported differences are meaningful.

2. **Several implementation details that would aid reproducibility are missing.** The paper does not specify: (a) the control frequency of the MPPI inner loop (with K=200 rollouts of H=50 steps, the real-time feasibility is unclear); (b) the memory unit's embedding model, similarity metric, and retrieval threshold (described only as "RAG" in Eq. 1); (c) how the LLM's free-form cost function output (Eq. 2 is "illustrative only") is parsed, validated, and enforced to prevent malformed or non-sensical cost terms. These are not fatal omissions but would make it difficult for others to build on this work.

3. **The claim of LIBERO benchmarking is overstated.** Only 2 of 6 tasks (T2, T3) are from the LIBERO suite, and these are the simplest pick-and-place tasks where all methods perform well. The other 4 tasks are custom. This is acknowledged in the paper's experimental setup (§4, line 151) but the abstract mentions "standardized benchmarks from the LIBERO suite" without indicating the limited scope.

### Trivial
None.

## Nice-to-Haves

- A comparison against at least one LLM/MPC baseline (e.g., a simplified IMPACT or VLMPC adapted to the same simulation setup).
- Analysis of GPT-4o API costs and per-cycle latency, to help assess the system's real-time feasibility.
- An ablation where the MPPI controller's feedback gain matrix K_f (Eq. 7) is also determined by the LLM, rather than being a pre-tuned hyperparameter, which would make the "zero-shot" claim stronger.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **"The system fails on the majority of trials on the very tasks it was designed to solve"** — This is true only for T1 (4/10). On T2–T6, success rates range from 7/10 to 10/10. Removed as an inaccurate overall characterization.
2. **"The VLA comparison is not informative"** — The OpenVLA/π₀.₅ comparison is still informative: it shows that end-to-end VLAs fail on contact-rich tasks, which is a valid empirical finding. The real weakness is the *missing* LLM/MPC comparison, not that the VLA comparison is useless. Reframed.
3. **"System avoids task-specific data, not data in general"** — The paper only claims to avoid task-specific tele-operated data, not all data. This is a strawman criticism. Removed.
4. **Generic/superficial strengths** from the input review (e.g., "clean paper organization") — Kept because the paper is genuinely well-organized. No strengths were dropped.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's analysis of the mass correction discrepancy is a genuinely novel finding that the original paper's internal reviewers apparently missed.

## Suggestions

1. **Reconcile the mass correction evidence.** Either correct the claim in the text, fix the figure, or provide a clear explanation of what "true values" refers to. As it stands, the evidence contradicts the claim.
2. **Add at least one LLM/MPC baseline comparison.** The paper cites IMPACT and VLMPC as the closest related work; evaluating against a re-implemented or adapted version of at least one of these is essential to support the claimed contribution.
3. **Report per-trial statistics or confidence intervals** for the main results, given the small number of trials (10 per condition).
4. **Report the real control frequency** of the MPPI inner loop in Hz and briefly comment on whether the system can run at a useful rate for the manipulation tasks shown.
5. **Discuss the failure modes** for the ~60% of T1 trials that fail — are failures due to poor initial VLM estimates, the LLM generating a bad cost function, MPPI failing to find a good trajectory, or the reactive controller being insufficient?

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| WtHKqtHVXo (Generating Robot Policy Code) | 4.00 | 1 | Very similar topic (LLM for contact-rich manipulation). Weaker evaluation (only 2 task types, no ablation studies for LLM component). CoRAL is stronger across all dimensions. |
| cbVnJa4l2o (LLM+A) | 4.00 | 1 | Similar idea (LLM for planning + control) but simpler tabletop tasks. CoRAL has more complex tasks and stronger architecture justification. |
| iTsHStJKcm (Make a Donut) | 5.25 | 1 | LLM+MPC for deformable objects with real-robot validation. CoRAL has stronger ablation study but no real-robot experiments. Comparable overall. |
| c0chJTSbci (Zero-Shot Robotic Manipulation) | 6.25 | 2 | Stronger benchmark evaluation (CALVIN) with real-robot experiments and comparison against RT-2-X. CoRAL has more novel architectural contribution but weaker evaluation. |

**Round 1 bracket:** [4.0, 6.0]

**Round 2 narrowing:** Within this bracket, CoRAL clearly exceeds the 4.0 papers (more tasks, stronger ablation, more novel contribution) but falls below the 6.25 paper (no real-robot, no comparison against closest baselines, mass correction discrepancy). The closest comparable paper is "Make a Donut" at 5.25, which had real-robot experiments but weaker ablation. CoRAL's mass correction issue and missing baseline comparison prevent it from reaching that level.

**Final score:** 5.0 — The paper presents a genuinely interesting architectural idea with a clean ablation study, but the evaluation has significant gaps (no comparison against the most relevant baselines, a discrepancy between the mass correction claim and the evidence, no statistical rigor) that prevent its contribution from being firmly established.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>