Now I'll produce the final consolidated review.

## Summary

This paper targets illicit Bitcoin transaction detection in CoinJoin/Shared Send Mixer transactions. It assembles a large-scale dataset (1.15B transactions, 163M CoinJoin), engineers features from address clustering heuristics and transaction complexity metrics (KeyLinker, SSU, CS, OTC, REUSE), and evaluates supervised (XGBoost, CatBoost, Random Forest) and semi-supervised (pseudo-labeling) classifiers. The paper's central thesis is that "quality over quantity" in feature engineering, guided by a selective pseudo-labeling scheme, enables SSL to outperform supervised baselines.

## Strengths

- **Large-scale dataset (Section 5.1, Table 1):** The paper compiles 1.15 billion transactions with 163 million CoinJoin transactions, integrating labels from WalletExplorer, Elliptic++, MBAL, and Kaggle up to block 882,421 (Feb 2025). This is a genuinely substantial resource for blockchain forensics, aggregating multiple label sources into a single corpus.
- **Thorough feature ablation analysis (Tables 2–3):** The paper evaluates seven feature configurations across three model types, systematically adding/removing feature groups (DEFAULT, REUSE, CS, OTC, SSU). The finding that OTC features slightly degrade performance when added to the best feature set (DEFAULT+REUSE+CS) is a genuinely interesting and somewhat counterintuitive empirical result — a useful insight for practitioners designing forensic systems.
- **Honest reporting of SSL limitations (Section 6.3, lines 291–293):** The paper explicitly states "Pseudolabeling slightly increased recall (up to +0.03) while reducing precision (from -0.04 to -0.05)" and "The semi-supervised phase did not produce dramatic metric gains." This transparency is commendable, though it creates a tension with the paper's own headline claims.

## Weaknesses

### Major

1. **Central claims contradict the experimental evidence.** The abstract and introduction repeatedly claim that SSL "outperforms supervised baselines" (line 29) and that "SSL effectively leverages unlabeled data" (abstract). However, the best supervised XGBoost achieves F1=0.844 (Table 2, DEFAULT+REUSE+CS) and the best SSL XGBoost achieves F1=0.845 (Table 3, DEFAULT+REUSE+CS+SSU) — a difference of 0.001. The paper's own reporting acknowledges a precision drop of 0.04–0.05 offsetting the recall gain. An F1 difference of 0.001 with no confidence intervals or standard deviations is not "outperforming" — it is statistically indistinguishable. This is a structural framing problem: the paper's headline contribution is contradicted by its own results.

2. **No comparison to any alternative SSL method.** The paper compares only supervised training vs. supervised + pseudo-labeling, calling the latter "SSL." It claims to improve upon "the standard SSL approach of labeling all high-confidence predictions" (line 207) but never implements or evaluates that approach or any modern SSL method (e.g., FixMatch, MixMatch, consistency regularization, or even standard self-training without quality filtering). Without any SSL baseline, readers cannot assess whether the quality-filtered approach offers any advantage. The paper cannot claim its SSL approach is superior when it never tests the alternative it claims to beat.

### Minor

3. **Overclaimed novelty of features.** The abstract calls KeyLinker and SSU metrics "Novel, high-fidelity features" (line 9) and the introduction says "We introduce" them (line 28). However, both are cited to prior publications (Smolenkova & Yanovich 2025; Larionov & Yanovich 2023, 2024). The paper does not explain how KeyLinker works beyond "clustering based on the reuse of public keys" (line 199) or distinguish which parts are newly contributed vs. adopted. This overstates the feature engineering novelty.

4. **Underspecified pseudo-labeling procedure (Section 5.3, lines 226–230).** The paper states it selects "the top fraction of samples on both sides of the decision boundary" but does not report: what fraction, how many pseudo-labels were added (absolute count and proportion of labeled set), what confidence threshold was used, whether a validation set was used for threshold tuning, or how many self-training iterations were performed. These details are essential for reproducibility of the paper's only SSL-specific methodological step.

5. **No confidence intervals or standard deviations.** All metrics in Tables 2–3 are reported as point estimates without variance. Since the key comparison (supervised vs. SSL) differs by 0.001–0.005 in F1, the reader cannot assess whether any observed difference is meaningful.

### Trivial

None.

## Nice-to-Haves

- Adding a "standard" pseudo-labeling baseline (all confident predictions, no quality filtering) to substantiate the claim that quality filtering is beneficial.
- Reporting pseudo-labeling operational details (fraction, threshold, iteration count, accuracy).
- Adding a limitations section discussing label quality from external sources, the ceiling effect observed with SSL, and generalizability to other blockchains.
- Adding confidence intervals or standard deviations to all reported metrics.

## Removed Points

These points were raised in the input review but are removed or downgraded with justification:

- **"KeyLinker is treated as a black-box feature"** — The paper describes KeyLinker as "a clustering approach based on the reuse of public keys" (line 199) and cites the reference. A full algorithmic description is appropriate for the cited technical report.
- **"No limitation section"** — True but a presentation preference, not a validity issue; the paper is missing it but this is minor.
- **"Tables garbled by PDF extraction"** — Parser artifact, not a paper weakness.
- **"Computational cost and runtime missing"** — Nice-to-have, not a core weakness.
- **"Dataset release commitment lacks schema/field descriptions"** — Standard for camera-ready conditional releases.
- **"Recall values substantially lower than precision not discussed"** — The paper does discuss this at lines 252 and 291–292, justifying the precision-recall tradeoff for forensic analysis.

## Novel Insights

Beyond the paper's own contributions, the key insight from the review is that the paper's strongest empirical finding — the feature ablation showing OTC features degrade performance — is actually in tension with its own SSL narrative. The feature ablation study would stand alone as a contribution, but the paper frames it as supporting an SSL outperformance claim that the data cannot sustain. The negative result (SSL produces no measurable improvement when the supervised model is already well-featurized) is itself interesting, but the paper does not present it as such.

## Suggestions

1. **Reframe the contribution.** Drop the unsupported "SSL outperforms" claim. Reposition the paper around the feature ablation study as the primary contribution, with the SSL result presented honestly as a negative finding: pseudo-labeling does not help when high-quality features already produce strong supervised performance. This negative result is publishable and useful to the community.
2. **Implement a proper SSL baseline.** At minimum, run pseudo-labeling without quality filtering (the "standard approach" mentioned in line 207) and compare to the quality-filtered version. This would either validate or qualify the "quality over quantity" thesis.
3. **Report pseudo-labeling details.** The fraction of unlabeled data pseudo-labeled, confidence thresholds, number of iterations, and pseudo-label accuracy (if measurable) are essential for reproducibility.
4. **Add uncertainty estimates.** Confidence intervals or standard deviations for all metrics, especially given the tiny differences between key comparisons.

## Score and Decision

**Score:** 3.5  
**Decision:** Reject

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/.../yM7rw8Bo1f.md | 4.25 | R1 | Yes | FE-GNN: Similar blockchain classification paper. Shares dataset contribution + missing SOTA baseline weaknesses. Our paper has an additional claims-evidence mismatch. |
| /home/.../q7Xi4yZYcH.md | 3.00 | R1 | No | Transaction anomaly detection. More severely lacking in novelty and experimental rigor than our paper. |
| /home/.../LPXfOxe0zF.md | 5.75 | R1 | Yes | Blockchain foundation model with stronger experimental rigor, ablation studies, and open-sourced code — above our paper. |
| /home/.../juE0rWGCJW.md | 6.33 | R1 | Yes | Blockchain dataset paper with clearly scoped contribution and reproducible artifacts — Accept range, above our paper. |
| /home/.../6yXAKleluj.md | 4.00 | R2 | Yes | Similar Ethereum anomaly detection. Missing baselines and incomplete presentation — comparable to our paper in severity of issues. |

**Score justification:** The paper's weighted items net at -11.20 (model-assigned), driven primarily by the missing SSL baseline comparison (-7.90) and the claims-evidence mismatch (-4.74). These heavy-weight negatives are comparable to yM7rw8Bo1f.md's missing SOTA comparison (-7.53) and lack of novelty (-9.04), which anchors at 4.25. However, our paper additionally suffers from a structural claims-evidence mismatch that yM7rw8Bo1f.md does not, placing it slightly below that anchor. The round-1 bracket was 3.0–5.0, narrowed to 3.5 given that the paper has genuine empirical contributions (dataset, ablation study) but its central framing is contradicted by its own data. The problems are addressable with reframing and additional baselines, but in the current form the paper's headline claims are not supported.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>