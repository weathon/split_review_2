## Summary

This paper investigates whether the counterintuitive phenomenon where deep generative models assign higher likelihoods to out-of-distribution (OOD) data occurs in tabular anomaly detection (AD), as it does in the image domain. The authors propose a domain-agnostic formal definition of this phenomenon based on relative performance against comparison models. Through extensive experiments on 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench, benchmarked against 12 baseline models, they show that normalizing flow-based simple likelihood tests (NF-SLT) rarely exhibit the counterintuitive phenomenon in tabular data and consistently outperform competitors. They further provide theoretical analysis linking the phenomenon to dimensionality and empirical evidence connecting feature correlation (quantified via intrinsic dimension ratio) to likelihood-based detection success.

## Strengths

- **Comprehensive and unbiased empirical study.** The paper evaluates on all 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench, avoiding selection bias (citing Shwartz-Ziv & Armon, 2022). Twelve diverse baselines (shallow and deep AD models) are compared, and results show NF-SLT consistently achieves the best average AUROC (0.8575), average rank (3.43), top-2 ratio (0.45), and fail ratio (0.02). This convincingly demonstrates that likelihood-based detection works well in tabular domains.

- **Formal definition of the counterintuitive phenomenon.** Prior work described the phenomenon vaguely. Definition 3.3 operationalizes it using two intuitive conditions: most comparison models must outperform the generative model (Eq. 2), and the performance gap must be nontrivial (Eq. 3). This provides a principled framework for detecting the phenomenon across domains.

- **Theoretical insight into dimensionality effects.** Theorem 5.4 shows that under independence assumptions, the lower bound of the likelihood gap between normal and abnormal data decreases linearly with dimension \(d\) when entropic conditions hold. Corollary 5.6 links this to an upper bound on AUROC that is inversely related to dimension. These results align with the observation that tabular data has relatively low dimensionality.

- **Empirical validation of dimension and correlation hypotheses.** The ICA-based dimension reduction experiments on images (Table 2) show that lowering dimension substantially increases AUROC when \(\mathbb{H}(P) > \mathbb{H}(Q)\), supporting the theoretical prediction. The intrinsic dimension (ID) analysis (Figure 1, Table 4) demonstrates that tabular datasets have much higher \(d\)-ratio (ID/ambient dimension) than image datasets, indicating weaker feature correlations, which correlates with NF-SLT’s strong performance.

## Weaknesses

### Major

- **Definition 3.3 is not directly applied to the experimental results.** The paper proposes a formal definition of the counterintuitive phenomenon but never explicitly applies it with concrete thresholds \(\beta\) and \(\gamma\) to classify which datasets exhibit the phenomenon. Instead, the rarity claim is supported by aggregated metrics (fail ratio, top-2 ratio, small minimum performance gap on the worst dataset). This leaves a gap between the proposed framework and its empirical backing. To fully support the claim, the authors should operationalize the definition (e.g., \(\beta = 0.5\), \(\gamma = 0.05\)) and report how many tabular datasets satisfy the condition.

- **Theoretical results assume independence (Theorem 5.4, Corollary 5.6).** The independent distribution assumption is strong and does not hold for real-world tabular data (or images). The authors acknowledge this for image interpolation experiments but still use the theorem to argue about tabular data. The feature correlation analysis later suggests that tabular data has weaker correlations, but the theory itself does not directly address non-independent settings. This weakens the theoretical contribution’s direct applicability to the main claim.

- **Causal link between feature correlation and counterintuitive phenomenon is not rigorously established.** The intrinsic dimension analysis shows a correlation between low \(d\)-ratio and cases where NF-SLT underperforms (Table 4 bottom). However, correlation does not imply causation. Alternative explanations (e.g., dataset difficulty, label noise) are not ruled out. The argument that “tabular data is heterogeneous” as the reason for the phenomenon’s rarity remains plausible but speculative.

### Minor

- **The experimental protocol equates anomaly detection and OOD detection.** While the paper notes this in a footnote, the training uses only 50% of normal data (following Zong et al., 2018), which differs from standard OOD settings where the full in-distribution is used for training. This choice affects comparability with some OOD literature and may influence the likelihood test’s behavior.

- **Main results rely on a single normalizing flow architecture (NICE).** Additional flows are reported in Appendix G, but the primary claims are based on NICE. The generalizability to other flow architectures (RealNVP, Glow, etc.) is not fully validated in the main experiments.

- **Dimension reduction on images via ICA changes data properties beyond dimension alone.** Reducing dimension to independent components removes correlation structure, which may confound the effect of dimension reduction with the effect of removing feature correlation. The paper attributes the AUROC improvement to dimension, but the intervention is not purely dimensional.

- **The definition of counterintuitive phenomenon uses AUROC ranking against other models, which may conflate phenomenon with model choice.** The phenomenon is intrinsically tied to the generative model underperforming other methods. If the generative model happens to be strong, the phenomenon cannot occur by definition. Thus, the paper’s conclusion that the phenomenon is rare in tabular data partly follows from NF-SLT being a strong method, which is a positive finding but not surprising given the domain.

### Trivial

- No significant issues.

## Nice-to-Haves

- Apply Definition 3.3 concretely with specified \(\beta\) and \(\gamma\) values and report the fraction of tabular datasets that satisfy the counterintuitive phenomenon condition.
- Extend the theoretical analysis to settings with feature correlations (e.g., using covariance structure) to strengthen the link between theory and the tabular domain.
- Investigate the effect of training set size and anomaly contamination rate on the likelihood test’s performance in tabular data.
- Compare NF-SLT against more recent flow-based AD methods that incorporate auxiliary statistics (e.g., LID, typicality tests) to further contextualize the performance.

## Novel Insights

Beyond the paper’s own contributions, the insight that the counterintuitive likelihood phenomenon is highly domain-dependent, mediated by dimensionality and feature correlation, is valuable. The use of intrinsic dimension ratio (\(d\)-ratio) as a diagnostic tool to predict when likelihood-based detection will succeed or fail is a novel perspective that could guide practitioners. The observation that even within tabular data, datasets with low \(d\)-ratio (higher correlation) are precisely where NF-SLT underperforms (Table 4 bottom) suggests that intrinsic dimension is a meaningful indicator of likelihood-based AD efficacy.

## Suggestions

- **Operationalize and test Definition 3.3 explicitly.** Choose reasonable thresholds (e.g., \(\beta = 0.5\), \(\gamma = 0.05\)) and classify each of the 47 datasets. Show that very few (e.g., 0–2) satisfy the condition, directly supporting the claim that the counterintuitive phenomenon is rare.
- **Strengthen the theoretical link by relaxing the independence assumption.** Consider analyzing how feature correlation affects the likelihood gap (e.g., using the covariance structure in Eq. 5) and deriving bounds that depend on intrinsic dimension rather than ambient dimension.
- **Conduct an ablation on tabular data: artificially increase feature correlation (e.g., via adding dependent features) and observe whether counterintuitive behavior emerges.** This would provide direct causal evidence for the correlation hypothesis.
- **Include a discussion on the choice of \(\beta\) and \(\gamma\) thresholds and their sensitivity.** This would make the definition more practical and reproducible.

## Score and Decision

The paper makes a solid empirical contribution by demonstrating the effectiveness of likelihood-based anomaly detection in the tabular domain on a large-scale benchmark, and it provides a formal definition and initial theoretical insight into the phenomenon. However, the disconnect between the formal definition and its empirical application, combined with assumptions in the theoretical analysis, prevent the paper from being a fully resolved treatment. Despite these weaknesses, the empirical findings are valuable to the community and likely to influence practical deployment of flow-based AD in tabular settings. The paper is above the acceptance threshold but has room for improvement.

**Score:** 6  
**Decision:** Accept  

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: Accept