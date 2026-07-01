## Summary
This paper investigates whether the known “counterintuitive phenomenon” (where generative models assign higher likelihood to anomalous than normal data) seen in image anomaly detection also occurs in tabular data. It proposes a domain-agnostic definition of the phenomenon based on relative AUROC against baseline models, and through extensive experiments on all 47 tabular datasets and 10 embedding datasets from ADBench, the authors show that such behavior is rare in tabular settings. The paper further provides theoretical analysis linking the phenomenon to dimensionality and feature correlation, and demonstrates that a simple likelihood test with normalizing flows (NF-SLT) is both reliable and competitive for tabular anomaly detection.

## Strengths
- **Clear and practically important research question.** The paper addresses a significant gap: whether the well-documented failure of likelihood-based anomaly detection in images extends to the widely-used tabular domain. This question has direct implications for practitioners.
- **Domain-agnostic definition of the counterintuitive phenomenon.** While the definition (Definition 3.3) relies on thresholds, the effort to formalize a previously vague concept is a valuable contribution that could enable more systematic comparisons across domains.
- **Thorough and unbiased experimental evaluation.** The authors use all 47 tabular and 10 CV/NLP embedding datasets from ADBench without selection bias, and compare against 12 diverse baseline models. The use of extensive hyperparameter search and repeated runs adds reliability.
- **Insight into underlying causes.** The theoretical analysis (Theorem 5.4 and Corollary 5.6) and empirical support via dimensionality reduction (ICA, PCA) and intrinsic dimension estimation provide a plausible explanation rooted in lower dimensionality and weaker feature correlations, distinguishing tabular from image data.
- **Strong empirical performance of NF-SLT.** The model achieves the highest average AUROC/AUPRC, low fail ratio, and competitive results even on embedding datasets, suggesting the simple likelihood test is a strong baseline for tabular anomaly detection.

## Weaknesses
### Fatal
None.

### Major
- **The definition of the counterintuitive phenomenon is not fully operationalized.** Definition 3.3 depends on thresholds β and γ, but these are never specified or justified. The conclusion that the phenomenon is “rare” is therefore drawn without a clear decision rule. For the ‘yeast’ dataset, a min gap of 0.02 is claimed to be insufficient, but what constitutes “significant” (γ) is undefined. Without explicit thresholds, the empirical claim cannot be rigorously validated or falsified.
- **The theoretical analysis relies on the strong assumption of feature independence (P and Q specify the dimensions are independent).** While the paper acknowledges this in the ICA experiments, the main theoretical results (Theorem 5.4, Corollary 5.6) and the dimensionality-reduction experiments that support them (Table 2) assume independence. This limits the direct applicability of the theory to real tabular data where features are often not independent.
- **Evaluation of the phenomenon is indirect.** The paper infers rarity from NF-SLT’s high performance and low fail ratio, rather than directly applying Definition 3.3 with explicit thresholds. The connection between high AUROC/rank and the absence of the phenomenon is intuitive but not formally shown. A direct test (e.g., checking Condition (2) and (3) on each dataset with chosen β, γ) is missing.
- **The bilinear-interpolation experiment (Table 3) is not well-controlled.** The authors note that resizing strengthens pixel correlations, which confounds the dimensionality effect. The results sometimes contradict the theoretical direction (e.g., when SVHN is in-distribution and CelebA is out-of-distribution, AUROC increases as dimension decreases), and the explanations are post-hoc. This limits the strength of the empirical support for the dimensionality hypothesis.

### Minor
- **Intrinsic dimension estimation is sensitive to hyperparameters and estimators.** The paper uses MLE (k=10,20) and TwoNN with a fixed number of neighbors; different choices could alter the quantitative d-Ratio values and the qualitative conclusions.
- **The paper focuses only on one normalizing flow architecture (NICE) for the main experiments.** While Appendix G reports results with other flows, the main claims are tied to NICE. The robustness of the findings to different flow architectures is not fully established in the main text.
- The “high-dimensional tabular data with correlation” limitation is mentioned in the conclusion but not explored in depth. Datasets like genomics are cited, but no experiments are conducted to probe the boundary where the phenomenon might start to appear.

### Trivial
- “Fact 1.1” and “Fact 1.2” are presented as facts but are informal observations; they could be stated more precisely as assumptions or stylized facts.

## Nice-to-Haves
- Specify plausible default values for β and γ in Definition 3.3 (e.g., β=0.5, γ=0.1) and apply the definition directly to both tabular and image datasets to calibrate the method.
- Extend the theoretical analysis to dependent features (e.g., using copula models or factor models) to strengthen the connection with real tabular data.
- Provide an ablation study on the effect of the independence assumption in the theory, e.g., use synthetic data with known correlation structure.
- Include a table that explicitly lists for each dataset whether the counterintuitive phenomenon occurs according to Definition 3.3 with chosen thresholds.

## Novel Insights
Beyond the paper’s own contributions, no fundamentally surprising insight emerges; the finding that tabular data is less prone to likelihood inversion is consistent with known differences in dimensionality and correlation structure between images and tabular data. The most novel aspect is the formal definition and the systematic empirical validation across a large benchmark.

## Suggestions
- **Operationalize the definition.** Provide specific values for β and γ (or a sensitivity analysis over them) and apply Definition 3.3 directly to each dataset. This would make the claim “rare” concrete and reproducible.
- **Relax the independence assumption in theory.** Explore how the likelihood gap behaves under Gaussian or factor-model dependence, or use synthetic experiments with correlated features to complement the ICA experiment.
- **Calibrate on image data.** Show that with the same β/γ thresholds, the definition flags the known counterintuitive cases (e.g., CIFAR-10 vs SVHN) as positive, validating the definition before using it on tabular data.
- **Add a discussion of limitations.** Acknowledge that the theoretical results assume independent features and that the empirical detection of the phenomenon relies on unspecified thresholds.

## Score and Decision
The paper addresses a relevant question with a thorough experimental design and provides a formalization that could be useful beyond this work. However, the major weakness—the lack of operationalized thresholds in the core definition—undermines the central empirical claim and limits the paper’s conclusiveness. A revision that addresses this issue could increase the contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>