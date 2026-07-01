## Summary

The paper introduces DeepScientist, an LLM-based multi-agent system for autonomous scientific discovery, formalized as a Bayesian optimization problem with a persistent Findings Memory that balances exploitation and exploration. The system is evaluated on three frontier AI tasks (Agent Failure Attribution, LLM Inference Acceleration, AI Text Detection), claiming to surpass human-designed SOTA methods by redesigning core methodologies. The paper also provides analysis of the discovery process, including scaling laws and human evaluation of generated papers.

## Strengths

- **Ambitious and timely problem**: The paper tackles the important challenge of automating scientific discovery on complex, real-world AI tasks, moving beyond synthetic or narrow problems.
- **Large-scale experimentation**: The system consumed over 20,000 GPU hours, generated ~5,000 ideas, validated ~1,100, and produced 21 progress findings, demonstrating the scale of autonomous exploration.
- **Concrete results on multiple tasks**: DeepScientist achieves improvements over human SOTA on three distinct tasks, with the AI text detection result being particularly notable (7.9% AUROC improvement and 2x latency reduction).
- **Detailed analysis of the discovery process**: The paper provides valuable insights into the discovery funnel (ideas → implemented → progress), the critical role of selection, the high rate of implementation errors (60%), and the scaling behavior with parallel resources.
- **Human evaluation of generated papers**: A small program committee rated the system's papers, with two papers scoring 5.67 (exceeding the ICLR 2025 average of 5.08), indicating genuine novelty in the generated ideas.

## Weaknesses

### Fatal
None.

### Major
1. **Uneven and insufficiently validated performance claims**: The improvements are not uniformly strong. On LLM Inference Acceleration, the gain is only 1.9% (3.65 tokens/second), which may be within measurement noise. On Agent Failure Attribution, the baseline accuracy is very low (12.07% and 16.67%), so the 183.7% relative improvement corresponds to modest absolute gains. The paper provides no error bars, confidence intervals, or statistical significance tests for any of the main results.

2. **Lack of rigorous comparison to alternative approaches**: The paper does not compare DeepScientist's discovery efficiency or final method quality to other automated discovery systems (e.g., AI Scientist-V2, CycleResearcher) on the same benchmarks. The comparison of generated papers via DeepReviewer is indirect and does not evaluate the discovery process itself.

3. **Bayesian optimization formulation is not empirically validated**: The surrogate model and acquisition function are described but not ablated against simpler selection strategies (e.g., random selection, greedy selection, or uniform exploration). The paper briefly mentions that without selection the success rate is "effectively zero," but provides no detailed results or analysis to support this claim.

4. **Human evaluation is based on a very small sample**: Only 3 reviewers evaluated 5 papers. While inter-rater reliability is reported, the variance is high for some papers (e.g., PA-TDT and ACRA have variance 1.33 in Rating). The claim that the system's average rating "closely mirrors" ICLR 2025 average is based on a single number without statistical comparison.

5. **Scaling analysis is preliminary and overclaimed**: The scaling experiment uses only 4 data points (1,2,4,8,16 GPUs) over one week. The "near-linear relationship" claim is not strongly supported, especially given that individual tasks show very different scaling behavior and the overall curve has only 5 points with small counts (0,0,1,4,11).

6. **Overstated novelty claims**: The paper claims to be "the first large-scale empirical demonstration of an automated system that continuously advances scientific frontiers on complex AI tasks," but prior work (e.g., AI Scientist-V2) has demonstrated automated discovery on real tasks. The distinction in goal-oriented discovery is not fully substantiated by the experiments, and the paper does not directly compare to these systems on the same tasks.

### Minor
1. The system relies on proprietary LLMs (Gemini-2.5-Pro, Claude-4-Opus) that are not publicly available, limiting reproducibility.
2. The description of the surrogate model and acquisition function is high-level; details of how the LLM produces the valuation vector ⟨v_u, v_q, v_e⟩ are not provided.
3. The paper does not discuss the monetary cost or API call volume of the system, only GPU hours.
4. Some claims are vague, e.g., "compressing years of human research" is based on a single task and a rough comparison without controlling for differences in problem difficulty or evaluation setup.

### Trivial
None.

## Nice-to-Haves
- Provide error bars and statistical significance tests for all main performance results.
- Include ablation studies of the Bayesian optimization components (surrogate model, acquisition function, different weighting schemes).
- Compare DeepScientist's discovery process to other AI Scientist systems on the same tasks and benchmarks.
- Release the full Findings Memory and execution logs to enable reproducibility and further analysis.

## Novel Insights

The paper's key insight is that autonomous scientific discovery can be modeled as a Bayesian optimization problem with a persistent memory of findings, and that the discovery process follows a progressive trajectory where each success enables new directions. The analysis of the discovery funnel (5000 ideas → 1100 validated → 21 progress → 5 papers) and the identification of implementation errors as a major bottleneck (60% of failures) are valuable for the community. The scaling analysis suggesting near-linear returns from parallel exploration with shared memory is also noteworthy, though preliminary. However, these insights are partially obscured by the paper's overclaimed novelty and insufficient validation.

## Suggestions
- Add error bars and statistical tests to all main results, and clarify whether the 1.9% improvement on LLM Inference Acceleration is statistically significant.
- Conduct ablation studies comparing the proposed selection mechanism (UCB with surrogate model) to simpler baselines (random selection, greedy selection) on at least one task.
- Compare DeepScientist's discovery efficiency and final method quality to prior AI Scientist systems on the same benchmarks, rather than only comparing generated papers via an automated reviewer.
- Tone down the novelty claims, particularly "first large-scale evidence," and more clearly delineate what is new relative to prior work.
- Provide a more detailed description of the surrogate model and how the valuation vector is computed, including the prompt template and any calibration.

## Score and Decision

**Score**: 4.5  
**Decision**: Reject

MY FINAL SCORE: <score>4.5</score>  
MY FINAL DECISION: <decision>Reject</decision>