Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper proposes UniHM, a framework for generating sequential dexterous hand manipulation trajectories from open-vocabulary language instructions and RGB-D input. The method couples three components: (1) a Unified Hand-Dexterous Tokenizer that maps heterogeneous hand morphologies into a shared VQ-VAE codebook via staged distillation, (2) a Qwen3-0.6B-based VLM conditioned on CLIPort-derived target trajectories and point clouds, and (3) a physics-guided dynamic refinement module using Gauss-Newton optimization with contact, generative, and temporal priors. Evaluations on DexYCB and OakInk datasets plus real-world robot trials are reported.

## Strengths

- **Cross-morphology codebook is a genuine technical contribution (Sec 3.2).** The staged distillation procedure (Eq. 3) that aligns new hand encoder latent spaces to a reference encoder before full VQ-VAE fine-tuning, bypassing the gradient discontinuity of quantization, is a clean design that addresses the real engineering challenge of unifying heterogeneous hand kinematics into a shared discrete action space. The resulting pose translation across hands (Eq. 6) is straightforward and practically useful.

- **Physics-guided refinement is technically well-grounded (Sec 3.4).** The Gauss-Newton with Levenberg-Marquardt formulation (Eq. 17–18) correctly integrates three complementary priors: a contact energy with an asymmetric penalty (Eq. 12) that is soft-quadratic outside and exponential inside the object surface, a generative prior preserving intent, and a temporal prior enforcing smoothness. The mathematical derivation is clear and appropriate.

- **Real-world robot validation across diverse task types (Table 3, Figure 3).** The paper reports success rates on a physical dexterous hand across four task categories (Grab, Pick&Place, Pull&Push, Open&Close) for both seen and unseen objects. This is more real-world evidence than many manipulation papers provide.

- **The problem direction is well-motivated (Sec 1, Sec 2).** Moving from static grasp-pose generation to temporally-extended manipulation sequences guided by language is the right next step for the field.

## Weaknesses

### Major

- **The baseline selection does not support the headline SOTA claim.** The paper compares against TM2T, MDM, FlowMDM, and MotionGPT3 — human full-body motion generation methods not designed for dexterous hand manipulation. The paper acknowledges this mismatch (Sec 4.3: "we post-process their outputs with our physics-guided refinement") but post-processing does not change the underlying task misalignment. More critically, **HOIGPT (Huang et al., 2025) — cited in Sec 2.2 as extending token-based generation to long 3D hand-object interaction sequences — is a directly relevant dexterous-HOI-sequence baseline that is never quantitatively compared against anywhere in the paper.** The omission is not justified. Either HOIGPT is weaker (in which case the paper should show this) or stronger (in which case the SOTA claim is false). This gap prevents the reader from assessing whether UniHM advances the state of the art for sequential dexterous manipulation specifically.

- **The primary metrics (MPJPE, FOL, FPL) are labeled "Physically Feasible" (Sec 4.2) but measure pose accuracy against a single ground-truth trajectory.** For a generative task, many valid trajectories exist for the same instruction — different approach angles, finger configurations, wrist orientations. Penalizing deviation from one ground-truth answers a different question (pose accuracy) than the one claimed (physical feasibility). The paper states it will "validate feasibility in simulation" (Sec 4, line 208) but presents no simulation-based feasibility metrics such as collision penetration depth, force-closure quality, or simulation task success rate. Real-world success rates (Table 3) are a valid feasibility signal, but the majority of quantitative evidence (Tables 1, 2, 4) uses metrics that do not measure what they are labeled as measuring.

### Minor

- **Real-world experiments lack trial counts and statistical reporting (Table 3).** Success rates are reported as percentages without indicating the number of trials per condition, the number and identity of objects used, or the failure criteria. For example, 65% could mean 13/20 or 65/100 — the confidence intervals differ enormously. The statistical significance of improvements over baselines cannot be assessed.

- **Several underspecified implementation details.** (a) The CLIPort module (Sec 3.3) is used to predict SE(3) target trajectories from RGB-D, but CLIPort (Shridhar et al., 2022) was originally designed for pick-and-place with suction grippers predicting pixel-wise affordances. How this module was adapted to output full SE(3) hand trajectories is not explained beyond "CLIPort-style." (b) The keyframe selection procedure for GPT-4o annotation (Sec 3.1) is not described — five instructions are generated per sequence, but the criteria for selecting which keyframes to provide and whether instructions were human-verified are absent. (c) Qwen3-0.6B fine-tuning details (learning rate, batch size, training steps) are not reported.

- **The standard deviation values for TM2T, MDM, and FlowMDM in Table 1 (e.g., ±341 for a mean of 85.33 mm) are geometrically impossible for hand joint errors.** Table 2 and Table 4 show normally-formatted standard deviations (e.g., ±2.34), strongly suggesting a formatting artifact specific to Table 1 that lost decimal points. As presented, these baseline results are uninterpretable and must be corrected.

### Trivial

None beyond the standard deviation formatting issue noted above.

## Nice-to-Haves

- Include simulation-based feasibility metrics (collision counts, penetration depths, force closure) to directly substantiate the "physical feasibility" claim.
- Provide a precise definition of the "seen/unseen" split (different objects vs. different sequences with the same objects).
- Quantitatively compare against dexterous-grasp methods (SemGrasp, AffordDexGrasp) on first-frame metrics to establish whether the generation quality is competitive at the grasp level.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Teleoperation data claim overstatement (weight +1.69):** The model weight indicates this is not actually a valid weakness. The paper trains on human-object interaction data (DexYCB, OakInk), which are human demonstration datasets, not robot teleoperation data. The claim about "eliminating teleoperation" accurately describes the data paradigm, not the annotation level.
- **Diversity inconsistency across datasets:** A valid observation but not a structural weakness; the paper does not stake its core contribution on diversity.
- **Ablation: physical refinement's small effect on diversity:** The refinement's purpose is accuracy and physical realism, not diversity.
- **No explicit simulation results:** The paper already provides real-world results which are stronger evidence.
- **Failure modes not discussed:** A scope limitation, not a core weakness.
- **Seen/unseen ambiguity:** The 80/20 split is defined in Sec 4.1; more precision would help but is incremental.
- **"First" claim repetition:** Already addressed by the HOIGPT-omission weakness above.
- **Missing hyperparameters (α, k, λ_c, etc.):** Many papers in this area do not report every hyperparameter; this is not a structural gap.

## Novel Insights

Beyond the paper's own contributions, the review reveals a specific calibration gap: the paper's evaluation strategy creates a systematic disconnect between its technical contributions and its empirical claims. The cross-morphology tokenizer and physics-guided refinement are genuine contributions that the paper describes well, but the evaluation compares against methods from the wrong domain (human full-body motion) while omitting the most directly related method (HOIGPT) that the paper itself cites. Simultaneously, the main quantitative metrics measure pose accuracy while being labeled as "physical feasibility." This means a reader cannot determine, from the evidence presented, whether UniHM actually advances the state of the art for dexterous hand manipulation sequences. The real-world results are promising but underreported. The technical pieces are solid; the evaluation package needs significant strengthening.

## Suggestions

1. Include HOIGPT as a quantitative baseline on the same datasets and metrics.
2. Reframe MPJPE/FOL/FPL as "pose accuracy" rather than "physically feasible," or add genuine feasibility metrics (collision penetration, force closure, simulation task success).
3. Report trial counts (N), objects used, and confidence intervals for all real-world experiments.
4. Clarify the CLIPort adaptation: what architecture changes were needed to predict SE(3) trajectories instead of pixel-wise affordances?
5. Fix the standard deviation formatting in Table 1 so baseline numbers are interpretable.

## Score and Decision

**Calibration Details:**

| Anchor Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| xcHIiZr3DT (pseudo-tactile dexterous grasping) | 2.50 | 1 | Yes | Far weaker contribution; lacked baselines and had marginal novelty (-9.13, -9.47). UniHM is significantly stronger. |
| KBSHR4h8XV (EF-VLA early fusion) | 3.33 | 1 | Yes | Technical contribution questioned as incremental over ClearCLIP (-7.22). UniHM has more original technical contributions. |
| Aqfwhna1D7 (CrayonRobo) | 5.20 | 1 | Yes | Similar weakness magnitudes (~ -4). UniHM has slightly stronger technical strengths (+6.04 vs +6.19). |
| VYOe2eBQeh (LAPA) | 5.83 | 2 | Yes | Had severe weaknesses (-9.02 data inconsistency) but strong contribution (+7.06). UniHM's weaknesses are less severe. |
| AJQuTFd9es (HandsOnVLM) | 6.33 | 1 | Yes | **Most comparable profile.** Strengths: +6.65, +4.98. Weaknesses: -5.62, -4.80. UniHM: +6.04, +5.16 strengths; -5.57, -4.32 weaknesses. Near-identical weighted item distribution. |
| friHAl5ofG (GVL value learners) | 7.50 | 2 | Yes | Stronger experimental evaluation and clearer framing than UniHM. |
| 9pKtcJcMP3 (Video Language Planning) | 7.00 | 1 | No | More comprehensive evaluation and broader scope. |

**Initial bracket (Round 1):** 4.0–6.5

**Narrowing:** The closest anchor is HandsOnVLM (6.33), whose weighted item profile (strengths +6.65/+4.98, weaknesses -5.62/-4.80) almost exactly mirrors UniHM's (+6.04/+5.16, -5.57/-4.32). However, HandsOnVLM's weaknesses were about missing details in a newly-proposed task definition, whereas UniHM's missing-HOIGPT-baseline weakness is a more targeted evaluation gap that directly undermines the SOTA claim. Moreover, UniHM's strongest positive weight (+6.04 for the codebook) reflects a genuine architectural contribution, anchoring the paper above the 4–5 range.

**Final score:** 5.5. This reflects a paper with genuine technical contributions and a well-motivated problem, but whose evaluation in its current form does not adequately support its strongest claims. The technical pieces are solid; the empirical validation needs realignment.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline</decision>