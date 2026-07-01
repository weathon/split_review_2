## Summary

INFOTok proposes an adaptive video tokenization framework that replaces fixed-rate compression with an information-theoretic, ELBO-guided approach. A router estimates each video's token budget from the ELBO, and a transformer-based adaptive compressor selects which tokens to keep based on per-token likelihood. The method wraps existing fixed-compression tokenizers (e.g., Cosmos), is trained end-to-end, and achieves substantially better reconstruction quality at the same bitrate as the leading adaptive baseline (ElasticTok) while requiring 11× fewer network evaluations at inference.

---

## Strengths

- **ELBO-based routing ablation (Table 2) is strong evidence for the core claim.** The paper compares its ELBO-guided router against an exhaustive-search "optimal" routing strategy across three compression levels. Performance is nearly identical (e.g., PSNR 29.86 vs. 29.92 at BPP₍₁₆₎=0.81, FVD 54 vs. 54). This directly validates that ELBO is an effective surrogate for optimal token allocation, supporting the paper's central thesis.

- **Consistent and sizable improvements over the leading adaptive baseline (ElasticTok).** Across TokenBench and DAVIS at multiple compression levels (BPP₍₁₆₎ = 0.81 and 0.56), INFOTok achieves 1–2 PSNR improvement and 40–60% FVD reduction at the same bitrate. The INFOTok-Flex variant is trained once and deployed at multiple compression rates without performance loss relative to rate-specific models.

- **Modular design that reuses existing tokenizer backbones.** The framework wraps a fixed-compression tokenizer (Cosmos) and reuses its encoder/decoder, adding only the router and adaptive compressor. This design makes the approach compatible with future improvements in backbone tokenizer architectures.

---

## Weaknesses

### Fatal
None.

### Major

1. **The per-token ELBO computation used by the adaptive compressor is underspecified, making a core component of the method irreproducible from the paper as written.** The ELBO is defined in Equation 3 as a single scalar per video sample. The adaptive compressor (Section 3.2, line 162) states that it preserves the top *Nₓ* tokens "according to their corresponding per-token log-likelihood, which is also approximated via the ELBO values," and that it computes a binary mask where the kept tokens are determined by these per-token ELBO values. However, no definition, derivation, or procedure is given for how the scalar ELBO is decomposed into per-token contributions — whether by attributing per-pixel reconstruction errors to each latent token's receptive field, computing per-token KL divergences, or some other proxy. The paper claims "it does not incur extra network evaluation since the log-likelihood term has been computed in the router" (line 163), but the router computes a single scalar, not per-token quantities. This is not a minor implementation detail; the compressor's entire selection mechanism — deciding *which* tokens to discard — depends on this computation. The method cannot be reproduced without this specification.

2. **The theoretical guarantees (Theorems 2.1–3.1) are established under idealized assumptions that are disconnected from the lossy regime where the method operates, and the paper's framing overstates what is actually proven.** Theorem 2.1 is a restatement of Shannon's Source Coding Theorem under the explicit idealization of lossless compression ("consider an idealized scenario where the tokenizer T can perfectly reconstruct any input video," line 58). Theorem 3.1's bound — *E[Nₓ] ≤ H_C(D) + β − E[−log p(x)]* — depends on the ELBO being a tight approximation of the true log-likelihood, which is acknowledged in passing (line 132: "the bound becomes tight when the approximate posterior approaches the true posterior") but never quantified or bounded for the actual models and datasets. The abstract claims to "rigorously prove that existing methods are suboptimal… and present a novel ELBO-based algorithm that approaches theoretical optimality." This overstates the gap between the idealized theorems and the lossy, approximate posterior setting in which the method is evaluated. The theorems provide valuable intuition and motivation, but they do not constitute a proof of optimality for realistic lossy tokenization. The paper should either (a) reframe the theoretical contribution as information-theoretic *motivation* with rigorous guarantees limited to the lossless limit, or (b) empirically bound the ELBO approximation gap for the actual models.

### Minor

3. **The mask overhead is described as "approximately 5% in token length" (line 164), which is inaccurate at the compression levels where adaptive tokenization is most valuable.** The binary mask costs *Nₘₐₓ* bits, corresponding to 1/16 in BPP₍₁₆₎ units regardless of compression level. At BPP₍₁₆₎ = 0.56, this is ~11.2% of total bitrate; at BPP₍₁₆₎ = 0.31, it is ~20.2%. The reported BPP numbers in the tables correctly account for this (line 199), so the results are honest, but the textual description is misleading. The overhead should be reported as a fraction of total bitrate at each operating point.

4. **Algorithm 1 shows *Nₓ ~ r(N|x)* (sampling from a stochastic router) while the actual router in Equation 4 is a delta distribution (deterministic).** This is a minor inconsistency between the general algorithm pseudocode and the specific implementation.

5. **The adaptive compressor's hidden dimension and total parameter count are not reported in the main text.** The paper specifies "eight-layer transformer with block-causal attention" (line 199), but without the hidden dimension, readers cannot assess the added computational cost relative to the backbone tokenizer.

6. **The router's sensitivity to the EMA-based estimate of 𝔼[ELBO(x)] is not discussed.** The expectation is maintained as an exponential moving average over training samples (line 199), but the paper does not address initialization or whether early in training — when this estimate may be far off — the router could assign extreme token lengths and destabilize training.

7. **The NFE-based inference efficiency metric (Figure 4g) captures the routing overhead but not the increased per-forward-pass cost of the adaptive compressor's 8 transformer layers.** The fixed backbone (Cosmos) does not include these layers. Reporting wall-clock latency or total FLOPs in addition to NFEs would give a more complete picture of the efficiency trade-off.

### Trivial

- None.

---

## Nice-to-Haves

- Compute the ELBO approximation gap (ELBO vs. log-likelihood) empirically on the actual models and datasets. This would quantify how close Theorem 3.1's idealized bound is to the observed token lengths and turn a rhetorical gap into an additional piece of evidence.
- Show the per-token ELBO decomposition with an explicit formula or algorithmic procedure.
- Report the mask overhead as a percentage of total bitrate at each operating point rather than as a percentage of token length.

---

## Removed Points

These points appeared in the input review but were removed for the reasons stated; treat them with caution:

- **Strength: "The problem is real and well-articulated"** — generic; lacks a specific anchor to the paper's content.
- **R2L baseline comparison note (Section 4.3)** — the reviewer observed that the R2L ablation (PSNR 27.43) is lower than ElasticTok's reported number (~28.26). This comparison conflates different backbones; the paper's Table 3 (Right) properly controls for architecture by comparing both mechanisms on the same Cosmos backbone. The ablation is fair and correctly scoped.
- **Rejection of theoretical contribution as disconnected** — while the theory-practice gap is real (kept as Major weakness #2), the reviewer's framing that the theorems "do not constitute a proof of optimality for realistic lossy tokenization" overstates the concern. The paper explicitly qualifies its theorems as idealized (line 58) and acknowledges the ELBO approximation gap (line 132). The retained weakness focuses on the *framing overreach* in the abstract and introduction, not on the validity of the theorems within their stated assumptions.
- **Speculation about EMA initialization causing training instability** — a reasonable implementation question but speculative; the paper provides the standard EMA mechanism and empirical results demonstrate stable training.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Specify the per-token ELBO decomposition with a formula or explicit algorithmic procedure.** This is the single most important fix — without it, the adaptive compressor mechanism is not reproducible. A simple description (e.g., attributing per-pixel reconstruction MSE to each latent token's receptive field and combining it with per-token KL divergence) would suffice.

2. **Adjust the framing of the theoretical contribution** to acknowledge that the rigorous guarantees (Theorems 2.1–3.1) apply in the lossless or near-optimal limit, while the practical method operates in a lossy regime with an approximate posterior. The empirical results stand on their own; the theory provides motivation, not a proof of practical optimality.

3. **Report the mask overhead honestly** as a fraction of total bitrate at each compression level used in the evaluation, and consider whether run-length encoding or other lightweight mask compression could reduce it.

---

## Score and Decision

**Score**: 7  
**Decision**: Accept

The paper makes a clear, well-motivated contribution with strong empirical evidence. The two major weaknesses — the underspecified per-token ELBO and the overstated theoretical guarantees — are both addressable without changing the method or its results. The per-token ELBO needs a concrete specification for reproducibility; the theoretical framing needs more precise language about the gap between idealized guarantees and lossy practice. Neither undermines the core empirical finding that INFOTok substantially outperforms the leading adaptive baseline (ElasticTok) in both quality and efficiency.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>