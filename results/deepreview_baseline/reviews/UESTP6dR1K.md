## Summary

This paper introduces ASPEC, a framework for automated stateful specialization of agent systems. ASPEC manages a full agent lifecycle through two phases: (1) **Discovery**, where an LLM-based Architect uses evolutionary search (creation, crossover, selection) to discover specialist agent archetypes from a pool of base operators, and (2) **Cultivation**, where selected specialists accumulate persistent, experience-driven memory through reflection on a training corpus. A lightweight "retain-then-escalate" meta-controller policy decides whether to reuse the current specialist team or invoke the expensive Architect to resample a new architecture. Experiments on five benchmarks (MATH, HumanEval, MMLU, GPQA, SciCode) show ASPEC achieves state-of-the-art or competitive results, with particular gains on expert-level benchmarks like GPQA (62.8%), while maintaining low computational cost ($0.88 USD inference cost on GPQA).

## Strengths

- **Novel and well-motivated problem framing.** The paper clearly identifies a genuine tension in the literature between static task-level optimization (e.g., AFlow, ADAS) and per-query adaptation (e.g., MaAS, MAS-GPT), and proposes a principled reconciliation through stateful specialists with a hierarchical control policy. This is a genuinely interesting research direction.
- **Comprehensive and rigorous experimental evaluation.** The paper evaluates on five diverse benchmarks spanning math, QA, and code, against 13 baselines spanning hand-designed agents, automated specialization, and autonomous design frameworks. The efficiency analysis (Table 2) is particularly strong, showing ASPEC achieves the best accuracy with the lowest training and inference costs. The ablation study (Figure 6) is thorough, isolating the contribution of each component.
- **Strong empirical results on expert-level benchmarks.** The 6.5% improvement over vanilla Gemini 2.0 Flash on GPQA and the leading performance on SciCode are compelling, especially given the low cost. The cross-benchmark and cross-model transferability results (Figure 5) further strengthen the claims.
- **Well-designed and interpretable methodology.** The "retain-then-escalate" policy is intuitive and the two-stage lifecycle (discovery + cultivation) mirrors human expertise development in a sensible way. The case study (Figure 4) showing the lineage and memory of a physics specialist provides concrete interpretability.

## Weaknesses

### Fatal
None.

### Major
- **Limited novelty of individual components.** While the *combination* is novel, the individual components (evolutionary search over agent prompts, memory/reflection mechanisms, a learned gating policy) are each well-established in prior work (EvoAgent, Reflexion, MaAS). The paper's primary contribution is the *system-level integration* and the lifecycle framing. This is a valid contribution, but the paper would benefit from more clearly delineating what is genuinely new versus what is a novel synthesis.
- **The meta-controller's training and evaluation are underspecified.** The paper defines the meta-controller as a neural policy trained via an MDP (Equation 4), but provides no details on the training algorithm (e.g., PPO, DQN, REINFORCE), the reward function design beyond the abstract formulation, the training data generation process, or the number of training steps. The rationality analysis (Section 5.3.1) compares against an LLM-as-gate "oracle proxy," but it's unclear how the meta-controller was trained to make these comparisons meaningful. This is a significant gap for a core component.
- **The "retain-then-escalate" policy is evaluated only in a limited setting.** The paper evaluates on benchmarks where queries are independent and identically distributed (i.i.d.) within a domain. The core motivation for the policy—that related queries can benefit from retained state—is not directly tested. A more convincing evaluation would involve a stream of related queries (e.g., multi-turn interactions, a sequence of subproblems in a scientific workflow) where the "retain" action demonstrably leverages accumulated memory. The current evaluation on i.i.d. benchmarks may underestimate the policy's value or, conversely, may not fully stress-test its limitations.
- **The "Cultivation" phase is relatively simple.** The cultivation process is described as post-execution reflection on a training corpus with semantic retrieval. This is essentially Reflexion + RAG applied to discovered specialists. The paper does not explore more sophisticated cultivation strategies (e.g., curriculum learning, inter-specialist knowledge sharing, or active learning to select which experiences to gather). Given that cultivation is half of the claimed lifecycle, this feels underdeveloped.

### Minor
- **The sensitivity analysis (Figure 6) is only on GPQA.** The paper should show sensitivity to k and m on at least one other benchmark (e.g., MMLU or MATH) to demonstrate that the findings are not domain-specific.
- **The "convergence" analysis (Figure 7) is qualitative.** The paper claims convergence on GPQA and divergence on MMLU based on visual inspection of 2D PCA plots. A quantitative measure (e.g., average pairwise cosine similarity between discovered specialists across runs, or a clustering metric) would be more rigorous.
- **The paper does not report variance across runs for the main results (Table 1).** Given that the discovery process involves stochastic LLM calls and evolutionary search, reporting standard deviations or confidence intervals over multiple trials is important for assessing the reliability of the results.

### Trivial
- The paper states "We will release the code at ." (missing URL). This is a minor oversight.

## Nice-to-Haves

- An evaluation on a multi-turn or sequential reasoning benchmark (e.g., a subset of SWE-bench or a multi-hop QA dataset) would directly test the "retain" policy's ability to leverage accumulated state.
- A deeper analysis of the learned meta-controller policy: what features (query embedding, architecture embedding) drive the "resample" vs. "retain" decision? Are there interpretable patterns?
- An exploration of alternative cultivation strategies, such as having specialists share experiences or using a curriculum over the training corpus.

## Novel Insights

None beyond the paper's own contributions. The paper's primary insight is the system-level integration of discovery, cultivation, and a learned gating policy, which is a valuable synthesis but does not introduce a fundamentally new theoretical or algorithmic concept.

## Suggestions

1. **Provide full details on meta-controller training.** Specify the RL algorithm, reward function, training data generation process, and hyperparameters. This is essential for reproducibility.
2. **Evaluate on a sequential or multi-turn task.** Design an experiment where a stream of related queries (e.g., subproblems of a larger scientific question) is presented, and measure whether the "retain" policy leads to better performance or lower cost compared to always resampling.
3. **Report variance for main results.** Run the full ASPEC pipeline (discovery + cultivation + evaluation) at least 3 times and report mean and standard deviation for Table 1.
4. **Quantify convergence.** Instead of visual inspection of PCA plots, compute the average pairwise cosine similarity between discovered specialist prompts across runs for GPQA and MMLU.

## Score and Decision

The paper presents a well-motivated, novel synthesis of existing ideas into a coherent framework, supported by strong empirical results and a thorough ablation study. The main weaknesses are the underspecification of the meta-controller training and the limited evaluation of the "retain" policy in its intended sequential setting. These are significant but not fatal; they can be addressed in a revision. The paper makes a clear contribution to the agent design automation literature.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>