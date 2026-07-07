Now I have enough to write the draft review. Let me proceed.## Summary
BuilderBench is a benchmark for evaluating generalist RL agents on open-ended 3D block-building tasks. It provides a MuJoCo+JAX hardware-accelerated simulator, a curated 42-task suite requiring physics intuition, geometric reasoning, and long-horizon planning, six single-file algorithm implementations, and two training protocols — a self-supervised multi-task protocol and a supervised single-task "training wheels" protocol.

## Strengths
- **Genuinely creative and non-trivial task design.** The five case-study tasks (Section 5.1) each require non-obvious reasoning: T-Block demands a 45° rotation for geometric support, Four Cube Packing is a tight spatial constraint problem, the Hexagonal Portal requires scaffolding discovery and simultaneous two-cube placement, the Leaning Tower requires counterweights and strict ordering. Task difficulty arises from Newtonian physics + planning rather than visual complexity.
- **Concrete simulator speed advantage.** The claimed 10–100× speedup over CPU-based benchmarks (Appendix B) is a practical benefit for academic labs using consumer hardware, and two-block stacking training in 30 minutes on a GPU is a directly verifiable claim.
- **Dual-protocol design with genuine utility.** The self-supervised protocol tests generalization under no task supervision; the supervised debug protocol (Section 6) enables algorithmic iteration and provides usable gradient signal (Figure 7 shows PPO making progress on 1–2 cube tasks while failing at 3–4 cubes).
- **Honest inclusion of tasks with unknown solutions.** Section 5.2 explicitly acknowledges that "tasks should include some whose solutions are unknown even to the authors," which is an intellectually honest benchmark design choice that positions it as genuinely open-ended.

## Weaknesses

### Fatal
None.

### Major
- **Unexplained training-to-evaluation mapping in the self-supervised protocol.** Section 6 states the agent "does not receive any task specification during training" yet must "learn a task conditioned policy, which can take as input a state (R^{11+13n}) as well as a task specification (R^{34})." Section 7 clarifies that MEGA/SFL generate autotelic goals from previously visited states — but the paper never states whether these autotelic goals are encoded in the same R^{34} representation as the evaluation task specifications, nor how the test-time target cube position vector maps into the training goal space. This matters because, without this explanation, the validity of the self-supervised evaluation results (Figure 6) cannot be verified from the paper alone. A reader attempting to reproduce the self-supervised protocol would face a fundamental gap.

- **Self-supervised results provide nearly no discriminative signal above 1-cube tasks.** Figure 6 shows UDRL and RND at near-zero across all configurations, and MEGA succeeds only for 1-cube tasks. While showing that current algorithms fail is appropriate for a benchmark paper, the complete absence of finer-grained metrics (fraction of blocks correctly placed, distance-to-target) means the self-supervised results cannot distinguish between slightly better and slightly worse algorithms in the failing regime. Researchers seeking to use BuilderBench to iterate on algorithms will find Figure 6 offers almost no actionable signal for 2+ cube tasks.

### Minor
- **Incomplete experimental coverage without stated selection criteria.** Figure 6 covers 12 tasks and Figure 7 covers 17 tasks out of 42 total. The paper notes "12 of the lowest complexity tasks" for Figure 6 but gives no principled account of which 17 tasks were selected for Figure 7 or how they were chosen. For a benchmark paper this undercuts the ability to characterize the full difficulty profile of the suite.

- **LLM evaluation (Section 7.1) lacks qualitative failure analysis.** Table 8 shows all-fail (✗) for ChatGPT-5 and Gemini 2.5 Pro across all five tasks. No analysis is provided of *what* the models got wrong — did they fail on stability constraints, missed scaffolding steps, or something else? A brief failure mode analysis would transform this from a binary result table into a window into the nature of the tasks' difficulty.

### Trivial
None.

## Nice-to-Haves
- A concrete example in the main text showing how an autotelic goal representation maps to the R^{34} evaluation task specification would clarify the self-supervised protocol without requiring additional experiments.
- Reporting per-block displacement from target or partial-credit metrics alongside Figure 6 would give researchers a usable gradient even in the all-near-zero regime.
- Naming at least one "author-unsolvable" task in the main text (not deferred to Appendix E) would sharpen the Section 5.2 design philosophy claim.
- A brief sentence in the main text explaining which reward variant (dense, permutation-invariant) is used by default in Figure 7, rather than full deferral to Appendix A.2, would improve interpretability.

## Removed Points
*These points are flagged as removed — treat them with caution.*

- **Harsh critic's "maximalist framing" concern** (agents-as-scientists language in introduction). This is a tone/scope comment, not a methodological flaw. The actual technical contribution stands independently. Removed as a distinct weakness.
- **Section 5.2 tasks not named in main text** — moved entirely to Nice-to-Haves rather than treated as a weakness, as Appendix E is cited and covers this.
- **Reward function details deferred to appendix** — removed per hard rule against criticizing appendix deferral.

## Novel Insights
BuilderBench demonstrates that a 5-DOF robotic hand interacting with cubes under Newtonian physics generates tasks spanning motor control, geometric constraint satisfaction, combinatorial reasoning, and emergent tool use (scaffolding, counterweights), all within a unified state-action space. This suggests that the combination of a physically grounded simulator, a simple enough action space to require genuine planning, and a scalable task parameterization (number of cubes) may be a more productive benchmark design strategy than complex task-specific engineering — an insight applicable beyond this benchmark.

## Suggestions
- Include one explicit worked paragraph in Section 6 showing how MEGA/SFL's autotelic goal representation corresponds to R^{34} at evaluation time.
- Compute and report at least one finer-grained metric (e.g., mean per-block displacement from target position) from the existing self-supervised runs to enable algorithmic discrimination in the near-zero regime.
- State explicitly in the main text which 17 tasks were included in Figure 7 and why (or give the selection principle).

---

## Score and Decision

**Calibration Anchors:**

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| KL Divergence GFlowNets | Uj0h13lVrR.md | 1.00 | R1 | Strong reject; fundamentally flawed — not comparable |
| RL generalization (non-param) | fvTaoyH96Z.md | 2.33 | R1 | Reject; incomplete methodology; weaker than BuilderBench |
| Open-ended policy RL (Minecraft) | 5f0n5yi8qK.md | 3.40 | R1 | Reject; incremental video-prompt idea on Minecraft, weaker contribution |
| Discovering Minimal RL Envs | VDkye4EKVe.md | 3.00 | R1 | Reject; limited scope synthetic envs; lower novelty |
| SoftPhy benchmark | pNlntv7A9X.md | 5.00 | R1 | Borderline reject; similar benchmark class, narrower task design |
| FEABench | hDkLpu1E64.md | 4.50 | R1 | Borderline reject; benchmark for LLM physics reasoning; less novel than BuilderBench |
| Overcooked Generalisation Challenge | YKvBiRWdQC.md | 5.75 | R1 | Rejected; GPU-accelerated generalization benchmark; comparable structure but narrower domain |
| AgentQuest | fp6t3F669F.md | 6.25 | R1 | Accepted; LLM/VLM benchmark with diverse tasks; comparable benchmark paper |
| OGBench | M992mjgKzI.md | 7.00 | R1 | Accepted; offline GCRL benchmark, 85 datasets, 8 env types, well-documented; more complete coverage than BuilderBench |
| PhysBench | Q6a9W6kzv5.md | 8.00 | R1 | Accepted; 100K entry VLM physics benchmark; much larger scale |

**Round 1 Bracket:** 5.5–7.0

BuilderBench has domain novelty and creative task design at the level of OGBench (7.0) but falls short on completeness: OGBench covers 85 datasets and 8 env types with clear selection criteria; BuilderBench presents results on fewer than half of its 42 tasks without justified selection, and the self-supervised protocol has a methodological documentation gap. The Overcooked Challenge (5.75, rejected) is similar in spirit — GPU-accelerated, shows SOTA fails, clean benchmark — and was rejected partly due to limited analysis depth. BuilderBench is stronger than Overcooked (richer task design, more reasoning diversity, two protocols), but not as complete as OGBench.

**Final score: 6.0** — borderline accept. The benchmark contribution is real and timely, with a genuinely novel task design and meaningful practical advantages. The two major weaknesses (under-documented self-supervised evaluation mechanism; incomplete experimental coverage) are addressable in revision but are significant enough to prevent a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>