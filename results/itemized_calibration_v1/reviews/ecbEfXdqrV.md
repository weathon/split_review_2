Now let me produce the final consolidated review.

## Summary

The paper investigates whether the "counterintuitive phenomenon" (generative models assigning higher likelihood to out-of-distribution data than in-distribution data) that is well-documented in image domains also occurs in tabular anomaly detection. The authors propose a formal definition of this phenomenon (Definition 3.3) based on relative performance against baselines, then conduct extensive experiments on all 47 tabular and 10 CV/NLP embedding datasets from ADBench with 12 baselines. Their method, NF-SLT (normalizing flow with simple likelihood test), achieves mean AUROC 0.8575 with average rank 3.43 and fail ratio 0.02, substantially outperforming all baselines (next best ICL: 0.8208, rank 5.17). The paper provides theoretical analysis (linking the phenomenon to dimensionality via Theorem 5.4) and empirical analysis (using intrinsic-dimension ratio as a proxy for feature correlation) to explain why the phenomenon is rare in tabular data.

## Strengths

- **Comprehensive, selection-bias-free evaluation.** The paper uses all 47 tabular datasets and all 10 CV/NLP embedding datasets from ADBench without exclusion, explicitly motivated by Shwartz-Ziv & Armon (2022). This raises the bar for empirical claims about tabular anomaly detection and directly addresses a well-known reproducibility concern in the field.

- **Strong, consistent empirical results.** NF-SLT achieves mean AUROC 0.8575 (avg rank 3.43, top-2 ratio 0.45, fail ratio 0.02) vs. next best ICL at 0.8208 (rank 5.17, top-2 0.32, fail 0.23). The fail ratio of 0.02 (ranked 9th or lower on only 1/47 datasets) means that on 46 out of 47 datasets NF-SLT is among the top-8 methods — a very strong signal that the generative model is not systematically failing in tabular data.

- **Clever and well-motivated use of intrinsic dimension.** The d Ratio (intrinsic dimension / ambient dimension) as a proxy for overall feature correlation is elegant. The toy Gaussian experiment (Figure 1, left/center) cleanly validates the relationship between correlation strength and dimension reduction, and the comparison of tabular vs. image datasets (Figure 1, right) provides a visually compelling argument: image d_Ratio ≈ 0.001–0.02, tabular d_Ratio ≈ 0.4–0.8.

- **Multi-faceted explanation.** The paper provides both theoretical (Theorem 5.4, Corollary 5.6) and empirical (ICA dimensionality reduction, ID analysis) analyses linking the phenomenon's rarity to dimensionality and feature correlation, offering a more complete picture than prior work.

## Weaknesses

### Fatal
None.

### Major

1. **β and γ thresholds in Definition 3.3 are never specified.** The definition introduces two free parameters (β: fraction of baselines that must outperform the generative model; γ: minimum AUROC gap) but the paper never states what values are used. It applies the definition only qualitatively — e.g., "the minimum performance difference between MCM and AUROC is 0.02; hence, we cannot assume counterintuitive phenomenon" — without specifying what γ threshold makes this determination rigorous. Without concrete β and γ values, the definition is a framework rather than an operational definition, and the paper's central claim that the phenomenon "is consistently rare" cannot be directly verified.

2. **Definition 3.3 is never systematically applied to all 47 datasets.** The paper's main empirical claim about the phenomenon's rarity relies on indirect evidence (NF-SLT's low fail ratio, high average rank). But condition (2) of Definition 3.3 requires that *most* baselines outperform the generative model — a much stronger condition than "not in the bottom quartile." The paper discusses only two datasets (yeast, imdb) qualitatively and never provides a per-dataset accounting with explicit thresholds. The abstract's claim that the phenomenon "occurs far less often" remains an assertion without direct evidence using the paper's own definition.

### Minor

3. **Theorem 5.4 assumes independent features, which does not cover the paper's own argument.** The theorem assumes fully independent distributions (P = ∏ p_i, Q = ∏ q_i), but the paper's argument (Fact 1.2, Section 5.2) is that tabular data has *weaker* correlations than images, not *zero* correlations. The theorem does not cover the intermediate regime of weak-but-nonzero correlation that actually characterizes tabular data. The paper acknowledges this indirectly (the image-resize experiments in Table 3 produce results that "conflict with the theorems" due to violated independence) but does not resolve the gap between the theory's assumptions and the intended application.

4. **Relationship between Definition 3.3 and the original likelihood-inversion definition is insufficiently discussed.** The original "counterintuitive phenomenon" (Nalisnick et al., 2019a) refers to likelihood inversion: a generative model assigning higher likelihood to OOD data than in-distribution data. Definition 3.3 replaces this with a *relative* property (underperformance vs. baselines). While the paper provides some motivation, it does not systematically discuss boundary cases where the two definitions diverge — e.g., a generative model with AUROC=0.55 where all baselines also score ~0.55 would show likelihood inversion under the original definition but would not qualify under Definition 3.3 (since condition (2) is not met). This ambiguity affects how readers should interpret the paper's headline claim.

5. **d Ratio comparison uses only 4 image datasets.** The comparison in Table 4 and Figure 1 (right) relies on MNIST, CIFAR-10, CIFAR-100, and SVHN — a thin sample for drawing domain-level conclusions about feature correlation differences. The 47 tabular datasets are compared against these 4 image datasets.

6. **Hyperparameter selection procedure for baselines is ambiguous.** The paper states "the hyperparameter combination with the highest average AUROC for all datasets is selected" but does not clearly state whether this procedure (global-average tuning) was applied to all 12 baselines or only to NF-SLT. If baselines received per-dataset tuning instead, the comparison may not be fair.

### Trivial
- Theorem 5.4 references "same conditions as Lemma 5.1" which is relegated to the appendix, making the main text not self-contained.

## Nice-to-Haves
- Provide a table comparing the two definitions (likelihood-inversion vs. Definition 3.3) on the 47 datasets to clarify where they agree and diverge.
- Report per-dataset AUROC results for all 47 tabular datasets (currently only aggregate statistics are in the main text).
- Include standard deviations or confidence intervals from the 10 repeated experiments for close comparisons.
- Extend the d Ratio analysis to more image datasets and check whether baselines also degrade on low-d-Ratio tabular datasets.

## Removed Points
- **"Abstract states finding before experiments"** — This is a presentational framing issue, not a substantive weakness. The abstract uses standard academic language ("we demonstrate that...").
- **"Split protocol differs from ADBench default"** — The paper clearly states its protocol (Zong et al., 2018). This is a methodological choice, not an omission.
- **"CIFAR-10/SVHN example (6.4%) should discuss whether definition is equally meaningful near 0.5"** — An interesting observation but speculative; the paper's definition applies consistently regardless of absolute AUROC value.

## Novel Insights

The d Ratio analysis provides a crisp, visually compelling way to compare the feature-correlation structure of tabular vs. image data that goes beyond earlier qualitative arguments. The finding that image d_Ratio is ~0.001–0.02 while tabular d_Ratio is ~0.4–0.8 offers a concrete, measurable explanation for why the likelihood-inversion problem is domain-dependent. This is a genuine step forward from prior work that relied on vague appeals to "data complexity" or "pixel correlations." Combined with the comprehensive 47-dataset evaluation, the paper convincingly demonstrates that normalizing-flow likelihood tests are practically reliable for tabular anomaly detection — a non-obvious result given the image-domain literature.

## Suggestions

1. **Specify β and γ values** in Definition 3.3 with justification (e.g., β=0.5 meaning a majority of baselines must outperform, γ=0.05 as a minimum meaningful AUROC gap).
2. **Systematically apply Definition 3.3** to all 47 datasets with the specified thresholds and report the count of datasets where the phenomenon occurs.
3. **Clarify the hyperparameter selection** procedure for all 12 baseline models — whether each received the same global-average tuning or per-dataset tuning.
4. **Discuss the relationship** between Definition 3.3 and the original likelihood-inversion definition explicitly, including boundary cases.

## Score and Decision

**Calibration analysis.** Round 1 bracketing retrieved 15 anchors across score bands. For each band the most relevant anchors are:

| Anchor path | Avg score | Band | Itemized? | Comparison to this paper |
|---|---|---|---|---|
| jQ596tXT3k.md (OOD Paradox via Likelihood Peaks) | 5.67 | 5.5–7.5 | Yes | Similar topic (OOD detection paradox); had more severe technical flaws (Taylor approximation rigor, hyperparameter sensitivity) |
| 7VkHffT5X2.md (AnoLLM) | 6.75 | 5.5–7.5 | Yes | Tabular AD; accepted with minor weaknesses (missing baselines, computational cost). Our paper has more substantial definitional issues |
| Vi6p2TeujL.md (PTAD) | 4.25 | 3.5–5.5 | Yes | Tabular AD; rejected with major reproducibility issues (3 seeds, incomplete hyperparams). Our empirical evaluation is substantially stronger |
| 3a505tMjGE.md (AVOID) | 6.00 | 5.5–7.5 | Yes | VAE OOD detection with theoretical analysis. Similar hyperparameter-sensitivity issue (weight -3) to our β/γ issue |
| rCaA79Obsj.md (Time series AD evaluation) | 5.20 | 3.5–5.5 | Yes | Similar in critiquing standard practices; had weaker benchmark performance and missing baselines |
| cJs4oE4m9Q.md (Hypersphere AD) | 8.00 | 7.5–8.5 | No | Higher-tier AD paper with cleaner theoretical contribution |

**Initial bracket** (Round 1): Narrowest plausible range is 4.5–6.5 based on the comparison. The paper is clearly stronger than PTAD (4.25) and the time-series AD paper (5.20) due to its comprehensive evaluation and strong results. It is comparable to AVOID (6.00) and the likelihood paradox paper (5.67). It is weaker than AnoLLM (6.75, accepted) because AnoLLM's weaknesses were minor while this paper has two unresolved major issues.

**Narrowing from itemized comparison:** The two major weaknesses (β/γ unspecified, definition never systematically applied) are genuine gaps that prevent verification of the paper's central claim, similar in severity to AVOID's hyperparameter sensitivity issue (weight -3). However, the paper's empirical evaluation (47 datasets, 12 baselines, strong consistent results) is a genuine strength that weighs positively (comparable to weight +4). The AVOID anchor (6.00) was rejected despite having only one major weakness of similar severity to each of ours — suggesting two such issues should push the score below 6.

**Final score: 5.5** — between borderline reject and borderline accept.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>