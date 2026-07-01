## Summary

UniHM proposes a unified framework for generating sequential dexterous hand manipulation sequences from open-vocabulary language instructions. The core technical contributions are: (1) a morphology-agnostic VQ-VAE codebook that maps heterogeneous hand kinematics into a shared discrete latent space, enabling cross-hand transfer; (2) a small VLM (Qwen3-0.6B) coupled with a decoupled CLIPort perception module for instruction-conditioned trajectory token generation; and (3) a physics-guided post-hoc optimization (frame-by-frame Gauss-Newton with contact, generative, and temporal priors) for physical feasibility. Experiments on DexYCB and OakInk datasets, plus real-world validation on a robotic hand, report improvements over adapted full-body motion baselines across both seen and unseen objects.

## Strengths

1. **Well-motivated problem and clean architecture.** The paper correctly identifies that existing language-conditioned dexterous hand methods generate static grasp poses rather than sequential manipulation — a genuine gap — and proposes a complete pipeline (tokenizer → VLM → physics refinement) to address it. The morphology-agnostic codebook design (Section 3.2) with staged knowledge distillation (Eq. 3) is technically sound and practically valuable.

2. **Real-world validation.** Table 3 reports success rates across four task types (Grab, Pick&Place, Pull&Push, Open&Close) on a physical robot, covering both seen and unseen objects. Real-robot evaluation is genuinely difficult and adds credibility that simulation-only results cannot provide.

3. **Practical decoupled perception-generation design.** Separating the CLIPort perception module (fine-tunable for distribution shift) from the frozen HOI generation VLM (Section 3.3) is a pragmatic choice that addresses data efficiency concerns — the VLM can focus on sequence generation while perception adapts to new scenes.

## Weaknesses

### Major

1. **Baseline adaptation is not explained.** The paper compares against TM2T, MDM, FlowMDM, and MotionGPT3 (Tables 1, 2) — all full-body human motion generation methods trained on datasets like HumanML3D or KIT-ML. Section 4.3 states only: *"Because prior action-generation baselines lack explicit physical-feasibility guarantees, we post-process their outputs with our physics-guided refinement to ensure a fair comparison."* It does not describe how these models were adapted to output dexterous hand joint trajectories. Were they retrained on DexYCB/OakInk hand data? Was their output space modified from SMPL body parameters to hand joint angles? Were only the hand subset of their outputs used? In Table 3, the baselines are labeled "MDM+Dex-Retargeting" and "MotionGPT3+Dex-Retargeting," hinting at an adaptation strategy not mentioned in the main quantitative evaluation. Without this information, the reader cannot assess whether UniHM's large margins reflect genuine superiority or simply the inappropriateness of the baselines for the task.

2. **No simulation-based physical feasibility metrics.** The paper lists physical feasibility as a core contribution and claims "simulation checks" (Section 4, Conclusion), but reports no quantitative simulation metrics — e.g., penetration depth, joint-limit violation counts, force-closure scores, or torque-limit analysis — that are standard in the dexterous grasping literature. The primary evaluation metrics (MPJPE, FOL, FPL, FID) measure proximity to ground-truth human hand poses (reconstruction accuracy), not physical feasibility per se. The only feasibility-directed metric is real-world success rate (Table 3), which conflates perception, planning, and execution. The ablation section (4.4) says *"We run a lightweight simulation-based optimization that adjusts poses, contacts, and timing to reduce collisions and slips, enforce joint and torque limits,"* but the output of this optimization is never quantified in a table.

### Minor

3. **Unseen-object split is ambiguous.** The paper uses an 80/20 train/test split on both DexYCB (10 object categories) and OakInk, labeling the 20% as "unseen objects and trajectories" (Section 4.1). DexYCB contains only 10 object categories; it is unclear whether "unseen" means novel object categories, novel instances of seen categories, or simply held-out sequences of the same objects with different trajectories. This ambiguity affects the strength of the generalization claims throughout the paper.

4. **No quantitative cross-morphology transfer results.** The unified codebook is a core contribution (Contribution bullet 2: *"direct token reuse and transfer across robotic and anthropomorphic hands"*), but the paper provides no quantitative evaluation of cross-hand transfer. How well does a token from MANO decode on the Shadow hand? How do success rates differ across the five robot hands? Without such evidence, the cross-hand claim is unsubstantiated.

5. **Language understanding is not evaluated.** The VLM (Qwen3-0.6B) is central to the open-vocabulary instruction claim, but no metric assesses whether the model correctly interprets diverse instructions. A basic classification accuracy on instruction types or a human evaluation of instruction-following would strengthen this claim.

6. **Real-world experiments lack trial counts and variance.** Table 3 reports success rates as single percentages without error bars or trial counts. The reliability of a 65% success rate from 20 trials vs. 200 trials differs materially.

### Trivial

None.

## Nice-to-Haves

- Hyperparameter disclosure for the VQ-VAE (codebook size K, commitment weight β) and optimization weights (λ_c, λ_vel, λ_acc, α, k) would aid reproducibility.
- Analysis of failure cases and/or language complexity handling by the 0.6B VLM would help assess whether the model generalizes linguistically or memorizes dataset-specific patterns.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **Table 1 standard deviations appear implausible (85.33 ± 341).** The criticism about SDs being 4× the mean is a parser artifact where decimal points were stripped from SD values in Table 1. This is confirmed by Table 4 (ablation on the same DexYCB dataset) which shows normal SDs (e.g., 85.47 ± 3.42). Removed per formatting-artifact rule.

2. **Missing comparison with dexterous static-grasp methods.** The reviewer asks for comparison with SemGrasp, AffordDexGrasp, DexGrasp Anything, etc. These methods produce static poses, not sequences; direct comparison on trajectory metrics is infeasible. The paper's Related Work clearly delineates this distinction. This is not a flaw in the evaluation; however, the paper could be improved by explicitly stating why such comparison is not possible.

3. **"Physics-guided" refinement is really geometry-guided.** The paper's refinement is described as using point-to-plane contact energy without dynamics or simulation rollouts. The paper acknowledges this limitation in the conclusion ("simplified energy terms for contact and friction"), and the term "physics-guided" is standard usage for such optimization. The criticism overstates the issue.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the core tension: the paper has a novel technical contribution and real-world validation, but its evaluation does not adequately support the headline claims because the baselines are not from the same subfield and physical feasibility is not directly measured.

## Suggestions

1. **Clarify baseline adaptation.** Describe how each full-body motion baseline was made to produce dexterous hand joint sequences (retraining, output-space adaptation, etc.). If retargeting was used for the main tables as it was for Table 3, state this explicitly.

2. **Report simulation feasibility metrics.** Include a table with penetration depth, joint-limit violation counts, and force-closure scores — even a single simulation-based table would sharply increase credibility.

3. **Disambiguate the unseen split.** Clarify whether the held-out 20% of DexYCB tests novel object categories or novel trajectories of seen categories. Reframe generalization claims accordingly.

4. **Add cross-hand transfer experiments.** Show quantitative results for token transfer across at least a subset of the five robot hands.

5. **Report trial counts and variance** for real-world experiments.

## Score and Decision

**Calibration details.** I retrieved anchor papers from the human-review corpus organized by score band and filtered by topical similarity (dexterous manipulation, VLM for robotics, hand-object interaction, language-conditioned motion generation). The round-1 bracket was [5.5, 6.5]. Anchors consulted:

| Anchor | Path | Avg Score | Round | Comparison |
|--------|------|-----------|-------|------------|
| HandsOnVLM | AJQuTFd9es.md | 6.33 | 1 | Hand-VLM prediction paper with missing evaluation details; similar task domain but weaker technical contribution than UniHM |
| HAMSTER | h7aQxzKbq6.md | 6.00 | 1 | Hierarchical VLA for manipulation, accepted despite limited 3D reasoning; comparable evaluation breadth to UniHM |
| RoboFlamingo | lFYj0oibGR.md | 6.50 | 1 | VLM fine-tuning for manipulation, accepted with clean simulation-only evaluation; UniHM has real-world validation but weaker evaluation rigor |
| LaMP | LYawG8YkPa.md | 6.00 | 2 | Language-motion pretraining, accepted with clean experiments across multiple tasks; weaker novelty than UniHM but stronger evaluation |
| "Bridging Gap" | 80faVLl6ji.md | 6.00 | 2 | Motion-semantics alignment, rejected due to clarity/positioning issues; less technically novel than UniHM |
| CrayonRobo | Aqfwhna1D7.md | 5.20 | 1 | Visual prompting for manipulation, rejected; UniHM is technically stronger |
| DTP | VaoeAi5CW8.md | 4.25 | 1 | Diffusion trajectory policy, rejected for missing baselines and weak novelty; UniHM is substantially stronger |

The round-1 bracket narrowed to 5.5–6.5. After comparing against the accepted papers in this range (HAMSTER 6.00, RoboFlamingo 6.50, LaMP 6.00), the final score is 6.0. UniHM's technical novelty and real-world validation are comparable to or stronger than these anchors, but the evaluation gaps — unexplained baseline adaptation and absent simulation feasibility metrics — are more significant than those of the accepted anchors. The paper needs to address these before acceptance.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Reject</decision>