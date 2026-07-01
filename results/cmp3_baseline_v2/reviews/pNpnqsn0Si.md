## Summary

This paper introduces **Thoughtbubbles**, a transformer variant that learns to dynamically fork and prune residual streams during pretraining using only language modeling loss. The method allows tokens requiring more computation to spawn "bubbles" of cloned residuals for additional parallel processing in latent space, which are later merged via score-weighted averaging. Experiments across 150M-772M parameter scales on OpenWebText and peS2o show consistent perplexity improvements and gains on zero-shot benchmarks (LAMBADA, HellaSwag) over both parameter-matched and computation-matched baselines.

## Strengths

- **Novel and well-motivated approach to adaptive computation**: The idea of learning to dynamically fork/prune residual streams during pretraining without any supervision beyond LM loss is genuinely novel. The paper correctly identifies the limitation of existing pause-token methods (which require manual placement or test-time intervention) and addresses it directly.

- **Consistent empirical gains across scales and datasets**: The results in Table 1 show Thoughtbubbles outperforms both the standard transformer and the computation-matched "Copy" baselines on perplexity across all 6 model/dataset combinations, with gains of 1-2 perplexity points. The 319M model beating the 772M baseline on OpenWebText perplexity (20.23 vs 21.22) is a striking demonstration of the method's efficiency.

- **Interpretable computation allocation analysis**: Figure 5 provides compelling evidence that the model allocates more forks to tokens with moderate-to-high entropy, and Figure 4 shows that forked tokens receive substantially higher attention from their parent token. These analyses go beyond simple performance reporting and demonstrate the mechanism is working as intended.

- **Clean, principled design**: The score attenuation mechanism (Eq. 8-10) that forces the model to assign higher scores to important tokens by attenuating attention and residual updates is elegant. The top-k bottleneck with forced keep for the rightmost token (Eq. 4) is a sensible design choice to ensure stability.

## Weaknesses

### Major

- **The computation-matched baseline is weak and potentially misleading**: The "Copy-3" and "Copy-5" baselines simply duplicate the input residual multiple times before running the transformer and take the rightmost residual for decoding. This is a strawman baseline—it adds computation but provides no mechanism for the model to *use* that computation adaptively. A stronger baseline would be a model with more layers/parameters to match FLOPs, or a model that uses pause tokens at fixed positions. The paper claims Copy-5 is "roughly FLOPs-matched" against κ=4L, but this is not rigorously justified, and the Copy baselines perform poorly on LAMBADA (often worse than the standard baseline), suggesting they are not meaningful comparisons.

- **Limited evaluation on reasoning tasks**: The paper evaluates on LAMBADA, HellaSwag, BLiMP, and PIQA—all of which are relatively simple benchmarks where modern LMs saturate. The paper explicitly acknowledges (Section 8) that they cannot evaluate on harder reasoning datasets like GSM8k due to scale limitations, but this is a significant weakness for a paper claiming to enable "parallel thinking" and "adaptive computation for difficult multi-step problems." The core claim of the paper is about enabling better reasoning through adaptive computation, yet no reasoning benchmark is evaluated.

- **Autoregression gap is not fully resolved**: Figure 6 shows that naive fixed-budget autoregression causes a significant distribution shift and perplexity degradation. While the "dynamic" mitigation helps, the paper does not provide a principled solution or analysis of when/why the gap occurs. This is a practical concern for deployment.

- **Missing ablation studies**: The paper does not ablate key design choices: (1) the effect of the score attenuation mechanism (Eq. 8-10) vs. a simpler gating mechanism, (2) the impact of the number/location of forking layers, (3) the effect of the top-k budget κ on performance vs. compute trade-off, (4) whether the learned fork embeddings are necessary. Without these, it's unclear which components are essential.

### Minor

- **Training compute is not reported**: The paper compares parameter-matched and computation-matched models, but does not report the actual training FLOPs or wall-clock time. Since the forking mechanism adds overhead (scatter-max kernels, top-k operations), it's unclear if the gains come from additional compute or from better allocation of the same compute.

- **The entropy-computation relationship is partially contradictory**: The paper claims the model allocates more computation to high-uncertainty regions, but then notes it reduces computation at the *highest* uncertainty levels, forming a concave relationship. This is explained post-hoc but not predicted or controlled for, weakening the interpretability claim.

- **BLiMP results are inconsistent**: On BLiMP, the Copy baselines often outperform Thoughtbubbles, and the paper's explanation ("pruned dynamic parallel computation may not be as helpful for syntax") is speculative and not supported by analysis.

### Trivial

- The paper uses "pe2o" and "peS2o" inconsistently in the text and table.
- Figure 1 is difficult to parse and the caption is overly long.

## Nice-to-Haves

- Evaluate on a multi-step reasoning benchmark (e.g., GSM8k, MATH) at larger scales or with a distilled model to demonstrate the reasoning benefits.
- Compare against a pause-token baseline where tokens are inserted at fixed positions (e.g., every k layers) to isolate the benefit of *adaptive* placement.
- Provide an analysis of the computational cost (FLOPs and wall-clock time) of the forking mechanism vs. standard attention.

## Novel Insights

Beyond the paper's own contributions, the key insight is that *implicit* adaptive computation can be learned purely from the language modeling objective without any auxiliary loss or supervision. The score attenuation mechanism (Eq. 8-10) is a clever way to create a training signal for the forking decisions: by attenuating attention and residual updates by the cumulative scores, the model is forced to assign higher scores to tokens it needs to attend to and update. This is a form of "learning to compute" that emerges from the structure of the architecture rather than from explicit regularization. The finding that the model allocates more computation to moderate-entropy tokens (but not the highest-entropy ones) is also interesting and suggests that the model learns to distinguish between resolvable uncertainty (where more computation helps) and irreducible uncertainty (where it doesn't).

## Suggestions

1. Add a stronger computation-matched baseline: either a deeper transformer with more layers to match FLOPs, or a pause-token model with fixed token insertion. This would isolate the benefit of *adaptive* allocation vs. simply having more compute.

2. Report training FLOPs and wall-clock time for all models to clarify whether the gains come from better allocation or simply from using more compute during training.

3. Add ablation studies removing the score attenuation mechanism (replacing it with a simple gating or no modulation) to demonstrate its necessity.

4. Evaluate on at least one multi-step reasoning benchmark, even if at smaller scale or with a distilled setup, to support the claim of enabling "parallel thinking."

## Score and Decision

The paper presents a genuinely novel and well-executed approach to adaptive computation in transformers, with consistent empirical gains and interpretable behavior. However, the weak computation-matched baseline, lack of evaluation on reasoning tasks, and missing ablations temper the strength of the claims. The core idea is valuable and the empirical results are solid, but the paper would benefit from stronger baselines and broader evaluation before acceptance at a top venue.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>