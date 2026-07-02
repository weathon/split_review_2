## Summary
UniHM proposes a framework for generating sequential dexterous hand manipulation sequences from open-vocabulary language instructions and RGB-D input. The method has three components: (1) a VQ-VAE-based unified tokenizer that maps multiple hand morphologies into a shared codebook, (2) a small VLM (Qwen3-0.6B) trained with a progressive masking curriculum to generate token sequences from text + visual input, and (3) a physics-guided Gauss-Newton trajectory refinement. The paper evaluates on DexYCB and OakInk datasets and reports real-world results.

## Strengths
- **Cross-morphology shared codebook is a technically novel contribution.** The idea of a unified VQ-VAE codebook with per-hand encoders/decoders and knowledge-distillation-based alignment for new morphologies (Eq. 3) provides a clean way to share data across hand types. The hand-pose translation formula (Eq. 6) is a natural consequence and enables cross-hand retargeting without separate retraining. This is the paper's most novel technical ingredient.
- **Data-efficient training paradigm is well-motivated.** Training the VLM on existing HOI datasets (DexYCB, OakInk) with GPT-4o annotation and retargeting, rather than requiring large-scale real-world teleoperation data, is a practical advantage. The motivation in §3.3 for using a 0.6B VLM (rather than 7B+) given data scarcity is sensible.
- **Physics-guided refinement formulation is principled.** The energy-based optimization (Eq. 11–18) combining contact, generative, and temporal priors is clearly specified with differentiable contact penalty functions and Gauss-Newton with Levenberg-Marquardt damping. The frame-by-frame optimization procedure is practical.
- **Real-world deployment is demonstrated.** Despite thinness of the statistics, the fact that the system was deployed on a physical dexterous hand across four task categories (Table 3) provides some evidence of practical viability.

## Weaknesses
### Fatal
None.

### Major
- **The SOTA claim is not supported because the most relevant prior work is not compared against.** The paper compares against TM2T, MDM, FlowMDM, and MotionGPT3 — all human whole-body motion generation models not designed for hand-specific manipulation, point-cloud inputs, or contact-rich constraints. More critically, the paper cites HOIGPT (Huang et al., 2025) in §2.2 as a method that "extends token-based generation to long 3D hand-object interaction, learning a bidirectional mapping between text and HOI sequences" but never compares against it. SemGrasp, AffordDexGrasp, and DexGrasp Anything are also discussed in §2 as language-guided dexterous methods. If the paper's core claim is SOTA on language-conditioned dexterous hand manipulation, these are the natural competitors. Applying UniHM's own refinement module to baselines (line 257: "we post-process their outputs with our physics-guided refinement to ensure a fair comparison") tests (UniHM VLM + refinement) vs. (human-motion model + UniHM's refinement), which only isolates the VLM difference. This comparison protocol does not support the headline "state-of-the-art" claim.

- **The main evaluation metrics are misaligned with the paper's central claim of physical feasibility.** The abstract and introduction emphasize "physically feasible dexterous hand manipulation" as the core challenge. The paper categorizes MPJPE, FOL, and FPL under "Physically Feasible" (§4.2, line 250), but these are trajectory-similarity metrics measuring distance from a human demonstration, not direct measures of physical feasibility (collision, force closure, joint limits, task completion). No simulation-based feasibility metrics (penetration depth, force-closure scores, task-completion rates in physics simulation) are reported. The only direct feasibility measure is the real-world success rate (Table 3), which has its own limitations. This mismatch between the paper's stated goal and its evaluation framework weakens the evidential basis for the central claim.

### Minor
- **Real-world evaluation lacks statistical rigor.** Table 3 reports success rates (range 5–65%) without trial counts, confidence intervals, or error bars, making it impossible to assess whether differences between methods are meaningful. The paper does not specify which dexterous hand was used, how many objects, or the number of trials per cell. The baselines ("MDM+Dex-Retargeting", "MotionGPT3+Dex-Retargeting") are again human motion models, and no static-grasp-then-execute baseline is included.

- **Training/inference distribution mismatch is not analyzed.** The VLM receives ground-truth target trajectories and object point clouds during training, but at inference these are estimated by CLIPort and PointSAM (§3.3). The paper frames this modularization as a feature, which is reasonable in principle, but never quantifies the degradation. A controlled experiment feeding ground-truth vs. CLIPort-estimated inputs at inference would clarify whether the decoupling holds up.

- **Missing ablations for the paper's claimed key contributions.** The ablation study (Table 4) tests depth input, masked training, and physical refinement. It does **not** ablate: (a) the unified codebook vs. separate codebooks per hand, (b) cross-morphology distillation, (c) ground-truth vs. CLIPort-estimated trajectories at inference, or (d) different VLM sizes. These would isolate the contributions presented as novel.

- **VQ-VAE diagnostic details are missing.** The paper defines the codebook as {e_k}_{k=1}^K with e_k in R^{d_z} (line 76) but never reports K, d_z, the number of tokens per sequence, or reconstruction accuracy (e.g., reconstruction MPJPE). Tokenization quality bounds downstream VLM performance, so these details matter. Codebook utilization is also not discussed.

- **CLIPort and PointSAM modules are underspecified.** The paper describes "a CLIPort-style vision module" and "Point-SAM" (§3.3) without architecture details, training procedure, or independent evaluation of their accuracy. Since errors in these modules propagate into the VLM, their reliability is important for understanding the full system.

- **The masking schedule p_t is not specified.** The paper describes a progressive masking curriculum where p_t increases from 0 to 1 (§4.4) but does not report the schedule (linear, cosine, step-wise, etc.). This is needed for reproducibility.

### Trivial
- The DexYCB description (§4.1) reads "10 objects, 20 objects" — likely "10 categories, 20 instances" — but is ambiguous.
- The "first framework" claim (§1, line 9) is somewhat overstated given that HOIGPT (cited in §2.2) also generates sequential HOI from text, even if the task boundaries differ.

## Nice-to-Haves
- Simulation-based feasibility metrics (penetration depth, force-closure percentage, task completion rate in a physics simulator) would directly support the "physical feasibility" claim.
- An independent evaluation of CLIPort's trajectory estimation accuracy.
- Inference-time latency statistics for real-world deployment.
- Comparison against a static-grasp-then-execute pipeline as a simpler baseline.

## Removed Points
These points were raised in the input review but are removed for the following reasons:
- **FOL/FPL naming confusion** — The paper defines FOL as "Final Orientation Location Error"; the acronym is consistent with the expansion. This is a misreading by the reviewer.
- **Data annotation quality not validated** — Using GPT-4o for annotation is standard practice; calling this out without evidence of failure is speculative.
- **Inference speed, codebook utilization diagnostics** — Standard nice-to-have diagnostics, not core weaknesses affecting the paper's validity.
- **General characterization of prior work in §1** — The paper does acknowledge language-guided methods and correctly notes they target static grasps; the claim that this is "too sweeping" is not well-supported.
- **Diversity metric interpretation on DexYCB** — The gap between GT Diversity (125.53) and Ours (39.62) is large, but the paper does not claim superiority on this metric (Ours is not bolded for Diversity in Table 1). The reviewer's concern here reflects a misreading of the table.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Replace or supplement the baselines with HOIGPT** (the most directly comparable prior work for text-conditioned sequential HOI generation) and the other language-guided dexterous methods cited in §2.
2. **Add simulation-based physical feasibility metrics** (penetration depth, task completion rate, force-closure percentage) to directly support the "physically feasible" claim.
3. **Quantify the training/inference gap** by evaluating the VLM with ground-truth vs. CLIPort-estimated inputs at inference.
4. **Report trial counts and confidence intervals** for all real-world experiments.
5. **Add ablations** for the unified codebook (replace with per-hand codebooks), cross-morphology distillation, and ground-truth vs. CLIPort trajectories.
6. **Report VQ-VAE diagnostics**: codebook size, reconstruction MPJPE, codebook utilization.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>