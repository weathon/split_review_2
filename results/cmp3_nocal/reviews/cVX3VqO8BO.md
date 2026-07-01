Now let me produce the final consolidated review.

## Summary

UniHM proposes a three-component framework for language-conditioned dexterous hand manipulation: (1) a unified VQ-VAE tokenizer with distillation-based encoder alignment to share a codebook across heterogeneous hand morphologies, (2) a VLM (Qwen3-0.6B) that generates token sequences conditioned on language, visual perception, and target trajectories, and (3) a physics-guided Gauss–Newton refinement that enforces contact, temporal smoothness, and generative priors. The model is trained solely on HOI video data without teleoperation.

## Strengths

1. **Well-motivated cross-morphology tokenizer with principled alignment.** The shared VQ-VAE codebook with distillation-based encoder alignment (Section 3.2, Eq. 3–6) cleanly addresses the genuine problem that heterogeneous dexterous hand kinematics (Shadow, Allegro, SVH, Leap, Panda) cannot share a pose space. The distillation bypasses the non-differentiability of VQ during cross-morphology alignment, and the encode–quantize–decode formulation for cross-hand translation (Eq. 6) is a well-designed property.

2. **Clean formulation of physics-guided refinement.** The energy in Section 3.4 (Eq. 11–16) combining contact (asymmetric signed-distance penalty), generative (deviation from VLM output), and temporal (velocity/acceleration) priors is concise and properly justified. The Gauss–Newton with Levenberg–Marquardt damping (Eq. 17–18) is appropriate for the frame-by-frame optimization setting.

3. **Practical decoupled architecture for data efficiency.** Separating scene perception (CLIPort) from HOI token generation (Qwen3-0.6B VLM), as described in Section 3.3, is sensible. The insight that only the perception module needs adaptation to distribution shifts while the HOI generator stays fixed is practically useful for data efficiency.

## Weaknesses

### Fatal
None.

### Major

1. **Baseline comparison setup is underspecified; the reported performance gaps are uninterpretable.** The paper compares against TM2T, MDM, FlowMDM, and MotionGPT3 (Tables 1, 2) — all full-body human motion generation models — on hand-only HOI datasets (DexYCB, OakInk). The paper states only that "we post-process their outputs with our physics-guided refinement to ensure a fair comparison" (Section 4.3, line 257), which addresses post-processing, not the fundamental output-space mismatch. Several critical details are absent: How were these full-body motion models adapted to produce hand-only sequences? Were they retrained from scratch, finetuned, or used as-is with body joints discarded? What data and language annotations were they conditioned on? DexYCB and OakInk do not natively provide free-form language instructions — the paper uses GPT-4o to annotate them (Section 3.1). Were the baselines trained on the same GPT-annotated instructions? Without this information, the large reported performance gaps (e.g., Ours MPJPE 61.40 vs. MotionGPT3 74.80 on DexYCB seen) cannot be attributed to genuine superiority over alternative task setups. This undermines the central "state-of-the-art" claim.

2. **The cross-morphology codebook, listed as a core contribution, receives no direct validation.** The unified tokenizer is the second claimed contribution ("Morphology-Agnostic Codebook"), yet the main quantitative evaluation (Tables 1, 2) is conducted entirely on DexYCB and OakInk — both containing only human hand (MANO) poses. There is no experiment demonstrating: (a) token reconstruction accuracy across different hand morphologies (Shadow, Allegro, SVH, Leap, Panda), (b) whether the unified codebook outperforms separate per-morphology codebooks of the same total size, or (c) whether cross-hand pose translation (Eq. 6) produces physically valid results. The real-world experiments (Table 3) do not specify which hand was used and do not compare across morphologies. A core claimed contribution is left unmeasured.

3. **Real-world experiments are critically underspecified.** Table 3 reports success rates (Grab, Pick&Place, Pull&Push, Open&Close) without answering: which dexterous hand hardware was used? How many trials per condition (a single failed trial changes results substantially in a small-\(n\) setup)? What environment and objects were used? How were the baselines (MDM+Dex-Retargeting, MotionGPT3+Dex-Retargeting) actually deployed — MDM generates full-body motion; the pipeline from full-body outputs to robot hand joint commands is not explained. Without this information, the real-world results are anecdotal.

4. **HOIGPT, the most closely related prior work, is discussed but not compared against.** HOIGPT (Huang et al., 2025) is cited in the related work (Section 2.2) and described as extending "token-based generation to long 3D hand-object interaction, learning a bidirectional mapping between text and HOI sequences" — i.e., it already does text-conditioned sequential hand-object interaction. Yet it is absent from the experimental comparison. Including HOIGPT as a baseline would substantially strengthen the evaluation and clarify how UniHM's contributions (cross-morphology codebook, physics refinement, video-supervised training) advance beyond the closest existing method.

### Minor

5. **"First" claim is overstated.** The abstract and contributions (Section 1, line 37) claim "the first unified, language-conditioned framework for dynamic dexterous hand manipulation beyond static grasps." Given HOIGPT already generates text-conditioned HOI sequences (as acknowledged in Section 2.2), this claim is misleading without qualifying what specific aspect is first (e.g., cross-morphology unification, physics refinement integration). The paper should acknowledge HOIGPT's capabilities and state UniHM's specific novelties relative to it.

6. **VLM architecture description lacks key fusion details.** Section 3.3 says the initial hand pose, target trajectory \(\mathcal{T}_{\text{tar}}\), object point cloud \(\mathcal{P}_{\text{obj}}\), and text tokens are "concatenated" and fed into the VLM (Eq. 9), but does not specify: how many tokens the VLM outputs per frame, whether the VLM is trained end-to-end with the tokenizer or separately, or the architecture of the "MLP-based trajectory encoder." The connectivity between modalities is not clearly shown.

7. **No analysis of GPT-4o annotation quality.** The auto-annotation process (Section 3.1) is described in one sentence: GPT-4o receives keyframes and returns five instructions. Since the entire VLM training depends on these annotations, some validation (human evaluation, sample outputs, or consistency checks) is needed.

8. **The unusually tight standard deviations in Table 1 warrant explanation.** Ours has substantially smaller standard deviations than all baselines across most metrics (e.g., DexYCB seen FPL: 12.15 ± 0.24 vs. MotionGPT3 19.32 ± 0.77; a ~3× ratio in standard deviation). This pattern is consistent and merits explanation — does it reflect fewer evaluation samples, different random seeds, or a genuine property of the method (e.g., physics refinement acting as a deterministic post-processor)?

9. **The full method produces lower diversity than the ablated "w/o Masked Training" variant.** In Table 4, the full method achieves Diversity 39.62 vs. "w/o Masked Training" 73.09 (GT = 125.53). The ablated version is actually closer to GT diversity. This should be discussed.

### Trivial
None.

## Nice-to-Haves

- Validate the GPT-4o annotations with human evaluation or sample outputs.
- Add an experiment showing cross-morphology reconstruction accuracy (encode from MANO, decode to Shadow/Allegro/Panda, report per-joint error).
- Include an ablation comparing the unified codebook against per-morphology codebooks.
- Report compute budget and training time.
- Provide failure case analysis for both the VLM generation and the physics refinement.

## Removed Points

- **"~8x coefficient of variation" claim:** The harsh critic stated "~8x in the coefficient of variation" for the standard deviations. The actual ratio is ~2–3× (std, not CV). The observation about tighter stds is valid and retained as Minor #8, but the 8× figure is removed as numerically inaccurate.
- **Criticism about "missing appendix, missing proofs" etc.:** Not present in the input review, but flagged in case — the paper's appendix content cannot be verified due to parsing; do not penalize for absent appendix content.
- **Strengths about "important problem," "interesting question":** Not present in the input; the strengths listed are concrete and specific, so none were removed.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's review surfaces a recurring issue in this area: papers that propose modular frameworks often validate individual modules (tokenizer, refinement) in isolation but then evaluate the full system against baselines adapted in underspecified ways, making the headline comparisons difficult to interpret. This pattern is worth noting but does not constitute a novel insight about this specific paper.

## Suggestions

1. **Fix the baseline comparison.** Either (a) compare against HOIGPT and other methods that natively handle hand-object sequences, or (b) provide a clear, detailed explanation of how full-body models were adapted (retraining procedure, output space modification, data and conditioning used). Without this, the reported SOTA numbers cannot be trusted.

2. **Validate the cross-morphology codebook directly.** Add an experiment showing per-joint reconstruction error across hand morphologies, and an ablation comparing unified vs. per-morphology codebooks. This is the distinguishing technical contribution; it needs evidence.

3. **Flesh out the real-world evaluation.** Specify the hardware platform, number of trials per condition, randomization procedure, and a clear pipeline description for baseline deployment (full-body → hand → robot).

4. **Qualify the "first" claim.** Acknowledge HOIGPT's capabilities and state the specific novelties that differentiate UniHM.

## Score and Decision

The paper proposes a well-motivated framework with several technically sound components (cross-morphology tokenizer, physics refinement, decoupled architecture). However, the evaluation has substantial gaps: the main quantitative comparison is against baselines adapted in an unspecified manner, the core claimed contribution (cross-morphology codebook) is not directly validated, the real-world experiments lack critical details, and the most relevant prior work (HOIGPT) is discussed but not compared against. These issues collectively prevent the paper from convincingly establishing its claimed state-of-the-art results. The contributions are real and the direction is valuable, but the evidence as presented does not support the strength of the claims. The paper could become acceptable with major revisions to the evaluation.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>