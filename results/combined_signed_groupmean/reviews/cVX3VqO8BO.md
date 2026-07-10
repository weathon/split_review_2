Now I have all the information I need. Let me compile the final review with calibrated score.

**Calibration Summary:**

**Round 1 — Bracketing:** Retrieved anchors across all bands. Most relevant:
- Cross-Embodiment Dexterous Grasping (5.00, Accept): Similar topic (dexterous hands), similar weakness profile (baseline concerns, limited real-world detail), but its weaknesses had comparable impact scores (-9.00 to -9.99) and it still scored 5.00
- DexTrack (6.25, Accept): Stronger experiments, major presentation weaknesses
- HandsOnVLM (6.33, Reject): VLM-based hand interaction, but different task (prediction vs. generation)
- HAMSTER (6.00, Accept): Hierarchical VLA, similar baseline criticism (-9.97)
- CrayonRobo (5.20, Reject): Robot manipulation, similar weakness severity

**My draft's impact scores:** Physics refinement (+9.39), ablation (+7.41), tokenizer (+5.93) push UP; baseline selection (-9.64), diversity contradiction (-9.92), missing cross-morphology ablation (-9.98), missing simulation (-9.90) pull DOWN.

**Round 1 Bracket:** 4.0–6.0 (closest anchors score 4.25–6.33)

**Round 2 — Narrowing:** Compared against Cross-Embodiment (5.00) — similar weakness magnitudes: -9.00 to -9.99 for both papers' major concerns. Cross-Embodiment's strength magnitudes (+6.85, +4.51, +3.23) are lower than UniHM's top strengths (+9.39, +7.41, +5.93), but UniHM has more distinct high-magnitude weaknesses. The papers are comparable; placing UniHM at 5.0.

**Final Score:** 5.0 — The paper has a genuine technical contribution (cross-morphology tokenizer + VLM + physics refinement for dynamic sequences) and well-executed components, but the evaluation has gaps (baseline selection, unaddressed diversity issue on DexYCB, missing ablation of the core tokenizer claim, and missing simulation metrics) that prevent stronger support for the headline claims.

---

## Summary

This paper introduces UniHM, a framework for generating dynamic dexterous hand manipulation sequences from open-vocabulary language instructions. The approach combines a shared VQ-VAE codebook that maps heterogeneous hand morphologies into a common discrete action space, a vision-language model (Qwen3-0.6B) that produces manipulation tokens conditioned on language, object point clouds, and target trajectories, and a physics-guided dynamic refinement module that optimizes sequences for physical feasibility. The system is trained on human-object interaction video and evaluated on DexYCB and OakInk datasets with real-world robot experiments.

## Strengths

- **Cross-morphology tokenizer design.** The shared VQ-VAE codebook with per-hand encoders/decoders (Eqs. 1–2) and distillation-based alignment (Eq. 3) provides a clean, principled way to handle heterogeneous hand kinematics. The natural pose translation property (Eq. 6) is a practical advantage. (Section 3.2)

- **Physics-guided refinement formulation.** The energy-based optimization (Eqs. 11–16) integrating contact, generative, and temporal priors in a Gauss-Newton framework with Levenberg-Marquardt damping is technically sound, well-specified, and its contribution is validated through ablation (Table 4). (Section 3.4)

- **Ablation study validates individual components.** Table 4 provides controlled experiments showing the contribution of depth input, masked training, and physical refinement, which helps isolate the effect of each module.

- **Learning from HOI video.** Training on human-object interaction data without expensive teleoperation is a practical advantage, and the decoupled architecture (CLIPort for perception, VLM for generation) supports modular fine-tuning for domain shifts. (Contributions, bullet 4; Section 3.3)

- **Well-motivated problem.** The paper targets a genuine gap: most prior language-guided dexterous manipulation work (SemGrasp, AffordDexGrasp) generates static grasp poses, while this paper tackles dynamic manipulation sequences. (Section 1)

## Weaknesses

### Major

- **Baseline selection limits support for SOTA claims.** The paper compares against TM2T, MDM, FlowMDM, and MotionGPT3 — all general human full-body motion models. The paper's own Related Work (Section 2.2) discusses HOIGPT, which also generates text-conditioned hand-object interaction sequences. HOIGPT is the most directly relevant baseline and its absence weakens the claim of state-of-the-art among hand-specific methods. While most other methods discussed (SemGrasp, AffordDexGrasp, DexGrasp Anything) target static grasps and are justifiably excluded, HOIGPT's absence is a gap that should be addressed or explicitly justified.

### Minor

- **Diversity metric partially contradicts reported claims on DexYCB.** The paper states results "consistently outperform all baselines" (Section 4.3), but on DexYCB (Table 1) UniHM's diversity (39.62 seen) is substantially lower than ground truth (125.53) and worse than MotionGPT3 (72.51 seen). The paper defines "Diversity →" as closer to GT being better but does not acknowledge this discrepancy. On OakInk (Table 2), diversity is reasonable, suggesting a dataset-specific issue that merits discussion.

- **Real-world experiments lack statistical detail.** Table 3 reports success rates (e.g., 65% Grab on seen) without trial counts, confidence intervals, hardware specifications (which dexterous hand, robot arm), or number of objects tested. The reader cannot assess statistical significance or reproducibility.

- **No ablation of the cross-morphology tokenizer's core claim.** The unified codebook is a central contribution (Section 3.2), but Table 4 ablates depth input, masked training, and physical refinement — not the shared codebook. An ablation comparing the unified codebook against separate per-hand tokenizers would directly validate the core design.

- **Simulation validation is mentioned but not presented.** The paper states "validate feasibility in simulation" (Section 4) and mentions "lightweight simulation-based optimization" (Section 4.4), but provides no simulation-based metrics (e.g., penetration depth, contact forces) to substantiate physical feasibility claims.

### Trivial

- **Training/inference mismatch not explicitly evaluated.** The VLM is trained on ground-truth trajectories but tested with CLIPort predictions (lines 142–143). An oracle vs. estimated-conditioned comparison would strengthen confidence in the modular design.
- **Missing reproducibility details.** Codebook size K (Eq. 1), physics refinement hyperparameters (α, k, λ_c, λ_vel, λ_acc), and training details (learning rate, batch size, optimizer) are not specified. The CLIPort adaptation for SE(3) trajectory prediction is described as "CLIPort-style" without explaining modifications from its original 2D design.

## Nice-to-Haves

- **Physics refinement applied to baselines:** Applying the same post-processing to all methods is fair, but showing UniHM without refinement vs. baselines with/without refinement would better isolate the source of improvement. (Partially addressed by Table 4's "w/o Physical Refinement" ablation.)
- Clarify what constitutes "seen" vs. "unseen" in the dataset split — object instances, categories, or interaction types?
- Verify the anomalously large standard deviations in Table 1 (e.g., TM2T: 85.33 ± 341), which appear to be PDF-extraction artifacts.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Criticism about standard deviations being suspiciously large:** Parser artifact from PDF extraction, not an author error.
- **Criticism about physics refinement conflation:** Applying the same post-processing to all methods is standard practice for fair comparison; this does not invalidate results.
- **Criticism about missing related work baselines (SemGrasp, AffordDexGrasp, DexGrasp Anything, Multi-GraspLLM):** These methods generate static grasp poses, not manipulation sequences, making them not directly comparable for the paper's task. Only HOIGPT is a relevant missing baseline.
- **Criticism about "first" framework claim:** The paper's scope ("beyond static grasps") is a defensible framing; removing this would over-correct.
- **Generic strengths about "important problem" or "interesting approach":** Insufficiently specific.
- **Reproducibility nitpicks about individual hyperparameter values:** Standard missing details but not decisive for evaluation.

## Novel Insights

None beyond the paper's own contributions. The key evaluation issues (baseline selection relative to hand-specific methods, the diversity discrepancy, and missing cross-morphology ablation) are specific to this paper's experimental design rather than yielding cross-paper synthesis.

## Suggestions

1. Include HOIGPT as a baseline or explicitly justify why it is not comparable (e.g., if it targets a different hand type or task formulation).
2. Acknowledge and explain the diversity discrepancy on DexYCB — does the model trade diversity for precision on this dataset?
3. Add an ablation comparing the unified codebook against separate per-hand tokenizers to validate the core design claim.
4. Report trial counts, hardware specifications, and confidence intervals for real-world experiments.
5. Specify codebook size K, key hyperparameters (α, k, λ_c, λ_vel, λ_acc), and training details for reproducibility.
6. Include simulation-based metrics (penetration depth, contact forces) if available.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>