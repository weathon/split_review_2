## Summary

The paper addresses the problem that chain-of-thought (CoT) reasoning traces in large language models are often not monitorable—they can be unfaithful (hiding true reasoning, e.g., ignoring hints) or overly verbose. The authors formalize CoT monitorability as a constrained optimization problem and propose a pipeline that uses a strong instruct model as a prior policy to transform raw CoT traces into faithful and concise versions, then fine-tunes the base model via supervised learning on these transformed traces. Experiments on MMLU-Pro, GSM8K, and MATH500 show improvements in faithfulness (approximately 10 absolute percentage points) and conciseness (up to 60% reduction in length) while maintaining most of the original task accuracy.

## Strengths

- **Problem significance**: Making CoT traces truly monitorable (faithful and concise) is an important and timely challenge for interpretability and AI safety. The paper clearly motivates why standard RL fine-tuning fails due to sparse reward signals.
- **Principled formulation**: The paper formalizes the problem as a constrained optimization (Eq. 1) and provides a clean mathematical explanation for why naive policy gradients fail (Eq. 4–5), leading to a sparse gradient problem.
- **Practical solution**: The idea of using an external prior (instruct model) to transform traces into high-monitorability versions and then using those as dense supervision targets is practical and effective. The pipeline (Algorithm 1) is clearly described.
- **Empirical validation**: Results on three benchmarks show meaningful gains in both faithfulness and conciseness while accuracy remains high. The distribution shift in thinking lengths (Figure 6) is a compelling visualization.

## Weaknesses

### Fatal

None.

### Major

- **Inconsistent reporting of faithfulness improvement**: The abstract and Figure 1 caption claim "about an additional 10%" improvement, which appears to be absolute percentage points (15.2% → 25.0% = +9.8pp). However, the caption also says "relative gain of over 67%," and the body says "proportion rises by 22 percentage points" (but 25.0 – 15.2 = 9.8pp, not 22). These discrepancies are confusing and must be resolved.
- **Narrow operationalization of faithfulness**: Faithfulness is defined as simply verbalizing an injected hint in the CoT trace. This is a useful but limited proxy; it does not guarantee that the CoT faithfully reflects the model's actual internal reasoning (e.g., the model might mention the hint but still be unfaithful in other ways). The paper would benefit from a broader discussion of faithfulness beyond hint-injection scenarios.
- **Lack of comparison with stronger baselines**: The only baseline compared is a naive RL approach (Figure 2). There is no comparison with other faithfulness-enhancing methods (e.g., direct prompting to be faithful, self-consistency, or other alignment techniques). The claim that "naive RL fails" is not surprising, but it is unclear whether alternative approaches could match the proposed method.
- **Limited evaluation of conciseness thresholds**: The conciseness thresholds (β=125 for GSM8K, β=950 for MATH500) are chosen arbitrarily and used both for filtering training data and evaluating conciseness. The results could be skewed by threshold selection. The paper reports accuracy drops of ~10% relative, which contradicts the claim that accuracy is "essentially unchanged." More nuanced analysis of the accuracy–conciseness trade-off is needed.

### Minor

- **Dependence on a prior model**: The quality of transformed traces depends entirely on the prior policy (Qwen 2.5-7B Instruct). The paper does not analyze failure modes of the prior, nor does it study sensitivity to the choice of prior model.
- **Faithfulness evaluation via LLM-as-a-judge**: The paper uses an LLM to determine whether hints are verbalized. While practical, this introduces potential bias and subjectivity. Human verification or multi-judge consistency checks would strengthen the results.
- **Limited ablation studies**: There is no ablation on filtering criteria (e.g., reward preservation, likelihood selection) or on dataset size. The contribution of each component in Algorithm 1 is not isolated.

### Trivial

- Some figures are referenced before they appear in the text, causing slight confusion (e.g., Figure 3 is discussed on page 5 before its caption appears).
- The ethics and reproducibility statements are standard but very brief; they could be more detailed.

## Nice-to-Haves

- An analysis of cases where the prior model produces poor transformed traces and how the filtering step handles them.
- A comparison with a method that directly optimizes conciseness/faithfulness via reward shaping or better RL (e.g., using a reward model for CoT steps).
- Human evaluation of faithfulness for a subset of examples to validate the LLM-as-a-judge approach.
- Ablation on the choice of prior model (e.g., same-scale vs. larger) to understand the method's robustness.

## Novel Insights

The key insight is that the failure of direct RL for CoT monitorability stems from the extreme sparsity of the monitorability signal at initialization—the model almost never samples a trace with high monitorability. The paper shows that such desirable traces are actually reward-compatible, meaning the base model can produce correct answers when conditioned on them, but the model cannot generate them on its own. This observation motivates using an external prior to generate these traces and then using imitation learning via supervised fine-tuning, effectively converting a sparse-reward RL problem into a dense supervised learning problem. This insight is valuable and could be applied to other settings where sparse reward signals limit learning.

## Suggestions

- **Clarify the faithfulness numbers**: Resolve the inconsistency between "10% additional improvement," "22 percentage points," and "67% relative gain." Provide both absolute and relative improvements clearly in a table.
- **Broaden the faithfulness evaluation**: Consider additional faithfulness metrics (e.g., whether the CoT would allow a human to predict the model's behavior under counterfactuals, or whether the CoT is causally faithful) to demonstrate that hint verbalization is indeed a useful proxy.
- **Include stronger baselines**: Compare against direct prompting (e.g., "Please be faithful and mention all hints"), self-consistency, or a reward-model-based RL approach for conciseness/faithfulness.
- **Discuss the accuracy–conciseness trade-off more carefully**: Report accuracy at multiple conciseness thresholds and include error bars. Clearly state that accuracy drops are around 10% relative (or absolute) rather than claiming it is "essentially unchanged."
- **Provide qualitative examples beyond Figure 1**: Show cases where the method succeeds and fails, especially for conciseness, to give readers intuition.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>  
MY FINAL DECISION: <decision>Accept</decision>