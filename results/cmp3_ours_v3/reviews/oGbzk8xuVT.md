## Summary

BuilderBench introduces a block-building benchmark for RL with a JAX-accelerated MuJoCo simulator, 42 hand-designed tasks requiring diverse physical reasoning skills (geometry, counterweights, scaffolding, packing), and two evaluation protocols (self-supervised for zero-shot generalization, supervised single-task "training wheels"). The paper benchmarks several RL algorithms (SFL, MEGA, PPO, SAC, etc.) and finds current methods succeed only on the simplest 1-2 cube tasks, establishing that the benchmark captures meaningful difficulty.

## Strengths

1. **Creative and well-motivated task design.** The five case studies (T-Block, Four Cube Packing, Hexagonal Portal, Leaning Tower, Maximum Overhang) each require non-trivial physical reasoning—rotating a base cube for diagonal support, packing through re-orientation, building temporary scaffolds, counterweights for overhangs, center-of-mass reasoning—that goes well beyond what standard RL benchmarks test. These examples convincingly demonstrate that block-building with few cubes can generate problems spanning a genuine range of difficulty and connect to known mathematical problems (Paterson et al., 2007).

2. **Practical simulation infrastructure.** The JAX-accelerated MuJoCo simulator (claimed 10-100× speedup over CPU-based benchmarks like Crafter, Minecraft, NetHack) is a genuine practical advantage that lowers the barrier to entry for academic research. The paper states that training a PPO agent to stack two blocks takes 30 minutes on a single GPU.

3. **Sensible "training wheels" protocol.** The single-task supervised protocol provides a tractable entry point for studying architectural and algorithmic choices before tackling the harder self-supervised generalization problem. Including both dense and sparse reward variants is good practice.

4. **Open-source release with reference implementations.** The paper open-sources the benchmark and provides single-file algorithm implementations.

## Weaknesses

### Fatal
None.

### Major

1. **Evaluation covers only 17 of 42 tasks, with no characterization of the remaining 25.** The paper claims a 42-task suite (line 96). The self-supervised protocol evaluates 12 tasks (2 one-cube, 5 two-cube, 5 three-cube); the supervised protocol evaluates 17 tasks (the same 12 plus 5 four-cube tasks). The remaining 25 tasks (60% of the suite) receive no benchmarking results, difficulty characterization, or even a description of what skills they require in the main text. The paper states "the complete list of tasks, along with visualizations and the capabilities required to solve them, is provided in Appendix E" (lines 102-103), but the main text does not characterize these tasks or explain why they were excluded. For a benchmark paper, this is a significant gap: it is impossible to assess whether the full suite is genuinely harder, trivially similar, or even solvable.

2. **Human-solvability and unknown-solution claims are asserted without quantitative evidence.** Section 5.2 states that "we manually solved most tasks using the same action space as the agent" and that "a small minority of tasks" have solutions unknown even to the authors. These claims are critical for establishing that the benchmark is solvable and that failure reflects algorithmic weakness rather than impossible tasks. However, no quantitative evidence is provided—no success metrics, video demonstrations, or identification of which tasks fall into which category. The five case studies in Section 5.1 describe solutions qualitatively but do not report quantitative success metrics.

3. **LLM evaluation (Section 7.1) tests none of the capabilities BuilderBench is designed to measure.** The paper asks ChatGPT-5 and Gemini 2.5 Pro to produce high-level open-loop plans in natural language given a textual description of the environment and task (lines 217-229). This tests none of the benchmark's core capabilities: low-level motor control, exploration through interaction, trial-and-error learning, or skill composition. The LLMs were never given the opportunity to interact with the environment, so their failure is entirely expected and uninformative. The paper itself acknowledges "this is not meant to be an extensive evaluation" (line 219), further questioning why the section is included. This section should be removed or replaced with a meaningful evaluation (e.g., multimodal models given visual input, or LLM-as-planner combined with a low-level policy).

### Minor

4. **"Normalized return" and "normalized success" are not defined in the main text.** These are the primary evaluation metrics for the benchmark, but the paper defers their definition to Appendix A.2 (stripped). For a benchmark paper, readers should not need to consult the appendix to interpret the central experimental results.

5. **Aggregate results obscure the per-task difficulty structure.** Figures 6 and 7 report aggregated normalized returns across task groups (e.g., 5 two-cube tasks pooled together). The paper's central claim is that tasks require distinct reasoning skills, yet the evaluation collapses these distinctions. A per-task breakdown (e.g., a heatmap showing which methods solve which tasks) would be far more informative and is standard practice for benchmark papers.

6. **"Open-ended exploration" framing is inflated.** The paper positions BuilderBench as centering "open-ended exploration" (Abstract, line 41). However, the evaluation uses a fixed set of 42 hand-designed target structures under a train/test split. This is zero-shot generalization from unsupervised pre-training—a valuable problem in its own right—but it is not "open-ended" in the sense the term has acquired in the literature (e.g., XLand's procedural task generation, POET's adaptive task evolution). The tasks are well-designed, and the zero-shot generalization framing is sufficient justification; the open-ended framing overreaches.

### Trivial

7. **Inconsistency in algorithm counts.** The abstract says "six different algorithms" (line 9), the contributions list says "four representative RL algorithms and three self-supervised data-collection algorithms" (7 total, line 44), and Section 7 benchmarks 4 self-supervised + 6 supervised algorithms (with RND in both lists). This should be resolved.

8. **Task specification vector (R^34) mentioned but not explained.** Line 179 states the agent receives a task specification in R^34 without describing what the 34 dimensions represent. Since this is the core interface for goal-conditioned policies, it should be specified.

## Nice-to-Haves
- Per-task result visualizations (e.g., a heatmap) would substantiate the claim that tasks require distinct skills.
- A speed comparison summary with concrete numbers in the main text (currently deferred to the stripped Appendix B).
- Quantifying human performance on a representative subset of tasks would strengthen the solvability baseline and benchmark validity.

## Removed Points
- *"LLM evaluation does not test multimodal models"* → Removed because this is a variant of Weakness 3 (the LLM evaluation is uninformative regardless of modality).
- *"Section 2 related work is generic"* → Removed as a not-substantive criticism; the related work sufficiently positions the benchmark.
- *"Missing discussion of 2D vs 3D distinction with Kinetix"* → Removed as a nice-to-have rather than a weakness; the paper discusses the comparison in Section 2.
- Various formatting/style nitpicks from the section-by-section commentary → Removed per filtering rules.
- *"Speed test deferred to stripped appendix"* → Folded into Nice-to-Haves rather than a standalone weakness.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Provide per-task results (e.g., a heatmap or table) for all benchmarked tasks, and at minimum characterize the remaining 25 tasks by difficulty tier and required skills.
2. Establish solvability baselines with either human performance data or automated replay of demonstrated solutions for a representative subset of tasks.
3. Remove the LLM evaluation section (Section 7.1) or replace it with a meaningful evaluation where the model can interact with the environment.
4. Define the normalization scheme for "normalized return" and "normalized success" in the main text.
5. Correct the "open-ended" framing to more accurately reflect that the benchmark evaluates zero-shot generalization from unsupervised pre-training on a fixed task suite.
6. Resolve the algorithm count inconsistency and explain the task specification vector (R^34) in the main text.

## Score and Decision

**Calibration:** | Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| MuJoCo Manipulus (b9Ne5lHJ8Y) | 3.40 | 1 | Much weaker: simpler tasks, CPU-only, fewer tasks. BuilderBench is clearly stronger. |
| Jumanji (C4CxQmp9wc) | 6.25 | 2 | Similar JAX-accelerated benchmark. Jumanji evaluated all 18 environments; BuilderBench only 17/42. |
| Generalization Gap in Offline RL (3w6xuXDOdY) | 6.50 | 1 | Thorough benchmark evaluation. BuilderBench has more creative tasks but weaker validation. |
| OGBench (M992mjgKzI) | 7.00 | 1 | Comprehensive benchmark with thorough evaluation across all environments. BuilderBench weaker in completeness. |
| OMNI-EPIC (Y1XkzMJpPd) | 6.75 | 1 | Similar gap between ambitious claims and evidence. Comparable dynamic. |
| RLP (pYmQId95iR) | 4.25 | 2 | Puzzle-based RL benchmark, rejected. BuilderBench's physical domain is better motivated. |
| ManiSkill-HAB (6bKEWevgSd) | 5.75 | 2 | GPU-accelerated manipulation benchmark. BuilderBench comparable in infrastructure quality. |

**Round 1 Bracket: [5.5, 6.5]** — BuilderBench's core contribution (creative task design, JAX-accelerated simulator, reference implementations) is solid and comparable to accepted benchmark papers like Jumanji (6.25) and the Generalization Gap paper (6.50). However, it has more significant evaluation gaps than those anchors.

**Final Score: 6.0** — The paper's core contribution—the creatively designed task suite, fast JAX-accelerated environment, and reference implementations—is real and valuable. The five case studies in Section 5.1 are genuinely compelling and demonstrate depth of physical reasoning absent from existing RL benchmarks. However, the evaluation is incomplete (only 17/42 tasks benchmarked with no characterization of the rest), the human-solvability claims central to the benchmark's validity are unverified, and the LLM evaluation section adds nothing. These are fixable problems that do not invalidate the core contribution but prevent a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>