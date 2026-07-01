## Summary

This paper proposes a self-supervised framework for learning the Minimum Action Distance (MAD) from state trajectories alone, without requiring reward signals or action labels. It introduces two algorithms—MadDist (direct distance regression) and TDMadDist (temporal-difference bootstrapping)—that use quasimetric distance functions to capture the inherent asymmetry of MAD. The paper also defines a simple yet effective quasimetric and contributes a benchmark suite of environments with known ground-truth MAD. Experiments across discrete/continuous, deterministic/stochastic, and noisy settings show that MadDist significantly outperforms existing methods (QRL, Hilbert) in representation quality and downstream planning success.

## Strengths

- **Well-motivated problem and clear identification of prior limitations.** The paper correctly identifies that existing MAD approximation methods rely on symmetric distance metrics, which cannot capture the asymmetry of MAD in environments with irreversible dynamics. The use of quasimetrics is a natural and important improvement.

- **Novel and principled learning objectives.** The MadDist loss is scale-invariant (dividing by the temporal gap), preventing long-horizon pairs from dominating the gradient. The inclusion of a contrastive term and upper-bound constraints is well justified. The TDMadDist variant introduces bootstrapping, which is a sensible extension.

- **Comprehensive and controlled evaluation.** The paper evaluates on a diverse suite of environments (grid worlds, mazes, stochastic/noisy variants) where ground-truth MAD is known, enabling precise quantitative assessment. Multiple metrics (Spearman, Pearson, CV) are used, and results are reported with error bars over multiple seeds.

- **Strong empirical results.** MadDist consistently achieves the highest correlation and lowest coefficient of variation across all environments, and attains near-perfect success rates in downstream planning tasks on OGBench PointMaze, decisively outperforming baselines.

- **Valuable benchmark contribution.** The suite of environments with known MAD provides a standardized testbed for future research on distance learning in MDPs.

## Weaknesses

### Fatal

None.

### Major

1. **Missing comparison with the most direct predecessor (Steccanella & Jonsson, 2022).** The paper discusses this method in related work but does not include it as a baseline. Since Steccanella & Jonsson (2022) uses the same symmetric-distance + trajectory-supervision paradigm, a direct comparison would isolate the benefit of the proposed scale-invariant loss and quasimetric. Without this, it is unclear how much of the improvement comes from the loss design versus the quasimetric.

2. **The simple quasimetric (d_simple) is claimed to outperform more elaborate quasimetrics, but this evidence is relegated to the appendix.** The main paper does not specify which quasimetric is used in the primary experiments, nor does it show a comparison among quasimetric choices. Given that the paper introduces d_simple as a contribution, the main text should at least include a brief table or figure demonstrating its effectiveness relative to IQE and Wide Norm.

3. **TDMadDist underperforms MadDist and QRL, yet the paper does not analyze why.** The TD variant is presented as a second algorithm, but its consistently lower performance (especially in correlation and CV) is not explained. Possible reasons (e.g., instability from bootstrapping, target network lag, loss formulation) are not discussed. This weakens the contribution of TDMadDist and raises questions about the value of the TD approach.

4. **The downstream planning experiment is described too briefly.** The planning algorithm is only sketched (Appendix H is not visible), and it is unclear whether the same planning procedure is equally suitable for all baselines. The very low success rates of the Hilbert baseline (e.g., 0.05–0.22) suggest that the planning method may be poorly matched to symmetric embeddings, which could exaggerate the advantage of MadDist. More details and a fairness analysis are needed.

### Minor

- The paper uses the term “self-supervised” but the loss functions rely on temporal gap labels (j−i) from trajectories, which is a form of weak supervision. This is not a flaw, but the terminology could be clarified.
- The contrastive loss (L_r) uses a hyperparameter d_max, but there is no discussion of how it is set or its sensitivity.
- The paper mentions gradient clipping but does not specify the clipping value or where it is applied.

### Trivial

None.

## Nice-to-Haves

- An ablation comparing MadDist with a symmetric distance (e.g., Euclidean) under the same loss would cleanly isolate the benefit of the quasimetric.
- A brief analysis of why TDMadDist underperforms (e.g., gradient variance, target network lag) would strengthen the paper.
- A table in the main paper comparing the three quasimetrics (d_simple, Wide Norm, IQE) on a representative environment would substantiate the claim about d_simple’s effectiveness.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that a scale-invariant regression loss combined with a simple ReLU-based quasimetric can recover the Minimum Action Distance from trajectory data more accurately than methods that rely on local constraints or symmetric embeddings. The finding that a straightforward max+mean of positive differences works as well as more complex quasimetrics (IQE) is practically valuable and suggests that the inductive bias of the quasimetric matters less than the global structure of the learning objective.

## Suggestions

1. Include Steccanella & Jonsson (2022) as a baseline in the main experiments, or at least provide a clear justification for its exclusion.
2. Move a brief quasimetric comparison (d_simple vs. IQE vs. Wide Norm) from the appendix to the main paper, or at least state explicitly which quasimetric is used in the primary results.
3. Add a short discussion of why TDMadDist underperforms, and consider repositioning it as a secondary variant rather than a co-equal contribution.
4. Provide more details on the planning algorithm in the main text (e.g., how the learned distance is used, whether it is the same for all methods) to ensure the downstream results are interpretable.

## Score and Decision

The paper makes a clear, well-supported contribution to learning the Minimum Action Distance from trajectories. The proposed MadDist algorithm is simple, principled, and empirically strong across a diverse set of environments. The weaknesses (missing baseline, insufficient analysis of TDMadDist, and reliance on the appendix for quasimetric comparison) are addressable and do not invalidate the core claims. The paper is a solid contribution to the representation learning and RL communities.

**Score:** 8

**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>