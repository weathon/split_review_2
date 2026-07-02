## Summary

This paper proposes CALM (Co-evolution of Algorithms and Language Model), a framework for automatic heuristic design (AHD) that jointly optimizes both the prompt generation process and the LLM itself via reinforcement learning (GRPO). In contrast to existing LLM-based AHD methods that keep the LLM frozen and only manipulate prompts, CALM fine-tunes a quantized 7B model using heuristic performance as reward signals, enabling the LLM to co-evolve with the search process. Experiments on Online Bin Packing, TSP, CVRP, and Orienteering Problem show that CALM outperforms state-of-the-art baselines, including methods using significantly more powerful API-based models, while running entirely on a single 24GB GPU.

## Strengths

- **Novel paradigm for LLM-based AHD:** CALM is among the first frameworks to combine verbal guidance (prompt engineering) with numerical guidance (RL-based fine-tuning of the LLM). This co-evolutionary approach is a genuine conceptual advance over frozen-LLM methods (EoH, ReEvo, MCTS-AHD, etc.), and the paper provides a clear motivation for why LLM adaptation should help.
- **Strong empirical results across four tasks:** CALM consistently outperforms SOTA baselines (including GPT-4o-mini-based methods) on OBP, TSP, CVRP, and OP. The improvement is particularly pronounced on out-of-domain scales, demonstrating genuine generalization. Notably, CALM achieves a 0% optimality gap on OBP 1k_500 and outperforms all LLM-based baselines on CVRP and OP by meaningful margins (e.g., 3.83% vs 5.44% on CVRP N=50).
- **Comprehensive and well-designed ablation study:** The paper systematically ablates the RL component, collapse mechanism, each operator, and reward variants (Table 4). The results confirm that all components contribute positively and that the RL fine-tuning has the largest individual impact—providing strong evidence for the core claim.
- **Practical efficiency:** Running locally with an INT4-quantized 7B model on a single 24GB GPU, CALM demonstrates that sophisticated AHD is accessible without commercial API dependence. This is a meaningful step toward democratizing LLM-based algorithm discovery.
- **Well-motivated technical components:** The injection/replacement operators for fine-grained mutation, the diversity-aware crossover, and the collapse mechanism for escaping local optima are all clearly motivated and empirically validated. The collapse mechanism’s analytical approximation (Eq. 2) adds theoretical grounding.

## Weaknesses

### Major

- **Claims of surpassing stronger models are nuanced and context-dependent:** The paper asserts that CALM “surpasses methods that rely solely on verbal guidance, even when those use significantly more powerful API-based models.” While the overall trend supports this, the margins are sometimes small and not uniform across all settings. For example, on TSP in-domain (N=50), the GPT-4o-mini variant of CALM (without RL) achieves 10.54% gap versus MCTS-AHD’s 9.69%—slightly worse. The claim holds on average and especially at larger scales, but the paper would benefit from a more precise characterization of where and by how much improvements occur.
- **Statistical significance not reported in main paper:** The main results report means over 3 runs without standard deviations or confidence intervals. Given that some performance gaps between CALM and top baselines are modest (e.g., 0.71% vs 0.89% on OBP average; 10.04% vs 9.69% on TSP N=50), it is unclear whether these differences are statistically significant. The appendix mentions p-values, but this should be visible in the main text to support the claims.
- **Complexity and hyperparameter sensitivity:** The framework has many components (5 operators, collapse mechanism with two hyperparameters, reward function with multiple scalars). The ablation shows that some collapse hyperparameter choices can substantially degrade performance (e.g., δ₀=0.005, C=15 gives 27.22% on OP vs 17.41% default). While the paper discusses this, the practical challenge of tuning these hyperparameters is underemphasized. A clearer hyperparameter sensitivity analysis in the main text would strengthen the paper.

### Minor

- **The API-based variant comparison is somewhat asymmetric:** The “Efficacy of verbal gradient” experiment replaces the backend with GPT-4o-mini, sets G=1, and uses more queries—effectively testing a different method. While informative, this comparison conflates model capability with prompt design, making it difficult to isolate the contribution of the verbal gradient operators alone. A controlled comparison using the same Qwen2.5 model (without RL) would be cleaner.
- **Limited discussion of potential overfitting or distribution shift during fine-tuning:** The LLM is continuously fine-tuned on responses generated from prompts seen during the search. The paper does not discuss whether the LLM overfits to the specific prompt distribution, which could limit generalization across different tasks or search trajectories.

## Nice-to-Haves

- An analysis of what the fine-tuned LLM has “learned”—e.g., whether it internalizes specific heuristic patterns or becomes better at following the operators—would provide deeper insight into the co-evolution mechanism.
- A comparison of total wall-clock time between CALM and API-based baselines (including fine-tuning overhead) would help practitioners assess the practical trade-offs.
- A discussion of limitations: how does CALM scale to more than 2000 queries? Does the fine-tuning benefit eventually saturate?

## Novel Insights

Beyond the paper’s own contributions, the key insight is that evolutionary heuristic search naturally generates a curriculum of training data (prompt-response-performance triplets) that can be used to adapt the LLM itself. This turns the search process into a co-evolutionary loop where the LLM internalizes patterns from successful heuristics, and the improved model produces better heuristics, creating a self-reinforcing cycle. This perspective bridges prompt-based evolution (which treats the LLM as a fixed oracle) and model fine-tuning (which treats the prompt as fixed), suggesting a more unified view of LLM-guided optimization.

## Suggestions

- In the main paper, provide standard deviations or confidence intervals for the key results (Tables 1–3) to convey statistical reliability.
- Nuance the claim about surpassing API-based methods: explicitly state where improvements are largest (e.g., out-of-domain scales, CVRP/OP) and where they are marginal (e.g., in-domain TSP small scale).
- Add a concise hyperparameter sensitivity table for collapse parameters (δ₀, C) in the main text, showing that default values work robustly.
- Discuss potential limitations of the approach: overfitting to prompt distribution, computational overhead of frequent GRPO updates, and sensitivity to the number of samples G.

## Score and Decision

This paper presents a well-executed and novel contribution to LLM-based automatic heuristic design. The core idea—co-evolving the LLM via RL during heuristic search—is conceptually clean and empirically validated across multiple benchmarks. The experimental setup is thorough, the ablation studies are informative, and the practical efficiency (runs on a single 24GB GPU) is compelling. The overall quality and significance are clearly above the ICLR acceptance threshold.

**Score:** 8

**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>