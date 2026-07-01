## Summary

This paper introduces ASPEC, a framework for automated stateful specialization of agent systems that bridges the gap between static task-level workflows and per-query adaptive optimizers. The framework operates through a two-stage lifecycle: (1) **Discovery**, where evolutionary search autonomously identifies specialist agent archetypes, and (2) **Cultivation**, where these specialists accumulate persistent expertise through experience and reflection. A lightweight "retain-then-escalate" meta-controller decides when to leverage the existing specialist team versus when to resample a new architecture, enabling cost-effective adaptation. Experiments on five benchmarks (MATH, HumanEval, MMLU, GPQA, SciCode) show ASPEC achieves state-of-the-art or competitive performance, with particularly strong gains on expert-level benchmarks like GPQA (62.8% vs. 56.3% vanilla), while maintaining significantly lower computational costs than comparable adaptive methods.

## Strengths

- **Novel problem framing and synthesis**: The paper identifies a genuine gap in the literature—the tension between static task-level optimization and per-query adaptation—and proposes a principled reconciliation through stateful specialist agents. The "retain-then-escalate" control policy is a clean conceptual contribution that addresses a real practical bottleneck in adaptive agent systems.

- **Comprehensive empirical evaluation**: The paper evaluates against 13 baselines spanning four categories (hand-designed single agents, hand-designed multi-agents, automated specialization, and autonomous design frameworks) across five diverse benchmarks. The efficiency analysis (Table 2) is particularly valuable, showing ASPEC achieves the best accuracy with the lowest training cost ($1.38) and competitive inference cost ($0.88).

- **Well-designed ablation studies**: The ablation in Figure 6 systematically isolates the contribution of each component (specialist operators, base operators, meta-controller, architect, specialist memory) and alternative control policies. The finding that removing specialists causes a 5.4% accuracy drop and triples cost provides strong evidence for the core claim.

- **Convergence analysis**: Figure 7's visualization of discovered specialist embeddings across trials is insightful, showing that the discovery process converges to similar archetypes on narrow domains (GPQA) while exploring diverse compositions on broad domains (MMLU). This demonstrates the method adapts its behavior to domain specificity.

- **Cross-benchmark and cross-model transferability**: Figure 5 shows that specialists trained on one domain transfer effectively to others, and the method generalizes across three different LLM backbones (Gemini 2.0 Flash, GPT-4o-mini, Llama 3.3 70B), supporting robustness claims.

## Weaknesses

### Fatal
None.

### Major

- **Limited novelty of individual components**: While the overall framework is novel, the individual building blocks are largely existing techniques: evolutionary search for agent design (EvoAgent, ADAS), memory/reflection mechanisms (Reflexion, ExeL), role-based prompting (ExpertPrompting), and learned gating policies. The paper's contribution is primarily in the *integration* and *lifecycle management* of these components. This is a valid contribution, but the paper would benefit from more clearly articulating what specific technical innovations beyond integration are introduced.

- **Insufficient analysis of the meta-controller's learned policy**: The rationality analysis (Section 5.3.1, Figure 8) reveals that the meta-controller disagrees substantially with the LLM-as-gate oracle—on GPQA, 45.9% of queries are "risk overconfidence" (controller retains when oracle would resample). The paper attributes this to "pragmatic economic policy," but this interpretation is speculative. Without ground-truth labels of whether retaining or resampling was actually optimal for each query, it's unclear whether the controller is making smart cost-quality trade-offs or simply making errors. A more rigorous analysis would compare the controller's decisions against actual outcome-based optimality.

- **Limited evaluation on truly complex, multi-step tasks**: The benchmarks, while diverse, are relatively standard. SciCode is the most complex, but the paper's strongest results are on GPQA (multiple-choice QA). The paper claims the method is suited for "expert-level scientific benchmarks," but the evaluation would be strengthened by including more realistic, long-horizon tasks like SWE-bench (which the paper itself mentions as future work). The current evaluation doesn't fully demonstrate the benefits of stateful specialization for complex multi-step reasoning.

- **The "rediscovery cost" argument is not directly measured**: A central motivation is that per-query methods incur "rediscovery costs" by regenerating architectures. However, the paper never directly measures this cost—e.g., by comparing ASPEC against a version of MaAS or MAS-Zero that caches and reuses architectures. The efficiency comparison (Table 2) shows ASPEC is cheaper, but this could be due to other factors (simpler architectures, fewer LLM calls) rather than the specific benefit of state retention.

### Minor

- **The meta-controller's state representation is underspecified**: The "bag-of-operators" approach with attention-weighted averaging is described briefly, but details about the attention mechanism, embedding dimensions, and training procedure are sparse. Given that the meta-controller is a core contribution, more implementation details would aid reproducibility.

- **The specialist discovery process's computational cost is not fully characterized**: The paper reports training cost ($1.38 on GPQA), but doesn't break down how many Architect invocations, specialist evaluations, or crossover operations were performed. This makes it difficult to assess the scalability of the discovery phase to larger domains.

- **Limited discussion of failure modes**: The paper acknowledges that specialists may amplify training biases, but doesn't analyze specific failure cases or edge cases where the method underperforms. For example, are there query types where the meta-controller systematically makes poor decisions?

### Trivial
None.

## Nice-to-Haves

- A direct comparison against a version of MaAS or MAS-Zero that includes a simple caching mechanism (e.g., reuse the previous architecture if query similarity exceeds a threshold) would directly test the "rediscovery cost" hypothesis.
- Including SWE-bench or similar software engineering benchmarks would strengthen the claim of applicability to complex, multi-step tasks.
- An analysis of how specialist memory content evolves during cultivation (e.g., number of memory entries, types of insights) would provide qualitative insight into the learning process.

## Novel Insights

Beyond the paper's own contributions, the most interesting observation is the convergence/divergence behavior of the discovery process across domains (Figure 7). On narrow domains like GPQA, the process reliably converges to the same specialist archetypes (chemistry, biology, physics) across independent runs, suggesting the existence of a natural "basis set" of expert roles for specialized scientific reasoning. On broad domains like MMLU, the process explores diverse team compositions, indicating that the optimal decomposition of expertise is underdetermined when the task space is vast. This suggests a principle: the stability of automated role discovery depends on the specificity of the target domain, and methods may need to adapt their convergence criteria accordingly. The paper's finding that a Goldilocks number of specialists (k=5) emerges from the trade-off between domain coverage and experience depth is also a practically useful insight for designing similar systems.

## Suggestions

- Strengthen the meta-controller analysis by comparing its decisions against actual outcome-based optimality (e.g., for each query, compute whether retaining or resampling would have yielded better accuracy, and evaluate the controller against this ground truth). This would resolve the ambiguity in the current rationality analysis.
- Add a direct ablation that measures the "rediscovery cost" by comparing ASPEC against a version of the method that always resamples (i.e., no meta-controller, always invoke the Architect). The current ablation "w/o meta-controller" does this, but the paper should explicitly frame this comparison as measuring the cost of rediscovery.
- Provide more implementation details for the meta-controller, including the exact architecture, training hyperparameters, and the attention mechanism for the bag-of-operators representation.
- Include a breakdown of the discovery phase's computational cost (number of Architect invocations, specialist evaluations, etc.) to help readers assess scalability.

## Score and Decision

The paper presents a well-motivated framework that addresses a genuine gap in the literature, with comprehensive empirical evaluation and thoughtful ablation studies. The core ideas—stateful specialist agents with a retain-then-escalate policy—are novel in their integration, even if individual components are borrowed from prior work. The results are convincing, particularly the efficiency gains and the convergence analysis. The major weaknesses (limited novelty of individual components, insufficient meta-controller analysis, lack of direct rediscovery cost measurement) are significant but not fatal; they primarily affect the depth of the contribution rather than its validity. The paper is a solid contribution to the agent design automation literature and merits acceptance.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>