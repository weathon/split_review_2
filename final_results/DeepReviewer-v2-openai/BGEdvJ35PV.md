## Summary
# Final Review Report

## Summary

This paper identifies and addresses a fundamental challenge in applying diffusion models to 3D molecular generation: the "dense-concentrated structure" (DC-structure) of molecular data distributions. The authors argue that molecular data occupy narrow, densely packed probability peaks separated by low-density regions, making standard diffusion fragile — small errors at intermediate timesteps can push samples off-distribution, causing irreversible structural violations. They formalize this intuition through Definition 3.1 (DC-structure) and analyze overshoot dynamics in the reverse diffusion process. Building on this analysis, they propose DIST (Diffuse and Steer), a plug-in corrective sampling method that filters intermediate distributions by running pilot reverse inferences on batches of samples, discarding trajectories that deviate from the true distribution, and retaining only valid ones. Experiments on QM9 and GEOM-Drugs with three backbone models (EDM, GeoLDM, RADM) show consistent improvements across atom stability, molecule stability, validity, and uniqueness metrics, while also reporting reduced average denoising timesteps.

The paper presents a compelling intuition about molecular distribution geometry and provides both theoretical analysis and empirical validation. However, several significant weaknesses affect its rigor and completeness: (1) the central DC-structure claim lacks direct empirical validation; (2) the theoretical analysis (Definition 3.1, Corollary 3.1, Proposition 3.1) uses imprecise mathematical formulations and idealized assumptions that limit practical implications; (3) the DIST method description is underspecified regarding critical components (pilot score function, threshold selection, batch radius); (4) the efficiency analysis uses a misleading metric that excludes pilot and overhead costs; and (5) novelty claims cannot be independently verified due to Retrieval-Disabled Mode. The experimental results are promising but require more thorough statistical and ablation analysis to fully validate the method's effectiveness.

## Strengths
1. **Clear and well-motivated problem framing.** The paper identifies a genuinely important challenge: why standard diffusion models underperform on molecular data compared to images. The DC-structure intuition (narrow, densely packed probability peaks) is clearly communicated through well-designed figures (Fig. 1) and accessible language. This conceptual contribution helps explain a phenomenon that practitioners have observed but not formalized.

2. **Model-agnostic corrective approach.** DIST is designed as a plug-in module that can be applied to any existing diffusion-based molecular generator without retraining. The experiments demonstrate consistent improvements across three diverse backbone architectures (GNN-based EDM, latent-space GeoLDM, Transformer-based RADM), supporting the claim of generality. This is practically valuable because it means DIST can be layered on top of future architectural advances.

3. **Promising empirical results.** The gains reported in Table 2 are substantial across multiple metrics. For instance, EDM's molecule stability improves from 82.0% to 89.9% on QM9, and GeoLDM's from 89.4% to 93.4%. The improvements are consistent across both datasets (QM9 and GEOM-Drugs) and all three backbones. The standard deviations (reported for QM9, ≤0.4%) suggest the improvements are statistically meaningful.

4. **Efficiency-validity trade-off exploration.** The ablation study (Table 4) systematically examines the trade-off between pilot subset size and sample quality, providing practical guidance for deployment. Finding that even a small pilot budget (30 samples) yields substantial improvements over the baseline (96.7% validity vs. 91.9%) is practically useful.

5. **Theoretical scaffolding.** Despite the imprecision issues noted in Weaknesses, the paper makes a credible attempt to place the corrective sampling idea on a theoretical footing through Definition 3.1, Corollary 3.1, and Proposition 3.1. The TV-contraction perspective on intermediate distribution correction is conceptually sound and could inspire further theoretical work on diffusion model correction strategies.

## Weaknesses
### W1. Central DC-structure claim lacks direct empirical validation (Major)

The paper's entire motivation rests on the claim that molecular data distributions are "dense-concentrated" — narrower peaks and more densely packed than image distributions. However, this claim is supported only by qualitative analogy and intuition (Fig. 1), not by quantitative distribution analysis. The paper does not report any empirical measurement of peak widths, pairwise distances between nearest-neighbor samples, or density ratios for molecular versus image data. Without this evidence, the reader cannot distinguish whether the DC-structure is a genuine scientific finding or a plausible but untested hypothesis. This weakens the empirical foundation for the entire theoretical framework.

- **Required fix:** Add an empirical analysis comparing the distribution geometry of QM9/GEOM-Drugs versus CIFAR-10/CelebA. Compute and report at least one quantitative measure: (a) average pairwise distance to nearest-neighbor in coordinate/latent space, (b) estimated eigenvalue spectrum of local covariance, or (c) fraction of mass within a small radius threshold. This analysis should appear in the main text or a dedicated appendix section.

### W2. Imprecision in the formal mathematical framework (Major)

While the authors attempt to formalize DC-structure, Definition 3.1 contains informal elements that reduce its rigor: (1) "≃" (approximately equal) is used without specifying the approximation metric or tolerance; (2) "O(Δ)" is asymptotic notation without explicit constants; (3) the covariance bound Σ_{k,t} ⪯ σ_*²I bounds eigenvalues but does not capture the "narrow peak" geometry without additional constraints. Most importantly, the definition's consequences for the score field and overshoot (Eq. 6-7) rely on approximations that are not verified against actual noise schedules. Corollary 3.1's TV-contraction bound assumes an ideal reverse kernel (perfect score model), which does not reflect operating conditions. Proposition 3.1 states an error bound f(·) whose functional form is entirely deferred to the appendix, making it uninformative in the main text.

- **Required fix:** (1) Make Definition 3.1 precise: replace "≃" with a mixture model with bounded residual in TV, replace "O(Δ)" with an explicit constant, and add a remark on what the covariance bound implies geometrically. (2) Add a complete derivation of Eq. (6-7) from Eq. (5) with the exact scaling factors, and numerically verify the overshoot condition using actual β_t schedules from the experiments. (3) Include a simplified form of the bound f(·) in the main text (e.g., a leading-order expression) so readers can interpret Proposition 3.1 without visiting the appendix. (4) Explicitly mark Corollary 3.1 as applying to the idealized perfect kernel and discuss extensions to the imperfect-kernel setting.

### W3. Underspecification of the DIST algorithm (Major)

The DIST method description introduces several critical components without concrete specification: (a) the batch radius r is never defined numerically or tied to σ_* from Definition 3.1; (b) the pilot score s_j is described through four qualitatively different examples ("round-trip residual, self-consistency, ensemble variance, or chemistry-based penalty") without stating which was actually used; (c) the threshold τ is described qualitatively without specifying the selection procedure; (d) the relationship between pilot subset size |B_j^sub| and full batch size |B_j| is not given. This underspecification prevents independent reproduction of the reported results and makes it difficult to assess whether the method's effectiveness is robust to these choices.

- **Required fix:** Provide the exact instantiation for all experiments: the specific pilot score function (e.g., molecule stability after full reverse simulation), the threshold selection criterion (e.g., top-70% quantile), the batch radius (e.g., r = 0.1·σ_*), and the pilot fraction (e.g., 1 pilot per 10 candidates). This information should be added to Appendix F.

### W4. Efficiency analysis uses a misleading metric (Major)

The paper claims "reducing the computational cost to nearly half" based on "average number of timesteps" (Table 3). This metric counts only the expected denoising steps for accepted samples after filtering. It does not account for: (1) the cost of pilot inference runs (full reverse simulation on pilot subsets), (2) the candidate pool generation (duplication, perturbation, score evaluation), and (3) the discarded samples whose computation is wasted. The total computational cost — including all overhead — could be comparable to or exceed the 1000-step baseline. The "nearly half" claim in the abstract and conclusion is therefore potentially misleading without a full computational accounting.

- **Required fix:** (1) Report total effective cost including pilot overhead (e.g., total FLOPs or wall-clock time) alongside the step counts in Table 3. (2) Add a column showing the ratio of total cost to baseline cost. (3) Revise the abstract and conclusion to state "reducing the expected number of denoising steps for accepted samples by nearly half" rather than "reducing the computational cost to nearly half."

### W5. Unverifiable novelty claims and missing comparative positioning (Minor-Major)

The contribution list claims "We are the first to highlight that molecular data distributions are highly concentrated and dense that makes diffusion-based generative processes fragile." This is a strong priority claim that cannot be verified in this review due to Retrieval-Disabled Mode. More importantly, several prior works cited by the authors themselves (Choi et al., 2025; Bohde et al., 2025; Hoogeboom et al., 2022) already discuss the narrow validity region challenge in molecular generation. The paper does not clearly differentiate the DC-structure formalization from these prior observations. The related-work comparison is deferred to Appendix B (not available in the provided manuscript), which further limits assessment.

- **Required fix:** (1) Remove or qualify the "first to highlight" claim (e.g., "To the best of our knowledge, we provide the first formal definition of the dense-concentrated structure"). (2) Add a dedicated Related Work section (not just an appendix) that explicitly compares DC-structure to prior observations about molecular generation difficulty, clearly stating what is new versus what is synthesized from existing knowledge. (3) If the appendix is essential for positioning, ensure the main text summarizes the key differentiators.

### W6. Insufficient ablation on the correction mechanism itself (Minor)

The ablation study (Table 4) varies the pilot subset size, which confirms that more pilots improve quality at higher cost. However, it does not ablate the core components of DIST: (1) What happens if we keep all samples (no filtering) but still use the same reduced timesteps? This would isolate whether the gains come from filtering or from the efficiency-implicit regularization of fewer steps. (2) What happens if we use random filtering instead of score-based filtering? This would test whether the pilot score adds value beyond stochastic subsampling. (3) What is the effect of the batch radius r? Without these ablations, the reader cannot attribute the gains to the selective correction mechanism versus simply running fewer steps or stochastic subsampling.

- **Required fix:** Add three ablations: (a) "DIST-no-filter" — same reduced timesteps but accepting all batches without pilot scoring; (b) "DIST-random-filter" — random rejection of batches at the same rate as DIST; (c) vary the batch radius r across at least two values. Report these on QM9 with EDM backbone.

### W7. Differential metric degradation in Table 1 is undiscussed (Minor)

Table 1 shows that as starting timestep increases, atom stability barely drops (99.0→98.7, -0.3pp) while molecule stability drops substantially (95.2→82.0, -13.2pp). This differential effect is interesting and potentially informative about the nature of distribution drift, but the paper does not analyze or explain it. Understanding why the DC-structure affects molecule-level constraints more severely than atom-level constraints would strengthen the connection between the theoretical framework and empirical observations.

- **Required fix:** Add 2-3 sentences interpreting the differential degradation in Table 1. Discuss whether this pattern is consistent with the overshoot mechanism in Eq. (7) and what it implies about the geometry of the molecular distribution.

### W8. Overclaiming on architectural independence (Minor)

The claim that score error is "largely independent of architectural choices" (Sec. 2.2) is based on observing that DIST improves three architectures. This is insufficient evidence for independence — it only shows that the method works across three architectures, not that architectural choices are irrelevant to score error. The supporting citations (Song et al., 2023; 2024; Joshi et al., 2025) address different aspects of score model error and do not specifically establish architectural independence.

- **Required fix:** Rephrase to "Score prediction errors persist across diverse architectural choices (GNN, Transformer, equivariant, non-equivariant, latent-space), suggesting that the DC-structure challenge is not fully addressed by architecture alone."

### W9. Undue speculation in conclusion (Minor)

The conclusion introduces two speculative directions without prior discussion: protein generation and application to other generative paradigms (normalizing flows, autoregressive models). These unsupported claims weaken the otherwise-concrete conclusion. The future work section should prioritize questions that directly arise from the current analysis.

- **Required fix:** Replace speculative statements with 2-3 concrete open questions from this work: optimal correction timestep selection, adaptive thresholding strategies, generalization to other molecular datasets with different chemical properties.

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses an important problem with a conceptually interesting approach and promising preliminary results. However, the current version has significant gaps that must be addressed before the work can be considered fully rigorous. The central DC-structure hypothesis lacks direct empirical validation. The mathematical framework, while ambitious, contains imprecise formulations and idealized assumptions that limit its practical value. The DIST method is underspecified at key decision points, preventing reproducibility. The efficiency analysis uses a metric that systematically undercounts computational cost relative to the claimed "nearly half" reduction, which could mislead readers about the method's practical benefit. Novelty claims cannot be independently verified due to Retrieval-Disabled Mode.

The core ideas — identifying narrow-peak geometry in molecular distributions and using pilot-driven corrective filtering — are valuable and likely to be influential. With (a) direct empirical validation of the DC-structure claim, (b) tighter mathematical formulations, (c) a fully specified algorithm with proper ablations, and (d) honest accounting of computational costs, the score could rise to 7-8/10. The experimental improvements (e.g., EDM molecule stability +7.9pp; GeoLDM +4.0pp) are practically meaningful and suggest the method captures a real phenomenon. The primary limitation is not in the results but in the rigor of the presentation and analysis.