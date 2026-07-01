## Summary
This paper introduces BuilderBench, a benchmark for evaluating generalist agents that must learn through open-ended exploration and interaction. The benchmark features a hardware-accelerated MuJoCo/JAX simulator where a robotic hand interacts with physical blocks, along with a task suite of 42 diverse target structures requiring skills ranging from motor control to intuitive physics, geometry, and long-horizon planning. The paper provides both a challenging self-supervised training protocol (where agents must explore without task specification) and a supervised "training wheels" protocol, along with baseline implementations of several RL algorithms.

## Strengths
- **Well-motivated problem**: The paper makes a compelling case for why existing benchmarks fail to evaluate open-ended exploration and generalization, and block-building provides a rich, scalable domain for studying these capabilities.
- **Carefully designed task suite**: The 42 tasks are thoughtfully curated to test distinct reasoning abilities (physics, geometry, planning, counterweights, scaffolding), with clear examples showing how simple block arrangements can require non-trivial solutions. The inclusion of tasks whose solutions are unknown to the authors is a nice touch.
- **Practical infrastructure**: The simulator is hardware-accelerated (10-100x faster than CPU-based alternatives like Crafter or Minecraft), and single-file algorithm implementations lower the barrier to entry. Training a PPO agent to stack two blocks in 30 minutes on a single GPU is genuinely useful for the community.
- **Honest evaluation**: The paper does not oversell its baselines—it clearly shows that current algorithms (SFL, MEGA, PPO, SAC, etc.) fail on all but the simplest tasks, and that even GPT-5 and Gemini 2.5 Pro cannot produce correct high-level plans. This honestly frames the benchmark as a challenge for future work.

## Weaknesses
### Fatal
None.

### Major
- **Limited evaluation of the self-supervised protocol**: The self-supervised experiments only test on 12 of the 42 tasks, and only with 1-3 cubes. The paper claims the benchmark is for "open-ended exploration," but the evaluation is restricted to the simplest tasks. The claim that "current algorithms are not directly scalable to complex tasks" is supported, but the paper does not provide any analysis of *why* they fail (e.g., exploration efficiency, representation learning, credit assignment). Without diagnostic experiments, it is hard for researchers to know where to focus.
- **Missing analysis of task difficulty and structure**: The paper does not quantify what makes tasks hard (e.g., number of steps required, branching factor, reward sparsity, state space coverage). The 42 tasks are described qualitatively, but there is no systematic characterization (e.g., task taxonomy, difficulty ranking, or analysis of which skills transfer between tasks). This makes it difficult to interpret results or design targeted improvements.
- **No comparison to existing block-building or manipulation benchmarks**: The paper mentions Kinetix, XLand, and Minecraft as related, but does not provide quantitative comparisons (e.g., speed, task diversity, or baseline performance on those benchmarks). Without such comparisons, it is unclear whether BuilderBench offers advantages beyond being "faster" and "curated."

### Minor
- **The "training wheels" protocol is standard RL, not novel**: The single-task supervised protocol is essentially standard goal-conditioned RL. While useful for debugging, it does not directly evaluate the core claim of "open-ended exploration and generalization." The paper acknowledges this, but the framing could be clearer.
- **LLM evaluation is superficial**: Testing LLMs on high-level planning in language is a reasonable sanity check, but the paper does not explore whether LLMs could be used as subgoal planners or combined with low-level controllers. The conclusion that "scaling alone is insufficient" is weak given the limited evaluation (5 tasks, 2 models, no in-context learning or fine-tuning).

### Trivial
- The paper claims "single-file implementations of six different algorithms" in the abstract but lists only four RL algorithms and three self-supervised algorithms in the contributions. This is a minor inconsistency.

## Nice-to-Haves
- Provide a difficulty ranking or taxonomy of the 42 tasks (e.g., by number of blocks, required skills, or baseline success rates).
- Include diagnostic experiments that isolate why algorithms fail (e.g., exploration vs. representation vs. credit assignment).
- Compare BuilderBench quantitatively to Kinetix or Minecraft on metrics like environment speed, task diversity, or baseline performance.

## Novel Insights
None beyond the paper's own contributions. The key insight—that block-building provides a rich, open-ended domain for studying exploration and generalization—is well-articulated but not entirely novel (Minecraft and Kinetix make similar claims). The paper's main value is in the careful task curation and fast simulator, not in a new theoretical or algorithmic insight.

## Suggestions
- Add a systematic analysis of task difficulty (e.g., number of steps, reward density, state space coverage) to help researchers interpret results and design experiments.
- Include ablation studies that isolate why self-supervised algorithms fail (e.g., does failure come from poor exploration, poor representation learning, or poor credit assignment?).
- Provide a quantitative comparison to Kinetix or Minecraft on speed, task diversity, and baseline performance to substantiate the claim that BuilderBench is "better suited for academic research."

## Score and Decision
The paper presents a well-motivated, carefully designed benchmark with practical infrastructure. The honest evaluation of baselines and the clear framing of the challenge are strengths. However, the limited evaluation of the self-supervised protocol and the lack of diagnostic analysis weaken the paper's ability to guide future research. The benchmark is a solid contribution, but the paper does not provide sufficient insight into *why* current methods fail or how to improve them.

Score: 6 (borderline accept)

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>