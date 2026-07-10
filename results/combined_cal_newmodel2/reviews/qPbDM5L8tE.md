Now I have all the information I need. Let me compile the final review.

## Summary

This paper proposes CoRAL, a modular framework for zero-shot contact-rich robotic manipulation that integrates an LLM with an MPPI controller. The key innovation is using the LLM to generate the cost function structure and contact strategies for the controller, rather than just producing perceptual cues as prior work does. The system separates perception (VLM + FoundationPose) from reasoning (LLM), with nested feedback loops: a high-frequency inner loop for reactive MPPI control and a low-frequency outer loop for LLM-driven plan refinement. Experiments on six simulated contact-rich manipulation tasks, together with ablations, demonstrate the framework's capabilities.

## Strengths

- **Genuinely novel core idea.** Using the LLM to generate the cost function structure and contact strategies for an MPPI controller (Eqs. 2–3) is a meaningful step beyond prior work (IMPACT, VLMPC) where foundation models only provide perceptual cues that still require a human-designed objective. This contribution is clearly articulated and well-motivated.
- **Informative ablation study.** The Unified VLM ablation provides clean evidence that collapsing perception and reasoning into a single model degrades performance catastrophically. The w/o Pose Tracking, w/o Refinement, and w/o Memory ablations each isolate a specific architectural choice and yield interpretable conclusions about what each component contributes.
- **Compelling contact-strategy analysis on T6 (Flip with Wall).** The 83.9% reduction in steps and 63.9% shorter path when the LLM provides the contact strategy vs. uninformed MPPI sampling (Section 4.1.4) offers the strongest quantitative evidence that the LLM's symbolic reasoning is doing useful work beyond generating plausible-sounding text.
- **Clean, well-motivated architectural design.** The nested feedback-loop structure (inner loop for reactive MPPI control, outer loop for LLM-driven strategic refinement) is conceptually sound. Separating high-level reasoning from low-level control at the architectural level rather than trying to learn them jointly is a reasonable design choice, explained clearly in Sections 3.3–3.4.

## Weaknesses

### Major

- **The SOTA comparison against OpenVLA-OFT and π_0.5 is structurally asymmetric.** These baselines are evaluated using their LIBERO checkpoints on four custom tasks (T1, T4, T5, T6) outside their fine-tuning distribution, while CoRAL uses GPT-4o (a massive proprietary model) to generate task-specific cost functions and contact strategies, plus FoundationPose with known 3D object models. The paper acknowledges this (line 163: "tests CoRAL's zero-shot capabilities against powerful policies") but then draws conclusions about "significantly outperforming" (line 193) that conflate architectural superiority with an asymmetric resource advantage. The results are still informative about what out-of-distribution VLAs cannot do on contact-rich tasks, but the headline overreaches without a controlled comparison (e.g., a GPT-4o-based VLA or fine-tuned VLAs on the custom tasks).

- **The evaluation lacks statistical rigor.** All results are reported as raw counts (x/10) with no confidence intervals, error bars, or statistical tests. With only 10 trials per condition and randomized object masses, friction coefficients, and dimensions (line 155), each trial samples different physics parameters. Differences of 1–2 successes out of 10 (e.g., memory benefit on T1: 4/10 vs 2/10; T5: 9/10 vs 7/10) are within what the random draw of parameters could produce. The paper draws conclusions about significance (e.g., "significantly" improved performance from memory, line 234) without any statistical foundation.

### Minor

- **The explainability benefits are claimed but not rigorously demonstrated.** The abstract and Section 4.1.4 claim that CoRAL "significantly enhances explainability" and provides "a level of transparency that is simply not possible with black-box policies." The evidence is a single anecdotal example where the LLM provides a natural language diagnosis (line 238). There is no user study, systematic evaluation of explanation correctness, comparison against alternatives, or analysis of failure modes in the LLM's diagnoses.

- **The memory unit's benefit is small and underspecified.** Differences of +1 to +2 successes out of 10 trials are within noise given the sample size and randomized parameters. The mechanism is also underspecified: "the LLM embeds the current task into a latent semantic space to retrieve the most relevant past experience" (line 75) does not specify what embedding is used, how similarity is thresholded, or what happens on retrieval of a poor match. This makes the memory contribution difficult to assess or reproduce.

- **The evaluation is entirely in simulation.** The paper mentions the "sim-to-real gap" (line 126) and includes a reactive control term (Eq. 7) intended to address it, but provides no real-world validation. While simulation-only evaluation is common in ICLR robotics papers, the paper's claims about "robotic manipulation" and robustness in "complex, dynamic manipulation scenarios" would benefit substantially from a real-robot demonstration.

- **No experimental comparison against dedicated contact-rich manipulation methods.** The paper critiques ForceVLA, TLA, VLA-Touch, RDP, and FACTR as having a "data bottleneck" (line 45), but provides no comparative evidence. While these methods require specialized hardware that may not be available in the simulation setup, their omission means the paper's positioning against the contact-rich manipulation literature is asserted rather than demonstrated.

- **The "zero-shot" characterization could be clarified.** FoundationPose requires known 3D geometric models (M) of every interactable object (Section 3.1), which is a significant prior. The LLM prompts and the amount of prompt engineering are not disclosed. The term "zero-shot" is used consistently to mean "no task-specific demonstration data," which is a valid usage, but this should be explicitly clarified relative to the system's other requirements (CAD models, prompt engineering, proprietary API).

### Trivial

None.

## Nice-to-Haves

- Include the LLM prompts to make the "zero-shot" claim verifiable.
- Increase the number of trials (≥50 per condition) and report confidence intervals or Bayesian credible intervals.
- Add a comparison where a VLA model is fine-tuned on the custom tasks, or where an open-source LLM replaces GPT-4o, to disentangle the modular architecture contribution from the proprietary model advantage.
- Provide a real-robot demonstration of at least one task to substantiate claims about robustness and real-world applicability.
- Report the VLM's physical parameter estimation accuracy (mass, friction) separately, as the entire planning world depends on these estimates.

## Removed Points

- Critic's claim that the limitations section "defers to the appendix" — the appendix is stripped by the parser; the limitation exists in the original submission.
- Critic's concern about latency/planning time per step — a nice-to-have rather than a core weakness; total completion time is reported.
- Critic's claim that comparing against out-of-domain VLA checkpoints is "structurally unfair" in a fatal sense — kept as a Major weakness because the comparison is still informative about VLA limitations, just not conclusive about architectural superiority.
- Section-by-section notes about well-structured related work and generic presentation points — removed as not constituting specific weaknesses or strengths.

## Novel Insights

None beyond the paper's own contributions. The review surfaces a tension between the paper's genuinely novel core idea (LLM-guided cost function generation) and the gap between its strong claims and the rigor of the evaluation. This is a common pattern in foundation-model-for-robotics papers: the ablations convincingly show what works, but the comparison against learned methods is weakened by resource asymmetry and low statistical power.

## Suggestions

- Most critically, strengthen the statistical foundation of the evaluation by increasing per-condition trials and reporting confidence intervals.
- Replace or augment the SOTA comparison with more controlled baselines (fine-tuned VLAs on the same tasks, or ablations that isolate the LLM+modular architecture advantage from the GPT-4o+FoundationPose resource advantage).
- Disclose the LLM prompts in the paper to make the "zero-shot" claim verifiable and reproducible.

## Score and Decision

**Calibration summary:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Generating Robot Policy Code for Contact-Rich Manipulation | WtHKqtHVXo.md | 4.00 | R1 | Yes | Similar topic (LLM for contact-rich). That paper had more negative weakness favorability (−3.22) and lower strength favorability (~11 max). My paper's core idea is rated higher (14.74 vs 11.36). |
| Make a Donut (Zero-shot Deformable Manipulation) | iTsHStJKcm.md | 5.25 | R1 | Yes | Also zero-shot LLM-guided manipulation. That paper had real-world validation (favorability ~10.88) and mild weaknesses. My paper has higher strength favorability (14.74 vs 10.88) but lacks real-world validation and has a significant statistical rigor weakness (−3.17). |
| Zero-Shot Robotic Manipulation with Diffusion Models (SuSIE) | c0chJTSbci.md | 6.25 | R1 | Yes | Stronger paper with real-world experiments, state-of-the-art results on CALVIN. My paper has higher peak strength favorability but less comprehensive evaluation. |
| Automated Rewards via LLM-Generated Progress Functions | lvDHfy169r.md | 5.75 | R2 | Yes | LLM for reward/cost generation (similar theme). Strength favorability up to 13.57, but had its own concerns about simulation-only evaluation. |
| LLMPhy: Complex Physical Reasoning | qGL6fE1lqd.md | 4.40 | R2 | Yes | LLM+simulator for physical reasoning. Had significant weaknesses about limited evaluation (−2.27, −0.25). My paper's evaluation is broader but has similar concerns about statistical rigor. |

**Bracketing:** Round 1 established that my paper is clearly above the 1–3.5 reject band (which contains papers with no coherent contribution) and below the 7.5+ band (which contains papers with rigorous, comprehensive evaluation and often real-world validation). The plausible bracket was 4.0–6.0. Round 2 compared against anchors at 4.40, 5.25, 5.75, and confirmed the paper sits between 4.40 and 5.75.

**Positioning within bracket:** The paper's strength items have higher favorability (core idea 14.74, ablation study 14.32, T6 analysis 13.57) than comparable anchors at 4.0–5.75. However, the major weakness on statistical rigor (−3.17) is a real drag that papers at 5.25 and above do not carry to the same degree. The asymmetry in the SOTA comparison (favorability −0.05) is a further concern. The paper's highest favorability items are strong enough to place it above the 4.0–4.4 anchor range, but the evaluation gaps prevent it from reaching the 5.75–6.25 range, where papers typically have more rigorous experimental design and often real-world validation. I place the final score at **5.0**.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>