## Summary

This paper empirically investigates whether the well-known failure mode of likelihood-based anomaly detection in images (where OOD data receives higher likelihood than in-distribution data) also occurs in tabular data. The authors propose a new definition of this "counterintuitive phenomenon" based on relative model performance, run comprehensive experiments on all 47 ADBench tabular datasets with 12 baselines, and find their normalizing flow method (NF-SLT) achieves the highest average AUROC. They provide theoretical and empirical analyses linking the absence of the phenomenon to lower dimensionality and weaker feature correlations in tabular data.

## Strengths

1. **Comprehensive evaluation without selection bias.** The paper uses all 47 tabular and 10 CV/NLP embedding datasets from ADBench with 12 baseline models, following the principle of Shwartz-Ziv & Armon (2022). This is the most extensive empirical test of likelihood-based tabular AD to date, and the commitment to avoiding cherry-picking is a genuine methodological strength. (Section 4, Table 1)

2. **Creative use of intrinsic dimension (ID) estimation to quantify feature correlation.** The analysis using ID to measure and compare feature correlation across domains is the paper's most technically interesting contribution. The autoregressive Gaussian toy example (Equation 5, Figure 1 left/center) cleanly validates the relationship between correlation and ID reduction, and the d Ratio metric provides a concrete, interpretable way to compare tabular and image data along this axis. (Section 5.2, Figure 1, Table 4)

3. **Non-trivial theoretical extension of the likelihood-gap analysis.** Theorem 5.4 shows the lower bound on the expected likelihood gap can decrease linearly with dimension (under stated assumptions), extending Caterini & Loaiza-Ganem (2022). Corollary 5.6 connects this to AUROC upper bounds, providing a theoretical bridge between dimensionality and detection performance. While the independence assumption limits direct application, the result is a valid mathematical contribution. (Section 5.1)

## Weaknesses

### Major

1. **Framing mismatch: the title and abstract promise to study likelihood inversion, but the experiments measure relative model performance.** The original "counterintuitive phenomenon" (Nalisnick et al., 2019a) is that OOD data receives *higher* likelihood than in-distribution data. Definition 3.3 redefines it as the generative model being substantially outperformed by other methods in AUROC. The paper never directly tests whether anomalous samples receive higher likelihood than normal samples on any tabular dataset. The abstract claims to examine "such counterintuitive behavior" (higher likelihood to anomalies), but the evidence supports only the redefined criterion. These are logically distinct — a model could have correctly ordered likelihoods but poor AUROC (high overlap), or inverted likelihoods but still be competitive (if other methods also fail). This mismatch runs throughout the paper and undermines the connection between the title's question and the evidence presented. (Title, Abstract, Definition 3.3, Section 4)

2. **Hyperparameters selected by optimizing average test-set AUROC across all 47 datasets.** The paper states: "the hyperparameter combination with the highest average AUROC for all datasets is selected as the representative hyperparameter combination." This leaks test-set information into model selection — the reported numbers reflect hyperparameters indirectly fit to the evaluation metric. Standard practice requires validation-based selection per dataset or a held-out validation split. The magnitude and direction of bias from this procedure is unknown but could inflate reported performance. (Section 4, Evaluation paragraph)

### Minor

3. **Definition 3.3's thresholds β and γ are not specified in the main text.** The definition requires thresholding the proportion of outperforming models (β) and the minimum performance gap (γ), yet no concrete values are given. The paper's central empirical conclusion depends on these thresholds, but the analysis uses informal reasoning ("the gap is very small," "cannot be judged") instead of applying the definition transparently. While Appendix B may provide a rigorous formulation (stripped by the parser), the main text should at minimum state and justify the chosen values. (Definition 3.3, Section 4 Experiment Result)

4. **The IMDB failure case (AUROC=0.5013) is dismissed rather than analyzed.** NF-SLT achieves essentially random performance on imdb. The paper dismisses this by saying the gap with the best comparison model (GOAD at 0.5398) is too small to satisfy Definition 3.3's conditions, but an AUROC of 0.50 means the likelihood test has *no discriminative power* on this dataset. This is a genuine failure case that should be analyzed — not defined away. The paper should investigate whether likelihood inversion occurs, how the ID compares to other datasets, and what distinguishes imdb. (Table 1 bottom, Section 4)

5. **Theorem 5.4 assumes independent features (product distributions P = ∏ p_i, Q = ∏ q_i).** Real tabular data has correlated features, even if less so than images. While the paper validates the theorem experimentally via ICA (which enforces independence), the per-dimension contribution to the likelihood gap is not quantified. It is therefore unclear whether the linear-in-d effect is practically meaningful at the dimensions typical of tabular data (d < 100). The broader qualitative argument — that lower dimensions reduce the effect — is supported by the interpolation experiments (Table 3), but the theoretical grounding for real (non-independent) data remains weaker. (Theorem 5.4, Section 5.1)

6. **Architecture-domain confound is acknowledged but not controlled for.** The tabular experiments use NICE (MLP-based flow), while the image-domain phenomenon was established with CNN-based flows (Glow, RealNVP). Kirichenko et al. (2020) showed MLP flows reduce the phenomenon even on images. The paper acknowledges this connection (Section 5.2) but does not run a control experiment (e.g., NF-SLT/NICE on CIFAR-10 vs. SVHN) to separate architecture from domain effects. (Section 5.2)

### Trivial

7. **Table 4 shows ID estimates for only 4 tabular datasets** while the right panel of Figure 1 plots many more tabular points. The paper should clarify how many ADBench datasets were used for ID estimation and whether the 4 shown are representative.

## Nice-to-Haves

- Directly test for likelihood inversion by comparing average log-likelihood of normal vs. anomalous test samples per dataset. This would directly address the original Nalisnick phenomenon.
- Run NF-SLT (NICE) on CIFAR-10 vs. SVHN to disentangle architecture from domain effects and strengthen the domain-level claim.
- Report standard deviations for Table 1 averages (10 repeats are performed but only means are shown).
- Analyze imdb as a case study — report likelihood distributions, ID, and discuss why the method fails.

## Removed Points

The following points from the input review are excluded with justification:
- **"Baseline selection is tilted toward weak methods"** — The paper uses the complete ADBench benchmark suite (12 models) without selection bias. Using the full standard benchmark is a principled decision, not a weakness. Extending to more recent methods would be useful but is not required.
- **Section 1 dimensionality criticism** ("conflates manifold dimensionality with tensor structure") — The factual observation that ADBench tabular datasets have lower ambient dimensions than images is correct and stated without technical error.
- **Section 3 "straw man" criticism** — The paper's critique that "any result outside 100% AUROC as counterintuitive" is a reasonable characterization of one interpretation; it is not a fabrication.
- **NeuTraLAD scaling inconsistency** — The paper explicitly explains why NeuTraLAD uses different preprocessing ("significant performance decrease was observed when scaling").
- **All formatting, grammar, and presentation nitpicks** — These reflect parser artifacts, not author errors.
- **"Strengthening the Paper on Its Own Terms" section from the critic** — These are constructive suggestions but do not constitute weaknesses in the paper as submitted.
- **Claim that the paper is "circular"** — The paper does not assume what it sets out to prove; it proposes Definition 3.3 and then tests whether data satisfies it. The issue is a framing mismatch, not circular reasoning.

## Novel Insights

None beyond the paper's own contributions. The core observation from the harsh critic — that Definition 3.3 shifts the research question from likelihood-inversion to relative-model-ranking, creating a mismatch between the paper's framing and its evidence — is a direct reading of the paper's structure, not a hidden insight.

## Suggestions

1. **Reframe the paper's contribution to match what is actually measured.** Either change the title and abstract to reflect that the paper studies whether likelihood-based AD is *competitive* on tabular data (under Definition 3.3), or add a direct test of likelihood inversion to support the original framing.
2. **Specify β and γ explicitly in the main text** with justification and sensitivity analysis showing how conclusions change at different thresholds.
3. **Use validation-based hyperparameter selection** per dataset, or at minimum acknowledge the optimistic bias from the current approach and discuss its potential magnitude.
4. **Analyze the imdb failure case** — report likelihood values for normal vs. anomalous samples, ID estimates, and discuss what distinguishes this dataset from the others.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>