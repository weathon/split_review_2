Now I have enough to finalize the review.

---

## Summary
UniHM proposes a framework for generating dexterous hand manipulation sequences conditioned on free-form language. It introduces a morphology-agnostic VQ-VAE tokenizer with staged cross-hand distillation, trains a small VLM (Qwen3-0.6B) on human-object interaction (HOI) video without teleoperation, and applies a physics-guided Gauss–Newton refinement for temporal consistency and physical feasibility. Results are reported on DexYCB and OakInk benchmarks, plus real-world trials across four task categories.

## Strengths
- **Real-world evaluation across diverse task types.** Table 3 reports success rates for Grab, Pick&Place, Pull&Push, and Open&Close on both seen and unseen objects, with large absolute margins over baselines (e.g., 65% vs. 30% Grab seen, 60% vs. 25% Pull&Push seen). This is more substantive evidence than simulation-only dexterous manipulation papers.
- **Staged knowledge-distillation tokenizer.** The two-phase scheme — aligning a new encoder's latent space with a reference encoder via Equation 3 before VQ integration — is a technically clean solution to the gradient discontinuity across quantization boundaries, with a well-motivated formulation (Equations 1–6).
- **Eliminating teleoperation data.** Training entirely on HOI video and demonstrating cross-embodiment transfer is a genuine practical contribution that reduces data acquisition cost; this paradigm is validated in the real-world experiments.

## Weaknesses

### Fatal
None.

### Major
- **Baselines are out-of-class throughout.** Tables 1 and 2 compare only against general whole-body motion generation models (TM2T, MDM, FlowMDM, MotionGPT3). Methods directly competing in the dexterous hand manipulation space—HOIGPT, Multi-GraspLLM, SemGrasp, AffordDexGrasp—are cited in Section 2's related work but absent from every experimental table. The real-world Table 3 likewise uses "MDM+Dex-Retargeting" and "MotionGPT3+Dex-Retargeting" rather than SemGrasp or Multi-GraspLLM. Section 4.3's claim that the method "unequivocally" establishes cutting-edge performance cannot be sustained when the direct competitors are not included; outperforming body-motion models on a hand-manipulation benchmark is a much weaker claim than the paper makes.

- **Primary architectural contribution—the tokenizer—is never ablated.** Table 4 tests depth input, masked training, and physical refinement, but not the tokenizer itself. There is no variant using per-hand VQ-VAEs (no shared codebook), no variant with a shared codebook but without cross-hand distillation, and no retargeting-only baseline in place of the tokenizer. The paper's stated first contribution is the morphology-agnostic codebook, yet its quantitative impact on the reported metrics is entirely unverified.

- **Physical refinement is applied to baselines, confounding the main comparison.** Section 4.3 states: "we post-process their [baselines'] outputs with our physics-guided refinement to ensure a fair comparison." This means the gap in Tables 1–2 could originate from the refinement rather than the VLM or tokenizer. Table 4 shows UniHM "w/o Physical Refinement" (65.78 MPJPE seen), but does not show baselines without refinement. The contribution of the generation model vs. the post-processing step cannot be distinguished.

### Minor
- **Diversity metric is worse on DexYCB, unacknowledged.** Tables 1 and 2 define Diversity (→) as closer to GT being better. On DexYCB seen, GT=125.53, UniHM=39.62, and MotionGPT3 achieves 72.51 (closer to GT). Similarly for DexYCB unseen: UniHM=42.70 vs. MotionGPT3=75.84. The paper claims to "consistently outperform all baselines across both seen and unseen objects" without qualifying this exception. Diversity is relevant to the core "open-vocabulary instruction" framing, as it indicates whether outputs are semantically varied or mode-collapsed.

- **Training/inference mismatch is acknowledged but not quantified.** Section 3.3 explicitly notes that at training, ground-truth trajectories and point clouds are used; at inference, CLIPort and Point-SAM estimates are used. The paper calls this a feature ("robustness to environmental shift"), but no ablation isolates how much performance degrades from imperfect CLIPort estimates vs. oracle inputs. Given the precision requirements of dexterous manipulation, this gap is non-trivial to dismiss.

- **Real-world trial counts and success definitions unspecified.** Table 3 success rates are all multiples of 5%, consistent with ≤20 trials per cell. The main text does not report the number of trials per condition, object selection criteria, or how "success" is operationally defined for each task type (e.g., what counts as a successful Open&Close). This limits reproducibility and critical assessment.

### Trivial
- The abstract claim — "first framework for unified dexterous hand manipulation guided by free-form language" — is insufficiently delimited: HOIGPT generates text-conditioned HOI sequences; SemGrasp is language-conditioned for static grasps. A more precise delimitation (e.g., "first to generate temporal sequences under language across heterogeneous robot hand morphologies") would be more defensible.

## Nice-to-Haves
- A cross-morphology transfer quality table (e.g., reconstruction error when encoding with one hand and decoding with another) would provide direct quantitative evidence for the tokenizer's central design claim.
- Even a single properly adapted direct competitor (HOIGPT for sequence generation, or Multi-GraspLLM for cross-hand grasping) would substantially strengthen the SOTA claim and distinguish the contribution from body-motion adaptation baselines.
- Report the number of real-world trials and a clear success definition in Table 3.
- Disentangle the refinement contribution from the generation model contribution by showing baselines both with and without the physics post-processing.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Missing appendix/proofs**: reviewer concern about appendix-deferred proofs removed per policy (parser strips appendix sections).
- **Reproducibility concerns about CLIPort/Point-SAM hyperparameters**: removed per policy on trivial implementation details.
- **"Unfair comparison" framing**: the reviewer notes baselines are post-processed with UniHM's refinement — this is retained as a Major weakness since it genuinely confounds results, but the framing that it "favors" the baselines was reframed correctly: the authors apply their own refinement to baselines to close the gap, which confounds attribution rather than being simply unfair to UniHM.
- **Generic strength about problem importance**: removed per policy on superficial strengths.

## Novel Insights
The staged distillation approach — aligning a new encoder's latent space with the reference encoder *before* VQ integration (Equation 3), to circumvent the non-differentiable quantization barrier — is an underappreciated engineering pattern for multi-morphology discrete action spaces. This suggests that cross-embodiment tokenizers may systematically require two-phase curriculum integration rather than joint training, a principle potentially applicable beyond dexterous hands to any multi-agent/multi-embodiment VQ-based policy framework.

## Suggestions
1. **Replace or supplement baselines** with at least one direct competitor from the dexterous hand generation space (HOIGPT, Multi-GraspLLM, SemGrasp with sequence adaptation). This is the single highest-impact change.
2. **Add tokenizer ablation**: per-hand VQ-VAEs vs. shared codebook without distillation vs. shared codebook with distillation. These three variants directly validate the paper's first stated contribution.
3. **Disentangle refinement from generation**: show Tables 1–2 with baselines both with and without UniHM's physics refinement, and with UniHM both with and without it. This is already partially present in Table 4 but must be extended to baselines.
4. **Report real-world experimental protocol**: number of trials per cell, success definition per task type, and object selection criteria for Table 3.
5. **Acknowledge and discuss the diversity deficit** on DexYCB in Section 4.3, including its potential implication for language-conditioned generalization.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| xcHIiZr3DT (Vision-Based Pseudo-Tactile Dexterous Grasping) | 2.50 | R1 | Weak dexterous grasping paper, much narrower scope than UniHM |
| sXF5P4N7e8 (Vision-Based Grasping Goal-Conditioned Masking) | 3.00 | R1 | Simple grasping method, limited contribution; UniHM has more system-level depth |
| wl1Kup6oES (From Appearance to Motion) | 3.00 | R1 | Basic visual representation, insufficient for dexterous manipulation specifics |
| aVyJwS1fqQ (Mani-WM) | 4.67 | R1 | Interactive world model for manipulation, rejected; more complete evaluation than UniHM's baseline selection |
| 29p13QihRM (Language-Guided Object-Centric World Models) | 4.00 | R1 | Language-guided manipulation world model; rejected with similar scope issues |
| VaoeAi5CW8 (Diffusion Trajectory-guided Policy) | 4.25 | R1 | Two-stage manipulation framework, rejected; has more appropriate baselines |
| AJQuTFd9es (HandsOnVLM) | 6.33 | R1 | VLM for hand-object interaction prediction; accepted at 6.33, has proper benchmark and suitable baselines |
| hPWWXpCaJ7 (GEVRM) | 6.00 | R1 | Closed-loop VLA for robust manipulation; accepted with proper baselines |
| ajSmXqgS24 (DexTrack) | 6.25 | R1 | Dexterous manipulation tracking from human references; very similar domain, accepted at 6.25, with proper evaluation |
| h7aQxzKbq6 (HAMSTER) | 6.00 | R1 | Hierarchical VLA for open-world robot manipulation; accepted at 6.0 |

**Round 1 bracket:** UniHM sits between the 3.0–4.5 reject range and the 6.0–6.5 accept range. The paper has genuine contributions (real-world system, interesting tokenizer design, HOI-from-video training), but three concurrent major flaws—out-of-class baselines, unablated primary contribution, and confounded refinement contribution—are similar in severity to why papers like VaoeAi5CW8 (4.25) were rejected. Papers that were accepted at 6.0–6.25 (DexTrack, HAMSTER, GEVRM) all featured appropriate baseline comparisons and ablations that directly validated their stated contributions. UniHM's missing tokenizer ablation and out-of-class baselines are disqualifying for a score above 5. Given the real-world results (which are more substantive than most rejected papers) and the coherent system design, the paper sits above the 3.0 reject range. **Initial bracket: 4.0–5.0.**

**Round 2 reasoning:** The three major weaknesses are each individually significant: (1) SOTA claim unsubstantiated against actual competing methods; (2) the primary contribution's quantitative impact is unverified; (3) the refinement contribution is confounded in the main tables. These are not addressable by a brief rebuttal — they require rerunning experiments. However, the paper does have substantial real-world results (Table 3), a well-motivated architecture, and genuine technical novelty in the tokenizer design. This places it at **4.0** (borderline reject): the technical contributions are real but the core evaluative claims are insufficiently supported to warrant acceptance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>