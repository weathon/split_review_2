## Summary

This paper introduces InfoTok, a framework for adaptive discrete video tokenization grounded in Shannon's information theory. It connects token-length selection to the Source Coding Theorem, proves that data-agnostic routers (fixed-rate or uniform-sampling) are suboptimal, and derives a router that selects token counts proportional to the ELBO (negative reconstruction loss). A transformer-based adaptive compressor then retains only the top-\(N_x\) tokens by ELBO value. Experiments on TokenBench and DAVIS show that InfoTok consistently outperforms the adaptive baseline ElasticTok at matched BPP values (PSNR +1–2 dB, FVD –40–60%), achieves ~20% token savings over the fixed-length Cosmos-DV at equivalent quality, and requires only 1 decoder pass per video vs. ElasticTok's 11.

## Strengths

1. **Novel and well-executed information-theoretic framing (Sections 2.2–2.3, 3.1).** The paper formalizes expected token length as an information-theoretic quantity, proves that uniform-length routers can be arbitrarily inefficient (Theorem 2.2), and shows that routing proportional to log-likelihood achieves near-optimal expected length (Theorem 3.1). This theory directly motivates the ELBO-based router design rather than serving as lip service.

2. **Clean and practical ELBO-based router (Section 3.1, Eq. 4).** Rather than requiring search at inference time, the router reuses the reconstruction error the model already computes, needing only 1 additional decoder pass vs. ElasticTok's 11 forward evaluations (Figure 4g). The ablation in Table 2 confirms that ELBO-based routing closely matches an exhaustive-search "optimal" routing — a concrete sanity check.

3. **Substantial and consistent empirical results against ElasticTok (Table 1, Figure 4).** At matched compression rates (BPP16 = 0.81 and 0.56), InfoTok outperforms ElasticTok across all four metrics on both datasets. The "2.3×" compression-rate advantage (achieving similar quality at ~2.3× higher compression) is credible from the rate-distortion curves in Figure 4.

4. **Well-designed cross-architecture ablation (Table 3 Right).** InfoTok's adaptive mechanism systematically outperforms ElasticTok's uniform mechanism on both the Cosmos architecture and a ViT architecture, ruling out the concern that gains are architecture-specific.

## Weaknesses

### Fatal
None.

### Major

1. **Inconsistent and unsupported claims about token savings (Abstract vs. Introduction).** The abstract (line 9) claims "saving 20% tokens without influence on performance," while the introduction (line 38) claims "save approximately 50% tokens without loss of reconstruction quality compared to state-of-the-art fixed-length tokenizers." Table 1 supports only the 20% claim: InfoTok at BPP16 = 0.81 achieves PSNR 30.08 vs. Cosmos-DV at BPP16 = 1.00 (PSNR 30.01) — ~19% savings with equivalent quality. The 50% savings claim (BPP16 = 0.56 vs. 1.00) corresponds to ~44% fewer tokens but with a measurable quality drop (PSNR 30.01→29.27, LPIPS 0.138→0.176). The introduction's "without loss" assertion for ~50% savings is contradicted by the paper's own data. This must be corrected before publication.

2. **Comparison with fixed-length tokenizers confounds adaptivity with added model capacity.** InfoTok adds an 8-layer transformer-based compressor/decompressor on top of Cosmos-DV. The headline comparison (InfoTok at BPP16 = 0.81 vs. Cosmos-DV at BPP16 = 1.00) compares Cosmos-DV + extra layers to Cosmos-DV without those layers. The paper does not include a control: Cosmos-DV with 8 additional transformer layers operating at fixed compression. Without this, it is unclear how much of the gain is from adaptivity vs. from extra parameters. The within-architecture comparison (Table 3 Right) confirms the ELBO-based routing itself provides gains over uniform routing on the same architecture, but does not resolve the fixed-length comparison confound.

### Minor

3. **Evaluation is limited to reconstruction quality.** The paper's motivation emphasizes downstream tasks (generation, understanding), but all experiments measure pixel-level and perceptual reconstruction (PSNR, SSIM, LPIPS, FVD). The paper honestly scopes this out (lines 168, 272), and reconstruction quality is a necessary condition for good representation. However, the central claim of "more compressed yet accurate tokenization" is only supported for reconstruction fidelity, and the paper's significance would be strengthened by even a small-scale downstream sanity check.

4. **Insufficient detail on ElasticTok alignment.** Since ElasticTok only accepts square 256px input, datasets were cropped and ElasticTok was re-run. The paper states they "align our methods with their settings" (line 201) but provides limited detail on whether ElasticTok's loss thresholds were re-tuned or calibrated for the processed data. Given that ElasticTok uses loss-threshold-based inference while InfoTok directly specifies BPP, the alignment procedure is non-trivial and the description is too brief for reproducibility.

### Trivial
None.

## Nice-to-Haves
- A parameter-matched control (Cosmos-DV + 8 transformer layers at fixed compression) would cleanly isolate the contribution of adaptivity from added capacity.
- A small-scale downstream sanity check (e.g., linear probe on UCF-101) would substantiate the claim that adaptive tokens retain task-relevant information.
- Quantitative analysis of within-video token allocation (e.g., per-frame allocation vs. motion complexity) would strengthen the qualitative illustration in Figure 1.

## Removed Points
These points were identified in the input review but removed per the filtering guidelines. They are included here for traceability but should not affect the final evaluation.

- **"No wall-clock timing data"**: The paper states (line 237) that wall-clock latency details are in Appendix D, which is stripped by the parser. Removing per the hard rule on missing appendix content.
- **"No discussion of the 8-layer transformer compressor's training cost/parameter count"**: The paper references Appendix C (line 168) for training and resource details, which is stripped. Removing per the same hard rule.
- **Criticisms about Theorem 2.2 being idealized**: The paper explicitly frames it as an in-principle bound ("to rigorously prove why this is biased"), so this is a self-aware theoretical bound, not a flaw.
- **Criticisms about the ELBO gap in Theorem 3.1**: The paper acknowledges the approximation and validates it empirically in Table 2. The gap is standard for ELBO-based methods.
- **"Adaptive decompressor not described separately"**: The paper states (line 164) that the decompressor "contains multiple Transformer layers" — the description is brief but present.
- Various formatting/style nitpicks and "area of concern" speculative framings that lacked a concrete anchor in the paper.

## Novel Insights
The harsh review insightfully identifies that the paper's central comparison (InfoTok vs. fixed-length Cosmos-DV) is confounded by the 8-layer transformer compressor added to InfoTok but not to Cosmos-DV. This is sharper than a generic "add more baselines" critique because it targets a specific missing control experiment that would cleanly isolate adaptivity from added capacity. The review also correctly catches the contradictory 20%/50% claim — a factual overstatement that needs correction but does not invalidate the method itself.

## Suggestions
1. Correct the introduction's 50% claim to match the data in Table 1; the abstract's 20% claim is accurate.
2. Add a parameter-matched ablation: train Cosmos-DV with 8 additional transformer layers at fixed compression and compare its rate-distortion curve to InfoTok's.
3. Provide more detail on how ElasticTok's loss thresholds were tuned on the processed datasets.
4. Add a small-scale downstream experiment (e.g., linear probe) to demonstrate that the adaptive tokens preserve task-relevant information.

---

**Calibration report (for transparency):**

*Round 1 — Bracketing.* Retrieved anchors in six bands (score ranges: <1.5, 1.5–3.5, 3.5–5.5, 5.5–7.5, 7.5–8.5, >8.5) using the query "video tokenization adaptive compression information theory." The most directly relevant anchors were ElasticTok (6.00, accepted), BSQ-ViT (5.75, accepted), "How many tokens is an image worth" (5.75, accepted), and LARP (7.50, accepted). Round-1 bracket: [6.0, 7.5].

*Round 2 — Narrowing.* Itemized the ElasticTok anchor (6.00) and LARP anchor (7.50). ElasticTok's strongest weaknesses were methodological (left-mask strategy –9.08, computational overhead –9.70), while InfoTok's only decisive weakness is a fixable overclaim (–9.99). InfoTok's strengths (+10 for theory, +10 for empirical results, +9.92 for router design) outpace ElasticTok's strongest strength (+9.98 for writing). LARP (7.50) demonstrated downstream generation SOTA, a more complete evaluation than InfoTok's reconstruction-only scope. InfoTok sits cleanly between these two — above ElasticTok due to stronger theory, cleaner method, and better results, below LARP due to the uncorrected overclaim and reconstruction-only evaluation. Final score: **7.0**.

**Anchors retrieved (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison to this paper |
|------|-----------|-------|-----------|-------------------------|
| gwZ90hFSL2.md | 1.00 | 1 | No | Unrelated topic (cross-lingual robots) |
| 5lUdTogEL3.md | 1.00 | 1 | No | Unrelated (person re-ID) |
| Uj0h13lVrR.md | 1.00 | 1 | No | Unrelated (GFlowNets) |
| IqGVIU4rvM.md | 2.50 | 1 | No | Loosely related (VQ-VAE + diffusion tokenizers) |
| 6j0GH40mFt.md | 3.40 | 1 | No | Loosely related (image compression, different task) |
| DsMxVELk3K.md | 3.00 | 1 | No | Loosely related (text compression) |
| aQ7qYnY2nF.md | 4.00 | 1 | No | Loosely related (video compression, different task) |
| EukM0UuqLx.md | 4.00 | 1 | No | Related token-level compression concept |
| 1xG3MN1RRW.md | 5.20 | 1 | Yes | Token pruning for VLMs; InfoTok is stronger |
| tFV5GrWOGm.md | 6.00 | 1 | Yes | **Direct baseline ElasticTok**; InfoTok has stronger theory, better results, cleaner method, but has a fixable overclaim |
| yGnsH3gQ6U.md | 5.75 | 1 | Yes | Video tokenizer (BSQ-ViT); InfoTok's theoretical grounding is deeper |
| mb2ryuZ3wz.md | 5.75 | 1 | Yes | Adaptive image tokenization; InfoTok's video + theory contribution is stronger |
| CxXGvKRDnL.md | 8.00 | 1 | No | Diffusion + compression; different topic |
| 9Cu8MRmhq2.md | 8.00 | 1 | No | Video-language learning; different topic |
| 2dnO3LLiJ1.md | 8.00 | 1 | No | Vision Transformers; different topic |
| Wr3UuEx72f.md | 7.50 | 2 | Yes | **LARP** video tokenizer for generation; InfoTok has stronger theory but reconstruction-only evaluation |
| WNLAkjUm19.md | 7.00 | 2 | No | Discrete tokenization theory for SSL; different task |
| B5iOSxM2I0.md | 6.50 | 2 | No | NLP tokenization theory; different domain |
| FlvtjAB0gl.md | 6.25 | 2 | No | Vision-language tokenization; different topic |

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>