## Summary

This paper formalizes the All-Day Multi-Scenes Lifelong VLN (AML-VLN) problem, where agents must continually adapt across diverse scenes and environmental conditions (normal, low-light, scattering, overexposure) without forgetting. The authors propose Tucker Adaptation (TuKA), which represents multi-hierarchical navigation knowledge as a fourth-order tensor and uses Tucker decomposition to decouple it into shared components (core tensor, encoder, decoder) and separate scene/environment expert factor matrices. A Decoupled Knowledge Incremental Learning (DKIL) strategy with EWC-based consolidation and expert consistency constraints is used for lifelong learning. The resulting agent, AllDayWalker, is evaluated on a 24-task benchmark spanning simulated and real-world scenes, showing consistent improvements over LoRA-based baselines.

## Strengths

1. **Well-motivated problem formulation.** The AML-VLN setting captures a realistic gap: VLN agents in practice must handle both scene diversity and environmental degradation (low-light, scattering, overexposure) simultaneously while avoiding catastrophic forgetting. The formal definition (Section 2) cleanly separates the scene set *S* and environment set *E*, giving the problem a natural multi-hierarchical structure that maps directly onto practical deployment constraints.

2. **Clean technical solution matching the problem structure.** Representing multi-hierarchical knowledge as a fourth-order tensor (a<sub>l</sub> × b<sub>l</sub> × M × N) and applying Tucker decomposition to decouple it into a shared core tensor (G), shared encoder-decoder (U¹, U²), scene experts (U³), and environment experts (U⁴) is a natural architectural fit. The dimensional alignment trick (Equation 3) that selects a single row from U³ and U⁴ to produce a 2D weight matrix compatible with LLM backbones is both simple and elegant.

3. **Strong and consistent empirical results.** AllDayWalker achieves 65% average SR vs. 44% for BranchLoRA (the best non-TuKA baseline) in Table 1. Forgetting rates (Table 2) are dramatically lower (11% average F-SR vs. 36% for BranchLoRA). Generalization experiments (Table 5) show a 15–16 point SR advantage on completely unseen scene–environment combinations. These margins are large and consistent across metrics (SR, SPL, OSR).

4. **Principled ablation on tensor order** (Section 5.3, Figure 8). The comparison between third-order (collapsing scene and environment into one dimension) and fourth-order (keeping them separate) tensors directly tests the paper's central claim. The fourth-order variant consistently outperforms the third-order variant across all 20 tasks, providing direct evidence that decoupling the two hierarchical dimensions is beneficial.

## Weaknesses

### Fatal
None.

### Major

1. **Forgetting rate metric has a coherence problem.** Equation (13) defines F-SR<sub>t</sub> = (M-SR<sub>t</sub> − SR<sub>t</sub>) / M-SR<sub>t</sub>, where M-SR<sub>t</sub> is the performance when training solely on tasks 1 through *t*. The paper explicitly states M-SR is only computed for t ≤ 20 (line 227). However, Table 2 reports F-SR values for T21–T24 without explaining how M-SR is extended beyond t=20. Additionally, AllDayWalker shows *negative* F-SR values at T14 (−3%) and T20 (−4%), implying the model performs better on these tasks after further training — which is unusual for a forgetting metric and is not discussed. These issues do not affect the primary SR comparison (Table 1) but undermine the secondary forgetting analysis that supports the paper's claims about decoupled incremental learning.

### Minor

2. **"Real-world deployments" claim is overstated.** The contribution list (Section 1) states that "additional real-world deployments also validate the superiority of our AllDayWalker." However, the paper only describes simulated environments in the Habitat platform using scanned real-world scene *data*. There is no description of physical robot hardware, real sensor data from physical navigation episodes, or any actual hardware deployment. The "real-world scenes" in the benchmark are simulated reconstructions of real spaces. This language should be calibrated to match what was actually done.

3. **DKIL hyperparameter sensitivity is unexplored.** The training objective (Equation 9) combines a navigation loss with EWC consolidation (λ₁=0.2), expert consistency (λ₂=0.2), expert orthogonalization (λ₃=0.1), and an EMA coefficient ω=0.95. (Note: the navigation loss weight λ is deterministically set to 1−λ₁−λ₂−λ₃.) No sensitivity analysis or ablation on these coefficients is provided, making it difficult to assess robustness to hyperparameter choice.

4. **Shared component ablation (Table 3) has a duplicate/ambiguous row.** Rows 3 and 6 both have all three components (G, U¹, U²) shared, with nearly identical results except OSR differs by 1 point (69 vs. 68). Either these rows are duplicates by mistake or there is an undocumented difference; the paper should clarify.

### Trivial

5. **FeedTTA reference missing year.** Cited as "(Kim et al.)" with no publication year (line 231).

## Nice-to-Haves

- Provide an analysis of learned expert matrices (e.g., cosine similarity between U³ rows and between U⁴ rows) to offer direct evidence for the decoupled representation claim.
- Measure how each component (core tensor G, scene experts U³, environment experts U⁴) changes during sequential learning to visualize whether the core tensor stabilizes while expert rows absorb new information.
- Report training time and GPU memory costs relative to baselines.

## Removed Points

These points were raised in the input review but are removed for the following reasons:

- **Parameter-count fairness not verifiable (Critic's Issue 1):** REMOVED per the missing appendix rule — the paper states parameter comparison details are in Appendix C, which is stripped by the parser.
- **O-LoRA row ends at T17:** REMOVED — factually incorrect. O-LoRA has values for all 24 tasks in Table 1 (line 205 confirms 24 entries).
- **Sd- notation "not clearly defined":** REMOVED — the paper explicitly defines it in the text (line 257).
- **SD-LoRA truncation / missing Avg. values claimed to "undermine the quantitative comparison":** REMOVED — these are likely parser formatting artifacts; the column structure cannot be reliably verified from the parser output.
- **Miscellaneous section-by-section speculative criticisms** (Fisher overhead, benchmark size, task-id assumptions): REMOVED as speculation or scope-creep not grounded in specific paper errors.

## Novel Insights

None beyond the paper's own contributions. The reviews converge on the paper's stated contributions and raise mostly presentation-level concerns rather than uncovering fundamental issues.

## Suggestions

1. Clarify how F-SR values for tasks 21–24 are computed given the t ≤ 20 scope of M-SR, and explain the negative forgetting rates.
2. Calibrate the "real-world deployments" language to match the simulator-based evaluation.
3. Add a brief hyperparameter sensitivity study (varying λ₁, λ₂, λ₃ over a reasonable range) to demonstrate robustness of the main results.
4. Fix the duplicate/ambiguous rows in Table 3 and add the missing publication year for FeedTTA.

**MY FINAL SCORE:** <score>7</score>  
**MY FINAL DECISION:** <decision>Accept</decision>