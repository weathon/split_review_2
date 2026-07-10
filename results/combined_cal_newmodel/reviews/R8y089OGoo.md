Here is the final consolidated review.

---

## Summary

This paper proposes DIPOLE (Dichotomous diffusion Policy improvement), a novel RL algorithm for training diffusion/flow-matching policies. The key idea is to replace the unstable exponential weighting term in KL-regularized weighted regression with a bounded sigmoid weight, then decompose the optimal policy into a pair of dichotomous policies (π⁺ for reward maximization, π⁻ for reward minimization) whose scores are linearly combined at inference time — a form isomorphic to classifier-free guidance. The method is evaluated on 39 tasks across ExORL and OGBench (offline and offline-to-online), plus a 1B-parameter VLA driving model on NAVSIM.

## Strengths

- **Clean theoretical derivation (Sections 3.1–3.2).** The chain from the greedified KL-regularized objective (Eq. 5) → closed-form solution (Theorem 1, Eq. 6) → sigmoid-based decomposition (Eq. 7–8) → score combination (Eq. 10) is mathematically sound and clearly presented. The observation that the final form is isomorphic to classifier-free guidance is genuinely insightful, not tacked on.

- **Concrete practical benefit of sigmoid weighting.** Replacing the unbounded exp(βG) weight with σ(βG) ∈ [0,1] directly eliminates the loss-explosion failure mode described in Section 3.1. The sigmoid is the right choice because it is both bounded and smooth, and the paper correctly identifies this as the central mechanism enabling stable training.

- **Broad experimental scope.** The paper evaluates on 39 tasks across ExORL and OGBench (Tables 1–2), plus offline-to-online (Table 3), plus a 1B-parameter VLA model on NAVSIM (Table 4). Demonstrating effectiveness at two very different scales (standard RL benchmarks and real-world autonomous driving) is uncommon and strengthens the contribution.

- **Honest reporting.** DIPOLE does not win every cell. On OGBench (Table 2), FQL is competitive on antsoccer and cube-single. On offline-to-online (Table 3), FQL ties or beats DIPOLE on cube-double and scene. The paper does not cherry-pick favorable results.

## Weaknesses

### Fatal

None.

### Major

- **Missing DPPO navtrain baseline in the NAVSIM experiment (Table 4).** DPPO is only reported on the navtest split (89.0 PDMS), while DIPOLE is reported on both navtrain (89.7) and navtest (94.8). Without DPPO results on navtrain, the reader cannot fully isolate whether DIPOLE's advantage over DPPO is consistent across splits. The comparison DIPOLE navtest (94.8) vs DPPO navtest (89.0) is a valid same-split comparison that strongly favors DIPOLE, but the 2×2 table is incomplete. This is the single most significant evidential gap in the paper and should be addressed.

### Minor

- **The stability claim lacks empirical substantiation.** The paper's central argument that DIPOLE resolves the "loss explosion" problem of exp-weighted regression rests entirely on the mathematical form (sigmoid boundedness). While this theoretical argument is valid, no training curves or loss trajectories are shown that directly compare DIPOLE's sigmoid-weighted loss against exp-weighted regression loss over training steps. Such a plot on a representative task would visually substantiate the stability claim that currently rests on algebra alone.

- **Computational cost of dual diffusion models is not quantified.** The paper criticizes gradient-through-time methods as "extremely costly" and PPO-based methods as having "prolonged training," but does not report training time, FLOPs, or parameter count overhead of its own dual-model approach relative to single-model baselines like FQL. For the VLA experiment, LoRA adapters on a shared backbone mitigate this concern, but for the standard RL experiments the text says "two diffusion models" without quantifying the overhead. A wall-clock time comparison with FQL or IFQL on a representative task would clarify the practical trade-off.

- **The claim about π⁻ is slightly overstated.** The paper states (line 105) that π⁻ ∝ μ·(1−σ(βG)) "focuses on reward minimization." More precisely, this policy assigns higher weight to low-G actions, preserving density in low-return regions, but it does not explicitly minimize reward. A more accurate phrasing would be that it "favors low-return regions" or "preserves density in low-return regions."

### Trivial

- **Notation inconsistency.** The score combination formula in the implementation text (line 115) uses `(1 + w)ε⁺ − wε⁻` with lowercase `w`, while the derivation uses ω (omega). This is a typesetting inconsistency.

## Nice-to-Haves

- **Ablation of the greediness factor ω.** A sweep showing performance at ω = 0, 0.5, 1.0, 2.0, larger would demonstrate the claim of "flexible control" and reveal whether performance plateaus or degrades at high ω values. The paper refers to Appendix D.4 for ablations, but that section is stripped by the parser.

- **Clarification of the navtest/navtrain distinction.** The largest empirical result (94.8 PDMS) comes from fine-tuning on the test split. The paper acknowledges this ("variant trained on the test split without using ground-truth") but additional discussion of what navtest data contains and why it enables such dramatically better results than navtrain would be helpful.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Eq. (5) is structurally different, not just greedier" (from Harsh Critic Critical Issue 1):** The paper is fully transparent about Eq. (5), explicitly stating it "regularizes policy π with a greedified, value-aware reference policy weighted by σ(βG)/Z." The term "greedified" reasonably describes the modification. This observation is correct but the paper does not hide it, so it does not constitute a weakness.

- **"DPPO navtest vs DIPOLE navtest conflates two variables":** The reviewer claimed this comparison conflates algorithm and training split, but DPPO navtest vs DIPOLE navtest is actually a same-split comparison (both on navtest). The valid gap is only the missing DPPO navtrain baseline, which is already captured as a major weakness above.

- **"Standard deviation formatting issues":** Parser artifact, not a paper problem.

- **"Missing appendix content (ablation, proofs)":** The appendix is stripped by the parser; these exist in the original submission.

- **Generic strengths from input (e.g., "the paper addressed an important problem"):** These lack specific content and are not included.

## Novel Insights

None beyond the paper's own contributions. The key insight — that greedified KL-regularized RL yields a dichotomous policy decomposition that is isomorphic to classifier-free guidance — is the paper's own contribution and is already well-articulated.

## Suggestions

- Add DPPO results on the navtrain split to Table 4 for a complete 2×2 comparison.
- Include a training curves plot comparing DIPOLE's sigmoid-weighted loss against exp-weighted regression loss on a representative task to empirically substantiate the stability claim.
- Report wall-clock training time for DIPOLE vs. FQL on a representative task to clarify the computational trade-off of dual-model training.
- Reconcile the `w`/`ω` notation in Eq. (10) and its surrounding text.

---

**Calibration Anchors:** All anchors retrieved across rounds, with comparison:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ldVkAO09Km.md` (DAC) | 6.50 | R1+R2 | Yes | KL-constrained diffusion policy iteration; DIPOLE has cleaner theory, broader evaluation, less severe weaknesses |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/xCRr9DrolJ.md` (SRPO) | 6.25 | R1+R2 | Yes | Score-regularized policy optimization; DIPOLE has stronger contribution, fewer weaknesses |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/HA0oLUvuGI.md` (EFM/QIPO) | 6.25 | R1+R2 | Yes | Energy-weighted flow matching; DIPOLE has more distinct contribution, broader evaluation |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TeeyHEi25C.md` | 6.25 | R1 | No | Conditional diffusion for value estimation; less directly comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tGQirjzddO.md` | 6.33 | R2 | No | Latent diffusion for offline RL reasoning; different approach |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7BQkXXM8Fy.md` | 7.50 | R1 | Yes | Diffusion planner design analysis; DIPOLE has stronger theory but weaker empirical breadth (missing baseline) |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gEdg9JvO8X.md` (BDQL) | 3.67 | R1 | No | Behavior diffusion Q-learning without constraint; less strong methodologically |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/mc97L2QVIa.md` | 3.00 | R1 | No | Offline multi-agent with score decomposition; less related |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/cXxfVkRCHJ.md` | 3.00 | R1 | No | Offline-to-online with CFG; less directly comparable |

**Round 1 bracket:** 5.5–7.5 (bounded below by DAC/SRPO at ~6.25, above by the diffusion planner analysis at 7.50).

**Round 2 narrowing:** DIPOLE's strengths have higher favorability than DAC's (13.30 vs 12.64 for top strength) and lower-severity weaknesses (worst at -1.45 vs DAC's -3.22). Compared to the 7.50 anchor, DIPOLE has stronger theoretical novelty but a genuine missing-baseline gap. The paper is clearly above the 6.0–6.5 cluster and below the 7.50 level, placing it at **7.0**.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>