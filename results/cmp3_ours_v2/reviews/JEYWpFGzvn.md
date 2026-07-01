## Summary

InfoTok proposes an adaptive discrete video tokenizer that uses an ELBO-based router to dynamically allocate token counts per video based on information-theoretic complexity, and a transformer-based adaptive compressor to produce variable-length token sequences. The method builds on top of existing fixed-length tokenizers (Cosmos) and is grounded in Shannon's source coding theorem. Empirical results show substantial improvements over the adaptive baseline ElasticTok (2–3× FVD reduction at matched compression) and comparable reconstruction to fixed-length Cosmos with ~20% fewer tokens, while requiring only 1 additional decoder pass versus ElasticTok's 11 forward passes.

## Strengths

- **Principled theoretical framing grounded in information theory.** The paper anchors its method in Shannon's source coding theorem (Theorem 2.1), proves that uniform routers are suboptimal (Theorem 2.2), and provides a theoretical bound on its own method's expected token length (Theorem 3.1). This elevates the work above purely heuristic adaptive approaches like ElasticTok.

- **Large and consistent empirical margins over the primary baseline.** Table 1 shows InfoTok substantially outperforming ElasticTok at matched compression rates. At BPP₁₆=0.81 on TokenBench, InfoTok achieves PSNR 30.08 vs. ElasticTok's 28.26, and FVD 49 vs. 141 — a nearly 3× improvement. The advantage holds across both datasets and both compression levels tested.

- **Inference efficiency.** InfoTok requires one additional decoder pass to estimate the ELBO, versus ElasticTok's 11 forward passes (log₂(4096)−1) for binary search (Figure 4g). This is a genuine practical advantage.

- **Clean ablation study showing the router works near an oracle.** Table 2 compares the ELBO-based router to an exhaustive search over token lengths with dataset-level optimization. Results are extremely close (e.g., PSNR 29.86 vs. 29.92 at BPP₁₆=0.81 on TokenBench), demonstrating that the ELBO proxy effectively determines token lengths without brute-force search.

## Weaknesses

### Fatal

None.

### Major

- **The per-token ELBO used for adaptive compressor masking is not defined.** Section 3.2 states: "we preserve the top N_x tokens according to their corresponding per-token log-likelihood, which is also approximated via the ELBO values." However, the ELBO in eq. (3) is defined as a scalar over the entire video. The paper never explains how a per-token ELBO is obtained — whether it decomposes the reconstruction loss across spatial-temporal grid cells, derives from per-token KL contributions, or uses some other decomposition. Since the adaptive compressor's masking mechanism is a central component of the method, this underspecification is a significant reproducibility gap. A reader cannot implement the method without inferring this detail.

- **The router estimates complexity from the backbone alone, while actual reconstruction passes through a different pipeline.** The router computes ELBO(x) using only the fixed-length backbone encoder and decoder (Section 3.1: "we first encode x and decode back to x̃ without using the adaptive compressor"). However, the actual token sequence z is produced by passing h through the adaptive compressor M_ψ, quantizing, dequantizing, decompressing, and only then decoding. The paper does not justify why the backbone's ELBO should be a good predictor of the full pipeline's needed token count. Theorem 3.1's guarantee assumes the tokenizer minimizes L_recon (eq. 2), which is the loss of the full adaptive pipeline, while the router uses ELBO from the backbone alone. The strong empirical results suggest this works in practice, but the theoretical justification has a gap that is not addressed.

### Minor

- **The "Optimal" baseline in Table 2 is called a "strict upper bound" but InfoTok-Flex sometimes achieves better FVD.** At BPP₁₆=0.56 on TokenBench, InfoTok-Flex achieves FVD 71 while "Optimal" achieves FVD 74. Similar patterns appear at BPP₁₆=0.31 (FVD 155 vs. 165) and on DAVIS. The differences are small and likely within noise, but calling "Optimal" a "strict upper bound" is inaccurate when InfoTok-Flex outperforms it on some metrics. The claim in Table 2's caption should be softened.

- **The theoretical bound in Theorem 3.1 has an uncharacterized slack term.** The guarantee is 𝔼[N_x] ≤ H_C(D) + β − 𝔼[−log p(x)], where the slack term involves the gap between ELBO and true log-likelihood (the KL divergence between approximate and true posterior). The paper acknowledges this ("Provided by large-scale neural networks... ELBO values are believed to be close enough") but provides no evidence that this gap is small for video data. If the gap is large, the bound becomes vacuous. This does not invalidate the empirical results but weakens the claimed theoretical contribution.

- **The "20% tokens saved" in the Abstract and "50% tokens saved" in Section 4.2 refer to different comparisons without clear disambiguation.** The Abstract states "saving 20% tokens without influence on performance" while Section 4.2 states "save approximately 50% tokens without loss of reconstruction quality compared to state-of-the-art fixed-length tokenizers." These appear to refer to different compression regimes, but the text does not disambiguate, creating confusion about the headline claim.

### Trivial

- **Theorem 2.1 discusses lossless compression of an idealized "fully reconstruct" tokenizer, while the paper operates in the lossy setting.** The paper acknowledges this is "a simplified case," so this is not a flaw, but the framing somewhat overstates the rigor of the connection to real lossy tokenizers.

## Nice-to-Haves

- Define the per-token ELBO used in Section 3.2 for the adaptive compressor's masking mechanism — the single highest-leverage improvement for reproducibility.
- Measure the ELBO gap for a subset of videos on the datasets used, so readers can assess how tight the bound in Theorem 3.1 actually is.
- Include wall-clock latency measurements (not just NFE counts) to strengthen the efficiency claim.
- Disambiguate the 20% vs. 50% token savings claims by explicitly stating which baseline each refers to.

## Removed Points

- Missing baselines (FlexTok, ALIT): Removed per scope rule — these are primarily image-focused methods and the paper explicitly scopes itself to video.
- Dataset cropping making results not comparable with published papers: The paper acknowledges this tradeoff; it is a standard limitation of re-benchmarking.
- All formatting/typographical nitpicks: Removed per hard rules (parser artifacts, not author errors).
- Reproducibility concerns about undisclosed hyperparameters or trivial implementation details: Removed per hard rules.
- Generic concerns about "evaluation lacking rigor" without specific anchoring: Removed as unfocused and speculative.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Clarify how per-token ELBO is computed for the adaptive compressor's masking mechanism (Section 3.2). This is essential for reproducibility.
2. Either provide empirical evidence that the backbone ELBO gap is small for the video data used, or temper the theoretical claims in Theorem 3.1 accordingly.
3. Soften the "strict upper bound" claim for the Optimal baseline in Table 2, or explain why FVD sometimes favors InfoTok-Flex.
4. Disambiguate the 20% vs. 50% token savings claims between the Abstract and Section 4.2.

## Score and Decision

**Calibration.** Anchors retrieved across all rounds:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| ElasticTok (tFV5GrWOGm.md) | 6.00 | R1 (5.5–7.5) | Direct baseline; InfoTok achieves substantially better results (3× FVD improvement) with principled theory and fewer NFEs. |
| ALIT / "How many tokens" (mb2ryuZ3wz.md) | 5.75 | R1 (5.5–7.5) | Image-only adaptive tokenization; InfoTok has stronger results vs its own baseline and clearer theoretical motivation. |
| BSQ-ViT (yGnsH3gQ6U.md) | 5.75 | R1 (5.5–7.5) | Video tokenizer with different quantization scheme. |
| TokenFlow (lKK50q2MtV.md) | 7.00 | Narrow (6.5–7.5) | Accepted video paper in a different category; comparable solid contribution level. |
| RECOMBINER (VkWbxFrCC8.md) | 6.67 | Narrow (6.5–7.5) | Compression paper; InfoTok has stronger empirical validation. |

**Bracket:** Round 1 bracket was 6.5–7.5 (above ElasticTok at 6.0, below seminal 8.0+ papers). Narrowing against TokenFlow (7.00) confirmed this range. The paper's two major weaknesses (underspecified per-token ELBO, router-pipeline disconnect) prevent an 8, but the strong empirical validation, principled theory, and clear advantages over ElasticTok justify above-borderline status.

**Score: 7.0** — A solid contribution with genuine strengths and fixable weaknesses.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>