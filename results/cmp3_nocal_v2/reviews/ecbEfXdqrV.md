## Summary

This paper investigates whether the "counterintuitive phenomenon" (deep generative models assigning anomalously high likelihoods to out-of-distribution data, well-documented in images) occurs in tabular data. The authors propose a domain-agnostic definition of this phenomenon based on relative model performance, conduct extensive experiments on 47 tabular and 10 CV/NLP embedding datasets (12 baselines), and find that simple likelihood-based anomaly detection with normalizing flows (NF-SLT) reliably outperforms specialized anomaly detection methods. They explain this through theoretical analysis linking the likelihood gap to dimensionality, and empirical analysis connecting feature correlation to intrinsic dimension reduction.

## Strengths

1. **Comprehensive, bias-aware benchmark evaluation.** The paper uses *all* 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench without selective exclusion, explicitly citing concerns about dataset-selection bias (Shwartz-Ziv & Armon, 2022). The 12-baseline comparison covers both shallow and deep anomaly detection methods. This is a meaningful methodological improvement over prior work that used only 1–2 tabular datasets (e.g., Kirichenko et al., 2020).

2. **Strong and consistent empirical results.** Across 47 tabular datasets, NF-SLT achieves AUROC 0.8575, average rank 3.43 (out of 13), Top2 Ratio 0.45, and Fail Ratio 0.02 — the best on every aggregate metric. On the 10 CV/NLP embedding datasets, NF-SLT wins on 9 out of 10. These results are striking: a simple likelihood test should not dominate specialized deep AD methods (DeepSVDD, GOAD, NeuTraLAD, ICL) if the counterintuitive phenomenon were a serious issue in tabular data.

3. **Feature correlation analysis via intrinsic dimension is a principled contribution.** The use of ID estimation (TwoNN, MLE) to quantify global feature correlation is well-executed. The synthetic experiment with autoregressive covariance (Figure 1, left/center) convincingly shows ID decreasing as correlation increases. The comparison of ID vs. ambient dimension for real tabular and image datasets (Figure 1, right; Table 4) provides clear visual evidence that tabular data has higher d-ratio (ID/ambient dimension) than image data — i.e., tabular features are less correlated. The finding that NF-SLT failures correlate with low d-ratio even within tabular data (Table 4, bottom) further strengthens the explanation.

4. **Honest discussion of conflicting evidence.** The paper acknowledges that the bilinear-interpolation resize experiments (Table 3) produce results that "conflict with the theorems in Appendix D" and offers a clear explanation involving increased correlation from interpolation. This candor is commendable.

## Weaknesses

### Fatal

None.

### Major

1. **Definitional framing gap between the original phenomenon and the paper's operationalization.** The paper redefines the "counterintuitive phenomenon" in terms of *relative model performance* (Definition 3.3: the generative model is substantially outperformed by most comparison models). However, the phenomenon documented in the image literature (Nalisnick et al., 2019a; Kirichenko et al., 2020) was specifically about *likelihood inversion* — anomalous/out-of-distribution data receiving higher likelihood than in-distribution data, which is an intrinsic property of the model-data interaction. The paper argues (lines 24–27) that simple likelihood comparison has limitations (any non-100% AUROC could be called counterintuitive; inversion can arise from dataset difficulty), which is a reasonable justification for a new definition. However, the paper *never reports the simple likelihood inversion rate* — the fraction of datasets where the mean likelihood of anomalous test data exceeds that of normal data. This means the paper's headline claim ("the counterintuitive phenomenon is rare in tabular data") only holds under its own redefinition, leaving the original question from the image literature unanswered. The title and abstract (line 9: "where deep generative models frequently assign higher likelihoods to anomalous data") frame the paper as addressing the original phenomenon, creating a mismatch between the framing and the methodology. **Impact:** The paper would be significantly strengthened by reporting both analyses — (i) simple likelihood inversion rates as supplementary evidence, and (ii) Definition 3.3 as the primary analysis — and explicitly acknowledging the distinction.

2. **Theory-assumption gap in Theorem 5.4.** Theorem 5.4 assumes factorized (independent) distributions: $P = \prod p_i(x_i)$ and $Q = \prod q_i(x_i)$ (line 142). Yet the paper's explanatory story for why tabular data avoids the phenomenon is that tabular features have *weaker* correlations than image pixels, not that they are independent. The theorem shows what happens under complete independence — the strongest possible form of "no correlation" — but the actual claim is about weak correlation. The paper needs either a result that interpolates between independence and strong correlation (e.g., depending on the effective rank of the covariance matrix or the eigenvalue spectrum) or a clear acknowledgment that the theory only covers a limiting case and does not directly support the correlation-based explanation. The ICA experiments (Table 2) enforce independence rather than testing weak correlation, and the bilinear interpolation experiments (Table 3) conflate dimension reduction with increased correlation (as the authors note). **Impact:** The theoretical and empirical evidence for the correlation-based explanation is weaker than the paper's narrative suggests.

### Minor

1. **Hyperparameter selection protocol may warrant sensitivity analysis.** The paper selects one global hyperparameter configuration per model across all 47 datasets (line 122: "the hyperparameter combination with the highest average AUROC for all datasets is selected"). This is a defensible design choice, but models like DeepSVDD (nu parameter, architecture) and OCSVM (kernel, gamma) are known to be sensitive to per-dataset tuning. NF-SLT (NICE with 10 coupling layers, fixed prior) may be unusually robust to a single configuration. The paper should either discuss whether this protocol could systematically favor NF-SLT, or provide evidence (even on a subset of datasets) that the ranking holds under per-dataset tuning.

2. **No variance reporting.** The paper reports mean AUROC over 10 repeated experiments but does not provide standard deviations or confidence intervals (line 122). For key comparisons (e.g., NF-SLT 0.8575 vs. ICL 0.8208), knowing the variance is important to assess whether the advantage is statistically meaningful.

3. **No per-dataset AUROC results for tabular data.** Table 1 shows only aggregate metrics for the 47 tabular datasets. A full table or heatmap of per-dataset AUROC (which could go in the appendix) would let readers assess whether NF-SLT's advantage is broad across datasets or concentrated on a subset.

### Trivial

- Corollary 5.6 relies on a moment-scaling assumption ($\mathcal{O}(d^k)$ with $k < n$) that is stated without empirical validation on real data distributions.
- The paper discusses the 'yeast' dataset failure briefly but does not analyze *why* NF-SLT underperforms there, which could further test the paper's explanatory framework.

## Nice-to-Haves

- Report simple likelihood inversion rates (fraction of datasets where the mean likelihood of anomalous test data exceeds that of normal data) as a supplementary analysis — this would directly connect to the original image-domain phenomenon.
- Relax the independence assumption in the theoretical analysis, e.g., by showing how the likelihood gap depends on the effective rank of the covariance matrix or the eigenvalue spectrum.
- Analyze why NF-SLT underperforms on specific datasets (e.g., 'yeast', 'imdb') — are these cases where feature correlation is higher (lower d-ratio)?

## Removed Points

These points were raised in the input review but are excluded under the filtering rules:

- **Missing β/γ thresholds in Definition 3.3:** The paper states that the full rigorous formulation is in Appendix B. Hard rules remove weaknesses about content that was in the appendix (stripped by the parser).
- **CV/NLP embedding interpretation is "strained":** This is an opinion-based assessment of internal consistency rather than a concrete weakness; the paper's explanation is internally coherent.
- **Definition does not reference k or address small k:** Speculative concern without evidence that this is a practical problem.
- **Genomics claim without justification:** This is a contextual assertion, not a core claim, and does not rise to the level of a weakness.
- **Various formatting and presentation nitpicks:** Excluded per hard rules.

## Novel Insights

The most interesting observation to emerge from the reviews is the tension between the paper's two explanatory mechanisms (dimensionality and correlation) and the fact that Theorem 5.4 only addresses dimensionality under the independence assumption, while the correlation analysis (ID estimation) is entirely empirical. This gap suggests that a unified theoretical framework connecting correlation strength (parametrized by, e.g., the covariance eigenvalue decay rate) to the likelihood gap would be a natural and impactful extension.

## Suggestions

1. In addition to Definition 3.3, report the simple likelihood inversion rate across the 47 datasets and explicitly acknowledge how this relates (or does not) to the definition-based analysis.
2. Add a sensitivity experiment: re-run the top-3 baselines and NF-SLT with per-dataset hyperparameter tuning on a representative subset of ~10 datasets and verify that the ranking does not qualitatively change.
3. Add standard deviations to Table 1 or a supplementary per-dataset table.

## Score and Decision

The paper makes a genuine empirical contribution: demonstrating that likelihood-based anomaly detection with normalizing flows works reliably across a comprehensive tabular benchmark is practically useful, and the intrinsic-dimension analysis of feature correlation is a clever and well-executed contribution. However, the definitional framing gap (the paper redefines the phenomenon of interest and never reports the original metric) and the gap between the independence-assumed theory and the weak-correlation claim are substantive concerns that affect the strength of the central claims. These issues are fixable, and the core empirical finding is solid.

**Score:** 6  
**Decision:** Borderline Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>