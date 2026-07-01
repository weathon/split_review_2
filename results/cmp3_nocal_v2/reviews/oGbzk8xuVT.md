## Summary

BuilderBench introduces a block-building benchmark with a hardware-accelerated (MuJoCo + JAX) simulator and a task suite of 42 diverse target structures designed to test physical reasoning, long-horizon planning, and generalization. The paper provides two evaluation protocols (self-supervised multi-task and supervised single-task), open-source baseline implementations, and experimental results showing that current RL algorithms struggle with all but the simplest configurations. The core contribution is the task suite itself—five detailed case studies (T-block, Four Cube Packing, Hexagonal Portal, Leaning Tower, Maximum Overhang) each requiring distinct reasoning skills—and the fast simulator infrastructure that lowers the barrier for academic research.

## Strengths

1. **Genuinely creative and diverse task suite (Section 5.1).** The five case studies each test a distinct physical reasoning ability—geometric rotation for packing, scaffolding with simultaneous dual-block lifting for the hexagonal portal, counterweights and staged scaffold removal for the leaning tower, center-of-mass reasoning for the maximum overhang. The T-block (rotating the base cube 45° so its diagonal supports two top cubes) is a particularly elegant minimal example of non-obvious physical insight. This is the paper's strongest contribution and gives the benchmark headroom for future algorithms.

2. **Hardware-accelerated simulator (Section 1, contributions).** The 10–100× speedup over CPU-based benchmarks like Crafter, Minecraft, and NetHack is a practical advantage that lowers the adoption barrier. The concrete example (30 minutes on a single GPU for a 2-block PPO task) makes this tangible.

3. **Two-tier protocol design with clear rationale (Section 6).** The self-supervised protocol tests open-ended exploration and generalization to unseen goals—the paper's primary setup. The supervised "training wheels" protocol is explicitly positioned as a debugging tool for verifying that architectures can represent solutions before tackling generalization. This design choice is well-motivated and clearly explained.

4. **Open-source release with baseline implementations.** The paper commits to releasing code for the simulator, task suite, and algorithm implementations. For a benchmark paper, this is the most important deliverable.

## Weaknesses

### Fatal

None.

### Major

- **The hardest, most interesting tasks are not benchmarked.** The paper describes Hexagonal Portal (10 cubes) and Leaning Tower (9 cubes) as signature challenges requiring scaffolding, counterweights, and simultaneous dual-block lifting—yet all experiments stop at cube-4 (supervised) or cube-3 (self-supervised). Of the claimed 42 tasks, only 12–17 of the lowest-complexity configurations are evaluated. This leaves the paper's central question—whether BuilderBench "challenge[s] the current iteration of algorithms" on genuinely hard reasoning tasks—unanswered for the tasks that would make the strongest case.

- **The LLM evaluation (Section 7.1) does not support the conclusion drawn from it.** Testing text-only LLMs (ChatGPT-5, Gemini 2.5 Pro) on a physical manipulation task with no visual input, no simulator access, and no ability to interact is a setup where failure is expected ex ante. The paper claims this "highlights how solving our tasks requires non-obvious steps of reasoning that are beyond what current models can achieve through scaling alone," but the setup is too constrained to support this inference. This section reads as a rhetorical flourish rather than a meaningful benchmark result.

### Minor

- **Gap between the paper's aspirational framing and what is actually evaluated.** The paper is written with maximal rhetoric—"agents should become scientists, performing micro experiments to discover the laws governing the environment" (p. 2), "solve tasks that go well beyond the tasks they have practiced solving before" (p. 2). The actual experiments are a goal-conditioned RL setup on up to 4 cubes, where agents explore the same state space they are evaluated on (same cube count, same environment). While the self-supervised protocol does evaluate generalization to unseen goal configurations, this is a standard goal-conditioned RL generalization setup, not a new paradigm of open-ended discovery. The paper would be more accurate and no less important if it positioned itself as a "diverse block-building task suite for multi-task and goal-conditioned RL."

- **No evidence that the task setup is learnable by gradient-based RL beyond trivial configurations.** The paper states "we manually solved most tasks using the same action space as the agent" (Section 5.2), which confirms solvability in principle but does not rule out that the reward landscape, action representation, or episode horizon makes learning via RL needlessly difficult. When all tested algorithms achieve "trivial performance on tasks with three cubes" (self-supervised) and "struggle to achieve non-zero success" at cube-4 (supervised), the reader cannot distinguish between "these tasks are genuinely hard and require new algorithms" and "the training setup is broken." An ablation showing that a shaped curriculum or hand-coded oracle can solve at least one moderate-complexity task would substantially strengthen confidence in the benchmark design.

- **Key evaluation metrics are not defined in the main text.** The paper reports "normalized return" and "normalized success" (Figures 6 and 7) without specifying what these are—whether success is all-cubes-within-ε or per-cube threshold, how return is normalized, what the bounds are. For a benchmark paper, the metric is as important as the task. The reader should be able to interpret the central results without consulting the appendix.

- **The ℝ^34 task specification dimension is stated without explanation** (Section 6). The paper says the task-conditioned policy takes a task specification of dimension ℝ^34 but never explains what this vector encodes. This is confusing to a reader trying to understand the protocol setup.

- **No confidence intervals or variance shading on any experimental results.** Results are reported "across three seeds" but no error bars are shown or described in figure captions, making it hard to assess the stability and reliability of the reported curves.

### Trivial

- **Numerical inconsistency:** The abstract says "six different algorithms" while the contributions list says "four representative RL algorithms and three self-supervised data-collection algorithms" (= 7). This minor inconsistency should be resolved.

## Nice-to-Haves

- A table mapping each of the 42 tasks to (number of cubes, known solution status, attempted/not attempted) would greatly help readers understand the benchmark's coverage.
- Adding variance shading to the learning curves (Figures 6 and 7) would improve interpretability of the results.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Criticism about the maximum episode length *H* not being stated in Section 4:** The paper mentions *H* as a parameter. The specific value would be in the appendix, which is stripped by the parser. Removed per hard rule about missing appendix content.
- **Criticism that the Minecraft comparison is unfair to Minecraft:** The paper explicitly names Minecraft as an exception ("other than a few exceptions like Minecraft"). The reviewer's concern misreads the paper. Removed.
- **Criticism about the claim "some tasks have solutions unknown even to the authors" being unsubstantiated:** This is stated as a design philosophy, not an empirical claim requiring footnoted justification. Removed as overly nitpicky.
- **Criticism that the supervised protocol "does not directly evaluate generalization" yet occupies half the experimental space:** The paper explicitly acknowledges this (Section 6: "Although this setup does not directly evaluate generalization, it makes the problem of building general agents much more approachable"). Removing a point the paper already addresses.
- **Criticism about the metrics being deferred to the appendix is softened:** The main text lacks metric definitions, which is a real issue, but the specific complaint about "deferring to appendix" is a parser artifact; the appendix exists in the original. Kept only as a minor weakness about main-text completeness.

## Novel Insights

The harsh review's most insightful observation is the structural gap between the paper's narrative arc (open-ended discovery, agents as scientists) and the actual experimental paradigm (goal-conditioned RL with modest cube counts where all algorithms fail on moderately complex tasks). This gap is real but reflects a tension common to benchmark papers: the benchmark is designed for future work but the initial results are necessarily limited. The reviewer's suggestion to reposition the paper as a "diverse block-building task suite" rather than a "benchmark for open-ended exploration and generalization" would make the paper more accurate without diminishing its contribution. The observation that the paper provides no analysis to distinguish genuine task difficulty from a broken training setup is also a genuinely useful critique that the authors should address.

## Suggestions

1. **Add at least one positive result.** Show that a carefully tuned PPO with a shaped curriculum can solve a moderate-complexity task (e.g., the T-block or a 2-cube stack). Provide rollout trajectories and analyze whether the learned policy discovers the intended insight (e.g., the 45° rotation for the T-block). This would confirm the setup is sound.
2. **Define the evaluation metrics in the main text.** A single sentence specifying what "normalized success" and "normalized return" mean operationally would make Figures 6 and 7 interpretable without the appendix.
3. **Calibrate the framing.** The paper's real contribution—a creative, diverse, fast-simulator block-building task suite—is strong enough to stand without the "agents as scientists" rhetoric. Matching the claims to what is demonstrated would strengthen the paper.
4. **Explain the ℝ^34 task specification** and add variance information to the learning curves.
5. **Address the 6 vs 7 algorithm inconsistency.**

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>