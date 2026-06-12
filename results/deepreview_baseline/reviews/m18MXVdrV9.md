## Summary

This paper introduces INFO-SEDD, a method for estimating information-theoretic quantities (KL divergence, mutual information, entropy) for high-dimensional discrete data using Continuous Time Markov Chains (CTMCs). The key idea is to leverage the score function of a discrete diffusion process, trained via the DWDSE loss, to compute these quantities without requiring the common "embedding trick" of projecting discrete data into a continuous space. The authors derive theoretical error bounds showing consistency, and demonstrate strong empirical performance on synthetic benchmarks, text summarization, and genomics tasks, outperforming existing variational and embedding-based estimators, especially in high-MI and high-dimensional settings.

## Strengths

- **Novel and principled approach**: Bridging discrete diffusion generative models with information estimation is original. The derivation using Dynkin's formula provides a clean mathematical foundation, and the use of absorbing-state CTMCs to extract marginal scores from a joint model (Equation 6) is elegant and practically impactful.
- **Strong empirical validation**: Synthetic experiments with known MI values show clear and consistent superiority over a wide range of competitors, including in challenging high-MI / high-dimensional regimes. Real-world applications in text summarization (consistency, model selection) and genomics (consistency, motif discovery) demonstrate practical utility and alignment with domain knowledge.
- **Theoretical consistency guarantee**: The error bound (Equation 7) decomposes estimation error from score approximation and truncation bias, establishing that INFO-SEDD is consistent up to an exponentially decaying bias. This provides a rigorous foundation for the method.
- **Practical advantages**: INFO-SEDD can leverage pretrained discrete diffusion models, avoids the need for continuous embeddings, and is sample-efficient (accurate with 10^3 samples). The ability to handle high-dimensional discrete data directly is a significant improvement over embedding-based alternatives.

## Weaknesses

### Fatal
None.

### Major
1. **Scalability and computational cost are insufficiently addressed.** The paper claims scalability via sparse rate matrices, but provides no analysis of how training or inference cost scales with sequence length, vocabulary size, or number of dimensions. In the experiments, sequence lengths are modest (e.g., 200 bases for DNA, a few hundred tokens for text). For longer sequences (e.g., entire genomes), the cost may become prohibitive. A comparison of wall-clock time or parameter counts against competitors is missing.

2. **Heavy dependence on pretrained discrete diffusion models.** INFO-SEDD requires a score model trained with DWDSE loss. While the paper shows successful fine-tuning of MDLM and CADUCEUS, for a new discrete domain without a pretrained model a user would need to train a discrete diffusion model from scratch, which is non-trivial and expensive. The paper does not discuss this barrier to adoption.

3. **Real-world consistency tests rely on heuristic approximations of ground truth.** For text, the ground-truth MI is approximated from entropy rate estimates; for genomics, from classifier accuracy. These approximations are reasonable but not rigorous. The paper's claim that INFO-SEDD "outperforms" competitors should be interpreted with caution, as the baselines are themselves approximations. The synthetic benchmarks provide the true ground truth and are more definitive.

4. **Entropy estimation results are relegated to the appendix.** The Ising model experiment (Appendix D) is an important part of the method's claimed versatility but receives no discussion in the main text. A brief summary in the main paper would strengthen the case.

### Minor
1. **Missing comparison with classical discrete estimators.** The paper mentions Pinchas et al. (2024) as a classical estimator but does not include it as a baseline. Adding a simple plug-in estimator (with bias correction) would help contextualize the difficulty of the problem.

2. **The theoretical bound contains unspecified constants.** The bound (Equation 7) depends on constants C1, C2, and the score errors ε_p, ε_q. While this is standard for such analyses, the paper does not discuss how these constants could be estimated in practice or used to guide hyperparameter choices (e.g., T, network capacity).

3. **No statistical significance reported for correlations in Table 2.** With only 15 models, some correlations may not be statistically significant. P-values or confidence intervals would strengthen the model selection analysis.

### Trivial
- Some notation in Section 2.1 (\( s_b^p(a, t)_t \), later simplified) appears slightly awkward, likely due to parser artifacts.
- Figure captions in the provided text are overly repetitive.

## Nice-to-Haves
- Include runtime and parameter count comparisons with competitors.
- Provide a practical guide for selecting T, σ(t), and network size based on the theoretical bound.
- Release code and pretrained models for reproducibility.
- Demonstrate on longer sequences (e.g., 1000+ tokens) to further test scalability.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
- Add a subsection discussing computational complexity (training and inference) and how it scales with sequence length and vocabulary size.
- Improve the comparison by including a simple discrete estimator (e.g., Miller-Madow) to show why traditional methods fail and to emphasize the contribution.
- Provide confidence intervals or significance tests for the correlations in Table 2.
- Summarize the Ising model results briefly in the main text to support the claim of versatility.

## Score and Decision

**Score**: 8 (Accept)

**Decision**: Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: Accept<decision>Accept</decision>