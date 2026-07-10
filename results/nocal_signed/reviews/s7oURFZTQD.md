Now let me compile my final review based on the verified findings and the impact scores.

## Summary

This paper studies Multi-Grade Deep Learning (MGDL), which decomposes end-to-end training into sequential shallow subproblems trained on residuals. It provides convergence theorems for smooth activations, a convex reformulation for single-layer ReLU grades (Theorem 3), eigenvalue-based stability analysis, and experiments across image regression, denoising, deblurring, CIFAR-10/100, and transformer time series.

## Strengths

1. **Theorem 3 (convex reformulation for single-layer ReLU grades) is a genuine theoretical contribution.** Linking MGDL to the Pilanci & Ergen (2020) convex optimization framework is the most interesting idea in the paper. It shows that, under the condition that each grade contains only one ReLU hidden layer, the nonconvex MGDL problem can be reframed as a sequence of convex programs. This is non-trivial and potentially insightful for understanding the optimization landscape of multi-stage training.

2. **The empirical scope is broad.** The paper tests MGDL across image regression, denoising, deblurring, CIFAR-10/100, and transformer-based time series — more tasks than many MGDL papers. This breadth, while unevenly executed, reflects genuine ambition.

## Weaknesses

### Major

1. **Theory–activation mismatch.** Theorems 1, 2, and 4 all assume the activation function σ is twice continuously differentiable (or thrice for Theorem 4's second part). However, every experiment in the paper uses ReLU activations (lines 36, 114, 154, 289), which are not differentiable at zero, let alone twice continuously differentiable. The paper never acknowledges this gap, never justifies why the smooth-activation theory should extend to ReLU, and never verifies whether the theoretical predictions hold for non-smooth activations. This creates a structural disconnect between the paper's theoretical framework and its empirical claims.  
   *The paper does have a ReLU-specific result (Theorem 3), but that is about convex reformulation, not convergence. The convergence theory that the paper presents as explaining MGDL's advantages does not apply to the setting in which those advantages are demonstrated.*

2. **Confounded experimental comparisons.** In every experiment, SGDL and MGDL use fundamentally different architectures. For image regression (lines 156–157), SGDL uses a depth-8 network with hidden width 128 while MGDL uses 4 sequential depth-2 grades. These differ in total depth, total parameter count, number of independent training runs (MGDL gets 4 separate optimizations, SGDL gets 1), and the residual-learning structure itself. The paper never controls for any of these — there is no ablation where SGDL is given comparable total capacity, no comparison with matched total depth, and no comparison where SGDL is trained with a residual-learning structure. The claim that "MGDL outperforms SGDL" conflates the training framework with these architectural confounds.

3. **No statistical significance or variance reporting.** All results in Tables 1–5 are reported as single numbers with no error bars, standard deviations, or confidence intervals. There is no mention of multiple random seeds or number of runs. Some PSNR improvements are small (e.g., 0.42 dB gain for Cameraman test PSNR in Table 1). Without variance estimates, it is impossible to judge whether such differences are meaningful or stem from a single favorable initialization. This is a basic standard of experimental reporting.

4. **Non-standard CIFAR evaluation undermines classification claims.** The paper advertises CIFAR-10 and CIFAR-100 classification as part of its benchmark suite, but:
   - CIFAR-100 uses MSE loss rather than cross-entropy (line 223), with no test accuracy reported — only training loss curves.
   - CIFAR-10 uses only 10,000 sampled images (not the full 50,000), fully connected networks (line 289 — despite line 154 claiming CNNs for classification), and squared loss, again with no test accuracy.
   - These results do not connect to any standard CIFAR benchmark and provide no evidence of practical classification performance.

### Minor

5. **Eigenvalue analysis is observational, not explanatory.** Section 7 empirically monitors eigenvalues of I−ηH(W^k) and observes that MGDL's stay within (−1,1) while SGDL's drift below −1. This describes what happens during training but does not explain *why* MGDL's eigenvalues behave this way. Theorem 4 is a standard linearization argument (Picard iteration + Taylor expansion) that gives no testable condition distinguishing MGDL from SGDL. The use of different learning rates for SGDL and MGDL (e.g., η=0.02 vs η=0.2 in Figure 5) further complicates interpretation, as different η values produce different I−ηH spectra by construction.

6. **Transformer baseline performance is implausibly poor without tuning details.** SGT achieves TeMSE of 2.6 on synthetic data (Table 4) and 0.089 on SPX data — values that indicate near-complete failure. The paper does not describe hyperparameter tuning for either MGT or SGT, making it unclear whether the large gap reflects a genuine MGDL advantage or a poorly configured baseline.

### Trivial

7. **Proof sketch of Theorem 3 is too compressed.** The key step ("regrouping parameters by the partition {C_{l,i}} and using closure under addition yields aggregated vectors") is stated without justification. While the result follows from Pilanci & Ergen (2020), the sketch alone is insufficient for standalone verification.

## Nice-to-Haves

- Controlled experiments where SGDL and MGDL have matched total parameter count and total depth, differing only in whether training is end-to-end or sequential.
- Experiments with smooth activations (tanh, SiLU) to validate the convergence theory, or convergence theory for ReLU (subgradient methods, Clarke Jacobians).
- Error bars / standard deviations over multiple random seeds for all experimental results.
- Test accuracy reporting for CIFAR experiments using standard cross-entropy loss.
- Hyperparameter tuning description for transformer baselines.

## Removed Points

These points were raised in the input review but are removed for the following reasons:
- **Missing appendix content (architectures 26, 27 not defined in main text):** The parser strips appendix sections; these exist in the original submission. Per hard rules, this criticism is invalid.
- **"Standard transformers do not collapse to this degree without severe misspecification":** This is speculation about the reviewer's external knowledge, not a weakness rooted in the paper's content.
- **Claim that Theorems 1-2 are "textbook GD results":** Even if the structure follows standard analysis, the application to the MGDL sequential setting is a legitimate contribution. This characterization is reductive.
- **"Paper is not salvageable" / identity-change judgments:** These are verdict-level opinions, not actionable weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add controlled experiments where SGDL and MGDL have matched total parameter count and total depth, differing only in whether training is end-to-end or sequential (or compare SGDL with a matched MGDL where each grade has the same architecture as the SGDL network).
2. Either develop convergence theory for ReLU networks or run experiments with smooth activations to validate the theory.
3. Report results with standard deviations over multiple random seeds.
4. Report test accuracy for CIFAR experiments using standard cross-entropy loss and the full datasets.
5. Describe hyperparameter tuning for transformer baselines and demonstrate that the SGT baseline is reasonably configured.

## Score and Decision

The paper makes a genuine theoretical contribution (Theorem 3) and demonstrates broad empirical ambition. However, the three Major weaknesses — the mismatch between theory (smooth activations) and experiments (ReLU), the confounded experimental comparisons, and the absence of any statistical rigor — collectively prevent the paper from supporting its central claim that MGDL is a framework that "unites rigorous theoretical guarantees with broad empirical improvements." The convergence theory does not apply to the experiments run, the experiments do not isolate the MGDL mechanism from architectural confounds, and the results are reported without variance. These issues are addressable in principle but substantial revisions would be needed.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>