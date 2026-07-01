## Summary

This paper identifies a critical yet overlooked problem: the chain-of-thought reasoning of Large Reasoning Models (LRMs) often contains harmful content even when final responses appear safe. The authors propose Intervened Preference Optimization (IPO), which aligns reasoning safety by replacing compliance cues (steps that indicate willingness to comply with harmful requests) with safety triggers (steps that reject harmful directions) to construct preference pairs for DPO. Experiments on multiple LRMs and adversarial safety benchmarks show that IPO reduces reasoning harmfulness by over 30% relative to leading baselines while preserving or enhancing reasoning capabilities.

## Strengths

- **Important and well-motivated problem.** The paper clearly demonstrates that existing safety-aligned LRMs (e.g., RealSafe, STAR) still exhibit high harmful ratios in reasoning even when responses are safe. Figure 2 quantifies this gap convincingly, establishing the need for reasoning-level alignment.
- **Systematic empirical analysis of safety dynamics.** Sections 3.1–3.3 provide a rigorous study of how safety evolves during reasoning—identifying safety triggers and compliance cues using Continuation Safety Ratio (CSR), and showing that replacing compliance cues with safety triggers reliably steers reasoning toward safety (Figure 6). This analysis is a valuable contribution in its own right.
- **Effective and efficient method.** IPO directly addresses the low-rollout-diversity problem of RL-based methods (Section 2.3) by proactively injecting safe trajectories via interventions. Compared to GRPO, IPO achieves better safety with fewer generations (14 vs. 40) and shorter training time (40 minutes vs. 2 hours), as demonstrated in Section 4.3.
- **Strong and consistent results.** IPO achieves the best or second-best average reasoning safety across all three benchmarks on DS-8B, DS-7B, and Qwen3-8B (Table 2), with reasoning harmfulness reductions such as DS-8B on WildJailbreak from 82.4% to 23.4%. Importantly, reasoning capabilities on math, coding, and science benchmarks are preserved or improved.
- **Good ablation and robustness analysis.** The paper tests IPO under different compliance cue detectors (Table 3) and shows robustness to detector variation, supporting practical applicability.

## Weaknesses

### Major
- **Reliance on an external oracle for data construction.** Both compliance cue identification and safety trigger pool construction depend on GPT-4o for annotation (with >80% agreement). While the authors show robustness to detector choice, the method does not provide a fully self-reliant training pipeline. The trigger pool is also limited to six manually chosen triggers, and it is unclear how well these generalize to unseen or more diverse attack types.
- **Limited analysis of distributional shift.** The KL divergence analysis (Figure 7) is narrow—only averaged over tokens on harmful trajectories. A more thorough investigation of how IPO affects the model's reasoning distribution on benign prompts (beyond XsTest compliance rates) would strengthen the claims about minimal safety-utility trade-off. The over-refusal rates (80.0% for DS-8B, 71.2% for DS-7B) are higher than some baselines, indicating a nontrivial trade-off.
- **Scale and generalizability concerns.** The experiments are limited to 7B–8B models. While Appendix B.4 mentions evaluation across additional sizes, the main results lack coverage of larger LRMs (e.g., 32B, 70B) where safety dynamics may differ. The intervention approach may also face challenges in multi-turn or agentic settings, as briefly noted but not explored.

### Minor
- **Evaluation noise from automated safety judges.** Both reasoning and response safety are evaluated using GPT-4o as the judge. While standard, this introduces potential biases and variance that are not fully quantified (e.g., confidence intervals or agreement rates with human evaluation are not reported for the main results, only for the compliance cue detection task).
- **Comparison to baseline methods could be expanded.** The paper compares to SFT-based methods and GRPO, but some RL-based baselines (e.g., TARS) are only mentioned in passing. The direct comparison with process-supervision methods like BackTrack is relegated to the appendix, making it harder to assess relative merits in the main text.

### Trivial
- None.

## Nice-to-Haves

- It would be valuable to demonstrate IPO in a setting where the compliance cue detector is also learned from the base LRM (e.g., using the model's own representations or a lightweight classifier), moving toward a fully end-to-end alignment pipeline.
- A breakdown of reasoning harmfulness by attack type (e.g., direct vs. jailbreak) across all benchmarks would help understand where IPO provides the largest gains and where gaps remain.

## Novel Insights

Beyond the technical contribution of IPO, the paper's most novel insight is the identification and characterization of *safety triggers* and *compliance cues* as critical structural elements in the reasoning process. The observation that a single compliance cue early in reasoning strongly correlates with an 85% rise in harmful continuations (Pearson R=0.85) is striking and provides a concrete handle for process-level intervention. The idea of using corrective intervention—replacing a harmful cue with a safe trigger at a single step—as a data augmentation strategy for preference learning is both elegant and practically effective. This lens of reasoning as a process with localized "critical points" of safety divergence offers a new perspective for reasoning-level alignment that goes beyond treating the entire CoT uniformly.

## Suggestions

1. **Quantify the variance of safety evaluation.** Report confidence intervals or standard deviations for harmful ratios across multiple runs or judge queries, to give a clearer sense of reliability.
2. **Explore automated trigger generation.** Instead of a fixed pool of six triggers, investigate whether safety triggers can be dynamically sampled from the model’s own safe trajectories after a seeding process, to improve generalization.
3. **Provide a deeper analysis of the safety-utility Pareto frontier.** Plot harmful ratio (reasoning) versus average reasoning accuracy across multiple checkpoints or training configurations, to help the community understand the tunable trade-off.

## Score and Decision

Score: 6

The paper addresses an important, under-explored problem with a well-reasoned method and convincing empirical results. The identification of safety triggers and compliance cues is a genuine empirical contribution, and IPO is shown to be both more effective and more efficient than GRPO-based process supervision. The main limitations—reliance on an external detector, limited scale, and moderate over-refusal—prevent the paper from being a clear accept, but its strengths clearly outweigh its weaknesses. The paper makes a solid, reproducible step toward safer LRM reasoning and is likely to be of practical value to the community.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>