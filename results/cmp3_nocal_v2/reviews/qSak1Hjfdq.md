Now I have all the information needed to produce the final consolidated review.

## Summary

This paper formalizes the all-day multi-scenes lifelong vision-and-language navigation (AML-VLN) problem and proposes Tucker Adaptation (TuKA), which represents multi-hierarchical navigation knowledge (skills × scenes × environments) as a 4th-order tensor using Tucker decomposition. The core technical contribution is decoupling scene-specific and environment-specific knowledge into separate factor matrices with a shared core tensor, plus a Decoupled Knowledge Incremental Learning (DKIL) strategy for continual learning. The resulting agent, AllDayWalker, is evaluated on a 24-task benchmark spanning 5 simulated and 2 real-world scenes across multiple illumination conditions, outperforming LoRA-based continual learning baselines by large margins (65% vs. 44% avg. SR).

## Strengths

- **Conceptually novel and well-motivated architecture (Sections 3.1–3.2).** The paper correctly identifies that existing MoE-LoRA adapters are limited to two hierarchical levels, while VLN agents face three or more levels (navigation skills × scene identity × environment type). Representing this as a 4th-order tensor with separate factor matrices for scenes and environments is a clean conceptual contribution, and the tensor-matrix alignment trick (Eq. 3) that collapses the high-order tensor to a 2D ΔW is clever engineering.

- **Strong and consistent empirical results (Tables 1–2, 5).** AllDayWalker achieves 65% average SR across 24 tasks vs. the best baseline (BranchLoRA at 44%). The average F-SR of 11% vs. BranchLoRA's 36% indicates substantially less forgetting. Generalization to unseen scene–environment combinations (Table 5: 55% vs. 35–40% for baselines) provides direct evidence that the decoupled representation transfers meaningfully.

- **The 3rd-order vs. 4th-order ablation (Section 5.3, Figure 8) directly validates the central thesis.** Showing that explicitly decoupling scene and environment into separate factor matrices outperforms collapsing them into a single expert dimension is exactly the right ablation, and it confirms that multi-hierarchical representation matters.

## Weaknesses

### Fatal
None.

### Major
- **No error bars, standard deviations, or statistical significance reported for any result (Tables 1–5).** Every reported number is a single point estimate. VLN involves stochastic action sampling, and lifelong learning results can vary with task ordering and random seeds. The absence of variance estimates makes it impossible to assess whether the observed 21-point gap between AllDayWalker (65%) and BranchLoRA (44%) is robust. This is the most significant weakness, as it affects the reliability of all headline comparisons.

### Minor
- **The forgetting baseline (M-SR) is underspecified (Equation 13, Section 5.1).** The paper defines M-SR_t as performance "when training solely on navigation tasks 1 through t" but does not specify the training schedule, compute budget, or hyperparameters for this multi-task joint training. This matters because AllDayWalker shows negative F-SR values at T14 (−3%) and T20 (−4%), meaning the lifelong model *outperforms* this "upper bound." The paper does not discuss these negative values. This could indicate genuine forward transfer (interesting) or that the M-SR baseline was trained under different conditions. Clarification is needed.

- **The "parameter-efficient" framing relative to vanilla LoRA is imprecise (abstract, contributions, conclusion).** TuKA uses ~328K parameters per layer (U¹: 4096×8, U²: 4096×8, core tensor: 8×8×64×64=262K) vs. vanilla LoRA (r=6) at ~49K per layer — roughly 6–7× more. The paper calls TuKA "parameter-efficient" without qualifying that this is relative to full fine-tuning, not to the specific LoRA baselines. (To the paper's credit, TuKA likely uses *fewer* parameters than the MoE-LoRA baselines it primarily compares against — with r=16, K=8 those use ~590K per layer — so the paper should present this comparison honestly rather than making a blanket claim.)

- **FSTTA and FeedTTA should not be in the main comparison table (Tables 1–2).** As the paper itself states, these are test-time adaptation methods designed for temporary, single-scene distribution shifts — they store no persistent knowledge across tasks. Including them in a lifelong learning benchmark inflates the apparent margin. They should be moved to a separate analysis or removed from the main tables.

- **The CLIP-based expert retrieval mechanism is not validated (Section 3.4).** The inference protocol matches the current observation's CLIP features against stored features for each scene and environment independently. No analysis of retrieval accuracy is provided (e.g., confusion matrices, ablation of the matching mechanism). Since the baselines (BranchLoRA, SD-LoRA) use learned routers, the difference in inference mechanism could be a confound in the generalization results (Table 5).

- **SD-LoRA is missing T23–T24 in Table 1**, and several baselines lack their averaged SR values. This weakens the completeness of the comparison.

### Trivial
- The paper has no limitations section, which would be appropriate given (a) synthetic degradations may not capture real-world lighting complexity, (b) the retrieval mechanism is unvalidated, and (c) the cross-product benchmark leaves some (scene, environment) pairs unfilled.
- The "real-world deployments" claim in the contributions (point 3) appears to refer to simulated reconstructions of real scenes rather than physical robot deployments; this should be clarified.
- Calling U¹ a "decoder" and U² an "encoder" (Section 3.2) suggests a semantic interpretation that the Tucker decomposition itself does not enforce — these are just factor matrices.

## Nice-to-Haves
- Analyze the expert retrieval accuracy (confusion matrices for scene and environment identification) to validate that the decoupled representation is correctly leveraged at test time.
- Analyze what the factor matrices actually learn — e.g., visualizing whether similar scenes are close in U³ space, or probing whether perturbing U³/U⁴ changes agent behavior in expected directions.
- Report the computational overhead of the EWC-based DKIL strategy (Fisher computation for 262K core parameters per layer).
- Add a 30-task comparison including baselines (currently only AllDayWalker results are shown for 30 tasks).

## Removed Points
These points are flagged to be removed; treat them with caution.
- *"O-LoRA is missing a value at T12"* — Incorrect; O-LoRA has all 24 task values filled in Table 1 (T12=38). The Avg. column is empty for several baselines, which is a separate formatting/presentation concern.
- *"Duplicate rows in Table 3"* — Rows 3 and 6 share the same ✓✓✓ pattern but differ in OSR (69 vs. 68). Likely a parser artifact; not an author error.
- *"Negative F-SR values not discussed"* — Absorbed into the M-SR underspecification point above rather than listed separately; the core issue is the baseline definition.
- *"Limitations section missing"* — Moved to Trivial as a presentation note; not a methodological weakness.
- *Various generic speculation about "could the metric be measuring a proxy?"* — No concrete anchor in the paper text.
- *"Missing related works"* — Cannot be verified.
- *Formatting/parser nitpicks* — Removed per hard rules.
- *Criticism about the orthogonal constraint being too strong* — This is a reasonable design choice, not a demonstrated weakness; the paper empirically validates the approach.

## Novel Insights
None beyond the paper's own contributions. The review surfaces no fundamental flaw in the method or its evaluation that the authors had not already considered.

## Suggestions
1. Add variance estimates (multiple seeds/task orderings) to all main results, or at minimum acknowledge the absence and justify why single-run evaluation is sufficient for this setting.
2. Clarify the M-SR training protocol and explicitly discuss the negative F-SR values.
3. Either remove FSTTA/FeedTTA from the main tables or add a clear justification for their inclusion.
4. Replace the blanket "parameter-efficient" claim with a precise comparison table showing per-method parameter counts.
5. Add retrieval accuracy analysis for the CLIP-based expert matching.
6. Add a brief limitations section.

## Score and Decision
MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>