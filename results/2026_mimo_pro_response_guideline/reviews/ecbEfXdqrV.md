Now I have enough calibration data. Let me finalize my analysis.

**Round 1 Bracket: 5.5 – 6.5**

Key comparison points:
- "NCSNAD" (5.75, Reject): Similar approach — applies existing generative model (NCSN) to tabular AD with extensive benchmark. Criticized for limited novelty and fairness concerns. Our paper has additional theoretical contribution.
- "AVOID" (6.00, Reject): Analyzes DGM overestimation in OOD detection, proposes fix. Similar theoretical/empirical investigation style. Our paper has broader evaluation.
- "MCM" (6.67, Accept): Novel method for tabular AD with strong experiments on 20 datasets. More novel method but narrower evaluation.
- "AnoLLM" (6.75, Accept): Novel LLM-based tabular AD approach. Similar evaluation breadth.

Our paper is an empirical/theoretical investigation rather than a methods paper. Its comprehensive evaluation (47 datasets + theory) is a strength, but the non-operational definition and hyperparameter protocol concerns are real issues that hold it back.

Let me finalize the review and write it out.

## Summary
This paper investigates why the counterintuitive phenomenon (where generative models assign higher likelihoods to anomalous than normal data, well-documented in image domains) is rare in tabular anomaly detection. The authors propose a domain-agnostic formal definition of this phenomenon (Definition 3.3), demonstrate through extensive experiments on 47 tabular and 10 CV/NLP embedding datasets from ADBench against 12 baselines that NF-SLT (Normalizing Flow with Simple Likelihood Test) achieves strong performance with only a 2% fail ratio (Table 1), and provide theoretical analysis (Theorem 5.4) and empirical validation attributing this success to tabular data's lower dimensionality and weaker feature correlations (d-Ratio analysis).

## Strengths
- **Comprehensive, unbiased evaluation**: The paper evaluates on all 47 tabular + 10 CV/NLP embedding datasets from ADBench with no dataset selection, directly addressing Shwartz-Ziv & Armon (2022)'s criticism of cherry-picking. Against 12 baselines (6 shallow, 6 deep), NF-SLT achieves 0.8575 AUROC, average rank 3.43, and a fail ratio of only 0.02 (Table 1). This substantially extends prior work (Kirichenko et al., 2020) that examined only 2 tabular datasets.
- **Theoretical contribution on dimensionality and likelihood inversion**: Theorem 5.4 extends Caterini & Loaiza-Ganem (2022) to show that for independent d-dimensional distributions where H(P) > H(Q), the lower bound of the expected likelihood gap decreases linearly in d. Corollary 5.6 further shows the AUROC upper bound becomes inversely proportional to d. This provides a principled explanation for why low-dimensional tabular data avoids the likelihood inversion phenomenon.
- **Multi-pronged empirical validation**: Tables 2 and 3 use dimensionality reduction (ICA + RealNVP, bilinear interpolation + Glow) to show AUROC increases as dimension decreases when H(P) > H(Q), confirming theoretical predictions. The d-Ratio analysis (Table 4, Figure 1) quantifies feature heterogeneity via intrinsic-to-ambient dimension ratio, showing tabular data has d-Ratio near 1 while image data has d-Ratio ~1%.
- **Internal consistency**: Table 4 demonstrates that 92% of datasets where NF-SLT underperforms (rank ≥ 3) have d-Ratio < 0.7, establishing a clear link between feature heterogeneity and likelihood-test success. The CV/NLP embedding results (intrinsic dimensions 18-23 vs. ambient 1000) further validate the framework.

## Weaknesses

### Fatal
None.

### Major
- **Definition 3.3 leaves β and γ unspecified**: The paper's first listed contribution is a formal definition, but the two parameters that determine when the counterintuitive phenomenon "occurs" — β (proportion threshold, Equation 2) and γ (minimum AUROC gap, Equation 3) — are never assigned concrete values. The definition thus remains a template rather than a testable criterion. The paper applies it informally (line 124: "the minimum performance difference between MCM and AUROC is 0.02; hence, we cannot assume that it exhibited low performance due to a counterintuitive phenomenon"), but this post-hoc reasoning is not the same as applying a fixed criterion. Committing to specific values and reporting exactly how many datasets trigger the definition would make the central claim concrete and independently verifiable.

- **Non-standard global hyperparameter selection protocol with potential asymmetry**: The evaluation selects a single hyperparameter configuration per model by "the hyperparameter combination with the highest average AUROC for all datasets" (line 122), which is non-standard and disadvantages models that are more hyperparameter-sensitive. Additionally, NF-SLT's hyperparameters are described separately as specific values ("10 coupling layer, 200 epochs, weight decay 1e-4," line 120), creating ambiguity about whether NF-SLT underwent the same global search protocol as baselines — potentially introducing asymmetry that favors NF-SLT.

### Minor
- **Only NICE architecture in main results**: Table 1 uses NICE exclusively. While the paper notes Appendix G contains results with other flows, the claim that normalizing flow likelihood tests are "generally reliable" for tabular AD requires broader support in the main text. The phenomenon's severity is known to depend on flow architecture in the image domain. Including even one additional flow family in Table 1 would substantially strengthen the generality claim.

- **Gap between theoretical assumptions and empirical domain**: Theorem 5.4 requires P and Q to be independent d-dimensional product distributions. This is violated by essentially all real datasets. Table 3 (image resizing without independence assumption) shows some results that contradict the theorem's predictions (SVHN-in/CelebA-out: AUROC increases from 0.15 to 0.70 with decreasing dimension), which the paper explains speculatively via entropy changes from bilinear interpolation. The disconnect between the theory and empirical results should be stated more explicitly — the theorem provides intuition, not a direct explanation for real data.

- **Title/framing presupposes the conclusion**: The title asks "why is the phenomenon rare" before establishing that it is rare. Framing the contribution as investigating *whether* and then *why* would be more rigorous.

### Trivial
- The Fail Ratio threshold (rank ≥ 9th out of 12 models) is arbitrary and not discussed.
- The d-Ratio analysis does not disentangle correlation from dimensionality — low d-Ratio datasets tend to be higher-dimensional, making it unclear which factor dominates.

## Nice-to-Haves
- Per-dataset hyperparameter results alongside global results would eliminate the most significant methodological concern.
- A multivariate analysis in Section 5.2 controlling for ambient dimension would strengthen the d-Ratio analysis.
- Systematic analysis of NF-SLT failure cases, correlating relative rank with dataset properties (dimension, d-Ratio, anomaly ratio, feature types).

## Removed Points
These points are flagged to be removed, treat them with caution.
- None removed. All reviewer weaknesses were verified against the paper text and kept, demoted, or adjusted in severity as appropriate.

## Novel Insights
The combination of the formal definition (despite unspecified parameters), the comprehensive empirical demonstration that NF-SLT's fail ratio is only 2% across all ADBench datasets, and the dual theoretical/empirical explanation via dimensionality and feature correlation (d-Ratio) collectively establish a practically important finding: simple flow-based likelihood tests are reliable for tabular anomaly detection, contrary to the problems documented in images. The d-Ratio concept — quantifying feature heterogeneity via intrinsic-to-ambient dimension ratio — provides a useful diagnostic for predicting when NF-based anomaly detection will succeed.

## Suggestions
- Specify concrete β and γ values in Definition 3.3 and report how many datasets trigger the definition under those values.
- Present results under both global and per-dataset hyperparameter selection to verify the conclusion is robust.
- Include at least one additional flow family (RealNVP or Glow) in the main table.
- Add explicit language in Section 5.1 stating that Theorem 5.4 provides a sufficient-but-not-necessary condition and that the empirical evidence extends beyond the theorem's independence assumption.

---

## Reporting: Calibration Anchor Comparison

| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| "Normalizing Flows For OOD Detection via Latent Density Estimation" | 3.40 | R1 | Similar topic but much more limited evaluation (~6 datasets), novelty concerns. Our paper substantially stronger. |
| "Dealing with Out of Distribution in Prediction Problem" | 2.50 | R1 | OOD on tabular data but very limited scope. Our paper far more comprehensive. |
| "TabKANet: Tabular Data Modeling with KAN" | 3.00 | R1 | Tabular data modeling, different focus. Less relevant. |
| "Inference, Fast and Slow: Reinterpreting VAEs for OOD Detection" | 4.67 | R1 | Similar OOD detection theme but poor presentation, conceptual issues, limited experiments. Our paper clearly stronger. |
| "Explaining the OOD Detection Paradox through Likelihood Peaks" | 5.67 | R1,R2 | Highly relevant — analyzes likelihood inversion via LID. More elegant theoretical mechanism but much narrower experiments. Our paper has broader evaluation but less precise theory. |
| "AVOID: Alleviating VAE's Overestimation in Unsupervised OOD Detection" | 6.00 | R2 | Analyzes DGM overestimation in OOD detection, proposes fix. Experiments centered on FashionMNIST/CIFAR-10. Our paper has broader evaluation, similar theoretical investigation style. Comparable quality. |
| "Anomaly Detection by Estimating Gradients (NCSNAD)" | 5.75 | R1,R2 | Most similar in structure — applies existing generative model to tabular AD with large benchmark. Rejected despite extensive experiments due to limited novelty and fairness concerns. Our paper has additional theoretical contribution. |
| "DRL: Decomposed Representation Learning for Tabular AD" | 5.75 | R2 | Novel method for tabular AD, accepted at this level. More method novelty, narrower evaluation. |
| "Double Descent Meets OOD Detection" | 6.50 | R2 | Theoretical analysis, different focus. Less directly comparable. |
| "MCM: Masked Cell Modeling for Tabular AD" | 6.67 | R1,R2 | Novel method for tabular AD, accepted. More method novelty (20 datasets) but narrower evaluation than our paper. |
| "AnoLLM: LLMs for Tabular Anomaly Detection" | 6.75 | R1,R2 | Novel approach, accepted. Similar evaluation breadth. |
| "Deep Orthogonal Hypersphere Compression" | 8.00 | R1 | Strong anomaly detection paper with novel method. Clearly above our paper. |

**Round 1 bracket**: 5.5 – 6.5. Our paper is clearly above the NCSNAD (5.75, Reject) and AVOID (6.00, Reject) papers due to broader evaluation and theoretical contribution, but below MCM (6.67) which has a genuinely novel method. 

**Final score**: 6.0. The paper is at the weak-accept/borderline level — comparable to AVOID (6.00) but with better evaluation breadth. The non-operational definition and hyperparameter protocol issues prevent a higher score, but the comprehensive evaluation, theoretical contribution, and practical importance of the finding warrant acceptance.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>