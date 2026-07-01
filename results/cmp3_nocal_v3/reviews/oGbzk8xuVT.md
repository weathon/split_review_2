Here is the final consolidated review.

---

## Summary

BuilderBench introduces a block-building benchmark for open-ended exploration and generalization in RL. It provides a fast MuJoCo + JAX simulator with a simulated robotic hand, a task suite of 42 hand-designed block structures requiring diverse physical reasoning skills (counterweights, scaffolding, packing, overhangs), and two evaluation protocols: a self-supervised protocol (agents explore without reward, then generalize to unseen test tasks) and a supervised "debug" protocol (single-task RL with rewards). Baseline results from existing algorithms are reported.

## Strengths

1. **The task design is genuinely novel and thoughtfully curated.** The five case-study tasks (T-Block, Four Cube Packing, Hexagonal Portal, Leaning Tower, Maximum Overhang) are concretely described, non-trivial, and clearly require different forms of physical reasoning. The Hexagonal Portal requiring simultaneous two-cube placement and temporary scaffold removal is an especially creative evaluation target. These tasks are a real contribution — they go substantially beyond standard pick-and-place benchmarks and could drive new research in physically-grounded exploration.

2. **The hardware-accelerated simulator (MuJoCo + JAX) is a practical enabler.** The claim of 10–100× speedup over CPU-based environments like Crafter, Minecraft, or NetHack is plausible and valuable. The availability of single-file, fast-to-train baseline implementations (e.g., "training a PPO agent to stack two blocks takes 30 minutes on a single GPU") lowers the barrier to entry for researchers. This matters for a benchmark that needs community adoption.

3. **The framing around open-ended physical exploration fills a real gap.** The paper makes a convincing case that most existing interaction benchmarks (Ant-Maze, Kitchen, Montezuma's Revenge) have too narrow a skill range to support open-ended pretraining, while Minecraft is too slow for rapid iteration. The argument that block-building is rich enough to require motor skills, geometric reasoning, intuitive physics, and long-horizon planning — all through self-directed experience — is well-motivated.

## Weaknesses

### Fatal
None.

### Major

1. **Insufficient experimental validation of the benchmark itself.** The paper claims 42 tasks but provides experimental results on only 17 (≈40%). The self-supervised protocol — the paper's *main* contribution — tests only 12 tasks (cube-1: 2, cube-2: 5, cube-3: 5), and existing algorithms achieve essentially zero success on cube-3 tasks (the bold caption states results "only succeed for the simplest tasks"). The supervised protocol does slightly better (PPO achieves non-zero success on cube-4) but covers at most 17 tasks. This means:
   - There is no empirical evidence that the benchmark provides a meaningful difficulty gradient for the self-supervised protocol beyond 2 trivial tasks (floor = 0, ceiling = "succeeds on 2 tasks"). 
   - The paper claims tasks range "from very easy to extremely hard" (Section 5.2) but evaluates only the easiest end of that range.
   - It is unclear whether the benchmark usefully discriminates between methods: on the harder tasks, all methods fail at approximately the same point.
   
   A benchmark paper needs to demonstrate that the benchmark *works* — that the difficulty signal is sensible, that the evaluation protocol is reproducible, and that the benchmark can differentiate methods. The current evidence falls short of this standard. Without at least a subset of tasks where multiple methods show differentiable performance, the paper is essentially asking the community to trust that the benchmark is well-calibrated based on manual play-throughs alone.

2. **The self-supervised protocol is underspecified in critical details.** Several aspects needed to reproduce the evaluation are unclear:
   - **Goal representation (ℝ³⁴).** The paper states the task-conditioned policy takes a task specification of ℝ³⁴ (line 179), but earlier describes target positions as ℝ^{3k} (line 86). 34 is not divisible by 3 (34/3 ≈ 11.33). It is unclear how tasks with different numbers of cubes (k) are encoded into a fixed 34-dimensional vector, or what the 34 dimensions represent.
   - **Goal proposal mechanism.** During self-supervised training, agents "propose goals" and learn to reach them. The paper does not specify how goals are proposed, sampled, or filtered. The description refers to Appendix A (not available in the submitted version), making this impossible to evaluate from the main text.
   - **Distribution mismatch.** The paper asserts that "it is highly unlikely that the agents will have seen these hand-designed tasks" (line 181), but provides no analysis of the distribution of self-proposed training goals versus test goals. Whether the test tasks are genuinely out-of-distribution or merely unseen instances from a similar distribution is an assumption, not a measured property. For a benchmark centered on generalization, this matters.

### Minor

3. **No quantitative human performance baseline.** The paper states "we manually solved most tasks using the same action space as the agent" (line 169) but reports no human success rates, number of attempts, or times. Human baselines calibrate the task ceiling and validate that tasks are solvable as specified. Without them, the reader cannot distinguish between "this task is genuinely hard for any intelligent agent" and "this task has design issues that make it unnecessarily difficult."

4. **Several internal inconsistencies in stated numbers.** (a) Abstract says "over 42" tasks, body says exactly "42 tasks." (b) Abstract says "single-file implementations of six different algorithms," while the contributions list says "four representative RL algorithms and three self-supervised data-collection algorithms" (= 7). (c) The reference "Kaeling, 1993" is a typo for Kaelbling. These are individually small but, for a benchmark paper where precision about what is being released is important, they signal carelessness.

5. **The LLM evaluation adds limited value.** Asking ChatGPT-5 and Gemini 2.5 Pro to produce high-level open-loop text plans for physically-grounded manipulation tasks — and reporting that they fail — is not a meaningful evaluation. Open-loop language plans are not how these models would be used for physical reasoning, and the result tells the reader nothing about the benchmark's utility. The paper acknowledges this is "not meant to be an extensive evaluation," which undercuts the section's own motivation. This space would be better spent on more RL experiments or human baselines.

### Trivial
None.

## Nice-to-Haves

- **Provide human performance data** (e.g., 3–5 humans attempting the 5 case-study tasks with success rates and time). This would immediately validate solvability and calibrate the ceiling.
- **Report results on a wider subset of the 42 tasks**, even if algorithms fail — showing which tasks are at what difficulty level would provide the difficulty gradient the paper claims.
- **Clarify the ℝ³⁴ goal encoding** in the main text and explain how multi-cube tasks with varying k are represented.
- **Specify the goal proposal mechanism** used during self-supervised training in enough detail to enable reproduction.
- **Consider removing or replacing the LLM evaluation** with additional algorithmic baselines or a difficulty analysis.

## Removed Points

These points from the input review were removed with justification:

1. **"Figure 6 caption vs body text inconsistency (only MEGA and SFL mentioned in caption)"** — The image alt-text and body text list all 4 algorithms. The bold caption focuses on the two that achieve non-zero performance. This is a stylistic choice, not an inconsistency. Removed.

2. **"BRO is relatively obscure"** — An opinion about baseline selection, not a verified weakness. Removed.

3. **"GNN-ATT is an architecture, not an RL algorithm"** — GNN-ATT is cited from Ghasemipour et al. (2022), which is an RL method paper. The criticism is pedantic. Removed.

4. **"State space lacks finger velocity"** — The paper includes finger distance. Whether to include velocity is a design choice. No evidence this harms the benchmark. Removed.

5. **"Unsolved tasks: how is success determined?"** — Success is determined by whether the physical structure matches target cube positions, which is fully specified. The paper's design principle is clear. Removed.

6. **"Results only in figures, not tables"** — A formatting preference, not a substantive weakness. Removed.

7. **"Three seeds is bare minimum"** — A generic criticism common to most RL papers, not specific to this work. Moved to nice-to-have.

8. **"Minecraft comparison is too narrow"** — An opinion about a related work framing choice. Removed.

9. **"Missing limitations about narrow action space, lack of vision"** — The limitations section scopes the benchmark's intended focus; these exclusions are design choices the paper is transparent about. Removed.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a tension between the benchmark's genuine thoughtful design and the insufficient empirical validation of that design, but this is a standard gap in benchmark papers rather than a novel observation.

## Suggestions

1. Substantially expand the experimental evaluation. Show results on at least 25–30 of the 42 tasks (even if most methods fail on harder ones) to demonstrate the difficulty gradient. Include at least one method that achieves non-trivial success on cube-4 or cube-5 tasks in the self-supervised protocol.

2. Provide quantitative human performance baselines on 5–10 tasks spanning the difficulty range.

3. Resolve the ℝ³⁴ encoding in the main text and specify the goal proposal mechanism concretely enough for reproduction.

4. Clean up the inconsistencies in algorithm/task counts between abstract and body.

5. Either remove the LLM evaluation section or redesign it as a grounded evaluation (e.g., an LLM generates reward functions or subgoal sequences that are then executed by a low-level policy).

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>