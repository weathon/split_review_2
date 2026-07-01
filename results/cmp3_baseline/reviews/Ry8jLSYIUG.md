## Summary

This paper provides theoretical bounds on watermarking capacity under PSNR (ℓ₂) constraints, with and without linear robustness constraints (crop, rotation, JPEG), showing that current deep-learning-based watermarking models operate orders of magnitude below these bounds. The authors then conduct controlled experiments that isolate the cause: even in the minimal setup of a single gray image with only a PSNR constraint, state-of-the-art models like Video Seal fail to reach the predicted capacity, while simple linear or handcrafted embedders succeed. Finally, they scale Video Seal to create Chunky Seal, which achieves 4× the capacity (1024 bits) of prior work while maintaining comparable image quality and robustness, yet remains far from the theoretical limits—demonstrating that current architectures, not fundamental constraints, are the bottleneck.

## Strengths

- **Important question and clear framing**: The paper directly asks whether watermarking has reached its fundamental limits, a timely and impactful question that the community needs answered. The "five possible explanations" taxonomy provides a clean structure for investigation.
- **Novel theoretical bounds**: The geometric approach (counting integer lattice points inside the intersection of a ball and a cube) yields clean, interpretable upper bounds that go beyond prior information-theoretic methods which relied on restrictive assumptions like Gaussian noise or small perturbations. The analysis covers the central cover case, the worst-case corner cover, and linear robustness constraints.
- **Rigorous controlled experiments**: The single-gray-image PSNR-only setup is elegant—it removes data distribution, perceptual losses, and augmentations, isolating the model architecture as the key variable. The fact that Video Seal fails to embed 1024 bits while a linear layer and a handcrafted model succeed is strong evidence for architectural limitations, not fundamental capacity ceilings.
- **Positive demonstration of improvement**: Chunky Seal shows that scaling up a modern architecture does yield 4× higher capacity with comparable quality and robustness, providing concrete proof that current methods are suboptimal and that meaningful progress is possible.
- **Actionable sanity checks**: The proposed criteria for Pareto-optimal watermarking (linear scaling with image size, outperforming linear/handcrafted baselines, predictable drops under augmentations) give the community clear targets for future work.

## Weaknesses

### Major
1. **Heuristic robustness bounds (Bounds 10–12) are not validated as achievable**: The paper admits these are heuristic and provides a conservative lower bound (Bound 13) that is much lower. This means the claim that "robustness constraints cannot fully explain the performance gap" rests on bounds whose achievability is unproven. The handcrafted embedder works only for the PSNR-only case; no constructive scheme is given that approaches the heuristic bounds under robustness. Thus, the real gap under realistic robustness constraints remains uncertain. While Chunky Seal provides empirical evidence that improvement is possible, the theoretical gap under robustness is not as firmly established as the PSNR-only gap.

2. **The theoretical analysis is limited to linear transformations and a linearized JPEG**: Real-world watermarking must survive non-linear augmentations (median filtering, gamma correction, combinations of attacks, etc.). The paper acknowledges this but only partially addresses it by removing all augmentations in the controlled experiments. The possibility remains that the combination of realistic, non-linear robustness constraints and perceptual constraints could explain a larger portion of the gap than suggested.

3. **The practical demonstration (Chunky Seal) is extremely large (1.8B parameters)**: While the paper explicitly states this is not intended as a practical solution, the extreme scale limits the strength of the demonstration that "better performance in practice is possible." Achieving high capacity via model scaling is not the same as achieving it through architectural innovation, which the paper itself argues is needed. A smaller, more efficient model achieving similar capacity gains would have been a stronger proof of concept.

### Minor
- **PSNR as the sole quality metric**: The bounds are derived purely under PSNR constraints. While the controlled experiments match this, the conclusion that "our models are significantly underperforming" in the realistic setting relies on PSNR-bounds, even though practitioners care about perceptual quality. The paper acknowledges this (point B in the five explanations) but does not fully resolve it.
- **The dataset-distribution analysis (Section 2.6) is brief and relies on VQ-VAE codebook capacity as an upper bound**: Using codebook capacity of a VQ model to bound the number of perceptually distinct images is reasonable but crude. The reduction of 10,240 bits on top of the 1 bpp loss is plausible but not rigorously derived.
- **Table formatting issues (parser artifact)**: The message size column in Table 1 has broken alignment, but this is not a paper flaw.

### Trivial
- The paper occasionally uses "orders of magnitude" loosely—the gap at 40 dB is roughly 1000×, which is three orders of magnitude, consistent with the claim.

## Nice-to-Haves
- A constructive scheme (even a simple one, e.g., based on the handcrafted model with error-correcting codes) that approaches the heuristic robustness bounds would greatly strengthen the paper's conclusion that "robustness cannot explain the gap."
- An analysis of how the bounds change under a perceptual metric like LPIPS or DISTS (even if approximate) would connect the theory more tightly to practice.
- An ablation showing that a smaller, more efficient architecture can achieve similar capacity gains (to strengthen the message that scaling is not the only path).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
- Strengthen the robustness-bounds contribution by either (a) providing a constructive coding scheme that achieves the heuristic bounds (even on synthetic images), or (b) proving a tighter lower bound that holds under a broader class of transformations, or (c) more explicitly stating that the heuristic bounds are upper bounds on what is achievable and may overestimate true capacity.
- Clearly separate the two settings (PSNR-only vs. PSNR+robustness) when summarizing the gap: for the PSNR-only case the gap is rigorously established; for the robustness case the gap is suggestive but less rigorous.
- In the discussion, tone down the "orders of magnitude" language for the robustness case to match the evidence level.

## Score and Decision

The paper makes a strong contribution by reframing the watermarking problem and providing clean theoretical limits, clever experimental controls, and a concrete demonstration that higher capacity is achievable. The major weakness (unvalidated heuristic robustness bounds) is openly acknowledged and partially compensated by the Chunky Seal experiment and the conservative lower bound. The paper is well-written, thorough, and addresses an important community question. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>