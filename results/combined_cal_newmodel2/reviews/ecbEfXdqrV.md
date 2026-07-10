Now I have all the information needed. Let me compile the final review.

## Summary

This paper investigates whether the "counterintuitive phenomenon" (generative models assigning higher likelihood to OOD data than in-distribution data) occurs in tabular anomaly detection, as it does in images. The authors propose a domain-agnostic definition of this phenomenon, then conduct extensive experiments on all 47 tabular and 10 CV/NLP embedding datasets from ADBench, showing that a simple likelihood test with normalizing flows (NF-SLT) achieves strong performance (AUROC 0.8575, Top2 Ratio 0.45, Fail Ratio 0.02) against 12 baselines. They further provide theoretical and empirical analysis linking the absence of the phenomenon in tabular data to lower dimensionality and weaker feature correlation compared to images.

## Strengths

- **Comprehensive benchmark evaluation without selection bias.** The paper uses all 47 tabular and 10 CV/NLP embedding datasets from ADBench against 12 baselines. NF-SLT's average AUROC of 0.8575 with Top2 Ratio 0.45 and Fail Ratio 0.02 represents a genuinely striking result that is substantially better than any of the 12 baselines (Table 1).

- **The empirical finding is interesting and practically useful.** The observation that a simple likelihood test with normalizing flows works well across a large, diverse collection of tabular anomaly detection tasks is non-trivial and contrasts with the well-known failure mode in images. This has practical implications for practitioners selecting anomaly detection methods.

- **Intrinsic dimension analysis linking feature correlation to model performance.** The d-ratio analysis (ID/ambient dimension) provides a measurable quantity that differentiates image from tabular domains (Table 4, Figure 1). The synthetic-data demonstration that stronger correlation reduces ID is clean, and the observation that datasets where NF-SLT underperforms tend to have low d-ratio provides a nice sanity check.

- **Dimension-reduction experiments on images (Tables 2 and 3) are clever.** Showing that reducing image dimension via ICA or bilinear interpolation improves AUROC for cases where H(P) > H(Q) provides concrete empirical support for the dimensionality argument.

## Weaknesses

### Major

1. **Definition 3.3 redefines the phenomenon in terms of relative model performance, not likelihood inversion, and its thresholds are never specified in the paper body.** The original "counterintuitive phenomenon" (Nalisnick et al., 2019a) refers to a specific failure mechanism: generative models assigning *higher likelihood* to OOD data than to in-distribution data. Definition 3.3 replaces this with a relative-performance comparison (proportion of baselines outperforming the generative model exceeding β, and the minimum gap exceeding γ). These are different: a model could achieve AUROC well above 0.5 (no likelihood inversion) yet be outperformed by stronger baselines — Definition 3.3 would call this a "counterintuitive phenomenon" under sufficiently low β. Conversely, a model with AUROC near 0.5 (possible mild inversion) would not be flagged if all baselines also score near 0.5. The paper's title and abstract claim the original phenomenon is rare, but Definition 3.3 measures something else. Furthermore, **β and γ are never specified** — the paper only gestures at the analysis for two datasets (yeast, imdb) without stating what thresholds are used. The claim that "the fully rigorous formulation is in Appendix B" does not remedy this, as the body of the paper should be self-contained on this point.

2. **Because Definition 3.3 is defined relative to the choice of comparison models, the classification of "phenomenon occurs" depends on which baselines are selected.** A different or stronger set of baselines could change the classification even if NF-SLT's likelihood behavior is unchanged. This conflates two distinct questions: (Q1) does likelihood inversion occur? and (Q2) does NF-SLT outperform other methods? The paper shows that NF-SLT is *good* (Q2) and concludes the phenomenon is *rare* (Q1), but these are logically separate.

### Minor

3. **The paper never directly tests for likelihood inversion (AUROC < 0.5) on individual datasets**, which would be the simplest diagnostic of the original phenomenon. Only average AUROC across 47 datasets is reported in Table 1. Reporting per-dataset NF-SLT AUROC and counting how many fall below 0.5 would provide direct, definition-independent evidence. (The CV/NLP embedding table shows imdb at 0.5013 — essentially at-chance — but this is not discussed as a potential inversion case.)

4. **Theorem 5.4 assumes P and Q are product distributions (independent features).** This is a strong condition; real tabular data may not satisfy it. The paper does not discuss how robust the theoretical results are to violations of this assumption. The theorem's connection to real data is therefore unclear, especially since the image-domain phenomenon occurs precisely because of *dependence* between pixels.

5. **The CV/NLP embedding d-ratio analysis weakens the feature-correlation explanation.** Embeddings have d-ratio ~2% (ID 23-18 / ambient 1000), which is much closer to image d-ratios (0.3-1.9%) than to tabular d-ratios (39-81%). The paper claims this explains why embeddings work well, but the d-ratio is in fact far closer to the image regime, making the explanation less compelling.

6. **No per-dataset breakdown of NF-SLT AUROC for the 47 tabular datasets is provided** — only averages. This makes it impossible for readers to assess how many datasets have near-chance performance or to verify robustness beyond the aggregate.

7. **No confidence intervals or standard deviations are reported** for the AUROC comparisons despite 10 repeated experiments.

8. **Hyperparameter selection detail.** A single configuration is chosen by maximizing average AUROC across all datasets. The paper does not explicitly confirm that the same procedure was applied to all 12 baselines, which would be necessary for a fair comparison.

## Nice-to-Haves

- A computational cost comparison (training/inference time) between NF-SLT and the baselines would help practitioners assess the practical trade-off.
- Relaxing the independence assumption in Theorem 5.4, or providing separate analysis for the correlated-feature case, would strengthen the theory.
- Reporting confidence intervals and per-dataset results would improve reproducibility and trust.

## Removed Points

- **"Missing appendix for Definition 3.3":** REMOVED per rule that parser strips appendices from all papers.
- **"Related work not engaging with tabular OOD with flows beyond Kirichenko":** REMOVED per rule about not criticizing missing related works without external confirmation.
- **"Jump from Assumptions 3.1/3.2 to Definition 3.3 not justified":** REMOVED as a design-choice critique rather than a specific identified problem.
- **"Computational cost not discussed":** MOVED to Nice-to-Haves (not a core flaw).
- **"Statistical test for d-ratio table":** REMOVED as it demands a practice not standard for this kind of correlational analysis.
- **Generic "limitations acknowledgment" about baseline dependence:** MERGED into Major weakness 2.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe the paper around the direct evidence that NF-SLT works well for tabular anomaly detection and that likelihood inversion is rare (checkable via per-dataset AUROC against 0.5), rather than claiming the original phenomenon is rare via a redefined measure.
2. Report per-dataset AUROC for NF-SLT across all 47 datasets, ideally with a histogram.
3. Either specify concrete, justified values for β and γ in Definition 3.3 and directly apply it to every dataset, or remove the definition and use the direct likelihood-inversion diagnostic.
4. Add confidence intervals or standard deviations to the main results table.
5. Discuss the independence assumption of Theorem 5.4 and its implications for real tabular data.

## Score and Decision

**Round 1 bracket:** The paper's comprehensive experiments (favorability 12.95) and strong empirical findings are comparable to accepted tabular AD papers in the 5.75–6.75 range (MCM: 6.67, AnoLLM: 6.75, DRL: 5.75). Its definitional/framing weakness is more significant than MCM's minor concerns (lowest weakness favorability 1.40) but less severe than the fairness and novelty issues that brought Gradient-based AD (5.75, Reject) down (weakness favorabilities as low as -5.42). The Likelihood Peaks paper (5.67, Reject), which studies the same phenomenon from a different angle, had weakness favorabilities down to -3.93 and was rejected.

**Narrowing:** The paper sits between the cleanly-accepted tabular AD method papers (MCM at 6.67, AnoLLM at 6.75) and the rejected papers with significant flaws (Likelihood Peaks at 5.67, Gradient AD at 5.75). The Definition 3.3 issue (favorability 0.63) is real and pulls the score down from the 6.5+ range, but the core empirical contribution (favorability 12.95) and the explanatory analysis are too strong for a reject-level score. The paper's strengths are comparable to accepted papers, but the framing issue is a meaningful weakness that those papers do not share.

**Final placement:** The paper makes a genuine empirical contribution with good explanatory analysis, but the central framing via Definition 3.3 is compromised. The fix is achievable within a revision cycle (reframe around direct evidence, specify thresholds, or drop the problematic definition). In its current form, the contribution is solid but the framing overreaches.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>