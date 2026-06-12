## Summary

This paper proposes IRIS, a reinforcement learning framework for autoregressive text-to-image generation that uses Negative Self-Certainty (NSC)—the negative KL divergence between the model's output distribution and a uniform distribution—as an intrinsic reward. The key finding is that, contrary to text-only LLMs where maximizing self-certainty improves reasoning, minimizing self-certainty improves image generation, because low-certainty T2I models produce visually richer and more diverse images. Applied to Janus-Pro models, IRIS achieves competitive results with methods using external reward models while requiring no human labels or domain-specific verifiers.

## Strengths

- **Genuinely novel and well-supported observation.** The paper identifies a compelling task-dependent behavior of self-certainty: maximizing it benefits language reasoning (Fig. 2, blue line) while minimizing it benefits T2I generation (Fig. 2, orange line, and Fig. 1 qualitative comparisons). This is a surprising and important finding that challenges the prevailing assumption from LLM literature that higher self-certainty is universally beneficial.

- **Thorough ablation study design.** The paper systematically dissects design choices: with/without CoT (Fig. 5), minimize vs. maximize image self-certainty (Fig. 6), minimize vs. maximize text self-certainty (Fig. 7), forward vs. backward KL (Fig. 8), and RL vs. direct optimization (Fig. 9). Each ablation is well-motivated and clearly presented, providing strong empirical evidence for each design decision.

- **Practical significance and broad applicability.** By eliminating dependence on external reward models (HPSv2, DINO, GIT, ORM), IRIS removes scalability bottlenecks from human labeling and domain-specific verifiers. The method is architecture-agnostic in principle and can be adapted to any autoregressive T2I model.

- **Competitive empirical results.** On Janus-Pro 1B, IRIS improves over the base model by 9.1%, 13.3%, and 28.8% on GenEval, T2I-CompBench, and WISE respectively, achieving results comparable to T2I-R1 (which uses four external reward models). IRIS particularly excels on WISE natural-science categories, where external reward models lack domain knowledge.

- **Identifies and corrects a bug in T2I-R1.** The paper notes that T2I-R1 uses an incorrect chat template for Janus-Pro models, and reports corrected numbers—a responsible and valuable contribution to the community.

## Weaknesses

### Fatal

None.

### Major

- **Evaluation limited to a single model family.** IRIS is only evaluated on Janus-Pro (1B and 7B). The paper claims general applicability but provides no evidence on other autoregressive T2I architectures. Given that the core claim is about a general principle (lower self-certainty helps image generation), testing on only one model family significantly limits the generalizability of the findings. The paper acknowledges this in Section 4.4 but does not address it.

- **IRIS consistently underperforms external rewards on several important metrics.** While the paper frames IRIS as "competitive," a closer look at Table 1 reveals systematic gaps: on GenEval 1B, IRIS trails T2I-R1 in Counting (0.41 vs. 0.50) and Color Attribution (0.51 vs. 0.63); on T2I-CompBench, IRIS is lower on 2D-Spatial (0.2909 vs. 0.3153 for 1B; 0.2875 vs. 0.3246 for 7B); on WISE 7B, IRIS achieves 0.48 vs. 0.50 overall. The paper's narrative would benefit from a more honest accounting of these tradeoffs rather than presenting IRIS as broadly equivalent.

- **Insufficient mechanistic explanation for why lower self-certainty helps image generation.** The paper asserts that low-uncertainty models generate "simple and uniform images" but offers only intuitive explanations. Why does this happen specifically for image tokens in autoregressive T2I models? Is it related to the discrete VQ-VAE tokenization, the spatial redundancy in images, or the sequential generation order? A deeper analysis would significantly strengthen the contribution.

### Minor

- **Sensitivity to GRPO group size not explored.** The paper uses 8 text strings per query and 1 image per text. Why 8? Is the method sensitive to this hyperparameter? This seems like an important practical consideration that is not discussed.

- **Training efficiency not quantified.** Since IRIS eliminates external reward model inference during training, it should be computationally cheaper than T2I-R1. This practical advantage is not mentioned or measured.

- **Limited failure mode analysis.** Beyond Figure 1, there is limited qualitative or quantitative analysis of cases where IRIS performs worse than external rewards or the base model.

### Trivial

Minor naming inconsistencies (e.g., "HPsV2" vs. "HPSv2" in figure labels).

## Nice-to-Haves

- Evaluate IRIS on at least one other autoregressive T2I model (e.g., SEED-X, Show-o, or a non-autoregressive method) to demonstrate generalizability.
- Provide a more rigorous analysis connecting self-certainty to image quality—e.g., by examining per-token self-certainty distributions across different image regions or complexity levels.
- Report training wall-clock time savings compared to T2I-R1.

## Novel Insights

The paper's most novel contribution is the empirical demonstration that self-certainty exhibits task-dependent behavior across modalities: it should be maximized for objective reasoning tasks but minimized for subjective generation tasks. This finding, supported by both training dynamics (Fig. 2) and qualitative evidence (Fig. 1), fundamentally challenges the assumption from the LLM literature that higher self-certainty is universally desirable. The additional finding that forward KL (mode-covering) outperforms backward KL (entropy, mode-seeking) for this purpose suggests that encouraging the model to maintain probability mass across multiple plausible visual interpretations—rather than collapsing to a single mode—is key to generating visually rich images. These insights offer a new lens for understanding intrinsic signals in multimodal generative models and suggest that the optimal direction of entropy/certainty manipulation depends critically on the modality and task structure.

## Suggestions

- Add experiments on at least one additional model architecture to substantiate the generalizability claims.
- Provide a deeper mechanistic analysis of why self-certainty behaves differently for image tokens—potentially examining the token-level self-certainty maps overlaid on images.
- Include an explicit comparison of computational costs (training time, GPU hours) between IRIS and T2I-R1 to highlight IRIS's practical advantages.
- Discuss the relationship between IRIS and existing diversity-encouraging techniques in image generation (e.g., classifier-free guidance) to better position the work.

MY FINAL SCORE: 6.0
MY FINAL DECISION: Accept