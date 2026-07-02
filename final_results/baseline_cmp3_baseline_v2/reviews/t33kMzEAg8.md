## Summary

This paper proposes SWIREASONING, a training-free framework that dynamically switches between explicit chain-of-thought reasoning and latent (continuous-embedding) reasoning based on entropy-based confidence signals. A switch count controller caps transitions to suppress overthinking and improve token efficiency. Experiments across multiple model families (Qwen3-1.7B/8B/32B, DeepSeek-R1-Distill-Llama-8B) and diverse benchmarks (math, STEM, coding, multi-hop QA, commonsense) show consistent accuracy gains (1.8%–3.1%) under unlimited budgets and substantial token efficiency improvements (57%–79%) under limited budgets.

## Strengths

- **Novel and well-motivated approach**: The idea of dynamically alternating between explicit and latent reasoning based on confidence is clever and addresses genuine limitations of each mode. The entropy-trend based switching is simple yet effective.
- **Practical and efficient**: The method is training-free, operates entirely at inference time, and requires no additional model training or fine-tuning. This makes it directly applicable to existing reasoning LLMs.
- **Thorough experimental validation**: Evaluation covers 4 model scales (1.7B to 32B), two model families, 11 benchmarks across four domains, and includes both accuracy and token efficiency metrics. Ablation studies on window size, signal mixing coefficients, and switch count are comprehensive.
- **Consistent improvements across settings**: Accuracy gains are observed on all benchmarks and all models, with larger gains on harder problems (AIME24/25, GPQA Diamond, hard-level coding). The Pareto frontier improvements for token efficiency are clear and persistent across budget levels.
- **Meaningful efficiency analysis**: The Pass@k evaluation demonstrates that SWIREASONING achieves peak accuracy with significantly fewer samples than baselines, which is a practically important result for budget-constrained deployment.

## Weaknesses

### Fatal
None.

### Major

1. **Heuristic switching criterion without theoretical justification**: The entropy comparison (Eq. 2–3) is intuitive but ad-hoc. The paper does not analyze why next-token entropy relative to block reference entropy reliably indicates when to switch modes, nor does it compare to alternative confidence measures (e.g., probability of the top token, softmax calibration, predictive variance). The asymmetric dwell windows (W_{L→E}=0, W_{E→L}>0) are motivated empirically but lack principled derivation. This weakens the overall technical rigor.

2. **Incomplete specification of early-answer mechanism**: Under the termination trigger (Sec. 3.4), the model is forced to generate a final answer. However, the paper does not specify how the injection queue interacts with the model’s own answer generation—e.g., whether the model continues reasoning internally after the forced < /think> or simply produces an answer from an incomplete trajectory. The reported token efficiency gains rely on this mechanism, but its correctness and robustness are not analyzed (e.g., does forcing early answering sometimes produce nonsensical outputs? How often does the convergence trigger at half C_max yield correct answers?).

3. **Hyperparameter sensitivity without adaptation**: The method introduces several tunable hyperparameters (dwell window size, α₀, β₀, switch count budget C_max) that affect performance significantly (as shown in ablations). While the paper picks default values based on ablations, there is no discussion of how to set these in practice for new tasks or models without a validation set. The linear scheduling of α_t and β_t with T_max is also not justified; the sensitivity to β₀ (ranging from 39% to 63% average accuracy) is particularly concerning.

4. **Token efficiency metric interpretation**: The reported efficiency gains (e.g., +213% on GPQA Diamond, 4.6×–6.8× peak) are computed using a normalized accuracy-per-token ratio relative to CoT’s best performance. The metric is sensitive to the token budget range used for integration. The paper should clarify whether these large gains mainly come from very small budgets where CoT accuracy is near zero, and whether the metric could be inflated by the choice of denominator (CoT’s plain efficiency at its peak). A more direct comparison (e.g., accuracy at fixed token budgets) would be easier to interpret.

### Minor

- The paper uses "SWIREASONING" in the title and abstract but switches to "SWiR" or "Swit" in tables and figures. Consistency would improve readability.
- The caption of Figure 3 appears to be duplicated.
- The matrix of pass@k results (Fig. 5) is shown only for Qwen3-8B on AIME; it would strengthen the claim if similar results were shown for other models/benchmarks.

### Trivial

- Some figure references appear before the figure is defined (e.g., "Fig. 3" in Sec. 3.1).

## Nice-to-Haves

- An analysis of when the convergence trigger (half C_max) vs. termination trigger (full C_max) fires would help understanding when early answering is successful.
- A sensitivity analysis of the dwell window hyperparameter across different model sizes would be informative.
- Comparing against a simple baseline that interpolates between explicit and latent reasoning with a fixed schedule (without entropy) could further highlight the benefits of dynamic switching.
- Ablation removing the signal mixing (Eq. 4–5) entirely would clarify its necessity.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Provide a more principled justification or alternative analysis for the entropy-based switching rule, or at minimum an empirical comparison to other confidence estimators.
- Clarify and describe the answer extraction process under the convergence and termination triggers: how does the model generate the answer, and what happens if the forced injection conflicts with the model’s own output?
- Add a direct accuracy-vs-tokens plot at a few fixed budget points (e.g., 256, 512, 1024 tokens) to complement the efficiency metric and make the gains more interpretable.
- Discuss how hyperparameters (W, α₀, β₀, C_max) can be set in practice for new models or tasks, perhaps via a simple rule-of-thumb or adaptation based on average entropy.

## Score and Decision

The paper presents a novel, training-free, and empirically effective method that improves reasoning LLMs in both accuracy and token efficiency. The experiments are comprehensive and consistently support the claims. The main weaknesses are the heuristic nature of the switching criterion and the incomplete specification of the early-answer mechanism, but these do not invalidate the core contribution. The work is likely to be of high interest to the ICLR community and has practical value for deploying reasoning models under resource constraints.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>