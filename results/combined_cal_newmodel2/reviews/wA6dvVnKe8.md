Now I have thorough calibration. Let me compile the final review.

## Summary

This paper proposes EDPA (Embedding Disruption Patch Attack), a novel adversarial patch attack for Vision-Language-Action (VLA) models that requires only access to the visual encoder's parameters, unlike prior work requiring knowledge of the action space or robot manipulator. The attack uses two complementary objectives: patch contrastive loss to maximize embedding discrepancy between clean and perturbed visual inputs, and image-instruction alignment loss to disrupt visual-textual semantic alignment. The paper further proposes an adversarial fine-tuning scheme for the visual encoder as a defense. Experiments across OpenVLA, OpenVLA-OFT, and π₀ on the LIBERO benchmark show EDPA substantially increases task failure rates, while the defense partially mitigates this degradation on OpenVLA.

## Strengths

- **Genuinely less restrictive threat model.** EDPA requires only access to the visual encoder's parameters, whereas UADA and UPA (Wang et al., 2024) require knowledge of the action space or robot manipulator, plus access to all VLA model parameters. Table 1 and Figure 1 provide a clean, honest summary of these differences — this is a meaningful practical advance.
- **Evaluation spans multiple VLA models.** The paper tests on OpenVLA, OpenVLA-OFT, and π₀ across all four LIBERO task suites (Spatial, Object, Goal, Long). Results across models with different architectures and camera configurations lend credibility to the attack's broad applicability.
- **Practical defense design.** Adversarial finetuning only the visual encoder (not the full VLA, including the expensive LVLM backbone) is computationally efficient and architecturally modular. The use of periodically reinitialized patches (Algorithm 1, φ = 1000) to prevent overfitting to a single patch pattern is a sensible design choice.
- **Interesting qualitative observation.** The observation that adversarial patches consistently exhibit structural patterns resembling robot arms (Figure 2), together with the hypothesis that VLA visual encoders overfit to the limited viewpoints and arm appearances in robotic datasets (Section 5), is a genuine insight that goes beyond the paper's core contribution.

## Weaknesses

### Major

- **Defense evaluation protocol under-specified regarding adaptive attacks.** The paper evaluates the adversarially fine-tuned encoder "against patch attacks" (Section 4.2) but does not state whether the patches used for evaluation were generated against the original (undefended) encoder or against the fine-tuned encoder. If only against the original encoder, the defense results (Table 2) could largely reflect that patches do not transfer perfectly between different encoders — a substantially weaker claim than "the defense is robust to adversarial patches." Algorithm 1 shows the right adaptive training procedure, but the evaluation protocol needs to be clearly stated. This is the most significant concern and should be addressed in the rebuttal.

### Minor

- **The comparison with UADA and UPA on LIBERO is under-specified.** The paper evaluates these baselines on the LIBERO benchmark (Section 4.2) but does not explain how they were adapted to LIBERO's action space or evaluation protocol. Since UADA is explicitly tied to the action token structure of a 7-DoF arm (Wang et al., 2024), it is unclear whether the implementation is a faithful reproduction without further detail.
- **Defense is only evaluated on OpenVLA.** While the paper justifies this choice (OpenVLA showed weakest robustness against EDPA, Section 1), this limits the generality of the robustness claim. The conclusion that "the proposed defense can effectively mitigate these threats" (Section 7) is broader than the evidence (one model) directly supports.

### Trivial

None.

## Nice-to-Haves

- A cross-model transfer experiment (e.g., a patch generated for OpenVLA tested on OpenVLA-OFT) would clarify what "model-agnostic" means in practice regarding whether patches themselves transfer.
- A brief analysis of patch location sensitivity would strengthen the practical relevance claims.
- Qualitative examples of failure modes (e.g., does the robot freeze, move randomly, or confidently execute wrong actions?) would help distinguish between different types of safety implications.

## Removed Points

These points from the input review are flagged as removed and should be treated with caution:

1. **"Model-agnostic" framing is imprecise** — REMOVED. The paper explicitly defines "model-agnostic" via Table 1 and the surrounding text: it means no knowledge of the action space, robotic manipulator, or LVLM parameters is required. The abstract states "without requiring prior knowledge of the model architecture," which is consistent with this definition. The reviewer's interpretation as "cross-model transferability" is not the definition the paper uses and is not supported by the paper's explicit framing.

2. **Patch contrastive loss using InfoNCE within the same image is unusual** — REMOVED. This is a discussion-level observation, not a weakness. The loss is clearly defined in Eq. 2 and is a sensible design for maximizing patch-level embedding discrepancy between clean and perturbed versions of the same image.

3. **K=1 inner iteration is unusually low** — REMOVED. With 50,000 outer iterations and batch size 16, the patch is updated against ~800K samples. Single-step inner updates are standard in many adversarial training setups for universal patches over datasets.

4. **100.0 ± 0.0% failure rate is unusually clean** — REMOVED. This simply means the attack succeeded on all 50 executions × 10 tasks × 3 seeds. A sufficiently strong attack can achieve zero variance in failure rate.

5. **Patch placement sensitivity and qualitative failure modes** — REMOVED. These are beyond the stated scope or nice-to-have suggestions, not core weaknesses. They are included in Nice-to-Haves above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. In the rebuttal, explicitly state whether the evaluation patches for the defense were generated against the original encoder or the fine-tuned encoder. If only against the original, add a supplementary experiment generating patches against the fine-tuned encoder (even as a limited sensitivity analysis).
2. Clarify how UADA and UPA were adapted for LIBERO's action space and evaluation protocol.
3. Acknowledge the limitation that the defense was only evaluated on OpenVLA explicitly in the limitations section, and consider testing on at least one additional model in future work.
4. The "model-agnostic" terminology, while correctly defined, could be clarified with a brief disambiguation in the introduction to prevent misinterpretation.

---

**Calibration Anchors (all retrieval rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| gwZ90hFSL2.md | 1.00 | R1 | No | Not relevant (unrelated topic) |
| 5kMwiMnUip.md | 1.40 | R1 | No | Not relevant (LLM jailbreaking) |
| KBSHR4h8XV.md | 3.33 | R1 | No | VLA model paper with serious generalization issues; our paper stronger |
| zQXX3ZV2HE.md | 3.00 | R1 | No | Adversarial instance attacks; less relevant |
| YzFNJ571A7.md | 4.00 | R1 | Yes | DynVLA: MLLM attack with overclaimed transferability; our paper has clearer contribution |
| DYVSLfiyRN.md | 4.00 | R1 | No | VLLM transfer attack; less relevant |
| XFeiq8FMEF.md | 4.40 | R1,R2 | Yes | HardPatch: hard-label LVLM patch attack; our paper has cleaner evaluation |
| 7OO8tTOgh4.md | 5.25 | R1,R2 | Yes | MIE: VLM entropy-based attack; our paper has stronger threat model contribution |
| K7xpl3LZQp.md | 6.25 | R1,R2 | Yes | PLA: copyright tracking; comparable rigor, different contribution |
| tZozeR3VV7.md | 6.33 | R1,R2 | Yes | VLOOD: backdoor attack; comparable evaluation depth |
| wvFnqVVUhN.md | 6.25 | R1,R2 | Yes | Transfer Jailbreaks: comprehensive empirical study; stronger evaluation but different contribution type |
| plmBsXHxgR.md | 6.25 | R2 | Yes | Compositional VLM attack; similar vision-encoder-only access idea; our paper has stronger favorability on strengths |

**Bracket reasoning:** Round 1 bracketing placed the paper in the 5.5–7.5 range (above DynVLA 4.0, HardPatch 4.4, MIE 5.25; comparable to PLA 6.25, VLOOD 6.33, and Transfer Jailbreaks 6.25). Round 2 narrowing compared itemized favorability ratings: our paper's strengths (11.9–13.8) are consistently higher than those in the 6.25 anchors (typically 7–12), while our weaknesses (3.5–4.0) are less severe than those in the 6.25 anchors (some as low as -4.75 to 0.3). This places the paper at or slightly above the 6.25 anchor level, but the defense evaluation under-specification (the most impactful weakness) pulls it down from a higher score. Final score: 6.0.

**MY FINAL SCORE:** <score>6.0</score>
**MY FINAL DECISION:** <decision>Accept</decision>