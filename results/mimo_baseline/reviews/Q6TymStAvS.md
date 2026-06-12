## Summary

ShadowFM introduces geometric flow matching methods for learning Hamiltonian-conditional distributions of classical shadows, motivated by the observation that single-qubit shadows naturally map to the Bloch sphere S². Two approaches are proposed: (1) a Riemannian flow matching on S² ("Spherical Flow") and (2) an anisotropic Dirichlet flow that generalizes standard Dirichlet flow by incorporating target/anti-target pairing structure of measurement outcomes. Both methods outperform existing baselines on TFIM and Heisenberg models across 1D and 2D systems for estimating correlation functions and entanglement entropy.

## Strengths

- **Well-motivated geometric insight with empirical support.** The paper makes a clean argument connecting the Bloch sphere to shadow geometry, and backs it with a compelling toy experiment (Figure 2) showing that spin errors (traversing the sphere) are substantially more damaging to observable estimation than basis errors (rotating along it). This motivates the entire framework in a principled way.

- **Two complementary technical contributions.** The Spherical Flow applies Riemannian flow matching directly on S² using closed-form exp/log maps, while the Anisotropic Dirichlet flow generalizes standard Dirichlet flow (Stark et al., 2024) with a principled derivation from the continuity equation, introducing a "push-toward-target, pull-from-anti-target" mechanism. The latter is a genuine generalization (recovers Dirichlet flow at γ=0) and is applicable beyond quantum shadows.

- **Comprehensive experimental evaluation.** Experiments span TFIM and Heisenberg models, L=10 and L=30, 1D and 2D systems, ground states and quantum dynamics (extrapolation to unseen time points), multiple POVMs (Pauli-6 and tetrahedral), and training data scaling analysis. Tables 1–6 show consistent improvements over LinearFM, Diff-LM, StatisticalFM, and classical kernel methods.

- **Phase transition capture.** Figure 5 demonstrates that ShadowFM accurately captures the critical point at c=1/2 in TFIM, whereas baselines like LinearFM and StatisticalFM fail to capture the abrupt derivative change—a physically meaningful qualitative result.

## Weaknesses

### Fatal
None.

### Major

- **Inconsistent relative performance of the two proposed methods.** The Spherical approach dominates in some settings (Heisenberg L=10 correlation in Table 3, dynamics correlation in Table 5) while the AD approach dominates in others (TFIM L=10 in Table 1, Heisenberg L=30 in Table 4). The paper provides no analysis of when or why each approach should be preferred, leaving practitioners without guidance. This is especially important since the two methods have very different computational profiles (Riemannian maps vs. precomputed integrals).

- **Modest system sizes relative to the stated motivation.** The paper argues that classical shadows are valuable because full quantum state tomography scales exponentially, yet the experiments use L=10 (exact diagonalization) and L=30 (DMRG) for 1D, and 4×4 for 2D—sizes where classical simulation is already tractable. The paper would be substantially stronger if it discussed at what system sizes ShadowFM provides a genuine computational advantage over direct simulation, or demonstrated scaling to larger, more challenging regimes.

### Minor

- **No comparison to autoregressive methods.** The introduction highlights autoregressive approaches (Carrasquilla et al., 2019; Yao & You, 2024) as competitors that suffer from sequential bottlenecks, yet no autoregressive baselines appear in the experiments. Without this comparison, the claimed advantage of non-autoregressive generation remains unsubstantiated.

- **Limited hyperparameter analysis for AD flow.** The paper evaluates γ ∈ {0, 0.05, 0.1} and reports the best, but provides no sensitivity analysis or guidance for choosing γ in new settings. Given that γ controls the core mechanism (anti-target repulsion), this deserves more attention.

- **Computational cost not discussed.** The AD flow requires precomputing integrals (Equations 8–9), and the Spherical flow involves exp/log map evaluations. Training time, inference time, and memory requirements relative to baselines would help practitioners assess practical value.

### Trivial
None.

## Nice-to-Haves

- An analysis or visualization of *generated shadow distributions* rather than only downstream observable errors would help diagnose what specifically the geometric modifications improve (e.g., do they actually suppress spin errors as hypothesized?).
- A discussion of the connection between the Spherical approach's use of cross-polytope noise and the Bloch sphere's octahedral symmetry would deepen the geometric narrative.

## Novel Insights

The paper's central novel observation is that classical shadows from Pauli-6 POVM are not just discrete tokens but carry intrinsic Riemannian geometry inherited from the Bloch sphere, and that generative models exploiting this geometry yield measurably more faithful shadow distributions. The empirical finding that spin errors (geodesic-distance-maximizing on S²) are far more detrimental than basis errors provides physical grounding for this geometric perspective. The anisotropic Dirichlet flow, while building on existing discrete flow matching, introduces a genuinely new mechanism for incorporating natural pairing structure in data—repelling from anti-targets during transport—which is a conceptually clean contribution applicable beyond the quantum setting.

## Suggestions

- Add a comparison against at least one autoregressive baseline (e.g., the method from Yao & You, 2024) to validate the non-autoregressive advantage.
- Include a runtime/efficiency comparison table showing training time and inference time for all methods.
- Provide a figure or analysis showing the distribution of generated shadows versus true shadows (e.g., marginals or t-SNE) to visualize what geometric corrections actually achieve at the distribution level.
- Discuss the scaling prospects: at what qubit count does ShadowFM become more practical than DMRG or tensor network methods?

## Score and Decision

The paper presents a technically sound and well-motivated contribution at the intersection of geometric generative modeling and quantum physics. The geometric insight is natural, the two proposed methods are cleanly derived, and experiments consistently show improvements. However, the limited system sizes and absence of key comparisons (autoregressive methods, computational cost) temper enthusiasm. The inconsistent relative performance of the two methods without explanation is also a gap. Overall, this is above average for ICLR but not yet at the level of a clear accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept