Now I have verified all key claims. Let me write the final review.

## Summary

This paper investigates whether the likelihood inversion pathology documented for normalizing flows in the image domain (where anomalous/OOD data receives higher likelihoods than normal data) also manifests in tabular anomaly detection. The paper: (1) proposes a domain-agnostic definition of this "counterintuitive phenomenon" based on relative AUROC against other detection models, (2) evaluates NF-SLT (NICE normalizing flow with a simple likelihood test) on all 47 ADBench tabular datasets plus 10 CV/NLP embedding datasets against 12 baselines, (3) provides a theoretical extension linking dimensionality to the likelihood gap, and (4) uses intrinsic dimension (d-Ratio) analysis to explain why tabular data is less affected than images. The core empirical finding is that NF-SLT achieves the highest average AUROC (0.8575) and Top2 Ratio (0.45), with the lowest Fail Ratio (0.02) among all methods tested.

## Strengths

- **Comprehensive benchmark coverage without selection bias.** The paper uses all 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench (Section 4), a meaningful improvement over prior work (Kirichenko et al., 2020) which examined only two tabular dataset pairs. The decision to include the full benchmark, motivated by Shwartz-Ziv & Armon (2022)'s criticism of selection bias, strengthens the generality of the empirical claims.

- **Intrinsic dimension analysis (Section 5.2, Figure 1, Table 4).** The connection between feature correlation (quantified via the d-Ratio of intrinsic to ambient dimension) and NF-SLT's relative ranking is the paper's most compelling evidence. Table 4's bottom panel — showing that 100% of datasets where NF-SLT ranks ≥3 have d-Ratio < 0.8, with this fraction dropping monotonically as the threshold tightens — provides a clear necessary-condition argument: low d-Ratio is strongly associated with cases where NF-SLT is not top-ranked. The synthetic Gaussian experiment (Figure 1, left/center) cleanly establishes the relationship between correlation strength and ID reduction.

- **Theoretical framing of the dimensionality effect (Equation 4, Theorem 5.4).** Extending Caterini & Loaiza-Ganem (2022)'s likelihood-gap expression to analyze the role of dimensionality is a sensible direction. The core idea — that the entropy-difference term in the likelihood gap can be magnified by high dimension, making the gap more negative — is sound and worth stating formally.

## Weaknesses

### Major

- **Definition–conclusion mismatch: the phenomenon being tested does not match what the title promises.** The paper's title asks why the "counterintuitive phenomenon of likelihood" (i.e., likelihood inversion, as documented by the CIFAR-10/SVHN case where Glow achieves AUROC 6.4%) is rare in tabular data. However, Definition 3.3 operationalizes the phenomenon not as likelihood inversion per se, but as the generative model's AUROC being substantially *lower than comparison models* (via thresholds β and γ, Equations 2–3). This means the paper primarily answers "does NF-SLT underperform relative to alternatives on tabular data?" rather than "do tabular normalizing flows exhibit the same likelihood inversion pathology as image flows?" The `imdb` case illustrates the problem: NF-SLT achieves AUROC 0.5013 (random-level), yet the paper dismisses it because the gap to the best model is only 0.04 (line 124: "the difference in performance with the comparison model is very small"). Whether likelihood inversion occurred on `imdb` — which is the question the title asks — is left unanswered. The paper's empirical finding (NF-SLT is competitive on tabular AD) is genuinely interesting but would be better framed on its own terms rather than as an answer to a different question about likelihood inversion.

- **Hyperparameter selection protocol deviates from standard practice and complicates interpretation.** The paper states (line 122): "the hyperparameter combination with the highest average AUROC for all datasets is selected as the representative hyperparameter combination." This means a single configuration is chosen to maximize aggregate performance across all 47 datasets simultaneously, using test-set performance to guide the choice. This departs from the ADBench protocol (Han et al., 2022), which uses per-dataset validation-based tuning. The approach creates two concerns: (a) test-set information from all datasets informs the hyperparameter choice (a form of information leakage across the benchmark), and (b) methods with higher per-dataset sensitivity (e.g., DAGMM, DeepSVDD) may be systematically disadvantaged relative to methods with robust default behavior. Without per-dataset tuning or an ablation showing ranking stability across reasonable hyperparameter choices, the aggregate comparison is harder to interpret than it would be under standard practice.

- **Theoretical analysis rests on an independence assumption that is violated by all real data.** Theorem 5.4 assumes P = ∏ p_i(x_i) and Q = ∏ q_i(x_i) — product distributions with independent dimensions. This assumption is false for both images (strong pixel correlations) and tabular data (the paper's own ID analysis shows d-Ratios well below 1.0, e.g., magicgamma = 0.70, satellite = 0.42, indicating substantial correlation structure). The theorem shows that a *lower bound* of the likelihood gap becomes more negative linearly with d under independence, but a looser lower bound does not imply the actual gap shrinks, nor does it imply AUROC decreases. The paper acknowledges the limitation in the context of Table 3 (line 164: "independence between pixels is not guaranteed"), but still uses the theorem to support central claims about why the phenomenon is rare in tabular data. Corollary 5.6 adds further assumptions about central moment scaling (𝒪(d^k) for k < n) that are not verified on any real dataset. The theoretical framework is best treated as a suggestive toy model rather than a proof that carries the paper's argument.

### Minor

- **Thresholds β and γ are not given in the main text.** Definition 3.3 (the paper's core conceptual contribution) requires two thresholds — β (Equation 2) and γ (Equation 3) — whose values determine whether any given result constitutes the phenomenon. The main text states these are defined in Appendix B (line 77) but does not report them, making it impossible for a reader to evaluate the central claim from the information presented. (This is a presentation issue; the appendix — stripped by the parser — likely contains the values, but they belong in the main text given that the entire empirical conclusion depends on them.)

- **Table 2 does not fully support the claimed monotonic trend.** The paper states (line 162): "when H(P) > H(Q) holds, the AUROC increases as the dimensionality decreases." In the CIFAR-10/SVHN row, however, AUROC goes 0.3311 (1024 dims) → 0.2924 (512) → 0.2984 (256) → 0.3143 (30). The AUROC at 30 dimensions (0.3143) is *lower* than at 1024 (0.3311), and the trend is non-monotonic. The claim holds on average across rows but the individual counterexample warrants discussion.

- **The `imdb` failure case is not analyzed.** NF-SLT achieves AUROC 0.5013 (essentially random) on `imdb`. The paper notes this but only to argue it does not satisfy Definition 3.3 (gap is small). Whether this case exhibits actual likelihood inversion (which would be directly relevant to the title's question) or stems from poor density estimation is not investigated. A brief analysis would strengthen the paper.

- **No direct measure of likelihood inversion is reported.** The paper never computes a direct metric of whether anomalous test points have higher likelihoods than normal points (e.g., the fraction of anomalies with likelihood exceeding the median normal likelihood). Such a metric would directly connect to the original research question and would not depend on the relative-performance thresholds β and γ.

### Trivial

None.

## Nice-to-Haves

- Report per-dataset AUROC results for all 47 datasets (e.g., a histogram or table) beyond the aggregate statistics in Table 1.
- Provide sensitivity analysis of the conclusion to the choice of β and γ, showing over what range the "rare" claim holds.
- Run NF-SLT (NICE) on raw image data (CIFAR-10 vs SVHN) to provide a direct apples-to-apples comparison of the same architecture in both domains, rather than relying on prior work's Glow results for the image baseline.

## Removed Points

- *"The definition is circular"* — Downgraded from the harsh critic's framing. Definition 3.3 is not logically circular (the paper defines the phenomenon in terms of relative performance, then tests that definition). The real issue is construct validity — the definition may not capture the phenomenon the title references. This is captured in the Major weakness above.
- *"Bilinear interpolation experiments conflict with theory"* — The authors explicitly acknowledge this conflict (line 176: "a result that conflicts with the theorems") and offer a post-hoc explanation. This transparency is good practice; the limitation is already surfaced.
- *"Several deep baselines perform very poorly"* — This is not a weakness of the paper; it is an empirical finding. The paper does not control which baselines perform well.
- *"No comparison with image-domain results under equivalent methodology"* — Scope is tabular AD; this is a nice-to-have.
- *"ADBench data split sensitivity"* — The paper follows a published protocol (Zong et al., 2018), which is a reasonable methodological choice.
- All formatting, grammar, and typographical nitpicks — these are parser artifacts, not author errors.
- All complaints about missing appendix content, proofs, or references — the parser strips these sections; they exist in the original submission.

## Novel Insights

The reviewer's analysis surfaces a genuine tension between the paper's title/framing (about likelihood inversion) and its operational definition (based on relative AUROC performance). This is a useful observation about construct validity that goes beyond what the paper itself discusses. A second insight is that the d-Ratio analysis, while associational, provides a *necessary-condition* argument (low d-Ratio → NF-SLT does not rank highly) but not a *sufficient-condition* argument; this distinction sharpens the interpretation of the paper's strongest evidence.

## Suggestions

1. **Reframe the contribution.** The paper's strongest finding is that NF-SLT is competitive on tabular AD (average AUROC 0.8575, Top2 Ratio 0.45). This is interesting and publishable on its own terms. A reframing around "likelihood-based detection works well on tabular data, and here is why" would be more accurate than "the counterintuitive phenomenon is rare."

2. **Report β and γ values in the main text** with justification anchored to the known image-domain case (e.g., "β = X and γ = Y would classify CIFAR-10/SVHN as counterintuitive; we set these thresholds and find no tabular dataset meets them").

3. **Add a direct likelihood inversion metric** (e.g., the fraction of anomalies with above-median normal likelihood) to bridge the gap between the definition and the original research question.

4. **Use per-dataset hyperparameter tuning** following ADBench's standard protocol, or provide an ablation showing that the ranking is stable under alternative tuning schemes.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| jQ596tXT3k (Explaining OOD Paradox) | 5.67 | R1, R2 | Stronger theory, similar topical focus; rejected |
| hlijRgXTDK (Pathologies of OOD) | 4.75 | R2 | Weaker empirical evidence; conceptual contribution |
| LjygLD0AkT (Rethinking Test-time Likelihood) | 5.00 | R2 | Comparable quality; rejected |
| 6Z8rZlKpNT (Normalizing Flows for OOD) | 3.40 | R1 | Weaker on all dimensions |
| Vi6p2TeujL (PTAD) | 4.25 | R1 | Comparable topic, different contribution type |
| 7QDIFrtAsB (Gradient-based Tabular AD) | 5.75 | R1 | Comparable scope; rejected |
| SabhfFUfA1 (VAEs for OOD) | 4.67 | R1 | Similar analysis paper |
| lNZJyEDxy4 (MCM) | 6.67 | R1 | New method paper; accepted |
| 7VkHffT5X2 (AnoLLM) | 6.75 | R1 | New method paper; accepted |

**Round 1 bracket:** 4.5–5.5. **Round 2 narrowing:** 5.0 (midpoint of the bracket, reflecting that the paper has substantial empirical strengths but framing and methodological issues prevent acceptance).

The paper's empirical scope (all 47 ADBench datasets, 12 baselines) and ID analysis are genuine contributions, and the finding that NF-SLT is competitive on tabular AD is non-trivial. However, the definition–conclusion mismatch means the paper does not convincingly answer the question posed in its title, and the hyperparameter protocol introduces interpretation difficulties. These are not fatal flaws but they prevent the paper from achieving the clarity and rigor needed for acceptance. The paper is borderline but leans toward rejection in its current form.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>