Now let me compose the final review based on this analysis.

## Summary

UniHM proposes a framework for generating dexterous hand manipulation sequences from free-form language instructions and RGB-D input. The key technical contributions are: (1) a morphology-agnostic VQ-VAE tokenizer with cross-hand knowledge distillation that maps heterogeneous dexterous hands into a shared codebook, (2) a VLM (Qwen3-0.6B) trained on HOI video data (not teleoperation) with a progressive masking curriculum to generate manipulation token sequences conditioned on language and perception, and (3) a physics-guided dynamic refinement module that performs segment-wise energy-based optimization combining contact, generative, and temporal priors. The approach is validated on DexYCB, OakInk, and real-world robot experiments across multiple hand morphologies and task types.

## Strengths

- **Morphology-agnostic tokenizer with cross-hand knowledge distillation (Section 3.2).** Training a shared VQ-VAE codebook with per-hand encoders/decoders plus a distillation loss to align new hand morphologies is a well-motivated engineering contribution. The ability to translate poses between hand types by simply swapping decoders (Eq. 6) demonstrates genuine practical value for cross-embodiment transfer.
- **Training from human HOI video rather than teleoperation (Section 3.1, Section 4.3).** The paper uses retargeted HOI data rather than expensive real-world teleoperation, which meaningfully lowers the barrier to building dexterous manipulation systems. The results demonstrate that this paradigm can produce reasonable results.
- **Physics-guided dynamic refinement (Section 3.4).** The energy-based formulation combining contact (asymmetric penalty with point-to-plane distance), generative prior, and temporal smoothness is well-structured, and the Gauss-Newton with Levenberg-Marquardt damping is appropriate for this nonlinear least-squares problem.
- **Real-world cross-embodiment validation (Table 3, Figure 3).** The paper validates on actual robot hardware across multiple task types (grab, pick&place, pull&push, open&close), which is stronger than purely simulation-based evaluation.

## Weaknesses

### Fatal
None.

### Major

- **Missing comparison against relevant dexterous-manipulation baselines (Section 4.3, Tables 1-3).** The paper compares only against human full-body motion models (TM2T, MDM, FlowMDM, MotionGPT3) adapted via Dex-Retargeting. None of these were designed for dexterous hand manipulation. The paper does not compare against HOIGPT (Huang et al., 2025), which the paper itself cites as generating long 3D hand-object interaction sequences from text and is a directly relevant baseline. While some other cited methods (SemGrasp, AffordDexGrasp) produce static grasps and may not be directly comparable for sequence generation, HOIGPT is a notable omission. The claim of "state-of-the-art" is not properly supported when evaluated only against methods from a different task domain.

- **No direct evaluation of language grounding (Section 4.2).** The paper's core claim is "unified dexterous hand manipulation guided by free-form language commands." However, the main evaluation metrics (MPJPE, FOL, FPL, FID, Diversity) all measure pose accuracy or distribution similarity — not whether the generated sequence matches the language instruction. The real-world success rate (Table 3) is a coarse binary metric that conflates perception, execution, and language grounding errors. There is no human evaluation of instruction alignment, no classification accuracy of performed actions, and no analysis of whether "grasp the bottle" produces different motion from "push the bottle." This is a significant gap for a paper whose central claim depends on language guidance.

- **"First" claims are too strong given existing work (Abstract, Section 1).** The paper claims "the first framework for unified dexterous hand manipulation guided by free-form language commands" and "the first unified, language-conditioned framework for dynamic dexterous hand manipulation beyond static grasps." HOIGPT (Huang et al., 2025), which the paper cites, generates long 3D hand-object interaction sequences from text. While the paper's multi-morphology tokenizer and physics-guided refinement are novel contributions, the "first" framing is overstated given prior sequence-level HOI generation from language.

- **Diversity metric contradicts the claimed superiority on DexYCB (Table 1).** The paper defines Diversity as "closer to the ground truth indicates a more reasonable generation." On DexYCB, GT Diversity = 125.53. The paper's method achieves 39.62 (seen) and 42.70 (unseen), while MotionGPT3 achieves 72.51 (seen) and 75.84 (unseen) — substantially closer to GT. The paper correctly bolds MotionGPT3 in the Diversity column for DexYCB, but the text claims "our method consistently outperforms all baselines across both seen and unseen objects" (Section 4.3), which is not accurate for this metric on this dataset. This discrepancy is not discussed.

- **"Unseen objects" claim is overstated for DexYCB (Section 4.1, Tables 1-2).** DexYCB has only 10 objects. The paper uses an 80/20 split without specifying whether it is sequence-level or object-level. With 10 objects, an 80/20 sequence-level split means the same objects appear in both training and test sets — "unseen" refers to unseen trajectories/interaction patterns, not unseen objects. The abstract, introduction, and conclusion (lines 9, 19, 259, 299) repeatedly claim generalization to "unseen objects." This is more plausible for OakInk (100 objects across 32 categories), but the two datasets' "unseen" regimes are conflated.

### Minor

- **Auto data annotation pipeline is underspecified (Section 3.1).** The GPT-4o annotation procedure is described in one sentence: "provide keyframes as visual context, specifically the first and last frames and the three frames preceding first contact, and the model returns five distinct open-vocabulary natural language instructions." No information is given about prompt design, quality filtering, annotation validation, or how five distinct instructions per sequence are ensured to be meaningfully different. Since language annotations are a core training signal, this underspecification is a reproducibility concern.

- **Circular dependency in cross-hand distillation not discussed (Section 3.2).** The distillation objective (Eq. 3) uses retargeted hand pairs (x_new, x_ref) to align encoders. The paper notes these are "obtained through retargeting." If retargeting is inaccurate for a new hand morphology, those errors propagate into the encoder alignment. This potential circular dependency is not acknowledged or analyzed.

- **VLM architecture details are vague (Section 3.3).** The description mentions a "CLIPort-style vision module" without specifying the exact variant or training details, and an "MLP-based trajectory encoder" without dimensions. The progressive masking curriculum schedule and key hyperparameters (codebook size K, latent dimension d_z, learning rates) are not reported.

- **CLIPort error propagation unanalyzed (Section 3.4, Section 4).** The physics-guided refinement uses CLIPort's predicted target trajectory T_tar(t). At inference, only the CLIPort perception head is adapted to distribution shifts. However, there is no evaluation of CLIPort's trajectory prediction accuracy separately from the full pipeline, so the impact of CLIPort errors on the overall system is unknown.

### Trivial
None.

## Nice-to-Haves
- Statistical significance tests would help clarify whether improvements over MotionGPT3 (e.g., MPJPE: 61.40 vs. 74.80 on seen DexYCB) are significant given the variance in the baselines.
- An analysis of how ablation components trade off (e.g., VLM+tokenizer vs. physics refinement) could better characterize the system's operating regime, since "w/o Physical Refinement" still achieves competitive results.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Suspicious standard deviations in Table 1 (e.g., 85.33 ± 341):** Comparison with the ablation table (Table 4), which correctly shows "61.40 ± 1.93" vs. the main table's "61.40 ± 193", confirms that decimal points were dropped during PDF parsing. The original values are standard deviations in the 0.5–4.0 range, which are normal. This is a parser artifact, not an author error.
- **Any formatting/style criticisms:** Per the hard rules, these are parser artifacts, not author errors.
- **Missing hyperparameters and training details:** Partially subsumed by the minor weakness on VLM architecture underspecification; the broader demand for complete logs is a generic reproducibility concern that applies to most papers and does not constitute a specific weakness of this work.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add proper dexterous-manipulation baselines. At minimum, compare against or justify excluding HOIGPT, which generates HOI sequences from text. For static-grasp methods like SemGrasp, explain why they are not comparable for the sequential setting.
2. Clarify the 80/20 split type (sequence-level vs. object-level) for each dataset and qualify the "unseen objects" claim — report what proportion of the test set involves truly unseen object instances vs. unseen trajectories of seen objects.
3. Address the Diversity discrepancy on DexYCB: either explain why lower diversity is an acceptable trade-off (e.g., physics refinement constrains the output space for feasibility) or acknowledge the limitation in the paper's claims.
4. Add an instruction-following evaluation metric, such as human ratings of semantic alignment between the generated sequence and the language instruction, or classification accuracy using a pretrained action recognizer.
5. Provide more detail on the GPT-4o annotation pipeline (prompt design, quality filters, inter-annotation agreement) and VLM architecture (CLIPort variant, MLP dimensions, training hyperparameters including codebook size, latent dimension, learning rates, and masking schedule).

## Score and Decision

The paper's core technical contributions — a unified tokenizer across hand morphologies, VLM training from HOI video, and physics-guided refinement — are genuinely useful and well-motivated. The real-world hardware validation across multiple task types further strengthens the work. 

However, the evaluation has significant gaps that prevent the paper from supporting its central claims. The comparison against only human motion models (not dexterous-manipulation methods, and notably omitting HOIGPT) means the "state-of-the-art" claim lacks proper support. The absence of any instruction-following evaluation metric undermines the core premise of "language-guided manipulation." The "first" framing is overstated given prior work. Together, these evaluation issues mean the paper's claims are broader than its evidence supports.

The weaknesses are fixable but require non-trivial additional experiments (proper baselines, language grounding evaluation) that go beyond simple clarifications. In its current form, the paper is not ready for acceptance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>