## Summary

This paper introduces INFO-SEDD, a method for estimating information-theoretic quantities (KL divergence, mutual information, entropy) for high-dimensional discrete data using discrete diffusion models based on Continuous Time Markov Chains (CTMCs). The key insight is to express KL divergence in terms of score functions learned by discrete diffusion models, with a clever design choice (absorbing-state diffusion) that allows computing marginal scores from a single model trained on the joint distribution. The method is evaluated on synthetic data, text summarization, and genomics tasks, demonstrating consistent advantages over existing approaches that rely on embedding discrete data into continuous spaces.

## Strengths

- **Novel and principled approach to an important problem**: Information estimation for high-dimensional discrete data is a genuine gap, and using discrete diffusion models is a creative and theoretically grounded solution. The derivation from CTMCs and Dynkin's formula provides a solid mathematical foundation.

- **Theoretical error analysis**: Equation (7) provides a clean decomposition of the estimation error into a term scaling with score approximation error and a truncation bias that decays exponentially, establishing consistency of the estimator. This is a valuable contribution beyond the algorithmic recipe.

- **Single-model design via absorbing-state diffusion**: The observation (Equation 6) that marginal scores can be derived from a model trained on the joint distribution when using absorbing-state transitions is both elegant and practically impactful, reducing the computational burden of training separate models.

- **Comprehensive and convincing experimental validation**: Synthetic experiments with known ground truth show INFO-SEDD consistently outperforming competitors across varying MI values and dimensionalities, particularly in high-MI regimes where other methods fail. The real-world applications (text summarization model selection, genomics motif discovery) demonstrate concrete utility beyond synthetic benchmarks.

## Weaknesses

### Fatal
None.

### Major

- **Derivation clarity in Section 2.2**: The transition from Equation (2) to Equation (4) is not adequately justified in the main text. Equation (2) claims KL[p0∥q0] = E[log(p0/q0)(X_T)] without explaining why the expectation over X_T (time-T position) equals the KL defined at time 0. The omitted term E[log(p0/q0)(X_0)] is dismissed as negligible because both distributions converge to π, but the connection between the terminal distributions and the initial KL is not obvious. While the appendix likely contains the full derivation, the main text should provide a self-contained sketch that lets readers verify the logic.

- **Computational cost not discussed**: The paper claims INFO-SEDD is "lightweight and scalable" but provides no wall-clock time, FLOP estimates, or convergence speed comparisons relative to competitors. Training discrete diffusion models (with DWDSE loss, noise sampling, and score estimation) is computationally non-trivial, and practitioners need to understand the practical cost before adopting the method. The synthetic experiments use 10^5 steps for all methods, but the per-step cost differs substantially.

- **Missing comparison with classical discrete estimators**: The paper notes that classical discrete estimators (Pinchas et al., 2024) exist but "their accuracy rapidly decreases with increasing data dimensionality." However, no experiments compare against these methods. For low-to-moderate dimensionality regimes where classical estimators might still work, it is unclear whether INFO-SEDD offers advantages. Including such a comparison would strengthen the claim that the embedding trick is a common workaround that INFO-SEDD avoids, and would better characterize when the method is beneficial.

- **Dependence on pre-trained backbones**: The real-world experiments rely on pre-trained models (MDLM for text, CADUCEUS for genomics). The paper frames this as seamless integration, but it also means the quality of MI estimation is bounded by the quality and availability of suitable pre-trained discrete diffusion models for a given domain. When no such model exists, training from scratch is expensive.

### Minor

- **Limited guidance on choosing between INFO-SEDD-J and INFO-SEDD-C**: The two variants show different performance characteristics (e.g., in the genomics consistency test, INFO-SEDD-C significantly outperforms INFO-SEDD-J), but the paper does not provide clear principles for when to use each variant.

- **Entropy estimation relegated to appendix**: Given that entropy estimation is presented as a contribution (Section 3, Algorithm 3), having it only in the appendix with no main-text results weakens this claimed contribution.

## Nice-to-Haves

- Ablation study isolating the benefit of the discrete diffusion framework vs. the specific choice of absorbing-state dynamics vs. the single-model trick would help disentangle which components drive the empirical gains.
- Analysis of how the estimator's accuracy varies with the quality (convergence) of the pre-trained backbone model would help practitioners understand when the method can be applied versus when additional fine-tuning is needed.
- A discussion of limitations and failure modes (e.g., data where score approximation is difficult, very small vocabulary sizes, extremely long sequences) would improve the paper's completeness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Clarify the KL derivation**: Provide a more explicit sketch in the main text showing how Dynkin's formula is applied to the log-ratio function f = log(p_t/q_t) and how the equality in Equation (2) is justified. The step from the last equality in Equation (2) to the integral form is currently too large.
- **Add a computational cost table**: Report training time, inference time, and parameter counts for INFO-SEDD and all competitors on a representative experiment.
- **Include a baseline with classical discrete estimators**: Even on a small-scale experiment, showing where classical estimators break down (and that INFO-SEDD handles those same settings) would substantiate the motivation.
- **Provide explicit guidance on J vs. C variants**: State the conditions under which one variant is preferred (e.g., when the label space is small and the input space is large, INFO-SEDD-C is advantageous because it avoids modeling the joint score of high-dimensional structured data).

## Score and Decision

**Score**: 7.0

**Decision**: Accept

**Rationale**: INFO-SEDD addresses a genuinely important and underexplored problem with a novel, well-motivated approach. The theoretical grounding is solid, the empirical validation is extensive and convincing, and the real-world applications demonstrate concrete value. The main weaknesses are the insufficiently clear derivation in the main text and the missing discussion of computational cost, both of which are addressable without invalidating the contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>