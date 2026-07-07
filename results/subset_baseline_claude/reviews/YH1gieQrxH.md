## Summary

This paper proposes incorporating geometric priors into self-supervised abstract world models by structuring the latent space as a product of quotient spaces (e.g., ℝ/kℤ for cyclic/rotational symmetry) and standard Euclidean subspaces for non-symmetric features. Transitions are modeled via modular addition in the structured subspaces and standard addition in unstructured ones. A sparsity regularization encourages disentanglement between symmetric and non-symmetric features. Experiments on Passage, Torus, MiniGrid, and VizDoom show improved generalization on unseen transitions and better downstream RL performance compared to unstructured baselines.

## Strengths

- **Elegant and lightweight formulation.** Using ℝ/kℤ as the latent topology for cyclic symmetry is mathematically clean and requires no architectural changes to the encoder/decoder networks—symmetry is encoded purely through the transition operator and loss. This is a clear advantage over equivariant network architectures with their added computational complexity.
- **Practical handling of mixed symmetry settings.** The product-space design (structured × unstructured subspaces) plus the action-conditioned disentanglement loss is a genuine extension over prior work (Quessard et al., 2020; Park et al., 2022), which require fully symmetric features. Table 1 shows this concretely: Quessard's rotation-matrix method collapses on VizDoom (H@1 of 17.6) while the proposed method maintains 81.0.
- **Quantitative validation across representation quality and RL.** The paper measures both representation quality (H@k, MRR) and downstream RL performance (Figure 8), across multiple environments and data regimes. The consistent improvements—especially in the low-data regime—support the claimed generalization benefit.
- **Visualization supporting interpretability claims.** Figures 3–6 provide concrete evidence that the model learns a topology-consistent latent space (torus, circular orientation), lending credibility to the disentanglement claims.

## Weaknesses

### Fatal
None.

### Major

1. **The symmetry group must be specified a priori.** While the paper notes that the exact group order need not be known, the user must still identify the correct symmetry type (cyclic/rotational vs. translational vs. other). In environments where the symmetry structure is ambiguous or only approximately satisfied, it is unclear how the method degrades. No experiment probes this sensitivity—e.g., what happens when the latent space is parameterized with the wrong group, or when symmetry is only approximate?

2. **The disentanglement loss requires knowing σ: A → I.** The mapping specifying which actions affect which latent subspaces (Eq. 11) must be provided by the designer. This is a significant supervision signal beyond just specifying the group type. The paper does not discuss how to determine σ in practice, nor whether errors in σ substantially harm performance.

3. **RL experiments are limited in scope.** The downstream RL evaluation uses a simplified setup (frozen world model, DDQN, goal-reaching with step-penalty), and the environments are small/custom. No comparison to a model-free agent with equivariant architecture is provided, and there is no test on standard RL benchmarks. The frozen-world-model protocol also means the RL performance depends heavily on how well the world model was pre-trained, conflating representation and RL algorithm quality.

### Minor

1. The comparison baseline set is limited to two older methods (PRAE, 2020; Quessard, 2020). More recent equivariant world models or latent-space symmetry methods would strengthen the empirical case.

2. The VizDoom experiment uses a heavily simplified custom setup (only 4 actions, fixed 36° rotation, static map) compared to standard VizDoom benchmarks. It is unclear whether the approach would hold in less controlled settings.

3. The paper claims to handle "abstract unstructured information alongside symmetries" but the unstructured subspace in VizDoom experiments is effectively only position (2D). How the method handles richer non-symmetric structure is not demonstrated.

### Trivial
None worth noting.

## Nice-to-Haves

- An ablation on the sensitivity to the choice of group (e.g., using a cyclic group of the wrong order, or using a continuous SO(2) prior when the true group is discrete ℤ/nℤ).
- A discussion of how σ might be inferred automatically (e.g., from action semantics or learned).
- An experiment probing the number of training transitions needed as a function of group complexity.

## Novel Insights

The key insight is that encoding cyclic structure via modular arithmetic in the latent space—rather than through equivariant network weights—achieves similar inductive bias at lower architectural cost and naturally generalizes to mixed symmetric/non-symmetric settings. The product-space design for handling heterogeneous symmetry groups is a practically useful contribution that prior methods lacked, and the empirical observation that this structure persists even with high-dimensional (image) inputs in VizDoom is nontrivial, suggesting the contrastive objective can successfully bind CNN features to a topologically constrained latent manifold.

## Suggestions

- Add an experiment varying the specified group vs. the true group to characterize robustness to group misspecification.
- Clarify how σ is determined in experiments and discuss whether it can be learned or inferred.
- Expand the RL evaluation to include at least one standard benchmark (e.g., standard VizDoom tasks, Atari) with a competitive model-based RL algorithm rather than vanilla DDQN.

## Score and Decision

The paper presents a clean, well-motivated idea with solid empirical evidence for its core claims (better representation generalization and downstream RL). The formulation is elegant and practically lightweight. The primary concerns are: (a) the prior knowledge required (group type + σ mapping) limits applicability; (b) RL experiments are limited; (c) the comparison set is dated. These are real limitations but do not invalidate the contribution, which is a meaningful extension of prior work to mixed structured/unstructured settings with empirical validation on a nontrivial environment (VizDoom).

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>