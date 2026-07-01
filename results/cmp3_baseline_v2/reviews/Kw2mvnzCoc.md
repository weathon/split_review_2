## Summary

TSPulse introduces a family of ultra-lightweight (1M parameter) pre-trained time-series models designed for diagnostic tasks—anomaly detection, classification, imputation, and similarity search. The key innovation is a pre-training framework that performs disentangled masked reconstruction across multiple representation spaces (time and frequency) and abstraction levels (local patterns and global semantics), producing three complementary embedding views (temporal, spectral, and semantic). Despite its tiny size, TSPulse achieves strong zero-shot and fine-tuned performance across over 75 datasets, often outperforming models 10–100× larger while supporting CPU-only deployment.

## Strengths

- **Ultra-lightweight yet highly performant:** With only 1M parameters, TSPulse consistently matches or surpasses models 10–100× larger across four diagnostic tasks, while enabling CPU inference speeds that are 10–120× faster than comparable pre-trained models (Figure 7, Table 1). This is a genuinely practical contribution for real-time and resource-constrained deployments.

- **Well-motivated disentangled representation learning:** The idea of explicitly separating temporal, spectral, and semantic embeddings during pre-training is sound and addresses a real limitation in existing time-series models that entangle these heterogeneous signals. The sensitivity analysis (Table 2) convincingly shows that the three embedding types respond to perturbations (noise, missing data, phase shifts) in distinct and predictable ways—temporal embeddings are highly phase-sensitive, FFT embeddings capture spectral structure, and semantic embeddings are robust across distortions.

- **Comprehensive experimental validation:** The paper evaluates TSPulse on four distinct diagnostic tasks using established benchmarks (TSB-AD for anomaly detection, UEA for classification, LTSF datasets for imputation, and a custom similarity search setup). Ablation studies (Table 1a–d) systematically quantify the contribution of each design component (dual-space learning, hybrid masking, TSLens, identity initialization, disentanglement), with performance drops of 5–79% when removing key components.

- **Simple yet effective innovations:** The hybrid masking strategy (mixing full-patch and partial-patch masking with variable ratios) is a straightforward fix to the unrealistic missing patterns used in prior work, and the ablation shows a 79% MSE degradation when omitted under hybrid evaluation. The identity initialization for channel mixers during fine-tuning is a practical solution to a known instability problem.

- **Transparent and reproducible design:** The paper provides clear architecture diagrams (Figures 2 and 3), detailed loss formulations, and states that all pre-training and evaluation datasets are publicly available.

## Weaknesses

### Fatal
None.

### Major

1. **Task-specific pre-training weakens the "versatile" claim.** Section 3.1 states that TSPulse is specialized for each task through reweighting loss objectives during pre-training. This means that different downstream tasks require different pre-trained model variants (e.g., one for anomaly detection, another for classification). While pre-training is cheap (1 day on 8×A100 GPUs), the paper does not demonstrate that a single pre-trained model works across all four tasks simultaneously. The abstract and introduction emphasize "direct zero-shot usability" and "general transferability," which implies a single model, yet the actual design produces task-optimized copies. This is a significant nuance that moderates the claimed versatility.

2. **Disentanglement is empirically demonstrated but not formally quantified.** The sensitivity analysis (Table 2) shows that different embeddings respond differently to perturbations—this is evidence of specialization, not necessarily disentanglement in the representation learning sense (independent factors of variation). No formal disentanglement metrics (e.g., mutual information between embedding dimensions, factorized decoder analysis, or intervention-based measures) are provided. The term "disentangled" may overstate the degree of factorization achieved. The paper should either use a more precise term like "complementary" or "specialized" or provide stronger formal evidence.

3. **Similarity search evaluation uses a non-standard, custom setup.** The paper constructs its own evaluation based on synthetic data and UCR datasets with hand-crafted augmentations (time shifts, magnitude changes, noise). While the comparison with MOMENT and Chronos is fair within this setup, the lack of a widely accepted benchmark for time-series similarity search with distorted queries makes it difficult to interpret the absolute numbers or compare against future work. The paper would be stronger if it also reported results on an existing retrieval benchmark (e.g., UCR archive with standard evaluation protocols).

### Minor

1. **The "GPU-Free deployment" phrasing is imprecise.** The model is clearly deployable on CPU and the paper shows CPU latencies, which is commendable. However, the term "GPU-Free" appears in the abstract (line: "GPU-free deployment") and contributions, yet GPU timings are also reported (Figure 7). The model was pre-trained on 8×A100 GPUs, and the fine-tuning likely uses GPUs. A more accurate framing would be "CPU-deployable" or "efficient without GPU dependence."

2. **Imputation evaluation potentially advantages TSPulse.** The model is pre-trained with hybrid masking and evaluated under hybrid masking. While this is realistic, it creates an evaluation that aligns with the pre-training distribution. The ablation shows that pre-training with block masking only causes a 79% drop under hybrid evaluation—but what about the reverse: how does hybrid-pre-trained TSPulse perform under traditional block-masking evaluation? This comparison would help quantify whether the gains are due to better generalization or simply distribution matching.

3. **Missing comparisons for anomaly detection.** The TSB-AD leaderboard includes many methods, but it is unclear whether the comparison is fair in terms of computational budget or model size. TSPulse (ZS) outperforms statistical methods (e.g., SubPCA) by 14% and neural methods (CNN) by 16%. But statistical methods use zero parameters, so the comparison primarily demonstrates transfer learning advantage rather than efficiency advantage. The paper would benefit from also comparing against other tiny neural methods (not pre-trained) at similar parameter counts.

4. **The register token count R and embedding dimension D** are not specified in the main text (they appear in Appendix A.9, which is not provided in the main content). While I should not criticize missing appendix, the main text should include key architectural dimensions to allow readers to understand the model without consulting the appendix.

### Trivial
None of notable weight.

## Nice-to-Haves

- Release a single universal TSPulse pre-trained checkpoint (without task-specific loss reweighting) and compare its performance against the task-specific variants to quantify the cost of specialization.
- Provide a formal disentanglement metric (e.g., mutual information between embedding subspaces, or the DCI score) to strengthen the claim.
- Release the similarity search benchmark data to facilitate standardized evaluation.
- Include a comparison of TSPulse with other tiny non-pre-trained models at similar parameter counts (e.g., lightweight CNNs or MLPs) on the same tasks to highlight the value of pre-training beyond just model size.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Clarify in the abstract and introduction that TSPulse produces task-specific pre-trained model variants (via loss reweighting), not a single universal model. If the authors believe a single model suffices, provide evidence.
- Replace or supplement the term "disentangled" with a more precise descriptor (e.g., "specialized" or "complementary") unless formal disentanglement metrics are provided.
- Report imputation performance of TSPulse under block-masking evaluation to quantify how much the gains depend on matching the pre-training mask distribution.
- Add a brief discussion of why the semantic embedding dimension (256) is smaller than the temporal/FFT dimensions (1536), and whether the dimensionality mismatch affects downstream task performance.

## Score and Decision

**Score:** 7.0 – This paper makes a solid contribution to lightweight time-series pre-training. The ideas are well-motivated, the experiments are extensive, and the results are impressive for a 1M parameter model. The primary concerns are the task-specific pre-training (which limits the "versatile" claim) and the overstatement of the "disentanglement" concept without formal evidence. These are addressable and do not invalidate the core contribution, which is a genuinely useful family of models for time-series diagnostics. I lean toward acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>