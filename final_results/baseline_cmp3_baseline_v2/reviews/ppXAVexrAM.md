## Summary

The paper introduces ARSS, the first framework that applies a GPT-style decoder-only autoregressive model to novel view synthesis from a single image under a prescribed camera trajectory. The method uses a video tokenizer for temporally consistent discrete representations, a camera autoencoder to encode Plücker raymaps into 3D positional tokens, and a hybrid token permutation strategy that preserves temporal order while randomly shuffling spatial tokens to adapt the causal transformer to bi-directional visual data. Experiments on RealEstate10K, ACID, and zero-shot on DL3DV show results competitive with or surpassing several diffusion-based and transformer-based baselines.

## Strengths

- **Novel application of autoregressive models to NVS**: The paper is the first to apply a decoder-only causal transformer to the task of novel view synthesis with explicit camera control. This opens a new direction distinct from the dominant diffusion-based paradigm and offers a principled causal generation path along camera trajectories.
- **Effective design of 3D positional guidance**: The camera autoencoder maps Plücker rays into token-aligned latent representations, providing explicit geometric conditioning that enables the autoregressive model to maintain 3D consistency across views. The geometry-constrained reconstruction loss is well-motivated.
- **Strong empirical results with good ablation support**: Quantitative results on three datasets show ARSS achieves the highest or second-highest scores on most metrics (e.g., PSNR, LPIPS, FVD) compared to multiple baselines. The ablation studies convincingly demonstrate the necessity of the hybrid spatial-permutation-with-temporal-preservation strategy and the video tokenizer over a per-frame VQ tokenizer.

## Weaknesses

### Fatal
None.

### Major
- **Incomplete baseline comparisons and overclaimed results**: The paper claims to "outperform current state-of-the-art methods", but the quantitative table (Table 1) shows mixed results. For example, on RealEstate10K, SEVA achieves higher SSIM (0.670 vs 0.624) and lower FID (46.98 vs 47.60); on ACID, SEVA also has higher SSIM and lower FID. This weakens the claim of state-of-the-art performance. Additionally, several evaluated methods (e.g., SEVA, RayZer) are missing from the DL3DV zero-shot comparison, making cross-dataset comparisons incomplete. The paper should include all baselines on all datasets when possible or justify exclusions.
- **Missing ablation on the camera autoencoder**: The camera autoencoder is a core contribution (Sec. 3.2.2), yet there is no ablation study to validate its importance—e.g., replacing it with simpler conditioning (cross-attention to camera parameters, FiLM modulation, or no camera conditioning). Without this, it is unclear whether the proposed camera autoencoder design is critical or if a simpler alternative would suffice.
- **Fairness of training setup**: The paper notes that ARSS is trained from scratch on limited public datasets at low resolution (256×256), whereas many diffusion baselines are fine-tuned from large-scale pretrained models. This discrepancy should be directly addressed when interpreting comparisons. The paper mentions it as a limitation but does not quantify how much performance difference can be attributed to pretraining versus model architecture.

### Minor
- **Equation 5 contains a notational error**: The loss term writes "‖𝐝̃ −𝐝‖" where both are defined as the normalized ray direction; the second term "‖𝐦̃ −𝐦‖" correctly uses the momentum variable, but the first term uses "𝐝̃ −𝐝" rather than "𝐝̃ −𝐝" (likely a typo). The text also states "d is the normalized camera ray direction, d is the momentum term", which is confusing—the momentum should be denoted m.
- **Limited discussion of practical advantages**: The paper argues that the autoregressive paradigm is desirable for world models because it supports causal and incremental generation, but no experiment directly demonstrates this advantage (e.g., dynamic insertion of frames, continued generation after a change in trajectory). The claim remains motivational rather than validated.

### Trivial
None.

## Nice-to-Haves

- An analysis of inference speed or computational cost compared to diffusion-based methods would strengthen the practical motivation.
- Higher-resolution generation (e.g., 512×512) would increase applicability; the current 256×256 limit may limit impact.
- A more systematic error analysis beyond per-frame metrics—e.g., measuring 3D consistency or geometric accuracy using depth or correspondence.

## Novel Insights

The paper’s key insight is that the autoregressive formulation can be adapted for NVS by converting the generation into a next-token prediction problem over a temporally-ordered sequence of discrete visual tokens, with 3D positional tokens inserted to provide camera-aware conditioning. The hybrid permutation strategy (spatial shuffle within frames, fixed temporal order) is a practical compromise that aligns the causal transformer’s unidirectional nature with the bidirectional spatial structure of images while preserving the causal temporal dependency needed for multi-view generation. This insight, borrowed from prior image AR works but newly applied to multi-view sequences, offers a neat way to handle both spatial and temporal structure in a single autoregressive framework.

## Suggestions

- Tone down the claims of state-of-the-art and instead present the method as "competitive" or showing "favorable performance on multiple metrics" given the mixed quantitative results.
- Add an ablation study where the camera autoencoder is replaced by simpler conditioning (e.g., concatenating camera parameters to the input tokens) to demonstrate the necessity of the learned 3D positional tokens.
- Include all applicable baselines on the DL3DV zero-shot split, or clearly explain why certain methods cannot be evaluated (e.g., if they were trained on DL3DV). Provide per-scene scores to give a more nuanced comparison.
- Clarify in the main text the practical benefit of the autoregressive approach by reporting, for example, generation time, ability to extend trajectories, or computational efficiency relative to diffusion baselines.

## Score and Decision

Score: 6

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>