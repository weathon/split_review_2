## Summary

This paper proposes Multi-Grade Deep Learning (MGDL), which decomposes a deep network into sequential shallow training stages ("grades"), each trained on residuals of previous grades. It provides convergence analysis for GD applied to MGDL (Theorems 1, 2, 4), a convexity result for single-layer ReLU grades (Theorem 3), an eigenvalue analysis linking training stability to spectral properties, and experiments on image regression, denoising, deblurring, CIFAR-10/100 classification, and time series using FCNs, CNNs, and Transformers.

---

## Strengths

1. **Clean architecture with clear motivation.** The MGDL decomposition into grades that train shallow networks on residuals of previous grades (Eq. 3–4, Figure 1) is well-motivated, parallels ideas from boosting and iterative refinement, and is clearly presented.

2. **Theorem 3 (convex decomposition) is a genuine theoretical bridge.** Adapting Pilanci & Ergen (2020) to show that each MGDL grade with a single ReLU layer reduces to a convex program (Eq. 7–8, Theorem 3) is a non-trivial theoretical contribution that extends convexification from shallow to deep architectures. The proof sketch (line 146) is concise and correct.

3. **Eigenvalue analysis provides a compelling mechanistic explanation for MGDL's stability advantage.** Tracking eigenvalues of \(\mathbf{I} - \eta\mathbf{H}_{\mathcal{L}}(W)\) during training (Figures 4–6) and showing that SGDL's eigenvalues exit \((-1,1)\) while MGDL's remain inside is the strongest explanatory contribution of the paper, directly linking training dynamics to the observed stability difference.

4. **Broad experimental scope across architectures and tasks.** The paper tests MGDL on image regression, denoising, deblurring, CIFAR-10, CIFAR-100, synthetic time series, and financial time series using FCNs, CNNs, and Transformers — giving confidence that the reported benefits are not confined to a single architecture or task.

5. **Learning rate robustness analysis (Section 6) is well-designed.** The synthetic data experiments (Figure 2) cleanly demonstrate that MGDL tolerates a wider range of learning rates than SGDL, with the admissible range quantified (e.g., \(\eta \in [0.01, 0.3]\) for MGDL vs. \([0.03, 0.08]\) for SGDL in Setting 1). This is the paper's strongest empirical contribution.

---

## Weaknesses

### Fatal
None.

### Major

1. **No test accuracy reported for CIFAR-10 or CIFAR-100 classification.** The paper claims MGDL achieves "superior accuracy" on classification (line 225, line 289) and states it is "evaluating SGDL and MGDL in terms of both accuracy and training dynamics" (line 223). Yet it reports only training loss curves (Figure 3) for CIFAR-100 and training loss + training time for CIFAR-10 (lines 289–291). No test accuracy, top-1/top-5 error, precision, or any standard classification metric is reported anywhere in the paper — a grep for "test accuracy" returns zero matches. Additionally, CIFAR-100 uses MSE loss (line 223) rather than cross-entropy, an unusual choice that is not justified. Without test accuracy, the claim that MGDL "outperforms" SGDL on classification is unsupported by the evidence presented, which undermines a significant part of the experimental contribution.

2. **Theory–practice gap in convergence theorems.** Theorems 1, 2, and 4 assume \(\sigma\) is "twice continuously differentiable" (lines 70, 104, 255), but every experiment uses ReLU activations (line 36, line 154). The paper does not acknowledge this gap or provide a bridging argument (e.g., subgradient framework, smooth approximation, or empirical justification). The abstract's claim of "rigorous theoretical guarantees" (line 10) is overstated given that the core assumption of the convergence theory is violated in every empirical setting. While this gap is common in ML theory papers, the failure to even mention it weakens the claimed theoretical grounding.

3. **Transformer (SGT) baseline raises fairness concerns.** In Table 4, SGT achieves a test MSE of 2.6 on synthetic time series vs. MGT's 0.16, and the paper reports SGT predictions "diverge sharply" (Figure 7). A test MSE of 2.6 suggests the model has effectively failed (worse than predicting the mean). The paper attributes this to SGT "collaps[ing] under distribution shift" (line 332), but provides no hyperparameter tuning details, learning rate sweeps, or evidence that SGT was reasonably configured. Without this information, the comparison (including the claim that MGT requires "only 28% of the training time") cannot be interpreted as a fair apples-to-apples comparison.

### Minor

4. **No statistical uncertainty reported for any result.** Every result in Tables 1–5 and every figure appears to come from a single run, with no error bars, standard deviations, or mention of random seeds. For the image tasks, the qualitative pattern is consistent across many images, partially mitigating this concern. But for the CIFAR and Transformer results, a single run means the reported advantage could reflect chance variation in initialization or data splits.

5. **Convexity result (Theorem 3) is never empirically validated.** The paper proves that with single-layer ReLU grades, each grade reduces to a convex program (Eq. 8), but all experiments train the *nonconvex* formulation (Eq. 7) via Adam/GD. The convex equivalence is never solved, validated, or compared against nonconvex training. The abstract's claim that MGDL "reduces a highly nonconvex problem to a sequence of convex subproblems" (line 10) describes what is *theoretically possible* under specific conditions, but the paper never demonstrates this reduction in practice.

6. **Model capacity not explicitly verified across comparisons.** The paper asserts "assuming comparable layer and neuron counts" (line 96), and the architectures (Eq. 26/27 in the appendix) suggest comparable total depth (e.g., 4 grades × 2 hidden layers = 8 vs. SGDL's 8 hidden layers for image tasks). However, total parameter counts and FLOPs are never reported, making it impossible for readers to fully verify the comparisons are apples-to-apples.

### Trivial
None.

---

## Nice-to-Haves

- Report test accuracy (top-1 and top-5) for CIFAR-10 and CIFAR-100.
- Add error bars or variance information from multiple random seeds (even 3) to the main quantitative results.
- Include hyperparameter tuning details for the SGT baseline to verify it was reasonably configured.
- Report total parameter counts and inference FLOPs for each SGDL/MGDL architecture pair.
- Conduct a small-scale experiment solving the convex program from Theorem 3 to validate the theoretical equivalence in practice.
- Acknowledge the smooth-activation assumption gap explicitly and provide a heuristic justification or subgradient-based extension for ReLU.

---

## Removed Points

These points were flagged for removal but are preserved here for traceability:

- **"The convergence theorems (1, 2, 4) are textbook results"** — This criticism was partially correct but the paper does adapt them to the MGDL setting, and the novelty claim is about the framework-level observation, not the theorems themselves. The criticism is somewhat standard for applied-theory papers and does not add new information beyond the theory-practice gap already noted in weakness 2.

- **"The condition \(m_l \geq P_l\) for Theorem 3 may be prohibitive for large datasets"** — This is a standard limitation that is present in the source (Pilanci & Ergen, 2020) as well; singling it out as a weakness without testing whether it is actually prohibitive is speculative.

- **"The eigenvalue analysis assumes the linearization is valid but does not verify this empirically"** — The linearization (neglecting the remainder \(r^{k-1}\)) is a standard analytical simplification; verifying it would require its own paper and is not standard practice. The correlation between eigenvalue behavior and observed loss dynamics (Figures 4–6) already provides empirical support.

- **"The CNNs are not described in the main text"** — Architectures are referenced by equation numbers (Eq. 28, 29) that point to the appendix, which is standard for papers with space constraints.

- **"The CIFAR-100 experiment uses MSE loss rather than cross-entropy"** — Noted in weakness 1; no need for separate mention.

- **Pure formatting/style nitpicks** from the harsh critic removed as per instructions.

---

## Novel Insights

None beyond the paper's own contributions. The harsh critic and strength finder did not surface any observation about the paper that the paper itself does not already state or imply.

---

## Suggestions

1. **Report test accuracy for CIFAR-10 and CIFAR-100.** This is the single highest-impact fix. Without it, the classification experiments are uninterpretable and the claim of MGDL "outperforming" SGDL on classification is unsupported.

2. **Address the SGT baseline concern explicitly.** Add a section showing that SGT was reasonably tuned (e.g., via a learning rate sweep or hyperparameter grid). If SGT genuinely fails on these tasks despite proper tuning, that is itself an interesting finding that deserves deeper investigation rather than a brief mention.

3. **Add multiple random seeds with error bars** to the most important quantitative results (Tables 1–3, 4–5). Even 3 seeds would substantially strengthen the evidence.

4. **Acknowledge the smooth-activation assumption gap** in Theorems 1, 2, and 4. A brief note that the theory covers smooth activations while the experiments use ReLU (which is common in practice but outside the strict scope of the theorems) would suffice, along with a heuristic justification or reference to non-smooth analysis frameworks.

---

## Score and Decision

### Calibration Anchors

**Round 1 (Bracketing):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/u1cQYxRI1H.md | 0.50 | R1 | Illumination harmonization; very different topic, not comparable |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/nSDOkm0SKo.md | 1.00 | R1 | Financial news analysis; rejected, not comparable |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NbbsRnPBoS.md | 2.33 | R1 | Deep linear networks; rejected for narrow scope — our paper has broader scope |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Zap3nZhRIQ.md | 3.00 | R1 | Non-differentiability in NNs; rejected as disconnected/superficial — our paper has more coherent narrative |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/n2RIkaf1S4.md | 4.00 | R1 | BCD for neural networks; rejected for circular argument — our paper has cleaner theory |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6Ey8mAuLiw.md | 5.25 | R1 | Multitask representation learning; rejected for oversimplification — our paper has more realistic experiments |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/25j2ZEgwTj.md | 6.00 | R1 | Teacher-student ReLU dynamics; accepted — stronger theory but narrower scope |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/h7GAgbLSmC.md | 7.00 | R1 | Sharper guarantees for neural network classifiers; accepted — stronger, more rigorous theory |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4xWQS2z77v.md | 8.00 | R1 | Loss landscape of regularized NNs via convex duality; accepted — much stronger theory |

**Round 2 (Narrowing):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/59r0ntInvF.md | 4.67 | R2 | Image restoration training strategy; rejected — similar experimental breadth, narrower theory |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/AKMOrcobBE.md | 4.33 | R2 | Image restoration dataset/attention; rejected — narrower contribution |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ONWLxkNkGN.md | 5.25 | R2 | Blind image restoration with diffusion; rejected — stronger empirical results |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/z8PcUSKXXN.md | 5.75 | R2 | Image denoising with random noise injection; accepted — cleaner empirical story |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/x7d1qXEn1e.md | 6.25 | R2 | Restoration network as implicit prior; accepted — stronger theory + empirical results |

### Initial Bracket and Final Score

**Round 1 bracket:** 3.5 – 5.5 (between the "disconnected/superficial" paper at 3.0 and the accepted theory papers at 6.0+)

**Round 2 narrowing:** The paper shares characteristics with the 4.33–5.25 range — it has broader experimental scope than the 4.00 BCD paper but has a significant evidence gap (missing test accuracy) that the 5.25 and 5.75 papers do not. The missing test accuracy and SGT baseline concerns prevent it from reaching the 5.5+ range.

**Final score:** 4.5. The paper has genuine contributions (clean MGDL formulation, convexity connection, eigenvalue analysis, broad experimental coverage) but the missing test accuracy for CIFAR classification, the theory-practice gap, and the insufficiently documented SGT baseline prevent the central claims from being fully supported. The paper could be substantially strengthened with targeted revisions; the current version does not meet the acceptance bar.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>