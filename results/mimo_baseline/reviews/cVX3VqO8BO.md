## Summary
UniHM introduces a unified framework for language-conditioned dexterous hand manipulation that generates sequential manipulation trajectories (rather than just static grasp poses). It combines a morphology-agnostic VQ-VAE codebook that maps heterogeneous hand kinematics to a shared discrete space, a VLM trained on human-object interaction data with progressive masked training, and an energy-based physics refinement module enforcing contact, generative, and temporal priors.

## Strengths
- **Well-motivated problem and clear positioning.** The paper convincingly argues that prior work is limited to static grasp poses or lacks open-vocabulary language guidance, and the progression from this gap to the proposed solution is logical and well-supported by the literature review.
- **Unified cross-morphology tokenizer design.** The staged knowledge distillation approach for aligning heterogeneous hand encoders to a shared codebook (Eq. 3) elegantly avoids the gradient discontinuity of direct non-differentiable token alignment, and enables direct token reuse across five different robot hands (Shadow, Allegro, SVH, Leap, Panda).
- **Strong empirical results with comprehensive evaluation.** Tables 1 and 2 show consistent improvements over four baselines (TM2T, MDM, FlowMDM, MotionGPT3) across MPJPE, FOL, FPL, and FID on both DexYCB and OakInk for seen and unseen splits. Real-world experiments (Table 3) demonstrate 60%+ grasp success on seen objects and meaningful improvements on unseen scenarios.
- **Well-structured ablation study.** Table 4 cleanly isolates the contribution of each component: removing depth input, masked training, or physical refinement each degrades performance, with physical refinement providing consistent improvements across metrics.

## Weaknesses
### Fatal
None.

### Major
- **Diversity-accuracy trade-off poorly addressed on DexYCB.** On DexYCB, UniHM achieves diversity of 39.62 (seen) and 42.70 (unseen), significantly lower than the GT diversity of 125.53 and much worse than MotionGPT3 (72.51 and 75.84). This suggests potential mode collapse or limited expressiveness in the generated sequences, yet the paper does not discuss this trade-off at all. On OakInk, UniHM's diversity is closest to GT, making this dataset-dependent issue more puzzling.
- **Real-world evaluation lacks protocol details.** Table 3 reports success rates across four task categories but provides no information about the number of trials per task, how many distinct objects were tested, the evaluation criteria for "success," or confidence intervals. Without these details, the strong real-world claims (e.g., 65% vs. 30% grab success) cannot be properly assessed.
- **Baseline comparisons are against human motion generators, not dexterous manipulation methods.** The four baselines (TM2T, MDM, FlowMDM, MotionGPT3) are general human motion generation models not designed for dexterous hand manipulation. While the paper justifies this by noting the lack of prior sequential dexterous manipulation methods, comparing against at least one manipulation-specific baseline (e.g., DexMV, which is discussed in the related work) would significantly strengthen the claims.

### Minor
- **Overly strong language.** Phrases like "these results unequivocally affirm our method as cutting-edge" (Section 4.3) and "state-of-the-art" throughout the paper are not supported by the diversity performance issues noted above. More measured claims would be appropriate.
- **CLIPort dependency during inference is not deeply analyzed.** The CLIPort trajectory estimation module is critical at inference time but the paper does not evaluate its failure modes or how trajectory estimation errors propagate to manipulation quality.

### Trivial
None.

## Nice-to-Haves
- A comparison of UniHM's diversity vs. accuracy trade-off with an explicit Pareto analysis across methods.
- A table or visualization showing how the unified codebook tokens are shared/distributed across different hand morphologies.
- Error analysis on the real-world failure cases.

## Novel Insights
The cross-morphology distillation approach (aligning new hand encoders to a reference encoder before VQ-VAE fine-tuning) is a genuinely practical contribution that enables scalable addition of new hand morphologies without retraining the entire codebook. The paper also makes a valuable observation that learning from human-object interaction video rather than teleoperation data can transfer effectively to robotic dexterous hands, which has important implications for reducing data collection costs.

## Suggestions
- Add a discussion of the diversity metric discrepancy on DexYCB, including potential causes and whether it reflects a limitation of the tokenizer or the VLM.
- Report the number of real-world trials per task and provide confidence intervals or standard errors for the success rates.
- Include at least one dexterous manipulation-specific baseline to strengthen the comparison.
- Provide failure case analysis in the real-world experiments to identify systematic limitations.

## Score and Decision
The paper makes solid contributions with the unified cross-morphology tokenizer, physics-guided refinement, and a complete pipeline from language instruction to executable manipulation. The empirical results are strong on standard metrics, but the unaddressed diversity regression on DexYCB and insufficient real-world evaluation details prevent a stronger endorsement.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept