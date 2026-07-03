## Summary

This paper introduces DelRec, a method for learning per-neuron transmission delays in the recurrent connections of spiking neural networks (SNNs) using surrogate gradient learning (SGL). The method uses differentiable interpolation (a triangle spread function with an annealing schedule) to handle non-integer delays during training, then rounds to integers at inference. DelRec achieves strong results on SSC (82.58%), PS-MNIST (96.21%), and SHD benchmarks using only simple LIF neurons. A thorough functional study demonstrates that learned recurrent delays maintain accuracy better under parameter constraints than feedforward delays or vanilla RSNNs.

---

## Strengths

1. **First SGL-based per-neuron delay learning in recurrent SNNs**: DelRec fills a clear methodological gap. Prior work either learned only feedforward delays (DCLS; Hammouamri et al. 2024), used EventProp with scalability limitations (Mészáros et al. 2025), or learned one delay per layer via softmax selection from a fixed set (Xu et al.). DelRec is the first to learn per-neuron axonal delays in recurrent connections with SGL, enabling per-neuron granularity without a predefined delay set.

2. **Strong empirical results with simple LIF neurons**: Table 1 shows DelRec achieving 82.58% ± 0.08% on SSC (outperforming SiLIF at 82.03%) and 96.21% on PS-MNIST (outperforming ASRC-SNN at 95.77%) using only vanilla LIF neurons with stateless synapses—while competing approaches often rely on adaptive mechanisms, resonant dynamics, or multi-compartment architectures. This cleanly attributes the performance gain to the delay-learning method rather than to complex neuron dynamics.

3. **Careful ablation isolates the benefit of *learning* delays from the structural benefit of having delays**: The functional study (Sec. 3.2, Fig. 3) compares six configurations. The comparison between *fixed random* recurrent delays (~78% on SHD) and *learned* recurrent delays (~82%) cleanly separates the structural advantage of introducing delays from the additional benefit of optimizing them. The accuracy-vs-parameter curves (Fig. 3C top) show that learned recurrent delays degrade less steeply under parameter compression—direct evidence for the paper's core claim that recurrent delays make more efficient use of limited representational capacity.

4. **Methodologically rigorous benchmarking**: The paper acknowledges SHD saturation (lines 176–178), adopts a clean train/validation/test split using 20% of training data, reports results over 10 seeds on SHD, and explicitly recommends it only for initial validation rather than SOTA claims. On SSC, results are reported over 3 seeds with standard deviations. This is a higher standard than much prior work.

---

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **"First SGL-based method" claim is slightly overstated.** The abstract and introduction (§1, line 36) state DelRec is "the first SGL-based method to train axonal or synaptic delays in recurrent spiking layers." However, the paper itself cites Xu et al., who train recurrent delays via backpropagation (which, in the SNN context, inherently uses surrogate gradients), albeit at coarser per-layer granularity via softmax selection from a fixed set. The genuine novelty is *per-neuron* granularity combined with differentiable interpolation (no predefined delay set), not SGL-for-recurrent-delays per se. The authors should explicitly state what prior work exists and what granularity/technique gap they are filling, rather than using the unqualified "first."

2. **Unqualified "state-of-the-art" in the abstract.** The abstract claims "new state-of-the-art (SOTA) on two challenging temporal datasets." Footnote 1 (line 162) acknowledges that multi-compartment neurons (Zheng et al. 2024: 82.46% on SSC; Chen et al. 2024: 97.78% on PS-MNIST) and attention-based neurons (Wang et al. 2024: 83.69% on SSC) achieve higher scores. Excluding these models from Table 1 is defensible—they use substantially more complex mechanisms that make direct comparison less meaningful—but the abstract should reflect this scope restriction (e.g., "new SOTA among LIF-based models" or "among comparably simple neuron models").

3. **PS-MNIST result from only one seed, no variance estimate.** The paper reports 96.21% on PS-MNIST from a single seed (line 132), with the justification that "all the previous state-of-the-art models on the dataset" followed the same practice. The 0.44% gain over ASRC-SNN (95.77%) is modest, and without any measure of variance, it is impossible to assess whether this difference is meaningful or within noise. Whether prior work followed the same practice does not absolve the current paper from providing stronger evidence.

4. **Undiscussed discrepancy: recurrent-only outperforms recurrent+feedforward on SSC.** Table 1 shows DelRec with *only* recurrent delays achieves 82.58% (0.37M params), while DelRec with *both* recurrent and feedforward delays achieves only 82.19% (0.55M params). This is counterintuitive—adding feedforward delays to an already-delayed recurrent network *hurts* performance. The paper does not discuss this result. Possible explanations (optimization challenges, redundancy, overfitting with more parameters) would deepen the analysis, especially given the paper's claim that recurrent delays outperform feedforward ones.

### Trivial

1. **"Eliminates the need to predefine a maximum delay range" (line 36) is slightly overstated.** The scheduling matrix uses an effective range based on current delay values (Eq. 13: `ceil(1 + max(d_j) + (1+σ))`), so delays are still bounded in practice—the method defers the bound to optimization rather than eliminating it entirely. The practical claim is reasonable but the wording is imprecise.

2. **Reference to "Eq. 15" on line 98** while equations in the visible text only number up to Eq. 12 is likely a PDF extraction artifact from an equation in a stripped appendix section. (Parser artifact, not an author error, but the authors should verify consistency.)

---

## Nice-to-Haves

- A brief discussion of when recurrent delays help most (beyond parameter constraints) and for what types of temporal structure.
- Computational cost analysis (wall-clock time or memory footprint of the scheduling matrix relative to a standard RSNN).
- Hyperparameter sensitivity for the σ annealing schedule and the delay learning rate.

---

## Removed Points

These points were raised by the reviewers but are not included as weaknesses:

- **Borrowing from DCLS (Hammouamri et al., 2024)**: The harsh critic suggests the attribution "A similar strategy was used in (Hamouamri et al., 2024)" should be more explicit. The paper properly cites DCLS; the contribution is the application to *recurrent* delays, not the interpolation technique itself. **Removed** (paper adequately cites prior work).
- **Missing limitations section**: Not a standard requirement; information is implicit. **Moved to Nice-to-Haves**.
- **Generic strength ("addresses an important problem")**: Superficial and not specific to the paper. **Removed**.

---

## Novel Insights

The harsh critic's observation about the recurrent-only vs. recurrent+feedforward discrepancy on SSC (82.58% vs. 82.19%) is genuinely insightful and highlights a tension the paper's own analysis misses—if adding feedforward delays hurts performance, that is itself interesting and worth discussing. The strength finder's identification that the fixed-random vs. learned recurrent delay comparison (Fig. 3B: ~78% vs. ~82%) cleanly separates structural benefit from optimization benefit is a methodological point worth emphasizing: this distinction is rarely made cleanly in the delay-learning literature.

None beyond the paper's own contributions.

---

## Suggestions

1. **Qualify the "first" and "SOTA" claims** in the abstract to avoid overstatement: reference Xu et al. explicitly and note the per-neuron granularity gap; qualify SOTA as "among LIF-based models."
2. **Report PS-MNIST results across multiple seeds** (or at minimum acknowledge the limitation prominently in the main text rather than a passing comment).
3. **Discuss the recurrent-only vs. recurrent+feedforward discrepancy on SSC** explicitly—this deepens the paper's own analysis.
4. **Add a brief limitations paragraph** covering computational cost of the scheduling matrix, the σ annealing schedule sensitivity, and the discrete-time assumption.

---

## Score and Decision

**Score:** 7.0  
**Decision:** Accept

The calibration search was unavailable due to a persistent tool error, so I anchor this score by direct reasoning: the paper has no fatal or major flaws. The method is technically sound, clearly described, and fills a genuine gap (SGL-based per-neuron recurrent delay learning). The experimental design is rigorous—the SHD handling, multi-seed reporting on SSC, and the functional study all exceed common community standards. The weaknesses are all minor, addressable in a rebuttal, and do not threaten the core contribution. This is clearly an Accept (7), not a borderline Accept (6), because the claimed contribution (learning per-neuron recurrent delays with SGL) is achieved and convincingly demonstrated, and the weaknesses are about precision of claims, not substantive gaps.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>