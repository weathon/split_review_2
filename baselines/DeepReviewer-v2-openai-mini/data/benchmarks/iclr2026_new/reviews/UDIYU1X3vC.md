## Summary
This paper introduces Proper Velocity Neural Networks (PVNNs), a novel framework that leverages the Proper Velocity (PV) model of hyperbolic geometry as an alternative to the commonly used Poincaré ball and hyperboloid (Lorentz) models. The PV model is an unconstrained representation of hyperbolic space rooted in Einstein's special relativity, which avoids the numerical instabilities that arise near the boundaries of constrained hyperbolic models.

The authors' core contributions are threefold: (1) establishing the complete Riemannian geometric toolkit for PV space — including closed-form exponential and logarithmic maps, geodesic distance, and parallel transport — derived via isometry with the Poincaré ball; (2) developing fundamental neural network building blocks in PV space, including Multinomial Logistic Regression (MLR), Fully Connected (FC), convolutional, activation, and batch normalization layers; (3) validating the framework through experiments on numerical stability, image classification (CIFAR-10/100 with ResNet-18), graph node classification (Disease, Airport, PubMed, Cora), and genomic sequence learning (TEB transposable element dataset).

The paper is technically strong: the mathematical derivations appear correct, the experimental evaluation is broad and includes meaningful ablations (tangent vs. Riemannian layers, different activation strategies, batch normalization variants), and the results demonstrate that PVNNs match or outperform existing hyperbolic baselines on most tasks. Particularly impressive are the gains on genomic sequence learning (up to +8.33 MCC points on SINEs) and graph classification on strongly hyperbolic datasets (Airport +5.86% accuracy).

Key weaknesses include the absence of statistical significance testing for modest performance gains, lack of explicit limitations discussion, and an introduction that front-loads citation lists rather than foregrounding the numerical stability gap. Novelty assessment is deferred to manual verification due to Retrieval-Disabled Mode in this run.

## Strengths
**S1. Novel theoretical contribution with rigorous derivations.** The paper provides the first complete derivation of the Riemannian operators (exponential map, logarithmic map, parallel transport, geodesic distance) for the PV model, establishing a principled isometry with the Poincaré ball. The mathematical derivations in Theorem 4.2-4.3 and the correspondence between gyrovector and Riemannian structures (Theorem 4.4) are carefully presented and appear correct. This fills a clear gap in the hyperbolic geometry literature, where the PV model's Riemannian structure had not been systematically developed despite its known advantages.

**S2. Clean, reusable neural network building blocks.** The development of PV MLR (Theorem 5.2), PV FC (Theorem 5.3), and PV GyroBN (Theorem 5.4) follows established design patterns from prior hyperbolic networks while addressing PV-specific challenges. The reparameterization from (p_k, a_k) to (z_k, r_k) in Eq. (19) is computationally elegant — converting a O(b·C·n) gyroaddition into an O(b·n·C) matrix multiplication via inner products. The closed-form solution for the FC layer (Eq. 22) and its extension with activations (Eq. 23) are similarly well-designed.

**S3. Comprehensive experimental evaluation.** The paper evaluates PVNNs across four distinct tasks (numerical stability, image classification, graph learning, genomic sequence learning), which is unusually broad. Each experiment includes meaningful baselines representing the three major hyperbolic models (Poincaré ball, hyperboloid, and Klein ball). The numerical stability experiments (Tables 1-3) provide the clearest evidence of the PV model's advantage, with 3-4 orders of magnitude better round-trip accuracy than the Poincaré ball in FP32.

**S4. Thorough ablation studies.** The paper includes ablations on: tangent vs. Riemannian FC layers (Table 6), Fréchet vs. tangent vs. Euclidean batch statistics (Table 7), effect of exponential map for input lifting (Table 8), and three activation strategies (Table 9). These ablations systematically isolate the contribution of each design choice, which significantly increases confidence in the reported results. The finding that the simpler "without Exp_0" variant achieves comparable results (Tables 4, 8) is practically useful.

**S5. Strong empirical results on key benchmarks.** The genomic sequence learning results (Table 10) are particularly impressive: PVCNN outperforms both Euclidean CNN and HCNN-S on all five TEB sub-datasets, with gains of 5-9 MCC points and lower variance (standard deviations 0.27-0.80 vs. 0.56-2.16 for baselines). The Airport graph classification gain (+5.86% over the strongest baseline) is substantial and consistent across folds (std 0.42). These results convincingly demonstrate practical value.

**S6. Well-documented reproducibility.** The paper provides a reproducibility statement, references to detailed appendices for all theoretical proofs (App. E), experimental details (App. C), and a GitHub repository for code release. The Fréchet mean computation via Poincaré ball mapping (using Lou et al., 2020, Alg. 1) is explicitly referenced, reducing implementation ambiguity.

## Weaknesses
**W1. Statistical significance of empirical gains not established.** [Severity: Major]
Several reported improvements are modest in magnitude relative to their standard deviations. For example, in Table 5, the gain on Disease over HNN++ is 81.15 vs. 80.57 (+0.58%) with overlapping standard deviations (±0.23 vs. ±0.23), and on PubMed the gain is 74.33 vs. 73.68 (+0.65%) with non-overlapping but narrow margins. The paper does not report any statistical significance tests (paired t-test, bootstrap confidence intervals, or effect sizes). While the Airport and genomic sequence learning gains are clearly substantial (5.86% and 5-9 MCC points, respectively), the smaller-gain datasets need significance verification. Without this, readers cannot fully assess whether the observed improvements reflect genuine methodological advantages or random variation.
- *Required action:* Add significance tests (e.g., 95% bootstrap confidence intervals for the difference) for all pairwise comparisons, or at minimum report per-fold results and state whether gains are consistent across all folds.

**W2. Missing explicit limitations discussion.** [Severity: Minor-Major]
The paper presents results and future work but does not include a limitations section. Several important limitations are not discussed: (a) The computational overhead of sinh/sinh^{-1}/cosh operations vs. Euclidean layers; (b) sensitivity to curvature K (only partially explored); (c) weaker performance on non-hyperbolic or weakly hyperbolic datasets (e.g., Cora in Table 5); (d) the iterative Fréchet mean computation for GyroBN increases training time (Table 7 shows 2-30× slower on some datasets). The absence of a limitations paragraph reduces scientific completeness.
- *Required action:* Add a brief limitations paragraph to the Conclusion (or as a separate section) explicitly addressing computational cost, curvature sensitivity, and conditions under which PVNN may underperform baselines.

**W3. Introduction narrative structure weakens motivation clarity.** [Severity: Minor]
The first introduction paragraph (line 8) devotes ~60% of its content to a dense citation list of hyperbolic applications before stating the numerical stability gap. This structure delays the key motivation — the constraint-induced numerical instability of existing models — and reads as a literature survey rather than a focused argument. Reviewers may lose the narrative thread before reaching the central claim.
- *Required action:* Condense the application citation list into a short parenthetical. Restructure to foreground the numerical stability gap within the first 3-4 sentences. (See annotation on Page 1 - Introduction for a concrete rewrite.)

**W4. Related work organized as taxonomic lists rather than comparison axes.** [Severity: Minor]
The Related Work section (Section 2) presents papers grouped by topic ("Hyperbolic representation," "Hyperbolic models and networks," "Riemannian normalization") but does not organize them around decision-relevant comparison axes (constrained vs. unconstrained models, Riemannian vs. gyrovector approaches, curvature handling strategies). This makes it harder for readers to quickly understand where PV fits relative to prior work and which gaps remain open.
- *Required action:* Restructure each paragraph around 2-3 comparison axes with explicit positioning statements. For example, contrast the Poincaré ball and hyperboloid models on numerical stability, computational cost, and expressivity, then position PV as offering the best of both (unconstrained yet exact).

**W5. Curvature handling requires more transparency.** [Severity: Minor]
The genomic sequence learning experiment (Section 6.4) states "We use a single curvature shared for all layers" without specifying whether K is learned, fixed to a specific value, or tuned. Since curvature K is a critical hyperparameter in hyperbolic models that controls the geometric properties of the space, this omission affects reproducibility. The image classification and graph learning experiments similarly do not clearly state their curvature handling strategy in the main text.
- *Required action:* Explicitly state the curvature value(s) used, whether K is learned or fixed, and provide curvature sensitivity analysis (e.g., performance as a function of K) in the main text or appendix, referenced clearly.

**W6. Overclaimed efficiency argument in PV MLR.** [Severity: Minor]
The paragraph following Theorem 5.2 claims that the original parameterization "could cause out-of-memory errors in high dimensions" due to an intermediate tensor of size b×C×n. For typical settings (b=64, C=10, n=512), this tensor has 327K elements (~1.3 MB in FP32) — well within GPU memory. The primary advantage is computational efficiency (matrix multiply vs. per-class gyroadditions), not memory avoidance.
- *Required action:* Replace "out-of-memory" with "computationally expensive" or "inefficient for large b×C×n" to avoid overstatement.

**W7. Gradient analysis (Table 3) lacks functional form.** [Severity: Minor]
Table 3 reports only the min-max range of gradient magnitudes across 24 logarithmically spaced radii. Without knowing whether the gradient is monotonically decreasing, oscillating, or flat as a function of radius, readers cannot assess whether the PV gradient behavior is truly more conducive to optimization. A visualization (log-log plot of ||∇f|| vs. r) would be more informative.
- *Required action:* Add a figure showing gradient magnitude vs. radius for PV, Poincaré, and hyperboloid models, or add a description of the functional trend in text.

**W8. Novelty assessment deferred.** [Severity: Verification]
Due to Retrieval-Disabled Mode in this run (external paper search unavailable), the novelty of the claimed contributions relative to prior work cannot be independently verified. The author claim of being "first systematic study" of the PV model for representation learning may be correct, but manual literature verification is required before final acceptance. This is a routine procedural limitation, not a substantive criticism.
- *Status:* Deferred to manual verification.

## Score
**Final Score: 7/10**

*Rationale:* The paper makes a solid theoretical contribution by establishing the complete Riemannian toolkit for the PV model and demonstrating its practical viability through broad experiments. The derivations are rigorous and the empirical evaluation is unusually comprehensive, spanning numerical analysis, computer vision, graph learning, and bioinformatics. The genomic sequence learning results are particularly strong. However, the score is moderated by the absence of statistical significance testing for several modest gains, the lack of an explicit limitations discussion, and narrative weaknesses in the introduction and related work that reduce readability. Additionally, the novelty — while valid — is partially incremental, as the isometry between PV and Poincaré spaces was already known in the gyrovector literature; the contribution lies in systematically deriving the Riemannian operators and building neural network layers, which is a worthwhile engineering advancement. If the authors address the statistical rigor concerns and add a limitations paragraph, the paper would merit a higher score.

| Dimension | Score (0-10) | Notes |
|-----------|-------------|-------|
| Research Value | 7 | Broad, applicable across domains; fills a clear gap |
| Novelty | 6 | First RL treatment of PV model; isometry known from Ungar |
| Soundness | 7 | Theory correct; empirical rigor needs significance tests |
| Reproducibility | 8 | Appendices + code release; could improve curvature specification |
| Writing Quality | 6 | Clear but intro/related work need structural revision |

**Post-Revision Target: [8, 9]/10** — achievable after adding significance tests, limitations section, and narrative restructuring.