Now I have sufficient calibration data. Let me write the final review.

## Summary
This paper introduces DelRec, the first surrogate gradient learning (SGL) method for training axonal delays in recurrent spiking neural network connections. The method adapts the differentiable triangle interpolation kernel (from DCLS) to a "scheduling matrix" that dispatches spikes into future timesteps for recurrent connections, with a progressively narrowing width parameter σ during training. DelRec achieves new SOTA on SSC (82.58%) and PS-MNIST (96.21%) using only simple LIF neurons, matches SOTA on the saturated SHD dataset, and presents a functional ablation study comparing recurrent vs. feedforward delays.

## Strengths
- **New SOTA on SSC and PS-MNIST using only simple LIF neurons (Table 1):** DelRec achieves 82.58%±0.08% on SSC and 96.21% on PS-MNIST, surpassing methods like SiLIF (82.03%, structured state-space), ASRC-SNN (95.77%), and SE-adLIF (80.44%, adaptive) that use more complex neuron architectures. This demonstrates that learned recurrent delays can substitute for complex neuron dynamics.
- **First SGL-based method for recurrent delays:** Prior work on recurrent delays was limited to EventProp (Mészáros et al., 2025), which has scalability issues and suboptimal performance on real-world benchmarks. All current SNN SOTA methods rely on SGL, making this a genuine gap that DelRec fills.
- **Systematic ablation study with clear methodology (Section 3.2):** The three-phase approach (validation, simplification, comparative) on SHD provides structured evidence. Fig. 3B shows learned recurrent delays (~82%) outperform feedforward delays (~80%) and even random fixed recurrent delays dramatically improve over vanilla RSNN (~78% vs ~40%), supporting the gradient-flow hypothesis.
- **Clean isolation of delay contribution:** By using only LIF neurons with stateless synapses across all experiments, the paper cleanly attributes performance gains to learned delays rather than to neuron model complexity.

## Weaknesses

### Fatal
None.

### Major
- **Single-seed PS-MNIST headline result with no variance reported:** The claim of new SOTA on PS-MNIST rests on a single run (96.21%), with no error bars. The improvement over ASRC-SNN is only ~0.44 percentage points. The paper justifies this by noting prior SOTA models also tested one seed, but replicating a methodological weakness does not neutralize it—especially for a paper claiming SOTA. (SSC results are stronger: 3 seeds with tight variance ±0.08%.) This weakens one of the paper's two headline claims.
- **Core ablation conducted only on SHD with tiny ~10k-parameter models; tension with SSC results unexplained:** The functional study comparing recurrent vs. feedforward delays (Section 3.2) uses models orders of magnitude smaller than the headline SSC/PS-MNIST models. More importantly, on SSC (Table 1), combining recurrent and feedforward delays *degrades* performance (82.19% vs. 82.58% for recurrent-only, despite 0.55M vs. 0.37M parameters). This contradicts the clean narrative from SHD ablations and is not analyzed. The paper would be substantially strengthened by explaining this tension—it could reveal whether the issue is optimization difficulty, overfitting, or genuine architectural insight about delay type interactions.

### Minor
- **Core interpolation mechanism borrowed from DCLS:** The triangle kernel with annealing σ is directly taken from DCLS (Hammouamri et al., 2024; Khalfaoui-Hassani et al., 2023), acknowledged at line 122 ("A similar strategy was used in [Hammouamri et al., 2024]"). The abstract frames DelRec as "the first method to train axonal or synaptic delays in recurrent connections using SGL," implying a larger methodological leap than what is presented. The genuine novelty is the scheduling matrix for recurrent connections and the empirical finding that they matter—the paper would benefit from more clearly scoping its novelty claim.
- **No analysis of learned delay distributions:** What delays does DelRec actually learn? Do they concentrate near 1 (the minimum), or spread out? How do they differ across layers or training trajectory? This analysis would provide insight into *why* recurrent delays help and is more informative than additional benchmark numbers.

### Trivial
None.

## Nice-to-Haves
- Report wall-clock training time and GPU memory usage vs. vanilla RSNN to help practitioners assess the practical cost of the scheduling matrix mechanism.
- Provide direct evidence for the gradient-flow argument (Fig. 1B) by measuring gradient norms during training with and without recurrent delays.

## Removed Points
These points are flagged to be removed, treat them with caution.
- **"Eliminates the need to predefine a maximum delay range" overstated (line 36):** The paper's statement is reasonable; the scheduling matrix adapts based on learned delays, which is meaningfully different from pre-defining a fixed range. The harsh critic's concern about Eq. 13 implicitly bounding the range is overly pedantic.
- **SHD augmentation inconsistency (footnote b in Table 2):** The paper explicitly notes this with a footnote. Augmentation is applied consistently within the validation phase.
- **"Synaptic delays" capability undemonstrated (line 74):** The paper states code compatibility, not a claimed experimental contribution.
- **Conclusion language "critical" vs. "beneficial":** Minor framing issue; the paper's language in context is defensible.

## Novel Insights
The paper provides the first empirical evidence that recurrent delay learning via SGL can achieve SOTA on temporal benchmarks using simple LIF neurons. The functional study (Fig. 3B) showing that even random fixed recurrent delays dramatically improve over vanilla RSNN (~78% vs ~40%) is a genuinely interesting finding supporting the gradient-flow hypothesis. The practical insight that feedforward delays achieve peak accuracy at lower firing rates than recurrent delays (Fig. 3C bottom) could guide hardware deployment decisions.

## Suggestions
- Run 3–5 seeds on PS-MNIST to strengthen the headline SOTA claim.
- Analyze the degradation from combining recurrent+feedforward delays on SSC (82.19% vs. 82.58%). This could become a genuine insight about delay type interactions.
- Include a brief analysis of learned delay distributions (histograms across neurons/layers).
- Report computational overhead (training time, memory) vs. vanilla RSNN baseline.

## Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| DeNN | pIJR9uPjy3 | 4.50 (Reject) | 1 | Delay networks for event data; DelRec has cleaner SOTA and better focus |
| SOLO | vq75kRCYuY | 4.00 (Reject) | 1 | SNN online training with performance drops; DelRec clearly stronger |
| Forward Gradient | yBP36xQhZl | 5.00 (Reject) | 1 | SNN training, novelty concerns, no clear SOTA; DelRec stronger |
| Layer Sync | 6iM7mmVhXh | 5.75 (Reject) | 1 | SNN async processing, mixed reception; DelRec has clearer SOTA |
| Spatio-Temporal Dep. | eN4g4cjFX1 | 5.75 (Reject) | 2 | SNN neuron optimization; similar quality but DelRec achieves SOTA |
| TS-LIF | rDe9yQQYKt | 6.00 (Accept) | 2 | Novel SNN neuron for time series; comparable quality to DelRec |
| Temporal Flexibility | 9HsfTgflT7 | 6.20 (Accept) | 2 | SNN temporal training; comparable quality, both fill genuine gaps |
| DeepTAGE | drPDukdY3t | 6.25 (Accept) | 1,2 | Novel SNN gradient method; most directly comparable to DelRec |
| SpikePoint | 7etoNfU9uF | 5.75 (Accept) | 2 | Event camera SNN; less relevant topically |
| Rethinking SNNs | ZyknpOQwkT | 5.50 (Accept) | 2 | SNN ensemble perspective; less relevant |

**Round 1 bracket:** 5.5–7.0. DelRec is clearly above the 4–5 range (SOLO, FGT, DeNN) and comparable to accepted papers at 6.0–6.25 (TS-LIF, Temporal Flexibility, DeepTAGE).

**Round 2 narrowing:** Confirmed the 6.0–7.0 range. DelRec fills a more unique niche than DeepTAGE (recurrent delays are a genuine gap) and has cleaner SOTA claims than TS-LIF, but the single-seed PS-MNIST issue and borrowed core mechanism keep it from a 7+. Final score: 6.5.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>