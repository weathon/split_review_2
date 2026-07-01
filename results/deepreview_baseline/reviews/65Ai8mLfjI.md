## Summary

This paper investigates the role of pooled text embeddings (global text conditioning) in diffusion transformers. The authors first demonstrate that in many modern models (FLUX, HiDream, COSMOS), the pooled CLIP embedding has negligible impact on generation quality when used conventionally. However, they propose "modulation guidance"—a training-free technique that amplifies the pooled embedding's effect by extrapolating between positive and negative prompt embeddings in the modulation space. This approach improves aesthetics, complexity, object counting, and hand correction across multiple text-to-image and text-to-video models with negligible computational overhead.

## Strengths

- **Clear and well-motivated research question**: The paper directly addresses a timely architectural design choice (whether to include pooled text embeddings) that has been made inconsistently across recent diffusion transformers, and provides systematic analysis to understand its role.
- **Practical and simple method**: Modulation guidance requires no training, no fine-tuning, and minimal computational overhead (only two additional forward passes of the CLIP encoder per generation). The dynamic variant (applying guidance only to later layers) is elegantly simple and empirically effective.
- **Comprehensive evaluation across diverse tasks and models**: The method is validated on 5 text-to-image models (FLUX schnell, FLUX dev, SD3.5 Large, HiDream, COSMOS), 2 text-to-video models (Hunyuan, CausVid), and an image editing model (FLUX Kontext), with both human evaluation and automatic metrics. The inclusion of models that originally lack CLIP (COSMOS, CausVid) with a lightweight fine-tuning procedure strengthens the generality claim.
- **Insightful analysis of what modulation guidance does**: Figure 4 provides a compelling mechanistic explanation—modulation guidance shifts attention toward relevant tokens (e.g., "hands"), which is a concrete and interpretable effect.

## Weaknesses

### Major

- **Limited novelty relative to prior work**: The core idea of extrapolating between positive and negative conditions in feature space is well-established in classifier-free guidance (CFG) and its variants. The specific application to modulation layers is novel, but the technical contribution is incremental—essentially applying CFG-style extrapolation to the pooled embedding vector rather than to the noise prediction. The paper's own related work section acknowledges attention guidance methods that do similar extrapolation in attention space. The distinction ("applies through a small MLP rather than through attention") is thin.

- **The "training-free" claim for CLIP-free models is misleading**: For models like COSMOS and CausVid that lack pooled text embeddings, the paper requires fine-tuning (4K iterations for COSMOS, 1K for CausVid) to introduce a small MLP. While this is lightweight, it is not training-free. The paper should clearly separate the two regimes: (1) models with existing CLIP embeddings (truly training-free) and (2) models without CLIP embeddings (requires fine-tuning).

- **Human evaluation methodology is underspecified**: The paper reports side-by-side win rates but provides minimal detail about the evaluation protocol. How many annotators? What instructions were they given? Were they shown images in randomized order? Was there any quality control or inter-annotator agreement metric? The claim of "statistically significant" improvement (green in Table 2) is not backed by confidence intervals or p-values in the main text. Given that human evaluation is a key evidence pillar, this lack of detail is concerning.

- **The "dynamic modulation guidance" is not convincingly dynamic**: The proposed strategy (Figure 3b) is simply a step function that applies guidance only to later layers. This is a static per-layer schedule, not a dynamic adjustment that depends on the current generation state. The paper acknowledges this ("We consider the simplest variant") and defers more complex strategies to the appendix, but the term "dynamic" is misleading.

### Minor

- **The analysis of CLIP's inactivity (Section 4) is somewhat superficial**: The paper shows that removing CLIP has little effect on metrics, but does not explore *why* this happens. Is it because the model learns to ignore the pooled embedding during training? Is it because T5 already captures the same information? Is it an architectural issue (e.g., the MLP that processes the pooled embedding has limited capacity)? Understanding the root cause would strengthen the paper's contribution.

- **The comparison with baselines is limited**: Only two baselines are compared (Normalized Attention Guidance and Concept Sliders), and the comparison is only on a subset of tasks. The paper does not compare against other test-time optimization methods (e.g., Attend-and-Excite, layout guidance) or against simply using a more descriptive prompt (which is the simplest baseline for improving aesthetics/complexity).

- **The paper does not discuss failure cases or limitations in sufficient depth**: Appendix H is mentioned but not included in the main text. The paper would benefit from a brief discussion of when modulation guidance might hurt (e.g., prompts that are already very specific, or cases where the positive/negative prompt design is ambiguous).

### Trivial

- The paper uses "modulation guidance" to refer to the technique, but this term could be confused with other guidance methods in the literature. A more distinctive name might help.

## Nice-to-Haves

- An analysis of how the choice of positive/negative prompts affects results would be valuable. The paper provides the prompts used (Appendix D) but does not analyze sensitivity to prompt wording.
- A comparison with simply increasing CFG scale (which also pushes the model toward the prompt) would help clarify the unique benefits of modulation guidance.
- The paper could explore whether modulation guidance can be combined with other test-time optimization methods (e.g., attention guidance) for additive gains.

## Novel Insights

The paper's key insight is that the pooled text embedding, while seemingly redundant when attention already provides text conditioning, can serve a different function: it provides a compact, interpretable handle on the modulation space that enables controlled shifts toward desirable properties. This reframing—from "how to condition on text" to "how to steer generation quality"—is the paper's most novel contribution. The finding that this steering works by shifting attention toward relevant tokens (Figure 4) provides a mechanistic understanding that goes beyond the typical "it works" empirical demonstration. However, the insight that extrapolation in feature space can improve generation quality is not fundamentally new; the novelty lies in identifying the modulation space as a particularly effective and efficient locus for this extrapolation.

## Suggestions

1. Clarify the human evaluation methodology: number of annotators, instructions, randomization, and statistical significance testing.
2. Rename "dynamic modulation guidance" to "layer-wise modulation guidance" or "staged modulation guidance" to avoid misleading connotations.
3. Add a brief discussion of when modulation guidance might fail or degrade performance, and how practitioners can detect such cases.
4. For the CLIP-free model experiments, clearly separate the fine-tuning cost from the inference-time cost, and discuss whether the fine-tuning generalizes across prompts or needs to be redone for new domains.

## Score and Decision

The paper addresses a relevant and timely question, proposes a simple and practical method, and provides reasonably comprehensive empirical validation. However, the technical novelty is incremental (applying CFG-style extrapolation to modulation layers), the "training-free" claim is partially misleading, and the human evaluation methodology lacks sufficient detail. The paper is solid and useful but does not rise to the level of a top-tier contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>