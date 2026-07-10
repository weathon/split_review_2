## Summary

This paper introduces DelRec, the first surrogate gradient learning (SGL) method to train axonal or synaptic delays in recurrent connections of spiking neural networks. The method extends DCLS's triangle-interpolation approach to the recurrent setting via a scheduling buffer mechanism that allows non-integer delays to be optimized during training and rounded to integers at inference. DelRec achieves 82.58% on SSC (Spiking Speech Commands) — a new SOTA among LIF-based models — and 96.21% on PS-MNIST (single seed), while matching SOTA on the saturated SHD dataset. The paper also presents a controlled ablation study showing that learned recurrent delays provide particular benefits in low-parameter regimes.

## Strengths

- **Novel and well-engineered method.** The scheduling buffer mechanism (Section 2.2, Eq. 8–13) is a clean, non-trivial adaptation of the DCLS triangle-interpolation approach to the recurrent setting. The key technical challenge — that recurrent delays require projecting spikes forward to future time steps whose positions depend on both the learned delay and the annealing schedule — is addressed with an elegant pointer-buffer mechanism that exploits the finite support of the triangle function. The code is provided and the method is compatible with any spiking neuron model.

- **SOTA on SSC with simple LIF neurons.** The 82.58% (±0.08%) on Spiking Speech Commands using only vanilla LIF neurons and 0.37M parameters (3 seeds) is a genuine advance. Prior LIF-based methods (DCLS at 80.69%, EventProp at 76.1%) are clearly below, and the gap to SiLIF (82.03%) is statistically meaningful. This is the paper's most convincing empirical result.

- **Methodologically rigorous handling of SHD.** The paper correctly identifies that SHD is saturated, uses a clean train/validation/test split with 20% of the training set held out, reports 10 seeds, and explicitly discusses why further improvements on SHD are unlikely to be statistically significant given the small test set (2264 samples). This is better practice than most prior work on this dataset.

- **Informative low-parameter ablation study.** The controlled comparison on SHD with models ≤10k parameters (Fig. 3C) provides meaningful evidence that recurrent delays confer advantages when representational capacity is limited. The firing-rate analysis adds a nuanced energy-efficiency trade-off discussion. This ablation genuinely tests the claimed benefit of the method rather than only showing it on large models.

## Weaknesses

### Major

- **Abstract overclaims that recurrent delays outperform feedforward delays.** The abstract states definitively "We show that trainable recurrent delays outperform feedforward ones," but the evidence is mixed across settings. On SHD (Table 2), DCLS (feedforward delays only) achieves 93.77% while DelRec (Rec. delays only) achieves 93.39% — the central tendency favors feedforward, even if within confidence intervals. On SSC, adding feedforward delays to recurrent delays *hurts* performance (82.58% → 82.19%), a result the paper does not discuss. The strongest support for the claim comes from the low-parameter regime (Fig. 3C). The body of the paper uses more cautious language ("may yield greater benefits," "suggesting that"), but the abstract is unqualified. This should be corrected.

- **PS-MNIST SOTA claim rests on a single seed.** The 96.21% result on PS-MNIST is reported without variance because "we only test one seed as all the previous state-of-the-art models on the dataset" (line 132). This justification is not scientifically sufficient — if prior work also used single seeds, that is a weakness to improve upon, not to replicate. Three additional seeds could plausibly fall below the prior SOTA of 95.77%. Without an error estimate, this result cannot be evaluated at the standard expected for a SOTA claim.

### Minor

- **No discussion of why combining recurrent and feedforward delays degrades performance on SSC.** DelRec (Rec. delays only) achieves 82.58% while DelRec (Rec. and Ff. delays) achieves 82.19% — a 0.39 percentage point drop (~2–3× the SEM of the rec-only variant). This is a counterintuitive result directly relevant to the paper's central claim and should be explained (e.g., overfitting from additional parameters, optimization interference, or architectural imbalance).

- **Missing complexity/memory analysis.** The scheduling buffer (Eq. 10–13) has computational and memory costs that scale with the maximum delay and buffer size. A brief discussion of O(T·N·max_delay) complexity and how buffer size evolves as σ anneals would help readers assess practical deployment costs.

- **No analysis of learned delay values.** The paper reports no analysis of what delays are actually learned — their distribution, convergence across seeds, or relationship to task-relevant temporal scales. Such analysis would provide insight into the mechanism (e.g., do delays cluster around values corresponding to task-relevant temporal scales? Do they converge consistently across runs?).

### Trivial

None.

## Nice-to-Haves

- A gradient analysis (even a simple one measuring gradient norms with vs. without delays) would substantiate the gradient-mitigation intuition presented in Fig. 1B.
- A discussion of which neuromorphic platforms support programmable delays and how DelRec's rounded integer delays map to specific hardware would strengthen the hardware-deployment motivation.

## Removed Points

These points from the input review were removed with justification:

- **Novelty concern about DCLS relationship** — Removed. The paper properly acknowledges DCLS as prior work. The scheduling buffer is a genuine architectural adaptation for the recurrent setting, and the claim "first SGL-based method for recurrent delays" is factually correct.
- **Gradient analysis request for Fig. 1B** — Removed. The figure presents an intuition/motivation ("reduces the risks"), not an empirical claim. Demanding a full gradient analysis is scope creep for this paper.
- **Missing related works** — Removed. Cannot be independently verified.
- **Formatting/style nitpicks (missing year on Xu et al., Vanilla RNN 40% accuracy concern)** — Removed. The missing year is a citation convention; the 40% RNN accuracy is attributed to known gradient issues and is a reasonable baseline.
- **SOTA bounded by LIF-only comparison** — Removed. The paper is transparent about this boundary in a footnote and the comparison set is clearly defined.
- **ASRC-SNN reference without a year** — Removed. Citation style issue, not substantive.
- **Hardware discussion** — Moved to Nice-to-Haves as it's beyond the paper's stated scope.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add multi-seed results for PS-MNIST.** Run 3+ seeds and report mean ± std. This is the single most impactful fix.
2. **Qualify the abstract's claim.** Replace "trainable recurrent delays outperform feedforward ones" with language reflecting the mixed evidence (e.g., "can outperform in low-parameter regimes" or "show competitive or better performance").
3. **Analyze the SSC combined-delays degradation.** Explain why adding feedforward delays hurts — is it overfitting from more parameters? Optimization interference? This analysis could itself be a useful finding.
4. **Add a brief complexity analysis.** One paragraph quantifying O(T·N·max_delay) costs and how the buffer size shrinks as σ anneals.
5. **Report learned delay distributions.** Even a simple histogram showing learned delay values across seeds would add insight.

## Score and Decision

**Calibration summary:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| DeNN | pIJR9uPjy3.md | 4.50 | R1 | Yes | More radical approach (delay-only, no weights) but weaker results and clarity issues. DelRec is stronger. |
| SOLO | vq75kRCYuY.md | 4.00 | R1 | Yes | Online SNN training with accuracy drops. DelRec has stronger results. |
| FGT | yBP36xQhZl.md | 5.00 | R1 | Yes | Forward gradient SNN training; similar novelty/overclaim concerns. DelRec has better SOTA results. |
| Layer Sync | 6iM7mmVhXh.md | 5.75 | R2 | Yes | SNN asynchrony paper; comparable quality but different domain. |
| DeepTAGE | drPDukdY3t.md | 6.25 | R1 | Yes | SNN gradient enhancement; accepted. Similar quality but fewer overclaim issues. |
| Temporal Flex. | 9HsfTgflT7.md | 6.20 | R2 | Yes | SNN time-step flexibility; accepted. Comparable quality with similar overclaim concerns. |
| Signed Rate Enc. | qLh6Ufvnuc.md | 6.33 | R2 | Yes | SNN encoding method; accepted. Stronger theoretical foundation. |

**Round 1 bracket:** [4.0, 7.5] — DelRec is clearly above the 4.0–5.0 papers (DeNN, SOLO, FGT) due to its sound method and strong SSC result. It sits below the 8.0 papers which have more thorough evaluation or stronger theoretical contributions.

**Round 2 narrowing:** Inside the bracket, DelRec is closest to DeepTAGE (6.25, accept) and Temporal Flexibility (6.20, accept). DelRec's SSC result and ablation study are comparable strengths, but the PS-MNIST single-seed issue and the unqualified abstract claim are more significant weaknesses than those papers had. The paper's core method is sound and the SSC result is solid, placing it just above the acceptance threshold.

**Final score: 6.0.** This reflects a borderline accept: a solid method with a clear contribution (first SGL-based recurrent delay learning, strong SSC result, informative ablation), held back by the single-seed PS-MNIST SOTA claim and an overclaimed abstract that should be qualified.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>