## Summary

This paper proposes PCE (Planner-Composer-Evaluator), a modular framework for multi-agent embodied planning under partial observability. The key insight is that LLM planners already produce implicit assumptions about environmental uncertainty in their reasoning traces but fail to aggregate them. PCE extracts these assumptions, structures them into a binary decision tree, and scores each root-to-leaf path by likelihood, gain, and cost to select actions without heavy inter-agent communication. Experiments on C-WAH and TDW-MAT across three LLM backbones show consistent improvements over communication-centric baselines.

## Strengths

- **A genuinely novel and well-operationalized insight.** The observation that LLM reasoning traces contain implicit, fragmented assumptions about uncertainty — and that these can be extracted and structured into a decision tree — is both intuitively correct and practically actionable. Converting this into a tree over environmental assumptions (rather than over reasoning steps as in ToT, or over communication actions as in CoTS) is a clean and distinctive design choice. (Section 1, lines 23–25; Section 4.3)

- **Consistent empirical wins across all backbones and both benchmarks.** PCE achieves the best task performance on every primary metric in C-WAH (Total Steps) and TDW-MAT (Total/Food/Stuff) across all three LLM backbones (GPT-4o mini, GPT-OSS:20B, Gemma3:4B). This consistency across models and environments rules out the possibility that the method only works for a single configuration. (Tables 1 and 2)

- **Meaningful ablation design that isolates the claimed mechanism.** The component ablation (Table 3) shows that removing any module degrades performance. The scaling ablation (Figure 3) is particularly well-conceived: it demonstrates that the *Planner only* baseline improves only modestly with larger models or deeper reasoning, while PCE consistently outperforms it, convincingly arguing that structured uncertainty handling is additive to and distinct from scaling. (Section 5.2, Table 3, Figure 3)

- **Clear conceptual positioning against related work.** The paper correctly distinguishes PCE from ToT (which operates on cognitive steps under full observability) and CoTS (which treats communication as the search mechanism itself). The framing of communication as "an atomic action within the search space to be evaluated against physical actions" (Section 2, final paragraph) is a crisp formulation that anchors the contribution precisely. (Section 2, paragraphs on Tree-Structured Reasoning)

## Weaknesses

### Fatal

None.

### Major

- **No measure of statistical reliability on very small benchmarks.** C-WAH has 10 episodes; TDW-MAT has 24 episodes. The paper reports only point estimates — no standard deviations, confidence intervals, significance tests, or even a mention of whether results are averaged over multiple runs with different seeds. With n=10, a single unusual episode can shift the mean substantially. The difference between PCE (42.76) and REVECA (46.80) on C-WAH GPT-4o mini is roughly 4 steps out of a 250-step horizon — about 1.6% — and without variance information, neither the superiority over the second-best baseline nor the gap between ablations can be assessed as statistically reliable. Given that the entire empirical case rests on these numbers, this is the paper's most serious weakness. (Section 5, Tables 1–2; no mention of multiple seeds or variance anywhere in the paper)

### Minor

- **The "comparable token usage" claim is overstated for TDW-MAT, and the introduction is inconsistent with the abstract.** The abstract and conclusion claim "comparable token usage." In C-WAH this holds reasonably. But in TDW-MAT (Table 2), PCE uses **1.42–1.88× more tokens** than CoELA across backbones (e.g., 197,807 vs. 113,059 for GPT-4o mini). While this tradeoff may be justified by PCE's much higher success rates (87.5% vs. 62.5%), the paper should acknowledge the increase rather than stating "comparable." Furthermore, the introduction (line 29) claims PCE "outperforms communication-centric baselines in ... token usage" — this stronger claim is not supported in TDW-MAT. (Abstract line 9, Introduction line 29, Conclusion line 282, Table 2)

- **User study is too small and underreported to carry weight.** Twelve participants with no effect sizes, confidence intervals, or significance tests is insufficient to support the claim that "humans perceive [PCE] as more efficient and trustworthy." Participants passively observed agent behavior rather than actively collaborating (they "received the same observations and action choices as the agent"). A bar chart of means without any measure of variability could be driven by a few participants. (Section 5.3, Figure 4)

- **No discussion of how agents' independently constructed trees interact in the decentralized setting.** Each agent runs its own PCE pipeline, but the paper never clarifies whether the decision tree of one agent considers the other agent's tree structure or assumptions. In a truly decentralized setting, agents may reach conflicting conclusions based on different assumption sets. The communication module sends messages, but the relationship between the two agents' trees is not addressed. (Section 3, Section 4)

### Trivial

- The y-axis in Figure 3 starts at ~40 rather than 0, which visually exaggerates the gap between PCE and the Planner-only baseline. A truncated y-axis is a minor presentation concern in an otherwise strong ablation figure. (Figure 3)

## Nice-to-Haves

- **Failure analysis:** The paper presents only positive results. Analyzing episodes where PCE performs poorly (e.g., when the LLM generates poor assumptions, when the tree depth limit D=3 is binding, or when likelihood estimates are poorly calibrated) would strengthen credibility and provide actionable diagnostic insights.
- **Binary uncertainty simplification as a limitation:** The Composer represents assumptions as binary (True/False) nodes, binarizing what is inherently distributional uncertainty. A brief limitations paragraph acknowledging this simplification and discussing whether it loses practically important information would improve intellectual honesty.
- **Justification of D=3:** The tree depth is set to 3 (at most 8 scenarios). The paper does not report whether this limit is ever binding in practice, or whether increasing D changes results. (The paper references hyperparameter sensitivity analysis in Appendix A.5.)

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Composer underspecification:** The harsh critic claimed the Composer's internal mechanism is critically underspecified. However, the main text (Section 4.3) describes the tree structure, the top-down expansion process, the ranking criterion (uncertainty reduction), the use of LLM commonsense for approximation, consistency constraints, and the termination condition. Implementation details and exact prompts are referenced to Appendix A.12 — standard practice for a main conference paper. Removed per Hard Rule: the appendix was stripped by the parser, and the main-text description is at an appropriate level of abstraction.

## Novel Insights

Beyond the paper's own contributions, the reviews surface no genuinely novel synthesis that the paper itself does not already articulate. The reviewers' main constructive insight is that the evidential link between the proposed mechanism (structured assumption handling) and the observed results would benefit from tighter isolation — specifically, showing concrete examples where the tree structure changes action selection relative to what the raw Planner trace would have produced, and attributing that change to better uncertainty handling rather than to other side effects. This is a refinement of the paper's own ablation logic, not a fundamentally new insight.

## Suggestions

1. **Add statistical reporting.** Re-run experiments with multiple seeds and report means with standard deviations or confidence intervals. Even a simple statement about the number of runs and the variance observed would substantially strengthen the empirical case.
2. **Qualify the token usage claim.** Replace "comparable" with a more precise characterization (e.g., "competitive with most baselines" or "higher than CoELA but offset by substantial gains in success rate"). Fix the inconsistency between the introduction's "outperforms...in token usage" and the abstract's more measured wording.
3. **Strengthen the user study** by adding statistical tests (e.g., paired t-tests or Wilcoxon signed-rank tests), reporting effect sizes, and clarifying whether participants were blinded to condition. Even better, consider an interactive study where humans actively collaborate with the agent.
4. **Acknowledge the decentralized interaction gap.** Briefly discuss whether — and how — independently constructed trees might lead to conflicting agent conclusions, and how the communication module resolves this.
5. **Add a failure analysis case study** showing an episode where PCE underperforms, to bound the method's limitations and make the positive results more credible.

## Score and Decision

This paper presents a genuinely novel and well-motivated idea with consistent positive results across benchmarks and backbones. The core contribution is real and distinct from prior work. However, the lack of any statistical reliability measures on very small benchmarks (10 and 24 episodes), combined with an overstated token-usage claim and an underreported user study, prevents full confidence in the quantitative conclusions as currently presented. The weaknesses are fixable — they do not invalidate the core idea — but they warrant addressing before acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>