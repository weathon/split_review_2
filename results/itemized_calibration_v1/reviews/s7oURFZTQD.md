## Summary

This paper proposes Multi-Grade Deep Learning (MGDL), which decomposes end-to-end training of a deep network into sequential training of shallow "grades" on residuals. The authors provide convergence analysis (Theorems 1-2, standard GD convergence results re-stated for SGDL and MGDL), show that single-layer ReLU grades reduce to convex subproblems (Theorem 3, adapting Pilanci & Ergen 2020), and analyze eigenvalue distributions of the iteration matrix (Theorem 4) to explain MGDL's stability. Experiments on image regression, denoising, deblurring, CIFAR classification, and time-series transformers show MGDL achieving lower loss and more stable training than end-to-end baselines.

## Strengths

- **Empirical eigenvalue diagnostic (Section 7, Figures 4–6).** The paper tracks eigenvalues of I − ηH during GD training and shows that MGDL's smallest eigenvalues stay within (−1,1) while SGDL's drop below −1, correlating with loss oscillations. This is a clean, verifiable diagnostic connecting Hessian structure to training stability that practitioners could monitor.

- **Transformer extension with substantial gains (Section 8, Tables 4–5).** MGT achieves significantly lower test MSE (0.16 vs 2.6 on synthetic; 0.018 vs 0.089 on SPX) with only 28–33% of the training time, demonstrating that the MGDL principle extends to transformer architectures with practically meaningful improvements.

- **Broad empirical coverage across domains and architectures.** The paper evaluates MGDL across image regression, denoising, deblurring, synthetic regression, CIFAR classification, and financial time-series, using fully-connected networks, CNNs (stated, architectures in appendix), and transformers. This breadth supports the generality claim.

## Weaknesses

### Major

1. **CIFAR classification evaluates only MSE loss while claiming "superior accuracy."** The CIFAR-100 and CIFAR-10 experiments (Sections 5, 7) report only MSE loss, yet the paper states "MGDL delivers superior accuracy" (line 225) and "MGDL consistently outperforms SGDL" on classification (line 227). For multi-class problems, lower MSE does not imply higher classification accuracy (e.g., a model could be closer in Euclidean distance to one-hot targets but wrong on argmax). No classification accuracy, top-1 error rate, or any classification-specific metric is reported. This is a mismatch between claim and evidence — the headline claim about classification is unsupported.

2. **Core theoretical advantage (α_l ≪ α) is asserted without proof or bound.** The paper's claimed theoretical distinction between SGDL and MGDL hinges on the statement (line 112) that MGDL's per-grade Hessian spectral norm α_l is "substantially smaller" than SGDL's α, enabling larger admissible learning rates. This claim is never derived, bounded, or linked to network depth or width — it is simply stated. Without it, Theorems 1 and 2 are the same standard GD convergence condition (η < 2/α) applied to two different architectures, offering no insight into why one should admit larger learning rates. The paper's eigenvalue analysis provides empirical support for this claim but no theoretical justification.

### Minor

3. **No variance or statistical significance reported.** No experiment reports standard deviations, confidence intervals, or multiple-run statistics. Some PSNR gains are modest (e.g., Cameraman: 25.21 vs 24.79 = +0.42 dB), and without variance estimates the reader cannot assess reliability.

4. **No capacity/compute controls for the core image experiments.** The paper does not report parameter counts, FLOPs, or wall-clock time for the image regression/denoising/deblurring experiments (time is reported only for transformers). Without such controls, it is unclear whether MGDL's advantages stem from its multi-grade structure or from differing model capacity.

5. **Eigenvalue claim is partially inconsistent.** For synthetic data, the paper states (line 265) that MGDL's "largest [eigenvalues] stay slightly above 1," meaning the spectral radius is not strictly within (−1,1). Yet for CIFAR-10 (line 289) it claims eigenvalues are "strictly within (−1,1)." The general claim that MGDL eigenvalues are within (−1,1) (made in the abstract, introduction, and conclusion) is not uniformly supported — it holds for the smallest eigenvalues but not uniformly for all.

### Trivial

6. Several figure captions have duplicated text (parser artifact, not author error).

## Nice-to-Haves

- Prove or bound the α_l ≪ α claim, even with a simple depth-dependent bound for a restricted architecture class — this would substantially strengthen the theoretical contribution.
- Report classification accuracy (top-1 error) on CIFAR-100 and CIFAR-10. If the accuracy numbers support the MSE trends, this straightforwardly fixes the largest evidential gap.
- Include variance estimates from multiple runs for the main comparisons.
- Report parameter counts and wall-clock time for at least one image experiment to control for capacity.

## Removed Points

These points are flagged to be removed from the input review; treat with caution:

- **CNN claim not matching evaluation (from Harsh Critic #3).** The reviewer states CNNs are not described in the main text. However, the paper explicitly states "For classification, we use convolutional neural networks (CNNs)" (line 154) and references architecture equations 28-29 in the appendix. Per the rules, missing appendix content (including architecture equations) should not be penalized — they exist in the original submission. The paper does cover CNNs as claimed.

- **Missing related work comparisons (boosting, greedy layer-wise training).** Per instructions, I cannot flag missing citations as a weakness since external sources to confirm their existence are not available.

- **Theory-experiment optimizer gap (GD theory vs Adam experiments).** The paper uses GD in the eigenvalue analysis (Section 7) and learning rate study (Section 6), and uses Adam for the main image experiments. The theory is specifically about GD, and the eigenvalue analysis is conducted under GD. This concern is partially addressed by the paper's own structural separation.

- **Edge of Stability framing.** The reviewer notes the eigenvalue analysis (eigenvalues below −1 → oscillation) differs from the Edge of Stability regime (eigenvalues above 2/η). This is a framing observation rather than a technical flaw; the paper mentions EoS briefly in the introduction but does not claim its analysis resolves EoS.

- **10⁶ epochs being implausible.** These are synthetic analysis experiments designed to study long-term eigenvalue dynamics, not a practical training recommendation.

- **Generic or unfalsifiable criticisms** about the paper needing "theoretical justification" for features already empirically demonstrated (e.g., eigenvalue diagnostic) are not retained as specific weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report classification accuracy (top-1 error rate) on CIFAR-100 and CIFAR-10. If accuracy mirrors MSE trends, this fixes the most conspicuous evidential gap.
2. Add a bound or heuristic argument connecting grade depth to Hessian spectral norm, even for a simplified setting (e.g., the composition of two grades).
3. Include at least one controlled experiment matching parameter counts between SGDL and MGDL, and report wall-clock time for the image experiments.
4. Report standard deviations over multiple runs for the main PSNR and loss comparisons.
5. Be precise about eigenvalue claims: state "the smallest eigenvalues remain within (−1,1)" rather than "eigenvalues remain within (−1,1)" when the largest eigenvalues may slightly exceed 1.

---

**Final score calibration:** The paper is compared against three relevant calibration anchors. (1) *Can Stability be Detrimental?* (avg 4.20, Reject) — similar in being an empirical study of eigenvalue/dynamics with limited theory, but this paper has clearer empirical evidence across more tasks. (2) *Approaching Deep Learning through the Spectral Dynamics of Weights* (avg 6.25, Reject) — broader empirical scope but even weaker theory; this paper is comparable in empirical quality but significantly weaker than that paper in breadth. (3) *Learning Dynamics of Deep Matrix Factorization Beyond the Edge of Stability* (avg 7.00, Accept) — this paper is substantially weaker on theoretical rigor (standard results re-stated vs. novel proofs). The paper sits below the acceptance threshold due to the unsupported accuracy claim and unproven core theoretical assertion.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>