Now let me produce the final consolidated review.

## Summary

This paper studies detection of illicit Bitcoin transactions through CoinJoin mixers, proposing a semi-supervised learning framework with feature engineering. It makes three claimed contributions: (1) a large historical dataset of 163M CoinJoin transactions; (2) forensic features based on KeyLinker address clustering and Shared Send Untangling (SSU) complexity metrics; (3) a quality-driven SSL approach that selectively pseudo-labels unlabeled transactions. The core thesis is that feature quality (KeyLinker/SSU) matters more than feature quantity (OTC heuristics) for SSL success.

## Strengths

- **The dataset is a significant engineering effort.** The paper compiles 1.15B total transactions, 163.4M CoinJoin transactions, and integrates multiple labeling sources (WalletExplorer, Elliptic++, MBAL, Kaggle) with manual deduplication (Section 5.1). If released, this would be a valuable community resource for blockchain forensics research.

- **The feature engineering study produces a clear empirical finding.** The paper reports a controlled comparison showing that adding OTC (One-Time Change) features consistently degrades performance across XGBoost, CatBoost, and Random Forest in both supervised and SSL settings, while the combination of KeyLinker-clustering-derived features and SSU complexity metrics produces the best results (Tables 2 and 3). This pattern — that a widely used heuristic (OTC) introduces noise — is a practically useful finding for practitioners building forensic classifiers.

## Weaknesses

### Fatal
None.

### Major

- **The central claim that SSL "outperforms supervised baselines" is unsupported by the reported metrics.** The paper's contribution 3 (line 29) states that the SSL framework "outperforms supervised baselines by leveraging unlabeled data strategically." The evidence does not support this. The best supervised XGBoost achieves F1=0.844 and ROC-AUC=0.970 (Table 2, line 270), while the best SSL XGBoost achieves F1=0.845 and ROC-AUC=0.969 (Table 3, line 315). The "improvement" is **+0.001 F1, −0.001 ROC-AUC** — effectively flat. The paper acknowledges this ("did not produce dramatic metric gains," line 293) but nevertheless frames SSL as a core contribution (abstract line 9; introduction line 29). The actual empirical finding is that SSL produces essentially identical results to supervised learning in this setting, which does not substantiate the claim that SSL "effectively leverages unlabeled data." This mismatch between claim and evidence undermines the paper's primary advertised contribution.

### Minor

- **The "quality over quantity" thesis is demonstrated by the supervised experiments alone; the SSL component is not needed to show it.** The pattern that OTC degrades performance and KeyLinker/SSU features perform best is fully visible in Table 2 (supervised). The SSL results in Table 3 replicate the same pattern without adding new evidence for the feature-quality claim. This means the three contributions are less interdependent than presented — contribution 2 (features) stands on its own, while contribution 3 (SSL) does not add evidentiary weight to it.

- **KeyLinker and SSU are attributed to prior work but framed as "novel" contributions.** The paper cites KeyLinker as prior work by Smolenkova & Yanovich (2025) and SSU metrics as prior work by Larionov & Yanovich (2023) (line 28). Yet the abstract (line 9) describes them as "Novel, high-fidelity features." The paper says it uses "enhanced" SSU metrics but provides no detail about what the enhancement consists of. The contribution in this area is applying existing techniques to a new domain, not inventing them.

- **Tables 2 and 3 contain duplicate rows with identical feature sets but different metrics, with no explanation of what distinguishes them.** Examples: CatBoost rows with all five features checked in Table 2 (lines 265–267) reporting F1=0.800, 0.830, 0.827; CatBoost in Table 3 (lines 306–309) with F1=0.807, 0.834, 0.829, 0.829. Some duplicate rows are numerically identical (e.g., lines 308–309, 316–317, 325–326). Without annotations for what varies between these rows (hyperparameters? random seeds? different pseudo-label batches?), the reader cannot meaningfully interpret the results or verify the headline numbers. The paper also has a minor inconsistency: the text (line 250) claims an F1-score of 0.845 for supervised XGBoost, but Table 2 shows 0.844 as the best supervised XGBoost result.

- **The paper reports 5-fold cross-validation but provides no variance or confidence intervals.** Given that the key comparison turns on a difference of 0.001 in F1, the absence of any standard deviation, per-fold breakdown, or statistical test makes it impossible to assess whether any claimed differences are meaningful.

- **Ground-truth label quality is acknowledged as a concern but never analyzed.** The paper states that "off-chain labeling sources may introduce inaccuracies" (line 23) and that labels come from sources of unknown reliability (line 173). For a paper whose thesis centers on data quality, the absence of any analysis of label noise, inter-source agreement, or propagation errors from address-level to transaction-level labels is a gap — particularly because noisy ground truth could explain the flat SSL results.

- **The pseudo-labeling procedure lacks concrete implementation details.** The paper describes selecting "the top fraction of samples on both sides of the decision boundary" (line 228) but never specifies what fraction was used, how many pseudo-labels were added per class/SSU category, or how many rounds of pseudo-labeling were performed. Without these details, the experiments cannot be reproduced, and it is unclear whether the flat SSL results reflect a genuine ceiling or an insufficient number / poor selection of pseudo-labels.

### Trivial
None.

## Nice-to-Haves

- An ablation study showing how SSL performance varies with the fraction of pseudo-labels retained, and how many pseudo-labels come from each SSU complexity class, would directly test the quality-over-quantity hypothesis.
- Reporting per-class precision/recall (given the extreme 12% illicit class imbalance) and confusion matrices would be more informative than aggregate F1.
- The paper could validate the propagation from address-level labels to transaction-level labels — a transaction with both a "mixer" address and a "legal" address currently receives an ambiguous label via clustering.

## Removed Points

The following points from the input review were removed with justification:

- **"The SSL framework is not needed, the paper should reframe"** and **"the paper's central thesis is the SSL contribution"** — While the reviewer's suggestion to reframe around feature engineering is reasonable, this is presented as a structural/fatal flaw. The paper's actual supervised and SSL experiments do form a coherent, if modest, empirical study. The removal is because the reviewer's framing of the issue is editorial (suggesting reframing) rather than a demonstrated error; the core weakness (flat SSL results) is already captured in the Major section above.

- **"The paper cannot claim to have demonstrated SSL works when SSL produces no improvement"** — Already captured above; restating it with different severity language is redundant.

- **Critique about "off-chain labeling sources" being "unknown reliability"** — The criticism that label quality is unexamined is kept as a Minor weakness. The input review's stronger phrasing ("if labels are noisy, the SSL result is uninterpretable") is speculative. The paper acknowledges the concern, and the core findings (OTC vs. KeyLinker/SSU patterns) are unlikely to reverse under label noise analysis.

- **The reviewer's Suggestions section items (1-4)** — These are imperfectly reproducible details that are more appropriate as Nice-to-Haves or Minor weaknesses. The specific suggestion to "report how many pseudo-labels were added per SSU class" is now folded into the Minor weakness about missing pseudo-label details.

- **"The formalization assumes tag propagation through clustering is error-prone and unanalyzed"** — The paper does describe clustering heuristics (CS, OTC, KeyLinker) and their basis; the propagation assumption is standard in the domain. Kept only to the extent that no empirical validation is provided.

## Novel Insights

The most penetrating observation from the review process is that the paper's actual empirical contribution is the feature engineering comparison (OTC degrades, KeyLinker/SSU improves), not the SSL framework. The SSL results are essentially a null result: adding unlabeled data through pseudo-labeling produces no measurable improvement over a supervised baseline. However, the paper's framing leads with the SSL contribution, creating a mismatch between the headline claims and the evidence. This suggests the paper would be stronger if positioned as a feature engineering study for forensic CoinJoin classification, with the SSL experiments presented as a negative result (quality-aware pseudo-labeling does not harm but also does not improve performance) rather than as a positive demonstration. The dataset contribution is genuine but currently undersold relative to the unsupported SSL claim.

## Suggestions

1. Either demonstrate that SSL actually improves over the supervised baseline (with meaningful margins and significance testing) or reframe the paper around the feature engineering contribution, presenting the SSL experiments as a replication of the same pattern in a semi-supervised setting.
2. Annotate the duplicate table rows in Tables 2 and 3 to explain what differentiates them (hyperparameters, seeds, batch sizes).
3. Report the number of pseudo-labels added per SSU complexity class, and provide per-fold cross-validation results with standard deviations.
4. Add a brief analysis of label quality — at minimum, inter-source agreement for addresses with multiple labels.
5. Correct the inconsistency between the text (F1=0.845, line 250) and Table 2 (F1=0.844, line 270) for supervised XGBoost performance.

## Score and Decision

The paper makes a genuine contribution through its feature engineering study and large-scale dataset, but the primary advertised contribution (SSL outperforming supervised) is not supported by the evidence. The flat SSL results contradict the paper's framing, and the presentation issues (unannotated table rows, missing pseudo-label details, no significance testing) further weaken reliability. On balance, the paper's actual empirical contribution is the feature engineering comparison, which is a useful but incremental finding.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>