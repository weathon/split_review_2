## Summary

This paper proposes SpatialBoost, a three-stage framework that enhances pre-trained vision encoders with 3D spatial knowledge by converting dense spatial information from 2D images into linguistic form and injecting it through an LLM. The key technical contributions are: (1) a dual-channel attention mechanism that adds a parallel attention branch with a learnable mixture factor to prevent catastrophic forgetting during fine-tuning, and (2) a multi-turn hierarchical spatial reasoning dataset (pixel-level → object-level → scene-level) constructed from single-view and multi-view images using external depth, segmentation, and 3D reconstruction models. The method is evaluated across an unusually broad range of tasks (depth estimation, semantic segmentation, 3D scene understanding, robot learning, image classification/retrieval) and four backbone encoders, showing consistent improvements.

## Strengths

1. **Broad and systematic evaluation across diverse tasks and backbones.** The paper evaluates on depth estimation (2 datasets × 2 protocols), semantic segmentation (2 datasets × 2 protocols), 3D scene understanding (Lexicon3D with 4 sub-tasks), robot learning (4 domains), and image classification/retrieval (4 datasets), across 4 backbone encoders (OpenCLIP, SigLIPv2, DINOv2, DINOv3). The breadth is substantial and unusual for a representation learning paper.

2. **Consistent positive results across all settings.** Every backbone improves on every task with SpatialBoost. The pattern is consistent (no cherry-picked task/backbone pairs where it works), which supports the claim that the method injects genuinely useful spatial knowledge.

3. **Well-designed ablations that isolate individual components.** Table 6 (LLM vs. pixel-level supervision heads), Table 7 (multi-turn order, single vs. multi-view data), Table 8 (vs. simple post-training), and Figure 6 (dual-channel vs. LoRA vs. full fine-tuning) collectively tell a coherent story about what contributes to the gains. The forward-hierarchical ordering outperforming reverse/random orders (Table 7) is a particularly informative result.

4. **Dual-channel attention is a clean, empirically validated design.** Adding a parallel attention branch with a learnable, zero-initialized mixture factor that preserves original frozen weights while learning new spatial features is simple and effective. Figure 6 shows it avoids the catastrophic forgetting that full fine-tuning and LoRA cause on classification tasks.

## Weaknesses

### Fatal
None.

### Major

1. **Missing clarification on train/evaluation data separation for ScanNet-based experiments.** The paper constructs multi-view training data using "3D dataset (Jensen et al., 2014; **Dai et al., 2017**; Mildenhall et al., 2021; Barron et al., 2022)" (line 162). Dai et al. (2017) is ScanNet. The evaluation in Table 3 uses Lexicon3D, a benchmark built on **ScanNet scenes**, evaluating ScanQA, SQA3D, and ScanRefer — all derived from ScanNet. The paper does **not** state whether the ScanNet scenes used for training data construction are from a disjoint split than those used in the Lexicon3D evaluation. This omission is consequential: if the same scenes appear in both the training data and the feature-probing evaluation, the reported gains — particularly the dramatic jumps (e.g., SigLIPv2 3D semantic understanding from 6.9 to 54.9 mIoU, RR@0.05m from 47.8% to 86.4%) — could be inflated by the model having been exposed to those specific scenes during fine-tuning. **This does not mean contamination occurred, but the paper must explicitly clarify the split separation for its core empirical claims to be interpretable.**

### Minor

2. **Lack of variance or statistical significance for most results.** Tables 1, 2, 3, and 5 report only point estimates without standard deviations, confidence intervals, or significance tests. Table 4 (robot learning) is the only exception with ± ranges. While single-run evaluation is standard in this setting, the absence of variance estimates makes it difficult to assess whether smaller improvements (e.g., DINOv3 51.4→54.9 on SQA3D, or ImageNet gains of ~1–2%) are meaningful or within evaluation noise. Adding variance estimates would materially strengthen evidential quality.

3. **Computational cost is not discussed.** The pipeline involves: running Depth Pro, SAM, and 3D reconstruction on 300K+ images; calling GPT-4o for question generation; three training stages (projector alignment, visual instruction tuning with a 7B LLM, and dual-channel attention fine-tuning through the LLM). The paper provides no discussion of GPU-hours, training time, or inference overhead from the dual-channel attention (which doubles attention parameters per layer). This omission makes it difficult to assess the method's practical cost-benefit trade-off.

4. **The "Simple FT" baseline in Table 8 is underspecified.** The paper describes it as fine-tuning with "their original pre-training objectives" without specifying what this means concretely for different architectures (OpenCLIP uses contrastive loss, DINOv2 uses self-distillation). The training data, budget, and protocol are not described, which limits interpretability of this comparison.

5. **No discussion of limitations or failure cases.** The paper presents only successes. The method's reliance on upstream models (Depth Pro, SAM, 3D reconstruction) means errors in those models propagate — this is not analyzed. The paper would benefit from acknowledging settings where SpatialBoost yields marginal or negative improvements.

6. **Table 6 ablation compares supervision signals that differ in both data and supervision type.** The LLM-based fine-tuning uses the full multi-turn VQA dataset (pixel, object, scene questions + captions), while the pixel-level baselines (linear depth, linear seg, SAM decoder, VGGT decoder) use only their respective single-target data. The result that LLM supervision works better could reflect richer data rather than language-based supervision per se. A more controlled comparison (e.g., training the LLM on only pixel-level depth QA data) would strengthen the claim that "language provides superior dense information transfer." As presented, the table is informative but does not fully isolate the factor the paper attributes it to.

### Trivial
None.

## Nice-to-Haves
- Adding standard deviations to Tables 1, 2, 3, and 5 would improve evidential quality.
- Including a controlled ablation in Table 6 that matches data scope across supervision types.
- Reporting GPU-hours or training time for the full pipeline.
- Discussing what kinds of scenes or spatial relationships SpatialBoost fails to improve, and analyzing how errors propagate from upstream models.

## Removed Points
- **"CoT framing is misleading" (from reviewer):** Removed because it misreads the paper's contribution. The paper's stated goal is representation learning, not building a spatial reasoning model. The "Chain-of-Thought" terminology describes the hierarchical structure of the dataset (pixel→object→scene), which is a valid and standard use of the term — the model is trained via SFT on these multi-turn conversations. The distinction the reviewer draws ("reasoning is baked into the dataset, not learned by the model") is how CoT training works in general.
- **"SA1B may contain evaluation images" (part of data contamination criticism):** Significantly weakened/absorbed into the ScanNet point. The claim that SA1B "is known to contain images that overlap with standard evaluation datasets including ImageNet, ADE20K, Pascal VOC" is an assertion by the reviewer without evidence in the paper. Unlike the ScanNet case (where the same *dataset* is cited for both training and evaluation), the SA1B→ImageNet/ADE20K/Pascal VOC overlap is speculative. For a 100K random subset of 11M diverse images, the practical contamination risk is low, and the consistent pattern of improvements across many tasks makes a single-dataset contamination explanation unlikely.
- **"Missing citation for line 17 claim":** Removed as a trivial nitpick about a general motivating statement.
- **"Table 4 has variance but others don't":** Already captured in weakness #2 above.
- **"No inference-time analysis of dual-channel attention FLOPs":** Merged into computational cost weakness (#3).

## Novel Insights

Beyond the paper's own contributions, the reviews surface one genuinely useful observation that the paper does not make explicit: the hierarchical ordering of spatial reasoning in the training data (pixel→object→scene) causally matters for representation quality (Table 7), and this effect is distinct from the data content itself. This suggests that how spatial knowledge is *structured* during training — not just what knowledge is provided — is an important design dimension for representation learning. The paper documents this empirically but does not discuss the implications for curriculum design or multi-task representation learning more broadly.

## Suggestions

1. **(Critical)** Explicitly state the split separation between ScanNet scenes used for training data construction and those used in the Lexicon3D evaluation. Provide details on which specific scenes/splits were used in each setting.
2. Add standard deviations to all main result tables (1, 2, 3, 5) to allow readers to assess the significance of the reported improvements.
3. Discuss training cost (GPU-hours) and inference overhead of the dual-channel attention mechanism.
4. Add a limitations paragraph acknowledging settings where the method underperforms and analyzing the impact of upstream model errors.
5. Specify the "Simple FT" baseline (Table 8) more concretely — what objective, data, and training budget were used for each backbone?

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>