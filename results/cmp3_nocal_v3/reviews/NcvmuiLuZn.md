## Summary

This paper introduces the noise-to-process (N2P) paradigm for single-trajectory stochastic process modeling, where a shared base-noise process is pushed through a single learnable generator to produce a full trajectory, making projective consistency intrinsic by design. The paradigm is instantiated as Deconvolution-Based Process Transformation (DBPT), a deconvolution-based decoder trained with masked MSE. Experiments span synthetic data, financial time series, image completion (MNIST, CIFAR), and black-box optimization, showing that DBPT performs competitively against both prior-driven (GP, WGP) and data-driven (CNP) baselines.

## Strengths

1. **Clean theoretical formalism.** The N2P representation (Definition 1: shared base-noise + single measurable generator) is clearly stated, and Proposition 3 (projective consistency) is correct and concisely proved from the pushforward construction. The connection to Kolmogorov extension (§2.2) is appropriately scoped as a compatibility statement rather than a training requirement. This theoretical framing of the single-trajectory regime is genuinely novel.

2. **Strong image completion results.** DBPT convincingly outperforms all baselines on both MNIST and CIFAR (Table 2): PSNR 21.65 vs. CNP's 16.58 on MNIST, and 24.04 vs. 18.56 on CIFAR. The SSIM scores (0.94 and 0.90) are substantially higher than any competitor. These are large, unambiguous margins.

3. **Broad task diversity.** The paper evaluates across four distinct problem types (synthetic, time series, image completion, black-box optimization), which is unusual and demonstrates the generality of the approach beyond any single domain.

## Weaknesses

### Fatal
None.

### Major

1. **"Calibrated uncertainty" claimed but not empirically demonstrated.** The abstract (line 27) states that DBPT "delivers flexible representations and calibrated uncertainty," and the conclusion reiterates this framing. However, the paper reports no calibration-related metrics anywhere in the main body — no expected calibration error, no reliability diagrams, no coverage checks for prediction intervals, no empirical evaluation of whether the uncertainty estimates are actually calibrated. The only reference to calibration is a theoretical pointer to Appendix C (line 105), which is stripped by the parser. NLL mixes calibration and sharpness but does not separate them; a model could achieve reasonable NLL through uninformatively wide intervals. For a paper whose core selling point is reliable uncertainty quantification from a single trajectory, this is a significant empirical gap that directly undercuts a central claim.

2. **On the most natural single-trajectory task (time series), DBPT is second-best to a prior-driven method.** Table 1 shows WGP achieves the best average rank (1.75) while DBPT ranks second (2.50). On the BIA dataset, WGP is strictly better on both NLL (602.42 vs. 647.92) and MSE (4.12 vs. 5.98). On PDB, DBPT wins on NLL (501.00 vs. 504.32) but loses on MSE (3.40 vs. 2.34 for WGP, and vs. 1.63 for Markov). The paper's explanation (line 145–174) — that DBPT "places a stronger emphasis on modeling the uncertainty" — is not substantiated by any evidence (no calibration metrics, no analysis of why the trade-off occurs). This outcome weakens the narrative that DBPT surpasses prior-driven methods in the single-trajectory regime. The paper would be stronger if it analyzed *why* WGP outperforms DBPT on this task rather than spinning the gap as a trade-off without supporting data.

### Minor

3. **NGGP inconsistency.** In §4.1 (line 139), the paper states "We observe that NGGP struggles to converge on single-trajectory data," yet NGGP is not listed among the evaluated baselines in §4 (line 125: GP, WGP, Markov, DKL, SDE Matching, CNP). NGGP is introduced only in the related work (§3, line 117). This is a drafting error — either the mention should be removed or NGGP should be formally included in the method list.

4. **The deconvolution architecture's inductive bias is not discussed.** The paper repeatedly characterizes the approach as "weak-prior" and contrasts it with the "strong structural priors" of GPs. The definition in §2.1 (line 39) clarifies that "weak prior" refers to the structural assumption "shared noise + single generator," which is fair. However, the DBPT architecture itself (deconvolution layers with upsampling and convolution, line 95) encodes a strong spatial continuity bias — translation-invariant kernels and hierarchical upsampling that explicitly assume local smoothness. This is precisely why DBPT excels at images and why it might fail on processes without such structure. The paper never acknowledges this architectural inductive bias, which would help readers understand the method's applicability scope.

5. **Synthetic experiment (§4.1) reports only visual inspection with no quantitative metrics.** The experiment uses only 2 observed points (positions 10 and 20 on the trajectory). The section is titled "VISUALIZATION" so qualitative results are the stated scope, but the paper draws conclusions about DBPT's "superior flexibility and adaptability" from these visuals without reporting NLL, MSE, or coverage numbers. Adding quantitative metrics for this experiment would strengthen the evaluation and make the claims verifiable.

6. **No error bars or confidence intervals on the BBO convergence curves (Figure 4).** The figure shows averaged convergence curves for the Schwefel and Rastrigin problems, but without any indication of variance across runs, it is impossible to assess whether the observed differences are statistically significant.

### Trivial
None.

## Nice-to-Haves

- Include simple baselines such as linear interpolation or a feedforward MLP to help isolate whether DBPT's gains come from the specific deconvolution architecture or merely from being a flexible function approximator.
- Test DBPT on processes that violate local smoothness assumptions (e.g., permuted indices, long-range independent noise, or discontinuous functions) to map out where the method breaks down.
- Add a comparison against a full Neural Process (with latent variables), not just CNP.

## Removed Points

- **Criticisms about architecture details being deferred to the appendix** — removed per parser-rules (the appendix exists in the original submission).
- **Question about whether GP baselines use learned or fixed hyperparameters** — removed because experimental configuration details are in the stripped appendix.
- **Speculation that SDE Matching's catastrophic failure indicates misconfiguration** — removed as unverifiable speculation; the paper may have configured it correctly and it simply performs poorly on these tasks.
- **Criticism about missing related works** — removed per policy (reviewer cannot verify existence of unmentioned works).
- **Claim that DBPT lacks architectural novelty** — removed as overstated; the paper's contribution is the N2P paradigm and its application, not architectural invention per se, and the paper appropriately cites Chen et al. (2022) for the deconvolution component.
- **Request for number of layers / kernel sizes in the main text** — removed because these details are in the appendix (stripped by parser).

## Novel Insights

The most insightful observation from the reviews is that the paper's central empirical claim ("DBPT surpasses prior-driven methods") is partially contradicted by its own best evidence: on the single-benchmark most naturally aligned with the paper's stated regime of interest (time series with few observations), a classical prior-driven method (WGP) outperforms DBPT. This reveals a tension between the paper's narrative framing and its actual results that needs to be honestly addressed rather than explained away. The second key insight is that the "weak-prior" claim conflates two different notions of prior: the structural assumption of the N2P paradigm (which is indeed weak — just a shared noise process and a generator) and the inductive bias of the deconvolution architecture (which is strong — assuming spatial smoothness and translation invariance). Disentangling these would substantially clarify the paper's actual contribution.

## Suggestions

1. **Report empirical calibration metrics** (expected calibration error, coverage of 80%/90% prediction intervals, or reliability diagrams) across all experiments, especially the time series task. Without these, the "calibrated uncertainty" claim is unsupported.
2. **Explicitly discuss the inductive bias of the deconvolution architecture** in §2.3 — state what structural assumptions the decoder makes (local smoothness, translation invariance) and how this differs from "strong prior" in the GP sense. This would help readers understand the method's applicability scope.
3. **Add quantitative metrics (NLL and MSE) to the synthetic experiment** (§4.1) so the visual claims are backed by numbers.
4. **Include error bars or confidence bands on the BBO convergence curves** to establish statistical significance.
5. **Resolve the NGGP inconsistency** — either remove the mention from §4.1 or include NGGP in the formal baseline list.
6. **Provide a deeper analysis of why WGP outperforms DBPT on financial time series** — is it the warping, the kernel structure, the smaller parameter count, or something else? This would be more informative than the current trade-off explanation.

## Score and Decision

**MY FINAL SCORE:** <score>5.0</score>
**MY FINAL DECISION:** <decision>Reject</decision>