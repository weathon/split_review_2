## Summary

This paper proposes ScaPre, a closed-form framework for large-scale concept unlearning in text-to-image diffusion models. It introduces a conflict-aware stable design (spectral trace regularizer + geometry alignment via Bures distance) to handle conflicting updates when unlearning many concepts, and an Informax Decoupler that uses mutual information to confine updates to concept-relevant parameters. The method is training-free, efficient (120 seconds for 50 concepts), and achieves strong unlearning performance while maintaining generation quality across object, style, and explicit content benchmarks.

## Strengths

- **Novel and principled framework for large-scale unlearning.** The combination of spectral trace regularization (to suppress conflicting directions) and Bures distance geometry alignment (to preserve global covariance structure) is a well-motivated approach to stabilize optimization when unlearning many concepts simultaneously. The Informax Decoupler provides a principled, information-theoretic way to focus updates on concept-relevant parameters without requiring additional data or auxiliary modules.

- **Comprehensive and convincing experimental evaluation.** The paper evaluates on multiple benchmarks (Imagenette, ImageNet-Diversi50 with 50 concepts, ImageNet-Confuse5 for precision, artistic styles, and explicit content) against a wide range of baselines (FMN, SPM, ESD, MACE, UCE, RECE, SP). ScaPre consistently achieves the best or near-best trade-off between unlearning effectiveness and generation quality, as measured by the proposed UQ metric, CLIP scores, and FID.

- **Efficiency and scalability.** The closed-form solution avoids iterative fine-tuning, completing unlearning of 50 concepts in 120 seconds with only 5 GB peak memory. This is a significant practical advantage over training-based methods (e.g., SPM, ESD) that require hours and substantially more memory, while also outperforming other closed-form methods (UCE, RECE) that suffer from generative collapse at scale.

- **Addresses a timely and important problem.** Machine unlearning in generative models is of high practical relevance for copyright, privacy, and content moderation. The paper directly tackles the underexplored challenge of scaling unlearning to large concept sets, which existing methods fail to handle reliably.

## Weaknesses

### Fatal

None.

### Major

- **Ablation study is not presented in the main paper.** The paper claims ablation studies are in Appendix C.5–C.7, but the main text would benefit from a clear table isolating the contribution of each component (spectral trace regularizer, geometry alignment, Informax Decoupler). Without this, it is difficult to assess whether all components are necessary or if simpler alternatives could achieve similar results.

- **The Informax Decoupler details are underspecified.** The mutual information estimation requires discretizing activations with a threshold τ_i and a sample size K. The paper does not specify how many samples (prompts/images) are used, how τ_i is set, or how sensitive the method is to these choices. This affects reproducibility and the understanding of the method's practical requirements.

### Minor

- **The claim of "×5 more concepts" is not precisely defined.** The paper states ScaPre "can forget up to ×5 more concepts than the best baseline within the limits of acceptable generative quality," but does not specify the threshold for "acceptable generative quality" or how the factor is computed. While the scalability curves (Figure 4) support the general trend, a precise definition would strengthen the claim.

- **The UQ metric, while useful for summarizing trade-offs, is a composite that may obscure individual weaknesses.** The paper already reports separate metrics (unlearn accuracy, CLIP score, FID), so this is not a serious issue, but the reliance on a new metric without broader community adoption is a minor concern.

### Trivial

None.

## Nice-to-Haves

- Include an ablation table in the main paper (e.g., removing spectral trace regularizer, replacing Bures distance with ℓ₂, removing Informax Decoupler) to clearly demonstrate the necessity of each design choice.
- Provide a sensitivity analysis for key hyperparameters: number of samples K for MI estimation, threshold τ_i, and the geometry alignment coefficient β.
- Discuss limitations: the method currently edits only cross-attention layers; whether it can be extended to other components (e.g., self-attention, MLP) and whether the closed-form solution scales to very large models (e.g., SDXL) would be useful context.

## Novel Insights

The paper's core insight is that large-scale unlearning can be cast as a closed-form optimization problem with carefully designed regularizers that stabilize the optimization space and decouple concept-relevant parameters. The use of spectral trace regularization to penalize directions where multiple concepts overlap (via SVD-based gating) and Bures distance to align covariance structures rather than raw weights is a novel and theoretically grounded approach. The Informax Decoupler provides a principled way to focus updates on relevant parameters using mutual information, avoiding the need for additional data or masks. This combination enables scalable, precise, and efficient unlearning in a single closed-form step.

## Suggestions

- Add an ablation table in the main paper (e.g., Table 1 or a new table) showing the effect of removing each component on unlearn accuracy, CLIP score, and UQ on Imagenette or ImageNet-Diversi50.
- Clarify the sample size K used for mutual information estimation and discuss how it was chosen. Provide guidance on setting the threshold τ_i (e.g., using a percentile of activations).
- Define the "×5 more concepts" claim with a concrete threshold (e.g., UQ > 50 or CLIP score > 29) and show the number of concepts each method can unlearn while meeting that threshold.

## Score and Decision

**Score:** 8

**Decision:** Accept

The paper makes a significant contribution to machine unlearning for diffusion models by proposing a novel, principled, and efficient closed-form framework that demonstrably scales to large concept sets while maintaining precision. The experimental evaluation is thorough and the results are strong. The weaknesses are minor and can be addressed with additional clarifications and ablation results.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>