Now let me finalize with the calibration report and score.

## Calibration Report

### Anchors Retrieved

**Round 1 (all bands):**
| Path | Avg Score | Round | Relevance |
|------|-----------|-------|-----------|
| xcHIiZr3DT.md | 2.50 | R1 | Related: vision-based dexterous grasping |
| sXF5P4N7e8.md | 3.00 | R1 | Related: goal-conditioned grasping |
| KBSHR4h8XV.md | 3.33 | R1 | Related: VLA models, generalization |
| aVyJwS1fqQ.md | 4.67 | R1 | Related: world model for manipulation |
| VaoeAi5CW8.md | 4.25 | R1 | Related: diffusion trajectory for manipulation |
| Aqfwhna1D7.md | 5.20 | R1 | Related: robot manipulation via visual prompting |
| WtHKqtHVXo.md | 4.00 | R1 | Related: policy code for manipulation |
| AJQuTFd9es.md | 6.33 | R1 | Very relevant: VLM for hand-object interaction (rejected) |
| h7aQxzKbq6.md | 6.00 | R1 | Related: hierarchical VLA (accepted) |
| c0chJTSbci.md | 6.25 | R1 | Related: zero-shot manipulation with diffusion (accepted) |
| ajSmXqgS24.md | 6.25 | R1 | Very relevant: dexterous manipulation tracking (accepted) |
| OI3RoHoWAN.md | 8.00 | R1 | Somewhat related: LLM for simulation tasks |
| 7BLXhmWvwF.md | 8.00 | R1 | Related: geometry-aware manipulation RL |

**Round 2 (narrowing):**
| Path | Avg Score | Round | Relevance |
|------|-----------|-------|-----------|
| twIPSx9qHn.md | 5.00 | R2 | Very relevant: cross-embodiment dexterous grasping (accepted) |
| HHWlwxDeRn.md | 6.00 | R2 | Related: one-shot dexterous manipulation (accepted) |
| lFYj0oibGR.md | 6.50 | R2 | Related: VLM for robot imitation, RoboFlamingo (accepted) |
| Afjf6izLvJ.md | 5.33 | R2 | Related: grounding robot policies with VLM |
| NxoFmGgWC9.md | 5.50 | R2 | Related: video pre-training for manipulation |
| nTNElfN4O5.md | 5.50 | R2 | Related: 3D interacting hands diffusion |
| ZYwLfi50GI.md | 5.25 | R2 | Related: text-driven 3D HOI generation |

### Bracketing Logic

**Round 1 bracket: 5.0–6.5.** UniHM has stronger technical contributions than the 4.0–5.0 papers (Mani-WM at 4.67, Diffusion Trajectory at 4.25), which were rejected and had thinner experimental validation. It's clearly above Cross-Embodiment Dexterous Grasping (5.0, accepted) due to more comprehensive evaluation (language conditioning, two benchmarks, ablation). It sits alongside HAMSTER (6.0, accepted) and SparseDFF (6.0, accepted), which have comparable technical depth and real-world scope. It's slightly below RoboFlamingo (6.5, accepted) because UniHM's baseline selection issue is a more significant evaluation concern than anything RoboFlamingo had.

**Final score: 6.0.** UniHM's morphology-agnostic codebook and physics refinement are genuine contributions that advance the state of the art in unified dexterous hand manipulation. The consistent improvements across two benchmarks and the fair comparison protocol (applying refinement to baselines) demonstrate solid engineering. However, the baseline comparison against only generic motion generators (not dexterous manipulation methods) prevents a higher score, as does the thinly documented real-world evaluation. This places the paper in the HAMSTER/SparseDFF range — solid work with real contributions but evaluation gaps that should be addressed.

## Summary
UniHM proposes a unified framework for language-conditioned dexterous hand manipulation across heterogeneous hand morphologies. It introduces a morphology-agnostic VQ-VAE codebook with distillation-based cross-morphology alignment, a VLM-based token generator, and a physics-guided dynamic refinement module, trained on retargeted human-object interaction data and evaluated on DexYCB, OakInk, and real-world robotic trials.

## Strengths
1. **Morphology-agnostic VQ-VAE codebook with distillation-based alignment (§3.2, Eqs. 1–6):** The staged training pipeline — distilling a new encoder's latent space to match a reference encoder (Eq. 3), then fine-tuning with standard VQ objectives (Eqs. 4–5) — is a principled approach to bypass the gradient discontinuity of non-differentiable VQ tokenization. Cross-morphology translation (Eq. 6) enables direct token reuse across five different dexterous hands.
2. **Well-designed physics-guided dynamic refinement (§3.4, Eqs. 11–18):** The contact energy uses an asymmetric, smooth penalty (Eq. 12) that is slope-matched at d=0 for stable optimization. The generative prior (Eq. 14) and temporal prior (Eq. 15) create a balanced objective, and the frame-by-frame Gauss-Newton with LM damping (Eq. 17) is a sound solver choice.
3. **Consistent quantitative improvements across two benchmarks (Tables 1, 2):** On DexYCB, UniHM reduces MPJPE from 74.80 to 61.40 (seen) and 77.93 to 63.56 (unseen). Improvements hold across FOL, FPL, FID, and Diversity metrics.
4. **Fair comparison protocol (§4.3):** Baselines also receive physics-guided refinement, ensuring gains come from the generation pipeline rather than post-processing alone.
5. **Component ablation validates each module (Table 4):** Removing masked training increases MPJPE from 61.40 to 73.41; removing depth input to 85.47; removing physical refinement to 65.78.

## Weaknesses

### Fatal
None.

### Major
1. **Baseline selection does not include competing dexterous manipulation methods — SOTA claim is overstated.** The paper compares against TM2T, MDM, FlowMDM, and MotionGPT3 (Tables 1, 2) — all generic human motion generation models retargeted to dexterous hands. Yet §2.1–2.2 discuss numerous dexterous manipulation methods (SemGrasp, AffordDexGrasp, DexMV, Multi-GraspLLM) that address language-guided grasping. While the paper correctly notes these target static poses, the omission is not justified: even a partial comparison (e.g., SemGrasp for static grasp quality, or DexMV for video-to-robot transfer) or an explicit infeasibility argument would substantially strengthen the SOTA claim. Currently, "state-of-the-art" is established only against generic motion generators.
2. **Real-world evaluation lacks critical experimental details.** Table 3 reports success rates for four task types but provides no information about: (a) number of trials per task, (b) specific objects used, (c) dexterous hand hardware, (d) success criteria, or (e) variance/confidence intervals. Success rates are round multiples of 5% (20%, 30%, 65%), suggesting very few trials. For a paper whose fourth contribution is "Generalization without Teleoperation," the reader cannot assess whether improvements are robust.

### Minor
1. **Physics refinement fairness not fully established.** The generative prior $\mathcal{E}_{\text{gen}}$ (Eq. 14) and hyperparameters ($\lambda_c$, $\mathbf{W}_{\text{gen}}$, $\mathbf{W}_{\text{vel}}$, $\mathbf{W}_{\text{acc}}$) are presumably tuned for UniHM's output distribution. Whether equally appropriate for MDM/FlowMDM outputs is not discussed. An ablation without refinement would clarify the margin's source.
2. **Lower diversity than MotionGPT3 not discussed.** On DexYCB (Table 1), UniHM's diversity is 39.62 vs. MotionGPT3's 72.51 (seen) and 42.70 vs. 75.84 (unseen), sometimes approaching or below GT (125.53). This could indicate mode collapse or reflect physical constraints, but is unacknowledged.
3. **Progressive masking schedule unspecified.** The masking curriculum is described qualitatively ("as training progresses," §4.4) but the schedule for $p_t$ (Eq. 10) is not given, hampering reproducibility.
4. **OakInk ablation missing.** Table 4 only ablates on DexYCB. Given OakInk's different object diversity (100 objects, 32 categories), an ablation there would strengthen the component analysis.

### Trivial
None.

## Nice-to-Haves
- Analysis of when physics refinement helps vs. hurts as a function of initial generation quality.
- Reporting confidence intervals and trial counts for real-world experiments.
- Discussion of the diversity gap relative to MotionGPT3.
- Specification of the progressive masking schedule ($p_t$).

## Removed Points
These points are flagged to be removed, treat them with caution.
- The harsh critic's framing that baseline selection "undermines the headline comparison" is partially kept as Major 1 but toned down: the paper's task scope (sequential language-conditioned manipulation) does narrow the field, and many cited dexterous methods target static poses. The motion generators are reasonable baselines for sequence quality, but the SOTA claim still needs better grounding.
- Critiques about formatting/typos/grammar — parser artifacts, not paper problems.
- Claims about missing appendix content — stripped by parser.

## Novel Insights
The cross-morphology distillation approach (aligning new encoder latent spaces via knowledge distillation before VQ fine-tuning, Eq. 3) is a genuinely useful technique for scaling VQ-VAE-based tokenizers to new robot morphologies without retraining from scratch. The asymmetric contact penalty with slope-matching at d=0 (Eq. 12) is also a thoughtful engineering contribution for stable contact optimization in dexterous manipulation.

## Suggestions
1. Add at least one comparison with a dexterous-manipulation method, or explicitly explain why existing methods cannot be adapted to sequential evaluation.
2. Expand real-world evaluation with trial counts, success criteria, object lists, and hardware description.
3. Add an ablation on physics refinement fairness (UniHM vs. baselines without refinement).
4. Acknowledge and analyze the diversity gap relative to MotionGPT3.
5. Specify the progressive masking schedule and report OakInk ablation results.

## Score and Decision

**Round 1 bracket: 5.0–6.5.** UniHM clearly outperforms the 4.0–5.0 rejected papers (Mani-WM, Diffusion Trajectory) which had thinner evaluations and less novelty. It's above Cross-Embodiment Dexterous Grasping (5.0, accepted) due to more comprehensive evaluation and language conditioning. It sits alongside HAMSTER (6.0, accepted) and SparseDFF (6.0, accepted), with comparable technical depth and real-world scope. It's slightly below RoboFlamingo (6.5, accepted) and DexTrack (6.25, accepted) due to the more significant baseline selection concern.

**Final score: 6.0.** The morphology-agnostic codebook and physics refinement are genuine contributions. Consistent improvements across two benchmarks and the fair comparison protocol demonstrate solid work. However, the baseline comparison against only generic motion generators and the thinly documented real-world evaluation prevent a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>