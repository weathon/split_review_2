## Summary

The paper studies how to aggregate answers from multiple LLMs beyond simple majority voting by leveraging higher-order information: first-order (individual model accuracies) and second-order (correlations between model predictions). The authors propose Optimal Weight (OW) – a Bayesian optimal linear weighting scheme when accuracies are known – and Inverse Surprising Popularity (ISP) – a second-order method designed to provably outperform majority voting when accuracies are unavailable. Theoretical analysis, simulations, and experiments on UltraFeedback, MMLU, and a real-world healthcare dataset (ARMMAN) consistently show that both OW and ISP beat majority voting, with OW extended to unsupervised settings via accuracy estimation from second-order information.

## Strengths

- **Principled theoretical framework.** The paper derives the Bayesian optimal aggregator (OW) under conditional independence, establishing closed-form weights that depend on the inverse of a sigmoid-like function. This result gives a clear theoretical justification for weighted aggregation and connects to the Bradley–Terry model.
- **Novel algorithm with provable guarantees.** ISP is a thoughtfully designed variant of the surprisingly popular rule, adapted to the LLM setting where systematic human biases are absent. Theorem 2 shows ISP is expected to outperform both majority voting and the original SP rule, and Theorem 3 provides a finite-sample guarantee.
- **Comprehensive empirical validation.** Experiments span synthetic data, two standard LLM benchmarks, and a real-world healthcare task, using 16 model combinations across four model families. The methods consistently outperform majority voting (97.92% of ensembles for OW-L), and per-question hypothesis tests confirm statistical significance.
- **Practical adaptation for unsupervised settings.** The paper addresses the key challenge that true accuracies are unknown by estimating accuracies from second-order information (OW-L, OW-I), enabling the use of the Bayesian optimal aggregator without any ground-truth labels. This makes the framework directly applicable to real-world annotation and reasoning pipelines.

## Weaknesses

### Fatal

None.

### Major

- **The conditional independence assumption (Assumption 1) is strong and likely violated in practice.** LLMs often share training data, exhibit correlated failure modes, and are sensitive to question difficulty. While the authors mention extending results in Appendix C, the core theoretical claims and the derivation of OW’s optimality rely on this assumption. The empirical results are encouraging, but the guarantees may not hold when agents are substantially correlated.
- **Missing comparisons to other aggregation baselines.** The paper compares only against majority voting and the original SP rule. Other natural baselines – such as confidence-weighted voting, averaging of logits or probabilities, or Bayesian model averaging – are not evaluated. Including these would strengthen the claim that the proposed methods are practically superior rather than merely better than simple voting.

### Minor

- **The practical gains on real datasets are modest.** Absolute accuracy improvements over majority voting are often less than 1% (e.g., 73.66% vs 72.21% on UltraFeedback, 90.37% vs 89.32% on MMLU). Although the authors correctly note that improvements are concentrated on questions where models disagree (where gains are 2–3%), the overall impact may be incremental for many applications.
- **ISP’s advantage diminishes as \(K\) grows.** Theorem 2 shows the expected improvement scales as \(\Theta(1/K)\), and experiments confirm the gap narrows for larger \(K\). This limits the method’s utility for tasks with many answer choices, which is common in multiple-choice QA.
- **Estimation of second-order information requires large datasets.** Theorem 3 shows the advantage degrades with \(\tilde{O}(\sqrt{1/M})\). The experiments use large datasets (tens of thousands of questions), but for smaller datasets the benefits may vanish. The paper does not explore this boundary empirically.

### Trivial

- Notation overload: \(x_i\) is used for both accuracy and agent index in some equations, causing minor confusion.

## Nice-to-Haves

- **Comparison with alternative aggregation methods** such as confidence-weighted voting or averaging of softmax probabilities, to better position the proposed methods.
- **Sensitivity analysis on the conditional independence assumption**, e.g., by simulating correlated agents with known correlation structures and measuring the degradation of OW/ISP performance.
- **Guidance on choosing between OW-L and OW-I** in practice, as they often tie but may diverge in some settings.

## Novel Insights

Beyond the paper’s own contributions, the analysis of *why* the surprisingly popular rule fails in LLM contexts (compared to human crowds) is insightful. The explanation that LLMs exhibit weaker systematic biases than humans, making SP’s bias-correction mechanism less effective, is a clear conceptual bridge between behavioral economics and multi-agent LLM systems. The inversion to ISP – which amplifies controlled biases – is a principled response to this observation and may inspire similar adaptations of human-centric aggregation methods for AI agents.

## Suggestions

- Add comparisons with confidence-weighted voting or other LLM aggregation baselines (e.g., from recent multi-agent frameworks) to contextualize the improvements.
- Discuss the robustness of OW and ISP when the conditional independence assumption is violated, either through additional simulation experiments or theoretical analysis (e.g., worst-case bounds).
- Provide practical recommendations on the minimum dataset size \(M\) required for ISP to reliably beat majority voting, based on the bound in Theorem 3.

## Score and Decision

The paper presents a well-motivated theoretical framework, novel algorithms, and thorough empirical validation. The main weaknesses (conditional independence assumption and lack of broader baselines) are not fatal and can be addressed in discussion or future work. The contributions are significant for the multi-agent LLM community and represent a clear advance over the default majority voting. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>