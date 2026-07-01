## Summary

This paper introduces DPG, a unified framework for "imperfect-label guidance" tasks that span weak-label guidance (e.g., style transfer) and degraded-label guidance (e.g., image super-resolution and deblurring). The key ideas are: (1) **data knowledge integration** – injecting noisy versions of the imperfect label into early steps of reverse diffusion to provide rich task-relevant information, and (2) **process knowledge integration** – a progressive alignment loss that enforces the prediction at each denoising step to be closer to the label than the previous step, mitigating cumulative error. Experiments on style transfer, super-resolution, and deblurring show consistent improvements over a wide range of baselines in both qualitative and quantitative metrics.

## Strengths

1. **Novel problem framing**: The paper formally analyzes the gap between weak-label and degraded-label guidance tasks, identifying differences in data content validity and task objectives as barriers to a unified framework. This conceptual framing is valuable and motivates the work well.

2. **Simple yet effective method**: The proposed integration of data knowledge (diffused label injection) and process knowledge (progressive margin loss) is technically straightforward and does not require task-specific architectural modifications. The ablation study confirms both components contribute positively.

3. **Broad empirical validation**: Experiments cover three diverse tasks (style transfer, super-resolution, deblurring) with both qualitative and quantitative comparisons against many recent methods (e.g., StyleShot, FlowDPS, DMAP). DPG achieves leading or competitive results across all tasks, demonstrating its generalizability.

4. **Clear writing and figures**: The paper explains the motivation for data and process knowledge clearly, and Figures 1–2 provide helpful visualizations of the framework. The main ideas are accessible.

## Weaknesses

### Major

1. **Incremental technical contribution**: The "process knowledge" is a simple margin-based loss that encourages monotonic improvement of the reconstruction loss over steps (`max(L1(z_{0|t-1},y) - L1(z_{0|t},y) + margin, 0)`). This is a straightforward application of existing ideas (e.g., triplet losses, monotonic constraints) to the diffusion denoising path. The paper does not provide theoretical justification or analysis of why this should work beyond the intuitive argument against error accumulation. The novelty of this component is limited.

2. **Computational cost and efficiency not addressed**: The method requires (a) running two parallel forward passes for data knowledge (Eq. 7), (b) computing gradients w.r.t. the latent prediction `z_{0|t}` via backpropagation through the decoder at every step (Eq. 9), and (c) an additional gradient update for process knowledge (Eq. 11). This introduces significant computational overhead compared to standard sampling. The paper provides no runtime comparison or complexity analysis, making it difficult to assess practical applicability.

3. **Unfair or incomplete baseline comparisons**: Several methods marked with asterisks in Figure 4 (FPS-SMC, SITCOM, DOC, TFG, FreeDom) operate in pixel space, while DPG operates in latent space. Direct visual comparison is questionable due to different operating spaces. Moreover, baselines like TFG and FreeDom are general loss-guidance methods not designed for these specific inverse problems; their very poor quantitative results (e.g., PSNR 10.8 for FreeDom in super-resolution) may be expected and do not strongly validate DPG's superiority over dedicated methods.

4. **Overclaimed novelty**: The statement "this paper is the first study to analyze the gap between weak-label and degraded-label guidance tasks and to propose a unified approach to bridge it" is overstated. Prior work on unified frameworks for diffusion-based inverse problems (e.g., DPS, RedDiff, DDNM) already addresses multiple degraded-label tasks. While style transfer is less common in those frameworks, the claim of "first" is too strong, and the paper does not adequately position itself against these existing unified inverse problem solvers.

### Minor

5. **Figure 3 is poorly explained**: The x-axis is labeled "Sample Size (1 to 5)" but the text describes it as showing the effect of process knowledge on a single example. It is unclear what "sample size" refers to (number of iterations? different test images?). The curves show "TIG" vs "TIG with process knowledge" but "TIG" is not defined in the caption or main text. This makes the figure hard to interpret.

6. **Quantitative ablation table has formatting errors**: In Table 2, the first column for style transfer shows "PSNR ↑" and "SSIM ↑" as row labels, which appear to be copy-paste errors from the other blocks. The actual metrics should be "Text Score, Style Loss, CLIP Loss". This suggests careless formatting.

7. **Limited analysis of hyperparameter sensitivity**: The method introduces several weighting factors (`α_data, γ_data, α_margin, η_1, η_2`) and the number of early steps for data knowledge injection. No ablation or sensitivity analysis is provided for these choices, casting doubt on how easy the method is to tune across different tasks.

### Trivial

8. The paper uses "imperfect-label guidance tasks" as an umbrella term but does not cite or discuss relevant taxonomies of condition types or guidance quality in diffusion models.

## Nice-to-Haves

- A comparison of inference time or FLOPs against baseline methods to contextualize computational overhead.
- An experiment showing whether process knowledge alone can be applied to existing loss-guided methods (e.g., TFG) to improve them, which would strengthen the claim of generality.
- A theoretical or empirical analysis of the margin parameter `α_margin` and how it trades off improvement rate vs. stability.

## Novel Insights

The paper's primary insight—that injecting noisy label data into early reverse diffusion steps acts as a soft data prior without requiring task-specific constraints—is practically useful and general. The secondary insight of using a monotonic improvement constraint across denoising steps to reduce error accumulation is also sensible, though similar in spirit to curriculum learning or ranking losses. The combination of both strategies across distinct imperfect-label tasks is empirically validated but does not yield a surprising new theoretical understanding of diffusion guidance.

## Suggestions

1. Provide a runtime/number-of-NFE comparison against the most competitive baselines (e.g., DMAP, FlowDPS) to help readers assess the efficiency vs. quality trade-off.
2. Clarify Figure 3, define "TIG" (presumably "task-independent guidance"?), and explain the x-axis. Consider using a more informative x-axis like "denoising step" or "iteration".
3. Fix the formatting of Table 2 so that the metric names match the reported task.
4. Discuss limitations: e.g., the method assumes access to an explicit label `y` in pixel space (for the loss), and may not work for tasks without a well-defined reconstruction loss (e.g., text-driven generation without a target image).
5. Add an experiment with a Transformer-based diffusion backbone (e.g., DiT) to support the claim of model-agnosticism.

## Score and Decision

The paper tackles an interesting unification problem, proposes a simple method that works across multiple tasks, and provides extensive empirical support. However, the technical novelty of the "process knowledge" is limited, the computational cost is not addressed, and some comparison choices weaken the claims. Given the ICLR 2026 distribution where most papers score around 4–6, this paper is solid but not outstanding. It merits a borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>