Now I have comprehensive calibration. Let me produce the final review.

## Summary

QubitCache proposes a KV-cache compression method that keeps ~15% of tokens in classical storage while encoding per-token attention weights for the remaining ~85% as a 9-qubit quantum state (classically simulated via Qiskit). During inference, it computes hybrid attention: hard attention over preserved tokens plus soft (probabilistic) attention over non-critical tokens derived from quantum measurement probabilities and interpolated value vectors. The paper reports 7× memory compression with 92-97% of baseline performance across 5 models and multiple benchmarks.

## Strengths

1. **Validated core insight about attention-based token selection.** The ablation study (Table 4) cleanly demonstrates that attention-based token selection (0.491 F1) dramatically outperforms random selection (0.335 F1) — a 15.6% gap. This provides clear evidence that the token-selection strategy matters, and the attention-based heuristic is sound independent of the quantum framing.

2. **Reasonably broad experimental scope.** Five models (4B–8B range) are evaluated across seven benchmarks with comparisons against several established baselines (H2O, ScissorHand, StreamingLLM, GEAR), all reported in a unified table. The test across model families (Llama, Mistral, Qwen, Phi, DeepSeek-Coder) shows applicability beyond a single architecture.

## Weaknesses

### Fatal
None.

### Major

1. **The headline compression claim — "logarithmic compression beyond classical information-theoretic limits" (Abstract) — is not supported by the actual implementation.** The paper acknowledges "the current implementation operates as a classical simulation" (Section 3.2.2). A classical simulation of a 9-qubit state requires storing and manipulating 2⁹ = 512 complex amplitudes — one per computational basis state — which is the same number of values as the 512 attention weights being encoded. There is no memory savings from the encoding itself. The memory complexity formula in Table 3 ("O(L × H × 0.15S × D + log N)") lists only qubit count without accounting for classical simulation overhead. As shown in the "No Quantum" ablation (Table 4: 0.472 vs 0.491), the quantum/reconstruction component adds only ~4% improvement when non-critical tokens are dropped. The 7× compression comes from aggressive 15% token retention, not from the quantum representation. The paper's central disciplinary claim — surpassing classical information-theoretic bounds via quantum encoding — is **unsupported** when the method runs on a classical simulator storing precisely as many values as a classical alternative.

2. **PG19 evaluated with F1 instead of the standard perplexity metric, without any explanation.** PG19 is a language modeling benchmark (Rae et al., 2019) standardly evaluated with perplexity. Table 1 reports "PG19 F1(↑)" with values like 0.124 for Full KV on Mistral-7B. An F1 score of 0.124 is not interpretable as a language modeling result without substantial explanation of what classification or generation task produced it. Section 4.2 refers to this as "PG19 language modeling" but never clarifies the metric. This is a sufficiently unusual evaluation choice that it undermines confidence in the reported numbers.

3. **The 15-25% multi-hop reasoning improvement claim (Abstract) is cherry-picked from the single most favorable model-baseline pair.** On HotpotQA (Table 1), the improvement over H2O ranges from ~1.6% (Llama-8B: 0.510 vs 0.502) to ~24% (Qwen2-7B: 0.604 vs 0.487). For Mistral-7B it is ~9.3%, for DeepSeek-Coder ~9.4%. Only the Qwen2-7B case falls in the 15-25% range. Reporting a range that covers only the best case misrepresents the method's typical advantage.

### Minor

4. **"Relational preservation" substantially overstates what the method stores.** The paper claims a "paradigm shift from discrete token selection to continuous relational preservation" (Abstract) and "preserving attention relationships between tokens" (Section 3.1). However, what QubitCache encodes (Equation 1: α_i = a_i / Σ a_j) is a per-token scalar — the aggregate importance of each token, not pairwise attention edges. The value reconstruction for non-critical tokens (Equation 6) uses inverse-distance-weighted interpolation between nearest preserved tokens, which is a spatial smoothing operation, not a relational encoding of the attention matrix. Preserving per-token importance is strictly less information than preserving the pairwise attention structure that the paper's motivation (Section 1, paragraph 3) argues is essential.

5. **The "No Quantum" ablation is ambiguously defined and the key disambiguation experiment is missing.** Table 4 shows "No Quantum" at 0.472 vs Full QubitCache at 0.491. The paper says (line 238) the quantum component provides "a 3.9% performance improvement by partially preserving information from discarded tokens," which suggests "No Quantum" drops non-critical tokens entirely. This should be stated explicitly. Beyond this, two baselines are needed to interpret the quantum encoding's contribution: (a) 15% retention with no reconstruction (to isolate reconstruction benefit at the actual operating point, since the ablation runs at 49.8% retention), and (b) storing the attention weight distribution as a classical FP32 vector (to test whether the quantum encoding provides any benefit over direct classical storage).

6. **No wall-clock time, FLOPs, or throughput comparison.** The paper reports only memory. Quantum circuit simulation (statevector evolution with controlled-Ry gates) on classical hardware carries non-trivial computational cost. Without tokens/second or FLOPs data, it is unclear whether the 7× memory savings come at a prohibitive computational overhead.

7. **Ablation study runs at a different retention ratio (49.8%) than the main experiments (15%).** The ablation discussion in Table 4 refers to "preserving the same 49.8% of tokens" (line 238), while the paper's main results use 15% retention. This makes it difficult to directly apply ablation conclusions (e.g., the 3.9% quantum benefit) to the reported 7× compression setting.

### Trivial
None.

## Nice-to-Haves
- Include a baseline that keeps 15% of tokens via attention-based selection and simply drops non-critical tokens without reconstruction, to isolate the reconstruction benefit at the actual operating point.
- Include a baseline that stores the attention weight distribution as a classical FP32 vector per segment, to test whether the quantum encoding provides any benefit over direct classical storage.
- Report inference throughput (tokens/second) for all methods.
- Provide statistical significance (error bars, multiple seeds) for the main results.
- Clarify what task formulation yields F1 scores on PG19.

## Removed Points
- **Suspiciously low ScissorHand performance on PG19 (e.g., 0.018 for DeepSeek-Coder, 9.3% of baseline):** While these numbers are indeed unusual, the claim that ScissorHand is "misconfigured" cannot be verified from the paper content alone. This concern is noted but not included as a confirmed weakness.
- **Memory comparison at 15% vs 50% retention is unfair:** Comparing at different operating points is standard practice when methods support different compression ratios. The more relevant missing comparison (15% retention baselines) is covered in Weakness #5.
- **75-85% figure for classical methods in Conclusion lacks clear derivation:** This is a presentational concern that does not affect the core evaluation.
- **Missing circuit gate complexity analysis (O(2^n) gates for state preparation):** While this is a genuine concern for quantum implementations, the paper uses classical simulation where the gate cost matters only for compute time, not for correctness of the method description. The computational cost concern is partially covered by the throughput suggestion (Nice-to-Haves).

## Novel Insights

The harsh critic's central observation — that the quantum encoding provides no memory advantage in a classical simulation context — reframes what the paper actually accomplishes. The "logarithmic compression" headline buys rhetorical weight from quantum computing's exponential speedup narrative, but in the classical implementation, storing 512 amplitudes per segment costs the same as storing 512 attention weights directly. The paper's real contribution (attention-based token selection + inverse-distance-weighted interpolation for reconstruction) is a classical hybrid scheme, not a quantum one. This mismatch between framing and delivery is the paper's most significant weakness.

## Suggestions

1. **Most impactful revision:** Remove or substantially qualify the quantum framing. Present the method as a classical hybrid: keep ~15% of important tokens identified via attention scores, store the full attention weight distribution for interpolation, and reconstruct non-critical token values via inverse distance weighting. This is a reasonable contribution to the KV-cache compression literature that can stand on its own.

2. If retaining the quantum framing, (a) explicitly account for classical simulation overhead in the memory complexity and reported memory numbers, (b) compare against a classical baseline that stores attention weights directly without quantum encoding, and (c) qualify all "logarithmic compression" claims as achievable only on actual quantum hardware with efficient state preparation and readout.

3. Correct the PG19 metric to perplexity or provide a detailed explanation of what task produced F1 scores.

4. Add a 15%-retention-no-reconstruction baseline to isolate the reconstruction benefit at the paper's actual operating point.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| IntelLLM (4QWPCTLq20) | 3.0 | R1 | KV cache compression paper at 50% memory saving. Rejected for being incremental and missing baselines. QubitCache has a more severe overclaim problem (quantum framing unsupported) but broader experimental scope. Comparable quality level. |
| KV-Distill (p7vJ3wsm34) | 4.0 | R1 | Training-based KV compression with mixed reviews. QubitCache's quantum overclaim is a more fundamental issue than KV-Distill's missing baselines. |
| MiKV (CRQ8JuQDEd) | 5.0 | R1 | Mixed-precision KV quantization, seen as limited novelty but solid evaluation. QubitCache has a more serious evaluation concern (PG19 F1 metric) and a central overclaim that MiKV does not have. |
| KV-Dict (FkXYvV7nEB) | 5.25 | R1 | Sparse dictionary learning for KV compression. Solid novelty, accepted-tier work. QubitCache does not reach this quality level due to the unsupported central claim and metric issues. |
| PyramidKV (jZVNmDiU86) | 5.6 | R1 | Dynamic KV compression based on attention patterns, rejected but with some positive reviews. QubitCache has more fundamental issues. |
| MatryoshkaKV (BQwsRy1h3U) | 6.0 | R1 | Solid KV compression paper, accepted. QubitCache is clearly below this threshold. |

### Round 1 Bracket
Based on these anchors, the narrowest plausible score range for this paper is **2.0–4.0**. The paper is below the accepted KV compression papers (5.5+) and below even some rejected ones like KV-Dict (5.25) and MiKV (5.0). Its closest comparator is IntelLLM (3.0), which was rejected for being incremental and having weak evaluation — issues that QubitCache shares plus the additional problem of an unsupported central claim.

### Final Score

The paper identifies a genuine limitation of token-eviction methods and contains a reasonable technical idea (hybrid token retention + interpolation). However, it is undermined by: (1) a headline compression claim (quantum "logarithmic compression beyond classical information-theoretic limits") that is not supported by the classical-simulation implementation, (2) an unexplained non-standard evaluation metric (PG19 as F1), and (3) cherry-picked improvement claims in the Abstract. These issues are severe enough that the paper would need substantial revision — particularly removal or honest qualification of the quantum claims — before it could be fairly evaluated as a classical KV-cache compression method. In its current form, the claims do not hold up.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>