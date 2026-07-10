## Summary

This paper introduces Automatic Complementary Separation Pruning (ACSP), a structured pruning method that (a) encodes each component's class-pair separability (via JM distance) into a graph space, (b) selects diverse, complementary components via k-Medoids clustering evaluated by the Mean Simplified Silhouette (MSS) index, and (c) automates the per-layer pruning extent using the Kneedle knee-finding algorithm. ACSP achieves competitive FLOP reductions (1.5–2.5×) across VGG, ResNet, DenseNet, and MobileNet on CIFAR-10/100 and ImageNet, often with minimal accuracy loss or small gains.

## Strengths

- **Principled formulation of complementary selection.** Encoding each component's separability across all class pairs into a graph space and then clustering to enforce diversity is a well-motivated, genuine conceptual contribution. The reasoning for why similar components are redundant even if individually strong (Section 3.3.2) is clearly grounded. *(Impact: +9.7)*

- **Fully automated pruning extent.** ACSP eliminates the need for user-specified pruning ratios via Kneedle-on-MSS, and this automation is cleanly integrated into the method rather than bolted on. The paper demonstrates it across multiple architectures. *(Impact: +5.9)*

- **Broad empirical coverage.** Evaluation spans three datasets (CIFAR-10/100, ImageNet) and four architecture families (VGG, ResNet, DenseNet, MobileNet), giving reasonable confidence that the method generalizes. *(Impact: +6.5)*

- **Inference latency reporting.** Table 2 reports actual wall-clock times (batch and single inference) rather than only FLOPs, which is good practice that many pruning papers skip. *(Impact: +6.7)*

## Weaknesses

### Fatal
None.

### Major

- **No ablation studies isolating any design choice.** The method makes several interdependent decisions—using k-Medoids (then discarding medoids for highest-weight components per cluster), using MSS over standard Silhouette, using a second-degree polynomial in Kneedle, using JM distance—but not a single one is experimentally validated. It is impossible to tell whether the graph-based complementary selection is driving the results, whether weight-based selection alone would suffice, whether a simpler clustering index would work as well, or whether the automated extent determination beats manual tuning at the same pruning rates. The paper claims JM, Hellinger, and Wasserstein were compared (line 127) and JM was best, but no such results appear in the experiments section, making the JM selection unverifiable. This is the paper's most significant gap. *(Impact: -9.8)*

### Minor

- **No variance or statistical significance reported.** Every accuracy number in Table 1 is a point estimate with no error bars. The pruning process involves random 25% data subsets, iterative per-layer decisions, and Kneedle sensitivity, yet no multiple-run statistics are provided. Small deltas (e.g., +0.09% for MobileNet-V2 on ImageNet) are uninterpretable without variance. Inference latencies in Table 2 report means over 100 runs but no standard deviation. *(Impact: -7.7)*

- **FLOPs-to-latency gap is large and unanalyzed.** The headline speed-ups are FLOP-based (2.25× for ResNet-50, 2.59× for VGG-16), but actual wall-clock improvements (Table 2) are far smaller (e.g., −8.07% single inference for ResNet-50, −6.32% batch). The paper acknowledges the gap (line 277: "hardware utilization is not perfectly linear with FLOP count") but does not investigate why the removed FLOPs do not translate to commensurate latency gains. This matters for the paper's stated focus on "inference-time efficiency." *(Impact: -6.0)*

- **Fine-tuning protocol differs from common practice and the potential advantage is unaddressed.** ACSP fine-tunes after each pruned layer (2–3 epochs on 25% data per layer), which for a deep network accumulates to substantial fine-tuning (e.g., ~60 epoch-equivalents on partial data for ResNet-56). Baselines in Table 1 were typically evaluated in their original papers with post-hoc fine-tuning. The paper does not discuss whether this per-layer protocol inflates ACSP's accuracy relative to baselines evaluated under different regimes. *(Impact: -0.9)*

### Trivial

- **Weakest result (DenseNet-40 on CIFAR-100, Table 1).** ACSP matches NS in accuracy drop (−0.36%) with a marginal speed-up advantage (1.91× vs. 1.89×), providing little evidence of improvement in this case. *(Impact: -4.2)*

## Nice-to-Haves

- The most impactful improvement would be a controlled ablation study: (i) ACSP with medoid selection instead of highest-weight-per-cluster; (ii) ACSP with standard Silhouette instead of MSS; (iii) ACSP with uniform random pruning at the same per-layer rate (controlling for Kneedle); (iv) ACSP with random component selection at the same rate. This would directly test whether the complementary selection mechanism adds value.
- Report total pruning wall-clock time for ImageNet-scale experiments (the O(N_i²) analysis in line 71 gives the per-layer cost but not the total).
- Include per-layer pruning statistics (how many components removed from each layer) to give insight into which layers the method prunes aggressively.
- Supply the promised comparison of JM, Hellinger, and Wasserstein metrics (if not in the now-removed appendix).

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **Table error "ACSP (Gao et al., 2023)" (line 193):** Removed as a parser/formatting artifact — the instructions state parser artifacts are not author errors.
- **"Single pass" claim vs. O(N_i²) cost:** The paper already discloses O(N_i²) cost (line 71) and notes it is negligible for N_i ≤ 256. "Single pass per layer" refers to not requiring iterative search or RL training, not literal algorithmic complexity. Removed as minor wording imprecision.
- **Graph space memory feasibility for large C:** The paper acknowledges this limitation in the conclusion (line 283). Removed as duplicating an already-stated limitation.
- **Missing comparison with auto-pruning baselines configured for automatic extent:** The paper compares against AMC and MetaPruning (both auto-pruning methods) in Table 1. Requesting reconfiguration of these baselines is scope creep.
- **Section-by-section notes on computational overhead:** The paper provides O(N_i²) analysis with wall-clock cost; further quantification is a nice-to-have, not a core weakness.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the conceptual contribution (complementary selection via graph-space clustering) but do not surface any unstated insight about the method or problem.

## Suggestions

- Add a controlled ablation study (as described under Nice-to-Haves) as the single highest-priority revision. This is necessary to close the evidential gap on why ACSP works.
- Report accuracy results as means and standard deviations over at least 3 runs with different random seeds and data subsets.
- Add a discussion of the FLOPs-to-latency gap, including profiling analysis of which operations dominate wall-clock time in the pruned models.

## Score and Decision

The paper's core idea—complementary selection via graph-space separability encoding with automated extent determination—is genuinely novel and well-motivated, and the empirical evaluation is broad in scope. However, the complete absence of ablation studies prevents the reader from attributing the results to any specific component of the method, and the lack of variance reporting undermines confidence in small accuracy deltas. The paper is at the borderline: its contribution is real but not yet fully substantiated. A revised version with careful ablations could be a solid accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>