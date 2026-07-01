Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper introduces a large-scale Bitcoin transaction dataset (1.15B transactions, 163M CoinJoin) and a semi-supervised learning pipeline for detecting illicit flows in Shared Send Mixers. The central thesis is that **data quality matters more than data quantity** when applying SSL to blockchain forensics — operationalized by comparing high-fidelity features (KeyLinker address clustering, SSU complexity metrics) against a noisy heuristic (OTC). The dataset and the finding that OTC features consistently harm performance are useful contributions. However, the paper's headline claim that SSL "outperforms" supervised baselines is not supported by its own results, and several experimental details are underspecified.

## Strengths

1. **Large-scale, carefully assembled dataset.** The paper integrates on-chain data with labels from WalletExplorer, Elliptic++, MBAL, and Kaggle to produce a dataset of 163M CoinJoin transactions with SSU complexity classification and 4.6M labeled instances. This is a substantial resource for blockchain forensics (Table 1, Section 5.1).

2. **The OTC feature ablation is clearly useful.** Across both supervised and SSL settings, adding OTC features consistently degrades or fails to improve F1, precision, and recall relative to feature sets without OTC (Tables 2–3, Sections 6.2–6.3). This is a practically actionable finding for practitioners choosing clustering heuristics.

3. **Explicit, falsifiable thesis about data quality.** The paper's core research question — whether feature quality matters more than pseudo-label volume in SSL for blockchain forensics — is well-motivated, and the feature-ablation design is the right experimental framework to test it (Section 5.2).

## Weaknesses

### Fatal

None.

### Major

1. **The claim that SSL "outperforms" supervised learning is contradicted by the paper's own evidence.** The abstract states: "We demonstrate that a semi-supervised learning framework outperforms supervised baselines." The introduction reiterates this. But the actual results show the best supervised XGBoost achieves F1 = 0.845 (Section 6.2, line 250) and the best SSL XGBoost also achieves F1 = 0.845 (Table 3, line 315). These are identical. The paper itself acknowledges "the semi-supervised phase did not produce dramatic metric gains" (Section 6.3, line 293). The SSL results show a precision-recall tradeoff (recall up +0.03, precision down −0.04 to −0.05), not an improvement. This structural disconnect between framing and evidence is **the paper's most significant weakness**. The core findings about OTC harming performance and quality features helping are independent of this claim and remain valid, but the paper should either produce evidence of SSL improvement or revise its central claim.

2. **The tables are partially uninterpretable for verifying the reported results.** In both Table 2 and Table 3, multiple rows for the same model show identical feature checkmarks (e.g., all five features ✓) but report different metric values. For example, XGBoost in Table 2 has three rows with ✓✓✓✓✓ yielding F1 = 0.821, 0.842, and 0.840 (lines 272–274). CatBoost in Table 3 has four such rows (lines 306–309). The paper does not explain what distinguishes these rows (different hyperparameters? different folds? different subsets within feature groups?). Further, the text claims the best supervised result is "default+reuse+cs+ssu" (no OTC), but no row in Table 2 shows that exact combination — every row with SSU also has OTC checked. This mismatch between the textual claim and the tabular presentation makes it impossible for a reader to independently verify the reported best result.

### Minor

3. **The SSL pseudo-labeling procedure is underspecified.** The paper states that "the top fraction of samples on both sides of the decision boundary" is retained (Section 5.3, line 228), but never reports: (a) how many pseudo-labels were added, (b) what fraction of the unlabeled pool this represents, or (c) what fraction was selected on each side. Without these numbers, the reader cannot assess whether the pseudo-labeling introduced meaningful new information or was a trivial expansion. Given that the labeled training set already contains 4.6M CoinJoin transactions, the scale of pseudo-labeling relative to the existing labeled data is a critical experimental parameter.

4. **KeyLinker is cited as prior work but listed as a novel contribution.** The paper lists "novel, high-fidelity features — KeyLinker address clustering" as Contribution #2 (Section 1, line 28), but KeyLinker is cited to Smolenkova & Yanovich (2025), an external prior work. The paper provides no algorithmic description of how KeyLinker works beyond "cryptographic key reuse patterns" (Section 5.1, line 199). If KeyLinker is not novel to this paper, it should not be claimed as a contribution; if it is novel in some respect, that novelty is not explained. The paper also does not isolate KeyLinker's effect in an ablation (e.g., comparing clustering with vs. without KeyLinker), so its contribution cannot be separately evaluated.

5. **No statistical significance or variance is reported.** All metrics are point estimates. Given that the differences discussed are small (F1 differences of 0.01–0.03), standard deviations across the 5 CV folds or significance tests are needed to distinguish signal from noise. This is especially relevant for the SSL vs. supervised comparison, where the claim of "outperformance" rests on differences that may be within the noise range.

6. **No error analysis stratified by SSU complexity class.** The paper has SSU labels (simple, separable, ambiguous, time-limit, regular) for all CoinJoin transactions but does not report whether model errors concentrate in specific SSU classes. Since the "data quality" thesis predicts that high-quality features help most on cleaner transaction types, this analysis would directly support the paper's central argument.

7. **No baseline comparison against other SSL methods.** The paper frames itself as an SSL contribution but only compares SSL results against its own supervised variants. Comparison with other SSL approaches (e.g., self-training without quality filtering, co-training, or consistency regularization) would contextualize the claimed improvement and clarify whether the quality-aware design is responsible for any observed stability.

### Trivial

None.

## Nice-to-Haves

- **A direct quality-filtering ablation.** The strongest test of the data-quality thesis would compare SSL with quality-filtered pseudo-labels (e.g., by SSU complexity class or KeyLinker cluster confidence) vs. SSL with unfiltered pseudo-labels, rather than conflating quality-filtering with feature selection.
- **Label noise estimation.** The paper acknowledges that off-chain labels "may introduce inaccuracies" (Section 2, line 23) but does not quantify this noise. An estimate of ground-truth label noise would help bound the metrics and strengthen the reproducibility argument.
- **Report pseudo-label accuracy against held-out ground truth.** The paper asserts that pseudo-labels from KeyLinker and SSU-simple transactions are high-quality but does not measure their accuracy against known labels, which would directly validate the quality principle.

## Removed Points

These points were raised in the input review but are removed or substantially weakened after cross-checking against the paper:

- **"Fundamental logical circularity" of SSL**: Removed. Self-training/pseudo-labeling is a standard SSL method, not logically circular. The critic's claim that "there is no mechanism by which this should improve performance" is incorrect — self-training can provide regularization and expand the effective training distribution even with large labeled sets. The underlying concern (large labeled set may limit SSL gains) is retained in Weakness #3.
- **"Comparison unfair" speculation**: Removed — the baselines are the paper's own supervised variants; no asymmetric favoring of the proposed method is evident.
- **Abstract phrasing of "SSL effectively leverages unlabeled data (F1-score: 0.84)"**: The abstract's (3) does *not* claim outperformance in that sentence. Only the introduction and the first sentence of the abstract do. This nuance does not remove the overclaiming problem but is noted for accuracy.
- **Reproducibility nitpicks about hyperparameters**: Removed per instructions — cross-validation for hyperparameter selection is described, and full training logs are impractical to include.
- **"Class distribution should be explicitly stated"**: Partially addressed — the paper states "illicit transactions constitute only about 12% of the labeled dataset" (Section 5.3, line 220), which is consistent with Table 1's 33.2K illicit vs. 251.1K legal addresses (~11.7%). The remaining gap is minor.
- **Strengths that conflict with verified weaknesses**: The critic listed "the ablation shows OTC harms performance" as a strength — this is genuine and retained. The critic's "clear, falsifiable thesis" strength is retained. The "scale of dataset" strength is retained.

## Novel Insights

The reviews surface one insight that goes beyond the paper's own framing: the SSL component is effectively a null result that the paper tries to frame as a positive finding. The data-quality thesis would be better tested by an experiment that directly filters pseudo-labels by quality (e.g., SSU class or cluster confidence) rather than indirectly through feature selection. The paper's current design confounds feature quality with pseudo-label quality, so the observed stability across SSL settings could equally be explained by the pseudo-labels being redundant with the already-large labeled set (4.6M examples), regardless of their quality. A cleaner experiment would hold features constant and vary only the pseudo-label filtering criterion.

## Suggestions

1. **Revise the central claim.** Remove or substantially weaken the claim that SSL "outperforms" supervised baselines. The paper's strongest and best-supported finding is that OTC features harm performance regardless of learning paradigm — this is independently interesting and does not require an SSL improvement claim.
2. **Clarify the tables.** Annotate rows with identical feature checkmarks to indicate what differs (hyperparameter configuration, CV fold, etc.). Add a row in Table 2 for Default+REUSE+CS+SSU (no OTC) to match the textual claim.
3. **Report pseudo-labeling statistics.** Add the number of pseudo-labels retained, their fraction of the unlabeled pool, and the per-class breakdown.
4. **Add error bars.** Report standard deviations or confidence intervals from 5-fold CV, especially for the key comparisons (supervised vs. SSL, OTC vs. no-OTC feature sets).
5. **Stratify errors by SSU class.** Show whether the "quality" features specifically reduce errors on the cleaner SSU classes (Simple, Separable) compared to the noisier ones (Ambiguous, Time-Limit).

## Score and Decision

**Score: 5.0**

The paper has two genuine contributions: a large-scale dataset of CoinJoin transactions with SSU classification, and a clear experimental demonstration that OTC features harm performance. However, the paper's central framing claim — that SSL outperforms supervised learning — is not supported by its own evidence (identical F1 scores). The experimental presentation has significant clarity issues (uninterpretable table rows, mismatch between text and table, missing pseudo-labeling details). The KeyLinker contribution is claimed as novel but cited as prior work without explanation. These issues are addressable through reframing and additional exposition, but in its current form the paper overstates its results relative to what the evidence supports.

**Decision: Reject**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>