Here is the final consolidated review:

---

## Summary

This paper proposes a theoretical and empirical analysis of Multi-Grade Deep Learning (MGDL), which trains shallow networks sequentially on residual targets, compared to standard end-to-end (single-grade) deep learning (SGDL). The paper presents convergence theorems for GD on MGDL, a convex reformulation for ReLU networks with single-layer grades, eigenvalue-based stability analysis, and experiments on image regression, denoising, deblurring, CIFAR-10/100, and time-series transformers.

## Strengths

**1. Consistent PSNR improvements on image reconstruction tasks (Tables 1–3).** MGDL beats SGDL across all six image regression settings (0.42–3.94 dB), all six denoising noise levels (0.16–4.23 dB), and all three deblurring kernel sizes (0.85–2.84 dB). The pattern is clear and consistent across tasks. **[favorability=13.43]**

**2. Convex reformulation for single-layer ReLU grades (Section 4, Theorem 3).** The connection to Pilanci & Ergen (2020) — showing that when each MGDL grade uses a single ReLU hidden layer, the nonconvex problem decomposes into a sequence of convex subproblems — is a genuine theoretical insight. The proof sketch is clear and the connection is non-obvious. **[favorability=16.58]**

**3. Eigenvalue analysis (Section 7) provides a compelling mechanistic explanation.** The figures showing eigenvalues of I−ηH crossing −1 for SGDL but staying within (−1,1) for MGDL give a clear visual story for why MGDL avoids oscillatory training. **[favorability=11.43]**

**4. Learning rate robustness study (Section 6).** MGDL is shown to be effective over a wider range of learning rates than SGDL on both synthetic and real tasks, supporting the claimed practical advantage. **[favorability=11.91]**

**5. Broad experimental scope.** The paper tackles image regression, denoising, deblurring, CIFAR-10, CIFAR-100, synthetic data regression, and time-series forecasting with transformers, demonstrating the framework is not narrowly applicable. **[favorability=7.48]**

## Weaknesses

### Fatal
None.

### Major

**1. No classification accuracy reported despite repeatedly claiming superior accuracy.** The abstract, introduction, and conclusion claim MGDL achieves "better accuracy" on CIFAR-10 and CIFAR-100, but neither experiment reports any classification accuracy metric. CIFAR-100 (lines 223–227) reports only training MSE loss curves. CIFAR-10 (line 289) reports only MSE loss on a 20% subset using a fully connected network. Training loss is not classification accuracy. The paper explicitly claims to evaluate "in terms of both accuracy and training dynamics" (line 223) yet provides no accuracy numbers. For a paper whose abstract and contribution list prominently advertise CIFAR-10/100 classification, this is a significant gap between claims and evidence. **[favorability=-2.61]**

**2. Theorems 1, 2, and 4 are standard gradient descent convergence results, not novel theoretical contributions as claimed.** Theorem 1 is the textbook GD convergence guarantee for smooth nonconvex objectives (if η < 2/α, GD converges to a stationary point). Theorem 2 is the same result applied per grade — structurally identical. Theorem 4 restates the contraction condition for a linearized iteration (if ||I−ηH|| < 1, the linearized scheme converges). The paper's claimed novelty hinges on the assertion that α_l ≪ α (line 112), meaning each grade's Hessian spectral norm is much smaller than the full network's. This assertion is stated without proof, formal bound, or empirical measurement. Without substantiation of α_l ≪ α, Theorems 1 and 2 contribute analysis but no novel theory. **[favorability=-4.90]**

**3. The P_l scaling requirement in Theorem 3 makes the convex reformulation impractical without discussion.** Theorem 3 requires m_l ≥ P_l, where P_l is the number of distinct activation patterns induced by X_l — exponential in the data dimension (the number of possible dichotomies of N points in d_l dimensions). For N=50,000 (CIFAR-100) and d_l=3072, P_l is astronomically large, far exceeding any practical number of neurons. The paper presents this as "extending convexification from shallow to deep architectures" (line 148) but does not discuss that the condition is unsatisfiable in any realistic setting or propose a relaxation. **[favorability=-2.32]**

**4. The CIFAR-10 experiment uses a nonstandard protocol that does not connect to the literature, and contradicts the paper's own claim about using CNNs.** The CIFAR-10 experiment (line 289) uses: (a) only 10,000 sampled images (20% of the training set), (b) fully connected networks (not CNNs — despite line 154 claiming "For classification, we use convolutional neural networks (CNNs)"), (c) squared error loss (not cross-entropy), and (d) reports only MSE loss, not accuracy. No CNN classification result with accuracy is presented anywhere in the paper, despite the abstract claiming to cover CNNs for CIFAR-10/100. **[favorability=-1.49]**

**5. The SGDL vs MGDL comparison is confounded by architecture differences.** In every experiment, SGDL and MGDL use different architectures (e.g., SGDL (2,1,128,8) vs MGDL (2,1,128,2,4) for image regression; SGDL (2,1,128,12) vs MGDL (2,1,128,3,4) for denoising). The improvement could partly reflect that training shallow networks is easier than training deep ones. The paper includes no controlled ablation where the same total architecture is trained both end-to-end and multi-grade. This conflates the multi-grade training procedure with architectural differences. **[favorability=-0.47]**

### Minor

**6. Internal inconsistency in CIFAR-100 learning rates.** The main text (line 225) states learning rates 5×10⁻⁴ and 1×10⁻⁴, but the figure caption (line 233) states η=5×10⁻⁵ for the first two panels and η=1×10⁻⁴ for the last two — a 10× discrepancy for the first learning rate. **[favorability=3.56]**

**7. The transformer experiments (Section 8) show very large gaps (SGT TeMSE 2.6 vs MGT 0.16 — a 16× gap on synthetic data) that suggest the SGT baseline may be poorly configured.** The paper attributes this to distribution shift but provides no tuning details for the SGT baseline. Withhold this as a major criticism since it is somewhat speculative without access to the full experimental setup. **[favorability=5.94]**

**8. Gap between theory and practice regarding activation smoothness.** Theorems 1, 2, and 4 assume σ is twice continuously differentiable, but all experiments use ReLU activations, which are not differentiable at 0. The paper acknowledges this only implicitly (line 60 references Xu (2025) which handles the zero-bias case) but does not clearly justify why the theory applies to ReLU-based experiments. **[favorability=4.41]**

### Trivial
None.

## Nice-to-Haves

- Add controlled ablation keeping architecture fixed and varying only training method (end-to-end vs. multi-grade).
- Provide formal bounds or at least systematic empirical measurements of α_l relative to α to substantiate the claimed wider learning rate range.
- Discuss the P_l scaling limitation of Theorem 3 explicitly and propose practical relaxations.
- Compare against greedy layer-wise pretraining (Bengio et al., 2006) and residual networks (ResNets), which are conceptually related.
- Report variance/error bars across runs.

## Removed Points

These points were raised in the input review but are removed for the reasons given:
- "No comparison to existing iterative training methods (greedy layer-wise pretraining, ResNets)": This is reasonable but falls under "nice-to-have" rather than required for validity. The paper explicitly scopes itself as MGDL vs SGDL.
- "No statistical significance or error bars": This is nonstandard for PSNR-based image reconstruction evaluations in this literature. Moved to nice-to-have.
- "Architecture details relegated to appendix": The parser strips appendices from all papers. Not a valid criticism of the original submission.
- Various formatting/style nitpicks: parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the disconnect between claimed contributions (especially regarding classification and theory novelty) and what the paper actually demonstrates, but do not add new analytical insights beyond what the authors themselves present.

## Suggestions

1. Report classification accuracy (top-1%) on CIFAR-10 and CIFAR-100 using standard CNN architectures with both SGDL and MGDL matched for total parameter count. Alternatively, honestly reframe the contribution around what the experiments actually demonstrate (image reconstruction).
2. Add a controlled ablation keeping total architecture fixed and varying only whether training is end-to-end or multi-grade, to isolate the benefit of the sequential training framework from the benefit of training shallower networks.
3. Provide a formal bound or empirical measurement of α_l relative to α.
4. Discuss the P_l scaling limitation in Theorem 3 explicitly.
5. Resolve the learning rate discrepancy in Figure 3 (5×10⁻⁴ vs. 5×10⁻⁵).

## Score and Decision

**Round-1 bracket:** The paper sits above score-3.40 anchors (narrow experiments, weak theory) but below score-5.75 anchors (rigorous theory or well-focused empirical contributions). Closest comparative anchor is zPaTnGjgpa (4.20), which shares the pattern of interesting empirical observations about GD stability paired with theoretical contributions that don't fully deliver on their promises.

**Placing within bracket:** The current paper's strongest items (convex reformulation favorability 16.58, PSNR improvements 13.43) are materially stronger than zPaTnGjgpa's best items (~10-12 favorability). However, its worst items (theorems are standard at -4.90, missing classification accuracy at -2.61) are more damaging than zPaTnGjgpa's worst items (around -3 to -1). The combined weight of five MAJOR weaknesses against five strengths narrows the gap to and slightly above zPaTnGjgpa (4.20) but clearly below JslyktsKMY (5.75) and UMOlFJzLfL (5.75).

**Final score: 4.5** — Borderline reject. The paper establishes a genuine empirical finding (MGDL produces more stable training and better PSNR on image reconstruction) and the convex reformulation is a real theoretical insight. However, the gap between advertised contributions and demonstrated evidence is too wide: classification accuracy is claimed but never reported, standard convergence theorems are presented as novel, and key experimental comparisons confound method with architecture. A major revision addressing these issues could strengthen the paper considerably.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>