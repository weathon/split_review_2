## Summary

This paper investigates the role of pooled CLIP text embeddings in modern diffusion transformers, finding that these embeddings are partially or fully inactive in models like FLUX schnell, HiDream-Fast, and COSMOS. The authors then propose "modulation guidance," a training-free technique that repurposes the pooled embedding as a directional correction in modulation space to steer generation toward better properties (aesthetics, complexity, hand correctness, object counting), demonstrating consistent improvements across multiple models, tasks (text-to-image, text-to-video, image editing), and evaluation metrics.

## Strengths

- **Timely and well-defined research question**: The paper addresses a concrete and practically relevant question about an active trend in the field—recent diffusion transformers are discarding pooled text embeddings without rigorous justification. The systematic ablation in Section 4 (Table 1, Figure 1) provides clear, quantitative evidence that CLIP pooled embeddings contribute negligibly to generation quality, especially for long prompts, which is a genuinely useful finding for the community.

- **Simple, broadly applicable technique**: Modulation guidance is training-free, has negligible runtime overhead (a single vector addition shared across all blocks), and is trivial to implement. The fact that it improves 5 different diffusion models across text-to-image, text-to-video, and image editing tasks (Tables 2, 3, 4) demonstrates strong practical value. The improvements on automatic metrics (consistent ImageReward and HPSv3 gains) and human preferences (e.g., +72% aesthetics win rate for FLUX schnell, +22% object counting improvement) are substantial.

- **Interesting interpretability analysis**: The attention visualization in Figure 4 provides meaningful insight into how modulation guidance operates—shifting the model's attention toward relevant tokens and spatial regions (e.g., hands). This goes beyond a purely empirical contribution.

- **Elegant extension to CLIP-free models**: The distillation-based fine-tuning approach to reintroduce pooled embeddings into models like COSMOS and CausVid is well-designed. The key design choice of using an unconditional prompt for T5 forces the model to route textual information through the pooled embedding, and training on synthetic data controls for dataset effects. The CausVid dynamic degree improvement (+11.34 on VBench) is particularly noteworthy for a distilled video model.

## Weaknesses

### Fatal

None.

### Major

- **Prompt selection sensitivity is unanalyzed**: The method's effectiveness depends on selecting appropriate positive and negative prompts for each target property (e.g., "high quality photo" vs. "low quality photo" for aesthetics). While the prompts are provided in Appendix D, the paper offers no analysis of how sensitive the method is to prompt choice. This is important because the method's practical adoption depends on whether users can easily find effective prompts, or whether the listed prompts are fragile. A small sensitivity study varying prompt phrasing would substantially strengthen confidence in the approach.

- **Incomplete mechanistic understanding**: The analysis in Section 4 shows pooled embeddings are inactive, and Section 5 shows that amplifying them via guidance works. But the paper does not adequately explain *why* the pooled embedding is inactive during normal generation yet effective when amplified. Is the issue that the MLP in Eq. 1 maps CLIP embeddings into a low-magnitude subspace of the modulation space? Understanding this mechanism would move the contribution from a useful trick to a genuine insight.

### Minor

- **The dynamic guidance strategy (step function) is presented without justification**: The paper uses a step function that applies guidance only to layers after index *i* (Figure 3(b)) but does not explain why this particular form works well. A brief analysis of why applying guidance to later layers is preferable (e.g., early layers handle structure while later layers handle details) would add clarity.

- **Some negative results are underdiscussed**: Table 2 shows drops in text relevance for FLUX dev aesthetics guidance and increases in defects for COSMOS complexity guidance. These are briefly acknowledged but not analyzed. Given that the method's value proposition is improving quality without sacrificing prompt fidelity, understanding these failure cases would be helpful.

### Trivial

None.

## Nice-to-Haves

- A comparison of computational cost (wall-clock time, memory) to confirm the negligible overhead claim with concrete numbers.
- Analysis of whether modulation guidance composability—applying multiple guidance signals simultaneously (e.g., aesthetics + hands correction)—works as expected or produces interference.
- Video-specific guidance prompts beyond aesthetics (e.g., motion quality, temporal consistency).

## Novel Insights

The paper's most novel observation is that the pooled CLIP embedding, widely considered uninformative in modern diffusion transformers, is not inherently useless but rather underutilized. The inactive status is an artifact of how the embedding is processed through the modulation MLP, not a fundamental limitation. By amplifying the embedding's influence through simple vector arithmetic in modulation space, the paper demonstrates that the CLIP embedding space contains interpretable directions (aesthetics, complexity, object attributes) that can be accessed without any training. This is conceptually distinct from both classifier-free guidance and attention-based guidance methods, as it operates in a lower-dimensional, globally-shared modulation space rather than in per-token attention outputs.

## Suggestions

- Add a prompt sensitivity study: vary the positive/negative prompts for one target property (e.g., aesthetics) across several paraphrases and report the variance in improvement. This would directly address the practical reliability concern.
- Include a brief mechanistic analysis: probe the magnitude of the modulation coefficient changes caused by the CLIP embedding vs. the timestep embedding to explain why CLIP appears inactive yet can be reactivated.
- For the video results (Table 4), the CausVid improvement on dynamic degree is dramatic; the paper should discuss why modulation guidance specifically recovers dynamics that were lost during distillation.

## Score and Decision

The paper presents a clear, practical, and well-validated contribution. The analysis of pooled embedding inactivity is valuable in its own right, and modulation guidance is a genuinely useful technique with broad applicability and strong empirical support across multiple models and tasks. The main weakness—the lack of prompt sensitivity analysis and deeper mechanistic understanding—prevents a stronger recommendation, but these are addressable issues that do not undermine the core contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept