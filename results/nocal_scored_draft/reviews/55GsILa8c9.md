Based on the scoring model's feedback, I can see the conditional MI gap (favorability 0.03) is extraordinarily damaging, while the empirical strengths are uniformly strong (0.80-1.00). Let me finalize the review with this calibration.

---

## Summary

This paper introduces CausalNovo, a model-agnostic framework for de novo peptide sequencing that aims to learn causal representations of mass spectra by focusing on signal fragment ions rather than spurious noise. The method uses a causality extraction module with information-theoretic objectives to disentangle causal from non-causal factors, and is demonstrated on three strong baselines (CasaNovo, AdaNovo, π-HelixNovo) across three benchmark datasets.

## Strengths

- **Well-motivated problem with direct evidence.** The vulnerability analysis (Figure 1) empirically demonstrates that three strong baselines suffer systematic performance drops when noise peaks are replaced, establishing a concrete, measurable problem that CausalNovo is designed to solve.

- **Consistent and substantial empirical gains.** Table 1 shows CausalNovo improves *all three* baseline models on *all three* datasets across amino acid, peptide, and PTM-level metrics. Gains include +12.0% amino acid precision on Seven-species (CasaNovo) and +14.2% on HC-PT (AdaNovo). The improvements are systematic, not cherry-picked.

- **Model-agnostic architecture.** CausalNovo operates as a plug-in module added to the encoder, demonstrated on three architecturally different baselines (CasaNovo, AdaNovo, π-HelixNovo). The contribution is independent of the backbone architecture.

- **Mechanistic validation.** The attention analysis (Table 7) shows that CausalNovo shifts the distribution of attended peaks: 32.87% of predictions have all three top-attended peaks as causal peaks (vs. 19.26% for baseline), directly connecting the proposed mechanism to observed outcomes.

- **Cross-species generalization.** Table 3 shows CausalNovo improves CasaNovo on all nine individual species in leave-one-out experiments on the Nine-species dataset, with average peptide precision gain of +2.6%.

## Weaknesses

### Major

- **The conditional mutual information loss does not condition on Y — a structural gap between theory and implementation.** The paper derives an independence objective $I(z_c; z_c' | C)$, substitutes $Y$ as a proxy for $C$, then approximates it with Eq. (5), which is a standard unconditional InfoNCE loss. Eq. (5) maximizes similarity between $z_c$ (original) and $z_c'$ (intervened) while pushing apart batch negatives — this is a lower bound on $I(z_c; z_c')$, not $I(z_c; z_c' | Y)$. A proper conditional estimator would need to compare within the same $Y$ class (e.g., a supervised contrastive loss). The paper never justifies why an unconditional contrastive loss recovers conditional mutual information. Two leaps are unaddressed: (a) that $Y$ is a perfect proxy for $C$, and (b) that an unconditional InfoNCE approximates $I(z_c; z_c' | Y)$. The practical approach (contrastive invariance between original and perturbed views) is reasonable and still yields empirical gains, but the paper's causal theoretical framing claims more than the loss delivers. This is a fixable framing issue but a meaningful one.

### Minor

- **Missing hyperparameters.** The replacement fraction $\alpha$ (Section 3.4.1) is mentioned but never given a value. The tolerance threshold $\gamma$ used during *training* (as opposed to evaluation) is also not specified. These parameters define the causal intervention and are needed for reproducibility.

- **Purification mechanism is underspecified.** The paper claims maximizing $I(z_s; Y)$ "can indirectly lead to the purification of $z_c$" (Section 3.3) without explaining the competition mechanism. Since $z_c$ and $z_s$ are extracted via complementary masks ($M$ and $1-M$), the logic is plausible — maximizing $I(z_s; Y)$ could pull spurious-but-predictive information into $z_s$ — but the paper does not justify why this would "purify" $z_c$ rather than simply distribute information across both representations.

- **"CausalNovo (Duo)" variant is unexplained.** It appears in the Figure 1 caption but is never defined or described in the paper text, which will confuse readers.

- **Relative Improvement (RI) metric is ambiguously defined.** The paper states RI is "the relative performance reduction of CausalNovo compared to the baseline models" (Section 4.4), but the reported values are positive (suggesting improvement, not reduction). The formula is never given and the description is at odds with how the numbers are used.

- **No statistical uncertainty reported.** No standard deviations, confidence intervals, or significance tests accompany any result. While the overall pattern across multiple baselines and datasets is persuasive, individual comparisons could be within noise. Variance estimates would strengthen the empirical claims.

- **Warm-up schedule description may be inconsistent with training duration.** The paper states 100k warm-up steps with batch size 32 and 30 epochs. Depending on the training set size, this could be close to or exceed the total number of training steps. The paper should clarify.

### Trivial

None.

## Nice-to-Haves

- A sensitivity analysis for $\alpha$ (replacement fraction) would strengthen the causal intervention justification.
- The paper could benefit from a conditional MI estimator that actually conditions on $Y$, or an honest reframing of the independence loss as an unconditional invariance objective.
- An explicit formula for RI would resolve the ambiguity.

## Removed Points

- **Table 4/5 ablation table checkmark issue:** REMOVED — The all-checkmark rendering is a PDF extraction artifact; the original almost certainly shows incremental additions as described in the text.
- **Spelling inconsistency ("CasaNovo" vs "CasaNovo"):** REMOVED — Trivial copyediting issue / parser artifact.
- **$C \perp S$ assumption criticism:** REMOVED — This is standard in SCM-based approaches, presented as a reasonable modeling assumption.
- **Warm-up "far more steps than total training" claim:** REMOVED — Not verifiable from the paper alone; weakened to a clarification question.
- **Missing related works / appendix / proofs:** REMOVED per instructions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the conditional MI gap.** Either implement a proper conditional contrastive loss that conditions on $Y$ (e.g., using same-$\mathbf{y}$ positives as in-class negatives), or reframe the independence loss honestly as $I(z_c; z_c')$ — an unconditional invariance objective — and explain why this is sufficient given the setup. The method works empirically either way; the gap is in the theoretical framing.

2. **Report missing hyperparameters.** State $\alpha$ and the training-time $\gamma$ and, if possible, include a sensitivity analysis for $\alpha$.

3. **Clarify the purification mechanism or drop the "purification" framing.** If the auxiliary $I(z_s; Y)$ objective simply provides additional supervision, say that. The word "purification" implies a specific behavior that is not demonstrated.

4. **Define RI explicitly and fix the description.**
5. **Add standard deviations or confidence intervals** to the main results tables, or at minimum clarify which differences you expect to exceed noise.
6. **Define or remove the "CausalNovo (Duo)" reference.**

## Score and Decision

The paper's empirical contribution is genuine and well-supported: consistent improvements across three baselines, three datasets, three metric families, with mechanistic evidence. The model-agnostic design is a genuine practical virtue. However, the paper overclaims its theoretical grounding — the conditional MI objective does not implement what it claims — and several details needed for reproducibility are missing. These are fixable issues that do not invalidate the core contribution but meaningfully reduce the paper's rigor in its current form.

**Score:** 7.0  
**Decision:** Accept

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>