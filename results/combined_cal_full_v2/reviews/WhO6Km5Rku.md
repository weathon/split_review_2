Now I have all the information needed. Let me finalize the review with the calibrated score.

**Round 1 Bracket:** Based on the calibration search, the paper fits in the 3.0–5.0 range among KV cache compression papers that have evaluation issues. The anchors in that band (IntelLLM avg 3.00, LSH-E avg 3.83, MiKV avg 5.00, ChunkKV avg 5.25) all have similar structural characteristics (novelty concerns, missing baselines, no latency reporting) but none have the additional burden of a cosmetic quantum formalism that inflates the contribution.

**Narrowing (Round 2):** Comparing weighted items, IntelLLM (3.00) is the closest match — its most negative items are -4.33, -4.75, -4.25 (missing references, insufficient baselines, unclear writing), while my paper's most negative is -3.37 (quantum formalism ornamental). However, my paper's quantum formalism is a deeper problem than IntelLLM's issues because it misrepresents what the method actually does (it's not about missing references or incomplete evaluation; it's about the core claimed contribution being overstated). The unfair comparison weakness (-0.39) and unsupported performance claims (1.74) add additional burden. LSH-E (3.83) had a strongest negative of -3.38 (limited novelty) but cleaner claims overall.

**Final Score:** 3.0. The paper has real empirical content (7× compression, useful ablation), but the quantum framing is ornamental and the central claims are overstated in ways visible from the paper's own data. The evaluation stacks baselines at a much lower compression ratio, and performance retention claims fail for multiple task-model pairs. The underlying heuristic (static importance-weighted interpolation of discarded tokens) is reasonable but does not justify the quantum formalism or the "relational structure preservation" framing. This places it among papers that have real contributions but significant methodological or presentation problems that preclude acceptance.

---

## Summary

This paper proposes QubitCache, a KV-cache compression method that encodes attention importance scores of non-critical tokens into "quantum-inspired" amplitude encodings (simulated classically) and uses the decoded probabilities as static interpolation weights for their value vectors during inference, achieving 7× memory compression.

## Strengths

- **The 7× memory reduction is substantial and internally consistent** (Table 3): 0.55 GB vs 3.91 GB for Full KV on 8K sequences with Llama-8B, matching the stated 15% token retention. This is a genuine achievement. [weight=9.54]

- **The ablation study (Table 4) provides useful signal**: removing attention-selected "critical" tokens causes a 20.4% performance drop, while removing anchor or recent tokens has negligible effect (~0.6%). This cleanly identifies attention-based importance scoring (not the quantum encoding) as the active ingredient. [weight=8.82]

- **The paper correctly identifies an underexplored direction**: framing KV-cache compression as preserving attention relationships rather than just selecting tokens. This motivation, supported by references to Michel et al. 2019 and Choromanski et al. 2020 (lines 21-22), is a valid starting point. [weight=8.26]

## Weaknesses

### Major

- **The quantum formalism is ornamental and adds no algorithmic value.** The method (Eq. 3-5) computes static normalized attention weights α_i = a_i / Σ a_j, encodes them as amplitudes in a quantum state, and "measures" to recover p_j = |⟨j|ψ⟩|² = α_j — which simply retrieves the pre-computed weights. During inference (Eq. 6-7), these static weights are used for value vector interpolation; there is no dynamic, query-dependent attention reconstruction. The paper admits it is a classical simulation (line 100). Storing the normalized scores as FP32 values and using them directly as interpolation weights would achieve identical behavior. The claim of "logarithmic compression beyond classical information-theoretic limits" (line 9) is misleading for a classical simulation of amplitude encoding. [weight=-3.37]

- **The comparison to baselines is fundamentally unfair.** Table 3 evaluates H2O, ScissorHands, and StreamingLLM at only 2× compression (50% retention) while QubitCache operates at 7× (15% retention). These baselines can operate at higher compression ratios by adjusting their retention budgets — the paper evaluates them at a point that makes them look weaker. Only GEAR (6.7×) is at a comparable ratio, and QubitCache's advantage over GEAR is modest (1-14% relative improvement on most tasks). All methods should be compared at matched compression ratios. [weight=-0.39]

- **The method does not actually preserve pairwise "relational structure"** as the paper's central framing claims. Eq. (3) computes a_i^{(l,h)} = Σ_j A_{j,i}^{(l,h)} — accumulated incoming attention to each token, yielding a single scalar per token, not pairwise relationships between arbitrary query-key pairs. During autoregressive generation, the pre-computed static weights p_j interpolate value vectors (Eq. 6-7) without dynamic, query-dependent attention for compressed tokens. The claimed "paradigm shift from token selection to relational structure preservation" (line 29) is inconsistent with the actual mechanism. [weight=0.34]

- **Performance claims in the abstract and introduction are not uniformly supported.** The "92-97% of baseline performance" claim (lines 9, 29, 178) is violated by multiple task-model pairs in Table 1: DeepSeek-Coder achieves 80.8% on PG19, 75.5% on HotpotQA, 75.9% on SummScreen; Phi-4-mini achieves 82.4% on SummScreen; Llama-8B achieves 84.9% on TriviaQA. The "15-25% higher F1 scores on multi-hop reasoning" claim — against the strongest comparable baseline (GEAR) on HotpotQA — shows improvements of 4.9-14.3%, none reaching 15%. [weight=1.74]

### Minor

- **No latency or throughput measurements.** The paper mentions "minimal latency overhead" (line 216) and three optimizations (gate fusion, parallel segment encoding, adaptive shot allocation) but provides no wall-clock time, tokens-per-second, or end-to-end inference overhead. A 7× memory reduction that incurs non-trivial computational cost needs to be transparent about this tradeoff. [weight=3.88]

- **No variance or statistical significance reported.** Every number in Tables 1, 2, and 4 is a single point estimate with no error bars, standard deviations, or mention of number of runs or random seeds. [weight=1.90]

### Trivial

- **Dataset discrepancy.** Section 4.1.2 (line 136) lists "five benchmark datasets" (LongBench, PG19, SCROLLS, PIQA, LAMBADA) while Table 1 has 7 columns including HotpotQA, TriviaQA, GovReport, Contract, and SummScreen not listed in the setup description. [weight=2.96]

## Nice-to-Haves

- Compare all baselines at matched compression ratios (e.g., all at 7× or at 15% retention).
- Report latency and throughput to quantify the memory-speed tradeoff.
- Add a random 15% retention baseline in the ablation (the current random baselines use 49.8% retention, not 15%).
- Evaluate on longer sequences (>8K tokens) as claimed in the introduction.
- If the rank-r preservation theorem exists, reference it from the main text.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Claimed theorem about rank-r preservation absent from main text (Critic Weakness 7):** The abstract asserts "We prove QubitCache preserves rank r attention structure with bounded reconstruction error" (line 9). Removed because the appendix was stripped by the parser — the theorem and proof likely reside there. The filtering rules prohibit penalizing papers for missing appendix content.
- **GEAR citation error:** The critic flags that GEAR is cited as "(Kang et al., 2024)" rather than the standard reference. Removed because the references section was stripped by the parser and cannot be verified.
- **Full KV baselines look anomalously low:** The critic notes DeepSeek-Coder Full KV scores 0.339 F1 on HotpotQA and 0.100 on TriviaQA. This is speculative — DeepSeek-Coder is a code model and may underperform on text QA tasks even uncompressed.
- **No evaluation on longer sequences:** The paper claims relevance to 100K contexts but evaluates on 2K-8K tokens. This is noted as a scope limitation but not a distinct weakness beyond the evaluation scope.
- **No comparison to random 15% retention:** The ablation uses 49.8% retention for random baselines, not 15%. While informative, this asks for additional experiments beyond the presented scope.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Drop the quantum formalism entirely and present the method directly: maintain 15% of tokens in classical storage; for the remaining 85%, store their normalized attention importance scores and use them as static interpolation weights for value vectors. This would make the core idea — static importance-weighted interpolation as an alternative to binary eviction — transparent and testable.
- Compare all baselines at matched compression ratios.
- Report throughput (tokens/sec) and peak memory under the same hardware.
- Add variance reporting (standard deviations over multiple seeds).
- Ensure all claims in the abstract are verifiable from the data in the paper.

## Score and Decision

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>