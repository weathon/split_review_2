Now I have sufficient calibration data. Let me produce the final review.

**Round 1 bracket**: 4–6. The paper has genuine strengths (compact architecture, good sensitivity analysis) but is dragged down by a misleading imputation claim and missing variance reporting. Comparing with **FITS (8.00)** — the gold standard lightweight TS paper — TSPulse has a more serious reporting-integrity issue. Comparing with **ROSE (5.75)** — which shares register-token ideas — TSPulse covers more tasks but has the additional misleading claim. Comparing with **LPTM (3.80)** — TSPulse is clearly stronger, with better validation and fewer severe weaknesses. Narrowing to **4.5–5.5** based on these comparisons.

---

## Summary

TSPulse proposes a family of ultra-light (1M parameter) pre-trained time-series models with three disentangled embedding views (temporal, spectral, semantic) obtained via multi-objective masked reconstruction, plus hybrid masking for imputation robustness and lightweight post-hoc fusers (TSLens, MHT) for task specialization. It is evaluated across anomaly detection, classification, imputation, and similarity search on 75+ datasets.

## Strengths

- **Genuinely compact architecture (1M parameters).** The paper delivers a pre-trained time-series model with 1M parameters that achieves broadly competitive results across 4 tasks. Models like MOMENT (40M–340M) and UniTS (~30M) are an order of magnitude larger, making TSPulse a plausible candidate for CPU-only and edge deployment — this is a real engineering contribution. (Supported by Section 4, Fig. 4–7, and the parameter counts in Fig. 7.)

- **Sensitivity analysis provides meaningful evidence of differentiated representations (Table 2, Section 6).** The controlled perturbation experiments on synthetic data cleanly demonstrate that temporal embeddings distort 130% under phase shift while semantic embeddings distort only 12%. This is genuine behavioral evidence for embedding specialization — the kind of analysis many methods papers skip. (Table 2, Section 6, lines 305–333.)

- **The hybrid masking scheme is a practical improvement (Section 2, Fig 3-A).** Moving beyond fixed block masking to a hybrid point/block strategy during pre-training is a sensible response to the known limitation that block-masked models generalize poorly to irregular missingness. The ablation (Table 1c: 79% drop without hybrid masking under hybrid-mask evaluation) strongly supports its importance for imputation. (Lines 63–65, Table 1c, Section 5.)

## Weaknesses

### Fatal
None.

### Major

- **Misleading imputation claim.** The paper's text (line 202) states "Compared to statistical interpolation methods, TSPulse shows 50%+ gains," and the abstract claims "+50% on imputation" without qualification. However, the paper's own table (Figure 6) lists "Interpol" at Mean MSE = 0.039 — substantially *better* than TSPulse (ZS) at 0.074 — with IMP(%) shown as "-" (no improvement). Since Interpol is a statistical interpolation method, the blanket claim about "50%+ gains over statistical interpolation methods" is inaccurate. The paper lists Interpol in the table but the text selectively references only the baselines TSPulse beats (Naive: 0.339, Linear: 0.161), creating a misleading overall impression. This discrepancy between the headline claim and the underlying data undermines trust in the reported results.

- **No variance or uncertainty reporting across any experiment.** Across four task families, dozens of datasets, and multiple baselines, the paper reports only point estimates. For classification (29 UEA datasets, Fig. 5) — where the margin over VQShape is 0.733 vs. 0.701 (3.2pp absolute) — there are no standard deviations, error bars, or significance tests. The same is true for anomaly detection (40 TSB-AD datasets), similarity search, and imputation (6 datasets × 4 mask ratios). Without variance estimates, it is impossible to assess whether the reported gains are reliable, and the modest margins in some settings make this omission consequential.

### Minor

- **The claimed "disentanglement" is weaker than the terminology implies.** The temporal, spectral, and semantic tokens are concatenated ([Time_E; FFT_E; Reg_E], line 67) and processed jointly through the entire TSMixer backbone, which can freely mix information among them. Disentanglement is enforced only at the output via different loss functions on different embedding segments (lines 73–79) — there is no mutual information minimization, orthogonality constraint, or information bottleneck between segments. The sensitivity analysis (Table 2) demonstrates that embeddings *respond differently* to perturbations, which is evidence of specialization/behavioral differentiation but not necessarily of the strong disentanglement the terminology suggests. The paper would benefit from more precise language (e.g., "weak disentanglement" or "specialization through separate supervision").

- **The similarity search comparison to Chronos inflates reported gains.** The paper highlights surpassing Chronos "by 100%" (line 295). Chronos (Ansari et al., 2024) is a *forecasting* foundation model — using its raw representations for a retrieval task is an off-task baseline that does not represent the state of the art in time-series similarity search. While MOMENT provides a more appropriate comparison (TSPulse beats it by 25–40%), the Chronos framing overstates the result. The paper should acknowledge this limitation or include a proper apples-to-apples baseline (e.g., TS2Vec embeddings).

- **The classification ablation (Table 1b) is run on an unsubstantiated subset of 17 out of 29 UEA datasets.** The paper states "a representative subset of 17 UEA datasets for faster analysis" (line 300) without any justification for how the subset was chosen. If the subset excludes datasets where effects are smaller, this could inflate the reported ablation gaps.

### Trivial
None.

## Nice-to-Haves

- Report zero-shot classification accuracy (e.g., using semantic embeddings with nearest-centroid classifier) to complement the fine-tuned results.
- Evaluate similarity search on a real retrieval benchmark with human-annotated relevance, rather than only synthetic augmented queries.
- Present the w/o Hybrid PT ablation under *both* block-masking and hybrid-masking test conditions to disentangle train-test mismatch from the genuine benefit of hybrid pre-training.
- Include a discussion of failure cases: across 75+ datasets, which types of time series does TSPulse handle poorly?

## Removed Points

These points from the input review were filtered out with justification:

- **"No evaluation of zero-shot classification"** — Scope creep. The paper does not claim zero-shot classification; classification is done via TSLens fine-tuning, which is explicitly part of the method's stated design.
- **"No analysis of failure cases"** — Nice-to-have, not a core weakness.
- **"Hybrid PT ablation conflates train-test mismatch"** — The paper acknowledges (line 301) this is evaluated "under hybrid-mask eval settings," so the concern is partially addressed. Not a major flaw.
- **"Univariate pre-training limits zero-shot multivariate capability"** — The paper explicitly states this limitation and discusses it (line 86).
- **Various section-by-section formatting/scope notes** — Are either addressed by the paper, scope-creep, or are minor observations that do not constitute weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Correct the imputation claim in both the abstract and main text.** Acknowledge that Interpol (a simple interpolation baseline) achieves lower MSE than TSPulse (ZS), and qualify the "+50%" claim to refer only to specific baselines (Naive, Linear) rather than to "statistical interpolation methods" broadly.
- **Add multi-seed variance reporting**, at minimum for the main results (classification, anomaly detection). This is critical for credibility given the modest margins in some settings.
- **Replace or supplement the Chronos similarity search baseline** with a model designed for representation learning (e.g., TS2Vec).
- **Justify the 17-dataset ablation subset** or report per-dataset results so readers can assess potential selection bias.

## Score and Decision

**Calibration Anchors Referenced:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| bWcnvZ3qMb.md (FITS) | 8.00 | 1 | Yes | Gold-standard lightweight TS model. Cleaner writing, no reporting issues, 10k params vs TSPulse's 1M. TSPulse's misleading imputation claim places it well below this anchor. |
| e1wDDFmlVu.md (Time-MoE) | 7.33 | 1 | Yes | Large-scale MoE for TS forecasting. More rigorous evaluation, no reporting issues. TSPulse is not comparable in scope or rigor. |
| tdttNKCtyB.md (ROSE) | 5.75 | 2 | Yes | Shares register-token and time-frequency ideas. Evaluated only on forecasting. TSPulse covers more tasks but has the additional imputation reporting issue that ROSE lacks. |
| Iip7rt9UL3.md (Presto) | 4.75 | 2 | No | Lightweight pre-trained TS model for remote sensing. Similar parameter-efficiency motivation. Mixed reviews (6,3,5,5). Comparable quality to TSPulse. |
| ZkEsEFFUyo.md (CloudOps) | 4.33 | 2 | No | Pre-training for TS forecasting, limited domain focus. Score 3,5,5. |
| KJ1w6MzVZw.md (LPTM) | 3.80 | 1 | Yes | Pre-trained TS model with notable weaknesses (limited novelty, poor writing, missing baselines). TSPulse is clearly stronger. |
| SZErAetdMu.md (TOTEM) | 3.00 | 1 | Yes | Universal TS representation with severe weaknesses (overclaiming, weak experiments). TSPulse is substantially stronger. |

**Weighted-Item Comparison:** My draft's strengths (+4.77, +4.78, +4.61) are comparable to FITS's strongest items (+4.89, +4.71, +4.69), confirming that the paper's positive contributions are genuine. However, my draft's weakest items are the misleading imputation claim (-3.15) and missing variance (-3.91) — weights that align with papers scoring 4–5. The variance issue alone is common in 4–5 range papers (cf. LPTM's -5.49 for missing std, and TOTEM's -5.49 for "experimental methodology not robust"). The imputation claim is a distinct integrity concern that pushes the score downward from what the method alone would warrant.

**Round 1 bracket**: 4–6. **Narrowed to**: 4.5–5.5 after Round 2 comparison with ROSE (5.75) and Presto (4.75). The misleading imputation claim is a significant reporting issue that prevents the paper from reaching the borderline-accept range (≥6), while the genuine contributions (compact architecture, sensitivity analysis, hybrid masking) keep it above strong rejection (≤3).

**Score**: 4.5 — The paper has genuine contributions but is undermined by a demonstrable discrepancy between its text/abstract claims and its own data in the imputation evaluation, combined with the absence of any variance reporting across all experiments.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>