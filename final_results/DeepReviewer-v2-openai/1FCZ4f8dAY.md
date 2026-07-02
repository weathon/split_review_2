## Summary
# Final Review Report

## Summary

This paper presents a novel theoretical framework for constructing equivariant machine learning models on tensors. The authors use classical invariant theory to parameterize polynomial (and, more generally, analytic) functions from tensor inputs to tensor outputs that are equivariant under the diagonal action of the orthogonal group O(d), the indefinite orthogonal group O(s,d−s) (which includes the Lorentz group), and the symplectic group Sp(d). The key theoretical contribution is showing that any O(d)-equivariant polynomial tensor function can be expressed as a linear combination of tensor products of inputs with isotropic tensors (Kronecker delta and Levi-Civita symbol) followed by Einstein-summation contractions (Theorem 1). This generalizes to entire functions for the Lorentz and symplectic groups (Theorem 2), with the isotropic tensors replaced by the corresponding bilinear forms (𝕀_{s,d−s} or J_d). Practical architectures are derived for the special case where inputs are vectors (Corollaries 1 and 3) and for symmetric 2-tensors (Corollary 2), where coefficients become learned functions of invariant inner products.

The paper demonstrates the approach on three applications: (i) learning stress-strain relationships for isotropic neo-Hookean materials, (ii) path-signature approximation from sparse path samples for time series, and (iii) sparse vector estimation in linear subspaces. In all cases, the equivariant models outperform non-equivariant baselines (standard MLPs and data-augmented MLPs), often by large margins. The sparse vector experiment further shows that learned equivariant models can compete with or outperform sum-of-squares methods when the theoretical assumptions of the latter are violated.

The paper is mathematically rigorous, well-structured, and provides a genuine extension of equivariant ML to groups beyond O(3) without relying on Clebsch-Gordan decompositions. However, several limitations temper the impact: (a) the practical architectures are restricted to vector inputs and low-rank tensor outputs; (b) the computational complexity scales poorly with output tensor rank (O(k'! n^{k'})); (c) the stress-strain experiment learns an already known analytical function; (d) the sparse vector results show inconsistent performance across noise covariance settings; and (e) quantitative comparisons with existing equivariant methods (e3nn, escnn) are absent. External literature verification was unavailable in this run; novelty and comparison conclusions are intentionally deferred.

**Paper type**: Theoretical method paper with proof-of-concept experiments on synthetic data.

## Strengths
1. **Mathematical rigor and theoretical completeness**: The paper provides a full characterization of equivariant polynomial tensor functions for three classical Lie groups (Theorems 1 and 2), grounding the architecture design in classical invariant theory. The proofs are referenced to appendices, and the main results are stated with clear assumptions and notation.

2. **Generality beyond O(3)**: Unlike prior equivariant tensor architectures (e3nn, escnn) that are restricted to SO(3) and O(3) with Clebsch-Gordan decompositions, the proposed framework naturally extends to indefinite orthogonal groups (Lorentz) and symplectic groups. This opens up applications in special relativity, quantum mechanics, and other areas where these symmetries arise.

3. **Elegant practical parameterization for vector inputs**: Corollaries 1 and 3 provide a clean, implementable architecture where scalar coefficients depend only on invariant inner products, making the model automatically equivariant without data augmentation or group-theoretic coefficient tables. The complexity analysis (O(k'! n^{k'})) is honestly disclosed.

4. **Clear empirical demonstrations across disparate domains**: The three applications cover materials science, time series analysis, and theoretical computer science, showing the breadth of the framework. The sparse vector estimation experiment in particular provides an interesting comparison between learned equivariant models and theoretically guaranteed sum-of-squares methods.

5. **Honest discussion of limitations**: The paper acknowledges the computational impracticality of the general Theorem 1, describes the restriction to vector inputs for practical use, and admits uncertainty about whether the characterization extends to all continuous equivariant functions. The Related Work comparison with Clebsch-Gordan methods is balanced.

6. **Reproducibility**: The authors provide open-source code and synthetic data generation procedures, which is commendable for a theory-grounded paper.

## Weaknesses
### W1. Practical architectures address only the vector-input special case (Major)

The general theoretical results (Theorems 1 and 2) characterize equivariant functions for arbitrary tensor inputs, but the practical architectures follow from Corollaries 1-3, which cover only two restricted settings: (i) vector inputs to tensor outputs (Corollaries 1 and 3), and (ii) symmetric 2-tensor inputs to symmetric 2-tensor outputs (Corollary 2). For input tensors of higher order (e.g., 3-tensors or mixed-order inputs), the general Theorem 1 is acknowledged as "impractical" due to the combinatorial explosion of isotropic tensors. This creates a significant gap between the claimed generality and what can actually be implemented.

**Impact**: Readers expecting a general-purpose equivariant tensor learning framework may find that the method is essentially an equivariant architecture for vector-valued data. The paper should more prominently state this limitation in the abstract and introduction, not only in the method section.

**Recommendation**: Add a sentence in the Contributions paragraph: "While the theoretical characterization applies to arbitrary tensor inputs, our practical architectures focus on the important special case of vector inputs, which already covers many scientific applications."

### W2. Stress-strain experiment learns a known analytical function (Major)

The stress-strain experiment (Page 7 - Section 5) learns the second Piola-Kirchhoff stress tensor S from the Cauchy-Green strain tensor C, where the ground-truth relationship is given by the closed-form analytical expression S = (½ λ log det C - μ) C^{-1} + μ I_d (Eq. 23). The paper does not compare the learned model's error against simply using this analytical formula directly. Since C is observable at test time, the analytical formula provides a zero-error (up to numerical precision) baseline that would outperform all methods shown in Table 1.

**Impact**: This undermines the practical significance of the stress-strain experiment. The paper frames the task as "learning" a material model, but the ground truth is known exactly. If the goal is to demonstrate that the equivariant architecture can capture the correct functional form from limited data, this should be stated explicitly, and the analytical baseline should be included for calibration.

**Recommendation**: (a) Add an "Analytical formula" row to Table 1 showing the error of Eq. (23) applied to test data (expected ~0). (b) Reframe the experiment as a proof-of-concept for learning unknown material models, or replace with a dataset where the true function is not analytically known.

### W3. Sparse vector results show inconsistent performance across settings (Major)

In the sparse vector estimation experiment (Page 9 - Section 5), the proposed method's performance varies dramatically across noise covariance settings. For example, under Bernoulli-Gaussian sampling with Identity covariance, "Ours" achieves only 0.342 ± 0.043 vs. SoS's 0.962 ± 0.002, while under Random covariance, "Ours" achieves 0.937 ± 0.002. Furthermore, the "Ours (Diag)" variant—which uses only vector norms rather than full pairwise inner products—sometimes substantially outperforms the full model (e.g., Bernoulli-Gaussian Diagonal: Diag=0.914 vs. Ours=0.463).

**Impact**: This inconsistency suggests that the full model may overfit to cross-product noise in certain covariance regimes. The paper mentions this pattern but does not analyze its root cause. Without understanding when and why the full model fails, practitioners cannot reliably apply the method to new problems.

**Recommendation**: (a) Add training/validation curves for the low-performing settings to verify that the model is not overfitting. (b) Analyze why "Ours (Diag)" outperforms "Ours" on some settings—this could indicate that the additional cross-product features add noise rather than signal. (c) Provide guidance on when to use the diagonal variant vs. the full model.

### W4. Missing quantitative comparison with existing equivariant methods (Major)

The Related Work section (Page 2) correctly identifies e3nn, escnn, and Domina et al. (2025) as the closest competitors, and states that those methods are "more memory efficient than our general formulation" but "comparable to our Corollaries 1 and 3." However, no quantitative comparison is provided—no runtime, memory usage, or parameter count benchmarks are reported for any of the three experiments.

**Impact**: Readers cannot assess the practical trade-off between the proposed invariant-theoretic approach and existing representation-theoretic approaches. The paper's claim that "computational and approximation power should be equivalent" is unverifiable without empirical evidence.

**Recommendation**: Add either (a) a small benchmarking table comparing parameter count, memory (GB), and forward-pass time for matching architectures on a representative task, or (b) an analytical complexity comparison table showing how the scaling laws differ.

### W5. Path signature experiment lacks statistical detail and has metric typo (Minor)

In Table 2 (Page 8), the proposed method's results are reported as single numbers (0.002 for O(d), 0.005 for Lorentz) without standard deviations, while all baseline methods include variance estimates. Additionally, the metric definition in the table caption contains a typo: "d_F/d_F" appears to be a formatting error (likely intended to be 1/d_F or similar). The path generation process is described only in the appendix, making it difficult to assess task difficulty from the main text.

**Impact**: The missing variance makes it impossible to assess whether the proposed method's advantage is statistically significant, especially given the very small absolute values (0.002 vs. 0.007 for the best MLP baseline under O(d)).

**Recommendation**: (a) Report standard deviations for all methods in Table 2. (b) Fix the metric definition typo. (c) Briefly describe the path distribution in the main text.

### W6. Strong novelty claim requires verification (Minor)

The Discussion (Page 9 - Section 6) states: "To the best of our knowledge this is the first work that provides a recipe for equivariant machine learning models for tensors at this level of generality." This claim is ambiguously scoped: does "level of generality" refer to (a) covering three classical Lie groups simultaneously, (b) handling arbitrary tensor orders and parities, or (c) avoiding Clebsch-Gordan coefficients? The paper's own related work identifies multiple prior equivariant tensor architectures, and external literature verification was unavailable in this run.

**Impact**: A reviewer familiar with the literature could challenge this claim if a counterexample exists. The paper would be more defensible with precise scope qualifiers.

**Recommendation**: Replace with: "This work provides the first unified invariant-theoretic parameterization of equivariant tensor functions covering the orthogonal, indefinite orthogonal, and symplectic groups without requiring Clebsch-Gordan decompositions."

### W7. Computational complexity limits scalability (Suggestion)

The complexity O(k'! n^{k'} (Q d n^2 + d^{k'})) from Corollary 1 is acknowledged but not benchmarked. Even for the suggested practical range k' ∈ {1,2,3,4}, the factorial and n^{k'} terms lead to rapid growth. For example, with n=100 input vectors and k'=4, the n^{k'} term alone contributes 10^8 operations. The paper does not report actual wall-clock times or parameter counts for any of the three experiments.

**Recommendation**: Add a table in the appendix showing total parameter count, training time, and inference time for each experiment, so readers can calibrate feasibility for their own problem sizes.

### W8. Experiments are exclusively on synthetic data (Suggestion)

All three applications use synthetically generated data: the stress-strain data comes from an analytical material model, the path data is simulated, and the sparse vector data is synthetic. While this is appropriate for a theory paper, it limits the demonstrated practical impact.

**Recommendation**: If possible, include at least one real-world dataset to demonstrate that the method works under realistic noise conditions and data distributions. Failing that, explicitly state that real-world validation is left for future work.

### W9. Lack of ablation studies on the role of equivariance vs. capacity (Suggestion)

The paper attributes performance gains to the equivariance inductive bias, but the baselines (MLPs) have different architectures. The MLP baselines are compared at "same width" and "same number of parameters," but no control experiment isolates equivariance as the causal factor. For example, one could add an equivariance-promoting regularizer to the MLP to see if it closes the gap.

**Recommendation**: Add a controlled experiment where the same base architecture is trained with and without the equivariance constraint (e.g., by removing the inner-product invariance in the q functions).

## Score
**Final Score: 6/10**

**Rationale**: The paper presents mathematically rigorous theoretical contributions—the first unified invariant-theoretic characterization of O(d)-, O(s,d-s)-, and Sp(d)-equivariant tensor functions—which has clear value for the geometric deep learning and scientific ML communities. The theoretical work is clean and well-connected to the classical invariant theory literature. However, the score is tempered by several significant limitations: (a) the practical architectures are restricted to vector inputs, creating a gap between the claimed generality and what is implementable; (b) the stress-strain experiment's practical significance is undermined by learning a known analytical function; (c) the sparse vector results show inconsistent performance that is not adequately explained; (d) quantitative comparisons with existing equivariant methods (e3nn, escnn) are absent; and (e) all experiments are on synthetic data with limited dimensionality. The novelty claim ("first work at this level of generality") could not be verified against external literature in this run and is marked as deferred. Priorities for strengthening the paper are: adding analytical-baseline comparisons, benchmarking against existing equivariant architectures, and providing guidance on when the method succeeds versus fails in sparse vector estimation.

The paper is publishable at a good venue after addressing the major weaknesses, particularly W2 (known analytical function issue) and W4 (missing comparison with existing methods).