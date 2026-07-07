Now let me synthesize my findings into a final review.

**Round 1 Bracket: 4.5 – 6.0**

My analysis of anchors:
- **SpikeZIP (3.60)**: Very similar topic (ANN-QANN-SNN conversion), rejected for novelty concerns. Current paper is stronger — addresses LLM-specific scaling problem, cleaner theory, genuinely novel calibration. Should score above this.
- **QAC (5.75)**: Similar core idea (quantization ↔ timesteps connection), rejected. Shared weakness: "why not just use the QANN?" Current paper has slightly stronger motivation.
- **Error-Free ANN-to-SNN (5.75)**: Stronger theory and ImageNet results but rejected for limited novelty and data inconsistencies.
- **SpikeBERT (6.33)**: Spiking for language, rejected despite high scores — energy reduction was only theoretical, similar to this paper's core issue.
- **Spatio-Temporal (7.00)**: Accepted SNN conversion for Transformers — more comprehensive evaluation and direct energy analysis.

The current paper's genuine contributions (IS neuron for LLMs, parameter-efficient calibration) place it well above SpikeZIP's 3.60, but the missing energy evaluation, limited experimental scope, and underspecified calibration details keep it below the 5.75–6.33 anchors that were also rejected. I narrow to **5.5**.

Here is the final consolidated review:

---

## Summary

This paper proposes a dual ANN-to-SNN conversion framework for LLMs that uses a pre-trained quantized LLM (via PrefixQuant) as the starting point rather than training a conversion-friendly ANN. The key technical contributions are: (1) an Integer Spiking (IS) neuron with multi-hierarchical thresholds designed to approximate the quantization function, (2) theoretical analysis bounding conversion error (Theorem 3), and (3) a parameter-efficient layer-wise calibration that adjusts only thresholds and initial membrane potentials (0.107K parameters per layer) to correct unevenness error. Experiments on LLaMA-2-7B and LLaMA-3-8B show the calibrated SNN achieves accuracy close to the source quantized model (W6A6), e.g., 67.65% vs 68.70% Avg. Acc. at T=2 on LLaMA-2-7B.

## Strengths

- **Well-motivated problem framing.** The paper correctly identifies that conventional ANN-to-SNN conversion requires training a conversion-friendly ANN, which is prohibitive for LLMs. Using a pre-trained quantized LLM obtained via training-free PTQ as the starting point is a genuinely practical idea that avoids this cost, presented clearly in Sections 1 and 3.2.

- **Clean theoretical connection between quantization and spiking.** Theorems 1 and 2 formally establish conditions under which the IS neuron can approximate the quantization function used in PTQ. The multi-level threshold design is a natural fit for quantized activations, and the relation $LT = 2^n - 1$ elegantly connects threshold levels, timesteps, and bit-width.

- **Parameter-efficient calibration is genuinely useful.** Table 4 shows that adjusting only thresholds and initial membrane potentials (0.107K parameters per layer) achieves better or comparable accuracy to fine-tuning all 202M weights. This is a concrete, practical finding for the SNN community.

- **The ablation is informative.** The gap between "Conversion" (uncalibrated) and "Ours" (calibrated) in Table 2 is dramatic — e.g., on LLaMA-2-7B at T=2, uncalibrated gets 59.99 Avg. Acc. while calibrated gets 67.65. This cleanly demonstrates that the calibration step is doing critical work.

## Weaknesses

### Fatal
None.

### Major

- **Energy-efficiency claims are unsubstantiated.** The entire paper is motivated by enabling energy-efficient LLM deployment on edge devices (abstract: "brain-inspired efficiency and low power consumption"; Section 2.1: quantized ANNs still suffer from "significant energy consumption... due to the power demands of dense matrix multiplication"; contribution 3: "potentially reduces the energy consumption of LLMs"). Yet the evaluation contains **zero** energy/power measurements, zero FLOPs comparisons, zero spike-count analysis, and zero latency benchmarks. Moreover, the IS neuron fires up to L spikes per timestep (L = ceil(2^{n-1}/T), e.g., L≈16 at T=2, n=6), so the spike-based efficiency story is nontrivial. Without any energy characterization, the reader cannot determine why the spiking version should be preferred over the simpler quantized ANN it derives from (which already achieves similar accuracy at 68.70%). The paper's central motivational premise is left untested against its own evaluation.

### Minor

- **Calibration procedure is underspecified for a core contribution.** The paper optimizes $\min_{\theta^k, v^k(0)} \| \sum_{t=1}^T \hat{y}^k(t) - y^k \|$ but provides no details about the optimizer, learning rate, number of calibration steps/epochs, amount of calibration data, how data is partitioned across layers, or initialization for thresholds and membrane potentials. Given that calibration is the key mechanism transforming accuracy (e.g., 59.99→67.65 at T=2), these details are essential for reproducibility. The paper states the overhead is "minimal" without quantifying it.

- **Theoretical error bound and calibration target are slightly misaligned.** Theorem 3 decomposes total conversion error into two terms: (a) per-layer SNN-to-QANN errors (weighted by Lipschitz constants) and (b) per-layer QANN-to-ANN errors. The calibration addresses only term (a) by minimizing $\| \sum_t \hat{y}^k(t) - y^k \|$. The paper states calibration "minimizes the upper bound in Theorem 3," but it actually minimizes only one component of the bound while term (b) (quantization error inherited from PTQ) is left untouched. The framing should be more precise about which error terms the calibration addresses.

- **Performance degradation at larger T is acknowledged but not analyzed.** Accuracy consistently drops as T increases (LLaMA-3-8B: 71.67 at T=1 → 69.03 at T=2 → 67.21 at T=4 → 63.76 at T=8). The paper attributes this to "growing unevenness error" but does not analyze whether the calibration's residual error increases with T, whether the degradation stems from the LT=2^n-1 integer constraint noted in Remark 1, or whether different calibration strategies could mitigate it. This limits understanding of the method's scaling properties.

- **Weight-calibration baseline in Table 4 lacks methodological detail.** Fine-tuning 202M weights yields lower accuracy (66.39) than optimizing 0.107K parameters (67.65) on LLaMA-2-7B at T=2. While this result is plausible with a very small calibration set (overparameterized fine-tuning can overfit), the paper provides no details on the optimization protocol (optimizer, learning rate, steps, data budget, whether the same calibration data were used). Without this, the comparison appears uncontrolled.

- **Limited experimental scope.** Experiments cover only two model families (LLaMA-2, LLaMA-3), one quantization setting (W6A6), and one PTQ method (PrefixQuant). It is unclear whether the method generalizes to other PTQ methods (e.g., QuaRot, SpinQuant), other bit-widths (W4A4), or other model families (OPT, Falcon).

### Trivial

- Figure 3's right y-axis is described as showing MSE loss on a linear scale ranging from -8 to 2. MSE cannot be negative, so the axis description appears erroneous or uses a different metric than stated.

## Nice-to-Haves

- **Energy characterization.** Measure actual spike counts per forward pass at each T setting and estimate energy using established SNN energy models (proportional to spike count × synaptic operations) to directly test the paper's motivational premise.
- **Comparison with trivial SNN baseline.** The QANN produces discrete activations; a trivial baseline would directly use the quantized values as "spike counts" at T=1. Comparing this to the multi-timestep IS neuron approach would justify why temporal dynamics add value.
- **Calibration data budget analysis.** Report how many calibration samples are needed, how sensitive results are to this choice, and the computational overhead of calibration in terms of time and FLOPs.

## Removed Points

The following points from the input review were removed after verification:

1. **"Compares against quantization methods, not spiking methods"** — Removed because the paper's contribution is framed as enabling spiking LLMs that match quantized ones, making the QANN source the natural comparison target. No applicable spiking LLM conversion baselines exist at this scale. Comparing against PrefixQuant and DuQuant directly supports the stated claim of "performance comparable to state-of-the-art quantization techniques."

2. **"Missing related work on SNN energy efficiency metrics"** — Removed per instructions (you do not have complete knowledge of all released work and cannot confirm whether such references exist).

3. **"Weight-calibration baseline is not credible"** — Demoted to Minor and rephrased as "lacks methodological detail" rather than questioning credibility, since the result is plausible with a small calibration set.

4. **"Theory does not connect to calibration"** — Partially merged into Minor but significantly weakened. The calibration targets the SNN-specific error component of Theorem 3's bound. The issue is only imprecise phrasing ("minimizes the upper bound") rather than a fundamental disconnect.

5. **Various formatting/reproducibility nitpicks** — Removed per instructions (parser artifacts, appendix stripped).

## Novel Insights

None beyond the paper's own contributions. The reviews validate the paper's stated strengths (clean quantization-to-spiking connection, parameter-efficient calibration) while surfacing expected gaps (missing energy evaluation, limited scope, underspecified calibration details) that directly follow from the paper's content.

## Suggestions

1. Add an energy analysis section: measure spike counts per forward pass at each T and estimate energy using established SNN energy models. Compare against the QANN's estimated energy (FLOPs or MACs) to directly support the motivational claim.
2. Specify the calibration optimization protocol in full: optimizer, learning rate, number of iterations, calibration data size and source, data partitioning strategy across layers.
3. Provide details on the weight-calibration baseline in Table 4 so readers can assess the fairness of the comparison.
4. Expand experimental scope: test with at least one additional PTQ method (e.g., QuaRot), one additional bit-width (W4A4), and one additional model family (OPT).
5. Analyze the causes of performance degradation at larger T more deeply — is it the LT=2^n-1 approximation error from Remark 1, or residual calibration error?

---

**Calibration Anchors Used:**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| SpikeZIP (u438df0Uce) | 3.60 | R1 | Yes | Very similar topic (ANN-QANN-SNN conversion). Current paper is stronger — addresses LLMs specifically, cleaner theory, novel calibration. Should score above. |
| QAC (D4sQzdMvcG) | 5.75 | R1 | Yes | Similar core contribution (quantization↔timesteps). Shared weakness: "why not just use the QANN?" Current paper has clearer motivation but similar evaluation gaps. |
| Error-Free ANN-to-SNN (GTzP2GC7NR) | 5.75 | R1 | Yes | Stronger ImageNet results but rejected for novelty/data issues. Current paper's LLM focus is more novel. |
| SpikeBERT (6c4gv0E9sF) | 6.33 | R2 | Yes | Spiking for language tasks via distillation. Rejected despite high scores — energy estimates were only theoretical, a parallel to this paper's core weakness. |
| Spatio-Temporal Approx. (XrunSYwoLr) | 7.00 | R1 | Yes | SNN conversion for Transformers, accepted. More comprehensive evaluation and direct energy analysis. Current paper is weaker in evaluation breadth. |
| SpikeBERT (qzZsz6MuEq) | 6.60 | R2 | Yes | SNN-ViT with saccadic attention. Stronger experiments but completely different technical approach. |

**Final anchoring:** The paper sits below SpikeBERT (6.33, rejected) and QAC (5.75, rejected) because those papers, despite their weaknesses, had more comprehensive evaluations on their own terms. The current paper's core weakness — promising energy efficiency without any measurement — is shared with SpikeBERT (whose energy was also only theoretical), but SpikeBERT had additional architectural novelty (first Transformer SNN for language) and more extensive experiments. Meanwhile, the paper is clearly above SpikeZIP (3.60) due to the LLM-specific framing, cleaner theory, and novel calibration. The narrowest bracket after comparing weighted items is 5.0–6.0; within that, the missing energy evaluation and limited experimental scope tip the balance to the lower half.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>