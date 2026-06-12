## Summary
ARSS proposes applying decoder-only autoregressive (GPT-style) models to novel view synthesis from a single image, conditioned on camera trajectories. The framework uses a video tokenizer (with finite scalar quantization) for temporally consistent tokenization, a camera autoencoder that maps Plücker raymaps into latent camera tokens serving as 3D positional guidance, and a hybrid token permutation strategy that randomly shuffles spatial token order while preserving temporal causality. Experiments on RealEstate-10K, ACID, and zero-shot DL3DV benchmark show competitive performance against diffusion-based and transformer-based baselines.

## Strengths
- **First application of AR models to camera-controlled NVS:** The paper identifies a genuine gap—existing AR visual generation works focus only on single images, while NVS methods predominantly use diffusion models. Adapting the AR paradigm to multi-view generation with camera conditioning is a meaningful research direction, especially for scenarios requiring causal, incremental generation along trajectories.
- **Thorough ablation studies:** The paper provides clear ablations on token permutation strategies (raster vs. full permutation vs. hybrid spatial-only permutation) with both quantitative (Table 2) and qualitative evidence (Figure 7), demonstrating that each design choice contributes meaningfully. The video tokenizer ablation (Table 3) shows a striking 62% FVD improvement over VQ tokenization, convincingly justifying the video tokenizer choice.
- **Error accumulation analysis:** Figure 6 demonstrates that ARSS maintains quality better over long trajectories compared to all baselines, with flatter degradation curves on PSNR, SSIM, and LPIPS. This directly validates the core motivation of causal AR generation for sequential view synthesis.
- **Zero-shot generalization:** The DL3DV zero-shot results (Table 1) and qualitative results on AI-generated images (Figure 5) demonstrate reasonable generalization, strengthening the practical relevance of the approach.

## Weaknesses
### Fatal
None.

### Major
- **Marginal quantitative improvements over strong baselines:** The headline gains are modest—on RealEstate10K, PSNR improves only +0.29 dB over SEVA; on ACID, +0.16 dB. Furthermore, ARSS is not uniformly better: on RealEstate10K, SEVA achieves better SSIM (0.670 vs. 0.624) and FID (46.98 vs. 47.60). The paper claims "our method out-performs current state-of-the-art methods" in the abstract and introduction, but the results are more nuanced—this inconsistency weakens the paper's credibility.
- **Inconsistent claim strength across the paper:** The abstract says "comparable to state-of-the-art," Section 1 claims "out-performs," and Section 4 says "outperforms most." This oscillation between hedged and strong claims undermines confidence in the experimental assessment. A clearer, consistent framing would be more convincing.
- **Low resolution and limited training scale:** Training at 256×256 resolution with 8 H100s for 100K iterations is relatively limited compared to state-of-the-art diffusion methods that often train at higher resolutions with much larger compute budgets. The authors partially acknowledge this, but it limits the strength of the comparison and the practical relevance of the results.

### Minor
- **No validation of the causal generation advantage:** The primary conceptual argument for AR over diffusion is causal, incremental generation. However, there is no experiment demonstrating, for example, incremental trajectory extension or dynamic re-planning—scenarios where the AR paradigm would be uniquely advantageous. The paper relies entirely on standard fixed-trajectory benchmarks where the causal structure provides no obvious benefit.
- **Limited baselines:** No comparison with other AR-based video generation methods (e.g., VideoPoet, LTX-Video) that could serve as closer comparisons, nor with more recent NVS methods beyond the selected ones.

### Trivial
None.

## Nice-to-Haves
- An experiment demonstrating incremental trajectory extension or online generation, which would uniquely motivate the AR approach over diffusion.
- Comparison at higher resolutions to strengthen practical relevance.
- A discussion of computational cost (inference speed, memory) relative to diffusion-based baselines, since efficiency is often cited as an advantage of AR models.

## Novel Insights
The paper's most interesting observation is that camera tokens naturally serve as positional instruction tokens for randomly permuted visual tokens, unifying two previously separate ideas (camera conditioning and random spatial permutation for AR image generation). This is a genuinely elegant design insight—the camera tokens provide both the geometric guidance needed for NVS and the positional instructions needed for the spatial permutation strategy. However, beyond this architectural observation and the broader demonstration that AR models can work for NVS, the novel insights are incremental rather than fundamental.

## Suggestions
- Frame the claims consistently: either "comparable" or "outperforming" but not both. Given the mixed metric results, "competitive with" is most honest.
- Add an experiment that showcases the unique advantage of the causal AR structure (e.g., incremental trajectory extension, dynamic camera re-planning during generation).
- Provide inference speed comparisons against diffusion baselines to strengthen the practical motivation for AR-based generation.
- Clarify in the main text that training is from scratch on limited data, and discuss how scaling data/compute might close the gap with diffusion methods trained on larger datasets.

## Score and Decision

MY FINAL SCORE: 4.5
MY FINAL DECISION: Reject