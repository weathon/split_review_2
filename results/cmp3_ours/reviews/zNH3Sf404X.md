Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper tackles detection of illicit CoinJoin transactions in Bitcoin. The authors contribute (1) a dataset of 163M CoinJoin transactions (the largest such collection), (2) novel forensic features (KeyLinker address clustering, SSU complexity metrics), and (3) a semi-supervised learning framework motivated by a "data quality" principle — the thesis that SSL success depends on feature quality, not just data quantity. The core finding is that OTC heuristics slightly degrade performance while REUSE/CS features help.

## Strengths

1. **Large-scale, domain-specific dataset.** The paper assembles 163M CoinJoin transactions from the full Bitcoin blockchain up to block 882,421, with 4.6M labeled and extensive address clustering statistics (Table 1). This is a substantive resource for blockchain forensics, and the commitment to release it is commendable.

2. **Systematic feature ablation across model classes.** The paper evaluates Random Forest, XGBoost, and CatBoost on five feature groups (DEFAULT, REUSE/KeyLinker, CS, OTC, SSU), testing every incremental combination. The finding that OTC features consistently fail to improve (and sometimes degrade) performance while REUSE and CS are reliably beneficial is a clean empirical result, visible across both supervised and SSL settings.

## Weaknesses

### Major

1. **The claimed SSL "improvement" over supervised learning is negligible and does not support the paper's central claim.** The best supervised XGBoost F1 is 0.844 (Table 2, line 270). The best SSL XGBoost F1 is 0.845 (Table 3, line 315) — a gain of 0.001. The paper acknowledges "The semi-supervised phase did not produce dramatic metric gains" (line 293), yet the abstract claims "SSL effectively leverages unlabeled data (F1-score: 0.84)" and the introduction claims SSL "outperforms supervised baselines" (line 29). An improvement within any reasonable measurement noise does not constitute successful SSL. The paper's central narrative — that SSL success is contingent on data quality — collapses if SSL does not, in fact, improve over supervised learning. This is a structural mismatch between claim and evidence.

2. **The text and tables are internally inconsistent about which feature set performs best.** The paper repeatedly asserts that the best results come from the `Default+REUSE+CS+SSU` configuration (without OTC). Specifically:
   - Line 250: "XGBoost achieves the best supervised performance with an F1-score of 0.845 (default+reuse+cs+ssu)." But Table 2 has no row with this configuration. The closest is XGBoost with DEFAULT+REUSE+CS (no SSU) at F1=0.844 (line 270).
   - Line 287: "the best results were consistently achieved with the `Default+REUSE+CS+SSU` feature set" in the SSL phase. But Table 3 never includes this configuration for any model. The best SSL result (XGBoost F1=0.845, line 315) uses **all five features including OTC** — directly contradicting the claim that OTC degrades performance.
   These are factual errors, not presentation issues, and need correction.

3. **Tables 2 and 3 contain duplicate and unexplained rows.** Both tables show multiple rows with identical feature checkmarks but different metrics (e.g., CatBoost lines 265–267 with all features checked show F1=0.800, 0.830, 0.827). In Table 3, rows 308–309 are exact duplicates (all metrics identical), as are rows 316–317 and 324–325. The paper never explains what distinguishes these rows — different random seeds, hyperparameter configurations, pseudo-label fractions, or something else. This is a serious reporting flaw that undermines confidence in the results.

4. **No comparison against any existing detection method.** The related work (Section 3) cites GNNs at 92% accuracy (Nerurkar 2022), decision trees detecting 97% of mixing services (Rathore et al. 2022), and quantum-inspired feature selection (Sie et al. 2024), among others. Yet the evaluation benchmarks only three gradient-boosted tree variants against each other, without comparing against any prior method. Without situating the proposed features and framework against existing approaches, the reader cannot assess whether the contributions advance the state of the art.

5. **Conclusions substantially overstate the evidence.** The abstract claims to "prove that common heuristics like One-Time Change (OTC), though abundant, introduce noise, while strategic reliance on higher-fidelity features like KeyLinker is essential." The experiments show that adding OTC decreases F1 by ~0.01–0.03 and that REUSE/CS increase F1 relative to DEFAULT-only — a modest feature-engineering finding. The framing as a "proof" about data quality, SSL success, and blockchain forensics principles is disproportionate. The strongest supported claim is: *for these gradient-boosted models on this dataset, omitting OTC and including REUSE/CS yields slightly better results.*

### Minor

6. **The pseudo-labeling protocol is critically underspecified.** The paper describes selecting "the top fraction of samples on both sides of the decision boundary" (lines 228, 285) but never reports: what fraction was used, how many pseudo-labels were added, how many rounds of pseudo-labeling were performed, or how the fraction was chosen. Without these details the experiment is not reproducible, and the reader cannot assess whether the near-zero SSL gain reflects the data-quality principle or simply a conservative pseudo-labeling choice.

7. **KeyLinker's individual contribution is not isolated.** The ablation treats "REUSE" as a binary flag, but Table 1 shows KeyLinker covers only 131.4K addresses versus 859M for CS and 472.3M for OTC. Without statistics on overlap or a finer-grained ablation within the REUSE group, the claim that KeyLinker is "essential" is not well supported by the evidence presented.

8. **No variance or significance reporting.** No standard deviations, confidence intervals, or significance tests accompany any metric. Given that many feature-set differences are in the 0.01–0.03 range, the reader cannot assess stability versus noise.

### Trivial

None.

## Nice-to-Haves

- A dedicated error analysis of *why* OTC features degrade performance (e.g., spurious correlations, label propagation errors).
- Label quality characterization: statistics on conflict resolution, label source breakdown.
- A limitations section acknowledging the limited SSL gain and discussing possible reasons.

## Removed Points

- **"Missing related works"** — The paper has a substantial related works section (Section 3); the criticism was about lack of experimental comparison, which is already covered in weakness #4 above.
- **Formatting/style nits about table bolding, commas, etc.** — These are parser artifacts or below the threshold of substantive review.
- **"No explicit limitations section"** — Not a standard requirement for conference papers.
- **"SSL improvement is zero" framed as fatal** — It is a major weakness but not fatal to the entire paper; the feature ablation study and dataset remain contributions even if the SSL claim is dropped.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Restructure the paper to present the feature ablation study (OTC hurts, REUSE/CS help) as the main empirical contribution, and either drop the claim that SSL "outperforms" supervised baselines or present it transparently as a neutral/negative result.
2. Resolve the inconsistencies between text and tables: the `Default+REUSE+CS+SSU` configuration either needs to appear in the tables or the text needs correction.
3. Clearly label what distinguishes the duplicate rows in Tables 2 and 3 (e.g., different seeds, thresholds) and remove true duplicates.
4. Add variance estimates or statistical tests for key metric comparisons.
5. Benchmark against at least one prior method from the cited literature.

## Score and Decision

**Calibration:** Anchoring against the human-reviewed corpus:

| Anchor | Path | Avg Score | Comparison |
|--------|------|-----------|------------|
| Ethereum Anomaly Detection | q7Xi4yZYcH.md | 3.00 | Similar domain, but our paper has a larger dataset. However, our paper has more severe reporting issues (inconsistent tables, duplicate rows). |
| FE-GNN (blockchain account classification) | yM7rw8Bo1f.md | 4.25 | Similar weaknesses: no error bars, missing baselines, incremental contribution. Our paper adds table inconsistencies and an unsupported central claim. |
| BlockFound (blockchain foundation model) | LPXfOxe0zF.md | 5.75 | Much stronger methodology and thorough evaluation; our paper is substantially weaker. |
| EX-Graph (Ethereum+X dataset) | juE0rWGCJW.md | 6.33 | Cleaner dataset contribution with thorough evaluation; our paper's reporting issues are more severe. |

**Round 1 bracket:** 3.0–5.0. The paper's dataset contribution is real and large-scale, placing it above a strong reject (1–2). However, the central SSL claim is unsupported by the evidence (0.001 F1 gain), the tables contain factual inconsistencies with the text and unexplained duplicate rows, and no comparison against prior methods is provided. These issues align the paper with the lower end of the bracket.

**Final score rationale:** The dataset and feature ablation are genuine contributions, but the paper overstates its claims (SSL outperformance is not demonstrated), its evidence is internally inconsistent (text-table mismatch, duplicate rows), and it lacks baselines against prior work. Restructuring around the feature engineering study would strengthen the paper considerably, but as submitted the gap between claims and evidence is too large.

**Decision: Reject**

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>