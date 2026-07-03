I have verified the relevant sections. Let me now produce the final review.

## Summary

This paper empirically studies whether the "counterintuitive phenomenon" where deep generative models assign higher likelihoods to out-of-distribution data than in-distribution data—well-documented in images—occurs in tabular anomaly detection. The authors propose a domain-agnostic definition (Definition 3.3) based on relative AUROC comparisons against baselines, then benchmark NF-SLT (a normalizing flow with a simple likelihood test) across all 47 tabular datasets from ADBench against 12 baselines. NF-SLT achieves strong aggregate performance (avg AUROC 0.8575, avg rank 3.43). The paper provides theoretical analysis (Theorem 5.4) linking the likelihood gap to dimensionality and empirical analysis relating feature correlation (via intrinsic dimension) to detection performance.

## Strengths

- **Exhaustive benchmarking without selection bias (Table 1, Section 4):** The paper uses all 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench against 12 baselines, explicitly citing Shwartz-Ziv & Armon (2022) to justify avoiding cherry-picking. NF-SLT achieves the best average AUROC (0.8575), AUPRC (0.6398), average rank (3.43), Top2 Ratio (0.45), and the lowest Fail Ratio (0.02). This is a substantial and well-executed empirical study.

- **Theoretical connection between dimensionality and likelihood gap (Theorem 5.4, Corollary 5.6):** The paper proves that under independent-factor assumptions, the lower bound of the expected likelihood gap between normal and anomalous data decreases linearly with dimension d, and the maximum achievable AUROC is inversely related to d. This extends the likelihood-gap framework of Caterini & Loaiza-Ganem (2022) and gives a formal rationale for why lower-dimensional tabular data may avoid likelihood inversion.

- **Controlled dimensionality experiments supporting the theory (Table 2):** ICA-based dimensionality reduction on images (1024→30 components) shows AUROC rising substantially when ℍ(P) > ℍ(Q)—e.g., CIFAR-100/SVHN from 0.0843 to 0.3490—directly supporting Theorem 5.4's predictions.

- **Intrinsic-dimension analysis linking feature correlation to detection (Section 5.2, Figure 1, Table 4):** The paper estimates ID for tabular and image datasets, showing image d Ratio ≈ 1% while tabular datasets are far higher (e.g., magicgamma 0.700, waveform 0.810). The toy covariance experiment (Equation 5) validates that correlation strength reduces ID. Table 4 (bottom) further shows that low-d Ratio correlates with worse NF-SLT ranking, providing evidence for the feature-correlation explanation.

- **Consistency check on CV/NLP embeddings (Section 5.2):** ADBench CIFAR-10/SVHN embeddings have estimated IDs of 23 and 18 (ambient dim 1000), yielding higher d Ratio than raw pixels. This explains why NF-SLT succeeds on embeddings and is consistent with Kirichenko et al. (2020)—a cross-check that strengthens the explanatory story.

## Weaknesses

### Fatal

None.

### Major

- **Definitional mismatch between the paper's framing and its evidence (Major):** Definition 3.3 operationalizes the "counterintuitive phenomenon" through relative model ranking: the proportion of baselines that outperform the generative model exceeds β, and the minimum AUROC gap exceeds γ. This conflates two distinct situations: (A) genuine likelihood inversion where AUROC < 0.5 (the phenomenon documented in images, e.g., CIFAR-10/SVHN AUROC 6.4%), and (B) the generative model simply being less accurate than specialized anomaly detectors (e.g., AUROC 0.86 vs. 0.90). Under Definition 3.3, the conclusion that the phenomenon is "rare" follows partly because NF-SLT happens to be a strong method on tabular data (avg AUROC 0.8575)—not because likelihood inversion is specifically absent. The paper's justification (lines 25–26) mischaracterizes the existing definition ("any result outside 100% AUROC as counterintuitive"), which no prior work actually claimed, and then proposes a definition that discards the core notion of likelihood inversion. The result is that the paper answers a different question than the one posed in the introduction.

- **β and γ thresholds unspecified (Major):** Definition 3.3 depends on two free parameters β and γ (Equations 2–3), but their values are never stated in the main text. The paper defers to "the fully rigorous formulation" in Appendix B, which is not available in the main submission. Without β and γ, the reader cannot independently verify whether any specific dataset satisfies Definition 3.3. The paper's central empirical claim—that the phenomenon is "consistently rare"—is therefore not verifiable from the presented evidence alone.

- **Hyperparameter selection protocol may inflate NF-SLT's standing (Major):** Lines 122–123 state: "the hyperparameter combination with the highest average AUROC for all datasets is selected as the representative hyperparameter combination." This selects hyperparameters based on **test-set** AUROC averaged across all datasets—a form of data leakage. The paper does not clarify whether the 12 baseline models received comparable hyperparameter optimization. If baselines used default or lightly-tuned settings while NF-SLT's were chosen to maximize test-set AUROC, the comparison is materially unfair and the reported margins may be inflated.

### Minor

- **Theorem 5.4 relies on strong independence assumptions not satisfied by real tabular data:** The theorem assumes P = ∏p_i(x_i) and Q = ∏q_i(x_i) (factorized independent distributions). The ICA experiment (Table 2) creates data that artificially satisfies this assumption, validating the theorem under its own conditions rather than providing independent evidence. The bilinear interpolation experiment (Table 3) produces results that "conflict with the theorems" (line 176), which the paper acknowledges but cannot resolve within the theoretical framework.

- **Per-dataset AUROC for tabular data not shown in main text:** Table 1 reports only aggregate metrics across 47 datasets. The reader cannot assess performance variability or identify specific failure cases. Only the 'yeast' dataset is mentioned qualitatively (gap of 0.02). Individual results may be in the stripped appendix, but the main text lacks this distributional view.

- **No statistical significance reported:** The paper reports averages across 10 repeated experiments but does not provide confidence intervals or significance tests for the differences between NF-SLT and baselines.

### Trivial

None.

## Nice-to-Haves

- Specify β and γ values in the main text and justify their choice with reference to the image-domain results (e.g., what values would classify CIFAR-10/SVHN as exhibiting the phenomenon?).
- Report per-dataset AUROC for all 47 tabular datasets (as a table or figure) to enable readers to see the full distribution.
- Add confidence intervals or statistical tests for the key AUROC comparisons.
- Disclose the hyperparameter tuning protocol for all baselines, or report results with both tuned and default settings for fairness.

## Removed Points

These points were flagged by one or both reviewers but removed after verification. Treat them with caution if reviewing on your own.

- **"Facts 1.1 and 1.2 are coarse generalizations"** (Harsh Critic): The paper uses qualifiers like "generally" and acknowledges exceptions (e.g., genomics datasets in Appendix C.4). The framing is reasonable for a high-level characterization.
- **"Theorem 5.4 only proves lower bound, not actual gap"** (Harsh Critic): The theorem shows the lower bound decreases linearly, which is directly relevant to understanding when the gap can become negative. The criticism misreads the theorem's purpose.
- **"Section 5.2 does not directly test the causal chain"** (Harsh Critic): The paper provides correlational evidence (d Ratio differences, Table 4 bottom), which is appropriate for an empirical analysis of this type. The criticism demands an experiment outside the paper's stated scope.
- **Several formatting and presentation nitpicks** (both reviewers): Removed per instruction—these are parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the paper's contribution.** The current framing (studying whether the "counterintuitive phenomenon" occurs) is misaligned with the evidence, because Definition 3.3 recasts the phenomenon in terms of relative model performance rather than likelihood inversion. The paper would be substantially stronger if it honestly reframed its contribution as: "NF-SLT with simple likelihood testing is a practical and competitive approach for tabular anomaly detection, and the reasons it avoids the likelihood inversion failure seen in images can be traced to differences in dimensionality and feature correlation." This would resolve the definitional tension and better match the evidence.

2. **Specify β and γ explicitly** in the main text. Without these values, the central claim is unverifiable.

3. **Clarify the hyperparameter selection protocol** for NF-SLT and all baselines. Report results with both the selected configuration and default/baseline configurations to allow readers to assess the impact.

4. **Show per-dataset AUROC results** for all 47 tabular datasets, even as a supplementary figure, so readers can assess variability.

## Score and Decision

Based on my analysis: the paper makes genuine contributions—an exhaustive benchmark, a theoretical dimensionality result, and an intrinsic-dimension analysis. However, the definitional mismatch is structural (the paper studies a different question than it claims), the β/γ thresholds are unspecified, and the hyperparameter protocol raises fairness concerns. These are significant issues that prevent the paper from being acceptable in its current form, though the empirical findings and analyses could form the basis of a strong paper after substantial reframing and clarification.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>