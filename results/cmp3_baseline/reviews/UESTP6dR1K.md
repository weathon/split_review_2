## Summary

The paper introduces ASPEC, a framework that automates the creation and management of stateful specialist agents. It operates in two phases: an offline **Discovery** phase that evolves a diverse pool of specialist archetypes via evolutionary search, and a **Cultivation** phase where selected specialists accumulate persistent, experience-driven memory. A lightweight neural meta-controller implements a “retain-then-escalate” policy that decides whether to reuse the current agent team or resample a new architecture for each query. Experiments on five benchmarks (MATH, HumanEval, MMLU, GPQA, SciCode) show that ASPEC matches or outperforms existing static and adaptive agent systems, with the largest gains on expert-level benchmarks like GPQA, while maintaining low inference cost.

## Strengths

- **Well-motivated problem and clear framing.** The paper identifies a genuine gap between static task-level workflows and per-query adaptive systems, and proposes a principled reconciliation through stateful specialists and a hierarchical control policy.
- **Novel two-stage lifecycle (Discovery + Cultivation).** The idea of first evolving a diverse set of agent archetypes and then letting them accumulate domain-specific memory is a creative and plausible approach to building persistent expertise without human engineering.
- **Comprehensive experimental evaluation.** The paper compares against 13 baselines across multiple domains, includes ablation studies of all major components, sensitivity analyses for key hyperparameters, cross-model and cross-benchmark transferability tests, and a rationality analysis of the meta-controller. The efficiency analysis (Table 2) convincingly shows that ASPEC is cost-competitive.
- **Practical efficiency gains.** The meta-controller’s lightweight design (MiniLM + MLP) leads to substantial cost savings compared to always resampling or using an LLM-as-gate, while retaining most of the performance benefit.
- **Clear and well-structured writing.** The paper is easy to follow, with helpful figures and a logical flow from motivation to methodology to results.

## Weaknesses

### Fatal
None.

### Major
- **Modest performance improvements.** While ASPEC achieves the best average score (69.6%), the gains over the strongest baselines are small: +1.2% over AFlow, +1.5% over EvoAgent on average. On individual benchmarks, the improvements are often 1–2 percentage points. The paper claims “significant performance gains,” but the practical significance of these margins is debatable, especially given the complexity of the framework.
- **Meta-controller alignment issues.** The rationality analysis (Figure 8) shows that the meta-controller disagrees with the LLM-as-gate oracle on a large fraction of queries (e.g., 45.9% false negatives on GPQA). The paper frames this as a deliberate cost-efficiency trade-off, but the cost savings are modest (0.88 vs 3.74 USD) and the accuracy drop is small (0.3%). The underlying limitation—that the lightweight state representation leads to suboptimal decisions—is acknowledged but not fully addressed. The meta-controller’s generalization to unseen query distributions is not tested.

### Minor
- **Cross-benchmark transferability results are puzzling.** Figure 5 shows that using only specialists trained on a different domain (ONLYSPEC) matches or exceeds the full system. The paper attributes this to “T-shaped” reasoning strategies, but this explanation is speculative and undermines the claim that domain-specific cultivation is crucial. This result deserves deeper analysis.
- **Limited diversity of base models.** All main experiments use Gemini 2.0 Flash. While cross-model transferability is shown for GPT-4o-mini and Llama 3.3 70B, the core claims rest on a single backbone. The framework’s sensitivity to the choice of LLM for the Architect and Judge is not explored.
- **Overclaim on “without human intervention.”** The Discovery phase relies on an LLM-based Architect and Judge, which are themselves large, pre-trained models. The process is automated within the LLM ecosystem, but it is not free from human-designed components (e.g., the base operator pool, the prompt templates for the Architect).

### Trivial
- The paper states “we will release the code at ” but provides no link. This is a minor omission that should be fixed.

## Nice-to-Haves

- A theoretical analysis of the convergence properties of the specialist discovery process, as mentioned in the limitations section, would strengthen the paper.
- Testing on more realistic, long-horizon tasks (e.g., SWE-bench) would better demonstrate the value of stateful expertise.
- An analysis of how the meta-controller’s policy co-evolves with the specialists’ memory accumulation would deepen the understanding of the system dynamics.

## Novel Insights

Beyond the paper’s own contributions, the most interesting insight is the observation that the meta-controller’s conservative “retain” policy can concentrate experience into a smaller set of active architectures, potentially leading to more robust and generalist specialists. This creates a co-evolutionary dynamic where the control policy and the specialists’ memory shape each other—a phenomenon that could inspire future work on joint optimization of adaptation and learning in agent systems.

## Suggestions

- Provide a more detailed analysis of the cross-benchmark transferability result (Figure 5). For example, measure the overlap in reasoning strategies between specialists trained on different domains, or ablate the memory component in the transfer setting.
- Include experiments with a stronger base model (e.g., GPT-4o or Claude 3.5) to verify that the gains are not an artifact of the weaker backbone.
- Discuss the meta-controller’s decision boundary more explicitly: what types of queries lead to false negatives (overconfident retain) and false positives (wasteful resample)? This could guide improvements to the state representation.

## Score and Decision

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>