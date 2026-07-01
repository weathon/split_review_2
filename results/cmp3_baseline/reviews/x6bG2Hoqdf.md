## Summary

This paper proposes CALM, a framework for automatic heuristic design (AHD) that co-evolves the large language model (LLM) itself alongside the heuristic search process. Unlike prior LLM-based AHD methods that keep the LLM frozen and rely solely on prompt engineering (“verbal gradients”), CALM fine-tunes the LLM via reinforcement learning (GRPO) using the performance of generated heuristics as reward signals (“numerical gradients”). The method introduces fine-granularity mutation operators, a diversity-aware crossover, and a collapse mechanism to escape local optima, and demonstrates that a locally-run 7B INT4-quantized model can outperform stronger API-based baselines (e.g., GPT-4o-mini) across several optimization tasks (OBP, TSP, CVRP, OP).

## Strengths

* **Novel and well-motivated contribution.** The idea of applying RL-based LLM fine-tuning within an AHD evolutionary loop is a clear step beyond existing frozen-model approaches. The paper carefully motivates why numerical gradients (via fine-tuning) can complement verbal gradients (via prompt manipulation) and provides a principled framework for this co-evolution.
* **Strong empirical results with resource efficiency.** CALM, using a small quantized 7B model on a single 24GB GPU, consistently outperforms or matches API-based baselines (GPT-4o-mini) across four optimization tasks, often achieving the best overall results. This is a practical advantage that makes the method accessible and impactful.
* **Thorough ablation studies and analysis.** The paper ablates each major component (RL fine-tuning, collapse mechanism, each operator, reward design) and provides visualizations of the training dynamics. The results convincingly isolate the contributions, with the GRPO module showing the largest impact.
* **Well-designed evolutionary operators.** The injection, replacement, and diversity-aware crossover operators are specifically tailored to support fine-grained credit assignment during RL, a subtle but important design consideration. The collapse mechanism is theoretically grounded with an analytical formula for expected collapse rounds.

## Weaknesses

### Minor

* **Overclaim on in-domain performance.** The paper states that CALM “outperforms state-of-the-art baselines,” but on several in-domain test sets (e.g., TSP N=50, OP N=50) CALM’s local model is slightly behind the best baseline (MCTS-AHD, HSEvo). The claim is still largely true for out-of-domain and overall averages, but a more precise claim would strengthen credibility.
* **Hyperparameter sensitivity of collapse mechanism is not fully explored.** While the paper provides an ablation with different δ₀ and C values, the analysis is limited to two settings on two problems. The collapse mechanism introduces two new hyperparameters that could significantly affect performance; a broader sensitivity study (even in the main paper) would be informative.
* **Concurrent work is acknowledged but the “first” claim is softened.** The paper cites Surina et al. (2025) and Liu et al. (2025) as concurrent works that also fine-tune LLMs for AHD. While CALM distinguishes itself by using GRPO and specific operator designs, the novelty relative to these concurrent works could be articulated more sharply to avoid ambiguity about what “first” means.

### Trivial

* The reward function in Equation (4) uses α₁ and α₂ but does not define r_rand (used in ablation). This is clarified in the text but could be more explicit.

## Nice-to-Haves

* An analysis of the actual number of collapse events triggered during runs and how the search trajectory changes after collapse would deepen understanding of the mechanism.
* A discussion of failure modes: are there cases where GRPO fine-tuning harms performance (e.g., overfitting to a narrow set of heuristics)?

## Novel Insights

Beyond the paper’s own contributions, a key insight is that the performance gap between small quantized models and large API models can be closed—and even reversed—by judicious RL-based adaptation, even when the adaptation is limited to a tiny fraction (1.15%) of the model weights. This suggests that in AHD, the model’s ability to *adjust to the specific reward landscape of the problem* matters more than raw language understanding capacity. The combination of fine-grained mutation operators with token-level credit assignment from GRPO provides a practical recipe for making the RL signal effective despite the “credit assignment problem” across heuristic components.

## Suggestions

* Clarify in the abstract and introduction that CALM achieves superior results *on average or on out-of-domain tests*, rather than claiming universal superiority across all in-domain settings.
* Provide a brief discussion of the computational cost (wall-clock time) of the full RL fine-tuning loop compared to baseline methods, beyond the query budget. The appendix already mentions running time; a high-level summary in the main paper would be useful.
* Consider reporting results with error bars or intervals for the main tables to facilitate statistical comparison (the appendix has p-values; citing them in the main text would strengthen claims).

## Score and Decision

Score: 9

Decision: Accept

MY FINAL SCORE: <score>9</score>
MY FINAL DECISION: <decision>Accept</decision>