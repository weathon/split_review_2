Now let me write the final consolidated review.

## Summary

This paper proposes Aligned Scoring Rules (ASR), a method for optimizing proper scoring rules for textual elicitation to align with human preference scores (e.g., instructor review scores). The key technical contribution is a convex optimization over the space of separate (weighted-average) scoring rules, minimizing MSE between the scoring rule's output and a reference score while maintaining properness. The approach builds on the Wu & Hartline (2024) framework for textual elicitation via LLM oracles.

## Strengths

- **Clear identification of a genuine gap.** The paper correctly identifies that prior work on proper textual scoring (Wu & Hartline, 2024) achieves properness but does not address alignment with human preferences. The framing in Section 1 (lines 23–29) is precise about what is being added.

- **Convex formulation.** The paper shows that optimizing the MSE objective over the space of separate scoring rules (weighted averages of single-dimensional proper rules) yields a convex optimization problem (Corollary 3.4, Section 3.2). This is a genuine technical property — the max-over-separate alternative does not share it — and it means the optimization is efficient with convergence guarantees.

- **Interpretability from the separate structure.** Because each single-dimensional scoring rule is convex in its parameters, the learned weights \(w_i\) indicate which rubric dimensions the reference score values (Section 3.2, lines 231–233). This is a real advantage over black-box alignment methods.

## Weaknesses

### Major

- **No out-of-sample evaluation.** The paper evaluates MSE between ASR and the reference score on what appears to be the same data used for optimization. The paper nowhere mentions a train/test split, cross-validation, or held-out data. Since MSE against the reference score is exactly the training objective (Program 1, line 229: \(\min \mathbf{E}[(S(\mathbf{r},\theta)-s)^2]\)), the reported MSE and correlation values in Table 1 and Figure 4 are essentially measures of optimization success, not generalization. The dataset description (lines 304–305) gives 22 assignments with 6–8 submissions each; the per-assignment sample sizes are modest. Without out-of-sample evaluation, the central empirical claim that ASR "outperforms previous methods in aligning with human preference" is unsubstantiated. This is the most critical gap in the paper.

- **Baselines do not isolate the effect of optimization from hypothesis space richness.** EGPT(AV) and EGPT(MV) use V-shaped scoring rules, which are a restricted subset of the separate scoring rule family that ASR optimizes over (Definition 2.7). The observed improvements could stem entirely from the richer hypothesis space rather than from the alignment optimization itself. A proper comparison would require ablations within the same hypothesis space — e.g., a separate scoring rule with uniform weights, or one with randomly initialized parameters — to isolate the effect of the optimization. As presented, Table 1 shows that optimizing in a richer hypothesis space beats a fixed functional form, which is a much weaker claim than "ASR aligns with human preference."

- **Assumption 2.2 (Know-it-or-not) is a strong restriction that is not adequately justified.** The assumption restricts the agent's posterior to \(\{0, 1, p_i\}\) — either certainty or the prior. The paper justifies this (lines 110–111) by observing that textual reports in the dataset "either express a state being 0 or 1, or have no information." This conflates a dataset property (observed reporting patterns) with a model of agent behavior (the space of possible posterior beliefs an agent could form after receiving a signal). A mechanism-design assumption about what beliefs agents can form requires a different kind of justification than a dataset statistic. This assumption limits the generality of the properness guarantee, and the paper does not discuss how violations would affect results.

### Minor

- **No variance or statistical significance reporting.** Table 1 reports point estimates with no standard deviations, confidence intervals, or significance tests. The dataset has only 22 assignments with variable sizes (6–8 submissions each); per-assignment sample sizes for optimization are small (roughly 36–64 data points each). Without variance estimates, the reader cannot assess whether the reported improvements over baselines are reliable or driven by a few assignments.

- **The non-inverting condition of the QA oracle is not empirically verified.** Theorem 3.2's properness guarantee depends on the QA oracle having error probability strictly less than 1/2 (Definition 3.1). The paper provides no empirical check of this condition (e.g., QA accuracy on a labeled subset). This leaves a gap between the theoretical guarantee and the actual implementation.

### Trivial

None.

## Nice-to-Haves

- **Behavioral or outcome evaluation.** The paper frames ASR as a mechanism for eliciting truthful, high-quality textual reports, but the evaluation only measures correlation with reference scores. A behavioral study testing whether agents actually produce more truthful reports under ASR, or an evaluation of whether ASR leads to instructor-preferred review rankings, would substantially strengthen the applied claims. The absence of such evidence is understandable given the paper's scope but limits what can be concluded about "alignment."

- **Per-assignment results.** Aggregating across 22 assignments obscures per-assignment variation. Reporting per-assignment MSE and correlation (with variance across assignments) would be more informative than the aggregate numbers in Table 1.

## Removed Points

- **Convexity concern about boundedness constraint in Program 2.** The harsh critic worried that the boundedness constraint \(\sum_i S_i(r_i,\theta_i) \in [0,1]\) "could make the optimization non-convex across dimensions." This is factually incorrect — the constraint is linear in the optimization variables, and linear constraints preserve convexity. The paper's convexity argument is sufficient.

- **Behavioral evaluation missing (as a Critical Issue).** The request for a full behavioral experiment testing agent response to ASR goes beyond the paper's stated scope. The paper's contribution is designing a proper scoring rule aligned with reference scores; a behavioral study is a natural next step but not a requirement for the current paper. Demoted to Nice-to-Have.

- **"Maintaining properness" phrasing concern in the abstract.** The phrase is technically accurate (the optimization is constrained to the space of proper scoring rules, so properness is guaranteed by construction). Trivial.

- **Footnote 3 about Spearman correlation.** The paper explains its methodological choice clearly. The harsh critic's concern about "limited comparability" is speculative and the paper's rationale is sound. Removed.

- **Various formatting nitpicks and presentation suggestions** that are parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a train/test split or cross-validation evaluation.** Report MSE and correlation on held-out data (either held-out assignments or held-out reviews within each assignment). Without this, the central empirical claim is unsubstantiated.

2. **Add ablations within the separate scoring rule family.** Compare against a separate scoring rule with uniform weights, or with randomly initialized parameters not optimized for alignment. This would isolate the effect of the alignment optimization from the expressivity of the hypothesis space.

3. **Verify the non-inverting condition empirically** by measuring QA oracle accuracy on a labeled subset of reviews, or at least discuss the plausibility of this condition given the LLM used.

4. **Report per-assignment results with variance across assignments** and statistical significance tests for the comparison against baselines.

## Score and Decision

### Calibration Anchors Used

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| EW62GvCzP9 — Truthfulness Without Supervision (peer prediction) | 4.67 | R1 | Yes | Most topically similar anchor. Both papers apply mechanism design to text/LM evaluation. That paper had stronger empirical breadth but also significant weaknesses in its assumptions and evaluation. The reviewed paper has a cleaner theoretical contribution but weaker empirical evaluation. |
| ga4LyaucKr — Learning-based Mechanism Design (PFM-Net) | 2.50 | R1 | Yes | About automated mechanism design with neural nets. Much lower quality — poorly motivated contributions and weak experiments. The reviewed paper is significantly stronger in clarity and theoretical grounding. |
| tiiAzqi6Ol — Compositional Preference Models | 5.75 | R1 | Yes | About decomposing preference into interpretable features for LLM alignment. Stronger empirical validation across multiple dimensions. The reviewed paper's theoretical framing is cleaner, but CPM has much more convincing experiments. |
| EVZnnhtMNX — CVX-DPO (convex optimization for alignment) | 3.00 | R2 | Yes | Uses convex reformulation for alignment. Poorly explained, weak contributions, unclear evaluation. The reviewed paper is substantially better in clarity and theoretical soundness. |

### Bracket and Final Score

**Round 1 bracket:** 3.5–5.5. The paper's theoretical contribution (convex optimization formulation for aligned proper scoring) is genuinely novel and cleanly presented, placing it well above the 1–3 range (strong rejects). However, the empirical evaluation is significantly incomplete — no out-of-sample testing, no variance estimates, baselines that don't isolate the claimed contribution — which prevents it from reaching the 5.5+ range where papers typically have convincing empirical support for their applied claims.

**Round 2 narrowing:** The most topically comparable anchor (EW62GvCzP9, 4.67) had a similar profile: a theoretically grounded mechanism-design paper with empirical gaps. That paper's most negative weakness items had favorability around -0.85; the reviewed paper's most negative item (no out-of-sample eval) has favorability -2.50, indicating a more severe empirical gap. Compared to EVZnnhtMNX (3.00), the reviewed paper is much clearer and better-motivated. The CVX-DPO paper's weaknesses were more severe (favorability down to -3.43) and included fundamental presentation/explanation issues that the reviewed paper does not share.

**Final score: 4.0.** The paper makes a genuine theoretical contribution (convex optimization over separate scoring rules for alignment), and the problem framing is clear and well-motivated. However, the empirical evaluation is insufficient: the central applied claim requires out-of-sample testing that is not provided, the baselines do not control for hypothesis space richness, and no variance estimates are reported. The paper would be significantly strengthened by addressing these empirical gaps; as it stands, the contribution is primarily theoretical and the applied claims are not adequately supported.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>