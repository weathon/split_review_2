## Summary

The paper proposes DGNet, a self-supervised multi-head SimCLR framework for EEG-based dementia classification. The method decomposes EEG signals into five frequency bands (delta, theta, alpha, beta, gamma), processes each band with an independent CNN encoder and projection head, and uses an adaptive temperature contrastive loss. The authors report 92.90% accuracy on an Alzheimer's vs. cognitively normal classification task, claiming state-of-the-art performance and significant improvements over training from scratch and single-head baselines.

## Strengths

- The problem is important: scalable, low-cost EEG-based dementia screening could address a real diagnostic bottleneck.
- The multi-band processing approach is neurophysiologically motivated, as dementia is known to produce frequency-specific spectral changes.
- The ablation study systematically examines the contribution of each component (SSL, multi-head, augmentation, adaptive temperature, regularization).

## Weaknesses

### Fatal
None.

### Major

1. **Unclear and potentially inconsistent methodology.** The architecture description is confusing: the frequency band extractor is described as both bandpass filters and parallel 1D depthwise convolutions. The encoder output dimension is given as [5, C', L/32] but the linear evaluation layers have 612 and 256 units—612 does not match 5×128=640, and the source of 612 is unexplained. The training objective equation (1) is garbled and does not match standard contrastive loss forms; the notation is inconsistent and the derivation of the regularization term is missing.

2. **Results are suspiciously high and lack statistical rigor.** The proposed method achieves 92.90% accuracy while the next best baseline in Table 1 is 74% (ATCNet). Such a large gap (nearly 20 percentage points) on a small dataset (88 subjects) raises concerns about overfitting, data leakage, or improper baseline tuning. No standard deviations or confidence intervals are reported for the main results, making it impossible to assess significance. The only method that reports variance (BI-MCGNN, 91.25±0.38) is within 1.65% of the proposed method, suggesting the claimed advantage may not be statistically meaningful.

3. **Inconsistent and potentially miscalculated relative improvements.** The abstract claims a 31.5% relative improvement over training from scratch, but the ablation shows training from scratch at 63.35% and the full model at 92.90%. The actual relative improvement is (92.90-63.35)/63.35 ≈ 46.6%, not 31.5%. The 25.4% improvement over single-head is approximately correct (73.52→92.90 gives 26.4%). This discrepancy suggests the authors may have used different baselines or miscalculated.

4. **Inadequate comparison with related multi-band or self-supervised EEG methods.** The paper claims state-of-the-art in "multi-head approaches" but does not define this category or compare with other multi-band SSL methods for EEG (e.g., contrastive predictive coding, masked autoencoding, or other frequency-band decomposition approaches). The baselines in Table 1 are generic EEG models not designed for dementia classification and are likely undertuned. Table 2 compares with prior work on the same dataset, but the proposed method's advantage over the best prior method (BI-MCGNN, 91.25%) is marginal (~1.65%) and within the reported standard deviation of that method.

5. **Limited novelty.** The core idea—multi-band EEG processing with self-supervised contrastive learning—has been explored in prior work (e.g., multi-band SimCLR for EEG, frequency-specific SSL). The adaptive temperature mechanism is taken from Wang et al. 2024 without clear attribution of what is novel beyond applying it to EEG. The paper does not clearly delineate which components are novel contributions versus existing techniques.

### Minor

- The dataset is small (88 subjects) and results may not generalize to larger, more diverse populations. The paper does not discuss this limitation.
- The segmentation into 30-second epochs is motivated by sleep research, but the paper does not analyze whether epoch length affects results or whether there is temporal dependency between epochs from the same subject.
- The paper uses LOSO cross-validation, which is appropriate, but does not report per-subject performance or failure cases.

### Trivial

- The paper states "adaptive 5 band heads" in tables but the model name is DGNet; the naming is inconsistent.
- Figure 3 (spectrogram visualization) is referenced but not clearly explained; it is unclear what insight it provides.

## Nice-to-Haves

- Release code and pretrained models to enable reproducibility and fair comparison.
- Report results with standard deviations across multiple runs or LOSO folds.
- Compare with other self-supervised EEG methods that use frequency-band decomposition (e.g., contrastive predictive coding on band-filtered signals).
- Include a more thorough hyperparameter analysis, especially for the adaptive temperature and regularization parameters.

## Novel Insights

None beyond the paper's own contributions. The paper applies existing techniques (SimCLR, multi-head processing, adaptive temperature) to a specific EEG dementia classification task, but does not produce a new theoretical insight or surprising empirical finding that would reshape understanding of EEG representation learning.

## Suggestions

- Clarify the architecture: provide a precise description of the frequency band extractor, encoder, and projection head with exact dimensions. Explain the discrepancy between 5×128=640 and the 612-unit linear layer.
- Correct the relative improvement numbers and report absolute improvements with proper baselines.
- Add statistical significance tests (e.g., paired t-test across LOSO folds) and report standard deviations for all metrics.
- Compare against properly tuned, task-specific baselines and other self-supervised EEG methods that use frequency-band information.
- Clearly state which components are novel contributions and which are adopted from prior work (especially Wang et al. 2024).

## Score and Decision

The paper addresses an important problem and the multi-band SSL approach is reasonable, but the evaluation is insufficiently rigorous, the methodology is unclear, and the claimed improvements are not convincingly supported. The results are suspiciously high compared to poorly tuned baselines, and the novelty is limited. The paper requires substantial revision to be acceptable.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>