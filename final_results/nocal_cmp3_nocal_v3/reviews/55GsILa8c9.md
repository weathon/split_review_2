## Summary

This paper proposes CausalNovo, a model-agnostic framework for de novo peptide sequencing that uses causal-inspired training objectives to make sequencing models robust to noise peaks. The framework formalizes the task via a Structural Causal Model, derives independence and sufficiency principles from Reichenbach's Common Cause Principle, and operationalizes these through contrastive invariance learning and information-theoretic objectives. Experiments across three benchmark datasets and three baseline architectures (CasaNovo, AdaNovo, π-HelixNovo) show consistent improvements at amino acid, peptide, and PTM levels, along with cross-species validation, NSR analysis, and attention-based interpretability checks.

## Strengths

1. **Well-motivated with empirical grounding.** Figure 1 concretely demonstrates that existing models degrade when noise peaks are replaced, and that degradation worsens as the m/z tolerance threshold tightens. This provides direct evidence of the problem before proposing a solution.

2. **Principled causal formalization that directly translates to objectives.** The SCM (Figure 2A) with variables C, S, X, Y and the two derived principles — independence (C ⟂ S) and sufficiency (Y = g(C)) — map cleanly to concrete training losses: contrastive invariance for independence and cross-entropy on causal representations for sufficiency. The theory is not decorative; it drives the design.

3. **Model-agnostic design validated across three architectures.** CausalNovo is instantiated on three different baselines (CasaNovo, AdaNovo, π-HelixNovo) and improves all of them across all three datasets (Tables 1, 2). This breadth is strong evidence that the framework captures something general rather than exploiting a quirk of a single architecture.

4. **Thorough and multi-angle evaluation.** Beyond standard metrics, the paper includes: cross-species leave-one-out validation (Table 3), component ablation (Tables 4, 5), analysis across Noise Signal Ratios (Figure 4), attention analysis of whether the model actually focuses on causal peaks (Table 7), and robustness to different ion-type definitions (Table 6). The evidence is consistently positive across all these angles.

5. **Honest about limitations.** The paper transparently acknowledges the ~2.3× training overhead and notes that its evaluation follows NovoBench rather than the more realistic large-scale out-of-distribution setup.

## Weaknesses

### Fatal

None.

### Major

1. **Confusing theoretical justification for the purification objective (maximizing I(z_s; Y)).** In Section 3.3, the paper states: "However, since z_c and z_s may share certain overlapping information about Y, optimizing I(z_c; Y) ensures that the inclusion of a partial contribution from non-causal information within z_c does not affect the optimality... However, it can reduce I(z_s; Y). To address this issue, we introduce an auxiliary objective that maximizes I(z_s; Y) which can indirectly lead to the purification of z_c." The logical chain is unclear: (a) the referent of "it" is ambiguous, (b) the mechanism by which *maximizing* I(z_s; Y) *purifies* z_c (which one would expect to happen by *minimizing* I(z_s; Y)) is not explained, and (c) the paper does not clarify why this does not simply encourage z_s to duplicate Y-relevant information rather than "purifying" z_c. The empirical ablation (Table 4) shows this component helps, so something beneficial is happening — but the theoretical exposition as presented is incoherent and needs a clear rewrite. This is the most significant weakness because it undermines the methodological narrative at a critical juncture.

### Minor

2. **Missing hyperparameter value.** The fraction α of noise peaks to replace (Section 3.4.1) is introduced but its value is never reported in Section 4.2 or anywhere else in the main text. This is a design parameter that could affect results, and its absence is an oversight.

3. **No variance or confidence intervals reported.** All results in Tables 1–7 are point estimates. Given that retrained baselines (marked †) sometimes differ substantially from originally reported numbers (e.g., CasaNovo on Nine-species goes from 0.697 to 0.741 — a 4.4% gap that rivals some claimed improvements), some measure of uncertainty across runs or seeds would substantially strengthen confidence in the results. That said, single-run evaluation is the norm in this subfield, so this is a limitation of the evaluation convention rather than of this paper alone.

### Trivial

4. **The peak-distinguishing strategy (Eq. 4) is a well-known domain heuristic.** The paper correctly cites prior works that use the same approach (Tyanova et al., 2016; Mao et al., 2023; Qiao et al., 2021). The novel contribution is the causal framework and training objectives built on top of this identification, not the identification itself. The paper is transparent about this, but the framing throughout — "causal factors," "causal representations," "causal intervention" — could give readers the impression of a stronger methodological contribution than what is delivered. A clearer early statement that the paper leverages existing domain knowledge for peak identification and focuses its novelty on the learning framework would align expectations more precisely.

## Nice-to-Haves

- The causal intervention relies on ground-truth peptide labels to identify noise peaks (Eq. 4), making it applicable only during training. A discussion of whether this limitation could be addressed (e.g., via self-supervised approaches) would be useful context.
- The "model-agnostic" claim is supported for three Transformer-based models. Testing on at least one non-Transformer architecture (e.g., a convolutional model like PepNet) would strengthen the generality claim.
- A simple baseline comparing CausalNovo against a non-causal method for focusing on signal peaks (e.g., training with a learned peak-weighting mask using standard supervised learning) would help isolate the benefit of the causal framework from the benefit of peak weighting alone.

## Removed Points

**These points appeared in the input review but are removed, treat with caution:**

- **Vulnerability argument overinterpretation.** The reviewer claimed the paper conflates "sensitivity to distribution shift" with "reliance on spurious correlations." The paper's inference — that replacing noise peaks (features that by definition have no causal link to the label) causes performance degradation, implying models rely on those non-causal peaks — is reasonable and standard. The "distribution shift" interpretation is a restatement, not a contradiction. **Removed:** criticism is not valid as written.

- **"Causal label" overclaiming.** The reviewer argued that the causal framework overclaims novelty because peak identification uses a well-known heuristic. The paper explicitly acknowledges this lineage (citing Tyanova et al., Mao et al., Qiao et al.) and clearly states the contribution is in the training framework and objectives. The framing is accurate and transparent. **Removed:** criticism contradicts the paper's own disclosures.

- **Tables 4 and 5 unreadable.** The checkmark symbols are identical across rows due to PDF parsing artifacts. This is a rendering issue, not an author error. **Removed:** parser artifact.

- **SCM gap between theory and implementation.** The reviewer noted that the SCM assumes separate latent variables C and S but they are inferred via a heuristic threshold. The paper addresses this practical limitation by operating in latent space and acknowledges the strategy's lineage. No flaw. **Removed.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the purification objective (Section 3.3).** This is the highest-priority revision. Provide a clear, non-contradictory explanation of how maximizing I(z_s; Y) contributes to purifying z_c. If the mechanism is a competitive/minimax dynamic (e.g., forcing z_c to encode invariant causal features since z_s, which is trained on Y, can capture only the non-causal Y-relevant info), state this explicitly. If the justification follows Chen et al. (2022) more closely, reference the specific mechanism.

2. **Report α and ideally some variance estimates.** State the value of α in Section 4.2 alongside other hyperparameters. Running main experiments with at least 3 seeds and reporting mean ± std for Tables 1 and 2 would substantially increase confidence.

3. **Rephrase the abstract and introduction to clarify the division of labor.** Add a sentence such as: "CausalNovo leverages existing domain knowledge (theoretical ion series) to identify likely causal peaks, and its contribution is the causal-inspired training framework that makes models robust to the remaining noise." This would preempt any perception of overclaiming.

## Score and Decision

This paper makes a genuine, empirically well-supported contribution to de novo peptide sequencing. The core idea — using causal-inspired training objectives (independence via contrastive invariance, sufficiency via cross-entropy on causal representations) to improve robustness to noise — is sound and consistently validated across extensive experiments. The main weaknesses are (a) a confused theoretical explanation for the purification objective that needs rewriting but does not invalidate the empirical results (the ablation shows it works), and (b) the absence of variance estimates and one missing hyperparameter value, both easily addressable. None of these issues threaten the paper's core claims or contributions. The evaluation is thorough, the gains are reproducible across architectures and datasets, and the honest discussion of limitations strengthens credibility.

**MY FINAL SCORE: <score>8</score>**
**MY FINAL DECISION: <decision>Accept</decision>**