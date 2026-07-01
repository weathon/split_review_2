Now I have a clear picture from calibration. Let me write the final review.

## Summary

This paper investigates why the "likelihood inversion" phenomenon (where generative models assign higher likelihoods to anomalous/out-of-distribution data than to in-distribution data), which is well-documented in the image domain, rarely occurs in tabular anomaly detection. The paper contributes: (1) a domain-agnostic definition of the counterintuitive phenomenon (Definition 3.3); (2) extensive experiments on all 47 ADBench tabular datasets and 10 CV/NLP embedding datasets showing that NF-SLT (Normalizing Flow with Simple Likelihood Test) achieves strong performance; and (3) theoretical and empirical analyses explaining the phenomenon's rarity through dimensionality (Theorem 5.4, Corollary 5.6) and feature correlation (intrinsic dimension / d-Ratio analysis).

## Strengths

1. **Comprehensive evaluation across ADBench's full suite.** The paper evaluates on all 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench against 12 baseline models (6 shallow, 6 deep). This avoids selection bias (explicitly motivated by Shwartz-Ziv & Armon, 2022) and makes the empirical findings substantially more credible. (Section 4, lines 83-84, Table 1)

2. **The domain-agnostic definition (Definition 3.3) is conceptually sensible.** Rather than declaring any AUROC < 0.5 as "counterintuitive," the definition requires both (a) that most comparison models outperform the generative model (Eq. 2), and (b) that the performance gap is nontrivial (Eq. 3). This avoids conflating "dataset is hard" with "likelihood is actively misleading." (Section 3, lines 71-77)

3. **The dimensionality experiment (Table 2) cleanly isolates the effect of dimension.** By applying ICA to images and retaining varying numbers of independent components, the authors show that when H(P) > H(Q), AUROC increases as dimension decreases, even down to ~1% of original dimension. This provides direct causal evidence for the dimension hypothesis. (Section 5.1, Table 2, lines 148-162)

4. **The intrinsic dimension analysis (Table 4, Figure 1) is a clever operationalization of "feature correlation."** Using the d-ratio (ID/ambient dimension) to quantify global correlation is elegant, and the comparison between image datasets (~1% d-ratio) and tabular datasets (often >40% d-ratio) is striking. The finding that NF-SLT underperforms on the low-d-ratio tabular datasets (Table 4 bottom) provides convergent evidence. (Section 5.2, lines 190-232, Table 4, Figure 1)

## Weaknesses

### Fatal
None.

### Major

1. **Definition 3.3 is never operationalized with concrete thresholds.** The definition depends on two free parameters: β (proportion of comparison models that must outperform the generative model) and γ (minimum AUROC gap). The paper never states what values of β and γ are used, and never systematically applies the definition with specified numerical thresholds to any dataset. The argument in Section 4 instead uses qualitative judgments (e.g., a gap of 0.02 on 'yeast' is described as "small" without reference to a stated γ threshold). The paper's central empirical claim — "the phenomenon, as defined, is consistently rare" — cannot be fully verified without knowing the thresholds used. The definition is presented as a key contribution but remains a framing device rather than an operational tool. Setting and justifying explicit β, γ values and checking conditions per dataset would directly address this. (Section 3, lines 71-77; Section 4, lines 124-126)

### Minor

2. **Hyperparameter selection protocol is non-standard.** The paper selects a single hyperparameter configuration by maximizing average AUROC across all 47 datasets simultaneously, rather than performing per-dataset tuning. While the same procedure is applied to all models (internal fairness), it deviates from ADBench's standard per-dataset protocol. NF-SLT, as a relatively simple model (10-layer NICE flow, 200 epochs), may be more robust to this "one-size-fits-all" selection than more complex deep baselines that could benefit more from per-dataset tuning. Without per-dataset results, it is unclear whether NF-SLT's reported advantage (0.8575 AUROC vs. ICL's 0.8208) is robust to tuning protocol. (Section 4, lines 122-123)

3. **No measures of variability reported.** The paper reports averages over 10 repeated experiments but provides no standard deviations, confidence intervals, or significance tests for any of the metrics in Table 1. Reporting variance is straightforward given the repeated trials and would substantially strengthen confidence in NF-SLT's reported superiority. (Table 1, line 122)

4. **Claims about "tabular data" are broader than the evidence base.** The paper's title and abstract refer to "tabular anomaly detection" and "general tabular data," but the empirical evidence is drawn exclusively from ADBench datasets. The paper briefly acknowledges that high-dimensional tabular data with strong correlations (e.g., genomics) exists, but the scope should be more precisely bounded in the claims. (Abstract, line 9; Section 1, line 35)

### Trivial

5. **Theory-empirics assumption gap.** Theorem 5.4 assumes P and Q are product distributions with independent components, yet Section 5.2's central contribution is quantifying feature correlation (which by definition means features are not independent). The paper explicitly acknowledges this gap (lines 164-165), so this is not a flaw per se, but the logical tension between the independence-based theory and the correlation-based empirics could be more clearly reconciled. (Section 5.1, line 142; Section 5.2)

## Nice-to-Haves
- Per-dataset hyperparameter tuning results to verify that NF-SLT's advantage is robust to tuning protocol.
- Standard deviations or confidence intervals for Table 1's metrics.
- An explicit application of Definition 3.3 with stated β, γ values to each dataset (even as a supplementary table).
- Controlled experiments that manipulate feature correlation while holding other factors fixed to support the causal claim about heterogeneity.
- A clearer statement about which parts of the theoretical analysis rely on the independence assumption vs. applying more broadly.

## Removed Points

These points from the input review are removed with justification:

1. **"Definition depends on which comparators are chosen"** — The paper uses 12 diverse baselines covering shallow and deep methods. This is a general limitation of any relative definition; the paper's choice is reasonable. Removed as too generic/speculative.

2. **"CV/NLP embedding results undercut the tabular narrative"** — The paper explicitly addresses this (lines 234-235) by showing that embeddings have higher intrinsic dimensionality than raw pixels, which is consistent with the paper's framework. Removed because the paper already handles this concern.

3. **"Low-dimensional image experiments are treated as conflicting rather than supporting"** — The paper discusses these results thoughtfully, noting both the cases consistent with and those conflicting with the theory. Removed because the paper does not mishandle these results; it acknowledges the conflict and offers an explanation.

4. **"Independence assumption is incompatible with the paper's own narrative"** — The paper explicitly acknowledges the assumption and notes where the theorem cannot be applied (line 164-165). The theory is a simplified model, which is standard in theoretical work. Removed as the paper already addresses this limitation.

5. **"Theoretical analysis is disconnected from evidence"** — While the theory uses independence assumptions, the paper is transparent about this, and the key empirical contributions (dimensionality experiments, d-Ratio analysis) stand on their own. Removed as over-stated.

## Novel Insights

None beyond the paper's own contributions. The input review did not surface a novel perspective not already present in the paper.

## Suggestions

- Set explicit values for β and γ (e.g., β = 0.5, γ = 0.05) and systematically apply Definition 3.3 to all 47 datasets. Report how many datasets exhibit the counterintuitive phenomenon per the definition. This would turn the definition from a framing device into a genuine analytical tool and directly test the paper's headline claim.
- Report per-dataset optimal hyperparameters, or at minimum run a sensitivity analysis showing that the reported results are not artifacts of the "one config fits all" protocol.
- Add standard deviations or confidence intervals to Table 1.
- Scope the title/abstract claims more precisely (e.g., "tabular anomaly detection benchmarks" rather than "tabular anomaly detection").
- Reconcile the independence assumption in Theorem 5.4 with the correlation analysis in Section 5.2, or be more explicit about the theory being a simplified bound.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>