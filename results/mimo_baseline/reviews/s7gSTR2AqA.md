## Summary

This paper investigates whether Large Language Models develop human-like inductive biases toward Information Bottleneck (IB) efficiency in semantic categorization. Using color naming as a primary testbed, the authors (1) benchmark 39 LLMs on English color naming, finding that larger instruction-tuned models align better with human systems, and (2) introduce Iterated In-Context Language Learning (IICLL) to simulate cultural evolution of color-naming systems within LLMs, demonstrating that models converge toward IB-efficient, human-aligned category systems. Only Gemini 2.0 reproduces the full range of near-optimal IB tradeoffs observed across human languages, while other models converge to lower-complexity solutions.

## Strengths

- **Strong theoretical grounding and experimental design**: The paper is exceptionally well-motivated by established cognitive science frameworks (IB principle, iterated learning) and replicates two influential human experiments (Lindsey & Brown, 2014; Xu et al., 2013) with LLMs. This enables direct, quantitative comparison between LLM and human behavior using established metrics (NID, efficiency loss, IB-alignment).

- **Comprehensive model evaluation**: Testing 39 models across 6 families with systematic variation of size, instruction-tuning, modality (text vs. image), and even training checkpoints (Olmo 2) provides a thorough landscape of LLM color-naming capabilities. The finding that instruction tuning is crucial for English-alignment, and that many state-of-the-art models struggle with this basic task, is itself a valuable empirical contribution.

- **IICLL paradigm is a genuine methodological contribution**: The extension of iterated in-context learning to iterated in-context *language* learning is novel and well-designed. It closely mirrors the human iterated learning experiments (Xu et al., 2013), using pseudo-labels rather than English terms to disentangle training data memorization from inductive bias. The demonstration that IICLL systems converge near the IB bound after ~4 generations, paralleling human dynamics, is compelling.

- **Multiple lines of converging evidence**: The paper supports its claims through (a) mode maps showing qualitative alignment, (b) IB tradeoff plots, (c) efficiency loss and alignment trajectories over generations, (d) rotation analyses demonstrating non-trivially structured solutions, and (e) a baseline comparison against a feature-based clustering algorithm. This convergence strengthens the overall argument.

- **Interesting cross-domain extension**: The Shepard circles experiment in Section 4.3 provides initial evidence that IICLL-driven category formation may be domain-general, which significantly broadens the potential impact of the findings.

## Weaknesses

### Fatal

None.

### Major

- **Limited analysis of why Gemini differs from other models**: The paper identifies that only Gemini 2.0 captures the full range of human IB tradeoffs, attributing this to "strongest in-context capabilities," but provides minimal analysis of what specific architectural or training properties drive this difference. The claim that in-context learning ability is the key factor would be significantly strengthened by (a) measuring in-context learning performance on independent benchmarks for each model and correlating with IICLL outcomes, and (b) more carefully disentangling the roles of model size, training data, and instruction-tuning methodology.

- **Constrained generation methodology creates potential confounds**: For the Gemini API, constrained generation is used, while for open-weight models, log probability scoring of allowed terms is used. These are fundamentally different mechanisms—one ensures the output is always a valid term, while the other selects among valid terms based on probabilities but doesn't constrain the generation process itself. This difference could systematically affect the resulting category systems in ways unrelated to the research question, and the paper does not adequately address or control for this.

- **Shepard circles analysis is preliminary**: While the Shepard circles experiment is interesting, it is limited to a single model (Gemini) with k=4 categories, uses images rather than text, and does not compute IB-efficiency metrics. The claim of domain-generality is thus only weakly supported. Additionally, visual inspection of Figure 5b shows some chains that don't clearly demonstrate progressive refinement (e.g., Chain 3 appears relatively stable).

### Minor

- **N=20 human IL chains vs. potentially different numbers of LLM chains**: The paper does not always clearly state how many IICLL chains were run per condition for each model. The human study had 20 chains (4 replications × 5 category conditions), and matching this count is important for fair statistical comparison.

- **Color representation issue**: The finding that CIELAB coordinates hurt performance (Section 4.1) is interesting but raises a question about whether the text-based color naming task truly tests color *categorization* versus numerical pattern matching. The paper could more thoroughly discuss how input representation affects the interpretation of results.

- **Training data analysis is incomplete**: The paper mentions analyzing Olmo 2 training checkpoints (Appendix F) but only briefly in the main text. Understanding how color naming capabilities emerge during pre-training versus instruction-tuning would be more valuable with analysis across multiple model families, not just one.

### Trivial

- The paper occasionally switches between "IICL" and "IICLL" abbreviations in a way that could cause confusion.

## Nice-to-Haves

- A statistical analysis (not just visual) comparing the complexity distributions of LLM IICLL chains versus human IL chains at the final generation would strengthen the comparison.
- Testing whether IICLL convergence speed correlates with in-context learning benchmarks would help validate the proposed mechanism.
- An ablation on the number of in-context examples provided at each generation would clarify how much the convergence depends on example quantity versus model bias.

## Novel Insights

The most novel insight of this paper is that IB-efficiency in semantic categorization can emerge in LLMs through iterated in-context language learning alone—without any explicit optimization for compression—paralleling the cultural evolution dynamics observed in human experiments. This suggests that optimal compression may be a general emergent property of intelligent systems that must learn from limited data, whether biological or artificial. The finding that only the model with the strongest in-context learning capabilities (Gemini 2.0) can reproduce the full diversity of human near-optimal tradeoffs, while other models converge to simplified solutions, is also a genuinely interesting observation that connects representational capacity to the richness of emergent semantic structure.

## Suggestions

- Measure and report in-context learning ability on standard benchmarks for all models tested, and correlate these scores with IICLL outcomes to substantiate the claim that in-context learning capacity drives convergence quality.
- Address the constrained generation vs. logit scoring difference more explicitly, ideally by running both methods where possible and comparing outcomes.
- Expand the Shepard circles analysis to multiple models and compute IB-efficiency metrics to properly test domain-generality.
- Report chain counts per condition and provide confidence intervals or statistical tests for the key comparisons between human and LLM trajectories.

## Score and Decision

This is a well-executed, theoretically grounded paper that makes both methodological (IICLL paradigm) and empirical contributions. The experimental design is thoughtful, the analyses are largely thorough, and the research question is important and well-motivated. The major weaknesses—insufficient analysis of model differences, the constrained generation confound, and the preliminary nature of the Shepard circles experiment—are real but do not invalidate the core findings. The paper provides a novel cognitive science–informed lens for understanding LLM capabilities and will be of genuine interest to both the ML and cognitive science communities.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>