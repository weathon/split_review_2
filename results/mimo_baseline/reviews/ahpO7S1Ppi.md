## Summary

This paper proposes PCTX, a personalized context-aware tokenizer for generative recommendation that conditions item tokenization on a user's interaction history, allowing the same item to receive different semantic IDs under different user contexts. The approach uses contrastive learning-based context encoding, adaptive clustering, frequency-based merging, data augmentation, and multi-facet beam search decoding. Experiments on three Amazon Review datasets demonstrate improvements of up to 8.9% in NDCG@10 over the strongest baselines.

## Strengths

- **Well-motivated and genuinely novel contribution.** The core observation—that static tokenizers in GR implicitly enforce universal item similarity across all users, while users may interpret the same item differently—is compelling and practically important. To my knowledge, this is the first personalized action tokenizer for GR, and the motivation is clearly articulated with a concrete example (watch purchased as gift vs. investment vs. aesthetic).

- **Thoughtful engineering to balance personalization and generalizability (C2).** The paper identifies the over-personalization risk and addresses it through multiple complementary strategies: k-means++ adaptive clustering to condense context representations, frequency-threshold merging to remove infrequent semantic IDs, and data augmentation to connect multiple semantic IDs of the same item. The ablation in Table 3 (rows 2.2 and 3.4) convincingly shows these are essential—removing redundant SID merging causes severe degradation, and random target augmentation underperforms the meaningful personalization of PCTX.

- **Comprehensive and well-designed ablation study.** The ablations systematically isolate each design choice across all three dimensions: personalized context source, tokenization strategy, and training/inference components. Particularly valuable is variant (3.3) vs. (3.4): showing that TIGER with PCTX IDs performs worse confirms gains come from personalization, not merely from having multiple IDs, and variant (3.4) confirms gains are not just from token diversity.

- **Solid experimental execution.** All improvements over ActionPiece are statistically significant (p < 0.05). The model ensemble analysis (Table 4) effectively rules out the trivial explanation that PCTX merely combines DuoRec and TIGER. The StarCraft II case study provides intuitive evidence that different user contexts lead to semantically meaningful token differences (story-driven vs. RTS interpretation).

- **Interesting finding about representation model choice.** DuoRec outperforms SASRec as the context representation model within PCTX despite SASRec being a better sequential recommender, suggesting that representation distinguishability (via contrastive learning) matters more than next-item prediction accuracy for generating useful context representations. This is a valuable empirical insight.

## Weaknesses

### Fatal
None.

### Major

- **Two-stage pipeline design limits end-to-end optimization.** The personalized tokenization relies on a pre-trained auxiliary model (DuoRec) whose representations are frozen during tokenizer training, and the tokenizer itself is frozen during GR model training. This information bottleneck between stages likely limits performance. The paper acknowledges this briefly as future work, but a discussion of what information is lost and quantification of the gap relative to end-to-end approaches would strengthen the contribution.

- **Limited experimental domain diversity.** All three datasets are from Amazon Reviews (musical instruments, industrial/scientific, video games) with similar sparsity (~99.97%) and average sequence lengths (~8.5). It remains unclear whether PCTX's benefits extend to domains with different characteristics (e.g., music streaming with longer sequences, e-commerce with dense interactions, or news recommendation with temporal dynamics). Given the high similarity of the datasets, the "consistent improvements across three datasets" claim is weaker than it appears.

- **Incomplete ablation on Game dataset.** Table 3 reports ablation results only for Instrument and Scientific datasets, omitting Game. This is inconsistent with the main results (Table 2), which include all three datasets. The Game dataset shows the smallest improvements over baselines (3.67-4.26%), making it especially important to verify that the same component contributions hold there.

### Minor

- **Sensitivity analysis is incomplete.** Several key hyperparameters lack analysis: the fusion weight α (Equation 2), the frequency threshold τ for merging infrequent semantic IDs, and the augmentation probability γ. The paper mentions these are set as hyperparameters but provides limited guidance on their sensitivity. Figure 3 shows the distribution of personalized semantic IDs per item, but doesn't connect this to performance.

- **The "up to 8.9%" claim is somewhat selective.** Looking across all metrics and datasets, improvements range from 2.44% to 12.32%. On the Game dataset, improvements are 2.59-4.26%, which is more modest. While all are statistically significant, the headline figure applies only to NDCG@10 on Scientific.

- **Computational overhead not discussed.** PCTX adds several stages beyond standard GR: (1) pre-training an auxiliary contrastive model, (2) encoding all training sequences to get context representations, (3) running k-means++ clustering per item, (4) running RQ-VAE on augmented representations. For practical deployment, training time and memory comparisons would be valuable.

### Trivial
None.

## Nice-to-Haves

- Analysis of how the number of personalized semantic IDs per item relates to recommendation quality (e.g., do items with more IDs benefit more from personalization?)
- A comparison with simply adding a user embedding to the RQ-VAE quantization process as a lighter-weight personalization approach
- Discussion of whether PCTX's benefits increase with longer interaction histories or denser user profiles

## Novel Insights

The paper's central insight—that autoregressive GR models with static tokenizers implicitly impose a universal item similarity standard that is suboptimal for diverse user populations—is genuinely novel and important for the GR research direction. The observation that a contrastive learning objective (DuoRec) produces better context representations for tokenization than a next-item prediction objective (SASRec), despite the latter being a better recommender, is a valuable finding suggesting that the objectives for learning good representations for downstream tokenization differ from those for direct recommendation. This highlights a broader principle: the optimal representation model for a given task may not be the one that performs best on the standard benchmark for that domain.

## Suggestions

- Report ablation results on all three datasets for completeness
- Add a table comparing training/inference time of PCTX vs. TIGER vs. ActionPiece to quantify the overhead
- Consider exploring a simpler personalization baseline (e.g., adding user-conditioned bias to RQ-VAE) to better situate PCTX's contribution relative to the design complexity
- Provide hyperparameter sensitivity analysis for α, τ, and γ

## Score and Decision
The paper presents a well-motivated, technically sound, and thoroughly evaluated contribution to personalized generative recommendation. The core idea is novel, the experimental design is rigorous with comprehensive ablations and statistical significance testing, and the results are consistent. The main limitations—the two-stage pipeline, limited domain diversity, and incomplete ablation—prevent a higher score but do not undermine the contribution's validity.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>