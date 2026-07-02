## Summary

This paper identifies the overlooked problem of unsafe reasoning traces in Large Reasoning Models (LRMs): even when final responses are safe, the intermediate chain-of-thought can still contain harmful content that could be exploited. The authors conduct an empirical analysis revealing that safety in reasoning is concentrated in a few critical steps—*safety triggers* and *compliance cues*—and that replacing compliance cues with safety triggers can steer reasoning towards safety. Based on these insights, they propose **Intervened Preference Optimization (IPO)**, which constructs preference pairs by substituting compliance cues with safety triggers and applies DPO only on the diverging segments, providing strong contrastive signals for safe reasoning. Experiments across three LRMs and multiple safety/reasoning benchmarks show that IPO reduces reasoning harmfulness by over 30% relative to leading SFT- and RL-based baselines while preserving or even enhancing core reasoning capabilities.

## Strengths

- **Important and timely problem.** The paper correctly identifies that reasoning-level safety in LRMs has been overlooked in prior alignment work, which focuses primarily on response safety. The experiments in Section 2.2 convincingly demonstrate that even state-of-the-art safety-aligned models (RealSafe, STAR) exhibit high harmful ratios in reasoning traces, validating the relevance of the research question.
- **Novel empirical analysis of safety dynamics.** The systematic analysis of safety triggers and compliance cues (Section 3.1–3.3) provides a principled understanding of how safety evolves during reasoning. The definitions of Continuation Safety Ratio (CSR) and the automated identification of critical steps go beyond prior qualitative observations and directly motivate the IPO method. The intervention experiment (Figure 6) cleanly shows that minimal corrections can steer reasoning towards safety.
- **Effective and efficient method.** IPO is well-motivated by the limitations of GRPO (low rollout diversity) and directly addresses them through supervised intervention. The method is computationally more efficient than RL-based approaches (fewer generations, shorter training time) while achieving stronger or competitive safety gains. The ablation study on training algorithm (Table 3) confirms the importance of applying DPO only from the divergence point.
- **Thorough evaluation.** Experiments cover three different LRM families, three adversarial safety benchmarks, and four reasoning benchmarks. The paper also tests generalization to broader capabilities (Appendix B.1), robustness to stronger attacks (Appendix B.2), and scalability across model sizes (Appendix B.4). The comparison against multiple strong baselines (SafeChain, RealSafe, STAR, SafeKey, GRPO) is comprehensive.
- **Balanced safety-utility trade-off.** IPO achieves the best average reasoning safety across all three benchmarks while maintaining or improving reasoning accuracy, demonstrating that reasoning-level alignment need not hurt core capabilities. The over-refusal rate is higher than some baselines but acceptable given the significant safety gains.

## Weaknesses

### Fatal

None.

### Major

- **Heavy reliance on GPT-4o as an external detector and evaluator.** The compliance cue detector and the safety evaluator both rely on GPT-4o. Although the authors test alternative detectors (DS-8B, DeepSeek-R1) in Table 3, the safety evaluation still uses GPT-4o, which may introduce systematic bias and raises reproducibility concerns (e.g., GPT-4o API updates or deprecation). A more self-contained pipeline (e.g., using the model itself or a smaller open-source judge) would strengthen the contribution.
- **Limited scope of dynamics analysis.** The identification of safety triggers and compliance cues is based on only 30 prompts from JailbreakBench (Section 3.1). Although the patterns appear consistent, the sample size is small and it is unclear whether the same dynamics hold for more diverse or adversarial prompts (e.g., from WildJailbreak). The thresholds $\mu=0.9$, $\eta=0.1$, and $K=15$ are chosen without rigorous justification or sensitivity analysis.
- **On some benchmarks, baselines are competitive or better.** For example, on JailbreakBench, GRPO achieves 0.3% reasoning harmfulness for DS-8B compared to IPO's 5.7%. While IPO excels on average, the gap on the simplest benchmark suggests that the method may not uniformly dominate across all settings. The paper's claim of "over 30% relative reduction" should be contextualized: the improvement is most pronounced on the hardest benchmarks (WildJailbreak).
- **Over-refusal tendency.** The XsTest compliance rate for IPO models is 80.0% (DS-8B) and 71.2% (DS-7B), which is notably lower than RealSafe (47.5%) and the base model (98.4%). While the paper acknowledges this, the over-refusal is higher than several baselines (STAR 76.9%, SafeKey 83.2%, GRPO 86.8%) and may limit deployability in benign contexts. The paper does not systematically analyze the false positive rate on safe-but-sensitive queries.

### Minor

- **Pipeline complexity.** IPO involves multiple stages: generating rollouts, detecting compliance cues, sampling safety triggers, intervening until safe continuation, constructing preference pairs, and additional stages for over-refusal mitigation and auxiliary SFT loss. This complexity may hinder adoption and reproducibility. An end-to-end variant would be cleaner.
- **Choice and number of safety triggers.** The paper uses six manually sampled triggers from a pool but does not ablate how the number or specific choice of triggers affects performance. It is unclear whether the method is sensitive to trigger selection.
- **Theoretical framing via reward shaping is speculative.** The connection to potential-based reward shaping (end of Section 3.4) is interesting but not formally developed or empirically validated. The paper does not demonstrate that IPO corresponds to an optimal reward-shaping scheme or that the shaped rewards improve learning efficiency in a measurable way.
- **No comparison to process-supervision methods like tree search or step-level RL.** Related work mentions methods that build step-level supervision via tree search or external labeling (e.g., Zhang et al. 2025d, Zhao et al. 2025), but these are not included as baselines. A direct comparison would strengthen the claim that IPO is more sample-efficient.

### Trivial

- The conclusion mentions "multi-turn dialogue and agentic system" as future extensions, but the paper does not evaluate these settings. This is appropriate for a conclusion but slightly over-claims generality.

## Nice-to-Haves

- An open-source release of the intervention pipeline (detector, trigger pool, training code) would significantly improve reproducibility and adoption.
- A sensitivity analysis of the thresholds for CSR turning points (e.g., $\mu$ and $K$) would strengthen the empirical basis of the dynamics analysis.
- An evaluation on a broader set of benign prompts to measure over-refusal more thoroughly (e.g., XsTest is small; a larger dataset like SimpleSafetyTests or BOLD would be informative).

## Novel Insights

The key novel insight is that safety in LRM reasoning is not uniformly distributed but is concentrated in a few critical steps—*safety triggers* that consolidate safe continuations and *compliance cues* that strongly correlate with unsafe continuations. This structure makes reasoning-level alignment amenable to targeted intervention: replacing a single compliance cue with a safety trigger can redirect an entire trajectory toward safety. Building on this, IPO operationalizes the idea by using interventions to create high-quality preference pairs, thereby overcoming the rollout-diversity bottleneck of reinforcement learning for safety alignment. This contrasts with prior work that treats reasoning traces as monolithic and attempts to supervise the entire sequence with sparse rewards or full-sequence SFT.

## Suggestions

- Provide a more extensive validation of the dynamics analysis using a larger and more diverse set of prompts (e.g., from WildJailbreak) and report sensitivity of the turning-point thresholds.
- Consider replacing GPT-4o as the compliance cue detector with a smaller open-source model or a rule-based heuristic to improve reproducibility and reduce API dependence.
- Include a direct comparison against a process-supervision RL baseline that uses step-level rewards (e.g., from a trained safety critic) to further substantiate the efficiency advantage of IPO.
- Analyze the false positive rate on benign-but-sensitive queries to better characterize the over-refusal behavior and consider mitigation strategies (e.g., balanced training with more benign prompts).

## Score and Decision

Based on a thorough review, the paper makes a strong contribution by identifying an important and overlooked problem (reasoning-level safety in LRMs), providing novel empirical insights, and proposing an effective and efficient method (IPO) that outperforms strong baselines. The weaknesses—reliance on GPT-4o, limited sample size in dynamics analysis, competitive baselines on some benchmarks, and pipeline complexity—are significant but do not invalidate the core claims. Overall, the paper is likely to have a meaningful impact on the safety alignment of reasoning models and is well within the quality bar for acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>