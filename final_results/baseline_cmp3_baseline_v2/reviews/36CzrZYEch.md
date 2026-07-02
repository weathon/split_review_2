## Summary

This paper proposes IRIS, a reinforcement learning framework that fine-tunes autoregressive text-to-image (T2I) models using only an intrinsic reward—negative self-certainty (NSC), defined as the negative KL divergence between the model's output distribution and a uniform distribution. The key empirical finding is that, contrary to text generation where maximizing self-certainty improves reasoning, minimizing self-certainty (i.e., maximizing uncertainty) improves image generation quality. Experiments on Janus-Pro models show that IRIS achieves performance competitive with or superior to methods using external reward models across GenEval, T2I-CompBench, and WISE benchmarks.

## Strengths

- **Novel and well-motivated research question**: The paper asks whether T2I models can be improved using only intrinsic signals without human labels or domain-specific verifiers, which is a timely and important problem given the scalability challenges of RLHF for image generation.
- **Clear empirical discovery**: The observation that self-certainty behaves oppositely in text reasoning vs. image generation is convincingly demonstrated through controlled experiments (Figure 2) and ablation studies, providing a concrete counterpoint to prior work in LLMs.
- **Thorough experimental evaluation**: The paper evaluates on three diverse benchmarks (GenEval, T2I-CompBench, WISE) with multiple sub-metrics, includes extensive ablation studies (CoT usage, direction of self-certainty optimization, forward vs. backward KL, RL vs. direct optimization), and reports results with standard deviations.
- **Practical significance**: IRIS requires no external reward models, human annotation, or domain-specific heuristics, making it scalable and easily generalizable to new domains. The method is architecture-agnostic within autoregressive T2I models.

## Weaknesses

### Fatal
None.

### Major
- **Limited architectural generality**: Experiments are conducted only on Janus-Pro (1B and 7B). The paper acknowledges this in Section 4.4 but does not provide any evidence on other autoregressive T2I models (e.g., Show-o, SEED-X) or diffusion-based models. The claim of being "agnostic to the model architecture" is not supported by experiments.
- **Overclaimed novelty**: The paper states it is "the first framework to improve autoregressive T2I models with reinforcement learning using only an intrinsic reward." However, using negative KL divergence (or entropy) as an intrinsic reward is a well-known idea in RL (e.g., exploration bonuses, maximum entropy RL). The novelty lies in the application to T2I and the specific empirical finding about self-certainty direction, but the framing as a fundamentally new framework is somewhat overstated.
- **Comparison to external rewards is not fully controlled**: The external reward baseline (T2I-R1) uses a specific set of reward models (HPSv2, DINO, GIT, ORM). The paper shows IRIS is competitive, but it is unclear whether the external reward models are the best available or whether a stronger external reward ensemble would outperform IRIS more significantly. The paper also corrects a bug in the T2I-R1 implementation, making direct comparison to published numbers difficult.

### Minor
- **Theoretical justification is weak**: The paper provides an empirical observation (low self-certainty → richer images) but does not offer a theoretical explanation for why this occurs. The claim that "less self-confident models generate more visually rich images" is intuitive but not deeply analyzed.
- **Evaluation metrics in ablation studies**: The ablation studies use the same external reward models (HPSv2, DINO, GIT, ORM) as evaluation metrics. While the paper states these are not used in training, they may still have biases that favor certain image characteristics, and the results might not fully reflect human preferences.
- **Single model family**: The main experiments use only Janus-Pro. While the paper includes both 1B and 7B variants, the findings may not generalize to other autoregressive T2I architectures with different tokenization or training procedures.

### Trivial
None.

## Nice-to-Haves

- Experiments on additional autoregressive T2I models (e.g., Show-o, VILA-U) to demonstrate architectural generality.
- Human evaluation study to complement automated metrics, especially for the claim that lower self-certainty aligns with human preferences.
- Analysis of the generated images' diversity (e.g., FID, CLIP score) to quantify the "visually rich" claim beyond reward model scores.
- Theoretical analysis or intuition for why self-certainty behaves differently in text vs. image generation (e.g., role of tokenization, modality-specific properties).

## Novel Insights

The paper's most novel insight is the task-dependent behavior of self-certainty: maximizing self-certainty benefits objective reasoning tasks (math, code) while minimizing self-certainty benefits subjective generation tasks (text-to-image). This challenges the prevailing assumption that higher model confidence is universally beneficial and suggests that the optimal intrinsic reward direction depends on whether the task requires convergent or divergent thinking. The paper also demonstrates that intrinsic rewards can be as effective as carefully engineered external reward ensembles for T2I alignment, which has practical implications for reducing the cost and complexity of RL-based fine-tuning.

## Suggestions

- Add experiments on at least one other autoregressive T2I model (e.g., Show-o or SEED-X) to support the claim of architecture agnosticism.
- Include a human evaluation (e.g., pairwise preference judgments) to validate that the improvements measured by automated reward models correspond to actual human preferences.
- Provide a more detailed analysis of why forward KL outperforms backward KL in this setting, perhaps connecting to mode-covering vs. mode-seeking behavior in the context of image generation.
- Discuss potential failure modes: e.g., could minimizing self-certainty lead to overly noisy or incoherent images? The paper shows it works well on benchmarks, but a qualitative analysis of failure cases would be valuable.

## Score and Decision

**Score**: 6

**Decision**: Accept

The paper presents a clean, well-executed study with a clear empirical finding and practical implications. The main limitations are the lack of architectural generality and the somewhat overstated novelty framing. However, the core contribution—demonstrating that intrinsic reward (negative self-certainty) can effectively align T2I models without external supervision—is solid and valuable to the community. The paper is well-written, the experiments are thorough, and the ablation studies convincingly support the claims. I recommend borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>