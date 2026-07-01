Now I have sufficient calibration data. Let me write the final consolidated review.

## Summary

This paper introduces DelRec, a method for learning per-neuron axonal (or synaptic) delays in recurrent connections of spiking neural networks using surrogate gradient learning. The key technical innovation is a differentiable interpolation mechanism (triangle spread function with an annealing schedule for σ) that allows gradient-based training of integer delay parameters. The method is evaluated on three benchmarks (SSC, PS-MNIST, SHD), achieving the best reported accuracy among LIF-based models with instantaneous synapses on SSC and PS-MNIST. An ablation study on SHD under low-parameter and sparsity constraints provides insights into the relative benefits of recurrent vs. feedforward delays in small networks.

## Strengths

1. **Clean and well-specified method (Section 2.2).** The differentiable interpolation using a triangle spread function with a decreasing σ is a principled way to handle discrete delay parameters during gradient-based training. The scheduling-matrix formulation (Eq. 8–11) and pointer mechanism (Algorithm 1) make the approach concrete and implementable. The method is compatible with any spiking neuron model fitting the Eq. 1–3 formalism.

2. **Credible SSC result (Table 1).** DelRec achieves 82.58 ± 0.08% with 0.37M parameters on SSC, surpassing the prior best LIF-based result (SiLIF, 82.03 ± 0.25%, 0.35M params). The gain is ~0.55 pp with comparable parameter count, and the lower standard deviation (0.08% vs. 0.25%) suggests improved stability. This is a genuine advance within the LIF-with-instantaneous-synapses model class.

3. **Informative ablation study (Section 3.2, Fig 3).** The systematic comparison of six model variants under low-parameter (2k–10k) and firing-rate constraints provides concrete evidence for the utility of delays in general, and specifically shows that recurrent delays degrade less steeply as network size shrinks. This regime-specific finding is non-obvious and merits attention.

4. **Honest discussion of SHD saturation (lines 176–178, 196–198).** The paper explicitly acknowledges SHD's small test set (2264 samples), the overlap of Bayesian confidence intervals among top accuracies, and the risk of test-set overfitting. This methodological self-awareness is commendable.

## Weaknesses

### Fatal
None.

### Major

1. **Unqualified SOTA claims in the abstract and conclusion.** The abstract states the paper achieves "new state-of-the-art (SOTA) on two challenging temporal datasets (Spiking Speech Command … and Permuted Sequential MNIST …)" without scope qualification. However, the paper's own footnote (line 162) lists higher accuracies from models using more complex neurons — Wang et al. (2024) at 83.69% on SSC and Chen et al. (2024) at 97.78% on PS-MNIST. Excluding these from the main comparison table because they use "substantially more complex neuron models" (line 132) is a defensible scientific choice, but the abstract and conclusion do not communicate this boundary to the reader. A reader will interpret "new SOTA" as the best-known accuracy on these datasets, which is false. The claims must be scoped to "new SOTA among LIF-based spiking models with instantaneous synapses" — which remains an impressive claim that the evidence supports.

2. **"Recurrent delays outperform feedforward delays" is not supported as a general claim.** The abstract asserts this as a finding (line 9), but:
   - On SHD (Table 2), the feedforward-only DCLS achieves 93.77 ± 0.68%, which is numerically higher than DelRec recurrent-only (93.39 ± 0.45%) and DelRec combined (93.73 ± 0.69%). The paper's own head-to-head comparison does not support the claim.
   - On SSC (Table 1), no feedforward-only delay variant is run under identical conditions. The comparison to DCLS (80.69%) is confounded by architectural differences (depth, parameter count, training setup).
   - The claim *is* supported in the small-model regime (Fig 3C, ≤10k params), where recurrent-delay models outperform feedforward-delay models as parameter count shrinks. But this is a narrow, regime-specific finding, not a general principle. The conclusion uses more measured language ("suggesting that recurrent delays can achieve better performance"), but the abstract's unqualified statement overreaches the evidence.

3. **PS-MNIST result reported without variance information (single seed, 96.21%).** The paper states (line 132) that only one seed was tested "as all the previous state-of-the-art models on the dataset" — but this does not justify the practice. A 0.44 pp gain over ASRC-SNN (95.77%) could easily fall within one standard deviation of either method. The paper elsewhere reports variance statistics consistently (SSC: 3 seeds; SHD: 10 seeds), making this omission conspicuous and undermining confidence in a claimed SOTA result.

### Minor

4. **The "first SGL-based method" framing needs sharper scoping.** The paper describes Xu et al. as learning "a single recurrent delay parameter per layer using backpropagation" with "a softmax function with a decreasing temperature" (line 30). If Xu et al. used backpropagation in an SNN context (which implies surrogate gradients), then DelRec is not the first SGL-based method for recurrent delays. The genuine novelty — per-neuron delays, continuous-valued via differentiable interpolation rather than softmax selection from a fixed set — should be foregrounded and clearly distinguished.

5. **Computational/memory cost of the scheduling matrix is not analyzed.** The scheduling matrix has dimension N × dim(Ẽ(σ, D)), which grows with both the maximum delay and σ (lines 118–120). At σ = 5, the support spans 13 time steps per spike. The paper does not discuss the memory footprint of this approach or its scaling behavior for larger networks or longer sequences.

6. **No ablation of the σ annealing schedule.** The paper uses a schedule from σ = 5 down to 0 but does not study sensitivity to this schedule or establish whether annealing is necessary vs. using a fixed small σ.

7. **Fixed random delay baseline not fully specified (Fig 3B).** The comparison between fixed recurrent delays (~78%) and learned recurrent delays (~82%) is informative, but the paper does not describe the distribution, range, or tuning process for the fixed random delays, making it difficult to assess whether the comparison uses a reasonable default.

8. **No discussion of delay regularization or clipping.** The paper states the method "eliminates the need to predefine a maximum delay range" (line 36), but the scheduling matrix dimension depends on max(d_j). Without discussion of whether delays are regularized or clipped, it is unclear how unbounded delay growth is handled in practice.

### Trivial
None.

## Nice-to-Haves

- Run a controlled feedforward-only delay baseline on SSC using the same architecture, hyperparameters, and training budget as the DelRec models, to directly test the central recurrent-vs-feedforward claim.
- Report PS-MNIST results with multiple seeds and variance.
- Provide the full citation for "Xu et al." (currently appears without year or venue).
- Analyze how the scheduling matrix memory cost scales with network width, maximum delay, and sequence length.

## Removed Points

These points from the input review are excluded or downgraded per the filtering rules:

- *"The anonymous repository URL is not shown"* — This is a parsing artifact; the original submission format carries this. Removed per Hard Rule (formatting artifact).
- *"Hyperparameters are claimed to be in the Appendix (which is stripped)"* — The reviewer explicitly notes this is not a flaw. Removed.
- *"The citation 'Xu et al.' is incomplete and makes it impossible for the reader to verify"* — Partially retained as Minor point 4 (scoping of "first SGL-based" claim). The reference section was truncated by parsing; the full citation may be present.
- *"Section-by-section notes"* containing observations that are not weaknesses (e.g., "the SiLIF baseline improvement is 0.55 pp with comparable params") — Observations without normative weight. Removed.
- *Strengths that are generic or conflict with verified weaknesses* — No such strengths were present in the input; the four strengths listed are all specific and evidence-grounded. Retained.

## Novel Insights

A genuinely novel observation emerges from the calibration comparison: papers in the SNN delay-learning space (DeNN at 4.50, DelRec at ~5.5) consistently face rejection pressure from overclaiming — specifically, making unqualified SOTA claims that the paper's own data or cited literature contradict. This pattern suggests that the community places a premium on precise claim-scoping in this subarea, and that the overclaiming common to many SNN papers is particularly damaging in the delay-learning sub-niche, where results are often incremental (a few tenths of a percent on saturated benchmarks). DelRec's core technical contribution (per-neuron differentiable recurrent delays) is stronger than its headline framing suggests, and the paper would be better served by letting the method speak for itself rather than reaching for unqualified SOTA language.

## Suggestions

1. **Revise the abstract** to scope the SOTA claims explicitly (e.g., "achieves new SOTA on SSC and PS-MNIST among LIF-based models with instantaneous synapses, and matches SOTA on SHD").
2. **Qualify the recurrent-vs-feedforward claim** to reflect the evidence: e.g., "recurrent delays provide greater benefits than feedforward delays in small networks and under low-parameter constraints."
3. **Run PS-MNIST with at least 3 seeds** and report mean ± std.
4. **Clarify the "first SGL-based method" claim** by explaining how DelRec differs from Xu et al.'s per-layer softmax approach (per-neuron learning, continuous delays via differentiable interpolation).

## Score and Decision

**Calibration anchors used** (all from deepreview_13k_calibration):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| DeNN (pIJR9uPjy3.md) | 4.50 | Narrow | Delay-focused SNN paper, rejected for poor exposition and overclaiming. DelRec is significantly clearer. |
| PMSN (FlH6VB5sJN.md) | 5.20 | Bracket | Multi-compartment neuron, rejected. DelRec has a more clearly motivated problem. |
| TFSNN (RmQAKu1wCe.md) | 5.00 | Narrow | Temporal flexibility, rejected for overstated claims. DelRec's method is more solid. |
| SpikE-SSM (4ILqqOJFkS.md) | 3.67 | Bracket | Spiking SSM, rejected for incremental contribution. DelRec has stronger novelty. |
| DeepTAGE (drPDukdY3t.md) | 6.25 | Bracket | Gradient enhancement, accepted despite theoretical gaps. Comparable strength. |
| TS-LIF (rDe9yQQYKt.md) | 6.00 | Bracket | Dual-compartment neuron, accepted. DelRec has slightly more significant overclaiming. |
| Layer Sync (6iM7mmVhXh.md) | 5.75 | Bracket | Layer synchronization, rejected. Mixed scores (6,8,6,3). |
| Spatio-Temporal Dep. (eN4g4cjFX1.md) | 5.75 | Narrow | Neuron optimization, rejected. Mixed scores (6,6,6,5). |

**Round 1 bracket**: 4.0–6.5  
**Round 2 narrowing**: 5.0–6.0  
**Final score anchored between**: TS-LIF (6.00, accepted) and PMSN/TFSNN (5.00–5.20, rejected). DelRec has a stronger core contribution than the rejected papers but overclaims more than TS-LIF.

The paper presents a real, well-specified technical contribution (learning per-neuron recurrent delays via differentiable interpolation), with a credible advance on SSC within a clearly defined model class. However, the abstract and conclusion overstate the scope of these results in ways that would mislead readers. The overclaiming is fixable without altering the method or experiments. The PS-MNIST result's missing variance is a meaningful gap in evidence quality. On balance, the core contribution is solid enough to merit acceptance conditional on fixing these framing issues.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>