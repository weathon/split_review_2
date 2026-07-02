## Summary

This paper introduces Free-Form HOI generation, extending hand-object interaction synthesis beyond the grasp-centric paradigm to include non-grasping actions like pushing, poking, tipping, and rotating. The authors contribute (1) WildO2, an in-the-wild 3D HOI dataset (4.4k samples, 92 intents, 610 object categories) built from internet videos via an automated O2HOI frame-pairing pipeline, and (2) TOUCH, a three-stage framework combining contact map prediction (CVAEs), multi-level conditioned diffusion, and physical constraints refinement. The method conditions on coarse SSC text and fine-grained DSC text with explicit contact modeling to generate diverse, physically plausible hand-object interactions.

## Strengths

1. **Well-motivated task redefinition.** The paper convincingly argues that existing HOI generation is trapped in a grasp-centric paradigm (Sec. 1), identifying specific structural limitations (palm priors, contact region assumptions) that prevent modeling actions like pushing, poking, or tipping. This reframing is concrete, not just a gap statement.

2. **Clever and scalable data pipeline.** The O2HOI frame-pairing strategy (Sec. 3.1) addresses occlusion by using object-only frames from the same video, avoiding both diffusion-inpainting geometric inconsistencies and manual labor. The mask-transfer via dense matching (Edstedt et al., 2024) from the clean frame to the interaction frame is an elegant alternative that enables automated large-scale reconstruction — critical for a dataset paper.

3. **Architecture follows task structure.** The coarse-to-fine conditioning design (Sec. 4.2, Eq. 4-5) — SSC text and global geometry in early diffusion blocks, DSC text and local contact features in later blocks — is naturally motivated by the problem: global intent constrains the overall pose, local details refine finger placement.

4. **Out-of-domain generalization demonstrated.** Fig. 7 shows plausible interactions on Objaverse CAD models, including verbs outside the primary annotated intents, providing evidence that the method generalizes beyond the training distribution.

## Weaknesses

### Fatal
None.

### Major

1. **Semantic consistency evaluation metrics are critically underspecified.** The paper uses three metrics for semantic consistency, none of which can be properly evaluated as presented:
   - **P-FID** (point-cloud FID): No feature extractor or reference distribution is specified. The citation to Nichol et al. 2022 (GLIDE) describes image FID, not point-cloud FID.
   - **VLM-assisted evaluation**: No protocol is described — what VLM model (Qwen? GPT-4V?), what prompt template, what scoring rubric, how many samples? The numbers in Table 1 (Ours: 7.1, Text2HOI: 6.5, ContactGen: 4.8) cannot be interpreted without this.
   - **Perceptual Score (N=10)**: No details on blinding, instructions, randomization, or inter-rater reliability.
   
   The metric inconsistency in Table 1 — Text2HOI scores substantially worse than ContactGen on P-FID (15.72 vs 6.08) despite scoring higher on VLM (6.5 vs 4.8) and PS (7.5 vs 6.3) — further undermines confidence. Without a transparent evaluation protocol, the headline claim of semantic consistency is not properly supported.

2. **Baseline comparison is too narrow to isolate the source of improvement.** The paper compares only against ContactGen (CVAE) and Text2HOI (diffusion model adapted by removing its temporal axis). While the paper correctly notes that existing methods have not explored this specific task, the absence of any adapted diffusion HOI baseline (e.g., retraining a grasp-oriented diffusion model on WildO2 with appropriate modifications) makes it unclear whether the performance gap comes from the method's specific design or simply from training a diffusion model on a more diverse dataset. The post-processing module used to augment baselines is described only as "optimization-based" with no details (Sec. 5.2), making the comparison non-reproducible and potentially unfair if the baselines' post-processing is weaker than the paper's own refiner.

3. **Dataset limitations and selection bias not discussed.** The automated pipeline achieves only 55% success (Fig. 3a), with 31% of failures attributed to "Pose Estimation Failure." The paper does not analyze whether the surviving 55% is biased toward simpler, more grasp-like interactions — a real concern if the pose estimator systematically fails on unusual poses. The 4.4k samples across 92 intents and 610 objects yield sparse coverage (~7 per intent on average), and the acknowledged "long-tailed distribution of hand part labels" (Sec. 5.1) means many conditions have very few examples. Neither concern is addressed in Sec. 6 (Limitations).

### Minor

4. **Ablation reveals text conditioning contributes modestly.** From Table 2: removing DSC text drops P-IoU by 0.030, removing SSC text drops by 0.041, while removing the multi-level architecture drops by 0.203. The text modality contributes positively, but the paper's narrative overweights it relative to what the evidence shows. The key innovation appears to be the multi-level architectural design and contact prediction, not the multi-level text conditioning per se.

5. **Several design details needed for reproducibility.** (a) How the hand-part mask is "initialized from the fine-grained text T_DSC" (Sec. 4.1) — is this rule-based or learned? This is the primary mechanism linking text to contact. (b) The number of TTA iterations N_tta is not reported. (c) The global pose loss (Eq. 6) and the refiner (Sec. 4.3) both address global pose drift — their relationship could be clarified.

### Trivial

6. No statistical significance reported (no error bars or multiple seeds) for Tables 1 and 2.

## Nice-to-Haves
- Adding one adapted diffusion baseline (e.g., training a grasp-oriented diffusion on WildO2) would substantially strengthen the claim that prior approaches cannot handle non-grasping interactions.
- Showing a controlled qualitative comparison on explicitly non-grasping actions (push, tip, rotate) where prior methods produce implausible grasps while TOUCH succeeds would be more convincing than the current visual comparisons.

## Removed Points
These points are flagged to be removed; treat them with caution as they were filtered for the reasons stated.
- **"PD of 0.932 — in what units?":** Removed as a formatting nitpick. Penetration Depth is standard and units (e.g., mm) can be assumed.
- **"The claim that prior LLM-guided methods fail on non-grasping prompts is unsupported":** Removed — the paper's argument is about inductive biases in model designs, not about empirical failure, and it cites Zhang et al. 2025a,b for the LLM-guidance direction.
- **"Missing related works (GraspDiff, GRAB/OakInk methods)":** Removed per hard rule — cannot verify existence/relevance of unchecked methods.
- **"The introduction makes claims without specific citations":** Removed — this is a presentation preference, not a weakness.
- **"The user study N=10 is too small":** Merged into Major #1 — the primary issue is underspecification, not sample size alone.
- **"Nothing in the paper about statistical significance":** Moved to Trivial — error bars are not standard for single-run evaluations in this field.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify the VLM evaluation protocol in full:** model used, prompt template, scoring rubric, number of samples, and provide example successful/failed generations.
2. **Describe the P-FID feature extractor and reference distribution.**
3. **Add at least one adapted diffusion baseline** (e.g., train a grasp-oriented diffusion model on WildO2 with grasp-specific losses replaced by contact-based losses).
4. **Analyze pipeline selection bias:** which interactions fail at the pose estimation stage, and is the surviving data skewed toward simpler poses?
5. **Report N_tta** and show sensitivity of performance to this hyperparameter.
6. **Clarify the text-to-hand-part-mask mapping** in Sec. 4.1 — this is critical for reproducibility.

## Score and Decision

**Round 1 Bracket (initial estimate after calibration search):** 4.0 – 6.0

**Anchor papers retrieved (all rounds):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| HOI-Diff: Text-Driven 3D HOI (ZYwLfi50GI) | 5.25 | 1, Narrow | Similar task (text-driven HOI), rejected due to limited baselines and evaluation gaps. Our paper has stronger contributions (new task + dataset) but similar evaluation weaknesses. |
| 3D Interacting Hands Diffusion (nTNElfN4O5) | 5.50 | Narrow | First diffusion for two-hand interaction, rejected for weak technical novelty and limited evaluation. Our paper has stronger technical novelty but similar evaluation concerns. |
| Interactive-Action Image Gen. (OWIk5E4lJs) | 5.20 | Narrow | Synthetic data + fine-tuning for action images. Had concerns about metric reliability and scope. Comparable evaluation gap to our paper. |
| Dynamic HOI Reconstruction (J4D5WVoc5g) | 4.50 | Narrow | Visual-tactile HOI reconstruction. Lower score due to limited comparison and unclear novelty. Our paper has stronger contributions. |
| Do EgoVLMs Understand HOI? (M8gXSFGkn2) | 7.00 | Bracketing | Benchmark + method paper with extensive experiments across multiple tasks. Our paper's evaluation is substantially less thorough. |
| HandsOnVLM (AJQuTFd9es) | 6.33 | Bracketing | Hand trajectory prediction with VLM, rejected due to underspecified details and weak baselines — similar issues to our paper. |

**Narrowing:** Compared to HOI-Diff (5.25) and IHDiff (5.50), our paper has stronger core contributions (new task formulation + new dataset + new method), which argues for a score at or above 5.5. However, the evaluation gaps — particularly the completely underspecified VLM metric and narrow baseline set — are significant enough that the paper cannot be accepted in its current form. Compared to the accepted EgoHOIBench (7.00), our evaluation is substantially less rigorous. The paper sits between a borderline reject and borderline accept.

**Final score: 5.0** — The paper introduces a genuinely novel task and provides a useful dataset and thoughtfully designed method. However, the evaluation is insufficient to support the core claims: the semantic consistency metrics are underspecified to the point of being uninterpretable, the baseline comparison is too narrow, and the dataset's limitations are not honestly discussed. These issues are fixable with substantial revision, but in the current form the evidence does not meet the bar for acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>