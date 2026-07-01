## Summary

This paper proposes a semi-supervised learning framework for detecting illicit Bitcoin CoinJoin (Shared Send Mixer) transactions. The main contributions are a large-scale dataset of Bitcoin transactions with SSM classification, novel forensic features based on address clustering (KeyLinker) and mixing complexity (SSU), and a demonstration that semi-supervised pseudo-labeling improves detection only when guided by high-quality features rather than noisy heuristics. The work emphasizes that feature engineering for data quality is more critical than simply increasing data volume.

## Strengths

- **Relevant and timely problem**: Illicit cryptocurrency transaction detection is an important and active area, and the focus on CoinJoin transactions—which are particularly challenging to trace—adds practical value.
- **Clear articulation of the data quality principle**: The paper correctly points out that not all pseudo-labels are equally beneficial and that feature quality matters for SSL effectiveness.
- **Comprehensive feature engineering effort**: The integration of KeyLinker clustering (based on cryptographic key reuse) and SSU complexity metrics (structural untangling categories) goes beyond standard heuristics and is motivated by domain knowledge.
- **Solid supervised baselines**: The paper thoroughly evaluates XGBoost, CatBoost, and Random Forest with multiple feature sets, showing reasonable performance and clear ablation results.

## Weaknesses

### Major

- **Marginal SSL improvement over supervised learning**: The claimed advantage of semi-supervised learning is not convincingly demonstrated. In the key comparison (Table 2 vs. Table 3), the best supervised F1-score (0.845) is nearly identical to the best SSL F1-score (0.845). The paper states SSL "outperforms supervised baselines," but the evidence shows, at best, stability within noise rather than a clear gain.
- **Lack of comparison with state-of-the-art SSL methods**: The paper only compares pseudo-labeling with supervised models, but does not benchmark against other SSL techniques (e.g., self-training with consistency regularization, Mean Teacher, MixMatch, graph-based SSL). Without such comparisons, it is impossible to assess whether the proposed framework is competitive or whether simpler methods would suffice.
- **Incomplete validation of the "quality over quantity" claim**: The central hypothesis is that SSL success depends on data quality (features) rather than quantity (pseudo-label volume). However, the experiments only compare fixed feature sets and do not directly manipulate the *quality of pseudo-labeled instances* (e.g., comparing pseudo-labels only from simple transactions vs. including ambiguous ones). The claim is supported only indirectly by the observation that adding OTC features hurts performance—which is a standard feature selection result, not a proof of the data quality principle.
- **Dataset novelty and availability**: The paper claims "the first complete historical dataset" but heavily relies on existing labeled sources (WalletExplorer, Elliptic++, MBAL, Kaggle). The dataset is not yet released, so its value cannot be verified by the community. The manual resolution of label conflicts is mentioned but not described in sufficient detail for reproducibility.

### Minor

- **Vague pseudo-labeling procedure**: The paper states it selects "the top fraction of samples on both sides of the decision boundary" but does not specify the fraction, the number of pseudo-labels added, or how the threshold is chosen. This makes the SSL experiments difficult to reproduce or assess for potential data leakage.
- **No statistical significance**: All results are reported as point estimates without confidence intervals or cross-validation standard deviations. Given the very small differences between configurations, it is unclear whether observed improvements are meaningful.
- **Unexplained table entries**: Tables 2 and 3 contain rows with duplicate feature sets (e.g., seven rows for CatBoost where some seem to repeat the same checkmarks). This suggests formatting errors or redundancy that should be clarified.
- **Imbalance and label composition**: The labeled dataset contains ~12% illicit transactions, which is orders of magnitude higher than the real-world prevalence (<0.2%). This skew risks overestimating practical performance on truly rare illicit flows.

### Trivial

- The experimental setup (200 GB RAM, i9 CPU) is adequate but not noteworthy.

## Nice-to-Haves

- **Controlled experiment on pseudo-label quality**: Directly compare SSL trained on pseudo-labels filtered by SSU complexity (e.g., simple only) versus all pseudo-labels to isolate the effect of data quality.
- **Learning curves**: Show how performance changes as more pseudo-labels are added, with and without high-quality features.
- **Comparison with common SSL baselines** for tabular data, such as entropy minimization or VAT.
- **Discussion of limitations**: The paper does not address how the framework would degrade under adversarial attack (e.g., criminals mimicking mixer behaviour).

## Novel Insights

None beyond the paper's own contributions. The idea that data quality matters in SSL is well-established in the wider literature; the paper's specific insight is that for Bitcoin CoinJoin detection, feature sets like KeyLinker and SSU work better than OTC, which is a domain-specific observation but not a general methodological advance.

## Suggestions

1. **Strengthen the SSL evidence**: Either show a clear improvement over supervised models (e.g., via a statistically significant gain on a more challenging test set) or reframe the contribution as a feature engineering study rather than an SSL framework.
2. **Add SSL baselines**: Compare with at least self-training with fixed confidence threshold, consistency-based methods, or a transductive SVM to contextualize the pseudo-labeling approach.
3. **Provide detailed pseudo-labeling protocol**: Specify the confidence threshold selection, number of added instances per iteration, and whether early stopping was used.
4. **Release the dataset** prior to acceptance or provide a reproducible subset.
5. **Ablate pseudo-label quality directly**: Construct training sets with different balances of high-quality (simple/KeyLinker) vs. low-quality pseudo-labels and show that quality, not quantity, drives performance.

## Score and Decision

- **Score**: 3 – Strong Reject  
  The paper's central claim that SSL outperforms supervised learning is not supported by the experimental results (marginal gains). The lack of comparison to existing SSL methods and the incomplete validation of the data quality principle weaken the contribution below the acceptance threshold for a top venue.

MY FINAL SCORE: <score>3.0</score>  
MY FINAL DECISION: Reject