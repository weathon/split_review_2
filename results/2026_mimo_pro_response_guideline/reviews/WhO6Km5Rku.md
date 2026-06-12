Now I have enough calibration data. Let me finalize the review.

**Round 1 bracket: 3.5–5.0**

Key comparisons:
- QubitCache is clearly better than IntelLLM (3.0) — much better evaluation, ablation study
- QubitCache is comparable to KVTQ (4.40) and Quantum entanglement for attention (4.50) — both have limited novelty and similar framing issues
- QubitCache is worse than LazyLLM (5.0) and ChunkKV (5.25) — those papers have clearer, less misleading contributions
- QubitCache is clearly worse than D2O (5.80, accepted) — D2O has a more substantive contribution

**Round 2 narrowing: 3.5–4.5**

The paper's comprehensive evaluation and ablation push it above 3.5, but the pervasive misleading claims and marginal quantum contribution keep it well below 5.0.

**Final score: 4.0**

Here are all the anchors I retrieved and how they compare:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 8QTpYC4smR | 1.00 | 1 | Survey paper, clearly worse than QubitCache |
| 5kMwiMnUip | 1.40 | 1 | Jailbreaking paper, irrelevant |
| gwZ90hFSL2 | 1.00 | 1 | Cross-lingual robots, irrelevant |
| bEgDEyy2Yk | 1.00 | 1 | Graph algorithm, irrelevant |
| 4QWPCTLq20 (IntelLLM) | 3.00 | 1 | KV cache compression, QubitCache has better evaluation |
| 2DD4AXOAZ8 (MixAttention) | 2.00 | 1 | KV cache sharing, QubitCache is more comprehensive |
| vw0NurJ7UX (PrefixQuant) | 3.00 | 1 | Quantization, different approach |
| E4Fk3YuG56 (Cut Cross-Entropy) | 2.67 | 1 | Loss computation, different topic |
| am5Z8dXoaV (LazyLLM) | 5.00 | 1 | Dynamic token pruning, clearer contribution than QubitCache |
| 0ZcQhdyI3n (LSH-E) | 3.83 | 1 | KV cache compression, QubitCache has better evaluation |
| 8sglLco8Ti (ChunkKV) | 5.25 | 1 | Chunk-based eviction, more straightforward than QubitCache |
| pG820nmDvy (Running Huge) | 4.67 | 1 | Top-k attention, rejected |
| lRTDMGYCpy (Critical KV Cache) | 5.75 | 1 | Output perturbation, rejected |
| HzBfoUdjHt (D2O) | 5.80 | 1 | Dynamic operations, accepted; stronger than QubitCache |
| jZVNmDiU86 (PyramidKV) | 5.60 | 1 | Pyramidal funneling, rejected |
| CkCFoN3j4s (Locret) | 5.80 | 1 | Trained retaining heads, rejected |
| OfjIlbelrT (FlexPrefill) | 8.00 | 1 | Context-aware sparse attention, much stronger |
| wg1PCg3CUP (Scaling Laws) | 8.00 | 1 | Precision scaling laws, different topic |
| hqxzi4d3Ws | 3.00 | 1 | Quantum circuits noise resilience |
| bB0OKNpznp | 6.00 | 1 | Quantum parameter adaptation, accepted |
| eZAlb8fX5y (KVTQ) | 4.40 | 2 | Ternary quantization, similar novelty issues |
| 0ZcQhdyI3n (LSH-E) | 3.83 | 2 | KV cache, similar tier |
| xHPVGmLXjd (QJL) | 3.50 | 2 | 1-bit quantization KV cache |
| 3jRzJVf3OQ | 4.50 | 2 | Quantum entanglement attention, similar quantum framing issues |
| usX2ixXopC | 4.00 | 2 | Quantum transformer, similar issues |
| PWtx9fJqM5 | 5.00 | 2 | Attention mechanism study |
| QlvL6eEOC6 | 4.50 | 2 | KV prediction for TTFT |

---

## Summary
QubitCache proposes a KV cache compression framework that partitions tokens into anchor, recent, critical, and non-critical categories, encodes the attention patterns of non-critical tokens (85%) into quantum states via amplitude encoding, and during inference uses hybrid attention combining hard attention over preserved tokens with soft probabilistic attention over non-critical tokens. The paper claims 7× memory compression while maintaining 92-97% of baseline performance across 5 models and 7 benchmarks, and frames this as a "paradigm shift" from token selection to relational structure preservation.

## Strengths
- **Well-designed ablation study (Table 4):** Removing attention-based critical token selection causes a 20.4% F1 drop (0.491→0.391), while removing position-based anchor or recent tokens causes only 0.6% each. Random selection with quantum encoding achieves only 68.2% of QubitCache's performance at matched retention, empirically validating that attention-based selection drives compression quality.
- **Comprehensive evaluation across diverse models and benchmarks:** 5 architecturally diverse models (Llama-8B, Mistral-7B, Phi-4-mini, Qwen2-7B, DeepSeek-Coder-7B) and 7 benchmarks spanning language modeling, commonsense reasoning, multi-hop QA, and summarization. QubitCache outperforms all baselines in 33 of 35 reported metric-model combinations in Table 1.
- **Empirically validated memory efficiency (Table 3):** Concrete GPU memory measurements on 8K-token sequences show QubitCache at 0.55 GB vs Full KV at 3.91 GB, confirming 7× compression with actual hardware measurements.
- **Comparison against GEAR at similar compression:** Against GEAR (6.7×), QubitCache (7×) shows consistent improvements, e.g., 14.3% on HotpotQA with Llama-8B (0.510 vs 0.446), validating the method at matched compression ratios.
- **Transparent acknowledgment of classical simulation (line 100):** The paper explicitly states the current implementation operates as classical simulation on GPU hardware.

## Weaknesses

### Fatal
None.

### Major
- **Misleading "logarithmic compression" framing pervades the paper.** The paper repeatedly claims "logarithmic compression beyond classical information-theoretic limits" (Abstract, line 9) and lists memory complexity as O(L × H × 0.15S × D + log N) in Table 3. In a classical simulation (which is what the paper implements, per line 100), a 9-qubit quantum state is specified by 2⁹ = 512 complex amplitudes — 512 floats, not 9. The paper itself acknowledges in Section 2 that "arbitrary state preparation requires O(2ⁿ) gates in the general case." The +log N term conflates the number of qubits with the information content of the quantum state. In practice the quantum state overhead is negligible compared to the KV cache, so this doesn't affect the actual memory savings, but it is a conceptual error that pervades the narrative. The real compression comes from retaining 15% of tokens — aggressive token eviction — not from logarithmic encoding.

- **Baseline comparisons at mismatched compression ratios.** Table 3 explicitly shows ScissorHand, H2O, and StreamingLLM at 2× compression (50% retention) while QubitCache operates at 7× (15% retention). All performance comparisons in Table 1 use these non-matched ratios. The paper never runs H2O or ScissorHand at 15% retention to isolate whether the quantum encoding or even the specific token selection strategy provides value over existing methods at the same compression level. The only same-ratio comparison is vs GEAR (6.7×), where improvements are more modest (typically 5-14%). Without a matched-ratio ablation, it is impossible to determine how much of QubitCache's advantage comes from compressing more aggressively versus the quantum encoding mechanism.

- **Systematically overstated claims relative to the paper's own data.** (1) "92-97% of baseline performance across all tasks" (lines 9, 25, 29, 178): DeepSeek-Coder retains only 75.5% on HotpotQA (0.256/0.339), 80.8% on PG19, and 75.9% on SummScreen. Mistral-7B HotpotQA is 81.1%. Llama-8B TriviaQA is 84.9%. Multiple model-task combinations fall well below 92%. (2) "15-25% higher F1 scores on multi-hop reasoning tasks" (Abstract): On HotpotQA with Llama-8B, QubitCache vs H2O is only 1.6% relative improvement (0.510 vs 0.502). The 15-25% range is cherry-picked from specific model-baseline pairs. (3) "order of magnitude reduction" (line 25): 7× is not an order of magnitude.

- **The paper's own ablation undermines its central thesis.** Table 4 shows "No Quantum" achieves 0.472 vs Full QubitCache's 0.491 — only a 3.9% improvement from the quantum encoding. Meanwhile, "Random + Quantum" (0.335) is essentially identical to "Random No Quantum" (0.334), showing quantum encoding provides no benefit without intelligent token selection. This directly contradicts the paper's claim of a "paradigm shift from token selection to relational structure preservation" — the paper's own data shows token selection IS the critical component, and the quantum encoding is marginal.

### Minor
- **No latency or throughput analysis.** The quantum circuit simulation involves computing segment-wise amplitude encoding, measurement probabilities, and value interpolation for every attention layer at every generation step. No wall-clock latency or throughput benchmarks are reported, making it impossible to assess computational overhead.
- **Evaluation limited to short sequences (2K-8K tokens).** For a method targeting long-context applications (the introduction discusses 100K-token sequences), evaluating only up to 8K tokens is insufficient — two orders of magnitude shorter than the claimed use case.
- **Ablation table (Table 4) lacks context.** The ablation does not specify which model, task, or sequence length is used, making the numbers difficult to interpret. The "No Quantum" configuration is also not precisely described.

### Trivial
None.

## Nice-to-Haves
- Run H2O/ScissorHand at 15% retention to directly test whether the quantum encoding adds value over simple aggressive token eviction at matched compression.
- Add wall-clock latency measurements and test on longer sequences (32K-128K tokens).
- Correct the overstated claims to accurately reflect the data.
- Frame the contribution honestly as attention-weighted soft token reconstruction rather than "quantum compression beyond classical limits."

## Removed Points
These points are flagged to be removed, treat them with caution.
- "IDW interpolation is simplistic" — this is a design choice, not a flaw. The paper acknowledges locality bias and cites supporting work (Abnar & Zuidema, 2020; Xiao et al., 2023b).
- "GEAR is a different category of compression" — the paper compares against multiple categories, and GEAR is at a similar compression ratio, making the comparison informative.
- "O(log n) amortized update cost is suspicious" — the paper describes a sliding window approach where only affected segments are updated; without detailed analysis this claim cannot be definitively falsified.
- Missing related works — removed per policy.
- "First framework recognizing attention patterns as primary information carrier" — the paper's claims of novelty are overstated but I cannot verify the existence of specific prior works to confirm overlap.

## Novel Insights
The paper's most interesting empirical finding is that quantum amplitude encoding provides a small but real (3.9%) improvement over plain attention-based token selection, and this improvement vanishes entirely when token selection is random (Table 4, Random+Quantum vs Random No Quantum: 0.335 vs 0.334). This interaction effect — quantum encoding only helps when paired with intelligent token selection — is a genuine observation worth investigating further, though the paper frames it as a paradigm shift when it is a marginal refinement.

## Suggestions
- Run H2O and ScissorHand at 15% retention — this is the single most important missing experiment to isolate the quantum encoding's contribution.
- Reframe the paper honestly: the contribution is attention-weighted soft token reconstruction with probabilistic value interpolation, not "quantum compression beyond classical limits."
- Correct all overstated claims to match the actual data.
- Add latency/throughput measurements and longer sequence evaluation.

## Score and Decision
The paper has genuine contributions — comprehensive evaluation across 5 models and 7 benchmarks, a well-designed ablation study, and empirically validated memory savings. However, it is marred by pervasive misleading claims ("logarithmic compression beyond classical limits"), systematically overstated performance numbers, unfair baseline comparisons at mismatched compression ratios, and a core quantum contribution that the paper's own ablation shows to be marginal (3.9%). Compared to calibration anchors, QubitCache sits above IntelLLM (3.0) and KVTQ (4.40) due to better evaluation, but below LazyLLM (5.0) and ChunkKV (5.25) which have clearer, less misleading contributions, and well below D2O (5.80, accepted) which has a more substantive technical contribution.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>