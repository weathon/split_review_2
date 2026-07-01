## Summary

This paper proposes LDP, a lightweight denoising autoencoder plug-in for single-image super-resolution (SISR) that aims to improve generalization to unseen degradations. LDP models the degradation process within a DAE framework by conditioning on LR high-frequency components and using patch-dependent noise. It can be used as a training-time loss for fine-tuning SR models or as an inference-time correction module via posterior sampling for diffusion models. Experiments on multiple SR architectures (SwinIR, MambaIR, FeMaSR, StableSR, etc.) show consistent PSNR/SSIM improvements on synthetic benchmarks and mixed results on real-world datasets.

## Strengths

- **Important problem**: Improving generalization of SISR models to unknown degradations is a practical and well-motivated challenge.
- **Lightweight design**: LDP has only 642K parameters and can be integrated into various SR architectures with modest overhead.
- **Extensive evaluation**: The paper tests LDP across a broad range of SR models (CNN, Transformer, Mamba, diffusion-based) and multiple degradation types, with both synthetic and real-world benchmarks.
- **Ablation studies**: The paper ablates loss components and the \(\tau\) weight, providing insight into the contribution of each term.

## Weaknesses

### Fatal

None.

### Major

1. **Inconsistent and sometimes negative results for posterior sampling and real-world benchmarks**. In Table 5, applying LDP to LDM degrades most metrics (e.g., NIQE, MANIQA, CLIPIQA all worsen on RealSR and DPED). For FeMaSR on real-world datasets (Table 4), LDP lowers CLIPIQA and NIQE on several datasets. The paper attributes this to suppressed GAN artifacts, but the evidence is weak and undermines the claim that LDP consistently improves generalization.

2. **Missing comparison with competing plug-in methods**. The paper cites Lway (Chen et al. 2024) as a related test-time adaptation method but does not compare LDP with it or other plug-in approaches (e.g., CorrectFilter, DRN). Without such comparisons, it is unclear whether LDP offers tangible advantages over existing plug-in solutions for improving generalization.

3. **Poorly justified design choices**. (a) The computation of \(y_{hf}\) uses \(s^2\)-fold downsampling (Eq. 4). For 4× SR, this means 16× downsampling of the LR, which seems overly aggressive and likely discards useful high-frequency information. No ablation or justification is provided. (b) Patch-dependent noise timesteps are introduced but not ablated against uniform noise; the claim that this helps capture spatially varying degradation is not empirically validated.

4. **The claimed diffusion-model property is not convincingly leveraged**. The paper states that “after noise is added, HR images and LR features become aligned” (citing DR2) and uses this to justify degradation modeling via a DAE. However, LDP does not use diffusion models during training and adds random patch-level noise rather than following a learned diffusion process. The connection to diffusion theory is tenuous and does not drive the method’s design in a substantive way.

### Minor

- The writing in Section 3.1 (Motivation) is unclear. The alignment property is stated but not explained in a self-contained manner, making it hard to follow how it motivates the DAE framework.
- No ablation on the patch-dependent noise versus whole-image noise or on the \(s^2\) downsampling factor in Eq. 4.

## Nice-to-Haves

- Comparison with Lway or other plug-in generalization methods.
- Ablation on the patch-dependent noise design (e.g., uniform vs. patch-wise timesteps, different patch sizes).
- Ablation on the \(s^2\) factor in the \(y_{hf}\) computation.
- Per-method runtime or FLOPs comparison for the posterior sampling mode.

## Novel Insights

None beyond the paper’s own contributions. The core idea of using a lightweight DAE conditioned on LR high-frequency components to model degradation and enforce cycle consistency is a practical combination of existing ideas (DR2, DRN, conditional denoising) rather than a fundamentally new insight.

## Suggestions

1. Include a direct comparison with Lway or other plug-in test-time adaptation methods on the same benchmarks to demonstrate LDP’s relative effectiveness.
2. Add an ablation study that investigates the patch-dependent noise schedule (e.g., compare with uniform noise over the whole image) and the \(s^2\) downsampling factor in Eq. 4.
3. Provide a more thorough discussion of why LDP sometimes degrades no-reference metrics (e.g., FeMaSR on RealSRSet, LDM across multiple datasets) and whether these cases are acceptable trade-offs.
4. Clarify the motivation section (3.1) by explaining more concretely how the diffusion alignment property is used in the DAE degradation modeling.

## Score and Decision

The paper addresses an important problem and provides extensive experiments, but the contributions are incremental and the results are inconsistent, particularly for real-world benchmarks and posterior sampling. The lack of comparison with existing plug-in methods and the insufficient justification of key design choices weaken the overall contribution. Given these issues, the paper does not meet the acceptance bar for ICLR.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>