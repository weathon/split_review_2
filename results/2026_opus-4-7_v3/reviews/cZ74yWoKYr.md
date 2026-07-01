Now let me verify the key claims from the reviewer. Let me re-read the critical sections.Now I have a thorough understanding of the paper. Let me submit my draft review before calibration.Now let me proceed to calibration Round 1 — Bracketing. I'll search for papers on KV cache eviction / efficient LLM inference across score bands.Interesting — the first result in the 5.5-7.5 band (`lRTDMGYCpy.md`) appears to be the same paper! Let me read it and a few other key anchors.Now let me read the D2O anchor (similar KV cache paper, accepted with 5.80) for comparison:Now I have all the information I need to produce the final consolidated review. Let me synthesize everything.

## Summary
This paper formalizes KV cache entry selection from an output perturbation perspective, deriving an L₁ perturbation upper bound (Theorem 3.3) showing that selection should depend on $A_i \|V_{i,:}W^O\|_1$ (attention weight × projected value norm), not attention weight alone. A two-stage greedy selection algorithm is proposed to minimize this bound and integrated as a plug-and-play enhancement into three SOTA cache eviction methods (SnapKV, AdaKV, HeadKV), demonstrating consistent improvements across three LLMs and 29 datasets from Ruler and LongBench benchmarks.

## Strengths
- **Crisp theoretical insight with direct practical utility (Section 3.3, Theorem 3.3).** The perturbation bound revealing that cache selection should incorporate projected value norms alongside attention weights is a genuine, formally derived contribution that concretely explains *why* attention-weight-only selection is suboptimal. The derivation path through Theorems 3.2→3.3→3.5 is natural. This is not just a heuristic improvement — it is grounded in a clearly stated bound on L₁ perturbation (Eq. 5).

- **Comprehensive experimental coverage (Tables 1–3, Figures 1–2).** The evaluation spans three models (Llama-3.1-8B, Mistral-7B-v0.3, Qwen2.5-32B), three structurally different base methods (SnapKV, AdaKV, HeadKV), 29 datasets across two benchmarks (Ruler and LongBench), plus SCBench for multi-turn QA, at multiple cache sizes. This combinatorial grid is convincingly broad — improvements are not artifacts of a single model-method-dataset combination. The 97.8% success rate across 90 long-dependency test cases (Table 2 discussion) is notable.

- **Direct mechanistic validation (Section 4.7, Figures 4–6).** Showing perturbation reduction in 92% of Llama attention heads (Figure 4) with accumulating advantages across layers (Figure 5) directly validates the theoretical motivation. This goes beyond task-score improvements to demonstrate the method operates through the hypothesized mechanism.

- **Negligible overhead (Section 4.6, Figure 3).** The 0.06s TTFT increase at 32K context length for batch-1 is convincingly small and well-documented. The method replaces only the selection criterion, requiring one linear-complexity computation ($VW^O$ and L₁ norms).

- **Universality as plug-and-play enhancement (Algorithm 2, Section 3.6).** Clean integration into three structurally different eviction frameworks without modifying budget allocation or attention accumulation demonstrates practical modularity.

## Weaknesses

### Fatal
None.

### Major
1. **Gap between single-token theory and observation-window practice.** Theorems 3.2, 3.3, and 3.5 are derived for a single query token where $A = \text{softmax}(qK^T/\sqrt{d})$ is a valid probability distribution summing to 1. However, in Algorithm 2 (lines 2–4), the practical implementation uses averaged/max-pooled attention from an observation window of $n'$ query tokens: $\bar{A} = A.\text{mean}(\text{dim}=0)$ followed by max-pooling. The resulting $\bar{A}$ does not sum to 1 and is not a softmax distribution. The coefficient $(2 - 1/\sigma)$ and bound structure in Theorem 3.3 depend on properties of a probability distribution. The paper never acknowledges this gap. While the strong empirical results suggest the approach transfers, the paper's central narrative of being "formally grounded" is weakened — in practice, it is a theoretically *motivated* heuristic applied outside its exact formal regime. This matters because the paper repeatedly emphasizes formal grounding as its differentiator from prior "empirical" methods.

2. **Algorithm 1 pseudocode ambiguity undermines reproducibility.** Line 5 writes "$A_i \in \text{Top}_k(\mathcal{A}, b')$" while line 8 writes "$\mathcal{A}_i \in \text{Top}_k(\mathcal{A}, b'')$". The text description (Section 3.4: "prioritizes KV cache entries with high attention weights") and Assumption 3.4 ("collect the cache entries corresponding to the highest attention weights, ensuring their cumulative attention weights σ exceed half") clearly imply stage 1 selects by attention weight $A_i$, not the combined score $\mathcal{A}_i$. But the pseudocode appears to use $\mathcal{A}$ for both stages. If both stages rank by the same criterion, the two-stage process is mathematically equivalent to a single Top-k — making the stage split vacuous. This distinction is consequential: the catastrophic failure at $\alpha=0$ on Mistral (Table 4: 31.94 vs 42.85) shows the attention-weight-first stage is necessary for some models. An implementer following the pseudocode literally would get different behavior from the intended algorithm.

### Minor
1. **Missing single-stage ablation to isolate contribution source.** The natural ablation comparing (a) select by $A_i$ alone (baseline), (b) select by $A_i \cdot \|V_{i,:}\|_1$ single-stage, and (c) the two-stage algorithm is absent. The $\alpha$ analysis (Table 4) partially addresses this: $\alpha=0$ on Llama actually performs *best* (44.35 vs 43.77 at $\alpha=0.5$), suggesting the insight alone suffices for some architectures. On Mistral, $\alpha=0$ fails catastrophically. This ablation would sharpen the paper's claims about whether the gain comes from the insight (value norms) or the algorithm (two-stage process).

2. **$\alpha$ hyperparameter inconsistency.** Algorithm 1's input specification states $\alpha = 0.25$ (line 132) but the text (Section 3.5) and all experiments use $\alpha = 0.5$. This likely reflects an earlier draft revision but creates confusion.

3. **SCBench evaluation is underdeveloped.** The multi-turn QA evaluation (Table 3) covers only one model (Llama-3.1-8B) and one base method (AdaKV), while the main experiments cover three models and three methods. This section feels thin by comparison with the main evaluation.

4. **Small code-domain regressions not acknowledged.** Table 2 shows several regressions in the code domain: Llama HeadKV 40% (61.34→57.89), Mistral HeadKV 40% (63.16→61.56), Qwen SnapKV 40% (44.89→43.75). While the paper correctly notes code is insensitive to cache eviction, it dismisses the entire domain rather than acknowledging cases where the method slightly hurts.

5. **"More than half" claim masks variance.** The abstract's claim of reducing compression loss by "more than half on average" is driven by strongest cases (e.g., Qwen+AdaKV on Ruler: 24.3%→0.69%). On Mistral+SnapKV on Ruler, loss drops from 58.9% to only 46.9% (~20% relative reduction). The claim is technically correct on average but the distribution is highly skewed.

### Trivial
1. **V notation overloading.** Section 3.3 uses $\mathbf{V} \in \mathbb{R}^{n \times d} = VW^O$, overloading $V$ (originally the $n \times d_h$ value cache). While clarified in text, $V$ and $\mathbf{V}$ are visually similar in many fonts.

## Nice-to-Haves
- Analysis of bound tightness: how does the bound $\theta$ compare to actual perturbation $\mathcal{L}$ across heads, empirically or theoretically?
- Discussion of what happens when Assumption 3.4 is violated (the acknowledged 1% of heads where $\sigma \leq 0.5$) — does the bound become vacuous or does the algorithm gracefully degrade?
- Brief argument or experiment showing the bound's ranking of entries is preserved under observation-window averaging (addressing Major weakness 1).
- Confidence intervals or variance measures across the 100 Ruler samples per task.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Demanding confidence intervals/variance"** — moved to nice-to-have. Single-run evaluation is standard in this field for large-scale benchmarks; the 100-sample Ruler evaluation already provides reasonable statistical stability.
- **"The two-stage structure is vacuous as implemented"** — the reviewer framed this as a potential structural flaw, but upon verification, the text and Assumption 3.4 clearly indicate stage 1 selects by attention weight while stage 2 selects by combined score. The issue is a notational ambiguity in the pseudocode, not a fundamental algorithmic problem. Retained as a clarity/reproducibility concern (Major #2) but not a structural flaw.
- **"The claim that the algorithm reduces compression loss by more than half is misleading"** — verified the claim is technically correct on average across all model-method-benchmark combinations. Retained as a minor framing concern rather than a factual error.

## Novel Insights
The core insight that KV cache selection should incorporate projected value norms ($VW^O$) alongside attention weights, formally derived from perturbation analysis, is genuinely novel in the cache eviction literature. Prior methods universally relied on attention weights alone. The mechanistic validation showing perturbation reduction accumulating across layers (Figure 5) provides a new diagnostic lens for evaluating cache eviction methods. The observation that the two-stage approach is necessary for some architectures (Mistral) but not others (Llama) is an interesting empirical finding that suggests architectural differences in attention weight distribution matter for cache selection strategies.

## Suggestions
1. **Clarify Algorithm 1 pseudocode** to unambiguously show that stage 1 selects by attention weight $A_i$ and stage 2 by combined score $\mathcal{A}_i$. This is a simple fix with high impact on reproducibility.
2. **Add a paragraph discussing the theory-practice gap** — why the bound still approximately guides selection when attention scores are averaged/pooled rather than single-token softmax. Even an informal argument would strengthen the paper.
3. **Add the single-stage ablation** (select by $A_i \cdot \|V_{i,:}\|_1$ without two-stage) to disambiguate contribution sources — this is trivial to implement and would sharpen claims.
4. **Fix the $\alpha=0.25$ vs $\alpha=0.5$ inconsistency** in Algorithm 1.
5. **Acknowledge code domain regressions** explicitly, even if the domain is considered insensitive overall.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Human Score | Round | Comparison |
|-------|------|-----------------|-------|------------|
| Survey of LLMs | 8QTpYC4smR.md | 1.00 | R1 | Not a research contribution; irrelevant comparison |
| NEMESIS Jailbreaking | 5kMwiMnUip.md | 1.40 | R1 | Far weaker; no formal framework |
| Cross-Lingual Humanoid | gwZ90hFSL2.md | 1.00 | R1 | Not a research paper; irrelevant |
| All Pairs Minimax | bEgDEyy2Yk.md | 1.00 | R1 | Not a research paper; irrelevant |
| IntelLLM (KV cache) | 4QWPCTLq20.md | 3.00 | R1 | Same domain, far weaker: no real theorems, weak baselines, limited evaluation. Paper under review is substantially better. |
| MixAttention | 2DD4AXOAZ8.md | 2.00 | R1 | KV cache related, much weaker contribution |
| Cut Cross-Entropy | E4Fk3YuG56.md | 2.67 | R1 | Different domain (loss computation), not directly comparable |
| PrefixQuant | vw0NurJ7UX.md | 3.00 | R1 | Quantization focus, not directly comparable |
| LSH-E (KV cache) | 0ZcQhdyI3n.md | 3.83 | R1 | Same domain, much weaker: limited novelty, weak baselines. Paper under review clearly better. |
| Running Huge Context | pG820nmDvy.md | 4.67 | R1 | KV cache, weaker theoretical grounding and evaluation. Paper under review is better. |
| CAKE (KV cache) | EQgEMAD4kv.md | 3.80 | R1 | Same domain, weaker evaluation. Paper under review has stronger theory and broader experiments. |
| KV Prediction | QlvL6eEOC6.md | 4.50 | R1 | Different approach (auxiliary model), not directly comparable |
| **This paper (earlier version)** | lRTDMGYCpy.md | **5.75** | R1 | **Same paper, earlier version with only LongBench (16 datasets), 2 models, no Ruler/SCBench/perturbation analysis. Current version dramatically improved.** |
| D2O (KV cache) | HzBfoUdjHt.md | 5.80 | R1 | Same domain, accepted. Empirical contribution without formal theory; comparable experimental scope. Paper under review has stronger theoretical motivation. |
| Locret (KV cache) | CkCFoN3j4s.md | 5.80 | R1 | Same domain, introduces trained retaining heads. Different approach, comparable quality level. |
| Cascading KV Cache | dSneEp59yX.md | 6.00 | R1 | Same domain, accepted. Training-free approach. Paper under review has stronger formal grounding. |
| FlexPrefill | OfjIlbelrT.md | 8.00 | R1 | Sparse attention (different focus), much stronger reception with two key innovations and flexible framework. Paper under review has narrower but genuine contribution. |
| Retrieval Head | EytBpUGB1Z.md | 8.00 | R1 | Mechanistic analysis of attention; different focus but demonstrates the bar for 8-scoring papers. |

**Round 1 Bracket: 5.5 – 7.0**

The paper under review is a substantially improved version of the earlier paper that scored 5.75 (Reject). The improvements — 3 models (including 32B), 29 datasets across two benchmarks, SCBench multi-turn evaluation, perturbation analysis (Figures 4–6), and efficiency evaluation — directly address the main weaknesses identified by human reviewers (insufficient experiments, limited models, missing analyses). It compares favorably with D2O (5.80, Accept) and Cascading KV Cache (6.00, Accept), both in the same domain with comparable but less theoretically grounded contributions. However, the theory-practice gap and focused nature of the contribution (a better selection criterion, not a new paradigm) prevent it from reaching the 7+ range.

**Final Assessment:** The paper makes a genuine, practically useful contribution: the insight that KV cache selection should incorporate projected value norms, backed by perturbation-theoretic derivation and validated across an impressively thorough experimental grid. The theory-practice gap is a real but not fatal weakness, and the algorithm clarity issue is addressable. The improvements over the earlier version are substantial and address most prior reviewer concerns. This paper sits at the borderline accept threshold — it contributes new, formally motivated knowledge to the cache eviction field with strong empirical backing, though the disconnect between theory and practice somewhat undermines the "formally grounded" narrative.

**Score: 6.0**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>