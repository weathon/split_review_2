## Summary
# Final Review Report

## Summary

This paper presents a hybrid framework for real-time interactive fluid simulation that combines a graph neural network (GNN) trained at low spatiotemporal resolution with a fallback mechanism to the classical Material Point Method (MPM). The core idea is to leverage neural physics for efficient updates while reverting to the high-fidelity numerical solver when a cosine-similarity complexity measure indicates challenging dynamics. For interactive control, the authors propose a diffusion-based generative controller (Fluid ControlNet) trained via a reverse simulation strategy that solves external force fields from forward trajectories and user sketches.

The hybrid simulator is evaluated across seven 2D/3D scenarios (water and sand, with and without ramps), reporting 11–29% per-step latency reduction versus full-resolution MPM while maintaining grid-level RMSE_m below 0.02. The Fluid ControlNet achieves 12–20% lower end-state RMSE than a constant-force baseline. The paper addresses an important practical problem—bringing neural physics acceleration and controllable fluid simulation to real-time applications—and the hybrid architecture is a sensible design choice for balancing speed and fidelity.

However, the current manuscript has several significant weaknesses: (1) experimental evaluations lack statistical variance reporting and strong baselines, making it difficult to assess the reliability and relative advantage of the proposed methods; (2) the surrogate training loss (particle RMSE_p) does not match the evaluation metric (grid RMSE_m), and the gap is not justified; (3) the fallback trigger shows only moderate correlation with simulation error and its threshold is validated only on a single scenario; (4) the fluid control baseline is weak, and improvements are modest without trajectory-level metrics or user studies; (5) the claimed latency reduction (11–29%) is incremental for a core contribution; and (6) the conclusion overstates the evidence without discussing limitations. Novelty assessment is deferred due to the unavailability of external literature retrieval in this run.

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: Real-time interactive fluid simulation]
  ├── Challenge 1: Numerical solvers (MPM) are accurate but slow
  ├── Challenge 2: Neural physics is fast but accumulates error
  └── Challenge 3: No built-in control interface for users

[Proposed Solution: Hybrid Neural-MPM]
  ├── Component A: GNN at low spatiotemporal resolution (r_p=1/1.75, r_t=2)
  │   ├── Claim: 78.8% latency reduction vs full-res neural physics
  │   └── Evidence: Water 2D comparison (1.954ms → 0.4048ms)
  ├── Component B: Cosine-similarity fallback trigger (threshold r_c=0.8)
  │   ├── Claim: Fallback corrects error accumulation
  │   ├── Evidence: Figure 7 (RMSE_m 0.0109 vs 0.0188)
  │   └── Gap: Correlation only -0.39, threshold not cross-validated
  └── Component C: Diffusion-based Fluid ControlNet
      ├── Claim: Generates force fields from sketches for fluid control
      └── Evidence: Table 3 (12-20% end-state RMSE improvement vs constant-force)

[Key Evidence Gaps]
  ├── No variance/CI reported for any experiment
  ├── Baselines: missing simple learned regressor, oracle, ablated fallback
  ├── Train-test metric mismatch (RMSE_p vs RMSE_m) not justified
  └── Control evaluation: end-state only, no user study, no trajectory metrics
```

## Strengths
**S1. Well-motivated hybrid architecture.** The core idea of combining a fast-but-approximate neural physics model with a high-fidelity numerical fallback is a sensible and practical approach to the real-time simulation problem. The design clearly identifies the complementary strengths of each component: neural networks for speed at coarse resolution, MPM for accuracy when dynamics become complex. The fallback mechanism is driven by a physically intuitive signal (cosine similarity of particle accelerations), which is computationally cheap to evaluate.

**S2. Practical problem with clear application domain.** The paper targets a genuine need in computer graphics and interactive applications: real-time fluid simulation with user-controllable behavior. The reverse simulation strategy for automatic training data generation is clever and addresses a key bottleneck in learning-based control—acquiring paired sketch-force-field data without manual annotation. The end-to-end system integration (hybrid simulation → user sketch → force field → controlled particles) is a complete pipeline that could be useful for prototyping in games, VR, and design tools.

**S3. Reasonable experiment coverage.** The evaluation spans seven distinct scenarios, including two material types (water and sand), obstacle interactions (ramps), and 3D domains. This is a broader evaluation than many prior works that focus on a single material or 2D only. The ablation of downsampling ratios (r_p, r_t) and fallback threshold (r_c) provides useful insight into the trade-offs involved in designing the hybrid system.

**S4. Reproducibility commitment.** The authors commit to releasing both models and data upon acceptance, which is valuable for a paper with a complex multi-component pipeline. If fulfilled, this would significantly lower the barrier for follow-up work.

**S5. Clean reverse simulation formulation.** The reversed simulation derivation (Eq. 3) provides a closed-form approximation for recovering external force fields from trajectory data, avoiding expensive adjoint optimization. While the assumptions need clarification (as noted in weaknesses), the overall approach is elegant and enables scalable training data generation.

## Weaknesses
**W1. No statistical variance or confidence intervals (Major).** All latency and RMSE measurements in Table 1, Table 3, and Figure 10 are reported as point estimates without standard deviation, confidence intervals, or significance tests. For example, the claimed 11.8% latency reduction on Sand 3D (1.02ms → 0.90ms, a difference of 0.12ms) could easily fall within hardware-measurement noise without multi-run repetition. This omission affects all quantitative claims in the paper. *Fix: Report mean±std over ≥3 random seeds for every latency and RMSE measurement. Add paired significance tests against the strongest baseline.*

**W2. Surrogate training loss does not match evaluation metric (Major).** Section 3.1.1 trains the neural physics model using particle-level acceleration RMSE_p at low resolution, but evaluates using grid-level mass RMSE_m at full resolution. The paper acknowledges this discrepancy but provides no empirical evidence that optimizing RMSE_p translates to good RMSE_m. The authors explicitly avoid p2g operations during training for efficiency, yet p2g is required for evaluation—creating a clear methodological inconsistency. *Fix: Compute Spearman correlation between RMSE_p and RMSE_m on a validation set. If correlation is insufficient, fine-tune with RMSE_m or a multi-task objective. Report the correlation in the paper.*

**W3. Fallback trigger has limited validation (Major).** The cosine-similarity fallback trigger achieves a Spearman correlation of only -0.39 with grid RMSE on Water 2D, meaning roughly 85% of the variance in error is unexplained. The threshold r_c = 0.8 is selected based solely on Water 2D ablation (Figure 6d) and is not validated on held-out scenarios or other material types. Since sand and water have different dynamics, the optimal threshold likely differs. *Fix: (a) Report Spearman correlation and AUC for the cosine-similarity trigger across all six evaluated scenarios; (b) validate r_c = 0.8 on each scenario or propose per-scenario tuning; (c) consider an adaptive threshold that tracks recent error trends.*

**W4. Fluid control evaluation is insufficient (Major).** The generative fluid control contribution has four specific deficiencies: (i) the only baseline is a constant spatiotemporal force field—a very weak comparator; (ii) improvements are modest (12–20% RMSE reduction), with no statistical significance reported; (iii) only end-state RMSE is measured, ignoring trajectory quality, smoothness, and intermediate deviation from the sketch; (iv) no human evaluation is conducted despite the claim of "user-friendly" control. *Fix: Add a learned non-diffusion baseline (MLP or UNet predicting force fields), report trajectory-level metrics (average RMSE, shape IoU at each step), and include a small user study (≥10 raters) comparing controlled fluid naturalness.*

**W5. Incremental empirical gains relative to contribution strength (Moderate).** The headline improvement of 11–29% latency reduction versus full-resolution MPM is modest for a core contribution at a top venue. Moreover, the comparison with MPM at matched low resolution (r_p = 1/1.75) shows that MPM is already quite fast (Figure 10), and the hybrid's advantage over low-res MPM is even smaller. The 78.8% reduction cited for Water 2D is versus the original neural physics at full resolution—not against the operational baseline (MPM). This framing can give a misleading impression of the practical speedup. *Fix: Clarify all comparisons with explicit baseline labels: "(vs full-res MPM)" and "(vs neural physics at matched resolution)." Add a summary table showing absolute latency, relative reduction, and RMSE for each method.*

**W6. Surrogate loss and evaluation metric notation issues (Moderate).** The paper switches notation several times: RMSE_β in Section 2.2 is defined as the particle-level acceleration loss, but later the grid-level metric is RMSE_m with a tilde variant (RMSE_̃m) and a bar variant (RMSE_¯m). Equation (3) uses a_t for acceleration but the diffusion model uses α for the same concept. These inconsistencies, while not fatal, reduce readability and create opportunities for confusion during implementation. *Fix: Unify notation: use RMSE_p for particle-level, RMSE_m for grid-level, and a single symbol for predicted acceleration/force.*

**W7. Conclusion overstates without limitations (Minor).** The conclusion claims "robust, low-latency fluid dynamics capable of handling complex scenarios" and "extensive experiments" but does not mention key limitations: only two material types, modest particle counts (4k), per-scenario training, fixed control horizon, and moderate fallback correlation. *Fix: Restructure conclusion into validated findings, bounded limitations, and concrete future priorities (see Annotation 10 for a revised version).*

**W8. Limited novelty verification (deferred).** Due to the unavailability of external literature retrieval in this run, I cannot verify novelty claims against prior work. The paper claims a novel hybrid neural-numerical framework with diffusion-based control, but the individual components (GNN-based physics, MPM, diffusion models, reverse simulation) are each established techniques. The novelty lies primarily in the integration and the specific fallback design. A manual literature verification is required to assess overlap with concurrent works such as MPMNet, Neural SPH, and differentiable physics hybrids. *Status: Deferred manual verification.*

```text
ASCII Diagram — Revision Strategy Roadmap

W1 (No variance)            →  Add ≥3 seeds, CI, significance tests   →  Statistical reliability
W2 (Loss-metric mismatch)   →  Validate RMSE_p↔RMSE_m correlation     →  Methodological consistency
W3 (Weak fallback trigger) →  Cross-scenario validation + adaptive τ  →  Reliable hybrid safeguard
W4 (Weak control eval)     →  Add learned baseline, traj. metrics     →  Convincing control demo
W5 (Incremental gains)     →  Clarify baselines, add summary table    →  Honest contribution framing
W6 (Notation)              →  Unify symbols                            →  Readability
W7 (Conclusion)            →  Add limitations + future work           →  Scientific completeness
W8 (Novelty)               →  Manual literature verification          →  Novelty assessment

Priority ordering for revision: W1 (most critical for validity) > W2 > W4 > W3 > W5 > W7 > W6 > W8.
```

## Score
**Final Score: 5/10**

**Rationale.** The paper addresses a relevant and practical problem—real-time interactive fluid simulation—with a sensible hybrid architecture that combines GNN-based neural physics and MPM with a cosine-similarity fallback. The reverse simulation strategy for generating training data is clever. However, the overall contribution is significantly weakened by four major evidence gaps: (1) no variance or statistical significance is reported for any experimental result, making the claimed improvements unverifiable; (2) the surrogate training loss does not match the evaluation metric, with no empirical justification; (3) the fallback trigger is validated on a single scenario with moderate correlation; and (4) the fluid control evaluation uses a weak baseline and reports only end-state metrics without trajectory quality or user studies. The latency improvements (11–29% vs MPM) are modest for a core contribution. Novelty assessment requires manual literature verification, which was unavailable in this review run. The paper has a solid technical foundation and addresses an important application, but the current evidence does not yet support the strength of the claims made. Substantial revisions to the experimental methodology and framing are required before the paper can be considered for acceptance.