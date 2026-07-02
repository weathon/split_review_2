Now let me write the final consolidated review.

## Summary
This paper introduces a nonlinear multimodal encoding model for naturalistic speech fMRI. Using PCA for dimensionality reduction and a single-hidden-layer MLP, it maps audio (Whisper) and semantic (LLaMA) features to brain activity, achieving improvements over linear baselines. The authors then use the model for spatiotemporal clustering (RED) and variance partitioning to probe cortical organization, finding patterns consistent with neurolinguistic theories.

## Strengths

1. **Clean ablative architecture (Section 2.4, Table 1).** The paper does not merely compare Linear vs. MLP. It constructs MLLinear (same architecture as MLP but with identity activation) to isolate nonlinearity from dimensionality reduction, and DIMLP (separate modality pathways with linear fusion) to isolate cross-modal nonlinear interactions from within-modality nonlinearity. This directly addresses the core question: "Nonlinearity or multimodality—or both?"

2. **First demonstration of nonlinear multimodal encoding for naturalistic continuous speech.** Prior nonlinear work in language fMRI used isolated words or unimodal features (Section 1, paragraph 4). The paper correctly identifies this gap. The method itself is architecturally simple (PCA + single-hidden-layer MLP), which is a strength for a first demonstration in a domain where overfitting is a known concern.

3. **Public dataset and reproducible baselines.** The paper uses the LeBel et al. (2023) public dataset and re-implements the Antonello et al. (2024) baseline (same ridge regression, same feature extraction pipeline). This enables direct verification and extension.

4. **RED metric for spatiotemporal analysis (Section 2.5).** The Relative Error Difference preserves the temporal dimension (f(v,t) rather than f(v)), enabling joint spatiotemporal clustering that standard connectivity measures cannot capture. A practically useful addition for the speech fMRI community.

## Weaknesses

### Major

1. **Unverifiable headline improvement percentages (Abstract, Discussion).** The abstract claims "a 7.7% and 14.4% improvement over prior state-of-the-art models relying on weighted averaging of linear unimodal predictions." The Discussion (line 208) repeats "a 14.4% increase in mean normalized correlation compared to previous state-of-the-art models (Antonello et al., 2024)." However, these percentages cannot be verified from Table 1. The best multimodal model in Table 1 that approximates the prior SOTA is the text+audio Linear (all voxels) at 31.36% CC_norm. The MLP multimodal achieves 34.32% CC_norm, giving a relative improvement of (34.32−31.36)/31.36 = **9.4%**, not 14.4%. For r², (4.29−4.10)/4.10 = **4.6%**, not 7.7%. If the "prior SOTA" refers to a different configuration (e.g., the weighted averaging ensemble from Antonello et al., 2024, which is not replicated in Table 1), the paper must state this explicitly and show those numbers alongside the replications. As written, a reader comparing the abstract to Table 1 finds a discrepancy that undermines trust in the central quantitative claim. **This does not invalidate the overall finding** (nonlinear multimodal > linear multimodal is clear from Table 1), but it is a transparency issue that must be resolved.

2. **Ambiguous PCA fitting procedure (Section 2.3).** The paper states (line 52): "PCA was applied to the aggregate response matrix Y_org ∈ ℝ^{N_TR × N_voxels} to obtain Y_PCA." The term "aggregate" is ambiguous: it could mean the full dataset (training + test) or only the training set. If PCA was fit on the full dataset, the 512-dimensional target representation is shaped by test-set response structure, constituting a form of leakage. While the dimensionality reduction is mild (512 from ~80k) and the practice is not uncommon in fMRI encoding, the paper does not acknowledge or discuss this. The authors should state explicitly whether PCA was fit on training data only or on the full dataset, and if the latter, explain why this does not compromise evaluation validity.

### Minor

3. **"Unusually large improvements" framing is unsupported in the main text (Abstract, Section 3).** The paper repeatedly characterizes the gains as "unusually large for fMRI speech encoding" (Abstract, line 28) and "substantially exceed[ing] the incremental advances typically reported" (Section 3, line 98), deferring to Appendix N.2 for justification. In absolute terms, the best model explains 4.29% r², and the gain over the best comparable linear model in Table 1 is 0.19 pp r² (4.6% relative) or 2.96 pp CC_norm (9.4% relative). Whether this is "unusually large" depends on the field's year-over-year improvement distribution, which is not presented in the main text. The claim should be tempered or supported with field benchmarks in the main paper.

4. **No hyperparameter details in the main text (Section 2.4).** The MLP is described as having "a single hidden layer of 256 units" trained via "Optuna," but no learning rate, optimizer, batch size, number of epochs, regularization strength, or search space is reported. For a nonlinear method where overfitting is an acknowledged concern (Section 4), these details are essential for reproducibility. (If this information is in the appendix, it should be summarized in the main text.)

5. **RED-based clustering modularity differences are small and untested (Section 3.1.2, Figure 1).** The modularity values cited are Q=0.155 (nonlinear), 0.145 (linear), 0.068 (FC). The difference of 0.01 between nonlinear and linear RED clustering is small, and no statistical test or confidence interval is reported. The paper treats this as strong evidence ("superior functional grouping"), but the quantitative basis for this claim is thin.

6. **Some neurolinguistic interpretations exceed what the correlational evidence supports (Section 3.3.2).** The paper maps findings onto the dual-stream model, Motor Theory of Speech Perception, Convergence-Divergence Zone model, and embodied semantics, claiming the results "extend" these theories. The evidence is correlational (the encoding model attributes variance to modalities, and this aligns with known functional anatomy). The paper acknowledges this limitation in one case (line 190: "our current design cannot distinguish between these explanations") but not for the other theoretical alignments. The claims should be uniformly caveated.

7. **No variance estimates in Table 1.** The main results table reports point estimates without error bars, confidence intervals, or significance tests (deferred to Appendix C). Given the small absolute differences between models (e.g., 4.10% vs. 4.18% vs. 4.29% r²), variance information would help readers assess the reliability of the rankings.

### Trivial

None.

## Nice-to-Haves

- The MLLinear (PCA) model matching the Linear (all voxels) model at exactly 4.10% r² with far fewer parameters (5.64M vs. 1.72B) is an interesting observation that the paper does not comment on.
- Subject-level results could be more visible in the main text, rather than mostly relegated to appendices.
- A statistical test (e.g., permutation test) for the modularity difference between nonlinear and linear RED clustering would strengthen the claim.

## Removed Points

- The reviewer's specific calculation that 14.4% → 9.4% and 7.7% → 4.6% (comparing to multimodal Linear all-voxels) is noted, but this assumes a particular prior SOTA model. The "weighted averaging" model from Antonello et al. (2024) may differ from the concatenation model in Table 1. The broader transparency criticism is retained as Major; the specific arithmetic is correct only under one set of assumptions about which model is the reference.
- "No analysis of per-subject variability beyond a brief mention" — moved to Nice-to-Haves as it is not a core flaw.
- "The 'first' claim is narrowly scoped" — this is an accurate characterization of the contribution's scope, not a weakness.
- "Missing appendix content" — parser issue; the original submission contains these sections.

## Novel Insights
The reviewer correctly identifies that the paper's strongest evidence comes from its ablative architecture: MLLinear isolates dimensionality-reduction effects, DIMLP isolates within-modality nonlinearity from cross-modal nonlinearity. This design cleanly decomposes the question and is the paper's most impactful methodological contribution, regardless of the absolute encoding performance. The numerical transparency issue and PCA ambiguity are concrete fixable problems rather than structural flaws.

## Suggestions

1. In Table 1 or a companion table, explicitly state the published performance numbers from Antonello et al. (2024) for the "prior SOTA weighted averaging" model(s), and show the percentage improvements relative to those numbers alongside the improvements relative to the re-implemented baselines. This would resolve the abstract-to-table discrepancy.
2. Add a sentence in Section 2.3 clarifying whether PCA was fit on training data only or on the full dataset, with a brief justification of the chosen practice.
3. Add error bars or confidence intervals to Table 1, or move a variance-inclusive version of the table to the main text.
4. Temper the "unusually large improvements" language or include a brief quantitative benchmark of typical year-over-year gains in speech fMRI encoding.
5. Report key hyperparameters (learning rate, optimizer, batch size, regularization, training epochs) in the main text or a main-text table.
6. Add statistical testing (e.g., permutation test) for the modularity difference between nonlinear and linear RED clustering.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>