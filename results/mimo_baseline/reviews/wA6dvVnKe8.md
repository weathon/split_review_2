## Summary
This paper proposes EDPA, a model-agnostic adversarial patch attack that targets the embedding/latent representation space of Vision-Language-Action (VLA) models by maximizing the discrepancy between clean and perturbed visual embeddings and disrupting visual-language semantic alignment. The paper also proposes an adversarial fine-tuning defense for the visual encoder. Evaluations on the LIBERO benchmark across OpenVLA, OpenVLA-OFT, and π₀ demonstrate that EDPA substantially increases task failure rates, while the defense meaningfully reduces degradation.

## Strengths
- **Well-motivated model-agnostic attack design**: By targeting the embedding space rather than the action space, EDPA relaxes the stringent requirements of prior work (UADA requires action space knowledge, UPA requires robot manipulator knowledge). Table 1 clearly summarizes the reduced access requirements, and Table 1/Figure 1 show this is a genuine practical advantage for transferring attacks across VLA architectures.
- **Comprehensive multi-model evaluation**: The paper evaluates across three SOTA VLA models (OpenVLA, OpenVLA-OFT, π₀) and four LIBERO task suites, providing a broad empirical picture of VLA vulnerability. The consistent effectiveness of EDPA across all models (Tables 2 and 3) convincingly demonstrates the threat.
- **Interesting empirical observations in Section 5**: The discussion about adversarial patches resembling robotic arms and the hypothesis about visual encoder overfitting to limited training viewpoints provides genuine insight into why VLA models may be particularly susceptible to such attacks.

## Weaknesses
### Fatal
None.

### Major
- **Defense evaluated only on OpenVLA**: The adversarial fine-tuning defense is only tested on OpenVLA (Table 2), the model showing the weakest robustness. OpenVLA-OFT and π₀ are never evaluated with the defense, making it unclear whether the defense generalizes to more robust or architecturally different models. The justification that "OpenVLA exhibited the weakest robustness" is not sufficient—defense generalization to stronger models is precisely what needs to be demonstrated.
- **Defense has limited effectiveness on harder tasks**: Even on OpenVLA, the defense shows diminishing returns on harder task suites. For the Long suite, the defense reduces EDPA failure rate only from 100% to 91.2%, and for Goal from 100% to 73.9%. These residual failure rates remain very high, raising questions about the practical utility of the defense.

### Minor
- **No cross-model patch transferability analysis**: The paper generates patches per model but never evaluates whether a patch crafted for one VLA transfers effectively to another. Given the model-agnostic claim, demonstrating cross-model transferability would significantly strengthen the paper.
- **No ablation of loss components**: While both loss objectives are described, there is no ablation showing the individual contribution of the patch contrastive loss versus the image-instruction alignment loss to overall attack effectiveness (presumably deferred to the appendix, which is stripped).
- **Missing defense for multi-camera models**: The multi-camera evaluation (Section 4.3) only evaluates attacks. Given that OpenVLA-OFT and π₀ showed greater robustness, understanding whether the defense further reduces vulnerability in multi-camera settings would be valuable.

### Trivial
None.

## Nice-to-Haves
- Evaluate the adversarial fine-tuning defense on OpenVLA-OFT and/or π₀ to demonstrate defense generalizability.
- Include a cross-model transferability experiment (patch crafted on OpenVLA, evaluated on OpenVLA-OFT and π₀).
- Discuss computational costs of EDPA patch generation and adversarial fine-tuning relative to the baselines.

## Novel Insights
The hypothesis that adversarial patches resemble robotic arms because VLA visual encoders overfit to the near-ubiquitous presence of the robot arm in training frames (due to limited dataset scale and fixed camera viewpoints) is a genuinely novel and plausible explanation. This insight connects data diversity in pretraining to adversarial vulnerability, and the differential robustness of OpenVLA (single camera, less diverse data) versus π₀ (wrist camera data from pretraining, more diverse) provides supporting evidence.

## Suggestions
- Extend defense evaluation to OpenVLA-OFT and π₀, even if only on a subset of task suites, to demonstrate generalizability.
- Add an ablation study isolating the contribution of each loss term (patch contrastive vs. alignment) to attack effectiveness.
- Discuss the practical deployment considerations: e.g., can the defense fine-tuned encoder be further updated with new attack patches in an iterative manner?

## Score and Decision
The paper addresses an important and underexplored problem with a well-motivated approach and solid multi-model empirical evaluation. The model-agnostic attack design is a genuine contribution that lowers the barrier for adversarial attacks on VLA models. However, the defense evaluation is limited to a single (weakest) model and shows diminishing returns on harder tasks, which weakens the defense contribution. The overall work is a meaningful contribution to the nascent field of VLA robustness, with the attack portion being strong and the defense portion being adequate but incomplete.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>