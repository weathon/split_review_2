Now I'll produce the final consolidated review.

## Summary

This paper proposes QubitCache, a KV-cache compression method that retains 15% of tokens (selected by accumulated attention scores) in classical storage while encoding the attention patterns of the remaining 85% into quantum-inspired amplitude representations. At 7× compression, the method achieves consistent improvements over H2O, ScissorHand, GEAR, and StreamingLLM across 5 LLMs and multiple benchmarks, with particularly strong results on multi-hop reasoning.

## Strengths

1. **Genuinely insightful conceptual motivation.** The observation that attention *relationships* between tokens may carry more information than individual tokens is well-supported by sparsity analyses from prior work (Michel et al. 2019a; Jaszczur et al. 2021; Choromanski et al. 2020) and provides a useful reframing of the KV-cache compression problem.

2. **Consistent empirical improvements across diverse settings.** QubitCache outperforms all baselines on the vast majority of model×benchmark combinations in Table 1, including on challenging multi-hop reasoning (HotpotQA), despite operating at a substantially higher compression ratio (7× vs. 2× for H2O/ScissorHand).

3. **Informative ablation study.** Table 4 disentangles component contributions and provides clear evidence that attention-based critical token selection drives most of the gain (20.4% drop when removed), while the quantum component contributes ~4%.

## Weaknesses

### Fatal
None.

### Major

1. **The method does not compute query-dependent attention for compressed tokens; it uses a static prior derived from historical attention patterns. The claimed "relational preservation" overstates what is implemented.**  
   For the 85% of compressed tokens, key vectors are discarded. The weight assigned to a compressed token in Eq. 7 is `p_j(ψ) = |⟨j mod n_s | ψ_{S_j/n_s}⟩|²`, where the quantum state encodes *aggregated attention that token received from other tokens in the same segment during the initial forward pass* (Eq. 3–5). This is a static distribution with no dependence on the current query Qₜ — it does not compute softmax(QₜKᵢᵀ/√d). Using historical attention as a proxy for future relevance is a reasonable heuristic, but the paper's central framing — that it "preserves attention relationships" where prior methods "irreversibly discard relational information" — is misleading. The method replaces query-dependent attention with a fixed prior, and this gap between framing and implementation must be explicitly acknowledged.

2. **The quantum encoding is simulated classically and provides negligible compression benefit; claims of "logarithmic compression beyond classical information-theoretic limits" are misleading.**  
   The paper states (Section 3.2.2) that "the current implementation operates as a classical simulation." Simulating a 9-qubit state requires storing 2⁹=512 complex amplitudes per segment — a 1∶1 representation of the 512-token attention distribution. The 7× memory reduction comes from the 15% token retention ratio (discarding 85% of K/V pairs), a classical strategy. The quantum encoding adds overhead (storing amplitude vectors, measurement simulation) rather than reducing memory. "O(log N)" refers to qubit count, not actual memory footprint in simulation. The compression is achieved through classical token selection; the quantum component provides at most a 3.9% performance lift (Table 4) and no memory savings.

3. **"92–97% of baseline performance" does not hold across all models.**  
   For DeepSeek-Coder (Table 1), QubitCache achieves retention rates as low as 75.5% (HotpotQA: 0.256/0.339), 75.9% (SummScreen: 0.202/0.266), and an average of ~86% across tasks — well below the claimed 92–97% range. The paper presents this as a universal property, but the evidence does not support it for all models.

### Minor

4. **No latency or throughput measurements are provided.** The paper claims "minimal latency overhead" but reports zero runtime data. Given the overhead of simulating thousands of quantum circuits (32 layers × 32 heads × ~16 segments), the computational cost must be quantified to assess practical feasibility.

5. **The "15–25% higher F1 on multi-hop reasoning" claim is selectively reported.**  
   Computing relative improvements over H2O on HotpotQA from Table 1: Mistral-7B 9.3%, Qwen2-7B 24.0%, Phi-4-mini 41.8%, DeepSeek-Coder 9.4%, Llama-8B 1.6%. The range is 1.6%–41.8%, not 15–25%. The paper's summary centers the distribution while excluding the extremes.

6. **Averaging attention scores across all layers and heads (Eq. 4) destroys multi-head structure.** The paper collapses per-layer, per-head attention into a single scalar per token. Different attention heads specialize in different functions; averaging loses this information. This design choice is not ablated or justified.

7. **The claim that classical methods are "bounded by H(X) ≥ log₂|X| bits" (Section 2) is technically incorrect.** This is the Shannon lower bound for *lossless* compression. Lossy methods (including quantization) routinely operate below this bound by accepting distortion.

8. **Inconsistent benchmark counts and missing evaluation.** The abstract says "six benchmarks," Section 4.1.2 says "five benchmark datasets," and Table 1 shows 7 metrics. LAMBADA is listed in the setup but never appears in any results table.

9. **Figure 3b's y-axis (F1 0.7–0.85) does not match the scale of values reported elsewhere (typically 0.2–0.6), and the benchmark is not identified.**

### Trivial

10. The "catastrophic degradation" characterization of prior work (introduction) is overstated relative to the paper's own results — e.g., H2O retains 74% of HotpotQA F1 for Mistral-7B (0.420 vs. 0.566), which is meaningful degradation but not catastrophic.

## Nice-to-Haves

- Evaluate all methods at matched compression ratios (e.g., 2×, 4×, 7×) to produce trade-off curves.
- Ablate the segment size (512 tokens / 9 qubits) to show sensitivity to this hyperparameter.
- Show results on longer sequences (e.g., 32K–100K tokens) given the long-context motivation.

## Removed Points

These points were flagged for removal per filtering rules; treat with caution:

1. **"Unfair comparison against baselines" (asymmetry favors baselines).** The baselines operate at 2× compression while QubitCache operates at 7×. Per rules, criticisms of unfair comparison where the asymmetry favors the baseline are removed. This asymmetry actually strengthens QubitCache's demonstrated superiority.

2. **"Theoretical analysis absent from main paper."** The parser strips appendix sections from all papers. The claimed theoretical analysis likely exists in the original appendix; per rules, criticisms about missing appendix content are removed.

3. **"Value interpolation is not novel."** The paper does not claim novelty for inverse distance weighting; this is an observation about technique lineage, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Significantly de-emphasize or reframe the quantum claims. Present the method honestly as: attention-based critical token selection (15%) + value interpolation for non-critical tokens + a quantum-inspired weighting that provides a ~4% performance lift. Acknowledge that the 7× compression comes from the token retention ratio, not the quantum encoding, and that the implementation is classical simulation.

2. Add latency/throughput measurements to substantiate the "minimal overhead" claim.

3. Correct the "92–97%" claim to reflect per-model retention rates (e.g., ~86% for DeepSeek-Coder).

4. Report the full range of relative improvements instead of "15–25%" for multi-hop reasoning.

5. Fix the Shannon entropy bound error in Section 2 and correct the inconsistent benchmark count.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>