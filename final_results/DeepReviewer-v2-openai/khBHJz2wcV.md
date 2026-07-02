## Summary
# Final Review Report

## Summary

This paper proposes a post-training fine-tuning framework for flow-matching generative models to enforce parameter-dependent PDE constraints without requiring paired parameter-solution training data. The method combines weak-form PDE residuals with the Adjoint Matching framework (Domingo-Enrich et al., 2025) to tilt the generative distribution toward physically consistent samples. A key technical innovation is the joint evolution of state variables $x$ and latent physical parameters $\alpha$ through a surrogate base flow constructed via an inverse predictor $\varphi$, enabling inverse problem inference from observational data alone. The framework is evaluated on four PDE families (Darcy flow, linear elasticity, Helmholtz, Stokes) and one natural-image task, demonstrating reduced PDE residuals while maintaining distributional fidelity through tunable hyperparameters.

**Core Contributions (C1–C3):**
- **C1:** Post-training enforcement of physical constraints via weak-form PDE residuals within a fine-tuning paradigm.
- **C2:** Adjoint-matching fine-tuning extended to joint generation of latent parameters alongside states, enabling inverse problem inference without paired data.
- **C3:** Scaled memoryless noise schedule providing a numerical stabilization knob for the adjoint-matching framework.

**Novelty Status (Retrieval-Disabled Mode Active — Deferred Verification):**
External literature verification was not available in this run due to API limitations. Novelty/comparison conclusions are based solely on manuscript evidence and are marked as requiring manual verification. The proposed framework builds on Adjoint Matching (Domingo-Enrich et al., 2025) and extends it with joint parameter evolution and scaled noise scheduling. Whether these extensions constitute sufficient novelty over existing physics-constrained generative models (e.g., PBFM, physics-constrained diffusion, projection-based methods) cannot be fully determined without external retrieval.

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: Parameter-dependent PDE constraints without joint training data]
    |
    v
[Proposed Solution: Post-training fine-tuning of FM via Adjoint Matching]
    |
    +--[Method Component 1: Weak-form PDE residuals (R_weak)]
    |     Evidence: Sec 3.1, Eq for R_weak using local test functions
    |     Gap: No analysis of N_test sensitivity or test function hyperparameters
    |
    +--[Method Component 2: Joint evolution of x and alpha]
    |     Evidence: Sec 3.2, surrogate base flow via inverse predictor phi
    |     Gap: No analysis of phi error propagation through surrogate flow
    |
    +--[Method Component 3: Scaled memoryless noise schedule]
    |     Evidence: Sec 3.3, sigma^2(t) = (1-kappa)2*eta_t
    |     Gap: Novelty claim overstated for trivial multiplicative scaling
    |
    v
[Empirical Evaluation: 4 PDE systems + natural images]
    |
    +--[Darcy Flow: Residual reduction, tunable trade-off]
    |     Gap: Single-seed qualitative; no error bars on MMD/SSIM
    |
    +--[Linear Elasticity: Low residuals, modest distributional shift]
    |     Gap: FM+ECI zero BC footnote needed
    |
    +--[Helmholtz: Best residuals among methods]
    |     Gap: Selective "representative configurations" reporting
    |
    +--[Stokes: Joint model enters low-MMD regime]
    |     Gap: PBFM failure unexplained; selective omission in plot
    |
    +--[Natural Images: Qualitative only, no metrics]
          Gap: Missing FID/PickScore/CLIP quantitative evaluation
```

```text
ASCII Diagram — Revision Strategy Roadmap

[Priority 0 — Scientific Rigor]
    |-- Add statistical uncertainty (error bars, multi-seed) to all experiments
    |-- Report absolute residuals alongside relative ones
    |-- Include all methods in scatter plots (no selective omission)
    v
[Priority 1 — Claim Bounding & Honesty]
    |-- Rewrite abstract: replace "without distorting" with bounded trade-off
    |-- Tone down "novel extension" claim for scaled noise schedule
    |-- Add explicit discussion of inverse predictor error sensitivity
    v
[Priority 2 — Completeness]
    |-- Add quantitative metrics for natural images experiment
    |-- Provide main-text sketch of guidance mechanism for sparse obs
    |-- Restructure conclusion with specific validated findings
    v
[Priority 3 — Presentation Polish]
    |-- Fix mixed narrative roles in introduction paragraphs
    |-- Clarify selection criteria for comparative tables
    |-- Add footnotes for ECI zero-error entries
```

## Strengths
**S1 — Well-motivated problem with practical significance.** The paper addresses a genuinely important challenge in scientific machine learning: enforcing parameter-dependent PDE constraints in generative models without requiring paired parameter-solution training data. This problem arises naturally in atmospheric modeling, seismic inversion, and medical imaging, where latent physical parameters are unobserved. The motivation is clearly articulated and the proposed approach of post-training fine-tuning is a practical paradigm.

**S2 — Clean integration of adjoint matching with PDE residuals.** The reformulation of physics-constrained fine-tuning as a stochastic optimal control problem via Adjoint Matching (Domingo-Enrich et al., 2025) is technically sound. The use of weak-form residuals with local test functions is a sensible choice for numerical stability, and the connection to reward-based fine-tuning provides a principled theoretical foundation. The joint evolution of states and parameters via a surrogate base flow is a creative solution to the challenge of missing ground-truth parameter dynamics.

**S3 — Comprehensive PDE evaluation across diverse systems.** The experimental evaluation covers four distinct PDE families (elliptic diffusion, elasticity, wave propagation, incompressible flow), spanning both elliptic and hyperbolic regimes with different types of model misspecification (noisy observations, boundary condition mismatch, damping mismatch, forcing mismatch). This breadth strengthens the claim that the method is general-purpose rather than tailored to a specific PDE.

**S4 — Tunable trade-off mechanism with practical potential.** The introduction of hyperparameters $(\lambda_x, \lambda_\alpha, \lambda_f)$ provides explicit control over the balance between PDE residual reduction and distributional fidelity. The Darcy ablation study (Fig. 3) demonstrates this trade-off empirically, which is valuable for practitioners who may prioritize different objectives depending on the application.

**S5 — Computational efficiency.** The Darcy fine-tuning requiring only 20 gradient steps and completing in under 15 minutes on a single L40S GPU is a practical strength, as it suggests the method can be applied to existing pre-trained models without massive compute budgets. The fact that sampling proceeds at base-model cost with no inference-time adjustments is also notable.

**S6 — Open-source code release.** The authors provide an implementation at GitHub, which supports reproducibility and enables further research building on this work.

## Weaknesses
**W1 — Abstract overclaims distribution preservation (Critical).** The abstract states the method promotes "physical consistency and adherence to boundary conditions without distorting the underlying learned distribution." This directly contradicts the paper's own empirical findings: Fig. 3(a) shows that increasing $\lambda_x = \lambda_\alpha$ reduces PDE residuals but simultaneously reduces SSIM-based diversity in inferred parameters, and Fig. 3(b) demonstrates a systematic trade-off where stronger regularization preserves distributional fidelity at the cost of higher residuals. The phrase "without distorting" is scientifically indefensible given these results. This is not a minor phrasing issue — it misrepresents the core behavior of the method and would mislead readers about a fundamental limitation. **Fix:** Replace with an honest characterization of the tunable trade-off, as proposed in the Abstract annotation (Page 1 - Abstract).

**W2 — Statistical rigor is insufficient across all experiments (Major).** Several critical weaknesses in statistical reporting undermine confidence in the results:
- (a) No error bars, confidence intervals, or standard deviations are reported on the MMD and SSIM-diversity metrics in Fig. 3, despite claims being based on 256 samples.
- (b) The Darcy qualitative comparison (Fig. 2) shows a single seed with no indication of representativeness.
- (c) The Helmholtz comparison (Table 2) selects "representative configurations" using different criteria per method (some optimized for R_weak, others for MMD_x), introducing selection bias. Full results are deferred to the appendix.
- (d) The Stokes scatter plot (Fig. 5) omits the FM baseline and PBFM "for clarity," creating a potentially misleading visual comparison.
**Fix:** Add error bars/confidence bands to all quantitative plots. Use a consistent selection criterion for all methods in main tables. Include all baselines in scatter plots (use insets or zoom panels for large-residual methods).

**W3 — Natural images experiment lacks quantitative evaluation (Major).** The cross-domain validation on natural images (Section 4.6) is entirely qualitative: "joint fine-tuning with recoloring produces markedly more vibrant palettes." No FID, IS, CLIP score, PickScore, or any other quantitative metric is reported. Without numerical comparison between vanilla Adjoint Matching and the joint model, the reader cannot assess whether the joint approach genuinely improves quality or whether the shown examples are cherry-picked. For an experiment intended to "demonstrate cross-domain utility," this is a significant evidentiary gap. **Fix:** Add a quantitative comparison table (PickScore, FID, CLIP score) over at least 256 samples with standard deviations, as proposed in the annotation on Page 9 - Natural Images.

**W4 — Scaled noise schedule novelty claim is overstated (Major).** The paper claims the scaled memoryless noise schedule $\sigma^2(t) = (1-\kappa)2\eta_t$ "constitutes a simple but novel extension of the adjoint-matching framework" and that "our analysis shows that a family of scaled schedules remains consistent with the memoryless condition." If the memoryless condition is linear in $\sigma^2$ (which it appears to be, given the canonical choice $\sigma^2(t) = 2\eta_t$), then multiplying by a constant trivially preserves the property without new analysis. The theoretical justification (Lemma 1) is deferred entirely to Appendix D.4. The claim would be more credible if presented as a practical stabilization technique rather than a theoretical advance. **Fix:** Reframe as a practical numerical stabilization technique and provide a brief proof sketch in the main text, as proposed in the annotation on Page 5 - Adjoint Matching.

**W5 — Surrogate base flow sensitivity to inverse predictor quality is unanalyzed (Major).** The joint evolution framework (Section 3.2) constructs the surrogate base flow $v_{t,\alpha}^{\text{base}}$ using one-step predictions $\hat{x}_1$ and the inverse predictor $\varphi$. The accuracy of this surrogate flow depends critically on $\varphi$'s ability to estimate parameters from partially denoised samples. If $\varphi$ is poorly calibrated for intermediate noisy states (especially early in the flow), the surrogate flow could systematically misguide the parameter evolution. The paper provides no analysis of this sensitivity, no ablation of $\varphi$ pre-training quality, and no online correction mechanism. **Fix:** Add an analysis of how $\varphi$ errors propagate through the surrogate flow, and investigate sensitivity to $\varphi$ pre-training quality as proposed in the annotation on Page 4 - Joint Evolution.

**W6 — Comparison fairness concerns in experimental evaluation (Major).**
- **PBFM failure in Stokes (Section 4.5):** PBFM "fails to converge to meaningful velocity-pressure fields" but no analysis is provided of *why* it fails. Possible causes include architectural incompatibility, hyperparameter choices not tuned for PBFM, or fundamental limitations of training-time constraint embedding under model misspecification.
- **FM+ECI zero BC error (Table 1):** The entry "0.0" for FM+ECI's boundary condition error is presented without explanation that ECI enforces BCs via hard projection by design. This makes the comparison appear misleading.
- **Helmholtz "representative configurations":** Methods are evaluated under different optimization criteria, creating an apples-to-oranges comparison.
**Fix:** Add failure analysis for PBFM. Footnote the zero-error entry. Use consistent selection criteria across all methods.

**W7 — Guidance mechanism for sparse observations is underspecified in the main text (Major).** The guidance mechanism (Section 4.2) is described in only 3 sentences, with all technical details deferred to Appendix E.4. The main text does not explain how the guidance term is constructed, how sparse observations are integrated into the joint evolution, or how guidance strength is controlled. For a core claimed capability (inverse problem inference from sparse observations), this level of detail is insufficient for main-text evaluation. **Fix:** Provide a 2-3 sentence technical sketch of the guidance mechanism in the main text, as proposed in the annotation on Page 7 - Guidance on Sparse Observations.

**W8 — Evaluation metrics may be biased toward the assumed PDE specification (Major).** The MMD metrics are computed against $\mathcal{D}_{\text{ref}}$, a "synthetic, clean dataset generated under the target PDE specification assumed during fine-tuning." This means a model that perfectly matches the (potentially incorrect) assumed PDE specification scores well on MMD even if it deviates from actual physics. Relative residuals are also scaled by the mean residual of this reference set. Without also reporting absolute residuals or MMD against the original training data, the evaluation may overstate the method's ability to capture real physical behavior. **Fix:** Report absolute residuals alongside relative ones, and compute MMD against both $\mathcal{D}_{\text{ref}}$ and the original training dataset.

**W9 — Introduction narrative structure is suboptimal (Minor).** The introduction mixes gap identification and solution preview across paragraphs, making the narrative arc harder to follow. The second paragraph ends with a solution preview that belongs in the third paragraph, and the third paragraph is a single compressed sentence that crams method, evaluation scope, results, and claims together. The contribution list includes C3 ("Bridging Generative Modeling and Physics-Informed Learning"), which is a positioning statement rather than a specific technical contribution. **Fix:** Restructure introduction with clear role separation per paragraph. Replace C3 with a concrete technical claim.

**W10 — Conclusion lacks specific validated findings (Minor).** The conclusion re-announces the method vaguely ("Through a novel architecture, combined with the combination of...") and lists four unmotivated future directions without prioritization. No specific quantitative achievements are mentioned. **Fix:** Restructure into validated findings with quantitative anchors, bounded limitations, and 1-2 prioritized future directions, as proposed in the annotation on Page 9 - Conclusion.

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)
(Note: External verification deferred; taxonomy based on manuscript's own citations)

Related Work: Physics-Constrained Generative Models (Root)
├── Branch 1: Pre-training constraint embedding
│   ├── Leaf 1.1: Diffusion + physics residual loss
│   │   └── Bastek et al. (2024)
│   ├── Leaf 1.2: Flow matching + physics loss (PBFM)
│   │   └── Baldan et al. (2025)
│   └── Leaf 1.3: Distillation-based constraint enforcement
│       └── Zhang & Zou (2025)
├── Branch 2: Inference-time / post-hoc constraint enforcement
│   ├── Leaf 2.1: Guidance-based steering
│   │   ├── Huang et al. (2024)
│   │   └── Xu et al. (2025)
│   ├── Leaf 2.2: Projection-based hard constraints (ECI)
│   │   ├── Christopher et al. (2024)
│   │   ├── Cheng et al. (2024)
│   │   └── Utkarsh et al. (2025)
│   └── Leaf 2.3: Post-training fine-tuning (THIS PAPER)
│       └── Adjoint Matching + PDE residuals (proposed)
├── Branch 3: Generative models for Bayesian inverse problems
│   ├── Leaf 3.1: Conditional diffusion for posterior inference
│   │   ├── Song et al. (2021)
│   │   └── Zhang et al. (2023)
│   └── Leaf 3.2: Flow matching for simulation
│       ├── Price et al. (2023) [weather]
│       ├── Hassan et al. (2024) [molecular]
│       └── Zhang et al. (2025) [geology]
└── Branch 4: Classical physics-informed learning (non-generative)
    └── Leaf 4.1: PINNs
        └── Raissi et al. (2019)
```

**Note on Novelty (Retrieval-Disabled Mode):** External literature search was unavailable for this run. The taxonomy above is constructed from the manuscript's own citations. All novelty verdicts require manual verification against the broader literature. Based on manuscript evidence alone, the core technical novelty lies in extending Adjoint Matching to joint state-parameter evolution and applying it to PDE-constrained fine-tuning. The scaled noise schedule is a minor practical modification. Whether these extensions are sufficient relative to the rapidly evolving literature on physics-constrained generative models (especially concurrent work on flow-matching constraint enforcement) cannot be determined without external retrieval.

**Page Coverage Audit:**
The paper is contained in a single PDF page with all main-body content. All substantive paragraphs across Abstract, Introduction (P1-P3), Related Work, Method (Reward, Joint Evolution, Adjoint Matching), Experiments (setup, Darcy, Guidance, Elasticity, Helmholtz, Stokes, Natural Images), and Conclusion received at least one annotation. Non-substantive elements (figure captions, author affiliations, code repository link) were skipped as boilerplate. Total annotations: 15 (within recommended 12-25 range).

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses an important and well-motivated problem with a technically sound approach. The integration of Adjoint Matching with weak-form PDE residuals for post-training fine-tuning is principled, and the joint evolution of states and parameters provides a creative solution to the challenge of missing ground-truth parameter dynamics. The comprehensive evaluation across four PDE families demonstrates breadth and the computational efficiency is a practical strength.

However, the score is constrained by several significant concerns that affect research value and scientific credibility:

1. **Scientific overclaim in the abstract (Critical):** The claim of achieving constraint enforcement "without distorting the underlying learned distribution" directly contradicts the paper's own empirical findings showing a systematic trade-off. This misrepresentation undermines trust.

2. **Statistical rigor gaps (Major):** Multiple experiments lack error bars, confidence intervals, or consistent evaluation criteria. Selective reporting (omitting baselines from plots, using different optimization criteria across methods) weakens the comparative evaluation.

3. **Missing quantitative validation for cross-domain claim (Major):** The natural images experiment — the only evidence for "cross-domain utility" — is entirely qualitative.

4. **Novelty uncertainty (Deferred verification):** Without external literature retrieval, the novelty relative to concurrent work in physics-constrained generative modeling cannot be fully assessed. The scaled noise schedule contribution appears overstated.

5. **Underspecified critical components (Major):** The guidance mechanism for sparse observations is barely described in the main text, and the surrogate base flow's sensitivity to inverse predictor quality is unanalyzed.

The paper has a solid technical core and the main idea is interesting, but the evidence presentation needs substantial improvement before the claimed contributions can be accepted at face value. The fixable nature of most weaknesses (adding error bars, rewriting overclaims, adding quantitative metrics) means the score could improve significantly with a careful revision.