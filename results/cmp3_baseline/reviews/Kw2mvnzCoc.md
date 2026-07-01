## Summary
This paper proposes TSPulse, an ultra-light (1M parameter) family of pre-trained time-series models designed for diagnostic tasks (anomaly detection, classification, imputation, similarity search). The key technical contribution is a pre-training framework that enforces disentangled representations across three views: temporal (fine-grained time-domain), spectral (frequency-domain), and semantic (high-level abstraction via register tokens). The model uses a hybrid masking strategy, lightweight post-hoc fusers (TSLens for classification, multi-head triangulation for anomaly detection), and identity-initialized channel mixing for stable fine-tuning. Experiments across 75+ datasets show that TSPulse matches or outperforms models 10–100× larger while being deployable on CPU.

## Strengths
- **Ultra-compact yet competitive**: With only 1M parameters, TSPulse achieves results that rival or exceed models with 10–340M parameters, making it highly practical for resource-constrained deployment.
- **Well-motivated disentanglement**: The division of embeddings into temporal, spectral, and semantic views is clearly justified by the different sensitivity patterns observed in the perturbation analysis (e.g., temporal embeddings are shift-sensitive, semantic embeddings are robust). This design is novel for time-series pre-training.
- **Strong empirical coverage**: Evaluation spans four major diagnostic tasks on standard benchmarks (TSB‑AD, UEA, LTSF datasets) with consistent positive results. Ablation studies confirm the contribution of each design component (disentangled heads, hybrid masking, TSLens, identity initialization).
- **Thorough sensitivity analysis**: Controlled experiments with missing data, noise, and phase shifts quantitatively demonstrate that each embedding type behaves as expected, providing direct evidence that disentanglement is achieved.

## Weaknesses
### Minor
- **Scope of zero‑shot claim**: The paper uses “zero-shot” for anomaly detection and imputation, but classification results are obtained after fine‑tuning with TSLens. The abstract and figure captions sometimes conflate the two settings; clarifying the exact zero‑shot scope in each task would improve precision.
- **Comparison fairness**: Several baselines (e.g., statistical methods, non‑pretrained DNNs) are trained from scratch on target data, while TSPulse benefits from ~1B sample pre‑training. The large performance gaps are impressive, but direct comparisons with other pretrained models (and a discussion of data leakage avoidance) would strengthen the argument further.
- **Evaluation of similarity search**: The similarity search evaluation uses a custom setup rather than a widely‑adopted benchmark. While the methodology is reasonable, adopting or adapting an existing retrieval benchmark (e.g., from UCR or monash) would increase credibility.

## Nice-to-Haves
- Provide per‑dataset classification accuracy for all 29 UEA datasets (currently only mean is reported), so that standard deviation and best/worst cases are visible.
- Include inference latency measurements for the full pipeline (masking + backbone + decoder + task head) under real‑world CPU conditions.
- Release the pretrained model weights and code to facilitate reproducibility and community adoption.

## Novel Insights
Beyond the paper’s own contributions, the most interesting insight is that a very small (1M) pretrained model can outperform much larger counterparts by deliberately structuring the embedding space to separate spatiotemporal information from high‑level semantics. The perturbation analysis also reveals that register‑based semantic embeddings are surprisingly robust to time shifts—an important property for retrieval tasks that has not been systematically demonstrated in prior time‑series pretraining work.

## Suggestions
- Clearly separate the reporting of zero‑shot and fine‑tuned results in the main tables (e.g., separate rows or distinct marker shapes in figures).
- Add a short discussion on the potential limitations of univariate pretraining for multivariate tasks and how channel‑mixing during fine‑tuning mitigates this.
- Include a comparison with the recently released Tiny Time Mixer (TTM) family to further contextualize the size‑performance trade‑off.

## Score and Decision
Score: 8  
Decision: Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>