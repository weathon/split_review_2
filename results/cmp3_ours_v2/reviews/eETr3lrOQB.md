## Summary

This paper proposes VQ-Transplant, a framework that enables plug-and-play replacement of VQ modules in pre-trained visual tokenizers (specifically VAR) by freezing the encoder-decoder and adapting only the decoder to the new quantized space. A secondary contribution is MMD-VQ, which replaces the Wasserstein distance with Maximum Mean Discrepancy for distribution alignment. Experiments on ImageNet-1k and cross-dataset evaluations (FFHQ, CelebA-HQ, LSUN-Churches) show that transplanted VQ variants can match or modestly exceed the original tokenizer's reconstruction quality at reduced computational cost.

## Strengths

1. **Well-motivated and practically useful problem.** The observation that VQ module development is bottlenecked by the cost of full tokenizer retraining (Section 1) is real and important. The idea of freezing the encoder-decoder and adapting only the decoder to a new VQ module's quantized space is conceptually clean and addresses a genuine need in the VQ research community.

2. **Solid within-tokenizer validation.** Tables 3 and 7 provide the fairest evaluation in the paper: comparing transplanted VQ variants against the *same original VAR tokenizer* on the *same dataset* (ImageNet-1k). MMD VAR achieves r-FID 0.81 vs. original VAR's 0.92 (Table 3, K=8192), a real improvement. The two-stage ablation (Substitution vs. Adaptation) cleanly validates the design — decoder adaptation substantially improves over VQ substitution alone.

3. **Cross-dataset generalization.** Tables 8–10 show the framework works on FFHQ, CelebA-HQ, and LSUN-Churches — datasets structurally different from the base VAR tokenizer's training data — demonstrating the approach is not overfit to a single domain.

4. **Transparent tracking of adaptation epoch effects.** Table 5 and Figure 3 honestly report r-FID progression over 20 epochs, showing continued improvement beyond the 5-epoch mark. The paper does not hide that longer training yields better results.

## Weaknesses

### Major

1. **Misleading headline comparisons conflate backbone advantage with method advantage.** Table 2 places MMD VQ (r-FID 0.86) and MMD VAR (r-FID 0.81) alongside from-scratch baselines such as VQGAN (5.96), RQVAE (3.20), and VQGAN-LC (2.62). These baselines were trained from scratch, with different architectures, different token counts, and without the benefit of the powerful pre-trained VAR encoder-decoder backbone. The visual impression is that VQ-Transplant dramatically outperforms prior work, but this is primarily because the transplanted methods inherit a strong pre-trained backbone. The controlled comparison (Tables 3, 7, against the original VAR tokenizer on the same data and backbone) shows real but more modest gains (0.81 vs. 0.92 r-FID).

   The same issue affects the abstract's headline claims. The "95% reduction in training cost" is computed as (16×60 − 2×22)/(16×60) = 95.4% — comparing VAR on OpenImages (16×A100, 60h) against VQ-Transplant on ImageNet-1k (2×A100, 22h). The "21.8× faster" claim uses the same GPU-hour ratio (960/44 = 21.8). In both cases, the comparison conflates differences in dataset size (OpenImages is ~7.5× larger than ImageNet-1k), hardware configuration, and training objective (full end-to-end training vs. decoder-only adaptation). Computing a single percentage from these non-comparable numbers is not informative as stated.

2. **Controlled efficiency comparison is missing.** The paper should compare VQ-Transplant against training the *same* MMD VAR architecture from scratch with the *same* compute budget (22 hours on 2×A100 on ImageNet-1k). Table 6 attempts this but only runs from-scratch training for 5–7 epochs, which the paper itself acknowledges is "insufficient" and "expected" to perform poorly. The reader cannot assess whether VQ-Transplant's advantage is due to the method or simply because it inherits a pre-trained backbone. Showing how many epochs of from-scratch training are needed to match VQ-Transplant's r-FID would directly quantify the benefit.

### Minor

1. **Adversarial training framing inconsistency.** Sections 1 and 2 frame adversarial training as the primary source of computational expense and instability — the core motivation for avoiding full retraining. Yet the decoder adaptation stage (Stage II, Equation 4) explicitly includes an adversarial loss (L_GAN) with a DINO-S discriminator, trained with DiffAug and consistency regularization. The paper never acknowledges this tension. The fact that Stage II requires only 5–20 epochs (vs. hundreds for full training) is a valid differentiator, but the paper does not make this argument explicitly, leaving an apparent contradiction.

2. **MMD-VQ's claimed advantage over Wasserstein VQ is not demonstrated.** MMD-VQ replaces the Wasserstein distance with MMD, motivated by MMD's ability to handle non-Gaussian feature distributions without parametric assumptions. However: (a) across all experiments (Tables 3, 7, 8, 9, 10), MMD VQ and Wasserstein VQ produce near-identical results — differences are often within noise (e.g., r-FID 0.91 vs. 0.93 in Table 3 K=4096; 1.05 vs. 1.04 in Table 7 K=16384); (b) the claimed non-Gaussian advantage is never empirically tested — no experiment demonstrates a scenario where Gaussian assumptions break down and MMD succeeds where Wasserstein fails. The theoretical motivation is sound but unsupported by evidence.

### Trivial

- The abstract and introduction highlight "only 5 epochs" as a hallmark of efficiency, but Table 5 shows MMD VAR's r-FID continues to drop from 0.81 (epoch 5) to 0.74 (epoch 20) with no plateau at epoch 5. The paper is transparent about longer runs (Table 5, Figure 3), making this a presentation nitpick rather than a substantive flaw, but the framing in the abstract is somewhat arbitrary.

## Nice-to-Haves

- **Downstream generation evaluation.** Since VQ-based tokenizers are used for downstream generation (AR modeling, diffusion), showing that transplanted VQ modules preserve or improve generation quality would strengthen the contribution. Currently only reconstruction quality is evaluated.
- **Hyperparameter sensitivity analysis.** The method has hyperparameters (γ in the uniqueness loss of Equation 3, the σ_i in the multi-Gaussian MMD kernel of Equation 5) whose sensitivity is not discussed.
- **From-scratch comparison with sufficient epochs.** Training the same architecture from scratch for enough epochs (e.g., to convergence or to match VQ-Transplant's r-FID) would quantify the computational savings more precisely than the current 5–7 epoch runs (Table 6).

## Removed Points

These points were flagged in the input review but are removed from the main assessment for the following reasons:

- **"Table 1 comparison is not meaningful because no two rows share the same experimental conditions"** — The table is presented as a landscape overview of computational costs across different tokenizers, not a controlled experiment. This serves a legitimate purpose. However, the "Speedup" column derived from this table *is* misleading, and this concern is already covered under Major weakness 1.
- **"L_Perf typo in Equation 2"** — This is a parser artifact of the PDF extraction; the original submission likely has proper notation.
- **"LDM-16 experiment deferred to appendix"** — The main text (Section 5.1, line 269) discusses the LDM-16 experiment and acknowledges its lower adaptability. Deferring the full table to the appendix is standard practice.
- **Missing related works, reproducibility nitpicks** — Removed per filtering rules.
- **The "5 epochs" criticism as a weakness** — Downgraded from the harsh critic's framing to Trivial because the paper transparently provides longer-run results (Table 5, Figure 3).
- **"95% reduction" and "21.8× faster" as standalone criticisms** — These are merged into Major weakness 1 as part of the broader comparison-fairness issue, not treated as independent points.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a clear framing-vs-evidence gap: the paper's strongest evidence is its within-backbone comparison (Tables 3, 7), but it front-loads cross-method comparisons (Table 2, abstract claims) that are not controlled for backbone, dataset, or compute budget. This is a presentation problem rather than a fatal flaw — the core technical contribution is sound.

## Suggestions

1. Restructure the evaluation to make Tables 3 and 7 the centerpiece. Move the cross-method comparison (Table 2) to an appendix or clearly annotate it to distinguish between VQ-Transplant results and from-scratch baselines, specifying which backbone each method uses.
2. Report the "95% reduction" and "21.8× faster" claims only when controlling for the backbone (i.e., compare against training the same architecture from scratch on the same dataset). Qualify any cross-method efficiency comparisons explicitly.
3. Acknowledge the adversarial training tension directly in the introduction or method section: e.g., note that decoder adaptation uses adversarial training but runs for only 5–20 epochs rather than the hundreds required for full tokenizer training.
4. Provide at least one experiment demonstrating MMD's claimed advantage over Wasserstein VQ on non-Gaussian feature distributions (synthetic or real-world). Without this, MMD-VQ's motivation remains theoretical only.

## Score and Decision

**Calibration anchors.** All papers from the deepreview_13k_calibration corpus:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| nS2DBNydCC (Wasserstein VQ) | 4.75 | Bracketing | Directly related (distribution-matching VQ); that paper has weaker empirical validation, this paper has a stronger framework idea but similar framing issues |
| YlWvQSBCgl (Channel-wise Quant.) | 4.00 | Bracketing | Similar-level contribution with comparison fairness issues; this paper has stronger empirical support |
| yGnsH3gQ6U (BSQ-ViT) | 5.75 | Bracketing | Stronger paper overall with a novel quantization method; this paper has a less novel secondary contribution |
| QE1LFzXQPL (ImageFolder) | 6.25 | Bracketing | Stronger, more complete paper with downstream generation results; this paper lacks downstream eval |
| IqGVIU4rvM (VQ-VAE+Diffusion) | 2.50 | Bracketing | Much weaker paper; this paper is clearly above this anchor |
| gMGUa8C0tL (TaCA adapters) | 5.25 | Narrowing | Similar "plug-and-play module replacement" framing; comparable strength |
| 2zMHHZ569S (Qinco2) | 6.40 | Narrowing | Stronger VQ paper with more complete evaluation |
| mRw9BuNO9i (Cross-platform codec) | 6.00 | Narrowing | Different domain but similar codebook-based approach; weaker comparison section |

**Round 1 bracket**: 4.0 – 6.0 (between Channel-wise Quantization at 4.00 and BSQ-ViT at 5.75)

**Narrowing**: Based on comparison with the Wasserstein VQ paper (4.75, weaker empirical validation), the TaCA adapters paper (5.25, similar "plug-and-play" framing), and the BSQ-ViT paper (5.75, stronger contribution), this paper sits between 4.75 and 5.5. The core VQ-Transplant idea is genuinely useful and validated, but the presentation overclaims significantly, and MMD-VQ is an incremental secondary contribution. The paper's strengths (clean framework idea, solid within-backbone validation) balance against its weaknesses (misleading headline comparisons, lack of controlled efficiency comparison). A score of **5.0** reflects a borderline paper — the technical contribution is real but the framing distorts the claimed impact.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>