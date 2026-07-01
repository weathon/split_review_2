## Summary

This paper introduces DelRec, a method for learning per-neuron (axonal) delays in recurrent connections of spiking neural networks using surrogate gradient learning and differentiable interpolation (triangular kernel with σ-annealing, extended from DCLS). The key algorithmic contribution is a scheduling matrix mechanism that handles the temporally non-local credit assignment created when a spike at time t affects future time steps t+1+d. Experiments on three benchmarks show that DelRec with simple LIF neurons achieves new SOTA on SSC (82.58±0.08%, 3 seeds), a single-run result above prior work on PS-MNIST (96.21%), and matches SOTA on the saturated SHD dataset. A controlled ablation study on SHD (~10k params) compares six conditions and finds that learned recurrent delays outperform learned feedforward delays under low-parameter constraints.

## Strengths

- **First SGL-based method for per-neuron recurrent delays in SNNs.** The paper extends the DCLS triangular-kernel interpolation to recurrent connections, requiring a non-trivial scheduling matrix mechanism (Eq. 8, Algorithm 1) because spikes emitted at time t affect future time steps t+1+d_j. This algorithmic innovation is genuinely novel—prior work (Xu et al.) learned one delay per layer via softmax selection from a fixed set, while Mészáros et al. used EventProp, not SGL.

- **New SOTA on SSC with meaningful statistical support.** The recurrent-delays-only model achieves 82.58±0.08% (3 seeds) on SSC, outperforming the strongest prior approach (ASRC-SNN, 81.54%) and several more complex neuron models (SE-adLIF, SiLIF), using competitive parameter counts (0.37M) and simple LIF neurons. This is the paper's strongest and cleanest empirical result.

- **Thorough ablation on SHD with controlled comparisons.** The functional study (Fig 3) compares six conditions at approximately equal parameter counts (~10k params), showing that learned recurrent delays outperform learned feedforward delays, fixed random recurrent delays, and vanilla architectures in the low-parameter regime. The energy-vs-accuracy trade-off analysis provides practical insight.

- **Methodological rigor in SHD evaluation.** The paper correctly identifies flaws in prior SHD evaluation (no dedicated validation set, test-set overfitting) and adopts a clean 80/20 training/validation split. It also acknowledges when differences are not statistically significant due to the small test set (2264 samples). This transparency is commendable.

## Weaknesses

### Fatal
None.

### Major

1. **PS-MNIST SOTA claim rests on a single seed and is not statistically substantiated.** The paper reports 96.21% on PS-MNIST (vs. 95.77% for ASRC-SNN, a 0.44% gap) and states (line 132): *"we only test one seed as all the previous state-of-the-art models on the dataset."* This reasoning is circular—prior work using a single seed does not make the practice acceptable. A 0.44% gap on a single run could easily fall within noise, and the paper provides no mean, standard deviation, or confidence interval. The claim of SOTA on PS-MNIST is not convincingly supported as written.

2. **Central theoretical motivation (gradient mitigation) is asserted but entirely untested.** The paper argues (Fig 1B, lines 22, 28) that recurrent delays *"mitigate gradient challenges by implementing temporal skip connections, improving gradient propagation during training."* This is presented as a primary motivation alongside expressivity, yet no gradient norm analysis, training loss curves, or comparison of gradient propagation at different time horizons is provided. The closest evidence is the observation (line 213) that random fixed recurrent delays help vs. vanilla RSNN—but this does not specifically validate the gradient-mitigation mechanism. This gap weakens the paper's theoretical framing.

3. **The finding that recurrent-only delays outperform combined recurrent+feedforward delays on SSC is unexplained and undermines the claimed benefit of hybrid delay learning.** In Table 1, the model with only recurrent delays (82.58±0.08%, 0.37M params) achieves higher accuracy than the model combining both delay types (82.19±0.16%, 0.55M params). The difference (0.39%) is within ~2 standard errors, so it may not be significant—but the central tendency goes against the paper's narrative that combining both types is beneficial. The only offered explanation appears in the SHD context (line 215: *"we found no advantage in using both types of delays in these small configurations"*), not for the large SSC models. This result deserves direct discussion.

### Minor

1. **Asymmetric comparison between per-neuron axonal delays and per-synapse feedforward delays.** The paper acknowledges (line 170) that it is *"comparing synaptic feedforward delays (one delay per synapse), with axonal recurrent delays (one delay per neuron)"*—but the functional study in Section 3.2 draws the conclusion that recurrent delays outperform feedforward delays without fully accounting for this asymmetry. A per-neuron delay gives all outgoing connections of a neuron the same temporal offset, while per-synapse delays allow connection-specific timing. The feedforward approach has far more temporal degrees of freedom for a given neuron count, which could affect both expressivity and optimization. This caveat should be more prominently discussed when interpreting the "recurrent delays are better" conclusion.

2. **Slightly overstated SHD claim.** Line 178 states *"our models achieve state-of-the-art performance on SHD,"* but Table 2 shows DelRec (Rec. and Ff.) at 93.73±0.69%, below SE-adLIF (2L) at 93.79±0.76% and DCLS at 93.77±0.68%. The differences are within noise (as the paper correctly notes elsewhere), but the phrasing is technically inaccurate. The abstract more carefully says "match the SOTA," which is the correct characterization.

### Trivial
None.

## Nice-to-Haves
- **Gradient analysis (highest leverage):** A simple experiment comparing gradient norms across time steps for vanilla RSNN vs. DelRec-trained RSNN would directly validate or refute the Fig 1B motivation.
- **PS-MNIST multi-seed results:** 3–5 seeds with mean and std would turn the unsubstantiated SOTA claim into a credible one.
- **Analysis of learned delay distributions:** Visualizing what delay values the network converges to (clustered, diverse, correlated with task timescales) would strengthen the claim that the method learns meaningful temporal structure.
- **Ablation of interpolation mechanism:** Comparing the triangular kernel with σ annealing against alternatives (straight-through estimator on integer delays, softmax over discrete bins as in Xu et al.) would isolate the value of the interpolation method for the recurrent setting.
- **Computational cost characterization:** The scheduling matrix size scales with N × dim(Ẽ), which depends on max delay and σ. Wall-clock time or memory overhead vs. vanilla RSNN would help practitioners assess the trade-off.

## Removed Points
These points from the input review are flagged to be removed; treat them with caution:

- **Question about "first SGL-based" claim vs. Xu et al.:** The reviewer questioned whether Xu et al. also qualifies as SGL-based since they use backpropagation. This requires external knowledge about Xu et al.'s method that cannot be verified from the paper alone. The paper's claim is specifically about *per-neuron* delay learning via differentiable interpolation, which differs from Xu et al.'s per-layer softmax selection from a fixed set. Removed by Hard Rule (cannot be verified from paper alone).

- **Methods verification notes (Eq. 9, Eq. 13):** The reviewer's verification that the triangular kernel normalization and scheduling range are mathematically correct are analysis notes, not weaknesses. Removed as not weaknesses.

- **Requests for delay distribution analysis, interpolation ablation, and computational cost:** These are requests for additional experiments that go beyond standard evaluation expectations for a methods paper. Moved to Nice-to-Haves.

## Novel Insights
The synthesis of the three major gaps reveals a pattern: the paper's strongest claim (SOTA on SSC) is well-supported, but its secondary empirical support (PS-MNIST single seed) and theoretical framing (gradient mitigation) are materially weaker than the paper's tone suggests. Taken together, these gaps do not threaten the core contribution—the method itself is sound and the SSC result is credible—but they mean the paper's advertised contributions are not uniformly evidenced. The SSC result should be the headline, with the PS-MNIST claim downgraded to "promising single-run result" and the gradient mitigation motivation either experimentally supported or removed from the paper's central justification.

## Suggestions
1. **Run 3–5 seeds on PS-MNIST** and report mean ± std. This single change would substantially strengthen the empirical profile.
2. **Add a gradient-norm experiment** comparing vanilla RSNN vs. DelRec over training, even as a short appendix section, to support or qualify the gradient mitigation claim in Fig 1B.
3. **Discuss the recurrent-only > combined result on SSC directly.** If it is within noise, state that explicitly. If it signals overfitting or optimization difficulty with additional delay parameters, explain the likely cause.
4. **Reframe the SHD claim** from "state-of-the-art" to "competitive with state-of-the-art" or "matching state-of-the-art" to be consistent with Table 2 and the abstract.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>