## Summary

This paper proposes a post-training fine-tuning framework for flow-matching generative models that enforces PDE-based physical constraints and jointly infers latent PDE parameters. The method combines adjoint matching (Domingo-Enrich et al., 2025) with weak-form PDE residuals and a joint state-parameter evolution, enabling physically consistent generation from models trained only on observed states. The framework is evaluated on four PDE families (Darcy flow, linear elasticity, Helmholtz, Stokes) and a natural-image application.

## Strengths

1. **Well-motivated problem framing.** The paper identifies a genuine difficulty: scientific generative models trained on observed states learn surface statistics while ignoring governing physics, and PDE parameters needed to evaluate constraints are typically unobserved. The post-training/fine-tuning design point is practically appealing and fills a clear gap.

2. **Scaled memoryless noise schedule (κ) is a concrete theoretical extension.** The observation that a family of scaled schedules preserves the memoryless property (Section 3.3, Lemma 1 in Appendix D.4) gives practitioners a useful tuning knob for numerical stability, extending the original adjoint-matching framework beyond the single canonical schedule previously identified.

3. **Ablation on Darcy (Figure 3) clearly maps the trade-off space.** Systematic sweeps over λ_x/λ_α and λ_f demonstrate that the practitioner can target either residual reduction or distributional fidelity, and that these are in tension. This makes the method's behavior interpretable and guides hyperparameter selection.

4. **Computational cost is low and honestly reported.** Fine-tuning on Darcy completes "under 15 minutes on a single NVIDIA L40S" with only 20 gradient steps (Section 4.1). This aligns with the paper's stated motivation for lightweight post-training enforcement.

## Weaknesses

### Fatal
None.

### Major

1. **Inverse problem claims are not quantitatively validated at the per-sample level.** The abstract and contributions claim "accurate recovery of latent coefficients" and that the method "effectively addresses ill-posed inverse problems." However, **no per-sample parameter recovery accuracy is reported anywhere in the paper.** The only parameter metric is MMD_α, a distributional distance — a method could achieve low MMD_α while making large errors on individual samples. Ground-truth parameters are available from the reference dataset D_ref (explicitly described as containing data generated under known target PDE specifications), yet no direct comparison such as relative L2 error, correlation, or coverage is provided. This gap directly undermines a central advertised contribution. The paper needs to report per-sample accuracy or temper its claims.

2. **Helmholtz results have overlapping confidence intervals that do not clearly support the claimed superiority.** In Table 2, AM achieves R_weak = 4.3 ± 1.29 vs. Base AM at 4.9 ± 1.85. The difference (0.6) is much smaller than the standard deviations (1.3–1.9). The paper states "Our full joint AM model achieves the lowest residuals overall" without any statistical testing. While the broader multi-experiment trends are directionally consistent, the Helmholtz evidence alone is too noisy to support a strong superiority claim.

### Minor

1. **Natural image experiment is too thin to support the claimed generality.** Section 4.6 evaluates a single class ("macaw") with one prompt and shows only qualitative samples (Figure 6). No quantitative metrics (PickScore, FID, CLIP score) and no comparison to standard image fine-tuning methods (DreamBooth, LoRA, vanilla reward tuning) are provided. The cross-domain utility claim would benefit from basic quantitative evaluation.

2. **Guidance experiment lacks quantitative evaluation and comparison.** Section 4.2 shows three qualitative samples conditioned on sparse observations but provides no quantitative metric (posterior coverage, marginal likelihood, or comparison to Huang et al. (2024)'s guidance approach, which the paper explicitly cites). Since the guidance setting is exactly where Huang et al. applies, a comparison would meaningfully strengthen the evaluation.

3. **No ablation isolates the benefit of the joint flow from added model capacity.** The joint model adds a separate head for v_{t,α} and conditions v_{t,x} on α_t. It is unclear how much improvement comes from the joint evolution mechanism versus simply having more parameters. A control experiment (e.g., a wider v_{t,x} network without the α-flow, matched for parameter count) would isolate this.

### Trivial
None.

## Nice-to-Haves
- Direct per-sample parameter recovery metric (relative L2 error) using the ground-truth parameters already available in D_ref.
- Statistical significance testing (e.g., paired bootstrap) for the Helmholtz comparisons where method differences are small relative to variance.
- Ablation controlling for added model capacity in the joint flow vs. Base AM comparison.
- Quantitative metrics (PickScore/FID) and a standard baseline for the natural image experiment.
- Comparison to Huang et al. (2024)'s guidance approach in the guidance setting.

## Removed Points

These points were raised by the reviewer but removed after verification against the paper:

- **"Missing comparison to pre-training (Bastek et al. 2024)"**: The paper already compares against PBFM (Baldan et al., 2025), which is a flow-matching pre-training baseline that embeds PDE constraints during training. Requesting a separate Bastek-style baseline adapted from DDPMs to flow matching goes beyond standard evaluation expectations.

- **"Missing comparison to inference-time projection (Christopher et al., Utkarsh et al.)"**: The paper includes FM+ECI (Cheng et al., 2024) in the elasticity experiment (Table 1), which is an inference-time projection method specifically designed for flow matching. This comparison is present.

- **"Introduction overstates prior work limitations"**: The paper says prior work "has largely focused on simple or global constraints" — a reasonable characterization of the literature's emphasis. The paper acknowledges Bastek et al. and PBFM in Related Work, so there is no misrepresentation.

- **"Method error compounding not analyzed"**: The surrogate base flow uses one-step Euler estimate + φ, stacking two approximations. This is a valid observation but standard practice in amortized inference settings; the paper demonstrates empirical effectiveness across four PDE systems.

- **"Reference set D_ref conflates metrics"**: The paper explicitly states D_ref is "generated under the target PDE specification assumed during fine-tuning (no noise, modified BCs, lossless Helmholtz, or unforced Stokes respectively)" — this is transparently disclosed, not a hidden confound.

- **"Missing appendix/proofs/supplementary"**: The parser strips these sections from all papers at this venue; they exist in the original submission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report per-sample parameter recovery accuracy (relative L2 error or mean correlation) for each PDE experiment using the ground-truth parameters already available in D_ref. This single addition would directly validate or qualify the inverse problem claims.
2. Add statistical significance assessment (e.g., paired bootstrap confidence intervals) for the Helmholtz results where method differences are small relative to variance.
3. Either add quantitative metrics or a standard fine-tuning baseline to the natural image experiment, or remove this experiment as it does not currently provide meaningful evidence.
4. Include a comparison to Huang et al. (2024) in the guidance setting (Section 4.2).
5. Add an ablation that controls for added model capacity (e.g., wider network without α-flow, matched parameter count) to isolate the benefit of the joint evolution mechanism.

## Score and Decision

**Calibration anchors** (all retrieved across rounds):

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| Physics-Informed Diffusion Models (tpYeermigp) | 5.75 | R1 | Similar topic, accepted; has cleaner evaluation, fewer gaps |
| Flow Matching for Posterior Inference (DoDNJdDntB) | 4.20 | R1,R2 | Similar method concept; our paper is stronger (more experiments, clearer) |
| Efficient Physics-Constrained Diffusion Models (Da3j02cHe0) | 3.60 | R1,R2 | Similar topic; our paper has stronger methodology and more experiments |
| Correcting Flows with Marginal Matching (kRjLBXWn1T) | 5.25 | R2 | Similar novelty level; both have evaluation gaps, but ours are more central to claims |
| Consistency Flow Matching (bS76qaGbel) | 5.67 | R1 | Flow matching method paper with evaluation gaps but cleaner claims |
| Solving DEs with Constrained Learning (5KqveQdXiZ) | 5.25 | R2 | Related PDE-constrained approach with different methodology |

**Round 1 bracket**: 4.0–5.5. The paper is stronger than DoDNJdDntB (4.20) due to broader evaluation and clearer methodology, but weaker than tpYeermigp (5.75, accepted) due to more significant evaluation gaps — particularly the unsupported inverse problem claims.

**Final narrowing**: Against kRjLBXWn1T (5.25, rejected) — both papers have novel methods with evaluation gaps, but our paper's gaps (unvalidated inverse problem claims, thin qualitative-only experiments for guidance and images) more directly affect the stated contributions. Score set at 5.0.

The paper proposes a technically coherent method and identifies a real problem. However, a central claim — accurate recovery of latent coefficients for inverse problems — is entirely unvalidated at the per-sample level, despite ground-truth data being available. Other comparative claims rest on overlapping error bars without statistical testing. The paper needs substantial evaluation strengthening before its contributions can be assessed at their claimed level.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>