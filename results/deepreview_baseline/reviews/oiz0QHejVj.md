## Summary
This paper proposes CLIP-Map, a mapping-based compression framework for CLIP models that replaces traditional select-based pruning with learnable transformation matrices. The method uses Kronecker factorization to map larger weight matrices to smaller ones with reduced parameter overhead, introduces Diagonal Inheritance Initialization to stabilize training, and employs a two-stage mapping-retraining pipeline with knowledge distillation. Experiments on zero-shot retrieval and classification benchmarks show improvements over TinyCLIP baselines, particularly under high compression ratios.

## Strengths
- **Novel approach to CLIP compression**: The paper introduces a mapping-based paradigm (inspired by model growth techniques) that avoids the hard parameter removal typical of pruning methods. This is a conceptually clean departure from select-based approaches and offers a fresh perspective on compression.
- **Effective technical contributions**: The Kronecker factorization strategy is well-motivated for reducing the parameter count of the mapping matrices from O(D₁²D₂²) to O(D₁D₂), and the Diagonal Inheritance Initialization is supported by a clear analysis of variance shifting issues in Kronecker-structured mappings. The initialization gives large practical gains (e.g., 28.9% vs. 4.9% on IN-1K in Tab. 5).
- **Strong experimental results under high compression**: At 1.0% and 10.0% compression ratios, CLIP-Map consistently and substantially outperforms TinyCLIP across retrieval and classification benchmarks (e.g., 15.8 vs 10.5 TR@1 on MSCOCO at 1.0%). The method also shows competitive performance at 50% compression with fewer training epochs.

## Weaknesses
### Fatal
None.

### Major
- **Unclear depth mapping details and validation**: The paper repeatedly claims that depth compression is performed via linear combination of layers (Eq. 2), but it is never explicitly demonstrated in the experiments. Table 3 reports results from a 1.0% compression ratio configuration that involves both width and depth reduction, but there is no ablation or direct comparison isolating the effect of the depth mapping component. Without such validation, it is unclear whether the depth mapping is actually contributing or if the gains come solely from width mapping and the improved initialization.
- **Insufficient comparison with non-CLIP baselines**: The experimental comparisons are almost entirely limited to TinyCLIP. While TinyCLIP is a strong baseline, the paper does not compare against other recent CLIP compression methods beyond what is shown in Table 3 (e.g., no comparison with CLIP-KD or other pruning+distillation methods on the same settings). The comparison with MobileCLIP in Table 3 is also questionable because MobileCLIP uses a qualitatively different training dataset (DataCompDR).

### Minor
- **Limited analysis of the mapping stage's role**: The paper shows that 5 epochs of mapping training outperforms 0 or 1 epoch, but it does not provide a clear analysis of *why* the mapping helps beyond weight inheritance. For example, does the mapping converge to a meaningful structure, or does it primarily serve as a learned initialization that retraining can refine? The visualization in A.7 is mentioned but not explained in the main text.
- **The two-stage pipeline adds engineering complexity**: While the paper argues for a simplified pipeline, it actually introduces a separate optimization stage (mapping) with its own hyperparameters. This is not necessarily simpler than progressive pruning pipelines; the claim of "less engineering complexity" is not substantiated.

### Trivial
- The table captions and figure references are somewhat repetitive (e.g., Figure 2 caption appears three times). This is likely a parser issue.
- The writing occasionally uses redundant phrases (e.g., "and then" appears multiple times in close succession).

## Nice-to-Haves
- An ablation study that compares full CLIP-Map against a version that only uses width mapping (no depth mapping) would clarify the contribution of each component.
- A comparison with other initialization strategies (e.g., using random noise on the diagonal, or scaling factors) could further justify the identity initialization choice.
- Reporting the wall-clock training time for the mapping stage would strengthen the efficiency claims.

## Novel Insights
The paper's key conceptual insight is that compression can be framed as a learnable mapping optimization problem, analogous to model growth but in reverse. The observation that Kronecker factorization introduces multiplicative variance, motivating a diagonal initialization, is a technically sound and practically useful analysis. The finding that a moderate number of mapping steps (5 epochs) yields the best performance, while too many steps degrade results, suggests that the mapping serves as a structured warm-start rather than a full optimization of the compressed weights. This distinction—mapping as initialization versus mapping as compression—is an interesting nuance that could inform future work on learnable compression paradigms.

## Suggestions
1. Provide explicit experimental results isolating the depth mapping component, either through an ablation (width-only vs. width+depth) or by showing the depth mapping learned weights for a concrete case.
2. Add comparisons with additional CLIP compression baselines (such as CLIP-KD or UPop) using the same training data to strengthen the evaluation.
3. Include a brief discussion of what the learned mapping matrices look like after training (e.g., do they remain near-diagonal, or do they develop rich off-diagonal structure?) to help readers understand what the mapping stage actually learns.

## Score and Decision
The paper presents a novel and well-motivated approach to CLIP compression with effective technical components and strong empirical results under high compression. The main weakness is the incomplete validation of the depth mapping component and the narrow baseline comparison. These are addressable in revision but do not invalidate the core contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>