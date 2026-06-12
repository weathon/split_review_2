## Summary

The paper proposes UniMoD, a task-aware token pruning method for unified multimodal transformers (models that handle both generation and understanding). Through an empirical analysis of attention weights, layer importance, token redundancy (using the ARank metric), and cross-task interactions in models like Show‑o and Emu3, the authors observe that token redundancy varies significantly across tasks and layers. Based on these insights, they introduce separate routers per task and a layer switch module that uses ARank to decide which layers to sparsify and at what ratio. UniMoD reduces training FLOPs by 15% for Show‑o (1.4B) and 40% for Emu3 (8.5B) while maintaining or improving performance on standard multimodal understanding and text-to-image generation benchmarks.

## Strengths

- **Comprehensive empirical analysis.** The paper systematically examines attention weight patterns, layer importance, token redundancy (via ARank), and task interactions across several unified transformers (Show‑o, JanusFlow, Emu3, Lumina‑mgpt). These experiments provide clear, actionable insights that motivate the task‑aware pruning design.
- **Well‑motivated, practical method.** UniMoD’s task‑specific routers directly address the observed heterogeneity in redundancy across tasks. The layer‑switch module based on ARank is a principled way to decide which layers to prune, avoiding ad‑hoc selection.
- **Solid experimental validation.** Results on two representative unified transformers (Show‑o and Emu3) show that UniMoD saves substantial FLOPs (15–40%) while delivering performance competitive with the full dense baseline. Ablations confirm that both the task‑aware router and layer‑switch module are essential.
- **Generality and scalability.** The method extends beyond two tasks (e.g., pure text, Sec. A.12) and adapts to pure diffusion models (DiT, PixArt‑α). It also becomes more efficient at larger model scales (20% FLOP reduction for an 8B model vs. 15% for 1.4B).
- **Clear presentation of findings.** Observations 1–5 are well‑articulated and directly linked to the proposed design. Figures (attention weights, ARank curves, token competition) effectively support the narrative.

## Weaknesses

### Fatal
None.

### Major
- **Performance trade‑offs not fully characterized.** While the paper claims “maintaining or improving performance,” some understanding benchmarks show non‑negligible degradation. For Show‑o, GQA drops from 56.3 to 54.5; for Emu3, POPE drops from 76.0 to 74.7. The paper would benefit from a more rigorous discussion of when the method loses quality and whether task‑specific thresholds can be tuned to avoid such drops.
- **Limited comparison with alternative efficient methods.** The baselines are only “EarlyExit” and “Interleaved Layer Skipping.” More recent token‑level pruning methods (e.g., ToMe for multimodal models, or cross‑layer redundancy reduction like FastV) are not compared. Without showing that UniMoD outperforms or is competitive with other sparse‑computation approaches, the empirical contribution is less sharp.
- **Dependence on ARank for layer selection.** The layer‑switch module computes ARank on a small set of samples (50 per task) to decide which layers to convert. The paper does not analyze the stability of this selection across different random seeds or data subsets, nor does it discuss the overhead of this preliminary step. If the optimal layer assignment changes during training, the fixed selection may become suboptimal.

### Minor
- **Emu3 results use different training data.** The authors acknowledge that because the official Emu3 code/data are not public, they finetune using LLaVA‑v1.5‑mix‑665K and Show‑o’s T2I data. Consequently, the absolute numbers differ from the original Emu3 paper, making it harder to gauge the true efficiency‑quality trade‑off. A controlled comparison on the original data (if possible) would strengthen the claim.
- **UniMoD adds extra parameters (routers) per task.** While the number is small, the paper does not quantify this overhead or discuss whether it could be amortized. The FLOPs savings are clear, but parameter count is not reported.
- **Section ordering.** The empirical analysis (Section 3) is rich, but the method (Section 4) is relatively brief. Some design choices (e.g., why the last 12 layers are chosen for Show‑o, why capacity is scaled from 1 to 0.2 for MMU) could be better justified by connecting them more explicitly to the ARank observations in that section.

### Trivial
- Figure 1(b) is partially redundant with the text; the observations are already stated.
- Table 1 could be moved to an appendix to avoid breaking the flow of the main analysis.

## Nice-to-Haves
- Investigate whether the layer‑switch module can be made dynamic (e.g., learned jointly with the routers) so that pruning decisions adapt during training.
- Evaluate UniMoD on other recent unified models like JanusFlow or Lumina‑mgpt to further demonstrate generalization.
- Provide a sensitivity analysis of the pruning ratios estimated from ARank (e.g., how much does performance change if the ratio is varied by ±10%?).

## Novel Insights

Beyond the paper’s own contributions, the most salient insight is that in unified multimodal transformers, token redundancy is not a monolithic property of the model but is instead strongly decoupled along both task and layer axes. The competitive pruning experiment (Sec. 3.4) reveals that generation tokens consistently dominate understanding tokens when they compete for compute, even though joint training does not degrade individual task performance. This suggests that a single token‑importance measure learned across all tasks is biased; the method’s success follows directly from restoring per‑task control over which tokens are processed. The ARank analysis further shows that redundancy is not uniformly distributed: early layers for understanding tasks can be highly redundant, while later layers for generation retain more structure. These patterns are likely general across multimodal models that mix autoregressive and diffusion objectives, and they provide a principled guide for future efficient architecture design.

## Suggestions
- Compare UniMoD with at least one well‑known token‑level pruning method from vision‑language models (e.g., FastV or LLaMA‑Pruner adapted to this setting) to strengthen the baseline comparison.
- Clarify whether the reported FLOPs savings account for the additional computation of the routers themselves and the ARank selection stage.
- Include a small experiment that varies the ARank sample size (e.g., 10, 50, 200) to demonstrate that the layer choice is robust.

## Score and Decision
Score: 8

Decision: Accept

The paper provides a thorough empirical analysis of token redundancy in unified multimodal transformers and introduces a well‑motivated, task‑aware pruning method that delivers meaningful FLOPs reductions (up to 40%) with minimal quality loss on standard benchmarks. While a few aspects (baseline coverage, sensitivity analysis) could be improved, the work is sound, clearly presented, and offers practical value to the community. The method is general and scales well, making it a solid contribution to efficient multimodal training.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>