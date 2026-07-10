Now I have all the calibration data. Let me write the final consolidated review.

## Summary

This paper provides the first formal analysis of critical KV cache identification from an output perturbation perspective. It derives an upper bound on output perturbation (Theorem 3.3) that depends on both attention weights *and* projected value state norms $||V_{i,:}W^O||_1$, revealing a blind spot in prior attention-only methods. Based on this insight, the authors design a two-stage perturbation-constrained selection algorithm that first prioritizes entries by attention weight, then jointly considers attention and value norms. When integrated as a plug-and-play enhancement into SnapKV, AdaKV, and HeadKV across three LLMs (Llama-3.1-8B, Mistral-7B, Qwen2.5-32B), the algorithm reduces compression loss substantially on 29 datasets from Ruler and LongBench, and on SCBench multi-turn QA. The empirical validation is backed by head/layer/budget-level perturbation analysis confirming the mechanism.

## Strengths

- **Formal grounding of a previously heuristic problem.** Theorem 3.3's derivation showing that output perturbation's upper bound depends on *both* attention weights $A_i$ *and* projected value state norms $||V_{i,:}W^O||_1$ is genuinely novel and identifies a concrete oversimplification in all prior attention-only methods. This is not a minor tweak but a principled advance over accumulated-attention heuristics (H2O, SnapKV, AdaKV).

- **Consistently strong empirical results across diverse settings.** Across 29 datasets (Ruler + LongBench), three model families (Llama-3.1-8B, Mistral-7B, Qwen2.5-32B), three cache eviction methods (SnapKV, AdaKV, HeadKV), and multiple cache budgets, the algorithm improves upon the base method in nearly every case. Striking examples: on Ruler at 40% cache, AdaKV's loss on Mistral drops from 55.4% to 11.6%; on Qwen, AdaKV's loss drops from 24.3% to 0.69% (Table 1). On LongBench, 97.8% success rate (88/90) across long-dependency domains. The SCBench multi-turn evaluation (Table 3) provides corroborating evidence.

- **Negligible computational overhead.** The additional computation is a single $||VW^O||_1$ norm per head (linear complexity). TTFT increase is 0.06s on 32K context for batch size 1 (3.54s → 3.60s, a 1.7% increase), and decoding latency is unaffected because selection happens during prefill. This means the method can be adopted without practical deployment cost.

- **Mechanism validation via perturbation analysis.** Section 4.7 confirms that the algorithm actually reduces measured output perturbation across heads (92% of Llama heads, 86% of Mistral heads), across layers (progressively accumulating to near-zero in the final layer), and across budget sizes. This provides empirical evidence bridging the theoretical upper bound and practical performance.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Algorithm 1 pseudocode contains a notation bug and an inconsistent default.** Stage 1 is described in the text (lines 126–127) as selecting entries with high attention weights. However, line 5 selects entries where $A_i \in \text{Top}_k(\mathcal{A}, b')$ — checking whether the attention weight $A_i$ belongs to the top-k of the *combined score* $\mathcal{A}$. This is mathematically incoherent (comparing values from two different vectors). The correct expression should select by $\text{Top}_k(A, b')$ for Stage 1. Additionally, the input signature lists $\alpha = 0.25$ as default (line 132), while all experiments use $\alpha = 0.5$ (Section 4.1). The two-stage logic and the $\alpha$ default should be reconciled.

- **Integration of Algorithm 1 into the observation-window framework is underspecified.** Algorithm 1 takes a single query vector $q$ and computes attention from scratch (line 2). However, the methods it integrates with (SnapKV, AdaKV, HeadKV) use accumulated attention scores over an observation window of multiple queries (Algorithm 2, lines 2–4, producing $\bar{A}$). Algorithm 2 line 8 calls Algorithm 1 without specifying which query(s) to pass or whether the accumulated $\bar{A}$ replaces the internal attention computation. The theoretical derivation (Theorems 3.2–3.5) is based on single-query attention, but the deployed method likely uses accumulated attention — the paper does not clarify this gap.

- **The explanation for Mistral's $\alpha = 0$ failure is incomplete.** Table 4 shows $\alpha = 0$ (using only the combined score $A_i \cdot ||V_{i,:}||_1$ with no attention-prioritization) collapses performance on Mistral (31.94 vs. 42.85 at $\alpha = 0.5$, below baseline AdaKV at 41.18). The paper attributes this to "violation of Assumption 3.4" (lines 314–315), which restates the phenomenon rather than explaining *why* the combined metric selects poorly for Mistral specifically. A brief diagnostic — e.g., showing the distribution of $||VW^O||$ norms across Mistral heads vs. Llama heads — would clarify whether the two-stage design is a principled safeguard or a heuristic patch.

### Trivial
None.

## Nice-to-Haves

- A clean ablation comparing three designs (attention-only, combined-score single-stage, combined-score two-stage) across all models would precisely isolate each component's contribution.
- Perturbation analysis at later decoding tokens (beyond the first) would strengthen the mechanism claim, though the current choice is methodologically justified.
- Standard deviations for representative results (e.g., the main Ruler result at 40% cache) would help assess whether modest gains are statistically distinguishable from noise.

## Removed Points

- *Figure caption clarity about "4 samples per batch" / "1 sample per batch":* The paper's text in Section 4.6 clearly explains the batching setup. The figure captions are parser extraction artifacts.
- *Request for standard deviations or significance tests:* Single-run evaluation on large benchmarks is the norm in this community; this is a nice-to-have.
- *Perturbation analysis measures only first decoding token:* The paper explicitly states this choice and it is a reasonable methodological decision to isolate cache compression effects from autoregressive error accumulation.
- *Abstract claim "more than half" is slightly inflated:* The combined average across both benchmarks (29 datasets) does exceed 50%; the critic's 49.2% figure was for LongBench alone.
- *Compression scenario does not include question queries:* The paper explicitly acknowledges this design choice (line 198) and references Appendix F for the joint setting.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix Algorithm 1**: rename the combined score variable (e.g., $\mathcal{S}$ instead of $\mathcal{A}$), make Stage 1 select by $\text{Top}_k(A, b')$, and change the default $\alpha$ to 0.5 to match experiments.
2. **Clarify integration path**: state explicitly how Algorithm 1 receives input in the observation-window context — whether it receives the accumulated $\bar{A}$ directly, or uses a representative query, or is called per-window-query.
3. **Add diagnostic for Mistral $\alpha=0$ collapse**: show the distribution of $||VW^O||$ norms across Mistral heads vs. Llama heads, and discuss whether the two-stage design is a principled safeguard or an ad-hoc patch.

## Score and Decision

**Round-1 Bracket: 5.5–7.5.** The same paper from a prior review cycle (lRTDMGYCpy, avg 5.75) had reviewers requesting needle-in-haystack tasks, larger models, stronger baselines, and efficiency analysis — all of which the current version now includes. The current version is clearly above 5.75. Papers at the lower end of this bracket (ChunkKV avg 5.25, PyramidKV avg 5.60) have more severe weaknesses (novelty concerns, missing comparisons, questionable practical utility). The current paper's weaknesses are uniformly minor (presentation clarity, diagnostic depth). HeadKV (avg 6.50) — a well-reviewed KV cache paper in the same area — has comparable evaluation breadth but less theoretical grounding and was criticized for limited generality. The current paper has stronger theoretical novelty and broader empirical scope.

**Round-2 Narrowing: 6.5–7.5.** Compared to HeadKV (6.50), the current paper offers a more general theoretical framework (applicable to any attention-weight-based method) rather than a task-specific head importance scoring scheme, and its evaluation is broader (29 datasets vs. LongBench+LooGLE). However, it falls short of the FlexPrefill level (avg 8.00), which had uniformly strong methodology with no substantial presentation issues. The favorability comparison confirms: the current paper's strengths are rated very highly (10.48–15.28), while its weaknesses are uniformly low-severity (1.42–6.95), with no item below zero. By contrast, HeadKV's item ratings included negative- and near-zero-favorability items (e.g., "marginal contribution" at -3.22, "not practically useful" at -0.53). The current paper has no such critical items.

**Final Score: 7.0. Decision: Accept.** The paper's theoretical contribution is genuine and practically useful, the empirical evaluation is the most comprehensive among comparable KV cache papers, and the remaining weaknesses are presentation issues that can be resolved in revision.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>