Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proposes **ARSS**, the first decoder-only autoregressive (GPT-style) framework for novel view synthesis (NVS) from a single image with explicit camera trajectory control. The system combines a video tokenizer for temporally consistent visual tokens, a camera autoencoder that converts Plücker raymaps into 3D positional instruction tokens, and an autoregressive transformer with spatial-only token permutation to balance causal generation with bi-directional spatial context. Experiments on RealEstate10K, ACID, and DL3DV show competitive performance against diffusion-based methods.

## Strengths

- **First application of causal decoder-only AR to NVS with camera trajectory control (Section 3, Figure 2).** Prior AR visual generation work (LlamaGen, VAR, etc.) focused exclusively on single-image generation, while diffusion-based NVS methods generate all views jointly. ARSS genuinely bridges this gap, and the paper correctly delineates the prior art.

- **Well-motivated design of camera tokens as 3D positional instruction tokens (Section 3.2.2).** The camera autoencoder maps Plücker raymaps to latent tokens that serve a dual purpose: providing 3D positional guidance and functioning as the positional instruction token required for random spatial permutation (following Pang et al., 2025; Yu et al., 2024a). This is an elegant solution to integrating camera control with shuffled-token AR generation.

- **Clean and informative ablation of token permutation strategies (Table 2, Figure 7).** The ablation clearly demonstrates that spatial-only permutation (preserving temporal order) outperforms both raster ordering and full spatiotemporal permutation, providing concrete evidence that the design choice is correct. The error accumulation analysis (Figure 6) further shows flatter degradation trajectories for ARSS than baselines, which is genuinely informative.

## Weaknesses

### Major

- **Discrepancy between the paper's claims and its quantitative evidence.** The introduction (line 88) and discussion (line 281) claim ARSS "out-performs current state-of-the-art methods" and "outperforms state-of-the-art methods leveraging diffusion models and transformers." The results in Table 1 show a clear tradeoff, not a win: against SEVA on both datasets, ARSS wins on PSNR and LPIPS but loses on SSIM (by ~6-7%) and FID (by 1.3% on Re10K, 44% on ACID). The abstract more cautiously says "overall comparable," but the intro/discussion overstate the evidence. The paper's own quantitative section (line 231) acknowledges geometric inconsistencies, yet the conclusion ignores this nuance. This framing misrepresents the evidence and would mislead a reader about the method's standing.

- **The camera autoencoder — a core component — is not validated.** Section 3.2.2 describes its architecture and loss (Eq. 5), but the paper provides: (a) no reconstruction accuracy metrics for the camera autoencoder, (b) no ablation comparing it to simpler alternatives (e.g., directly encoding camera parameters as learned embeddings, or using Plücker coordinates as raw input features without an autoencoder), and (c) no analysis of how camera token quality affects downstream NVS performance. The claim that camera tokens "provide accurate 3D position in the scene" (line 86) is entirely unsupported. Since the entire spatial permutation strategy depends on camera tokens providing accurate positional information, this gap is significant.

- **Unexplained discrepancy between main results and ablation tables.** Table 1 reports ARSS at PSNR 19.02 on RealEstate10K, while Tables 2 and 3 report "ours" at PSNR **19.22** with substantially different SSIM (0.565 vs 0.624) and FID (60.11 vs 47.60). Neither ablation table specifies which dataset or evaluation subset the numbers are on. This undermines reproducibility and makes it impossible to assess whether the ablations are conducted under comparable conditions.

### Minor

- **No autoregressive baseline is included.** The paper's central thesis is that AR models can perform NVS competitively with diffusion, yet all baselines are either diffusion-based or feed-forward transformers. The VQ image tokenizer ablation (Table 3) partially addresses the tokenization aspect, but a comparison to a camera-conditioned AR image generator (e.g., adapting LlamaGen or VAR for NVS) would help isolate whether ARSS's specific design choices matter beyond the general viability of AR for NVS.

- **Unsubstantiated claim about SEVA's resource requirements (Section 4.2, line 241).** The paper states "SEVA benefits from large-scale, high-resolution training data and heavy computational resources, whereas our approach attains competitive performance without such requirements" without providing any evidence about SEVA's training budget. Using a pre-trained model (as SEVA does) is an advantage, not a weakness, so this rhetorical framing is misleading.

- **No inference speed or computational cost comparison.** AR models typically offer fast inference (single forward pass, no iterative denoising), which is a natural advantage of the approach. The paper does not report wall-clock time, FLOPs, or any efficiency metric against diffusion baselines, which would strengthen the case for AR-based NVS.

- **No discussion of sampling strategy.** The method uses "next-token prediction manner" during inference (line 210), but there is no mention of sampling temperature, top-k, top-p, or any decoding hyperparameters. For AR visual generators, the sampling strategy significantly affects generation quality; its omission makes the results harder to reproduce.

### Trivial

None.

## Nice-to-Haves

- Clarify the causal vs. non-causal video tokenization distinction in Section 3.1, which is currently fragmented and uses confusing notation ($L$ vs $L+1$).
- Fix the typo in Eq. 5's caption (line 153): "d is the momentum term" should read "m is the momentum term."

## Removed Points

These points are flagged to be removed. Treat them with caution.
- *"MotionCtrl is a weak baseline"* – Including a range of baselines is standard practice; the paper does not claim beating MotionCtrl as a significant achievement.
- *"Concurrent work from 2025–2026 not discussed"* – The hard rule prohibits speculating about missing related works without external verification.
- *"Error accumulation analysis may be unfair to baselines"* – This is speculative; the paper cannot control how baselines were evaluated in prior work, and the analysis remains informative.
- *"Typo in Eq. 5"* – A trivial notation error that does not affect correctness; moved to Nice-to-Haves.
- *"Causal video tokenization needs rewriting"* – A presentation note that does not affect the technical contribution; moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reconcile the framing with the evidence.** Replace "outperforms SOTA" with an honest characterization of the tradeoff: e.g., "ARSS achieves competitive performance with diffusion-based methods, excelling on token-level fidelity (PSNR, LPIPS) while exhibiting tradeoffs on structural similarity (SSIM) and distributional metrics (FID)."
2. **Validate the camera autoencoder.** Provide reconstruction accuracy metrics and an ablation comparing it to simpler alternatives (e.g., learned per-view embeddings from raw camera parameters, or raw Plücker features without compression).
3. **Clarify ablation evaluation conditions.** Specify the dataset/subset used in Tables 2 and 3, and explain the PSNR/SSIM/FID discrepancy with the main table.
4. **Add an AR baseline.** Adapt a causal image generator (e.g., LlamaGen) for NVS with camera conditioning to isolate the effect of the paper's specific design choices.
5. **Report efficiency metrics.** Include wall-clock inference time or FLOPs to quantify the speed advantage of AR over diffusion.
6. **Document the sampling strategy.** Report the temperature, top-k, top-p, or other decoding hyperparameters used during generation.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>