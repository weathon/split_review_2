## Summary

This paper proposes VQ-Transplant, a two-stage framework that replaces the VQ module in a pre-trained visual tokenizer (specifically VAR) while keeping the encoder-decoder frozen (Stage I), then performs lightweight decoder fine-tuning (5–20 epochs) to resolve distribution mismatch (Stage II). Within this framework, the authors also introduce MMD-VQ, which substitutes the Wasserstein loss with an MMD loss for distribution alignment. Experiments across 4 datasets and 5 VQ algorithms show that decoder adaptation recovers reconstruction quality after VQ module substitution, and with a larger codebook (K=8192) can modestly exceed the original VAR tokenizer's r-FID.

## Strengths

1. **The two-stage design is clean and empirically validated.** The paper clearly identifies the decoder-quantization mismatch problem (Section 5.1, lines 224–226) and shows that decoder adaptation resolves it: r-FID drops from 1.52 (substitution-only) to 0.91 (K=4096) and 0.81 (K=8192) after 5 epochs of adaptation (Table 3). The ablation tracking r-FID over 20 epochs (Table 5, Figure 3) confirms consistent improvement, giving practitioners a practical recipe.

2. **Comprehensive empirical coverage.** The paper evaluates 5 VQ algorithms (Vanilla, EMA, Online, Wasserstein, MMD) in both multi-scale and fixed-scale configurations, across 4 datasets (ImageNet-1k, FFHQ, CelebA-HQ, LSUN-Churches), with codebook sizes from 4096 to 65536, and includes ablation on adaptation epochs (5/10/15/20). This thoroughness allows readers to assess the framework's behavior across diverse settings.

3. **Cross-dataset generalization is demonstrated.** The paper validates VQ-Transplant on FFHQ, CelebA-HQ, and LSUN-Churches — datasets visually distinct from ImageNet/OpenImages — showing that the framework is not simply memorizing in-distribution patterns (Tables 8–10).

## Weaknesses

### Fatal
None.

### Major

1. **Headline efficiency claims are misleading.** The paper asserts "21.8× faster training" (line 34) and "95% cost reduction" (line 9) by comparing VQ-Transplant's 22 hours on 2×A100 GPUs against VAR's 60 hours on 16×A100 GPUs (Table 1). This comparison bundles the entire pre-training cost of VAR's encoder-decoder into the baseline while exempting VQ-Transplant from it. VQ-Transplant *depends on* the pre-trained VAR encoder-decoder, which itself required substantial resources. The fair framing is "22 additional hours on top of the pre-trained encoder-decoder," not "22 hours vs. 60 hours." The comparison in Table 1 also mixes different training datasets (ImageNet-1k vs. OpenImages), GPU counts, and architectures, making the speedup numbers hard to interpret. Table 6 further compounds this by comparing VQ-Transplant (22 hours) against MMD VAR trained from scratch for only 5–7 epochs (25–35 hours) — a comparison the paper itself undermines by noting that "discrete tokenizers typically require hundreds of epochs" (line 265). This presentation overstates the efficiency contribution.

2. **Improvement over VAR is confounded by codebook size.** At equal codebook size (K=4096), MMD VAR achieves 0.91 r-FID vs. VAR's 0.92 (Table 3) — essentially a tie. The headline improvement to 0.81 r-FID requires K=8192 (Table 3, line 162). The paper does not ablate whether the original VAR's native VQ module with K=8192 (plus decoder fine-tuning for the same number of epochs) would achieve comparable gains. Without this control, the claimed superiority of MMD-VAR over the original VAR cannot be attributed to the VQ method rather than simply a larger codebook. This weakness directly affects the paper's central quality claim in the abstract and introduction.

### Minor

3. **MMD-VQ shows no clear empirical advantage over Wasserstein VQ.** MMD-VQ and Wasserstein VQ perform near-identically across most settings. On ImageNet-1k multi-scale, the difference is 0.91 vs. 0.93 r-FID at K=4096 adaptation (Table 3). On FFHQ after adaptation at K=32768, Wasserstein VQ achieves 1.21 r-FID while MMD VQ achieves 1.37 r-FID — *worse* (Table 8). On LSUN-Churches adaptation, the methods are effectively tied (1.79 vs. 1.87 r-FID, Table 10). The paper's theoretical motivation (MMD is better for non-Gaussian distributions, line 105) is not empirically substantiated — no evidence is provided that feature distributions in these datasets are non-Gaussian or that MMD captures differences Wasserstein misses. Since MMD-VQ is presented as a "secondary contribution" (line 49), this weakens that contribution but does not affect the primary VQ-Transplant framework.

4. **Cross-dataset evaluation compares only against older methods.** Tables 8–10 on FFHQ, CelebA-HQ, and LSUN-Churches include RQVAE, VQGAN variants, VQ-WAE, and MQVAE — all older from-scratch methods. The original VAR tokenizer (the paper's base model) is not evaluated on these datasets, making it difficult to assess whether VQ-Transplant's cross-dataset generalization is competitive with its own starting point. The claim of "state-of-the-art reconstruction performance across all three benchmarks" (line 279) would be stronger with direct comparison to the base tokenizer on these domains.

5. **Inconsistent stance on adversarial training.** The paper motivates VQ-Transplant by noting that adversarial training is "computationally intensive" and "inherently unstable" (lines 15, 55), yet Stage II (decoder adaptation) uses the same adversarial training regime — a StyleGAN-like discriminator, DiffAug, and consistency regularization (line 101). The paper is not avoiding adversarial training; it is reducing its scale by starting from pre-trained weights. This is a reasonable approach but the framing should be precise.

### Trivial

None.

## Nice-to-Haves

- **Test with a weaker base tokenizer.** All experiments use the VAR tokenizer (near SOTA). Would VQ-Transplant work as well starting from a VQGAN with lower baseline reconstruction quality? This would strengthen claims about generality.
- **Evaluate downstream generation.** The paper focuses on reconstruction fidelity, but the ultimate use of visual tokenizers is generation. Showing that VQ-Transplant tokenizers enable good AR-based or diffusion-based generation would broaden the impact.
- **An ablation of the original VAR VQ module with larger codebook.** As noted in weakness 2, this would cleanly separate codebook-size effects from VQ-method effects.

## Removed Points

The following points from the input review were removed with justification:

- *"No statistical significance or variance reporting"* — Single-run evaluation on large-scale benchmarks is standard in this field; not a meaningful weakness.
- *"No evaluation with weaker base tokenizer"* and *"No evaluation of downstream generation"* — These are scope extensions, not faults; moved to Nice-to-Haves.
- *Section-by-section notes on specific lines* — Most are subsumed by the main weaknesses above; the individual line-level critique does not add independent information.
- *"Table 1 mixes training datasets, GPU counts, and architectures"* — This is a valid sub-point but already captured within weakness 1 above.
- *"The MMD motivation in Section 4.2 lacks analysis of loss interaction"* — A theoretical nice-to-have, not a demonstrated flaw.

## Novel Insights

None beyond the paper's own contributions. The primary novel observation from the input review is that the decoder adaptation finding is the paper's strongest evidence, which the paper already presents clearly; the critic's suggestions for re-centering the narrative are helpful framing advice rather than new analytical insights.

## Suggestions

1. **Re-center the narrative.** Drop the "21.8× faster" framing from the abstract and introduction. Present VQ-Transplant honestly: "22 GPU-hours of additional fine-tuning on top of a pre-trained encoder-decoder" rather than "22 hours vs. 60 hours." If the pre-training cost is mentioned, it should be as a one-time cost amortized across many VQ experiments, not omitted entirely.

2. **Add the missing control experiment.** Train the original VAR's native multi-scale VQ module with K=8192 and run decoder adaptation for the same 5 epochs. Report the r-FID. This single experiment would resolve whether the quality improvement comes from the larger codebook or from MMD-VQ specifically.

3. **Either strengthen or de-emphasize MMD-VQ.** If MMD-VQ is to remain a contribution, provide evidence (e.g., synthetic distribution experiments, analysis of feature distributions in the encoder) that the non-parametric MMD loss captures distributional differences that the parametric Wasserstein loss misses on these datasets. Otherwise, present it as a straightforward variant.

4. **Include the original VAR tokenizer as a baseline in cross-dataset tables** (FFHQ, CelebA-HQ, LSUN-Churches). This adds only an inference cost and would make the generalization claim much more concrete.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>