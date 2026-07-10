Now I have a clear picture of the calibration landscape. Let me write the final review.

## Summary

This paper introduces the task of **Free-Form HOI Generation**, moving beyond the grasp-centric paradigm that dominates existing work to enable generation of diverse hand-object interactions (pushing, poking, rotating, pressing, etc.). The authors contribute: (1) **WildO2**, a dataset of 4.4k 3D HOI samples spanning 92 intents and 610 object categories, built from Something-Something V2 videos via a semi-automated reconstruction pipeline; (2) **TOUCH**, a three-stage framework with contact map prediction, multi-level conditioned diffusion (coarse SSC → fine DSC), and physical refinement with a self-supervised cycle-consistency loss; (3) comprehensive experiments including ablations, out-of-domain generalization, and force-semantics analysis.

## Strengths

- **Well-motivated problem shift (Sec. 1, Abstract).** The observation that existing HOI generation is overwhelmingly grasp-centric and excludes non-grasping interactions is significant and clearly articulated. The paper convincingly explains why inductive biases of prior work (force closure priors, palm-centric contact representations) prevent generalization to free-form interactions.

- **Dataset construction pipeline (Sec. 3.1–3.2, Fig. 2).** The O2HOI frame-pairing strategy — extracting an unoccluded object-only frame and a corresponding interaction frame from video, then reconstructing the object from the clean frame while estimating the hand from the interaction frame — is a practical and scalable solution to the core data bottleneck of hand occlusion. The mask transfer via dense matching avoids both geometric inconsistency and scaling limitations. The multi-level annotation scheme (SSCs, DSCs, 17-part hand segmentation including dorsal contact, contact maps) is well-designed and likely to be useful beyond this paper.

- **Method architecture coheres with the problem (Sec. 4.1–4.3, Fig. 4).** The three-stage design — separate contact map prediction, multi-level conditioned diffusion, then physical refinement — is structurally appropriate. The coarse-to-fine conditioning (global SSC + geometry in early diffusion blocks, local DSC + contact features in later blocks) cleanly instantiates the intuition that overall interaction type should be resolved early and fine-grained contact details later. The self-supervised cycle-consistency loss (Eq. 7) directly addresses the ambiguity of one-directional contact matching.

- **Ablation study is informative (Table 2).** The ablations cover the main design choices (contact prediction, refiner, multi-level architecture, DSC vs SSC, text encoder choice) and results are consistent with the method's claims. The observation that removing the refiner causes hand drift, yielding deceptively low penetration values, demonstrates awareness of metric pitfalls.

## Weaknesses

### Major

1. **Ground-truth quality of WildO2 lacks external validation.** The reconstruction pipeline (Sec 3.2) — LRM-based object reconstruction, MANO hand fitting, camera alignment via differentiable rendering, ray-casting + ICP refinement — has a **45% failure rate** (Fig. 3a shows only 55% reconstruction success). While the remaining 4,414 samples pass "manual inspection and refinement," the paper reports **no quantitative validation of reconstruction accuracy against independent ground truth** (e.g., multi-view capture, manual geometric annotation, or a held-out subset reconstructed by a different method). Since the same pipeline produces both the training data and the evaluation ground truth, the absolute reliability of metrics in Tables 1 and 2 is difficult to assess without external verification. This is the paper's most significant weakness.

### Minor

2. **Limited baseline comparison (Sec 5.2, Table 1).** Only two baselines are compared (ContactGen, Text2HOI), both originally designed for grasping. The paper describes their adaptation in only one sentence and does not fully clarify whether they received the same fine-grained conditioning signals (DSC-level prompts, contact maps) that TOUCH uses, or only coarser SSC-level input. However, this limitation is partially justified by the fact that no existing method was designed for free-form HOI.

3. **"In-the-wild" characterization is somewhat overstated.** WildO2 is sourced from Something-Something V2, which consists of scripted, goal-directed actions by paid actors in a controlled studio environment with a fixed overhead camera. While more diverse than lab mocap datasets (GRAB, HOI4D), it is not fully "in-the-wild" like Ego4D or EPIC-Kitchens. The terminology could be more precise.

4. **No statistical uncertainty reported.** Tables 1 and 2 present point estimates without standard deviations, confidence intervals, or significance tests. With a test set of 677 samples and known variability in HOI metrics, it is difficult to assess whether reported advantages (especially for diversity metrics where differences are small, e.g., Entropy: 2.85 vs 2.85 vs 2.93) are reliable. The perceptual score comes from 10 users with no inter-rater reliability reported.

5. **Some implementation details are missing.** (a) N_tta (number of test-time optimization iterations) is not reported (Sec 4.3); (b) the individual contributions of the two auxiliary losses (global pose loss, distance map loss) in Eq. 6 are not ablated; (c) inference runtime and computational cost of the three-stage pipeline are not discussed.

6. **Unsubstantiated quantitative claim.** The "22-25% larger average contact area for firm/tight interactions" (Sec 5.4.3) is presented without statistical support — no baseline comparison, standard deviation, or sample count.

### Trivial

None.

## Nice-to-Haves

- Validate a subset of WildO2 (50–100 samples) against independently obtained ground truth (multi-view capture or manual annotation) to establish reconstruction accuracy.
- Add standard deviations or bootstrapped confidence intervals to all key metrics.
- Include failure case analysis to complement the successful results shown.
- Report N_tta, inference runtime, and ablation of auxiliary losses.

## Removed Points

The following points from the input review are removed with brief justification:

- **Circularity risk in evaluation metrics** — The claim that pipeline errors "may correlate with what TOUCH learns to predict" is speculative without evidence from the paper. The core concern (lack of external validation) is retained in the Major weakness above.
- **Questions about object deformation/lighting changes (Sec 3.1) and camera alignment details (Sec 3.2)** — These are likely addressed in the appendix, which was stripped by the parser.
- **Claim that paper should empirically demonstrate grasp-centrism of prior methods** — This is a suggestion, not a flaw; the literature analysis claim is a reasonable motivation.
- **Missing more recent baselines (diffusion-based grasp generation 2024–2025)** — No specific methods are named, and those would still be grasp-centric, unlikely to change the comparison fundamentally.
- **All formatting/style nitpicks and missing related work concerns** — Removed per review guidelines (parser artifacts and inability to verify external sources).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Validate a subset of WildO2 against independently obtained ground truth.
2. Add standard deviations or confidence intervals to Tables 1 and 2.
3. Report N_tta, inference runtime, and ablate the auxiliary losses to improve reproducibility and transparency.
4. Include a failure analysis section.
5. Clarify what conditioning signals the baselines received (SSC only, or DSC + contact maps as well).

---

## Calibration Report

**Round 1 — Bracketing.** I searched for topically similar papers across score bands. The most relevant anchor is **HOI-Diff** (file: `ZYwLfi50GI.md`, avg score 5.25, rejected), a text-driven 3D HOI synthesis paper with modular diffusion design, whose weaknesses include missing citations (-2.44 favorability), unclear motivation (-0.52), and missing baselines. Other relevant anchors include **3D Interacting Hands Diffusion Model** (5.50, rejected) and **InterMask** (6.00, accepted). Initial bracket: [4.5, 6.5].

**Round 2 — Narrowing.** I itemized HOI-Diff (5.25) and InterMask (6.00) for close comparison. 

Against **HOI-Diff** (5.25, rejected): My paper shares the same genre (text-driven HOI generation) but tackles a harder, less-explored sub-problem (free-form vs. grasping). My paper's weaknesses have higher favorability (least favorable: -0.41 for "no statistical uncertainty") than HOI-Diff's most negative items (-2.44 for missing citations, -0.52 for unclear motivation). My paper has stronger problem motivation, a more significant dataset contribution (WildO2 from videos vs. text annotation of BEHAVE), and more thorough ablations. This places my paper above 5.25.

Against **InterMask** (6.00, accepted): InterMask achieves SOTA on established benchmarks (InterHuman, InterX) with proper comparisons and has a clear quantitative case. However, InterMask has multiple very low-favorability weaknesses (-3.75 for ill-defined innovation, -2.41 for insufficient description, -1.85 for underwhelming contribution). My paper's weaknesses are less severe but involve a more fundamental concern (dataset validation) that affects all quantitative claims. InterMask's acceptance at 6.00 sets an upper bound; my paper's weaker quantitative evaluation places it below this threshold.

**Final placement:** Score **5.5** — above HOI-Diff (5.25) due to stronger problem motivation, dataset contribution, and less severe weaknesses; below InterMask (6.00) due to the dataset validation concern and thinner baseline comparison that weaken the quantitative case.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>