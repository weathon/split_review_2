Now I'll write the final consolidated review.

## Summary

This paper proposes VQ-Transplant, a framework that enables plug-and-play replacement of VQ modules in pre-trained visual tokenizers (e.g., VAR) without full end-to-end retraining. Stage I substitutes the VQ module with a frozen encoder-decoder; Stage II performs lightweight decoder adaptation (5–20 epochs) to resolve distributional mismatch. The paper also introduces MMD-VQ, a distribution-aligned quantization method using Maximum Mean Discrepancy. Experiments across five VQ methods, multiple codebook sizes, and three cross-dataset settings validate the framework's effectiveness for reconstruction.

## Strengths

- **Practically motivated and clearly designed.** The VQ-Transplant framework directly addresses a real bottleneck — VQ research is gated by the cost of end-to-end adversarial training. The two-stage design (substitution + decoder adaptation) is well-described and the experimental savings (22 hours on 2×A100) are meaningful.
- **Thorough ablation across VQ methods and codebook sizes.** The paper evaluates five VQ algorithms (Vanilla, EMA, Online, Wasserstein, MMD) under both multi-scale and fixed-scale configurations, multiple codebook sizes (4096–65536), and both substitution and adaptation stages (Tables 3, 7). This level of detail is valuable for practitioners.
- **Cross-dataset generalization validation (Section 5.3).** Evaluation on FFHQ, CelebA-HQ, and LSUN-Churches demonstrates that VQ-Transplant generalizes beyond ImageNet-1k to structurally distinct domains, strengthening the case for practical applicability.

## Weaknesses

### Major

- **Inflated efficiency claims.** The headline "21.8× speedup" and "95% cost reduction" are computed across confounded settings: VAR was trained on OpenImages with 16×A100 GPUs for 60 hours, while VQ-Transplant was evaluated on ImageNet-1k with 2×A100 GPUs for 22 hours (Table 1). The calculation conflates dataset size, GPU count, and training scope (full end-to-end vs. decoder-only fine-tuning). The cost of pre-training the base VAR tokenizer is also excluded. The individual parameters are disclosed in the table, but the framing presents the comparison as a direct speedup, which overstates the true advantage. The claims should be reframed as the cost of VQ module integration given an existing pre-trained model.

### Minor

- **MMD-VQ's advantage over Wasserstein VQ is inconsistent.** The paper presents MMD-VQ as a secondary contribution that improves upon Wasserstein VQ, but the experimental evidence is mixed. On FFHQ (Table 8) and LSUN-Churches (Table 10), Wasserstein VQ outperforms MMD VQ (e.g., 1.21 vs. 1.37 r-FID on FFHQ at K=32768; 1.79 vs. 1.87 r-FID on Churches). On ImageNet, the margins are tiny (0.01–0.02 r-FID) and within noise range. The theoretical advantage (nonparametric alignment) is not empirically validated — the paper never examines whether feature distributions are actually non-Gaussian or shows a case where this matters.
- **Table 2 mixes incomparable baselines.** The claim that VQ-Transplant "outperform[s] competing baselines" (line 125) is based on comparisons against methods trained from scratch under different token counts, training budgets, and architectures. While reference comparisons are common, the framing overstates what the experimental design can support. These should be labeled as reference numbers from prior work, not directly comparable.
- **Adversarial training is criticized but retained.** The paper frames adversarial training as "computationally intensive" and "prone to optimization instability" (Section 2), yet Stage II of VQ-Transplant (Eq. 4) uses the same adversarial losses (hinge GAN, DINO-S discriminator, DiffAug, consistency regularization, LeCAM). The paper should acknowledge that VQ-Transplant reduces the *scope* of adversarial training (decoder-only) rather than eliminating it.
- **Missing error bars for close comparisons.** The margins between MMD and Wasserstein VQ are often ≤0.02 r-FID. Without variance estimates or multiple-seed experiments, it is unclear whether the observed differences are meaningful.

### Trivial

- **Misleading loss term name.** $\mathcal{L}_{\text{unique}}$ in Eq. (3) is used for distribution-matching losses (Wasserstein loss, MMD), not for enforcing uniqueness. Renaming to $\mathcal{L}_{\text{align}}$ would be clearer.

## Nice-to-Haves

- Downstream generation evaluation (e.g., class-conditional image generation with the transplanted tokenizer) would strengthen the claim that the new latent spaces are suitable for generative modeling.
- An ablation of MMD's kernel bandwidth selection would help assess sensitivity, though this may be in the stripped appendix.

## Removed Points

These points were flagged for removal; treat them with caution:

- "Table 6 from-scratch comparison runs only 5–7 epochs" — The paper transparently acknowledges this limitation ("discrete tokenizers typically require hundreds of epochs"). This is a stated limitation, not a flaw.
- "No downstream generative evaluation" — Out of scope for a tokenizer reconstruction paper; standard VQ papers are evaluated on reconstruction.
- "Democratization claim is conditional on pre-trained tokenizers" — The paper repeatedly and clearly scopes itself to pre-trained tokenizers (abstract, lines 28, 83). This is adequately acknowledged.
- "Demands analysis of MMD kernel sensitivity" — May be in the stripped appendix; not verifiable.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the efficiency comparison.** Present VQ-Transplant's cost as a plain statement (22 hours on 2×A90 on ImageNet-1k) and separately ablate each confounding factor (dataset size, GPU count, training scope). Add a controlled comparison holding dataset and GPU configuration constant.
2. **Acknowledge Wasserstein VQ as a peer.** Present MMD-VQ as an alternative variant of distribution-aligned VQ, discussing where each excels. Add multiple-seed experiments with error bars for the closest comparisons.
3. **Add error bars** for the MMD vs. Wasserstein comparisons that have margins ≤0.02 r-FID.
4. **Rename $\mathcal{L}_{\text{unique}}$** to $\mathcal{L}_{\text{align}}$ to avoid confusion.

## Calibration Anchors

The following anchor papers from the calibration corpus were used for score calibration:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `nS2DBNydCC.md` (Wasserstein VQ paper) | 4.75 | R1 | Yes | Similar topic and weaknesses (marginal improvements), but VQ-Transplant has stronger core contribution and broader experiments |
| `sfTsvy05MX.md` (LL-VQ-VAE) | 4.75 | R1 | Yes | Similar VQ-improvement paper with limited evaluation; current paper is more thorough |
| `YlWvQSBCgl.md` (Channel-wise Quantization) | 4.00 | R1 | Yes | Novel quantization with limited evaluation and comparison fairness issues; current paper is stronger |
| `iqqpx8hgSQ.md` (RAQ-VAE) | 5.50 | R2 | Yes | Similar motivation (avoid retraining), but VQ-Transplant has more thorough experiments |
| `yGnsH3gQ6U.md` (BSQ-ViT) | 5.75 | R1 | Yes | Well-evaluated tokenizer with cleaner claims; slightly stronger than current paper due to no overclaiming issues |
| `8ishA3LxN8.md` (FSQ) | 6.50 | R2 | Yes | Clean contribution with no overclaiming; stronger than current paper |
| `GMwRl2e9Y1.md` (Rotation Trick) | 8.00 | R1 | Yes | Well-executed paper with principled method and extensive validation; significantly stronger |

**Score rationale:** The VQ-Transplant framework is a genuinely useful contribution with thorough experimental validation, placing it above the Wasserstein VQ paper (4.75) and RAQ-VAE (5.50). However, the inflated efficiency claims and overstatement of MMD-VQ's advantage are real issues not present in FSQ (6.50) or the Rotation Trick (8.00). The paper sits between RAQ-VAE (5.50) and FSQ (6.50). My draft items show strong positive favorability (~12) on the framework contributions, with moderately negative favorability (0 to -1) on the overclaiming weaknesses — consistent with a paper that has solid value but presentation issues that need correction.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>