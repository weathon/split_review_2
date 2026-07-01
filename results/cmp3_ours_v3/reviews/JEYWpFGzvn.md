Now let me write the final review.

## Summary of Calibration

**Round 1 bracket:** 5.5–6.5

**Anchor papers used:**

| Anchor | Path | Score | Round | Comparison |
|--------|------|-------|-------|------------|
| ElasticTok | tFV5GrWOGm.md | 6.00 | R1, Narrow | Direct baseline; INFOTok shows stronger empirical results and principled motivation but has clarity gaps ElasticTok did not |
| BSQ-ViT | yGnsH3gQ6U.md | 5.75 | R1, Narrow | Solid tokenizer paper; similar profile, slightly less relevant (different focus) |
| "How many tokens is an image worth?" | mb2ryuZ3wz.md | 5.75 | R1, Narrow | Adaptive tokenization; similar quality level, more experiments in some dimensions |
| EVEREST | UM6QLuOVNi.md | 5.33 | R1 | Rejected; concerns about novelty compare unfavorably to INFOTok's stronger theoretical grounding |
| Discrete Tokenization Role | WNLAkjUm19.md | 7.00 | Narrow | Higher score due to cleaner presentation and more polished experiments; INFOTok has comparable theoretical depth but clarity issues hold it back |

**Final score rationale:** INFOTok's empirical results are stronger than ElasticTok (6.0), and its information-theoretic motivation is more principled. However, the underspecified per-token ELBO computation and the overclaimed Theorem 3.1 prevent it from reaching the 7.0 level. Score of **6.0** — a solid borderline accept with fixable weaknesses.

---

## Summary
INFOTok proposes an adaptive discrete video tokenizer that uses an ELBO-based router to dynamically assign token lengths based on video information complexity, and a transformer-based adaptive compressor to discard low-information tokens. The framework is theoretically motivated by the Shannon Source Coding Theorem, and experiments show improved compression–quality tradeoffs compared to ElasticTok and fixed-rate baselines.

## Strengths
- **Principled information-theoretic motivation.** The paper connects tokenization to Shannon's Source Coding Theorem (Theorem 2.1) and provides a formal framework showing why fixed-length tokenizers are suboptimal (Section 2.2). Theorem 2.2 rigorously proves that data-agnostic uniform routers can be arbitrarily suboptimal.

- **Clear empirical advantage over ElasticTok.** In Table 1, INFOTok at BPP=0.81 outperforms ElasticTok at BPP=0.81 by substantial margins (PSNR +1.8, LPIPS −0.10, FVD −92 on TokenBench). Even INFOTok at BPP=0.56 (44% fewer tokens) beats ElasticTok at BPP=0.81 on most metrics (PSNR 29.27 vs 28.26, LPIPS 0.176 vs 0.244, FVD 70 vs 141).

- **Inference efficiency.** The router requires one additional decoder pass versus ElasticTok's ~11 NFEs for binary search (Figure 4g), a genuine practical advantage for deployment.

- **Sanity-check ablation against optimal routing.** Table 2 compares the ELBO-based router to an exhaustive search over token lengths, finding near-identical performance. This validates that the ELBO proxy is working as intended — a kind of validation uncommon in tokenization papers.

## Weaknesses

### Major

- **Per-token ELBO computation is underspecified (Section 3.2, line 162).** The adaptive compressor selects which tokens to discard based on "per-token log-likelihood" approximated via "ELBO values." However, ELBO as defined in Equation 3 is a scalar over the entire video. The paper never explains how this scalar is factorized into per-token values that drive the masking decision — whether via per-pixel reconstruction error aggregated per latent spatial-temporal region, per-token KL divergence, or some other decomposition. Since this is the core mechanism of the adaptive compressor, the specification is incomplete: a practitioner cannot reproduce the method from the description as given. This is the most significant barrier to assessing the paper's technical contribution.

- **Theorem 3.1 is overclaimed relative to what it proves (lines 148–154).** The theorem states E[N_x] ≤ H_C(D) + β − E[−log p(x)], where the slack term β − E[−log p(x)] is unconstrained (≥ 0, could be arbitrarily large). The paper then claims "compression rate is optimal up to the approximation error" and handwaves that "ELBO values are believed to be close enough to the log-likelihoods." No bound on the slack is provided, nor is there any analysis of when this gap is small. The theoretical guarantee as presented is weaker than the paper's claims about it.

### Minor

- **"Save approximately 50% tokens" claim is imprecise (line 38).** The best comparison in Table 1 shows 44% fewer tokens (BPP 0.56 vs 1.00) with a non-trivial PSNR drop (29.27 vs 30.01). The 20% savings claim in the abstract (BPP 0.81 vs 1.00) is well-supported with near-identical PSNR, but the 50% figure is rounded up and ignores the associated quality degradation.

- **No error bars or confidence intervals.** No standard deviations are reported for any metric in Tables 1–3. For a comparison claiming SOTA performance, this makes it harder to assess the significance of the improvements.

- **The ELBO-based router may have limited differentiation under certain conditions (Section 3.1).** If the fixed-length base tokenizer has sufficient capacity that ELBO values for different videos converge (both simple and moderately complex videos saturate the model's capacity), the router's ability to distinguish videos becomes weaker than the theory suggests. The paper does not discuss this regime.

### Trivial
None.

## Nice-to-Haves
- A wall-clock time comparison beyond NFEs would strengthen the efficiency claim (the paper defers this to the appendix).
- Clarifying how the binary mask m is encoded with ~5% overhead would aid reproducibility.
- Providing error bars would strengthen the empirical evaluation.
- The "optimal" routing baseline in Table 2 optimizes over the entire dataset; comparing against a per-video oracle (without cross-video optimization) would be a cleaner ablation.

## Removed Points
These points were considered but removed from the main review:
- **"Circularity in ELBO computation"** (framed as methodological gap): The paper explicitly describes a two-step process — encode and decode without the compressor to compute ELBO, then use the router, then use the compressor. This is a reasonable procedure, not a circularity. Removed.
- **Deterministic vs stochastic router notation**: Algorithm 1 uses sampling notation (N_x ~ r(N|x)) but Equation 4 explicitly specifies a delta distribution. This is standard conventions clashing, not an ambiguity. Removed.
- **Mask encoding scheme not specified**: The paper mentions ~5% overhead; the specific encoding scheme is a reasonable implementation detail. Moved to nice-to-have.
- **INFOTok-Flex β conditioning question**: The paper explicitly states (line 156) that β is input to the adaptive compressor during training. The reviewer missed this. Removed.
- **Wall-clock time not reported**: The paper defers this to the appendix, which is stripped by the parser. Removed.
- **Theorem gap framed as "fatal"**: The theorem is mathematically valid; the issue is about the strength of the claim made about it, not the theorem itself. Retained as Major (overclaim) rather than Fatal.

## Novel Insights
None beyond the paper's own contributions. The harsh critic's observation about the underspecified per-token ELBO is valid and worth emphasizing, but is a criticism, not a novel insight.

## Suggestions
1. **Clarify per-token ELBO computation explicitly.** Provide a formula or algorithm showing how the scalar ELBO (or its reconstruction error proxy) is decomposed into per-token values — e.g., per-pixel MSE aggregated per latent spatial-temporal position in the Cosmos 3D grid.
2. **Calibrate the claims about Theorem 3.1.** Either provide a tighter bound on the slack term β − E[−log p(x)], or explicitly acknowledge that the optimality guarantee depends on ELBO being close to log-likelihood (which is empirically plausible but not formally proven).
3. **Add error bars or confidence intervals to the main results.** Even bootstrapped estimates would help assess significance.
4. **Discuss the saturation regime** where the base tokenizer's capacity makes ELBO values converge across videos of differing complexity.

## Score and Decision
**MY FINAL SCORE:** <score>6.0</score>
**MY FINAL DECISION:** <decision>Accept</decision>