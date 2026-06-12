## Summary

This paper investigates why normalizing flows rarely exhibit the well-known counterintuitive likelihood phenomenon (OOD data receiving higher likelihood than in-distribution data) in tabular anomaly detection, contrasting with the image domain. The authors propose a domain-agnostic definition of the counterintuitive phenomenon, conduct extensive experiments on 47 tabular and 10 CV/NLP embedding datasets from ADBench showing that simple likelihood testing with normalizing flows (NF-SLT) outperforms 12 baselines, and provide theoretical and empirical analysis attributing this to lower dimensionality and weaker feature correlation in tabular data.

## Strengths

- **Comprehensive experimental evaluation**: The paper evaluates all 47 tabular and 10 CV/NLP embedding datasets from ADBench against 12 baselines (6 shallow, 6 deep), explicitly avoiding dataset selection bias. NF-SLT achieves the best average AUROC (0.8575), best average rank (3.43), highest Top2 ratio (0.45%), and lowest fail ratio (0.02%), providing strong empirical evidence for the paper's central claim.

- **Formal definition of a previously vague concept**: Definition 3.3 provides an operational framework with two conditions (proportion threshold β and minimum gap threshold γ) for determining when the counterintuitive phenomenon occurs, moving beyond the ad-hoc reasoning in prior work. The validation against the CIFAR-10/SVHN example (where Glow yields 6.4% AUROC) demonstrates the definition's face validity.

- **Multi-faceted analysis with theoretical grounding**: The paper provides complementary theoretical (Theorem 5.4, Corollary 5.6 showing dimension-dependent likelihood gap degradation) and empirical (intrinsic dimension analysis, dimensionality reduction experiments) perspectives. The intrinsic dimension ratio analysis comparing tabular (d-Ratio ~0.38–0.81) to image data (d-Ratio ~0.002–0.019) is a concrete and interpretable finding.

## Weaknesses

### Fatal

None.

### Major

- **Theory relies on assumptions that are in tension with the paper's own thesis**: Theorem 5.4 and Corollary 5.6 assume *independent* features (P = ∏p_i, Q = ∏q_i), yet a central argument of the paper is that tabular data differs from images precisely in its (lack of) feature correlation. The paper acknowledges that tabular features have some correlation (Section 5.2 devotes extensive analysis to this), but the theoretical results do not apply to correlated settings. The paper does not address how correlated tabular features interact with the dimensionality effect, making the theoretical contribution less convincing as an explanation for real tabular data.

- **Definition 3.3 lacks concrete instantiation**: The thresholds β and γ are never specified across the paper's own experiments. In Section 4, the authors evaluate Definition 3.3 informally (e.g., noting the yeast dataset has a 0.02 gap and concluding it doesn't satisfy the second condition), but without concrete threshold values, the definition cannot be independently applied. This limits the reproducibility and generalizability of the core contribution.

- **Comparison of image experiments conflates multiple factors**: Table 2 uses ICA (enforcing independence) on raw image pixels, while Table 3 uses bilinear interpolation resizing (destroying independence by introducing pixel correlations). The paper acknowledges this contradiction (Section 5.1, last paragraph) but does not resolve it. These experiments are the primary empirical support for the dimensionality hypothesis, and their mixed messages weaken the analysis.

- **Single flow architecture across all 47 datasets**: NICE with 10 coupling layers is a relatively simple flow architecture. While Appendix G reportedly includes other flows, the main results depend entirely on one architecture. The paper's claim that "NF-SLT" is broadly effective would be stronger with multi-architecture validation in the main text, especially given that prior work (Kirichenko et al., 2020; Schirmeister et al., 2020) showed architecture choices significantly affect likelihood inversion.

### Minor

- **The H(P) > H(Q) condition is assumed but never verified**: The entire theoretical framework (Theorem 5.4, Corollary 5.6, Tables 2–3) depends on the entropy ordering between normal and abnormal distributions, yet this condition is never measured on any tabular dataset. It is unclear whether this condition holds in the experimental settings of Table 1.

- **No analysis of anomaly type dependence**: The paper treats all anomalies uniformly, but tabular anomaly detection encompasses point anomalies, contextual anomalies, and collective anomalies. The relative performance of NF-SLT may vary by anomaly type, and the claim that the counterintuitive phenomenon "rarely occurs" may not hold uniformly.

- **Table 1 fails to report per-dataset results for tabular data**: Only aggregate statistics (avg AUROC, avg rank, Top2 ratio, Fail ratio) are reported for 47 tabular datasets. The discussion of specific datasets (yeast, imdb) is selective. Without per-dataset results, it is difficult to independently verify the paper's claims about when NF-SLT fails and whether failures qualify as counterintuitive under Definition 3.3.

### Trivial

None.

## Nice-to-Haves

- An analysis showing how the counterintuitive phenomenon frequency varies as a function of d-Ratio across tabular datasets, directly linking the theoretical prediction to empirical observation.
- Measuring the entropy difference H(P) - H(Q) on selected tabular datasets to validate the key assumption of the theoretical framework.
- A broader ablation across multiple flow architectures (RealNVP, Glow, NSF) in the main experimental results.

## Novel Insights

The intrinsic dimension ratio analysis (d-Ratio) comparing tabular and image domains is a genuinely novel and interpretable contribution. By showing that image datasets have d-Ratios of 0.2–0.3% while tabular datasets have d-Ratios of 38–81%, the paper provides concrete evidence that the manifold structure of tabular data is fundamentally different from image data. The finding that NF-SLT's failures in tabular data correlate with low d-Ratio datasets (Table 4) offers a practical diagnostic: practitioners can check the d-Ratio of their data to predict whether simple likelihood testing will succeed. This is a useful and non-obvious observation that connects manifold geometry to anomaly detection reliability.

## Suggestions

- Instantiate Definition 3.3 with concrete values of β and γ (e.g., β=0.5, γ=0.05) and apply it systematically across all 47 tabular datasets with per-dataset reporting.
- Present multi-architecture flow results in the main text (not just appendix) to strengthen the claim that the phenomenon is rare for normalizing flows generally, not just NICE.
- Add a column to Table 1 (or a supplementary table) reporting the d-Ratio for each dataset alongside NF-SLT rank, to directly test the correlation between feature structure and detection success.

## Score and Decision

The paper makes a meaningful empirical contribution by comprehensively demonstrating that the counterintuitive likelihood phenomenon is rare in tabular anomaly detection, addressing an important practical question with a large-scale experimental study. The operational definition (Definition 3.3) and the intrinsic dimension ratio analysis are valuable contributions. However, the theoretical analysis is undermined by its reliance on independence assumptions that contradict the paper's own thesis about feature correlation, the core definition lacks concrete instantiation, and the experimental design conflates multiple factors in the supporting experiments. The paper is close to the accept threshold but the theoretical and definitional gaps prevent full confidence.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept