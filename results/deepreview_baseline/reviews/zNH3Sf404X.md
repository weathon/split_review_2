## Summary
The paper addresses the detection of illicit Bitcoin transactions in CoinJoin mixers using semi-supervised learning (SSL). The authors introduce a large historical dataset of 163 million CoinJoin transactions, novel features based on KeyLinker address clustering and Shared Send Untangling (SSU) complexity metrics, and an SSL framework that selectively pseudo-labels unlabeled data based on feature quality. The central claim is that SSL success depends on data quality (high-fidelity features) rather than data quantity.

## Strengths
- The problem is practically important and timely: detecting illicit cryptocurrency flows in mixed transactions is a high-stakes challenge for blockchain forensics.
- The paper contributes a large-scale dataset (163M CoinJoin transactions with labels and SSU classifications) that, if released, could be a valuable resource for the community.
- The experimental design systematically evaluates feature sets, demonstrating that certain common heuristics (OTC) degrade performance, lending support to the message that careful feature engineering matters.

## Weaknesses
### Fatal
- **Central claim is not convincingly supported.** The SSL improvement over supervised learning is marginal (F1 from 0.842 to 0.845, Table 2 vs Table 3). The degradation caused by OTC features is consistent with OTC being a noisy feature for classification, but the paper does not demonstrate a general "quality over quantity" principle. There is no baseline SSL comparison that uses all unlabeled data (i.e., standard pseudo-labeling without quality-based selection). Without this control, the observed effects could simply reflect the quality of the features themselves rather than any insight about SSL.

### Major
- **Limited novelty.** The KeyLinker clustering and SSU metrics are direct applications of prior work (Larionov & Yanovich 2023; Smolenkova & Yanovich 2025). The "data quality principle" is an intuitive observation, not a theoretical or algorithmic innovation. The SSL methodology (selective pseudo-labeling from high-confidence predictions) is standard.
- **No comparison with state-of-the-art methods.** The paper only evaluates tree-based models (XGBoost, CatBoost, Random Forest). Recent work using GNNs, metapath-aware networks, or hypergraph-based approaches (cited in the related work) achieves higher accuracy (92% reported). The paper does not compare its performance against these methods on any common benchmark.
- **Experimental details are incomplete.** The number of pseudo-labels added, selection thresholds, number of SSL rounds, and stability across runs are not reported. Tables 2 and 3 contain duplicate rows (e.g., CatBoost rows 6 and 7 are identical feature sets with different metrics, indicating a formatting error). This undermines confidence in the rigor of the experiments.
- **Overstated contributions.** The abstract claims "SSL effectively leverages unlabeled data (F1-score: 0.84)" but the supervised best is also 0.842–0.845. The SSL phase did not produce meaningful gains, yet the paper frames it as a demonstration of success.

### Minor
- The paper is verbose and repetitive, especially in the introduction and conclusion.
- The dataset is compiled from multiple sources with manual label resolution, but no analysis of label noise, conflicts, or inter-source agreement is provided.
- The OTC feature set is shown to degrade performance, but the paper does not discuss why OTC might be noisy in this specific context (e.g., CoinJoin transactions where change addresses behave differently).

## Nice-to-Haves
- Compare against a vanilla SSL baseline (e.g., self-training with all unlabeled data) to isolate the effect of quality-based selection.
- Provide an ablation study varying the proportion of pseudo-labels added and the selection criteria (confidence threshold vs. SSU/KeyLinker-based selection).
- Include comparison with at least one graph-based or deep learning model from recent literature.

## Novel Insights
None beyond the paper’s own contributions. The observation that feature quality matters for SSL is a known principle in active learning and pseudo-labeling (e.g., curriculum pseudo-labeling). The paper does not formalize or generalize this insight beyond the specific blockchain domain.

## Suggestions
- Add a baseline SSL experiment that uses all available unlabeled data (without quality filtering) to directly test whether quality-based selection yields meaningful gains.
- Compare against one or two state-of-the-art detection methods (e.g., a GNN or a hypergraph model) on the same dataset split.
- Fix the duplicate rows in Tables 2 and 3 and provide clear definitions for each feature set abbreviation (e.g., DEFAULT = ?).
- Report the number of pseudo-labels added and the impact on training distribution.

## Score and Decision
The paper addresses a relevant problem and provides a dataset, but its core claim is not convincingly demonstrated, the novelty is limited, and the experimental support is weak. The lack of baselines and marginal SSL improvements suggest the paper does not yet offer sufficient contribution for acceptance at ICLR.

MY FINAL SCORE: 4.0score</score>  
MY FINAL DECISION: Rejectdecision</decision>