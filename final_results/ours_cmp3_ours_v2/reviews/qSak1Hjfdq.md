Now I have all the information needed for calibration. Let me write the final consolidated review.

## Summary

This paper formalizes the AML-VLN problem (lifelong VLN across multiple scenes and environmental conditions), proposes Tucker Adaptation (TuKA)—a fine-tuning method that uses 4th-order Tucker decomposition to decouple multi-hierarchical knowledge into shared subspaces and separate scene/environment experts—and builds the AllDayWalker agent. Experiments on a 24-task benchmark (extended to 30 tasks) spanning simulation and real-world scenes show consistent improvements over LoRA and MoE-LoRA baselines.

## Strengths

- **The AML-VLN problem formulation is well-motivated and timely.** Section 2 clearly identifies a gap: VLN agents that must operate across varying scenes *and* environmental conditions (low-light, overexposure, scattering) have no existing lifelong learning formulation that spans both dimensions simultaneously. The decomposition of navigation knowledge into scene-specific, environment-specific, and shared components (Figure 4) is intuitive and practically relevant.

- **The core idea—using a higher-order tensor (Tucker decomposition) to explicitly decouple scene and environment knowledge—is creative and principled.** Section 3.2's design of factor matrices U³ (scene experts) and U⁴ (environment experts), plus a shared core tensor G and encoder/decoder U¹/U², is a natural fit for the problem structure. This is a genuine architectural departure from LoRA and MoE-LoRA variants, which the paper correctly identifies as limited to two hierarchical levels (Section 3.1, Eq. 1).

- **The extensiveness of the evaluation is a strength.** 24 hierarchical task scenarios spanning 5 simulation scenes × 4 environments + 2 real-world scenes × 2 environments (Section 5.1), plus a 30-task extension (Table 4) and generalization to 6 unseen scenarios (Table 5), is substantially more thorough than typical VLN lifelong learning evaluations. AllDayWalker consistently outperforms all baselines on SR across nearly every task.

## Weaknesses

### Fatal
None.

### Major

1. **M-SRₜ values unreported and negative forgetting unexplained, making a key metric partially unverifiable.** The forgetting rate is defined as F-SRₜ = (M-SRₜ − SRₜ) / M-SRₜ (Eq. 13), where M-SRₜ is the multi-task joint training performance on tasks 1 through t. The paper states M-SRₜ is computed for t ≤ 20 (line 227), but the F-SR values in Table 2 span all 24 tasks with no clarification of how tasks 21–24 are handled. More critically, Table 2 shows **negative forgetting** for AllDayWalker on T14 (−3%) and T20 (−4%), indicating that lifelong sequential learning *outperforms* joint multi-task training on those tasks. This unusual result is never discussed. The M-SRₜ values themselves are not reported anywhere in the main paper, preventing readers from verifying the F-SR computations or assessing whether the multi-task baseline is reasonable. Adding a "Multi-task Joint Training" row to Table 1 and reporting the M-SRₜ values would resolve this.

2. **The "parameter-efficient" claim is unsubstantiated; no parameter counts are reported.** The paper calls TuKA "parameter-efficient" in the abstract, contributions (page 2), and conclusion, and states "To keep the number of trainable parameters comparable across comparison methods" (line 231). Yet no actual parameter counts are provided for TuKA or any baseline—not per-layer, not total. The paper gives the tensor dimensions (r₁=r₂=8, r₃=r₄=64, line 181) which, for a hidden dimension of 4096 (Qwen2-7B), imply approximately 328K parameters per layer for TuKA versus ~49K per adapted matrix for rank-6 LoRA. Whether TuKA's parameter count is competitive depends on how many layers are adapted and how shared components amortize across tasks in lifelong learning, but without explicit numbers and a clear definition of what "parameter-efficient" means in this context, the claim cannot be evaluated. The paper references Appendix C for implementation details and parameter comparisons (line 231), but the main paper must stand on its own for this central claim.

### Minor

1. **The non-overlap condition in the problem definition is ambiguous.** The condition "{Sₜ, Eₜ} ∩ (∪ⱼ₌₁ᵗ⁻¹ {Sⱼ, Eⱼ}) = ∅" (Section 2) could mean either that no exact (S,E) pair repeats (trivially satisfied) or that neither S nor E can repeat. The latter would contradict the paper's own design of reusing scene/environment experts across tasks. Clarification is needed.

2. **The CLIP-based expert retrieval mechanism (Section 3.4) is not analyzed.** During inference, the method selects scene/environment experts by cosine similarity of CLIP vision features. This introduces a failure mode (e.g., a low-light scene might be visually more similar to a different scene under normal lighting). No analysis of retrieval accuracy is provided, so it is unclear whether the reported results reflect the method's ability or the retrieval mechanism's accuracy.

3. **Real-world validation is thin despite the claim of "real-world deployments."** The benchmark includes two real-world scenes with only two environments (normal, low-light), contributing 4 of the 24 tasks. The contribution statement claims "additional real-world deployments also validate the superiority" (page 2), but the evidence is limited to evaluation on two real-world scene datasets—not actual robotic deployments. This overstates the real-world support.

4. **Task ordering sensitivity is not explored.** The paper states "the order of tasks is randomized" (Figure 6 caption) but reports results for only a single ordering. Lifelong learning results can be sensitive to task order; multiple random seeds would strengthen the conclusions.

5. **Tables 1 and 2 have formatting issues that affect readability.** SD-LoRA's row in Table 1 is missing entries for T23 and T24. O-LoRA's row lacks an Avg. column.

### Trivial

1. **Minor text inconsistency:** The benchmark description (line 179) says "two real-world scenes, each containing four environments: normal, low light"—listing two environments after stating four.

## Nice-to-Haves

- **Runtime and memory comparison:** The tensor operations in TuKA (mode products, 4D Fisher information matrices) are computationally heavier than LoRA's matrix products, but no runtime, training time, or memory footprint comparison is given. Reporting these would help assess practical deployability.
- **Second backbone experiment:** Testing TuKA with a different LLM backbone (beyond Qwen2-7B) would show generality.
- **Analysis of orthogonal constraint scaling:** As the number of scenes grows, the dimension r₃ may need to scale. A scaling analysis would clarify the method's capacity limits.

## Removed Points

The following points from the input review were removed:

- **Third-order vs. fourth-order tensor ablation as "unfairly stacked":** The ablation compares collapsing scene+environment into one dimension (3rd-order) against keeping them separate (4th-order) under the same Tucker framework. This is a clean comparison for the question asked (does explicit decoupling help?). Demanding a comparison against 28 independent LoRA experts with a learned router is a different architectural comparison, not an ablation of tensor order.
- **Orthogonal constraint scaling analysis:** The critic speculates that U³ rows may need to grow with more scenes (M). This is a reasonable question but is speculative—no evidence of capacity issues is shown in the paper. Moved to Nice-to-Haves.
- **Backbone generality request:** Asking for a second backbone is reasonable for a follow-up but is scope creep for evaluating the paper's stated contribution.
- **Various section-by-section notes** that are minor clarification questions or requests for details already referenced in the (stripped) appendix.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report the M-SRₜ values (or add a "Multi-task Joint Training" row to Table 1) and discuss the negative F-SR values observed for AllDayWalker.
2. Report parameter counts per layer and total for TuKA and all baselines, and clarify what "parameter-efficient" means in the lifelong learning context (e.g., total stored parameters across all tasks vs. per-task inference parameters).
3. Clarify the non-overlap condition (Section 2).
4. Analyze the CLIP-based retrieval accuracy (Section 3.4).
5. Tone down the "real-world deployments" claim or provide clearer evidence of actual deployment.

## Score and Decision

### Calibration

Before calibration, I first wrote a draft review and then identified relevant anchor papers from the human-review corpus. The following anchors were retrieved across all calibration rounds:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| General Scene Adaptation for VLN (GSA-VLN) | 6.40 | Bracket | Accepts a similar "new task + new method" paper; weaknesses were about scalability, missing baselines, and dataset scope—relatively minor. Our paper has more substantive evaluation gaps. |
| Constraint-Aware Zero-Shot VLN | 5.00 | Bracket | Rejected; weaknesses included incremental results and heavy engineering. Our paper has stronger method novelty but similar evaluation concerns. |
| Continual LLaVA | 4.75 | Bracket | Rejected; novelty concerns and benchmark limitations. Our paper's method is more novel. |
| Think Small, Act Big (PSPL) | 4.50 | Bracket | Rejected; unclear architecture choices. Our paper has clearer contributions. |
| Scalable Lifelong Multimodal Instruction Tuning | 6.50 | Bracket | Accepted; thorough experiments, presentation weaknesses only. Our paper has more significant evaluation gaps. |
| Task-Unaware Lifelong Robot Learning | 5.75 | Bracket | Rejected; overstated claims, insufficient lifelong learning evaluation. Our paper shares some overclaim issues. |

**Round-1 bracket:** The paper sits between 4.5 (papers with significant method-novelty concerns) and 6.4 (papers with minor evaluation issues). The paper has genuine method novelty (Tucker decomposition for multi-hierarchical knowledge) that places it above the 4.5–5.0 papers, but has evaluation gaps (unreported M-SRₜ, unsubstantiated parameter-efficiency claim) that prevent it from reaching the 6+ range.

**Narrowing:** Comparing against the GSA-VLN paper (6.40, accepted), that paper's weaknesses were about scalability, missing baselines, and dataset scope—concerns about future work or scope expansion. Our paper's weaknesses are more fundamental: a key metric is unverifiable, and a central claim is unsupported. This places our paper below 6.0. Comparing against Continual LLaVA (4.75) and Think Small Act Big (4.50) which were rejected, our method is more novel and the problem formulation is cleaner, placing us above 4.5. The Task-Unaware Lifelong Robot Learning paper (5.75, rejected) had similar issues with overstated claims and evaluation gaps, and is the closest comparison.

**Final score:** 5.0. The paper makes creative contributions to an interesting problem, but the evaluation gaps (unreported M-SRₜ values, unsubstantiated parameter-efficiency claim) are significant enough that the paper cannot be accepted in its current form. The core approach has genuine merit, and both issues appear fixable in revision.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>