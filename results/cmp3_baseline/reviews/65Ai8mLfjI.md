## Summary

This paper investigates the role of pooled text embeddings (global text conditioning) in diffusion transformers for text-to-image/video generation. The authors first demonstrate that in many modern models, the pooled CLIP embedding has negligible impact on generation quality when used conventionally. However, they propose "modulation guidance"—a training-free technique that amplifies the pooled embedding's effect by extrapolating between positive and negative prompt embeddings in the modulation space—which yields significant improvements in aesthetics, complexity, object counting, hands correction, and other aspects across multiple state-of-the-art models.

## Strengths

- **Clear and well-motivated research question**: The paper addresses a timely and practical question about whether global text conditioning is necessary in modern diffusion transformers, given the trend toward discarding it. The analysis is thorough and the findings are non-trivial.
- **Simple yet effective method**: Modulation guidance is training-free, requires negligible computational overhead, and can be applied to existing models without modification. The dynamic variant further improves the quality-fidelity trade-off. This practical simplicity is a major strength.
- **Comprehensive evaluation across diverse tasks and models**: The method is validated on text-to-image (FLUX, SD3.5, HiDream, COSMOS), text-to-video (Hunyuan, CausVid), and image editing (FLUX Kontext), with both automatic metrics and human evaluation. The inclusion of models that originally lack CLIP (COSMOS, CausVid) and the fine-tuning strategy to add it back is particularly thorough.
- **Insightful analysis of what modulation guidance does**: The attention map analysis (Figure 4) provides mechanistic understanding, showing that guidance shifts attention toward relevant tokens (e.g., "hands"), which explains the improvement in specific tasks like hands correction.

## Weaknesses

### Major

- **Limited novelty relative to prior work**: The core idea of using positive/negative prompt extrapolation in feature space is very similar to attention guidance methods (Chen et al., 2025; Hong et al., 2023; Ahn et al., 2025) and the modulation-based editing approach of Garibi et al. (2025). The paper's main novelty is applying this idea to the modulation space rather than attention space, and using it for general quality improvement rather than editing. While this is a valid contribution, the incremental nature should be acknowledged more explicitly.
- **The "training-free" claim for CLIP-free models is misleading**: For models like COSMOS and CausVid that lack a pooled embedding, the authors fine-tune a small MLP (4K iterations for COSMOS, 1K for CausVid) to introduce it. This is not training-free and requires access to the model's training pipeline and synthetic data generation. The paper should clearly separate the training-free case (models with existing CLIP) from the fine-tuning case.
- **Lack of comparison with simple baselines**: The paper compares against Normalized Attention Guidance and Concept Sliders, but does not compare against simply using a more descriptive prompt or LLM-enhanced prompts alone (though it does show that modulation guidance can be combined with LLM prompts). A more direct baseline would be: does simply appending "high quality, detailed" to the prompt achieve similar gains? The paper should address whether modulation guidance offers something beyond prompt engineering.
- **Human evaluation details are insufficient**: The paper mentions side-by-side comparisons with annotators on four criteria (relevance, aesthetics, complexity, defects) but does not report the number of annotators, inter-annotator agreement, or whether the annotators were blinded to the method. These details are critical for assessing the reliability of the human evaluation results.

### Minor

- **The analysis of CLIP's inactivity is somewhat superficial**: The paper shows that removing CLIP has little effect on long prompts for FLUX and no effect for HiDream, but does not investigate *why* this happens. Is it because the modulation MLP learns to ignore the CLIP input? Is it because T5 already captures all necessary information? Understanding the root cause would strengthen the paper.
- **Dynamic modulation guidance is under-explored**: Only one simple variant (step function over layers) is used in the main experiments. The paper mentions other strategies in Appendix B but does not systematically compare them. Given that dynamic guidance is claimed to be a contribution, more analysis would be beneficial.
- **The image editing results are weak**: Only qualitative examples are shown for FLUX Kontext, with quantitative results relegated to Appendix F. The editing task seems like an afterthought and the results are not convincing enough to be a core contribution.

### Trivial

- The paper uses "PadScore" in Figure 3(a) instead of "PickScore" (likely a typo from the OCR/parsing process).

## Nice-to-Haves

- A systematic study of how the choice of positive/negative prompts affects performance for each aspect (aesthetics, complexity, etc.). The paper provides the prompts in Appendix D but does not analyze sensitivity to prompt wording.
- An investigation of whether modulation guidance can be applied to other modalities (e.g., text-to-3D, text-to-audio) to demonstrate generality.
- A discussion of potential failure cases or when modulation guidance might hurt performance (beyond the brief mention in Appendix C about high guidance scales).

## Novel Insights

Beyond the paper's own contributions, the most interesting insight is that the pooled text embedding, which appears functionally redundant in modern diffusion transformers, actually encodes semantically meaningful directions that can be amplified for quality improvement. This suggests that these models implicitly learn a rich semantic manifold in the modulation space that is not fully utilized during standard generation. The finding that attention shifts toward relevant tokens under modulation guidance (Figure 4) provides a mechanistic link between global conditioning and local attention, which is a genuinely useful observation for understanding how these models work.

## Suggestions

- Clearly separate the "training-free" results (models with existing CLIP) from the "fine-tuning" results (models where CLIP is added back). The current presentation conflates these two scenarios.
- Add a baseline where prompts are simply augmented with quality-descriptive words (e.g., "high quality, detailed, aesthetic") to demonstrate that modulation guidance offers benefits beyond prompt engineering.
- Provide more details on the human evaluation setup: number of annotators, instructions given, whether they were blinded, and inter-annotator agreement metrics.
- Consider adding a simple ablation: what happens if you use random vectors instead of CLIP embeddings for the positive/negative prompts? This would test whether the effect is truly semantic or just a generic perturbation.

## Score and Decision

The paper addresses a relevant and timely question, proposes a simple and effective method, and provides thorough evaluation across multiple models and tasks. The main weaknesses are the limited novelty relative to prior guidance methods and the misleading "training-free" claim for CLIP-free models. However, the practical utility of the method and the quality of the evaluation outweigh these concerns. The paper is a solid contribution that will be of interest to the community.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>