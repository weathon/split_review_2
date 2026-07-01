## Summary

This paper introduces InfoTok, an adaptive discrete video tokenization framework that uses an ELBO-based router to dynamically allocate token budgets per video according to information complexity, combined with a transformer-based adaptive compressor that drops low-information tokens. The paper provides theoretical grounding via Shannon source coding (showing fixed-rate and uniform-adaptive routers are suboptimal) and demonstrates strong empirical results: matching Cosmos-DV's reconstruction quality with ~20% fewer tokens, and substantially outperforming the prior adaptive baseline ElasticTok at matched compression levels (FVD reduced by 40–60%, LPIPS by 25–40%).

## Strengths

1. **Principled theoretical framing (Sections 2.2–3.1).** The paper correctly identifies that fixed-rate and data-agnostic adaptive tokenization are suboptimal from an information-theoretic standpoint. Connecting the ELBO to optimal token length via Theorem 3.1 is a genuine step beyond prior heuristic work (ElasticTok, ALIT), and Theorem 2.2 formalizes why a uniform router can be arbitrarily suboptimal.

2. **Clear and substantial empirical advantage over the main adaptive baseline (Table 1, Figure 4).** InfoTok consistently outperforms ElasticTok at matched BPP₁₆ = 0.81 and 0.56 on both TokenBench and DAVIS across PSNR, SSIM, LPIPS, and FVD. The margins are large: at BPP₁₆ = 0.81 on TokenBench, InfoTok achieves FVD 49 vs ElasticTok's 141; LPIPS 0.145 vs 0.244. The improvement is systematic across compression levels.

3. **Inference efficiency.** ElasticTok requires ~11 additional forward evaluations (binary search over token lengths), while InfoTok needs only 1 additional decoder pass. This is a practically meaningful improvement clearly documented in Figure 4g.

4. **Oracle comparison validates the router (Table 2).** InfoTok's ELBO-based router achieves performance within ~0.1 dB PSNR of an exhaustive search-based optimal strategy, providing strong empirical evidence that the ELBO approximation is practically effective even if the theoretical gap is unmeasured.

## Weaknesses

### Fatal

None.

### Major

None that threaten the core claims. See Minor for substantive but addressable concerns.

### Minor

1. **The "near-optimality" guarantee of Theorem 3.1 depends on an unmeasured ELBO approximation gap.** Theorem 3.1 shows that E[N_x] ≤ H_C(D) + (β − E[−log p(x)]). The additive term depends on how close the ELBO is to the true log-likelihood. The paper asserts this gap is small because "large-scale neural networks (fixed-length tokenizers) [have] ELBO values close enough to the log-likelihoods" (line 154), but provides no empirical measurement of this gap for the Cosmos tokenizer actually used. This matters because the router computes ELBO using the fixed-length tokenizer's reconstruction, not the variable-length model's. However, the paper partially compensates with a different form of validation: Table 2 shows the ELBO-based router performs near-identically to an optimal search-based oracle (e.g., PSNR 29.86 vs 29.92 at BPP₁₆ = 0.81), which supports practical efficacy even if it does not directly measure the theoretical gap. The paper should either quantify the ELBO gap or moderate the theoretical optimality claims accordingly.

2. **The NFEs comparison (Figure 4g) counts evaluations without accounting for differing per-evaluation cost.** InfoTok's single NFE involves a decoder pass plus the 8-layer transformer adaptive compressor; each of ElasticTok's 11 NFEs is presumably a simpler encode→mask→decode pass. The paper references wall-clock timing data in Appendix D, which likely addresses this, but in the main text the "11× fewer NFEs" framing could mislead readers about the actual speedup magnitude. The conclusion of superior efficiency is almost certainly correct (1 evaluation vs 11), but the main text should be more explicit that NFEs are not equal-cost units.

3. **Per-token ELBO computation is not explained.** Equation (3) defines ELBO as a video-level scalar. Section 3.2 describes selecting tokens "according to their corresponding per-token log-likelihood, which is also approximated via the ELBO values" (line 162), but never specifies how video-level ELBO is decomposed into per-token scores. If per-token ELBO is simply the per-pixel reconstruction error aggregated over each token's spatial-temporal footprint, the paper should state this explicitly, as it is a design choice with potential alternatives.

4. **InfoTok-Flex β sampling strategy is underspecified.** The paper states that for the flexible variant, β is chosen from different values and input to the adaptive compressor during training (line 156), and lists ℬ = {0.25N_max, 0.5N_max, 0.75N_max, N_max} (line 199). However, it does not specify how β is sampled from this set during training (uniform over ℬ? per-sample? per-batch? scheduled?), which affects reproducibility.

5. **Conversion from continuous router output to integer token count is unclear.** Equation (4) defines r_β(N_x|x) = δ(β · ELBO(x)/E[ELBO(x)]), producing a real-valued result. Since N_x must be an integer (used to "preserve the top N_x tokens" and to index token sequences), the paper should explain how rounding, flooring, or clipping is applied.

### Trivial

6. **The abstract's claim "saving 20% tokens without influence on performance" slightly overstates the case.** In Table 1, Cosmos-DV (BPP₁₆=1.00) achieves SSIM 0.885, LPIPS 0.138 versus InfoTok (BPP₁₆=0.81) at SSIM 0.881, LPIPS 0.145. The differences are very small (~0.5% relative on SSIM), so the practical conclusion holds, but "negligible influence" would be more precise.

## Nice-to-Haves

- Measure the ELBO gap (e.g., via importance sampling or an ensemble of tokenizers) for the Cosmos tokenizer on a held-out set, to directly validate the mechanism behind Theorem 3.1.
- Report wall-clock inference times (ideally in the main text, not only the appendix) alongside NFEs.
- Clarify the per-token ELBO derivation and the N_x discretization in the main text for reproducibility.

## Removed Points

These points are from the input review but were removed for the reasons stated:

- **"Comparison between InfoTok and Cosmos is less clean"** — Removed: The critic claimed the abstract creates an impression that improvement comes purely from smarter allocation rather than additional parameters. The paper is transparent about adding an 8-layer transformer compressor (lines 164–165). InfoTok reuses Cosmos's encoder/decoder; the added compressor is the contribution being evaluated. This is a standard methodological pattern, not a weakness.
- **"Binary mask overhead under-discussed"** — Removed: The paper explicitly accounts for the 5% mask overhead in BPP computation (line 199: "β can be computed as N_max · (BPP_16 − 1/16), where 1/16 is the cost of binary mask"). The concern is addressed in the paper.
- **"Theorem 2.1 bound is too loose to be informative"** — Removed: This is a standard theoretical motivation restating Shannon's theorem. The bound's looseness is inherent to the setting and serves its qualitative purpose. Not a weakness.
- **"Theorem 2.2 is narrow"** — Removed: The critic acknowledged the language is "appropriately qualified." An existence proof showing uniform routing can be arbitrarily bad is a valid theoretical contribution even if it doesn't claim universal failure.
- Various section-by-section observations that were descriptive rather than identifying weaknesses.

## Novel Insights

None beyond the paper's own contributions. The review process surfaces the need for direct empirical validation of the ELBO approximation gap to fully substantiate the theoretical claims, but this is a standard "measure what you assert" observation rather than a novel insight about the paper or problem.

## Suggestions

1. Add a brief paragraph or table reporting the ELBO gap (ELBO vs. estimated log-likelihood) for the Cosmos tokenizer on a representative subset of TokenBench. Alternatively, soften the theoretical optimality claims and lean more heavily on the empirical oracle comparison (Table 2).
2. Clarify in the main text: (a) how the continuous output of eq. (4) is discretized to an integer N_x, (b) how per-token ELBO values are derived from the video-level ELBO, and (c) how β is sampled during InfoTok-Flex training.
3. Include wall-clock latency in the main text alongside NFEs, or at minimum add a sentence bounding the per-NFE cost difference between methods.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>