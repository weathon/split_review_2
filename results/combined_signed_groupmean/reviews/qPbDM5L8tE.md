Now I have sufficient calibration data. Let me compose the final review.

## Summary of Calibration

**Round 1 bracket:** The closest topical anchor is "Generating Robot Policy Code for High-Precision and Contact-Rich Manipulation Tasks" (avg 4.00), which shares the same topic (LLMs for contact-rich manipulation) and had weaknesses about missing baselines and limited novelty. Our paper has a stronger ablation study but introduces verifiable factual errors. The "Make a Donut" anchor (avg 5.25) had real-robot validation but closer to 5.25, while "Vision-Language Foundation Models" (avg 6.50) was a clearly stronger paper with SOTA results. The "GRAIL" anchor (avg 3.00) was much weaker.

**Round 2 narrowing:** Zooming into the 3.0–5.0 range confirmed the "Generating Robot Policy Code" paper (4.00) as the best comparator. "UniContact" (3.50) and "CORN" (4.75) are also relevant. Our paper has two verifiable factual errors that the 4.00 anchor lacked, pushing it slightly below 4.00, toward 3.5.

**Final placement:** Between 3.0 and 4.0. The paper has a well-designed ablation study (+10.00 impact) but two factual errors (-10.00 each) that undermine specific claims, plus limited statistical rigor (-8.97). This places it near 3.5 — a reject but not a strong reject.

Now let me write the final review.

**All anchors retrieved:**
1. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gwZ90hFSL2.md` — avg 1.00, Round 1, Not itemized. Unrelated paper.
2. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8QTpYC4smR.md` — avg 1.00, Round 1, Not itemized. Unrelated paper.
3. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Uj0h13lVrR.md` — avg 1.00, Round 1, Not itemized. Unrelated paper.
4. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5kMwiMnUip.md` — avg 1.40, Round 1, Not itemized. Unrelated paper.
5. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/oyXoGJQlUf.md` — avg 3.00, Round 1, Itemized. GRAIL — different topic (PDDL symbol grounding), much simpler evaluation. Our paper is clearly stronger.
6. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Q6HYM1EMu8.md` — avg 3.00, Round 1, Not itemized. LARG2 — LLM for reward/goal generation. Different topic.
7. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/I0To0G5J7g.md` — avg 3.20, Round 1, Not itemized. Self-improvement for foundation models. Different topic.
8. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/zEhTnQZB3D.md` — avg 2.33, Round 1, Not itemized. Continual RL with LLMs. Different topic.
9. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/WtHKqtHVXo.md` — avg 4.00, Round 1, Itemized. **Closest comparator.** LLMs for contact-rich manipulation. Had novelty/comparison weaknesses but no factual errors. Our paper has stronger ablations but factual errors.
10. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iTsHStJKcm.md` — avg 5.25, Round 1, Itemized. "Make a Donut" — LLM-guided deformable manipulation with real-robot. Stronger than our paper.
11. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NkYCuGM7E2.md` — avg 3.75, Round 1, Not itemized. LLMs for autonomous driving. Different domain.
12. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/qGL6fE1lqd.md` — avg 4.40, Round 1, Not itemized. LLMPhy — physical reasoning. Different setup.
13. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/MWHIIWrWWu.md` — avg 6.25, Round 1, Not itemized. MPC for musculoskeletal control. Different domain.
14. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/c0chJTSbci.md` — avg 6.25, Round 1, Not itemized. Zero-shot manipulation with diffusion models. Stronger paper.
15. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lFYj0oibGR.md` — avg 6.50, Round 1, Itemized. VLA imitation learning with SOTA results. Much stronger than our paper.
16. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/inOwd7hZC1.md` — avg 7.00, Round 1, Not itemized. MPC with pretrained models. Different approach.
17. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OI3RoHoWAN.md` — avg 8.00, Round 1, Not itemized. GenSim. Strong paper.
18. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7BLXhmWvwF.md` — avg 8.00, Round 1, Not itemized. Geometry-aware RL. Different approach.
19. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/KsUh8MMFKQ.md` — avg 8.00, Round 1, Not itemized. Thin-shell manipulation. Strong paper.
20. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/pISLZG7ktL.md` — avg 8.00, Round 1, Not itemized. Data scaling laws. Strong paper.
21. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Cf8HBieRzL.md` — avg 3.50, Round 2, Itemized. UniContact — contact synthesis. Had limited evaluation and missing baselines. Similar quality to our paper.
22. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Aqfwhna1D7.md` — avg 5.20, Round 2, Not itemized. CrayonRobo. Different approach.
23. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lvDHfy169r.md` — avg 5.75, Round 2, Not itemized. Automated rewards via LLM. Different topic.
24. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RhfYIJux9d.md` — avg 5.50, Round 2, Not itemized. Video2Policy. Different approach.
25. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/xcHIiZr3DT.md` — avg 2.50, Round 2, Not itemized. Vision-based tactile. Different topic.
26. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/koza5fePTs.md` — avg 2.00, Round 2, Not itemized. LLM planning benchmark. Different topic.
27. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RrIjnSMhMZ.md` — avg 2.50, Round 2, Not itemized. Open-ended learning. Different topic.
28. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/KTtEICH4TO.md` — avg 4.75, Round 3, Itemized. CORN — nonprehensile manipulation with zero-shot sim-to-real. Stronger than our paper due to real-robot validation.

**Impact-score comparison against closest anchor (WtHKqtHVXo, avg 4.00):**
- That anchor's strongest items: clear research question (+10.00), action space design (+8.95). Weakest: baselines (-9.96), limited novelty (-7.98), ad-hoc feel (-10.00).
- Our strongest: ablation study (+10.00). Weakest: mass inconsistency (-10.00), w/o Pose Tracking error (-10.00), single comparison (-10.00), statistical rigor (-8.97).
- Impact scores below -10.00 don't exist (cap), but our factual errors pull harder than that anchor's novelty concerns. The anchor had real-robot validation (+1.91) which we lack. However, our ablation study (+10.00) is a genuine strength the anchor lacked. Net: slightly below the anchor's 4.00, around 3.5.

Now let me write the final review.## Summary

This paper proposes CoRAL, a modular framework that integrates vision-language models and LLMs with a reactive MPPI controller for zero-shot contact-rich robotic manipulation. The key idea is to have the LLM generate the cost function structure and contact strategies for the MPPI planner, while a dedicated pose estimator (FoundationPose) and a VLM (GPT-4o) handle perception. An online adaptation loop and memory unit enable refinement from failures and reuse of past experiences. The system is evaluated on six simulated manipulation tasks against VLA baselines (OpenVLA, π0.5) and human-expert-designed cost baselines.

## Strengths

- **The ablation study convincingly demonstrates that each module is necessary.** The Unified VLM variant (0/10 on nearly all tasks) and the w/o Pose Tracking variant (0/10 on 5 of 6 tasks) provide strong evidence that separating perception from reasoning and using a dedicated pose estimator are genuine necessities, not just design preferences. The memory module also shows measurable improvement (e.g., T1 success from 2/10 to 4/10). [impact=+10.00]

- **The system's ability to output natural-language diagnoses of failures** (Section 4.1.4) is a genuine advantage over black-box policies. A concrete example is provided where the LLM correctly identifies a poorly weighted cost function and adjusts specific weights. [impact=+4.57]

## Weaknesses

### Major

- **The robustness experiment contains a clear numerical inconsistency that undermines a core claimed result.** The text (line 220) states: "we intentionally initialized the Evaluation World with a severely overestimated mass (2.0 kg vs. a ground truth of 0.1 kg)." However, Figure 4 shows a y-axis ranging 0.75–1.00 kg, with the "Corrected Mass" starting at 1.00 kg and converging to approximately 0.85 kg. Neither the initial value (1.00 kg, not 2.0 kg) nor the converged value (0.85 kg, not 0.1 kg) matches the textual claims. Since this experiment is presented as a centerpiece of the robustness argument (the paragraph claims "the agent's belief about both mass and friction converged remarkably close to their true values"), this inconsistency must be resolved. [impact=-10.00]

- **The paper claims the w/o Pose Tracking ablation "resulted in a catastrophic failure across all tasks (0/10 success)" (line 212) — but Table 1 shows 9/10 on T2 (Pick+Place Box).** This is a factual error that directly contradicts the paper's own data. While the broader point (pose tracking is critical for most contact-rich tasks) still holds (0/10 on 5 of 6 tasks), the text overstates the result and contains a clear inaccuracy. [impact=-10.00]

### Minor

- **All results are based on 10 trials per condition with no confidence intervals, standard deviations, or statistical tests.** With n=10, the difference between 4/10 and 2/10 (T1, with vs. without memory) is not statistically significant. This limits the reliability of the quantitative claims. [impact=-8.97]

- **The guided contact strategy analysis (83.9% faster, 63.9% shorter path) is based on a single comparison on a single task (T6) with no variance reported.** The precise percentages imply a rigor not supported by the data, which comes from one comparison without multiple runs. [impact=-10.00]

- **The closest prior methods (VLMPC, IMPACT) are discussed in Related Work but never experimentally compared against.** Since the paper claims to advance beyond these by having the LLM generate the cost function structure itself rather than just perceptual guidance, a direct empirical comparison would substantially strengthen the contribution. [impact=-5.62]

- **The comparison against OpenVLA and π0.5 on contact-rich tasks (T1, T4, T5, T6) is asymmetrical.** These baselines are evaluated using LIBERO checkpoints on tasks requiring skills (sustained force control, flipping with walls) absent from LIBERO, while CoRAL receives task-specific cost functions from GPT-4o. The claim that CoRAL "significantly outperforms both state-of-the-art baselines" on these tasks conflates out-of-distribution generalization failure with method superiority. The human-expert baselines partially mitigate this, but the framing overstates the result. [impact=-1.47]

- **The LLM prompt design, cost function validation mechanism, and memory unit retrieval details are not described.** The paper does not specify how the LLM knows which state variables are available for cost terms, how malformed or impossible cost functions are handled, or what embedding model is used for RAG retrieval. This limits reproducibility. [impact=-0.30]

- **All experiments are in simulation (ROBOSUITE/MUJoCo) with no real-robot validation.** The paper motivates the reactive control augmentation using the sim-to-real gap (line 126) and makes claims about real-world applicability, but these are entirely unvalidated on physical hardware. [impact=-0.15]

## Nice-to-Haves

- A direct experimental comparison against VLMPC or IMPACT would substantiate the claimed advance of LLM-generated cost functions over VLM-generated cost maps.
- Reporting wall-clock time, API call counts, and end-to-end latency would address the acknowledged computational latency concern (line 242).
- A larger number of trials (≥30) with confidence intervals would substantially strengthen the quantitative claims.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"The baseline comparison is fundamentally unfair"** — Demoted from "critical issue" to minor weakness. The comparison is asymmetric, but (a) the paper does not claim to beat the baselines on their own training tasks (T2/T3 show comparable performance), (b) the human-expert baselines provide a fairer comparison point, and (c) the asymmetry is partially acknowledged. It remains a framing concern but not a fatal flaw.

2. **"VLA models treated as a monolith"** — Removed because the paper's Related Work (lines 45-46) explicitly discusses ForceVLA, TLA, VLA-Touch, RDP, and FACTR as approaches targeting contact-rich tasks with supplementary sensing. The claimed omission does not exist.

3. **"Completion times computed over different subsets"** — While technically true, reporting average completion times for successful trials only is standard practice in the robotics literature. Demoted from consideration.

4. **"Mass is not visually observable"** — The paper acknowledges that initial estimates can be severely wrong (this is the point of the online adaptation experiment) and the LLM leverages appearance-based "world knowledge" about object properties, which is a reasonable approximation. Removed.

5. **Section-by-section formatting/style critiques** — Removed per instruction; these reflect parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions. The review confirms the paper's central finding that modular separation of VLM perception and LLM reasoning is critical for contact-rich tasks — this is well-supported by the ablation study despite the factual errors in specific claims.

## Suggestions

1. Resolve the mass correction inconsistency: align the textual values with the figure, or replace the figure, and recalibrate any claims about convergence to ground truth.
2. Correct the factual error in the w/o Pose Tracking ablation description (line 212) to accurately reflect that T2 succeeded at 9/10.
3. Include confidence intervals or increase trial counts for the main results.
4. Provide the LLM prompts and cost function validation procedure in an appendix for reproducibility.
5. Temper the framing of the VLA comparison to acknowledge the distribution mismatch between their training data and the contact-rich evaluation tasks.

## Score and Decision

**Round-1 bracket:** The closest topical anchor, "Generating Robot Policy Code for High-Precision and Contact-Rich Manipulation Tasks" (avg 4.00), shares the LLM-for-contact-rich-manipulation topic. Our paper has a stronger ablation study (+10.00 impact) but introduces two verifiable factual errors (-10.00 each). Papers in the 5–7 range (Make a Donut at 5.25, Vision-Language Foundation Models at 6.50) are clearly stronger due to real-robot validation and/or SOTA results. Papers in the 1–3 range (GRAIL at 3.00, LLIT at 2.33) are clearly weaker.

**Round-2 narrowing:** Within the 3.0–5.0 band, the "Generating Robot Policy Code" anchor (4.00) is the best comparator. Its weaknesses were about missing baselines and limited novelty; our paper's weaknesses include two verifiable factual errors that the anchor did not have. "UniContact" (3.50) confirms that papers with significant methodological gaps but some merit score in this range.

**Final placement:** Our paper has a well-designed ablation study (+10.00) that convincingly shows the necessity of modular design. However, the two factual errors (mass inconsistency, w/o Pose Tracking claim) are verifiable from the paper as written and undermine specific claims. The evaluation is limited to simulation with small sample sizes and no comparison against the most relevant prior methods (VLMPC, IMPACT). On balance, the paper sits slightly below the 4.00 anchor due to the factual errors, at 3.5.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>