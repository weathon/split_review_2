All strengths score 1.00 (strongly positive), the theoretical overclaim weakness scores 0.07 (truly damaging), and the remaining weaknesses are near-neutral (0.49–0.70). The empirical core is strong; the theoretical framing is the only issue that carries weight. Score **8 (Accept)**.

---

## Summary

INFOToK introduces an adaptive video tokenization framework that replaces fixed-rate compression with an ELBO-based router, which estimates per-video information complexity and allocates token budgets accordingly. Built on top of a fixed-rate tokenizer (Cosmos-DV) with added transformer layers for adaptive compression/decompression, the method demonstrates substantially better reconstruction quality than the existing adaptive baseline (ElasticTok) at matched compression rates while requiring far fewer network evaluations.

## Strengths

- **Principled motivation grounded in information theory.** The paper correctly identifies that fixed-rate video tokenization is suboptimal under Shannon's Source Coding Theorem (Section 2.2), providing a cleaner foundation than prior heuristic approaches like ElasticTok.

- **Strong empirical gains over the primary baseline (ElasticTok).** At matched compression rates in Table 1, INFOToK reduces FVD by 40–60%, LPIPS by 25–40%, and improves PSNR by 1.0–2.0 dB. At BPP₁₆=0.81 on TokenBench, INFOToK achieves PSNR 30.08 vs ElasticTok's 28.26.

- **Inference efficiency advantage.** INFOToK requires only 1 additional decoder pass to determine token length, versus ElasticTok's 11 NFEs for binary search (Figure 4g). This is a clear practical advantage.

- **Well-designed ablation study.** The comparison to an exhaustive-search oracle (Table 2, "Optimal") shows that INFOToK-Flex's ELBO-based allocation is empirically close to the best achievable over the evaluated BPP set (within ~0.1 dB PSNR), supporting the router's effectiveness.

- **Framework generality.** Building on top of Cosmos-DV and demonstrating effectiveness across both CNN and ViT architectures (Table 3, right) shows the approach is not tied to a specific backbone.

## Weaknesses

### Fatal
None.

### Major

- **The theoretical "near-optimality" claim (Theorem 3.1, line 150) is overstated relative to what the theorem actually guarantees.** The bound is E[Nₓ] ≤ H_C(D) + β − E[−log p(x)]. Since β ≥ E[−log p(x)] by construction (line 154), the slack term β − E[−log p(x)] is non-negative and grows with the user-chosen parameter β (which controls the average compression rate). This means the bound does **not** establish that the method approaches optimality — it only says expected token length is at most the Shannon limit plus a slack term that can be arbitrarily large. Additionally, there is a unit inconsistency: H_C(D) uses base-C logarithms while E[−log p(x)] (derived from the ELBO, which in ML convention uses natural log) appears to use a different base, making the addition/subtraction dimensionally ambiguous without a specified conversion factor. The paper's core empirical contribution does **not** depend on this optimality claim, but the theoretical framing overreaches. **This is fixable by reframing the theorem as a consistency bound rather than an optimality guarantee.**

### Minor

- **The per-token ELBO computation for the adaptive compressor is underspecified (line 162).** ELBO(x) as defined in Equation (3) is a global scalar per video. The paper states that the compressor computes a mask based on tokens with the "lowest ELBO values" and mentions per-token log-likelihood approximated via ELBO, but does not explain how a per-token value is obtained from the global objective. While one can infer that per-pixel reconstruction error is aggregated over spatial-temporal regions corresponding to each latent position in the Cosmos tokenizer's grid, this is not stated explicitly. This needs to be specified for reproducibility.

- **The adaptive baseline comparison is limited to ElasticTok.** The paper acknowledges that other adaptive tokenizers (ALIT, FlexTok, One-D-Piece) focus on images, but since the paper's framework is described as modality-agnostic, comparisons with image methods adapted to video would strengthen the evidence. This does not undermine the reported results but narrows the scope of the "state-of-the-art" claim.

### Trivial

- **Equation (4) defines r_β(Nₓ|x) = δ(β · ELBO(x) / E[ELBO(x)]) where δ(·) denotes a delta distribution.** The paper does not specify how this continuous-valued expression is converted to a discrete integer token count Nₓ, which is necessary for the method to be fully specified.

- **The "Optimal" oracle in Table 2 is optimal only over the evaluated discrete set {1/16, 6/16, ..., 1}, not over all possible compression rates.** The ablation remains informative, but the naming slightly inflates the baseline.

## Nice-to-Haves

- Report wall-clock latency (ms per video on a standard GPU) in addition to the NFE ratio in Figure 4g. The paper points to Appendix D for this, but including it in the main text would make the efficiency claim more concrete.
- Provide a brief empirical demonstration that the KL term is indeed approximately proportional to the reconstruction error in the Cosmos tokenizer's loss landscape, to support the claim in line 156.

## Removed Points

These points from the input reviews were removed after cross-verification against the paper:

- **"20% tokens saved" claim is unfair due to added parameters**: Removed because the paper compares at equal BPP (compression rate), which is standard and fair. The extra transformer layers are the method's contribution.
- **Theorem 2.2 intuition gap**: Removed because the proof is in the appendix (stripped by the parser); the critic could not verify it and speculated.
- **KL term approximation lacking support**: Removed because it speculates about evidence that may be in the appendix.
- **Cropping potentially skewing comparisons**: Removed because the paper transparently acknowledges this limitation.
- **VAE vs VQ-VAE imprecision in Section 2.1**: Removed as a presentation nitpick that does not affect any claim or result.
- **Paper understates overhead**: Removed as a subjective opinion; one extra decoder pass is indeed modest vs ElasticTok's 11 NFEs.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe Theorem 3.1 honestly**: present it as a consistency bound (expected token length ≤ Shannon limit + slack determined by the chosen budget β) rather than a near-optimality guarantee. Resolve the unit consistency between H_C(D) and E[−log p(x)] by explicitly adopting a consistent logarithm base throughout.
2. **Specify the per-token ELBO computation**: describe exactly how per-token values are derived (e.g., by aggregating per-pixel MSE over the spatiotemporal receptive field of each latent position in the Cosmos tokenizer grid).
3. **Clarify in Equation (4)** how the continuous ratio β·ELBO(x)/E[ELBO(x)] is converted to a discrete integer Nₓ (e.g., rounding).

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>