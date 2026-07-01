## Summary

The paper proposes VQ-Transplant, a framework that enables plug-and-play replacement of VQ modules in pre-trained discrete visual tokenizers (specifically VAR) without full retraining, using (1) VQ module substitution while freezing encoder-decoder parameters, followed by (2) lightweight decoder adaptation (5 epochs). A secondary contribution is MMD-VQ, a distribution-alignment VQ method using maximum mean discrepancy. Experiments show ~95% cost reduction (44 GPU-hours vs 960 GPU-hours for VAR) while achieving competitive or better reconstruction fidelity on ImageNet-1k and cross-dataset benchmarks.

## Strengths

1. **Clear, practical motivation with strong evidence.** Table 1 concretely quantifies the problem: training discrete tokenizers from scratch costs 960 GPU-hours for VAR, versus VQ-Transplant's 44 GPU-hours. This framing is well-supported and genuinely lowers the barrier to VQ research.

2. **Two-stage design is well-motivated and empirically validated.** Table 3 shows that Stage I achieves lower quantization error than the original VAR tokenizer (MMD VAR: 0.255 vs VAR: 0.283) but worse r-FID (1.52 vs 0.92), confirming the decoder-quantization mismatch. Stage II resolves this (r-FID improves to 0.91), validating the two-stage design convincingly.

3. **Computational savings are dramatic and robustly demonstrated.** 22 hours on 2×A100 (44 GPU-hours) vs 60 hours on 16×A100 (960 GPU-hours) for VAR. Even including decoder adaptation, total cost is a small fraction of end-to-end training.

4. **Ablation on adaptation epochs (Tables 4, 5, Figure 3) is informative.** The paper honestly tracks r-FID improvement over 20 epochs, showing clear improvements and revealing that "5 epochs" is a trade-off, not a convergence point.

## Weaknesses

### Major

- **Uncontrolled token counts in cross-method comparison (Table 2).** The paper claims MMD-VQ and MMD-VAR "outperform competing baselines" using Table 2, where MMD VQ (FS VQ) uses **512 tokens** while most baselines (DQVAE, DiVAE, VQGAN, VQGAN-LC, etc.) use **256 tokens**. Token count directly determines reconstruction quality — doubling tokens trivially improves r-FID. The controlled within-token-count comparison (MMD VAR at 680 tokens vs original VAR at 680 tokens) does show real improvements (r-FID 0.81 vs 0.92), and MMD VQ at 512 tokens also beats RQVAE at 512 tokens (r-FID 0.86 vs 2.69). But the paper's framing of general superiority cites the entire table including the uncontrolled 512-vs-256 comparison. The paper should present controlled comparisons or explicitly acknowledge this confound when making superiority claims.

- **"State-of-the-art" claims on cross-dataset experiments (Section 5.3) suffer from the same token-count confound.** On FFHQ (Table 8), VQ-Transplant models use 512 tokens while baselines (VQGAN, VQGAN-LC, RQVAE) use 256 tokens. The paper writes "achieving state-of-the-art reconstruction performance across all three benchmarks" and "Wasserstein VQ achieves a record r-FID of 1.21" — claims that are not controlled for token budget. These comparisons would be informative with proper caveats but are currently overstated.

### Minor

- **MMD-VQ's empirical advantage over Wasserstein VQ is marginal and inconsistent.** Across all comparisons, the two methods produce nearly identical results with no clear winner: MMD VAR r-FID 0.81 vs Wasserstein VAR r-FID 0.83 (Table 3, K=8192); on FFHQ (Table 8, K=32768), Wasserstein VQ r-FID 1.21 actually beats MMD VQ r-FID 1.37. No error bars are reported, so it is impossible to assess statistical significance. Since MMD-VQ is presented as a secondary contribution motivated by improving upon Wasserstein VQ (which "critically relies on Gaussian distribution assumptions"), the evidence for this claimed advantage is very thin.

- **No downstream generation evaluation.** The paper's stated motivation (Section 1, line 13) cites "downstream tasks including visual generation," and tokenizers like VAR are designed for generative modeling. Yet evaluation is limited to reconstruction metrics (r-FID, PSNR, SSIM, LPIPS). Reconstruction quality does not guarantee that the latent space supports good generation. Adding at least one generative experiment (e.g., training an autoregressive transformer on MMD VAR tokens) would substantially strengthen the paper's claims about practical significance for generative modeling. (That said, most VQ tokenizer papers in this subfield also evaluate primarily on reconstruction, so this is a gap but not a fatal omission.)

- **Decoder adaptation stage uses adversarial training despite the paper's framing.** The paper motivates VQ-Transplant partly by noting that adversarial training is "inherently unstable" and "computationally intensive" (Section 1, paragraph 2). Yet Stage II uses a full GAN loss with DINO-S discriminator, DiffAug, consistency regularization, and LeCAM regularization. While training only the decoder is indeed cheaper and more stable than end-to-end training (which is the correct comparison), the framing could more transparently acknowledge that adversarial training is still present.

### Trivial

- No variance or error bars reported across any table. For metrics like r-FID that depend on discriminator training, this limits assessment of small differences (e.g., MMD vs Wasserstein VQ).

- The MMD kernel bandwidth parameters (σ_i) are not specified in the main text (they may be in the appendix which was stripped by the parser).

## Nice-to-Haves

- Add MMD VQ results with 256 tokens to Table 2 to enable a direct controlled comparison against the 256-token baselines.
- Add a downstream generation experiment (e.g., class-conditional image generation using a transformer trained on VQ-Transplant tokens).
- Include error bars or confidence intervals for key comparisons, especially MMD vs Wasserstein VQ.
- The "95% cost reduction" claim in the abstract assumes a pre-trained base tokenizer exists; this caveat could be made more explicit.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"From-scratch comparison (Table 6) is a strawman"** — REMOVED. The paper compares VQ-Transplant (22h) with from-scratch training for 5–7 epochs (25–35h, which is *more* compute). The paper explicitly acknowledges "This outcome is expected, as discrete tokenizers typically require hundreds of epochs." The comparison demonstrates that with similar or greater compute, from-scratch training is far inferior, which is a meaningful validation of VQ-Transplant's advantage. The critic's suggestion to include pre-training cost of the base tokenizer misunderstands the framework's value proposition (reusing an existing pre-trained model).

2. **"LDM-16 experiment is an afterthought"** — REMOVED. Testing on a VAE-based tokenizer is a reasonable and honest probe of generality. Results are in the appendix as noted.

3. **"Table 1 mixes different dataset scales and GPU configurations"** — REMOVED. The Speedup column consistently compares GPU-hours (e.g., Llama GEN: 2×A100×200h = 400 GPU-hours vs VQ-Transplant: 2×A100×22h = 44 GPU-hours), making the comparison fair and interpretable.

4. **"Section 2 characterization of Wasserstein VQ is imprecise"** — REMOVED. This is a minor framing nuance, not a substantive weakness.

5. **"Equation (3) L_unique unclear for non-MMD methods"** — REMOVED. The paper explicitly says "e.g., Wasserstein loss for Wasserstein VQ (Fang et al., 2025)" which clarifies the pattern.

6. **"Missing codebook collapse analysis beyond utilization"** — REMOVED as a nice-to-have that does not affect the core claims.

## Novel Insights

The most interesting finding from the reviewer analysis is the decoder-quantization mismatch phenomenon documented in Table 3: Stage I achieves strictly lower quantization error (MMD VAR: 0.255 vs original VAR: 0.283) but substantially worse reconstruction (r-FID 1.52 vs 0.92). This counter-intuitive result — better quantization hurting reconstruction — is a genuine insight that the paper correctly identifies and resolves with decoder adaptation. This observation could have broader implications for VQ tokenizer design beyond the specific framework.

## Suggestions

1. **Fix the token-count confound.** Either: (a) add MMD VQ results at 256 tokens to Table 2, or (b) clearly separate the within-token-count comparisons from cross-token-count comparisons and temper the superiority claims accordingly.
2. **Address the MMD-VQ positioning.** Either add error bars showing statistical significance, or acknowledge that MMD-VQ and Wasserstein VQ perform similarly and position MMD-VQ as an alternative formulation rather than a clearly superior method.
3. **Add at least one downstream generation experiment.** Even a single experiment training a small autoregressive transformer on MMD VAR tokens would validate the practical relevance.
4. **Tone down "state-of-the-art" claims** on cross-dataset results where token counts are not controlled. Replace with "competitive" or "strong" performance and note the token-count caveat.

## Score and Decision

**Round 1 bracket (initial range after calibration):** 4.5 – 5.5

**Calibration anchors consulted:**
1. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/YlWvQSBCgl.md` — "Image Generation with Channel-wise Quantization" (avg 4.0, Reject). Similar VQ tokenizer paper rejected for unfair comparison (token count issues) and missing experiments. The current paper has a stronger core contribution (VQ-Transplant framework) but similar comparison issues.
2. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/IqGVIU4rvM.md` — "Balancing Token Efficiency..." (avg 2.5, Reject). Poorly executed VQ tokenizer paper with fundamental flaws. Current paper is substantially stronger.
3. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/yGnsH3gQ6U.md` — "Binary Spherical Quantization" (avg 5.75, Accept). Strong tokenizer paper accepted despite similar concerns about fair comparison. Had more thorough evaluation (generation, compression) and a novel quantization method.
4. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/mb2ryuZ3wz.md` — "How many tokens is an image worth?" (avg 5.75, Accept). Tokenizer paper accepted with thorough analysis.
5. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gKui6QvvfK.md` — "Compositional VQ Sampling" (avg 5.25, Reject). Rejected for limited novelty despite sound technical contribution.

**Final score determination:** The paper's core contribution (VQ-Transplant framework) is practically useful and well-validated on computational efficiency. However, the evaluation is weakened by uncontrolled token-count comparisons across main results, overstated SOTA claims, a marginal secondary contribution (MMD-VQ), and the absence of downstream generation experiments. Compared to accepted tokenizer papers at the 5.75 level (BSQ, "How many tokens"), this paper has a less thorough evaluation and a weaker secondary contribution. Compared to rejected papers at 4.0–5.25, this paper's core framework idea is stronger and better motivated. A score of 5.0 reflects a paper with a solid core contribution that is undercut by evaluative weaknesses — below the acceptance threshold in current form, but with a clear path to improvement.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>