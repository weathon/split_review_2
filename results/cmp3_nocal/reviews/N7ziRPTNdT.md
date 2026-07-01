Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper provides a theoretical and empirical analysis of whether generative (decoder-based) or non-generative (encoder-based) methods are better suited for compositional generalization under a formal model of visual perception. The key theoretical contribution is Theorem 3.2, which shows that when the observation dimension greatly exceeds the latent dimension (dx ≥ dz³), the first and second derivatives of inverse generators g ∈ G_int can be arbitrary in ambient space—the characterizing structure only persists when projected onto the data manifold's tangent space (Eq. 3.4), which is unknown for OOD regions. This makes encoder-side constraints infeasible because they depend on unknown OOD manifold geometry, while decoder-side constraints for F_int are axis-aligned and manifold-independent. Empirically, on PUG datasets, generative methods leveraging search and replay improve OOD compositional generalization over non-generative methods.

## Strengths

- **Theorem 3.2 is a genuine and non-trivial theoretical result.** The theorem formally proves that under the realistic condition dx ≥ dz³, the Jacobian and Hessian of functions g ∈ G_int can take arbitrary values at a point in ambient space (up to a set of measure zero). The contrast with Lemma 3.1 (where dx = dz and the structure is present) sharpens the point. The observation that the structure persists only under tangent-space projection (Eq. 3.4) is the paper's deepest insight.

- **The conceptual framing is clear and productive.** The paper articulates why constraining a decoder to F_int is axis-aligned (Eq. 3.1, Fig. 3 left) while constraining an encoder to G_int requires knowledge of the data manifold's geometry, including OOD regions that are by definition unobserved. This distinction is communicated effectively and provides a formal foundation for a long-standing intuition.

- **The PUG-Object (n=0) result provides an informative boundary condition (Fig. 5C).** When concepts do not interact, non-generative methods achieve near-perfect OOD accuracy without any special intervention. This finding demonstrates the empirical regime where the paper's pessimistic conclusion applies, and it aligns cleanly with the theoretical discussion of the n=0 special case in Sec. 3.1.

- **The empirical evaluation is internally consistent and well-controlled.** The use of PUG datasets enables clean ID/OOD splits that are rare in vision research. The comparison spans multiple pretrained base encoders (DINOv1/v2, CLIP, SigLIP2, I-JEPA) and consistently shows that generative methods with search/replay improve OOD performance, while non-generative methods require large-scale pretraining to make progress.

## Weaknesses

### Fatal
None.

### Major

- **The title "Generation Is Required for Data-Efficient Perception" overclaims relative to the paper's demonstrated contribution.** What the paper actually shows is: (i) under the assumption that f ∈ F_int (additive models with polynomial interactions), *guaranteeing* compositional generalization via encoder-side constraints is infeasible because those constraints depend on unknown OOD manifold geometry; (ii) empirically, on PUG datasets (controlled scenes with 2 animals and a background), generative methods with search/replay outperform non-generative methods. "Data-efficient perception" encompasses far more than compositional generalization under the F_int assumption. The paper acknowledges this scope limitation in Sec. 7, but the title presents an unconditional necessity claim that the evidence does not support. "Generation is required" implies an in-principle barrier; the paper's actual contribution is a well-motivated *case* that generative approaches have a structural advantage for compositional generalization when visual data follows the F_int model.

### Minor

- **The paper's argument about architectural constraints is a reasoned inference, not a formal result derived from Theorem 3.2.** Theorem 3.2 directly addresses derivative-based constraints (regulations like Eq. 3.2). The extension to "architectural constraints" (Abstract, Sec. 3) relies on the logical argument that any method operating in ambient space without manifold knowledge cannot exploit the manifold-dependent structure of Eq. 3.4. This argument is reasonable and the paper consistently uses hedging language ("suggests"—see lines 9, 123, 143, 147). However, the abstract presents the conclusion as a direct implication of the theoretical results ("We then provide theoretical results *suggesting* that such inductive biases cannot be enforced on an encoder through practical means such as regularization or architectural constraints") without making the inferential gap explicit. A clearer separation between what is proven (derivative constraints) and what is inferred (architectural constraints face the same fundamental challenge) would better serve the paper.

- **No confidence intervals, error bars, or statistical significance tests are reported.** Figures 5 and 6 report point estimates only for each model across splits. Given that the paper draws strong comparative conclusions (generative vs. non-generative methods differ substantially), the absence of any variance information weakens the empirical evidence.

- **The empirical scope is limited to simple, controlled scenes.** PUG datasets have ~20K images with 10 backgrounds × 32 animals in simple compositions. The paper acknowledges this in Sec. 7, but the gap between the broad title/framing and the controlled experimental setting remains large. Whether the theoretical predictions transfer to more complex real-world scenes with richer concept interactions is an open question.

### Trivial
None.

## Nice-to-Haves

- **Test an encoder with an explicit regularizer targeting the manifold-projected structure of Eq. 3.4.** The paper argues this is infeasible because it requires knowing the OOD manifold geometry. On controlled data like PUG, one could approximate the tangent-space projection (e.g., using a pretrained generative model to provide manifold samples). Even an imperfect attempt would strengthen the empirical case that the constraint is infeasible rather than untried.

- **Include a failure analysis of search and replay.** The paper reports mean improvements, but search (gradient-based optimization in latent space) can converge to spurious local minima, and replay can amplify decoder imperfections. Understanding when these methods fail would increase trust in the results.

- **Compare the computational cost of search/replay against scaling non-generative methods.** The paper argues non-generative methods require large-scale data (expensive at collection time), but search requires iterative optimization at test time and replay requires generating and training on synthetic data. A concrete cost comparison would make the engineering trade-offs transparent.

## Removed Points

These points were flagged for removal from the input review. Treat them with caution.

- "The experimental comparison stacks the deck in favor of generative methods through asymmetric inductive biases" — **Removed.** The asymmetry is by design and follows from the theory: decoder-side constraints are feasible, encoder-side ones are not. Both methods use the same pretrained base encoders. The comparison tests the theory's prediction, not a biased setup.
- "The methods section (Sec. 4) describes standard techniques as if they are contributions" — **Removed.** The paper does not claim novelty for search (Eq. 4.3) or replay (Eq. 4.4). Sec. 4 frames them as "strategies for solving this inference problem," which is appropriate.
- Various section-by-section notes (pretrained encoders benefiting both methods, best-performing combination selection, PUG-Texture replay limitation) — **Removed** because they are either acknowledged in the paper, standard practice, or do not affect the paper's core claims.
- "No analysis of computational cost" — **Demoted to Nice-to-Have** (not a core weakness).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Retitle the paper** to accurately reflect the scope. Suggested alternatives: "On the Structural Advantage of Generative Models for Compositional Generalization" or "Why Encoder Constraints Fail for Compositional Generalization under F_int."
2. **Add confidence intervals or error bars** to Figs. 5 and 6, or clarify if the reported numbers are single-run results and explain why this is standard for the setting.
3. **Clearly distinguish** in the abstract and introduction what Theorem 3.2 proves (derivative-based constraints cannot characterize G_int when dx ≫ dz) versus what is a reasoned extrapolation (architectural constraints face the same challenge due to manifold dependence).
4. **Include the key discussion from Appendix A.2** (architectural inductive biases toward G_int) in the main text, or at minimum summarize the conclusions.

## Score and Decision

<score>6.5</score>
<decision>Accept</decision>