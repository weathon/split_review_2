## Summary

This paper proposes ScaPre, a closed-form framework for scalable and precise concept unlearning in text-to-image diffusion models. The method combines a conflict-aware stable design (spectral trace regularizer + Bures distance geometry alignment) with an Informax Decoupler that uses mutual information to identify concept-relevant parameters, yielding a Sylvester equation-based closed-form solution that requires no additional data or auxiliary modules. Experiments across object, style, and explicit content benchmarks demonstrate that ScaPre can unlearn up to 50 concepts in 120 seconds while outperforming baselines in both unlearning effectiveness and generation quality preservation.

## Strengths

- **Well-motivated problem decomposition.** The paper clearly identifies three concrete challenges in large-scale unlearning (conflicting updates, imprecise unlearning, scalability bottlenecks) and addresses each with a dedicated component. This makes the design choices traceable and the method easy to follow.

- **Strong empirical results across diverse benchmarks.** ScaPre achieves 0.8% unlearning accuracy on Imagenette (vs. 4.9% for RECE), 3.9% on ImageNet-Diversi50, and 84.3% overall accuracy on the precision-focused ImageNet-Confuse5 benchmark (vs. 50.3% for the next best). The precision experiment is particularly compelling: while UCE and RECE achieve near-zero unlearn accuracy, they also destroy similar non-target concepts (preserve accuracy ~5.5%), whereas ScaPre retains 76.3% preserve accuracy.

- **Efficiency and practicality.** The closed-form solution eliminates iterative fine-tuning, completing 50-concept unlearning in 120 seconds with ~5 GB peak memory. This is a meaningful practical advantage over training-based methods like MACE (~2.5 hours) and SPM (~4.5 hours).

- **Comprehensive evaluation design.** The paper introduces ImageNet-Confuse5 for evaluating disentanglement of visually similar concepts and proposes the UQ metric jointly capturing unlearning and quality. The scalability analysis (Figure 4) clearly shows ScaPre maintaining performance as concept count increases while baselines degrade.

## Weaknesses

### Fatal
None.

### Major

- **UQ metric design and self-referential evaluation.** The paper introduces the UQ metric using sigmoid normalization of accuracy and CLIP scores, then uses it as the primary comparison metric across all tables. The sigmoid normalization with per-method mean/std statistics is somewhat ad-hoc and could be sensitive to the distribution of included methods (e.g., adding or removing a very poor method changes all scores). While combining unlearning and quality into one metric is useful, the paper should justify this specific formulation more carefully and show sensitivity to the normalization choices.

- **Informax Decoupler implementation details are underspecified.** The MI computation requires discretized activations with an "adaptive threshold" τ_i, target-concept inputs, and neutral inputs. The main paper does not specify how τ_i is chosen, how many samples K are used, or how "neutral inputs" are selected. These details significantly affect the reliability and reproducibility of the decoupler, and deferring them entirely to the appendix weakens the main contribution.

### Minor

- **The "×5 more concepts" claim is imprecise.** The paper states ScaPre can "forget up to ×5 more concepts than the best baseline within acceptable generative quality." This claim appears to be based on the scalability curves in Figure 4, but the threshold for "acceptable generative quality" is not defined. A more rigorous characterization (e.g., at a fixed CLIP score threshold) would strengthen this claim.

- **Heuristic design choices in R construction.** The sigmoid gating function applied to singular values (σ̃_i = (1 - sigmoid(σ_i))σ_i) for suppressing high-conflict directions is motivated intuitively but lacks theoretical justification for why sigmoid is the appropriate choice over other monotone decay functions.

- **Baseline fairness on Diversi50.** UCE and RECE achieve 0.0% accuracy on Diversi50 but with catastrophic quality collapse (CLIP ~22). These methods were not designed for 50-concept unlearning, so the comparison, while valid for demonstrating the scalability gap, somewhat overstates the relative advantage in the regime where all methods are meant to work.

### Trivial
None.

## Nice-to-Haves

- A discussion of failure cases or conditions under which ScaPre might struggle (e.g., highly entangled concepts in the text encoder's embedding space).
- Analysis of how the choice of substitute embeddings V* affects unlearning quality, since the paper mentions "often set to zero" without exploring alternatives.
- Comparison with SEMU (Sendera et al., 2025), which is mentioned in related work but not included in experiments.

## Novel Insights

The paper's most interesting observation is that large-scale concept unlearning requires stabilizing the optimization landscape *before* performing weight edits, rather than treating stability as a post-hoc regularization. The spectral trace regularizer's decomposition into a dynamic structure term S (capturing current concept statistics) and an interaction regulation term R (suppressing overlapping concept directions) provides a principled way to handle the growing complexity of multi-concept conflicts. The use of Bures distance for geometry alignment—preserving covariance structure rather than element-wise weights—is a meaningful departure from standard Frobenius regularization and offers a more principled way to maintain the pretrained model's global structure.

## Suggestions

- Provide a clearer specification of the Informax Decoupler's practical implementation in the main text, including threshold selection, sample requirements, and the choice of neutral inputs.
- Add sensitivity analysis for the UQ metric: show how rankings change under alternative normalization or weighting schemes.
- Include a failure mode analysis showing examples where ScaPre's precision degrades, to help practitioners understand its boundaries.

## Score and Decision

The paper presents a well-structured framework that addresses a genuinely important scalability bottleneck in concept unlearning. The method is technically sound, the closed-form solution is elegant, and the experimental evidence is comprehensive and convincing. The main weaknesses—the somewhat ad-hoc UQ metric and underspecified implementation details of the Informax Decoupler—are notable but do not invalidate the core contributions. The practical impact of enabling 50-concept unlearning in 120 seconds with strong quality preservation is significant for the community.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept