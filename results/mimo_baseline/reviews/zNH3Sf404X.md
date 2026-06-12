## Summary

This paper presents a semi-supervised learning framework for detecting illicit Bitcoin transactions within Shared Send Mixer (CoinJoin) transactions. The authors contribute a large-scale dataset of 163 million CoinJoin transactions, introduce domain-specific features (KeyLinker address clustering and SSU complexity metrics), and argue that SSL effectiveness depends on feature quality rather than data volume, with XGBoost achieving an F1-score of 0.845.

## Strengths

- **Impressive dataset scale**: The paper provides the first complete historical dataset of 163 million CoinJoin transactions with SSU complexity classifications, integrating on-chain data with off-chain labels from multiple sources. This is a substantial resource for the blockchain forensics community.
- **Well-motivated domain-specific feature engineering**: The KeyLinker cryptographic key-reuse clustering and SSU complexity metrics are thoughtfully designed to capture the structural properties of mixing transactions. The ablation study in Table 2 clearly shows that REUSE and CS features consistently improve performance across all three classifiers.
- **Clear experimental organization**: The paper systematically evaluates feature subsets across supervised and semi-supervised settings, making the contribution of each feature group transparent. The consistent use of F1-score, ROC AUC, precision, and recall with class-weighted models is appropriate for the imbalanced setting.

## Weaknesses

### Fatal

None.

### Major

- **SSL provides essentially no improvement over supervised learning**: The best supervised XGBoost F1 is 0.845 (Table 2, DEFAULT+REUSE+CS+SSU) and the best SSL XGBoost F1 is also 0.845 (Table 3, same features). The paper acknowledges this but frames it as confirming the "quality over quantity" thesis. However, this equally supports the interpretation that the pseudo-labeling scheme is ineffective. The central claim that "SSL effectively leverages unlabeled data" is not convincingly demonstrated when the gains are zero.

- **Weak SSL baselines and methodology**: The pseudo-labeling approach is a basic confidence-thresholded self-training scheme. No modern SSL methods (e.g., FixMatch, MixMatch, consistency regularization, co-training) are compared against. Given that the paper's central contribution involves SSL, the absence of comparison with established SSL techniques is a significant gap. The paper also does not compare against the GNN-based approaches cited in related work that reportedly achieve 92% accuracy.

- **The "quality over quantity" claim is not rigorously established**: The paper argues that adding OTC features degrades performance, proving that more data/features can hurt. However, the effect sizes are small and inconsistent. For CatBoost, adding OTC to DEFAULT+REUSE+CS changes F1 from 0.824 to 0.823 (Table 2)—essentially noise. The paper does not provide confidence intervals or statistical significance tests, making it impossible to distinguish genuine effects from random variation across the many experimental configurations.

- **Conflation of feature quality for classification vs. pseudo-labeling**: The paper claims pseudo-labels from high-fidelity features are more valuable, but the experiments do not directly test this. The SSL experiments simply retrain with the same feature sets; they do not, for example, generate pseudo-labels using one feature set and evaluate with another. The mechanism by which "quality features guide pseudo-label selection" is asserted but not experimentally isolated.

### Minor

- **Label quality is underexplored**: Labels are aggregated from multiple sources (WalletExplorer, Elliptic++, MBAL, Kaggle) with acknowledged potential inaccuracies. The paper mentions "manually resolved duplicates and conflicting labels" but provides no details on the resolution process, inter-annotator agreement, or the impact of label noise on results.

- **Missing ablation on pseudo-label volume**: The paper does not report how many pseudo-labels are added in each configuration, making it impossible to assess whether the quality-quantity tradeoff is being tested at meaningful scales. If only a small number of pseudo-labels are added, the lack of improvement could simply reflect insufficient data augmentation.

- **The 12% illicit class imbalance is relatively mild**: The paper emphasizes class imbalance as a key challenge, but 12% positive class is not extreme. The decision to avoid SMOTE/ADASYN is justified by the subsequent pseudo-labeling, but the actual severity of the imbalance challenge is somewhat overstated.

### Trivial

None.

## Nice-to-Haves

- A comparison with at least one modern SSL method (e.g., FixMatch or a simple consistency-based approach) to contextualize the pseudo-labeling results.
- Confidence intervals or standard deviations across cross-validation folds to assess the statistical reliability of the small differences between feature configurations.
- A direct experiment where pseudo-labels are generated using different feature subsets to isolate the "quality-guided pseudo-labeling" mechanism.

## Novel Insights

The paper's most interesting empirical finding is that the OTC heuristic—one of the most widely used address clustering methods in blockchain analytics—can introduce noise that degrades classifier performance when included as a feature. This is a practically useful observation for the blockchain forensics community, suggesting that practitioners should carefully evaluate heuristic quality rather than defaulting to standard approaches. However, the effect sizes are small and not statistically validated, limiting the strength of this conclusion.

## Suggestions

- Add error bars (standard deviations across CV folds) to all reported metrics in Tables 2 and 3 to enable readers to assess whether feature-set differences are statistically meaningful.
- Include a controlled experiment where pseudo-labels are generated using one feature configuration but the model is evaluated with another, to directly test the quality-guided pseudo-labeling hypothesis.
- Compare against at least one established SSL baseline (e.g., self-training with consistency regularization) to demonstrate that the proposed quality-aware pseudo-labeling offers advantages beyond basic self-training.
- Report the number of pseudo-labels added per configuration to clarify the quantity dimension of the quality-quantity tradeoff.

## Score and Decision

The paper addresses a relevant problem and contributes a valuable large-scale dataset. However, the central ML claim—that SSL effectively leverages unlabeled data when guided by quality features—is not supported by the experiments, which show zero improvement from SSL. The SSL methodology is basic, no modern SSL baselines are compared, and the key experimental differences lack statistical validation. The domain-specific feature engineering is the paper's genuine strength, but the ML contribution is insufficient for a top venue.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject