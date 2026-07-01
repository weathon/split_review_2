## Summary

This paper addresses the threat of covert misinformation injection in LLM-based multi-agent systems (MAS). It introduces **MISINFOTASK**, a dataset of 108 realistic tasks with associated misinformation injection scenarios and ground-truth arguments, designed to evaluate MAS robustness. The paper also proposes **ARGUS**, a two-stage, training-free defense framework that (1) adaptively localizes critical communication channels using topological importance, message frequency, and semantic relevance to inferred misinformation goals, and (2) performs goal-aware persuasive rectification via chain-of-thought reasoning to detect and correct misinformation. Experiments across multiple LLMs, attack methods, and topologies show that ARGUS reduces misinformation toxicity by ~28% and improves task success rates under attack by ~10% on average, outperforming baselines like Self-Check and G-Safeguard.

## Strengths

- **Timely and important problem**: The paper focuses on covert misinformation (as opposed to overt malicious content) in multi-agent systems, a realistic and under-explored threat that can silently derail collaborative tasks.
- **Novel dataset contribution**: MISINFOTASK fills a clear gap by providing realistic, multi-topic tasks with explicit misinformation injection points and supporting/refuting arguments, enabling systematic red-teaming evaluation.
- **Practical, training-free defense**: ARGUS is modular, requires no additional training, and leverages the LLM’s own reasoning capabilities, making it adaptable to different core models and topologies without fine-tuning.
- **Comprehensive evaluation**: Experiments cover four different LLMs, three injection methods, five topological structures, temporal dynamics, and ablation studies, providing strong evidence for the method’s effectiveness and generalizability.
- **Consistent and significant improvements**: ARGUS consistently reduces misinformation toxicity and improves task success rates across all settings, with clear margins over the compared baselines.

## Weaknesses

### Fatal
None.

### Major
- **Limited dataset size**: MISINFOTASK contains only 108 tasks. While the paper acknowledges this, the small scale raises questions about the statistical reliability of the results and the coverage of diverse misinformation scenarios. A larger dataset would strengthen the conclusions.
- **LLM judge for evaluation**: The metrics MT and TSR rely on an LLM (GPT-4o) to score semantic consistency. The paper does not provide any calibration, human validation, or analysis of the judge’s reliability, which introduces potential bias and reproducibility concerns.
- **Limited baseline comparisons**: Only two defense baselines (Self-Check and G-Safeguard) are compared. Other relevant approaches (e.g., multi-agent debate, consensus filtering, or graph-pruning methods) are mentioned in related work but not evaluated, making it unclear how ARGUS compares to the full landscape of MAS defenses.
- **Computational cost not quantified**: The paper acknowledges that ARGUS introduces overhead but does not measure or report the additional latency, token usage, or number of extra LLM calls. This is important for practical deployment.

### Minor
- **Ambiguity in corrective agent deployment**: It is unclear whether a single corrective agent monitors all selected edges or multiple instances are deployed. The description “deploy corrective agent a_cor onto the communication channels” could be interpreted either way.
- **Threshold sensitivity**: The adaptive re-localization uses a similarity threshold θ_sim, but the paper does not specify its value or analyze sensitivity to this hyperparameter.
- **“Training-free” nuance**: While ARGUS does not require training, it still relies on a pre-trained embedding model for semantic similarity, which is a learned component. The term is not misleading but could be clarified.

### Trivial
None.

## Nice-to-Haves

- Provide a cost analysis (e.g., additional tokens, wall-clock time) for ARGUS to help practitioners assess the trade-off.
- Include human evaluation or inter-annotator agreement for the LLM judge on a subset of outputs.
- Compare with additional defense methods such as multi-agent debate or consensus-based filtering.
- Release the MISINFOTASK dataset and ARGUS code to facilitate reproducibility and further research.

## Novel Insights

The paper’s key insight is that misinformation in MAS can be effectively countered by combining graph-theoretic localization (using edge betweenness centrality and dynamic semantic relevance) with the LLM’s own internal knowledge activation through goal-aware reasoning. The observation that misinformation toxicity increases monotonically over rounds without defense, and that ARGUS reverses this trend, provides a clear demonstration of propagation dynamics and the value of early, adaptive intervention. The idea of inferring the attacker’s intent-driven goal and using it to guide re-localization is a novel and principled approach to persistent misinformation attacks.

## Suggestions

- Clarify the deployment model of the corrective agent (single vs. multiple instances) and how it processes messages from multiple monitored edges.
- Report the value of θ_sim and perform a sensitivity analysis to show robustness.
- Include a brief discussion of the computational overhead (e.g., number of additional LLM calls per round) to help readers assess practicality.
- Consider expanding the dataset in future work or providing a plan for community contributions.

## Score and Decision

The paper makes a solid contribution to an important and timely problem. The dataset fills a gap, the defense method is practical and well-motivated, and the experiments are thorough. The major weaknesses (small dataset, limited baselines, lack of judge calibration) are not fatal but prevent the paper from being a strong accept. The work is clearly above the ICLR acceptance threshold and will be of value to the community.

MY FINAL SCORE: 7.0<score>  
MY FINAL DECISION: Accept<decision>