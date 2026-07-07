Now I have enough to draft the review. Let me prepare it.**Round 1 Bracket:** Based on the calibration anchors, this paper sits between the score-3 range (Ethereum anomaly detection papers with incomplete methodology, rejected) and the score-5.75–6.33 range (blockchain foundation model and dataset papers with genuine novel contributions). The paper has a real dataset contribution and principled framing (closer to 5–6), but the headline SSL claim doesn't hold and the experimental tables have a structural presentation flaw that makes a key portion of results uninterpretable (closer to 3–4). **Initial bracket: 3 to 5.**

The closest anchor is yM7rw8Bo1f (FE-GNN Ethereum, avg 4.25) — a blockchain classification paper with feature engineering but more methodologically complete. The paper under review has a larger-scale dataset but weaker claim validity. I settle on **score 3.5**: the dataset contribution is real, but the central SSL claim is unsupported by the numbers, major table rows are uninterpretable, and the pseudo-labeling procedure is not reproducible.

---

## Summary
This paper introduces a semi-supervised learning (SSL) framework for detecting illicit Bitcoin Shared Send Mixer (CoinJoin) transactions. It contributes (1) a large-scale dataset of 163M CoinJoin transactions with SSM classification across Bitcoin's full history, (2) novel forensic features based on KeyLinker address clustering and SSU complexity metrics, and (3) empirical evidence that pseudo-label quality (driven by cryptographically grounded features) matters more than pseudo-label volume for SSL effectiveness.

## Strengths

- **Scale and completeness of the dataset (Table 1).** The dataset covers 1.15B total transactions, 163M CoinJoin transactions, and 4.6M labeled samples with multi-source off-chain labels integrated across Bitcoin's full history through block 882,421. This is a substantial and practical research resource.
- **Principled quality-vs-quantity framing (Section 5.2).** The argument that pseudo-label quality is tied to the cryptographic certainty of the underlying clustering heuristic is domain-specific and non-trivial. The paper correctly identifies that CoinJoin transactions by design violate the OTC single-change-output assumption, motivating preference for KeyLinker-derived clusters.
- **Feature ablation structure (Tables 2 and 3).** Systematically toggling five feature groups across three model families in both supervised and SSL regimes is the correct experimental design for testing the paper's thesis. The consistent pattern (OTC degrades; REUSE+SSU improve) replicates across all models.

## Weaknesses

### Fatal
None.

### Major

- **SSL does not improve over the supervised baseline, directly contradicting the headline claim.** The abstract states SSL "effectively leverages unlabeled data (F1-score: 0.84)." Comparing Table 2 and Table 3 directly: the best supervised XGBoost achieves F1=0.845 (DEFAULT+REUSE+CS+SSU), and the best SSL XGBoost also achieves F1=0.845 (same feature set). Section 6.3 explicitly concedes: *"The semi-supervised phase did not produce dramatic metric gains."* The actual defensible finding is that quality-filtered pseudo-labeling *maintains* performance while OTC-guided pseudo-labeling *degrades* it. That is a narrower claim than the paper's framing. The abstract, introduction, and conclusion all need to be rewritten to match what was actually demonstrated.

- **Tables 2 and 3 contain multiple rows with identical feature check patterns but different reported metrics, with no explanation of what varies.** In Table 2, CatBoost rows 5–7 all show ✓ in all five columns (DEFAULT, REUSE, CS, OTC, SSU) but report F1 = 0.800, 0.830, and 0.827 respectively. The same occurs for XGBoost (rows 5–7). In Table 3, XGBoost has four such rows (F1 = 0.814, 0.845, 0.836, 0.836). No caption, legend, or text explains what dimension varies between these rows. Since the paper's thesis rests on fine-grained feature-combination comparisons, this structural presentation flaw makes a substantial portion of the experimental results uninterpretable and unreproducible.

- **The pseudo-labeling procedure is under-specified to the point of non-reproducibility (Sections 5.3, 6.3).** Section 5.3 states only: *"we select the top fraction of samples on both sides of the decision boundary, adjusting the share of positives and negatives."* No fraction is given, no iteration count, no stopping criterion, and no operationalization of the SSU-class filtering (which classes are included, at what confidence threshold). For a paper whose central methodological contribution is quality-filtered pseudo-labeling, this is a critical gap.

### Minor

- **Address-to-transaction label mapping is not explained (Section 5.1).** Table 1 shows 33,229 illicit and 251,083 legal *addresses*, while 4.6M CoinJoin *transactions* are labeled with ~12% illicit (~552K). How address-level labels are aggregated into transaction-level labels — especially for transactions with mixed-label inputs — is not described. This matters for interpreting the 12% imbalance figure and the label quality.

- **"Prove" overstates the experimental evidence (Abstract, Introduction).** The paper states "we prove that common heuristics like OTC introduce noise." The experiments demonstrate a correlation between OTC inclusion and performance degradation; they do not establish causality. "We demonstrate" or "we provide evidence" would be accurate; "prove" is not.

### Trivial
None verified.

## Nice-to-Haves

- A controlled experiment that disentangles (a) using OTC features during model training from (b) using OTC clusters to select pseudo-labels would sharpen the quality argument from correlational to causal.
- The connection between CoinJoin's multi-party pooling structure and why it violates the OTC single-change-address assumption should be stated explicitly in the text; it is the theoretical justification for avoiding OTC and is currently only implied.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **Dataset availability conditioned on acceptance**: Standard practice; not a paper flaw. Removed per hard rule.
- **Comparison to prior baselines achieving 90–97% accuracy**: Retained as Minor only in spirit; demoted/removed as a standalone weakness because the task setting (SSM-specific, CoinJoin-only detection under extreme label scarcity) differs from the general illicit-transaction detection tasks in those prior papers. Without knowing whether comparison is appropriate, this cannot be a verified flaw.
- **Causal mechanism for OTC noise**: Partially absorbed into the "prove" overstatement point; the claim that demonstrating the mechanism is required for publication is scope creep. Removed as a standalone weakness.

## Novel Insights

The paper's most distinctive conceptual contribution — that OTC heuristics are particularly unreliable *specifically for CoinJoin detection* because CoinJoin structurally violates the single-change-address assumption underlying OTC — is never stated explicitly. If the authors articulated this, the quality-vs-quantity framing would have a clear theoretical foundation rather than resting solely on empirical correlations. This insight, if developed, would substantially strengthen the paper's scientific contribution.

## Suggestions

1. Rewrite the abstract and conclusion to accurately reflect the finding: quality-aware pseudo-labeling *prevents SSL degradation* rather than producing improvement over supervised baselines.
2. Fully specify the pseudo-labeling procedure: exact fraction selected, number of iterations, stopping criterion, and SSU classes used for filtering.
3. Resolve the undocumented rows in Tables 2 and 3 — identify and label the axis that varies (e.g., pseudo-label budget, SSU inclusion threshold) and make it an explicit table column.
4. Explicitly state the theoretical connection between CoinJoin's pooling structure and OTC's violated assumption to ground the feature quality argument.

---

## Score and Decision

**Anchor papers:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| nSDOkm0SKo.md | 1.00 | R1 | Unrelated financial news paper; far below |
| q7Xi4yZYcH.md | 3.00 | R1 | Ethereum anomaly detection; similar domain, similar methodological level |
| aXSxSu3fvg.md | 3.00 | R1 | SSL pseudo-labeling paper with missing specificity; similar weaknesses |
| yM7rw8Bo1f.md | 4.25 | R1 | FE-GNN blockchain classification; more methodologically complete |
| dpnPOXoqVQ.md | 4.75 | R1 | SSL with feature selection; stronger theoretical grounding |
| LPXfOxe0zF.md | 5.75 | R1 | Blockchain foundation model; deeper methodological contribution |
| juE0rWGCJW.md | 6.33 | R1 | Dataset paper linking Ethereum+X; accepted, genuine dataset novelty |
| Bo6GpQ3B9a.md | 7.00 | R1 | SSL theory paper; much stronger theoretical contribution |
| RvUVMjfp8i.md | 8.00 | R1 | SSL robustness paper; complete theory + experiments |

**Round 1 Bracket:** 3–5.

The paper has a real and large-scale dataset (comparable to juE0rWGCJW in that dimension) and a coherent framing. However, the central empirical claim (SSL effectiveness) is directly contradicted by the numbers, major experimental tables are structurally uninterpretable, and the pseudo-labeling procedure is not reproducible. These are not cosmetic issues — they affect the core scientific contribution. The paper is closest in overall quality and weakness profile to q7Xi4yZYcH (avg 3.0, Ethereum anomaly detection rejected for incomplete methodology) and aXSxSu3fvg (avg 3.0, SSL pseudo-labeling rejected for missing specificity), but slightly above them due to the genuine dataset scale and principled feature framing. Score: **3.5**.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>