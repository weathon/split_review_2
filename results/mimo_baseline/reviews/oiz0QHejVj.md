## Summary
The paper proposes CLIP-Map, a mapping-based compression framework for CLIP that replaces traditional select-based pruning with learnable Kronecker-factorized transformation matrices (F^in, F^out) and depth-compression operators. The method uses a two-stage pipeline: (1) a mapping stage with diagonal inheritance initialization to produce a well-initialized compressed model, followed by (2) a retraining stage with knowledge distillation. Experiments across retrieval and zero-shot classification benchmarks show competitive or superior performance to TinyCLIP, with particularly significant gains at extreme compression ratios (1%).

## Strengths
- **Strong results at extreme compression**: At 1% compression, CLIP-Map significantly outperforms TinyCLIP on MSCOCO TR@1 (15.8 vs 10.5, a ~50% relative gain) and Flickr30K TR@1 (31.7 vs 25.1), directly validating the paper's core claim that mapping preserves more information than selection under aggressive compression.
- **Well-designed ablations**: The ablation on initialization methods (Table 5) convincingly shows that random/Kaiming/Xavier initialization nearly fails while diagonal initialization achieves 28.9% ImageNet accuracy, providing strong evidence for the distribution shifting analysis and the proposed solution. The mapping/retraining duration study (Table 4) clearly identifies the sweet spot at 5 mapping epochs.
- **Training efficiency**: Table 3 demonstrates that CLIP-Map achieves comparable ImageNet-1K accuracy to TinyCLIP (63.7 vs 63.5) while seeing only 0.30B samples versus 0.75B, and achieving 42.7% with just 0.45B samples where TinyCLIP achieves 41.1% with 1.125B samples.
- **Comprehensive evaluation**: The paper evaluates on 21 zero-shot classification datasets, two retrieval benchmarks (MSCOCO, Flickr30K), multiple compression ratios (1%, 10%, 50%), and generalizes beyond ViT-B/16 to Meta-CLIP and ResNet-based CLIP, demonstrating breadth.

## Weaknesses
### Fatal
None.

### Major
- **Limited methodological novelty**: The core technical components—Kronecker factorization for weight matrices and linear combination of layers for depth—are directly borrowed from LiGO (Wang et al., 2023a) and LeTs (Xia et al., 2024), merely reversing the direction from growth to compression. The paper's main contribution is this conceptual inversion plus diagonal initialization, which is a reasonable but incremental combination of known techniques rather than a fundamentally new approach.
- **Gains are marginal at moderate compression**: At 50% compression (Table 1), CLIP-Map and TinyCLIP are essentially tied: MSCOCO TR@1 is 55.1 vs 54.9, IR@1 is actually worse (37.9 vs 38.9), and Flickr30K IR@1 is slightly better (67.6 vs 66.7). The paper's framing suggests broad superiority, but the benefits are concentrated at extreme ratios. This should be discussed more explicitly.
- **Only one primary baseline (TinyCLIP)**: The paper repeatedly compares against TinyCLIP as the sole select-based baseline. Table 3 includes MoPE-CLIP and MobileCLIP, but these use different model sizes (MoPE-CLIP: 86+42M vs CLIP-Map: 39+19M), making effectiveness comparisons unfair. More structured pruning baselines (e.g., SparseGPT-style methods adapted for CLIP, or other recent CLIP pruning works) would strengthen the comparison.

### Minor
- **Mixed results in zero-shot classification**: In Table 2, CLIP-Map underperforms TinyCLIP on several datasets (e.g., VOC2007, Flowers102, Country211, GIROB in the ViT-8M configuration). The paper does not discuss these failure cases or characterize when select-based methods may still be preferable.
- **No analysis of learned mapping structure**: The paper claims mapping preserves pretrained information but never analyzes what the learned F^in and F^out matrices actually look like after training. Are they approximately low-rank? Sparse? Understanding this would deepen the contribution significantly.
- **ResNet experiments lack retraining stage**: When using ResNet-50 as the vision encoder, only the mapping stage (5 epochs) is used without retraining. This makes the comparison incomplete and the reported numbers (25.5 TR@1 on MSCOCO) are weak, potentially undermining the claim of generalizability.

### Trivial
- The distinction between "mapping-retraining" and "pruning-retraining" pipelines could be emphasized more—both are two-stage methods, and the paper could clarify what structural advantage the mapping stage offers beyond better initialization.

## Nice-to-Haves
- A visualization or quantitative analysis (e.g., CKA, representation similarity) of what information the mapping preserves versus what pruning discards.
- Downstream fine-tuning evaluation (not just zero-shot) to assess whether the compressed models transfer as well as pruned ones.
- Wall-clock time and FLOP comparisons for training and inference.

## Novel Insights
The paper's key insight—that model compression can be formulated as the inverse of model growth, using learnable mappings rather than hard parameter selection—is conceptually interesting and practically useful. The observation that standard initialization for Kronecker factors causes multiplicative variance scaling (Eq. 7-8), which necessitates the diagonal inheritance scheme, is a useful practical finding for anyone applying Kronecker-based parameter transformations. However, the individual techniques are well-established, and the synthesis, while sound, does not produce a deeply surprising or paradigm-shifting observation.

## Suggestions
- Add a structured comparison with at least one additional pruning baseline beyond TinyCLIP under identical settings.
- Analyze the learned mapping matrices (rank, sparsity, structure) to provide insight into what the mapping is actually doing.
- Discuss failure cases in zero-shot classification where CLIP-Map underperforms TinyCLIP and hypothesize why.
- Include a table or section explicitly decomposing the contribution: how much does Kronecker factorization help vs. diagonal initialization vs. the mapping-retraining pipeline?

## Score Assessment
The paper makes a useful practical contribution for extreme CLIP compression with a reasonable (if incremental) technical approach. The experimental results are thorough and the gains at 1% compression are significant. However, the methodological novelty is limited—primarily reversing the direction of known model growth techniques—and the benefits are concentrated at extreme compression ratios while being marginal at moderate ones. This places the paper at the borderline, leaning slightly toward reject due to the incremental nature of the technical contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: Reject