Now I have all the information I need. Let me compose the final consolidated review.

## Summary

This paper investigates whether the "counterintuitive phenomenon" of likelihood inversion — where deep generative models assign higher likelihoods to out-of-distribution data than in-distribution data — occurs in tabular anomaly detection, as it famously does in image settings. The authors propose a domain-agnostic definition of this phenomenon based on relative performance against baselines, conduct extensive experiments on all 47 tabular datasets in ADBench with 12 baselines, and provide theoretical and empirical analyses connecting dimensionality and feature correlation to likelihood-test success. The main finding is that a normalizing flow likelihood test (NF-SLT) performs competitively across tabular AD benchmarks, with the counterintuitive phenomenon being rare under the proposed definition.

## Strengths

- **Comprehensive and unbiased benchmarking (Table 1).** The paper evaluates on all 47 tabular ADBench datasets plus 10 CV/NLP embedding datasets against 12 baselines, explicitly citing the selection-bias critique of Shwartz-Ziv & Armon (2022). This avoids dataset cherry-picking that plagues many AD papers and makes the headline result robust.

- **Intrinsic dimension analysis (Section 5.2, Figure 1, Table 4).** The use of the *d* Ratio (intrinsic dimension / ambient dimension) to quantify feature correlation is creative. The toy experiment with autoregressive covariance (Equation 5) cleanly validates the correlation–ID relationship, and the comparison showing tabular datasets cluster near the identity line while image datasets scatter far below (Figure 1, right) is a compelling empirical observation.

- **Theoretical formalization (Theorem 5.4, Corollary 5.6).** The result that the lower bound on the likelihood gap and the upper bound on achievable AUROC degrade linearly with dimensionality provides a formal anchor for the intuition that high dimensions undermine likelihood-based detection.

- **Acknowledgment of failure cases.** The paper explicitly discusses the yeast and imdb datasets where NF-SLT performs poorly (imdb: AUROC 0.5013, essentially random), showing transparency about the method's limitations.

## Weaknesses

### Major

- **Definition 3.3 shifts the phenomenon from "likelihood inversion" to "relative underperformance against baselines," changing the question being asked.** The original literature (Nalisnick et al. 2019a) identified a specific, surprising failure mode: OOD data receiving *higher* likelihood than in-distribution data (AUROC 6.4%, well below 50%). The paper replaces this with a definition based on whether most comparison models outperform the generative model by a significant margin (conditions on β and γ). Under this definition, NF-SLT can score near-random AUROC (imdb: 0.5013) without being diagnosed as exhibiting the counterintuitive phenomenon, as long as the gap to baselines is small. The paper argues that the simpler view is "contradictory since... any result outside 100% AUROC [would be] counterintuitive" (p. 1, col. 1), but this overstates the original literature's position — Nalisnick et al. were specifically concerned with AUROC *below 0.5* (actual inversion). The definitional drift means the paper's headline finding ("the counterintuitive phenomenon is rare in tabular data") is better characterized as "a well-tuned normalizing flow achieves competitive AUROC on tabular AD benchmarks." This is a legitimate and useful empirical finding, but it does not directly answer whether the original likelihood-inversion puzzle extends to the tabular domain.

### Minor

- **The values of β and γ in Definition 3.3 are not stated in the main text.** The central claim that the phenomenon "rarely occurs" depends critically on these thresholds, yet they are never specified. The paper defers the "fully rigorous formulation" to Appendix B (which is standard), but operational threshold values should appear in the main text when they control the paper's core conclusion.

- **The hyperparameter selection procedure is non-standard and may advantage NF-SLT.** A single global hyperparameter configuration per model is chosen to maximize average AUROC across all 47 datasets. This contrasts with per-dataset tuning (e.g., via cross-validation on the training split). Models more sensitive to hyperparameter choice (e.g., DeepSVDD, DAGMM) may be systematically disadvantaged relative to the more robust normalizing flow.

- **No variance or confidence intervals are reported despite 10 repeated experiments (Table 1).** The reader cannot assess whether NF-SLT's margins over baselines (e.g., 0.8575 vs. ICL's 0.8208) are statistically meaningful. Reporting standard deviations or confidence intervals would strengthen the evaluation.

- **No per-dataset breakdown for the 47 tabular datasets.** The embedding results are shown per-dataset (Table 1 bottom), but the tabular results — the paper's main claim — are only reported as aggregates (Table 1 top). Per-dataset results would allow readers to verify the trend is broadly consistent rather than driven by a few datasets.

- **Theorem 5.4 assumes P and Q are products of independent univariate distributions.** This strong independence assumption limits the theorem's applicability to real tabular data, where features are not generally independent. The paper acknowledges this implicitly when discussing the bilinear interpolation experiments ("independence between pixels is not guaranteed, so the theorem... cannot be applied"), but the gap between theory and practice for tabular data is not addressed.

### Trivial

- **The bilinear interpolation experiments (Table 3) produce results that "conflict with the theorems" as the paper acknowledges.** The proposed explanation (interpolation strengthens correlation, reducing entropy) is post-hoc and not independently tested. This does not undermine the paper's core claims but reflects a limitation of this specific experiment.

## Nice-to-Haves

- Directly measure likelihood inversion (e.g., what fraction of anomalous samples receive higher likelihood than the median normal sample) as a complementary analysis that would bridge the paper's definition with the original literature's concern.
- Analyze the imdb failure case in more depth: why does NF-SLT achieve near-random AUROC on this specific dataset? Understanding this boundary condition would sharpen the "rarely" claim.
- Consider reporting per-dataset AUROC for the 47 tabular datasets in a supplementary table.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **"The core experimental evidence is circular"** — The paper defines the phenomenon, tests whether it occurs, and finds it does not. This is logically sound (definition → test → conclusion), not circular. Whether the definition is appropriate is a separate question (addressed above).
- **Straw-man claim about the justification for the new definition** — The paper provides two explicit reasons for proposing a new definition (p. 1, lines 24-26). Whether readers find these reasons persuasive is a judgment call, not a factual error.
- **Architecture sensitivity (NICE)** — Deferred to Appendix G, which is stripped by the parser. Cannot be evaluated.
- **Generic/superficial strengths** from the input (e.g., "the paper addresses an important problem") are removed as not specific to this paper's content.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Clarify the relationship between the proposed definition and the original likelihood-inversion phenomenon, either by recalibrating the paper's framing or by adding a direct likelihood-inversion analysis.
2. Specify β and γ threshold values in the main text and justify their choice.
3. Report variance statistics (standard deviation or confidence intervals) from the 10 repeated runs.
4. Provide per-dataset AUROC for the 47 tabular datasets.
5. Discuss how the independence assumption in Theorem 5.4 relates to real tabular data, and whether the theoretical result can be extended.

## Score and Decision

The paper makes solid empirical contributions: a comprehensive, unbiased benchmark evaluation and a creative intrinsic-dimension analysis of feature correlation. The theoretical results, while assuming independence, provide a useful formal framework. However, the definitional shift from likelihood inversion to relative performance creates a gap between the paper's framing and what it actually demonstrates. The central finding — that NF-SLT performs competitively on tabular AD — is empirically robust but less novel than the title and framing suggest. With revisions to clarify the framing, add missing operational details, and strengthen the evaluation reporting, the paper would make a worthwhile contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>