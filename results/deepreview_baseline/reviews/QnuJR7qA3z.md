## Summary

The paper proposes HARA, a framework that replaces the diverse non-linear operators in Transformers (GELU, Softmax, LayerNorm, etc.) with a single canonical architecture built from a shallow ReLU network and simple arithmetic primitives. HARA’s key algorithmic contribution is a dynamic-programming (DP) based parameter initialization pipeline that first finds an optimal piecewise-linear approximation and then analytically converts it to ReLU network weights, followed by fine-tuning. The authors evaluate HARA on BERT, Swin, LLaMA, and Stable Diffusion, reporting negligible performance degradation (<0.1%) and compatibility with 8-bit quantization. Hardware synthesis projections estimate over 60% silicon area reduction and over 51% power savings for the non-linear processing units compared to a baseline with separate specialized units.

## Strengths

- **Important problem:** Reducing the hardware cost of non-linear operators in Transformers is a genuine bottleneck for edge deployment, and the paper identifies a practical approach by unifying diverse operators into a single architecture.
- **Principled initialization pipeline:** The DP-based breakpoint selection combined with analytical conversion to ReLU parameters is a systematic and transparent alternative to heuristic training; the ablation study (Table 4) convincingly shows that DP initialization dramatically reduces approximation MSE compared to naive training.
- **Comprehensive model coverage:** The framework is tested across four models spanning NLP, vision, language generation, and text-to-image, with consistent performance preservation (<0.1% change).
- **Quantization compatibility:** The paper demonstrates that HARA-approximated models remain accurate after 8-bit post-training quantization, a critical requirement for edge deployment.

## Weaknesses

### Fatal
None.

### Major

1. **Incomplete hardware validation.** The claimed area/power savings (Table 5) are based on synthesis estimations, not a physical implementation or post-layout analysis. The baseline design (separate LUT-based units) may not represent the most efficient existing implementation; comparisons to approximate hardware units for _exp_, _sqrt_, etc. (e.g., CORDIC, reduced-precision iterative methods) are absent. Without measured latency, throughput, or energy per operation, the hardware claims remain speculative.

2. **Missing fair comparison under quantization.** Table 6 compares a full-precision baseline against a HARA model that is both approximated and 8-bit quantized. It is unclear whether the baseline was also 8-bit quantized. If the baseline remains in FP32, the comparison conflates the effect of quantization with the effect of HARA approximation. A proper ablation would show: (i) full-precision baseline, (ii) quantized baseline, (iii) full-precision HARA, (iv) quantized HARA. As reported, the drop from full-precision baseline to quantized HARA could be mostly due to quantization rather than HARA’s approximation.

3. **Limited novelty of the DP method.** DP for optimal piecewise-linear approximation is a standard technique (e.g., dynamic programming for min-# or min-ε problems). The conversion from PWL parameters to ReLU network weights is also known (a two-layer ReLU net with one hidden neuron per linear region represents any PWL function). The paper’s main algorithmic novelty is the application of this pipeline to Transformer operators, but it does not contribute a new optimization algorithm or theory.

4. **Insufficient characterization of out-of-domain behavior and domain selection.** Activation functions are defined over an infinite domain, yet the DP initialization uses a finite training interval. The paper exploits symmetry and asymptotic properties (Table 1) to constrain the approximation, but the choice of domain boundaries is not justified. The evaluation in Figure 3 is qualitative; quantitative out-of-domain MSE or performance under distribution shift is not reported.

5. **Lack of statistical significance.** All end-to-end results are reported as single numbers without confidence intervals or multiple trials. Given the extremely small observed differences (e.g., 87.616 → 87.615 F1), it is unclear whether these changes are within the noise of inference.

### Minor

- The paper claims “over 60% reduction in silicon area” but the actual number in Table 5 is 62.3%. The percentage relative to baseline could be sensitive to the baseline design choices (e.g., number of LUT entries, precision).
- The DP algorithm (Algorithm 1) is described only in terms of indices; the actual cost function for breakpoint selection (MSE) is mentioned in text but not formalized in the pseudocode.
- The URN architecture in Figure 2 includes multiple components (sum generator, max block, local buffer, controller) that themselves require some area and power; the savings are computed only for the non-linear processing units, not the entire system.

### Trivial
- The abbreviation “BL” is used without definition in Table 5.
- The reference list contains placeholder years (e.g., “Bhalgat et al., 2020” but the venue is incomplete).

## Nice-to-Haves

- A comparison to simpler baselines such as replacing GELU with ReLU, or using a single piecewise-linear approximation with 4 or 8 segments trained end-to-end with STE (straight-through estimator).
- A discussion of how the number of segments (N) and the hidden dimension (HD) were selected for each operator, and the sensitivity of end-to-end accuracy to these hyperparameters.
- An analysis of the computational overhead (number of operations) of the HARA ReLU network compared to the original operators, not just hardware area/power estimates.

## Novel Insights

None beyond the paper’s own contributions. The insight that unifying non-linear operators into a single ReLU-based approximator can yield large hardware savings while preserving accuracy is valuable, but the individual techniques (DP-based PWL approximation, analytical ReLU conversion) are well established in separate literatures.

## Suggestions

1. Provide a fair quantization ablation: evaluate the baseline model with the same 8-bit post-training quantization and report results for both FP32 and INT8 baselines alongside FP32 and INT8 HARA variants.
2. Add confidence intervals or error bars for end-to-end metrics, especially for the tiny performance differences observed.
3. Clarify and justify the domain interval used for DP training of each operator, and include quantitative out-of-domain MSE or performance on perturbed inputs.
4. Include a comparison to a hardware baseline that uses more efficient approximate implementations (e.g., 2-4 segment PWL for _exp_ and _sqrt_, which are common in edge accelerators) to demonstrate the advantage of the unified architecture.
5. Report or estimate the latency/throughput of the URN unit, not just area and power, to give a complete hardware picture.

## Score and Decision

MY FINAL SCORE: 4</score>
MY FINAL DECISION: Reject</decision>