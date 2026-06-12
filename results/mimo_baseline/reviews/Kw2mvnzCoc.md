## Summary

TSPulse introduces a family of ultra-compact (1M parameter) pre-trained time-series models that learn disentangled representations across three complementary views: temporal (detailed time-domain features), spectral (frequency-domain features), and semantic (high-level abstractions via register tokens). The framework augments masked reconstruction with explicit multi-space and multi-abstraction objectives, hybrid masking strategies, and lightweight task-specific post-hoc fusers (MHT for anomaly detection, TSLens for classification), achieving strong zero-shot and fine-tuned performance across anomaly detection, classification, imputation, and similarity search on 75+ datasets.

## Strengths

- **Strong empirical results across four diverse tasks.** TSPulse achieves first place on both the univariate and multivariate TSB-AD anomaly detection leaderboard (VUS-PR of 0.52 and 0.39 respectively), outperforming the next best method by 14–24% in fine-tuned mode. Zero-shot performance already exceeds all fully supervised baselines, which is a genuinely impressive result. Classification improvements of 5–16% over VQShape, UniTS, and Moment are competitive, and imputation results are strong.

- **Compelling efficiency story.** At 1M parameters, TSPulse runs 10–100× faster than competing models on CPU (0.387ms vs 46.71ms for Chronos on similarity search), making it practically deployable without GPUs. This is a genuine contribution for real-world industrial monitoring and observability applications where latency and compute constraints matter.

- **Well-structured disentanglement framework with supporting evidence.** The design of three embedding types (temporal, spectral, semantic) each optimized with distinct objectives is clean and well-motivated. The sensitivity analysis on synthetic signals (Table 2) provides systematic evidence that the embeddings capture genuinely different properties—temporal embeddings are highly sensitive to phase shifts (130% distortion) while semantic embeddings are most robust to noise and missing data (2.5% and 4.6% respectively). The ablation studies (Table 1) convincingly demonstrate the contribution of each component.

- **Practical design choices with demonstrated impact.** The identity initialization for channel-mixing blocks during fine-tuning (9% gain), the hybrid masking strategy (79% imputation improvement over block-only masking), and the lightweight TSLens module (11–16% over standard pooling) are simple but effective engineering contributions that benefit practitioners.

- **Comprehensive evaluation protocol.** The paper evaluates on established benchmarks (TSB-AD with 40 datasets, UEA with 29 datasets, 6 LTSF imputation datasets, similarity search on UCR), uses official metrics, and includes ablations across all four tasks.

## Weaknesses

### Fatal

None.

### Major

- **Overstated headline claims that rely on selective comparisons.** The abstract claims "+20% anomaly detection, +25% similarity search, +50% imputation, +5–16% classification." The +50% imputation claim is a zero-shot comparison against prompt-tuned UniTS, while the fine-tuned result matches spline interpolation (0.039 vs 0.039). The +25% similarity search compares against MOMENT and Chronos (a forecasting model that is not designed for embedding-based retrieval), which is an asymmetric comparison. The classification range of 5–16% depends on which baseline is chosen. While the results are genuinely strong, the abstract paints a more dramatic picture than the data warrants.

- **The disentanglement claim, while suggestive, is not rigorously proven.** The sensitivity analysis (Table 2) shows different embedding types have different perturbation responses, but the magnitude differences are sometimes modest (semantic 4.6% vs time 8.3% under 30% missing data). More critically, the paper does not include standard disentanglement metrics (e.g., mutual information between embedding spaces, direct cosine similarity analysis between pairs of embedding types) that would establish whether the representations are genuinely disentangled or merely trained with diverse objectives. The claim that TSPulse achieves "disentanglement across both representational spaces and abstraction levels" would be substantially strengthened by such analysis.

- **Incomplete reporting of experimental variability.** All results are reported as single numbers without variance, confidence intervals, or number of runs. For a paper claiming consistent improvements across 75+ datasets, understanding the variance is important—particularly for the zero-shot results where there is no training signal to regularize.

### Minor

- **The imputation evaluation uses hybrid masking during evaluation, which directly matches the proposed pre-training strategy.** This creates a potential confound: is TSPulse's superior imputation performance due to better learned representations, or simply because it was specifically pre-trained with the exact same corruption pattern used at test time? The paper does include block-masking ablation results in the appendix, but the main results would be more convincing with an additional evaluation under standard block masking to disentangle these factors.

- **The similarity search evaluation uses synthetic augmentations (time shifts, magnitude changes, noise) applied to generate queries.** While this enables controlled evaluation, the paper does not justify whether these augmentations reflect realistic retrieval scenarios or whether the improvement would persist on naturally occurring distortions in real datasets.

- **TSLens and MHT are described as "post-hoc fusers" but are actually trained end-to-end during fine-tuning.** The term "post-hoc" suggests they are applied after training without modifying the model, which is somewhat misleading. They are task-specific fine-tuning heads, which is a different design philosophy than what "post-hoc" typically implies.

### Trivial

None.

## Nice-to-Haves

- A direct disentanglement analysis (e.g., mutual information or cosine similarity between the three embedding spaces across many samples) would substantially strengthen the core claim.
- Reporting variance across multiple runs or seeds for key results.
- A discussion of failure cases—on which datasets or task configurations does TSPulse underperform?
- Comparison against more recent lightweight baselines (e.g., MOMENT-Tiny, smaller UniTS variants) to disentangle the benefits of architecture design from model scale.

## Novel Insights

The paper's most novel insight is that explicitly decomposing time-series representations into temporal, spectral, and semantic spaces with distinct reconstruction objectives can yield representations that are both more transferable and more robust than jointly learned monolithic embeddings. The sensitivity analysis provides empirical grounding for this, showing that semantic embeddings are naturally robust to perturbations while temporal embeddings preserve fine-grained alignment—properties that differentially benefit downstream tasks. The idea that a single 1M-parameter model can leverage these complementary views through lightweight task-specific fusers (selecting the right "lens" for each task) is a useful paradigm for efficient time-series analysis.

## Suggestions

- Add standard disentanglement metrics (e.g., mutual information between embedding types, linear probing to predict one embedding from another) to Section 6 to rigorously validate the disentanglement claim.
- Include variance estimates (standard deviation across runs or across datasets) for the main results in Figures 4–7.
- Clarify whether the imputation gains are attributable to hybrid masking during pre-training specifically by reporting results under both block and hybrid evaluation masking in the main text.
- Provide a clearer taxonomy of when to use zero-shot vs. fine-tuned configurations, and what performance trade-offs users should expect.

## Score and Decision

The paper makes a solid, practical contribution: a systematic framework for learning disentangled representations in time-series models with compelling efficiency (1M parameters, CPU-deployable) and strong empirical results across four tasks on established benchmarks. The ablations are thorough and the sensitivity analysis provides meaningful evidence for the core design choices. However, the headline claims are somewhat overstated through selective comparisons, the disentanglement evidence falls short of rigorous proof, and the novelty is primarily in the systematic combination and integration of existing ideas (register tokens, FFT processing, multi-objective pre-training, identity initialization) rather than in fundamentally new algorithms. The practical efficiency gains and consistent performance across tasks make this a useful contribution to the time-series community, particularly for deployment-constrained settings.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept