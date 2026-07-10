Now let me write the final consolidated review.

## Summary

This paper introduces BuilderBench, a benchmark for evaluating open-ended exploration and generalization in RL agents through block-building tasks. The benchmark includes a hardware-accelerated MuJoCo+JAX simulator of a robotic hand manipulating blocks, a task suite of 42 carefully curated structures requiring diverse reasoning skills (physics, geometry, planning), and two evaluation protocols: a multi-task self-supervised protocol (agents explore without supervision then are tested on unseen structures) and a single-task supervised "debug" protocol. The paper provides baseline implementations of several RL and self-supervised algorithms.

## Strengths

- **Genuinely well-motivated gap.** The paper correctly identifies that existing RL benchmarks test narrow skill ranges and that the field lacks good benchmarks for open-ended exploration and generalization (Section 1, paragraphs 2-3). The framing — that agents need to learn through interaction rather than from static human data — is specific and grounded.

- **Task design is the paper's strongest contribution.** The five case studies in Section 5.1 (T-Block, Four Cube Packing, Hexagonal Portal, Leaning Tower, Maximum Overhang) are genuinely interesting. Each requires non-trivial reasoning — diagonal rotation for structural stability, packing under geometric constraints, scaffold-and-counterweight strategies, the maximum overhang problem from combinatorial geometry. These demand qualitatively different strategies, not just harder instances of the same skill, and are clearly described with concrete solution steps.

- **Hardware-accelerated simulator.** Building on MuJoCo + JAX and achieving significant speedups over CPU-bound environments like Crafter, Minecraft, or NetHack is a practical contribution. The concrete example of single-task PPO training on a 2-block task taking 30 minutes on one GPU (Section 1, bullet 4) makes the benchmark accessible to researchers with modest compute.

- **Two-protocol design is sensible.** The multi-task self-supervised protocol tests the paper's central thesis (generalization through unsupervised exploration), while the single-task supervised protocol serves as a tractable entry point for debugging architectures before tackling the harder self-supervised setting.

- **LLM evaluation, while limited in scope, serves as an honest sanity check.** Testing ChatGPT-5 and Gemini 2.5 Pro and finding they fail on all five tasks (Figure 8) is a transparent data point, and the paper is upfront that this is not an extensive evaluation (Section 7.1).

## Weaknesses

### Fatal
None.

### Major

- **Tension between the paper's central framing and the empirical evidence.** The paper's core claim is that BuilderBench evaluates open-ended exploration and generalization via the self-supervised protocol (Section 6, line 177). However, on this protocol, tested algorithms achieve meaningful success only on 1-cube tasks (2 tasks, both solved by MEGA) and show partial improvement on 2-cube tasks (5 tasks, Figure 6), while performance on 3-cube tasks (5 tasks) is explicitly described as "trivial" (Section 7, line 213). The supervised protocol — which does show positive results up to 4 cubes (Figure 7) — is explicitly acknowledged as "not directly evaluat[ing] generalization" (Section 6, line 203). This creates a structural gap: the protocol that tests generalization has limited positive signal, and the protocol with positive results doesn't test generalization. While having hard tasks that current methods cannot solve is a defensible feature of a benchmark, the paper's framing throughout the abstract and introduction emphasizes the self-supervised protocol as the primary contribution.

### Minor

- **PPO dominates all baselines without discussion of tuning effort.** In Figure 7, PPO achieves higher normalized return and success than SAC, CRL, RND, BRO, and GNN-ATT across all cube counts (1–4). PPO even outperforms SAC on cube-1 tasks, which is unusual for continuous control. The paper provides no discussion of hyperparameter tuning, no description of how each baseline was configured, and no indication of whether equal search effort was expended on each method (Section 7, line 215). This makes it difficult to distinguish between "PPO is genuinely the best method for this domain" and "PPO's default hyperparameters happen to work better than other methods' defaults."

- **LLM evaluation's conclusion over-extrapolates from the experimental design.** The setup (Section 7.1, line 219) asks models to provide "a high-level open-loop plan in language" given only a text prompt — this does not test whether an LLM with access to visual observations, the action space, or a closed-loop interaction loop could solve the tasks. The conclusion that "solving our tasks requires non-obvious steps of reasoning that are beyond what current models can achieve through scaling alone" conflates "cannot describe the correct plan verbally from a text description" with "cannot solve the task through interaction." The paper is transparent about the evaluation's limits, but the conclusion drawn is stronger than the experimental design supports.

- **No variance visualization on any experimental figure.** Results are reported across three seeds (Section 7, line 207), but Figures 6 and 7 show single learning curves without error bars, shaded regions, or any indication of run-to-run variability. This makes it difficult to assess whether the reported differences between algorithms are meaningful or within noise.

- **42 tasks claimed but only a subset benchmarked in the main text.** The paper states the task suite contains 42 tasks (Section 5, line 96) but evaluates only 12 in the self-supervised protocol and 17 in the supervised protocol, with overlap. The remaining tasks are in Appendix E (stripped by the parser). While the paper's design principle includes tasks that range from easy to extremely hard (Section 5.2, line 171), the main text substantially over-represents the scope of what was actually tested.

### Trivial
None.

## Nice-to-Haves

- Run an oracle experiment for the self-supervised protocol (e.g., warm-start with the supervised protocol's success) to establish that the evaluation pipeline can produce signal on harder tasks.
- Add a small wall-clock time comparison table to the main text summarizing the simulator's speed advantage, rather than relegating all details to Appendix B.

## Removed Points

These points are flagged to be removed; treat them with caution.
- **Speed comparison unverifiable from main text** — Removed per policy: the speed comparison is in Appendix B of the original submission; the appendix was stripped by the parser, not omitted by the authors.
- **Reward function details missing from main text** — Removed per policy: the paper explicitly references Appendix A.2 for reward function details; the appendix was stripped by the parser.
- **LLM prompts deferred to Appendix D** — Removed per policy: prompts exist in the original Appendix D of the submission.
- **State space derivation not fully explained** — The paper clearly derives the 11+13n state space from the listed components; this is adequately specified.
- **Related work comparison is qualitative** — Qualitative comparison in a related work section is standard practice, not a weakness.
- **Algorithm count inconsistency (six vs seven)** — With RND overlapping in both RL and self-supervised categories (4+3−1=6), the counts can be consistent.

## Novel Insights

None beyond the paper's own contributions. The suggestions for improvement (oracle experiment for self-supervised protocol, better baseline tuning documentation, redesigning the LLM evaluation) are standard recommendations for strengthening a benchmark paper rather than novel insights.

## Suggestions

1. **Document hyperparameter tuning** for all baselines and indicate whether equal search effort was allocated to each method.
2. **Add variance visualization** (error bars or shaded regions) to all experimental figures.
3. **Recalibrate the paper's framing** to acknowledge that the self-supervised protocol currently has demonstrated signal primarily on simpler tasks, and present the supervised protocol as the primary near-term benchmark alongside the self-supervised one as the long-term challenge.
4. **Either redesign the LLM evaluation** to test closed-loop interaction (with visual observations and action outputs) or soften the conclusion drawn from the current open-loop text-planning setup.

## Score and Decision

This is a well-motivated benchmark with genuinely interesting task design and practically useful simulator infrastructure. The tasks are more diverse and cognitively rich than what most RL benchmarks offer. The core tension between the paper's framing and the self-supervised protocol's limited positive results is real but not fatal — hard unsolved tasks are a defensible feature of a benchmark, and the supervised protocol provides a tractable path forward. The remaining issues (PPO tuning documentation, variance visualization, LLM evaluation scope) are all addressable.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>