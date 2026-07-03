I've verified the contradiction directly from the paper text and table. Now I'll produce the final review.

## Final Review

## Summary

This paper proposes ASPD (Adaptive Serial-Parallel Decoding), a framework for training LLMs to interleave serial and parallel decoding within a single generation sequence. It introduces (1) a non-invasive data transformation pipeline that uses a larger LLM to identify and rewrite parallelizable segments in training responses, and (2) an internal parallelization module with branch-invisible attention masks and shared position IDs that enable seamless switching between serial and parallel modes without KV-cache loss. Evaluated on Vicuna-7B and Qwen2.5-7B/32B across general tasks, RAG, and math reasoning, ASPD achieves 1.3–1.82× average speedup on general tasks while maintaining output quality within 1% of the baseline.

## Strengths

1. **Novel shared-position-ID mechanism solves a known failure mode in prior work.** ASPD assigns identical position IDs to tokens at the same timestamp across parallel branches, then assigns sequential position IDs upon merging (Eq. 4, "Same-Seq" strategy). The ablation (Table 4) shows this achieves Score 7.64/TPS 104.21, substantially beating PASTA's "Predict" strategy (Score 6.75/TPS 72.15), which suffers from inconsistencies between predicted and actual branch lengths. This directly addresses the position-encoding mismatch problem identified in PASTA.

2. **Best speed-quality trade-off among compared methods on Vicuna Bench.** On Vicuna Bench (Table 1, Figure 4b), V-ASPD achieves 1.82× speedup with quality 7.74 — matching the sequential fine-tuned model (7.70) while being faster. SoT reaches 1.89× but at severely degraded quality (5.93 vs baseline 6.21). V-APAR* manages only 1.35× with quality 7.62. ASPD is the only method that keeps quality at or above the original model while delivering >1.8× acceleration.

3. **Non-invasive pipeline with automated verification demonstrably improves over rule-based alternatives.** The four-stage pipeline (Section 3.1) using LLM-based parallel rewriting, independence verification, integrity/answer verification, and preference-based selection yields substantially better results than rule-based APAR* (Score 5.81, 59.25 TPS) and PASTA† (Score 4.98, 106.83 TPS) in Table 4. The large quality gaps isolate the pipeline's contribution.

4. **Robust cross-domain generalization on RAG, where prompt-based competitors degrade.** On the out-of-domain RAG Bench (Figure 4c), ASPD maintains 1.46× speedup while SoT falls to 1.06× (due to redundant long-context prefilling) and V-APAR* reaches only 1.22×. This demonstrates that ASPD's architectural integration is more portable to new domains than prompt-engineering approaches.

5. **Seamless serial–parallel switching without batching, threading, or KV-cache re-prefilling.** The Hybrid Decoding Engine (Section 3.3) uses branch-invisible attention masks and shared position IDs within a single sequence, so mode transitions incur no re-initialization or re-prefill overhead. The paper contrasts this with SoT (re-prefills) and APAR (discards parallel-branch KV caches), establishing a cleaner architectural design.

## Weaknesses

### Fatal

None.

### Major

1. **Internal contradiction in the mask visibility ablation (Section 4.4.2 vs Table 4).** The paper states: *"Our empirical evaluation shows that Shared masks consistently outperform Indep masks across both Seq and Max position id configurations."* However, Table 4 shows the opposite: Seq+Indep scores 7.64 vs Seq+Shared scores 4.64; Max+Indep scores 6.78 vs Max+Shared scores 3.70. Indep clearly outperforms Shared in both configurations. Notably, the *conclusion* drawn — *"strongly validates our design decision to maintain strict branch isolation"* — IS consistent with Indep (Independent = strict isolation) being better. This indicates a simple label swap in one sentence (Shared ↔ Indep), but it is a concrete error that undermines reader trust in the ablation analysis. The authors must fix this in a revision.

2. **Framing conflates fine-tuning benefits with parallelization benefits.** In Table 1, V-ASPD achieves quality scores (MT Bench 5.59, Vicuna Bench 7.74) essentially identical to V-Seq (5.59, 7.70). The paper frames its results as *"14.55% and 24.78% improvement on the MT Bench"* and *"26.89% and 30.52% enhancement on the Vicuna Bench"* (lines 187) compared to V-APAR and SoT. While technically accurate (V-APAR and SoT are baselines), this framing gives the impression that the parallel architecture drives quality gains. In reality, the sequential fine-tuned model already achieves these levels; the parallelization's genuine contribution is enabling speed without quality loss. The paper should clearly separate the effect of fine-tuning from the effect of parallelization.

### Minor

3. **Modest speedups on math reasoning are under-emphasized in the framing.** The headline "up to 3.10× speedup (1.82× on average)" comes from Vicuna Bench. On math benchmarks (Table 3), overall TPS speedups against Seq are only 1.04–1.17× — essentially negligible on AIME2024 (1.04×) and AIME2025 (1.08×). The paper attributes this to low degrees of parallelism (8.60–8.84% DP on AIME tasks). This is a real limitation of the approach for tightly chained reasoning tasks. The data is presented transparently in the table, but the abstract and introduction could better contextualize the speedup range by task type.

4. **Data pipeline cost is not quantified.** The non-invasive pipeline (Section 3.1) invokes Qwen3-235B-A22B (a 235B-parameter model) for up to four operations per training sample: parallel rewriting (N=3), independence verification, integrity verification, and answer verification. No estimate is given of LLM calls per retained training sample, the fraction of samples that survive all stages, or the total compute cost. While this is a one-time preprocessing cost, transparency about the expense would strengthen the efficiency narrative.

5. **Practical limitation: full fine-tuning required.** The method adds 6 special tokens to the vocabulary and requires fine-tuning the full model. This means ASPD cannot be applied to black-box API models or users without fine-tuning access — unlike prompt-based methods (SoT) or draft-model methods (speculative decoding). This limitation is not acknowledged in the paper.

### Trivial

6. **Imprecise characterization of speculative decoding.** The paper states speculative decoding techniques are *"inherently sequential at the token level due to the autoregressive constraint"* (line 67). This somewhat understates that speculative decoding does generate multiple tokens in parallel via a draft model. The distinction is nuanced (verification is sequential) but the phrasing could be more precise.

## Nice-to-Haves

- A cost-benefit analysis of the data pipeline (estimated LLM calls per retained training sample, fraction of data that survives verification).
- Variance or confidence intervals for quality scores, given that LLM-as-judge evaluations are known to be noisy.
- Memory usage measurements — the paper criticizes SoT for "intensive memory usage" (line 187) but provides no memory numbers for either method, and ASPD's own memory footprint during parallel stages (multiple KV caches simultaneously) could be significant.
- A brief discussion of how ASPD compares to multi-token prediction approaches (e.g., Medusa/Cai et al. 2023) in terms of achievable speedup and applicability.

## Removed Points

- **"Medusa is not cited":** The paper cites Cai et al. (2023) which IS the Medusa paper. This criticism is factually wrong.
- **"No code link in abstract":** Standard for anonymous submissions; the reproducibility statement explicitly describes the code repository structure.
- **"Table 1 formatting is confusing":** Parser artifact; the table structure is standard.
- **"Proportion of Parallel Data at 44% is suspicious":** May be a parser artifact from the figure; cannot be verified from the text alone. Not actionable.
- **"Missing comparison to Multiverse":** The paper mentions Multiverse as concurrent work and describes the architectural difference. A quantitative comparison would be nice but the methods target different settings (single-sequence vs framework-based).
- **"ASPD's quality improvements are fully due to fine-tuning":** Merged into Weakness #2 (framing issue).
- Generic or speculative concerns about "confounders" and "proxy metrics" with no concrete anchor in the paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the label swap in Section 4.4.2.** Either change "Shared consistently outperform Indep" to "Indep consistently outperform Shared" (matching the table and the conclusion about strict branch isolation), or swap the table labels if the prose is correct.
2. **Reframe the contribution** as "parallel decoding without quality degradation" rather than implying quality improvement through parallelization. The sequential fine-tuned baseline already matches ASPD's quality; the value is in matching that quality while being faster.
3. **Add a brief cost analysis** for the data pipeline (even a rough estimate of calls per retained sample and survival rate).
4. **Explicitly acknowledge the fine-tuning requirement** as a limitation and discuss scenarios where ASPD is most applicable vs where prompt-based or draft-model methods would be preferable.
5. **In the abstract and introduction**, contextualize the speedup range by noting variation across task types (e.g., 1.3–1.82× on general generation, 1.04–1.17× on tightly chained math reasoning).

## Score and Decision

The paper makes a genuine technical contribution — the shared-position-ID mechanism combined with branch-invisible attention masks within a single sequence is novel and the empirical results demonstrate a favorable speed-quality trade-off. The evaluation is comprehensive across multiple domains, model sizes, and competing methods. However, the paper has a concrete internal contradiction (the mask visibility claim in Section 4.4.2 directly contradicts Table 4) and a framing issue that conflates fine-tuning gains with parallelization gains. The math reasoning speedups are modest (1.04–1.17×) and the data pipeline cost is unquantified. These are fixable issues — the core technical contribution is sound — but they prevent the paper from being a clear accept in its current form. I rate this as borderline accept to accept, closer to accept after revisions.

Since the calibration search tool was unavailable (backend file system error), I calibrated based on my knowledge of the ICLR reviewing standards and the paper's own merits relative to work in this area. The paper sits between "borderline accept" (6) and "accept" (8): it has a real contribution and solid experiments, but the error and framing issues are non-trivial.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>