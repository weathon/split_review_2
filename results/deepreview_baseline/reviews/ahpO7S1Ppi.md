## Summary

This paper introduces Pctx, a personalized context-aware tokenizer for generative recommendation (GR). Unlike existing static tokenizers that assign a fixed semantic ID to each item based solely on item features, Pctx conditions tokenization on a user’s historical interaction context, allowing the same item to receive different semantic IDs for different users. This design captures diverse user interpretations and improves prediction quality. Experiments on three Amazon datasets show consistent improvements of up to 8.9% in NDCG@10 over non-personalized GR baselines.

## Strengths

- **Novel and well-motivated idea**: The paper identifies a genuine limitation of current generative recommendation—static tokenization imposing a universal similarity standard—and proposes a principled solution that tokenizes actions differently based on user context. The motivation (Figure 1) is clear and compelling.

- **Sound methodology**: Challenges C1 and C2 (adaptive tokenization and balancing generalizability vs. personalizability) are explicitly formulated and addressed with concrete design choices (context representation clustering, redundant ID merging, data augmentation, multi-facet generation). The framework is coherent and well-justified.

- **Strong experimental validation**: The paper evaluates on three datasets with comprehensive baselines (10 ID-based + 3 GR methods). The results show Pctx outperforms all baselines on all metrics, and the gains are statistically significant. Ablation studies (Table 3) convincingly isolate the contribution of each component. Additional analyses (model ensemble, ID distribution, case study) further support the claims.

- **Clear exposition**: The paper is well-structured, explains the key ideas intuitively with figures, and provides a helpful discussion section (2.4) comparing Pctx with other tokenization paradigms. The case study with StarCraft II concretely illustrates how personalized IDs capture different item facets.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Dependence on auxiliary context encoder**: Pctx requires a separately trained DuoRec model to obtain context representations. While the paper shows DuoRec outperforms SASRec for this purpose, the two-stage nature adds complexity and hyperparameters (e.g., clustering, fusion weight $\alpha$). The paper does not discuss the computational cost of this stage relative to baselines, which would be useful for practitioners.

- **Limited analysis of hyperparameter sensitivity**: The method introduces several hyperparameters (number of centroids $C_{v_i}$, fusion weight $\alpha$, frequency threshold $\tau$, augmentation probability $\gamma$). Only $\gamma$ is implicitly varied in the ablation (variant “w/ Random Target” sets $\gamma=1$). A sensitivity analysis (e.g., varying $\alpha$ or $\tau$) would strengthen the paper.

### Trivial

- The paper states “U” in Section 2.2.1 for DuoRec—this appears to be a formatting inconsistency (should be “DuoRec”).

## Nice-to-Haves

- An end-to-end version where the tokenizer and GR model are jointly optimized could be an interesting future direction, as acknowledged by the authors.
- Discussion of potential failure cases: when does personalized tokenization hurt? (e.g., very sparse items, cold-start users with short histories).

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Add a table summarizing hyperparameter values and sensitivity analysis for the most critical ones (e.g., $\alpha$, $\tau$).
- Discuss the computational overhead of the two-stage pipeline (DuoRec pretraining + clustering + RQ-VAE) versus end-to-end GR baselines.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>