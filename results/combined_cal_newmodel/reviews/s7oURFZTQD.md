Now let me write the final review.

## Summary

This paper analyzes multi-grade deep learning (MGDL), which trains shallow networks sequentially on the residuals of previous grades, comparing it to standard end-to-end single-grade deep learning (SGDL). The paper provides convergence theorems for GD in both settings, shows that when each grade uses a single ReLU layer the problem reduces to a sequence of convex subproblems, analyzes eigenvalue distributions of the iteration matrix to explain MGDL's stability, and presents experiments across image regression, denoising, deblurring, CIFAR-10/100 classification, and transformer-based time series.

## Strengths

- **Broad empirical evaluation across multiple modalities.** The paper evaluates MGDL on image regression, denoising, deblurring, CIFAR-10/100 classification, and transformer-based time series within a single paper. This breadth demonstrates that the approach extends beyond a single task type.
- **Insightful eigenvalue visualization (Section 7).** Showing that the smallest eigenvalue of the iteration matrix I−ηH falls below −1 for SGDL but stays within (−1,1) for MGDL provides a plausible mechanistic hypothesis connecting a measurable quantity (Hessian spectrum) to a qualitative training behavior (oscillations vs. smooth decay).
- **Clean convex decomposition result (Theorem 3).** Connecting MGDL with single-layer ReLU grades to a sequence of convex subproblems via Pilanci & Ergen (2020) is a clean extension from shallow to deep architectures, and the paper correctly identifies and credits the prior work.

## Weaknesses

### Major

1. **Central claim (α_l ≪ α) is asserted without proof.** Line 112 states that the Hessian spectral norm at each MGDL grade is "much smaller" than the full network's (α_l ≪ α), and uses this to claim a broader admissible learning-rate range. This claim is essential to the theoretical contribution but is never formally justified. Without a bound relating α_l to the shallower grade's depth/width versus the full network's α, this part of the theoretical argument is incomplete.

2. **Experimental comparisons are not controlled for model capacity, especially for transformers.** The paper never reports total parameter counts for any method. For the Transformer experiments (Section 8), SGT uses "a deep stack" of blocks while MGT uses "a single block" per grade. The dramatic gaps (TeMSE of 0.16 vs. 2.6 in Table 4; 0.018 vs. 0.089 in Table 5) could be driven by architectural capacity differences rather than the training strategy. While the image regression/denoising comparisons appear to match total hidden-layer depth between SGDL and MGDL (e.g., SGDL 8 hidden layers vs. MGDL 4 grades × 2 hidden layers), parameter counts are still not reported, making it impossible to fully assess fairness.

3. **CIFAR classification experiments do not report accuracy.** The paper uses MSE loss for CIFAR-100 and CIFAR-10 classification (non-standard for classification) and claims MGDL "delivers superior accuracy" (line 225), but never reports actual classification accuracy. Only loss values are reported. Accuracy is the most interpretable metric for these benchmarks, and its absence is a significant omission.

4. **Eigenvalue analysis for ReLU networks is on questionable mathematical ground.** The Hessian of a ReLU network is not well-defined (ReLU is piecewise linear with zero second derivative almost everywhere and undefined at 0). The theorems assume σ is twice continuously differentiable, yet the experiments use ReLU. Computing "explicit Hessians" for ReLU networks and analyzing eigenvalues of I−ηH relies on quantities that are zero almost everywhere. The paper defers to the Supplementary Material but does not resolve this fundamental issue.

### Minor

5. **Linearization in the eigenvalue analysis (Section 7) is heuristic.** The Taylor expansion ∂F/∂W(W^k) = H_F(W^{k-1})W^k + u^{k-1} + r^{k-1} is a non-standard rearrangement. Theorem 4 establishes convergence of the linearized system when ∥I−ηH∥<1, but the link between the linearized dynamics and the original nonlinear GD is not rigorously established. The analysis is suggestive but not a proof.

6. **The convex program (Theorem 3) is not practically solvable.** The theorem requires m_l ≥ P_l, where P_l is the number of possible activation patterns — O(N^r) in practice and exponential in worst case. The paper does not discuss this combinatorial explosion or acknowledge that Eq. 8 is not practically solvable.

7. **Overstated novelty of convergence theorems.** Theorems 1 and 2 are standard GD convergence results for smooth nonconvex functions (η < 2/L condition), extended from Xu (2025) to include nonzero biases. While the extension is valid, the paper presents these as key contributions when they are standard results.

8. **No statistical significance or variance reporting.** Tables 1–5 report single numbers without standard deviations or confidence intervals. Results cannot be assessed for reliability.

9. **Use of 10^6 training epochs.** The synthetic and image regression experiments (lines 243, 245) use 10^6 epochs, far beyond what is practical. It is unclear whether MGDL's advantages persist under realistic training budgets.

## Nice-to-Haves

- The paper could be strengthened by first analyzing linear networks (where the Hessian is well-defined) and then presenting ReLU experiments as suggestive evidence rather than direct verification of the eigenvalue mechanism.
- Providing a formal bound for α_l ≪ α, or softening the claim to be conditional, would improve the theory's integrity.
- An ablation study controlling for total parameter count by testing SGDL with the same total depth as the sum of MGDL grades would help isolate the effect of the training strategy.
- Situating MGDL more explicitly within the literature on sequential additive training (e.g., gradient boosting, greedy layer-wise training) would clarify what is novel.

## Removed Points

These points were raised in the input but removed after cross-checking against the paper:

- **Missing related works (gradient boosting, AdaBoost):** The paper cites Bengio et al. (2006) and the broader literature. While the differentiation could be stronger, the paper does not wholly ignore these connections.
- **PSNR gains are modest:** Gains of 0.16–4.23 dB are non-trivial for image reconstruction. Removed.
- **MGDL also oscillates:** The paper explicitly acknowledges this (line 158: "MGDL oscillates initially but stabilizes in later stages"). Removed.
- **Compactness assumption is circular:** This is standard in optimization analysis. Removed.
- **Section 6 LR analysis confounded:** The paper matches total hidden-layer depth (SGDL: 8; MGDL: 4×2=8) in those experiments, reducing the confound's severity. Removed the strong version of this criticism.
- **Missing appendix with architecture definitions:** Parser artifact — those exist in the original submission. Removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report total parameter counts for SGDL and MGDL in every experiment, or design controlled experiments where total capacity is matched.
2. Report classification accuracy (top-1 or top-5) on CIFAR-10 and CIFAR-100, not just MSE loss.
3. Provide a formal bound or proof for the α_l ≪ α claim, or soften the theoretical claims to be conditional.
4. Use generalized Gauss-Newton matrices instead of Hessians for the eigenvalue analysis of ReLU networks, or analyze linear networks first.
5. Report variances/confidence intervals for all experimental results.

---

**Calibration Summary:** This review was calibrated against 8 anchor papers retrieved across two rounds. The closest anchors were: (a) n2RIkaf1S4 — Block Coordinate Descent for Neural Networks (avg 4.00, Reject), a sequential-training paper with theory + experiments similar in structure, whose most negative item (favorability -1.44) is comparable to our paper's most negative items; (b) O0FOVYV4yo — GD convergence for linear networks (avg 5.00, Reject), with cleaner theory but more incremental contribution (favorability -1.86); (c) nSYycd5tEC — Sequential vs. concurrent replay (avg 4.00, Reject), sharing the theory+experiment gap weakness. Our paper sits slightly below the 5.0 papers because its central theoretical claim is unproven and its experimental design has unresolved confounds, but above the ~2.8 papers due to its breadth and the eigenvalue diagnostic insight. The round-1 bracket was 3.0–5.0; round-2 narrowed to 3.5–4.5; the final score of 4.0 is anchored by the structural similarity to the BCD paper (n2RIkaf1S4, 4.00) and the replay paper (nSYycd5tEC, 4.00).

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>