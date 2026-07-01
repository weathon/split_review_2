Now I have enough context from the calibration anchors. Let me write the final consolidated review.

## Summary

VQ-Transplant proposes a two-stage framework for integrating new VQ modules into pre-trained visual tokenizers (using VAR as the testbed): (1) substitute the native VQ module while freezing the encoder/decoder, then (2) lightly adapt the decoder for 5 epochs to resolve the quantization-decoder mismatch. The paper also introduces MMD-VQ as a secondary contribution. Experiments span 5 VQ algorithms, multi-scale and fixed-scale configurations, multiple codebook sizes, and 4 datasets.

## Strengths

- **Well-motivated, practically relevant problem.** The paper identifies a genuine bottleneck: training VQ-based tokenizers with adversarial training is computationally prohibitive for most researchers. The framing — "Can we decouple VQ development from full tokenizer training?" — is concretely scoped and the two-stage solution is conceptually clean.

- **Clear diagnostic and resolution of the decoder mismatch.** The paper explicitly demonstrates (Section 5.1, Table 3) that VQ module substitution alone degrades r-FID even when quantization error drops, and that 5 epochs of decoder adaptation resolves this. The epoch-by-epoch tracking in Table 4 makes the improvement trajectory transparent. This is precisely the kind of sanity check that builds credibility.

- **Extensive empirical coverage.** The paper evaluates 5 VQ algorithms (Vanilla VQ, EMA VQ, Online VQ, Wasserstein VQ, MMD VQ) under both multi-scale and fixed-scale configurations, with 2–3 codebook sizes per method, across 4 datasets (ImageNet-1k, FFHQ, CelebA-HQ, LSUN-Churches). The consistent pattern — distribution-alignment methods (Wasserstein, MMD) outperform vanilla alternatives across nearly all settings — reinforces the technical claim.

- **Transparent reporting of within-method limitations.** The paper acknowledges that (a) substitution alone degrades reconstruction, (b) decoder adaptation is necessary, and (c) more epochs further improve results (Table 5: 0.81 → 0.74 r-FID over 20 epochs).

## Weaknesses

### Fatal
None.

### Major

1. **The headline 21.8× speedup claim conflates multiple confounds.** Table 1 compares VQ-Transplant (2×A100, 22h, ImageNet-1k) against VAR (16×A100, 60h, OpenImages). The factor of 21.8 mixes: (a) savings from not training the encoder-decoder, (b) a 5.6× difference in GPU count, (c) training on a smaller dataset (ImageNet-1k vs. OpenImages). The reader cannot attribute the speedup to the method versus the experimental setup. A controlled comparison using the same architecture, dataset, and hardware would be needed to support the headline claim.

   *Evidence*: Table 1 shows VAR trained on OpenImages with 16×A100 for 60h (960 GPU-hours), while VQ-Transplant uses ImageNet-1k with 2×A100 for 22h (44 GPU-hours). The abstract and introduction ("being 21.8× faster than training vanilla VAR") present this number without the necessary caveats about confounded factors.

2. **MMD-VQ performs indistinguishably from Wasserstein VQ, undermining the secondary contribution.** The paper motivates MMD-VQ by arguing that Wasserstein VQ relies on a Gaussian assumption that "fails to achieve effective distribution alignment" for non-Gaussian data. However, across nearly all configurations, MMD-VQ and Wasserstein VQ produce essentially identical results, and Wasserstein VQ sometimes slightly outperforms MMD-VQ:

   - Table 3, multi-scale K=8192 Adaptation: MMD VAR 0.81 r-FID vs. Wasserstein VAR 0.83 r-FID
   - Table 7, fixed-scale K=16384 Adaptation: MMD VQ 1.05 r-FID vs. Wasserstein VQ 1.04 r-FID (Wasserstein better)
   - Table 8, FFHQ K=32768 Adaptation: MMD VQ 1.37 r-FID vs. Wasserstein VQ 1.21 r-FID (Wasserstein better)

   The paper provides no diagnostic evidence (e.g., a synthetic experiment with controlled non-Gaussian data) that MMD captures higher-order statistics Wasserstein VQ misses. The empirical data is consistent with the null hypothesis that the two methods perform equivalently for this task.

### Minor

3. **Table 2's "state-of-the-art" comparisons lack adequate caveats about the backbone.** The paper compares VQ-Transplant variants (which inherit a fully trained VAR encoder-decoder) against tokenizers trained entirely from scratch (VQGAN, RQVAE, etc.). While this is a legitimate holistic comparison for the framework claim, the results primarily reflect the quality of the pretrained backbone rather than the VQ method itself. The paper should explicitly acknowledge this asymmetry.

4. **The from-scratch comparison in Table 6 is uninformative.** The paper trains MMD VAR from scratch for 5–7 epochs (25–35 hours) and observes worse performance than VQ-Transplant, then acknowledges that "discrete tokenizers typically require hundreds of epochs to achieve high-quality visual reconstruction when trained from scratch." The outcome is predetermined; the comparison does not provide useful information and detracts from the paper's credibility.

5. **No downstream generation evaluation.** The paper motivates VQ tokenizers for "visual generation" and "vision-language modeling" (Section 1) but evaluates only reconstruction metrics (r-FID, PSNR, SSIM, LPIPS, r-IS). While reconstruction is the standard evaluation in tokenizer papers and the scope is about VQ module integration, the absence of any generation experiment limits the assessment of whether the transplanted tokens are useful for the stated downstream applications.

### Trivial
None.

## Nice-to-Haves

- A controlled speedup comparison (same architecture, same dataset, same hardware) to cleanly isolate the method's savings.
- Synthetic non-Gaussian experiment to demonstrate whether MMD-VQ provides any advantage over Wasserstein VQ.
- A downstream generation experiment (e.g., training a small autoregressive transformer on transplanted tokens).
- Ablation of the parallel quantization design for fixed-scale VQ.

## Removed Points

- Criticism about Wasserstein VQ criticism lacking evidence: the paper's argument about Gaussian limitations is a cited theoretical claim from prior work (Fang et al., 2025); this is a reasonable motivation even if the empirical advantage is not borne out. However, the weakness about MMD-VQ not showing empirical advantage over Wasserstein VQ is retained above.
- Equation typo complaint about ℒ_Perf: this is a parser/formatting artifact.
- Missing appendix / proof content: parser strips these sections; they exist in the original submission.
- Missing bandwidth selection for MMD kernel: likely reported in the stripped appendix.
- Pure formatting nitpicks.
- Cross-dataset baselines complaint: functionally duplicates Minor #3 above (backbone advantage applies uniformly).

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observation that the quantitative support for MMD-VQ over Wasserstein VQ is essentially absent is the most novel critical insight — the paper's own data undermines its secondary contribution claim.

## Suggestions

1. **Reframe the speedup claim.** Either provide a controlled comparison or clearly decompose the 21.8× into components (architecture savings, hardware scaling, dataset size) so readers can assess how much is attributable to the method.

2. **Either provide evidence for MMD-VQ or reframe it.** If MMD-VQ cannot be shown to outperform Wasserstein VQ on this task, present it as a simple non-parametric alternative rather than an improvement. Remove or soften the language suggesting Wasserstein VQ "fails" for non-Gaussian features.

3. **Add caveats to Table 2.** Explicitly note that VQ-Transplant inherits a pretrained VAR encoder-decoder, which contributes substantially to the reconstruction quality.

4. **Remove or strongly caveat Table 6.** It adds no useful information and undermines credibility.

5. **Consider adding a generation experiment** in the camera-ready version to strengthen the practical significance of the contribution.

## Score and Decision

**Calibration.** I retrieved 10 anchor papers across score ranges via `calibration_search`. The closest topical matches are: "Vector Quantization By Distribution Matching" (avg 4.75, rejected) — the Wasserstein VQ paper, a closely related prior work whose main weaknesses (marginal improvement, insufficient ablation) are partially addressed by VQ-Transplant's more extensive evaluation; "LL-VQ-VAE" (avg 4.75, rejected) — a VQ method missing downstream generation evaluation; "Image Generation with Channel-wise Quantization" (avg 4.00, rejected) — similar unfair comparison concerns; "Binary Spherical Quantization" (avg 5.75, accepted) — a VQ tokenizer with SOTA reconstruction and generation, stronger claims but narrower evaluation; "Finite Scalar Quantization" (avg 6.50, accepted) — a clean, well-received VQ replacement; "ElasticTok" (avg 6.00, accepted) — adaptive tokenization with reconstruction and generation; "How many tokens is an image worth?" (avg 5.75, accepted) — variable-length tokenization with strong evaluation.

**Bracket.** Round 1 placed the paper in the 5.5–6.5 range. Round 2 anchored within this range using accepted papers with comparable strengths/weaknesses. VQ-Transplant has a stronger primary contribution and more extensive evaluation than the rejected anchors (4.75), while its comparison fairness issues and lack of downstream evaluation place it below FSQ (6.50). It is most comparable to BSQ (5.75) and ElasticTok (6.00) in scope and rigor, but with more caveats on the headline claims.

**Final score: 6.0.** The core VQ-Transplant framework is a solid, practical contribution with extensive empirical support. However, the overstated speedup claim, the empirically unsupported MMD-VQ secondary contribution, and the uninformative from-scratch comparison prevent this from being a stronger accept. The paper would benefit from more careful claim calibration rather than maximalist framing.

**Round-1 bracket stated explicitly:** 5.5–6.5

**Round-2 narrowed to:** 6.0

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>