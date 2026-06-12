## Summary

This paper addresses the problem of aggregating answers from multiple LLMs by moving beyond simple majority voting. The authors propose two algorithms: Optimal Weight (OW), a Bayesian-optimal linear aggregator using first-order accuracy information, and Inverse Surprising Popularity (ISP), a novel second-order aggregator that inverts the logic of Prelec et al.'s surprising popularity rule. The paper provides theoretical guarantees that ISP outperforms majority voting under conditional independence, and validates both methods on simulations and real-world datasets (UltraFeedback, MMLU, ARMMAN).

## Strengths

- **Novel and clean theoretical contribution.** The key insight that surprising popularity (SP) actually *underperforms* majority voting in the LLM setting (Theorem 2), and the subsequent design of ISP to correct for this, is genuinely novel and well-motivated. The intuition—that LLM agents lack the systematic biases SP exploits in human crowds—is clearly articulated and leads to a principled algorithmic fix (Equation 5-6).

- **Strong theoretical foundations.** The Bayesian optimality result for OW (Theorem 1) is elegant, and the connection to the Bradley-Terry model (Corollary 1) provides useful practical insight. The progressive weakening of guarantees from Theorem 1 (exact optimality) through Theorem 2 (expected advantage ordering) to Theorem 3 (finite-sample estimation) is well-structured and technically sound.

- **Practical relevance of the problem setting.** The distinction from mixture-of-experts is clearly drawn. The motivating scenarios—automated dataset annotation without ground truth, prediction markets, and healthcare (ARMMAN)—make a compelling case for the practical importance of unsupervised aggregation methods.

- **Comprehensive experimental validation.** The paper evaluates across synthetic data (varying K), two standard LLM benchmarks (UltraFeedback with K=2, MMLU with K=4), and a real healthcare dataset, using 16 model ensembles from 4 model families. The per-question comparison (Table 4) and hypothesis testing provide rigorous empirical support.

## Weaknesses

### Fatal
None.

### Major

- **Modest empirical gains on real datasets.** The absolute accuracy improvements over majority voting are relatively small: 1.05% on UltraFeedback, 1.05% on MMLU, and 0.54% on ARMMAN (Table 3). While statistically significant, these gains may limit the practical impact. The paper would benefit from a discussion of when these gains matter most—e.g., in large-scale automated annotation pipelines where even small accuracy gains accumulate across millions of queries.

- **Conditional independence assumption is strong for LLMs.** The theoretical guarantees (Theorems 1-3) all depend on conditional independence of LLM predictions given the ground truth. LLMs from the same family (e.g., Qwen models) or trained on similar data will have highly correlated errors. The paper acknowledges this and references Appendix C for extensions, but the experimental results don't carefully examine whether the methods degrade gracefully under correlated agents. A controlled experiment varying the degree of correlation would substantially strengthen the empirical case.

- **Limited range of N (number of agents).** All real-world experiments use exactly N=4 agents. The theoretical results scale with N (e.g., the advantage expressions in Theorem 2), but there is no empirical investigation of whether the methods maintain their edge with larger agent pools (e.g., N=8, 16), which is increasingly common in multi-agent LLM systems.

### Minor

- **OW-L and OW-I yield identical results in Table 3.** This is somewhat surprising and unexplained. If both approaches produce the same estimated accuracies across all datasets, it raises questions about whether the estimation landscape is trivially simple in these settings, or whether one approach is preferred for other reasons (computational cost, robustness).

- **Single Best baseline is not a fair comparison, yet prominent.** The paper acknowledges this explicitly (line "Single Best functions as a clairvoyant oracle"), but the baseline still appears prominently in every table. On MMLU, Single Best outperforms all proposed methods, which could confuse readers about the value proposition.

### Trivial
None.

## Nice-to-Haves

- An analysis of computational cost: OW-L requires solving an optimization problem over N variables; how does this scale and what is the runtime?
- Sensitivity analysis on the random label shuffling preprocessing step.
- Discussion of how to handle agents with accuracy below 1/K (random guessing).

## Novel Insights

The most novel insight is the theoretical demonstration that surprising popularity—a celebrated mechanism from behavioral economics for correcting systematic crowd biases—actually underperforms simple majority voting in the LLM aggregation setting. The paper correctly diagnoses this as arising from the absence of the systematic biases in human crowds that SP was designed to exploit, and then constructs ISP as a principled alternative that amplifies prediction diversity in a controlled manner. This connection between information aggregation theory and multi-agent LLM systems is genuinely new and opens a productive research direction.

## Suggestions

- Add experiments with N=8 or N=16 agents to demonstrate scalability and practical relevance for larger multi-agent pipelines.
- Include a brief analysis of when ISP's advantage over MV is most pronounced (e.g., by conditioning on the degree of agent disagreement or heterogeneity) to help practitioners decide when to adopt it.
- Clarify why OW-L and OW-I produce identical results and whether this holds generally or is an artifact of the specific experimental setup.

## Score and Decision

The paper makes a solid theoretical contribution with clean proofs, introduces a novel algorithm (ISP) with clear motivation, and validates on realistic settings. The empirical gains are modest but consistent and statistically significant. The conditional independence assumption is acknowledged and partially addressed. For a method paper at ICLR, the combination of principled theory and practical validation is valuable, though the limited experimental scope (fixed N=4, modest gains) prevents a strong accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>