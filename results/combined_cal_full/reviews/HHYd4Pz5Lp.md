Based on my analysis of the paper and calibration against the anchors, here is my final consolidated review.

---

## Summary

DelRec introduces the first surrogate gradient learning (SGL) method for training delays in recurrent connections of spiking neural networks. It extends the DCLS differentiable interpolation technique to the recurrent setting using a scheduling matrix with annealed σ and achieves competitive results on SSC, PS-MNIST, and SHD benchmarks using simple LIF neurons. The paper also presents a functional study comparing recurrent and feedforward delays under low-parameter constraints.

## Strengths

- **Sound and well-motivated method.** The paper identifies a genuine gap—prior work on learnable delays in SNNs focused on feedforward connections, while the recurrent case was tackled only by EventProp (Mészáros et al., 2025), which has scalability limitations. The differentiable interpolation with annealed σ (Eqs. 9–11, Fig. 2C) is a clean adaptation of DCLS to the recurrent setting, and the scheduling matrix formulation (Eqs. 8, 13) makes the mechanism concrete. The method is compatible with any spiking neuron fitting the Eq. 1–3 formalism and does not require predefining a maximum delay range.

- **Functional study goes beyond SOTA reporting.** The multi-phase ablation on SHD (validation → simplification → comparative, Fig. 3C) provides meaningful comparisons (accuracy vs. parameters, accuracy vs. firing rate) that are rare in the SNN delay literature, helping isolate whether recurrent delays specifically drive gains.

- **Competitive results with minimal neuron complexity.** DelRec achieves its best SSC result (82.58%) using vanilla LIF neurons with 0.37M parameters. Prior best results used adaptive neurons (SE-adLIF: 80.44%, 1.6M params; SiLIF: 82.03%, 0.35M params). Showing that delay learning can compensate for simpler neuron dynamics is a practically meaningful finding.

## Weaknesses

### Fatal

None.

### Major

- **SOTA claims lack necessary qualification in the abstract.** The abstract states "new state-of-the-art (SOTA) on two challenging temporal datasets (Spiking Speech Command... and Permuted Sequential MNIST...)" without caveats. While footnote 1 and the main text acknowledge that models using multi-compartment neurons, attention, or GRU mechanisms achieve higher scores (e.g., Wang et al., 2024: 83.69% on SSC; Chen et al., 2024: 97.78% on PS-MNIST), these exclusions are methodologically sound but the abstract's unconditional phrasing is misleading to a casual reader. Similarly, the claim of "state-of-the-art performance on SHD" (line 178) is debatable since Table 2 shows DCLS (93.77%) and SE-adLIF 2L (93.79%) numerically ahead of DelRec with both delays (93.73%), though within error bars. The abstract and conclusion should qualify the comparison class (e.g., "SOTA among LIF-based models").

- **The claim that "recurrent delays outperform feedforward delays" is only convincingly supported in a narrow regime.** The main evidence comes from small-model SHD experiments (2k–10k parameters, Fig. 3C). At larger scales on SHD (Table 2), DCLS with feedforward-only delays (0.22M params, 93.77%) outperforms DelRec with only recurrent delays (0.17M params, 93.39%), which contradicts the comparative claim. The paper acknowledges this asymmetry but still makes broad comparative statements in the abstract and conclusion. The claim should be scoped to small-model, low-parameter regimes.

### Minor

- **PS-MNIST result from a single seed (line 132).** The paper justifies this by citing community precedent, but the margin over ASRC-SNN (96.21% vs. 95.77%) is modest. Without multiple seeds or error bars, the statistical reliability of this improvement is unclear.

- **No analysis of learned delay distributions.** The paper never visualizes or analyzes what delays are actually learned (e.g., histograms or heatmaps of converged delay values). This would provide insight into whether the method converges to interpretable delay patterns and would substantially strengthen the scientific contribution.

- **Gradient-bridging motivation unverified.** Figure 1B motivates recurrent delays as mitigating vanishing/exploding gradients through temporal skip connections, but no experiment measures gradient flow (e.g., gradient norms across time steps with and without recurrent delays). This is stated as a benefit but never tested.

- **No ablation of the σ annealing schedule.** The σ annealing strategy is inherited from DCLS but never ablated (e.g., fixed σ throughout training, or rounding delays during training). The sensitivity of results to this key hyperparameter is unexplored.

- **Computational cost unreported.** The scheduling matrix approach (Eq. 13) has a buffer dimension scaling with the maximum delay, but training time, memory usage, and comparison to standard RSNNs are not reported, despite the method's claimed practical deployability.

### Trivial

None.

## Nice-to-Haves

- An analysis of the distribution of learned delays (histogram/heatmap) would help understand what the method learns.
- A comparison of gradient norms with and without recurrent delays to verify the gradient-bridging motivation.
- An ablation of the σ annealing schedule to assess sensitivity.
- Reporting of training time and memory usage vs. baseline RSNNs.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **SHD confound between architecture and delay type (removed):** The reviewer claimed that comparing recurrent delays in layer 2 vs. feedforward delays between layers 1-2 conflates delay type with architectural position. This is inherent to the comparison—recurrent delays are necessarily within-layer, feedforward delays are necessarily between-layer—and the paper explicitly notes this asymmetry (line 170). A controlled comparison in the same position is architecturally impossible.

- **Formatting/style nitpicks, missing appendix content, reproducibility concerns about the anonymous repository (removed per hard rules):** These are either parser artifacts or reflect that the appendix was stripped during extraction.

- **Missing related works (removed per hard rule):** Not verifiable without external sources.

- **Generic/superficial strengths from the input review (removed):** Claims about the paper "addressing an important problem" or "targeting an interesting question" without specific evidence were removed.

## Novel Insights

None beyond the paper's own contributions. The review analysis surfaces the framing mismatch between the abstract's unconditional SOTA claims and the paper's own qualifying footnotes, and highlights that the central comparative claim (recurrent > feedforward) is only supported in a narrow parameter regime on one dataset—observations that are implicit in the paper's data but not foregrounded in its narrative.

## Suggestions

1. Revise the abstract and conclusion to qualify SOTA claims precisely (e.g., "SOTA among LIF-based models without attention, multi-compartment, or GRU mechanisms").
2. Run PS-MNIST over 3–5 seeds with error bars.
3. Add a visualization/analysis of learned delay distributions (histogram or heatmap).
4. Add an ablation of the σ annealing schedule.
5. Report training time and memory usage vs. baseline RSNNs.

## Score and Decision

### Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| DeNN (delay networks) | pIJR9uPjy3.md | 4.50 | R1 | Yes | DeNN had major exposition issues and unclear methodology; DelRec is clearly stronger |
| Layer Sync | 6iM7mmVhXh.md | 5.75 | R1 | Yes | Mixed reviews (3–8); DelRec is more consistent |
| DeepTAGE | drPDukdY3t.md | 6.25 | R1 | Yes | Extensive large-scale experiments; DelRec comparable on SNN-specific benchmarks |
| TS-LIF | rDe9yQQYKt.md | 6.00 | R2 | Yes | Uniform 6 across reviewers; DelRec has clearer motivation but similar weakness severity |

### Final Score Rationale

**Round 1 bracket:** 5.5–6.5.

This paper's net weighted-item profile is comparable to TS-LIF (6.00) and DeepTAGE (6.25). DelRec's strengths (novel first SGL method for recurrent delays, clean method, competitive LIF-based results) are genuine and well-weighted. Its most impactful weakness items (SOTA framing at -2.85, narrow support for recurrent-vs-feedforward claim at -3.10, missing delay distribution analysis at -2.57) are fixable framing and missing analyses rather than methodological flaws. No fatal weaknesses are present. The paper lacks the large-scale experiments of DeepTAGE but surpasses the clarity and soundness of the DeNN anchor (4.50). The closest match is TS-LIF (6.00), where the severity of weaknesses is similar but DelRec has clearer motivation. I therefore place DelRec at 6.0—a borderline accept: solid methodological contribution with framing issues that must be corrected.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>