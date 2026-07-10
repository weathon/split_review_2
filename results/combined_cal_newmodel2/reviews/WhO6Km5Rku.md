Now I have a solid calibration. Let me write the final consolidated review.

## Summary

This paper proposes QubitCache, a hybrid KV-cache compression framework that combines classical token storage with quantum-inspired amplitude encoding of attention patterns. The core insight — that attention relationships between tokens may be more important to preserve than individual token identities — is well-motivated. The method partitions tokens into preserved (anchor, recent, critical; ~15%) and non-critical (~85%) sets, encodes the attention patterns of non-critical tokens into 9-qubit quantum states, and reconstructs soft attention weights during inference via probabilistic measurement. Evaluated across five models (4B–70B) and seven benchmarks, the paper reports 7× memory compression.

## Strengths

- **Well-motivated problem framing.** The paper convincingly argues (Section 1, 2) that existing KV-cache compression methods focus on binary token selection while the relational structure encoded in attention patterns may be a more important information carrier. It marshals relevant citations (Michel et al., 2019a; Choromanski et al., 2020; Jaszczur et al., 2021) to support this claim and stays true to this framing throughout.

- **Comprehensive evaluation scope.** The paper evaluates across five models (4B–8B plus 30B and 70B in Section 4.3) and seven benchmarks spanning language modeling, multi-hop QA, summarization, and commonsense reasoning, with comparisons against five baselines (ScissorHands, H2O, StreamingLLM, GEAR, FullKV) in Tables 1 and 2.

- **Ablation study cleanly identifies the main driver.** Table 4 shows that removing critical tokens (attention-score-based selection) causes a 20.4% performance drop, while removing the quantum encoding ("No Quantum") causes only a 3.9% drop. This is honest reporting that reveals which component actually drives performance. The random selection baselines (0.334–0.335 F1) convincingly demonstrate that attention-based selection is essential.

## Weaknesses

### Fatal
None.

### Major

- **Headline performance claims are not uniformly supported by the data.** The abstract claims "92-97% of baseline performance across five models and six benchmarks" and "15-25% higher F1 scores on multi-hop reasoning tasks." Computing from Table 1: For DeepSeek-Coder, 5 of 7 benchmarks fall below 92% retention (HotpotQA: 75.5%, PG19: 80.8%, PIQA: 87.8%, TriviaQA: 86.0%, SummScreen: 75.9%). The 15-25% multi-hop improvement claim is only consistently true for Qwen2-7B vs H2O (+24.0%); most other comparisons show smaller gains (e.g., Mistral-7B vs H2O: +9.3%, DeepSeek-Coder vs H2O: +9.4%, Llama-8B vs H2O: +1.6%). These ranges are stated globally in the abstract and introduction (lines 9, 25, 29, 34) without qualification by model or baseline, which overstates what Table 1 actually shows.

- **The quantum encoding's memory-complexity claim is misleading for the classical implementation.** The paper lists memory complexity as `O(L × H × 0.15S × D + log N)` (Table 3) and claims "logarithmic compression beyond classical information-theoretic limits" (abstract). However, Section 3.2.2 explicitly states the implementation "operates as a classical simulation" using Qiskit. On classical hardware, simulating a 9-qubit state requires storing 2⁹ = 512 complex amplitudes per state vector — O(N), not O(log N). Across 32 layers × 32 heads × ~16 segments, this adds approximately 131 MB of simulation overhead that the reported 0.55 GB figure may or may not include. The complexity expression and the "beyond classical limits" claim do not reflect the actual memory footprint of the implemented system.

- **The quantum component contributes modestly relative to the paper's framing.** Table 4 shows that removing the quantum encoding reduces F1 from 0.491 to 0.472 — a 3.9% drop — while removing critical-token selection causes a 20.4% drop. The paper frames its contribution as a "paradigm shift from discrete token selection to continuous relational preservation through quantum-inspired encoding" (abstract), but the empirical evidence shows the primary driver is attention-score-based token selection (a mechanism similar to H2O and ScissorHands), with the quantum encoding providing a small additive benefit. The claimed paradigm shift is not proportionate to the evidence.

### Minor

- **No statistical reporting for a method with probabilistic components.** The method reconstructs attention weights through quantum state measurement probabilities (p_j(ψ) = |⟨j|ψ⟩|²), which is fundamentally stochastic. Yet all results in Tables 1 and 2 are reported as point estimates with no variance, standard deviations, or confidence intervals. Without this, it is unclear whether QubitCache's small advantages over baselines (e.g., 0.121 vs 0.124 on PG19 for Mistral-7B) are meaningful or within noise.

- **No runtime/latency analysis.** The paper reports memory savings (Table 3) but provides no latency or throughput comparison. Since the method uses Qiskit for quantum circuit simulation — which is computationally expensive — it is unclear whether the compression gains come at a prohibitive inference speed cost. This is a practical concern for any deployment-oriented compression method.

- **The "103% of baseline performance" claim is stated without explanation.** Figure 3b's caption states that a circuit depth of 15 achieves "103% of baseline performance." A compression method exceeding uncompressed performance is unusual and likely reflects a measurement artifact or benchmark peculiarity. The paper does not address this.

### Trivial
None.

## Nice-to-Haves
- The paper could include runtime overhead measurements to establish practical deployability.
- Variance estimates (e.g., over multiple random seeds) would strengthen confidence in the results, especially given the probabilistic reconstruction.
- Clarifying whether the reported 0.55 GB memory figure includes the quantum simulation state vectors would improve transparency.

## Removed Points
These points from the input review were removed:
- "Quantum component is not novel" — the paper's novelty is the hybrid architecture, not the quantum encoding alone; removed as a strawman.
- "PG19 evaluated with F1, not perplexity" — while unusual, this is a consistent design choice; removed as a nitpick.
- "Bolding convention is misleading" — standard field practice; removed as a formatting nitpick.
- "Retention ratio for No Quantum ablation not stated" — minor omission, the paper likely uses the same 15% retention; removed as overly granular.
- "Missing implementation details from appendix" — parser strips appendices; removed per hard rules.
- "Drop the quantum framing" — a suggestion, not a weakness of the paper as presented.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Qualify the headline claims (92-97%, 15-25%) in the abstract and introduction with the specific model-baseline combinations where they hold, or report task-wise retention ratios transparently.
- Revise the memory complexity expression to reflect the actual classical simulation cost (O(N) rather than O(log N) for the quantum component).
- Report variance estimates for main results, especially given the probabilistic reconstruction mechanism.
- Include throughput/latency benchmarks to assess practical deployability.
- Either explain or remove the "103% of baseline" claim.

## Score and Decision

**Calibration summary.** All anchors retrieved:

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| IntelLLM (4QWPCTLq20) | 3.00 | 1 | Yes | Weaker evaluation, unsubstantiated theorems. QubitCache has broader evaluation and more honest ablation. |
| QJL (xHPVGmLXjd) | 3.50 | 2 | Yes | Similar overclaiming issues (claimed "zero overhead" when using 1-bit). QubitCache has a more novel core insight. |
| DynamicKV (uHkfU4TaPh) | 4.40 | 2 | Yes | Limited novelty, no efficiency evaluation. QubitCache has a more original idea but also overclaiming. |
| KVTQ (eZAlb8fX5y) | 4.40 | 1 | No | Solid quantization approach, limited novelty. Comparable execution quality. |
| Don't Discard/MiKV (CRQ8JuQDEd) | 5.00 | 1 | Yes | Mixed reviews on novelty but practical. QubitCache has a more novel core insight but worse overclaiming. |
| PyramidKV (jZVNmDiU86) | 5.60 | 1 | Yes | Rejected despite 5.60 avg. Interesting observation, inconsistent results. |
| MatryoshkaKV (BQwsRy1h3U) | 6.00 | 1 | No | Solid, clean paper with no major overclaiming. QubitCache is clearly weaker. |
| SqueezeAttention (9HK2rHNAhd) | 5.50 | 2 | No | Accepted. Clean execution. |

**Bracket and narrowing.** Round 1 bracketing placed the paper between 3.0 and 5.0 (weaker than MiKV at 5.0, stronger than IntelLLM at 3.0). Round 2 narrowed with DynamicKV (4.40) and QJL (3.50) as closest comparators. QubitCache's three most damaging weakness items (favorability scores: 0.05, -0.20, -0.78 — the overstated claims, misleading memory complexity, and modest quantum contribution) are comparable in damage level to the most damaging items in QJL (e.g., "marginal improvements" at -3.76) and DynamicKV (e.g., "limited novelty" at -4.19, "no efficiency eval" at -2.90). However, QubitCache has stronger positive items (well-motivated framing at 11.30, comprehensive evaluation at 8.11) than either QJL or DynamicKV. The paper's core insight about attention relationship preservation is genuinely novel, but the quantum framing inflates the contribution and the headline claims do not match the data. On balance, the paper is between QJL (3.50) and DynamicKV (4.40), with a final score of **4.0**.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>