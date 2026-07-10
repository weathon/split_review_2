## Summary

This paper proposes TrojanTO, the first action-level backdoor attack against Trajectory Optimization (TO) models in offline RL. It operates as a post-training attack — modifying a pretrained TO model's parameters with a small set of additional trajectories — and comprises three components: trajectory filtering (to maintain benign performance), batch poisoning (for trigger consistency), and alternating training (to co-optimize the trigger and model parameters). The paper also contributes a systematic empirical analysis (Section 4) of what drives backdoor success in TO models, establishing that target action selection and trigger design are critical while reward manipulation is ineffective.

## Strengths

- **Systematic factor analysis (Section 4).** The paper correctly identifies that existing RL backdoor attacks assume reward-based training and training-time access — neither applies to TO models. The empirical study of target action selection (boundary actions give near-perfect ASR while interior actions yield much lower ASR, Table 1) and trigger design (dimension choice can swing ASR from 0.915 to 0.000, Table 2) provides genuinely useful knowledge for the community regardless of TrojanTO's success as a specific method. **[impact=+9.95]**

- **Cross-architecture evaluation.** TrojanTO is evaluated across three TO architectures (DT, GDT, DC) and six D4RL environments, totaling 18 task-model combinations with results averaged over three random seeds and three target actions. The attack achieves a higher average CP (0.701) than both Baffle (0.342) and IMC (0.551). This breadth demonstrates the attack's general applicability. **[impact=+9.84]**

- **Low data requirement.** The attack operates at a reported 0.3% poisoning rate compared to Baffle's 10%, representing a meaningful efficiency advantage in terms of the amount of data the adversary needs to handle. **[impact=+1.71]**

## Weaknesses

### Fatal

None.

### Major

- **Poisoning rate comparison between TrojanTO and Baffle is presented without clarifying that the quantities differ.** The paper repeatedly contrasts TrojanTO's "0.3% poisoning rate" with Baffle's "10%" (Sections 1, 6.1) as if they measure the same thing. They do not: Baffle poisons 10% of the pre-training dataset before model training, while TrojanTO uses 0.3% of some trajectory set for post-training fine-tuning. The denominator for TrojanTO's 0.3% is never specified (0.3% of what reference set?). This is not a fatal flaw — comparing across attack paradigms is standard in security papers — but the framing oversimplifies the comparison and the missing denominator makes the claimed efficiency advantage hard to interpret precisely. The paper should specify the reference set and avoid presenting the two percentages as directly equivalent.

- **IMC baseline adaptation not described.** IMC (Pang et al., 2020) was originally designed for image classifiers. The paper uses it as a baseline for TO models but does not describe how it was adapted — what loss function, architecture modifications, or hyperparameters were used. Without this information, the reader cannot assess implementation fairness, especially since IMC achieves competitive CP in several settings (DC-Ant CP=0.752 vs TrojanTO 0.559, DC-Pen 0.655 vs 0.477, DT-Kit 0.681 vs 0.614). This is a reproducibility concern that the authors should address.

### Minor

- **Key experimental parameter ε for ASR not stated in the main paper.** The ASR definition (Eq. 2) depends on a threshold ε that determines whether an output action is "close enough" to the target action. The numerical value of ε is never provided in the main extracted text — it appears only as a variable. Without knowing ε, the reader cannot interpret whether the reported ASR values reflect tight or loose tolerance. The value should be stated in the main paper.

- **Threat model does not specify the trajectory data source.** The paper states (Section 3.3) that the adversary operates "without access to the original training dataset" and uses "a minimal set of poisoned trajectories (e.g., 0.3%)", but does not explain where the initial set of N trajectories (Section 5.1) comes from. Different sources (environment rollouts, a subset of the original data, third-party data) imply different adversary capabilities. This should be clarified.

### Trivial

None.

## Nice-to-Haves

- The alternating training component is adapted from IMC (Pang et al., 2020). The paper cites this transparently, but a sentence acknowledging the extent of reuse would be helpful.
- The trajectory filtering heuristic ("longer trajectories are more representative of successful behavior") could benefit from brief empirical validation.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- **"The alternating training component is directly adapted from IMC, reducing novelty"** — The paper transparently cites IMC as inspiration. Building on prior optimization techniques is standard; the paper does not claim this component as wholly novel. Removed.
- **"Selective reporting: IMC wins in several settings"** — The critic's table included GDT-Hopp as a "reversal" when TrojanTO actually won (0.503 vs 0.314). The core observation that IMC wins in a few settings (DC-Ant, DC-Pen, DT-Kit) has some merit but the overall narrative (TrojanTO wins on average and in most settings) is factually correct. The paper could mention these cases but the omission is not a major flaw. Demoted from kept weaknesses.
- **"Model sizes not reported"** — Minor; likely in the stripped appendix. Removed.
- **"Trajectory filtering heuristic is questionable"** — The ablation shows filtering improves BTP (0.914 vs 0.850 w/o TF), providing empirical justification. Removed.
- **"Ablation on DC: BP causes 62% ASR drop"** — The critic used GDT's full ASR (0.814) with DC's w/o BP value (0.312), which is factually wrong per Table 5: DC ASR drops from 0.631 to 0.312 (~50%), not 62%. Removed.
- **"Defense section too brief"** — Standard formatting; full details cited in the appendix. Removed.
- **"ASR averaged across target types includes trivial boundary cases"** — Table 1 reports per-type breakdowns; the reporting is transparent. Removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify the missing experimental parameters.** State the ε threshold value for ASR (Eq. 2) and the trajectory filtering length threshold (Section 5.1) numerically in the main paper. Readers should not need to consult the appendix for these core evaluation parameters.

2. **Clarify the poisoning rate.** State explicitly: "0.3% of what?" (e.g., "0.3% of the trajectories in the training dataset," or "0.3% of the trajectories we collected by rolling out the pretrained model"). This makes the claimed efficiency advantage interpretable.

3. **Document the IMC adaptation.** Provide the loss function, architecture details, and hyperparameters used to adapt IMC from image classifiers to TO models.

4. **Reframe the Baffle comparison.** Acknowledge that TrojanTO and Baffle operate under different attack paradigms (post-training model modification vs. pre-training data poisoning) and that the "poisoning rate" figures refer to different quantities. The comparison is still informative but should not be presented as apples-to-apples.

5. **Clarify the data source for the N trajectories.** Explain where the adversary obtains the trajectories used in Section 5.1, and how this relates to the claim of operating "without access to the original training dataset."

---

**Anchor papers used for score calibration (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| .../em0gAL8fbK.md (Temporal Logic Backdoor) | 4.00 | R1 | Yes | Same subfield (offline RL backdoor). Our paper has stronger factor analysis (+9.95 vs +3.88) and broader evaluation. That paper's weaknesses were more fundamental (over-assumed capabilities -9.85, high poisoning -9.51). |
| .../rp5vfyp5Np.md (BATTLE) | 4.25 | R1 | Yes | Behavior-oriented attacks; different setting. Our paper has stronger empirical breadth. |
| .../AKAlVyunxA.md (SHINE) | 5.75 | R1 | Yes | DRL backdoor defense. Stronger theoretical framing but presentation issues (-9.96). Our paper's strengths (+9.95, +9.84) are comparable but lacks formal theory. |
| .../HZnnHDrBXD.md (Tree-based Attack) | 5.75 | R1 | Yes | Continuous RL attacks with strong theory (+9.95) but limited environments (-9.74). Our paper has stronger empirical breadth but no theoretical analysis. |
| .../UhW2wA1pRV.md (Robust DRL) | 5.50 | R2 | No | Behavior manipulation defense; comparable score band but different focus. |
| .../sRop0N5NYV.md (Randomized Smoothing) | 5.00 | R2 | No | DRL robustness; different subarea. |
| .../vRyp2dhEQp.md (Efficient Backdoor) | 5.75 | R2 | No | Backdoor in constrained data scenarios; comparable quality. |
| .../nZP10evtkV.md (Optimal Transport Patch) | 6.20 | R2 | No | Adversarial patches; higher score but computer vision, not RL. |

**Round-1 bracket:** [4.0, 6.0] — the paper's topic (backdoor attack on offline RL/TO models) aligns with the 4.00 anchor, but its stronger empirical contributions push it above that level. The 5.75 anchors have stronger theoretical components that this paper lacks.

**Round-2 narrowing:** [5.0, 6.0] — comparison with 5.50-5.75 anchors confirms the paper's empirical breadth is stronger than the ~5.0-5.5 papers, but the lack of theoretical analysis and the presentation issues around the Baffle comparison keep it below 6.0.

**Final score placement:** The paper shares the strong empirical evaluation of 5.75-level papers (comparable breadth to SHINE and better breadth than the Tree-based attack) but lacks theoretical guarantees that lifted those papers. Its Baffle comparison framing is a presentation weakness (-9.95 impact) but does not invalidate the core contribution. The factor analysis (+9.95) is a genuine novelty not present in any anchor. Score **5.5** — borderline, leaning toward weak accept if the authors address the major and minor weaknesses in a rebuttal.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>