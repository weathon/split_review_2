Now I have my calibration anchors. Let me compile the final review.

**Round 1 bracket**: After reading the paper and calibrating against similar papers, I estimate the score is between 4.5 and 5.5.

**Anchor comparison**:
1. **HardPatch** (4.40, Reject) — adversarial patches for LVLMs, patch-based attack but in hard-label setting; evaluation limited to standard LVLM tasks, not embodied robotics. Our paper has a clearer contribution (reduced-access attack for VLA models) and evaluates across 3 models including an architecturally different one.
2. **MIE Attack** (5.25, Reject) — white-box untargeted attack on VLMs via entropy maximization; reviewers found contribution unclear relative to prior work. Our paper has a clearer novelty gap (attack and defense for VLA models specifically, with reduced access requirements).
3. **C-PGC** (5.00, Reject) — universal perturbations for VLPs; reviewers raised significant concerns about unclear contribution. Our paper is stronger on contribution clarity but weaker on defense evaluation.
4. **PADetBench** (4.75, Reject) — benchmarking physical attacks against object detection; different task but similar evaluation scope. Our paper has comparable evaluation depth on the attack side.
5. **OT-Patch** (6.20, Accept) — adversarial patches for classification with transferability claims and physical experiments. Stronger evaluation than our paper (includes physical-world experiments).

Our paper sits between HardPatch (4.40) and OT-Patch (6.20). The attack contribution is solid and better-evaluated than comparable attack papers in this band, but the defense evaluation is clearly weak. Score 5.0.

## Final Review

## Summary

This paper proposes EDPA (Embedding Disruption Patch Attack), an adversarial patch attack for Vision-Language-Action (VLA) models that requires only access to the visual encoder parameters — not the full LVLM backbone or knowledge of the action space or robot hardware. The attack jointly maximizes disruption of patch-level visual embeddings and visual-language alignment. The paper also proposes an adversarial fine-tuning defense for the visual encoder. Experiments on the LIBERO benchmark across three VLA models (OpenVLA, OpenVLA-OFT, π₀) show EDPA substantially increases failure rates, and the defense partially mitigates this on OpenVLA.

## Strengths

1. **Reduced access requirements relative to prior work.** Table 1 and Figure 1 clearly delineate what EDPA needs (only the encoder's parameters) versus what UADA and UPA need (action space knowledge, robot manipulator knowledge, and/or full LVLM parameters). This is a concrete and useful reduction in the attack's dependency on the victim system.

2. **Evaluation across three VLA models for the attack.** The attack is tested on OpenVLA, OpenVLA-OFT, and π₀ (Tables 2 and 3). The results for π₀ are particularly informative because π₀ is architecturally different from the OpenVLA family (a flow-matching model rather than an autoregressive one), giving genuine breadth to the evaluation.

3. **Honest limitation discussion.** Section 6 acknowledges the multi-camera alignment problem and the occlusion issue, which are genuine practical challenges that the paper does not attempt to paper over.

## Weaknesses

### Fatal
None.

### Major

1. **Defense evaluated only against single-step (K=1) attacks.** Algorithm 1 and Section 4.1 set the number of inner attack iterations K=1 during adversarial fine-tuning. This means the adversarial patches used during training are generated with a single FGSM-style gradient step. The adversarial training literature has long recognized that training against weak attacks can produce a false sense of robustness (gradient masking). The paper provides **no evaluation against EDPA with larger K** (e.g., K=10, K=50). Without this, we cannot distinguish genuine robustness from overfitting to the single-step attack used during training. Since the defense is presented as one of the paper's two main contributions, this gap significantly weakens the defense claim.

2. **Defense evaluated on only one model (OpenVLA).** The paper states OpenVLA was chosen "as the primary model for defense evaluation" because it exhibited the weakest robustness. However, the defense involves fine-tuning the visual encoder, and different VLA models use different encoders (e.g., π₀ uses a different visual backbone). Whether the approach generalizes to other encoders is entirely untested. The defense is presented as a general strategy ("adversarial fine-tuning scheme for the visual encoder"), but the single-model evaluation is insufficient to support that generality claim.

### Minor

1. **Defense effectiveness varies dramatically across task suites without analysis.** From Table 2, the reduction in failure rate from EDPA after defense is 60.6 pp on Spatial, 41.4 pp on Object, 26.1 pp on Goal, and only 8.8 pp on Long. The Long suite has a clean failure rate of 48.1% (much higher than other suites), meaning Long tasks are intrinsically harder and the defense is least effective precisely where it is most needed. The paper does not discuss this pattern or attempt to explain it.

2. **Physical-world evaluation is absent.** All experiments are in simulation where patches are digitally composited onto images. The gap between simulated patches (perfect overlay, no lighting variation, no perspective distortion) and physical patches (printed stickers with shading, parallax, and deformation) is substantial. While the paper does not claim to have performed physical experiments, the practical relevance claims ("directly placeable within the camera's view") would be strengthened by acknowledging this gap explicitly or including a real-robot pilot study.

### Trivial
None.

## Nice-to-Haves

- Evaluate the defense against stronger EDPA variants (K=10, K=50) to bound the scope of robustness.
- Test the defense on at least one additional VLA model (e.g., π₀ or OpenVLA-OFT).
- Analyze why the defense is far less effective on the Long task suite.
- Ablate the two loss components (α₁=0 and α₁=1) to clarify each objective's individual contribution (if not already in the appendix).
- Compare EDPA with a simple baseline like a uniform gray patch for OpenVLA-OFT and π₀.

## Removed Points

These points from the input are removed with justification:

1. **Criticism of "model-agnostic" framing as overstated.** The paper defines what EDPA requires (encoder parameters) and what it does not require (architecture knowledge, action space, manipulator knowledge). It never claims zero-shot cross-model transfer. The term "model-agnostic" is used to mean "applicable across different VLA models without model-specific architectural knowledge," which is a defensible usage given that the attack is demonstrated on three different model families. *Removed because the criticism misreads the paper's actual claim.*

2. **Question about InfoNCE vs. simpler alternatives (e.g., MSE).** This is a design choice; the paper is not required to justify every architectural decision. *Removed as a scope-creep design critique, not a genuine weakness.*

3. **Random noise baseline clipping details.** Minor implementation detail that does not affect the validity of the results. *Removed as a formatting/presentation nitpick.*

4. **Multi-camera patch practicality critique.** The paper already acknowledges this limitation in Section 6. *Removed because the paper addresses it.*

5. **"Overfitting" hypothesis as speculative.** The paper explicitly presents this as a hypothesis ("we propose a hypothesis"), so criticizing it as speculative penalizes the paper for being honest about its interpretive framing. *Removed as a strawman.*

6. **Missing ablation of α₁ (loss components).** The paper references Appendix C for hyperparameter sensitivity; the appendix is stripped by the parser and cannot be verified. Per instructions, "REMOVE weaknesses about missing appendix." *Removed.*

7. **Section-by-section notes on UADA/UPA framing difference (encoder vs. all parameters).** Debatable opinion about practical difficulty, not a factual error. *Removed.*

## Novel Insights

None beyond the paper's own contributions. The reviews surface clear gaps in the defense evaluation (K=1, single model, task-dependent variation) that are consistent with the paper as written and actionable for improvement.

## Suggestions

1. **Reframe the defense as a preliminary exploration.** The attack contribution (EDPA) is the stronger, better-evaluated part of the paper. The defense would benefit from being presented as an initial attempt with acknowledged limitations rather than as a fully validated complementary contribution.
2. **Evaluate the defense against stronger attacks (K > 1).** This is the single most impactful addition for strengthening the defense claim.
3. **Either evaluate the defense on another model or explicitly caveat the single-model scope.** If generalization to other encoders has not been tested, say so directly.
4. **Analyze the task-dependent variation in defense effectiveness.** Understanding why the defense works well on Spatial but poorly on Long would sharpen the contribution.

## Score and Decision

**Calibration anchors used**:
| Anchor | Score | Comparison |
|--------|-------|------------|
| HardPatch (LVLM adversarial patches) | 4.40 (Reject) | Our attack evaluation is broader (3 models); defense evaluation similar limitations |
| MIE Attack (VLM adversarial) | 5.25 (Reject) | Our paper has clearer contribution; comparable evaluation depth on attack |
| C-PGC (VLP universal perturbations) | 5.00 (Reject) | Our paper stronger on contribution clarity but weaker on defense |
| PADetBench (physical attack benchmark) | 4.75 (Reject) | Different task, comparable evaluation scope |
| OT-Patch (adversarial patch, classification) | 6.20 (Accept) | Stronger evaluation (includes physical experiments) |

**Round 1 bracket**: 4.5–5.5.

The attack contribution is solid — reduced access requirements are genuinely useful, and evaluation across three models (including architecturally different π₀) provides reasonable evidence of effectiveness. The defense contribution, however, is substantially under-evaluated (single model, single-step attacks only, no analysis of large task-dependent variation). The paper presents attack and defense as co-equal contributions, but the evidence for the defense is considerably weaker.

Score: **5.0** — a borderline paper. The attack is publishable, but the defense claims are not fully supported. A revision that reframes the defense as preliminary (or strengthens its evaluation) could move this into acceptance territory.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>