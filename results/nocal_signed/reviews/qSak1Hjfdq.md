Now I have all signals needed to produce the final review. Let me compile it.

## Summary

This paper formalizes the All-Day Multi-Scenes Lifelong VLN (AML-VLN) problem and proposes Tucker Adaptation (TuKA), a parameter-efficient fine-tuning method that uses 4th-order Tucker decomposition to decouple multi-hierarchical navigation knowledge (scene-specific and environment-specific) from shared core skills. The tensor-matrix alignment mechanism reduces the high-order representation to 2D for LLM backbone integration. The resulting agent, AllDayWalker, achieves substantially higher success rates (65% avg. SR) and lower forgetting rates (11% F-SR) than LoRA-based baselines (best baseline: 44% SR, 36% F-SR) across 24 navigation scenarios spanning simulation and real-world environments.

## Strengths

- **Well-motivated limitation analysis.** The paper correctly identifies that LoRA's two-matrix structure can represent at most two knowledge hierarchies (shared + task-specific), while multi-scene VLN involves at least three levels (core navigation, scene-specific, environment-specific). This provides clear motivation for the tensor approach. (Section 3.1, Figure 3)

- **Tucker decomposition is conceptually clean and well-matched.** Mapping scene expertise to factor matrix U³ and environment expertise to U⁴, with the core tensor G capturing interactions, is a natural fit. The tensor-matrix alignment trick (selecting rows from U³ and U⁴ to produce a 2D weight matrix for the LLM backbone) solves the dimensionality mismatch elegantly. (Section 3.2, Equation 3)

- **Large and consistent empirical gains.** AllDayWalker achieves 65% average SR vs. 44% for the best LoRA baseline (BranchLoRA) and 11% forgetting rate vs. 36% — gaps large enough that even accounting for evaluation details, a real effect is clearly present. Results are consistent across SR, SPL, OSR, and their forgetting-rate counterparts across all 24 tasks. (Tables 1, 2)

- **Physically grounded benchmark extension.** The AllDay-Habitat platform uses well-established imaging models (atmospheric scattering, CRF-based low-light and overexposure) to synthesize degraded environments, enabling reproducible evaluation across diverse visual conditions. (Section 4)

- **Ablations directly test the core claim.** The third-order vs. fourth-order tensor comparison (Figure 8) and the shared-component ablation (Table 3) isolate the contribution of the decoupled hierarchical representation, supporting the paper's central thesis.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **FSTTA and FeedTTA are test-time adaptation methods, not lifelong learning baselines.** The paper acknowledges this ("which aim to perform small, temporary adaptation during test time") but lists them alongside lifelong learning methods in the main comparison tables without clear separation. Their expected poor performance on a 24-task sequential benchmark does not inform the reader about AllDayWalker's relative quality. These should either be removed from the main comparison or placed into a clearly separate category with appropriate caveats. (Section 5.2, Tables 1-2)

- **Forgetting rate definition leaves ambiguity for tasks 21–24.** Equation (13) defines M-SR_t as "performance obtained when training solely on navigation tasks 1 through t" and constrains this to t ≤ 20, yet F-SR values are reported for all 24 tasks. It is unclear how M-SR_t is computed for tasks 21–24. Additionally, the negative F-SR values for T14 (-3%) and T20 (-4%) indicate positive backward transfer (final performance exceeding M-SR_t), which is noteworthy but requires explanation given M-SR_t is described as an upper bound. (Equation 13, line 227, Table 2)

- **Navigation loss weighting lacks sensitivity analysis.** The navigation objective is weighted at λ = 0.5 (since λ₁+λ₂+λ₃ = 0.2+0.2+0.1 = 0.5), meaning half the training signal comes from regularization. The generalization results (Table 5) suggest genuine transfer is occurring, but the paper does not analyze sensitivity to these coefficients or show training loss dynamics. A sweep over λ values or convergence curves would strengthen the case. (Equation 9, lines 147-149, 181)

- **Trainable parameter counts not directly reported.** The paper states parameters are "kept comparable" but does not report actual counts. For a typical LLM hidden dimension (e.g., 4096), TuKA has roughly 328K params/layer (core tensor 8×8×64×64 + U¹ + U² + U³ + U⁴), while rank-6 LoRA has ~49K and MoE-LoRA (r=16, K=8) has ~590K. Since TuKA outperforms MoE baselines with fewer parameters, reporting exact counts would strengthen the paper's claims. (Section 5.2, line 181)

### Trivial
None.

## Nice-to-Haves

- An ablation that removes or degrades the CLIP-based expert retrieval (e.g., averaging experts or using random selection) would isolate the contribution of the tensor structure from the task-identification mechanism.
- Reporting training loss trajectories would help confirm that the 50% regularization weight is not impeding new task learning.
- The paper notes M=7, N=4 (28 possible combinations) but only 24 tasks; this is implicitly explained by real-world scenes having only 2 environments each (5×4 + 2×2 = 24), but stating it explicitly would improve clarity.

## Removed Points (filtered from inputs)

- **Structural unfairness claim (comparison asymmetry):** Removed. The critic argued AllDayWalker's retrieval mechanism gives an unfair advantage over non-MoE baselines. Non-MoE baselines (Seq-FT, LwF-LoRA, EWC-LoRA) use single adapters and inherently do not require task identification — the comparison is apples-to-apples. MoE baselines (BranchLoRA, HydraLoRA) have their own routing mechanisms. The retrieval is based on visual features, not an oracle task-id, so it does not violate the task-agnostic testing condition.
- **Table 1 missing values (EWC-LoRA, O-LoRA, SD-LoRA, FeedTTA):** Removed as likely parser/formatted-extraction artifacts — the rules state these are parser issues, not author errors.
- **Speculative retrieval failure cases:** Removed — the critic's concern about ambiguous first-observation matching in low-light conditions is not supported by evidence in the paper.
- **General formatting and appendix-content nitpicks:** Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The reviews correctly identify that the tensor-matrix alignment mechanism is the paper's genuine technical novelty, and the large empirical margins suggest a substantive effect. The main takeaway from the review process is the need for more precise documentation of the forgetting-rate protocol and for ablations that disentangle the retrieval mechanism from the tensor decomposition itself.

## Suggestions

1. Clarify how M-SR_t is computed for tasks 21-24 and explain the negative F-SR values (positive backward transfer).
2. Add a brief sensitivity analysis showing how varying λ₁, λ₂, λ₃ affects overall performance.
3. Move FSTTA/FeedTTA to a separate supplementary comparison category or clearly label them as TTA baselines outside the main lifelong learning comparison.
4. Report actual trainable parameter counts per layer for TuKA and all baselines.

**MY FINAL SCORE: <score>9.0</score>**
**MY FINAL DECISION: <decision>Accept</decision>**