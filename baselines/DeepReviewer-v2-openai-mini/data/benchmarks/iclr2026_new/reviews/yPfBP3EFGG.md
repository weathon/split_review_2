## Summary
# Final Review Report

## Summary

This paper proposes STNAdam, a stochastic two-track variant of the Adam optimizer for solving composite optimization problems of the form "nonconvex + weakly-convex." The key algorithmic novelty is a two-track iteration framework that maintains two coupled update sequences—a regular track using bias-corrected momentum and an extrapolation track using Nesterov-corrected momentum—with the goal of balancing stable convergence with exploratory behavior. The stochastic gradient can be provided by any variance-reduced estimator (SGD, SAGA, SARAH). The authors establish almost-sure global convergence to a stationary point under the Kurdyka-Łojasiewicz (KL) property and provide a conditional convergence rate analysis. Experiments on low-light image enhancement (LIE) using the LOL dataset demonstrate that STNAdam with SARAH achieves superior PSNR (22.26), SSIM (0.906), and LPIPS (0.050) compared to standard SGD, Adam, SNAdam, and several LIE-specific algorithms. The paper addresses a relevant problem class (nonconvex + weakly-convex optimization) and provides a nontrivial theoretical analysis. However, several significant weaknesses limit the paper's contribution: the practical utility of the adaptive parameter scheduling is undermined by unobservable constants; the claimed "explicit rate" is conditional on an unknown KL exponent; the experiments lack statistical significance measures; and the convergence analysis applies to $\bar{x}^k$ while the algorithm outputs $\tilde{x}^k$. Novelty assessment is deferred due to unavailable external literature search in this run.

## Strengths
1. **Relevant problem class.** The paper targets "nonconvex + weakly-convex" composite optimization, which arises in many modern ML tasks (regularized risk minimization, low-level vision, sparse recovery). This is a more general and practically relevant setting than the convex or "nonconvex + convex" cases handled by existing Adam variants. The inclusion of a proximal-friendly, weakly-convex nonsmooth term $g(x)$ broadens applicability.

2. **Novel two-track algorithmic design.** The idea of maintaining two coupled iteration trajectories—one driven by bias-corrected momentum ($x^{k+1}$) and one driven by Nesterov-corrected momentum ($\tilde{x}^{k+1}$)—is a principled departure from single-track accelerated Adam variants (NAdam, SNAdam). The two-track structure is designed to decouple the conflicting goals of stable descent (adaptive, bias-corrected learning) and exploratory acceleration (Nesterov extrapolation), which provides a fresh perspective on optimizer design for nonconvex problems.

3. **General convergence analysis.** The theoretical framework (energy function + KL property) is general in two respects: (i) it accommodates arbitrary variance-reduced gradient estimators (SAGA, SARAH, SVRG, SPIDER) within a unified analysis; (ii) it allows the internal hyper-parameters $\gamma_{k+1}, \alpha_{k+1}, \lambda_{k+1}$ to be randomly selected within data-dependent intervals rather than fixed a priori. This flexibility is valuable for theory development.

4. **Strong empirical results on LIE.** The reported quantitative results on the LOL dataset are compelling: STNAdam-SARAH achieves PSNR 22.26 (vs. 18.44 for Retinex-Net and 17.14 for SNAdam), with consistent gains across all three metrics (PSNR, SSIM, LPIPS). The per-step timing (2.64e-05s) is competitive with or better than all baselines. Visual results are shown for qualitative verification.

5. **Comprehensive theoretical apparatus.** The proof structure (energy function decrease → subgradient boundedness → KL inequality → finite-length property → convergence rate) is logically complete and follows established optimization theory conventions. The theorems are presented with explicit reference to supporting lemmas in the appendix, indicating scholarly rigor.

## Weaknesses
### W1 (Major): Output variable mismatch between algorithm and convergence theory

The algorithm outputs $\tilde{x}^{k+1}$ (the extrapolation-track sequence), but the main convergence analysis (Lemma 2, Lemma 4, Theorem 1) is conducted on $\bar{x}^k$ (the regular-track sequence) and the joint variable $\theta^k = (\bar{x}^k, x^k)$. Theorem 2 switches back to $\tilde{x}^k$ for the convergence rate, but the paper does not establish that $\|\tilde{x}^k - \bar{x}^k\| \to 0$ or provide a connecting lemma. This means the algorithm's practical deliverable is not directly certified by the primary convergence guarantee. **Impact:** A practitioner implementing Algorithm 1 and outputting $\tilde{x}^{k+1}$ cannot be certain that the convergence theory applies to their output. **Fix:** Add a brief remark or lemma showing that the two sequences converge to the same limit under the stated assumptions, or revise the algorithm output to $\bar{x}^{k+1}$.

### W2 (Major): Adaptive parameter intervals depend on unobservable constants

The "Adaptive Update of Parameters" section defines intervals for $\gamma_{k+1}$, $\lambda_{k+1}$, and $\alpha_{k+1}$ in terms of constants $V_1, V_\Upsilon, \rho, M, s$ that are not known a priori for any given problem instance. The paper claims this "removes hand-tuning" (contribution ii), but in practice these constants cannot be computed without oracle knowledge of estimator variance properties and problem geometry. The lower bounds (e.g., $\underline{\gamma}$ in Eq. 6) involve nested expressions with multiple hidden constants, making them impossible to evaluate without the appendix—and even then, the constants are not constructive. **Impact:** The adaptive scheduling claim is misleading. Practitioners cannot implement the dynamic intervals as stated. The tuning problem is merely transferred from direct hyper-parameter selection to estimating latent constants. **Fix:** Provide either (a) provably safe default values for these constants, or (b) a practical estimation procedure from data, or (c) an explicit statement that the intervals are theoretical constructs and fixed values are recommended for practice.

### W3 (Major): Reported convergence rate is conditional, not explicit

The abstract claims convergence "at an explicit rate," but Theorem 2 provides a conditional classification: if the KL exponent $\vartheta \in (0, 1/2]$ the rate is geometric but with unspecified constants $d_1, \zeta$; if $\vartheta \in (1/2, 1)$ the rate is $O(k^{-(1-\vartheta)/(2\vartheta-1)})$ but $d_2$ is unspecified; if $\vartheta = 0$, finite termination is achieved. The KL exponent is unknown for virtually all practical problems. None of the rate constants ($d_1, d_2, \zeta$) is expressed in terms of verifiable problem parameters (condition numbers, Lipschitz constants, dimension). **Impact:** The rate is a qualitative taxonomy, not a computable bound. This overstates the practical value of the convergence result. **Fix:** Replace "explicit rate" with "conditional convergence rate" throughout the paper and clarify the limitations of KL-based rate analysis in the conclusion.

### W4 (Major): Experiments lack statistical rigor

All reported metrics in Tables 2 and 3 are single-point estimates without standard deviations, confidence intervals, or multi-seed reporting. The PSNR gap between STNAdam-SARAH and STNAdam-SAGA is about 1.2 dB—meaningful if consistent, but unverifiable without variance information. Training details (epochs, batch size, learning rate schedules, hardware) are relegated to the appendix. The noise experiment (Table 3) uses post-hoc selection of only three LIE baselines, introducing selection bias. **Impact:** The central empirical claim ("superior performance") cannot be evaluated for statistical reliability or reproducibility. **Fix:** Report mean $\pm$ std over $\ge 3$ seeds, add a paired significance test against the strongest baseline, and include full training configuration in the main text.

### W5 (Major): Theoretical-empirical gap for SGD variant

Lemma 1 defines variance-reduced estimators through conditions (i)-(iii), including geometric decay of $\Upsilon_k$. The paper explicitly states that SGD does not satisfy variance reduction (Page 4), yet includes STNAdam-SGD in experiments. If the convergence analysis relies on Lemma 1, then STNAdam-SGD has no theoretical guarantee. If the analysis does not require Lemma 1, the lemma's role is unclear. **Impact:** The paper's theory does not uniformly cover all experimental variants. **Fix:** Clarify whether the convergence analysis applies to SGD variants or only to SAGA/SARAH variants; if only the latter, state this explicitly and treat SGD as an empirical ablation.

### W6 (Major): Energy function has circular parameter dependencies

The energy function $G^k$ in Eq. (9) includes terms like $(D(\mu^k)^2/(1-\mu^k)^2 - Z)\|m^k\|^2$ where $D, Z$ are free parameters "within some certain intervals." Since $\mu \in (0,1/\sqrt{2})$, the factor $(\mu^k)^2/(1-\mu^k)^2 \to 0$ as $k\to\infty$, making this term eventually negative-definite (dominated by $-Z\|m^k\|^2$). The positivity of $G^k$ as a Lyapunov function is therefore not obvious. Moreover, the parameters $M, s$ in the energy function also appear in the interval definitions (6)-(8), creating a circular dependency that is not resolved in the main text. **Impact:** The convergence analysis may have hidden gaps if the energy function is not properly bounded below. **Fix:** State explicit conditions on $M, H, Z, D$ that guarantee $G^k \ge c\|\cdot\|^2$ and show such parameters exist.

### W7 (Minor): Notation inconsistency in the two-track description

Equation (47) and Figure 1 define the extrapolation point using $\hat{x}^k$, but Algorithm 1 uses $\tilde{x}^k$ as the second-track output. The variable $\hat{x}^k$ is never defined. This inconsistency creates confusion about which variables track which sequence. **Fix:** Replace $\hat{x}^k$ with $\tilde{x}^k$ in the trajectory description.

### W8 (Minor): "Distributed optimization" terminology is incorrect

The problem formulation paragraph states "if $g(x) \equiv 0$, (1) reduces to a classic distributed optimization problem." Problem (1) is a finite-sum minimization problem; "distributed optimization" involves multiple agents, communication constraints, and consensus—none of which are present. **Fix:** Replace with "standard finite-sum smooth optimization."

### W9 (Minor): Conclusion lacks limitations and future work

The conclusion is only three sentences and does not discuss any limitations, bounded claims, or future directions. Scientific credibility requires acknowledging the scope of validation (single task, single dataset) and the theoretical limitations (KL exponent requirement, unknown rate constants). **Fix:** Restructure into three paragraphs: validated achievements, specific limitations, and concrete future work directions.

### W10 (Minor): Introduction opens with generic ML background

The first paragraph lists successful ML fields (vision, NLP, finance) with generic citations, consuming reader attention without establishing the specific optimization gap. **Fix:** Replace with a tight problem-motivation paragraph that directly introduces the "nonconvex + weakly-convex" setting and explains why existing methods fail.

### Novelty Assessment (Deferred)

Due to Retrieval-Disabled Mode (external paper search unavailable in this run), novelty and related-work positioning comparisons could not be verified against the literature. The following judgments require manual verification:
- Whether the two-track framework is genuinely novel vs. existing multi-step or look-ahead methods (e.g., AdaBelief, Lion, or two-time-scale optimizers).
- Whether the convergence analysis under KL for Adam-type methods with variance reduction overlaps significantly with existing works (e.g., Wang et al. 2019, Zhao et al. 2021, Xie et al. 2024).
- Whether the empirical gains on LIE generalize to other tasks or are benchmark-specific.

**Recommendation:** Authors should provide a detailed comparison table contrasting STNAdam with the most closely related methods (SAdam, SNAAdam, SNAdam, SAdan) along the dimensions: problem setting, convergence guarantees, gradient estimator flexibility, and empirical scope.

## Score
**Final Score: 5/10**

**Scoring Rationale:**
The paper addresses a relevant problem class (nonconvex + weakly-convex composite optimization) with a novel two-track algorithmic design and provides a rigorous theoretical convergence analysis. The empirical results on low-light image enhancement are promising. However, the score is limited by several significant weaknesses:

- **Research Value (moderate):** The two-track framework is a principled idea, but its practical advantage over simpler methods is unclear due to the unobservable constants in the adaptive parameter intervals and the gap between theory and algorithm output. The KL-based convergence rate is conditional and not directly actionable.
- **Novelty (deferred—pending literature verification):** The combination of two-track iteration with variance-reduced estimators appears novel, but without external literature search the degree of overlap with existing methods (SAdam, SNAAdam, SNAdam, SAdan, AdaBelief) cannot be independently assessed.
- **Theoretical Soundness (adequate but with gaps):** The convergence framework is logically structured, but the energy function has circular parameter dependencies, the adaptive interval bounds involve uncomputable constants, and the output variable mismatch weakens the theory-practice connection.
- **Empirical Validation (insufficient for claimed strength):** The experiments show strong quantitative results but lack statistical rigor (no variance, no significance tests, selection bias in noise comparison), and training details are deferred to the appendix.
- **Reproducibility (limited):** Missing multi-seed statistics, full hyper-parameter disclosure, and practical guidance for the adaptive intervals reduce reproducibility.

**Revision could raise the score to the 6-7 range** if the authors address the major weaknesses (W1-W6), particularly: (1) fixing the output variable mismatch, (2) providing practical default values for the adaptive intervals, (3) adding statistical rigor to experiments, (4) clarifying the theoretical coverage of SGD vs. variance-reduced variants, and (5) bounding the KL-based rate claim. Manual novelty verification via literature search could further inform the final assessment.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: nonconvex + weakly-convex composite optimization]
    |
    v
[Proposed Method: STNAdam — Two-track iteration]
    ├── Track 1 (regular): x^{k+1} = Prox(x^k, bias-corrected momentum, adaptive LR)
    └── Track 2 (extrapolation): \tilde{x}^{k+1} = Prox(\bar{x}^{k+1}, Nesterov-corrected momentum, adaptive LR)
    |
    v
[Theoretical Analysis]
    ├── Assumption 1: Coercivity of \Phi
    ├── Lemma 1: Variance-reduced gradient estimator conditions
    ├── Eq. (9): Energy function G^k (with free parameters M,H,Z,D)
    ├── Lemma 2: Expected decrease of G^k → summability of 8 sequences
    ├── Lemma 3-4: Subgradient boundedness + accumulation point properties
    ├── Lemma 5 + Theorem 1: KL-based convergence + finite-length property
    └── Theorem 2: Conditional convergence rate (depends on unknown KL exponent \vartheta)
    |
    v
[Empirical Validation]
    ├── Task: Low-Light Image Enhancement (LOL dataset, Retinex-Net framework)
    ├── Variants: STNAdam-SGD, STNAdam-SAGA, STNAdam-SARAH
    ├── Baselines: SGD, SAdam, SNAdam + 5 LIE-specific algorithms
    ├── Metrics: PSNR, SSIM, LPIPS, runtime
    └── GAPS: No variance, no multi-seed, selection bias in noise experiment
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority  | Problem                              | Fix Action                                          | Expected Impact
----------|--------------------------------------|-----------------------------------------------------|----------------
P0 (Must) | Output variable mismatch (W1)         | Add lemma connecting \tilde{x}^k and \bar{x}^k     | Theory-practice alignment
P0 (Must) | Unobservable adaptive intervals (W2)  | Provide safe defaults or practical procedure       | Practical usability
P0 (Must) | Missing statistical rigor (W4)        | Add multi-seed ±std + significance tests           | Reproducibility
P1 (Must) | SGD vs. theory gap (W5)              | Clarify theoretical coverage or remove claim       | Consistency
P1 (Must) | "Explicit rate" overclaim (W3)       | Rephrase as conditional rate                       | Honest framing
P1 (Must) | Energy function circularity (W6)      | State explicit parameter existence conditions      | Proof completeness
P2 (Nice) | Notation inconsistency (W7)           | Replace \hat{x}^k with \tilde{x}^k                | Readability
P2 (Nice) | Conclusion missing limitations (W9)   | Add limitations and future work paragraphs         | Scientific credibility
P2 (Nice) | Introduction rewrite (W10)            | Tighten opening paragraph around optimization gap  | Narrative persuasiveness
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
Related Work Taxonomy (Root: First-Order Optimization Methods)
│
├── Branch 1: Deterministic Methods
│   ├── Leaf 1.1: Gradient Descent [Nemirovski et al., 2009; Bottou, 2010]
│   ├── Leaf 1.2: Nesterov Accelerated Gradient (NAG) [Ghadimi & Lan, 2016]
│   ├── Leaf 1.3: AdaGrad [Duchi et al., 2011]
│   ├── Leaf 1.4: RMSprop [Teleman & Hinton, 2012]
│   ├── Leaf 1.5: Adam [Kingma & Ba, 2014]
│   └── Leaf 1.6: NAdam [Dozat, 2016]
│
├── Branch 2: Stochastic Methods (Adaptive)
│   ├── Leaf 2.1: SAdam (strongly convex) [Wang et al., 2019]
│   ├── Leaf 2.2: SAdam for nonconvex+convex [Le-Duc et al., 2024]
│   ├── Leaf 2.3: SNAAdam (composite) [Zhao et al., 2021]
│   ├── Leaf 2.4: SNAdam (Nesterov+Adam) [Reddi et al., 2019; Xie et al., 2024]
│   └── Leaf 2.5: SAdan [Xie et al., 2024]
│
├── Branch 3: Variance-Reduced Gradient Estimators
│   ├── Leaf 3.1: SAG [Schmidt et al., 2017]
│   ├── Leaf 3.2: SVRG [Johnson & Zhang, 2013]
│   ├── Leaf 3.3: SAGA [Defazio et al., 2014]
│   ├── Leaf 3.4: SARAH [Ghadimi & Lan, 2012; Nguyen et al., 2017]
│   └── Leaf 3.5: SPIDER
│
└── THIS PAPER: STNAdam (Two-track + Nesterov + Adaptive + Variance-Reduced)
    ├── Position: Extends Branch 2 (stochastic adaptive methods) by adding a
    │             second update track and accepting variance-reduced estimators.
    ├── Novelty Risk: Overlap with SNAdam/SAdan (both use Nesterov+Adam) and
    │                 two-time-scale methods needs literature verification.
    └── Value Contribution: First stochastic Adam variant with convergence
                            guarantees for "nonconvex + weakly-convex" composites
                            and flexible variance-reduced estimator integration.
```

**Note:** Novelty verification is deferred due to Retrieval-Disabled Mode in this run. The taxonomy tree above reflects the paper's own literature review and may miss branches not cited by the authors. Manual literature verification is required before final novelty conclusions.

### Page Coverage Audit

Since all paper content is contained in a single extracted page block (Page 1), the annotations cover all substantive sections: Abstract (1 annotation), Introduction paragraphs 1-3 (3 annotations), Related Work (1 annotation), Contributions (1 annotation), Method/Algorithm (3 annotations), Convergence/Energy Function (2 annotations), Experiments (1 annotation), and Conclusion (1 annotation). Total: 13 annotations covering all key sections.