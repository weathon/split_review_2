Now let me compose the final review, incorporating the favorability signals.

## Summary

This paper investigates whether the well-known counterintuitive phenomenon of likelihood-based anomaly detection failure — documented in the image domain — extends to tabular data. The authors propose a domain-agnostic definition of the counterintuitive phenomenon (Definition 3.3), conduct a comprehensive benchmark on all 47 tabular and 10 embedding datasets from ADBench against 12 baselines, and provide theoretical and empirical analysis linking the phenomenon's rarity in tabular data to lower dimensionality and weaker feature correlation. The core empirical finding is that a simple likelihood test using NICE normalizing flows (NF-SLT) substantially outperforms all baselines (AUROC 0.8575, Avg. Rank 3.43, Fail Ratio 0.02).

## Strengths

- **Comprehensive, unbiased benchmark evaluation** using all 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench without selection bias (responding to Shwartz-Ziv & Armon 2022), benchmarked against 12 baselines (6 shallow + 6 deep). This addresses a well-known source of inflated claims in the tabular AD literature. (Evidence: lines 83, 39-41, Table 1)

- **Striking empirical result:** NF-SLT achieves AUROC 0.8575, Avg. Rank 3.43, Top2 Ratio 0.45, Fail Ratio 0.02 — substantially outperforming every shallow and deep baseline. For a method as simple as training a normalizing flow on normal data and thresholding on likelihood, this is a genuinely surprising finding given the vigorous literature documenting that the same approach fails on raw image pixels. (Evidence: Table 1)

- **Clean dimensionality experiments (Tables 2 and 3)** provide causal evidence: reducing image dimensionality via ICA or bilinear interpolation systematically improves AUROC, directly supporting the dimensional explanation for the contrast between image and tabular domains. (Evidence: lines 148-176, Tables 2-3)

- **Feature correlation analysis via intrinsic dimension (Section 5.2, Figure 1, Table 4)** is a creative approach that quantifies how feature correlation reduces effective dimensionality, connects this to AD performance, and shows convergent evidence that NF-SLT fails on low-d-Ratio datasets even within the tabular domain. (Evidence: lines 190-234, Figure 1, Table 4)

## Weaknesses

### Major

- **Definition 3.3 is underspecified and never systematically applied.** The definition introduces free parameters β (proportion threshold) and γ (minimum performance gap), but these values are never stated in the main paper. The paper's central claim — that the counterintuitive phenomenon is "consistently rare" — rests on this definition, yet it is never operationalized with concrete thresholds and systematically checked against each dataset. The "Fail Ratio" (rank ≥ 9, line 89) and the two anecdotal examples (yeast gap=0.02, imdb gap~0.0385, lines 124-128) are not equivalent to checking conditions (2) and (3) with stated β and γ. This creates an evidential gap between the definitional apparatus and the empirical evaluation. (Evidence: lines 71-77 for Definition 3.3; line 89 for Fail Ratio definition; lines 124-128 for anecdotal examples)

- **Theoretical analysis assumes independence that contradicts the paper's own correlation analysis.** Theorem 5.4 explicitly assumes P and Q are products of independent distributions (line 142: "Let P = ∏ p_i(x_i) and Q = ∏ q_i(x_i) be independent d-dimensional continuous probability density models") — this is critical to the proof that the likelihood gap scales linearly with d. Yet Section 5.2 is entirely about measuring feature correlation, which is the negation of independence. The paper does not acknowledge or address this tension: the theorem's conclusion holds under the very assumption that real tabular data violates, and the paper's own analysis demonstrates this violation. Corollary 5.6 further assumes moment scaling behavior O(d^k) for k<n without justification for any real distribution. (Evidence: line 142; lines 190-234 for correlation analysis)

### Minor

- **No confidence intervals or variance reported** despite 10 repeated experiments (line 122). Only mean AUROC is reported in Table 1, making it impossible to assess whether observed performance gaps between NF-SLT and the second-best baselines are statistically significant.

- **Definition 3.3 is benchmark-dependent:** whether the phenomenon is "detected" depends on which specific models are included in the comparison set. The paper acknowledges the framing shift from the original likelihood-inversion definition (lines 25-27) but does not discuss how the choice of 12 specific baselines affects the conclusions. A different baseline set could change which datasets are classified as exhibiting the phenomenon.

- **Controlled cross-domain experiment is absent.** The image-side evidence comes from prior work (Glow on CIFAR-10/SVHN from Morningstar et al. 2021, AUROC 6.4%) while tabular results use NICE on ADBench — different architectures, training protocols, and datasets. The embedding results (Table 1 bottom) showing NF-SLT works well on image embeddings complicate the domain-based narrative; the paper's ID-based explanation (line 234) is plausible but post-hoc.

- **Table 4 ID comparison uses different estimation sources:** image IDs are cited from Pope et al. (2021) while tabular IDs are computed by the authors (line 202). Any systematic differences in estimation methodology could confound the comparison. Additionally, the bottom half of Table 4 is computed on only the 25 datasets where NF-SLT rank ≥ 3 — a selected subset.

### Trivial

- **Table 3 results conflict with the paper's own theorems.** The paper acknowledges this directly (line 176: "a result that conflicts with the theorems in Appendix D"). While the post-hoc explanation (interpolation strengthens correlations, reducing entropy) is plausible, the theoretical framework does not cleanly accommodate these empirical findings.

## Nice-to-Haves

- Operationalize Definition 3.3 by stating β and γ with justification and systematically reporting which datasets satisfy conditions (2) and (3). This would directly support the paper's headline claim.
- Add a controlled cross-domain experiment using the same flow architecture on matched-dimensionality data from both domains.
- Expand the ID comparison to systematically cover all ADBench tabular datasets with consistent estimation methodology.
- Report standard deviations or use statistical tests for the 10-repeat experiments.
- Clarify whether the global hyperparameter selection (one setting across all datasets) used validation splits or test data.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **"Hyperparameter selection inflates results"** — REMOVED: The paper selects ONE global hyperparameter setting (the combination with highest average AUROC across all datasets). This avoids per-dataset overfitting and is a standard approach for demonstrating general applicability. The mild concern about using test data for selection does not rise to the level of a significant weakness.
2. **"Embedding results undermine domain-based narrative"** — REMOVED: The paper directly addresses this via ID estimation of embeddings (line 234), showing they have larger d Ratio than raw pixels, consistent with the paper's framework.
3. **"Facts 1.1 and 1.2 have clear exceptions"** — REMOVED: The paper explicitly acknowledges genomics counterexamples (line 35) and brackets them as atypical.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. The single highest-leverage improvement is to operationalize Definition 3.3: specify β and γ with justification, and systematically apply it to all 57 datasets. Currently the definition does no work that the aggregate metrics (Avg. Rank, Fail Ratio) don't already do.
2. Explicitly acknowledge and discuss the tension between Theorem 5.4's independence assumption and Section 5.2's correlation analysis. Either relax the assumptions or frame the theory as purely illustrative.
3. Add confidence intervals or standard deviations to Table 1 to allow readers to assess the reliability of performance gaps.
4. Consider whether the elaborate definitional apparatus is necessary. The paper's empirical finding — that likelihood-based AD with normalizing flows works well on tabular data, contrary to the image-domain literature — is interesting on its own merits and could be presented without the problematic Definition 3.3 framing.

## Score and Decision

The paper's core empirical contribution is strong: a comprehensive, unbiased benchmark showing that a simple likelihood test with normalizing flows substantially outperforms 12 baselines on tabular AD. The dimensionality and correlation analyses provide convergent evidence for why. However, the paper's central framing rests on Definition 3.3, which is underspecified (β/γ never stated, never systematically applied) and its theoretical analysis makes an independence assumption that directly contradicts the correlation analysis in the same paper. The empirical result is real and valuable, but the definitional and theoretical scaffolding needs significant revision. Borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>