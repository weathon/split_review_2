Now let me produce the final review based on the verified evidence and the impact scores.

## Summary

This paper tackles illicit Bitcoin transaction detection in CoinJoin/Shared Send Mixers, arguing that feature quality matters more than data volume in semi-supervised learning. It presents (1) a large labeled dataset of 163M CoinJoin transactions, (2) a feature engineering pipeline incorporating KeyLinker clustering and SSU complexity metrics, and (3) an SSL framework using pseudo-labeling. The dataset and ablation study are genuine contributions, but the paper's central claims are not supported by the evidence presented.

## Strengths

- **Massive dataset contribution (Section 5.1, Table 1):** 1.15B total transactions, 163M CoinJoin transactions with SSM classification spanning Bitcoin's full history to February 2025. This is a genuine resource if released upon acceptance.
- **Clean feature ablation study (Tables 2 and 3):** Systematic comparison across feature subsets (Default, +REUSE, +CS, +OTC, +SSU) makes marginal contributions straightforward to assess.
- **Honesty about SSL limits (Section 6.3):** The paper candidly acknowledges that SSL "did not produce dramatic metric gains" and that pseudo-labeling increased recall at the cost of precision.

## Weaknesses

### Major

- **The claim that SSL "outperforms" supervised learning is unsupported (lines 9, 29; Tables 2–3).** The abstract and contributions state SSL "outperforms supervised baselines," but the best SSL XGBoost F1 (0.845) and best supervised XGBoost F1 (0.844 per Table 2; 0.845 per the paper's own text at line 250) differ by at most 0.001. No confidence intervals or significance tests are reported. This directly undermines Contribution 3.

- **No comparison to existing methods from prior work (Section 3 vs. Section 6).** The paper cites methods achieving 92% accuracy (Nerurkar 2022), 91% accuracy across 16 classes (Nerurkar et al. 2021), and 97% detection of mixing services (Rathore et al. 2022), yet the experimental section compares only XGBoost, CatBoost, and Random Forest on the authors' own feature sets. No prior method is replicated on the same data, leaving the F1 of 0.84 uncontextualized against the state of the art.

- **KeyLinker is attributed to prior work but billed as a "novel" contribution (lines 9, 28, 331).** Contribution 2 and the Abstract present KeyLinker as a "novel, high-fidelity feature" introduced by this paper. However, KeyLinker is cited as Smolenkova & Yanovich (2025) — external prior work. The paper does not describe how KeyLinker works, what distinguishes it from standard public-key clustering, or what the present authors contributed beyond using it.

- **No variance or confidence intervals reported (Section 6.2–6.3).** Despite using stratified 5-fold cross-validation (line 224), all metrics (precision, recall, F1, ROC AUC) are reported as point estimates only. All comparative claims — feature importance (OTC vs. no OTC), SSL vs. supervised — lack error bars, so the reader cannot assess whether any reported difference is meaningful.

### Minor

- **The claim that OTC features "introduce noise" is overstated (Abstract, lines 248, 287; Table 2).** The paper repeatedly asserts OTC is harmful, but the F1 drops when adding OTC are 0.003 (XGBoost), 0.001 (CatBoost), and 0.004 (Random Forest). While the pattern is consistent (OTC always slightly hurts), the effect sizes are trivially small and unreported with confidence intervals. The evidence supports "OTC is essentially neutral" rather than "OTC introduces noise."

- **The quality-aware pseudo-labeling claim is asserted but not directly validated (Sections 5.2, 6.3).** The paper argues that pseudo-labels from high-fidelity features are better and asserts confident predictions "are disproportionately found in the more tractable SSU complexity classes" (line 285), but never quantifies this. No analysis shows the SSU-class distribution of selected pseudo-labels, the precision of pseudo-labels from different feature regimes, or the fraction from Simple/Separable vs. Ambiguous/Time-limited transactions. The selection mechanism is standard confidence-threshold pseudo-labeling, not an explicit feature-quality filter.

- **Insufficient detail on label conflict resolution (line 199).** The paper says "We manually resolved duplicates and conflicting labels" but provides no information on how many conflicts existed, the proportion requiring adjudication, the resolution rules, or inter-annotator agreement. This is important for a dataset contribution that is a primary claimed deliverable.

### Trivial

None.

## Nice-to-Haves

- Replicate at least one prior method (e.g., the semi-supervised GNN from Nerurkar 2022) on the same dataset to contextualize the F1 of 0.84.
- Report per-fold results or confidence intervals for all main metrics.
- Provide a brief technical description of KeyLinker for self-containedness, and clarify which features are novel vs. adopted from prior work.
- Include a data card with details on label conflict frequency and resolution rules.

## Removed Points

- "The dataset cannot be evaluated because it is not released": Removed per hard rule — criticism about release status/availability is not permitted; the dataset commitment is standard.
- "SSL methodology is rudimentary": Removed — the paper does not claim SSL method novelty; its contribution is the application and quality-over-quantity framing.
- "Table formatting issues / duplicate rows": Removed — formatting artifacts are parser errors, not author errors.
- "The central thesis is directionally sound" (from strengths): Removed as generic and conflicts with verified weaknesses about overclaiming.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Restructure the paper to honestly position its contributions: the dataset and feature ablation study are valuable; drop or substantially weaken the "SSL outperforms supervised" and "OTC introduces noise" claims, which are not supported by the data.
2. Replicate at least one prior method to give the reader context for the reported F1 of 0.84.
3. Add confidence intervals or per-fold breakdowns to all main tables.
4. Directly measure pseudo-label quality by SSU class and feature regime to validate the quality-aware selection thesis.
5. Clarify the provenance of KeyLinker and SSU metrics — what is adopted from prior work vs. what is newly contributed.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>