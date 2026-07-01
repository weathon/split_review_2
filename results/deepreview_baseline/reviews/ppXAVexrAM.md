## Summary

This paper introduces ARSS, the first framework that uses a GPT-style decoder-only autoregressive (AR) model for novel view synthesis (NVS) from a single image, conditioned on a camera trajectory. The method combines a video tokenizer for temporal consistency, a camera autoencoder that converts Plücker ray maps into 3D positional guidance tokens, and a hybrid token ordering that randomly permutes spatial tokens while preserving temporal causality to align uni-directional causal attention with bi-directional image data. Experiments on RealEstate10K, ACID, and zero-shot on DL3DV show competitive results against diffusion-based and feed-forward NVS methods.

## Strengths

1. **Novel application of AR models to NVS with camera control.** The paper is the first to demonstrate that decoder-only causal transformers can be effectively adapted for view synthesis, addressing the natural sequential structure of camera trajectories. This opens a new direction for world models that require incremental, causal generation.

2. **Well-motivated design choices for AR NVS challenges.** The three core challenges—temporal consistency, 3D camera conditioning, and bi-directional spatial context—are each addressed with principled components: a video tokenizer (FSQ-based), a camera autoencoder with geometric losses, and spatial-only token permutation. The ablation studies convincingly validate each design decision.

3. **Competitive quantitative results with strong perceptual metrics.** On RealEstate10K, ARSS achieves the best LPIPS (0.269) and competitive PSNR (19.02) and FVD (50.51). The error accumulation analysis shows that ARSS maintains quality much longer along camera trajectories than baselines, demonstrating the benefit of causal generation.

4. **Generalization to zero-shot and out-of-distribution inputs.** The method performs well on the DL3DV benchmark and on AI-generated images (Figure 5), indicating practical robustness.

## Weaknesses

### Major

1. **Mixed quantitative performance; claims of "outperforming" state-of-the-art are overstated.** On ACID, ARSS has significantly worse FID (47.76 vs. SEVA's 33.16) and comparable FVD (54.60 vs. 53.69). On RealEstate10K, SSIM (0.624) is notably lower than SEVA (0.670) and FID is slightly worse (47.60 vs. 46.98). The paper attributes these gaps to minor geometric inconsistencies, but the distributional metrics suggest a systemic trade-off that is not fully explained. The claim "outperforms current state-of-the-art methods" should be tempered.

2. **Limited demonstration of the causal advantage.** The paper asserts that causal generation enables incremental extension and reuse without joint re-generation, but the experiments only show standard fixed-trajectory evaluation. No experiment compares ARSS with diffusion methods on a scenario where the trajectory is extended or new observations are added incrementally. The error accumulation analysis is informative, but it does not isolate the causal benefit over a non-causal method applied to the same trajectory.

3. **Training details and dependencies are under-specified.** The video tokenizer (VidTok) and camera autoencoder appear to be pre-trained separately; it is unclear whether they are frozen or fine-tuned during the AR transformer training. The camera autoencoder loss (Eq. 5) uses weights λ1–λ4 but these are not reported. The tokenizer's temporal compression (5 frames from 17) means only 5 causal steps are generated, which may limit the significance of the causal structure for long trajectories.

### Minor

1. **Token order permutation analysis could be more thorough.** The ablation shows that spatial-only permutation is best, but the paper does not analyze how the random permutation interacts with the camera tokens as positional instructions—specifically, whether the camera tokens fully compensate for the lost spatial order, or whether some spatial structure is implicitly learned.

2. **Inconsistent metric emphasis.** The paper highlights LPIPS improvements (e.g., -21% on Re10K) but does not discuss the negative results (SSIM, FID) with equal depth. A more balanced discussion would strengthen the presentation.

### Trivial

3. **Equation formatting issues.** Eq. (3) is standard, but the formulation in Eq. (7) appears incomplete or ambiguous (the targets are not clearly separated from the inputs). These do not affect understandability significantly.

## Nice-to-Haves

- A direct comparison of the causal generation paradigm to a non-causal method on an incremental setup (e.g., extending the trajectory by adding new views after generation).
- Reporting inference speed or computational cost per frame, which is valuable for practitioners considering AR vs. diffusion models.
- Analysis of token fidelity: how often do generated tokens fall outside the codebook distribution compared to the tokenizer's reconstruction?

## Novel Insights

Beyond the paper's own contributions, the key insight is that pure causal generation can be made effective for 2D novel views by disentangling spatial and temporal causality—preserving temporal order while randomizing spatial order to match the bi-directional nature of images. This suggests that AR visual generation need not strictly follow raster or spatial orders; dense 3D positional condition tokens (from camera raymaps) can serve as proxy for spatial structure, allowing the model to learn spatial coherence purely from the causal cross-attention to camera tokens. This principle may apply to other 3D-conditional generation tasks.

## Suggestions

1. Relax the claim "outperforms" to "achieves competitive performance, particularly in perceptual quality, while offering causal generation capabilities."
2. Provide a controlled experiment where causal vs. non-causal inference on the same model (e.g., by removing temporal permutation during generation) demonstrates the causal advantage more directly.
3. Report the camera autoencoder loss weights and whether the tokenizer is fine-tuned, to improve reproducibility.

## Score and Decision

**Score:** 6  
**Decision:** Borderline Accept  

The work presents a novel and well-motivated approach to NVS using AR models, with sound ablations and competitive results. The mixed quantitative performance on distributional metrics and the limited explicit demonstration of the causal advantage prevent a higher score, but the novelty and potential impact on world modeling directions justify acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>