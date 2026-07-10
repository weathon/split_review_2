Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper tackles illicit transaction detection in Bitcoin CoinJoin transactions, proposing a semi-supervised learning framework guided by a "quality over quantity" principle. It contributes (1) a large-scale dataset of ~1.15B transactions (163M CoinJoin) up to February 2025, (2) feature engineering using KeyLinker address clustering and SSU complexity metrics, and (3) an SSL/pseudo-labeling framework that claims to outperform supervised baselines when guided by high-quality features rather than noisy heuristics like OTC.

## Strengths

- **Large-scale, up-to-date dataset.** The paper compiles blockchain data up to block 882,421 (February 2025), covering ~1.15B total transactions and 163M CoinJoin transactions with SSU classification. Table 1 documents the scope clearly, and the authors commit to releasing the dataset. This is a genuinely useful resource for the blockchain forensics community.

- **Well-motivated conceptual framing.** The distinction between data quality and data quantity applied to pseudo-labeling is sound. The idea that pseudo-labels from structurally simpler transactions (SSU Simple/Separable) and cryptographically grounded clustering (KeyLinker) are preferable to those from noisier heuristics (OTC) is clearly articulated in Section 5.2 and provides a principled lens for the work.

- **Practical relevance.** Detecting illicit flows in CoinJoin transactions is a hard, adversarial domain with direct law-enforcement applications. Label scarcity and deliberate obfuscation make this a meaningful testbed for SSL methods.

## Weaknesses

### Fatal
None.

### Major

1. **Claim-evidence mismatch on SSL outperforming supervised.** The introduction (line 29) states SSL "outperforms supervised baselines by leveraging unlabeled data strategically," but the best XGBoost F1-score is 0.845 in both the supervised setting (Table 2, line 250) and the SSL setting (Table 3, line 315). For CatBoost the delta is only +0.004 F1 (0.830 vs. 0.834). The paper acknowledges SSL "did not produce dramatic metric gains" (line 293) but never reconciles this with the "outperforms" language in the abstract, introduction, and conclusion. The headline claim is not supported by the evidence as presented; the paper would need to either demonstrate a statistically significant improvement or reframe the claim to reflect that SSL *matches* supervised performance while using fewer initial labels (an experiment not conducted).

2. **No statistical significance or variance reporting despite reliance on tiny F1 differences.** The paper's central narrative about feature quality — that OTC degrades performance and SSU improves it — rests on F1 differences of 0.005–0.01 points. Although 5-fold cross-validation is used, no standard deviations, confidence intervals, or statistical tests are reported anywhere. The reader cannot determine whether any observed difference reflects a genuine effect or random variation. For example, the difference between XGBoost SSL with vs. without OTC is only 0.003 F1. This is the single most consequential methodological gap: without variance information, the paper's core empirical claims are unverifiable.

3. **The SSL pseudo-labeling procedure is critically underspecified.** The description (lines 226–230) does not report: how many pseudo-labeled samples were added in absolute terms, what fraction/percentile threshold was used, whether pseudo-labels were added in one shot or iteratively, how the positive/negative ratio was adjusted, or what specific filtering by SSU class or KeyLinker was actually applied. Without these details, the SSL results cannot be interpreted or reproduced. If only a trivial number of pseudo-labels survived the "quality" filter, the SSL model would be nearly identical to the supervised model — which would perfectly explain the near-identical F1 scores. The paper's central SSL claim cannot be assessed without this information.

### Minor

4. **Novelty attribution of "novel features" is unclear.** KeyLinker is attributed to Smolenkova & Yanovich (2025) and SSU metrics to Larionov & Yanovich (2023). The paper calls these features "novel" and claims to "introduce" them (contribution 2, line 28), but what exactly constitutes a novel contribution beyond applying existing techniques to this specific setting is not clearly delineated. The REUSE feature is connected to KeyLinker (line 248: "key reuse") but the connection could be stated more explicitly to avoid confusion.

5. **Claim that OTC degrades performance is not uniformly supported.** While the paper states OTC features "reduced metrics" (line 248), the evidence is more mixed across models and configurations. Some OTC-inclusive vs. OTC-exclusive comparisons show differences within 0.003–0.004 F1, and the pattern is not equally clear for all models. A more measured characterization would strengthen credibility.

### Trivial
None.

## Nice-to-Haves

- Show a controlled comparison where pseudo-label quality (quality-filtered vs. unfiltered) is explicitly varied while holding the *number* of pseudo-labels constant, to directly demonstrate the claimed quality effect.
- Report the number of pseudo-labels added in each condition and their breakdown by SSU class and clustering heuristic.
- Analyze how often CS/OTC/KeyLinker produce conflicting label assignments, since the problem statement (line 161) assumes perfect propagation through clustering relationships.
- Compare against other SSL approaches beyond self-training (e.g., graph-based SSL) to test generality.

## Removed Points

These points were identified in the review process but are either parser artifacts, factual misunderstandings, scope-creep demands, or speculative claims that do not meet the standard for inclusion as weaknesses:

- **Garbled table checkmarks producing "different results for same feature set":** This is a parser artifact (the PDF-to-text conversion), not an author error.
- **Paper does not improve upon GNNs achieving 91–92% accuracy:** Those accuracy figures are on different datasets/tasks and are not directly comparable to F1-score on CoinJoin data.
- **Missing comparison to FixMatch/MixMatch/graph-based SSL:** This demands methods not standard in this application domain; moved to nice-to-haves.
- **Label-propagation error not analyzed:** A valid suggestion for future work but not a core flaw in the current paper.
- **KeyLinker only covers 131.4K addresses vs. 859M by CS:** The paper does not claim KeyLinker is the primary clustering method; it is presented as a higher-fidelity supplement. This is a factual observation, not a weakness.

## Novel Insights

None beyond the paper's own contributions. The review surfaces no perspective that the paper itself does not already articulate.

## Suggestions

1. **Bring claims into alignment with the evidence.** Remove or substantially soften the "outperforms" language for SSL vs. supervised learning unless a statistically significant improvement can be demonstrated — e.g., by showing F1 as a function of labeled-set size and showing that SSL reaches the same F1 with fewer labels.
2. **Report means and standard deviations across cross-validation folds** for all metrics, and ideally include a statistical test (e.g., corrected paired t-test) for key comparisons (OTC vs. no OTC, SSL vs. supervised).
3. **Fully specify the pseudo-labeling procedure:** number of samples added per iteration, confidence thresholds, positive/negative ratio adjustment, and any filtering criteria by SSU class or clustering heuristic.
4. **Clarify novelty attribution.** Explicitly state which components are novel contributions of this paper vs. applications of prior work, and clarify the relationship between the REUSE feature and KeyLinker.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>