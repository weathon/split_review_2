## Summary

BuilderBench is a benchmark for evaluating agents that must learn through open-ended exploration and then generalize to unseen block-building tasks. It provides a hardware-accelerated MuJoCo/JAX simulator of a robotic hand interacting with blocks, a curated task suite of 42 diverse structures requiring physics, geometry, planning, and reasoning skills, and baseline implementations of several RL algorithms. The benchmark includes both a challenging self-supervised protocol (train without task specification, test on unseen tasks) and a simpler supervised protocol for prototyping.

## Strengths

- **Addresses an important gap**: Most RL benchmarks focus on narrow, fixed tasks and do not test open-ended exploration and generalization to diverse unseen tasks. BuilderBench directly targets this gap with a rich, physics-based environment where agents must discover general principles through interaction.
- **Well-designed task suite**: The 42 tasks are carefully curated to require distinct reasoning abilities (e.g., counterweights, packing, scaffolding, overhang problems) and range from very easy to extremely hard, providing a clear difficulty progression and meaningful signal for algorithmic progress.
- **Fast, accessible simulator**: The JAX+MuJoCo implementation is hardware-accelerated, making training 10–100× faster than CPU-based open-ended benchmarks like Crafter or Minecraft. This lowers the barrier to entry for RL research on exploration and generalization.
- **Comprehensive baselines and protocols**: The paper provides single-file implementations of multiple algorithms for both self-supervised and supervised protocols, along with thorough benchmarking results that clearly show current methods struggle on harder tasks—highlighting the benchmark’s potential to drive new research.
- **Clear motivation and writing**: The paper makes a compelling case for why block-building is a rich domain for studying embodied reasoning, and the case study of five tasks effectively illustrates the complexity and diversity of required skills.

## Weaknesses

### Fatal
None.

### Major
- **Self-supervised protocol may be too hard for current methods**: The paper’s main results on the self-supervised protocol show that even the best algorithms (SFL, MEGA) achieve near-zero performance on tasks with three or more cubes. While negative results are acceptable for a benchmark, the paper does not provide any positive signal on harder tasks or discuss whether the protocol is currently tractable. This risks the benchmark being seen as a “too hard” dataset that few researchers can make progress on.
- **Limited scope of generalization**: The benchmark tests generalization to unseen structures within the same environment and physics. This is valuable, but the claim of “generalist agents” is somewhat overstated—the domain is still constrained to block-building with a fixed action space and deterministic physics. The paper would benefit from a clearer discussion of what kinds of generalization are and are not tested.
- **Inconsistency in algorithm count**: The abstract states “single-file implementations of six different algorithms,” but the paper describes four self-supervised algorithms and six supervised algorithms (total ten). This discrepancy should be resolved.

### Minor
- **LLM evaluation is superficial**: Testing only five tasks with a single prompt format and showing failure is not particularly informative. A more systematic evaluation (e.g., varying prompt detail, providing few-shot examples, testing on simpler tasks) would strengthen the claim that current LLMs cannot solve these tasks.
- **Task suite details are mostly in appendix**: While the case study of five tasks is helpful, the main text gives little sense of the full 42-task suite. A table or summary of task categories and difficulty levels in the main paper would improve readability.

### Trivial
- Inconsistent capitalization: “BuilderBench” vs “BUILDERBENCH” in title and text.

## Nice-to-Haves

- Provide a few positive results on the self-supervised protocol for very simple tasks (e.g., 1-cube tasks) to give researchers a clear starting point.
- Include a comparison with other GPU-accelerated benchmarks (e.g., Jumanji, Brax) to contextualize the speed advantage.
- Add a discussion of potential failure modes or “cheating” strategies (e.g., agents that learn to throw blocks randomly) and how the benchmark prevents them.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Clarify the self-supervised protocol: how exactly does the agent learn to condition on arbitrary target positions if it never sees them during training? The paper mentions goal-conditioned policies with self-supervised goal sampling, but the test tasks are specific structures that may not be reachable from visited states. Explain how generalization to these held-out goals is expected to work.
- Resolve the algorithm count inconsistency and ensure the abstract matches the paper content.
- Consider adding a small set of “easy” self-supervised tasks (e.g., single-cube placement) where current algorithms can succeed, to provide a positive baseline and encourage adoption.

## Score and Decision

**Score**: 8  
**Decision**: Accept

The paper presents a well-motivated, carefully designed benchmark that fills an important gap in evaluating open-ended exploration and generalization. The fast simulator, diverse task suite, and comprehensive baselines make it a valuable resource for the community. While the self-supervised protocol is extremely challenging and may limit immediate impact, the benchmark’s design and the negative results themselves provide a clear call for new algorithmic ideas. The paper is clearly written and the contributions are significant.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>