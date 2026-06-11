## Summary
# Final Review Report

## Summary

This paper studies preference optimization for Large Reasoning Models (LRMs) that generate intermediate reasoning traces before producing final answers. The key problem identified is that the statistically correct marginal objective (marginalizing over all possible traces) is intractable, while the common single-trace Monte Carlo approximation introduces high gradient variance that destabilizes training. The authors propose Bias–Variance Optimized Preference Optimization (BVPO), which forms a convex combination of two gradient estimators: a high-variance trace-based estimator $g_t$ (computed from sampled reasoning traces) and a low-variance empty-trace estimator $g_e$ (computed by suppressing trace generation via an empty <think></think> tag). The mixing coefficient $\alpha$ is chosen to minimize the Mean Squared Error (MSE) with respect to the ideal marginal gradient.

The paper provides theoretical analysis showing that (Theorem 1) the combined estimator reduces conditional variance from trace sampling, (Theorem 2) there exists an MSE-optimal mixing coefficient, and (Theorems 3-4) this variance reduction translates into convergence bounds for SGD. Empirically, BVPO is evaluated on three DeepSeek-R1-distilled models (1.5B, 7B, 8B parameters) using UltraFeedback prompts with ArmoRM-based preference labeling. Results on AlpacaEval 2 and Arena-Hard show consistent improvements over DPO and SimPO baselines (up to +7.8 points on AlpacaEval 2 win rate and +6.8 on Arena-Hard). Notably, despite training only on general conversational data, BVPO also improves average math reasoning performance across six benchmarks by up to 4.0 points, suggesting that variance-stabilized preference optimization can preserve or enhance reasoning capability.

**Overall assessment:** The paper addresses a relevant and timely problem (LRM alignment) with a clean, conceptually simple approach. The bias-variance framing is appropriate and the empirical gains are convincing. However, the theoretical contributions are largely standard results applied to a specific construction, the experimental evaluation lacks variance reporting and critical reproducibility details (e.g., the $\alpha$ value is not reported), and the claimed reasoning improvement lacks mechanistic analysis. With revisions addressing these gaps, the paper could make a solid contribution.

## Strengths
1. **Timely and well-motivated problem.** Aligning large reasoning models with human preferences is an important and under-explored problem as LRMs become increasingly deployed. The paper correctly identifies trace-induced gradient variance as a key technical bottleneck that existing alignment methods (designed for conventional LLMs) fail to address.

2. **Clean, principled method.** BVPO's core idea—forming a convex combination of a high-variance trace-based estimator and a low-variance empty-trace estimator—is conceptually simple, computationally lightweight, and grounded in the classic bias-variance trade-off. The method is agnostic to the base preference optimization algorithm and can be applied as a drop-in modification to DPO or potentially other variants.

3. **Solid empirical gains.** The experimental results are consistent across three model sizes (1.5B, 7B, 8B) and two alignment benchmarks (AlpacaEval 2, Arena-Hard). The improvements over DPO and SimPO are meaningful in magnitude (up to +7.8 points on AlpacaEval 2 win rate, +6.8 on Arena-Hard) and hold in both Thinking and NoThinking modes, demonstrating robustness.

4. **Intriguing cross-domain transfer finding.** The observation that preference alignment on general conversational data does not degrade—and sometimes improves—math reasoning performance is noteworthy and could have practical implications for LRM training pipelines. This finding is well-supported by results across six diverse math benchmarks.

5. **Rigorous theoretical framing.** The paper correctly frames the problem through the lens of the bias-variance trade-off and provides a clear mathematical formulation of the marginal preference loss, the trace-based approximation, and the empty-trace estimator. The connection between MSE minimization and SGD convergence error (Theorem 4) is clearly articulated.

## Weaknesses
### W1. Missing reproducibility-critical details (Major)
The experiments omit several details essential for reproducibility:
- **$\alpha$ value not reported**: The paper never states what mixing coefficient $\alpha$ was used in the experiments. This is a critical hyperparameter for BVPO. Without it, the experiments cannot be reproduced.
- **No multi-seed variance**: All results appear to be from single training runs. Neither standard deviations nor confidence intervals are reported. Given the small size of Arena-Hard (500 prompts) and the known variability of GPT-4-based evaluation, single-run results are insufficient to establish statistical significance of the reported gains.
- **Baseline tuning not described**: The paper compares against DPO and SimPO but does not state whether these baselines were hyperparameter-tuned for each model size. Without this information, it is unclear whether the comparison is fair.
- **No compute budget**: Training steps, batch size, learning rate schedule, and GPU hours are not reported, making it difficult to assess the practical cost of BVPO (which requires two forward passes per step).

### W2. Theoretical novelty is overstated (Major)
The theoretical results, while correct, are less novel than the paper suggests:
- Theorem 1 (variance reduction) follows directly from the definition of variance for a convex combination and does not require the detailed exposition it receives. The key insight is simply that $g_e$ is deterministic w.r.t. trace sampling, making $\text{Var}(g_c) = \alpha^2 \text{Var}(g_t)$.
- Theorem 2's closed-form $\alpha_{\text{unc}}$ depends on unobservable quantities (bias vectors, covariance matrices) that cannot be estimated in practice. The paper does not propose any practical estimation procedure or convergence analysis for an adaptive plug-in estimator.
- Theorems 3-4 are standard SGD convergence bounds adapted from existing literature (Karimireddy et al., 2022; Ghadimi & Lan, 2013; Ajalloeian & Stich, 2020). The claim of "tighter bounds" (Abstract, Introduction) is unsubstantiated because no comparison to bounds for alternative estimators is provided.
- The $\eta L = 1$ condition in Theorem 4 is a strong assumption that rarely holds in practice.

### W3. Reasoning improvement lacks mechanistic explanation (Major)
The finding that BVPO improves math reasoning despite training only on conversational data is presented as a key result, but the paper offers no hypothesis for why this occurs. Several plausible alternative explanations are not ruled out:
- The effect could be due to doubled training data (two datasets $\mathcal{D}_t$ and $\mathcal{D}_e$) rather than variance reduction specifically.
- The empty-trace gradient might act as a regularizer that prevents catastrophic forgetting of reasoning capabilities.
- The improvement might be a selection artifact—only models that preserved reasoning were shown; models where reasoning degraded could have been omitted.

Without ablations (e.g., controlling for dataset size, comparing against a single-dataset baseline with equivalent compute), the causal attribution to variance reduction is not established.

### W4. Off-policy trace sampling issue not addressed (Major)
The trace-based loss $\mathcal{L}_t$ uses traces sampled from the reference policy $\pi_{\text{ref}}$ but computes the gradient using the current policy $\pi_\theta$. As $\pi_\theta$ diverges from $\pi_{\text{ref}}$ during training, the importance-weighting ratio $\frac{\pi_\theta(r|x)}{\pi_{\text{ref}}(r|x)}$ in the joint probability decomposition can become very large or very small, introducing additional variance and potential bias. The paper's bias-variance analysis does not account for this off-policy effect, which grows during training.

### W5. Distributional shift in empty-trace estimator (Moderate)
The empty-trace estimator $g_e$ conditions the policy on $r = \emptyset$ by appending `<think></think>` to the prompt, creating a distributional mismatch: the model's behavior in "no-thinking" mode differs fundamentally from its behavior in "thinking" mode. The MSE analysis in Theorem 2 assumes a static bias $b_e$, but this bias may change during training as the policy adapts differently under the two input conditions. The paper does not monitor or discuss this dynamic bias.

### W6. Incomplete writing and structural issues (Moderate)
- **Abstract overclaims**: Claims that BVPO "tightens classical convergence bounds" without providing a comparative analysis.
- **Related work is a chronological listing**: Rather than organizing by methodological comparison axes, the Related Work section lists papers sequentially without analytical synthesis.
- **No limitations section**: The paper does not discuss failure cases, boundary conditions, or settings where BVPO might underperform.
- **Notation inconsistency**: The combined estimator is first denoted $g_e(\alpha)$ (page 1, line 12), reusing the $g_e$ symbol earlier used for the empty-trace gradient, before later switching to $g_c$.
- **Conclusion is too brief**: It summarizes contributions but does not discuss limitations, future work, or practical guidance for choosing $\alpha$.

### W7. Missing comparison to alternative variance-reduction approaches (Minor)
The paper presents the convex combination as a natural solution but does not discuss or compare against alternative approaches for reducing trace-induced variance, such as:
- Sampling multiple traces per prompt and averaging gradients (reducing variance by $1/k$ for $k$ samples).
- Using control variates based on the empty-trace gradient.
- Gradient clipping or adaptive learning rate schemes designed for high-variance settings.

A discussion of why the convex combination approach is preferable (e.g., computational efficiency, theoretical guarantees) would strengthen the positioning.

### Novelty & Comparison Notes
**External literature verification unavailable (Retrieval-Disabled Mode).** This run was unable to perform external paper searches. The following novelty-related judgments are therefore deferred for manual verification:
- Whether there exist prior works that already propose mixing traced and non-traced objectives for LRM alignment.
- Whether the claimed "first systematic treatment of LRM alignment" is accurate.
- Whether the empirical gains on AlpacaEval 2 and Arena-Hard are state-of-the-art for similarly sized models.
- Whether the MSE-based gradient mixing approach has been explored in related contexts (e.g., evolutionary strategies, off-policy reinforcement learning).

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a timely and well-motivated problem (LRM alignment) with a clean, principled method (BVPO) that demonstrates consistent and meaningful empirical gains across multiple model sizes and benchmarks. The bias-variance framing is appropriate and the connection between MSE minimization and SGD convergence is clearly articulated.

However, the score is constrained by (a) overstated theoretical novelty—the core theoretical results (Theorems 1-4) are standard properties of convex combinations and existing SGD bounds, not new theoretical advances; (b) missing reproducibility-critical experimental details, most notably the unreported $\alpha$ value and the absence of multi-seed variance reporting; (c) the lack of mechanistic analysis for the reasoning improvement finding, which is presented as a key contribution but remains unexplained; and (d) the omission of a limitations section and failure-mode analysis.

The paper has a solid empirical core and a practical, deployable method. With revisions addressing the reproducibility gaps, toning down the theoretical novelty claims, and adding at least one ablation or analysis experiment to support the reasoning improvement finding, the paper could be strengthened considerably.