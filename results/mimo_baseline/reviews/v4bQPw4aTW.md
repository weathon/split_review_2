## Summary

This paper proposes AdaBoN, a two-stage adaptive strategy for Best-of-N sampling that allocates inference-time compute across a batch of prompts by first exploring each prompt's reward distribution with a small budget, then greedily allocating the remaining budget based on estimated marginal gains. The method uses Gaussian kernel density estimation for reward distribution modeling and requires no auxiliary model training, working with any LM-RM combination. The paper also introduces two new evaluation metrics—Batch Win Rate (BWR) and Expected Survival Time (EST)—and demonstrates consistent improvements over uniform allocation across 12 LM-RM pairs, 3 datasets, and 50 batches.

## Strengths

- **Clean problem formulation and algorithm design.** The two-stage AdaBoN algorithm (Algorithm 2) is simple, well-motivated by latency concerns, and grounded in a clear theoretical result (Proposition 3.1 guarantees concavity of marginal value functions, making the greedy allocation optimal). The method is model-agnostic and requires no auxiliary training, making it immediately practical.

- **Comprehensive empirical evaluation.** The paper evaluates across 12 LM-RM pairs, 3 datasets (AlpacaEval, HH-RLHF, PKU-SafeRLHF), and 50 distinct batches per setting, providing broad coverage. Results are consistent: AdaBoN outperforms uniform allocation for 76-100% of batches (Table 2b), achieves BWRs up to 0.70, and is competitive against uniform allocations with 20% larger budgets (EST ≈ 150 for B=120).

- **Well-motivated novel metrics.** The BWR and EST metrics are carefully designed to address the fact that raw reward values are often only meaningful comparatively (since RMs are trained under Bradley-Terry models). The EST provides an intuitive interpretation of computational savings.

- **Scaling behavior.** The paper shows AdaBoN improves with batch size (Figure 3), with average BWR increasing by as much as 0.15 as K grows from 3 to 20, and robustness across inference budgets (Appendix K.1).

## Weaknesses

### Fatal
None.

### Major

- **No comparison with the most related method.** The most directly related work is Damani et al. (2024), which addresses the same inference allocation problem. The authors cite implementation difficulty and computational cost as reasons for omitting this comparison (216,000 MLPs needed). While understandable, this is a significant gap. Even a limited comparison on a single dataset/LM-RM pair with a simplified version of their method would substantially strengthen the empirical claims. Without it, the reader cannot assess whether AdaBoN's simplicity comes at a performance cost relative to trained allocation models.

- **Narrow experimental regime and unclear practical significance.** The paper focuses on small batch sizes (K=5) with large per-prompt budgets (B=120), motivated by on-device inference. However, the practical importance of this specific regime is asserted rather than demonstrated—there is no evidence about real on-device deployment scenarios or how these specific parameter choices relate to actual use cases. Moreover, the BWR improvements, while consistent, are modest in absolute terms (median BWRs of 0.55-0.62), and the paper does not translate these into concrete cost savings (e.g., dollars saved per batch, latency reduction in seconds, or quality improvement in downstream applications).

### Minor

- **Reward-level evaluation only.** All evaluations are conducted using reward model scores. There is no assessment of whether AdaBoN's improvements translate to better alignment quality as measured by human evaluation, LLM-as-judge win rates, or downstream task performance. Given that reward models are known to be imperfect proxies, it's unclear whether the modest BWR improvements would manifest as meaningful alignment gains.

- **Limited model scale.** All experiments use ~8B parameter models. The reward distributions (Figure 1) and the effectiveness of KDE estimation may behave differently at larger scales where reward distributions could have different characteristics.

- **Exploration budget sensitivity.** While the paper claims d=0.75B works well across experiments, Table 3 (Appendix G.1) shows that the optimal d varies across LM-RM pairs, and the paper doesn't provide guidance on how to choose d in practice beyond this default.

### Trivial
None.

## Nice-to-Haves
- A discussion of the computational overhead of the allocation algorithm itself relative to inference cost, even if it's expected to be negligible.
- Analysis of how AdaBoN interacts with different decoding strategies (the paper uses HuggingFace defaults).
- Visualization or analysis of how well KDE captures the true reward distributions as a function of d.

## Novel Insights

The key novel observation is that reward distributions across diverse LM-RM pairs are "smooth and easy to learn" with small exploration budgets, enabling simple KDE-based estimation to power adaptive allocation. This finding—that the structure of reward distributions is exploitable for compute allocation without expensive auxiliary models—complements the broader trend of test-time compute scaling but applies it at the inter-prompt level rather than the intra-prompt level. The contrast with Damani et al. (2024)'s approach (training an MLP per LM-RM pair-budget combination) suggests that in the large-budget regime, direct Monte Carlo estimation from samples may be sufficient, potentially obviating the need for learned allocators.

## Suggestions

- Add at least a limited comparison with Damani et al. (2024), even on a single LM-RM pair and dataset, to establish whether AdaBoN's simplicity carries any performance penalty.
- Include at least one evaluation beyond reward-model scores (e.g., GPT-4 win rates on AlpacaEval) to assess whether BWR improvements translate to actual alignment quality.
- Provide a concrete analysis of practical impact—e.g., if AdaBoN saves 20% of compute, what does this mean in terms of GPU-hours or inference latency for a deployment scenario?

## Score and Decision

The paper presents a clean, well-executed contribution with solid algorithmic design, theoretical grounding, and comprehensive evaluation. The method is practical and model-agnostic. However, the improvements are modest in absolute terms, the most closely related baseline is absent from comparison, and the practical significance of the gains is not established. The narrow experimental regime further limits the paper's generalizability claims. These factors place the paper at the borderline.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>