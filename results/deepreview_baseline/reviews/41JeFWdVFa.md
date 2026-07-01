## Summary
The paper proposes LDP, a lightweight denoising autoencoder plug-in for single-image super-resolution. LDP models the degradation process within a DAE framework using patch-dependent noise and conditioning on LR high-frequency components. It can be applied to SR models in two modes: as a training-time loss function to enforce cycle consistency, or as an inference-time post-processing step via posterior sampling. Experiments across multiple SR architectures and degradation types show consistent improvements.

## Strengths
- **Practical and flexible plug-in design**: LDP is lightweight (642K parameters) and can be integrated into diverse SR architectures (CNN, Transformer, Mamba, Diffusion) with minimal modification, operating in both training and inference modes.
- **Comprehensive experimental evaluation**: The method is tested on four SR models (FeMaSR, StableSR, SwinIR, MambaIR) across five synthetic degradation types and three real-world benchmarks, with both reference and no-reference metrics.
- **Ablation studies**: The paper ablates loss components, weight τ, and other design choices, providing insight into the contribution of each module.

## Weaknesses
### Fatal
None.

### Major
1. **Limited novelty relative to existing degradation modeling approaches**: The core idea of using a degradation model to enforce cycle consistency (SR → LR → prediction) is well-established (DRN, DualSR, SCL-SASR, Lway). The main claimed novelty—using a DAE with patch-dependent noise and LR high-frequency conditioning—is incremental. The connection to diffusion models (noise aligning LR/HR features) is mentioned only as motivation; the method itself is a DAE and does not leverage diffusion sampling dynamics beyond the noise schedule.

2. **Inconsistent results and overclaimed improvements**: Several metrics show degradation. For FeMaSR+LDP on Blur and Hybrid, LPIPS increases (0.3199 vs 0.3168; 0.3516 vs 0.3453). In Table 4, FeMaSR+LDP shows worse CLIPIQA on RealSR and RealSRSet, and worse NIQE on DPED and RealSRSet. In Table 5, LDM+LDP underperforms LDM on 4 out of 5 metrics on RealSR and DPED. The paper dismisses these as "GAN artifacts misinterpreted as texture" or metrics favoring "visually striking results," but this weakens the claim that LDP "substantially improves" generalization across the board.

3. **Missing details and unclear methodology**: 
   - The patch-dependent timestep assignment (Eq. 7) is described only as "each patch is assigned a random timestep t_i." The distribution and spatial sampling strategy are not specified.
   - The Noise Addition Module in Figure 2 shows Conv → Noise → Downsample, but Eq. 2 says x_t = NAM(x, t). It is unclear how timestep t is used in NAM.
   - The Degradation Prompt P_D is mentioned as jointly learned, but its dimension, initialization, and training are not described.
   - The gradient in Eq. 17 uses L_{sym}^{FT}, which depends on LDP's output; backpropagating through a full LDP forward pass at each diffusion step is computationally heavy, yet no runtime or FLOPs are reported.

4. **Reproducibility concerns**: The paper states that "LDP parameters can be universally configured as τ=100 and λ_1=λ_2=λ_3=1 for any super-resolution model." This claim is supported only by ablations on SwinIR with one dataset (Hybrid). Without validating on other architectures and degradation types, the claim is premature. The training of LDP itself (Section 4.1) uses specific data (LSDIR with BSRGAN degradations) but does not clarify whether the same pre-trained plug-in is used across all fine-tuning tasks.

### Minor
- The abbreviation "Lway" (Chen et al. 2024) is confusing; it is unclear if this is a method name or a typo.
- Table 2 shows that LDP's LR predictions have lower similarity to downsampled SR than DRN, which is presented as a strength. However, LDP also has lower similarity to the target LR than DRN on some metrics (e.g., PSNR on Down: 29.15 vs 31.57?), which might indicate less accurate LR prediction. The paper should directly compare LR prediction accuracy (Table 1) rather than using Table 2 as a diagnostic.
- The connection between LDP and diffusion posterior sampling is weak: Eq. 17 simply plugs L_{sym}^{FT} into the DPS gradient, which is a standard cycle-consistency loss, not a novel contribution.

### Trivial
- Figure captions contain repetitive text from the main body; the diagrams are difficult to parse without reading the full caption in context.

## Nice-to-Haves
- Provide runtime and FLOP comparisons for both training and inference modes.
- Ablate the patch-size P and the effect of patch-dependent noise vs. image-level noise.
- Validate the "universal" hyperparameter claim on at least one other architecture (e.g., MambaIR) in an ablation setting.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Clearly separate the two contributions: (a) LDP as a degradation model for LR prediction, and (b) LDP as a plug-in for SR fine-tuning/inference. The current framing conflates them.
2. Provide a proper algorithm box (pseudocode) for the training of LDP and for the fine-tuning of SR models with LDP, including how patch timesteps are sampled.
3. Report computational cost (time per image, FLOPs) for the posterior sampling mode, and discuss trade-offs between improvement and overhead.
4. Acknowledge and explain cases where LDP hurts certain metrics (e.g., FeMaSR CLIPIQA drops) more thoroughly, rather than attributing to metric bias without analysis.

## Score and Decision
Score: 4  
Decision: Reject

MY FINAL SCORE: 4<score>4</score>
MY FINAL DECISION: Reject<decision>Reject</decision>