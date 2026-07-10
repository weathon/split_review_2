Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper tackles illicit Bitcoin transaction detection in CoinJoin (Shared Send Mixer) transactions. It makes three claimed contributions: (1) a large-scale dataset of 163M CoinJoin transactions with SSM classification; (2) novel forensic features (KeyLinker address clustering, SSU complexity metrics); and (3) a demonstration that semi-supervised learning (SSL) effectively leverages unlabeled data (F1≈0.84) when guided by quality-focused features, establishing a "quality over quantity" principle for blockchain forensics.

## Strengths

- **Dataset scale is genuinely impressive.** The paper compiles 163M CoinJoin transactions and ~1.15B total transactions with SSU classification (Table 1). This is larger than any public Bitcoin forensic dataset this reviewer is aware of, and release upon acceptance would be a real community resource. [impact: +9.80]

- **Clear negative result on OTC features.** Tables 2 and 3 consistently show that adding One-Time Change (OTC) features degrades or fails to improve performance across multiple models. This is a non-obvious, practically useful empirical finding for practitioners building Bitcoin forensic tools. [impact: +10.00]

- **Honest reporting of SSL limitations.** The paper acknowledges (Section 6.3) that "the semi-supervised phase did not produce dramatic metric gains" and that pseudo-labeling trades precision for recall. This candor is rare and refreshing. [impact: +9.84]

## Weaknesses

### Fatal
None.

### Major

1. **Central thesis (SSL success via quality features) is not supported by the evidence.** The paper claims SSL "effectively leverages unlabeled data" and "outperforms supervised baselines" (line 29), but the best supervised XGBoost achieves F1=0.844 (Table 2, line 270) while the best SSL XGBoost achieves F1=0.845 (Table 3, line 315) — essentially identical. For the *same* feature configuration (Default+REUSE+CS), supervised F1=0.844 and SSL F1=0.839, meaning SSL is marginally worse. The claim that SSL "improves robustness" (line 293) is also untested — no perturbation, distribution-shift, or noise-robustness experiment is conducted. The gap between the paper's headline claims (abstract, introduction, conclusion) and the empirical evidence is significant. The paper has real value in its dataset and OTC finding, but the SSL narrative outruns what the data show. **[impact: -10.00]**

2. **Address-to-transaction label mapping is underspecified, threatening evaluation validity.** The classification task is defined over *transactions* ($f: \mathcal{T} \rightarrow \{0,1\}$, Section 4), but external labels are attached to *addresses* (Section 5.1: WalletExplorer, Elliptic++, MBAL). The paper defines tag propagation between addresses via clustering (Section 4: $A \sim A' \implies \text{Tag}(A) = \text{Tag}(A')$), but never specifies how address-level labels become transaction-level labels. When a transaction involves both illicit and licit addresses — the realistic case for mixing transactions — how is the transaction label determined? Without this, the 33.2K illicit / 251.1K legal address counts in Table 1 cannot be reliably translated into the 4.62M labeled CoinJoin transactions used for evaluation. **[impact: -10.00]**

3. **"Quality over quantity" framing is disconnected from the experimental design.** The title, abstract, and conclusion set up a dichotomy between "more data" and "better data." But the experiments compare models with different feature sets (OTC vs. no OTC), which tests feature engineering, not data quality vs. data quantity per se. The "Data Quality Principle" (Section 5.2) is stated but never operationalized as an independent variable: the paper never compares pseudo-labels selected by SSU/KeyLinker quality criteria vs. pseudo-labels selected by confidence only (standard approach). The only experimental variation is in which features the base model uses, which addresses a different question. **[impact: -10.00]**

### Minor

4. **No analysis of pseudo-label quantity or quality.** The paper never reports how many pseudo-labels were added per class, their SSU complexity distribution, or their accuracy. Without this, the reader cannot evaluate whether the SSL procedure actually changed the training set meaningfully or whether the pseudo-label pool was too small/noisy to affect the model. **[impact: -9.90]**

5. **SSL method is basic self-training with limited comparison.** The method (Section 5.3) is standard self-training / pseudo-labeling. No modern SSL methods (MixMatch, FixMatch, consistency regularization, graph-based SSL) are compared, and there is no side-by-side comparison of supervised vs. SSL in the same table — the reader must flip between Tables 2 and 3. **[impact: -10.00]**

6. **No variance or significance estimates.** Results are reported as point estimates despite using 5-fold cross-validation (line 224). Standard deviations are available but not reported; the F1 differences of ±0.01–0.02 in Tables 2 and 3 may not be statistically meaningful. **[impact: -0.13]**

7. **Label noise is not estimated despite "data quality" centrality.** The paper acknowledges that off-chain labeling sources "may introduce inaccuracies" (line 23) but does not estimate noise rates or study how label noise affects results. **[impact: -0.07]**

8. **"First complete historical dataset" claim is unqualified.** The paper states "the first complete historical dataset of CoinJoin transactions" (line 27) without clarifying what "complete" means. The data goes up to block 882,421 (line 173) — a well-defined endpoint that should be specified rather than using an ambiguous superlative. **[impact: -9.06]**

### Trivial
None.

## Nice-to-Haves

- A controlled experiment directly testing the "quality over quantity" thesis: hold the base model and feature set constant, and compare pseudo-labels selected by (a) confidence only vs. (b) SSU/KeyLinker quality criteria vs. (c) confidence within quality tiers.
- Standard deviations for the 5-fold cross-validation results.
- Clarify the address-to-transaction label mapping and discuss its limitations.
- Report pseudo-label counts, class distribution, and quality metrics.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Tables 2 and 3 have formatting ambiguities (repeated rows)"** — REMOVED as parser artifact; the original submission does not have these issues.
- **"No comparison to existing Bitcoin forensic datasets (e.g., Elliptic)"** — REMOVED. The paper's focus is CoinJoin-specific transactions; standard benchmarks like Elliptic cover conventional (non-CoinJoin) flows, making a direct comparison apples-to-oranges.
- **"Some of the paper's claims about SSU are borrowed from prior work, not invented here"** — Removed because the paper cites Larionov & Yanovich (2023) and Smolenkova & Yanovich (2025) appropriately; integrating prior taxonomy into a feature pipeline is a legitimate contribution.
- **"No comparison to supervised-only baseline in the SSL experiments"** — This is inaccurate; Tables 2 (supervised) and 3 (SSL) are both present. The point about not having them side-by-side is folded into Minor weakness #5.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. If the SSL results remain essentially identical to supervised, consider reframing the paper around what it does demonstrate: a large labeled CoinJoin dataset and the finding that OTC features are harmful while KeyLinker/SSU features are useful. Drop or substantially weaken the SSL-centric claims.
2. Clarify the address-to-transaction label mapping explicitly: when a transaction involves both illicit and licit addresses, how is the transaction-level ground-truth label determined? Provide the exact rule and discuss its limitations.
3. Run a controlled experiment to directly test the "quality over quantity" thesis as described in Nice-to-Haves.
4. Report standard deviations and pseudo-label statistics.

## Score and Decision

**Calibration summary:**

All anchors retrieved across rounds:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| TRW-GCN (Eth anomaly) | q7Xi4yZYcH | 3.00 | R1 | Yes | Weaker than paper under review; minimal dataset contribution, unclear novelty |
| FE-GNN (Eth account class.) | yM7rw8Bo1f | 4.25 | R1, R2 | Yes | Similar domain; the paper under review has a larger dataset and stronger empirical finding (OTC), but similar claim-evidence gap |
| SSL Two-sample Testing | X8RTdxzqJQ | 4.80 | R1 | Yes | SSL theory paper, less topical relevance |
| BlockFound (blockchain FM) | LPXfOxe0zF | 5.75 | R1, R2 | Yes | Stronger novelty and evaluation; the paper under review has larger dataset but weaker SSL claims |
| Better Call Graphs (malware) | nwjgeFGbAF | 5.25 | R2 | Yes | Pure dataset paper; accepted as dataset contribution. Paper under review has broader scope but less tight execution |
| EX-Graph (Eth+X dataset) | juE0rWGCJW | 6.33 | R2 | Yes | Accepted dataset paper with clear contribution and solid evaluation |
| Probabilistic Sampling GCN | 6yXAKleluj | 4.00 | R2 | No | Ethereum anomaly detection, similar refinement over existing methods |

**Round 1 bracket (3.5–5.5).** The paper's strengths (large dataset, OTC negative result) place it above purely incremental method papers like TRW-GCN (3.00). Its weaknesses (unsupported central thesis, underspecified label mapping, framing mismatch) prevent it from reaching the stronger dataset contributions of BlockFound (5.75) or EX-Graph (6.33).

**Round 2 narrowing.** Comparing against FE-GNN (4.25) — the closest topical anchor with similar strengths and weaknesses — the paper under review has a *larger* dataset contribution and a *cleaner* empirical finding (OTC degrades performance), both reflected in higher impact strengths (+9.80 to +10.00 vs. FE-GNN's max +6.40). However, the paper under review has equally severe weaknesses: the central SSL claim is unsupported by the data, and unlike FE-GNN which merely lacked novelty, this paper's *headline framing* is contradicted by its own results. The honest reporting of SSL limitations partially mitigates this, but the abstract and conclusion still overclaim. Score 4.0 reflects: the paper has genuine contributions that are useful to the community (dataset, OTC finding), but the main narrative is not supported and needs major restructuring.

**Final score: 4.0 — borderline reject.** The paper should be revised to match its claims to the evidence, dropping or substantially weakening the SSL-centric contributions and reframing around the dataset and the OTC negative result, which are its strongest actual contributions.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>