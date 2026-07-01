## Summary

This paper investigates the gap between theoretical watermarking capacity and the performance of current deep learning-based image watermarking methods. The authors derive upper bounds on message-carrying capacity under PSNR and linear robustness constraints, showing theoretical capacities orders of magnitude larger than what current models achieve. They demonstrate that even in simplified settings (single gray image, no augmentations), state-of-the-art models like Video Seal fail to approach these bounds, while simple linear or handcrafted models can achieve much higher capacities. Finally, they present Chunky Seal, a scaled-up version of Video Seal that achieves 4× the capacity (1024 bits) while maintaining comparable quality and robustness.

## Strengths

- **Important and timely research question**: The paper addresses a fundamental question in image watermarking—whether current methods are approaching fundamental limits or if significant room for improvement remains. This is valuable for guiding future research directions.
- **Novel theoretical framework**: The geometric approach to bounding watermarking capacity under PSNR constraints (using box-ball intersection analysis) is elegant and provides concrete, interpretable bounds. The extension to linear transformations via singular value analysis is a reasonable first step.
- **Strong empirical evidence for the gap**: The controlled experiments (single gray image, no augmentations) cleanly isolate the architecture limitation from other confounding factors. The fact that Video Seal fails to learn 1024 bits while a linear model succeeds at 2048 bits is compelling evidence of structural limitations.
- **The handcrafted model achieving near-bound performance** (456,509 bits at 42 dB) convincingly demonstrates that the theoretical bounds are achievable in principle, ruling out the hypothesis that the bounds themselves are unrealistic.

## Weaknesses

### Fatal
None.

### Major
- **The robustness bounds (Bounds 10-12) are heuristic and not formally justified**: The paper acknowledges these are "heuristic bounds" that can both over- and under-approximate true capacity. While the conservative Bound 13 provides a valid lower bound, it is acknowledged as "extremely conservative and unrealistic." This leaves a significant gap in the theoretical contribution—the paper cannot rigorously establish how much robustness constraints actually reduce capacity. The claim that "robustness to geometric transformations and compression significantly reduces the capacity but cannot fully explain the low watermarking capacity" rests on heuristic bounds whose reliability is unclear.
- **Chunky Seal's comparison to Video Seal is not controlled for fairness**: Chunky Seal uses a much larger model (90× larger embedder, 23× larger extractor) and was trained without hyperparameter tuning, while Video Seal was "extensively optimized." The paper attributes the capacity gain to "simple scaling," but this conflates architecture size with training optimization. A fairer comparison would involve training Video Seal at similar scale or training Chunky Seal with Video Seal's original hyperparameters.
- **The practical significance of 1024 bits is unclear**: The paper motivates higher capacity for applications like embedding entire C2PA manifests, but doesn't specify what manifest size is needed. 1024 bits (128 bytes) is still quite small for a full provenance record. The paper would benefit from clarifying what application-relevant thresholds exist.

### Minor
- **The analysis is restricted to PSNR as the sole quality metric**: While PSNR is standard, modern watermarking methods also optimize for perceptual metrics (LPIPS, SSIM). The paper acknowledges this limitation but doesn't explore how perceptual constraints might affect the bounds. The handcrafted model achieving 456,509 bits at 42 dB PSNR may have poor perceptual quality that PSNR doesn't capture.
- **The data distribution analysis (Section 2.6) is somewhat hand-wavy**: Using VQ-VAE codebook size to estimate the number of perceptually distinct images is a rough approximation. The claim that data distribution has "negligible effect" on capacity relies on this approximation and the assumption that all codebook entries could fall in the same PSNR ball.
- **The paper doesn't explore why Video Seal fails to scale**: While the paper demonstrates the failure, it doesn't provide analysis of what architectural components cause the bottleneck (e.g., is it the U-Net bottleneck, the decoder head, the loss landscape?). This would strengthen the call for architectural innovation.

### Trivial
- The paper uses "Chunky Seal" as the name for the scaled model, which is a minor stylistic choice but may be perceived as informal.

## Nice-to-Haves
- An ablation study isolating which architectural changes in Chunky Seal contribute most to the capacity gain (embedder scaling vs. extractor scaling vs. multi-channel watermarking).
- A discussion of whether the theoretical bounds could be tightened by considering more realistic perceptual models (e.g., contrast masking, texture masking).
- Analysis of the computational cost (FLOPs, latency) of Chunky Seal vs. Video Seal to contextualize the trade-off.

## Novel Insights

Beyond the paper's own contributions, the key insight is that **the bottleneck in current watermarking is not the fundamental information-theoretic limit but rather the inductive bias of neural network architectures**. The fact that a linear model outperforms a sophisticated U-Net on the simplest possible task (single gray image, no augmentations) suggests that deep learning architectures for watermarking are not learning the right representations. This parallels findings in other domains where simple baselines outperform complex models on certain tasks, but here it points to a specific architectural deficiency: current models cannot effectively learn to spread information across the full spatial extent of the image. The tiling experiment (32×32 model achieving same capacity as 256×256 model) confirms this spatial inefficiency. This suggests that future progress may require architectures with explicit long-range dependencies or different inductive biases for the embedding task.

## Suggestions
- Strengthen the robustness analysis by either: (a) providing a formal lower bound that is tighter than Bound 13, or (b) clearly delineating which transformations the heuristic bounds are reliable for and which they are not.
- For the Chunky Seal comparison, either train Video Seal at comparable scale or provide an ablation showing that scaling alone (without hyperparameter tuning) is responsible for the gain.
- Add a discussion of what capacity is needed for practical applications (e.g., C2PA manifests, content IDs) to contextualize whether 1024 bits or the theoretical bounds are practically relevant.

## Score and Decision

The paper makes a valuable contribution by rigorously establishing that current watermarking methods operate far below theoretical capacity limits, and by providing strong empirical evidence that this gap is due to architectural limitations rather than fundamental constraints. The theoretical bounds are novel and well-derived for the PSNR-only case. The main weaknesses are the heuristic nature of the robustness bounds and the uncontrolled comparison in Chunky Seal. However, the core claim—that significant capacity improvements are possible—is well-supported by the controlled experiments and handcrafted model. The paper is clearly written and addresses an important question for the community.

Score: 7.0

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>