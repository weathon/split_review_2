Now let me compose the final review.

## Summary

This paper proposes Pctx, a personalized context-aware tokenizer for generative recommendation (GR). Unlike existing static tokenization methods that map each item to a fixed semantic ID, Pctx conditions tokenization on the user's historical interactions, enabling the same item to receive different semantic IDs under different user contexts. The method uses a contrastively pre-trained sequence model (DuoRec) to encode user context, k-means++ to condense context representations into prototypes, RQ-VAE for quantization, and merging strategies to mitigate over-personalization. Experiments on three Amazon Review datasets show consistent improvements over non-personalized tokenization baselines, with up to 8.9% improvement in NDCG@10.

## Strengths

- **Well-motivated problem (Section 1, Figure 1).** The paper clearly articulates a genuine limitation of static tokenization in GR: because semantic IDs with shared prefixes receive similar probabilities under autoregressive generation, a fixed item-to-token mapping enforces a universal similarity standard across all users, ignoring diverse user interpretations.

- **Novel technical approach (Section 2.2).** The idea of tokenizing the same item into different semantic IDs conditioned on user context is genuinely new within GR. The pipeline — user context encoding via contrastively pre-trained DuoRec, k-means++ condensation, RQ-VAE quantization, and redundant ID merging — is well-structured, with each component addressing a specific design challenge (C1 and C2 from the introduction).

- **Well-designed ablations (Table 3, Section 3.3).** The ablation study systematically isolates the personalization mechanism. Critically, variant (3.4) "w/ Random Target" (γ=1) achieves worse performance than Pctx while maintaining the same token diversity level, confirming that the benefit comes from *meaningful* personalization rather than from simply increasing token diversity or data augmentation. Variant (3.3) (TIGER w/ Pctx IDs) further shows both data augmentation and multi-facet generation contribute.

- **Model ensemble control (Table 4).** The natural concern that Pctx simply combines strengths of DuoRec and TIGER is directly addressed by showing explicit ensembles (TIGER+SASRec, TIGER+DuoRec) underperform Pctx by a clear margin, confirming the gains are due to the personalized tokenization mechanism itself.

- **Interpretable case study (Figure 4).** The StarCraft II example concretely illustrates how the same item receives different semantic IDs under story-driven vs. RTS user contexts, making the tokenization mechanism tangible.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Inference-time personalization evidence gap (Section 2.3, Figure 4).** The paper argues that the GR model generates different semantic IDs for the same item under different user contexts during inference, but the primary direct evidence (Figure 4) shows the *tokenizer* differentiating contexts during training-data construction, not the GR model's generation behavior. The ablation removing multi-facet generation (variant 3.2) provides supporting indirect evidence, and the paper's reasoning is plausible, but there is no direct analysis showing, e.g., that given a test user with context A the model assigns higher probability to semantic ID variant X of a candidate item than to variant Y, while given context B the reverse holds. This does not invalidate the method, but the inference-time personalization claim is less directly demonstrated than the paper suggests.

- **No variance reporting in main results (Table 2).** All results in Table 2 are reported as point estimates without standard deviations or confidence intervals. The "*" notation indicates statistical significance via paired t-test (p<0.05), but the number of runs, variance across runs, and test procedure details are unspecified. Given that some absolute gains over ActionPiece are small (e.g., NDCG@10 on Game: 0.0508 vs. 0.0490, a difference of 0.0018), variance information is needed to assess the robustness of individual improvements. (The consistency of improvements across all metrics and datasets partially mitigates this concern.)

- **Limited dataset diversity (Table 1).** All three datasets (Instrument, Scientific, Game) are subsets of the Amazon Reviews corpus with near-identical characteristics: sparsity ~99.96%, average sequence length 8–9, and the same filtering criteria (≥5 interactions, max length 20). While using Amazon subsets is standard practice in this literature, testing on three slices of essentially the same distribution limits the generalizability claims. A dataset with different sparsity, longer sequences, or multi-behavior data (e.g., MovieLens) would strengthen the case that the personalization benefit is broadly applicable.

- **Unsupported explainability claim (Section 2.3).** The paper states that multi-facet semantic ID generation "reveals the likelihoods of different user interpretations, thereby enhancing the explainability of the recommendation process." However, no evaluation of explainability is presented — no user study, quantitative proxy, or systematic analysis. The explainability experiment mentioned briefly in the LLM usage statement (GPT-4o as a discriminator) is not described or connected to the main experiments. This claim should either be substantiated or reframed as a qualitative observation.

### Trivial

- **Slightly overstated claim about GR vs. conventional models (Section 3.2).** The paper states that "GR models generally achieve superior performance compared to item ID-based sequential approaches." While GR models (TIGER, LETTER, ActionPiece) are competitive and often at the top, conventional models like HSTU and SASRec are competitive on several metrics (e.g., HSTU achieves 0.0577 R@10 on Instrument vs. TIGER's 0.0564), making the generalization too broad.

## Nice-to-Haves

- An inference-time generation analysis showing the probability distribution the trained GR model assigns to different semantic ID variants of the same candidate item under contrasting user contexts would directly demonstrate the claimed behavior.
- Sensitivity analysis for key hyperparameters (α in Equation 2, frequency threshold τ, augmentation rate γ) would clarify the personalization-vs-generalization trade-off, especially since the method has several interacting components.

## Removed Points

The following points raised in the input review were filtered out per meta-reviewer guidelines:
- **Pipeline complexity concern** — Partially addressed by existing ablations (SASRec variant 1.1 shows benefit even with weaker context encoder).
- **Missing hyperparameter values in main text (τ, beam search parameters)** — These details appear in the appendix, which is stripped by the parser.
- **Thin GR baseline set** — 3 GR baselines (TIGER, LETTER, ActionPiece) plus 10 conventional SR baselines is standard coverage.
- **k-means++ being ad hoc** — Reference to Appendix B for centroid determination is standard; without seeing the appendix this criticism is speculative.
- **Table duplication** — Formatting nitpick.
- **Data augmentation diluting personalization** — Partially addressed by ablation (3.4) with γ=1.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add an inference-time analysis showing the probability distribution over semantic ID variants of a candidate item conditioned on different user contexts, to directly demonstrate that the GR model generates contextually appropriate IDs.
2. Report standard deviations or confidence intervals for main results (Table 2) over multiple seeds.
3. Either remove the unsupported explainability claim or provide a proper evaluation.
4. Consider including at least one dataset with different characteristics (longer sequences, different sparsity profile) to demonstrate generalizability beyond sparse Amazon subcategories.

## Score and Decision

**Score:** 8  
**Decision:** Accept

This is a solid paper with a genuine, well-motivated contribution. The problem of static tokenization in GR is clearly articulated, the personalized tokenization solution is novel within the domain, and the experimental evaluation is thorough, with particularly strong ablations that isolate the personalization mechanism from confounding factors (token diversity, data augmentation, model ensemble effects). The weaknesses identified are all minor and addressable — they do not threaten the paper's core claims. The paper would benefit from direct inference-time analysis and variance reporting, but the evidence provided is sufficient to support acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>