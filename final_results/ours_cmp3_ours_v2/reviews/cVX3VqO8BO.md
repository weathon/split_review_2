Now I have enough information to produce the final calibrated review. Let me write it up.

## Summary
UniHM proposes a framework for language-guided sequential dexterous hand manipulation. It uses a morphology-agnostic VQ-VAE codebook to unify multiple hand types, a VLM (Qwen3-0.6B) with a decoupled CLIPort perception module for instruction-conditioned trajectory generation, and a physics-guided dynamic refinement post-processing step to ensure physical feasibility. The system is trained on human HOI datasets (DexYCB, OakInk) and evaluated on seen/unseen splits plus real-world robot experiments.

## Strengths
1. **Sequential manipulation from language targets an important gap.** Prior language-guided dexterous methods (SemGrasp, AffordDexGrasp, DexGYS) generate static grasps. UniHM targets multi-step sequences — "Pick&Place the bottle," "Pull the drawer" — which is a genuinely harder and more useful setting. The paper correctly identifies this gap in Sections 1 and 2.

2. **Morphology-agnostic codebook is a practical contribution.** The idea of training a shared VQ-VAE codebook with per-hand encoder/decoder pairs (Section 3.2), then aligning new hands via distillation (Eq. 3), is well-motivated and cleanly described. Cross-hand transfer via Eq. 6 is a natural and useful property that follows from the design.

3. **Decoupled perception-generation architecture is sensible.** Using CLIPort for scene-to-trajectory inference and keeping the VLM focused on hand-object interaction (Section 3.3) is a pragmatic design choice. The paper motivates this in terms of data efficiency and robustness to distribution shift, noting that only CLIPort needs adaptation when the scene changes.

## Weaknesses

### Fatal
None.

### Major
1. **The most directly comparable prior work (HOIGPT) is missing from the experimental comparison, and the state-of-the-art claim is unsubstantiated.** The paper compares against TM2T, MDM, FlowMDM, and MotionGPT3 — human full-body motion generation methods that were not designed for hand manipulation. Meanwhile, HOIGPT (Huang et al., 2025), discussed in Section 2.2, "extends token-based generation to long 3D hand-object interaction, learning a bidirectional mapping between text and HOI sequences" — this is directly comparable sequential hand-object interaction from language. The paper claims state-of-the-art performance (Sections 1, 4.3) but the reader cannot determine whether UniHM improves over actual dexterous manipulation methods or merely over general motion models post-processed for this task. The paper's rationale that dexterous methods produce only static grasps (Section 2.1) applies to SemGrasp, AffordDexGrasp, and DexGrasp Anything, but not to HOIGPT, which is explicitly sequential.

2. **Real-world evaluation (Table 3) conflates method quality with post-processing.** The baselines in Table 3 are listed as "MDM+Dex-Retargeting" and "MotionGPT3+Dex-Retargeting" without mention of physics-guided refinement being applied to their outputs. Meanwhile, UniHM benefits from the full pipeline including refinement. The ablation (Table 4, DexYCB Seen) shows that removing physics refinement degrades MPJPE from 61.40 to 65.78 (~7%) — a non-trivial contribution. Without applying the same refinement to baseline outputs, the reported gap in real-world success (e.g., 65% vs 20–30% for Seen Grab) could be substantially driven by the refinement module rather than the generation model itself. The paper's statement about applying refinement for fair comparison (Section 4.3, "we post-process their outputs with our physics-guided refinement to ensure a fair comparison") explicitly applies only to Tables 1–2, not to Table 3.

3. **Physical feasibility — a central claim — is not directly measured in the main quantitative evaluation.** The paper claims "physically feasible manipulation" throughout (Abstract, Sections 1, 3, 5) as a core contribution. However, the reported metrics (MPJPE, FOL, FPL, FID, Diversity) measure pose accuracy relative to human ground-truth, not physical validity (penetration, contact stability, joint-limit violation). The paper states it will "validate feasibility in simulation" (Section 4, line 208) but provides no simulation results or quantitative physical metrics in any table. The only direct feasibility evidence is real-world success rate (Table 3), which has the fairness issue noted above. This disconnect between the claimed contribution and the measured evidence weakens the paper's core thesis.

### Minor
4. **The CLIPort-to-SE3 trajectory interface is underspecified.** The paper states that CLIPort infers a target execution trajectory $\mathcal{T}_{\text{tar}} \in \text{SE}(3)^K$ (Eq. 7). However, the original CLIPort (Shridhar et al., 2022) outputs pixel-wise affordance maps, not SE(3) trajectories. How this bridge is built — whether via additional heads, post-processing, or a learned mapping — is not explained. This is a non-trivial architectural detail that directly affects reproducibility.

5. **Overclaimed novelty of "learning from video."** Contribution bullet 4 ("Generalization without Teleoperation") states the framework "eliminates the dependency on expensive teleoperation data by learning dexterous manipulation skills from human videos." Training on human HOI datasets (DexYCB, OakInk) is already standard practice in this area (e.g., DexMV, HOIGPT), so this framing overstates the novelty. The contribution is better described as compatibility with existing HOI datasets rather than a fundamentally new training paradigm.

### Trivial
None.

## Nice-to-Haves
- Apply the same physics-guided refinement to baseline outputs in the real-world evaluation (Table 3) and report whether the gap narrows — this would cleanly separate method quality from post-processing.
- Report at least one simulation-based physical metric (penetration depth, contact stability, simulation success rate) to directly support the physical feasibility claim.
- Include HOIGPT as a baseline in the main quantitative comparison to substantiate the state-of-the-art claim.
- Add a dedicated implementation details section covering the key architectural parameters (codebook size, latent dimension, masking schedule, training hyperparameters).

## Removed Points
These points were identified in the input reviews but are removed or demoted per the filtering instructions:

- **Corrupted standard deviations in Table 1:** The ± values in Table 1 (e.g., "85.33 ± 341") appear to have a decimal point dropped during parsing (likely "85.33 ± 3.41" in the original). Table 2 and Table 4 have correctly formatted standard deviations. **Removed** — this is a parser formatting artifact, not an author error (Hard Rule).
- **Missing static-grasp dexterous baselines (SemGrasp, AffordDexGrasp, DexGrasp Anything, Multi-GraspLLM):** The paper explicitly scopes itself as targeting sequential manipulation (Section 2.1: "they remain pose-centric and typically generate **static poses** rather than sequence-level hand manipulation"). Comparing against static-grasp methods would not be informative for the paper's specific sequential claim. **Removed** — scope creep (Soft Rule: WEAKEN criticisms about problems outside the paper's stated scope).
- **Undisclosed hyperparameters as a reproducibility issue:** Codebook size K, latent dimension d_z, training hyperparameters are not reported. While not trivial, many of these details would naturally go in an appendix (which the parser strips) and are standard for conference papers. **Demoted** — Minor rather than a major methodological gap, with only the CLIPort-SE3 architecture gap retained as a core concern.

## Novel Insights
The harsh critic's analysis reveals a pattern across multiple weaknesses: the paper's evaluation regime systematically conflates what the method contributes intrinsically with what comes from the evaluation scaffolding. Specifically: (1) baselines are chosen from a different problem domain (human body motion), making the "SOTA" claim unverifiable against actual dexterous manipulation methods; (2) the physics refinement — a key component — is applied unevenly across comparisons (applied to baselines in Tables 1–2 but apparently not in Table 3); and (3) the metrics measure pose accuracy rather than the paper's claimed physical feasibility. Together these issues mean the reader cannot cleanly attribute the reported gains to the core technical innovations (codebook, decoupled architecture). This is not a fatal problem — the technical design has independent merit — but it means the empirical evidence as presented substantially overstates the conclusions it supports.

## Suggestions
1. Replace or supplement the human motion baselines with HOIGPT, which is a sequential hand-object interaction method from text. If the HOI sequences produced by HOIGPT are on digital hands rather than robot hands, discuss the adaptation required and include it.
2. Re-run the real-world evaluation with the same physics-guided refinement applied to all baseline outputs, and report both with and without refinement for all methods to enable clean attribution.
3. Add a table of simulation-based physical metrics (e.g., penetration depth per frame, percentage of frames with stable contact, task success rate in simulation) to directly measure the physical feasibility claim.
4. Clarify how CLIPort is adapted to produce SE(3) trajectories — this is a non-trivial architectural detail.

## Score and Decision
**Round 1 bracket:** Based on calibration against similar VLA/manipulation papers, the initial plausible range is [4.0, 5.5].

**Calibration anchors consulted:**
- `KBSHR4h8XV` (Early Fusion VLA, avg 3.33, Reject): Narrower contribution (CLIP modification), cleaner evaluation, but lower novelty. UniHM has stronger novelty but weaker evaluation fairness. → Places UniHM above 3.33.
- `Afjf6izLvJ` (Grounding Robot Policies, avg 5.33, Reject): Agent-based framework, good evaluation but limited task scope. UniHM has comparable technical ambition with a less convincing evaluation. → Places UniHM slightly below 5.33.
- `h7aQxzKbq6` (HAMSTER, avg 6.00, Accept): Hierarchical VLA with fair baselines and solid evaluation. UniHM has stronger novelty but substantially weaker evaluation rigor. → Places UniHM clearly below 6.00.
- `29p13QihRM` (Language-Guided World Models, avg 4.00, Reject): Similar overall quality level, comparable evaluation concerns.

The paper has a genuine technical contribution (morphology-agnostic codebook, decoupled architecture) and targets an important problem, but the empirical evaluation has significant gaps: the most relevant prior work (HOIGPT) is absent from comparison, the real-world comparison treats baselines unevenly, and the core claim of physical feasibility is not directly measured by the reported metrics. These are fixable issues but in the current form, the evidence does not meet the bar for acceptance.

**Final calibrated score:** This paper is a borderline reject — the technical ideas are solid and the problem is important, but the evaluation needs substantial revision before the claims are adequately supported.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>