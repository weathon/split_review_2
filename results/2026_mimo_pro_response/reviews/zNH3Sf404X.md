Now I have enough calibration data. Let me finalize the review and score.

**Round 1 Bracket:** Based on the anchors, the paper sits between **2.5 and 4.0**. 

- Papers at 3.0 (Ethereum anomaly detection q7Xi4yZYcH, SSL early stopping aXSxSu3fvg, underwater SSL E0UsEIRBQ8) have similar profiles: application-driven, limited ML novelty, reject.
- The paper under review has a genuinely larger dataset and more comprehensive ablation than the 3.0 anchors, but its central SSL claim is *contradicted* by its own results (which is arguably worse than just having limited novelty).
- Papers at 5.0+ (DIPS eSO9quCgmz, BOPL AEi2wyAMyb, SemiReward dnqPvUjyRI) have genuine ML methodological contributions that this paper lacks.

I'll place the final score at **3.0**, as the paper's genuine domain contributions (dataset, KeyLinker features, OTC negative result) are roughly balanced against the unsupported central claim and limited ML novelty.

---

## Summary
This paper proposes a quality-focused semi-supervised learning framework for detecting illicit Bitcoin CoinJoin transactions, introducing novel features based on KeyLinker address clustering and Shared Send Untangling (SSU) complexity metrics, evaluated on a large-scale dataset of 163M CoinJoin transactions. The central claim is that SSL guided by high-quality features outperforms both supervised baselines and SSL guided by noisier features.

## Strengths
- **Large-scale, comprehensive dataset**: The paper presents 163.4M CoinJoin transactions and 1.15B total transactions (Table 1), substantially exceeding prior work (e.g., 13M in Nerurkar 2022). The dataset integrates on-chain blockchain data with off-chain labels from multiple sources (WalletExplorer, Elliptic++, MBAL, Kaggle).
- **KeyLinker features demonstrably improve supervised classification**: Adding REUSE (KeyLinker) features consistently improves F1 across all three classifiers in Table 2 (e.g., CatBoost: 0.791→0.818, XGBoost: 0.814→0.837, RF: 0.804→0.816), providing empirical validation that cryptographic key reuse patterns capture genuinely informative signals.
- **Useful negative result on the OTC heuristic**: Adding OTC features—which increase labeled data to 472.3M addresses (Table 1)—consistently degrades performance across all models in both supervised (Table 2) and SSL (Table 3) settings. This challenges the conventional assumption that more clustering data is always beneficial and is a concrete, reproducible finding for the blockchain forensics community.
- **Honest acknowledgment of marginal SSL gains**: The paper acknowledges "the semi-supervised phase did not produce dramatic metric gains" (Section 6.3, line 293), avoiding overstatement of the results.

## Weaknesses

### Fatal
None.

### Major

- **Central SSL claim is contradicted by the paper's own results**: The paper's third contribution (Introduction, line 29) claims "a semi-supervised learning framework outperforms supervised baselines," and the abstract claims "SSL effectively leverages unlabeled data (F1-score: 0.84)." However, comparing the best supervised results (Table 2) with the best SSL results (Table 3): XGBoost achieves F1=0.845 in *both* settings, CatBoost goes from 0.830→0.834 (+0.004), and Random Forest goes from 0.830→0.826 (a *decrease*). These differences are negligible, and with no variance reported (5-fold CV was used but no standard deviations are given), we cannot establish significance. The conclusion (line 331) still claims SSL models "outperform those trained on larger, noisier datasets," which is not what the data shows.

- **Pseudo-labeling experiment does not test "quality over quantity"**: The paper's thesis is that pseudo-label quality matters more than pseudo-label quantity. But the experiment is a feature set ablation (adding REUSE, CS, OTC, SSU), not a pseudo-labeling quality ablation. When OTC features degrade performance (Table 2, Table 3), this shows OTC is a poor feature for the classifier, not that pseudo-labels generated from OTC are low quality. No experiment varies pseudo-label quantity at fixed quality or vice versa, or even reports how many pseudo-labels were retained. The paper conflates "features that improve the classifier" with "features that produce better pseudo-labels."

- **Pseudo-labeling procedure is under-specified**: Section 5.3 describes selecting "the top fraction of samples on both sides of the decision boundary, adjusting the share of positives and negatives," but the actual fraction, how the share is adjusted, how many pseudo-labels were retained, and the class distribution of the expanded dataset are never stated. This makes the experiment impossible to replicate and prevents assessment of whether the pseudo-labeling was meaningful or trivially small.

### Minor

- **No variance reported despite 5-fold cross-validation**: Standard deviations or confidence intervals from the CV folds should accompany all reported metrics. The differences between supervised and SSL (e.g., 0.845 vs. 0.845 for XGBoost) cannot be assessed for significance.

- **No comparison to other semi-supervised methods**: The paper does not compare its pseudo-labeling approach to any alternative SSL method (e.g., self-training with different selection strategies, varying confidence thresholds, or methods like MixMatch/FixMatch). For a paper claiming SSL contributions, this comparison is needed.

- **Oversampling baselines excluded**: SMOTE/ADASYN are excluded with the justification that "pseudo-labeling later introduces new positive examples," but this means the SSL is not compared against a fair alternative that also addresses class imbalance.

### Trivial
None.

## Nice-to-Haves
- Report pseudo-label statistics: how many pseudo-labels were retained, class distribution, and expanded training set size.
- Ablation on pseudo-label fraction to show how F1 changes as more pseudo-labels are added.
- Comparison to oversampling methods as a baseline for addressing class imbalance.

## Removed Points
- Table 2 formatting/parsing issues — these are parser artifacts, not problems with the original paper.
- Claims about missing appendix content — stripped by parser.

## Novel Insights
The negative result on the OTC heuristic — showing that one of the most widely used clustering methods in blockchain forensics (generating 472.3M clustered addresses) consistently degrades model performance despite its data richness — is a genuinely valuable finding for the blockchain forensics community. It provides concrete evidence that data quantity without quality control is counterproductive, which aligns with broader findings in data-centric AI but has not been demonstrated for blockchain clustering heuristics before.

## Suggestions
- **Reframe honestly**: The main contribution is feature engineering (KeyLinker + SSU) for CoinJoin detection, supported by a large dataset. The SSL component needs genuine experiments demonstrating quality-driven pseudo-labeling effectiveness, or it should be presented as a minor extension rather than a core contribution.
- **Add variance estimates** from the 5-fold CV runs to all reported metrics.
- **Specify all pseudo-labeling hyperparameters** (fraction selected, class balancing, expanded dataset size).
- **Add controlled ablations** varying pseudo-label quantity at fixed quality and vice versa, if pursuing the SSL story.

## Reporting — Calibration Anchors

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| q7Xi4yZYcH (Ethereum GCN+TRW anomaly detection) | 3.00 | 1 | Similar: application paper, limited ML novelty, reject |
| aXSxSu3fvg (SSL early stopping) | 3.00 | 1 | Similar: SSL application, single dataset, limited novelty |
| E0UsEIRBQ8 (Underwater SSL object detection) | 3.00 | 1 | Similar: SSL application, limited novelty, no confidence intervals |
| k9KKFhwNwg (EGLNN Ethereum/IoT) | 3.50 | 2 | Similar domain, slightly more methodological contribution |
| eSO9quCgmz (DIPS pseudo-labeling) | 5.00 | 1 | Stronger: genuine ML contribution to SSL, multi-modal benchmarks |
| AEi2wyAMyb (BOPL bi-level optimization) | 5.33 | 1 | Stronger: novel ML formulation for pseudo-labeling |
| dnqPvUjyRI (SemiReward) | 6.00 | 1 | Much stronger: extensive benchmarks, novel framework, accepted |
| dpnPOXoqVQ (S²MAM) | 4.75 | 2 | Stronger: theoretical contribution to SSL |
| X8RTdxzqJQ (Two-sample testing as SSL) | 4.80 | 2 | Stronger: genuine theoretical contribution |
| sLtuNGkKfH (Subject info extraction) | 4.00 | 2 | Similar level but different domain |
| iMnd6c5bAa (Density ratio BO with SSL) | 3.67 | 2 | Similar: limited SSL improvement, niche application |

**Round 1 bracket: 2.5–4.0.** The paper has genuine domain contributions (dataset, KeyLinker features, OTC negative result) that push it above pure "no novelty" papers (score 1-2), but the central SSL claim is unsupported and the ML methodological novelty is limited. The Ethereum anomaly detection papers at 3.0 have a very similar profile (application paper, limited ML novelty, some contribution). This paper has a *larger* dataset and more *comprehensive* ablation than those anchors, but also has the additional problem that its central claim is contradicted by its own results.

**Final score: 3.0** — The domain contributions (dataset, KeyLinker, OTC negative result) are real and valuable for the blockchain forensics community, but for ICLR the ML contribution is what matters, and the SSL framework—which is the paper's claimed ML novelty—does not hold up. The paper is on par with other application-driven SSL papers scored at 3.0.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>