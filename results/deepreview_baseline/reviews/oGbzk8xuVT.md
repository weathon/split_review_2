## Summary

This paper introduces BuilderBench, a benchmark for evaluating generalist agents that must learn through open-ended exploration and interaction rather than from human-generated data. The benchmark features a hardware-accelerated MuJoCo/JAX simulator where a robotic hand interacts with physical blocks, along with a task suite of 42 diverse target structures that test physics understanding, mathematical reasoning, and long-horizon planning. The paper provides both a self-supervised training protocol (where agents explore without task specification) and a supervised "training wheels" protocol, along with baseline implementations of several RL algorithms.

## Strengths

- **Well-motivated problem**: The paper makes a compelling case for why current benchmarks fail to evaluate open-ended exploration and generalization, and why block-building provides a rich domain for testing these capabilities. The connection to child development research and the mathematical richness of block-building problems is well-argued.

- **Carefully designed task suite**: The case study of five tasks (T-Block, Four Cube Packing, Hexagonal Portal, Leaning Tower, Maximum Overhang) demonstrates genuinely interesting and non-trivial reasoning challenges that require understanding of physics, geometry, and planning. The tasks are clearly designed to require distinct skills rather than just scaling up simple behaviors.

- **Practical infrastructure**: The simulator is hardware-accelerated (10-100x faster than CPU-based benchmarks like Crafter or Minecraft), and the single-file implementations of algorithms reduce barriers to entry. Training a PPO agent to stack two blocks in 30 minutes on a single GPU is genuinely accessible.

- **Honest evaluation**: The paper clearly shows that current algorithms struggle on all but the simplest tasks, and that even state-of-the-art LLMs cannot solve the high-level planning required. This sets a clear challenge for the community without overclaiming results.

## Weaknesses

### Fatal
None.

### Major

- **Limited evaluation of the self-supervised protocol**: The self-supervised evaluation (Figure 6) only tests on 12 tasks out of 42, and only with 1-3 cubes. The paper acknowledges that algorithms achieve "trivial performance" on 3-cube tasks, but this means the core claim of the benchmark—evaluating open-ended exploration and generalization—is not actually demonstrated to be feasible or meaningful. The benchmark's value depends on whether the self-supervised protocol can eventually differentiate between algorithms, but the current results show all algorithms fail similarly.

- **The "training wheels" protocol undermines the core contribution**: The single-task supervised protocol (Figure 7) is essentially standard RL on individual tasks. While useful for debugging, this does not evaluate open-ended exploration or generalization at all. The paper's main claimed contribution is about evaluating agents that learn through self-supervised exploration, but the only protocol that actually works (shows non-zero success) is the one that doesn't test the claimed capability.

- **Missing analysis of what makes tasks hard**: The paper describes tasks qualitatively but provides no analysis of why current algorithms fail. Is it exploration (finding the right sequence of actions), credit assignment (long horizons), representation learning (understanding physics from pixels/state), or something else? Without this analysis, it's unclear what algorithmic innovations are needed or how to interpret progress.

- **No comparison to existing block-building benchmarks**: The paper mentions Minecraft as a similar block-building environment but does not provide any quantitative comparison (e.g., how many tasks, difficulty distribution, computational cost). The claim that BuilderBench is "better suited for academic research" is asserted but not supported with evidence.

### Minor

- **The LLM evaluation is superficial**: Testing LLMs on high-level planning in language is a very different capability from what the benchmark actually tests (embodied interaction). The result that LLMs fail is unsurprising and doesn't add much insight. A more informative experiment would be to test whether LLMs can generate reward functions or subgoal sequences that help RL agents.

- **Task count is misleading**: The paper claims 42 tasks, but the evaluation only uses 17 (supervised) or 12 (self-supervised). It's unclear whether the remaining tasks are actually solvable or what their difficulty distribution is.

### Trivial
- The paper uses "42 tasks" as a number that appears in many places (Figure 6, Figure 7, Section 7) but the actual numbers evaluated are smaller. This is a minor inconsistency.

## Nice-to-Haves

- A "task difficulty taxonomy" that categorizes tasks by what skill they test (e.g., motor, geometric reasoning, physics, planning horizon) would help researchers target specific weaknesses.
- Providing oracle solutions or optimal trajectories for at least a subset of tasks would help validate whether algorithms are learning the right thing.
- Including a "partial credit" metric (e.g., number of blocks correctly placed) would give more signal than binary success/failure for hard tasks.

## Novel Insights

None beyond the paper's own contributions. The insight that block-building provides a rich domain for testing embodied reasoning is not new (Minecraft, Kinetix), but the paper's specific task design and the observation that current algorithms fail on tasks requiring non-trivial physical reasoning (like the T-block requiring diagonal rotation) is a useful concrete finding.

## Suggestions

- Provide a thorough analysis of failure modes for current algorithms on a representative subset of tasks. For example, do agents fail because they cannot discover the diagonal rotation trick, or because they cannot execute it precisely? This would guide algorithmic development.
- Consider adding a "curriculum" or "progressive" evaluation protocol where tasks are grouped by difficulty, so researchers can track progress even before solving the hardest tasks.
- Release human demonstration data or expert trajectories for a subset of tasks to enable imitation learning baselines and provide a performance upper bound.

## Score and Decision

The paper presents a well-motivated benchmark with thoughtful task design and practical infrastructure. However, the core evaluation protocol (self-supervised) is not demonstrated to be functional—all algorithms fail on all but the simplest tasks—and the working protocol (supervised) does not test the claimed contribution. The benchmark's value to the community depends on whether it can differentiate between future algorithms, but the current results provide no evidence for this. The paper is a solid contribution to infrastructure but does not yet demonstrate that the benchmark is useful for its stated purpose.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>