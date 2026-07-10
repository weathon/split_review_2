Now let me write the final consolidated review.

## Summary

This paper introduces InfoTok, an adaptive discrete video tokenizer that determines token length per-video based on information complexity, estimated via an ELBO-based router. The method retrofits adaptivity onto existing fixed-rate tokenizers (specifically Cosmos) using a transformer-based adaptive compressor. The core ideas are well-motivated by information theory, and the empirical results show clear improvements over the leading heuristic adaptive baseline (ElasticTok) at matched compression rates.

## Strengths

- **Well-designed optimal-search ablation (Table 2).** The exhaustive search over token lengths with constrained optimization provides a convincing upper bound. InfoTok-Flex matches this bound within a few hundredths of PSNR (e.g., 29.86 vs 29.92 at BPP 0.81 on TokenBench), which is the paper's strongest empirical evidence that the ELBO-based router works as intended.

- **Strong empirical results against the primary adaptive baseline (ElasticTok).** In Table 1 and Figure 4, InfoTok and InfoTok-Flex consistently outperform ElasticTok at matched average compression rates, with ~1–2 PSNR improvement and 40–60% FVD reduction at the same BPP. This is a substantial, non-incremental gain.

- **Principled conceptual framing.** The paper correctly identifies that fixed-rate tokenization is information-theoretically suboptimal for variable-complexity video data and connects this to Shannon's Source Coding Theorem, providing a conceptual foundation that prior heuristic methods (ElasticTok, ALIT) lack.

- **Practical inference efficiency.** The 1-pass ELBO computation compares favorably to ElasticTok's 11-pass binary search, a genuine practical benefit for deployment.

- **Composable framework.** Building on top of existing fixed-length tokenizers rather than requiring a from-scratch design extends the method's useful life and allows it to benefit from future advances in fixed-rate tokenizers.

## Weaknesses

### Fatal
None.

### Major

- **Introduction claims contradicted by the paper's own data (line 38).** The introduction states that InfoTok "can save approximately 50% tokens without loss of reconstruction quality compared to state-of-the-art fixed-length tokenizers." However, Table 1 shows that at ~44% savings (BPP=0.56 vs Cosmos-DV's BPP=1.00), PSNR drops from 30.01 to 29.27, LPIPS increases from 0.138 to 0.176, and FVD increases from 49 to 70 — all metrics degrade. The abstract's claim of "saving 20% tokens without influence on performance" is accurate and supported by the data (BPP=0.81 vs 1.00). The introduction should be corrected to match the abstract and the data.

- **A critical methodological claim about the router is asserted without empirical validation (line 156).** The paper states: "Empirically, we find that using the reconstruction error itself (without the KL term) to derive r_β(N_x|x) is sufficient, as the KL term is approximately proportional to the reconstruction error, and the ratio is similar." No evidence (scatter plot, correlation statistic, or any analysis) is provided. For a VAE, the KL divergence and reconstruction error have different functional forms and can vary independently across inputs. If the ratio varies across videos, the ranking by information content — and therefore token allocation — could change. This needs empirical substantiation. Note that the optimal-search ablation (Table 2) provides indirect validation that the router works well despite this gap, but the claim itself must be supported.

- **Logarithmic base inconsistency in Theorem 3.1.** Theorem 2.1 defines H_C(D) = 𝔼[−log_C p(x)] (base C, where C is codebook size). Theorem 3.1's bound states: 𝔼[N_x] ≤ H_C(D) + β − 𝔼[−log p(x)], where −log p(x) uses the natural logarithm (standard ML convention, used throughout the paper for ELBO and loss functions). Adding terms in different logarithmic bases is dimensionally inconsistent without an explicit conversion factor. The paper does not clarify the base convention for β and −log p(x), nor does it provide the conversion. The proof is in the appendix, but this issue is visible from the main text.

### Minor

- **The theoretical "near-optimality" claims are overstated relative to what is actually proven.** The optimality guarantees assume perfect reconstruction (lossless compression) and that the tokenizer achieves the global minimum of the loss. The paper acknowledges these are idealized assumptions (Section 2.2, Theorem 3.1's premise). However, the abstract claims the algorithm "approaches theoretical optimality" without these caveats, and Section 2.2 uses "near-optimal" (line 32) and "optimal up to the approximation error" (line 150) to describe what the method guarantees. The lossy regime where all experiments operate and the local minima reached by SGD are far from these assumptions. The theory is useful as motivation but does not provide the near-optimality guarantee that the framing suggests.

- **The router's discretization is unspecified (Equation 4).** The expression N_x = β · ELBO(x)/𝔼[ELBO(x)] produces a real number, but N_x must be an integer between 1 and N_max. How rounding, clipping, or quantization to an integer is performed is not explained. This affects both training stability and the fairness of comparisons at matched BPP.

### Trivial
None.

## Nice-to-Haves

- A scatter plot or correlation analysis validating the claimed proportionality between KL divergence and reconstruction error across the validation set.
- Reporting the distribution of token lengths (e.g., worst-case allocation) to help understand whether InfoTok ever allocates more tokens than the fixed-rate baseline to complex videos.
- A brief discussion of whether the fixed-length ELBO is a good proxy for the adaptive tokenizer's behavior, or whether the ELBO ranking is preserved after adaptive compression.
- Wall-clock latency comparison in the main text (currently deferred to Appendix D).

## Removed Points

- The criticism that the log_C(|D|) vs H_C(D) comparison in Section 2.2 is "apples to oranges" was removed. This is a standard information-theoretic argument (comparing fixed-length code length to entropy) and is used correctly in context.
- The "circularity" concern about the router was removed. The paper explicitly describes the sequential pipeline and it is by design, not a logical flaw. The broader question of whether the fixed-length ELBO is a good proxy is partially addressed by Table 2.
- Observations about the ViT backbone results being lower than Cosmos results were removed as they are observations, not weaknesses.
- Pure formatting and presentation nitpicks were removed as parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the factual overstatement in the introduction.** Replace "approximately 50% tokens without loss of reconstruction quality" with the accurate figure from the abstract (~20%).
2. **Add empirical validation of the KL≈reconstruction-error proportionality.** A scatter plot with per-video data across the validation set would either confirm or refute the claim and is a single figure's worth of work.
3. **Clarify the logarithmic base convention in Theorem 3.1.** Either state that all logarithms in the bound use the same base (and be explicit about which one), or provide the conversion factor between bases.
4. **Specify the discretization of N_x.** Explain how the real-valued router output is mapped to an integer between 1 and N_max.
5. **Calibrate the language around theoretical optimality.** Acknowledge explicitly that the theoretical guarantees assume conditions (perfect reconstruction, global optimality) that do not hold in practice, and that the experiments validate the method empirically in the lossy regime.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>