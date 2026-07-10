Now I have a complete picture. Let me produce the final consolidated review.

## Summary

The paper proposes TrojanTO, the first action-level backdoor attack against Trajectory Optimization (TO) models such as Decision Transformer, Graph Decision Transformer, and Decision ConvFormer. Unlike traditional RL backdoors that rely on reward manipulation during training, TrojanTO is a post-training attack that uses alternating training to forge a connection between a learned trigger and a target action, with trajectory filtering and batch poisoning for stealth. The paper provides a systematic investigation of key factors (target action, trigger design, reward manipulation) and demonstrates strong results across 6 D4RL environments with a low poisoning rate (0.3%).

## Strengths

- **Novel problem identification and systematic investigation.** The paper correctly identifies that TO models (DT, GDT, DC) operate on fundamentally different principles from traditional RL agents — they use sequence modeling and reconstruction loss rather than reward maximization. The finding that reward manipulation is ineffective while trigger design is crucial (Figure 1, Tables 1–3) is a genuine empirical contribution that will inform future work in this area.

- **Very low poisoning rate.** The headline result of 0.3% poisoned trajectories (versus Baffle's 10%) is striking and, if it holds up, represents a significant improvement in attack efficiency (Section 6.1).

- **Thorough evaluation scope.** The paper evaluates across 6 D4RL environments spanning locomotion, navigation, and manipulation, and across 3 distinct TO architectures (DT, GDT, DC). This is more extensive than most attack papers in this space (Table 4).

- **Honest ablation analysis.** The ablation study in Table 5 cleanly isolates the contribution of each component. The finding that Batch Poisoning and Alternating Training are the main drivers of ASR, while Trajectory Filtering primarily helps BTP, is informative and consistent with the paper's design narrative.

## Weaknesses

### Fatal
None.

### Major
- **The ASR threshold ε is not stated in the main text.** Equation (2) defines ASR with a threshold ε that determines how close the output action must be to the target action for a success to be counted. The actual value of ε is absent from the main paper. Since ASR is the central evaluation metric and the paper's claims hinge on it, the threshold value is essential for interpreting the results. The paper should state ε explicitly alongside the ASR definition in Section 3.4 and, ideally, include a sensitivity analysis. *(Likely deferred to the appendix, but the main text must be self-contained on this point given its centrality.)*

### Minor
- **The source of the adversary's base trajectories is underspecified.** Section 3.3 states the adversary operates "without access to the original training dataset" (line 60), and Section 5.1 describes "an initial set of N trajectories" used for filtering and backdoor training. However, the paper never clarifies where this initial set comes from (adversary-collected rollouts? a public proxy dataset?). This is not a contradiction — the adversary clearly has their own minimal trajectory set — but making the source explicit would strengthen the threat model's concreteness.

- **The IMC baseline adaptation is underspecified in the main text.** The paper uses IMC (Pang et al., 2020) as a baseline and claims a "27.2% gain over IMC," but does not explain how IMC — originally designed for image backdoors — was adapted to the trajectory optimization / continuous-control setting. Without this information in the main text, a reader cannot assess whether the comparison is fair. *(Details may be in the appendix; the main text should provide a brief summary.)*

- **Near-zero variance in Tables 6–7 needs clarification.** Several entries report ±0.000 standard deviation across 3 random seeds (e.g., Table 6: 0.922 ± 0.000, 0.972 ± 0.000; Table 7: 0.895 ± 0.000 across multiple perturbation levels). While this likely arises from rounding to 3 decimal places, the paper should explicitly state whether the variance is truly zero or small enough to round down.

- **Trigger dimensions are oracle-selected.** Table 2 selects dimensions (1,2,3) as the best-performing set, and these are fixed for all main experiments. While the paper is transparent about this, the main results represent a best-case scenario where the adversary already knows which state dimensions provide the strongest trigger signal. The limitation should be explicitly discussed in the main text (the paper mentions Appendix F but does not address this as a limitation in the main discussion).

### Trivial
None.

## Nice-to-Haves

- A sensitivity analysis of ASR as a function of ε would strengthen confidence in the metric.
- The paper could consider an ablation comparing length-based trajectory filtering against alternative filtering criteria (e.g., reward-based filtering).
- The persistent backdoor experiment (Section 6.3) is interesting but could benefit from a discussion of how the finite context window bounds practical attack durations.

## Removed Points

These points from the input review were removed after verification:

- *"Threat model contradiction (structural)."* The reviewer claimed a contradiction between "no access to original training dataset" and needing trajectories. However, the adversary clearly has its own minimal trajectory set (line 72) — this is standard for post-training attacks. The source is underspecified but not contradictory. Downgraded from Fatal to Minor.

- *"Claim about existing attacks being ineffective is unsupported."* The paper evaluates Baffle and IMC (the most relevant existing methods) and Section 4.3 demonstrates reward manipulation is ineffective. The claim is supported for the specific attack paradigms discussed.

- *"The bi-level optimization is not truly bilevel."* The paper describes a practical alternating optimization implementation, which is a standard approximation. This is sufficiently clear.

- *"0.3% poisoning rate definition unclear."* The paper states "0.3% of trajectories" (abstract) and "0.3% average data poisoning rate" (line 270). While the exact denominator could be stated more explicitly, the meaning is clear in context compared to Baffle's 10%.

- *"Defense evaluation described only in prose."* The paper states detailed results are in Appendix B.1 (line 327). This is appropriate for a main text limitation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Report ε explicitly in Section 3.4.** State the threshold value and ideally include a brief sensitivity analysis showing ASR across different ε values.
2. **Clarify the trajectory source.** Add one sentence specifying where the adversary's initial trajectories come from (e.g., collected via rollouts of the pretrained model).
3. **Describe the IMC adaptation.** Provide a short paragraph in Section 6 describing how IMC was adapted to the TO/continuous-control setting.
4. **Explain the zero-variance entries.** Add a note that ±0.000 values result from rounding to 3 decimal places.
5. **Acknowledge the oracle limitation.** Add a sentence in Section 6 or Section 7 noting that trigger dimensions were selected based on empirical comparison and that practical attacks would need alternative selection methods (referencing Appendix F).

## Score and Decision

Let me calibrate against the anchors.

**Calibration anchors retrieved (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| 5kMwiMnUip | 1.40 | R1 | No | Completely different topic (LLM jailbreaking); much weaker paper |
| Uj0h13lVrR | 1.00 | R1 | No | Unrelated (GFlowNets); much weaker |
| 5lUdTogEL3 | 1.00 | R1 | No | Unrelated (person re-ID); much weaker |
| OE67D1Oatr | 3.00 | R1 | No | General backdoor attack, narrower evaluation scope than TrojanTO |
| 66e22qCU5i | 3.00 | R1 | No | General backdoor attack, less thorough evaluation |
| S5JCqTJyKj | 3.00 | R1 | No | Deferred backdoor attack, similar quality issues |
| 9Orm76dUuT | 4.50 | R1 | Yes | Test-time backdoor on MLLMs; has more serious method-vague issues |
| ZyPRwskBli | 4.75 | R1,R2 | Yes | Post-training backdoor via model editing; missing baselines, unclear threat model |
| H6XiAoyugv | 4.33 | R1 | No | Backdoor attack in vision, comparable quality |
| em0gAL8fbK | 4.00 | R2 | No | RL backdoor for autonomous driving; narrower scope |
| DoB8DmrsSS | 4.25 | R2 | No | Adversarial perturbations in RL; different task |
| ZtOnddFVT3 | 4.67 | R2 | No | Safe RL; unrelated |
| vRyp2dhEQp | 5.75 | R2 | Yes | Data-constrained backdoor; thorough evaluation but limited architecture diversity |
| 1Z3C49JQVf | 6.00 | R2 | Yes | Clean-label backdoor; limited novelty, only 2 datasets |
| LsTIW9VAF7 | 5.80 | R2 | No | Clean-image backdoor; similar quality level |
| 29LC48aY3U | 6.00 | R2 | No | LLM backdoor defense; different domain |
| X2x2DuGIbx | 6.75 | R1 | Yes | Offline RL certified defense; stronger theory, good presentation |
| ilcsm8B7Pe | 6.00 | R1 | No | Conformal prediction for TO; different task |

**Round 1 bracket:** After initial assessment, I bracket the paper between 5.5 and 7.0.

**Round 2 narrowing:** Comparing itemized favorability ratings:

TrojanTO's strengths (8.61–10.29) are comparable to or higher than the 5.75–6.00 anchors. Its weaknesses (0.96–7.01) are less severe than the 4.50–4.75 anchors (which had weaknesses with favorabilities as low as -4.71, -7.58). Specifically:

- The 4.75 anchor (ZyPRwskBli) has weaknesses like "proposed method is not evidently an actual threat" (favorability 0.32) and "novelty is limited" (favorability -1.15) — these are more damaging than any weakness in TrojanTO.
- The 5.75 anchor (vRyp2dhEQp) has weaknesses around domain limitations and missing analyses (favorability 3.38–7.16) — comparable to TrojanTO's weaknesses.
- The 6.00 anchor (1Z3C49JQVf) has a weakness about "limited novelty" (favorability -2.65) and weak baselines (favorability -4.75) — more serious than TrojanTO's mostly-presentation issues.

TrojanTO sits above the 4.5–5.0 papers because (a) the problem is genuinely novel (first systematic study of this attack surface), (b) the evaluation is more thorough (6 environments × 3 architectures), and (c) the weaknesses are primarily about presentation clarity rather than fundamental methodology gaps. It sits below the 6.75 defense paper, which has stronger theoretical grounding. The closest comparisons are the 5.75–6.00 anchors, and TrojanTO is slightly stronger than them in evaluation scope and problem novelty, while having comparable presentation-level weaknesses.

**Final score: 6.0**

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>