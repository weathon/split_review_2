## Summary

TSPulse proposes a family of ultra-lightweight pre-trained time-series models (~1M parameters) with disentangled temporal, spectral, and semantic embeddings, learned through multi-objective masked reconstruction across multiple representation spaces. The method includes post-hoc fusers (Multi-Head Triangulation for anomaly detection, TSLens for classification) and a hybrid masking strategy. The paper evaluates across four diagnostic tasks (anomaly detection, classification, imputation, similarity search) on 75+ datasets, reporting SOTA results against models 10–100× larger.

## Strengths

- **Disentanglement is well-motivated and cleanly validated.** The controlled perturbation experiment (Section 6, Table 2) directly supports the core claim: temporal embeddings are phase-sensitive (130% distortion under time shift), FFT embeddings are phase-invariant (21%), and semantic embeddings are the most robust across all perturbations (4.6% under missing data, 2.5% under noise, 12% under phase shift). This is a clean, informative experiment that isolates the disentanglement behavior.

- **The model is genuinely tiny.** At ~1M parameters, TSPulse is 10–40× smaller than comparable pre-trained models (MOMENT: 40M, Chronos: 46M, UniTS: 340M). The efficiency numbers (CPU inference 0.387ms, GPU 0.050ms) are well-documented in the similarity search table (Figure 7) and support the claim of GPU-free deployment.

- **Extensive benchmark coverage.** The paper evaluates across four diagnostic tasks using 75+ datasets, including the TSB-AD leaderboard (40 datasets × 40 methods), UEA classification (29 datasets), and imputation across 6 standard benchmarks. This breadth is a genuine strength.

- **The hybrid masking ablation is informative.** The 79% drop in imputation performance when hybrid masking is removed (Table 1(c)) cleanly demonstrates that the masking strategy contributes substantially. While this creates a confound in the headline claims (see Weaknesses), the ablation itself is principled and honestly reported.

- **TSLens ablation is principled.** Removing TSLens causes 11–16% accuracy drops (Table 1(b)), and identity initialization of channel mixers yields a 9% improvement over random initialization. These are well-designed ablations that isolate specific design choices.

## Weaknesses

### Major

- **"Zero-shot" AD label is overstated.** Section 4.1 states that the official labeled tuning set is used for multi-head triangulation to select the best-performing head for TSPulse-ZS. Section 3.3 confirms Approach 2 uses "a small labeled validation set" for head selection. The ablation (Table 1(a)) shows Head$_{\text{triang.}}$ achieves 0.48 VUS-PR vs. 0.44 for the best single head (Head$_{\text{ensemble}}$) — a 9% gain from labeled-data-driven head selection. All leaderboard methods use the tuning set for hyperparameter selection, but selecting among qualitatively different reconstruction heads (Time, FFT, Pred, Ensemble) is a more consequential architectural choice than tuning a learning rate. The paper's claim that TSPulse "without any training on the target data, outperforms all models trained on it" (Section 4.1 Results) should be qualified: no weights are updated, but labeled target-domain data guides the head selection. This is more accurately described as validation-guided zero-shot inference.

- **Imputation gains are largely driven by pre-training masking strategy matching the evaluation masking distribution.** The ablation (Table 1(c)) shows that removing hybrid masking from pre-training (block-only) causes a **79% drop** under hybrid-mask evaluation. This means the headline "+50% on imputation" (abstract, contributions list) bundles contributions from the masking strategy together with disentanglement, TSMixer backbone, and other innovations, without disentangling their relative impact. The imputation results are valid for TSPulse as a complete system, but the attribution to the overall method is inflated.

- **No variance, error bars, or statistical significance reported anywhere in the paper.** No standard deviations, confidence intervals, or multi-seed experiments are provided. This makes it impossible to assess whether the reported improvements — especially the modest classification gains (e.g., TSPulse FT 0.733 vs. VQShape 0.701, a ~3.2pp gap) — are meaningful or within noise range. For a paper making strong comparative claims across four tasks, this is a significant methodological gap.

- **The Chronos comparison in similarity search is not meaningful.** Chronos (Ansari et al., 2024) is a forecasting-specific model, not a general-purpose representation model intended for similarity/retrieval tasks. The claimed "100% improvement" over Chronos (Figure 7, Section 4.4) is uninformative. The comparison against MOMENT (25–40% improvement for similarity search) is sufficient to demonstrate the method's strength and should be the headline comparison.

### Minor

- **Task-specific pre-training.** Section 3.1 states that pre-training is specialized per task through reweighted loss objectives, producing four separately pre-trained models (AD, classification, imputation, similarity search). The "1M parameter" claim is per-model, not a single model solving all four tasks. The abstract's phrasing as a "family of" models partially addresses this, but the framing throughout (e.g., "TSPulse achieves strong and consistent gains across four TS diagnostic tasks") could give the impression of a single universal model. This is worth clarifying.

- **The Interpol baseline matches TSPulse (FT) in imputation.** Figure 6 shows both Interpol and TSPulse (FT) achieving MSE of 0.039, but the paper does not discuss this. Simple interpolation matching the fine-tuned model's performance is a meaningful caveat that should be addressed.

- **Embedding dimension mismatch in the sensitivity analysis (Table 2).** Time/FFT embeddings have d=1536 while semantic embeddings have d=256. The distortion percentages are not directly comparable across different dimensions, since a lower-capacity embedding may naturally be less sensitive to perturbations. The paper notes the dimensions but does not account for capacity differences.

- **Semantic head projection is underspecified.** Section 2 describes the semantic head operating on R register tokens to predict the frequency signature $\mathbf{Y}_{\text{sign}}^f$, but the projection from R tokens to the output shape $\mathbb{R}^{S/2 \times C}$ is not explained. This is a minor reproducibility gap.

### Trivial

None.

## Nice-to-Haves

- Disentangle the imputation results by reporting TSPulse with block-only pre-training vs. MOMENT on both block-mask and hybrid-mask evaluations, to show the additive value of disentanglement and backbone innovations beyond masking.
- Normalize the sensitivity analysis for embedding dimension, or provide an analysis that accounts for capacity differences.
- Discuss the Interpol tie in the imputation results.

## Removed Points

These points from the input review were removed for the following reasons:
- *Missing open-source release*: removed per hard rule — not about questioning existing citations, and the paper's Reproducibility Statement documents parameters and datasets. This is a reasonable request but not a valid weakness for review purposes.
- *Preprocessing details deferred to appendix*: removed per hard rule — appendices are stripped by the parser and exist in the original submission.
- *Paper doesn't show competitors' embeddings are entangled*: removed — the paper's claim is about achieving disentanglement in TSPulse, not about measuring competitor entanglement; this asks for a comparison outside the paper's stated scope.
- *Several generic weakness framings* merged into the four major weaknesses above to avoid duplication.

## Novel Insights

Beyond the paper's own contributions, the review process reveals that the paper's architecture conflates two separable contributions: (1) the disentangled multi-space representation learning, and (2) the hybrid masking strategy. The ablation shows the imputation results are dominated by (2), not (1), meaning the headline performance gains should be attributed more precisely across contributions. Additionally, the AD "zero-shot" framing, while technically accurate about weight updates, stretches the standard definition — the paper is transparent about the procedure but the label itself could mislead readers about what information the model receives from the target domain.

## Suggestions

1. Rename "zero-shot" AD to "tuning-set-guided" or "validation-guided zero-shot," or explicitly note in the results paragraph that head selection uses labeled validation data.
2. Disentangle the imputation claims: report TSPulse with block-only pre-training vs. MOMENT on both block-mask and hybrid-mask evaluations.
3. Add error bars or multi-seed experiments for the main results (at minimum for classification and AD).
4. Remove or clearly qualify the Chronos similarity search comparison as a forecasting model not designed for retrieval.
5. Discuss the Interpol baseline matching TSPulse (FT) in imputation.
6. Clarify the semantic head projection in the architecture description.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>