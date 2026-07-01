Now I have sufficient calibration. Let me write the final consolidated review.

## Summary

This paper proposes PCE (Planner-Composer-Evaluator), a framework that extracts implicit assumptions from LLM reasoning traces and structures them into a decision tree for uncertainty-aware action selection in multi-agent embodied planning. The key insight is that LLMs already generate environment assumptions internally during reasoning, but handle them fragmentedly. PCE converts these into explicit decision nodes with True/False splits, scores each path by likelihood, gain, and cost, and selects the best action. Experiments on C-WAH and TDW-MAT across three LLM backbones (GPT-4o mini, GPT-OSS:20B, Gemma3:4B) show consistent task-performance improvements over four communication-centric baselines, with ablation and scaling studies confirming the framework's contribution.

## Strengths

1. **The core idea is genuinely novel and well-motivated.** The observation that LLM reasoning traces contain fragmented, implicit assumptions about the environment (Section 4.2, Figure 2-a), and that converting these into an explicit decision tree over assumptions is a meaningful departure from the communication-centric paradigm dominant in this literature. The paper's clearest contribution statement is (lines 27–28): "PCE explicitly treats environmental assumptions as first-class decision variables."

2. **The three-module decomposition (Planner → Composer → Evaluator) is clean and well-explained.** The distinction between extracting assumptions (Composer), evaluating them (Evaluator), and the original reasoning (Planner) structures the problem legibly (Sections 4.2–4.4). The tree construction where internal nodes are assumptions with True/False splits and leaves are actions (Figure 2) is clearly described.

3. **The scaling ablation (Figure 3) is genuinely informative.** Showing that increasing model capacity (Gemma3:4B→12B→27B) or reasoning depth (Low→Medium→High) yields only modest gains for the "Planner only" baseline, while PCE consistently improves across both scales, is the strongest evidence that the framework adds value beyond simply using a bigger model or deeper reasoning.

4. **The evaluation breadth is substantial.** Two benchmarks (C-WAH, TDW-MAT), three diverse backbones (GPT-4o mini, GPT-OSS:20B, Gemma3:4B — spanning commercial, open-source, and reasoning-specialized models), four baselines (CoELA, REVECA, CaPo, CoTS), component ablation, scaling studies, and a user study. PCE achieves the best or second-best task performance across *all* backbone×benchmark combinations.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or statistical significance reported anywhere in the paper.** All metrics are reported as point estimates with no standard deviations, confidence intervals, or statistical tests. This is a serious omission for several reasons: (a) C-WAH has only 10 episodes, where a single outlier can meaningfully shift the average; (b) LLM-based systems are inherently stochastic — different runs of the same prompt can yield different outputs; (c) The user study (N=12) reports no statistical test for Likert ratings, simply stating PCE "scored highest" without indicating whether differences are significant. This cuts across all the paper's main claims. Without this information, the reader cannot assess whether reported improvements are robust or could be noise.

2. **The "comparable token usage" claim in the abstract and conclusion is imprecise.** The abstract states PCE achieves "comparable token usage." On C-WAH this is reasonable (PCE is within 15% of the best baseline). However, on TDW-MAT, PCE's token usage is substantially higher than CoELA (the most token-efficient baseline): 75% higher on GPT-4o mini (197,807 vs. 113,058), 42% higher on GPT-OSS:20B (337,225 vs. 237,498), and 88% higher on Gemma3:4B (184,809 vs. 98,350). While CoELA achieves this token efficiency by being the worst-performing baseline on task metrics — so the comparison is asymmetric — the claim should be qualified. The paper should state that PCE achieves better task performance with token usage comparable to *other* baselines but higher than CoELA, and that the gap is more pronounced in longer-horizon settings (TDW-MAT).

3. **The user study methodology has significant limitations.** (a) Participants were passive observers who "received the same observations and action choices as the agent" (Section 5.3), not active collaborators — yet the abstract and introduction frame this as demonstrating "improved reliability in human-agent collaboration." Perceived trust from an observer's perspective may differ substantially from that of an active collaborator. (b) No statistical analysis is provided for the Likert ratings (Figure 4). With N=12, the observed differences could easily be non-significant. (c) No counterbalancing or randomization of condition order is described, which is important for a within-subjects design vulnerable to order effects and demand characteristics. (d) N=12 is modest even for a pilot study.

### Minor

4. **The framework's LLM-dependence means the "principled" framing is somewhat oversold.** The Composer selects assumptions using an LLM-based "local ranking policy" (Section 4.3), and the Evaluator estimates likelihood, gain, and cost using an LLM (Section 4.4). The decision tree's quality therefore depends entirely on whether the same LLM can reliably rank, expand, and score assumptions when asked in a different prompt format. The paper's language ("principled route," "rational action selection," "structured uncertainty handling") suggests something closer to formal decision-theoretic planning. The paper is transparent about this (Section 4.3: "Rather than computing true probabilities... we approximate these criteria using LLMs' commonsense reasoning"), so the contribution is better described as a structured prompting protocol that elicits better uncertainty-aware reasoning from LLMs.

5. **The cost function does not capture the one-step delay cost of communication.** The problem definition (Section 3) specifies that communication incurs a one-step delay: "messages arrive with a one-step delay, i.e. m_t^i appears in o_{t+1}^i." However, the cost function (Section 4.4, C(a) = α·d(a)·1{move(a)} + β·ℓ(a)·1{comm(a)}) only penalizes communication via message length ℓ(a), not the temporal delay. This means the cost function systematically underestimates the true cost of communication relative to the paper's own problem model.

### Trivial
None.

## Nice-to-Haves

- Reporting decision tree content and quality (e.g., how many assumptions are extracted per step, what fraction are genuinely useful vs. spurious, how often the tree leads to a different action than the Planner's initial choice) would directly validate the mechanism.
- A summary of hyperparameter sensitivity for α, β, λ, and D in the main text (currently deferred entirely to Appendix A.5) would help readers assess robustness.
- The "w/o Planner" ablation (Table 3) triples token consumption (139,918 vs. 44,353) while achieving reasonable performance — analyzing why would add insight.

## Removed Points

- The claim that "the 'comparable token usage' claim is *contradicted* by the data" is removed as too strong. The claim is imprecise/overstated for TDW-MAT vs. CoELA, but PCE's token usage is genuinely comparable to other baselines. Re-framed as weakness #2.
- The criticism that CoELA is "a weak baseline for task performance" is removed. The paper does not claim CoELA is a strong baseline; including a diverse set of baselines is standard practice, and the paper acknowledges CoELA's token efficiency comes at a cost.
- The LLM-dependence criticism was adjusted from the critic's framing of a "methodological gap" to a more measured "framing oversell" (weakness #4), since the paper is transparent about using LLM approximations.
- "Hyperparameter sensitivity deferred to appendix" — moved to Nice-to-Haves, as deferring detailed sensitivity analysis to an appendix is common practice.

## Novel Insights

The harsh critic's most insightful observation is the connection between the three weaknesses: the token usage overclaim, the absence of variance, and the user study limitations together create a pattern where the paper's claims are stronger than its evidence allows it to assert confidently. However, the critic usefully identifies that these are fixable — adding variance bars, qualifying token claims, and strengthening the user study reporting would substantially close this gap. The critic's suggestion to report decision tree quality metrics (how many assumptions per step, how often they change action selection) is a genuinely useful diagnostic that would strengthen the paper beyond what is typically expected.

## Suggestions

1. **Add variance information.** Even 2–3 random seeds with standard deviations for the main results (Tables 1–2) would substantially improve evidential strength. For the user study, report statistical tests (e.g., paired t-tests or Wilcoxon) for the Likert ratings.
2. **Qualify the token usage claim.** Replace "comparable token usage" with a precise statement: "PCE achieves better task performance, with token usage comparable to or lower than most baselines on C-WAH, and moderately higher than the most token-efficient baseline (CoELA) on TDW-MAT while beating all other baselines."
3. **Acknowledge the user study limitations.** Frame it as a third-party perception study rather than "human-agent collaboration," report whether conditions were counterbalanced, and add appropriate caveats about the small sample size and passive-observer design.

## Score and Decision

**Calibration anchors:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| CoELA (EnXJfQqy0K) — same benchmarks, same setting, less novel mechanism | 6.50 | 1, 2 | More novel than CoELA but has evidential gaps CoELA didn't |
| CaPo (KRv9NubipP) — same benchmarks, seen as incremental over CoELA | 6.00 | 1, 2 | PCE has stronger novel contribution than CaPo |
| COMBO (YXRyYkb1im) — same problem area, different technical approach | 6.67 | 2 | PCE less technically ambitious but more practical |
| Tree-Planner (Glcsog6zOe) — tree-based LLM planning, less comprehensive | 5.25 | 1 | PCE has broader evaluation and a more clearly motivated contribution |
| Embodied Instr. Following (pwKokorglv) — less comprehensive | 4.00 | 1 | PCE is substantially stronger on novelty and evaluation breadth |

**Round 1 bracket:** 5.5 – 7.0

**Final score determination.** The paper's core idea — extracting implicit LLM assumptions into an explicit decision tree for uncertainty-aware action selection — is genuinely novel and well-motivated, and the evaluation breadth is substantial. However, the complete absence of variance/statistical reporting across all experiments (including a 12-participant user study with no statistical tests) is a significant evidential gap that prevents a higher score. The token usage overclaim and user study methodological issues further reduce confidence. On balance, the paper sits slightly below CoELA (6.50) — whose contribution was less novel but whose evidence was presented without similar overclaims — and slightly above CaPo (6.00), whose novelty was thinner. Score 6.0 reflects a borderline-accept paper with a clear novel contribution that would be strengthened by addressing the evidential gaps.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>