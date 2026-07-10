Now let me write the final consolidated review.

## Summary

This paper proposes a "dual" ANN-to-SNN conversion framework for large language models. Instead of training a conversion-friendly ANN from scratch (which is prohibitively expensive at LLM scale), the method starts from a statically quantized LLM (obtained via post-training quantization) and converts it to an SNN using a novel Integer Spiking (IS) neuron with multi-hierarchical thresholds. A parameter-efficient layer-wise calibration step (optimizing only thresholds and initial membrane potentials) is introduced to reduce conversion errors. Experiments on LLaMA-2-7B and LLaMA-3-8B show that the resulting SNN achieves accuracy close to the quantized ANN baseline at low time steps (T=1, T=2).

## Strengths

- **The dual conversion framework is well-motivated.** Eliminating the need to train a conversion-friendly ANN from scratch addresses a genuine obstacle at LLM scale. The idea of repurposing an off-the-shelf quantized LLM as the intermediate representation is practically appealing and clearly articulated (Section 1, lines 37-39).

- **The layer-wise calibration strategy is parameter-efficient and well-supported.** Freezing weights and optimizing only thresholds θ^k and initial membrane potentials v^k(0) uses only 0.107K learnable parameters per layer vs. ~200M for full weight fine-tuning, while achieving comparable or better accuracy (Section 4.4, Table 4).

- **Experimental documentation is thorough across multiple settings.** The paper reports performance across two model families (LLaMA-2-7B, LLaMA-3-8B) and multiple time steps T∈{1,2,4,8}, providing a clear picture of how the method behaves under these settings (Table 2).

## Weaknesses

### Fatal
None.

### Major

- **Accuracy degrades monotonically as T increases, contrary to the expected behavior of ANN-to-SNN conversion.** For LLaMA-2-7B, average accuracy drops from 68.79% (T=1) to 66.03% (T=8), and WikiText2 perplexity rises from 5.61 to 12.03. For LLaMA-3-8B, accuracy drops from 71.67% (T=1) to 63.76% (T=8). Standard ANN-to-SNN conversion theory predicts that approximation quality should improve (or at least not degrade systematically) with more time steps. The paper acknowledges this (line 212) and attributes it to "growing unevenness error introduced by the larger time-step," but does not resolve it. Since the SNN cannot leverage additional time steps to improve quality, the core value proposition of the conversion — trading latency for accuracy — is compromised (Table 2).

- **No experimental comparison against other spiking LLM methods.** The paper compares only against quantization methods (PrefixQuant, DuQuant). The related work cites SpikeZIP (You et al., 2024) as a directly relevant ANN-to-SNN conversion method and mentions SpikeGPT/SpikeBERT, yet none appear in Table 2. A paper claiming to advance spiking LLMs must position itself relative to existing SNN methods to substantiate that claim (Table 2, Section 4.1).

- **The DuQuant results for LLaMA-2-7B and LLaMA-3-8B show identical per-task accuracy scores across all five zero-shot tasks** (67.88, 72.64, 40.53, 53.07, 77.15, Avg. 62.25) despite different PPL values (5.53 vs 6.27). Identical outputs from two different model families are extremely unlikely and signal a probable error in the table (Table 2, rows 220 and 231).

### Minor

- **No quantitative energy-efficiency evidence.** The paper motivates SNNs through "brain-inspired efficiency and low power consumption" (line 9) and claims the method "potentially reduces the energy consumption of LLMs" (line 49), but provides zero measurements, synaptic operation counts, or FLOPs comparisons against the quantized ANN baseline. The IS neuron's multi-level output (0…L, further modified by α^k(t) subtraction) is not binary, so it does not automatically inherit the energy advantages of conventional spiking neurons. This gap undermines the paper's central motivation.

- **The theoretical analysis provides limited actionable guarantees.** Theorem 1 restates the IS neuron's behavior under exhaustive intervals (i.e., always true). Theorem 2 requires LT = 2^n − 1, which Remark 1 concedes "rarely holds for arbitrary integer choices of L and T if T ≠ 1," so exact equivalence to the quantization function is practically unattainable. Theorem 3 is a standard Lipschitz error-propagation bound whose Remark 3 states the obvious implication (reducing per-layer error reduces total error). No non-trivial bounds or practical guidance about when calibration will or will not succeed are derived (Section 3.3, lines 134-184).

- **The calibration optimization is underspecified.** The paper states the objective min ||∑ ŷ^k(t) − y^k|| (line 188) but does not specify the optimizer, learning rate, number of steps, calibration dataset, or any hyperparameters needed for reproduction. This is a reproducibility concern (Section 3.4).

- **Equations (8)-(10) contain a notational ambiguity.** Equation (9) defines s^k(t) based on m^k(t), and Equation (10) redefines s^k(t) := s^k(t) − α^k(t). It is unclear whether the s^k(t) used in the membrane potential update (Eq. 8) refers to the pre- or post-subtraction value. If post-subtraction, the update is inconsistent with the definition in Eq. (9); if pre-subtraction, the notation conflates two quantities (Section 3.2.2).

- **More calibration parameters produce worse accuracy (Table 3).** Group size 1 (23.399K params/layer) yields 65.46% accuracy vs. group size -1 (0.107K params, coarsest granularity) yielding 67.65%. This counterintuitive trend is mentioned but not explained, raising questions about whether the calibration is correcting meaningful conversion errors or overfitting to noise.

### Trivial
None.

## Nice-to-Haves

- Report energy consumption relative to the quantized ANN baseline using standard metrics (estimated synaptic operations, AC vs. MAC ratios) to substantiate the efficiency motivation.
- Compare against at least one existing spiking LLM method (e.g., SpikeZIP) to properly position the contribution.
- Resolve the suspicious DuQuant duplication in Table 2.
- Provide complete calibration hyperparameters (optimizer, learning rate, calibration dataset, number of steps).
- Investigate the root cause of the T-degradation and either fix the neuron design or clearly delineate the regime (T ≤ 2) where the method is effective, with a principled rationale.

## Removed Points

These points from the input review are flagged for removal; treat them with caution:
- "The dual conversion novelty is overstated" — subjective opinion, not a verifiable weakness.
- "Section 3.3's error categorization is standard" — accurate description but not a weakness; the paper does not claim a novel taxonomy.
- "Evaluation should include 13B/70B models" — scope creep beyond what the paper sets out to demonstrate.
- "The IS neuron design may be the wrong abstraction" — speculation without supporting evidence.
- The "Strengthening the Paper on Its Own Terms" section and general "Section-by-section notes" that are editorial observations rather than identified weaknesses were absorbed into the Weaknesses and Nice-to-Haves where concrete, and removed otherwise.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Address the T-degradation problem head-on: either modify the IS neuron design so that unevenness error does not grow with T, or clearly delineate the effective operating regime (e.g., T ≤ 2) and explain why this is practically useful.
- Include at least one SNN-specific baseline (SpikeZIP) in the experimental comparison.
- Investigate and correct the DuQuant data in Table 2.
- Specify calibration hyperparameters for reproducibility.
- Add energy analysis (synaptic operations, estimated MAC vs. AC costs) to substantiate the core efficiency motivation.

## Score and Decision

The paper introduces a genuinely novel approach to obtaining spiking LLMs by repurposing quantized LLMs, and the calibration strategy is elegantly parameter-efficient. However, two major weaknesses undermine the contribution: (1) accuracy degrades with more time steps, contradicting the expected behavior of ANN-to-SNN conversion and limiting practical utility, and (2) the evaluation does not include any comparison to existing spiking LLM methods, making it impossible to assess the method's standing in the field it claims to advance. Additionally, the DuQuant data appears to contain an error. The energy-efficiency motivation, which is central to the SNN value proposition, is entirely unsupported by evidence. These issues collectively outweigh the strengths in the paper's current form.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>