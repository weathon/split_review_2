Now I will produce the final consolidated review.

## Summary

This paper provides theoretical and empirical analysis of Multi-Grade Deep Learning (MGDL), which decomposes end-to-end training into sequential shallow subproblems trained on residuals. The paper offers convergence guarantees for MGDL, shows that single-layer ReLU MGDL reduces to a sequence of convex programs (extending Pilanci & Ergen 2020), analyzes eigenvalue distributions to explain training stability, and presents experiments across image regression, denoising, deblurring, CIFAR-10/100 classification, and transformer-based time series regression. The core thesis is that MGDL yields greater stability and broader learning-rate tolerance than standard end-to-end (SGDL) training.

## Strengths

1. **Convex reformulation of single-layer ReLU MGDL (Theorem 3, Section 4).** The paper shows that when each MGDL grade is a single-layer ReLU network, the nonconvex subproblem becomes a convex program. This extends the Pilanci & Ergen (2020) convexification from isolated shallow networks to a sequential composition of shallow networks (lines 144–148). The proof sketch is coherent.

2. **Learning rate robustness analysis (Section 6).** The synthetic regression experiment (lines 241–247, Figure 2) is well-designed and provides clear evidence that MGDL tolerates a substantially wider range of learning rates than SGDL. In Setting 2 (higher-frequency target), MGDL remains stable with loss < 0.01 for η ∈ [0.08, 0.3] while SGDL converges only at η ≈ 0.005. This is the paper's most unambiguous practical result.

3. **Breadth of evaluation domains.** The paper tests MGDL across image regression, denoising, deblurring, CIFAR-10/100, and transformers on time series, providing a multi-domain perspective uncommon in a single paper.

## Weaknesses

### Major

1. **CIFAR-10/100 classification claims are unsubstantiated: the paper reports only MSE loss, not classification accuracy.** The paper explicitly frames these as classification experiments (lines 20, 223) and claims "MGDL achieves superior stability and accuracy across both reconstruction and classification tasks" (line 154) and "MGDL delivers superior accuracy" (line 225). However, the only metric reported is MSE loss (Figures 3, 6). Lower MSE on a classification task does not imply better classification accuracy — it can reflect overfitting to the MSE objective at the expense of the decision boundary. Since the paper's central empirical claim includes "accuracy" on classification, the absence of accuracy metrics means this claim is unsupported by the evidence presented.

2. **No statistical characterization across any experiment.** All results in Tables 1–5 are single numbers with no standard deviations, no mention of random seeds, and no indication that experiments were repeated. The PSNR differences claimed (e.g., 0.42–3.94 dB in Table 1) could fall within typical run-to-run variation for neural network training. Even the large TeMSE gap between MGT (0.16) and SGT (2.6) in Table 4 cannot be assessed without knowing whether it is systematic or reflects a single unlucky SGT run. This is a basic methodological gap for a paper drawing comparative conclusions.

### Minor

3. **Transformer comparison lacks main-text architectural controls.** The SGT model uses an unspecified number of blocks *n_h* (line 297), while MGT uses 1 block per grade (line 311). Parameter counts, per-iteration compute, and the value of *n_h* are deferred to Appendix C. Without these quantities in the main text, the dramatic test-error differences (Table 4: TeMSE 0.16 vs. 2.6; Table 5: 0.018 vs. 0.089) cannot be cleanly attributed to the training strategy versus possible capacity differences. *Note: This is a presentation issue — the appendix exists in the original submission — but the main text should make the comparison interpretable on its own.*

4. **Practical scope of the convexity result (Theorem 3) is unclear.** The result requires *m_l ≥ P_l*, where *P_l* (the number of possible activation patterns) can be exponential in the input dimension (acknowledged via citations to Cover 2006 and Stanley et al. 2007, line 136). The paper does not discuss whether this condition ever holds in realistic settings or what guarantees obtain when *m_l < P_l*. This limits the result to a theoretical observation with uncertain practical import.

### Trivial

5. **Eigenvalue analysis on small networks (48 hidden units, line 285).** The eigenvalue diagnostics (Figures 4–6) use networks with 48 hidden units for computational tractability, but the paper does not discuss how these findings scale to larger architectures. This does not invalidate the analysis but limits its generalizability.

## Nice-to-Haves

- **Baseline comparison against conceptually related sequential-training methods** (e.g., greedy layer-wise training, which the paper cites at line 76). Comparing MGDL to another sequential decomposition would clarify what MGDL adds beyond existing strategies. This is outside the paper's stated scope (MGDL vs. SGDL) but would substantially strengthen the novelty claims.
- **Include one standard task-specific baseline** for image denoising/deblurring (e.g., BM3D for denoising) to contextualize the absolute PSNR values achieved by both SGDL and MGDL.

## Removed Points

These points from the input review were removed and are listed here for traceability. Treat them with caution.

- **Criticism about missing comparison against greedy layer-wise pre-training/boosting/ResNet methods:** The paper's stated scope is comparing MGDL vs. SGDL (single-grade = standard end-to-end training). Demanding comparison against all other sequential/residual methods is scope creep. The reviewer's framing that the paper "avoids the more informative question" sets a broader agenda than the paper claims. → Removed as scope creep per soft rules.
- **Criticism that Theorem 1 is a "textbook" result / "minor technical extension":** This is an observation about the theorem's novelty level, not a weakness of the paper. The paper explicitly states it "extends Theorem 6 in Xu (2025), which assumes zero biases" (line 60). The theorem serves its purpose as a reference point for the MGDL comparison. → Removed (not a genuine weakness).
- **Criticism about Section 4 proof sketch being too terse:** The full proof presumably exists in the appendix (which is stripped by the parser). → Removed per hard rule about appendix stripping.
- **Criticism about missing standard CV baselines (BM3D, Wiener filter, DIP):** The paper's contribution is comparing training paradigms (MGDL vs SGDL), not achieving SOTA on these tasks. → Removed as scope creep.
- **Criticism about Theorem 4 lacking smoothness/contractivity conditions:** The paper states F is "thrice continuously differentiable" and requires τ < 1 — these are the conditions the reviewer claims are missing. → Removed (factually incorrect; the conditions are stated at line 255).

## Novel Insights

None beyond the paper's own contributions. The strengths identified in the review (convex reformulation, learning-rate robustness study, eigenvalue stability analysis) all originate from the paper itself.

## Suggestions

- **Report classification accuracy (top-1, top-5) for CIFAR-10 and CIFAR-100.** This is the single most impactful fix, as it directly supports or retracts the paper's "accuracy" claims for classification.
- **Add multi-run statistics (≥ 5 seeds, reporting mean ± std) for all main tables.** Without this, the reader cannot distinguish signal from noise.
- **In the transformer experiments, report total parameter counts and the value of *n_h* for both SGT and MGT in the main text.** Ideally, control for total parameter count to ensure the comparison reflects training strategy rather than model capacity.
- **Discuss the practical regime where *m_l ≥ P_l* can hold, or clarify what guarantees apply when it does not.**

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>