Now I have all the calibration data. Let me compile the final review.

## Summary

The paper proposes **VQ-Transplant**, a framework that enables plug-and-play replacement of VQ modules in frozen pre-trained visual tokenizers (specifically VAR), requiring only lightweight decoder adaptation (5 epochs) rather than costly end-to-end retraining. It also introduces **MMD-VQ**, a VQ variant using Maximum Mean Discrepancy for distribution alignment. Experiments across five VQ methods, two quantizer types, and four datasets demonstrate the framework's utility.

## Strengths

- **The framework design is clean and principled.** VQ-Transplant's two-stage process (VQ module substitution + decoder adaptation) follows naturally from the problem statement. Keeping the encoder frozen throughout is the obvious first approach to decoupling VQ development from full tokenizer retraining, and it is presented clearly. [draft weight: 9.04]

- **The controlled comparison against from-scratch training (Table 6) provides the cleanest evidence for the framework's value.** At matched compute budgets on ImageNet-1k (22 hours vs. 25–35 hours), VQ-Transplant achieves r-FID 0.81/0.91 while from-scratch training only reaches 1.26–1.40. This directly demonstrates that the frozen encoder-decoder provides a meaningful prior, and it is the paper's strongest result. [draft weight: 9.83]

- **The empirical evaluation is broad in scope.** Five VQ methods (Vanilla, EMA, Online, Wasserstein, MMD) × two quantizer types (multi-scale, fixed-scale) × multiple codebook sizes × four datasets (ImageNet-1k, FFHQ, CelebA-HQ, LSUN-Churches) cover both in-distribution and cross-dataset settings. [draft weight: 9.06]

## Weaknesses

### Fatal
None.

### Major

- **The headline claim comparing 0.81 r-FID vs. 0.92 r-FID is confounded by codebook size.** The paper's marquee result (abstract, introduction) states that VQ-Transplant with MMD-VAR achieves "superior reconstruction fidelity (0.81 rFID) while being 21.8× faster than training vanilla VAR (0.92 rFID)." However, the 0.81 result uses K=8192 while VAR uses K=4096. At the same codebook size (K=4096, Table 2), MMD VAR achieves 0.91 r-FID — essentially tied with VAR's 0.92 — and is *worse* on LPIPS (0.108 vs. 0.100), PSNR (24.16 vs. 24.37), and SSIM (63.2 vs. 63.9). The paper never acknowledges this confound in its narrative. At K=4096 the improvement on r-FID is marginal (0.91 vs. 0.92) and negative on other metrics; the main improvement comes from doubling the codebook, not from the method. [draft weight: 1.04]

- **MMD-VQ's claimed advantage over Wasserstein VQ is empirically unsubstantiated.** The paper motivates MMD-VQ by arguing that Wasserstein VQ's Gaussian assumption is limiting. However, across Tables 3, 5, 7, 8, 9, and 10, MMD VQ and Wasserstein VQ perform near-identically on virtually every metric and dataset. In some settings (FFHQ Table 8, Adaptation, K=32768), Wasserstein VQ actually achieves better r-FID (1.21 vs. 1.37). No diagnostic experiment is provided to demonstrate a case where MMD-VQ's non-parametric nature yields a practical advantage. Since MMD-VQ is listed as a "secondary contribution" (Section 1), this gap weakens that claim. [draft weight: -1.09]

- **The cross-dataset evaluation (Section 5.3) omits the most informative baseline.** Tables 8–10 compare VQ-Transplant methods against from-scratch baselines on FFHQ, CelebA-HQ, and LSUN-Churches. But the unmodified original VAR tokenizer evaluated directly on these datasets is absent. Since VAR was trained on OpenImages (which differs from these face/church datasets), the reported improvements from VQ-Transplant's decoder adaptation could partly reflect simple domain adaptation by the decoder rather than any property of the transplantation framework. Furthermore, the paper's claim of "exceptional cross-dataset generalization" overstates what is demonstrated — decoder adaptation is dataset-specific fine-tuning, not zero-shot generalization. [draft weight: 0.77]

### Minor

- **The 21.8× speedup claim (Table 1) conflates dataset size, GPU count, and training duration.** VAR uses OpenImages (~9M images, 16×A100, 60 hours) while VQ-Transplant uses ImageNet-1k (~1.2M images, 2×A100, 22 hours). The factor incorporates a 7.5× dataset size difference and 8× GPU count difference alongside any algorithmic efficiency. While the practical takeaway (cheaper hardware, smaller dataset) is valid, the 21.8× figure is presented without caveat. [draft weight: 3.59]

- **At matched codebook size, the metric picture is mixed and not discussed.** At K=4096 (Table 3 Adaptation), MMD VAR improves r-FID marginally (0.91 vs. 0.92) but is worse on LPIPS (0.108 vs. 0.100), PSNR (24.16 vs. 24.37), and SSIM (63.2 vs. 63.9). The paper builds its narrative around r-FID and r-IS while the metrics showing a mixed story are present in tables but never commented on. A more balanced presentation would improve credibility. [draft weight: 3.73]

- **The abstract claims "matching industry-level reconstruction performance"** but, as noted above, at matched codebook size the reconstruction is mixed (better on r-FID/r-IS, worse on LPIPS/PSNR/SSIM). This framing oversells the results. [draft weight: 2.82]

### Trivial

- **No breakdown of the 22 total training hours into Stage I vs. Stage II compute cost.** Understanding how much each stage requires would help practitioners decide whether the framework suits their resource constraints. [draft weight: 5.43]

## Nice-to-Haves

- Including the unmodified VAR tokenizer as a baseline in Tables 8–10 (cross-dataset) would strengthen the cross-domain analysis.
- A diagnostic experiment (e.g., on synthetic non-Gaussian feature distributions) showing where MMD-VQ outperforms Wasserstein VQ would substantiate the claimed advantage.

## Removed Points

- *"Multi-Gaussian kernel σ values and γ hyperparameter not specified in main text"* — Removed because the paper references Appendix A/B for implementation details; the appendix is stripped by the PDF parser and these details exist in the full submission.
- *"No generative downstream task evaluation"* — Removed because this is outside the paper's stated scope (reconstruction fidelity for tokenization). Requesting generative evaluation is a nice-to-have, not a required weakness.
- *Generic strengths about the problem being "well-motivated and practical"* — Removed as too generic to be retained as a specific, evidenced strength.

## Novel Insights

The most valuable critical insight from the review is the systematic identification of the codebook-size confound in the paper's headline claim. While the paper transparently presents all numbers in its tables, the narrative framing of "0.81 vs. 0.92 r-FID" without acknowledging the K=8192 vs. K=4096 asymmetry is a significant presentation weakness. This matters because it means the paper's central quantitative claim conflates two variables (method + codebook size), making the individual contribution of either unclear. A secondary insight is that MMD-VQ's empirical performance is indistinguishable from Wasserstein VQ across all tested settings, which undercuts the theoretical motivation and questions whether MMD-VQ should be presented as a distinct contribution.

## Suggestions

1. **Restructure the narrative to lead with the controlled comparison (Table 6)**, which cleanly demonstrates the framework's value (VQ-Transplant vs. from-scratch at matched budgets). Present the comparison against the original VAR with appropriate caveats about the codebook-size confound.
2. **Add the unmodified VAR tokenizer as a baseline in Tables 8–10** to isolate the effect of transplantation from domain adaptation in the cross-dataset setting.
3. **Either provide empirical evidence for MMD-VQ's advantage over Wasserstein VQ** (e.g., a diagnostic experiment with non-Gaussian features) or reframe MMD-VQ as a competitive alternative rather than a superior method.
4. **Discuss the trade-off between r-FID/r-IS and LPIPS/PSNR/SSIM at matched codebook sizes** to present a balanced evaluation.
5. **Add a caveat to the 21.8× speedup claim** clarifying that it incorporates differences in dataset size, GPU count, and training duration, not just algorithmic efficiency.

---

**Calibration Anchors (all retrieval rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| u1cQYxRI1H.md | 0.50 | R1 (1.5−) | No | Not topically relevant (illumination harmonization) |
| gwZ90hFSL2.md | 1.00 | R1 (1.5−) | No | Not relevant (humanoid robots/NLP) |
| P49gSPmrvN.md | 1.00 | R1 (1.5−) | No | Not relevant (scientific discourse visualization) |
| 5lUdTogEL3.md | 1.00 | R1 (1.5−) | No | Not relevant (person Re-ID) |
| IqGVIU4rvM.md | 2.50 | R1 (1.5–3.5) | Partial | VQ+diffusion tokenizer; weaker experiments, worse presentation than VQ-Transplant |
| vK8C37eHXM.md | 3.20 | R1 (1.5–3.5) | No | Autoencoder+diffusion; tangentially related |
| TDzAqTqDHV.md | 3.00 | R1 (1.5–3.5) | No | Quantized codebooks for retrieval; different task |
| lvgsPjRtLM.md | 2.50 | R1 (1.5–3.5) | No | Video generation; tangentially related |
| YlWvQSBCgl.md | 4.00 | R1 (3.5–5.5) | No | Channel-wise quantization; similar topic, less broad experiments |
| 7X2BFPl18T.md | 4.75 | R1 (3.5–5.5) | No | Bit-level scaling laws; similar evaluation methodology |
| sfTsvy05MX.md | 4.75 | R1 (3.5–5.5) | **Yes** | LL-VQ-VAE: similar VQ-improvement paper; rejected due to missing generative evaluation and questionable loss term. VQ-Transplant has broader experiments and stronger practical motivation |
| nS2DBNydCC.md | 4.75 | R2 (4.0–6.5) | **Yes** | Wasserstein VQ paper: closest comparator — also addresses distribution matching for VQ. Rejected with concerns about marginal improvements and limited novelty. VQ-Transplant has a more practical framework contribution |
| ZVe2k7mNAP.md | 4.50 | R2 (4.0–6.5) | No | MQ-VAE: meta-learning for VQ; related but different approach |
| iqqpx8hgSQ.md | 5.50 | R2 (4.0–6.5) | No | RAQ-VAE: rate-adaptive VQ; similar scope, different method |
| 49Tn5mfTy5.md | 5.00 | R2 (4.0–6.5) | No | Uncertainty quantification; only tangentially related |
| UN94vDiaJv.md | 5.50 | R2 (4.0–6.5) | No | Information-theoretic analysis of VQ-VAE; theoretical, not directly comparable |
| mb2ryuZ3wz.md | 5.75 | R1 (5.5–7.5) | No | Variable-length tokens; stronger execution but different focus |
| yGnsH3gQ6U.md | 5.75 | R1 (5.5–7.5) | **Yes** | BSQ-ViT: stronger VQ paper with cleaner method, accepted. VQ-Transplant is less polished but addresses a complementary problem |
| QE1LFzXQPL.md | 6.25 | R1 (5.5–7.5) | **Yes** | ImageFolder: accepted tokenizer paper; strong execution, broader downstream validation |
| 8ROIRnKloJ.md | 5.67 | R1 (5.5–7.5) | No | ε-VAE: denoising as decoding; different approach |
| GMwRl2e9Y1.md | 8.00 | R1 (7.5–8.5) | **Yes** | Rotation Trick: strong VQ improvement paper with principled contribution and extensive validation |
| FlvtjAB0gl.md | 6.25 | R2 (4.0–6.5) | No | Unified language-vision pretraining; different focus |
| 0Nui91LBQS.md | 6.33 | R2 (4.0–6.5) | No | SEED tokenizer; different focus (multimodal LLM) |
| 3TnLGGHhNx.md | 6.00 | R2 (4.0–6.5) | No | BPE image tokenizer; different focus |
| n64NYyc6rQ.md | 6.20 | R2 (4.0–6.5) | No | Semantic-equivalent tokenizer; different focus |

**Score placement rationale:** The closest anchors are the Wasserstein VQ paper (4.75, rejected) and LL-VQ-VAE (4.75, rejected). VQ-Transplant is stronger than both: it has a clearer practical motivation, broader experiments, and its core contribution (the framework) is more novel than "add a Wasserstein loss to VQ" or "use a lattice." However, the VQ-Transplant paper shares the same genre of weaknesses — overclaimed results, a secondary contribution that is not properly validated, and selective metric reporting. The Wasserstein VQ paper's most negatively weighted weakness was -4.32 (limited innovation); my draft's most negative is -1.09 (MMD-VQ unsubstantiated). On the upper end, BSQ-ViT (5.75, accepted) is clearly stronger: cleaner methodological contribution, well-polished presentation, and downstream validation. VQ-Transplant sits between these bands.

**Round 1 bracket:** [4.75, 5.75] — narrowed from the band between Wasserstein VQ (4.75) and BSQ-ViT (5.75). **Final:** 5.0, acknowledging that the core framework idea is sound and the Table 6 comparison is genuinely informative, but the presentation overclaims and the secondary MMD-VQ contribution is unsupported.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>