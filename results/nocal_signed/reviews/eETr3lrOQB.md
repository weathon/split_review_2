Now I have a thorough understanding of the paper. Let me produce the final consolidated review.

---

## Summary

This paper proposes VQ-Transplant, a framework that enables plug-and-play replacement of vector quantization (VQ) modules in pretrained visual tokenizers without costly end-to-end retraining. The method works in two stages: (1) substituting the VQ module while keeping the encoder-decoder frozen, and (2) lightweight decoder adaptation (5 epochs) to realign the decoder with the new quantized space. A secondary contribution, MMD-VQ, uses maximum mean discrepancy for distributional alignment between features and codebook. The paper demonstrates substantial computational savings (21.8× vs. full VAR training) and shows that VQ-Transplant can approach or match the reconstruction quality of the original model at a fraction of the cost.

## Strengths

- **A practically motivated problem, clearly stated.** The paper correctly identifies that developing novel VQ algorithms requires end-to-end adversarial training of encoder-decoder architectures, which imposes a prohibitive compute barrier. The idea of reusing a pretrained encoder-decoder and substituting only the VQ module addresses a real bottleneck in the research workflow.

- **The two-stage procedure is clean and well-specified.** Stage I (VQ module substitution with a standard VQ loss plus an auxiliary uniqueness/distance loss) and Stage II (lightweight decoder adaptation using the standard VQGAN composite loss) are clearly described in Section 4.1. The framework is simple enough that it could be readily adopted by other researchers.

- **Computational savings are genuine and well-documented.** The framework requires 44 GPU-hours (2×A100, 22h) vs. 960 GPU-hours for full VAR training (16×A100, 60h) — a real reduction that could enable researchers with modest budgets to iterate on VQ designs.

- **Consistent experimental pattern across multiple VQ variants.** The paper evaluates five quantization algorithms (vanilla, EMA, online, Wasserstein, MMD) under the same framework on both multi-scale and fixed-scale settings, and the pattern holds: distributional alignment methods outperform simpler approaches, and decoder adaptation consistently improves results.

## Weaknesses

### Fatal
None.

### Major

- **Headline claim of "superior" reconstruction confounds codebook size with method quality.** The paper repeatedly claims that VQ-Transplant achieves "superior" reconstruction (0.81 r-FID) vs. original VAR (0.92 r-FID), but this comparison uses different codebook sizes (K=8192 vs. K=4096). Doubling the codebook is a free-lunch parameter change that would improve any quantization method. At the same codebook size (K=4096), the improvement is marginal: MMD VAR achieves 0.91 r-FID vs. original VAR's 0.92 (Table 3). This 0.01 difference is not shown to be statistically significant. The paper should present the K=4096 comparison as the primary result (demonstrating comparable quality at greatly reduced cost) and frame the K=8192 result as an additional benefit of the framework's efficiency — not as evidence of intrinsic superiority.

- **Secondary contribution MMD-VQ does not clearly outperform existing Wasserstein VQ.** MMD-VQ is presented as the paper's secondary contribution, "specifically designed to enable improved compatibility with VQ-Transplant." However, across Tables 3, 7, 8, 9, and 10, MMD-VQ and Wasserstein VQ produce essentially tied results. In the multi-scale setting at K=4096 (Table 3), MMD VAR achieves 0.91 r-FID and Wasserstein VAR achieves 0.93. On FFHQ (Table 8), Wasserstein VQ actually achieves the best r-FID (1.21 vs. 1.37 for MMD VQ). The paper claims MMD-VQ avoids Gaussian assumptions of Wasserstein VQ, but the empirical evidence does not demonstrate a meaningful advantage. This does not harm the primary VQ-Transplant contribution, but it means MMD-VQ should be presented as an equivalent nonparametric alternative rather than a superior method.

- **Baseline comparisons in Table 2 conflate different token counts.** VQ-Transplant variants use 512 or 680 tokens, while most baselines (DQVAE, DiVAE, VQGAN variants, Llama GEN) use only 256 tokens. More tokens naturally improve reconstruction fidelity. The only baseline with a comparable token count (original VAR at 680 tokens) is compared with a confounded codebook size (see above). The paper's claim that MMD VQ "outperform[s] competing baselines" is inflated when token counts are unequal.

### Minor

- **Cross-dataset comparisons (Tables 8–10) are confounded by the pretrained backbone advantage.** VQ-Transplant initializes from a heavily pretrained VAR encoder-decoder (trained on OpenImages) and adapts the decoder for 5 epochs on the target dataset. The baselines (VQGAN, RQVAE, etc.) were trained from scratch on the target dataset. A controlled baseline — fine-tuning the original VAR decoder on the target dataset without swapping the VQ module — is needed to isolate the effect of the transplant from the value of the pretrained backbone.

- **No variance or statistical significance reported.** The r-FID values are reported as point estimates. Given that the differences between methods are often small (e.g., 0.91 vs. 0.92, 1.05 vs. 1.04), standard deviations across multiple runs are needed to assess whether these differences are meaningful.

### Trivial
- **"Speedup" column in Table 1 is unclearly labeled.** The column computes (method's GPU-hours) / (VQ-Transplant's GPU-hours) and calls it "Speedup," but the denominator is not explicit. A label like "GPU-hour Ratio vs. Ours" would be clearer.

## Nice-to-Haves

- **Downstream generation validation.** The paper motivates VQ-Transplant as supporting downstream generative modeling. Showing that images tokenized with transplanted VQ work well in a generative model (e.g., VAR's autoregressive transformer) would substantially strengthen the contribution. Reconstruction r-FID alone does not guarantee that the discrete codes preserve the structure needed for generation.
- **A controlled baseline for cross-dataset experiments.** Fine-tune the original VAR decoder (with its native VQ) on FFHQ for 5 epochs and compare against the VQ-Transplant result to isolate the effect of the VQ swap from the pretrained backbone.

## Removed Points

These points were raised by reviewers but are removed per consolidation rules:

1. **LDM-16 results deferred to appendix.** The paper notes that VQ-Transplant achieves "reasonable performance on LDM-16" and defers details to Appendix D. Since the parser strips appendices from all papers and they exist in the original submission, this criticism is removed.
2. **"No downstream generation results" — framed as a missing evaluation.** This is a reasonable extension but the paper's scope is visual tokenization, where reconstruction fidelity is the standard evaluation metric. Demoted to Nice-to-Have.
3. **Table 1 speedups for Llama GEN, ImageFolder, UniTok "included without being discussed."** These are clearly presented in a comparison table; the context is self-explanatory. Removed as a non-issue.
4. **Question about L_unique for vanilla VQ methods.** The paper states L_unique is "e.g., Wasserstein loss for Wasserstein VQ." For methods where no such loss applies, it is implicitly zero. This is a minor clarification, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Restructure the headline comparison: present the K=4096 result (0.91 vs. 0.92) as the direct method comparison (demonstrating comparable quality at 21.8× lower cost), and frame the K=8192 result (0.81) as an additional benefit of the framework's ability to use larger codebooks cheaply.
2. Add a controlled baseline for cross-dataset experiments (fine-tune original VAR decoder on target data without VQ swap).
3. Report variance across multiple runs for key r-FID comparisons where differences are small.
4. Either provide stronger evidence that MMD-VQ outperforms Wasserstein VQ, or reframe MMD-VQ as an equivalent but nonparametric alternative.

## Score and Decision

The VQ-Transplant framework addresses a real and well-motivated problem, the two-stage procedure is clean, and the computational savings are genuinely impressive (21.8× reduction). The paper's core thesis — that you can swap VQ modules at a fraction of the cost — is supported by the evidence.

However, the paper systematically overstates its findings. The headline "0.81 r-FID vs. 0.92" comparison uses a doubled codebook size, and at equal codebook size the improvement is a marginal 0.91 vs. 0.92. The secondary MMD-VQ contribution is empirically indistinguishable from the existing Wasserstein VQ baseline. Baseline comparisons in Table 2 are confounded by unequal token counts. These issues do not invalidate the primary contribution, but they mean the paper as written does not accurately represent what was demonstrated.

With honest reframing (comparable quality at greatly reduced cost, rather than superior quality), VQ-Transplant would be a solid contribution. In its current form, the overclaiming is significant enough that it warrants rejection with a clear path to revision.

**MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>**