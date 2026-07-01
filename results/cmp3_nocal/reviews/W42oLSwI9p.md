Here is the final consolidated review:

---

## Summary

This paper proposes three one-step diffusion-based solvers (CMILP, SCMILP, MFILP) for Integer Linear Programming (ILP), extending neural solvers beyond binary variables to general bounded integer variables. The key technical contribution is the Iterative Integer Projection (IIP) layer — a differentiable approximation to rounding that operates across the entire real line. The methods also incorporate objective-guided sampling with momentum to improve solution quality. Experiments on binary (set cover, capacitated facility location, combinatorial auction) and non-binary (inventory management, synthetic random) ILP problems demonstrate substantial speed advantages over multi-step diffusion methods (DDPM/DDIM) and competitive speed versus traditional solvers on large instances.

## Strengths

**1. The IIP layer is a genuinely useful technical contribution (Section 3.1).** The function \(f_{\text{proj}}(x) = x - \sin(2\pi x)/(2\pi)\) with recursive iteration provides a differentiable approximation to integer rounding that converges quickly and works across the entire real line. This directly addresses a real bottleneck — the exponential blowup from binarizing bounded integer variables. Table 4 confirms the practical benefit: IP Guided DDIM fails entirely (0% feasibility) on binarized IM-(50,5,2), while IIP-based methods maintain reasonable performance.

**2. The speed advantage over multi-step diffusion methods is clear and consistently demonstrated.** Across all six tables, the proposed methods solve problems in seconds to minutes, compared to hours for IP Guided DDPM and tens of minutes for IP Guided DDIM. On Random-(2000, 20, 2), the proposed methods take 19–22s, faster than Gurobi's 42.2s and SCIP's 48.4s — genuinely faster than strong traditional solvers on this class. This addresses a real practical limitation of Zeng et al. (2024).

**3. Comprehensive evaluation across diverse problem classes.** The paper evaluates on three binary ILP types (set cover, capacitated facility location, combinatorial auction), two families of non-binary ILP (inventory management with multiple scales and bounds, synthetic random ILPs up to 2000 variables), and compares against Gurobi, SCIP, COPT, multiple heuristic baselines (rins, feasibility pump), and multiple learning-based methods (Neural Diving, PS, DiffILO, IP Guided DDPM/DDIM).

## Weaknesses

### Major

**1. The abstract's claim of "outperforming existing learning-based methods" overstates the evidence.** In Table 1 (binary ILP), IP Guided DDIM achieves substantially lower optimality gaps on all three benchmarks: on SC (68.5% vs. 88.4% MFILP), CF (54.6% vs. 76.1% MFILP), and CA (25.4% vs. 79.2% MFILP). The proposed methods are faster and achieve higher sample feasibility (100% vs. 97–99% on most datasets), but this is a speed-quality trade-off, not unambiguous superiority. The paper's experimental text is honest about this ("IP Guided DDIM consistently produces the lowest gap... its inference time is considerably longer"), but the abstract's unqualified "outperforms" and the title's framing do not reflect this nuance. The contribution should be reframed around the speed-quality frontier.

**2. Tables 2–4 contain duplicated method labels that prevent proper attribution of results to the correct method.** In each of these tables, two rows are labeled "SCMILP (Ours)" with different numerical values (e.g., Table 2: 16.5% vs. 12.2% gap on IM-(50,5,2); Table 3: 4.9% vs. 5.3% on IM-(50,50,2)). CMILP is named as one of the three proposed methods and appears in Table 1 and Table 6 but is absent from Tables 2–5, consistent with one of the SCMILP rows being intended as CMILP. This error makes it impossible to evaluate the relative performance of the three proposed methods against each other on the non-binary benchmarks and reduces confidence in the non-binary experimental section.

### Minor

**3. No variance or confidence intervals are reported for any metric.** The paper samples 30 times per instance for generative models (Section 4.1), yet all gap, feasibility, and time numbers are reported as point estimates with no standard deviations or interquartile ranges. Given the stochastic nature of diffusion-based sampling, readers cannot assess whether reported differences between methods are significant or within noise.

**4. On several inventory management instances, optimality gaps exceed 100%, indicating predicted solutions are worse than trivial baselines.** On IM-(50,5,10) (Table 2), the proposed methods report gaps of 107–119%. Even with momentum and increased steps (Table 5), gaps remain at 95.8–104.5%. A gap above 100% means the solution is worse than the all-zero solution. While the paper acknowledges "relatively big optimality gap" as a limitation, it does not contextualize the severity — that on these instances the generated solutions are essentially unusable. This undercuts any unqualified claim of "strong scalability."

**5. The "one-step" framing is imprecise.** The title and contribution statements describe the methods as "one-step", which is accurate for the diffusion forward pass (one denoising step). However, the full pipeline includes objective-guided sampling with multiple gradient descent iterations (Table 5 varies \(T_i = 10, 20\)), so the overall inference procedure is multi-step. This is not a technical flaw, but the terminology should be clarified to distinguish between the one-step diffusion backbone and the multi-step refinement stage.

**6. No ablation study isolates the contribution of individual components.** The architecture has several interacting parts: CLIP-style contrastive pretraining, diffusion loss, feasibility penalty \(\mathcal{L}_{\text{penalty}}\), and IIP layer. The contrastive pretraining is mentioned but never evaluated. An ablation showing the marginal contribution of each component would meaningfully strengthen the paper.

### Trivial

**7. The role of the IIP layer vs. post-hoc hard rounding could be clarified.** The paper states that "integrality constraints are enforced before evaluation through the hard rounding function" (line 187). Since the final output is hard-rounded anyway, the reader may wonder about IIP's role during inference. The answer (IIP is needed during training for gradient flow and improves the starting point before hard rounding) is implicit but should be stated explicitly.

## Nice-to-Haves

- A Pareto frontier plot (optimality gap vs. inference time) for the binary ILP datasets would make the speed-quality trade-off much clearer than the current table layout.
- A quantitative analysis of the IIP layer's convergence (how many iterations \(K\) are needed, comparison with Gumbel-Softmax or straight-through estimators) would solidify the paper's strongest contribution.
- The MGD results (Table 5) are limited to SCMILP on one dataset (IM-(50,5,10)). Evaluation on additional datasets and methods would strengthen the generality of the conclusion.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Missing method descriptions for SCMILP and MFILP in the main text.** The paper states "The detailed introduction of shortcut and mean flow models are put in the appendix" (line 107). The appendix was stripped by the parser; these descriptions exist in the original submission. Deferring detailed derivations to the appendix is standard practice.
- **Novelty of guidance-as-gradient-descent reinterpretation.** The criticism that "classifier guidance has always been understood as gradient-based steering" is a general claim about diffusion models. The paper's specific application of this perspective to ILP guidance (Zeng et al., 2024) is a reasonable domain-specific framing contribution.
- **"Gurobi solves Random-(2000,20,2) in 42s — faster than proposed methods on some other datasets."** This compares across different problem classes, which is not meaningful. On that same dataset, the proposed methods are faster than Gurobi (19–22s vs. 42.2s).
- **Training with Gurobi 100s targets produces potentially suboptimal training data.** This is standard practice for neural ILP solvers and is explicitly disclosed in Section 4.2.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a consistent tension between the paper's ambitious framing ("outperforming") and the actual evidence (a meaningful but honest speed-quality trade-off), but this is an observation about presentation, not a novel technical insight.

## Suggestions

1. Reframe the abstract and contributions to honestly describe the speed-quality trade-off: e.g., "achieves dramatically faster inference than multi-step diffusion methods while maintaining competitive feasibility, at the cost of larger optimality gaps on some problem classes."
2. Fix the duplicated method labels in Tables 2–4 so that CMILP results are correctly attributed (the second SCMILP row should be CMILP).
3. Report variance (standard deviation or interquartile range) for gap and feasibility metrics given the stochastic generative sampling procedure.
4. Add an ablation study isolating the contributions of contrastive pretraining, feasibility penalty, and the IIP layer.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>