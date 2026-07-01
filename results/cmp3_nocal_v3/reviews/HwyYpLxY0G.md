Now let me write the final consolidated review.

## Summary

This paper proposes Aligned Scoring Rules (ASR) for textual information elicitation, extending the Elicitation<sup>GPT</sup> framework (Wu & Hartline, 2024) to optimize proper scoring rules for alignment with human/instructor preferences. The method restricts the hypothesis space to *separate scoring rules* (convex combinations of single-dimensional rules under the "know-it-or-not" assumption), yielding a convex optimization problem with six variables per rubric dimension. Experiments on peer grading data (22 assignments, ~516 reviews) show that ASR improves alignment metrics over baseline proper scoring rules.

---

## Strengths

1. **Well-motivated and clearly identified problem.** The paper recognizes a genuine gap: existing provably proper scoring rules for textual elicitation (Wu & Hartline, 2024) guarantee truthfulness but are not designed to match what humans consider a good score. The framing of optimizing a *proper* scoring rule for alignment with an external reference score (Section 3.2) is a natural and practically useful extension.

2. **Clean, tractable optimization formulation.** By restricting to *separate scoring rules* under the know-it-or-not assumption, the authors obtain a convex optimization problem with only 6 variables per rubric dimension (Corollary 3.4). This is a smart design choice — it avoids the non-convexity of alternatives (e.g., max-over-separate) while keeping the problem computationally efficient and the scoring rule interpretable via the convexity of single-dimensional scores.

---

## Weaknesses

### Fatal

None.

### Major

1. **No train/test split and no discussion of overfitting.** The paper never states whether the results in Table 1 reflect performance on training data, held-out data, or a cross-validation procedure. The paper describes optimization "with the gradient descent algorithm over samples" (Section 3.2) and defines the constant baseline using "training data D" (Section 5.3) but never clarifies the evaluation protocol. With ~516 reviews across 22 assignments, and 6m variables per assignment (where m, the number of summary points, could plausibly be 5–15), the model has sufficient capacity to overfit reference scores. Without any separation between training and evaluation, the reported MSE and correlation values cannot be interpreted as evidence of generalization. **This is the most consequential gap in the paper — it renders the core empirical claims uninterpretable.**

2. **No variance or uncertainty reporting.** All results in Table 1 are point estimates with no standard errors, confidence intervals, or significance tests. With 22 assignments of varying difficulty and an unknown number of summary points per assignment, variance across assignments could be substantial. The wide range across methods (MSE 1.73–18.36 for the instructor-score task) suggests high variance. Without error bars, the reader cannot assess whether ASR's advantage over baselines is robust or driven by a few assignments.

### Minor

1. **No empirical verification that the learned ASR is proper.** The paper claims ASR "maintains properness" (Abstract, Section 1) but provides only a theoretical guarantee conditional on two unverified assumptions: (a) that the QA oracle (Gemini-2.5) is non-inverting on the report side (Definition 3.1, Theorem 3.2), and (b) that the gradient-descent solver satisfies the properness constraints (Definition 2.5) to numerical precision. Neither assumption is checked empirically — e.g., by measuring the QA oracle's inversion rate or by verifying the learned scoring rule's inequality constraints on synthetic inputs. Since properness is the paper's distinguishing feature over direct LLM-as-Judge scoring, this gap weakens the central claim.

2. **Same model family for LLM-Judge and language oracles.** The paper uses Gemini-2.5 for both the reference LLM-Judge score and the language oracles (summarization and QA). This creates a self-consistency concern: the strong alignment on the LLM-Judge task could partly reflect the model scoring its own outputs consistently, rather than genuine alignment with the underlying construct. The paper partially mitigates this by testing GPT-4.1 as the LLM-Judge (Appendix B, referenced in Section 5.3), but the primary evaluation still uses the same model family for both roles. Using a different model family or human judgments for the reference would be a cleaner test.

3. **No conclusion or discussion section.** The paper ends abruptly after presenting Table 1, with no discussion of limitations, failure modes (e.g., when summary points are poorly clustered or the know-it-or-not assumption is violated), or connections back to the broader mechanism design literature. This is a significant structural gap that leaves the reader without guidance on how to interpret or contextualize the results.

4. **Oracle pipeline not validated.** The summarization oracle involves a multi-stage pipeline (summarize → create opposite pairs → cluster) with multiple LLM calls, and the QA oracle is a single LLM call. Neither pipeline is validated beyond the final aggregate results — e.g., no analysis of what fraction of summary points are meaningful, no QA accuracy measurement on a labeled subset. Confidence in the pipeline would be strengthened by such validation.

### Trivial

- Optimization hyperparameters (learning rate, number of iterations, batch size, initialization, termination criteria) are not specified, making exact reproduction difficult.
- The MSE training objective minimizes squared error, while evaluation uses Pearson and Spearman correlations — a brief acknowledgment of this mismatch would be helpful.
- The paper states optimization is "over samples" (Section 3.2, line 256) but does not clarify whether this is stochastic or full-batch gradient descent.

---

## Nice-to-Haves

- **Quantify the cost of properness.** Fitting an unconstrained scoring rule (same form, no properness constraints) to the reference scores and comparing its alignment to ASR's would directly measure how much alignment is sacrificed for properness. If the gap is small, the properness constraint is essentially free; if large, the paper has identified a meaningful trade-off. Either outcome strengthens the contribution.
- **Validate the know-it-or-not assumption.** The paper states that "textual reports either express a state being 0 or 1, or have no information" (Section 2.2), but does not report the distribution of report types across the dataset. A brief empirical check would strengthen the motivation for this modeling choice.
- **Analyze learned scoring rule weights.** The paper claims interpretability via convexity of single-dimensional scores and mentions a case demonstration in the appendix. A quantitative analysis of which rubric dimensions receive high/low weights and whether these align with human intuition would substantially strengthen the interpretability claim.

---

## Removed Points

These points were removed from the input review; treat with caution:

- **"Section 3.1 exposition ambiguity (O_A perfect vs. non-inverting)"** — Removed. The paper draws a clear distinction between the ground-truth side (Assumption: O_A is perfect) and the report side (Condition: O_A is non-inverting) at lines 211–217. These are different conditions applying to different uses of the oracle, not an inconsistency.
- **"Weak baseline comparison"** — Removed as stated. The baselines (Constant, EGPT-AV, EGPT-MV) are the existing truthful scoring rules from the prior literature; comparing against them is the natural evaluation for a method that claims to improve alignment while maintaining properness. The critic's call for unconstrained scoring rules is a valid nice-to-have (moved above) but not a flaw in the current comparison.
- **"Empirical improvement over baselines is large in magnitude" (as a strength)** — While the numerical differences are indeed large, this strength directly conflicts with the verified major weakness that the evaluation protocol (train/test split) is undisclosed. Retained only as context in the summary, not as a standalone strength.
- **Criticisms about missing appendix content** — Removed per hard rules. The appendix is stripped by the parser; the original submission contains it.
- **"Dataset is small" as a standalone weakness** — Removed. 22 assignments with ~516 reviews is modest but adequate for a proof-of-concept. The issue is properly about evaluation protocol, not dataset size per se.

---

## Novel Insights

The input reviews do not surface any genuinely novel insight beyond the paper's own contributions. The key observations — that the convex optimization is well-designed, that the empirical evaluation has critical gaps, and that the properness guarantee lacks empirical backing — are all faithful readings of the paper rather than cross-cutting epistemic insights.

---

## Suggestions

1. **Clarify the evaluation protocol.** The single highest-leverage improvement is to state explicitly whether the results in Table 1 are on training data, held-out data, or cross-validated. If only in-sample results are reported, re-run with a proper train/test split (e.g., held-out assignments or leave-one-assignment-out cross-validation) and report both in-sample and out-of-sample numbers.
2. **Report standard errors.** Add confidence intervals or standard errors to Table 1, computed across assignments (e.g., bootstrap the per-assignment MSE).
3. **Verify properness empirically.** Report the numerical values of the properness inequalities (Definition 2.5) for the learned scoring rule to demonstrate that the constraints are satisfied. Additionally, measure the inversion rate of the QA oracle on a random subset of reports.
4. **Add a discussion/conclusion section** that acknowledges limitations (know-it-or-not assumption, oracle error rates, generalizability across domains) and discusses how the results connect back to the mechanism design literature.
5. **Use a different model for the reference LLM-Judge** in the main evaluation (or, better, use human judgments for at least a subset) to rule out self-consistency confounds.

---

## Score and Decision

The paper addresses a well-motivated problem with a clean, theoretically grounded formulation. The method itself is sensible and the convex optimization is well-designed. However, the current empirical evaluation is insufficient to support the paper's claims. The lack of any train/test split or overfitting discussion means the results in Table 1 cannot be interpreted as evidence of generalization. The absence of variance/uncertainty reporting further weakens the empirical contribution. These are fixable issues — they require additional experimental discipline, not a different method — and a revised version with proper evaluation would be a stronger submission. In its current form, the evidence is not sufficient for acceptance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>