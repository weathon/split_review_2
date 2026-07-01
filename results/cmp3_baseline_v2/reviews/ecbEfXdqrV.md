## Summary

The paper investigates whether the well-known counterintuitive phenomenon where deep generative models assign higher likelihoods to out-of-distribution than in-distribution data (prevalent in images) also occurs in tabular anomaly detection. It proposes a domain-agnostic definition of this phenomenon based on relative performance against comparison models. Through extensive experiments on 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench, using 12 baselines, it finds that NF-SLT (Normalizing Flow with Simple Likelihood Test) rarely exhibits this counterintuitive behavior and outperforms competing methods by a clear margin. The paper also attempts to explain this rarity through theoretical analysis of dimensionality and empirical analysis of feature correlation (measured via intrinsic dimension reduction).

## Strengths

- **Clear and practically relevant research question**: Examining whether the counterintuitive likelihood phenomenon extends to tabular anomaly detection is timely and fills a concrete gap in the literature—most prior work focuses on image or embedding data.
- **Extensive and well-designed experimental setup**: The paper evaluates on all 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench without selection bias, against 12 diverse anomaly detection baselines (shallow and deep). This is far more comprehensive than prior tabular studies (e.g., Kirichenko et al. only used two datasets).
- **Strong empirical evidence**: NF-SLT achieves the highest average AUROC (0.8575) and AUPRC (0.6398), lowest average rank (3.43), highest Top2 ratio (0.45), and notably low Fail Ratio (0.02). These results convincingly support the claim that the phenomenon of interest is rare in tabular data.
- **Provides a formal definition of the phenomenon** (Definition 3.3) that moves beyond vague statements about likelihood overlap. While the definition has limitations (see weaknesses), it represents an attempt at operationalization that can be adopted, refined, or debated by the community.
- **Offers both theoretical and empirical explanations**: The paper links dimensionality and feature correlation (via intrinsic dimension ratio) to the likelihood gap. The experiments in Table 2 (ICA-based dimensionality reduction) and the intrinsic dimension analysis (Figure 1, Table 4) provide supportive evidence for the proposed mechanisms.

## Weaknesses

### Major

- **Definition of the counterintuitive phenomenon is not quantitatively operationalized in the experiments.** Definition 3.3 depends on hyperparameters β (proportion of outperforming models) and γ (minimum performance gap), but these are never specified or applied. The subsequent argument relies on qualitative inspection (e.g., comparing fail ratios and small performance differences on the "yeast" dataset) rather than a formal application of the definition. Without concrete thresholds, the claim that the phenomenon is “rare” lacks a precise empirical grounding, and the definition itself cannot be validated or falsified in the current framework.
- **Theoretical results (Theorem 5.4, Corollary 5.6) assume product distributions (independent features).** This assumption is rarely satisfied in real-world tabular data, where feature correlations are present (though possibly weaker than in images). The paper does not discuss how violations of independence affect the derived lower bounds or the AUROC upper bound. The theoretical connection to the observed empirical results is therefore tentative, and the independence assumption limits the practical relevance of the theoretical insights.
- **Intrinsic dimension analysis is not performed across all 47 tabular datasets.** The scatter plot in Figure 1 (right) and the d-ratio examples in Table 4 cover only a handful of tabular datasets (magicgamma, satellite, landsat, waveform). The claim that “tabular data generally have lower correlation” (higher d-ratio) is not substantiated for the full ADBench suite. Without a comprehensive ID analysis, it is unclear whether the few shown examples are representative or cherry-picked. The paper mentions that “even within the tabular domain, 25 datasets where NF-SLT does not achieve top performance” and then shows a sub-table (Table 4 bottom) about the fraction of those with low d-ratio, but this analysis still depends on ID estimates for those 25 datasets, which are not reported or summarized.
- **The empirical results focus on a single normalizing flow architecture (NICE).** While Appendix G mentions other flows, the main narrative and all aggregated tables rely on NICE. The general claim that “simple likelihood testing with normalizing flows rarely leads to the counterintuitive phenomenon” might be architecture-dependent. For example, flows with volume-preserving transformations (like NICE) vs. volume-changing transformations (RealNVP, Glow) could behave differently. The paper should present at least a brief comparison of multiple flow types on a subset of tabular datasets to support the general claim.

### Minor

- **The dimensionality reduction experiment (Table 3) using bilinear interpolation yields non-monotonic and sometimes contradictory results** compared to the theoretical predictions. The paper acknowledges this but the explanation (correlation introduced by interpolation) is post-hoc. The connection to tabular data remains indirect, and the value of that experiment for supporting the main thesis is limited.
- **The Fail Ratio threshold (rank 9th or lower out of 12 models) is arbitrary.** Different choices could alter the apparent robustness. A sensitivity analysis or justification would strengthen the claim.
- **The paper could benefit from reporting confidence intervals or statistical significance tests** for the AUROC and AUPRC differences, given that 10 repeated experiments are performed.

### Trivial

- None that affect the evaluation.

## Nice-to-Haves

- Operationalize Definition 3.3 by choosing specific (β, γ) values (e.g., β=0.5, γ=0.05) and explicitly apply it to all datasets. Report the proportion of datasets where the phenomenon qualifies as occurring.
- Provide ID ratio (d-ratio) estimates for all 47 tabular datasets, e.g., as a histogram or boxplot, and discuss the correlation with NF-SLT’s rank or AUROC.
- Show the effect of violating the independence assumption in the theoretical analysis, e.g., by analyzing Gaussian copula or factor-model data with controlled correlation.
- Compare multiple normalizing flow backbones (NICE, RealNVP, Glow, FFJORD) on a representative subset of tabular datasets to show that the low-failure phenomenon is not architecture-specific.

## Novel Insights

The paper’s central insight—that the counterintuitive likelihood phenomenon is domain-dependent, with tabular data being far less susceptible than images, and that this can be explained by lower dimensionality and weaker feature correlations—is both novel and practically valuable. The attempt to formalize the phenomenon via relative model performance is a useful step toward making discussions of this issue more rigorous. The empirical demonstration that NF-SLT outperforms many strong baselines on tabular anomaly detection is a concrete takeaway for practitioners who might otherwise dismiss likelihood-based methods due to their known failures in vision.

## Suggestions

- **Operationalize your definition clearly.** Choose a concrete (β, γ) pair, justify it, and apply it to the experimental results. This would greatly strengthen the claim that the counterintuitive phenomenon is rare.
- **Broaden the ID analysis.** Compute intrinsic dimension for all 47 tabular datasets and present a summary (e.g., distribution of d-ratio). Examine whether datasets where NF-SLT underperforms correspond to those with lower d-ratio.
- **Strengthen theoretical contribution.** Discuss how the theoretical results extend (or fail to extend) to correlated features. Consider a more general bound that includes a correlation term.
- **Add statistical rigor.** Report standard deviations or confidence intervals for the main performance metrics.

## Score and Decision

Score: 6  
Decision: Accept (borderline)

The paper presents a clear, well-motivated, and empirically thorough study on an important practical question. The main weaknesses are that the proposed formal definition is not operationalized, the theoretical analysis relies on a strong assumption, and the intrinsic dimension analysis is not comprehensive enough to support all claims. Nevertheless, the core empirical finding—that NF-SLT works robustly for tabular anomaly detection—is solid and of practical value. I lean toward acceptance with the expectation that the authors can address the definition and analysis gaps during revision.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>