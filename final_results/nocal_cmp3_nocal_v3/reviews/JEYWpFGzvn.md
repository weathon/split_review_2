## Summary

This paper introduces InfoTok, a framework for adaptive discrete video tokenization that uses an ELBO-based router to dynamically determine per-video token sequence lengths, plus a transformer-based adaptive compressor. The core idea is to allocate tokens proportional to the informational complexity of each video, motivated by Shannon's source coding theorem. The method is built on top of existing fixed-length tokenizers (specifically Cosmos-DV) and is evaluated against fixed-length tokenizers and the adaptive baseline ElasticTok on reconstruction benchmarks (TokenBench, DAVIS). Empirical results show improvements over ElasticTok at matched compression rates (e.g., FVD 49 vs 141 at BPP₁₆=0.81) and comparable quality to Cosmos-DV with ~20% fewer tokens, with the practical benefit of requiring only 1 additional forward evaluation versus ElasticTok's 11.

## Strengths

1. **Principled, well-motivated framing of the adaptive tokenization problem.** The paper rigorously identifies why data-agnostic routers (e.g., uniform random masking in ElasticTok) are suboptimal (Theorem 2.2, with a concrete 4-data counterexample) and correctly connects adaptive tokenization to Shannon source coding. This goes beyond prior heuristic engineering approaches.

2. **ELBO-based router is a novel design with strong empirical support.** Rather than binary search over token lengths, InfoTok estimates informational complexity in a single forward pass. The ablation in Table 2 shows the ELBO-based router achieves performance nearly indistinguishable from a brute-force optimal search (e.g., PSNR 29.86 vs 29.92 at BPP₁₆=0.81 on TokenBench), providing direct evidence that the approach works in practice.

3. **Clear empirical advantage over the primary adaptive baseline (ElasticTok).** In Table 1, InfoTok outperforms ElasticTok at the same compression levels by substantial margins (FVD 49 vs 141, PSNR 30.08 vs 28.26 at BPP₁₆=0.81 on TokenBench). The rate-distortion curves in Figure 4 show InfoTok-Flex dominating ElasticTok across the full compression range.

4. **Practical inference efficiency.** InfoTok requires 1 additional forward evaluation versus ElasticTok's 11 (Figure 4g), eliminating the need for binary search over token lengths. This is a concrete practical benefit.

5. **Well-designed ablation studies.** Table 2 (ELBO vs optimal search), Table 3 Left (compressor strategies R2L/Jump/Ours), and Table 3 Right (uniform vs ELBO routing across two backbones) isolate the effect of each design choice and convincingly show that both the ELBO-based routing and the ELBO-based token selection contribute to the improvement.

## Weaknesses

### Major

- **Overclaimed theoretical guarantee from Theorem 3.1.** The theorem states $\mathbb{E}[N_{\mathbf{x}}] \leq H_C(\mathbb{D}) + \beta - \mathbb{E}[-\log p(\mathbf{x})]$. Since $\mathbb{E}[N_{\mathbf{x}}] = \beta$ by construction (Equation 4), substituting yields $H_C(\mathbb{D}) \geq \mathbb{E}[-\log p(\mathbf{x})]$, which is either mathematically inconsistent (if $\mathbb{E}[-\log p(\mathbf{x})]$ uses a different base than $H_C(\mathbb{D})$) or vacuous (if the same base is used, the bound reduces to $\beta \leq \beta$, i.e., equality). In either case, the bound does not substantiate the claim that "the compression rate of INFOTOK is optimal up to the approximation error" (line 150). This does **not** undermine the method's empirical effectiveness — Table 2 independently demonstrates near-optimal routing — but the theoretical framing is overstated and should be corrected or substantially softened. The paper would be more credible with an honest acknowledgment that the empirical evidence (Table 2) is the primary support for near-optimality.

### Minor

- **Inconsistency between the abstract's "20% tokens saved" and the introduction's "50% tokens saved" (Abstract line 9 vs. Introduction line 38).** The abstract and the experimental section (line 219) both support the 20% figure (Cosmos-DV at BPP₁₆=1.00 vs InfoTok at BPP₁₆=0.81 is a ~19% reduction). The introduction's 50% claim is not tied to any specific result and appears to be a numerical error. This is an editorial issue but undermines reader trust — the introduction and abstract should be consistent.

- **Comparison against fixed-length tokenizers conflates adaptivity with added model capacity.** InfoTok adds an 8-layer transformer-based compressor on top of Cosmos-DV's 3D CNN encoder-decoder. When claiming "20% tokens saved without influence on performance" vs. Cosmos-DV, the improvement could partially come from the added transformer layers rather than adaptivity alone. Table 3 (Right) partially controls for this by comparing Uniform vs. ELBO routing on the **same architecture** (showing ELBO wins by ~2 dB PSNR), which confirms that adaptivity itself helps. However, the paper should more clearly disentangle these two factors when presenting the fixed-length comparison. The cleanest comparison — against ElasticTok, which also adds components to a base tokenizer — is unambiguous and should be foregrounded.

### Trivial

None.

## Nice-to-Haves

- **Wall-clock timing data** in the main paper (if available in the appendix) would strengthen the efficiency claims beyond the NFE comparison.
- **Training cost comparison** — InfoTok computes ELBO during training (requiring an extra decoder pass), while ElasticTok's random masking imposes no such overhead. Acknowledging this asymmetry would be informative.
- **Statistical significance** (error bars / confidence intervals) would improve rigor, though the large margins over ElasticTok make this non-critical.

## Removed Points

- **"Statistical significance not reported"** — Generic criticism; single-run evaluation on large benchmarks is standard practice in this area.
- **"Wall-clock timing deferred to Appendix D"** — The parser strips appendices; the paper cannot be faulted for content that exists in the original submission.
- **"ELBO computation requires extra decoder pass"** — Already acknowledged in Section 6 (Limitations, line 272). The paper is transparent about this overhead.
- **"Theorem 2.2's practical relevance to ElasticTok"** — A framing observation, not a concrete weakness of the paper. The theorem targets uniform routers in general, not ElasticTok specifically.
- **"Missing downstream evaluation"** — Beyond scope (noted in Section 4, line 168 and Section 6), and acknowledged as a limitation.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a gap or connection that the authors themselves missed.

## Suggestions

1. **Fix the 20%/50% numerical inconsistency** between the abstract, introduction, and experimental section. All three should agree.
2. **Correct or reframe Theorem 3.1.** Either fix the log-base inconsistency and provide a meaningful bound, or remove the optimality claim and rely on Table 2's empirical evidence, which is strong enough on its own.
3. **Disentangle the fixed-length comparison.** When claiming savings over Cosmos-DV (Section 4.2), explicitly note that InfoTok adds transformer layers and that the controlled comparison in Table 3 (Right) isolates the effect of adaptivity.
4. **Clarify the log base** used in $\mathbb{E}[-\log p(\mathbf{x})]$ throughout the paper to ensure Theorem 3.1 and related equations are consistent.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>