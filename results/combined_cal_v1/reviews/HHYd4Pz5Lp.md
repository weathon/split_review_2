Now I have a solid calibration. Let me produce the final review.

## Summary

This paper introduces DelRec, a method for learning delays in recurrent connections of spiking neural networks using surrogate gradient learning and backpropagation. It extends the DCLS feedforward delay-learning approach to the recurrent setting using a differentiable triangular-spread interpolation coupled with an annealing schedule, packaged into a scheduling-matrix formulation that handles the "future-oriented" bookkeeping problem. Evaluated on SSC, PS-MNIST, and SHD, the method achieves SOTA on SSC (82.58±0.08% with 3 seeds) using only simple LIF neurons, and presents a well-controlled ablation study on SHD showing that learned recurrent delays degrade more gracefully under low-parameter constraints than alternatives.

## Strengths

- **Well-motivated and timely problem.** The paper correctly identifies that prior work on delays in SNNs has focused almost exclusively on feedforward connections, while recurrent delays — which could support self-sustained activity, polychronization, and temporal skip connections — have been largely neglected. The biological grounding (plastic myelin, Izhikevich's theoretical results) is clearly articulated.
- **Technically clean method.** The differentiable interpolation via the triangular spread function $h_{\sigma,d}(\tau)$ coupled with an annealing schedule on $\sigma$ is a natural and principled extension of DCLS (Hammouamri et al., 2024) to the recurrent setting. The scheduling matrix formulation (Eq. 8–11) correctly handles the "future-oriented" bookkeeping problem, which is a genuine algorithmic contribution — adapting feedforward delay learning to the recurrent case is nontrivial because each neuron's spike feeds back onto itself and its neighbors with a self-consistent temporal offset.
- **Clear ablation study on SHD (small-model regime, Section 3.2).** Comparing 6 configurations (vanilla SNN, vanilla RSNN, fixed random recurrent delays, learned feedforward delays, learned recurrent delays, both) across varying parameter counts (2k–10k) cleanly isolates the effect of each delay type. The result that learned recurrent delays degrade more gracefully than alternatives as parameter count shrinks (Fig. 3C) is a genuinely informative finding, not just a SOTA chase.
- **Strong SSC result with multiple seeds.** On SSC, DelRec achieves 82.58 ± 0.08% with only recurrent delays (3 seeds), outperforming prior best (SiLIF at 82.03 ± 0.25%). The improvement (~0.55 pp) is modest but consistent given the tight error bars. This is the paper's most defensible headline result.
- **Uses simple LIF neurons throughout.** The paper does not rely on complex neuron models (adaptive, multi-compartment, attention-based) to achieve its results. This strengthens the claim that the benefit comes from delays, not from auxiliary neuron dynamics.

## Weaknesses

### Fatal
None.

### Major

- **The paper never addresses its own counterintuitive finding that recurrent-only delays (82.58±0.08%) outperform the combination of recurrent and feedforward delays (82.19±0.16%) on SSC (Table 1), with non-overlapping error bars.** This contradicts the paper's stated expectation that combining both delay types could further improve performance. The paper recommends combining both delay types in the conclusion while its own best SSC result uses recurrent delays alone. When the paper's own best evidence contradicts its recommendation, this silence is a significant omission that needs either an explanation or an honest acknowledgment as an open question.

- **The PS-MNIST SOTA claim (96.21%, +0.44 pp over ASRC-SNN's 95.77%) rests on a single seed.** The paper's rationale (line 132) that "all the previous state-of-the-art models on the dataset" used one seed is not a valid justification — prior weak practice does not excuse repeating it. Without multiple seeds, the 0.44 pp margin could be noise rather than a real improvement. Given that the SSC results required 3 seeds to establish significance, the inconsistency in statistical rigor is problematic for a claimed SOTA result.

### Minor

- **The claim of "state-of-the-art performance on SHD" (line 178) is overstated.** In Table 2, DelRec (Rec.+Ff. delays) achieves 93.73±0.69%, ranking below SE-adLIF 2L (93.79±0.76%) and DCLS (93.77±0.68%). While all differences are within error bars, "state-of-the-art" implies the best, not within noise of the best. The paper correctly de-emphasizes SHD as saturated, but the SOTA language should be removed or qualified.

- **No analysis of computational overhead.** The scheduling matrix has dimension $N \times \dim(\tilde{\mathbb{E}}(\sigma, D))$, which could be substantial at the start of training when $\sigma=5$. The paper never reports training time, GPU memory, or wall-clock speed compared to baselines. For a methods paper whose conclusion mentions neuromorphic deployment, this omission limits practical assessment.

- **No analysis of learned delay distributions.** What delay values do the networks actually learn? On SSC, are the learned $d_j$ values clustered around specific offsets, spread widely, or consistent across seeds? Do they correlate with weight magnitudes? This analysis would strengthen the claim that the method learns meaningful temporal parameters rather than just benefiting from extra degrees of freedom.

- **No sensitivity analysis for the $\sigma$ annealing schedule.** The initial $\sigma=5$ and the annealing rate are not ablated. Since $\sigma$ controls the gradient propagation range, this is a nontrivial hyperparameter whose behavior is not characterized.

### Trivial
None.

## Nice-to-Haves

- A comparison against Mészáros et al. (2025) on a matched architecture (same layer sizes, same neuron model) would help establish whether the SGL-based approach to recurrent delay learning offers advantages beyond architectural differences.
- An analysis of why random fixed recurrent delays help more than one might naively expect (Fig. 3B) would strengthen the mechanistic understanding.

## Removed Points

These points from the input review were flagged for removal; treat them with caution:
- **"Fixed random recurrent delays outperforming learned feedforward delays is an interesting result"** — REMOVED: Factually incorrect. Figure 3B shows learned feedforward delays at ~80% and fixed recurrent delays at ~78%. The comparison is reversed from what the reviewer stated.
- **"Algorithm 1 is referenced but not included in the main text"** — REMOVED: Parser artifact. The appendix (containing Algorithm 1) was stripped during PDF extraction; it exists in the original submission.
- **"Table 1 formatting uses an unusual marker"** — REMOVED: Parser artifact, not a paper issue.
- **"No comparison against Mészáros et al. in controlled setting"** — The parameter count mismatch (~5M vs 0.37M) makes this comparison nontrivial; omission is scope-appropriate.
- Missing related works concerns — REMOVED as per hard rules (cannot verify existence of uncited works).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run multiple seeds (3–5) for PS-MNIST** and report mean ± std. This single change would either confirm the SOTA claim or reveal the margin as noise, and either outcome is informative.
2. **Directly address the Rec-only > Rec+Ff finding on SSC.** Possible explanations to explore: (a) feedforward delays increase model capacity and hurt generalization on a fixed dataset size, (b) gradient interference between the two delay types, (c) statistical artifact. Even acknowledging the puzzle would resolve the current internal inconsistency.
3. **Remove or qualify the "state-of-the-art on SHD" language** to reflect the method's actual rank in Table 2.
4. **Report training-time/GPU-memory overhead** of the scheduling matrix mechanism relative to a vanilla RSNN baseline.
5. **Add analysis of learned delay distributions** (e.g., histograms of $d_j$ values across neurons and seeds on SSC) to support the claim that meaningful temporal parameters are being learned.

## Calibration

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| DeNN | pIJR9uPjy3.md | 4.50 | R1 | Yes | Delay-based SNN with clarity and comparison issues; this paper is clearer and better validated |
| S-TLLR | vlQ56aWJhl.md | 5.00 | R1 | Yes | Local learning SNN with novelty/experimental concerns; this paper has a cleaner contribution |
| Forward Gradient Training | yBP36xQhZl.md | 5.00 | R1 | Yes | SNN training with scalability concerns; this paper has stronger empirical validation |
| Temporal Flexibility SNN | 9HsfTgflT7.md | 6.20 | R1 | Yes | Real-hardware deployment validation, but had problem-method alignment gaps; this paper has a tighter scope but fewer deployment experiments |
| Layer Synchronization SNN | 6iM7mmVhXh.md | 5.75 | R2 | Yes | Polarizing paper on asynchronous SNN; this paper is clearer and less controversial |
| DeepTAGE | drPDukdY3t.md | 6.25 | R2 | Yes | Gradient optimization for SNNs with extensive ImageNet experiments; this paper has a narrower but cleaner contribution with weaker negatives overall |
| Spatio-Temporal Dependency | eN4g4cjFX1.md | 5.75 | R2 | Yes | Neuron optimization with major missing-related-work issue; this paper's weaknesses are less severe |

**Round 1 bracket:** 5.0–6.5 (after comparing weighted items: positive strengths comparable to DeepTAGE and Temporal Flexibility, but the two major negatives at -3.35 each are heavier than typical minor issues in the 6+ papers).

**Final score rationale:** My draft's net weight (+14.3) sits between Layer Synchronization (+8.5, score 5.75) and DeepTAGE (+24, score 6.25). The paper shares DeepTAGE's well-motivated methodological contribution and strong empirical core, but lacks its large-scale validation and has more severe unaddressed issues. It avoids the fatal clarity/novelty problems that dragged down DeNN (4.5), S-TLLR (5.0), and FGT (5.0). A score of 6.0 reflects a borderline-accept paper with genuine contributions that needs revision on presentation and rigor.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>