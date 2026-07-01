Now I have all the calibration context. Let me produce the final review.

## Summary

This paper studies semi-supervised learning (SSL) for detecting illicit Bitcoin transactions in CoinJoin/Shared Send Mixers. It presents three contributions: (1) a large-scale dataset of 163M CoinJoin transactions with SSU complexity classifications and external labels, (2) feature engineering using KeyLinker address clustering and SSU complexity metrics, and (3) an SSL pseudolabeling framework. The paper's central thesis is that data quality (via feature engineering) matters more than data quantity for SSL in blockchain forensics.

## Strengths

- **Large-scale CoinJoin transaction dataset.** The paper compiles 163M CoinJoin transactions spanning Bitcoin's entire history up to block 882,421, with SSU complexity classifications and external service-category/legality labels. At 1.15B total transactions and 1.37B addresses, this is the most comprehensive CoinJoin transaction dataset described in the literature. The paper commits to releasing it upon acceptance, which would be a valuable resource for the blockchain forensics community.

- **Systematic feature ablation across model families.** Tables 2 and 3 report results for 7 feature configurations (DEFAULT, +REUSE, +CS, +OTC, +SSU) across XGBoost, CatBoost, and Random Forest, in both supervised and SSL settings. The incremental feature addition allows readers to disentangle individual feature contributions.

- **SSU complexity classification as a quality-aware design choice.** Extending the SSU untangling framework (Larionov & Yanovich, 2023) to classify transactions as simple/separable/ambiguous/time-limited/regular, and using these classes both as features and as a criterion for pseudo-label selection, is a well-motivated domain-appropriate design.

## Weaknesses

### Major

**1. The central SSL claim is not supported by the evidence.** The paper's abstract, introduction, and conclusion assert that SSL "effectively leverages unlabeled data" and "outperforms supervised baselines" (contribution #3, line 29). However:

- The best supervised result (XGBoost, DEFAULT+REUSE+CS, Table 2) achieves F1=0.844.
- The best SSL result (XGBoost, all features including OTC, Table 3) achieves F1=0.845 — a difference of 0.001.
- When comparing the *same* feature set (DEFAULT+REUSE+CS), the supervised result (F1=0.844) is actually *higher* than the SSL result (F1=0.839, Table 3).

The paper acknowledges that "the semi-supervised phase did not produce dramatic metric gains" (line 293) but continues to frame SSL as a demonstrated success. An F1 improvement of 0.001 (with different features) and a 0.005 decrease (with the same features) cannot sustain the claim that SSL "outperforms" supervised baselines. The evidence shows SSL produces essentially no gain on this task, which directly undercuts the paper's third claimed contribution and its central narrative.

**2. The claim that OTC features "introduce noise" and "degrade performance" is contradicted by the paper's own tables.** The paper repeatedly asserts that OTC harms performance (abstract, lines 248, 287, 293). However:

- In Table 2 (supervised), the best CatBoost result (F1=0.830, line 266) and the best RandomForest result (F1=0.830, line 280) both include OTC.
- In Table 3 (SSL), the best result for every model includes OTC: CatBoost F1=0.834 (line 307), XGBoost F1=0.845 (line 315), RandomForest F1=0.826 (line 323).
- The differences between with-OTC and without-OTC configurations are at most 0.001–0.006 F1 with no statistical significance reported.
- Critically, the tables contain no row for DEFAULT+REUSE+CS+SSU (without OTC), so the claim that this combination yields the best results and that removing OTC is beneficial cannot be verified from the presented data.

**3. KeyLinker is claimed as a novel contribution but is cited as prior work and never described.** The abstract and introduction list "KeyLinker address clustering" as a novel feature contribution of this paper (lines 9, 28), but KeyLinker is cited as Smolenkova & Yanovich (2025) — a separate, externally published technique. The paper provides no algorithmic description, pseudocode, formal definition, or explanation of how KeyLinker differs from or improves upon existing clustering heuristics (CS, OTC). A reader cannot evaluate whether KeyLinker is genuinely a contribution of this paper or prior work being applied. The paper must either describe KeyLinker in sufficient detail or clearly demarcate it as prior work and adjust its contribution claims accordingly.

**4. No comparison to any prior detection method.** Section 3 surveys GNNs achieving 92% accuracy (Nerurkar, 2022), ensemble methods reaching 91% (Nerurkar et al., 2021), quantum-inspired feature selection (Sie et al., 2024), and hypergraph-based models (Lee et al., 2024). None are implemented as baselines. The reader cannot assess how the proposed approach compares to the state of the art, which is a significant gap for a paper claiming to advance the field.

### Minor

**5. Pseudo-labeling procedure is underspecified.** Section 5.3 states: "Rather than relying on fixed thresholds, we select the top fraction of samples on both sides of the decision boundary, adjusting the share of positives and negatives." No fraction is reported, no total number of pseudo-labels added, no breakdown by SSU class, and no estimate of pseudo-label accuracy on a held-out set. The SSL pipeline cannot be reproduced from this description.

**6. Tables contain duplicate checkbox patterns without explanation.** In both Table 2 (lines 265–267, 272–274, 279–281) and Table 3 (lines 306–309, 314–317, 322–325), multiple rows show the same checkbox pattern but different metric values. The paper does not explain whether these represent different random seeds, cross-validation folds, or hyperparameter configurations. This undermines interpretability.

**7. No statistical significance or variance reporting.** Every reported metric difference is presented without confidence intervals, standard deviations, or significance tests. Given that the entire "quality over quantity" argument rests on F1 differences of 0.001–0.006, this is a notable gap despite 5-fold cross-validation being mentioned (line 224).

### Trivial

None.

## Nice-to-Haves

- Vary the number of pseudo-labels (1K, 10K, 100K, 1M) with fixed high-quality features to directly test the "quality over quantity" thesis, rather than testing a single SSL condition.
- Report pseudo-label accuracy on a held-out labeled subset to verify whether the pseudo-labels are actually correct.
- Clarify the mapping between REUSE features and KeyLinker: does the REUSE column encode KeyLinker clustering outcomes?

## Removed Points

- **Label quality assessment (harsh critic).** The paper explicitly acknowledges this limitation (line 23: "We acknowledge that off-chain labeling sources may introduce inaccuracies"), and external label reliance is standard practice in this domain. Removed as not a paper-specific flaw.
- **Duplicate rows confusion (harsh critic).** Kept as Minor weakness #6 rather than the critic's implied structural concern.
- **"Strengthening the Paper" suggestions about varying SSL data volume.** These are valid improvement suggestions but not weaknesses in the current paper. Moved to Nice-to-Haves.
- **Formatting/style nitpicks.** Removed as parser artifacts.
- **Harsh critic's note about Section-by-Section notes on Abstract/Introduction overstatement.** Absorbed into Major weakness #1.

## Novel Insights

The harsh critic's central insight — that the paper's core SSL claim is contradicted by its own evidence — is sharp and correct. A 0.001 F1 gain with a different feature set and a 0.005 F1 loss with the same feature set cannot sustain the language of SSL "outperforming" supervised baselines. A secondary insight — that the OTC-degradation narrative is actually contradicted by the tables (the best-performing configurations in both tables include OTC) — is verifiable from the data as printed. These are not speculative concerns; they are directly visible in Tables 2 and 3.

## Suggestions

1. **Recalibrate the paper's framing.** The dataset and feature ablation are genuine contributions that stand on their own. Reduce the centrality of the SSL claim, or present it as what the evidence shows: SSL does not improve over supervised learning on this task, and the paper's core finding is that feature engineering drives performance in *supervised* learning.
2. **Implement at least 1–2 baselines from related work** (e.g., a GNN or the Nerurkar et al. ensemble method) to contextualize the reported F1 scores.
3. **Resolve the KeyLinker ambiguity** by either describing the algorithm in sufficient detail or clearly labeling it as prior work applied here.
4. **Report variance** (per-fold results or standard deviations) for all metrics, especially given the tiny differences being discussed.
5. **Correct the disconnect between text and tables.** The text claims best results come from DEFAULT+REUSE+CS+SSU, but no table row shows this combination. The duplicate rows need explanation.

## Score and Decision

**Calibration.** Round 1 bracketing retrieved 25 papers across six score bands. The most comparable anchors are:
- *FE-GNN* (4.25, Reject) — Ethereum account classification with feature engineering, missing baselines, no error bars. Our paper has a stronger dataset contribution but also has the claim-evidence gap.
- *BlockFound* (5.75, Reject) — blockchain anomaly detection foundation model with comprehensive baselines. Our paper's evaluation is weaker by comparison (no baselines).
- *EX-Graph* (6.33, Accept) — blockchain dataset bridging Ethereum and X. Our paper's dataset contribution is similar in spirit but the framing as an SSL method paper weakens it.
- *Rethinking pseudo-labeling* (5.00, Reject) — data-centric SSL paper with thorough evaluation. Our paper lacks the evaluation rigor.
- *Scalable Temporal-Spatial Framework* (3.00, Reject) — blockchain anomaly detection with GCNs, lacking novelty. Our paper has stronger dataset contribution.

The initial bracket was 3.0–5.5. After narrowing, the paper sits near FE-GNN (4.25) but slightly lower because its central claim is contradicted by its own evidence, which is more damaging than incremental novelty or missing baselines alone.

**Round-1 bracket:** 3.0–5.5. **Final score:** 4.0.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>