## Summary

This paper addresses two key limitations of existing diffusion-based ILP solvers: (1) slow inference (hours per instance) and (2) restriction to binary variables. The authors propose three one-step diffusion-based solvers (CMILP, SCMILP, MFILP) that dramatically accelerate inference, and introduce an Iterative Integer Projection (IIP) layer that extends neural ILP solvers to non-binary integer variables without costly binarization. Objective-guided sampling with momentum (MGD) is also introduced. Experiments cover binary benchmarks (set cover, facility location, combinatorial auction) and non-binary problems (inventory management, synthetic random), demonstrating inference speeds of seconds versus hours for prior diffusion methods.

## Strengths

1. **The IIP layer (Eq. 3) is a genuinely elegant and novel contribution.** The function \(f_{\text{proj}}(x) = x - \sin(2\pi x)/(2\pi)\) is a differentiable fixed-point iteration that converges to integers over the entire real domain, cleanly avoiding the exponential blowup from binary-encoding non-binary variables. Fig. 2 confirms convergence in few iterations.

2. **Dramatic and concretely demonstrated speed improvements.** On non-binary inventory management problems, the proposed methods solve in 2–3 seconds what IP-Guided DDPM takes ~34 minutes (Table 2, IM-(50,5,2)). On the larger Random-(2000,20,2) dataset (Table 6), the methods solve in ~20 seconds vs. IP-Guided DDIM's 46 minutes. This acceleration is real and practically meaningful.

3. **Broad evaluation across diverse problem classes.** The paper tests three binary ILP benchmarks (SC, CF, CA) and two non-binary ILP families (inventory management with varying dimensions, synthetic random up to 2000 variables), against multiple traditional solvers (Gurobi, SCIP, COPT), heuristic methods (RINS, Feasibility Pump), and neural baselines (Neural Diving, IP-Guided DDPM/DDIM, DiffILO).

## Weaknesses

### Fatal

None.

### Major

1. **Duplicate method labels in Tables 2–5 make the non-binary results partially uninterpretable.** In all non-binary result tables (Tables 2, 3, 4, 5), "CMILP" is absent and two rows are both labeled "SCMILP (Ours)." In Table 1 (binary) and Table 6 (synthetic non-binary), CMILP, SCMILP, and MFILP are correctly distinguished. The most natural correction is that one of the two "SCMILP" rows should be "CMILP," but as presented the reader cannot confidently attribute results to the correct method for the core non-binary experiments. **The paper must correct this labeling error before the experimental evidence can be properly evaluated.**

2. **The headline claim "outperforms" (Abstract, line 9) is overstated and conflates speed with solution quality.** On all three binary benchmarks in Table 1, IP-Guided DDIM achieves substantially *lower* (better) optimality gaps than any of the three proposed methods:
   - SC: DDIM 68.5% vs. best proposed (MFILP) 88.4%
   - CF: DDIM 54.6% vs. best proposed (MFILP) 76.1%
   - CA: DDIM 25.4% vs. best proposed (MFILP) 79.2%
   
   The paper's genuine advantage is *speed* (seconds vs. hours). The claim should be explicitly recalibrated to reflect a speed-quality trade-off, not an unqualified improvement. The paper's own text (Section 4.2) correctly notes that DDIM has the lowest gap but takes much longer, which is the honest framing the abstract should adopt.

### Minor

3. **CMILP loss (Eq. 6) creates a tension between the "learning distribution" motivation and the actual regression objective.** The paper motivates diffusion models as learning "the distribution of feasible solutions \(\mathbf{x}\) given instances \(\mathcal{P}\)" (Section 3.2). However, Eq. 6 trains \(f_\theta\) to minimize distance to a Dirac delta \(\delta(\mathbf{x} - \mathbf{x}^*)\) — a single target solution per training example. While the training set uses 500 solutions per instance (line 73) which provides variety across examples, the loss formulation collapses the conditional distribution to a point estimate rather than modeling it. This is not fatal (the method clearly works), but the paper should clarify what the diffusion process adds over a deterministic predictor trained with the same architecture and supervised loss.

4. **The gap metric is conditioned on feasibility, limiting cross-method comparability.** The paper states (Section 4.1): "The gap is only calculated among problems to which the solvers can get a feasible solution." This means a method that finds feasible solutions for 1% of test instances reports a gap computed on ~1 instance, while a method solving 90% reports a gap on ~90 harder instances. For example, in Table 2 on IM-(50,5,2), IP-Guided DDPM has 1% dataset feasibility but reports a 92.9% gap, while MFILP has 90% dataset feasibility and reports a 12.1% gap. These numbers are not directly comparable. The paper should also report gap computed on a common subset of instances solvable by all compared methods.

### Trivial

5. **Typographical errors in tables (Tables 2–6).** The heuristic "Relaxation Induced Neighbourhood Search" is abbreviated as "ris" instead of "rins"; "Feasibility Pump" appears as "feasupn" instead of "feaspump." In Table 2, the time for "ris" on IM-(50,5,5) is listed as "3.6%" instead of "3.6s." These should be corrected for consistency.

6. **Eq. (5) contains an incorrect coefficient in the standard DDPM denoising formula.** The epsilon coefficient is written as \(\frac{1-\alpha_t}{\sqrt{1-\alpha_t}}\) (which simplifies to \(\sqrt{1-\alpha_t}\)), whereas the correct term is \(\frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}\). This does not affect the proposed method but should be corrected.

## Nice-to-Haves

- **Ablation of the diffusion component:** Since Eq. 6 essentially trains a predictor from noisy inputs to \(\mathbf{x}^*\), comparing against a non-diffusion baseline (same architecture, no noise process) that directly predicts \(\mathbf{x}^*\) from problem features would clarify whether the diffusion framework adds value beyond a deterministic predictor.
- **Variance reporting:** All metrics (gap, time, feasibility) are reported as point estimates without standard deviations across instances or random seeds. Given the generative nature of the methods (30 samples per instance), reporting variance would strengthen the evidence.
- **Analysis of failure cases:** Dataset feasibility of 60–90% on some datasets means the methods fail to find any feasible solution for 10–40% of test instances. Understanding whether failures correlate with problem size, constraint density, or objective structure would be informative.

## Removed Points

These points from the input review are not included in the assessment above:

- **"nearly 100% claim is overclaimed":** The reviewer claimed this statement is inaccurate, but Table 1 shows 100% *dataset* feasibility for all proposed methods on all binary benchmarks. The claim is accurate as written and is removed.
- **"CLIP-style pretraining not ablated":** The paper mentions the pretraining but never analyzes it. This is a nice-to-have deeper investigation, not a weakness. Removed as scope creep beyond what is expected.
- **"Section 3.2 details deferred to appendix":** This is normal practice for conference papers. The main text explicitly acknowledges the deferral. Not a weakness. Removed.
- **"DiffILO missing from non-binary evaluation":** DiffILO is designed for differentiable ILP and is tested on binary problems where it is relevant. Its absence from non-binary problems is not a flaw. Removed.
- **"Equation numbering artifact (226, 231, etc.)":** These are parser artifacts from the PDF extraction, not errors in the submitted paper. Removed.
- **"Missing standard deviation reporting":** Downgraded to Nice-to-Haves. Single-run evaluation is standard for large-scale optimization benchmarks.
- **"No investigation of IIP iteration count K":** Downgraded to Nice-to-Haves. The paper notes K is small during training and larger during testing, which is sufficient for a conference contribution.

## Novel Insights

None beyond the paper's own contributions. The reviews surface no perspective on the method or results that the paper itself does not provide.

## Suggestions

1. **Fix the labeling error in Tables 2–5:** replace the duplicated "SCMILP" label with "CMILP" so that all three methods are clearly identified, consistent with Table 1 and Table 6.
2. **Recalibrate the abstract and conclusion claims** to accurately describe the contribution as a speed-quality trade-off rather than unqualified "outperforming."
3. **Report gap on a common subset** of instances solvable by all compared methods to enable fair cross-method comparison.
4. **Clarify in Section 3.2** why the diffusion framework is beneficial despite the CMILP loss effectively being a regression to \(\mathbf{x}^*\), and consider an ablation comparing against a deterministic predictor.
5. **Correct the typographical errors** in Tables 2–6 and the coefficient in Eq. (5).

## Score and Decision

The paper makes a genuine contribution — the IIP layer is novel and the speed improvements are dramatic and well-supported. However, the duplicate method labels in the non-binary result tables prevent full evaluation of the experimental evidence as presented, and the abstract's "outperforms" claim is not supported by the binary results. Both issues are fixable, and the core contributions are real. A revised version addressing these issues would be a solid paper.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>