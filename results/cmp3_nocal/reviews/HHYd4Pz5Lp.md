## Summary

This paper introduces DelRec, a method for learning per-neuron (axonal) delays in recurrent connections of spiking neural networks using surrogate gradient learning. It adapts the differentiable interpolation technique from DCLS (feedforward delay learning) to the recurrent setting via a scheduling-matrix formulation that handles non-integer delays during training and collapses to discrete delays at inference. Experiments show strong results — 82.58% on SSC and 96.21% on PS-MNIST using simple LIF neurons — along with a controlled ablation on SHD comparing six model variants.

## Strengths

1. **Addresses a genuinely underexplored direction.** Recurrent delay learning in SNNs has received far less attention than feedforward delay learning. The paper correctly identifies and targets this gap.

2. **The scheduling-matrix formulation (Eqs. 8–11, Algorithm 1) is a technically clean adaptation of the DCLS interpolation technique to the recurrent setting.** The triangle interpolation with σ-annealing provides well-defined gradients for non-integer delays during training while collapsing to discrete delays at inference, and the pointer-buffer mechanism addresses the engineering challenge of scheduling future recurrent inputs.

3. **The ablation study on SHD (Fig. 3) is the strongest experimental component.** Comparing six model variants (vanilla SNN, vanilla RSNN, learned feedforward delays, fixed random recurrent delays, learned recurrent delays, and combined delays) under controlled parameter counts (≤10k) provides genuine insight. The finding that learned recurrent delays degrade more gracefully as parameters shrink (Fig. 3C top) supports the paper's core thesis.

4. **Results on SSC (82.58%, ±0.08%) improve over published LIF-based SOTA** (SiLIF 82.03%, DCLS 80.69%). The standard errors are small across 3 seeds and the improvement appears statistically reliable.

## Weaknesses

### Fatal
None.

### Major

1. **The "first SGL-based method" claim is imprecisely framed and creates a narrative contradiction.** The abstract and introduction state DelRec is "the first SGL-based method to train axonal or synaptic delays in recurrent spiking layers." However, Xu et al. (ASRC-SNN) uses backpropagation through spiking neurons (which implies surrogate gradient learning) and learns delays in recurrent connections — even if only **one delay per layer** rather than per neuron. The paper later (line 30) says "only Mészáros et al. (2025) have proposed an algorithm specifically designed to learn optimal delays in recurrent connections," yet Table 1 lists Xu et al. with checkmarks for recurrent delays. This creates an ambiguity about what claim is being made priority over. The distinction that matters — per-neuron granularity vs. per-layer granularity — is present in the text but not made salient. The claims should be qualified (e.g., "first to learn **per-neuron** delays using SGL" or "first to use **continuous-valued differentiable interpolation** for recurrent delays") and the relationship to Xu et al. clarified.

2. **The abstract's unqualified "new SOTA" claim on SSC overreaches.** The abstract states "new state-of-the-art (SOTA) on two challenging temporal datasets (Spiking Speech Command… and Permuted Sequential MNIST…)." While excluding attention-based and multi-compartment models from the main comparison table is reasonable for a LIF-focused paper, the paper's own footnote (lines 162–163) acknowledges Wang et al. (2024) achieves 83.69% on SSC — 1.11 pp higher than DelRec's 82.58%. The abstract should qualify the SOTA scope (e.g., "among simple LIF-based RSNNs") to avoid misleading a casual reader.

3. **The inconsistency between SSC and SHD regarding combined vs. isolated delays is not addressed for the SSC case.** On SSC, adding feedforward delays to recurrent delays *hurts* (82.58% → 82.19%), while on SHD's large model it *helps* (93.39% → 93.73%). The paper acknowledges the SHD small-model case (line 215: "we found no advantage in using both types of delays in these small configurations") but does not discuss the SSC direction at all. Since SSC is one of two headline SOTA datasets, this gap weakens the paper's ability to make general claims about how the two delay types interact. An explanation (or at minimum an acknowledgment) is needed.

### Minor

1. **PS-MNIST result lacks statistical reliability.** The paper reports 96.21% from a single seed and justifies this by noting prior work also uses one seed (line 132). While following convention is defensible, for a result presented as "new SOTA" in the abstract, a single seed provides no measure of variance. The gap over ASRC-SNN (95.77%) is only 0.44 pp and could fall within run-to-run noise.

2. **No analysis of what delays are actually learned.** The paper treats delays as a black box that produces better accuracy, but does not examine the learned delay values. Questions that go unanswered: What range of delays do neurons converge to? Do some neurons learn long delays to bridge distant time steps while others learn short delays? How do delays evolve during training? A single figure showing delay distributions would substantially strengthen the paper's mechanistic contribution.

3. **Computational/memory overhead is not discussed.** The scheduling matrix with the pointer mechanism and σ-annealing introduces additional memory and compute relative to a standard RSNN. The paper motivates SNNs by energy efficiency but does not quantify this overhead.

### Trivial
None.

## Nice-to-Haves
- A direct empirical comparison with Xu et al. (ASRC-SNN) under controlled conditions to isolate why DelRec's continuous interpolation outperforms softmax-over-discrete-delays.
- Wall-clock time or FLOPs comparison against vanilla RSNNs to help readers assess the practical tradeoff of the scheduling matrix.
- An analysis of learned delay distributions (histograms, evolution during training) to provide mechanistic insight.

## Removed Points
- *Criticism about SHD "new SOTA" claim*: The reviewer claimed the abstract overreaches on SHD, but the abstract clearly says "match the SOTA" on SHD, not "surpass" or "new SOTA." The paper's language is accurate on this point.
- *Criticism about Algorithm 1 being in the appendix*: The algorithm exists in the original submission; the appendix was stripped by the parser. Per instructions, weaknesses about missing appendix content are removed.
- *Criticism about EventProp parameter count estimation*: The paper transparently marks this as an estimate from a figure. This is an acknowledged limitation, not a flaw.
- *Claim that mechanistic claims are unsupported by a "consistent pattern across experiments"*: Overstated — the core claim (recurrent delays help temporal processing) is consistently supported. The inconsistency involves combined vs. isolated delays, a secondary finding.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Revise the "first SGL-based" claim to accurately reflect the granularity distinction from Xu et al. (per-neuron vs. per-layer delay learning).
2. Qualify the SOTA claims in the abstract to acknowledge the scope of comparison (LIF-based models).
3. Add multiple seeds for PS-MNIST or acknowledge the statistical uncertainty.
4. Discuss (or at minimum acknowledge) the SSC combined-delay degradation.
5. Add an analysis figure showing learned delay distributions for at least one dataset.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>