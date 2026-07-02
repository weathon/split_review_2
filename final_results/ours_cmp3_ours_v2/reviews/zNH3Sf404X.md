Now I have a solid calibration picture. Let me write the final review.

## Summary

This paper presents a large-scale Bitcoin CoinJoin transaction dataset (1.15B total, 163M CoinJoin), applies forensic features (KeyLinker address clustering, SSU complexity metrics), and evaluates supervised and semi-supervised classifiers (XGBoost, CatBoost, Random Forest) for detecting illicit flows. The central empirical finding is that One-Time Change (OTC) features consistently degrade performance while REUSE+CS+SSU features are robust — a pattern replicated across three model families and both supervised and semi-supervised settings. The paper claims three contributions: (1) a comprehensive dataset, (2) novel forensic features, and (3) a quality-driven semi-supervised framework that outperforms supervised learning.

## Strengths

1. **Large-scale data engineering effort.** The dataset covers Bitcoin up to block 882,421 (Feb 2025), with 163M CoinJoin transactions classified by SSU complexity (Table 1). At 1.15B total transactions, this is substantially larger than existing public benchmarks like Elliptic++, and if released cleanly would be a useful community resource for blockchain forensics research.

2. **Non-obvious negative finding about OTC features.** The paper systematically shows (Tables 2 and 3) that adding OTC features consistently *reduces* F1, precision, or ROC AUC across three tree-based model families in both supervised and semi-supervised settings. This is a practically relevant observation given the widespread use of OTC in blockchain analytics, and the replication across models and learning paradigms gives it weight.

3. **Sound domain-appropriate evaluation choices.** Using F1-score over accuracy (justified by the 12% positive rate), PR-AUC reasoning, stratified cross-validation, and class weighting are appropriate methodological decisions for this highly imbalanced forensic problem.

## Weaknesses

### Fatal
None.

### Major

1. **Claimed SSL outperformance is contradicted by the paper's own results.** The abstract and contributions list state that SSL "outperforms supervised baselines" and "proves" that success is driven by data quality. However, the best supervised XGBoost achieves F1=0.844–0.845 and ROC AUC=0.970 (Table 2, rows 250/270), while the best SSL XGBoost achieves F1=0.845 and ROC AUC=0.969 (Table 3, row 315). These are essentially identical. The paper acknowledges "the semi-supervised phase did not produce dramatic metric gains" (line 293) but nevertheless continues to claim outperformance. This is not a minor wording issue — the claim of SSL superiority is central to Contribution 3 and is not supported by the evidence presented.

2. **The "quality-driven SSL framework" described in principle is not what was implemented.** Section 5.2 describes a "Data Quality Principle" that *prioritizes* pseudo-labels based on SSU complexity class and KeyLinker clustering. But the actual pseudo-labeling procedure (Section 5.3, lines 228–230) is standard confidence-based thresholding: "only the most confident predictions are retained." No filtering step by SSU class or KeyLinker clusters is described or operationalized. The observation that confident predictions are "disproportionately found in the more tractable SSU complexity classes" (line 285) is a post-hoc claim, not an active mechanism. This means the paper's central methodological contribution — a quality-guided SSL framework — cannot be evaluated from the reported experiments.

3. **Missing the ablation needed to support the core thesis.** The paper claims that quality-guided pseudo-labeling matters more than data volume. But there is no comparison to unguided self-training (e.g., adding all pseudo-labels above a confidence threshold regardless of SSU class). Without this baseline, the reader cannot determine whether SSL dynamics contributed anything beyond what the supervised feature ablation already shows. The fact that Table 3 (SSL) follows the same feature-ranking pattern as Table 2 (supervised) suggests the finding is about feature quality in general, not anything SSL-specific.

4. **KeyLinker and SSU are cited to prior work but claimed as "novel" features.** Contribution 2 claims "Novel, high-fidelity features—KeyLinker address clustering and Shared Send Untangling (SSU) complexity metrics." KeyLinker is cited to Smolenkova & Yanovich (2025) with no description of any modification. The SSU complexity classes (regular, simple, separable, ambiguous, time-limit) are described exactly as in Larionov & Yanovich (2023); the paper mentions "enhanced" SSU metrics but never specifies what the enhancement is. Applying existing tools in a new context is legitimate, but claiming them as novel contributions without describing any substantive modification is an overstatement.

### Minor

5. **KeyLinker coverage is negligible relative to its billing.** KeyLinker clusters only 131.4K addresses out of 1.37B total (0.01%, Table 1). The paper repeatedly invokes KeyLinker as a central contribution and as a source of "high-fidelity signal" for pseudo-labeling, but never quantifies how many labeled or pseudo-labeled transactions actually involve KeyLinker-associated addresses. Without this information, the practical impact of KeyLinker on the results is unclear.

6. **Duplicated rows in Tables 2 and 3 hinder interpretation.** Multiple rows with identical feature checkmarks (all five features checked) report different metrics without any distinguishing column (e.g., Table 2 rows 265–267 for CatBoost, rows 272–274 for XGBoost). This likely reflects different hyperparameter configurations or pseudo-labeling batch sizes, but as presented the reader cannot determine which configuration produced which result.

7. **Number of pseudo-labels added per experiment is not reported.** The paper describes selecting the "top fraction" (line 228) of confident predictions but never states how many pseudo-labels were added, what fraction of the unlabeled pool this represents, or how this varied across feature sets. This makes it impossible to assess the scale of SSL's contribution.

### Trivial
None.

## Nice-to-Haves

- **Statistical significance/variance estimates.** The F1 differences between feature sets are small (0.01–0.02). While the consistent directional pattern across three model families and two settings provides some internal validation, variance estimates or significance tests would strengthen confidence in the results.
- **Characterize pseudo-label quality.** If the paper asserts that selected pseudo-labels are "disproportionately" from Simple/Separable SSU classes, a table showing the SSU composition of selected pseudo-labels would directly test this claim and connect the principle in Section 5.2 to actual outcomes.
- **Label noise characterization.** Labels come from heterogeneous off-chain sources with unknown accuracy. Some assessment of label quality would strengthen the "data quality" narrative.

## Removed Points

- **"Missing SSL baselines (FixMatch, MixMatch, etc.)"** — This paper is about SSL applied to blockchain forensics, not about proposing a new SSL algorithm. Demanding comparisons to modern SSL methods designed for vision/image domains is scope creep. The core comparison that *is* needed (unfiltered vs. quality-filtered self-training) is covered in Major weakness #3.
- **"Statistical significance"** — Moved to Nice-to-Have as a reasonable suggestion, not a core weakness. The consistent directional pattern across 6 model×paradigm combinations already provides some internal validation.
- **"OTC overclaim — the word 'prove' is too strong"** — The word "prove" (line 9, line 29) is indeed colloquial for an empirical demonstration, but this is common usage in ML papers and not a fatal flaw. The more serious overclaim is the SSL outperformance claim (Weakness #1).
- **Generic criticisms about "evaluation lacks rigor" without concrete anchor** — Removed as unfalsifiable.
- **Criticisms about reproducibility citing undisclosed hyperparameters or missing code** — Removed per guidelines; full training logs and code are impractical to include in a submission.
- **"Strengthening the Paper on Its Own Terms" suggestions** — These are constructive suggestions now incorporated into Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviewer synthesis confirms that the most coherent message is the feature ablation showing OTC is harmful, but this is already the paper's implicit content, albeit buried under overstated SSL framing.

## Suggestions

1. **Reframe the paper honestly.** The strongest contribution is the large-scale dataset and the systematic feature ablation showing that OTC features are harmful while REUSE+CS+SSU features are robust. Drop the "SSL outperforms supervised" framing, which is contradicted by the identical F1 scores.

2. **Either implement the quality-guided filtering or remove the Data Quality Principle framing.** The mismatch between Section 5.2 (principled filtering by SSU class and KeyLinker) and Section 5.3 (standard confidence thresholding) is the paper's most serious structural flaw. Comparing quality-filtered to unfiltered self-training would directly test the central thesis.

3. **Clarify what distinguishes the duplicated rows** in Tables 2 and 3 (add a column or table note). Report the number of pseudo-labels added per experiment.

4. **Explicitly acknowledge that KeyLinker and SSU are existing techniques** and reframe Contribution 2 as their systematic evaluation at unprecedented scale — which is itself a valid empirical contribution.

5. **Provide SSU-class statistics for selected pseudo-labels** to substantiate the claim that confident predictions are disproportionately from tractable SSU classes.

## Score and Decision

**Round 1 bracket:** After reviewing anchors in the 3.0–5.25 range, I bracket this paper between 3.5 and 5.0. It is stronger than the Ethereum anomaly detection paper (avg 3.00) which had thin novelty and arbitrary hyperparameters, and comparable to FE-GNN (avg 4.25) which also had overclaimed novelty but genuine empirical substance. It is weaker than Better Call Graphs (avg 5.25) which was a cleaner dataset contribution without overclaimed methodology. The paper's dataset and OTC finding are real contributions, but the gap between claimed SSL/novelty contributions and delivered evidence prevents it from reaching accept territory.

**Final score:** 4.0. The paper has a useful core but requires substantial reframing and additional experiments (particularly implementing the quality-guided filtering and comparing to unfiltered SSL) to support its advertised contributions.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>