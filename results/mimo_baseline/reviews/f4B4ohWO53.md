## Summary

The paper proposes NVDP (Nonparametric Variational Differential Privacy), a method for sharing text embeddings in a privacy-preserving manner by integrating a Nonparametric Variational Information Bottleneck (NVIB) layer into the transformer architecture. The NVIB layer injects calibrated noise into multi-vector transformer embeddings, and the paper derives a Rényi Divergence formula for Dirichlet Process-based sampling distributions to measure privacy guarantees. Experimental results on GLUE tasks demonstrate that NVDP achieves a better privacy-utility tradeoff compared to a standard VIB-based ablation (VTDP).

## Strengths

- **Sound core idea**: Repurposing the information bottleneck as a privacy mechanism for embedding sharing is well-motivated. The insight that controlling information flow through a bottleneck simultaneously serves utility optimization and privacy protection is elegant and clearly articulated. Removing the residual connection around the MHA block to enforce the bottleneck is an important architectural detail.

- **Clear empirical improvement over VIB ablation**: The NVDP vs. VTDP comparison consistently demonstrates the value of the nonparametric approach across all six GLUE tasks. For example, on MRPC, NVDP achieves 83.0% accuracy with BDP 10.70 and RD 0.34, while VTDP at similar BDP reaches only ~74.8% accuracy with RD 1.20. This shows that NVIB's ability to reduce information capacity through Dirichlet process structure (dropping pseudo-counts, structured weight sharing) provides a meaningful advantage over token-wise VIB noise.

- **Dual privacy measurement**: Reporting both worst-case RDP and BDP measures provides complementary perspectives—the former as a strict distinguishability bound and the latter as a de-anonymization risk measure that accounts for the data distribution. This is a more thorough privacy analysis than reporting a single metric.

## Weaknesses

### Fatal
None.

### Major

- **No empirical privacy evaluation**: The privacy claims rest entirely on the mathematical measures (Rényi Divergence and BDP) without any empirical verification through actual attacks. There is no evaluation of reconstruction attacks, membership inference attacks, attribute inference, or any other adversary model on the shared noisy embeddings. Without this, it is difficult to assess whether the mathematical guarantees translate to meaningful practical privacy. For example, can an adversary who receives the noisy embedding S still recover sensitive attributes? The BDP values reported (ε_μ ≈ 10–20) are relatively high, and the paper does not discuss what level of ε_μ is considered "strong" in this setting or provide empirical grounding for interpreting these values.

- **No comparison with established DP baselines**: The paper compares only against VTDP (VIB-based ablation) and standard regularization (dropout, weight decay). There is no comparison with DP-SGD applied to the embedding model, or any other standard differential privacy mechanism for embeddings (e.g., adding Gaussian noise directly to embeddings, Laplace mechanism). Without such comparisons, it is impossible to assess whether NVDP offers advantages over simpler approaches or whether the NVIB machinery is necessary at all.

- **Privacy guarantee scope is limited**: The privacy analysis covers only the stochastic NVIB mapping but not the full pipeline. BERT is fine-tuned on the task data and produces the initial embeddings x that feed into the NVIB layer. If the BERT encoder is shared alongside the noisy embeddings (which is implied since downstream users need the classifier or encoder), this encoder was trained on the sensitive data and may itself leak information. The paper does not address this, making the practical privacy guarantee unclear.

### Minor

- **Privacy is measured post-hoc, not guaranteed during training**: The NVIB layer is trained with its standard regularization loss (Eq. 5), and privacy is measured after the fact. There is no explicit constraint during training to achieve a target ε. The paper states that "training the NVIB layer calibrates the noise level according to utility," but this means privacy is a byproduct of utility optimization rather than a hard constraint. A user who needs a specific privacy budget cannot directly specify it.

- **Adjacent inputs not formally defined**: For the RDP measure, the paper states they "do not assume any specific notion of adjacency between examples" and report the maximum divergence over all test pairs. While BDP sidesteps this by using the data distribution, the RDP measure without a clear adjacency definition makes the privacy interpretation ambiguous—maximum RD over all pairs conflates inputs that are truly "similar" with those that are inherently different.

- **Limited experimental scope**: Evaluation is restricted to GLUE with BERT-base. No experiments with larger models (RoBERTa, GPT-style encoders), different domains, or different tasks (generation, QA) are presented. The generality of the approach across transformer architectures is not established.

- **Single hyperparameter setting for privacy**: The paper fixes λ=1.1 and δ_μ=10^{-5} for reporting privacy. Sensitivity analysis of these hyperparameters is not provided (beyond the trade-off curves which vary NVDP's regularization strengths).

## Nice-to-Haves

- Empirical attack evaluation (reconstruction, membership inference, attribute inference) to validate that mathematical privacy translates to practical privacy
- Comparison with direct Gaussian noise addition to embeddings (a simple baseline that could be surprisingly competitive)
- Analysis of whether the NVIB layer's ability to drop tokens (set pseudo-counts to zero) contributes meaningfully to privacy beyond just reducing dimensionality
- Experiments on adversarial reconstruction to demonstrate that the shared noisy embeddings resist reverse-engineering

## Novel Insights

The paper's central novel insight is that the Dirichlet Process structure of NVIB provides a more effective privacy mechanism than token-wise Gaussian VIB, because it can simultaneously introduce noise at the weight level (via Dirichlet concentration) and the vector level (via Gaussian variance), and can eliminate vectors entirely. This multi-level noise injection, guided by the nonparametric prior, achieves a better privacy-utility tradeoff than independent per-token noise. This is supported by consistent empirical results across tasks, particularly the RD values which show much lower raw information leakage for NVDP (e.g., 0.34 vs. 1.20 on MRPC).

## Suggestions

- Add empirical attack evaluations, even simple ones (e.g., training a classifier on the noisy embeddings to predict sensitive attributes, or attempting text reconstruction with a decoder), to give readers confidence that the mathematical guarantees translate to practice
- Include a baseline that adds calibrated Gaussian noise directly to the BERT embeddings without any NVIB/VIB training, to isolate the contribution of learned noise calibration from the contribution of simply adding noise
- Discuss the practical implications of the reported BDP values (ε_μ ≈ 10–20) and what level of protection they provide in concrete terms

## Score and Decision

The paper presents a novel combination of NVIB with differential privacy for transformer embeddings, with a well-derived RD formula and clear empirical demonstration of NVDP's advantage over VIB-based approaches. However, the absence of empirical privacy evaluation and comparison with standard DP baselines significantly limits confidence in the practical value of the contribution. The privacy guarantee scope is also incomplete since the BERT encoder's information leakage is not addressed. These gaps place the paper in borderline territory.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject