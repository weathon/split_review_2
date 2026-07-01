Now let me write the final review with all the calibration data considered.

## Summary

The paper proposes combining contrastive pre-training of code graph embeddings with reinforcement learning for automated code refactoring. The framework consists of a syntax-guided contrastive encoder, a composite reward function that fuses learned embeddings with traditional code quality metrics, and a graph-attention policy network. Evaluation on three refactoring datasets compares against rule-based, learning-based, and RL-based baselines.

## Strengths

1. **Novel combination of contrastive pre-training with RL for code refactoring.** The idea of learning refactoring-aware representations through self-supervised contrastive objectives rather than handcrafting reward features is a genuine contribution. The paper correctly identifies a real limitation in prior RL-based refactoring work (handcrafted reward features) and proposes a reasonable alternative.

2. **Ablation study (Table 2) provides meaningful evidence that each component contributes.** The degradation patterns (−7.5% SI without contrastive pre-training, −8.6% SP without semantic tests, −4.2% SI without embedding rewards) are internally consistent and of plausible magnitudes, lending support to the claim that each component plays a functional role.

3. **Cross-language transfer experiment (Table 3)** goes beyond what most prior refactoring work reports by testing whether representations learned on Java transfer to Python and C++ without fine-tuning.

## Weaknesses

### Major

1. **No variance or statistical significance reported for any experimental result.** Every number in Tables 1, 2, and 3 is a single point estimate. RL training is notoriously high-variance; without multiple random seeds and standard deviations, the reader cannot assess whether reported improvements (e.g., 83.7% vs. 79.4% SI) are robust or within the noise floor. This is a basic methodological expectation for any empirical ML paper. The paper does not even mention how many runs were performed.

2. **GS (Generalization Score) is inadequately defined, making a headline result uninterpretable.** The paper defines GS as "Performance on unseen project types (cross-validation)" (Section 5.1) but does not specify what metric is being reported (SI? SP? a composite?), how "project types" are defined, or what the cross-validation split consists of. Since GS is the primary metric distinguishing the method from baselines in Table 1 (72.4% vs. 67.2% for the next best), this ambiguity is a serious gap.

3. **Cross-language "generalization" compares against linters, not refactoring tools.** In Table 3, the Python comparison is against PyLint and the C++ comparison against Cppcheck — both are static analysis linters that detect style violations and some bugs but do not modify code. The paper acknowledges this only indirectly by calling them "language-specific rule-based tools." Comparing a refactoring method against tools that cannot perform refactoring does not provide a meaningful baseline for evaluating refactoring quality. The appropriate comparison would be against actual refactoring tools (e.g., Rope for Python, clang-tidy for C++) or LLM-based approaches.

4. **The evaluation omits LLM-based baselines that are the de facto standard for code transformation by 2026.** The baseline set (PMD, Checkstyle, Code2Seq, Graph2Edit, RLRefactor, GraphRL, NeuroRefactor) does not include any LLM-based approach (prompt-based or fine-tuned). Without this comparison, the claim of state-of-the-art performance is weakly supported — the reported improvements may simply be against weak baselines.

### Minor

1. **The SP (Semantic Preservation) metric lacks coverage reporting.** The metric depends on test cases generated via symbolic execution (Section 4.5). The paper does not report how many test cases were generated per method, what statement/branch coverage they achieved, or what fraction of code paths were exercised. Symbolic execution tools like KLEE produce partial test suites for real-world code (path explosion, loop handling, external libraries). Without coverage statistics, a 93.8% pass rate is uninterpretable — it could reflect shallow tests rather than genuine semantic preservation.

2. **Data augmentation details are under-specified.** The three augmentations (subtree masking, edge rewiring, identifier shuffling) are described at a high level. The paper does not specify the augmentation distribution, how frequently each is applied, or what "maintaining program validity" means concretely for subtree masking. This makes the method difficult to reproduce.

3. **Ablation study is conducted on only one dataset (Refactory).** Table 2 reports ablation results only on the Java Refactory dataset. It is unclear whether the ablation patterns (e.g., the importance of contrastive pre-training) generalize across datasets with different languages (CodeRef/Python) or characteristics (BigCloneBench).

4. **No hyperparameter sensitivity analysis.** Reward weights (w_q = [0.4, 0.3, 0.3], α = 0.2, β = 1.0, γ = 0.5) are given as fixed values. A brief sensitivity study would substantially increase confidence that the method is not brittle to these choices.

### Trivial

1. **Qualitative analysis (Section 5.5) describes case studies at a high level without showing before/after code.** Showing actual code examples would significantly strengthen the reader's intuition about what the method produces.

## Nice-to-Haves

- A controlled experiment disentangling whether the embedding-dynamics reward (α tanh(β Δh_t)) genuinely drives refactoring quality or simply amplifies the magnitude of any change.
- Failure case analysis: what kinds of refactorings does the method get wrong? Does it ever break semantics despite the differential testing guard?
- Reporting of total GPU-hours for a full training run to enable comparison with alternative approaches.
- Code release, given the under-specified methodology details.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run all experiments with at least 5 random seeds and report means ± standard deviations.** This is the single most important improvement.
2. **Clarify the GS definition:** specify what metric is being measured, how "project types" are defined, and the cross-validation methodology.
3. **Replace linter "baselines" in the cross-language experiment** with actual refactoring tools or LLM-based approaches.
4. **Add at least one LLM-based baseline** (e.g., prompting an LLM to refactor, or fine-tuning CodeLlama). Even an unfavorable comparison would be informative — the paper could then reposition its contribution (e.g., as a compute-efficient alternative).
5. **Report test coverage statistics** for the symbolic execution component used in semantic preservation.
6. **Provide a hyperparameter sensitivity study** for the reward weights and scaling parameters.

## Score and Decision

**Round 1 bracket:** 3.5–5.5 (initial assessment based on comparing against retrieved anchors).

**Anchors consulted:**

| Anchor | Avg. Score | Round | Comparison |
|--------|-----------|-------|------------|
| FALCON (N18Z2MkMEa) | 3.00 | Round 1 | Also RL+code with evaluation gaps, but had more severe presentation issues; current paper has a clearer methodology but similar evaluation gaps |
| GEPCode (DgGdQo3iIR) | 4.33 | Round 1+2 | Graph-based code representation paper; had better evaluation rigor (5 seeds) but less novel core idea |
| Coarse-Tuning (vLqkCvjHRD) | 4.75 | Round 2 | RL+code generation paper with some similar evaluation concerns, got mixed reviews (3,5,6,5) |
| RefactorBench (NiNIthntx7) | 6.50 | Round 1 | Well-executed benchmark paper with thorough analysis; current paper does not match this rigor |
| LLM-Assisted Code Cleaning (maRYffiUpI) | 7.00 | Round 1 | Solid empirical paper with clear experiments and results; substantially more rigorous than current paper |

The paper's core idea is genuinely novel, but the experimental evaluation has several significant gaps (no variance reporting — particularly serious for an RL paper, misleading cross-language baseline comparison, undefined GS metric, missing LLM baselines). These gaps collectively prevent the evidence from supporting the claimed results. The paper is in the borderline reject range — interesting enough to warrant a substantially strengthened revision, but not acceptable in its current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>