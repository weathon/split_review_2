Now let me write the final review.

## Summary

BuilderBench introduces a hardware-accelerated (MuJoCo + JAX) block-building benchmark with 42 curated tasks designed to evaluate open-ended exploration, generalization, and embodied reasoning in RL agents. The environment simulates a robotic hand manipulating cubes under Newtonian physics. The paper defines two evaluation protocols (multi-task self-supervised and single-task supervised), benchmarks several existing algorithms, and provides open-source implementations with single-file algorithm baselines.

## Strengths

- **Hardware-accelerated simulator with genuine speed advantage.** The MuJoCo + JAX implementation achieves 10–100× speedup over CPU-based open-ended benchmarks like Crafter and Minecraft (line 42, with speed test deferred to Appendix B). This directly addresses a real bottleneck in RL research and is verified by the paper's claim that PPO for stacking two blocks trains in 30 minutes on one GPU (line 44).

- **Thoughtful task design requiring distinct reasoning abilities.** The five case studies in Section 5.1 (T-Block, Four Cube Packing, Hexagonal Portal, Leaning Tower, Maximum Overhang) convincingly demonstrate that block-building can require diverse non-trivial skills: geometric packing, counterweight reasoning, scaffold construction, simultaneous two-cube grasping, and the classic maximum-overhang problem. Each task is concretely illustrated with physical reasoning that goes beyond what procedurally generated benchmarks typically demand.

- **Two complementary evaluation protocols.** The multi-task self-supervised protocol (no task specification during training, testing zero-shot generalization) and the single-task supervised "training wheels" protocol (Section 6) provide a practical path for algorithm development. The paper is transparent that the supervised protocol "does not directly evaluate generalization" (line 203), positioning it honestly as a debugging tool.

- **Honest reporting of negative results.** The paper benchmarks four self-supervised and six supervised algorithms and transparently reports that all methods fail as task complexity grows (Figures 6, 7). On cube-3 tasks, "both algorithms achieve trivial performance" (line 213). This establishes a clear floor for future work without overfitting to any particular method.

- **Open-source release with accessible implementations.** Single-file algorithm implementations and fast training times lower the barrier to entry for researchers, which is a practical contribution.

## Weaknesses

### Major

- **Central claim about open-ended exploration and generalization is validated on only a small fraction of the task suite.** The self-supervised protocol—which is the protocol designed to test open-ended exploration and generalization—is evaluated on only 12 of 42 tasks (cube-1 with 2 tasks, cube-2 with 5 tasks, cube-3 with 5 tasks). On cube-3 tasks, all tested algorithms achieve "trivial performance" (line 213). The supervised protocol tests 17 tasks but also shows failure on cube-3 and cube-4 tasks (Figure 7). This creates a gap between the paper's ambitious framing ("open-ended exploration," "generalization to unseen tasks," "agents will have to learn general reusable skills and concepts through purely self-supervised interaction") and the experimental evidence, which for the harder and more distinctive tasks only demonstrates that existing methods fail. The benchmark infrastructure itself remains valuable, but the paper would benefit from either (a) demonstrating that harder tasks are tractable under some protocol, or (b) presenting a more measured framing that acknowledges the harder tasks are currently aspirational.

### Minor

- **The supervised protocol's diagnostic value is partially conflated with optimization difficulty.** The paper claims this protocol lets researchers "estimate whether an architecture is even capable of representing the solution to a complex task" (line 203). However, failure in this protocol could reflect optimization difficulty (credit assignment over long horizons, exploration challenges) rather than representational capacity. The paper acknowledges the protocol "does not directly evaluate generalization" but does not address this confound between representation and optimization.

- **"Normalized return" and "normalized success" metrics are underspecified.** The paper reports these quantities (lines 197, 209, Figures 6, 7) without defining the normalization baseline. Without knowing whether the baseline is a random policy, the maximum possible return, or something else, readers cannot interpret the absolute scale of the reported values. This is a straightforward omission that should be corrected.

- **Variance or confidence intervals for the 3-seed results are not shown.** The paper states "all experimental results are reported across three seeds" (line 207) but the figures show only mean curves. For a benchmark paper that aims to establish reliable metrics, indicating the spread across seeds is important for assessing metric stability.

- **Comparison between self-supervised algorithms is partially confounded.** SFL and MEGA both use PPO as the RL backbone, while UDRL and RND use MEGA for goal sampling (line 209). The comparison therefore mixes differences in the backbone algorithm with differences in the exploration/self-supervision strategy.

- **LLM evaluation (Section 7.1) is tangential to the benchmark's core purpose.** Both ChatGPT-5 and Gemini 2.5 Pro fail to produce correct high-level plans for the five case-study tasks. This result is unsurprising—these models were not designed for continuous-action physical reasoning—and does not provide evidence about the benchmark's usefulness for studying exploration or generalization. The paper itself calls it "not meant to be an extensive evaluation" (line 219). The space could have been better used for deeper analysis of the RL results.

### Trivial

- Minor inconsistency: the abstract states "six different algorithms" (line 9) while Section 1 bullet 4 states "four representative reinforcement learning (RL) algorithms and three self-supervised data-collection algorithms" = 7 (line 44).

## Nice-to-Haves

- Analysis of *why* algorithms fail on harder tasks (exploration vs. credit assignment vs. representation) would make the benchmark more useful diagnostically — even understanding the failure modes on currently unsolvable tasks would guide future research.
- A summary table mapping all 42 tasks to difficulty tier, cube count, and required reasoning abilities would give readers a better sense of the task suite beyond the five detailed case studies.

## Removed Points

*These points were raised by reviewers but filtered out after verification.*

- **"No quantitative task comparison with Minecraft."** The related work section (line 60) expresses a qualitative opinion ("we believe BuilderBench is better suited for academic research") — this is appropriate scope for a related work comparison, not a central claim requiring quantitative proof.
- **"Over 42 vs exactly 42 inconsistency."** The abstract says "over 42" and Section 3 says "42 tasks." This is a one-word discrepancy that does not affect the paper's substance.
- **"Missing explanation of ℝ^34 encoding."** The task specification uses ℝ^{3k} for target cube positions (line 86) while the policy input uses ℝ^34 (line 179) — the relationship is likely explained in the removed appendix and cannot be verified from the available text.
- **"PPO outperforming other baselines is not surprising."** This is a subjective assessment, not a weakness — honest benchmarking should report whatever results are obtained.
- **"Self-supervised label vs content."** The term "self-supervised" is used consistently in the literature for goal-conditioned RL methods that learn without external rewards; the paper's usage is standard.

## Novel Insights

The key insight that emerges from reading across the reviews is that BuilderBench occupies a useful but awkward position: its infrastructure and task design are genuinely well-executed, and the negative results honestly establish that current methods cannot handle the harder tasks. However, the paper's framing overpromises relative to what the experiments validate. The most valuable direction for revision would be to reframe the contribution around the *benchmark design and infrastructure* (which is strong) rather than around *validated measurements of open-ended generalization* (which are limited to the simplest tasks).

## Suggestions

1. **Reframe the paper's claims** to match what the experiments show. Emphasize that the benchmark provides a suite of tasks spanning several orders of difficulty, with the harder tasks serving as aspirational targets that current methods cannot solve — rather than claiming validated measurement of open-ended exploration and generalization across the full suite.

2. **Define the normalization baseline** for normalized return and success metrics in the main text.

3. **Add error bars or confidence bands** to Figures 6 and 7, or at minimum include a discussion of seed variance.

4. **Either remove the LLM evaluation** or reposition it to the appendix — it does not support the paper's central claims about exploration and generalization.

5. **Add a summary table** of all 42 tasks with difficulty tier, cube count, and required reasoning abilities in the main paper.

## Score and Decision

Based on my analysis, this paper sits in the low-acceptability / borderline range. The benchmark infrastructure, task design, and honest baseline reporting are genuine contributions that the community would benefit from. However, the gap between the ambitious framing and the limited experimental validation (only the simplest tasks are solvable; the harder tasks that make the benchmark distinctive are not validated by any method) is a real weakness that prevents a higher score.

The paper is not fatally flawed — benchmark papers routinely show that current methods fail on harder tasks. But the framing should be adjusted to match the evidence. With revisions to tone down the overclaiming and clarify what is vs. is not validated, this would be a solid contribution.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>