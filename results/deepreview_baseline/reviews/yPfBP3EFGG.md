## Summary
This paper proposes STNAdam, a stochastic optimization algorithm for solving "nonconvex + weakly-convex" composite optimization problems. The key innovation is a two-track iteration framework that maintains both an extrapolation trajectory (via Nesterov momentum) and a regular update trajectory (via Adam-style adaptive conditioning), which are interactively coupled. The authors provide a convergence analysis under the Kurdyka-Łojasiewicz property, showing almost sure convergence to stationary points with explicit rates, and demonstrate empirical performance on low-light image enhancement tasks.

## Strengths
- **Novel algorithmic framework**: The two-track iteration design is a genuinely new architectural idea for combining Nesterov acceleration with adaptive methods. Unlike prior work (NAdam, SNAdam) that simply applies Nesterov momentum to the momentum estimate, STNAdam maintains two separate coupled trajectories, which is conceptually distinct and potentially more expressive.
- **General convergence theory**: The analysis is impressively general—it accommodates arbitrary variance-reduced gradient estimators (SVRG, SAGA, SARAH, SPIDER) under a unified set of conditions, and allows hyper-parameters to be dynamically scheduled within iterate-dependent intervals. This level of generality is rare in the Adam-variant literature.
- **Strong empirical results**: On the low-light image enhancement task, STNAdam-SARAH achieves PSNR 22.26, SSIM 0.906, and LPIPS 0.050, substantially outperforming all baselines including SGD (14.80 PSNR), Adam (16.38 PSNR), SNAdam (17.14 PSNR), and specialized LIE methods like Retinex-Net (18.44 PSNR). The improvements are large and consistent across metrics.

## Weaknesses
### Fatal
None.

### Major
- **The paper is incomplete and inaccessible in its current form.** The main text ends abruptly at page 9 with "Rest of paper (reference and Appendix) is removed." The references are truncated, the appendix (containing all proofs, Lemma A.1, parameter definitions for A_i, and supplementary experiments) is entirely missing, and the convergence analysis in Section 3 is presented as a skeleton with key lemmas stated but no derivations. Without the appendix, the theoretical claims cannot be verified, and the paper is not self-contained. This is a fatal flaw for review purposes—the paper as submitted is not a complete research article.
- **The convergence analysis is presented as a sequence of lemmas without proof or sufficient context.** Lemma 2, Lemma 3, Lemma 4, Lemma 5, Theorem 1, and Theorem 2 are stated, but the constants A_1 through A_8, the energy function parameters (M, H, Z, D), and the derivations are all relegated to the missing appendix. The reader cannot assess whether the analysis is correct, whether the assumptions are reasonable, or whether the claimed rates are meaningful.
- **The empirical evaluation is limited to a single task (low-light image enhancement) on a single dataset (LOL).** While the results are strong, the paper claims STNAdam is a general-purpose optimizer for "nonconvex + weakly-convex" composite optimization. Standard practice in the optimizer literature is to evaluate on multiple tasks (e.g., image classification, language modeling, regression) to demonstrate generality. A single image enhancement task, even with multiple metrics, is insufficient to support the broad claims.
- **The comparison to baselines is incomplete and potentially unfair.** The paper compares against SGD, Adam, and SNAdam, but does not include NAdam (Dozat, 2016), which is the most direct single-track competitor. The "SAdam" cited as Kingma & Ba (2014) is actually just Adam—SAdam in the literature (Wang et al., 2019; Le-Duc et al., 2024) is a different algorithm. The paper also does not compare against other recent Adam variants like AdamW, AdaBelief, or Lion. The hyper-parameter tuning procedure for baselines is not described.

### Minor
- **The notation is overly complex and sometimes inconsistent.** For example, Table 1 uses both m^k and m^{k+1} for momentum, but the stochastic counterparts use varpi^k and varpi^{k+1}. The paper uses hat, tilde, and bar notation extensively, making it difficult to track which variable is which. The two-track update in Algorithm 1 uses x^{k+1}, bar{x}^{k+1}, and tilde{x}^{k+1} without clearly explaining the relationship between tilde{x}^k and the output.
- **The parameter update intervals (6)-(8) are defined in terms of constants that are themselves defined in the missing appendix.** The lower bound for gamma_{k+1} involves M, s, V_1, V_T, rho—none of which are defined in the main text. The reader cannot evaluate whether these intervals are practically meaningful or vacuous.
- **The paper claims "removing hand-tuning" of hyper-parameters, but the intervals themselves depend on problem-dependent constants (L, tau, V_1, V_T, rho) that are typically unknown in practice.** This undermines the practical contribution.

### Trivial
- The paper states "STNAdam" in the title but uses "STNAdam" and "STNAdam" inconsistently in the text.
- Figure 1 is described in the caption but the actual figure is a placeholder (showing "2fa4a1bf91d0f34e87c689fbc1211fe3_img.jpg" rather than a proper rendering).

## Nice-to-Haves
- A comparison against NAdam and other recent Adam variants (AdamW, AdaBelief) would strengthen the empirical evaluation.
- Ablation studies isolating the contribution of the two-track mechanism (e.g., comparing STNAdam against a version with only one track) would help validate the core claim.
- Experiments on standard deep learning benchmarks (CIFAR-10/100, ImageNet, language modeling) would demonstrate generality.

## Novel Insights
None beyond the paper's own contributions. The two-track framework is the central novel idea, but without the appendix, the theoretical insights cannot be fully assessed.

## Suggestions
1. **Complete the paper.** The appendix with all proofs, parameter definitions, and supplementary experiments must be included for the paper to be evaluable. The current submission is not a complete research article.
2. **Expand the empirical evaluation.** Add experiments on at least 2-3 additional tasks (e.g., image classification on CIFAR-10, language modeling on a small dataset) to demonstrate generality. Include NAdam and AdamW as baselines.
3. **Clarify the practical utility of the parameter intervals.** Provide guidance on how to set the constants (M, s, V_1, V_T, rho) in practice, or show that the algorithm is robust to their choice.
4. **Simplify the notation.** Consider using a more conventional notation scheme to improve readability. The current notation with multiple accents (hat, tilde, bar) on multiple variables is difficult to follow.

## Score and Decision
The paper presents a novel algorithmic idea with strong empirical results on one task and a general theoretical framework. However, the paper is fundamentally incomplete—the appendix containing all proofs, parameter definitions, and supplementary material is missing, making the theoretical claims unverifiable and the paper not self-contained. Additionally, the empirical evaluation is too narrow to support the broad claims. For these reasons, the paper cannot be accepted in its current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>