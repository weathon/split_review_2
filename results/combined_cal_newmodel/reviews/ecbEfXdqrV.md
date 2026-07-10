Now I have all the information needed. Let me compose the final review.

**Comparing this paper to calibration anchors:**

- **vs MCM (6.67, Accept)**: MCM proposes a novel method. Current paper has stronger dataset coverage (47 vs 20) but no new method and a more significant framing issue. Slightly below MCM.
- **vs AnoLLM (6.75, Accept)**: AnoLLM has conceptual novelty (LLMs for AD). Current paper has more rigorous evaluation across more datasets. Both have framing/scope concerns. Comparable but slightly below.
- **vs OOD Paradox (5.67, Reject)**: Both study the likelihood paradox. Current paper has much stronger empirical validation but its definition of the phenomenon is arguably more problematic than the approximations criticized in OOD Paradox. Above this reject.
- **vs PTAD (4.25, Reject)**: Current paper's empirical methodology is far superior (no selection bias, all ADBench datasets). Far above this.
- **vs Diff AD (7.00, Accept)**: Strong method paper with solid theory and experiments. Current paper is competitive in empirical rigor but lacks the methodological novelty.

My draft's strongest items (favorability >11): strength about comprehensive evaluation (11.02), striking results (12.24), ID analysis (12.11), connecting theory/experiments (13.00).
My draft's weakest items (favorability <1): β/γ thresholds not specified (-0.03), non-monotonicity not discussed (0.35), no statistical significance (-1.52), two disconnected threads (-0.97).

The cross-paper comparison: accepted papers in this space (MCM 6.67, AnoLLM 6.75) have favorability on their strongest items around 12+ for core contributions. Current paper's strongest items are similarly 12+. However, the accepted papers' worst items tend to be in the 1-4 range, while current paper has items in the -1.5 to 0 range (more negative). The definition issue's -0.32 and -2.73 favorability items are particularly damaging.

This puts the paper below MCM/AnoLLM but above OOD Paradox/PTAD. Score: 6.0.

**Round-1 bracket**: Between 4.5 and 6.5 (below accepted method papers but above clearly rejected ones)
**Final score**: 6.0 (borderline accept - solid empirical work with framing issues to resolve)

Let me write the final review.## Summary

This paper investigates whether the well-known "counterintuitive phenomenon" from the image OOD literature — where deep generative models assign higher likelihoods to anomalous/OOD data than to in-distribution data — also occurs in tabular anomaly detection. It proposes a domain-agnostic definition of this phenomenon (Definition 3.3, based on relative AUROC against other methods), conducts extensive experiments on all 47 ADBench tabular datasets plus 10 CV/NLP embedding datasets using NICE with a likelihood threshold (dubbed NF-SLT), and provides theoretical and empirical analysis linking the phenomenon's rarity to lower dimensionality and weaker feature correlation in tabular data.

## Strengths

- **Comprehensive, unbiased evaluation on all 47 ADBench datasets (favorability=11.02).** The paper uses every ADBench tabular dataset without selection bias, directly addressing the concern raised by Shwartz-Ziv & Armon (2022). This is the correct methodology for an empirical claim about a data domain and elevates the paper above studies that cherry-pick datasets.

- **Consistent and striking results (favorability=12.24).** NF-SLT achieves 0.8575 average AUROC, 0.45 Top2 Ratio, and 0.02 Fail Ratio across 47 datasets (Table 1), decisively outperforming all 12 baselines including dedicated deep AD methods. The finding that simple likelihood testing works *better* on tabular data than specialized methods is genuinely interesting and non-obvious.

- **Intrinsic dimension analysis is well-motivated and informative (favorability=12.11).** The synthetic Gaussian toy example (Section 5.2, Figure 1) cleanly shows ID decreasing as correlation increases. The empirical finding that tabular datasets have substantially higher d Ratio than image datasets (magicgamma at 0.700 vs. CIFAR-10 at 0.003) provides concrete quantitative support. The bottom panel of Table 4 — showing that NF-SLT failures concentrate on low-d-Ratio datasets even within tabular data — is the strongest evidence linking feature correlation to performance.

- **Dimensionality ablation experiments (Tables 2-3) connect theory to practice (favorability=10.84).** The ICA-based and bilinear interpolation experiments show AUROC improving when dimensionality is reduced for the H(P) > H(Q) regime, consistent with the theoretical analysis, even if the trends are not perfectly monotonic.

- **The paper's structure is more comprehensive than typical empirical papers (favorability=13.00),** attempting to connect theory (Theorem 5.4, Corollary 5.6), controlled experiments (Tables 2-3), and real-data analysis (Table 4, Figure 1) into a coherent narrative about why the phenomenon is rare in tabular data.

## Weaknesses

### Major

- **Definition 3.3 is misaligned with the phenomenon it claims to capture.** The existing literature (Nalisnick et al., Kirichenko et al., Serra et al., Caterini & Loaiza-Ganem) defines the counterintuitive phenomenon as a failure of *likelihood ordering*: anomalies/OOD data receive *higher* likelihoods than in-distribution data. Definition 3.3 replaces this with a relative-AUROC comparison against other methods. This conflates two distinct situations: (a) likelihood inversion is present (the pathological behavior from the image literature), and (b) NICE happens to be a relatively poor model for a given dataset compared to alternatives, even if no likelihood inversion is occurring. Furthermore, the thresholds β and γ are never numerically specified in the main paper, making the definition inoperative for quantitative evaluation — the paper applies it qualitatively (e.g., yeast gap of 0.02 is deemed insufficient, imdb gap of ~0.04 called "very small"), but without stated thresholds this judgment is not reproducible. (The paper references Appendix B for full formulation, but β and γ values remain unspecified.)

- **The theoretical analysis assumes independence that does not hold for real data.** Theorem 5.4 requires P and Q to be products of independent univariate distributions. On real tabular data — where features have complex dependencies (copula structures, categorical-continuous interactions) — the theorem does not directly apply. The paper's attempt to bridge this gap via the correlation/ID analysis (Section 5.2) is reasonable as a separate empirical argument, but there is no formal link connecting the independence-assumed theory to the correlated-data reality. The paper thus has two somewhat disconnected threads: a theoretical story for independent data and an empirical story about correlation/ID, without a proven bridge between them.

### Minor

- **The claim that "AUROC increases as dimensionality decreases" (Section 5.1, discussing Table 2) is not uniformly supported.** For CIFAR-10/SVHN with ICA-reduced dimensions: 0.3311 (1024) → 0.2924 (512) → 0.2984 (256) → 0.3143 (30). The AUROC drops from 1024 to 512 components before partially recovering. The non-monotonicity is not discussed, and the headline claim overstates the clarity of the trend.

- **No measures of statistical significance are reported** (confidence intervals, standard deviations, or paired tests) despite 10 repeated experiments being conducted. For a comparative claim about outperforming 12 baselines across 47 datasets, some significance assessment would substantially strengthen the evidence.

- **The Fail Ratio threshold (rank ≥ 9, Table 1) is chosen without justification.**

### Trivial

- **The choice of TwoNN over MLE for the d Ratio analysis (Table 4) is not justified.** The two estimators give quite different estimates (e.g., CIFAR-10: MLE=26 vs TwoNN=11), so the d Ratio values and downstream conclusions would differ meaningfully with the alternative estimator.

## Nice-to-Haves

- Test at least one additional normalizing flow architecture (e.g., RealNVP, Glow) in the main paper rather than relegating to the appendix to strengthen the generality claim.
- Directly measure likelihood ordering (e.g., what fraction of anomalies have higher likelihood than the median normal sample) to connect more cleanly with the prior literature, rather than relying solely on the relative-AUROC definition.
- Report per-dataset results with standard deviations to allow readers to see where NF-SLT succeeds and struggles.

## Removed Points

These points from the input reviews were removed with justification:

- **NF-SLT acronym is misleading**: Removed. The paper explicitly defines NF-SLT as a "methodology" (line 15), not a new method, and its contributions are framed as empirical/analytical, not methodological. The naming is standard practice for studied procedures.
- **CV/NLP embeddings undermine domain-level framing**: Removed. The paper acknowledges this tension and explicitly uses the embedding results to support its correlation/dimensionality mechanism (line 234). The embedding analysis strengthens rather than weakens the paper's mechanistic explanation.
- **Per-dataset results not shown**: Removed per parser-rules about missing appendix content (the appendix is stripped, so this cannot be verified).
- **Anomaly/OOD detection conflation**: Removed. Acknowledged in footnote 1. The paper addresses this concern explicitly.
- **Data split sensitivity**: Removed. The paper uses the standard Zong et al. (2018) protocol; this is a generic concern applicable to all tabular AD papers using this protocol.

## Novel Insights

The harsh critic's most insightful observation is that Definition 3.3 measures a fundamentally different quantity than what the OOD detection literature means by "counterintuitive phenomenon" — it captures relative model failure rather than likelihood inversion. This is a genuine conceptual mismatch. The paper would be more convincing if it either (a) adopted a definition directly measuring likelihood ordering (to connect to prior work), or (b) committed to specific β/γ thresholds with reported counts, while clearly distinguishing its definition from the literature's. A second insight is that the theory and empirical evidence remain two parallel stories — the independence-assumed theory and the correlated-data empirical analysis are never formally linked, limiting the theoretical contribution's reach.

## Suggestions

1. **Recalibrate the core framing.** Either adopt a definition that directly measures likelihood inversion (the literature's standard), or explicitly commit to specific β, γ values, report the fraction of datasets meeting the threshold, and rename the phenomenon to avoid conflating it with the likelihood-ordering concept studied in prior work.
2. **Add standard deviations or confidence intervals** to Table 1 for the 10 repeated runs.
3. **Discuss the non-monotonicity in Table 2** rather than presenting the trend as uniformly monotonic.
4. **Justify the TwoNN estimator choice** for ID estimation, or show results with both estimators.

## Score and Decision

**Calibration anchors considered:**
| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| MCM (lNZJyEDxy4) | 6.67 | R2 | Yes | Proposes new method; current paper has stronger empirical breadth but no new method and a definition issue |
| AnoLLM (7VkHffT5X2) | 6.75 | R2 | Yes | Conceptual novelty (LLMs for AD); current paper has more rigorous evaluation across more datasets |
| DRL (CJnceDksRd) | 5.75 | R2 | Yes | Proposes new method with theory; current paper comparable in rigor, less methodological novelty |
| Diff AD (lR3rk7ysXz) | 7.00 | R2 | No | Strong method paper; current paper competitive empirically but lacks method contribution |
| OOD Paradox (jQ596tXT3k) | 5.67 | R1/R2 | Yes | Also studies the likelihood paradox; current paper has much stronger empirical validation |
| PTAD (Vi6p2TeujL) | 4.25 | R2 | Yes | Current paper's empirical methodology is far superior (no selection bias, full benchmark) |
| NF OOD (6Z8rZlKpNT) | 3.40 | R1 | Yes | Limited novelty; current paper far more comprehensive |
| Autoencoders Unreliable (X8XQOLjLX6) | 4.50 | R2 | Yes | Theoretical but limited scope; current paper's empirical scope is much broader |

**Round-1 bracket (from topically similar anchors):** 4.5 – 6.5

**Narrowing rationale:** The paper's strongest items (comprehensive evaluation at 11.02, striking results at 12.24, ID analysis at 12.11) match or exceed those of accepted papers like MCM (6.67) and DRL (5.75). However, the definition/framing issue produces low-favorability items (-0.32, -2.73) that are more severe than anything in the accepted papers' reviews. This places the paper below MCM/AnoLLM but clearly above OOD Paradox/PTAD. The empirical contribution is genuine and well-executed; the framing issue is substantive but addressable.

**Final: Score 6.0 — Borderline Accept**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>