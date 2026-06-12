## Summary

This paper proposes PCE (Planner-Composer-Evaluator), a framework that extracts the implicit assumptions embedded in LLM reasoning traces for multi-agent embodied agents and structures them into a decision tree. By scoring each root-to-leaf scenario path by likelihood, goal-directed gain, and execution cost, PCE selects actions under partial observability without heavy communication. Experiments on C-WAH and TDW-MAT benchmarks across three diverse LLM backbones (including small open-source models) show consistent improvements over communication-centric baselines in success rate and task efficiency while maintaining comparable token usage. Ablations, scalability tests, and a user study further confirm the value of explicit uncertainty handling.

## Strengths

- **Novel and well-motivated approach**  
  The insight—that LLM reasoning traces contain fragmented, implicit assumptions about the environment, and that aggregating these into a structured tree can reduce reliance on costly communication—is original and clearly motivated by the limitations of existing communication-heavy methods.

- **Strong empirical results across diverse settings**  
  PCE consistently outperforms four strong baselines (CoELA, REVECA, CaPo, CoTS) on two challenging benchmarks (C-WAH and TDW-MAT) and across three very different LLM backbones (GPT-4o mini, GPT-OSS:20B, Gemma3:4B). Improvements are substantial (e.g., C-WAH steps 42.76 vs. 60.40; TDW-MAT total 87.50% vs. 62.50% on GPT-4o mini) and token usage is competitive, often lower than baselines.

- **Thorough evaluation and ablation design**  
  The paper includes component ablations, scaling analyses (model capacity from 4B→27B, reasoning depth), comparisons with reasoning-centric methods (CoT, ToT, Self-Consistency), scalability tests with more agents, and a human user study. This multi-faceted evaluation convincingly supports the claim that gains come from structured uncertainty handling rather than scaling alone.

- **Generality and practical relevance**  
  PCE operates on generic reasoning traces, not model internals, making it applicable to any LLM backbone. The user study demonstrates that the resulting communication patterns are perceived by humans as more efficient and trustworthy, increasing real-world applicability.

## Weaknesses

### Fatal
None.

### Major

- **Reliance on LLM quality for assumption extraction and scoring**  
  The Composer’s ability to identify relevant assumptions and the Evaluator’s estimates of likelihood, gain, and cost both depend heavily on the LLM’s commonsense and reasoning capabilities. If the LLM produces poor or inconsistent assumptions (e.g., on smaller models), the decision tree may be misleading. While results across backbones (including Gemma3:4B) are encouraging, the paper does not quantify how often the extracted assumptions are correct or how assumption errors propagate.

- **Limited depth and exploration of the decision tree**  
  The tree is expanded to a fixed depth (D=3) and stops early when further splits are deemed unproductive. No ablation on D is provided, making it unclear how sensitive performance is to this hyperparameter or whether deeper trees could improve results on more complex tasks.

- **Potential over-fitting to the specific problem formulation**  
  The DEC-POMDP model assumes costly communication with uniform one-step delay and explicit token costs. Real-world human-agent collaboration may involve richer communication dynamics (e.g., asynchronous messages, non-verbal cues, variable latency). The paper’s claims about “reducing communication overhead” are validated only within this specific setup.

### Minor

- **User study is relatively small (12 participants)**  
  While the clear gap in Likert scores is encouraging, the sample size limits statistical power and generalizability. The paper could note this limitation more explicitly.

- **Token usage definition includes all internal LLM tokens**  
  This is a reasonable system-level cost, but it conflates communication tokens with planning tokens. Some readers may prefer a breakdown to better understand where savings come from.

### Trivial

None.

## Nice-to-Haves

- A sensitivity analysis on the tree depth hyperparameter D would strengthen the claim of robustness.
- A breakdown of token usage into planning vs. communication would provide finer-grained insight into cost savings.
- Reporting variance (error bars or confidence intervals) for the main results would further increase credibility.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that LLM reasoning traces already contain the seeds of uncertainty resolution—they are not merely action justifications but can be systematically “read” to extract probabilistic assumptions about the environment. This reframes the problem from “how to gather information” to “how to organize what the model already knows it does not know.” The observation that scaling model size or reasoning depth alone yields only marginal improvement, while explicit structuring of these assumptions adds substantial and consistent gains, suggests a complementary axis for improving LLM-based planners: reasoning about uncertainty at the meta-level, not just deeper chains of reasoning.

## Suggestions

- Provide an ablation varying the tree depth D (e.g., D=1,2,3,4) to show sensitivity.
- Report confidence intervals or standard deviations for the main metrics across the 10/24 episodes.
- In the user study, include a free-text question asking participants to describe what they liked or disliked about the agent’s communication, to supplement the Likert scales.

## Score and Decision

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>