Now I have all the verification I need. Let me produce the final consolidated review.

## Summary

VQ-Transplant proposes a two-stage framework (VQ module substitution + lightweight decoder adaptation) that enables plug-and-play integration of new quantization modules into frozen, pretrained visual tokenizers, avoiding the prohibitive cost of end-to-end retraining. A secondary contribution is MMD-VQ, a distribution-aligned VQ method based on maximum mean discrepancy. The paper evaluates across five VQ algorithms, two quantization configurations, and four datasets, reporting substantial training cost reduction (~44 vs. 960 GPU-hours).

## Strengths

- **Well-motivated and practical contribution.** The paper targets a genuine bottleneck: exploring new VQ methods currently requires training an entire adversarial tokenizer from scratch. Decoupling VQ module development from encoder-decoder training is practically valuable. The efficiency numbers (22 hours on 2×A100 vs. 60 hours on 16×A100) concretely demonstrate this advantage.

- **Comprehensive experimental scope.** The evaluation covers five VQ algorithms (Vanilla, EMA, Online, Wasserstein, MMD) × two configurations (multi-scale, fixed-scale) × four datasets (ImageNet-1k, FFHQ, CelebA-HQ, LSUN-Churches), with both substitution-only and decoder-adaptation phases reported. This breadth provides a richer empirical picture than narrow evaluations.

- **Clear efficiency demonstration.** Table 6 directly compares VQ-Transplant against from-scratch training of the same MMD VAR architecture: VQ-Transplant (22 hours, r-FID 0.81/0.91) dramatically outperforms from-scratch training at even longer durations (35 hours, r-FID 1.26–1.40). Together with Table 1's cost analysis, the efficiency case is well-supported.

- **Insightful decoder-quantization mismatch diagnosis.** Section 5.1 makes the nuanced observation that even when a transplanted VQ module achieves lower quantization error than the original (0.255 vs. 0.283), reconstruction metrics like r-FID are worse (1.52 vs. 0.92) — correctly attributing this to decoder prior mismatch. This diagnosis is well-supported by the data.

## Weaknesses

### Major

- **Headline performance comparison is confounded by codebook size.** The paper's central performance claim (Abstract, line 34; Section 5, line 125) states that MMD VAR achieves 0.81 r-FID vs. vanilla VAR's 0.92 r-FID. However, the 0.81 result uses K=8192 while vanilla VAR uses K=4096. At equal codebook size (K=4096), MMD VAR achieves 0.91 r-FID — a marginal 0.01 improvement (Table 2, rows 160–161). The paper does not report vanilla VAR with K=8192, so it is impossible to determine whether the 0.81 result reflects VQ-Transplant's advantage or simply the benefit of a larger codebook. The same confound affects the fixed-scale comparisons in Table 2 (MMD VQ uses 512 tokens while VQGAN baselines use 256). This does not undermine the efficiency contribution (the 21.8× training speedup is real and independent of codebook size), but the "superior reconstruction fidelity" framing as presented is misleading and needs to be restated with controlled comparisons.

- **Cross-dataset comparisons lack proper control for pretraining.** Tables 8, 9, and 10 compare VQ-Transplant methods (which use an encoder-decoder pretrained on OpenImages+ImageNet-1k) against baselines trained *from scratch* on each target dataset (FFHQ, CelebA-HQ, LSUN-Churches). The pretrained encoder-decoder's head start is a confound: some of the reported advantage may come from the strong initialization rather than from VQ-Transplant itself. The paper should include a control where the *original* VAR VQ module is adapted on these datasets using the same decoder-only finetuning procedure, isolating whether the gains come from the transplant or from the adaptation itself. Without this baseline, the "state-of-the-art" claim on these datasets is insufficiently supported.

### Minor

- **MMD-VQ provides no demonstrated advantage over Wasserstein VQ.** MMD-VQ is presented as a secondary contribution motivated by its non-parametric nature and ability to handle non-Gaussian feature distributions (Section 4.2). However, across all comparisons in Tables 3, 7, 8, 9, and 10, MMD and Wasserstein VQ perform nearly identically — differences are typically within 0.01–0.02 r-FID, and neither consistently dominates (e.g., Table 8, FFHQ Adaptation, K=32768: Wasserstein 1.21 vs. MMD 1.37 r-FID, favoring Wasserstein). The paper never demonstrates a setting where MMD's non-parametric advantage actually matters (e.g., on features that are demonstrably non-Gaussian). Calling this a "novel VQ method" overstates its distinctiveness; it is an interchangeable variant of Wasserstein VQ as evaluated.

- **Evaluation focuses solely on reconstruction, not downstream generation utility.** The introduction motivates VQ tokenizers through their role in visual generation and vision-language modeling (lines 13–14), yet the entire evaluation measures only reconstruction fidelity (r-FID, PSNR, SSIM, LPIPS, r-IS). Reconstruction quality is necessary but not sufficient for a good generative tokenizer — the discrete latent space must also be well-structured for autoregressive modeling or other downstream tasks. While many tokenizer papers evaluate only reconstruction, a brief downstream validation (e.g., training a small autoregressive transformer on transplanted tokens) would bridge the gap between the motivation and the evidence.

### Trivial

- **Inconsistent metric direction for r-IS.** Tables 2 and 3 mark r-IS with ↓ (lower is better), but the actual values show higher is treated as better (MMD VAR K=8192: 201.0 bolded as best vs. VAR: 198.6). Table 7 correctly uses ↑ for the same metric (τ-IS). The arrow direction in Tables 2 and 3 should be corrected to ↑.

## Nice-to-Haves

- Adding statistical significance or variance reporting (e.g., confidence intervals) for key comparisons, especially since some differences (e.g., 0.91 vs. 0.92 r-FID at K=4096) are within a few hundredths.
- A failure-case analysis: Vanilla VQ achieves codebook utilization as low as 0.2–0.8% under transplant (Table 7). Discussing why some methods collapse under transplant while others succeed could provide insight into what properties make a VQ method transplant-friendly.
- Reporting the 20-epoch adaptation results (0.74 r-FID, Table 5) as the headline instead of 5-epoch results, or at least acknowledging the trade-off more prominently.

## Removed Points

- **Issue about MMD-VQ being a "thin" secondary contribution:** Kept as Minor rather than removed, but downgraded from the reviewer's stronger framing. The paper explicitly calls it a "secondary contribution" (line 49), which the reviewer acknowledges but still criticizes — this is a reasonably calibrated criticism.

- **Reviewer's speculation** that "a vanilla VAR with K=8192 would likely also improve" is a reasonable inference, not a paper error. The criticism stands as a Major weakness because the missing baseline is a concrete experimental gap, not because the reviewer's speculation is wrong.

- **Harsh critic's "Missing Part 1"** (comparing against training a new VQ module from scratch): This is already addressed by Table 6, which compares VQ-Transplant vs. from-scratch training of MMD VAR. Removed as already addressed.

- **Harsh critic's "Section-by-Section" note** about the GPU-hour comparison being apples-to-oranges: The reviewer retracts this themselves (acknowledging the calculation is correct). Removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Control for codebook size and token count** in the main comparison (Table 2). Report vanilla VAR with K=8192, or restructure claims so that the headline result is the fair comparison (e.g., "0.91 r-FID at a fraction of the training cost" rather than "0.81 r-FID vs. 0.92 r-FID").
2. **Add a controlled cross-dataset baseline** where the original VAR tokenizer (with its original VQ module) undergoes the same decoder adaptation on FFHQ/CelebA-HQ/LSUN-Churches, isolating VQ-Transplant's benefit from the pretraining advantage.
3. **Include at least one downstream generation experiment** to validate that transplanted tokens are useful for autoregressive modeling, directly connecting the evaluation to the stated motivation.
4. **Either demonstrate a concrete advantage of MMD over Wasserstein VQ** (e.g., on synthetic non-Gaussian features) or honestly reframe MMD-VQ as an alternative formulation rather than a distinct contribution.
5. **Remove the paper's appendix content** from the removed sections in the output (handled by the system).

## Score and Decision

The paper's core contribution — VQ-Transplant as a framework for efficient VQ module integration into frozen tokenizers — is sound, the efficiency gains are real, and the evaluation is comprehensive. The main problems are overclaiming (using uncontrolled comparisons in headline results) and a missing control in cross-dataset experiments. Both are addressable in revision.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>