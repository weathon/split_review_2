Now let me read the remaining sections to check for any additional details about LDM-16 or appendix mentions.Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me do calibration Round 1 — Bracketing:Let me read a few of the most relevant anchor papers for calibration.Now I have solid anchors for calibration. Let me form my bracket:

**Round 1 bracket:** Based on the anchors:
- IqGVIU4rvM (avg 2.50): Much weaker paper with fundamental design issues. VQ-Transplant is clearly better.
- sfTsvy05MX (LL-VQ-VAE, avg 4.75): Rejected primarily for "only evaluated on reconstruction, which is not the point of discretization" — the **exact same critique** applicable to VQ-Transplant. However, VQ-Transplant is better motivated, more comprehensive, and has a clearer practical contribution.
- YlWvQSBCgl (avg 4.00): Rejected for unfair comparisons and fundamental approach concerns. VQ-Transplant is stronger.
- 8ishA3LxN8 (FSQ, avg 6.50): Accepted. Simpler proposal validated across multiple tasks **including generation**. VQ-Transplant is narrower in scope with no generation validation.

**Initial bracket: 4.5 – 6.0**

The paper sits above the LL-VQ-VAE (4.75) due to stronger practical motivation and more comprehensive reconstruction experiments, but below FSQ (6.50) which validated on downstream generation and multiple tasks.

Now let me finalize the review.Now I have everything needed to write the final consolidated review.

---

## Summary
VQ-Transplant proposes a two-stage framework for cheaply replacing VQ modules in pre-trained visual tokenizers without end-to-end retraining. Stage I substitutes the VQ module while freezing encoder/decoder parameters; Stage II performs lightweight decoder adaptation (5 epochs with adversarial training) to resolve decoder-quantizer distributional mismatch. A secondary contribution is MMD-VQ, which uses maximum mean discrepancy for distribution-aligned codebook learning. The framework achieves 0.81 r-FID on ImageNet-1K at ~22 GPU-hours compared to VAR's ~960 GPU-hours.

## Strengths

- **Concrete cost quantification and convincing from-scratch comparison.** Table 1 quantifies the training cost of existing tokenizers (VAR: 960 GPU-hours, UniTok: 12,800 GPU-hours) against VQ-Transplant's 44 GPU-hours. Table 6 directly compares VQ-Transplant (22 hours, 0.91 r-FID at K=4096) against from-scratch MMD VAR training (35 hours, 1.34 r-FID), demonstrating that the advantage comes from leveraging the pre-trained decoder's priors, not merely clock-time savings.

- **Comprehensive reconstruction evaluation across settings.** Five VQ algorithms tested in both multi-scale (Table 3) and fixed-scale (Table 7) configurations, cross-dataset generalization on FFHQ, CelebA-HQ, and LSUN-Churches (Tables 8–10), and progression analysis across 20 adaptation epochs (Table 5, Figure 3). The consistent patterns across settings strengthen confidence in the framework's robustness.

- **Well-motivated two-stage decomposition.** The empirical observation that lower quantization error does not automatically translate to better reconstruction (e.g., MMD VAR achieves 0.255 quantization error vs VAR's 0.283, yet r-FID after substitution alone is 1.52 vs 0.92 in Table 3) provides clear evidence for the necessity of decoder adaptation and gives the framework principled justification.

## Weaknesses

### Fatal
None.

### Major

- **No downstream generation evaluation.** The paper's stated motivation is enabling VQ research for generative models — the abstract references "cutting-edge VQ techniques" and the introduction frames the problem around "visual generation" (Section 1, first paragraph). Yet all evaluation is reconstruction-only (r-FID, PSNR, SSIM, LPIPS, r-IS). A transplanted VQ module that achieves good reconstruction could still degrade generation quality if the resulting token distribution has different entropy or inter-token dependencies incompatible with an autoregressive prior. This gap between claimed application and evaluated scope is significant: the paper validates only the reconstruction half of the pipeline it claims to enable.

- **Narrow architecture validation undermines generality claims.** The entire main paper validates on a single pre-trained tokenizer: VAR (Tian et al., 2024). The LDM-16 experiment (Section 5.1, line 269) is relegated to the appendix and shows "lower adaptability… particularly with respect to r-FID and r-IS metrics." Claiming a general "plug-and-play integration framework" based primarily on one architecture — whose multi-scale design may be uniquely compatible with module substitution — overreaches the evidence provided.

### Minor

- **MMD-VQ shows inconsistent advantage over Wasserstein VQ.** While the theoretical argument against Gaussian assumptions is sound (Section 4.2), the empirical evidence does not demonstrate consistent superiority. On ImageNet multi-scale (Table 3), MMD VAR edges out Wasserstein VAR (0.81 vs 0.83 r-FID at K=8192), but on FFHQ (Table 8), Wasserstein VQ substantially outperforms MMD VQ (1.21 vs 1.37 r-FID at K=32768), and similarly on Churches (Table 10: 1.79 vs 1.87). The secondary contribution is incremental over its closest predecessor.

- **Per-dataset decoder adaptation partially undercuts "plug-and-play" framing.** In cross-dataset experiments (Tables 8–10), decoder adaptation is performed separately on each target dataset. This means the framework requires per-domain fine-tuning rather than a single adaptation that transfers, which limits the practical convenience implied by "plug-and-play."

- **Narrative tension around adversarial training.** The paper frames adversarial training instability as a key motivation (Section 1: "adversarial training is inherently unstable"), yet Stage II employs adversarial training with a discriminator (Eq. 4). The likely explanation — that the decoder is initialized near a good solution, making the landscape benign for 5 epochs — is never stated, leaving a tension in the paper's framing.

- **Fixed-scale VQ sub-vector design introduces confounding capacity.** The fixed-scale implementation (Section 5, experiment setup) splits 32-dimensional features into two 16-dimensional sub-vectors quantized with independent codebooks. This effectively doubles codebook capacity compared to single-codebook methods, which is not discussed and complicates comparisons between multi-scale and fixed-scale results.

### Trivial
None.

## Nice-to-Haves
- A single ImageNet-adapted decoder that transfers to FFHQ/CelebA-HQ/Churches without per-dataset retraining would more convincingly demonstrate "plug-and-play" utility.
- Deeper analysis of what architectural properties make a pre-trained tokenizer amenable to transplantation (why VAR works well, why LDM-16 works less well) would guide practitioners.
- Analysis of why different VQ methods produce different magnitudes of decoder-quantization mismatch after Stage I would make the framework more principled.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"95% cost reduction claim is misleading"**: Table 1 clearly shows the comparison is between VQ-Transplant's cost and the cost of training each full tokenizer. The framing is fair within the paper's stated scope — the pre-trained tokenizer is a prerequisite, not a claim of the paper. Removed as not a real weakness.

- **Token count mismatch in Table 2 (MMD VQ 512 tokens vs VQGAN-LC 256 tokens)**: While this comparison is not perfectly matched, the paper also shows the fair comparison: MMD VAR (680 tokens) vs VAR (680 tokens) in the same table, demonstrating genuine improvement (0.81 vs 0.92 r-FID). The table structure makes both comparisons visible. Removed as the paper provides the controlled comparison.

## Novel Insights
The empirical finding that lower quantization error does not automatically yield better reconstruction quality — demonstrated consistently across five VQ methods in both multi-scale and fixed-scale settings (Tables 3 and 7) — is a useful observation for the VQ community. It suggests that the decoder's learned feature priors create a distributional coupling that cannot be resolved by improving quantization alone, motivating the decoder adaptation stage as a necessary component of any module-substitution approach.

## Suggestions
- Add at least one downstream generation experiment: take an autoregressive model trained on the original VAR codebook, retrain/fine-tune it on the transplanted codebook, and report generation FID. Even negative results would clarify the framework's practical scope.
- Promote the LDM-16 results from the appendix into the main text, or validate on a second architecturally distinct tokenizer (e.g., a standard single-scale VQGAN), to substantiate generality claims.
- Explicitly state why 5-epoch adversarial training in Stage II is stable (near-optimal initialization hypothesis) to resolve the narrative tension with the motivation.
- Discuss the doubled codebook capacity in fixed-scale experiments and its implications for fair comparison.

## Score and Decision

### Calibration Anchors

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| IqGVIU4rvM (VQ-VAE + Diffusion Tokenizers) | 2.50 | 1 | Much weaker: overcomplicated, poor motivation. VQ-Transplant is clearly better. |
| gwZ90hFSL2 (Cross-Lingual Humanoid Robots) | 1.00 | 1 | Not topically relevant; used as low-score anchor only. |
| 5lUdTogEL3 (Lifelong Person ReID) | 1.00 | 1 | Not topically relevant; low-score anchor. |
| P49gSPmrvN (Scientific Discourse UMAP) | 1.00 | 1 | Not topically relevant; low-score anchor. |
| TDzAqTqDHV (Quantised Codebooks for Retrieval) | 3.00 | 1 | Different domain (text retrieval); VQ-Transplant is better scoped. |
| 6Mdvq0bPyG (EfficientQAT) | 3.00 | 1 | Different domain (LLM quantization); rejected for limited novelty. |
| 2HdZPEQUig (Object-Centric Videos) | 3.00 | 1 | Different domain. |
| tNxr38vfYR (Victor Visual Token Registers) | 5.00 | 1 | Token compression for VLMs; similar scope issue of limited downstream validation. |
| YlWvQSBCgl (Channel-wise Quantization) | 4.00 | 1 | VQ paper rejected for unfair comparisons and fundamental approach concerns. VQ-Transplant is better executed. |
| ym1dS37mZE (Visual Token Grouping) | 4.67 | 1 | Similar scope limitation. VQ-Transplant is comparable. |
| sfTsvy05MX (LL-VQ-VAE) | 4.75 | 1 | **Key anchor.** Rejected primarily for "only evaluated on reconstruction, not generation" — the exact same weakness as VQ-Transplant. But VQ-Transplant is better motivated and more comprehensive. |
| HYyRwm367m (Neural Language of Thought) | 6.50 | 1 | VQ-based, but includes generation evaluation. VQ-Transplant lacks this. |
| 8ishA3LxN8 (FSQ: VQ-VAE Made Simple) | 6.50 | 1 | **Key anchor.** Simpler VQ replacement validated on multiple tasks **including generation**. VQ-Transplant is narrower and lacks generation evidence. |
| wryFCrWB0A (DnD-Transformer) | 6.20 | 1 | Includes generation results; accepted. More complete evaluation than VQ-Transplant. |
| 8ROIRnKloJ (ε-VAE) | 5.67 | 1 | Evaluates both reconstruction and generation. Mixed reviews but more complete. |
| 2dnO3LLiJ1 (ViT Registers) | 8.00 | 1 | Much stronger, broadly validated contribution. Not directly comparable. |

**Round-1 bracket: 4.5 – 6.0**

**Narrowing rationale:** VQ-Transplant is clearly above LL-VQ-VAE (4.75) — it has stronger practical motivation, more comprehensive experiments, and the from-scratch comparison is compelling. However, it falls short of FSQ (6.50) and ε-VAE (5.67), both of which validate on downstream generation. The missing generation evaluation is the exact weakness that sank LL-VQ-VAE; VQ-Transplant partially mitigates this through much stronger reconstruction experiments and clear practical value, but doesn't fully escape it. The single-architecture validation compounds this concern.

The paper is a competent engineering contribution that addresses a real practical need. The reconstruction evaluation is thorough and convincing. But the gap between the generative-modeling framing and reconstruction-only evidence, combined with single-architecture validation, places it at the borderline. I settle at **5.0** — above the rejected VQ papers with similar scope issues, but below accepted papers that close the loop to generation.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>