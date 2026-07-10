## Summary

This paper investigates whether the "counterintuitive likelihood phenomenon" (where deep generative models assign higher likelihoods to anomalous than to normal data) occurs in tabular anomaly detection. It proposes a domain-agnostic definition of this phenomenon based on comparative AUROC performance, conducts extensive experiments across all 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench (benchmarked against 12 baselines), and finds that a simple normalizing-flow-based likelihood test (NF-SLT, using NICE from 2015) rarely exhibits the defined phenomenon while outperforming all comparison methods. The paper additionally provides theoretical and empirical analyses linking this finding to data dimensionality and feature correlation differences between tabular and image domains.

## Strengths

- **Comprehensive benchmark scope (Section 4).** Uses all 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench without selection bias, citing Shwartz-Ziv & Armon (2022). This is a genuine strength — many anomaly detection papers test on a handful of datasets and the results may not generalize. **[impact=+10.00]**

- **Striking empirical results on the tabular ADBench (Table 1).** NF-SLT achieves AUROC 0.8575, AUPRC 0.6398, Avg. Rank 3.43, Top2 Ratio 0.45, and Fail Ratio 0.02 — substantially outperforming all 12 comparison methods on every metric. A simple, well-understood 2015 architecture outperforming more recent specialized AD models on tabular data is a practically meaningful empirical finding. **[impact=+10.00]**

- **Intrinsic dimension analysis (Section 5.2, Figure 1, Table 4).** The d-ratio approach (intrinsic/ambient dimension) is a creative method for quantifying feature correlation. The toy example with autoregressive covariance (Equation 5) cleanly validates the correlation–ID relationship. The finding that tabular datasets cluster near the identity line while image datasets are far below it is genuinely informative. The additional analysis showing that datasets where NF-SLT underperforms tend to have lower d-ratio provides convergent evidence. **[impact=+9.15]**

- **Dimensionality-reduction experiments (Tables 2, 3).** ICA-based and bilinear-interpolation-based reduction experiments showing AUROC improvement as dimension decreases provide supporting empirical evidence for the theoretical claims about dimensionality's role. **[impact=+8.13]**

## Weaknesses

### Fatal
None.

### Major

- **Definition 3.3 operationalizes a different concept from the original phenomenon.** The paper's Definition 3.3 defines the "counterintuitive phenomenon" via comparative AUROC performance (whether other models substantially outperform the generative model). The original Nalisnick et al. (2019a) phenomenon is about *likelihood assignment* — OOD data receiving *higher* likelihoods than in-distribution data (AUROC < 0.5). These are different objects. The paper attempts to justify this redefinition (lines 25-26) by claiming the direct definition would "consider any result outside 100% AUROC as counterintuitive," which is a straw man — the original phenomenon concerns AUROC < 0.5, not AUROC < 1.0. The consequence is that the paper answers the question "does NF-SLT perform well relative to other methods on tabular data?" rather than the title's question "is likelihood inversion rare in tabular data?" This disconnect affects what the experiments actually establish. **[impact=-10.00]**

- **The imdb edge case (AUROC 0.5013) reveals a tension in Definition 3.3.** NF-SLT achieves essentially random performance on the imdb embedding dataset (AUROC 0.5013), yet the paper argues this is NOT a counterintuitive phenomenon because other methods also perform poorly (small performance gap, violating condition 2 of Definition 3.3). Under Definition 3.3, a generative model performing at chance is classified as "not exhibiting the counterintuitive phenomenon" as long as competitors also fail. A definition that cannot classify random discrimination as problematic for a likelihood-based method has reduced face validity. **[impact=-8.64]**

### Minor

- **The d-ratio analysis establishes correlation, not causation (Section 5.2).** The paper shows that datasets where NF-SLT underperforms tend to have lower d-ratio, and concludes that "one factor behind the high detection performance of tabular data is the heterogeneous nature of its features" (line 228). Confounding variables (dataset size, class imbalance, noise level, fraction of categorical features) are not controlled for, so the causal mechanism is asserted rather than demonstrated. The paper would benefit from acknowledging this limitation. **[impact=-6.07]**

- **The theoretical analysis (Theorem 5.4, Corollary 5.6) assumes strong conditions that do not match the empirical setting.** The theorem assumes independent features and a perfectly trained model (p_θ → p pointwise). Tabular features are not independent, and normalizing flows are not perfect density estimators. The theorem establishes a lower bound on the likelihood gap (not a guarantee of inversion), and the paper's conclusion that inversion "can become more severe" is appropriately hedged, but the gap between the idealized assumptions and the practical setting is substantial and deserves more explicit discussion. **[impact=-0.16]**

- **The paper conflates "heterogeneity" (features of different types/scales) with "low feature correlation" (weak statistical dependence).** Section 5.2 transitions from "tabular features are heterogeneous" to "tabular data has low feature correlation" to "tabular data has high d-ratio" without explicit justification that these concepts are measuring the same underlying property. While correlated in practice, they are conceptually distinct. **[impact=-0.04]**

- **The CV/NLP embedding experiments (Table 1, bottom) use only 5 deep model baselines compared to 12 for the tabular experiments.** The paper does not discuss whether this narrower baseline set affects the comparability of conclusions across the two settings. **[impact=-0.00]**

### Trivial
None.

## Nice-to-Haves

- **Direct likelihood comparison per dataset.** Computing log-likelihood histograms or mean likelihoods of normal vs. anomalous samples for each tabular dataset would directly measure likelihood inversion and strengthen the paper's central claim. This would not require changing Definition 3.3 but would provide convergent evidence.

- **Explicit β and γ threshold values in the main text.** If these are in the stripped Appendix B, moving them to the main text would make Definition 3.3 fully self-contained and falsifiable.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"β and γ thresholds never specified."** The paper states "The fully rigorous formulation of Definition 3.3 is provided in Appendix B" (line 77). The appendix was stripped by the parser; per filtering rules, criticisms about missing appendix content are removed.
- **"No direct test of likelihood inversion (likelihood histograms)."** The paper's stated methodology uses Definition 3.3, which operationalizes the phenomenon via comparative AUROC. This is a methodological disagreement rather than an identified flaw in the paper as written.
- **"ICA/bilinear interpolation confounds not acknowledged."** The paper explicitly acknowledges limitations (line 164: "independence between pixels is not guaranteed, so the theorem presented in Appendix D cannot be applied").
- **"NF-SLT uses only NICE."** Results with other flows are in Appendix G (stripped by the parser).
- Several generic strengths (e.g., "the paper addresses an important problem") removed for lacking specific content tied to this paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Substantially revise the paper's framing to align with what is actually measured. The empirical finding that NF-SLT (NICE) outperforms 12 baselines on the full ADBench suite is strong and stands on its own. The paper could either (a) add direct likelihood-inversion evidence (per-dataset likelihood histograms) to support the title's claim about the "counterintuitive phenomenon," or (b) reframe around the comparative performance finding and drop or qualify the claim about explaining why the original likelihood-inversion phenomenon is rare.
- Discuss the imdb edge case (AUROC 0.5013) more carefully: even if Definition 3.3 says no phenomenon, the fact that the likelihood-based method performs at chance on this dataset deserves commentary and weakens the blanket claim.
- Add explicit β and γ threshold values to the main text for Definition 3.3.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| Uj0h13lVrR.md | 1.00 | R1 | No | Unrelated (GFlowNets) |
| 5lUdTogEL3.md | 1.00 | R1 | No | Unrelated (person re-id) |
| nSDOkm0SKo.md | 1.00 | R1 | No | Unrelated (financial markets) |
| u1cQYxRI1H.md | 0.50 | R1 | No | Unrelated (diffusion illumination) |
| i28ZjVxl81.md | 2.50 | R1 | No | OOD on tabular, low-quality |
| 3qDhqj6qfu.md | 3.00 | R1 | No | Tabular modeling (KAN), different focus |
| zeeLxGw5pp.md | 3.20 | R1 | No | OOD detection with VAE |
| zB6uMznFuZ.md | 3.00 | R1 | No | Time series generation |
| **hlijRgXTDK.md** | **4.75** | R1 | **Yes** | Critical analysis of OOD detection; weaker empirical component than our paper |
| **SabhfFUfA1.md** | **4.67** | R1 | No | VAE reinterp. for OOD; score band match |
| **LjygLD0AkT.md** | **5.00** | R1 | No | Likelihood Path Principle for OOD |
| nJsfYo3HDy.md | 3.80 | R1 | No | GAN density model analysis |
| **7QDIFrtAsB.md** | **5.75** | R1 | **Yes** | Tabular AD with NCSN; similar structure but method paper; rejected for unfair comparison + limited novelty |
| **lNZJyEDxy4.md** | **6.67** | R1 | **Yes** | MCM tabular AD; clean method paper with minor weaknesses; substantially stronger framing than our paper |
| **7VkHffT5X2.md** | **6.75** | R1 | No | AnoLLM tabular AD; strong method paper |
| **CJnceDksRd.md** | **5.75** | R1 | **Yes** | DRL tabular AD; novel method, accepted despite some issues |
| I5lcjmFmlc.md | 8.00 | R1 | No | Robust classification, unrelated |
| cJs4oE4m9Q.md | 8.00 | R1 | No | Hypersphere anomaly detection |
| ZCOwwRAaEl.md | 8.00 | R1 | No | BO with normalizing flows, unrelated |
| k38Th3x4d9.md | 8.00 | R1 | No | Time series root cause analysis |
| **Vi6p2TeujL.md** | **4.25** | R2 | **Yes** | PTAD tabular AD; rejected for reproducibility issues; weaker than our paper |
| **R03zKO9T9S.md** | **4.75** | R2 | **Yes** | ADer benchmark; rejected for "novelty not at ICLR level"; our paper has stronger research question |
| rCaA79Obsj.md | 5.20 | R2 | No | Time series AD evaluation |
| hpeyWG1PP6.md | 5.75 | R2 | No | TDD benchmark for training data detection |

### Score Determination

**Round 1 bracket:** Papers in the 4.5–6.0 range are the most relevant comparison class. Our paper sits above the pure benchmark/critical-analysis papers (ADer at 4.75, Pathologies at 4.75) because it has a genuine research question and novel analysis (ID/d-ratio investigation). It sits below clean method papers like MCM (6.67) and DRL (5.75) because those papers have clear methodological contributions and minor weaknesses only, whereas our paper's central framing issue is a significant weakness.

**Round 2 narrowing:** The key distinguishing factor is the impact of the weakness about Definition 3.3 (-10.00 in the scored draft). The NCSNAD paper (5.75) was rejected primarily for limited novelty and unfair comparison — external criticism about its method. Our paper's -10.00 weakness is more central: it questions whether the paper actually studies what it claims to study. This is weightier than the weaknesses in NCSNAD or DRL. Among papers at similar scores, ADer (4.75) was a pure benchmark with no research question of its own, while our paper has a clear question but a flawed operationalization of it. The comparison suggests our paper should be scored slightly above ADer (better research question) but below NCSNAD/DRL (cleaner framing).

**Final score: 5.0.** The paper has genuinely strong empirical contributions (comprehensive benchmark, surprising results, creative d-ratio analysis) but the central framing issue with Definition 3.3 means the paper does not fully answer the question posed by its title. The empirical finding that NF-SLT outperforms baselines on ADBench is robust and worth documenting, but the claim about "why the counterintuitive phenomenon of likelihood is rare in tabular data" is not fully supported by the evidence collected.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>