Now I have all the information I need. Let me compose the final review.

## Summary

This paper proposes Multi-Grade Deep Learning (MGDL), which decomposes end-to-end deep network training into sequential shallow subproblems trained on residuals, and compares it to standard single-grade (end-to-end) training (SGDL). The authors provide three forms of analysis — convergence theorems, a convexity result for single-layer ReLU grades, and an eigenvalue-based stability analysis — along with experiments on image regression, denoising, deblurring, CIFAR classification, and time-series transformers.

## Strengths

- **Convexity connection for single-layer ReLU grades (Section 4, Theorem 3).** Showing that MGDL with single-layer ReLU grades decomposes into a sequence of convex subproblems is a genuine theoretical bridge to the Pilanci & Ergen (2020) line of work. This is the paper's cleanest and most interesting theoretical result, and it extends convexification from shallow to deep architectures in a well-motivated way.

- **Broad experimental scope.** The paper tests MGDL across image regression, denoising, deblurring, CIFAR-10/100, and time series with transformers — covering fully connected networks, CNNs, and transformers. The transformer extension (Section 8) is a non-trivial addition beyond the core fully-connected and CNN experiments.

- **Eigenvalue-based stability analysis (Section 7).** The consistent finding that MGDL's iteration-matrix eigenvalues remain within (-1,1) while SGDL's fall outside provides an intuitive and visually compelling explanation for oscillatory vs. stable training. Tying this to $\mathbf{I} - \eta \mathbf{H}_\mathcal{F}(W)$ and the Edge of Stability literature is a reasonable analytical choice.

## Weaknesses

### Fatal

None. While several weaknesses are serious, none unambiguously invalidate the paper's entire contribution when assessed from the paper as-written (e.g., the convexity result and eigenvalue analysis retain independent value even if the empirical comparison is weakened).

### Major

- **Architecture confound in all SGDL vs. MGDL comparisons.** In every experiment, SGDL and MGDL use different architectures (different depths, different numbers of hidden layers). For example: image regression uses SGDL depth 8 vs. MGDL depth 2 per grade (4 grades); denoising uses SGDL depth 12 vs. MGDL depth 3 per grade. The paper **never reports total parameter counts** for either method in any experiment. Without this information — and without at least one controlled comparison where the same architecture is trained end-to-end vs. decomposed into grades — it is impossible to determine whether MGDL's reported advantages come from the multi-grade training paradigm or simply from having a different (potentially better-suited) architectural configuration. This is the paper's most consequential weakness.

- **No test accuracy reported for CIFAR-10 or CIFAR-100 classification.** The abstract and contributions list CIFAR-10/100 classification as a key result, yet: (i) the CIFAR-100 experiment (Section 5) reports only training loss curves in a figure, with no test accuracy, test loss, or classification accuracy anywhere; (ii) the CIFAR-10 experiment (Section 7) uses only 10,000 sampled images, full-batch gradient descent, and reports only training loss and wall-clock time. The paper claims "superior accuracy" (line 225) without ever measuring accuracy. For classification benchmarks, test accuracy is the standard metric — training loss does not substitute for it.

- **Convergence theorems are standard results; the claimed MGDL advantage is unsubstantiated.** Theorem 1 is a textbook gradient-descent convergence result for smooth nonconvex objectives. Theorem 2 applies the same result to each MGDL grade. The paper asserts that MGDL's advantage follows because "$\alpha_l \ll \alpha$" (line 112), but no bounds on $\alpha_l$ vs. $\alpha$ are proved, and no empirical measurements of Hessian spectral norms across tasks are provided. Without this, Theorems 1 and 2 do not substantively distinguish MGDL from SGDL.

- **Theory-practice gap: all theorems assume twice-differentiable activations; experiments use ReLU.** Theorem 1 (line 70), Theorem 2 (line 104), and Theorem 4 (line 255) all require the activation function $\sigma$ to be twice continuously differentiable. ReLU, used throughout the experiments, is not even once differentiable at zero. The paper does not acknowledge or address this gap, meaning the theoretical framework technically does not cover the systems being empirically evaluated.

- **Internal contradiction about classification architectures.** Line 154 states "For classification, we use convolutional neural networks (CNNs)." However, the CIFAR-10 experiment (line 289) explicitly uses "fully connected ReLU networks." The CIFAR-100 architectures are deferred to the appendix. This inconsistency undermines trust in the experimental reporting.

### Minor

- **Eigenvalue analysis uses different (shallower) architectures and different learning rates than the main experiments.** Section 7 uses SGDL with depth 4 and MGDL with depth 1 per grade (line 285) — much shallower than the depth 8–12 networks used in the main performance comparisons. Different learning rates are used for SGDL and MGDL (η=0.08 vs. η=0.06 in Figure 4). The eigenvalue analysis therefore does not directly explain the actual empirical results from Sections 5–6; it demonstrates a property of different, shallower models.

- **No statistical evidence.** No experiment reports standard deviations, confidence intervals, or results from multiple random seeds. Given the well-known variance of neural network training outcomes, single-run results weaken confidence in the reported performance differences.

- **MGT vs. SGT transformer comparison does not control for total block count.** The paper states MGT uses "a single block" per grade while SGT uses "n_h" blocks (unspecified in main text). Without specifying n_h or controlling for the total number of transformer blocks across methods, the factor-of-3 training time advantage (Table 4) could reflect architectural differences rather than training paradigm advantages.

- **Convexity result's practical limitation unacknowledged.** Theorem 3 requires $m_l \geq P_l$, where $P_l$ (the number of possible activation patterns) can be $O(N^d)$ for $N$ data points of dimension $d$ — potentially exponential. The paper does not discuss this limitation.

## Nice-to-Haves

- Report parameter counts and FLOPs for every SGDL vs. MGDL comparison to address the architecture confound.
- For a cleaner comparison, take the same deep architecture and compare end-to-end training (SGDL) vs. decomposing it into grades (MGDL), holding total architecture constant.
- Report test accuracy for CIFAR-10 and CIFAR-100.
- Acknowledge the ReLU vs. twice-differentiable gap explicitly and discuss whether the theorems serve only as intuition or can be extended.
- Provide error bars (multiple random seeds) for the main comparisons.
- Clarify the CNN vs. fully-connected discrepancy and specify CIFAR-100 architectures in the main text.

## Removed Points

- **"No standard task-specific baselines for denoising or deblurring"** — REMOVED (scope creep). The paper's stated goal is to compare MGDL vs. SGDL, not to achieve SOTA on denoising benchmarks. Requesting BM3D/DnCNN baselines demands a different research question.
- **Section-by-section presentation notes** (notational density, proof sketch length, overselling in abstract) — REMOVED as style/presentation nitpicks without substantive content about correctness.
- **Generic or speculative weaknesses** (e.g., "could the metric be measuring a proxy") — REMOVED as category-driven noise without concrete anchoring in the paper.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a consistent structural concern (architecture confound) that the paper itself does not adequately address, but this is not a novel observation — it is a standard validity threat in controlled experiments.

## Suggestions

1. Report total parameter counts and FLOPs for every SGDL vs. MGDL comparison.
2. Report test accuracy for CIFAR-10 and CIFAR-100.
3. Add at least one controlled experiment where the same architecture is trained end-to-end vs. decomposed into grades.
4. Acknowledge the twice-differentiable vs. ReLU gap in the theory section.
5. Provide error bars from multiple random seeds for the main comparisons.

## Score and Decision

The paper tackles an interesting question and offers a genuine theoretical contribution in the convexity result (Theorem 3). The eigenvalue analysis is also a reasonable explanatory framework. However, the empirical evaluation — which the paper presents as a core contribution — has two critical and independently damaging weaknesses: (1) the architecture confound pervades every SGDL vs. MGDL comparison, making it impossible to attribute advantages to the training paradigm rather than to architectural differences, and (2) the classification results on CIFAR-10/100 (cited in the abstract and contributions) report no test accuracy whatsoever. Additionally, the convergence theorems are standard results oversold as novel, and the twice-differentiable assumption creates an unacknowledged gap between theory and practice. These weaknesses collectively prevent the paper from supporting its central claims with the required rigor.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>