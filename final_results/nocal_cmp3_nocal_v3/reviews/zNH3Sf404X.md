Now I have all the evidence I need. Let me produce the final consolidated review.

## Summary
This paper tackles illicit transaction detection in Bitcoin CoinJoin (Shared Send Mixer) transactions. It contributes (1) a large-scale dataset of ~163M CoinJoin transactions with labels, (2) novel forensic features (KeyLinker address clustering and SSU complexity metrics), and (3) a semi-supervised learning framework with selective pseudo-labeling guided by these features. The central thesis is that data quality, not just quantity, drives SSL performance in blockchain forensics.

## Strengths
1. **Large-scale, well-structured dataset.** The paper compiles ~1.15B transactions, identifies 163M CoinJoin transactions, and labels 4.6M with SSU complexity classes and service-category labels, spanning Bitcoin history up to February 2025. This is substantially larger than prior public efforts and, if released, would be a genuine community resource.

2. **Appropriate evaluation metrics.** The paper correctly avoids accuracy (given ~12% illicit fraction) and uses F1, ROC-AUC, and PR-AUC, acknowledging the precision-recall trade-off relevant to forensic analysts.

3. **Clear motivating thesis.** The claim that feature quality (e.g., KeyLinker's cryptographic key reuse) matters more than feature quantity (e.g., the OTC heuristic) for SSL in blockchain forensics is well-motivated and domain-appropriate.

## Weaknesses

### Major

1. **SSL results do not demonstrate improvement over supervised learning, yet the paper claims they do.** 
   - Supervised best (XGBoost, Table 2): F1 = 0.844, ROC-AUC = 0.970.
   - SSL best (XGBoost, Table 3): F1 = 0.845, ROC-AUC = 0.969.
   - The difference (F1 +0.001, ROC-AUC –0.001) is measurement noise.
   - The paper acknowledges "did not produce dramatic metric gains" (line 293) but the abstract, introduction (line 29: "a semi-supervised learning framework outperforms supervised baselines"), and conclusion (line 331: "models trained on strategically expanded high-quality data outperform those trained on larger, noisier datasets") claim SSL effectiveness and superiority. These prose claims are inconsistent with the experimental evidence.

2. **No comparisons to any existing SSL method or prior detection baseline.** 
   The paper evaluates three tree-based models within its own pipeline but does not compare against any established SSL algorithm (e.g., self-training with different selection criteria, co-training, or any SSL approach from the literature) nor against prior CoinJoin/illicit detection work (e.g., the GNN-based and ensemble methods achieving 90%+ accuracy that the paper itself cites in Section 3). Without baselines, the reader cannot assess whether the proposed approach advances the state of the art.

3. **Experimental design does not test the label-scarce regime that motivates the work.**
   The paper motivates SSL by arguing that "supervised approaches require extensive labeled datasets—a critical barrier" (line 23). However, the experiments train on 80% of 4.6M labeled transactions (~3.7M examples). A label-scarce regime (e.g., 1%, 5%, 10% of labeled data) is never tested. This is the scenario where SSL would be expected to show its value, and its absence is a significant gap relative to the paper's own framing.

4. **Pseudo-labeling procedure is critically under-specified.**
   The paper states it "select[s] the top fraction of samples on both sides of the decision boundary, adjusting the share of positives and negatives" (line 228). Essential details are absent: the fraction selected, number of pseudo-labeling rounds (one-shot vs. iterative), total number and proportion of pseudo-labels added, and any estimate of pseudo-label accuracy or quality filtering. Without these, the experiment is not reproducible and the "quality-aware" claim cannot be assessed.

5. **OTC "noise" claim rests on negligible differences without significance testing, and the best SSL result contradicts the claim.**
   - The paper states OTC features "introduce noise" and "degraded performance" (lines 248, 287). In Table 2, adding OTC to DEFAULT+REUSE+CS changes F1 from 0.844 to 0.841 (Δ = –0.003) — consistent with noise, not a demonstrated degradation.
   - Critically, the best SSL result (Table 3, line 315: F1=0.845) is from a configuration that *includes* OTC (all five feature groups checked). The text claims the best results come from `Default+REUSE+CS+SSU` (without OTC), but the table does not contain a row matching that configuration; the actual best row includes OTC.
   - No standard deviations, confidence intervals, or significance tests are reported. The rhetorical framing ("prove that common heuristics like OTC... introduce noise," abstract) exceeds what the data support.

6. **Factual inconsistency between text and tables for the best feature configuration.**
   - **Supervised (line 250):** Text says best result is "F1-score of 0.845 (default+reuse+cs+ssu)." Table 2 has NO row matching DEFAULT+REUSE+CS+SSU without OTC. The closest row (DEFAULT+REUSE+CS, no SSU, line 270) shows F1=0.844.
   - **SSL (line 287):** Text says "best results were consistently achieved with the `Default+REUSE+CS+SSU` feature set." Table 3 has no such row; the best result (F1=0.845, line 315) includes OTC, which contradicts the paper's claim that OTC degrades performance.
   - These discrepancies make the reported best results partially unverifiable from the tables as presented.

### Minor

7. **KeyLinker coverage limitation is not discussed.** KeyLinker clusters only 131.4K addresses out of 1.37B (≈0.01%, Table 1). The paper never addresses how a feature derived from 0.01% of addresses can drive SSL performance on millions of transactions. This is relevant to the central claim about KeyLinker's importance.

8. **Labeling pipeline quality is not examined.** The paper merges labels from four sources with different methodologies and reliability, and "manually resolved duplicates and conflicting labels" (line 199) without describing the resolution protocol, quantifying conflict rates, or validating against any ground truth. For a paper whose thesis is that data quality matters, the quality of the underlying label set receives no scrutiny.

9. **Discrepancy between claimed precision/recall changes and table data.** The paper states "Pseudolabeling slightly increased recall (up to +0.03) while reducing precision (from -0.04 to -0.05)" (line 291). For the best XGBoost configuration, supervised vs. SSL shows precision unchanged (0.897→0.897) and recall essentially unchanged (0.796→0.797). The claimed ranges do not cleanly match any specific configuration in the paired tables.

### Trivial

10. **Ambiguous table rows.** Multiple rows in Tables 2 and 3 share identical checkmark patterns but report different metrics, with no explanation (e.g., three consecutive CatBoost rows in Table 2, all with ✓✓✓✓✓, show F1=0.800, 0.830, 0.827). The paper does not explain whether these reflect different hyperparameter configurations, random seeds, or train/validation splits.

## Nice-to-Haves
- **Measure pseudo-label accuracy directly:** Instead of inferring "quality" from the feature source, report whether pseudo-labels from SSU Simple vs. Ambiguous transactions actually differ in accuracy.
- **Add error analysis:** What types of transactions are misclassified? Are errors concentrated in certain SSU complexity classes?
- **Add statistical significance measures** (standard deviations, confidence intervals) for all metrics, especially since key claims hinge on small differences.
- **Isolate KeyLinker's marginal contribution more cleanly** with a controlled ablation: Default+KeyLinker vs. Default+OTC vs. Default+CS, with confidence intervals.

## Removed Points
- "KeyLinker is never tested as an independent variable" — REMOVED (factually incorrect): Table 2 explicitly tests DEFAULT+REUSE without CS or OTC (F1 improves from 0.814 to 0.837 for XGBoost).
- "Section 5.2 presents the data quality principle as a hypothesis, not a demonstrated fact" — REMOVED: the paper explicitly says "We hypothesize" (line 207), which is appropriate; it then tests the hypothesis experimentally.
- "Section 3 does not establish a clear gap" — REMOVED: subjective assessment; the paper does cite prior work and positions its contribution.
- Various generic suggestions (error analysis, confidence intervals, more ablations) — MOVED to Nice-to-Haves.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Honestly reframe the contribution.** The dataset and feature engineering have independent value. Present the SSL results as showing the supervised model was near-saturated and the key insight is about feature quality driving performance, not SSL gains per se.
2. **Fix table-to-text discrepancies.** Ensure that claimed feature configurations (e.g., "default+reuse+cs+ssu") have corresponding rows in the tables, and that the text accurately describes what the tables show.
3. **Add a label-scarce experiment.** Train on 1%, 5%, 10% of labeled data and show that quality-aware pseudo-labeling recovers more performance than alternatives. This directly tests the paper's motivating scenario.
4. **Document the pseudo-labeling protocol fully:** selection fraction, number of rounds, total pseudo-labels added, and estimated accuracy.
5. **Address the KeyLinker coverage limitation explicitly** in the discussion.

## Score and Decision
MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>