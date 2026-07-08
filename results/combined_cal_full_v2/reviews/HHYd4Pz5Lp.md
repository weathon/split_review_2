Now I have all the information needed. Let me produce the final review.

## Summary

This paper introduces DelRec, the first surrogate gradient learning (SGL) method to train per-neuron continuous delays in recurrent connections of spiking neural networks. DelRec uses a differentiable triangle interpolation with an annealed width parameter (borrowed from DCLS) to handle non-integer delays during training, and a scheduling matrix to efficiently implement delayed recurrent inputs. The method achieves new SOTA on SSC (82.58% with 0.37M parameters using simple LIF neurons) and PS-MNIST (96.21%), while matching SOTA on SHD. A controlled ablation study on SHD isolates the contribution of recurrent delays and shows they outperform learned feedforward delays at low parameter counts.

## Strengths

- **Well-motivated gap.** The paper correctly identifies that prior work on learned delays in SNNs has focused almost exclusively on feedforward connections, and that the only prior SGL-based method for recurrent delays (ASRC-SNN) learns a single per-layer discrete delay via softmax selection, leaving per-neuron continuous recurrent delays as an open problem. **[weight=7.61]**

- **Clean and principled method.** The differentiable interpolation via a triangle function with annealed σ (borrowing from DCLS/DCLS-Delays) is a natural fit for the recurrent setting. The scheduling matrix formulation (Eqs. 8–11, Algorithm 1) is clearly described, and the area-preserving property of the triangle kernel (Eq. 9) is a nice property. The method is compatible with any spiking neuron model fitting the Eq. 1–3 formalism. **[weight=10.15]**

- **Genuinely strong results on SSC.** The main result — 82.58% ± 0.08% on SSC with only 0.37M parameters using simple LIF neurons — is a clear improvement over prior work in the same model class. DCLS (the leading feedforward-delay method) achieves 80.69% with 2.5M params; SE-adLIF achieves 80.44% with 1.6M params; ASRC-SNN achieves 81.54% with 0.37M params. DelRec's improvement is both in accuracy and parameter efficiency. **[weight=11.30]**

- **Informative ablation on SHD.** The controlled comparison in Section 3.2 — where model size is scaled down to ~10k parameters and architectures are equated — is the right way to isolate the contribution of recurrent delays. The finding that learned recurrent delays outperform learned feedforward delays at low parameter counts (Fig. 3C) is the paper's most interesting empirical contribution beyond SOTA numbers. **[weight=10.12]**

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **SHD "SOTA" claim contradicted by the paper's own Table 2.** Line 178 states "our models achieve state-of-the-art performance on SHD," but Table 2 (ranked by accuracy) shows DelRec's best variant (Rec. and Ff. delays, 93.73%) below both DCLS (93.77%) and SE-adLIF (2L) (93.79%). The abstract more cautiously says "match the SOTA," which is accurate. The difference is within overlapping error bars, and the paper discusses SHD saturation, so the issue is a wording overclaim rather than a substantive one, but it should be corrected. **[weight=4.69]**

- **PS-MNIST evaluation is incomplete in three ways.** (1) Only one seed is used — the paper acknowledges this by citing prior practice, but single-seed results on a 10k-image test set risk being non-representative. (2) The combined (Rec. + Ff. delays) variant — which the paper advertises as a contribution ("first to combine the optimization of feedforward delays... and delays in recurrent connections") — is not reported for PS-MNIST, leaving the reader unable to assess whether the combination helps on this task. (3) DCLS, a key feedforward-delay competitor included on SSC, is absent from the PS-MNIST portion of Table 1, making it harder to assess the relative contribution of recurrent delays on this task. **[weight=1.86]**

- **The comparison with ASRC-SNN — the closest prior work — lacks the ablation needed to understand why DelRec improves upon it.** ASRC-SNN also uses SGL and recurrent delays, and the paper's implementation builds on Xu et al.'s code. The differences (per-neuron vs. per-layer, continuous vs. discrete selection, triangle interpolation vs. softmax annealing) are described only briefly (line 30) and never isolated. Since the improvement over ASRC-SNN is modest (~1% on SSC, ~0.44% on PS-MNIST), a controlled ablation (e.g., running DelRec's triangle interpolation in ASRC-SNN's per-layer discrete framework) would substantially strengthen the claim. **[weight=5.30]**

- **No computational or memory cost analysis for the scheduling matrix.** The buffer dimension scales with max(d)+σ (Eq. 13), which could be non-trivial for long sequences with large learned delays. Without quantifying wall-clock time or GPU memory versus a vanilla RSNN, practitioners cannot assess the cost-benefit tradeoff. **[weight=5.69]**

- **The claim that recurrent delays "mitigate gradient challenges by implementing temporal skip connections" (Fig. 1B, line 22) is never empirically verified.** This is a plausible mechanism, but a simple gradient norm comparison during training on a controlled task would directly test it and is absent. **[weight=3.96]**

### Trivial
None.

## Nice-to-Haves

- A comparison of fixed random recurrent delays versus learned recurrent delays in the ablation (Fig. 3B) shows that even fixed random delays (~78%) substantially outperform a vanilla RSNN (~60%). This suggests that the advantage partly comes from the architectural inductive bias of longer skip connections in the unrolled graph, beyond learning specific delay values. The paper does not discuss this distinction.

## Removed Points

These points were flagged by the harsh critic but are removed with justification:

- **"Fixed random recurrent delays already outperform learned feedforward delays at 10k parameters":** Factually wrong. Figure 3B shows fixed recurrent delays at ~78% and learned feedforward delays at ~80%. The paper's data shows the opposite of what was claimed.
- **Large-σ discussion about gradient signal-to-noise ratio:** Not a weakness — the paper already acknowledges the loose optimization on long time scales (line 122). An observation about the method's behavior, not a substantiated flaw.
- **"Stateless synapses caveat":** The paper explicitly tracks which models use LIF neurons in all tables. The synaptic model distinction is already controlled for via the "LIF" column. 
- **"Axonal delay limitation should be acknowledged more explicitly":** The paper already states "for simplicity, we assume an identical delay... referred to as 'axonal delay'... we will use this setting in all our experiments. Yet our method/code is also compatible with synaptic delays" (line 74). This is adequately acknowledged.
- **Pure formatting/style nitpicks:** Parser artifacts, not author errors.

## Novel Insights

The harsh critic's observation about the architectural inductive bias of recurrent delays is worth noting: even *fixed random* recurrent delays (Fig. 3B, ~78% at 10k params) substantially outperform a vanilla RSNN (~60%), suggesting that simply having longer skip connections in the unrolled computational graph is beneficial independent of learning specific delay values. The paper attributes the benefit of recurrent delays primarily to learning, but the fixed-delay baseline suggests a confound. This does not invalidate the paper's contribution (learned recurrent delays still outperform fixed ones), but it would be valuable for the paper to acknowledge and discuss this distinction.

Otherwise, none beyond the paper's own contributions.

## Suggestions

1. Correct the SHD "SOTA" claim in the main text (line 178) to match what Table 2 actually shows: "competitive with SOTA" or "within error bars of SOTA."
2. Complete the PS-MNIST evaluation by running the combined (Rec. + Ff.) variant and reporting results over multiple seeds.
3. Add an ablation comparing DelRec's per-neuron continuous delay formulation against ASRC-SNN's per-layer discrete delay selection within the same architecture and training setup.
4. Report wall-clock time and GPU memory versus a vanilla RSNN baseline to quantify the overhead of the scheduling matrix.
5. Add empirical gradient-norm comparisons to support the claim about gradient mitigation via temporal skip connections.

## Score and Decision

**Calibration summary.** Round 1 bracketed the paper between 6.0 and 8.0. Round 2 narrowed by comparing weighted items against itemized anchors. The closest SNN-method anchors were Temporal Flexibility in SNNs (6.20, accept) and DeepTAGE (6.25, accept). Both have lower-strength profiles (max positive weights ~11-12 vs. DelRec's 11.30) **and** carry at least one heavy weakness (Temporal Flexibility had a weight-9.20 weakness about missing complexity analysis; DeepTAGE had weight-7.48 and weight-7.64 weaknesses). DelRec's weaknesses max out at weight-5.69 and none are fundamental. ST-DANO (5.75, reject) had a severe missing-baseline weakness (weight -4.15). The ensemble-perspective SNN paper (5.50, accept) had weaker empirical contributions. DelRec's SSC result (82.58% with 0.37M params, 3 seeds) is the strongest anchor-relative evidence, putting it above the 6.2–6.25 band. The paper does not reach the 8.0 band (reserved for papers like Oscillatory SSM or Brain Bandit, which had all-8 scores and no contested claims). **Final score: 7.0 — a solid accept with minor, addressable issues.**

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>