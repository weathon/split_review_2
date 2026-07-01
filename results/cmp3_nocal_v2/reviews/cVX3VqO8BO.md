Here is the final consolidated review:

---

## Summary

UniHM proposes a framework for generating sequential dexterous hand manipulation from open-vocabulary language instructions and RGB-D images. The method combines three stages: (1) a Unified Hand-Dexterous Tokenizer with a shared VQ-VAE codebook across multiple hand morphologies, (2) a VLM (Qwen3-0.6B) conditioned on visual/trajectory inputs to generate token sequences, and (3) a physics-guided dynamic refinement stage using Gauss-Newton optimization with contact, generative, and temporal priors. Evaluations on DexYCB and OakInk show competitive results on pose accuracy metrics, with real-world trials reported.

## Strengths

1. **Well-motivated problem and clear gap identification.** The paper correctly identifies that prior language-guided dexterous manipulation work (SemGrasp, AffordDexGrasp) generates static grasps rather than manipulation sequences, and that existing sequential methods lack open-vocabulary conditioning (Section 1, Section 2.1). This framing is timely and the paper genuinely targets this gap.

2. **Technically well-specified physics refinement stage (Section 3.4).** The contact energy (Equations 11–13) with its asymmetric penalty distinguishing surface penetration from approach, the generative prior (Equation 14), and the temporal smoothness prior (Equation 15) are combined into a Gauss-Newton solve (Equation 17) in a manner that is mechanically sound and clearly explained. This is the clearest, most complete part of the method.

3. **Sensible formulation for the cross-hand tokenizer (Section 3.2).** The idea of a shared discrete codebook with hand-specific encoders/decoders aligned via distillation (Equation 3) to bypass the non-differentiable quantization step is a technically reasonable design choice. The unified hand pose translation (Equation 6) cleanly formalizes cross-hand transfer.

## Weaknesses

### Fatal
None.

### Major

1. **The core claimed contribution—a cross-hand unified tokenizer—is never experimentally validated.** The paper claims a "Morphology-Agnostic Codebook" that "enables direct token reuse and transfer across robotic and anthropomorphic hands" (line 38) and lists this as a second contribution. However, all simulation experiments (Tables 1, 2) evaluate only on the MANO hand using DexYCB and OakInk datasets. There is no experiment demonstrating cross-hand transfer (e.g., encode with hand A, decode with hand B and measure retargeting error), no comparison of token usage across hands, and no ablation comparing the shared codebook against per-hand codebooks. The real-world experiments (Table 3) do not even specify which robot hand was used. The most novel component of the pipeline is described in detail but presented without supporting evidence.

2. **The Diversity metric results in Table 1 contradict the paper's stated claims.** The caption states "The arrow pointing to the right means closer to the GT." On DexYCB, the GT Diversity is 125.53. On the Seen split, MotionGPT3 achieves 72.51 (closest to GT), while Ours achieves 39.62 (farther from GT). On the Unseen split, MotionGPT3 achieves 75.84 (closest to GT), Ours achieves 42.70. Despite this, the Ours row is bolded across all columns including Diversity. The paper's text (line 257) claims "our method consistently outperforms all baselines across both seen and unseen objects," which is factually incorrect for Diversity on DexYCB. This is either a formatting error that misleads the reader or selective presentation of results.

3. **The ablation study (Table 4) omits the most novel component.** The ablation tests three variants (w/o Depth Input, w/o Masked Training, w/o Physical Refinement) but does not test the unified hand tokenizer itself. An ablation comparing separate per-hand codebooks vs. the proposed shared codebook is essential to support the paper's second claimed contribution and to verify that the shared codebook provides benefit rather than simply partitioning representational capacity across hands.

### Minor

4. **The "first" claim is difficult to substantiate given HOIGPT.** The abstract (lines 8–9) and contributions claim "the first framework for unified dexterous hand manipulation guided by free-form language commands" and "the first unified, language-conditioned framework for dynamic dexterous hand manipulation beyond static grasps." The paper's own Related Work section cites HOIGPT (Huang et al., 2025), which "extends token-based generation to long 3D hand-object interaction, learning a bidirectional mapping between text and HOI sequences" (line 52). The paper later argues prior work "predominantly target[s] Digital Hand, low-DoF grippers, or static grasp poses" (line 52), but the "first" claims need sharper delineation from HOIGPT, which also handles text-conditioned HOI sequences.

5. **"Learning from video" claim overstates what is done.** The paper states it "eliminates the dependency on expensive teleoperation data by learning dexterous manipulation skills from human videos" (line 40) and is "trained solely on human-object interaction data" (line 9). The datasets used (DexYCB, OakInk) are meticulously captured multi-view studio datasets with precise 3D MANO annotations and motion capture infrastructure—not casually recorded "videos." The approach avoids robot teleoperation data but still depends on expensive mocap infrastructure. The framing creates an inflated impression of data efficiency.

6. **Baselines are motion generation models, not manipulation-specific systems.** The paper compares against TM2T, MDM, FlowMDM, and MotionGPT3—general human full-body motion generation models. While the paper posts-processes their outputs with physics refinement (line 257), the comparison primarily shows that UniHM outperforms adapted motion generators. HOIGPT (cited as handling HOI sequences) would be a more relevant baseline. The omission limits the strength of the "state-of-the-art" claims.

7. **Real-world evaluation (Table 3) lacks experimental detail.** Success rates are reported as point estimates (e.g., "65%") without trial counts, confidence intervals, or error bounds. The specific robot hand and arm are not identified, and the seen/unseen split criteria for real-world objects are not defined.

### Trivial

8. **MPJPE, FOL, and FPL are labeled "Physically Feasible" metrics (line 250), but they are geometric reconstruction accuracy measures, not direct measures of physical feasibility (e.g., penetration depth, contact stability).**

9. **Point-SAM is mentioned (line 120) without a citation, and the CLIPort usage is ambiguous** ("CLIPort-style" in line 112 vs. "a CLIPort model" in line 114), with no explanation of how CLIPort—designed for SE(3) pick-and-place—is adapted for dexterous trajectory inference.

## Nice-to-Haves
- Report cross-hand transfer experiments (encode with hand A, decode with hand B, measure retargeting error) and ablation of shared vs. per-hand codebooks.
- Include trial counts and confidence intervals for real-world experiments.
- Clarify the precise relationship to HOIGPT and qualify the "first" claims.
- Provide a citation for Point-SAM and clarify the CLIPort adaptation.

## Removed Points
These points were considered but removed per filtering rules:
- **"No code or dataset release plan mentioned"** and **"No inference speed reported"**: These are reproducibility/completeness suggestions, not weaknesses that undermine the paper's claims. Removed per Hard Rule 7 (trivial reproducibility nitpicks).
- **"GPT-4o annotation is a convenience, not a scientific contribution"**: The paper does not list the auto-annotation pipeline as a contribution; this criticism mischaracterizes the paper. Removed.
- **"Progressive masking hyperparameters not reported"**: A minor implementation detail that does not affect the validity of the claims. Removed per Hard Rule 7.
- **Strength about "problem framing is timely and well-motivated"**: This was generic/superficial per the filtering rules. Kept a more specific version under Strengths.

## Novel Insights

The most useful observation across the reviews is the disconnect between the paper's central claimed contribution (morphology-agnostic codebook enabling cross-hand transfer) and the complete absence of experiments testing this capability. This is not a subtle omission—every experiment evaluates only the MANO hand, and the ablation omits the unified tokenizer entirely. The Diversity metric contradiction in Table 1 is a concrete, verifiable misrepresentation that would mislead a reader scanning the results. Together, these issues indicate that the paper overstates its claims relative to the evidence provided.

## Suggestions
1. Add cross-hand transfer experiments and an ablation of shared vs. per-hand codebooks to validate the unified tokenizer.
2. Correct the Diversity metric presentation in Table 1 and qualify the "consistently outperforms" claim.
3. Include HOIGPT or another manipulation-specific baseline, or clearly explain why such a comparison is infeasible.
4. Report trial counts and confidence intervals for real-world experiments and specify the robot hardware.
5. Sharply delineate novelty relative to HOIGPT and qualify "first" claims.
6. Provide a citation for Point-SAM and clarify the CLIPort adaptation mechanism.

## Score and Decision

The paper addresses a timely problem with a plausible technical pipeline and achieves competitive results on standard pose accuracy metrics. However, the most novel claimed contribution (cross-hand unified tokenizer) has no experimental validation, the Diversity metric presentation is misleading, and the ablation omits the paper's signature component. These issues are substantial enough that the paper cannot be accepted in its current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>