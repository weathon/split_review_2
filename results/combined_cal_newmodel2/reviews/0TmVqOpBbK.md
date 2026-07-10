## Summary

This paper studies how architectural factors (hidden size, MLP-to-attention ratio, GQA) affect both LLM pre-training loss and inference throughput. It proposes a conditional scaling law that augments Chinchilla-style laws with architectural parameters using a two-step reference-and-calibration approach, and a search framework for identifying architectures that are simultaneously inference-efficient and accurate. The paper validates these methods by training over 200 models (80M–3B parameters), fitting the scaling law on smaller models, and evaluating predictions at the 1B and 3B scales.

## Strengths

- **Empirical scope and systematic ablation (Sections 3.2–3.3, Figures 3–5).** The paper trains over 200 models across 80M–3B parameters and measures how hidden size, MLP-to-attention ratio, and GQA individually affect both training loss and inference throughput. The ablation design — varying one factor while holding others fixed — is clean and makes the U-shaped loss surfaces in Figures 4 and 5 convincing. This is a useful empirical contribution in its own right.

- **Conditional scaling law formulation (Section 3.3, Eq. 3).** The two-step approach — using the Chinchilla optimal loss as a reference and then calibrating with separable multiplicative/additive architecture-dependent terms — is a sensible way to incorporate architectural variables without requiring a monolithic fit over the entire joint space. The normalization of hidden size by √N to obtain scale-invariant optima (Figure 4) is well-motivated, and the resulting U-shaped curves exhibit nearly identical optima across model sizes.

- **Cross-stack and cross-hardware throughput validation (Section 5.1, Appendices F/G).** Efficiency comparisons are run on both vLLM (A100) and SGLang (H200), demonstrating that throughput gains (up to 42–47%) are not artifacts of a specific inference stack or GPU generation.

## Weaknesses

### Major

- **Accuracy comparison against LLaMA-3.2 is not controlled for training data or procedure.** The paper compares its Panda/Surefire models (trained on Dolma-v1.7, 100B tokens for 1B models) against the released open-weight checkpoints of LLaMA-3.2, which were trained on Meta's proprietary data at substantially larger token budgets. The abstract claims improvements "under the same training budget" — this qualifier applies to the paper's own models, not to the LLaMA-3.2 baseline, making the claim ambiguous. The accuracy differences (2.1% at 1B, 0.6% at 3B) conflate architectural choices with differences in data composition, data volume, and training hyperparameters. A controlled retraining of the LLaMA-3.2 architecture under the same pipeline would be needed to attribute the gains to architecture rather than to data/training differences. *(The throughput comparison — up to 42% — is not affected by this issue, as it measures inference on trained architectures.)*

### Minor

- **Scaling law extrapolation degrades beyond ~3× parameter range.** When fitting on 80M–1B models and predicting 3B, the Spearman rank correlation falls to 0.50 (Figure 8, left), which is only weakly informative for ranking architectural variants at the target scale. The paper acknowledges this ("the law's coefficients shift with model size") and pragmatically suggests fitting on models at ~1/3 the target scale. While the honesty is commendable, this finding limits the practical claim that small-model experiments can reliably guide large-model architecture choices.

- **No uncertainty quantification on downstream accuracy results.** Table 1 reports average accuracy across nine benchmarks as single numbers without confidence intervals, standard deviations across training seeds, or per-task breakdowns in the main text. The 0.6% gap at 3B (61.9 vs. 62.5) could plausibly fall within run-to-run variance. Per-task details are deferred to Appendix L.

### Trivial

- The perfect Spearman=1.0 correlation for 3B prediction when fitting on 1B data (Figure 8, right) is likely an artifact of too few evaluation points. The paper does not report how many architectures were evaluated at the 3B scale, making it difficult to interpret the correlation values.

## Nice-to-Haves

- Retrain the LLaMA-3.2-1B and LLaMA-3.2-3B architectures under exactly the same training pipeline (same data, token budget, hyperparameters) as the Panda/Surefire models. This would transform the accuracy comparison into a clean architecture ablation.
- Report per-task accuracy scores with uncertainty estimates (e.g., across evaluation seeds or a small number of training seeds) to allow readers to assess whether small aggregate differences are meaningful.
- Explicitly state the number of architectures evaluated at the 3B scale to make the Spearman correlations in Figure 8 interpretable.

## Removed Points

These points from the harsh critic review were removed or downgraded for the reasons stated:

1. **"Scaling law predicts training loss, not inference throughput (structural — narrower contribution)"** — REMOVED. The paper is explicit about this: Section 5.1 states "rather than solving for I_N(P) directly, we search over feasible configurations P_i that satisfy the loss constraint." The framework never claims to predict throughput from architecture parameters. This is a correctly scoped methodology, not a weakness.

2. **"The additive calibration lacks a b₀ constant term"** — REMOVED. A design choice for a simple two-parameter calibration form. The paper explains both multiplicative and additive variants.

3. **"LLaMA-3.2 was trained on ~9T tokens"** — REMOVED. Speculative about LLaMA-3.2 training data volume; exact numbers are not confirmed. The general point (different data/training) is already captured in the Major weakness.

4. **"Missing summary statistics for non-separable formulations in main text"** — REMOVED. The paper notes in Section 5 that non-separable formulations were tested in the appendix and did not improve performance. Deferring such ablations to the appendix is standard practice.

5. **"Scaling law doesn't model the accuracy-efficiency trade-off, only half of it"** — REMOVED. The paper's framework explicitly enumerates architectures that satisfy the loss bound and then measures throughput empirically. This is the stated methodology, not an oversight.

## Novel Insights

The favorability ratings from the draft scoring model highlight a clear asymmetry: the paper's strengths (12.84–14.88) are genuinely strong — comparable to or exceeding accepted papers in the calibration corpus — while the most damaging weakness (-1.59) is a single, discrete issue (the confounded accuracy baseline) rather than a structural flaw in the methodology. This suggests the paper's core technical contribution (conditional scaling law + search framework) is sound, but the presentation of the headline empirical results overstates what the evidence supports. The paper would be considerably strengthened by retracting the claim that the LLaMA-3.2 accuracy comparison is a controlled validation of the method, and instead presenting it as suggestive evidence alongside the controlled loss-prediction validation (Figure 6, Figure 7 left).

## Suggestions

- Reframe the accuracy comparison with LLaMA-3.2 explicitly as "models trained with our framework vs. existing open-weight checkpoints" rather than implying a controlled architecture ablation. Better yet, retrain the LLaMA-3.2 architecture under identical conditions.
- Add confidence intervals or note the single-run nature of the accuracy results.
- Report the number of architectures evaluated at each parameter scale so that Spearman correlations in Figure 8 can be interpreted.

## Calibration Anchors

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/xGM5shdGJD.md (Hitchhiker's Guide) | 5.20 | R1 | Yes | Similar topic (fitting scaling laws), lower avg strength favorability (max ~13.9 vs paper's ~14.9); had a -3.79 favorability weakness (lack of novelty) which is more severe than paper's -1.59 |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/i9K2ZWkYIP.md (Sparsely-Connected) | 7.00 | R1 | Yes | Stronger paper: cleaner experimental setup, broader validation, less confounded comparisons. Paper under review is below this. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iZeQBqJamf.md (Language models scale reliably) | 6.50 | R1 | Yes | Stronger empirical validation of scaling law predictions (300× compute savings), cleaner claims. Weaknesses were milder (lowest ~0.70 favorability vs paper's -1.59). Paper is below this. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/VNckp7JEHn.md (Inference Scaling Laws) | 5.75 | R2 | Yes | Similar avg score, comparable weakness severity (-3.79, -2.84 vs paper's -1.59), but lower strength favorability. Paper is comparable. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/xI71dsS3o4.md ((Mis)Fitting Scaling Laws) | 5.75 | R2 | Yes | Survey paper with lower strength favorability, weakness at -4.31. Paper is slightly stronger. |
| (Other R1/R2 anchors not itemized) | 1.00–8.00 | R1/R2 | No | All R1 strong reject anchors (0.50–1.40) are completely irrelevant papers. 3.00–5.25 R1 anchors are less relevant or weaker. 8.00 anchors are much stronger papers. |

**Round-1 bracket:** The paper sits between the 5.20–5.75 papers (which had severe weaknesses around -3 to -4 favorability) and the 6.50–7.00 papers (which had cleaner validation and milder weaknesses). The strengths are strong enough to lift it above the purely negative anchors, but the uncontrolled comparison keeps it below the cleanly validated papers.

**Round-2 narrowing:** Comparing itemized favorability ratings directly: the paper's strengths (14.88, 13.18, 12.84) exceed those of the 5.20–5.75 anchors (max ~13.9), but the paper's worst weakness (-1.59) is more damaging than the mildest weaknesses of the 6.50 anchor (~0.70). This places the paper between these groups. The deciding factor is that the -1.59 weakness is discrete and addressable (reframing claims, retraining baselines) rather than a fundamental flaw in the scaling law methodology itself, which justifies the higher end of the 5.5–6.0 range.

**Final score:** 5.5 — reflects strong technical contribution plus a significant but addressable gap between the claims and the evidence as presented.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>