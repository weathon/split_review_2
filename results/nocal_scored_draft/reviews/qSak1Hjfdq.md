Now I have all the information needed to write the final consolidated review.

## Summary

This paper formalizes the All-Day Multi-Scenes Lifelong VLN (AML-VLN) problem and proposes Tucker Adaptation (TuKA), a parameter-efficient fine-tuning method that represents multi-hierarchical navigation knowledge (shared core, scene-specific, environment-specific) as a 4th-order tensor decomposed via Tucker decomposition. The authors further introduce a Decoupled Knowledge Incremental Learning (DKIL) strategy and build a lifelong VLN agent (AllDayWalker). Results on a 24-task benchmark show substantial gains over baselines (65% vs. 44% Avg SR; 11% vs. 18% forgetting rate), with particularly strong generalization to unseen scene-environment combinations (55% vs. 39–40%).

## Strengths

- **Problem formulation addresses a genuine practical gap** — real VLN deployments face diverse illumination/weather conditions, and prior work has largely ignored the lifelong learning dimension across both scene and environment shifts simultaneously. The AML-VLN problem is well-motivated and scoped.

- **The Tucker decomposition framing for decoupled adaptation is elegant and principled.** Representing multi-hierarchical knowledge as a 4th-order tensor (shared core tensor G, encoder/decoder U¹/U², scene expert rows U³, environment expert rows U⁴) and aligning it to the LLM's 2D weight space via Tucker decomposition (Equations 2–3) is a clean mathematical formulation. This is more natural than concatenating task-specific LoRA modules.

- **Strong comparative results with large performance gaps.** AlldayWalker achieves 65% Avg SR vs. next-best 44% (BranchLoRA) in Table 1, 11% F-SR vs. 18% (SD-LoRA) in Table 2, and 55% vs. 39–40% generalization SR on unseen scene-environment combinations in Table 5. These gaps are substantial and consistent across multiple metrics (SR, SPL, OSR).

- **Generalization to unseen scene-environment combinations (Table 5) is a convincing test** of the decoupled representation. Showing that the method transfers to novel (scene, environment) pairs not seen during training provides stronger evidence than performance on training tasks alone.

## Weaknesses

### Fatal
None.

### Major

- **No variance or statistical significance reported anywhere.** Every result in Tables 1, 2, 3, 4, 5 is a single number with no standard deviations, error bars, or confidence intervals. Given the 64-point spread across tasks for AlldayWalker itself (T2: 23% SR vs. T7: 87% SR), single-run results could be affected by training stochasticity or task ordering. The paper's central comparative claim rests on these numerical gaps, and without variance the reader cannot fully assess whether improvements exceed run-to-run noise. This is the single most important issue to address.

- **Table 1 has genuinely missing data points.** SD-LoRA has only 22 of 24 task values (T23 and T24 missing, plus Avg). EWC-LoRA is missing T24 and Avg. Several other baselines (Seq-FT, Lwf-LoRA, O-LoRA, FeedTTA) have complete task-by-task data but the Avg column is empty. While task-level values can be inspected for most methods, the omissions for SD-LoRA and EWC-LoRA hamper direct comparison.

### Minor

- **The third-order vs. fourth-order tensor ablation (Figure 8) conflates a structural modeling choice with tensor order.** The 3rd-order version (ℝ^{a×b×(M×N)}) assigns one expert row per task, producing a flat task-expert representation. The 4th-order version (ℝ^{a×b×M×N}) factorizes into separate scene and environment expert matrices, enabling parameter sharing. The performance gap is well explained by this factorization (exploiting known structure) rather than by "higher tensor order" per se. The paper should reframe this ablation to correctly attribute the improvement.

- **Figure 7 radar charts list baselines ("BaseModel", "Recall", "Task2Vec", "CLIP") that do not match any methods in Table 1.** The appendix reference provides some recourse, but the mismatch makes the charts uninterpretable from the main paper alone.

- **The comparison with FSTTA and FeedTTA (test-time adaptation methods) lacks clarity on adaptation protocol.** The paper identifies these as TTA methods, but does not clarify how they were adapted to the sequential training setting, leaving the fairness of this comparison unclear.

- **No hyperparameter sensitivity analysis.** Four λ coefficients (λ₁=0.2, λ₂=0.2, λ₃=0.1, λ=0.5), ω=0.95, and asymmetric rank sizes (r₁=r₂=8, r₃=r₄=64) are set without ablation.

- **Results use a single fixed task ordering** with no sensitivity analysis or justification of representativeness.

### Trivial

- **Table 3 contains a near-duplicate row:** rows 3 and 6 both show ✓✓✓ with nearly identical metrics (OSR differs by 1 between 69 and 68), suggesting a formatting error.

## Nice-to-Haves

- Ablation of individual DKIL components (EWC, expert consistency, orthogonal constraint) to show which contributes most.
- Explicit parameter counts for all methods to verify comparable training budgets.
- A limitations section covering: reliance on CLIP feature similarity for expert retrieval, assumptions about which factors are hierarchical, and the synthetic nature of degraded environments.

## Novel Insights

The most useful insight from the reviews concerns the third-order vs. fourth-order tensor ablation: the paper frames this as a test of "tensor order," but the actual mechanism driving the improvement is the structural factorization into separate scene and environment expert matrices, which enables compositional parameter sharing. A 3rd-order tensor with one row per task cannot exploit the scene×environment compositional structure. This reframing would strengthen the paper without weakening the result — the factorized design is clearly the correct choice for this problem. A secondary insight: the paper's "high-dimensional space representation" framing somewhat overstates the novelty, since the Tucker decomposition is by design a dimensional reduction tool that produces a 2D weight matrix; acknowledging this more directly would be more persuasive.

## Suggestions

1. **Report means and standard deviations over at least 3–5 random seeds (or different task orderings) for all main results (Tables 1, 2, 5).** This is the single highest-leverage improvement and is standard practice for comparative claims.
2. Fill in the missing Avg values and missing T23/T24 for SD-LoRA in Table 1. If SD-LoRA did not converge on those tasks, state that explicitly.
3. Reframe the third-order vs. fourth-order ablation to clarify it compares factorized vs. flat expert representations, not tensor order per se.
4. Clarify the adaptation protocol for FSTTA and FeedTTA in the lifelong setting, or present them in a separate table.
5. Add hyperparameter sensitivity analysis for at least λ₁, λ₂, λ₃ and rank sizes.
6. Provide multiple task orderings or justify the chosen ordering.
7. Add explicit per-method parameter counts.

## Score and Decision

Based on the strengths and weaknesses weighted by their severity: the paper proposes a well-motivated problem and an elegant method (strengths all scored 1.00 favorability), with large performance gaps over baselines, but the lack of variance reporting (0.00 favorability) is a significant evidential gap that keeps the paper from being fully convincing. The missing data in Table 1 (0.21) and several minor issues temper the overall assessment. Given that the performance gaps are substantial enough that they are unlikely to vanish with variance reporting, and the core methodological contribution is sound, the paper merits a score above "borderline accept" but below a clean "accept." A score of 7 reflects a promising paper where the core contribution is genuine but where the experimental presentation needs strengthening before the comparative claims are fully verifiable.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>