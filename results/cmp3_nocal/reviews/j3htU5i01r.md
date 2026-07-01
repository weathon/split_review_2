Now let me produce the final consolidated review.

## Summary

This paper proposes a compositional meta-learning framework that formulates task learning as inference in a learned probabilistic generative model. The model consists of a gating RNN that selects among module RNNs, trained by maximizing marginal likelihood via particle filtering. At test time, new tasks are solved by inferring the module posterior over a single episode without any parameter updates. The method is demonstrated on synthetic rule-learning and motor-learning tasks with known compositional structure, including challenging sparse-feedback and length-generalization conditions.

## Strengths

1. **Principled probabilistic formulation (Section 2.1, Equations 1–8).** The paper cleanly separates within-module dynamics (module RNNs) from between-module dynamics (gating RNN) within a probabilistic generative model. The connection to HMMs — with RNNs replacing both transition and emission matrices — is well-drawn and provides a clear theoretical grounding. Training via marginal likelihood maximization and test-time inference via particle filtering is a coherent synthesis of modular networks, probabilistic inference, and meta-learning.

2. **Well-designed control experiments (Figure 3a–d).** The ablation sequence is logically structured and informative: (a) RNN without task ID → cannot learn; (b) RNN with task ID → learns training tasks but fails on held-out test tasks; (c) model without gating (uniform transitions) → fails on sparse feedback; (d) full model → succeeds. The "flat transitions" control (Figure 3c) is particularly informative, isolating the gating RNN's learned transition structure as the component enabling sparse-feedback inference.

3. **Generalization to longer sequences and sparse feedback (Figures 2e–f, 3f).** The model extends to tasks 2–4× longer than training without parameter updates, while retraining baselines with frozen recurrent weights fail. The sparse-feedback results (Figures 2e, 4e) are the paper's strongest qualitative demonstration: the posterior collapses during a module's expected duration and becomes uniform at the switch point, showing that the gating RNN has genuinely learned the temporal structure. This behavior would be difficult to achieve without the learned gating dynamics.

4. **Qualitative difference in adaptation speed (Figure 3e–f).** Even accounting for the asymmetry in evaluation settings (discussed below), the gap between single-episode inference and the hundreds of episodes required by gradient-based methods (MAML, MLDG, pre-trained RNNs) is large enough to indicate a genuine qualitative advantage for the inference-based paradigm on these tasks.

## Weaknesses

### Fatal

None.

### Major

1. **Asymmetric evaluation between proposed method and baselines in the headline comparison (Figure 3e).** In the full-feedback condition used for the main quantitative comparison, the proposed model's particle filter receives the target outputs **y**ₜ as observations at each timestep within the evaluation episode (Equation 5: particle likelihoods are computed from **y**ₜ) and reconstructs **y**ₜ from the inferred module sequence. The gradient-based baselines (MAML, MLDG, pre-trained RNNs) are evaluated on their ability to *predict* **y**ₜ from **x**ₜ alone on held-out episodes, having trained on separate episodes. The paper does not clarify whether the MSE plotted for the proposed model in Figure 3e is reconstruction error on the same episode used for inference or prediction error on held-out data from the same task. This conflates two different measurements under the same x-axis label "episodes." The sparse-feedback experiments (Figures 2e, 4e) partially redress this by requiring the model to predict at timesteps without observation, but the main quantitative comparison (Figure 3e) uses full feedback. The authors should either (a) adopt a protocol where the model must predict unseen outputs (e.g., provide first K timesteps with feedback and evaluate on remaining T−K timesteps) and compare all methods on that basis, or (b) explicitly acknowledge and discuss this asymmetry.

### Minor

2. **Empirical scope is narrow relative to the paper's framing.** Both evaluation domains use exactly 6 modules with trivial operations (6D vector shifts or 2D trajectory chunks), organized into tasks of exactly 3 operations with fixed per-operation durations (3, 4, or 5 timesteps). The "task grammar" is a known, deterministic pattern with no hierarchical structure, recursion, variable-length operations, or uncertainty about component count. The paper claims the framework "joins the expressivity of neural networks with the data-efficiency of probabilistic inference to achieve rapid compositional meta-learning" (Abstract), but the experiments only demonstrate very simple composition (3 fixed-duration elements out of 6). The paper acknowledges this as proof-of-principle (Section 3), yet the gap between the broad claims and the narrow evidence remains notable. Adding at least one domain with more complex compositional structure (e.g., hierarchical modules, variable-length operations, 20+ operations) would significantly strengthen the contribution.

3. **Fixed module count must be specified a priori.** While Appendix Figure A1 explores cases of data-model mismatch (redundant modules go unused; too few modules approximate a subset of operations), the method requires a fixed *N* at the outset, and the consequences of underestimation are not quantitatively characterized. The paper correctly identifies this as future work (Section 3), but it is a practical limitation for real-world applications where the number of reusable components is unknown.

4. **The motor learning domain does not test substantially new capabilities.** The motor task is essentially a reparameterization of the rule-learning task into a different output space (2D trajectories instead of 6D shifts), and the paper makes architecture changes between experiments (removing input, resetting module hidden states, adding module-specific parameters). While the paper frames this as a demonstration of the same framework across domains, the motor experiments do not test generalization to meaningfully different compositional structures.

5. **Missing reporting details for full reproducibility.** The main text does not specify (a) the number of training tasks and how the train/test split is constructed (e.g., for 6 operations with 3 per task, is the full set of 120 possible tasks used for training, or a subset?), (b) the number of particles *K* used in inference, or (c) wall-clock time or FLOPs comparison to baselines (all methods are compared only by "episodes," which have different meanings across paradigms). These details are likely in the stripped appendix but should be stated in the main text.

### Trivial

None.

## Nice-to-Haves

- A wall-clock time or FLOPs comparison would be more informative than "episodes" as the x-axis, since particle filtering with *K* particles over *T* timesteps costs *O(K·T)* forward passes, a different compute profile than gradient-based methods.
- A prediction-based evaluation protocol (provide first *K* timesteps with feedback, evaluate on remaining *T−K*) would put all methods on equal footing and strengthen the main comparison.
- The representation of the discrete variable **z**ₜ₋₁ as input to the gating RNN (one-hot, embedding, or via module hidden state) should be clarified.

## Removed Points

- **Gumbel-softmax and particle filter backpropagation details are opaque.** *Removed because the paper states these details are in Appendix A.2, which was stripped by the parser. Per review policy, missing appendix content should not be penalized.*
- **Requires knowing the number of modules ahead of time (overstated as "Critical").** *Moved from Critical to Minor because the paper acknowledges this limitation, explores the mismatch case (Figure A1), and identifies it as future work.*
- **Strawman/misread criticisms about the evaluation.** The critic's framing of "reconstruction vs. prediction" is a legitimate asymmetry (kept as Major). However, claims that the comparison is invalidated or that the paper never clarifies the setting overstate the issue — the sparse-feedback experiments already demonstrate genuine prediction, and the paper is transparent about the inference-based paradigm.
- **Generic "scope creep" weaknesses.** Requests for larger module counts or more complex structure, while valid, are scaled down to Minor since the paper transparently frames itself as proof-of-principle.
- **Formatting/style nitpicks and missing-related-work complaints.** Removed per policy.

## Novel Insights

None beyond the paper's own contributions. The review confirms that the core insight — compositional meta-learning cast as inference in a learned generative model with RNN-based modules and gating — is genuinely novel and well-executed, but the evaluation limitations and asymmetric comparison are the main factors limiting the paper's strength.

## Suggestions

1. Adopt a prediction-based evaluation protocol for the main comparison (e.g., provide first *K* timesteps with feedback, evaluate MSE on the remaining *T−K* timesteps without feedback) so that all methods are measured on the same task. The existing sparse-feedback experiments already do this partially; make them the primary quantitative comparison.
2. Add at least one evaluation domain with richer compositional structure (hierarchical modules, variable-length operations, or a larger operation set) to substantiate the broader claims about compositional meta-learning.
3. Report the number of training tasks, train/test split construction, and particle count *K* in the main text.
4. Include a computational cost comparison (wall-clock time or FLOPs) to make the "episodes" comparison more informative.

## Score and Decision

**Score:** 6 — The paper presents a well-motivated, principled approach with clean controls and informative ablations. The core idea is solid and the sparse-feedback results are compelling. However, the main quantitative comparison to baselines is undermined by an asymmetric evaluation protocol, and the empirical scope is narrow relative to the paper's framing. These issues are addressable in revision and do not invalidate the contribution, but they do limit the current strength of the evidence.

**Decision:** Accept — The paper makes a clear contribution (a principled inference-based approach to compositional meta-learning), the method is sound, and the limitations are identifiable and addressable. The weaknesses (evaluation asymmetry and narrow scope) should be addressed in a camera-ready revision.

<score>6</score>