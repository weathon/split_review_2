Now I have sufficient calibration data. Let me compile the final review.

## Summary

The paper proposes **VQ-Transplant**, a framework that replaces the VQ module in a pre-trained discrete visual tokenizer (e.g., VAR) with a new VQ module while keeping the encoder-decoder frozen, followed by a lightweight decoder adaptation stage (5 epochs). This avoids costly end-to-end retraining — reducing from 960 GPU-hours to 44 GPU-hours. The paper also introduces **MMD-VQ**, a distribution-matching quantization method using maximum mean discrepancy. Experiments across five VQ methods, two quantization schemes, multiple codebook sizes, and three cross-dataset evaluations show the framework can achieve competitive reconstruction fidelity at a fraction of the training cost.

## Strengths

- **The core idea is well-motivated and practically useful.** Training VQ-based tokenizers with adversarial training is prohibitively expensive (960 GPU-hours for VAR). Swapping VQ modules in a frozen encoder-decoder and doing lightweight decoder adaptation is a sensible approach that can democratize VQ research for resource-constrained groups. (weight: +3.40)

- **The two-stage design is clean and convincingly demonstrated.** The gap between "VQ Module Substitution" and "Decoder Adaptation" (Table 3) clearly establishes the mismatch problem, and the r-FID progression across epochs (Table 4) confirms that lightweight decoder fine-tuning is sufficient to close the gap. This is the paper's strongest empirical contribution. (weight: +5.73)

- **Comprehensive evaluation across VQ methods, schemes, and datasets.** The paper tests five VQ algorithms (Vanilla, EMA, Online, Wasserstein, MMD) in both multi-scale and fixed-scale configurations with multiple codebook sizes on ImageNet-1k, plus cross-dataset validation on FFHQ, CelebA-HQ, and LSUN-Churches (Tables 8–10). This provides a thorough characterization of the framework's generality. (weight: +3.51)

- **The computational savings are substantial.** Reducing from 960 GPU-hours (VAR) to 44 GPU-hours (VQ-Transplant) while achieving competitive or better r-FID is a meaningful efficiency gain. (weight: +4.57)

## Weaknesses

### Fatal
None.

### Major

- **The headline improvement over the native VAR tokenizer is marginal and conflates VQ method change with codebook size change.** The paper's best result (r-FID 0.81, Table 2) compares MMD VAR at K=8192 against the original VAR at K=4096 — changing both VQ method and codebook size simultaneously. At the same codebook size (K=4096, Table 3), MMD VAR achieves r-FID 0.91 vs the original VAR's 0.92 — a 0.01 difference. On other metrics the original VAR still leads: LPIPS (0.100 vs 0.108), SSIM (63.9 vs 63.2), PSNR (24.37 vs 24.16). The "state-of-the-art reconstruction fidelity" claim is supported against the broader field (e.g., RQVAE, VQGAN) but oversells the improvement over the direct VAR baseline. (weight: -5.92)

- **MMD-VQ's improvement over Wasserstein VQ is marginal and inconsistent.** Across Tables 3, 7, 8, 9, and 10, differences between MMD and Wasserstein VQ are typically within 0.01–0.02 r-FID, and Wasserstein VQ wins on several settings (e.g., FFHQ Adaptation K=32768: Wasserstein 1.21 vs MMD 1.37). No variance or significance estimates are reported, so it is unclear whether the tiny differences are meaningful. Since MMD-VQ is presented as a distinct contribution (Section 4.2), this weakens the novelty claim. (weight: -5.01)

- **No evaluation on downstream generation tasks.** Discrete visual tokenizers exist primarily to serve as the representation layer for autoregressive image generation and other generative models. After transplanting a new VQ module and adapting the decoder, the latent space differs from the original tokenizer's. The paper provides no evidence that a generative model can produce good samples using the transplanted tokenizer. Given that VAR is fundamentally a generative architecture, and the paper's framing emphasizes "industry-level models like VAR," this is a significant omission. (weight: -4.32)

### Minor

- **The cross-dataset comparisons (Tables 8–10) give VQ-Transplant an advantage not controlled for.** The baselines (RQVAE, VQGAN, etc.) were trained from scratch on each target dataset, while VQ-Transplant starts from a model pre-trained on OpenImages (a superset of ImageNet-1k). This transfer-learning advantage makes the "state-of-the-art" cross-dataset claim less clean. A fairer comparison would either train baselines with the same pre-training or restrict VQ-Transplant to the same starting point. (weight: -1.55)

### Trivial

- **Equation (3) under-specifies the VQ loss for module substitution.** It shows only the codebook loss term ‖sg(zₑ) − z_q(φ)‖²₂ plus the uniqueness loss, without the commitment loss term ‖sg(z_q) − z_e‖²₂ that is standard in VQVAE training and shown in Equation (2). This is a minor specification gap. (weight: -2.88)

## Nice-to-Haves

- Downstream generation experiments (e.g., training an autoregressive transformer on the transplanted tokenizer's codes) would transform the contribution from reconstruction proxy to generation evidence.
- A controlled comparison at matched codebook size and token count between MMD VAR and the original VAR would clarify the method's actual improvement.
- Variance or confidence intervals would help assess whether the small MMD-vs-Wasserstein differences are meaningful.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Table 6 from-scratch comparison is a strawman": REMOVED.** The paper itself acknowledges (line 265) that discrete tokenizers need hundreds of epochs. The comparison shows that even with *more* training time (25–35 hours vs 22 hours), from-scratch training cannot match VQ-Transplant's quality. This is a valid fixed-budget efficiency demonstration, not a deceptive comparison.

- **"95% cost reduction claim is misleading": REMOVED.** The paper clearly specifies it uses a "pre-trained VAR tokenizer" (line 28). The cost savings relative to full retraining is standard framing for transfer-learning/fine-tuning papers. The model's weight for this item was positive (+1.21), confirming it is not a genuine weakness.

- **"SOTA claim not supported due to token count mismatch": MERGED** into the first major weakness (the problematic comparison is specifically against VAR at K=4096, not against the broader field where MMD VQ at 512 tokens beats RQVAE at 1024 tokens, r-FID 0.86 vs 1.83).

- **Section-by-section notes about motivation, missing empirical Gaussian-failure demonstration, etc.: REMOVED** as these are either scope-creep demands or generic observations that don't threaten the paper's core value.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. For the key comparison with VAR, control for codebook size (compare K=4096 vs K=4096, not K=8192 vs K=4096) or explicitly decompose the effect of codebook size vs VQ method.
2. Add a downstream generation experiment — e.g., finetune the existing VAR generator on the transplanted tokenizer's codes and report generation FID.
3. Report variance or confidence intervals for the MMD-vs-Wasserstein comparisons.
4. In cross-dataset tables, clearly label the comparison as "transfer learning" vs from-scratch rather than implying a matched head-to-head.
5. Consider deemphasizing MMD-VQ as a separate contribution; the framework's value is already demonstrated by the consistent improvement across all five VQ methods.

## Score and Decision

**Calibration Anchors (all rounds):**

| Anchor Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| nS2DBNydCC.md (Wasserstein VQ paper) | 4.75 | R1 | Yes | Similar topic (distribution-matching VQ), similar weaknesses about limited practical impact and marginal improvement, but poorer writing quality and more fundamental issues |
| sfTsvy05MX.md (LL-VQ-VAE) | 4.75 | R1 | Yes | Similar "reconstruction only, no downstream" weakness (weight -5.14), but had suspicious loss formulation (-5.38) and poor writing (-8.46) that our paper doesn't have |
| yGnsH3gQ6U.md (BSQ-ViT) | 5.75 | R1/R2 | Yes | Stronger novelty (+7.80 weight), extensive downstream generation evaluation. Our paper's top strength is +5.73 vs BSQ's +7.80 |
| GMwRl2e9Y1.md (Rotation Trick) | 8.00 | R1 | Yes | Exceptional paper with no fatal weaknesses. Our paper doesn't approach this tier |
| CP6CAqxAGJ.md (UnifyVocab) | 5.67 | R2 | Yes | Parallel "swap-module + adapt" paradigm. Our paper has stronger top strength (+5.73 vs +3.58) but worse top weakness (-5.92 vs -5.24) |

**Bracket after Round 1:** 4.5 – 5.75 (between the Wasserstein VQ paper at 4.75 and BSQ-ViT at 5.75)

**Narrowing:** Comparing weighted items: our paper shares the "no downstream generation" weakness with the 4.75-tier papers (weight -4.32 vs -5.14) but has a stronger top strength (+5.73 vs +4.50–5.27) and lacks any fatal/structural issues (-9+ weights). Our paper is weaker than the 5.75-tier BSQ paper which has novelty weight +7.80 and no comparably heavy negatives. The UnifyVocab anchor at 5.67 has a more balanced profile (no -5+ weakness). Given our paper's -5.92 and -5.01 weights — both stronger negatives than any single negative in the 5.67 anchor — a slightly lower score is warranted.

**Final score:** 5.0 — between reject and borderline accept. The core VQ-Transplant idea is sound and practically useful, and the paper provides a thorough empirical characterization. However, the overclaimed comparisons (conflating method and codebook size changes), marginal MMD-VQ contribution, and lack of downstream generation evidence prevent a higher score.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>