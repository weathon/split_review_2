Now let me compile the final review.

## Summary

This paper introduces EGG-SR, a framework that uses equality graphs (e-graphs) to integrate symbolic equivalence awareness into three families of symbolic regression algorithms: MCTS, DRL, and LLM-based methods. The core idea is to compactly encode semantically equivalent but syntactically distinct expressions via e-graphs, then use these equivalences to prune redundant MCTS exploration, aggregate reward signals in DRL, and enrich LLM feedback prompts. Theoretical analysis shows tighter regret bounds for EGG-MCTS and variance reduction for the EGG-DRL gradient estimator.

## Strengths

- **The problem is well-motivated and underexplored.** The paper clearly articulates how symbolic equivalence causes redundant exploration in MCTS, DRL, and LLM-based SR methods. The running example (log(x₁²x₂³) and its equivalent forms) cleanly illustrates the issue.

- **Modular design with three concrete integrations.** The same e-graph module is adapted to three distinct algorithmic families in conceptually different ways: pruning redundant subtrees in MCTS backpropagation, aggregating probability mass over equivalent trajectories in the DRL policy gradient, and enriching LLM prompts. This is a genuine engineering contribution.

- **Theoretical analysis is a meaningful addition.** Theorem 3.1 (tighter regret bound via reduced effective branching factor κ_∞ ≤ κ) and Theorem 3.2 (unbiasedness + variance reduction of the EGG-DRL gradient estimator) go beyond what most SR papers provide, even though they build on prior work (Leurent & Maillard 2020; REINFORCE-style variance reduction).

- **Space efficiency demonstration is convincing.** Figure 4 cleanly shows exponential memory savings from e-graph compaction for crafted expressions with 2^{n-1} equivalent variants.

## Weaknesses

### Fatal
None.

### Major

- **Main quantitative results lack variance or multiple-run information.** Table 1 reports only "median NMSE" with no standard deviations, number of random seeds, or statistical tests. In a domain where NMSE values vary by orders of magnitude across runs, single medians are uninformative. Without this information the reader cannot assess whether the observed improvements are reliable or due to noise.

- **No comparison against external state-of-the-art SR methods.** The paper compares each EGG variant only against its own unaugmented baseline (EGG-MCTS vs MCTS, etc.). There are no comparisons to strong standalone methods such as PySR, AI-Feynman, or recent GP-based approaches. Since the improvements over internal baselines are modest in some settings (e.g., Table 1 noiseless: EGG-DRL NMSE 0.020 vs DRL 0.030 on (2,1,1)), it is unclear whether these gains translate to practical value against the state of the art.

- **Benchmark scope is narrow.** Table 1 uses only 4 trigonometric datasets from a single source (Jiang & Xue 2023), all containing sin/cos operators that the rewrite rules specifically target. Table 2 uses 4 scientific problems. This is a very limited evaluation for a paper claiming benefits "across several benchmarks." The Feynman, Nguyen, or Penn ML benchmark suites — standard in the SR literature — are not used (though 7 Feynman expressions appear in Appendix visualizations, they are not used for quantitative NMSE comparison).

- **The LLM comparison is methodologically uncontrolled.** The paper states: "The result of LLM-SR directly uses the reported result in Shojaee et al. (2025)." Without running LLM-SR in the same controlled setting (same API version, temperature, number of queries per budget, random seed), differences could arise from API drift, prompt format, or stochasticity. This is a significant confound.

- **A contradictory result is not discussed.** In Table 1's noisy setting, EGG-DRL underperforms standard DRL on (4,4,6) (5.09 vs 2.46), yet the text claims "Expressions returned by Egg-DRL achieve a smaller NMSE value on noiseless and noisy settings" without acknowledging this exception or providing an explanation.

### Minor

- **The DRL gradient estimator's unbiasedness claim needs better justification in the main text.** The EGG-DRL estimator (Eq. 4) uses ∇_θ log[Σ_k p_θ(τ_i^{(k)})] rather than Σ_k ∇_θ log p_θ(τ_i^{(k)}). The paper claims unbiasedness (Theorem 3.2) but the proof sketch ("expanding the definitions") is too terse to be convincing; the verification depends entirely on the appendix proof (which is stripped). The concern is substantive: the gradient is taken over a sum of probabilities of trajectories that may be sampled from a distribution different from p_θ.

- **The MCTS "search tree size" result is ambiguous.** The paper interprets the larger tree in EGG-MCTS as evidence of "exploration of a larger and more diverse search space" (Figure 3 left). However, the increased tree size may partly be an artifact of EGG explicitly storing entries for equivalent paths that standard MCTS would simply not store. The metric conflates mechanism (storing more nodes) with outcome (better exploration).

- **No ablation studies.** There is no analysis isolating the effect of each design choice: e.g., how the number K of equivalent extracted sequences affects DRL performance, or whether a simpler hashing-based transposition table (rather than e-graphs) would achieve similar gains for MCTS.

- **LLM integration is underspecified.** The LLM section (Section 3.2, one paragraph) lacks specifics: how many equivalent expressions are extracted per iteration, how they are summarized into a prompt, the prompt format, the number of rounds, and how Python-function-to-expression wrappers are validated. The claimed benefit — "enriching the feedback prompt" — is intuitive but the mechanism is not concretely described.

- **Failure cases and rewrite-rule coverage are not discussed.** The paper does not analyze what happens when target expressions involve identities not covered by the rewrite rule set, or when the rewrite system is not confluent. The method's practical scope is not bounded.

### Trivial
None.

## Nice-to-Haves

- Run all experiments with multiple random seeds (e.g., 10) and report mean ± std.
- Add standard SR benchmarks (e.g., the full Feynman dataset, Nguyen benchmarks).
- Compare against at least one strong external baseline (PySR, AI-Feynman).
- Run LLM experiments in a controlled setting rather than comparing against published numbers.
- Ablate the number K of equivalent sequences in the DRL gradient estimator.
- Show whether the time savings from faster convergence outweigh the EGG overhead, rather than only showing that overhead is small.
- The space efficiency comparison (Figure 4) compares against an "array-based" straw man (storing all 2^{n-1} variants). A more relevant comparison would be memory usage of EGG-SR vs. the baseline method without EGG during actual training.

## Removed Points

- **"Unified framework claim is overblown"** — REMOVED. The paper uses the same e-graph module across three methods in a modular way. Calling this a "unified framework" is a reasonable characterization, not an overclaim.
- **"Contradictory results on (3,2,2) noisy"** — REMOVED (with correction). The reviewer mistakenly attributed MCTS row numbers (0.012 vs 0.007) to DRL. The actual EGG-DRL noisy (3,2,2) comparison is 0.35 vs 0.44, which favors EGG-DRL. Only (4,4,6) noisy is genuinely contradictory; this is kept in the major weaknesses.
- **"Time efficiency experiment only measures overhead, not overall speedup"** — DEMOTED to Nice-to-Have. Showing that overhead is small is useful; demonstrating overall speedup would strengthen the paper but is not required.
- **"Space efficiency comparison is against a straw man"** — DEMOTED to Nice-to-Have. The comparison illustrates a property of e-graphs; a more practical comparison would be a nice addition but the current one is not invalid.
- **"No discussion of non-termination of equality saturation"** — REMOVED. The paper mentions "a maximum number of iterations" is used as a stopping criterion, which addresses termination.

## Novel Insights

The harsh critic's review offers one genuinely novel observation beyond the paper's own contributions: that the larger MCTS search tree in EGG-MCTS may be a confounded metric — the tree size increase could reflect the mechanism (explicit storage of equivalent paths) rather than better exploration. This is an insightful caveat for interpreting Figure 3. The remainder of the critique is standard evidential concerns (error bars, benchmarks, baselines) that any careful reader would identify.

## Suggestions

1. Provide variance information (standard deviations or confidence intervals) for all quantitative results, based on multiple independent runs.
2. Expand the benchmark suite to include standard SR collections (Feynman, Nguyen) where the rewrite rules are not hand-picked for the operators.
3. Run at least one external SR method (PySR, AI-Feynman) under the same evaluation protocol to calibrate whether the EGG improvements translate to practical gains.
4. For the LLM experiment, either run LLM-SR in a controlled setting or acknowledge the limitation explicitly.
5. Add ablation on K (number of equivalent sequences) for the DRL estimator.
6. Discuss the (4,4,6) noisy failure case and provide a hypothesis for why EGG-DRL underperforms there.
7. Expand the LLM section with concrete details about prompt construction and iteration protocol.

## Score and Decision

The paper identifies a genuine and underexplored problem, proposes a clean modular solution, and provides theoretical grounding that is uncommon in SR papers. However, the experimental evaluation is substantially weaker than what is needed to support the paper's claims: the main results lack any measure of variability, the benchmarks are narrow and hand-picked to match the method, there are no comparisons to competitive external methods, and the LLM comparison is methodologically uncontrolled. One contradictory result goes unacknowledged. These are evidential issues rather than fatal methodological flaws — the core idea has clear merit — but the evidence as presented does not convincingly demonstrate that the method works reliably.

Given the gap between the strength of the claims and the quality of the evidence, the paper is not ready for acceptance in its current form.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>