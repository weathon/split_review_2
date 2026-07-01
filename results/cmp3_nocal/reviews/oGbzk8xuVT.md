## Summary

BuilderBench introduces a hardware-accelerated block-building benchmark (MuJoCo + JAX) with 42 carefully curated tasks designed to test open-ended exploration, generalization, and embodied reasoning in RL agents. The benchmark provides two protocols (self-supervised and supervised), a fast simulator (10–100× speedup over CPU-based benchmarks), and open-source reference implementations of six algorithms. The core contribution is the benchmark infrastructure itself, not a new algorithm.

---

## Strengths

1. **Fast, hardware-accelerated simulator (Section 4, verified).** Built on MuJoCo + JAX, achieving 10–100× speedup over CPU-based open-ended benchmarks (Crafter, Minecraft, NetHack). This directly addresses a major practical bottleneck in RL research and makes the benchmark accessible for academic groups with limited compute.

2. **Well-conceived tasks that require genuine reasoning (Section 5.1, verified).** The five case-study tasks (T-Block, Four Cube Packing, Hexagonal Portal, Leaning Tower, Maximum Overhang) are genuinely novel and non-trivial. The Hexagonal Portal task, for example, requires scaffold construction, simultaneous two-cube lifting, and scaffold removal — all in a single episode. These tasks go well beyond simple pick-and-place and convincingly demonstrate the benchmark's potential.

3. **Open-source with single-file reference implementations (Section 1, contributions list, verified).** The combination of an open simulator, 42 tasks, and compact single-file algorithm implementations lowers the barrier to entry and is critical for community adoption.

4. **Principled task-suite design (Section 5.2, verified).** The four design principles (distinct skills per task, human-solvability, wide difficulty range including unsolved tasks) are the right criteria for a benchmark intended to drive multi-year algorithmic progress.

---

## Weaknesses

### Fatal
None.

### Major

1. **Baseline experiments cover only a minority of the 42-task suite (verified: Figures 6–7 and Section 7).** The self-supervised protocol evaluates 12 tasks (cube-1, cube-2, cube-3), and the supervised protocol evaluates 17 tasks (cube-1 through cube-4). These sets overlap, meaning at most ~17 of 42 tasks receive any experimental evaluation. The remaining ~25 tasks — presumably the hardest ones — are not benchmarked at all. While the paper's claim that "many of these tasks challenge the current iteration of algorithms" is true for the subset tested, the reader cannot assess the difficulty distribution or whether the other 25 tasks are genuinely diverse or merely impossible. A benchmark paper should provide per-task results (even if most entries are zero) or at minimum characterize why the untested tasks are beyond current methods.

### Minor

2. **No systematic human performance calibration (verified: Section 5.2).** The paper states that the authors "manually solved most tasks using the same action space as the agent," but presents no systematic human data — no success rates, no time-to-solve, no variance across solvers. Human calibration is a standard expectation for benchmark papers (Atari, Minecraft, ARC-AGI all include it) and would help distinguish tasks that are genuinely hard in an interesting way from those that are merely tedious or poorly specified.

3. **The LLM evaluation (Section 7.1) is tangential and its conclusions are weakly supported (verified).** The experiment asks ChatGPT-5 and Gemini 2.5 Pro to produce a single open-loop text-based plan from a text description. This tests text-based mental planning, not embodied reasoning in the benchmark's intended setting. The conclusion — that tasks require reasoning "beyond what current models can achieve through scaling alone" — is not well-supported by testing only two proprietary models on one specific (and arguably unnatural) use mode. The paper itself hedges ("not meant to be an extensive evaluation"), but the section adds little value to the benchmark and the conclusion overstates what the evidence can support. Replacing this section with a diagnostic analysis of where baselines fail would better serve the paper's goals.

4. **"Open-ended" framing is somewhat overstated relative to the actual environment (verified: abstract, Sections 1, 5, 8).** The paper repeatedly invokes "open-ended exploration" and compares to Minecraft and XLand. However, the environment has a single fixed setting (flat floor), a single agent morphology (flying gripper), a 5-D action space, and a limited behavioral repertoire (pick, place, nudge, rotate). The combinatorial space of block arrangements is large, but the space of qualitatively different *behaviors* is narrow relative to what "open-ended" typically describes in the literature. The paper acknowledges missing stochasticity and partial observability (Section 8) but does not address this more basic scope gap. This does not undermine the benchmark's value, but the framing sets up expectations the benchmark does not fully meet.

5. **Key definitions deferred from the main text (verified).** "Normalized return" and "normalized success" are used throughout Section 7 (Figures 6–7) without formal definition in the main body. The task specification dimension (R³⁴ in Section 6) is specified differently from the per-task vector of target cube positions (ℝ^(3k) in Section 4, where k ≤ 10 gives at most ℝ³⁰). These discrepancies should be clarified.

6. **No diagnostic analysis of why algorithms fail (verified: Section 7).** The paper reports that PPO succeeds on cube-1/cube-2 tasks while SAC, CRL, RND, BRO, and GNN-ATT all fail to achieve non-zero success on harder tasks, but provides no analysis of *why*. Is the bottleneck exploration, credit assignment, horizon length, or representation? For a benchmark aiming to "provide a meaningful feedback signal for algorithmic research" (Section 5.2), this is a missed opportunity to guide future work.

### Trivial

None.

---

## Nice-to-Haves

- A table with per-task success rates across all 42 tasks (even if most entries are zero) would give the full difficulty distribution.
- Including model-based RL baselines (DreamerV3, TD-MPC2) or hierarchical RL methods would strengthen the baseline coverage, but their absence does not undermine the benchmark's contribution.
- Reporting GPU hours per baseline would help researchers estimate resource requirements.
- A brief discussion of how policies handle variable-sized state inputs (R^{11+13n} where n varies) would address a natural architectural question.

---

## Removed Points

- *Criticism that the LLM evaluation tests "a fundamentally different task" and should be "removed or completely redesigned"* — Kept as Minor instead of Fatal/Critical because the paper explicitly hedges its claims ("not meant to be an extensive evaluation"), and the section is clearly supplemental rather than central to the benchmark contribution. The criticism about weak support for the "scaling" conclusion is valid but does not make the section a structural error.
- *Missing model-based RL / hierarchical RL / behavioral cloning baselines* — Demoted to Nice-to-Have. The paper provides 6 (supervised) + 4 (self-supervised) algorithms. Missing specific algorithm families is a coverage gap but not a fatal flaw for a benchmark paper whose primary contribution is the infrastructure, not a comprehensive leaderboard.
- *"Only 5 of 42 tasks receive detailed description"* — The remaining tasks are in the appendix (stripped by the parser). This is a paper organization choice, not a substantive weakness.
- *Criticism about the opening line ("Today's AI models learn primarily through mimicry and sharpening") being a sweeping characterization* — This is a stylistic observation, not a substantive weakness.
- *State space dimension varying with n* — The dimension is clearly stated as ℝ^{11+13n}. How policies handle this is a reasonable question but fits better as a nice-to-have.
- *Request for computational cost (GPU hours)* — Nice-to-have, not a weakness.
- *Various section-by-section notes that are commentary rather than concrete weaknesses* — Removed as noise.

---

## Novel Insights

None beyond the paper's own contributions. The reviewer's main novel observation is that the baseline coverage gap (only ~17/42 tasks tested) is the most significant weakness, and that the LLM evaluation section is too tangential to support the role it plays in the paper's narrative.

---

## Suggestions

1. **Expand baseline coverage.** At minimum, provide a table of per-task success rates across all 42 tasks for the algorithms tested, even if most entries are zero. This would give the full difficulty distribution and allow readers to understand which tasks separate current methods.
2. **Add human calibration data.** Have 3–5 humans attempt a representative subset of tasks using the same action space and report success rates, time, and observed strategies.
3. **Replace or reframe the LLM evaluation.** Either remove Section 7.1 entirely (it adds little to the benchmark's value) or redesign it to test LLMs as components of a larger system (e.g., providing visual state information, allowing iterative refinement). Alternatively, replace it with a diagnostic analysis of why PPO succeeds on simpler tasks but fails on harder ones.
4. **Clarify metric definitions and the task specification dimension discrepancy** (R³⁴ vs ℝ^(3k)) in the main text.
5. **Tone down the "open-ended" framing** where it compares to Minecraft/XLand, or add a discussion explaining how the benchmark's notion of open-endedness (combinatorial task diversity) differs from environmental open-endedness.

---

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>