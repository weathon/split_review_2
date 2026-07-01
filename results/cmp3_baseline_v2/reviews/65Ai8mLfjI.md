## Summary

This paper re-examines the role of pooled text embeddings (global text conditioning) in diffusion transformers. The authors first empirically show that the pooled CLIP embedding has minimal impact on generation quality in modern models, being partially inactive in FLUX schnell and fully inactive in HiDream-Fast and COSMOS. However, they propose "modulation guidance"—a training-free technique that amplifies the effect of the pooled embedding by extrapolating between positive and negative prompt embeddings in the modulation space. This approach improves aesthetics, complexity, object counting, and hand correction across multiple text-to-image models (FLUX, SD3.5, HiDream, COSMOS), extends to text-to-video, and can be applied to image editing tasks with negligible computational overhead.

## Strengths

- **Clear research question and systematic analysis**: The paper begins by asking a well-motivated question about whether global text conditioning is necessary, provides clean ablation experiments (zeroing out CLIP embeddings) across multiple models, and finds that the pooled embedding is largely inactive. This diagnostic contribution is valuable for understanding modern diffusion architectures.
- **Practical, simple, and effective method**: Modulation guidance is training-free, requires only selecting positive/negative prompts per task, adds negligible runtime cost (just one extra forward pass of the small MLP), and consistently improves human preference scores (e.g., +22% for object counting, +18% for hands correction, 60-80% win rates for aesthetics/complexity) across multiple state-of-the-art models.
- **Strong experimental breadth**: The method is validated on 5 text-to-image models (including one CLIP-free model that is fine-tuned), 2 text-to-video models, and an image editing task, using both human evaluation and 5 automatic metrics. The inclusion of dynamic modulation guidance (per-layer scheduling) further demonstrates careful design.
- **Interpretability analysis**: The paper provides mechanistic insight into why modulation guidance works—showing that it sharpens attention maps on relevant tokens (e.g., "hands")—which strengthens the claim that the method is not just a heuristic but has a principled effect.

## Weaknesses

### Major

- **Fine-tuning for CLIP-free models is under-explained and may limit reproducibility**: The paper fine-tunes COSMOS and CausVid to introduce the pooled embedding, training a small MLP on 500K synthetic samples with an MSE distillation loss. However, there is insufficient detail about the training hyperparameters, optimizer, learning rate, batch size, and how the synthetic data was generated. Since fine-tuning is a prerequisite for applying the method to CLIP-free models, the lack of reproducibility is concerning. The authors claim "minimal training" but do not provide the recipe needed for practitioners to replicate it.
- **Limited comparison to strong baselines**: The paper compares against only two post-training baselines (Normalized Attention Guidance and Concept Sliders) in the appendix, and notably does not compare against state-of-the-art test-time optimization methods like Attend-and-Excite, layout guidance, or prompt engineering approaches. For object counting specifically, the comparison with LLM-enhanced prompts is mentioned but the results (in Appendix E) are not sufficiently analyzed. A 22% win rate over the original model is good, but without comparison to existing specialized methods, it is unclear whether modulation guidance is state-of-the-art for object counting/hand correction.
- **No theoretical or qualitative bound on when modulation guidance fails**: The paper notes that "excessively high values can overweight the prompt" (Appendix C) but does not provide any analysis of failure modes. For instance, does modulation guidance ever degrade identity preservation, introduce artifacts, or cause concept bleeding? The paper reports a slight drop in defects for COSMOS but does not discuss the conditions under which practitioners should avoid using high guidance scales.

### Minor

- **The claim that the method is "training-free" is slightly misleading for CLIP-free models**: While the core modulation guidance is training-free, applying it to models like COSMOS and CausVid requires a fine-tuning step. The paper should more clearly distinguish between the training-free case (models with existing pooled embeddings) and the fine-tuning case.
- **The dynamic modulation guidance exploration is preliminary**: Only a simple step-function scheduling over layers is tested in the main paper; more complex strategies are relegated to Appendix B. The paper would be strengthened by comparing multiple dynamic strategies head-to-head on the same metric and ablating the choice of layer cutoff.
- **Human evaluation details are sparse**: The paper mentions "annotators" but does not specify how many annotators, whether they were experts, or how inter-annotator agreement was measured. Given that human evaluation is central to the main claims, more transparency is needed.

## Nice-to-Haves

- It would be interesting to see modulation guidance combined with CFG modulation (e.g., dynamic CFG) to test whether the two guidance mechanisms are additive or saturate.
- A small user study comparing modulation guidance against simple prompt engineering (e.g., "high quality, detailed, 4K") would help isolate the benefit of the modulation extrapolation from the benefit of adding descriptive adjectives.

## Novel Insights

The paper's core insight is that the pooled text embedding, despite being largely inert in standard generation, encodes an interpretable direction in the modulation space that can be amplified to steer the model toward more desirable properties. This flips the conventional narrative: rather than treating the pooled embedding as a weak text conditioner, the paper shows it is a latent handle for controllable image quality improvement. The finding that this works for both multi-step and few-step (distilled) models, and that it generalizes across architecture families (FLUX, SD3.5, HiDream, Hunyuan, CausVid), suggests that the modulation space is a universal and under-explored interface for post-hoc model control.

## Suggestions

1. **Provide full fine-tuning details for CLIP-free models**: Include optimizer (AdamW?), learning rate schedule, batch size, number of iterations, GPU requirements, and the exact prompt-to-noise synthesis pipeline. Without this, the fine-tuning step is not reproducible.
2. **Expand baseline comparisons in the main paper**: At minimum, compare against Attend-and-Excite for object counting and a standard prompt engineering baseline (e.g., appending "perfect hands, correct anatomy"). The results in the appendix show modulation guidance outperforms Normalized Attention Guidance by 34%—this is strong evidence that should be featured more prominently.
3. **Add a failure-case analysis or limitation section in the main text**: Currently limitations are in Appendix H. The paper would be stronger if it explicitly discussed when modulation guidance degrades quality (e.g., very high weights, mismatched positive/negative prompts) and provided guidelines for selecting w.
4. **Clarify the human evaluation setup**: Report number of annotators, annotation platform (e.g., Amazon Mechanical Turk, internal), and whether annotators were blinded to the method.

## Score and Decision

The paper addresses a timely and practically relevant question, provides clean diagnostic experiments, and introduces a simple yet effective method that works across multiple state-of-the-art models and tasks. The weaknesses are primarily about missing reproducibility details and limited baseline comparisons, which are addressable. The core contributions are solid.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>