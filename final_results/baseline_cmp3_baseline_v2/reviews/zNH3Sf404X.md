## Summary
The paper tackles detection of illicit Bitcoin transactions in CoinJoin (Shared Send Mixer) transactions, where labels are scarce and class imbalance is extreme. The authors introduce a large-scale dataset of 163 million CoinJoin transactions, propose novel forensic features (KeyLinker address clustering and SSU complexity metrics) aimed at improving data quality, and evaluate a semi-supervised learning (SSL) pipeline with pseudo-labeling. They argue that SSL success depends on feature quality rather than data volume, and show that adding high-fidelity features (KeyLinker, SSU) yields better results than including noisy heuristics like OTC.

## Strengths
- **Substantial dataset contribution:** The paper compiles and processes the first complete historical dataset of CoinJoin transactions (163M transactions) with multiple layers of labeling and clustering, which is a valuable resource for the blockchain forensics community.
- **Careful ablation study on feature quality:** The experiments systematically compare feature sets (Default, REUSE, CS, OTC, SSU) and demonstrate that adding noisy heuristics (OTC) degrades performance, while higher-fidelity features (KeyLinker, SSU) improve results. This supports the central claim about data quality over quantity.
- **Practical problem formulation:** The paper addresses a real-world challenge (illicit flows through mixers) with high societal relevance, and the evaluation metrics (F1, recall, precision) are appropriately chosen for the forensic use case.

## Weaknesses
### Fatal
None.

### Major
- **Marginal SSL improvement over supervised baselines:** The semi-supervised learning phase yields at most +0.001 F1 improvement (0.844 → 0.845 for XGBoost). The paper repeatedly asserts that SSL "effectively leverages unlabeled data," but the experimental evidence shows essentially no gain. The main lesson—that feature quality matters—is already demonstrated in the supervised ablation study and does not require SSL to confirm.
- **Lack of novelty in the SSL method:** The pseudo-labeling scheme is standard self-training with confidence-based selection. No new algorithmic contribution is made to semi-supervised learning itself. For a top ML venue, the paper offers little beyond applying off-the-shelf classifiers with a straightforward SSL wrapper.
- **No statistical significance or robustness tests:** The reported metrics are point estimates without confidence intervals, error bars, or significance tests. Given the minimal performance differences (e.g., F1 0.844 vs. 0.845), it is unclear whether the observed SSL improvements are meaningful or simply due to random variation.

### Minor
- **Dataset not yet released:** The paper states "Upon acceptance, we will release our dataset." This limits reproducibility and the ability to verify results during review. While not a fatal flaw, it weakens the contribution's immediate impact.
- **The "Quality over Quantity" narrative is partially self-evident:** The observation that noisy features hurt performance and better features help is a standard finding in feature engineering. The paper overclaims novelty by framing this as a surprising insight for SSL.
- **Inconsistent table formatting:** Table 2 and Table 3 contain duplicate rows with identical feature sets (e.g., several rows have the same checkmarks but different metrics). This appears to be a formatting or copy-paste error that makes interpretation difficult.

### Trivial
- The abstract states the dataset has "163 million Bitcoin transactions with SSM classification," but Table 1 shows 163.4M CoinJoin transactions. This minor inconsistency does not affect the overall contribution.

## Nice-to-Haves
- Provide confidence intervals or bootstrap-based error bars for all key metrics to assess the significance of SSL gains.
- Include a comparison with a fully supervised model trained on an equivalent amount of pseudo-labeled data to isolate the effect of SSL from merely having more data.
- Release the dataset as part of the review process to enable verification.

## Novel Insights
None beyond the paper's own contributions. The main insight—that feature quality matters more than data volume in SSL for blockchain forensics—is empirically demonstrated but not conceptually new. The specific finding that OTC heuristics introduce noise while KeyLinker (based on cryptographic key reuse) is a cleaner signal is a useful domain insight, but it remains a domain-specific result rather than a general ML principle.

## Suggestions
- Consider framing the paper more as a **domain application and dataset contribution** than as an ML methodology paper. The strongest parts are the large-scale dataset and the careful feature engineering, not the SSL algorithm.
- Add a statistical analysis (e.g., McNemar's test or bootstrap) to show whether the small F1 differences between supervised and SSL are significant.
- Clarify the repeated rows in Tables 2 and 3; ensure each row corresponds to a unique feature combination.

## Score and Decision
Given the limited ML novelty and the fact that the core claim about SSL effectiveness is not convincingly supported (marginal improvement), the paper's contribution is better suited for a specialized blockchain or security venue. The dataset and feature engineering have value, but the overall contribution to the ICLR community is modest.

MY FINAL SCORE: 4.0</score>
MY FINAL DECISION: Reject</decision>