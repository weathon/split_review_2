## Summary

This paper proposes a hierarchical attention model (CodeTransformer-GAT) for code embeddings that processes code at token, function, and module levels using a combination of transformer-based sequential attention and graph attention over ASTs and code dependency graphs. The system is designed for end-to-end RL state representation in code-related tasks including code completion, program repair, and algorithmic problem solving, claiming consistent improvements over several baselines.

## Strengths

- **Multi-level attention for code is a reasonable architectural idea.** Combining token-level transformer attention with function-level AST-based attention and module-level graph attention respects the natural hierarchical structure of code, and the ablation study (Table 2) suggests each component contributes positively.
- **End-to-end RL optimization of code representations** rather than learning embeddings in isolation from the downstream task is a potentially valuable direction, distinguishing this from purely supervised approaches like code2vec and CodeBERT.
- **The ablation study provides useful decomposition** of each component's contribution, with token-level attention showing the largest individual effect (-6.2% when removed).

## Weaknesses

### Fatal

- **Implausible experimental results, particularly on APPS.** The paper reports a 67.5% pass rate on the APPS benchmark using PPO. APPS is a challenging competitive programming benchmark where even large language models with billions of parameters struggle to achieve such rates. A PPO-trained RL agent with a 768-dim architecture achieving 67.5% is extraordinary and completely unsupported by the methodological description. No details are given on episode structure, episode length, or how an RL agent even iteratively generates full program solutions. This severely undermines the credibility of all reported results.
- **Critical experimental details are missing.** The MDP formulation is almost entirely unspecified: What exactly are the states, actions, and reward functions for each of the three tasks? How does the agent interact with the environment over timesteps for code completion or bug repair? Without these details, the experimental setup is non-reproducible and the results cannot be evaluated.

### Major

- **Comparison to LLM-based approaches is absent.** The paper cites Codex (Chen et al., 2021) but does not compare against any LLM-based method, which are the dominant paradigm for all three evaluated tasks. CodeBERT is used as a baseline but is not an RL method—it was fine-tuned for RL here, which is an unusual and questionable adaptation. The baselines are chosen to be weak.
- **No error bars or statistical significance results reported.** Despite claiming p < 0.01 in Section 5.4, Table 1 reports only point estimates with no standard deviations, confidence intervals, or number of runs. The ablation table (Table 2) similarly lacks variance estimates.
- **The RL contribution is not isolated from the architectural contribution.** The ablation (Table 2) removes attention components but never ablates the RL training itself. It is unclear whether the improvements come from the hierarchical attention architecture or from the RL fine-tuning, or both.
- **CodeBLEU is listed with a question mark** ("CodeBLEU score (?)"), indicating the metric was not computed or the paper is incomplete in its metrics evaluation.

### Minor

- **Scalability analysis (Table/Figure 3) is misleading.** Baselines show "-" for higher complexity programs, suggesting they cannot process them. This is not a fair comparison—if the baselines are simply inapplicable at those scales, comparing error rates is not meaningful. The claim of linear memory growth vs. quadratic for transformers is stated without evidence or measurement.
- **Task formulation as RL is a stretch for some tasks.** For code completion, standard supervised autoregressive approaches are well-understood. The paper does not convincingly argue why RL is necessary or beneficial for these tasks compared to supervised fine-tuning.
- **Several references are improperly cited or seem fabricated** (e.g., "Gomez et al., 2025" from "ngruver.github.io", "Guo et al., 2025").

### Trivial

- Section 9 ("The Use of LLM") acknowledges LLM-based polishing but the writing quality throughout is poor, with numerous garbled sentences, incomplete thoughts, and inconsistent terminology.

## Nice-to-Haves

- A comparison against at least one strong LLM baseline (e.g., CodeLlama, StarCoder) would substantially strengthen the evaluation.
- Clear specification of the RL environment (state/action/reward) for each task with pseudocode.
- Human evaluation of code quality beyond automated metrics.
- Analysis of computational cost and training time compared to baselines.

## Novel Insights

None beyond the paper's own contributions. The hierarchical attention idea is sensible but not novel given prior work on SG-Trans and hierarchical code representations. The claim of combining this with RL optimization is the distinguishing idea, but the experimental validation is too questionable to confirm that this combination yields genuine benefits.

## Suggestions

1. Provide complete MDP specifications for all three tasks, including exact reward function definitions and episode structures.
2. Re-run experiments with proper statistical reporting (mean ± std over 5+ seeds) and add LLM-based baselines.
3. If the APPS results are real, provide extensive supplementary material demonstrating the experimental setup, as these numbers would represent a major breakthrough if correct.
4. Ablate the RL training component separately to understand its contribution versus the architectural design.
5. Address the CodeBLEU metric question mark and complete all planned evaluations before submission.

## Score and Decision

The paper proposes a reasonable architectural idea but is undermined by implausible experimental results (particularly on APPS), missing critical experimental details that prevent reproducibility, absence of modern baselines, and poor writing quality. The claimed results cannot be trusted without far more detailed methodology and evidence.

MY FINAL SCORE: <score>2.0</score>
MY FINAL DECISION: <decision>Reject</decision>