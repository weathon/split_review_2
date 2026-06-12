Now I have enough calibration data. Let me finalize my review.

**Bracket determination:**
- **Round 1 bracket**: The paper clearly scores above the 3-4 range (unlike SOLO at 4.0 which had significant performance degradation) and below the 7+ range (unlike Spiking Vision Transformer at 6.60 which had more thorough multi-task evaluation). The most comparable papers are DeepTAGE (6.25, accepted) and Layer Synchronization (5.75, rejected). DelRec has a cleaner method than either but weaker statistical rigor. I place it in the **5.5–6.5 bracket**.

- **Final anchoring**: Against DeepTAGE (6.25), DelRec has comparable method quality but fewer experimental datasets and weaker statistical evidence. Against Spatio-Temporal Dependency-Aware (5.75, rejected), DelRec has a more novel method but similar weakness profile. I settle on **5.5** — borderline accept, reflecting a solid contribution that needs modest but meaningful revision.

---

## Summary

This paper introduces DelRec, a method for learning per-neuron delays in recurrent connections of spiking neural networks (SNNs) using surrogate gradient learning and backpropagation. The key technical contribution is a differentiable interpolation mechanism (triangle function with progressive σ annealing) that allows gradient-based optimization of continuous-valued delays during training, followed by rounding to integers at inference. The method is evaluated on standard SNN benchmarks: Spiking Speech Commands (SSC), Permuted Sequential MNIST (PS-MNIST), and Spiking Heidelberg Digits (SHD). DelRec achieves SOTA among LIF-based methods on SSC (82.58%) and PS-MNIST (96.21%) and matches SOTA on SHD. An ablation study on SHD systematically compares six delay configurations, showing that learned recurrent delays outperform feedforward delays under low-parameter constraints.

## Strengths

- **Clean method design.** The triangle-function interpolation with progressive σ annealing (Eqs. 9–11) is a well-motivated, principled approach to handling non-integer delays during training while rounding to integers at inference. The scheduling matrix with pointer mechanism is straightforward to implement, and the method is compatible with any spiking neuron model fitting the standard three-equation formalism (Section 2.2).

- **Strong empirical results on SSC and PS-MNIST using simple LIF neurons.** DelRec with only recurrent delays achieves 82.58% on SSC (0.37M params, 3 seeds, σ=0.08) and 96.21% on PS-MNIST (0.16M params), outperforming prior LIF-based methods including DCLS (80.69%), ASRC-SNN (81.54%), and SiLIF (82.03%) on SSC (Table 1). This is a clear empirical contribution — the method achieves competitive or superior performance with the simplest neuron model.

- **Thorough ablation study on SHD.** The comparison of six model configurations (vanilla SNN, vanilla RSNN, learned feedforward delays, fixed random recurrent delays, learned recurrent delays, and combined) across parameter counts (2k–10k) and firing rates is informative (Fig. 3). The finding that learned recurrent delays outperform learned feedforward delays at low parameter counts is the paper's most interesting scientific result. The methodological discipline of using a clean validation split on SHD (20% of training) is commendable (lines 174–198).

## Weaknesses

### Major

- **The "first SGL-based method" claim is insufficiently substantiated.** The abstract and introduction state that DelRec is "the first SGL-based method to train axonal or synaptic delays in recurrent spiking layers" and "the first method to train axonal or synaptic delays in recurrent connections using surrogate gradient learning (SGL) and backpropagation." Yet the paper itself describes Xu et al. (ASRC-SNN) as learning "a single recurrent delay parameter per layer using backpropagation" with "a softmax function with a decreasing temperature" — an approach that uses gradient-based learning for recurrent delays. While there are plausible distinctions (per-neuron vs. per-layer delays; continuous-valued vs. selection from a fixed discrete set; SGL specifically referring to surrogate gradients through the spiking nonlinearity vs. softmax gradients), the paper never articulates *why* DelRec constitutes the "first" in a way that excludes these prior works. The claim is also listed in DelRec's own results table (Table 1) with ASRC-SNN having both "Rec." and "Rec. Delays" checked. This should be either precisely qualified or dropped in favor of emphasizing DelRec's specific technical advantages (continuous per-neuron delays, no predefined max delay range, differentiable interpolation).

### Minor

- **Inconsistent behavior of combined feedforward + recurrent delays is acknowledged but not explained.** On SSC, DelRec with only recurrent delays (82.58%) outperforms DelRec with both recurrent and feedforward delays (82.19%), despite having fewer parameters (0.37M vs 0.55M). On SHD small models (Fig. 3B), the combined version underperforms both feedforward-only and recurrent-only. On SHD large models (Table 2), the combined version outperforms recurrent-only. The paper acknowledges this ("we found no advantage in using both types of delays in these small configurations") but offers no explanation for why combining the method's own components sometimes *hurts* performance. This does not threaten the core contribution but leaves an unresolved question about when the combination is beneficial.

- **Limited statistical evidence for SOTA claims.** On SSC, DelRec reports 82.58 ± 0.08% over 3 seeds, while the prior best (ASRC-SNN) reports 81.54% with no error bar — the 1% gap is plausible but its significance is unclear without knowing ASRC-SNN's variance. On PS-MNIST, only a single seed is reported, with the justification "as all the previous state-of-the-art models on the dataset" — following a flawed convention does not make it methodologically sound. The SOTA framing in the abstract overstates the evidential support for these results.

- **No discussion of computational cost.** The scheduling matrix has dimension N × dim(Ẽ(σ, D)), where dim(Ẽ) depends on the maximum learned delay. During early training when σ is large, the support of h_(σ,d) is wide, requiring updates to multiple future time slots per spike. The paper provides no runtime comparisons, memory usage analysis, or FLOP estimates relative to baselines. For a methods paper, this is a practically relevant omission.

### Trivial

- **Reference to "Eq.15" (line 98)** before it is defined — appears to be a mislabel during drafting.

## Nice-to-Haves

- **Validate the gradient-mitigation hypothesis directly.** The paper claims that recurrent delays "mitigate gradient challenges by implementing temporal skip connections" (Fig. 1B). This is an interesting hypothesis but is never experimentally tested. Gradient norm statistics during training for vanilla RSNN vs. random-delay RSNN vs. learned-delay RSNN would turn this into evidence. As it stands, the claim is consistent with the results but also consistent with other mechanisms (e.g., longer temporal integration windows).

- **Analyze learned delay distributions.** The paper would benefit from showing what delays the model actually learns — are they concentrated at specific values? Do they vary meaningfully across neurons? This could provide insight into *how* delays help temporal processing.

- **The paper notes that feedforward delays are per-synapse while recurrent delays are per-neuron (line 170).** A discussion of how this granularity difference affects the comparison would strengthen the ablation study.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Eq. 15 reference error"** — This is a trivial formatting artifact (line 98). Removed as a formatting/typographical nitpick per hard rules.
- **"Feedforward vs recurrent per-synapse vs per-neuron asymmetry"** — The paper explicitly acknowledges this asymmetry (line 170). Removed because the paper already addresses it.
- **"Missing related works" / "Missing appendix content"** — The appendix is stripped by the parser, not absent from the submission. Removed per hard rules.
- **"No limitations section"** — A nice-to-have but not a standard expectation for every conference paper format.
- **"Gradient hypothesis not validated"** — Moved to Nice-to-Haves above; it is a valuable suggestion but not a core weakness since the paper's main results do not depend on this specific mechanistic claim.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observation about the "first" claim being overstated is valid and would improve the paper if addressed, but it is a standard novelty-policing critique rather than a novel insight about the method itself. The critic's observation about the combined-delay inconsistency is useful but the paper already acknowledges it.

## Suggestions

1. **Qualify the "first" claim precisely** — articulate what distinguishes DelRec from Xu et al. (per-neuron vs. per-layer, continuous vs. discrete-set selection, SGL vs. softmax selection) and from Mészáros et al. (SGL vs. EventProp). Alternatively, drop "first" and emphasize the specific technical advantages.
2. **Add or justify more seeds** — If the 1-seed PS-MNIST result follows community convention, state this explicitly and add a caveat about statistical uncertainty. For SSC, provide error bars for the most competitive baselines if possible, or soften the SOTA framing.
3. **Explain the combined-delay inconsistency** — even a plausible hypothesis (e.g., optimization interference, tuning mismatches) would be better than leaving the observation unaddressed.
4. **Add a brief computational cost table** — training time per epoch and peak GPU memory for DelRec vs. a matched RSNN baseline on one dataset.
5. **Consider adding gradient norm analysis** to support or qualify the gradient-mitigation hypothesis in Fig. 1B.

## Score and Decision

**Anchors considered:**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| DeepTAGE (drPDukdY3t.md) | 6.25 (accept) | R2 | Stronger empirical breadth (4 datasets); comparable method quality |
| Layer Sync (6iM7mmVhXh.md) | 5.75 (reject) | R1, R2 | Mixed reviewer reception; interesting findings but borderline |
| Spatio-Temporal Dep. (eN4g4cjFX1.md) | 5.75 (reject) | R1 | Similar weakness profile but less novel contribution |
| Fwd Grad Train (yBP36xQhZl.md) | 5.00 (reject) | R1, R2 | Novelty concerns; weaker empirical results |
| SOLO (vq75kRCYuY.md) | 4.00 (reject) | R1 | Performance degradation; limited novelty |
| DeNN (pIJR9uPjy3.md) | 4.50 (reject) | R3 | Delay-based method with clarity/technical issues |
| Spiking ViT (qzZsz6MuEq.md) | 6.60 (accept) | R3 | More thorough multi-task evaluation; accepted |
| Canonic Signed Spike (mtmqwhQiaG.md) | 5.25 (reject) | R1 | Conversion-based; less novel contribution |

**Round 1 bracket:** 5.5–6.5. **Final calibration:** Against DeepTAGE (6.25, accepted), DelRec has comparable method quality but fewer datasets and weaker statistical evidence. Against Layer Synchronization (5.75, rejected), DelRec has a cleaner method contribution but similar weakness severity. The method is sound and the results are competitive, but the "first" claim overreach, limited statistical evidence on PS-MNIST, and unresolved combined-delay behavior prevent a higher score. Score settled at **5.5**.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>