Now I have a solid calibration picture. Let me write the final review.

My bracket assessment: Based on anchors, UniHM is stronger than EF-VLA (3.33) which had severe baseline fairness issues, comparable to Cross-Embodiment Grasping (5.00) which was accepted despite baseline concerns, and weaker than HandsOnVLM (6.33) whose evaluation was cleaner. I place it at **5.0** — a true borderline paper with real technical merit but evaluation that doesn't fully support the claims.

Let me now produce the final review.

## Summary

UniHM proposes a framework for generating sequential dexterous hand manipulation trajectories conditioned on open-vocabulary language instructions. The system couples (1) a morphology-agnostic VQ-VAE codebook that maps heterogeneous hand types (MANO, Shadow, Allegro, SVH, Leap, Panda) into a shared discrete space, (2) a VLM (Qwen3-0.6B) trained with a progressive masking curriculum for instruction-conditioned token generation, and (3) a physics-guided Gauss-Newton refinement with contact, generative, and temporal priors. Evaluations are conducted on DexYCB and OakInk datasets (retargeted to robot hands) and in real-world experiments.

## Strengths

- **Morphology-agnostic codebook with cross-morphology distillation (Sec. 3.2).** The shared VQ-VAE codebook with the staged training strategy — first establishing a reference encoder/decoder pair, then aligning new encoders via latent-space distillation (Eq. 3) — is a technically clean design. The ability to encode a pose from one hand and decode it to another (Eq. 6) is a concrete capability that goes beyond prior dexterous-grasp methods.

- **Physics-guided refinement is carefully formulated (Sec. 3.4).** The per-frame Gauss-Newton optimization with the asymmetric smooth-penalty contact energy (Eq. 12), generative prior (Eq. 14), temporal regularization (Eq. 15), and Levenberg-Marquardt damping (Eq. 17) forms a coherent energy-based approach. The mathematical formulation is rigorous and well-specified.

- **Clean ablation study (Table 4).** The controlled ablations (w/o Depth Input, w/o Masked Training, w/o Physical Refinement) systematically isolate each component's contribution, with clear degradations that validate the design choices.

## Weaknesses

### Fatal
None.

### Major

- **Baselines are not appropriate for substantiating SOTA claims.** The four quantitative baselines — TM2T, MDM, FlowMDM, MotionGPT3 — are human **full-body motion generation** methods. The paper states their outputs are "post-process[ed] with our physics-guided refinement" (line 257) but never explains what adaptation was needed to make these full-body models produce hand-manipulation outputs (hand pose has ~20+ DoF; full-body skeletons are ~60+ DoF). Meanwhile, the paper's own related work (Sec. 2.2) surveys directly comparable dexterous-hand methods — SemGrasp, AffordDexGrasp, HOIGPT, DexGrasp Anything, Multi-GraspLLM — yet none appear in the quantitative comparison. The claim that UniHM achieves "state-of-the-art results" (line 258) cannot be properly evaluated without comparisons to methods designed for the same task domain. This is the single most significant weakness: the paper's central empirical claim is not supported by the presented comparisons.

- **Cross-morphology transfer is claimed but not quantitatively evaluated.** The unified codebook and cross-morphology distillation are presented as a core contribution (Contributions point 2, lines 37–38), and the paper states it "enables direct token reuse and transfer across robotic and anthropomorphic hands." Yet no experiment directly measures cross-morphology transfer (e.g., train on one hand type → evaluate on another; compare token reuse accuracy across hand types; measure the impact of the distillation loss). The only evidence is that the real-world system uses "a dexterous hand" (unspecified which). For a claimed contribution of this prominence, a dedicated evaluation is needed.

- **Real-world experiments lack sufficient procedural detail for interpretation.** Table 3 reports success rates (20–65% Grab, etc.) for four task categories but does not specify: which of the five dexterous hands was used, number of trials per condition, task-specific success criteria, object sets, or whether evaluation was blinded. The baselines "MDM+Dex-Retargeting" and "MotionGPT3+Dex-Retargeting" are post-processed with the paper's own physics-guided refinement, which does not isolate the contribution of the VLM + tokenizer from the refinement module. Without these details, the reported success rates cannot be properly assessed for reliability or compared across methods.

### Minor

- **"First framework" claim is imprecise.** The paper describes HOIGPT (line 52) as "extend[ing] token-based generation to long 3D hand-object interaction, learning a bidirectional mapping between text and HOI sequences." While UniHM's distinguishing contributions lie in handling multiple robotic hand morphologies and physics-guided refinement, claiming to be "the first unified, language-conditioned framework for dynamic dexterous hand manipulation beyond static grasps" (line 37) overstates originality. The claim should be scoped more precisely (e.g., to multi-morphology robotic hand manipulation with physics feasibility).

- **Diversity metric interpretation is not discussed.** On DexYCB (Table 1), GT diversity is 125.53; UniHM produces 39.62 (seen) while MotionGPT3 produces 72.51 (closer to GT). By the paper's own standard ("Diversity closer to the ground truth indicates a more reasonable generation," line 253), the baselines produce more diverse outputs. On OakInk the situation reverses (UniHM at 165.47 is closer to GT's 147.40 than MotionGPT3 at 247.10). This cross-dataset inconsistency merits discussion.

- **Key model specifications omitted.** Codebook size K, latent dimension d_z, number of VQ-VAE training steps, GPU training time, and the progressive masking schedule p_t are not reported, limiting reproducibility.

- **"Learning from video" framing could be clearer.** The contributions claim the framework "learn[s] dexterous manipulation skills from human videos" (line 40) and "eliminates the dependency on expensive teleoperation data." The training data (DexYCB, OakInk) are multi-view, calibrated lab datasets with precise 3D annotations — technically "human videos" but not unlabeled in-the-wild footage. The phrasing may create an impression of data efficiency that the paper does not fully substantiate.

- **Simulation-based physics metrics not reported.** The paper mentions validating "feasibility in simulation" (line 208) but reports no physics metrics (penetration depth, contact forces, simulation success rate), leaving the "physical feasibility" claim qualitatively supported.

### Trivial
None.

## Nice-to-Haves

- An explicit cross-morphology experiment (train on one hand, decode to another, report MPJPE/success rate) would directly validate Contribution 2.
- Reporting physics-based simulation metrics (penetration depth per frame, contact force distribution, Isaac Gym or MuJoCo success rate) would strengthen the physical feasibility claims.
- Analyzing CLIPort's trajectory prediction accuracy separately would reveal how robust the system is to perception errors without conflating perception and generation.
- Replacing or supplementing the baselines with dexterous-hand-specific methods would make the SOTA claim credible.

## Removed Points

These points are flagged to be removed; treat them with caution:

- *Critic's claim that the paper "marks [diversity] as an advantage" on DexYCB.* The paper merely describes the metric's meaning (line 253) and the table correctly bolds MotionGPT3's diversity as better on DexYCB. The paper does not falsely claim diversity superiority.
- *Critic's claim that MPJPE/FOL/FPL are "uninterpretable" due to retargeting error.* The same retargeting pipeline applies to all compared methods, so relative comparisons remain valid even if absolute numbers embed some retargeting noise.
- *Critic's claim that "learning from video" is invalid because data is lab-captured.* DexYCB and OakInk are indeed human video datasets of hand-object interaction. The claim about avoiding teleoperation data is factually accurate, even if the framing could be more precise.
- *Critic's generic strengths* ("problem is well-motivated and timely") removed as not specific to the paper's content.
- *Critic's claim about "structural" and "not fixable" baseline issue.* While the baseline concern is Major, it is addressable (by adding proper comparisons and explaining adaptations), not a fatal structural flaw.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's main observation — that the baseline comparison uses methods from a different domain while citing but not comparing against directly relevant dexterous-hand methods — is a standard but valid point about evaluation design, not a novel insight.

## Suggestions

1. **Address the baseline problem.** Either explain how full-body motion models were adapted for hand manipulation and justify why this adaptation is fair, or (ideally) replace/supplement with comparisons against dexterous-hand-specific methods (HOIGPT, SemGrasp, AffordDexGrasp, Multi-GraspLLM) adapted to the same evaluation protocol.
2. **Add a cross-morphology transfer experiment.** Train the VLM on one hand type, decode to another, and report metrics. This directly validates a central claimed contribution.
3. **Provide full procedural details for real-world experiments:** specify the hand model, number of trials per condition, task-specific success criteria, and whether evaluation was blinded.
4. **Scope claims precisely.** Replace "first framework for dynamic dexterous hand manipulation" with a claim scoped to multi-morphology robotic hand manipulation with physics-guided refinement.
5. **Report key specifications:** codebook size K, latent dimension d_z, training hyperparameters, and masking schedule.

## Score and Decision

**Score: 5.0**  
**Decision: Reject**

The paper presents technically sound ideas — the morphology-agnostic codebook and physics-guided refinement are well-formulated contributions. The ablation study cleanly validates each component. However, the experimental evaluation does not adequately support the core claims. The baselines are from a different domain (full-body motion) with no documented adaptation, while directly comparable dexterous-hand methods are cited but not compared against. A central claimed contribution (cross-morphology transfer) is not quantitatively evaluated. The real-world experiments lack sufficient procedural detail. A substantially revised evaluation with appropriate baselines and proper validation of the cross-morphology claim could make this a strong paper, but in its current form the evidence is insufficient to accept the SOTA claims.

### Calibration Anchors

**Retrieved anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| EF-VLA (KBSHR4h8XV) | 3.33 | R1 | Weaker; similar baseline fairness issues but less technical novelty |
| Cross-Embodiment Grasping (twIPSx9qHn) | 5.00 | R1 | Comparable; similar domain (dexterous, cross-embodiment), accepted despite baseline concerns |
| CrayonRobo (Aqfwhna1D7) | 5.20 | R1 | Comparable; similar evaluation quality, rejected |
| HandsOnVLM (AJQuTFd9es) | 6.33 | R1 | Stronger; cleaner evaluation despite also being rejected |
| Grounding Robot Policies (Afjf6izLvJ) | 5.33 | R2 | Comparable; similar evaluation concerns |
| HOI-Diff (ZYwLfi50GI) | 5.25 | R2 | Comparable; similar domain (text-driven HOI) |
| DTP (VaoeAi5CW8) | 4.25 | R2 | Weaker; less technical novelty |

**Round 1 bracket:** 4.0 – 6.0  
**Narrowing:** Compared against Cross-Embodiment Grasping (5.00, accepted) and CrayonRobo (5.20, rejected), UniHM sits in the same quality band but has more severe baseline concerns than Cross-Embodiment while similar technical depth to CrayonRobo. Final score **5.0** reflects a borderline paper with real technical merit but evaluation insufficient to support the claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>