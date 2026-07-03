Now let me write the final consolidated review.

## Summary
This paper proposes a semi-supervised learning framework for detecting illicit Bitcoin CoinJoin transactions. Its main contributions are: (1) a large-scale dataset of 163M CoinJoin transactions with SSU complexity classification, (2) the application of KeyLinker address clustering and SSU untangling metrics as features, and (3) a quality-guided pseudo-labeling strategy that prioritizes structurally cleaner transactions. The central thesis is that SSL success depends on feature quality rather than data volume.

## Strengths
- **Large-scale CoinJoin dataset with multi-source labels and SSU classification (Table 1)**: The paper assembles 163.4M CoinJoin transactions classified by SSU complexity (simple, separable, ambiguous, time-limit, regular) and integrates multiple labeling sources (WalletExplorer, Elliptic++, MBAL, Kaggle). With 4.6M labeled CoinJoin transactions and 33K illicit addresses, this is the first dataset at this scale annotated with structural mixing properties—a potentially useful resource for the blockchain forensics community.

- **Systematic feature ablation across three model families in both supervised and SSL settings (Tables 2 and 3)**: The paper evaluates 7 feature configurations (DEFAULT, REUSE, CS, OTC, SSU in various combinations) under CatBoost, XGBoost, and Random Forest—first in supervised mode, then under pseudo-labeling. The consistent pattern across all six panels (OTC features produce slightly worse F1 than the REUSE+CS+SSU combination) lends weight to the feature-quality argument, even if the differences are small.

- **Domain-adapted pseudo-labeling principle (Section 5.2)**: Rather than standard confidence-thresholding, the framework conditions pseudo-label selection on SSU complexity class (prioritizing Simple and Separable transactions) and KeyLinker clusters over OTC-based clusters. This is a sensible domain-specific adaptation that translates blockchain structural knowledge directly into the training-signal selection process.

## Weaknesses

### Fatal
None.

### Major
1. **Overclaimed novelty of features**: The abstract and introduction label KeyLinker and SSU metrics as "Novel, high-fidelity features" (Contribution 2). However, the paper itself attributes KeyLinker to Smolenkova & Yanovich (2025) and SSU metrics to Larionov & Yanovich (2023) (Section 5.1, Section 1). These are existing forensic techniques being applied in a new context, not novel features introduced by this paper. The framing in the abstract ("Novel, high-fidelity features"), introduction ("We introduce the tools"), and conclusion ("Our novel features") is misleading and misrepresents what is actually new in the work.

2. **SSL did not meaningfully improve over supervised learning**: The best supervised F1 is 0.844 (XGBoost, Table 2, Default+REUSE+CS), and the best SSL F1 is 0.845 (XGBoost, Table 3, all features)—an improvement of 0.001, which is essentially flat. Contribution 3 (Section 1) states that "a semi-supervised learning framework outperforms supervised baselines by leveraging unlabeled data strategically," but the data show no meaningful outperformance. While Section 6.3 acknowledges "the semi-supervised phase did not produce dramatic metric gains," this is not reconciled with the paper's overall framing, which implies SSL effectiveness is a key result.

3. **No uncertainty estimates for the small metric differences that carry the argument**: The paper's central claims—that OTC features "degrade performance" and that KeyLinker/SSU features improve it—rest on F1 differences of 0.001–0.03 (Tables 2, 3). No confidence intervals, standard deviations, or statistical significance tests are reported anywhere. Given the extreme class imbalance (33K illicit addresses out of 1.37B), these differences could easily arise from random variation. Without uncertainty quantification, the reader cannot evaluate whether the observed patterns are meaningful.

4. **No SSL-specific baselines compared**: The framework is compared only to supervised versions of the same models. There is no comparison to standard pseudo-labeling without quality filtering, nor to any other SSL method (e.g., FixMatch, MixMatch). Without an ablation that contrasts quality-aware pseudo-labeling against vanilla pseudo-labeling using the same feature sets, it is impossible to attribute any observed effects to the "quality awareness" mechanism rather than the generic effect of adding confident predictions.

5. **Central thesis ("quality over quantity") is not directly tested**: The experiments compare feature sets but do not vary dataset size with and without quality filtering. The conclusion states that "models trained on strategically expanded high-quality data outperform those trained on larger, noisier datasets," but no experiment in the paper tests this claim directly. The results show that some features perform better than others—a feature-engineering finding, not evidence that data quality matters more than data quantity in SSL.

### Minor
6. **Missing details on pseudo-labeling process**: The paper does not report the number of pseudo-labels added, their SSU complexity distribution, what fraction of the unlabeled pool they represent, or how the "top fraction" threshold was determined. Since the quality-awareness mechanism is central, these details are needed for reproducibility and to support the claim that pseudo-labels are "disproportionately found in the more tractable SSU complexity classes."

7. **Tension between formalism and practice**: Section 4 assumes tags propagate perfectly through clustering relationships (∀A,A': A∼A' ⟹ Tag(A)=Tag(A')), but Section 5.1 acknowledges "manually resolved duplicates and conflicting labels." This discrepancy between the formal model and the practical pipeline is not addressed.

### Trivial
8. **Confusing table layout: duplicate-appearing rows**: In both Tables 2 and 3, multiple rows within each model group show identical checkmark patterns (all features selected) but different metrics. It is unclear what varies between these rows (hyperparameters? thresholds?). Additionally, Table 3 contains apparent duplicate rows (e.g., CatBoost lines 308-309, XGBoost lines 316-317, RandomForest lines 322-323) that may be parsing artifacts but create confusion.

## Nice-to-Haves
- Include at least one SSL baseline (e.g., standard pseudo-labeling without quality filtering) to isolate the effect of the quality-awareness mechanism.
- Report confusion matrices to help assess the precision-recall tradeoff claimed in Section 6.3.
- Provide a brief self-contained explanation of how KeyLinker works (beyond "cryptographic key reuse patterns") for self-containedness.

## Removed Points
- "Dataset will only be released upon acceptance" — Hard rule: do not question existence/availability of cited resources.
- "Cannot be independently verified" — Hard rule: cited entities are assumed to exist.
- "Missing related works" — Hard rule: do not assert missing related works without external verification.
- "Tables are difficult to interpret" (as a major weakness) — Partially a parser artifact; retained only as trivial formatting note above.
- Various formatting, typos, and parser artifact complaints — Hard rule: parser errors, not author errors.

## Novel Insights
None beyond the paper's own contributions. The reviewer analyses confirm the paper's stated contributions and flaws without surfacing unexpected cross-cutting findings.

## Suggestions
1. **Correct the framing**: KeyLinker and SSU metrics are existing techniques applied in a new context. Remove "novel" from their description and clarify that the novelty lies in their application within a quality-guided SSL pipeline for this specific domain.
2. **Add error bars**: Report standard deviations over cross-validation folds or independent runs for all metrics in Tables 2 and 3.
3. **Add a controlled SSL baseline**: Compare quality-aware pseudo-labeling against standard pseudo-labeling (all confident predictions regardless of feature source) to directly test the quality-awareness mechanism.
4. **Report pseudo-label statistics**: Number of pseudo-labels added, their SSU complexity distribution, and how the selection threshold was determined.
5. **Either add a dataset-size experiment or temper the claims**: If the paper cannot directly test "quality over quantity," it should not claim to have proven this thesis. The results support a narrower claim: that some feature sets work better than others for illicit CoinJoin detection.
6. **Acknowledge the flat SSL result**: Discuss why SSL did not improve over supervised learning, and reframe the contribution accordingly rather than presenting SSL as a demonstrated success.

## Score and Decision

After evaluating the paper against its own stated claims, the core issues are: (1) the "novel features" contribution is misleading since both KeyLinker and SSU metrics are cited as prior work; (2) the central experimental result (SSL vs. supervised) shows no meaningful improvement (F1: 0.844 vs 0.845); (3) the small metric differences supporting the paper's key claims lack any uncertainty quantification; (4) no SSL-specific baselines are compared; and (5) the "quality over quantity" thesis is not directly tested. The paper has real value in its dataset contribution and systematic feature ablation, and the domain-adapted pseudo-labeling idea is sensible. However, the evidence does not support the advertised claims, and the framing is overstated. The paper merits a score between borderline reject and borderline accept, recognizing the useful elements while reflecting that the core claims are not convincingly demonstrated.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>