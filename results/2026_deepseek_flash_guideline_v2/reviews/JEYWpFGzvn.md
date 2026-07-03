Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proposes INFOTok, an adaptive discrete video tokenizer that replaces the fixed or heuristic uniform-length token allocation used in prior work with an ELBO-based router and a transformer-based adaptive compressor. The key idea is to determine token length proportional to a video's estimated information content, grounded in information theory. The paper provides theoretical analysis showing that uniform routers can be arbitrarily suboptimal (Theorem 2.2), and empirically demonstrates substantial gains over the prior state-of-the-art adaptive method ElasticTok — ~1.5–2 dB PSNR improvement and ~3× FVD reduction at matched compression rates, while requiring 11× fewer additional network evaluations.

## Strengths

1. **Theoretical proof that uniform-length routers are arbitrarily suboptimal (Theorem 2.2, Section 2.3).** The paper proves that a uniform router (as used by ElasticTok and related methods) can yield an expected token length at least κ·H_C(D) for any κ>1, no matter how well the tokenizer is trained. This formalizes a genuine weakness in prior heuristic approaches and provides principled motivation for an information-aware router.

2. **Strong empirical gains over ElasticTok at matched compression rates (Table 1).** At BPP₁₆=0.81, INFOTok achieves PSNR 30.08 vs. ElasticTok's 28.26 on TokenBench and FVD 49 vs. 141. At BPP₁₆=0.56, the margins remain large (PSNR 29.27 vs. 27.34). These are not small margins — ~1.5–2 dB PSNR and ~3× FVD reduction — and they hold across both TokenBench and DAVIS datasets.

3. **Order-of-magnitude inference efficiency over ElasticTok (Figure 4g).** ElasticTok requires 11 additional network evaluations per video (binary search over 4096-token blocks), while INFOTok needs only 1 (one extra decoder pass for the ELBO). This is a concrete practical advantage that makes the adaptive approach far more usable.

4. **Ablation shows ELBO-based routing nearly matches an optimal oracle (Table 2).** The ELBO router closely matches an exhaustive search over 16 discrete compression rates per video — within 0.1 PSNR and ≤10 FVD across three compression levels on two datasets.

5. **Ablation confirms the compressor design matters and generalizes across architectures (Table 3).** The ELBO-based compressor (PSNR 29.30, FVD 71) substantially outperforms right-to-left masking (27.43, 137) and jump masking (28.07, 84). The adaptive mechanism also generalizes across Cosmos and ViT backbones, consistently beating ElasticTok's uniform approach.

## Weaknesses

### Fatal
None.

### Major
None. The paper's core contributions — the information-theoretic framing, the ELBO router design, and the empirical results — are solid and not undermined by any single fatal issue.

### Minor

1. **Underspecified discretization of the ELBO router (Section 3.1, Equation 4).** The router is defined as a delta distribution over the continuous value β·ELBO(x)/𝔼[ELBO(x)], but Nₓ must be a discrete integer between 1 and N_max. The paper never states how this continuous-to-integer conversion is performed (rounding? clamping? scaling?), nor how gradients flow through this discrete operation during training. While likely a simple rounding/clamping operation in practice, this missing detail affects reproducibility. The paper acknowledges Nₓ is "discrete and not directly optimizable" (line 124) but does not explain how the issue is circumvented.

2. **Lossless source coding theory applied to a lossy method (Theorems 2.1, 3.1).** The theoretical framing relies on Shannon's Source Coding Theorem, which assumes lossless compression. INFOTok is a lossy video tokenizer (minimizing MSE reconstruction error). The paper acknowledges this is an "idealized scenario" (line 58), but Theorem 3.1's bound relates expected token count to lossless entropy rather than to a rate-distortion function. The theory provides useful intuition and motivation, but the stated guarantees are looser than presented. Scoping the claims more carefully in the abstract and introduction would strengthen the paper.

3. **No error bars or multiple-seed variance reported (Tables 1–3).** None of the tables report standard deviations, confidence intervals, or results from multiple training seeds. Video tokenizer training involves stochastic elements (codebook initialization, data ordering). While the large margins (e.g., FVD 49 vs 141) suggest the qualitative conclusions are robust, the lack of variance estimates is a gap in experimental rigor.

4. **Model capacity confound in the main comparison (Table 1 vs Table 3).** INFOTok adds an 8-layer Transformer compressor/decompressor on top of Cosmos-DV, introducing substantial additional parameters. Table 3 (Right) partially addresses this by comparing the adaptive mechanism on shared architectures, but an explicit ablation — Cosmos-DV + Transformer layers + uniform masking vs. Cosmos-DV + Transformer layers + ELBO masking — is not provided. This makes it difficult to fully attribute the main headline gains to the router versus the added capacity.

5. **NFE comparison may understate ElasticTok's overhead for long videos (Figure 4g).** The paper reports ElasticTok's overhead as 11 NFEs (log₂(4096)−1), but notes that ElasticTok runs binary search "over each 4096-token block sequentially" (line 237). For long videos with multiple 4096-token blocks, the overhead could be 11 × (number of blocks). The paper should clarify whether Figure 4g accounts for this or assumes a single block.

6. **Slight overclaim in abstract regarding Theorem 2.2 scope.** The abstract (line 9) claims the paper "proves that existing data-agnostic training methods are suboptimal," but Theorem 2.2 specifically proves suboptimality for a uniform router under a loss-minimization assumption. The paper partially addresses this in Section 2.3 (line 120: "while this theorem is particular for the uniform router"), but the abstract overstates the scope.

### Trivial

1. The notation ℳ_ψ^{-1} for the decompressor is mildly misleading — it suggests the decompressor is the functional inverse of the compressor, which is not the case for learned neural networks.

2. Table 2 calls the 16-discrete-value search a "strict upper bound," which is too strong since the search has finite granularity.

## Nice-to-Haves

- A controlled experiment isolating the ELBO router from the added Transformer capacity (Cosmos-DV + Transformer layers + uniform masking vs. Cosmos-DV + Transformer layers + ELBO masking) would cleanly resolve the capacity confound.
- A discussion connecting the lossless theory to the lossy setting (e.g., via rate-distortion theory) would tighten the theoretical framing.

## Removed Points

These points were flagged during review but are removed from the main assessment:

- **Criticism about the ELBO estimation decoder sharing parameters with the reconstruction decoder:** The paper states both use the same encoder/decoder, and there is no evidence this causes training issues. Speculative.
- **Claim that the related work characterization is "reductive":** A matter of opinion, not a concrete weakness. The paper provides Theorem 2.2 as formal justification for its characterization.
- **Concern about missing appendix content (proofs, implementation details):** The appendix is present in the original submission but stripped during parsing. This is a parser artifact, not an author omission.
- **Several formatting/style nitpicks about capitalization, whitespace, and garbled symbols:** These are parser errors, not issues in the original submission.

## Novel Insights

None beyond the paper's own contributions. The reviews largely converge on the paper's own framing — the ELBO-based router is a principled improvement over heuristics, the empirical results are strong, and the main gaps are in presentation clarity (discretization mechanism, scoping of theoretical claims, experimental rigor with error bars).

## Suggestions

1. **Clarify the discretization mechanism** for Equation (4). Explain how the continuous value β·ELBO(x)/𝔼[ELBO(x)] is mapped to an integer Nₓ (rounding, clamping, or scaling), and how gradients flow through this operation during training (e.g., straight-through estimator, Gumbel-softmax, or a soft relaxation).

2. **Add error bars or multiple-seed results** to at least the main results (Tables 1 and 2), even if only for 2–3 seeds.

3. **Scope the theoretical claims more carefully** in the abstract and introduction: acknowledge that Theorems 2.1 and 3.1 apply to an idealized lossless setting, and that the method approximates this for the lossy case. This would make the paper stronger, not weaker.

4. **Add the controlled experiment** comparing uniform vs. ELBO masking on the Cosmos backbone with the 8 Transformer layers, to isolate the router's contribution from added capacity.

5. **Clarify whether Figure 4g assumes a single 4096-token block** or accounts for multiple blocks in longer videos.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>