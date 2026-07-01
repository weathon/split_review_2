Now I have all the info I need. Let me produce the final consolidated review.

**Bracket statement from calibration:** After comparing with anchors — "Normalizing Flows For OOD Detection via Latent Density Estimation" (3.40, weaker evaluation), "Autoencoders for AD are Unreliable" (4.50, similar framing but stronger theory), "Explaining OOD Detection Paradox through Likelihood Peaks" (5.67, stronger execution on similar topic), and "Anomaly Detection by Estimating Gradients" (5.75, broader evaluation) — I place this paper in the 4.0-5.0 range.

---

## Summary

This paper investigates why the "counterintuitive phenomenon" (generative models assigning higher likelihoods to anomalous data) appears rare in tabular anomaly detection. It proposes a formal definition of the phenomenon based on relative model comparisons (Definition 3.3), benchmarks NF-SLT (a NICE normalizing flow with simple likelihood test) against 12 baselines across all 47 tabular and 10 CV/NLP embedding datasets from ADBench, and provides both theoretical (dimensionality-based likelihood-gap bound under independence) and empirical (intrinsic dimension analysis of feature correlation) explanations. NF-SLT achieves the best aggregate AUROC (0.8575), average rank (3.43), and fail ratio (0.02).

## Strengths

- **Comprehensive, selection-bias-free evaluation.** Tests on all 47 tabular datasets and all 10 CV/NLP embeddings from ADBench against 12 baselines, directly addressing the selection-bias critique (Shwartz-Ziv & Armon, 2022). NF-SLT's aggregate results (AUROC 0.8575, rank 3.43, fail ratio 0.02) are genuinely strong across this large benchmark.
- **Intrinsic dimension analysis connecting feature correlation to NF performance.** The toy experiment (Figure 1, left/center) cleanly demonstrates that stronger correlation (higher ρ) reduces estimated ID, and the ID-ratio comparison between tabular and image datasets (Table 4, Figure 1 right) provides concrete evidence supporting the claim that tabular features are less correlated than image pixels. The finding that NF-SLT underperforms on low-d-ratio datasets even within the tabular domain is a useful empirical generalization.
- **Direct theoretical treatment of dimensionality.** Theorem 5.4 derives a lower bound on the likelihood gap that scales linearly with dimension d under the assumption of independent dimensions, formalizing the intuition that high dimensions can amplify the likelihood-inversion problem when H(P) > H(Q) holds.

## Weaknesses

### Major

1. **Definition 3.3 is never operationalized with concrete thresholds.** The paper introduces β and γ in Definition 3.3 (Eqs 2 and 3) but never specifies their values or evaluates the equations per dataset. The central claim that the phenomenon "rarely occurs" is supported by proxy reasoning (fail ratio; a qualitative AUROC gap of 0.02 on the yeast dataset) rather than by the paper's own formal definition. This is not a fatal issue — the conclusion would likely hold under reasonable thresholds (e.g., β=0.5, γ=0.05) — but it means the paper's headline analytical apparatus is not actually applied to its own data. Without this computation, the claim rests on informal intuition.

2. **The paper does not discuss DAGMM as a significant counterexample.** DAGMM (AUROC 0.6467, average rank 10.51, fail ratio 0.85) is also a deep generative model. Under Definition 3.3, many datasets would likely exhibit the counterintuitive phenomenon for DAGMM. The paper's title and framing refer broadly to "tabular anomaly detection with deep generative models," but the evidence only covers NF-SLT (a specific normalizing flow architecture). This scope gap — whether the phenomenon is rare for generative models generally or only for normalizing flows — is not addressed.

3. **No variance or uncertainty reporting despite 10 repeated runs.** All results in Table 1 are point estimates with no standard deviations, confidence intervals, or significance tests. The reader cannot assess whether NF-SLT's performance advantage over the second-best model (0.8575 vs. ICL's 0.8208) or the 0.02 gap on yeast is reliable, which weakens the quantitative argument.

4. **Unusual global hyperparameter selection method.** The paper states (line 122): "the hyperparameter combination with the highest average AUROC for all datasets is selected." This selects a single global configuration per model that maximizes the average across all datasets, rather than per-dataset selection via validation splits (which is standard in ADBench). This choice could systematically favor methods with consistent-but-not-peak performance and should be justified or analyzed for sensitivity.

### Minor

5. **The independence assumption in Theorem 5.4 limits its connection to real data.** The theorem assumes P and Q are product distributions, which does not hold for real tabular data where features can be correlated. The paper acknowledges this limitation (Table 3 results are described as "conflicting with the theorems," line 176), but the severity for tabular data applications is not discussed. The theory provides useful stylized intuition but does not directly support the empirical conclusions.

6. **ID conflates correlation with general nonlinear structure.** The paper uses ID as a proxy for "feature correlation" (line 226), but ID measures the intrinsic dimensionality of the data manifold, which is reduced by any nonlinear structure (clustering, manifold curvature) — not just the kind of pairwise local correlation that Kirichenko et al. (2020) discuss. The connection is suggestive but imprecise.

7. **Per-dataset tabular AUROC values are not shown in the main paper.** Only aggregate metrics appear in Table 1; individual dataset performance (beyond the single yeast example) is not visible. Given that the argument depends on per-dataset analysis of the definition's conditions, the reader cannot verify whether the phenomenon occurs on specific datasets from the main text alone.

### Trivial

None.

## Nice-to-Haves

- Specify β and γ and directly compute Definition 3.3 per dataset (a simple table showing for each dataset whether Eqs 2 and 3 are satisfied).
- Report the original AUROC < 0.5 metric alongside Definition 3.3 to bridge to prior literature.
- Add standard deviations or confidence intervals from the 10 repeated runs.
- Discuss whether DAGMM exhibits the phenomenon under Definition 3.3 to clarify the paper's scope.
- Clarify and justify the global hyperparameter selection procedure; ideally report sensitivity to this choice.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution if referenced.

1. **"The redefinition of the phenomenon conflates two distinct questions."** — The paper explicitly argues in the introduction (lines 24–27) that the original AUROC < 0.5 standard is too broad ("any result outside 100% AUROC as counterintuitive") and proposes a more sophisticated definition. This is a motivated methodological choice, not a flaw. However, the related point about DAGMM (merged into Major Weakness 2 above) is kept.

2. **"The theoretical analysis does not connect to the empirical results."** — The paper acknowledges the independence assumption explicitly and presents the bilinear interpolation results as a separate experiment where "the theorem ... cannot be applied" (line 164). The theory is presented as a stylized formalization, not as a direct explanation of the real data results. The ID analysis (Section 5.2) is the primary empirical explanation. This is an honest scoping choice.

3. **"Kirichenko et al. (2020) already showed likelihood overlap on tabular data"** — The paper cites Kirichenko et al. (2020) in the introduction (line 19) and explicitly describes its limitation ("only two datasets," "no comparison with other comparison models"). The paper's added value (scale, definitional framework, ID analysis) is delineated.

4. **"The conclusion claims too broadly"** — The conclusion states "this phenomenon rarely occurs in tabular data with simple likelihood tests using normalizing flows," which is a reasonable summary of what the paper shows. The title and framing about "deep generative models" more broadly is a concern but is addressed by the DAGMM counterexample point (kept in Major Weaknesses).

5. **Various minor speculative criticisms** (e.g., about flow architecture choice being unacknowledged, about ID estimator tendencies) that are either acknowledged in the paper or lack specific textual evidence.

## Novel Insights

The paper's most novel insight is the empirical connection between the intrinsic-dimension ratio (d-ratio, the ratio of estimated intrinsic dimension to ambient dimension) and normalizing flow performance on tabular anomaly detection. The finding that NF-SLT underperforms precisely on tabular datasets with low d-ratio (Table 4, bottom) provides a concrete, measurable predictor — not just a post-hoc explanation — for when likelihood-based detection may struggle. This is a useful empirical generalization that goes beyond prior informal observations about feature correlation.

## Suggestions

1. **Directly apply Definition 3.3.** Choose reasonable β and γ values (e.g., β=0.5, γ=0.05), compute Eqs 2 and 3 per dataset, and report the count of datasets where the phenomenon occurs. This would close the gap between the paper's formal framework and its empirical evidence.

2. **Add variance information.** Report standard deviations from the 10 repeated runs in Table 1, at least for the key metrics (AUROC of the top models).

3. **Discuss DAGMM.** Acknowledge that DAGMM (another generative model) performs poorly, and clarify whether the paper's claim about "deep generative models" generalizes or is specific to normalizing flows.

4. **Address hyperparameter selection.** Discuss why a global (average-maximizing) configuration was chosen over per-dataset selection, and analyze sensitivity to this choice.

5. **Show per-dataset tabular results.** Include a table of per-dataset AUROC values (at least for the tabular data) to allow readers to verify the definition-based analysis.

## Score and Decision

**Anchors used for calibration (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Normalizing Flows For OOD Detection via Latent Density Estimation (6Z8rZlKpNT) | 3.40 | Round 1 | Weaker evaluation scope, similar weaknesses (no error bars), but our paper is stronger empirically |
| Why are Modern GANs Poor Density Models? (nJsfYo3HDy) | 3.80 | Round 1 | Similar critical/analytical framing; our paper has broader evaluation but the GAN paper has stronger theoretical grounding |
| Autoencoders for AD are Unreliable (X8XQOLjLX6) | 4.50 | Round 1 | Similar framing (testing whether a method's failure assumption holds); comparable quality but our paper has broader scope |
| Explaining OOD Detection Paradox through Likelihood Peaks (jQ596tXT3k) | 5.67 | Round 1 | Stronger execution on a related topic; our paper is weaker in narrative clarity and operationalization |
| Anomaly Detection by Estimating Gradients (7QDIFrtAsB) | 5.75 | Round 1 | Broader evaluation (49 baselines), stronger method contribution; our paper is somewhat weaker |

**Round 1 bracket:** [3.5, 5.5]  
**Final score determination:** The paper has genuine empirical value (comprehensive benchmarking, interesting ID analysis) but the central definitional framework is not properly applied, several methodological details are missing (no variance, unusual hyperparameter selection), and a significant counterexample (DAGMM) is not discussed. Calibrating against the anchors, the paper sits between the ~3.8–4.5 range of critical empirical studies and below the ~5.7 range of well-executed phenomenon-explanatory papers. Score 4.0.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>