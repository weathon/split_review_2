## Summary

VQ-Transplant proposes a framework for plug-and-play replacement of VQ modules within frozen pretrained visual tokenizers (e.g., VAR), avoiding end-to-end retraining. The method decouples VQ module substitution from a lightweight 5-epoch decoder adaptation stage. A secondary contribution, MMD-VQ, uses maximum mean discrepancy for distributional alignment between features and codebook. The paper evaluates 5 VQ variants across multiple scales and 4 datasets, demonstrating that VQ-Transplant achieves competitive reconstruction fidelity with substantial compute savings.

## Strengths

- **Practical and well-motivated idea.** The core insight — freeze the encoder-decoder and only swap the VQ module — is simple, clearly articulated (Section 4.1), and directly addresses a real bottleneck: the prohibitive cost of end-to-end tokenizer retraining that discourages exploration of new VQ methods.

- **Decoder adaptation is convincingly shown to close the quantization mismatch gap.** Tables 3, 4, and 5 provide clear evidence: substitution alone leaves a gap (r-FID ~1.49–1.93), 5-epoch adaptation brings all distribution-alignment methods under r-FID 1.0, and extending to 20 epochs further improves to 0.74 r-FID (Table 5). The ablation on adaptation epochs (Table 4, Figure 3) supports the trajectory.

- **Broad and systematic evaluation.** The paper tests 5 VQ variants (Vanilla, EMA, Online, Wasserstein, MMD) under both multi-scale and fixed-scale configurations, across ImageNet-1K, FFHQ, CelebA-HQ, and LSUN-Churches (Tables 3, 7, 8, 9, 10). This breadth makes the conclusions about which VQ families are transplant-compatible more robust.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The headline efficiency numbers are not perfectly controlled.** Table 1 and the "95% cost reduction" / "21.8× faster" claims compare VQ-Transplant (trained on ImageNet-1K, 2×A100) against the VAR baseline (trained on OpenImages, 16×A100). Since ImageNet-1K is a subset of OpenImages (as the paper acknowledges, line 277), the dataset difference confounds the comparison — training on the smaller dataset likely contributes to the savings. The "Speedup" column in Table 1 is also never defined. The core point (VQ-Transplant saves substantial compute) is almost certainly true, but the exact 95% figure mixes dataset scale with method efficiency. The paper would be stronger if it reported a controlled comparison on the same dataset.

- **MMD-VQ's claimed advantage over Wasserstein VQ is not empirically validated.** The paper positions MMD-VQ as a separate contribution (Section 4.2), motivated by Wasserstein VQ's dependence on Gaussian assumptions. Yet across every experiment, MMD-VQ and Wasserstein VQ perform nearly indistinguishably (e.g., Table 3: MMD VAR r-FID 0.81 vs Wasserstein VAR 0.83; Table 7: 0.86 vs 0.92; Table 8 FFHQ: Wasserstein actually wins 1.81 vs 1.99). No evidence is provided that feature distributions in these models are actually non-Gaussian, or that MMD's non-parametric nature confers a real advantage. Without such evidence, MMD-VQ reads as a close variant of Wasserstein VQ rather than a distinct contribution.

- **No variance or significance reporting.** All results are point estimates with no standard deviations, confidence intervals, or indication of multiple runs (Tables 3, 7–10). Given that many reported differences between methods are small (r-FID gaps of 0.02–0.10), it is impossible to tell which differences are systematic and which are noise. This is a standard expectation for empirical ML papers.

- **Baseline comparisons in Table 2 are not fully controlled.** The baselines (DQVAE, DiVAE, RQVAE, VQGAN variants) use different token counts (mostly 256 vs. VQ-Transplant's 512–680), different architectures, and different training budgets. While this is a common limitation of benchmarking against published results, it limits the informativeness of the "outperform competing baselines" claim. The most controlled comparison (MMD VAR vs. original VAR, same architecture) is the most trustworthy, and it does show VQ-Transplant achieving competitive or better r-FID.

- **Two methodological details are underspecified.** (1) The $\mathcal{L}_{\text{unique}}$ term in Equation (3): the paper only gives examples for Wasserstein VQ and MMD-VQ but does not clarify what this term is for Vanilla, EMA, or Online VQ — methods that lack a natural "uniqueness-enforcing" loss. (2) The multi-Gaussian kernel in MMD-VQ (Equation 5) uses bandwidths $\sigma_i$ with no discussion of how they are chosen or sensitivity to this choice.

- **Cross-dataset generalization only tests two VQ methods.** Tables 8–10 evaluate only Wasserstein VQ and MMD VQ (not all 5 variants), so we cannot tell whether Vanilla, EMA, or Online VQ would also generalize well.

### Trivial
None.

## Nice-to-Haves
- Report results with variance estimates (e.g., over 3 seeds) to substantiate small metric differences.
- Clarify what $\mathcal{L}_{\text{unique}}$ is for each non-distributional VQ variant, and state the MMD kernel bandwidth selection method.
- Include more VQ variants in the cross-dataset experiments (Tables 8–10) to strengthen the generality claims.

## Removed Points
- **Claim about typo in Equation (2) ($\mathcal{L}_{\text{Perf}}$ vs $\mathcal{L}_{\text{Per}}$):** Removed per hard rule — the parser strips formatting details, and this discrepancy may be a PDF extraction artifact rather than an author error.
- **Criticism that Table 6 from-scratch comparison is unfair because training is short:** Removed — the paper explicitly acknowledges from-scratch training needs hundreds of epochs, and the point is to show VQ-Transplant wins even with more GPU hours. This misreads the experiment's purpose.
- **Criticism that "2×A100 GPUs for 22 hours is not democratized":** Removed — this is an opinion about wording, not a substantive flaw.
- **Claim that UniTok at 256×A100 is "cherry-picked":** Removed — the table fairly includes multiple baselines, and the paper does not highlight the 290.9× figure in the body text.
- **Generic "the evaluation lacks rigor" / "baselines may not be fair" speculative framings:** Removed — these were not anchored to specific concrete problems in the paper.
- **Criticism about "sunk cost of the pretrained model" not being counted as a fatal issue:** Calibrated — the pretrained model is publicly available and intended for reuse; including its cost would conflate one-time pre-training with per-experiment cost. The remaining concern about dataset mismatch is the controlled version of this point.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Run one controlled experiment: train VQ-Transplant and a from-scratch VAR tokenizer on the *same* dataset (e.g., ImageNet-1K) with the same GPU budget, and report both total and incremental cost clearly.
2. Either substantiate MMD-VQ's advantage with evidence of non-Gaussian feature distributions, or reposition it as a variant of distribution-matching VQ rather than a separate contribution.
3. Add a brief note defining the "Speedup" column in Table 1.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>