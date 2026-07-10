Now I'll write the final consolidated review.

## Summary

The paper proposes UniHM, a framework for language-conditioned dexterous hand manipulation sequence generation. It combines (1) a cross-morphology VQ-VAE tokenizer that maps poses from different robotic hands into a shared codebook, (2) a VLM (Qwen3-0.6B) that generates token sequences from language and visual inputs, and (3) a physics-guided dynamic refinement optimizer for smooth and contact-consistent trajectories. The key claimed advantages are unified handling of multiple hand morphologies and generalization beyond static grasp poses to sequential manipulation.

## Strengths

- **The paper correctly identifies a genuine limitation in prior work.** Most language-guided dexterous manipulation methods produce static grasp poses, not manipulation sequences with temporal structure (Section 1, para 2–3). Targeting sequence-level generation is well-motivated and the gap is clearly articulated.

- **The cross-morphology tokenizer design is principled.** The staged training procedure — establishing a reference encoder/decoder + shared codebook, then distilling new hand encoders into the same latent space (Section 3.2, Eq. 3–5) — is sensible and directly enables the claimed unified property. The distillation loss bypassing the non-differentiable quantization step is a good engineering choice.

- **The physics refinement energy is well-formulated.** The asymmetric contact penalty (Eq. 12) with different curvature inside vs. outside the object surface, combined with generative and temporal priors (Eq. 14–15), is physically reasonable. The Gauss-Newton with Levenberg-Marquardt damping (Eq. 17–18) is an appropriate optimization strategy for this setting.

## Weaknesses

### Fatal

None.

### Major

- **The baselines do not test the claimed contribution.** UniHM compares against TM2T, MDM, FlowMDM, and MotionGPT3 — all human *motion generation* models that have no mechanism for reasoning about objects, contact, or task completion. The paper's central claim is language-conditioned dexterous hand *manipulation*, but the baselines generate body/hand poses without any object interaction. Meanwhile, the Related Work discusses SemGrasp, AffordDexGrasp, Multi-GraspLLM, DexGrasp Anything, and HOIGPT (which already does text↔HOI sequence generation), yet none appear in the experiments. Comparing against these would directly test whether UniHM advances beyond static grasps or existing sequence-level HOI methods. The paper's justification that these prior methods "predominantly target Digital Hand, low-DoF grippers, or static grasp poses" (Section 2.2) does not excuse their absence from experiments — even adapting them as best-effort baselines would be informative.

- **The primary evaluation metrics measure pose reconstruction fidelity, not manipulation success.** MPJPE, FOL, FPL, FID, and Diversity all compare generated hand poses against ground-truth human demonstrations (Tables 1–2). They measure how closely the model reproduces recorded human trajectories, not whether the generated sequence accomplishes the instructed task. A sequence that exactly matches the human trajectory could still fail if the object is in a different position, and a successful task-completing sequence could have high MPJPE if it grasps differently from the human. The real-world success rates (Table 3) partially address this, but are themselves under-reported (see below). Without task-completion metrics from simulation or properly reported real-world trials, the quantitative evidence is fundamentally misaligned with the paper's claims about *manipulation* capability.

- **Real-world experiments are critically under-reported.** Table 3 reports success rates for four task types but withholds: (a) the number of trials per condition (without which 65% vs 45% could be 13/20 vs 9/20 — a difference that may not be significant), (b) which specific dexterous hand(s) were used, (c) which objects were used for seen and unseen splits, (d) the exact instructions used, (e) what qualifies as success for each task type, and (f) how baselines were adapted beyond "Dex-Retargeting." The baseline results are notably poor (e.g., MDM achieves 0% on Pull&Push, 5% on Open&Close in the seen setting), suggesting the Dex-Retargeting pipeline may be particularly ill-suited to motion-generation outputs — making the comparison less about manipulation capability and more about which model's output survives retargeting.

### Minor

- **The training/inference distribution shift is not diagnosed.** The VLM is trained on ground-truth target trajectories and object point clouds (Section 3.3, "Training Stage"), but at inference receives noisy estimates from CLIPort and PointSAM. The paper frames this as a deliberate design choice ("decoupling spatial perception from HOI sequence generation," Section 3.3), but never evaluates how CLIPort's accuracy affects downstream manipulation success. The gap between strong simulated results (using ground-truth inputs) and more modest real-world results could partially stem from this mismatch.

- **The "first" claim is overstated.** The paper claims "the first unified, language-conditioned framework for dynamic dexterous hand manipulation beyond static grasps" (Abstract, Section 1 bullet). However, HOIGPT (Huang et al., 2025) — cited in the paper's own Related Work — already performs text↔HOI sequence generation. While UniHM's cross-morphology robot-hand targeting is novel, the "first" framing is too broad and should be qualified.

- **Key architectural details are missing.** (a) CLIPort was originally designed for tabletop pick-and-place with parallel grippers; the paper says "CLIPort-style" (Section 3.3) without specifying what was modified or retrained for dexterous hand trajectory planning. (b) How 3D spatial quantities (point clouds P_obj, trajectories T_tar) are communicated to Qwen3-0.6B — a text-only language model — is not explained; the paper says "concatenated with... and fed into a VLM" (Eq. 9) without describing the encoding mechanism.

- **Diversity scores contradict the paper's stated criterion.** The paper states "Diversity closer to the GT indicates more reasonable generation" (Section 4.2). On DexYCB seen (Table 1), GT Diversity is 125.53, MotionGPT3 achieves 72.51, and UniHM achieves 39.62 — making MotionGPT3 substantially closer to GT. The same pattern holds on the unseen split. The paper does not discuss this.

- **The GPT-4o auto-annotation pipeline is not validated.** Section 3.1 describes generating language annotations by providing keyframes to GPT-4o, but no human evaluation, quality analysis, or discussion of failure cases (e.g., ambiguous instructions, hallucinations) is provided. For a language-conditioned system, the quality of text annotations is a primary input that should be characterized.

- **The distillation loss relies on a non-bijective retargeting mapping.** The distillation objective (Eq. 3) uses retargeting to produce "corresponding hand sequences" across morphologies, but retargeting from MANO to robot hands is not a bijection — multiple MANO poses can map to the same robot hand configuration. This injects systematic noise into the distillation target that is not discussed.

### Trivial

None.

## Nice-to-Haves

- Compare against at least HOIGPT and a static-grasp method adapted to produce per-frame sequences; if adaptation is impossible, document why as a contribution.
- Add simulation-based task-completion metrics (e.g., in Isaac Gym or MuJoCo) measuring whether objects are successfully grasped, lifted, and moved per instruction.
- Report real-world trials with per-condition sample sizes, confidence intervals, specific objects/hands, and explicit success criteria per task type.
- Diagnose the training/inference gap by fine-tuning the VLM on CLIPort-produced trajectories and reporting the performance change.
- Qualify or remove the "first" claim given HOIGPT's prior work on sequence-level HOI generation.

## Removed Points

These points are flagged to be removed, treat them with caution:
1. Missing codebook size K and d_z values — trivial implementation detail, removed per hard rules.
2. Claim that "teleoperation" framing overstates data requirements — the paper accurately claims it eliminates *teleoperation* data specifically; the data used (DexYCB, OakInk) are human-video datasets, not teleoperation data. The framing is defensible on its own terms.
3. Various formatting/style nitpicks removed per hard rules (parser artifacts, not author errors).

## Novel Insights

The key insight from the review process is that the paper suffers from a fundamental evaluation-claim misalignment: it surveys dexterous manipulation methods in Related Work but benchmarks only against unrelated human motion generators, and uses pose-reconstruction metrics rather than task-completion measures. This gap is more damaging than any individual design flaw because it prevents the reader from assessing whether the method actually achieves its stated goal of "dexterous hand manipulation." The cross-morphology tokenizer and physics refinement components are genuinely well-designed, but the empirical case for the overall system is significantly weaker than the contributions section suggests.

## Suggestions

1. Replace or supplement the Tables 1–2 comparisons with benchmarks against HOIGPT (sequence-level HOI) and at least one static-grasp method adapted to produce per-frame sequences. If adaptation is infeasible, explicitly document the challenges — this is itself a meaningful finding.
2. Add simulation-based task-completion metrics (grasp success, lift stability, task completion rate) that directly measure manipulation capability rather than pose similarity.
3. Report real-world experiments with full details: per-condition n, confidence intervals, specific hardware, object lists, success criteria definitions.
4. Diagnose the training/inference distribution shift by either fine-tuning the VLM on CLIPort outputs or evaluating the CLIPort module's error characteristics.
5. Clarify how 3D spatial data (point clouds, SE(3) trajectories) is encoded for a text-only VLM — this is a non-trivial architectural choice that affects the system's generality.

## Score and Decision

**MY FINAL SCORE:** <score>4.5</score>
**MY FINAL DECISION:** <decision>Reject</decision>

### Calibration

| Anchor Paper | Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|---|
| HandsOnVLM | AJQuTFd9es.md | 6.33 | 1 | Yes | HandsOnVLM has a cleaner evaluation (VLM for hand trajectory prediction) with well-reported benchmarks, but a narrower contribution (trajectory curves, not manipulation). My paper has stronger technical novelty but worse evaluation alignment. |
| Early Fusion VLA | KBSHR4h8XV.md | 3.33 | 1 | Yes | Strong reject anchor. EF-VLA's weaknesses are more severe (unfair comparisons, minor technical contribution). My paper is clearly stronger. |
| HAMSTER | h7aQxzKbq6.md | 6.00 | 1 | Yes | HAMSTER has comparable evaluation quality (hierarchical VLA for manipulation, real-world + sim). Its most negative weakness items (lacks comparison: -2.84, insufficient investigation: -1.71) are comparable in severity to my paper's W1 (-2.57). However, HAMSTER's core evaluation is better aligned with its claims. |
| CrayonRobo | Aqfwhna1D7.md | 5.20 | 2 | Yes | CrayonRobo has a similar evaluation gap (limited trajectory specification, practical concerns). Its weaknesses are less severe on the negative side (most negative: -2.28 for writing issues) but its strengths include solid experimental setup. My paper has more damaging evaluation weaknesses. |

**Calibration reasoning:** My paper's most negatively-rated weakness (baseline mismatch, favorability=-2.57) exceeds the most negative items of comparable anchors (HAMSTER: -2.84, CrayonRobo: -2.28). The evaluation-claim misalignment is structural: the paper claims manipulation capability but benchmarks against motion generators using pose-similarity metrics. HandsOnVLM at 6.33 was rejected despite a better-aligned evaluation, and my paper's evaluation issues are more severe. CrayonRobo at 5.20 was rejected with less damaging weaknesses. I place the paper at 4.5, solidly in borderline-reject territory: genuine technical contributions that deserve to be salvaged with major evaluation revisions, but insufficient evidence in the current form to support the paper's central claims.