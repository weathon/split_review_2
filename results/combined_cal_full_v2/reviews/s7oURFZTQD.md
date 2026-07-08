Now let me write the final review.

---

## Summary

This paper provides both theoretical and experimental analysis of multi-grade deep learning (MGDL), where a deep network is decomposed into sequential shallow grades trained on the residuals of previous grades. The authors establish convergence theorems for GD under smoothness assumptions, prove convexity of single-ReLU-layer grades (Theorem 3), and conduct eigenvalue analysis showing that MGDL's iteration matrix eigenvalues stay within (-1,1) while SGDL's drift below -1, causing oscillatory loss. Experiments span image regression, denoising, deblurring, CIFAR-10/100, and transformers.

## Strengths

- **Convexity connection (Theorem 3, Section 4):** Building on Pilanci & Ergen (2020), the paper proves that when each MGDL grade is a single ReLU hidden layer, the nonconvex optimization decomposes into a sequence of convex subproblems. This extends convexification ideas from shallow to deeper architectures via the multi-grade decomposition and is a clean formal result.

- **Comprehensive eigenvalue analysis across multiple tasks (Section 7):** The paper empirically tracks eigenvalues of *I* − η*H* during training for synthetic regression, image regression, denoising, and CIFAR-10. The consistent pattern — SGDL eigenvalues dropping below −1 while MGDL eigenvalues remain within (−1, 1) — is demonstrated across several distinct problem types, providing a plausible diagnosis for SGDL's oscillatory loss.

- **Multi-grade Transformer extension (Section 8):** The MGT extension shows the MGDL idea generalizes beyond fully connected and convolutional networks to transformers. The time-series experiments report concrete test MSE and wall-clock time, with MGT achieving substantially better test performance (e.g., TeMSE 1.6×10⁻¹ vs 2.6 for SGT on synthetic data) while requiring significantly less training time.

- **Learning rate robustness experiments (Section 6):** Both synthetic and image regression experiments demonstrate that MGDL maintains stable convergence over a wider range of learning rates than SGDL, with explicit ranges reported (e.g., MGDL sustains loss < 0.001 for η ∈ [0.01, 0.3] vs. SGDL only for η ∈ [0.03, 0.08] in Setting 1).

## Weaknesses

### Major

- **Uncontrolled comparison confounds architecture with training method.** Across every experiment, SGDL and MGDL use fundamentally different architectures with different parameter counts and structural advantages. For image regression: SGDL uses (2,1,128,8) — 8 hidden layers of width 128; MGDL uses (2,1,128,2,4) — 4 grades, each with 2 hidden layers (total 8 hidden layers), but earlier grades are frozen and serve as learned feature extractors for later grades. The paper interprets MGDL's advantages as stemming from its "training framework," but the comparison actually contrasts "train a deep network end-to-end" with "train a sequence of shallow networks that leverage previously trained shallow networks as feature extractors." The claimed benefits could be partially or fully explained by (a) the advantages of shallower networks, (b) sequential curriculum learning, (c) capacity differences, or (d) optimization budget differences. The experiments do not isolate the training framework from these confounds. This is the most significant weakness because it undermines the central claim that "MGDL outperforms SGDL" as a training methodology.

- **No classification accuracy reported for CIFAR-10 and CIFAR-100.** The CIFAR experiments report only MSE loss (lines 225, 289) and use the word "accuracy" (lines 15, 152, 154, 225, 349) to describe results, but never report actual classification accuracy (e.g., top-1 accuracy). For classification datasets, MSE is an optimization metric, not a standard evaluation of classification performance. Lower MSE does not necessarily translate to higher classification accuracy, so the paper's claims about superior classification performance on CIFAR datasets are not supported by the reported evidence.

- **Theory-practice gap in convergence theorems (Theorems 1, 2, and 4).** Both Theorem 1 (line 70) and Theorem 2 (line 104) explicitly assume the activation function σ is twice continuously differentiable, and Theorem 4 (line 255) assumes the objective is twice continuously differentiable. However, every experiment in the paper uses ReLU activation (σ(x) = max{0,x}), which is not twice continuously differentiable. The paper does not address this discrepancy, provide a relaxation (e.g., subdifferential analysis, smoothed ReLU in the theory while keeping ReLU in practice), or acknowledge this limitation. As stated, the formal theoretical guarantees do not apply to the architectures tested in the experiments. This weakens the paper's claim to provide "rigorous convergence guarantees" (line 26) for its practical setup.

### Minor

- **Claim αₗ ≪ α is unsubstantiated (line 112).** The paper asserts that the Hessian spectral norm for MGDL grades is much smaller than for the full SGDL network (αₗ ≪ α), which is central to the claim that MGDL allows a broader admissible learning-rate range. This is presented without proof, empirical measurement, or any bound — no verification is provided for any of the tested architectures.

- **No statistical significance or multiple runs.** Every reported number in every table (Tables 1–5) and every figure is a single point with no standard deviations, confidence intervals, or mention of how many random seeds or independent trials were run. This makes it impossible to assess whether reported advantages are statistically meaningful, especially for smaller improvements (e.g., 0.16 dB PSNR gain in Table 2 at noise level 60 for Chest image).

- **Theorem 3's condition (mₗ ≥ Pₗ) is extremely restrictive and unaddressed.** The number of activation patterns Pₗ can be exponential in the data dimension. The paper presents this convexity result as a theoretical contribution but does not acknowledge its practical limitations or discuss whether the condition can plausibly hold in the experiments conducted.

### Trivial

- **CIFAR-100 learning rate discrepancy.** The main text (line 225) reports testing learning rates of 5 × 10⁻⁴ and 1 × 10⁻⁴, but the Figure 3 caption (line 233) reports η = 5 × 10⁻⁵ and η = 1 × 10⁻⁴ — a discrepancy of an order of magnitude.

## Nice-to-Haves

- Controlled comparisons where the same total architecture (same depth, same parameter count) is trained end-to-end (SGDL) and via MGDL decomposition, isolating the training framework as the only variable.
- Ablation studies (e.g., training grades jointly vs. sequentially, unfreezing earlier grades, varying grade depths).
- Empirical verification or bounds for the claimed αₗ ≪ α relationship.
- Multiple seeds and error bars across all experiments.
- Real classification accuracy (top-1) for CIFAR-10 and CIFAR-100.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Interpretability claim not addressed":** The paper mentions interpretability as a motivation citing Xu (2025) but never claims interpretability as a contribution of this paper. Scope creep — removed.
- **"α (spectral norm bound) never computed":** A common theoretical limitation; eigenvalue analysis in Section 7 provides empirical spectral information. Removed as a generic concern.
- **"Missing comparison to greedy layer-wise pretraining, progressive networks, gradient boosting":** Removed per instructions — cannot confirm existence/absence of related works.
- **"Missing hyperparameters, learning rate schedules, batch size":** Reproducibility nitpick — removed per instructions.
- **"Figure captions too long":** Formatting nitpick — removed.
- **"Section 8 disconnected from theoretical framework":** The transformer experiments are presented as a generality demonstration, not as evidence for the specific theoretical claims. This is an acknowledged extension.
- **"Eigenvalue analysis on small networks only":** The paper acknowledges this (line 285). Already addressed by authors.
- **"Image regression is super-resolution/interpolation":** The task is clearly described; it is a valid experimental setting, not a flaw.
- **"Hessian-based analysis only captures 'stable' regime":** The eigenvalue analysis covers the relevant dynamic range and the paper discusses both stable and unstable regimes. Removed as not a genuine weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Redesign the controlled comparison.** The single most impactful fix: compare SGDL and MGDL on the *same* total architecture where the only difference is end-to-end vs. grade-by-grade training. For instance, take a fixed deep network, train it end-to-end (SGDL), and compare with decomposing that same network into sequential prefixes trained on residuals (MGDL).

2. **Report actual classification accuracy** (top-1) for CIFAR-10 and CIFAR-100 with error bars over multiple seeds.

3. **Reconcile the convergence theory with ReLU activations.** Either adopt subdifferential analysis, restrict the theory to smoothed activations while acknowledging the gap, or explicitly scope the claims.

4. **Provide empirical support for the αₗ ≪ α claim** by measuring or bounding the Hessian spectral norms of the actual architectures used.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>

---

**Calibration Report**

*Round 1 bracket:* The most topically similar retrieval anchors sat in the 3–5 range: "Three ways that non-differentiability affects neural network training" (3.00), "Block Coordinate Descent for Neural Networks Provably Finds Global Minima" (4.00), and "Can Stability be Detrimental?" (4.20). The 5.5–7.0 anchors (e.g., "Sharper Guarantees for Learning Neural Network Classifiers with Gradient Methods" at 7.00, "Make Haste Slowly" at 6.00) were accepted papers with stronger alignment between theory and experiments and more rigorous experimental design. The initial bracket was [3.5, 5.5].

*Round 2 narrowing:* Itemized comparison against zPaTnGjgpa.md (4.20, eigenvalue/training stability analysis) shows the present paper has higher-weighted strengths (all 9.3–9.8 vs 6.2–9.8) but also carries negative-weighted weaknesses (–0.87 for uncontrolled comparison, –0.04 for missing classification accuracy) that the anchor paper did not have in the same form. Against n2RIkaf1S4.md (4.00, BCD theory), the present paper avoids the proof errors that sank that paper but has experimental confounds instead. Against h7GAgbLSmC.md (7.00), that paper's theory is carefully scoped to smooth activations without claiming applicability to ReLU, whereas the present paper claims theoretical guarantees that do not formally cover its own experiments.

*Final placement:* The paper's genuine contributions (convexity connection, eigenvalue analysis, broad task coverage) are meaningful, but the uncontrolled comparison fundamentally weakens the central empirical claim, the missing classification accuracy for CIFAR is a significant evidential gap, and the theory-practice gap in convergence theorems prevents the theory from supporting the experiments as claimed. These issues together place it below acceptance threshold. Score 4.5 — between the 4.00 and 5.00 anchors — reflecting a paper with identifiable merit that nonetheless has structural weaknesses that prevent its core claims from being adequately supported.