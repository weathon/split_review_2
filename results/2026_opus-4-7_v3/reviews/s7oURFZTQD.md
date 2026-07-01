Let me read more of the paper to verify specific claims.Now I have a thorough understanding of the paper. Let me submit the draft review.Now let me proceed with Round 1 calibration — bracketing the score range.Let me read the most relevant anchor papers for calibration.Now I have good calibration data. Let me form my bracket.

**Round 1 bracket analysis:**

- **Strong reject (< 1.5)**: Papers like nSDOkm0SKo (1.0), gwZ90hFSL2 (1.0) are fundamentally flawed or pseudoscientific. The MGDL paper is far above this level — it's a real, coherent paper with genuine experiments.

- **Reject (1.5–3.5)**: NbbsRnPBoS (2.33, "Faster GD in Deep Linear Networks") was rejected for narrow scope and contrived examples. The MGDL paper is broader with more substantial experiments. Not this low.

- **Borderline reject (3.5–5.5)**: n2RIkaf1S4 (4.0, "Block Coordinate Descent for NNs") has a very similar profile: alternative training procedure with convergence theory, but circular arguments, theory-experiment gaps, and limited practical validation. zPaTnGjgpa (4.20, "Can Stability be Detrimental?") studies eigenvalue/stability analysis with limited novelty. LNYL96VIsD (4.75) studies learning rate sensitivity, rejected with mixed reviews. The MGDL paper shares many of these characteristics.

- **Borderline accept (5.5–7.5)**: sIE2rI3ZPs (7.0, "Central Flows") and J4Dvxv7WnG (7.0, "Deep Matrix Factorization Beyond EOS") have much stronger theoretical depth, rigorous analysis, and better connection between theory and experiments. The MGDL paper does not reach this level.

- **Accept (7.5+)**: 4xWQS2z77v (8.0, "Loss Landscape via Convex Duality") has thorough convex reformulation work far beyond the MGDL paper's Theorem 3.

**Initial bracket: 3.5 to 5.0.** The paper has interesting ideas and breadth but the theory-experiment disconnect, missing CIFAR test accuracy, and no parameter matching place it in the borderline reject range.

Now let me write the final consolidated review.

---

## Summary
This paper proposes Multi-Grade Deep Learning (MGDL), a sequential training paradigm that decomposes deep network training into successive "grades," each training a shallow network on the residuals from previous grades. The paper provides convergence theorems for GD (Theorems 1–2), a convexity result for single-layer ReLU grades (Theorem 3), eigenvalue analysis of the GD iteration matrix (Theorem 4 + empirical tracking), and experiments comparing MGDL to standard end-to-end training (SGDL) across image regression, denoising, deblurring, CIFAR-10/100, and time series tasks with fully connected networks, CNNs, and transformers.

## Strengths

- **Eigenvalue-tracking diagnostic provides a concrete, reproducible mechanistic signature (Section 7, Figures 4–6).** Across synthetic regression, image regression, denoising, and CIFAR-10, the paper monitors eigenvalues of **I** − η**H** during training and shows a consistent pattern: SGDL's smallest eigenvalue exits (−1, 1) correlating with loss oscillations, while MGDL's stays within (−1, 1). This is validated across four different task types and provides a complementary perspective to the "edge of stability" literature.

- **Test-set improvements on image and time series tasks are well-documented.** Tables 1–3 show MGDL achieves 0.42–3.94 dB higher test PSNR for image regression across 6 images, with similar consistent gains for denoising (6 noise levels × 3 images) and deblurring (3 blur levels × 3 images). Tables 4–5 show MGT achieves substantially better test MSE on time series (1.6×10⁻¹ vs 2.6 for synthetic; 1.8×10⁻² vs 8.9×10⁻² for financial data) while requiring only 28–33% of SGT's training time.

- **Learning rate robustness (Section 6, Figure 2)** provides concrete evidence that MGDL tolerates a wider range of learning rates: SGDL achieves loss < 0.001 only for η ∈ [0.03, 0.08], whereas MGDL sustains this for η ∈ [0.01, 0.3] on the same synthetic task. This is demonstrated on both synthetic and image regression settings.

- **Convexity result (Theorem 3)** is a clean structural contribution showing that single-layer ReLU grade optimization is equivalent to a convex program, extending Pilanci & Ergen (2020) to the sequential multi-grade setting.

## Weaknesses

### Fatal
None

### Major

- **Missing test accuracy for classification tasks** — CIFAR-100 (Section 5, Figure 3) and CIFAR-10 (Section 7) report only training MSE loss, never classification accuracy on the test set. Line 223 states the paper evaluates "both accuracy and training dynamics" for CIFAR-100 but then only shows training MSE convergence curves. Reporting that MGDL achieves training loss two orders of magnitude lower than SGDL without reporting test accuracy raises serious overfitting concerns and leaves the classification claims unsupported. Test accuracy is the standard evaluation metric for these benchmarks, and its absence is a significant gap that undermines the paper's classification-related claims.

- **Structural disconnect between theory and experiments** — The paper's three theoretical contributions each apply to different settings than the experiments: (1) Theorems 1–2 show MGDL admits a wider learning rate range because α_l ≪ α (smaller Hessian spectral norm for shallower subnetworks), but this is an expected consequence of optimizing smaller networks and does not address solution quality or generalization. (2) Theorem 3 (convexity) applies only to single hidden-layer ReLU grades with m_l ≥ P_l neurons, but all experiments use multi-layer grades — the paper never acknowledges this mismatch. (3) The eigenvalue analysis (Section 7) is conducted on networks with 48 hidden units (line 285: "SGDL with architecture 26 (2, 1, 48, 4)") because Hessian computation is otherwise intractable, while the performance benchmarks use 128-unit networks. No single theoretical result directly explains the empirical findings on the same problem instances.

- **No parameter count matching between SGDL and MGDL** — Throughout the experiments, SGDL and MGDL use different architectures. For example, image regression uses SGDL (2, 1, 128, 8) vs MGDL (2, 1, 128, 2, 4); CIFAR-10 uses SGDL (3072, 10, 128, 8) vs MGDL (3072, 10, 128, 2, 4). The paper never reports or explicitly matches total parameter counts, FLOPs, or effective capacity. Without controlling for this confound, observed performance differences could be attributed to architecture or capacity differences rather than the multi-grade training paradigm itself.

### Minor

- **Theory assumes vanilla GD, but main experiments use Adam** — Theorems 1–2 and Theorem 4 analyze gradient descent, but the performance experiments in Section 5 use the Adam optimizer (line 154). The learning rate robustness study (Section 6) and eigenvalue analysis (Section 7) use GD on different, smaller networks. Whether MGDL's theoretical advantages transfer to adaptive optimizers that already mitigate learning rate sensitivity is never tested.

- **Time series experiments lack statistical rigor** — Tables 4–5 report results from apparent single runs without confidence intervals or multiple seeds. For the financial data (SPX), where time series prediction is inherently noisy, a single run is insufficient to establish reliable conclusions. The claim that "MGT maintains accurate predictions" on the test set (Figures 7–8) is based on visual inspection of a single realization.

- **"Scalable" claim unsupported by evidence** — The abstract claims MGDL is "a scalable framework," but the largest experiment uses CIFAR-100 with standard CNNs, and the eigenvalue analysis requires full Hessian computation on 48-unit networks. No experiment approaches a scale where scalability claims become meaningful.

- **Error accumulation across grades not analyzed** — MGDL trains grades sequentially on residuals, but the paper does not analyze (theoretically or empirically) how approximation errors from early grades propagate and potentially compound in later grades. This is a fundamental concern for any sequential decomposition method.

### Trivial
None

## Nice-to-Haves
- Compare against established training techniques that address similar problems (progressive training, layer-wise pretraining, residual connections, learning rate scheduling) to demonstrate MGDL's benefits are unique to the paradigm.
- Show a case where MGDL's eigenvalues also exit (−1, 1) and performance degrades as predicted, demonstrating the eigenvalue analysis has predictive (not just post-hoc descriptive) power.
- Solve the convex program (Theorem 3) directly on a small problem to verify practical relevance of the convexification.
- External baselines for image denoising/deblurring (BM3D, etc.) to contextualize absolute performance levels.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Convergence theory is a tautology"**: The reviewer characterizes Theorems 1–2 as merely restating that smaller networks have smaller Hessians. While these theorems are standard convergence results applied to differently-sized problems, calling them "tautological" overstates the case — the paper does formalize the intuition that shallower subproblems are better-conditioned. Retained as part of the theory-experiment disconnect (Major) rather than as a standalone fatal flaw.

- **"Compact convex set assumption (Theorem 1) is unverifiable and load-bearing"**: This is a standard assumption in optimization convergence theory, used across the literature. Not unique to or more problematic in this paper than in comparable work. Removed as a standard theoretical practice nitpick.

- **"Paper conflates training stability with model quality throughout"**: This criticism is partially refuted by the paper's own data. Tables 1–3 report test PSNR (not just training loss) for image tasks, and Tables 4–5 report test MSE for time series tasks, both showing genuine test-time quality improvements. The concern is valid only for CIFAR experiments, which is already captured in Major weakness #1.

- **"No external baselines for denoising/deblurring"**: The paper's stated scope is comparing MGDL vs SGDL to explain why multi-grade outperforms single-grade. It does not claim state-of-the-art denoising performance. Moved to nice-to-have.

- **"Convexity result is practically intractable"**: While true that the convex program requires exponentially many activation patterns, this is a well-known limitation of the Pilanci & Ergen (2020) framework the paper extends. The result still has structural theoretical value. The mismatch with experiments (single-layer vs multi-layer grades) is retained under the theory-experiment disconnect weakness.

## Novel Insights
The eigenvalue-tracking methodology (Section 7) provides a concrete, task-agnostic diagnostic for distinguishing stable from oscillatory GD training dynamics, complementing the "edge of stability" literature. The consistent empirical finding that the *smallest* eigenvalue of **I** − η**H** is the dominant driver of instability — rather than the largest — is an observation that could inform learning rate scheduling and architecture design beyond the MGDL context. The sequential convexification result (Theorem 3) offers a structural perspective showing how residual decomposition can extend known single-layer convexifications to deep architectures, though practical impact remains limited.

## Suggestions
1. **Report test accuracy** (not just training MSE) for CIFAR-10 and CIFAR-100 — this is essential for any classification benchmark claim.
2. **Include a parameter count comparison table** matching total parameters, FLOPs, and wall-clock time for SGDL vs MGDL across all experiments.
3. **Run CIFAR experiments with explicitly matched parameter budgets** to isolate the training paradigm's effect from architecture differences.
4. **Test predictive power of eigenvalue diagnostic**: identify settings where MGDL eigenvalues also exit (−1, 1) and verify performance degrades accordingly.
5. **Report multiple seeds with confidence intervals**, especially for time series experiments.
6. **Acknowledge the gap between Theorem 3 (single-layer grades) and the multi-layer grades used in experiments.**

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Financial markets NN | nSDOkm0SKo | 1.0 | R1 | Far below — not a serious ML paper |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.0 | R1 | Far below — fundamentally flawed |
| Chinese NLP humanoids | gwZ90hFSL2 | 1.0 | R1 | Far below — pseudoscientific |
| Faster GD Deep Linear | NbbsRnPBoS | 2.33 | R1 | Below — narrower scope, contrived examples; MGDL paper has broader experiments |
| Weak Correlations | 2NwHLAffZZ | 2.33 | R1 | Below — unclear contribution; MGDL has more concrete empirical evidence |
| Non-differentiability NN | Zap3nZhRIQ | 3.0 | R1 | Slightly below — similar theory-practice disconnect but MGDL has more experiments |
| Increasing Batch Size | l2odw7OiNw | 2.5 | R1 | Below — weaker experiments; MGDL has more comprehensive evaluation |
| **Block Coordinate Descent** | **n2RIkaf1S4** | **4.0** | **R1** | **Most similar anchor — same profile: alternative training with convergence theory, theory-experiment gaps, limited practical validation. MGDL paper has broader experiments but more damaging omissions (missing CIFAR test accuracy)** |
| Syntax then Semantics | hNkXTqDrfb | 3.75 | R1 | Similar range — training dynamics theory with limited practical grounding |
| Multitask Representation | 6Ey8mAuLiw | 5.25 | R1 | Slightly above MGDL — clearer theoretical contribution connecting to experiments |
| Unified Scaling Laws | ewZSzO6bts | 3.75 | R1 | Similar — broad claims with insufficient theoretical/experimental support |
| Can Stability be Detrimental | zPaTnGjgpa | 4.20 | R1 | Similar — eigenvalue/stability analysis with limited novelty beyond observation |
| Large Learning Rates | LNYL96VIsD | 4.75 | R1 | Similar range — learning rate sensitivity analysis, slightly stronger execution |
| Stability Predictive Coding | OZZYqfplS3 | 4.0 | R1 | Similar — convergence/stability analysis with theory-practice gaps |
| Heavy-Tails Weight Spectrum | WL4BmXG7Pl | 5.0 | R1 | Slightly above — similar spectral analysis theme, more cohesive |
| Training Jacobian | kkVTeMvC9D | 3.40 | R1 | Very similar topic (Jacobian/eigenvalue analysis of training), rejected for limited scale and unclear insights |
| Operator Networks PDEs | xpmDc76RN2 | 2.33 | R1 | Below — narrower scope and weaker validation |
| Riemannian Optimization CNN | 6w9qffvXkq | 2.60 | R1 | Below — limited scope and novelty |
| How Students Become Teachers | 25j2ZEgwTj | 6.0 | R1 | Above — rigorous 3-phase theory with clear convergence rate |
| Hierarchical Polynomials | QgwAYFrh9t | 5.75 | R1 | Above — clear theoretical separation result |
| Continual Linear Classification | DTqx3iqjkz | 6.25 | R1 | Above — stronger theory with clear implicit bias result |
| Central Flows | sIE2rI3ZPs | 7.0 | R1 | Well above — much deeper theoretical contribution explaining optimizer behavior |
| Deep Matrix Factorization EOS | J4Dvxv7WnG | 7.0 | R1 | Well above — rigorous fine-grained EOS analysis |
| Loss Landscape Convex Duality | 4xWQS2z77v | 8.0 | R1 | Far above — thorough convex reformulation with deep theoretical results |
| Small-scale Proxies | d8w0pmvXbZ | 8.0 | R1 | Far above — training stability analysis at practical scale |
| Neural ODE Activations | AoraWUmpLU | 8.0 | R1 | Far above — rigorous convergence analysis |

**Round 1 bracket: 3.5 – 5.0**

The paper sits most naturally alongside n2RIkaf1S4 (4.0), zPaTnGjgpa (4.20), and kkVTeMvC9D (3.40). It has broader experiments than these anchors (Tables 1–5 showing real test improvements on non-classification tasks), but the missing CIFAR test accuracy, theory-experiment disconnect, and lack of parameter matching are structural issues comparable to those that earned these anchors their scores.

The paper does not reach the level of borderline accept anchors (5.5+) like 25j2ZEgwTj (6.0) or DTqx3iqjkz (6.25), which have much tighter theory-experiment connections and clearer novel contributions.

**Final score: 4.0** — The paper has an interesting training paradigm, a useful eigenvalue diagnostic, and genuine test improvements on regression/time-series tasks. However, the theory-experiment structural disconnect (Theorem 3 applies to single-layer grades while experiments use multi-layer grades), the missing test accuracy for classification benchmarks, and the absence of parameter count controls prevent it from convincingly supporting its central claim. These issues are addressable in revision but in their current form fall below the acceptance threshold.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>