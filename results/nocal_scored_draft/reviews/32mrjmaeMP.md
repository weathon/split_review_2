## Summary

This paper proposes TAK (Task Arithmetic with KFAC regularization), a method for weight disentanglement in task arithmetic. The key insight is that representation drift regularization (which normally requires access to other tasks' data) can be reformulated as a curvature matrix (GGN) approximation problem. Using Kronecker-Factored Approximate Curvature (KFAC), the authors derive a practical regularizer that operates without requiring external task data during fine-tuning. They further introduce a Kronecker factor merging heuristic that achieves O(1) complexity in the number of tasks. Experiments across vision and language benchmarks demonstrate strong performance on task addition and negation.

## Strengths

- **Clean theoretical derivation connecting representation drift to curvature (Sec. 3.1–3.2).** The identification that the Jacobian Gramian in Eq. (3) is a GGN matrix under squared-error loss is elegant and not obvious a priori. This connection is the paper's core intellectual move and is executed clearly.

- **Genuine practical advantage: data-free during fine-tuning.** Unlike τJp (Yoshida et al., 2025), which requires loading other tasks' data during fine-tuning of each new task vector, TAK pre-computes KFAC factors once and shares the factors — not the data. This is a meaningful improvement for modular, privacy-constrained, or decentralized settings.

- **The O(1) Kronecker factor merging heuristic (Eq. 8) is practically valuable.** Without it, per-task KFAC factors incur O(T) memory and runtime, limiting scalability. Table 3 validates the gap between the merged and un-merged formulations is ≤0.8 percentage points.

- **Strong task negation results (Table 2).** TAK achieves lower target-task accuracy (better forgetting) than τJp while maintaining competitive control-task accuracy — and does so without requiring external data. This is arguably the paper's most striking empirical result.

- **Thorough efficiency and robustness analysis.** The paper examines KFAC estimation quality (Fig. 7a), compression strategies (Fig. 7b), training overhead (Fig. 6), and sensitivity to regularization frequency (Fig. 8) — more comprehensive than many comparable papers.

## Weaknesses

### Fatal
None.

### Major

- **No variance or uncertainty reported for any main result.** All tables (1, 2, 3) report point estimates without standard deviations, confidence intervals, or number of seeds. The paper claims advantages of 0.2–0.5 percentage points over τJp in Table 1 — without error bars it is impossible to determine whether these differences are meaningful or within noise. The paper acknowledges variance increasing with MC samples (line 318) but never reports variance for its core claims. This is the most significant evidential weakness.

- **The regularization strength β (Eq. 7) is completely unexamined in the main paper.** β is introduced at line 143 but the paper never states its value, whether it was tuned, or how sensitive results are to it. This contrasts with the extensive analysis of α-robustness (Fig. 4). If β was tuned per experiment, the dataless advantage is partially undercut by needing validation data to tune β. If β was fixed, this should be stated with supporting evidence.

### Minor

- **The Kronecker factor merging heuristic (Eq. 8) lacks theoretical characterization.** The approximation ∑ λ_t B_t ⊗ A_t ≈ (∑ B_t) ⊗ (∑ λ_t A_t) is not generally correct — Kronecker products do not distribute over sums. The paper calls it a heuristic (line 151) and validates it empirically (Table 3), which is acceptable, but provides no analysis of when it is accurate, when it might break down, or why the B and A matrices are treated asymmetrically (B unweighted, A weighted by λ_t). This limits understanding of the method's general applicability.

- **The "dataless" framing in the abstract and contributions slightly overstates the case.** The KFAC factors A^l and B^l are pre-computed from data (acknowledged at line 83: "after initial pre-computation"), so the method is not literally dataless — it is data-free during fine-tuning. The paper would be more precise by qualifying "dataless" (e.g., "data-free during fine-tuning") in the abstract and key claims.

- **Language results are notably weaker than vision results, and this caveat is absent from the abstract's "state-of-the-art" claim.** On T5-base task addition (lines 206–215), τJp achieves 81.3/100 vs TAK's 78.7/98.9 — a 2.6 pp gap, much larger than in vision. The paper acknowledges this (line 231) but the abstract and introduction do not qualify the SOTA claim with this limitation.

### Trivial
None.

## Nice-to-Haves

- Provide diagnostics (e.g., Frobenius-norm error between the true sum and the merged approximation on actual data) to characterize when the Kronecker merging heuristic is reliable.
- Specify the KFAC variant (Exact vs. MC, and M value) used for main experiments in the table captions.

## Removed Points

These points are flagged to be removed; treat them with caution.
- "KFAC variant not specified in main tables" — The paper labels MC=1 as "ours" in Fig. 6b and states "With a single Monte Carlo sample" for the overhead analysis (line 302), implying MC=1 is the default. This may be further clarified in the appendix (stripped by parser).
- Section-by-section observations (e.g., "line 189: reasonably acknowledges limitation") — These are observations, not actionable weaknesses.
- Suggestion about PEFT extension — Outside the paper's stated scope.
- Comment about MC performance deterioration being "concerning" — This is the paper's own finding (line 318), not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add error bars or standard deviations to Tables 1–3; if multiple seeds were run, report the statistics and number of runs.
2. State β's value, tuning procedure, and include a β-sweep analogous to the α-sweep in Fig. 4.
3. Replace "dataless" with "data-free during fine-tuning" or add a footnote clarifying the pre-computation step in the abstract.
4. Qualify the "state-of-the-art" claim in the abstract to reflect the language task-addition results.

## Score and Decision

This paper makes a solid contribution: the theoretical connection between representation drift regularization and curvature approximation is clean and well-executed, and TAK offers a genuine practical advantage by removing the need for external task data during fine-tuning. The experiments are broad and the efficiency analysis is thorough. However, the paper has two significant evidential weaknesses — the complete absence of variance reporting despite sub-1% performance comparisons, and the unexamined regularization strength β — that prevent the empirical claims from being fully evaluated at their stated precision. These issues are addressable but currently weaken the paper. On balance, the core contribution is sound and the practical value is clear.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>