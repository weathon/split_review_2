## Summary

This paper proposes CLIP-Map, a compression framework for CLIP models that replaces conventional select-based pruning (weight selection) with learnable mapping matrices that linearly transform original weights into smaller counterparts. The method uses Kronecker factorization for parameter-efficient mapping (reducing complexity from O(D₁²D₂²) to O(D₁D₂)), a diagonal inheritance initialization for stable training, and a knowledge-distillation retraining stage. Results show meaningful gains over the TinyCLIP baseline at high compression ratios (1.0% and 10.0%) on MSCOCO and Flickr30K retrieval benchmarks.

## Strengths

1. **Conceptual novelty is real.** The core idea — replacing hard parameter selection (pruning) with a learnable mapping that combines pretrained weights — is a genuinely different approach from the dominant pruning-retraining paradigm for CLIP compression. The paper correctly identifies that pruning discards information irrecoverably and that a differentiable mapping can better preserve it. This is not an incremental variation on prior work.

2. **High-compression results are measurably stronger.** At 1.0% compression (Tab. 1), CLIP-Map achieves MSCOCO TR@1 of 15.8 vs TinyCLIP's 10.5 (non-progressive) or 12.5 (progressive, 3× the training budget). At 10.0%, the advantage is 38.4 vs 33.8 (non-progressive) or 36.2 (progressive). These margins hold across both MSCOCO and Flickr30K recall metrics. The 50.0% case is essentially a tie, consistent with the intuition that mapping helps most when compression is aggressive enough that naive selection causes real damage.

3. **The variance analysis motivating Diagonal Inheritance Initialization (Sec. 3.2.3) is mathematically clear.** The observation that independently initialized Kronecker factors produce multiplicative variance (Eq. 5–8) is correct, and the proposed diagonal initialization (Eq. 9) is a simple, principled fix. The ablation in Tab. 5 shows that without it, the mapping stage essentially fails (0.1% IN-1K with random init vs 28.9% with diagonal init).

## Weaknesses

### Major

1. **The mapping-stage loss function is never specified in the main paper.** Section 3.2.1 states that "we freeze original large CLIP model and train the mapping parameters," and Sections 3.2.2–3.2.3 describe the architecture and initialization of the mapping matrices. But the objective actually optimized during Stage 1 — the heart of the paper's claimed contribution — is never defined. Is it a reconstruction loss between original and compressed model representations? A contrastive loss on the compressed model's outputs? A distillation loss from the frozen teacher? The retraining stage loss is specified (Eq. 11–13), but the mapping stage loss is not. The paper defers to "detailed training settings are presented in A.5," but the core training objective for the paper's primary novelty should be stated in the main method section, not buried in an appendix. Without it, the method cannot be fully understood or reproduced.

2. **The critical ablation for Diagonal Inheritance (Tab. 5) only evaluates performance *before* retraining.** Tab. 5 shows that after the mapping stage alone, diagonal init achieves 28.9% IN-1K while Kaiming init achieves 4.4% and random init 0.1%. These gaps are enormous. But the paper never shows whether these gaps persist after the full retraining stage (Stage 2). If retraining largely erases the initialization differences — which is plausible given that both pipelines use the same teacher-student distillation — then the diagonal initialization is merely a convenience for mapping-stage convergence, not a driver of final compression results. If the gaps persist, that would be important evidence for the method's value. Either finding is publishable, but the paper currently provides neither, making it impossible to assess what the Diagonal Inheritance actually contributes to final performance.

### Minor

3. **No statistical significance or variance is reported.** Every result table reports a single number per metric per configuration. Given that differences at 50.0% compression are tiny (55.1 vs 54.9 TR@1 on MSCOCO), it is impossible to know whether even the larger gaps at 1.0% and 10.0% are meaningful or within noise. While single-run reporting is common in this area, the paper's strongest claims would benefit substantially from at least 2–3 runs with variance.

4. **Depth compression (L_depth) is under-explained.** Eq. 2 defines L_depth as a linear combination matrix that compresses L₁ layers into L₂ layers, and the pipeline claims to learn both width and depth mappings "simultaneously" (line 120). However, it is never made clear how L_depth is parameterized, initialized, or trained — whether it is jointly optimized with the Kronecker factors or separately — nor whether depth compression interacts with the width-mapping stage. This is a non-trivial component of the claimed unified pipeline that receives almost no methodological description.

5. **Performance degradation at longer mapping duration is observed but not analyzed.** Tab. 4 shows that 7 mapping epochs + 18 retraining epochs performs worse than 5 + 20 across all metrics, and the paper speculates about "unnecessary computational overhead" without analyzing the cause (e.g., overfitting to the mapping objective). A brief diagnostic would strengthen the paper.

6. **The paper's "mapping vs. selection" framing somewhat overstates the distinction.** The paper consistently contrasts "mapping-based compression" with "select-based compression," but both methods feed into the same knowledge-distillation retraining framework. The mapping determines only the initialization of the student model; the actual compression (size reduction) is achieved simply by choosing smaller dimensions. Acknowledging that the mapping is fundamentally a better *initialization scheme* for the compressed model — which the paper does in passing (line 27) — would not weaken the contribution and would make the framing more precise.

7. **Meta-CLIP-based variant underperforms OpenCLIP-based variant** (Tab. 1, 10.0%: 34.3 vs 38.4 TR@1), suggesting the method's advantage may depend on the pretrained checkpoint. The paper does not discuss this.

### Trivial

None.

## Nice-to-Haves

- **FLOPs or inference throughput comparison.** The paper reports only parameter counts. A model with fewer parameters can still be computationally expensive if its structure is not efficiently arranged (e.g., the Kronecker mapping introduces extra matrix multiplies at initialization). Reporting FLOPs or latency would substantially strengthen the practical claims.
- **Analysis of learned mapping matrices.** The paper mentions that the mapping evolves "toward a more uniform structure" (line 335) but provides no quantitative analysis of what the learned mappings actually encode (e.g., do they learn soft selection? Do they combine weights across input/output dimensions in interpretable ways?).
- **Post-retraining ablation of initialization methods** (related to Major Weakness #2). Running Tab. 5 through to completion would be the single highest-leverage addition.
- **Specifying the mapping-stage loss** (related to Major Weakness #1). This is not optional.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Criticism that Eq. 12's InfoNCE formulation is "unusual."** Removed because it is factually incorrect. Standard InfoNCE for CLIP is routinely implemented as cross-entropy over the similarity matrix with labels indexing correct pairings, which is exactly what Eq. 12 represents.
- **Criticism about non-square matrices or D₂ > D₁ scenarios (Sec 3.2.2).** Removed as scope creep. The paper is about compression where D₂ < D₁ by definition, and CLIP transformer weight matrices are square.
- **Criticism that comparing CLIP-Map to MoPE-CLIP in Tab. 3 is misleading.** Removed per the rule that comparisons asymmetrically favoring the author's method (fewer parameters, higher accuracy) are not grounds for criticism.
- **Criticism about off-diagonal "zero or small random values" ambiguity (line 200).** Removed; Eq. 9 clearly sets off-diagonals to 0, and the text mentioning "small random values" is a permissible variation that does not obscure the method.
- **Miscellaneous formatting nitpicks and speculation about appendix content.** Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify the mapping-stage loss function explicitly in Section 3.2.** This is the single most important fix. Without it, the method is underspecified and cannot be reproduced.
2. **Complete the initialization ablation (Tab. 5) by running all initialization methods through the full retraining stage.** Report both pre-retraining and post-retraining performance to establish whether Diagonal Inheritance is responsible for final results or only helps mapping-stage convergence.
3. **Add variance estimates** for at least the key comparisons in Tab. 1 (1.0% and 10.0% compression ratios) by reporting results over 2–3 random seeds.
4. **Provide a brief description of how L_depth is parameterized, initialized, and trained** — is it jointly optimized with the Kronecker factors? What is its initialization strategy?

## Score and Decision

The paper introduces a genuinely novel approach to CLIP compression with promising results at high compression ratios. However, as submitted, it has two significant gaps: the mapping-stage loss function is unspecified in the main paper (making the primary contribution underspecified), and the central ablation for the diagonal initialization is evaluated only before retraining, leaving unclear whether the initialization is actually responsible for the final results. These are fixable problems — the core idea is sound — but the paper in its current form cannot be fully evaluated or reproduced.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>