## Summary
This paper introduces ChaosNexus, a foundation model for forecasting chaotic dynamical systems. The core contribution is the ScaleFormer architecture, a U-Net-inspired Transformer that explicitly models multi-scale temporal structure through hierarchical patch merging and expansion, augmented with Mixture-of-Experts layers and a wavelet-based frequency fingerprint. The model is pretrained on a large corpus of synthetic chaotic ODEs and demonstrates strong zero-shot and few-shot forecasting performance on both synthetic benchmarks and real-world weather data, with a scaling analysis revealing that generalization benefits more from system diversity than per-system data volume.

## Strengths
- **Novel and well-motivated architectural design**: The ScaleFormer's U-Net-inspired multi-scale approach directly addresses a genuine limitation of prior work (Panda, DynaMix) that operates at single temporal resolution. The combination of hierarchical patch merging/expansion with axial attention, MoE layers, and wavelet frequency conditioning is a coherent and principled design for chaotic dynamics.
- **Strong empirical results on multiple fronts**: The model achieves state-of-the-art zero-shot performance on the large-scale synthetic benchmark (9.3K systems) across both point-wise (sMAPE) and attractor statistics (D_frac, D_step, D_lyap, ME_LRW). The weather forecasting results are particularly striking: zero-shot MAE below 1°C for 5-day global temperature, outperforming baselines trained on 473K samples from the target domain.
- **Insightful scaling analysis**: The finding that generalization scales with system diversity rather than per-system trajectory volume (Figure 4b vs 4c) is a valuable design principle for scientific foundation models. This goes beyond simply confirming prior work by providing a controlled comparison that isolates the effect of diversity from data volume.
- **Comprehensive evaluation methodology**: The paper evaluates both short-term point-wise accuracy and long-term attractor preservation using multiple complementary metrics (sMAPE, correlation dimension error, KL divergence, Lyapunov exponent error, weighted mean energy error), which is appropriate for chaotic systems where point-wise accuracy alone is insufficient.

## Weaknesses
### Fatal
None.

### Major
- **Insufficient comparison with Panda on the weather benchmark**: The paper states that "ChaosNexus also outperforms Panda on many variable forecasting tasks" but does not provide the actual Panda numbers in the main paper or the referenced Appendix A.6. Given that Panda is the most directly comparable baseline (same pretraining corpus, same domain), this omission is significant. The reader cannot assess whether the multi-scale architecture provides meaningful gains over the single-scale Transformer baseline on real-world data.
- **Missing details on model size and computational cost**: The paper reports parameter counts for scaling experiments (2.83M to 52.63M) but does not specify the parameter count of the main ChaosNexus model used in the zero-shot and few-shot evaluations. Similarly, training time, inference speed, and memory requirements are not reported. This makes it difficult to assess the practical trade-offs of the architecture.
- **The weather benchmark comparison is asymmetric**: ChaosNexus is pretrained on synthetic chaotic systems and then fine-tuned on weather data, while the baselines (CrossFormer, FEDFormer, etc.) are trained from scratch on the weather subsets. This is a reasonable setup for demonstrating transfer learning, but the paper should more clearly acknowledge that the comparison is between a pretrained model and models trained from scratch, not between models with equivalent training budgets.

### Minor
- **The MMD regularization term (Equation 10) uses the full predicted and ground-truth trajectories within a batch, but the paper does not specify how this interacts with the autoregressive generation process during training** (e.g., whether the model generates H steps in one shot or iteratively). Clarifying this would improve reproducibility.
- **The wavelet scattering transform is mentioned but not described in sufficient detail** (the reader is referred to Appendix C.3, which is stripped). The choice of wavelet family, number of scales, and how the scattering coefficients are computed should be summarized in the main text.
- **Figure 2 uses box plots with inset mean+CI plots, but the box plots themselves are difficult to read** due to the large number of models and the small figure size. A table with numerical values would complement the visualization.

### Trivial
- The paper uses "REVISE" markers in several places, suggesting incomplete editing of the manuscript.

## Nice-to-Haves
- An ablation study isolating the contribution of each component (multi-scale U-Net, MoE, wavelet fingerprint, MMD loss) would strengthen the paper. The paper mentions "extensive ablation studies" in Appendix A but the main text does not summarize the key findings.
- A comparison with a version of Panda that uses the same training objective (MSE + MMD) would help disentangle the effect of architecture from the effect of training objective.
- Analysis of which experts in the MoE layers specialize to which types of dynamics would provide mechanistic insight into the model's operation.

## Novel Insights
Beyond the paper's own contributions, the most novel insight is the controlled scaling experiment showing that system diversity, not per-system data volume, drives generalization in chaotic system foundation models. While prior work (Lai et al., 2025) established that scaling the number of systems improves performance, this paper's Figure 4(b) provides the complementary negative result: holding system diversity fixed while increasing trajectories per system yields negligible gains. This is a non-obvious finding—one might expect that more trajectories per system would help the model learn the attractor geometry more precisely—and it has practical implications for data collection strategies in scientific domains.

## Suggestions
1. Report the Panda baseline results on the weather benchmark in the main paper or a clear table, so readers can directly compare ChaosNexus with the most relevant prior work.
2. Specify the parameter count, training time, and inference speed of the main ChaosNexus model used in the experiments.
3. Clarify the training procedure: is the model trained to predict H steps in one forward pass, or is it trained autoregressively with teacher forcing? How does the MMD loss interact with the generation process?
4. Add a brief summary of the ablation study findings in the main text (e.g., "removing the multi-scale U-Net structure increases D_step by X%, removing MoE increases sMAPE by Y%").

## Score and Decision
The paper presents a well-motivated architecture that addresses a genuine limitation of prior work, with strong empirical results on both synthetic and real-world benchmarks. The scaling analysis provides a valuable design principle. The main weakness is the incomplete comparison with Panda on the weather benchmark, which should be addressed. Overall, the contribution is solid and the paper is likely to be of interest to the ICLR community.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>