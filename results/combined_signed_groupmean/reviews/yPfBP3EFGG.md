## Summary

This paper proposes STNAdam, a stochastic two-track Adam variant for solving "nonconvex + weakly-convex" composite optimization problems. The algorithm maintains two intertwined iteration trajectories — an extrapolation track and a regular update track — governed by Nesterov momentum and Adam-style adaptive conditioning. The stochastic gradient can be provided by any variance-reduced estimator (SGD, SAGA, SARAH). Under the Kurdyka-Łojasiewicz property, the paper establishes convergence rates. Empirical results on low-light image enhancement (LIE) using the LOL dataset show large improvements over baselines.

## Strengths

- **Theoretical generality.** The convergence analysis (Section 3) accommodates arbitrary variance-reduced gradient estimators (SGD, SAGA, SARAH, SPIDER) within a single framework and handles the full "nonconvex + weakly-convex" composite problem class under the KL property. This level of generality in the theory is a genuine strength — most Adam variants are analyzed only for specific estimator choices or simpler problem classes. [impact +9.98]

- **Strong empirical results on the LOL benchmark.** Table 2 shows STNAdam-SARAH achieving PSNR=22.26, SSIM=0.9062, LPIPS=0.0501, which substantially outperforms all baselines. The next-best optimizer baseline (SNAdam) achieves PSNR=17.14, and even the best LIE-specific method (Retinex-Net) achieves PSNR=18.44. These are wide margins that suggest a meaningful practical advance if the results hold up under rigorous evaluation. [impact +10.00]

## Weaknesses

### Fatal
None.

### Major

- **Limited empirical scope relative to framing.** The paper opens by framing the problem for "modern deep learning tasks" with "massive network parameters" (Introduction, lines 13–17), but the entire empirical validation is on a single optimization task — low-light image enhancement (LIE) on one dataset (LOL). Moreover, the LIE problem uses a hand-crafted regularized objective (Eq. 14) solved via a proximal-gradient framework, not a deep neural network trained with backpropagation. The paper's contribution (iii) claims performance specifically for LIE, but the abstract and introduction overclaim generality. This is a significant gap between the paper's framing and its evidence. [impact -10.00]

- **No statistical rigor.** All metrics in Tables 2 and 3 are reported as point estimates with no error bars, standard deviations, or indication of how many random trials were run. Every algorithm is a stochastic optimizer; results are subject to variance from random mini-batch selection, random parameter sampling (Step 3 of Algorithm 1), and random initialization. Without multiple runs, there is no way to assess whether the large reported advantages (e.g., PSNR 22.26 vs. 18.44) are statistically significant or reflect a single favorable run. [impact -10.00]

- **Two-track mechanism not ablated.** The paper's key innovation is the two-track iteration framework, yet there is no ablation that isolates this mechanism. Comparing STNAdam against a variant that removes the extrapolation track while keeping all other components identical would directly measure the incremental value of the second track. The existing comparisons (STNAdam-SGD vs. SGD or SAdam) confound the two-track mechanism with other differences (parameter scheduling, momentum corrections). [impact -9.27]

- **Parameter intervals depend on unknowable constants.** The adaptive parameter intervals (Eqs. 6–8) depend on constants (V₁, V_T, ρ, L, τ, M, s) that are not known a priori in practice. The paper provides no guidance on how to estimate them for a new problem. Remark 3's assertion that the bounds "exceed 0 and do not approach 0" does not make the intervals computable. Moreover, Algorithm 1 Step 3 says parameters are "randomly selected within some updated intervals" but never specifies the distribution (uniform? Gaussian?), making the algorithm underspecified for reproduction. [impact -10.00]

### Minor

- **Inconsistent baseline attribution.** The related work (line 33) attributes SNAdam to Reddi et al. (2019), but the experiments (line 281, Table 2) attribute SNAdam to Xie et al. (2024). Reddi et al. (2019) proposed AMSGrad, not SNAdam. Additionally, the baseline labeled "SAdam" in experiments is attributed to Kingma & Ba (2014) — the original Adam paper — while the related work separately describes SAdam by Wang et al. (2019) and Le-Duc et al. (2024) as different algorithms. These inconsistencies do not invalidate the results but undermine confidence in whether the baseline implementations correspond to the cited works. [impact -10.00]* 

- **Selective reporting in denoising experiment.** Table 3 compares only four methods (LIME, LR3M, Retinex-Net, STNAdam-SARAH) on the noisy LIE task. The other baselines from Table 2 (SGD, SAdam, SNAdam, STNAdam-SGD, STNAdam-SAGA) are excluded without explanation. [impact -4.77]

*Note: The impact model scores this at -10.00, but I assess it as a genuine but relatively minor issue; it is a citable inconsistency in the paper, not a flaw that would invalidate the core claims.*

### Trivial
None.

## Nice-to-Haves
- Provide convergence plots (objective value vs. iterations/wall-clock time) to allow readers to assess convergence speed, not just final quality.
- Disclose hyperparameter settings for all baselines (learning rates, momentum coefficients, etc.) to ensure reproducibility.
- Test on at least one standard deep learning benchmark (e.g., CIFAR with a ResNet) if the claim about general-purpose optimization is to be substantiated.
- Explain the design rationale for the two momentum corrections and why the output is from the extrapolation track rather than the regular track.

## Removed Points
The following points from the input review were removed per filtering rules:
- "Missing related work (Lookahead optimizer)" — removed per instructions: cannot request missing related works.
- "Per-iteration timing comparison is misleading" — removed; the model scored this at -0.34 (negligible impact). Small differences in microsecond-scale timings are not meaningful.
- "Mismatch between abstract and theorem (almost surely vs. in expectation)" — removed; model scored at -0.86 (negligible). Lemma 4 establishes some a.s. properties, and any gap is likely addressed in the (stripped) appendix.
- "The theory follows standard KL framework" — this is an observation about methodology, not a weakness; the paper applies a well-known framework to a novel algorithm.
- "LIE model may not fit weakly-convex framework" — removed; this is speculative without seeing the appendix, where the conversion is likely justified.
- Two removed points about per-iteration timing collapsed into a single removal.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add multiple-seed experiments with mean ± std for all reported metrics.
2. Include a direct ablation (STNAdam minus extrapolation track) to isolate the two-track contribution.
3. Test on at least one standard deep learning benchmark (image classification with a ResNet on CIFAR, or a small Transformer language model).
4. Either provide practical guidance for setting the parameter intervals or clarify that the intervals are needed only for the theory and any value in (0,1) works empirically.
5. Fix the SNAdam attribution (Xie et al. 2024 is correct; remove or correct the Reddi et al. 2019 claim).
6. Clarify what distribution is used when "randomly selecting" parameters in Algorithm 1 Step 3.

---

### Calibration Summary

| Anchor Path | Avg Human Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| `Uj0h13lVrR.md` | 1.00 | R1 | No | GFlowNets paper with fundamental issues; our paper is substantially stronger |
| `bEgDEyy2Yk.md` | 1.00 | R1 | No | Graph algorithm implementation paper; much weaker contribution |
| `1NYhrZynvC.md` | 2.50 | R1 | No | Stepsize theory paper; our paper has stronger empirical results |
| `5nldnvvHfw.md` | 2.50 | R1 | Yes | Adaptive Adam decay rates; flawed proofs and weak novelty — our paper has cleaner theory |
| `cya3eEczAx.md` | 1.67 | R1 | No | Proximal optimizer for P+O; narrow scope, our paper is stronger |
| `Zap3nZhRIQ.md` | 3.00 | R1 | No | Non-differentiability study; different topic |
| `mEBSeSk49H.md` | 4.25 | R1, R2 | Yes | Adam convergence theory with mathematical errors in proofs; ours has cleaner theory but weaker empirical coverage |
| `Fj6Yv5rPRe.md` | 4.25 | R1, R2 | Yes | Online learning + Adam theory with significant proof issues; ours has sounder theory |
| `DIAaRdL2Ra.md` | 5.00 | R1, R2 | Yes | Adafactor convergence (first analysis); comparable theoretical novelty, stronger standard benchmarks but still weak experiments |
| `rIJbFQ1zII.md` | 5.25 | R1 | No | Adam for bilevel optimization; different problem class |
| `gBT6rAEqvx.md` | 3.80 | R2 | Yes | Adaptive second-order methods; poor writing, narrow experiments — our paper is stronger |
| `YwJkv2YqBq.md` | 6.75 | R1 | Yes | Nesterov in benign non-convexity; accepted — cleaner analysis than ours, fewer experimental gaps |
| `JslyktsKMY.md` | 5.75 | R1 | No | Reevaluating optimization theory; meta-analysis paper |
| `ZA9XUTseA9.md` | 6.00 | R1 | No | Implicit bias of Adam; accepted, different contribution type |
| `SrGP0RQbYH.md` | 6.25 | R1 | No | Adaptive backtracking; accepted, thorough experiments |
| `fMTPkDEhLQ.md` | 8.00 | R1 | No | Tight lower bounds; strong theoretical paper, much stronger than ours |
| `CVldG5ohCy.md` | 4.00 | R2 | No | Adam through second-order lens; comparable score range |
| `VtT41Nniu4.md` | 4.60 | R2 | No | LIE paper (not optimizer); domain overlap but not directly comparable |
| `Y8i3rF4Umc.md` | 3.60 | R2 | No | LIE paper; reject-level |

**Bracket reasoning (Round 1 → Round 2):** The paper's theory is sounder than mEBSeSk49H (4.25, which had proof errors) but the experimental evaluation is weaker than DIAaRdL2Ra (5.00, which at least tested on standard benchmarks like ResNet). The strongest comparable paper (YwJkv2YqBq, 6.75) was accepted with clean analysis and proper experiments; this paper falls short of that standard. The narrow bracket is **4.0–5.0**.

**Final placement:** At 4.5, the paper sits between mEBSeSk49H (4.25) and DIAaRdL2Ra (5.00). It has stronger theory than the former (no proof errors identified) and more striking per-task empirical results than the latter, but its experimental evaluation is incomplete in ways the Adafactor paper's was not (single task with no error bars). The major weaknesses are fixable — adding error bars, an ablation, and one more benchmark — which distinguishes it from papers with fundamental theoretical errors.

---

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>