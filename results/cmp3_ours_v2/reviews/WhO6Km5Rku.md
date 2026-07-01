## Summary

QubitCache proposes a hybrid KV-cache compression method that retains 15% of tokens (critical/anchor/recent) in classical storage while encoding attention patterns of the remaining 85% into quantum-inspired amplitude representations. During inference, compressed tokens are reconstructed via interpolation weighted by quantum measurement probabilities. The core insight — that preserving token relationships matters more than preserving tokens — is reasonable and supported by the ablation study. However, the paper's central empirical claims are contradicted by its own Table 1, and the quantum encoding provides no compression in the actual classical-simulation implementation.

## Strengths

- **Core insight is well-motivated and validated by the ablation study.** The observation that attention relationships carry more information than individual tokens (Section 1, lines 21–22) is genuine, and the ablation in Table 4 cleanly demonstrates that attention-based token selection drives performance (~20.4% F1 drop without critical tokens selected by attention vs. ~0.6% for anchor/recent tokens). This is the paper's most transparent and valuable result.

- **Broad evaluation coverage.** The paper tests across five 4B–8B models (Llama-3-8B, Mistral-7B, Phi-4-mini, Qwen2-7B, DeepSeek-Coder-7B) and extends to larger models (Llama-70B, Qwen-30B) on seven benchmarks (Tables 1–2).

## Weaknesses

### Fatal
None.

### Major

- **Headline performance claim contradicted by the paper's own data.** The abstract and introduction claim QubitCache "maintains 92-97% of baseline performance across five models and six benchmarks" (line 9). Computing ratios from Table 1: DeepSeek-Coder achieves 75.5% on HotpotQA, 80.8% on PG19, 86.0% on TriviaQA, and a model-wide average of ~85.8%. Llama-8B achieves 84.9% on TriviaQA, Phi-4-mini achieves 82.4% on SummScreen and 90.9% on PIQA. Multiple entries across multiple models fall well below 92%. The paper's own empirical data disproves this central claim, which is presented as the headline result in the abstract, introduction (lines 9, 25, 29), and conclusion (line 256).

- **Quantum encoding provides no compression in the classical-simulation implementation, with incorrect memory accounting.** The paper states "the current implementation operates as a classical simulation" (line 100). A 9-qubit classical simulation stores 2^9 = 512 complex amplitudes per segment — the same cardinality as the 512 attention weights being encoded (line 84). The encoding itself achieves zero compression; all memory savings come from discarding 85% of token KV pairs. The memory complexity in Table 3 lists "O(L×H×0.15S×D + log N)", but the "log N" term is incorrect for classical simulation, which requires O(#segments × 2^9 × complex), i.e. O(S) storage. The claim of "logarithmic compression beyond classical information-theoretic limits" (line 9) conflates qubit counts with actual memory: on real quantum hardware, extracting 512 probability amplitudes from 9 qubits at useful precision would require a number of measurements the paper never analyzes. The ablation study (Table 4) confirms the quantum component contributes only ~3.9% relative improvement (F1 0.472→0.491), further demonstrating it is not driving performance.

### Minor

- **No latency or throughput measurements reported.** The paper claims "minimal latency overhead" (line 216) and describes optimizations (line 132), but reports zero wall-clock timing data. For a method that requires per-segment, per-layer, per-head 9-qubit circuit simulation during autoregressive generation, this is a significant omission that leaves the practical feasibility claim unverifiable.

- **"15-25% higher F1 on multi-hop reasoning" claim is inconsistently supported.** Comparing QubitCache to H2O on HotpotQA (the multi-hop benchmark): improvements range from 1.6% (Llama-8B) to 41.8% (Phi-4-mini), with several models (Mistral-7B at 9.3%, DeepSeek-Coder at 9.4%) falling well below 15%. The claim is too broad given the variance.

### Trivial
- No error bars, standard deviations, or statistical significance measures reported for any result in Tables 1, 2, or 4.

## Nice-to-Haves

- Comparisons at matched compression ratios (e.g., H2O/ScissorHand at 15% retention instead of their default 50%) would more cleanly isolate the benefit of the attention-reconstruction component.
- A discussion of why DeepSeek-Coder consistently performs much worse under any compression method (75–88% of baseline across most metrics) would improve the analysis.

## Removed Points

- **Missing theoretical proof:** The paper claims to "prove" rank-preservation with bounded error (lines 9, 25) but no theorem appears in the main body. Per review policy, the appendix was stripped by the parser and may have contained the proof. Removed per the rule that parser-stripped sections are not grounds for criticism.
- **Ablation comparison confusion about 49.8% retention:** The critic argued the random baselines at 49.8% retention make the comparison unfair. This is a misreading — the paper shows that random selection with ~3× more tokens (49.8% vs. 15%) still underperforms QubitCache, which actually strengthens the paper's argument. Removed.
- **LongBench labeling concern:** The critic noted LongBench metrics are absent from Table 1. HotpotQA, TriviaQA, and GovReport are standard LongBench sub-tasks; this labeling is correct. Removed.
- **O(2^n) gate cost as a fatal weakness:** The paper acknowledges the general-case cost in Section 2 (line 40). Whether the specific encoding avoids this is a reasonable question but not a demonstrated error. Demoted from the weakness list.
- **Section-by-section editorial notes** that are observational rather than identifying specific, verifiable errors.
- **Generic strengths** about importance of the problem or "paradigm shift" framing.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct or retract the "92-97%" claim** in the abstract and introduction to honestly reflect the Table 1 data. This is the single most damaging overclaim and should be the authors' top priority.
2. **Report wall-clock inference throughput** (tokens/sec) for QubitCache and all baselines, since the paper targets practical inference.
3. **Clarify memory accounting:** disclose the actual storage cost of the classical 9-qubit simulation (512 complex amplitudes per segment) and explain why this is not a net memory increase over the original attention weights.
4. **Either provide the promised theoretical proof** or remove the claim of provable guarantees from the abstract.
5. **Add error bars or variance estimates** to all main-table results.
6. **Consider removing or deprioritizing the quantum framing** — the paper's own ablation shows it contributes ~4% relative improvement, while the attention-based token selection and interpolation are the real drivers.

---

**Calibration round 1 bracket:** This paper sits between 2 and 4, based on comparison with similar KV-cache compression papers.

**Calibration anchors (all rounds):**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4QWPCTLq20.md` (IntelLLM, avg 3.00, round 1): KV cache eviction with overclaimed theorems and missing baselines. QubitCache has similar issues but with more severe factual inaccuracies (false 92-97% claim).
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/CRQ8JuQDEd.md` (MiKV, avg 5.00, round 1): Mixed-precision KV cache with solid empirical support. QubitCache is substantially weaker, lacking the empirical grounding this paper has.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FkXYvV7nEB.md` (KV-Dict, avg 5.25, round 1): Sparse dictionary learning for KV cache; also missing latency data but has no factual errors. QubitCache has more severe problems.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/vM4CdVScT8.md` (Quantum Entanglement Trees, avg 4.00, round 2): Quantum-named classical method; reviewers criticized the ornamental quantum framing. QubitCache's quantum machinery is similarly ornamental but with worse factual overclaims.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/eZAlb8fX5y.md` (KVTQ, avg 4.40, round 2): Ternary KV cache quantization with reasonable claims and no false assertions. QubitCache is weaker.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0ZcQhdyI3n.md` (LSH-E, avg 3.83, round 2): LSH-based KV cache eviction with moderate novelty concerns. QubitCache has more severe factual issues.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>