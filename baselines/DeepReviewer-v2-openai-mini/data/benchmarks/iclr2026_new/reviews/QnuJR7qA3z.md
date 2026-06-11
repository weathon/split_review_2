## Summary
# Final Review Report

## Summary

This paper presents HARA (Hybrid Arithmetic-ReLU Networks Approximation), a framework for replacing diverse non-linear operators in Transformer models (GELU, SiLU, Softmax, LayerNorm, RMSNorm) with a unified architecture based on a single-hidden-layer ReLU network and simple arithmetic primitives. The key methodological contributions are: (1) a unified operator architecture that maps all non-linear functions to a common ReLU-arithmetic pattern, enabling hardware resource sharing; (2) an optimized parameter initialization pipeline using dynamic programming (DP) for piecewise-linear approximation, analytical conversion to ReLU network parameters, and fine-tuning; and (3) a decomposition strategy that expresses complex operators (Softmax, LayerNorm) in terms of Pow2 and Log2 primitives, which are then approximated by the ReLU network.

The paper validates HARA across four model architectures (BERT, Swin, LLaMA3.2-3B, Stable Diffusion) with metrics spanning QA, classification, language modeling, and text-to-image generation. Results show performance within 0.1% of baselines. Hardware synthesis estimations at 6nm project a 62.3% area reduction and 51.7% power savings for non-linear processing units.

**Overall assessment:** The paper addresses a genuine and important problem—the hardware cost of non-linear operators in Transformers for edge deployment—and proposes a technically sound unification approach. However, the manuscript has several critical weaknesses that must be addressed before publication: a potential mathematical error in the LayerNorm decomposition (Eq 3), missing statistical rigor in experimental results (no variance reporting), an incomplete hardware comparison methodology, and insufficient technical detail in key algorithmic components. Novelty claims cannot be fully verified due to the absence of external literature retrieval in this review run.

## Strengths
1. **Well-motivated problem with practical significance.** The paper identifies a genuine hardware bottleneck: non-linear operators (exp, sqrt, div) in Transformers require diverse specialized functional units that consume significant silicon area and power. Replacing these with a unified, hardware-friendly approximation is a practically important goal for edge deployment, and the paper provides clear motivation for why existing approaches (quantization, operator-specific approximations) are insufficient.

2. **Technically sound core idea with elegant decomposition.** The approach of expressing all non-linear operators through Pow2 and Log2 primitives and approximating these with a single ReLU network is conceptually clean. The symmetry exploitation for activation functions (Table 1)—decomposing GELU/SiLU into ReLU(x) plus an even, decaying component—is a particularly elegant way to handle infinite-domain functions with a finite-domain approximator. This decomposition is non-trivial and demonstrates genuine technical insight.

3. **Principled optimization pipeline with clear ablation.** The three-stage initialization pipeline (DP breakpoint selection → analytical PWL-to-ReLU conversion → fine-tuning) is a significant improvement over naive direct training for function approximation. The ablation study (Table 4) convincingly shows that DP initialization outperforms naive training by several orders of magnitude in MSE, and that fine-tuning provides additional refinement. This is strong evidence that the DP-based approach is the key driver of accuracy.

4. **Comprehensive model coverage.** The validation across four architecturally diverse models (BERT for NLP, Swin for vision, LLaMA for language generation, Stable Diffusion for text-to-image) demonstrates that the HARA approach generalizes across Transformer variants. The inclusion of 8-bit quantization compatibility testing is appropriate for the target edge-deployment use case.

5. **Honest limitation disclosure.** The Discussion section explicitly acknowledges that hardware benefits are based on synthesis estimations rather than physical implementation, which is a major limitation but is stated transparently. The paper does not claim to have fabricated a chip.

## Weaknesses
### W1. Potential mathematical error in LayerNorm decomposition (Eq 3) — Validity-critical

**Evidence:** Equation (3) presents the LayerNorm decomposition in the Pow2/Log2 domain as:
```text
LayerNorm(x) = sgn(x̄) · 2^{(½)log₂(M) + log₂|x̄| − ½log₂(∑xⱼ²)}
```
where x̄ = Mx − ∑xⱼ and M is the sequence length.

**Verification:** Re-deriving from the standard definition LN(x) = (x−μ)/√(σ²) with σ² = (1/M)∑(xᵢ−μ)² gives an expression with −½log₂(M) (negative), not +½log₂(M) (positive), and with ∑(xᵢ−μ)² in the last term rather than ∑xⱼ². These discrepancies could affect the correctness of the LayerNorm implementation.

**Impact (Major):** If the equation is incorrect, the LayerNorm approximation in HARA would compute the wrong function at every forward pass. This could explain why the paper observes slight performance changes but raises questions about the validity of the decomposition and whether any errors are canceling out coincidentally. This is a validity-critical issue that must be resolved before publication.

**Required Fix:** The authors must either (a) provide a corrected derivation showing their form is mathematically equivalent to the standard definition under all conditions, or (b) update Eq (3) to match the correct derivation. The full step-by-step derivation should be included in the appendix.

---

### W2. Missing statistical rigor in experimental results

**Evidence:** Table 6 reports all end-to-end metrics as single-point estimates with no variance, confidence intervals, or multi-seed averages. The text describes changes like "F1: 87.616 → 87.615" and "perplexity: 7.814 → 7.819" but does not report standard deviations.

**Verification:** The paper lists "PyTorch implementation" and describes replacing operators, but does not specify how many evaluation runs were performed. For models with stochastic components (dropout in BERT, sampling in DiT), single-run metrics can vary by more than the reported deltas (e.g., BERT F1 delta = 0.001).

**Impact (Major):** Without variance information, readers cannot assess whether the performance changes are statistically significant or within noise. The claim of "<0.1% change" is not statistically grounded. If the standard deviations are large relative to the deltas, the paper's central claim that HARA "maintains performance" is weakened.

**Required Fix:** Report mean ± std over at least 3 random seeds for all metrics in Table 6. For the two largest models (LLaMA, DiT), include a paired significance test (bootstrap or t-test) comparing baseline vs HARA performance. See suggested values in the annotation at Page 6-7 (Section 4.3).

---

### W3. Incomplete and potentially unfair hardware comparison

**Evidence:** Table 5 compares HARA's URN area (7,560 μm² at HD=8) against the sum of three specialized units (20,056 μm²), claiming 62.3% area reduction. However, Section 3.1 describes the HARA system as containing "several parallel URN blocks, sum generator (SG), max block (MB), local buffer (LB) and one controller."

**Verification:** The reported 7,560 μm² appears to cover only one URN block, not the full HARA system including controller, buffer, and multiple URNs. The baseline uses three parallel specialized units (one per operator). If the comparison is one URN (sequential processing) vs three parallel units (higher throughput), the throughput difference must be reported.

**Impact (Major):** The 62% area saving may be partially or fully offset when accounting for the full system overhead or when matching throughput. The paper also does not report latency—without latency numbers, the area-power-latency tradeoff space is incomplete for evaluating the hardware claims.

**Required Fix:** (a) Clearly state which components are included in the HARA area estimate; (b) report latency for each operator under both baseline and HARA; (c) if the area saving relies on time-multiplexing, provide utilization analysis; (d) ideally compare at iso-throughput (multiple URNs if needed).

---

### W4. Ambiguous comparison setup in Table 3 (operator-level MSE)

**Evidence:** Table 3 compares HARA against NN-LUT and RI-LUT at varying "hidden dimension (HD)" values for GELU, Softmax, and LayerNorm. The term "HD" is not defined per method.

**Verification:** For HARA, HD likely refers to the URN hidden layer width. For NN-LUT and RI-LUT, HD likely refers to LUT size or neural network input dimension—these are not equivalent architectural choices. The baseline MSE values for LayerNorm (0.13–0.28) are extremely high (RMSE ~0.36), suggesting possible catastrophic failure, which seems inconsistent with these methods being used in practice.

**Impact (Major):** The "several orders of magnitude lower MSE" claim may be inflated if the baselines are forced to approximate the full vector-valued LayerNorm while HARA approximates only scalar Pow2/Log2 primitives. This is not an apples-to-apples comparison.

**Required Fix:** (a) Define "hidden dimension" unambiguously per method; (b) provide comparison at the scalar-primitive level (Pow2, Log2) where all methods face the same task; (c) include visual plots of the approximations so reviewers can assess qualitative quality.

---

### W5. Insufficient technical detail in DP-based initialization algorithm

**Evidence:** Section 3.2 describes Stage 1 as "employing a dynamic programming (DP) algorithm to identify the optimal breakpoint locations that globally minimize the mean squared error." No DP recurrence, error function, or complexity analysis is provided.

**Verification:** The Algorithm 1 pseudocode calls DynamicProgramming(x, y, N) as a black box without specifying the DP formulation. Classic PWL approximation with DP requires a segment error function E(i,j) and recurrence DP[j] = min_i (DP[i-1] + E(i,j)), none of which is disclosed. Additionally, the input domain discretization range and resolution are not specified for any operator.

**Impact (Major):** The DP pipeline is claimed as a core contribution (Claim 2), but the current description is insufficient for independent implementation or reproduction. A reviewer cannot determine whether the DP formulation is novel or a standard application.

**Required Fix:** Provide the explicit DP recurrence, segment error metric, complexity analysis, and the discretization parameters (domain bounds, step size) for each target function. This belongs in the main text or a dedicated appendix subsection.

---

### W6. Activation function decomposition (Table 1) lacks formal definition of g(x)

**Evidence:** The "Negative Approx" column in Table 1 uses notations like "gSigmoid(−x) + c" and "gGELU(−x) + ReLU(x)" without defining what gSigmoid, gGELU, etc., actually are.

**Verification:** The text says "g(x) represents the approximation function that closely matches the original function for x < 0." However, g(x) must be a concretely defined function for each activation. Without this definition, the decomposition cannot be implemented.

**Impact (Major):** The symmetry exploitation is presented as a key innovation (Claim 1/2), but the imprecise notation prevents reproduction. It is unclear whether g(x) is the same ReLU-network approximator applied to a transformed version of the target function, or a separate mathematical construction.

**Required Fix:** For each activation function, provide the explicit mathematical definition of g(x) in terms of the original function (e.g., g_GELU(t) = GELU(−t) − ReLU(−t) for t ≥ 0). Clarify that the HARA approximator is then applied to g(x) on a finite domain [0, T].

---

### W7. Missing novelty/related-work verification (deferred)

**Notice:** External literature retrieval was unavailable in this review run (paper_search provider not configured). Therefore, novelty claims regarding the unified architecture and DP-based initialization cannot be independently verified against the state of the art. The following questions remain open:
- Is the DP-based PWL-to-ReLU conversion (Section 3.2) a known technique in the function-approximation literature?
- Have prior works (e.g., NN-LUT, RI-LUT, or other approximation frameworks) proposed unified architectures that the paper does not cite?
- What is the closest prior art to HARA's "unified ReLU network for all non-linear operators" and what is the residual novelty?

**Impact (Moderate):** The paper's primary claims (unified architecture + DP initialization) may overlap with existing work. The authors should strengthen their related-work discussion with explicit comparison to the nearest prior approaches. This is flagged as deferred for manual verification.

---

### W8. Conclusion overclaims beyond evidence

**Evidence:** The Conclusion (Section 6) contains phrases like "bridges the gap between the advanced capabilities of large Transformer models and the stringent constraints of edge computing" and "establishing a new path forward for efficient and powerful AI on any device."

**Verification:** The paper's hardware results are at the synthesis-estimation stage, not physical implementation. The method was tested on only four model families under narrow benchmark conditions. The claim of "any device" is unsupported.

**Impact (Minor):** These overclaims weaken the paper's scientific positioning and may give readers an inflated impression of the work's maturity. They can be corrected with straightforward language tightening.

**Required Fix:** Replace the final sentences with bounded wording that acknowledges the synthesis-estimation limitation while conveying potential impact.

---

### Additional Minor Issues

- **Introduction writing quality (M2):** The second Introduction paragraph has a grammatical break between enumerated points 1 and 2 ("...and leading to increased silicon area and design complexity 2) Suboptimal..."). The forward reference "that we demonstrate in our experiments" belongs in a results preview, not in the problem statement.
- **Quantization protocol unspecified (M2):** The paper claims "fully compatible with 8-bit quantization" but does not specify the quantization scheme (symmetric/asymmetric, per-tensor/per-channel, calibration method).
- **"Without any architectural modifications" is misleading (M2):** Replacing operators is an architectural modification. The authors mean "without retraining or altering weight parameters."
- **Theoretical Foundations paragraph (M1):** Cites universal approximation theorems without connecting them to the specific properties of Transformer non-linear operators (smoothness, bounded curvature) that make them well-suited for ReLU approximation with small hidden dimension.

---

**Ranked Error Board (Top-5):**

| Rank | Issue | Severity | Validity Risk | Fixability | Confidence |
|------|-------|----------|--------------|------------|------------|
| 1 | W1: Eq (3) LayerNorm error | Major | High (invalid computation) | Easy (fix formula + re-run) | High |
| 2 | W2: Missing variance/statistics | Major | Medium (unsubstantiated claim) | Easy (add seeds + report) | High |
| 3 | W3: Hardware comparison fairness | Major | Medium (overstated savings) | Moderate (add system overhead) | High |
| 4 | W4: Table 3 ambiguous HD definition | Major | Medium (inflated MSE advantage) | Moderate (clarify + re-compare) | Medium |
| 5 | W5: DP algorithm insufficient detail | Major | Medium (irreproducible) | Easy (add recurrence + params) | High |

**Evidence-Sufficiency Audit:**

| Claim | Evidence Status | Assessment |
|-------|----------------|------------|
| Unified architecture enables hardware resource sharing | Partially proven | Conceptual design provided; hardware estimation supports area/power claims but with caveats (W3) |
| DP initialization achieves higher accuracy than direct training | Proven | Ablation study (Table 4) clearly shows DP > Naive; however, the DP formulation itself is insufficiently specified (W5) |
| HARA preserves performance within 0.1% across models | Partially proven | Table 6 shows small deltas, but no variance reporting (W2) weakens this conclusion |
| Eq (3) LayerNorm decomposition is correct | Unsupported | Derivation check reveals potential errors (W1); needs verification |
| HARA is robust to 8-bit quantization | Partially proven | Quantization protocol not specified; method used but details missing (Minor Issues) |

## Score
**Final Score: 5/10**

**Rationale:** The paper addresses a relevant and well-motivated problem (hardware-efficient non-linear operators for Transformers) with a conceptually clean approach (unified ReLU-arithmetic architecture with DP-based initialization). The ablation study convincingly demonstrates the advantage of DP initialization over naive training, and the cross-model validation suggests the approach generalizes across diverse architectures.

However, the score is reduced to 5/10 due to several validity-critical and major weaknesses:

1. **Validity risk (W1):** The potential error in Eq (3) for the LayerNorm decomposition is a mathematical correctness issue that could affect all LayerNorm-related results. This must be resolved before the paper's conclusions can be trusted.

2. **Insufficient evidence strength (W2):** The lack of variance reporting means the central claim ("<0.1% performance change") is not statistically substantiated. This weakens confidence in all end-to-end results.

3. **Incomplete comparison methodology (W3, W4):** The hardware area comparison may significantly overstate savings by omitting system overhead, and the operator-level MSE comparison may be unfair due to ambiguous "hidden dimension" definitions.

4. **Reproducibility gaps (W5, W6):** The core DP algorithm is specified only as a black-box call, and the activation decomposition functions g(x) are not formally defined, making the method only partially reproducible from the text.

5. **Novelty uncertainty:** External literature verification was unavailable in this review run; novelty claims regarding the unified architecture and the DP-to-ReLU conversion technique require manual verification.

**Bottom line:** The core idea has merit and the empirical scope is appropriate, but the mathematical correctness, statistical rigor, hardware comparison fairness, and algorithmic completeness need substantial improvement before the paper can be accepted. The weaknesses are fixable with moderate effort (formula correction, added variance reporting, specification of DP details, fairer hardware accounting), which warrants a score of 5 rather than lower. A revised version addressing the top-5 issues could reach 7-8/10.

*Note: Post-Revision Target is not provided per the submission constraints for this review run.*