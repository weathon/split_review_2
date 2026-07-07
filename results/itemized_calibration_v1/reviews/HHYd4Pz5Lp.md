Now I have all the information needed. Let me write the final consolidated review.

## Summary

DelRec introduces a method for learning *per-neuron continuous delays* in recurrent connections of spiking neural networks (SNNs) using surrogate gradient learning (SGL). The method uses differentiable triangle-function interpolation with an annealed width parameter to handle non-integer delays and a scheduling matrix with a pointer mechanism to manage memory efficiently. DelRec achieves state-of-the-art accuracy on SSC (82.58±0.08% with simple LIF neurons, 3 seeds) and PS-MNIST (96.21%) while matching SOTA on SHD. A controlled ablation study on SHD (Fig. 3) compares six model variants and provides insight into how recurrent delays improve temporal processing.

## Strengths

1. **Genuinely novel and well-engineered method.** DelRec is the first SGL-based method to learn per-neuron continuous delays in recurrent SNN connections. The differentiable interpolation with annealed σ (Eq. 9–11) is a principled extension of the DCLS feedforward-delay approach (Hammouamri et al., 2024) to the recurrent setting. The scheduling matrix with pointer mechanism (Algorithm 1) is a practical solution that avoids unbounded memory growth and does not require pre-defining a maximum delay range — a genuine advantage over discrete-search approaches (e.g., Xu et al.'s softmax over a fixed delay set).

2. **Credible SOTA on SSC with simple LIF neurons.** DelRec (recurrent-only, 0.37M params, LIF) achieves 82.58±0.08% on SSC, surpassing SiLIF (82.03±0.25%, 0.35M params) which uses a more complex SSM-based neuron model. The improvement (0.55%) exceeds combined error margins with low variance across 3 seeds. This cleanly demonstrates that the delay mechanism itself — not neuron complexity — is driving the improvement.

3. **Well-designed ablation study on SHD (Fig. 3).** The six-model comparison (vanilla SNN, vanilla RSNN, fixed random recurrent delays, learned feedforward delays, learned recurrent delays, both) under controlled parameter counts is the strongest part of the experiments. Finding that even *random fixed* recurrent delays improve over vanilla RSNN (Fig. 3B), and that learned recurrent delays outperform feedforward delays under low-parameter constraints (Fig. 3C), provides genuine mechanistic insight: recurrent delays act as temporal skip connections that improve gradient flow.

4. **Open and reproducible.** Anonymous repository provided, builds on SpikingJelly, uses public datasets, hyperparameters in appendix.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **PS-MNIST result lacks variance estimate.** The 96.21% result is from a single seed (line 132: "we only test one seed as all the previous state-of-the-art models on the dataset"). While this follows convention on this benchmark, it means the 0.44% improvement over ASRC-SNN (95.77%, also single seed) cannot be assessed for statistical reliability. Since PS-MNIST is one of two headline SOTA claims, the lack of replication weakens the result.

2. **Inconsistent SHD SOTA claim.** The paper states "our models achieve state-of-the-art performance on SHD" (line 178), but Table 2 shows DCLS (93.77%) and SE-adLIF 2L (93.79%) above DelRec's best (93.73%). The paper then pivots to argue SHD is "saturated" with overlapping confidence intervals (line 176). This framing reversal is confusing and overstates the contribution on SHD. The abstract's phrasing ("match the SOTA") is accurate; the body should be consistent.

3. **Recurrent vs. feedforward delay advantage is regime-dependent.** The paper claims "recurrent delays can achieve better performance than feedforward delays" (conclusion, line 233, also line 166). This is supported in the small-model SHD study (Fig. 3C, ~10k params) and by comparing DelRec recurrent-only (82.58%) against DCLS feedforward (80.69%) on SSC. However, on large-model SHD (Table 2), DCLS feedforward (93.77%) outperforms DelRec recurrent-only (93.39%). The paper acknowledges regime dependence only implicitly; the conclusion should state it explicitly.

4. **Non-monotonic effect of combining delay types is unexplained.** On SSC, DelRec with *both* feedforward and recurrent delays (82.19±0.16%) underperforms the recurrent-only variant (82.58±0.08%). This is an interesting and potentially informative result, but the paper offers no discussion of why adding feedforward delays *hurts* — whether due to overfitting, competing mechanisms, or redundant capacity (Table 1, lines 147–148).

### Trivial

None.

## Nice-to-Haves

- **Analysis of learned delay values.** The paper learns per-neuron delays but never shows what delays are actually learned — clustering patterns, layer-specific values, or relationship to dataset timescales. This would provide direct validation that the method learns meaningful temporal structure.
- **Sensitivity to the σ annealing schedule.** Performance depends on how σ is decreased over training, but no ablation is provided. Since the triangle interpolation and its annealing are core to the method, this is a notable omission.
- **Computational cost reporting.** Training time, inference time, or memory usage relative to a vanilla RSNN would help readers assess the practical trade-off introduced by the scheduling matrix.

## Removed Points

- **"SOTA claim is narrower than abstract suggests"** — The abstract claims SOTA on *two* datasets (SSC, PS-MNIST) and "match" on SHD, which is factually accurate. The exclusion of multi-compartment models (Chen et al., 2024: 97.78% on PS-MNIST) is explained in a footnote (line 162) with a reasonable justification. This is a scope choice, not a flaw. The criticism overstates the problem.
- **"First SGL-based method claim may be incorrect"** — Xu et al. learned a *single per-layer* delay from a discrete set via softmax. DelRec learns *per-neuron continuous* delays. The paper's distinction is clear and meaningful. The "first" claim in the abstract ("first SGL-based method to train axonal or synaptic delays in recurrent spiking layers") is accurate given these differences.
- **"Computational cost not discussed"** — This is a nice-to-have, not a weakness. The paper partially addresses it via the scheduling matrix dimension analysis (Eq. 12–13).
- **Various formatting/style nitpicks** — These are parser artifacts, not author errors.

## Novel Insights

The most interesting observation emerging from the review is the **regime-dependent effectiveness of recurrent vs. feedforward delays**: recurrent delays excel in low-parameter settings (Fig. 3C) but feedforward delays match or exceed them in large-model settings (Table 2: SHD). This tension, combined with the unexplained finding that combining both delay types *hurts* on SSC (82.19% vs. 82.58%), suggests that feedforward and recurrent delays may compete for limited representational capacity rather than complementing each other. This is a scientifically rich question that the paper does not explore.

## Suggestions

1. **Add variance estimates for PS-MNIST** (3–5 seeds) to confirm the improvement over ASRC-SNN is statistically reliable. This directly affects the credibility of the headline SOTA claim.
2. **Correct the SHD SOTA claim** in the body text (line 178) to say "competitive with SOTA" or "matching SOTA" — consistent with the abstract and Table 2.
3. **Acknowledge the regime dependence explicitly** in the conclusion: recurrent delays outperform feedforward delays in low-parameter settings, but the advantage is not universal.
4. **Discuss the combined-model underperformance on SSC** — this is the most interesting unexplained result in the paper and deserves analysis.
5. **Consider adding a visualization of learned delays** (e.g., histogram or layer-wise heatmap) and an ablation of the σ annealing schedule.

## Score and Decision

**Calibration anchors used (all from the 5.5–7.5 band):**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Delay Neural Networks | pIJR9uPjy3.md | 4.50 | R1 | Yes | Similar topic (delays in SNNs) but major exposition/technical issues. DelRec is significantly stronger. |
| Forward Gradient Training | yBP36xQhZl.md | 5.00 | R2 | Yes | Novelty concerns, limited experiments. DelRec has clearer contribution and better results. |
| Layer Synchronization | 6iM7mmVhXh.md | 5.75 | R1 | Yes | Clarity issues. DelRec is better written and more focused. |
| Spatio-Temporal Neuron Opt. | eN4g4cjFX1.md | 5.75 | R2 | Yes | Missing comparisons, limited ablations. DelRec has stronger empirical design. |
| TS-LIF | rDe9yQQYKt.md | 6.00 | R2 | Yes | Neuron model for time series. DelRec has cleaner contribution but narrower evaluation. |
| Temporal Flexibility / MTT | 9HsfTgflT7.md | 6.20 | R2 | Yes | Comprehensive experiments including neuromorphic chips. DelRec has clearer method. |
| **DeepTAGE** | **drPDukdY3t.md** | **6.25** | **R1** | **Yes** | **Most comparable: SNN training method, solid experiments, minor issues. DelRec is in the same tier.** |
| Barrel Cortex Model | UvfI4grcM7.md | 6.75 | R1 | No | Different paper type (biological modeling); not directly comparable. |

**Round 1 bracket:** 5.75–7.0. The paper is well above the 4.50–5.00 anchors (which have exposition or novelty issues DelRec does not share) and is most comparable to DeepTAGE (6.25). **Round 2 narrowing** confirmed this: against TS-LIF (6.00) and MTT (6.20), DelRec is comparable — cleaner method and better ablation than TS-LIF, less comprehensive hardware experiments than MTT. The shared heavyweight items are: strong method novelty (+3/+4 equivalent) and credible results against the field's SOTA. The missing heavyweight items are: PS-MNIST variance (a -2 equivalent that DeepTAGE and MTT do not have) and the SHD framing inconsistency (a -1 equivalent).

The method is genuinely novel, the SSC result is well-supported (3 seeds, low variance), and the ablation study is informative. The weaknesses are minor and addressable in revision — primarily a missing variance estimate on PS-MNIST and some framing inconsistencies. The paper does not have any major or fatal flaw.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>