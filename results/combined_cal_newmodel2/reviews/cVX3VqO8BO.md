Now I have a thorough comparison. Let me compile my final review.

## Summary

The paper proposes UniHM, a framework for generating dexterous hand manipulation sequences from open-vocabulary language instructions. It combines a morphology-agnostic VQ-VAE codebook (for cross-hand token sharing), a VLM-based sequence generator (Qwen3-0.6B with CLIPort trajectory planner), and physics-guided dynamic refinement for physical feasibility. Evaluations are on DexYCB, OakInk, and real-world trials.

## Strengths

1. **Important problem**. Language-conditioned sequential dexterous manipulation is a meaningful step beyond the static-grasp generation that dominates prior dexterous work. The paper correctly identifies this gap (Section 1).

2. **Architecturally sound design**. The morphology-agnostic VQ-VAE codebook with distillation-based cross-hand training (Eq. 3-6) is a clean idea for enabling token reuse across hand types without retraining the full system.

3. **Clean ablation structure**. Table 4 cleanly isolates the contribution of each component (depth input, masked training, physical refinement).

4. **Real-world trials**. Table 3 reports success rates across 4 task types on seen/unseen objects, providing evidence of practical feasibility beyond simulation.

5. **Honest limitations**. The conclusion acknowledges missing tactile sensing, simplified contact/friction modeling, and limited bimanual/tool-use coverage.

## Weaknesses

### Fatal
None.

### Major

1. **Missing comparison against relevant dexterous manipulation baselines.** The paper benchmarks only against general human motion generation models (TM2T, MDM, FlowMDM, MotionGPT3) that have no mechanism for conditioning on object geometry or physical interaction. HOIGPT (Huang et al., 2025), cited in Section 2.2, generates text-conditioned 3D hand-object interaction sequences and would be a natural baseline. The paper's claim to *"state-of-the-art"* results in dexterous manipulation is unsupported without comparison to methods actually in that domain. (The difficulty of direct comparison is acknowledged — most existing dexterous methods produce static grasps — but HOIGPT is a clear exception.)

2. **Core contribution experimentally unvalidated.** The morphology-agnostic codebook (Contribution 2, Section 3.2) is a centerpiece of the paper, yet no experiment demonstrates that tokens learned on one hand morphology transfer to another, or that cross-morphology training improves results over independent training. Without this evidence, the claim that the tokenizer *"enables direct token reuse and transfer across robotic and anthropomorphic hands"* remains unsupported.

3. **Real-world evaluation lacks essential detail.** Table 3 does not specify which robot hand was used among the five listed (Shadow, Allegro, SVH, Leap, Panda), how many trials were conducted per condition, how *"success"* was defined and judged, or which specific objects were used. Without these details the results cannot be evaluated or reproduced.

### Minor

4. **Metric mismatch with free-form generation.** MPJPE, FOL, and FPL measure per-frame error against a single ground-truth trajectory. For a free-form generation task where multiple valid manipulation strategies exist, this penalizes valid diversity. No metric directly measures functional manipulation success (grasp stability, task completion). The FID and Diversity metrics partially address realism/variety, and real-world success rate helps, but the primary simulated metrics are mismatched to the generation framing.

5. **Overclaiming on "first" and "state-of-the-art."** The claim of being *"the first unified, language-conditioned framework for dynamic dexterous hand manipulation beyond static grasps"* is overstated given that HOIGPT (Section 2.2) already generates text-conditioned 3D hand-object interaction sequences. While UniHM targets robot-hand morphologies specifically, this distinction does not warrant a *"first"* claim without explicit comparison. Additionally, the statement that UniHM *"consistently outperforms all baselines"* (Section 4.3) is contradicted by the Diversity metric, where MotionGPT3 achieves values closer to ground truth (72.51 vs. 39.62 on DexYCB seen; 75.84 vs. 42.70 on unseen).

6. **"Generalization without Teleoperation" needs qualification.** The method still relies on Dex-Retargeting (Qin et al., 2023) to map MANO poses to robot hands, which is a transfer pipeline built on human motion capture data. The claim is not false, but it conflates *"no new teleoperation collection"* with *"no dependency on human demonstration data."*

7. **Missing architectural details.** Codebook size *K*, latent dimension *d_z*, the masking schedule *p_t*, and training hyperparameters (learning rate, batch size, optimizer, training steps) are absent, limiting reproducibility.

### Trivial
None.

## Nice-to-Haves
- Add HOIGPT as a comparison baseline on sequence-level metrics, and adapt static-grasp methods (SemGrasp, AffordDexGrasp) with a reasonable extension to sequences.
- Add a functional manipulation metric in simulation (e.g., grasp success rate, object displacement).
- Report trial counts, hand used, and success criteria for the real-world evaluation.
- Include a small-scale cross-morphology transfer study (e.g., Allegro → Shadow) to validate the codebook contribution.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Diversity contradiction (Harsh Critic Issue 3):** The reviewer claimed the paper *"marks its own method as better on diversity"* despite a baseline being closer to GT. This is factually incorrect — in Table 1, MotionGPT3's Diversity values (72.51 seen, 75.84 unseen) are bolded, not UniHM's. The criticism was based on a misreading of the table formatting.
- **Metrics from wrong literature:** The claim that metrics are *"drawn from the human motion generation literature"* cannot be verified without access to the cited prior works (Wei et al., 2025a; Zhang et al., 2025, etc.). The paper cites a long list of references for its evaluation protocol.
- **Missing appendix / formatting / reproducibility nitpicks:** Removed per filtering rules.
- **Several Strengthening section suggestions** overlap with weaknesses already listed; duplicates removed.

## Novel Insights

The reviews surface a clear structural gap between the paper's framing (advancing dexterous manipulation SOTA) and its experimental design (evaluating against human motion methods while citing but not comparing against dexterous manipulation baselines). The unvalidated cross-hand codebook claim is another notable weakness that the paper's own contribution list foregrounds but the experiments do not address.

## Suggestions

1. Replace or supplement the human-motion baselines with HOIGPT and adapted static-grasp methods.
2. Add cross-morphology transfer experiments to validate the core codebook contribution.
3. Provide the missing experimental details for Table 3 (hand used, trial count, success criteria, object list).
4. Add a functional manipulation metric (e.g., grasp success in simulation) alongside trajectory error metrics.
5. Tone down "first" and "state-of-the-art" claims to match the actual comparison scope.

## Score and Decision

Now let me calibrate my score.

**Round 1 Bracket:** I searched bands (0-1.5], (1.5-3.5], (3.5-5.5], (5.5-7.5], (7.5-8.5], (8.5+). The most relevant anchors were:
- **xcHIiZr3DT** (2.50, band 1.5-3.5) — dexterous grasping paper with marginal contribution, combining existing techniques. UniHM is clearly stronger.
- **ZYwLfi50GI** / HOI-Diff (5.25, band 3.5-5.5) — text-driven HOI generation. Rejected. Same core weakness: comparing against general human motion instead of relevant HOI methods. Was scored 5, 5, 5, 6.
- **twIPSx9qHn** / Cross-Embodiment (5.00, band 3.5-5.5) — cross-embodiment dexterous grasping with RL. Accepted. Validated its core claim (cross-embodiment transfer) experimentally but had weak baselines (ablations only). Scored 6, 6, 3.
- **nTNElfN4O5** / 3D Interacting Hands (5.50, band 4.0-6.0) — Rejected. Technical novelty concerns but clean experiments.
- **h7aQxzKbq6** / HAMSTER (6.00, band 5.5-7.5) — hierarchical VLM for robot manipulation. Significantly stronger on evaluation rigor.

**Initial bracket (Round 1):** 4.0–5.5

**Round 2 narrowing** inside this bracket confirmed the closest anchors are HOI-Diff (5.25, same baseline-mismatch pathology) and Cross-Embodiment (5.00, similar scope but cleaner validation of core claim). UniHM has more architectural components and real-world evaluation than HOI-Diff, but has an unvalidated core contribution and less rigorous evaluation than Cross-Embodiment.

**Favorability comparison:** The items with the strongest negative favorability in my draft are the missing baselines (−0.75), unvalidated codebook (−1.14), and missing experimental details (−1.31). These directly mirror the weaknesses that scored HOI-Diff at 5.25 and Cross-Embodiment at 5.00. The most positive items (ablation structure at 13.24, architectural elegance at 12.18) are genuine strengths but cannot compensate for the structural evaluation gaps.

**Final score: 4.5.** The paper has a coherent architecture and tackles an important problem, but the evaluation does not match the claims: the baselines are from a different sub-field, the core contribution is unvalidated, key experimental details are missing, and several claims are overstated. These are correctable weaknesses that a major revision could address, but as submitted the evidence does not support the claimed level of contribution.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>