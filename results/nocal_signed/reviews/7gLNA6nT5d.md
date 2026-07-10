Now let me put together the final review.

## Summary

This paper applies n-gram attention layers (from Akyürek et al., 2024) to in-context reinforcement learning (ICRL), specifically Algorithm Distillation. The authors show that injecting hardcoded n-gram induction heads into the transformer improves data efficiency and reduces hyperparameter sensitivity in Dark Room, Key-to-Door, and Miniworld environments. For visual observations, they use Vector Quantization (VQ) to enable n-gram matching over images. The evaluation uses Expected Maximum Performance (EMP) across random hyperparameter searches, and includes a negative control demonstrating that broken n-gram masking does not harm performance.

## Strengths

- **The evaluation protocol using EMP is principled and well-controlled.** By reporting expected performance across a random hyperparameter search rather than cherry-picking the best run, the paper avoids a common failure mode in RL papers. It controls for data volume (same batch size, same 10K gradient steps) across methods, making the comparison fair.

- **The VQ-based adaptation for visual observations is a reasonable engineering contribution.** N-gram matching in continuous pixel space is non-trivial, and the quantization approach (Section 2.3) provides a workable solution that yields positive results on Miniworld environments.

- **The paper includes a negative control (Section 4.5, Table 1c).** Shuffling the n-gram attention matrix to simulate a broken n-gram head and showing performance similar to baseline is a good sanity check — it demonstrates that the n-gram layer does not harm performance even when its matching mechanism is incorrect.

## Weaknesses

### Fatal
None.

### Major

- **The paper lacks mechanistic analysis of what the n-gram patterns capture in the RL setting, which limits the contribution to a straightforward application of a known technique.** The paper tests two matching variants (full transitions vs. states only) in Figures 2 and 4 but does not analyze why they differ, what structure is being exploited (e.g., repeated state visitations, successful trajectories, task-specific patterns), or whether the model develops the predicted induction-head behavior. Without this analysis, the paper reads as "we tried this known NLP technique on RL data and it helped" rather than building understanding of inductive biases in ICRL. This is the paper's most significant limitation for a venue like ICLR, where the bar for contribution requires more than an empirical application of prior work.

- **The "27x less data" claim is not substantiated in the main text and rests on an imprecise comparison.** The paper states (lines 45, 129, 179) that the method needs "27x less data" than the baseline. The computation is deferred entirely to Appendix B (stripped). The main-text comparison contrasts the method at 100 goals against the baseline's reported requirement of 2048 goals from prior work (Laskin et al., 2022), rather than a controlled matched-performance comparison within the same experimental setup. The paper shows that the n-gram method works in a low-data regime where the baseline fails — this is a legitimate and useful finding — but the precise "27x" figure implies a more rigorous matched-performance comparison than is actually presented.

### Minor

- **The main EMP curves (Figures 2, 4, 5) lack uncertainty quantification.** They are plotted as single lines without confidence intervals, error bars, or shaded regions (only Figure 6 includes these). Given that hyperparameter search is inherently stochastic and the claims rest on comparing the rate of improvement across methods, the absence of uncertainty makes it difficult to assess whether the observed differences are statistically reliable.

- **The VQ-based approach for visual observations is validated on only one environment family (Miniworld).** The 4×4 index encoding from 64×64 images is very coarse, and the strict exact-match criterion (all 16 indices must match) limits applicability. The paper briefly acknowledges this limitation in the conclusion but does not test on a more diverse image-based environment.

- **The paper does not experimentally compare against alternative ICRL efficiency methods mentioned in the related work,** such as data augmentation (Kirsch et al., 2023), retrieval-augmented transformers (Schmied et al., 2024), or noise curriculum (Zisman et al., 2023). While the model-centric approach is a different direction, the absence of any experimental comparison makes it difficult to contextualize the contribution's significance relative to existing alternatives.

### Trivial
None.

## Nice-to-Haves

- Mechanistic analysis visualizing which n-gram patterns are captured (e.g., do n-grams match repeated state visitations, successful trajectories, or task structure?). This single addition would most strengthen the paper.
- Clarify the 27x data-reduction computation in the main text with a detailed breakdown rather than deferring entirely to the appendix.

## Removed Points

These points are flagged to be removed, treat them with caution:
- Criticism about "transitivity" typo (lines 71/227) — removed (parser artifact, not author error).
- Criticism about missing hyperparameter search space (deferred to Appendix C) — removed (appendix stripped by parser; the paper explicitly states the details are in the appendix).
- Criticism that Figure 6 uses asymmetric data budgets (50 vs 60 goals) — removed (asymmetry favors the baseline, which gets more data; per rules, such criticisms are removed when asymmetry favors the baseline).
- Criticism that EMP values in Table 1 (0.67–0.76) are low compared to Figure 5 optimum (~0.96) — removed (confuses EMP, an aggregate metric across hyperparameter search, with optimal return from a specific run; these are different quantities).

## Novel Insights

None beyond the paper's own contributions. The reviews surface no insight not already present in the paper.

## Suggestions

1. Add a mechanistic analysis section: visualize attention patterns, analyze which n-gram types are captured, and compare when each matching variant is preferable.
2. Provide uncertainty quantification (confidence intervals or multiple-seed runs) for all EMP curves.
3. Clarify the 27x claim by providing the full computation in the main text and/or showing a controlled matched-performance comparison at multiple data budgets.
4. Validate the VQ-based approach on at least one additional image-based environment beyond Miniworld.
5. Include experimental comparison to at least one alternative ICRL efficiency method to contextualize the contribution.

**MY FINAL SCORE: <score>5.0</score>**
**MY FINAL DECISION: <decision>Reject</decision>**