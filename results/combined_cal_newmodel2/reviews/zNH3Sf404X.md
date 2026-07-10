Now I have all the evidence I need. Let me write the final consolidated review.

## Summary

This paper constructs a large-scale Bitcoin dataset (1.15B transactions, 163M CoinJoin transactions) with SSU complexity classification, applies KeyLinker and SSU features (from prior work) to distinguish illicit from licit CoinJoin transactions, and evaluates supervised and semi-supervised models (XGBoost, CatBoost, Random Forest). Its central thesis is that feature quality (KeyLinker, SSU) matters more than feature quantity (OTC) for SSL in blockchain forensics.

## Strengths

- **Large-scale, practically relevant dataset.** The paper constructs a dataset spanning 1.15B transactions with 163M CoinJoin transactions and SSU classification (Table 1). For blockchain forensics researchers, a labeled dataset of this scale for CoinJoin transactions is a genuine resource. The release commitment (line 199) adds concrete community value.

- **Well-motivated central thesis about feature quality.** Section 5.2 articulates a clear, principled argument: not all pseudo-labels are equally valuable, and quality should be assessed via structural complexity (SSU classes) and clustering fidelity (KeyLinker vs. OTC). This framing reframes the SSL narrative in a way that could inform future work.

- **Useful empirical finding about OTC vs. KeyLinker/SSU in the supervised setting.** The paper demonstrates that in supervised learning, feature combinations using KeyLinker and SSU outperform configurations adding OTC (Table 2: XGBoost F1=0.844 without OTC vs 0.841 with OTC). This directional finding about feature quality is of practical use to blockchain forensic practitioners.

## Weaknesses

### Fatal
None.

### Major

**1. The central claim that SSL "outperforms supervised baselines" (Contribution 3, line 29) is not supported by the evidence.**

The paper's title and headline contribution center on SSL. However:
- Best supervised F1 = 0.844 (Table 2, line 270, XGBoost, DEFAULT+REUSE+CS+SSU).
- Best SSL F1 = 0.845 (Table 3, line 315, XGBoost, ALL features).
- This is a 0.001 difference with no statistical significance reported — well within noise.
- When comparing the **same feature configuration** (DEFAULT+REUSE+CS+SSU), SSL actually performs **worse** than supervised (F1=0.839 in Table 3 line 312 vs 0.844 in Table 2 line 270).
- The SSL framework uses all labeled data plus 158M+ pseudo-labels, making it strictly more complex and less efficient while producing no meaningful gains.

The paper concedes (line 293) that SSL "did not produce dramatic metric gains," but this understates the severity: the SSL framework produced *no* measurable benefit. This undermines Contribution 3 as stated.

**2. KeyLinker and SSU are presented as "novel features" but are cited from prior work.**

The abstract (line 9) lists "Novel, high-fidelity features—KeyLinker address clustering and Shared Send Untangling (SSU) complexity metrics." The conclusion (line 331) calls them "Our novel features." However, KeyLinker is cited as Smolenkova & Yanovich (2025) and SSU metrics as Larionov & Yanovich (2023). Line 28 reads "We introduce the tools to extract quality from quantity: KeyLinker Smolenkova & Yanovich (2025)" — citing a prior paper is not introducing a method. The genuine contribution is computing these features on a new large-scale dataset and demonstrating their predictive value, which is a valid empirical finding, but presenting them as novel methodological contributions of *this* paper is misleading.

**3. The claim that OTC features degrade SSL performance is contradicted by the paper's own Table 3.**

The paper states (line 287): "the best results were consistently achieved with the `Default+REUSE+CS+SSU` feature set… adding the noisier OTC features degraded performance." However, Table 3 shows:
- For XGBoost, the DEFAULT+REUSE+CS+SSU (no OTC) row has F1=0.839 (line 312), while the best ALL-features row (which includes OTC) has F1=0.845 (line 315).
- For CatBoost, the DEFAULT+REUSE+CS+SSU (no OTC) has F1=0.829 (line 304), while the best ALL-features row has F1=0.834 (line 307).

In both cases, the configuration *with* OTC yields higher F1 than the one without. The paper's textual claims are at odds with its own tabular data.

**4. Tables 2 and 3 contain unexplained duplicate rows with identical feature checkmark patterns but different metrics, making the results uninterpretable.**

In Table 2, the "ALL features" row for each model appears 3 times with different metrics (e.g., CatBoost lines 265-267: F1=0.800, 0.830, 0.827 — all with identical checkmarks). The same pattern repeats in Table 3 with 3-4 copies per model. The paper states it uses "stratified 5-fold cross-validation" (line 224) but never explains whether these rows represent folds, hyperparameter variants, or different runs. Without this explanation, the reader cannot determine which row represents the paper's claimed result, and comparisons between feature sets cannot be trusted when the same configuration produces F1 scores varying by 0.03 or more.

### Minor

**5. No variance, confidence intervals, or significance tests are reported.** The paper uses 5-fold CV (line 224), which naturally yields variance estimates, but these are not provided. With differences at issue being on the order of 0.001–0.003, the reader cannot distinguish signal from noise.

**6. Pseudo-labeling implementation lacks quantitative specifics.** The paper describes selecting "the top fraction of samples" and "adjusting the share of positives and negatives" (line 228) without reporting the actual fraction, confidence threshold, number of pseudo-labeled samples added, or number of pseudo-labeling iterations. This is insufficient for reproducibility.

**7. No comparison to standard SSL baselines.** The paper compares SSL only to its own supervised models but not to standard SSL methods (self-training, co-training, FixMatch approaches, or graph-based SSL). Without this comparison, the claimed advantage of quality-aware pseudo-label selection cannot be evaluated.

**8. The SSU-class-based quality filtering claim is asserted but not ablated.** Section 5.2 claims that restricting pseudo-labels to Simple and Separable SSU classes improves quality, but this is never tested independently (e.g., by comparing performance with vs. without this restriction).

**9. The paper uses "prove" (abstract, line 29, line 331) for claims supported only by correlational evidence from one dataset with small metric differences.** This overclaims the strength of the evidence.

### Trivial
None.

## Nice-to-Haves

- Reframe the paper around the dataset and feature engineering analysis rather than SSL. The null SSL result (SSL adds no measurable benefit) is worth reporting but should not be positioned as a positive contribution.
- Clean up Tables 2 and 3: each experimental configuration should have exactly one row with clear labels and reported mean ± std across cross-validation folds.
- Add statistical significance testing (McNemar's test or paired bootstrap) for all feature-set comparisons.
- Add controlled comparison to standard SSL baselines (self-training, FixMatch) using identical base models.
- Report precise pseudo-labeling parameters: confidence threshold, fraction retained per class, number of iterations.
- Add an ablation validating the SSU-class-based quality filtering claim.

## Removed Points

These points were identified in the input review but removed per filtering rules:

- **Strength about OTC degradation being "internally consistent across two tables"** — removed because this conflicts with verified Weakness #3 (Table 3 contradicts the OTC degradation claim).
- **Criticism that related work is a "catalog"** — removed as too subjective and not a concrete, verifiable weakness.
- **Rewriting/presentation suggestions already covered in Nice-to-Haves.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The paper's genuine value lies in the large-scale CoinJoin dataset and the empirical finding that KeyLinker and SSU features outperform OTC for supervised illicit transaction detection. The single highest-leverage revision is to recalibrate the claims: drop the unsupported SSL outperformance assertion, report the SSL result as a null finding (which is itself interesting given the large pool of unlabeled data), and reframe the paper around the feature engineering analysis and dataset contribution. The tables must be repaired to make each experimental configuration interpretable.

## Score and Decision

**Calibration summary:** I compared this paper against 9 anchors retrieved across two calibration rounds. The closest topical anchors are:
- **q7Xi4yZYcH (avg 3.00)** — Ethereum anomaly detection with TRW-GCN. Rejected for lack of novelty and weak baselines. Our paper has a stronger dataset but more severe presentation flaws (uninterpretable tables, text-table contradictions).
- **yM7rw8Bo1f (avg 4.25)** — FE-GNN Ethereum account classification. Rejected for incremental novelty and no error bars. Our paper has a larger dataset but its experimental presentation is worse (FE-GNN's tables are interpretable; ours are not). The unsupported SSL claim and text-table contradictions are additional weaknesses FE-GNN does not share.
- **nwjgeFGbAF (avg 5.25)** — Better Call Graphs dataset for malware classification. Mixed reviews (3-8); some reviewers found the dataset contribution insufficient for a top venue. Our paper has a more impressive dataset scale but weaker analysis and presentation.

**Round-1 bracket:** 2.5–4.5. **Round-2 narrowing:** the paper's dataset contribution is real, placing it above the 1.0–2.5 papers, but the uninterpretable tables, unsupported core claim, and text-table contradictions place it clearly below FE-GNN (4.25) and BCG (5.25). Within the 2.5–4.5 bracket, the paper is near the lower end due to the severity of the presentation issues.

**Final score: 3.0.** The dataset has value, and the feature quality thesis is directionally correct. However, the unsupported SSL headline claim, the contradiction between the paper's text and its own tables, and the uninterpretable duplicate-row tables mean the paper, in its current form, does not deliver on its stated contributions.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>