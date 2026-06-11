## Summary
# Final Review Report

## Summary

This paper presents PCE (Planner-Composer-Evaluator), a modular framework for LLM-based embodied multi-agent planning under partial observability. The core idea is to extract implicit environmental assumptions from LLM reasoning traces, structure them into a decision (scenario) tree, and evaluate each root-to-leaf path using a utility function combining scenario likelihood, conditional gain, and execution cost. This enables principled action selection with minimal inter-agent communication, addressing the inefficiency of communication-heavy approaches dominant in prior work.

**Strengths at a glance:** (1) The central insight—that LLM reasoning traces already contain fragmented assumptions that can be explicitly aggregated—is well-motivated and practically useful. (2) The PCE pipeline cleanly separates assumption extraction (Planner), structuring (Composer), and evaluation (Evaluator), with each component justified by ablation experiments. (3) The LLM scaling analysis (Figure 3) convincingly shows that PCE provides additive benefits beyond model capacity or reasoning depth gains, which is a non-trivial finding. (4) The user study, despite limitations, provides qualitative evidence that structured uncertainty handling yields interaction patterns humans prefer.

**Key weaknesses:** (1) No statistical significance or variance reporting for any experimental result, making it impossible to assess whether reported gains are robust. (2) The Evaluator scoring function has a scale inconsistency between normalized gain terms (in [0,1]) and unnormalized cost terms that could dominate utility. (3) The token usage claim ("comparable") is overstated based on the data—PCE often consumes more tokens than the best baseline. (4) The user study has methodological limitations (N=12, no counterbalancing, potential demand effects). (5) All experiments are limited to simulated household environments; claims of domain generality are aspirational.

## Strengths
**S1. Well-motivated conceptual contribution.** The paper identifies a genuine limitation of current LLM-based embodied agents: reasoning traces contain implicit, fragmented assumptions that are never explicitly aggregated. Converting these into a structured scenario tree with likelihood-gain-cost evaluation is a principled and novel approach that addresses a real bottleneck in communication-heavy multi-agent planning.

**S2. Clean modular architecture.** The Planner-Composer-Evaluator pipeline is well-designed with clear separation of concerns. The Composer's top-down tree expansion with LLM-approximated ranking (prioritizing assumptions that most reduce uncertainty) is a practical approximation to intractable POMDP planning. Each module's necessity is validated through careful ablation (Table 3).

**S3. Additive benefits beyond scaling.** The LLM scaling analysis (Figure 3) is one of the paper's strongest contributions. Demonstrating that PCE consistently improves performance across model sizes (Gemma3:4B→12B→27B) and reasoning depths, while a "Planner only" baseline shows diminishing returns, provides compelling evidence that structured uncertainty handling is complementary to model scaling. This finding has implications beyond the immediate application.

**S4. Strong empirical results on task performance.** Across 2 benchmarks × 3 LLM backbones × multiple metrics, PCE consistently achieves the best task performance (lowest Total Steps in C-WAH; highest Total/Food/Stuff success in TDW-MAT). The margin over communication-heavy baselines (CoELA, CaPo, CoTS) is substantial, especially in the more challenging TDW-MAT benchmark where PCE outperforms CoTS by 12-22 percentage points.

**S5. Thoughtful differentiation from prior work.** The Related Work section clearly articulates how PCE differs from both communication-heavy approaches (ProAgent, CoELA, REVECA, RoCo, CaPo, CoTS) and tree-based reasoning methods (ToT, CoTS). The key insight—treating communication as an atomic action within the search space rather than as the search mechanism—is well-articulated.

**S6. Human-centric validation.** The user study, while limited in scale, provides initial evidence that PCE's selective communication strategy aligns with human preferences. The finding that both "no communication" and "always communicate" conditions degrade perceived trust and efficiency is intuitive but usefully confirmed.

## Weaknesses
**W1. Absence of statistical uncertainty quantification (Major).** This is the most significant methodological weakness. Across all experiments (Tables 1-3, Figures 3-4), results are reported only as point estimates with no variance, standard deviation, confidence intervals, or significance tests. C-WAH has only 10 episodes (horizon 250); TDW-MAT has 24 episodes. With such small sample sizes, a few outlier episodes could substantially shift reported means. Without knowing the variance, readers cannot assess whether PCE's improvements over the second-best baseline (e.g., 42.76 vs 46.80 Total Steps in C-WAH with GPT-4o mini, a ~9% improvement) are statistically reliable or within noise range.

*Required fix:* Report mean ± std across all episodes/seeds. Add a paired significance test (paired t-test or Wilcoxon signed-rank) between PCE and the strongest baseline (REVECA) for each benchmark. If per-episode variance cannot be provided, add an explicit caveat: "Results are reported as means across N episodes without variance; statistical significance cannot be assessed."

**W2. Scale inconsistency in the Evaluator utility function (Major).** The utility function U(S,a) = E[gain] - λ·C(a) combines expected gain (product of two [0,1]-normalized terms, thus in [0,1]) with cost C(a) = α·d(a)·1{move} + β·l(a)·1{comm}, where d(a) is unnormalized distance (values up to 294 in the paper's example) and l(a) is message length. With α=β=λ=1, C(a) can be orders of magnitude larger than E[gain], which would make the utility ranking entirely cost-driven, contradicting the paper's claim that uncertainty and goal-directedness drive decisions. The reported U values (-0.1 to 0.4) suggest a different normalization is used, but this is not described. This inconsistency undermines the quantitative foundation of the Evaluator.

*Required fix:* Either (a) normalize d(a) and l(a) to [0,1] by dividing by maximum values, or (b) set λ adaptively (λ = 1 / max_{a,S} C(a)) to balance gain and cost terms. Report the normalization procedure explicitly.

**W3. Token usage claim is over-broad (Major).** The abstract and conclusion state PCE achieves "comparable token usage" relative to baselines. However, examination of Tables 1-2 reveals a more nuanced picture: PCE's token usage is competitive in some settings (C-WAH with GPT-4o mini: 44,354—second best) but clearly higher in others (TDW-MAT with GPT-4o mini: 197,807 vs CoELA's 113,058; C-WAH with Gemma3:4B: 50,985 vs REVECA's 44,638). The correct characterization is that PCE trades higher token consumption in some settings for substantially better task performance, achieving a favorable cost-performance trade-off rather than comparability.

*Required fix:* Replace "comparable token usage" with "competitive token usage in some settings" and discuss the cost-performance trade-off explicitly.

**W4. User study methodological limitations (Major).** The user study (N=12) uses a within-subjects design without reported counterbalancing, randomization, or blinding. Participants experienced all three conditions in sequence, creating order effects and demand characteristics. The participant pool is demographically narrow (mean age 26.8, from one institution). The paper does not report effect sizes, confidence intervals, or individual-level data. These limitations mean the study provides suggestive qualitative evidence rather than confirmatory results.

*Required fix:* Acknowledge these limitations explicitly in the user study section. Report effect sizes and confidence intervals for between-condition comparisons. If counterbalancing was used, state it; if not, note this as a limitation.

**W5. Domain generality is asserted without support (Minor).** The conclusion claims "the proposed mechanism is not tied to a specific domain," but all experiments are in simulated household environments (C-WAH and TDW-MAT). No cross-domain evaluation (e.g., warehouse logistics, search-and-rescue, or outdoor navigation) is provided. The generality claim should be presented as a hypothesis for future work rather than a conclusion.

*Required fix:* Replace "the proposed mechanism is not tied to a specific domain" with "the mechanism is designed to be domain-agnostic; validating its generality requires experiments in diverse environments, which we leave as future work."

**W6. Composer's tree expansion policy is underspecified (Minor).** The Composer uses a "local ranking policy" to select which assumption to branch on next, prioritizing those that "most reduce uncertainty and most strongly influence subsequent action choice." The paper states this uses "LLMs' commonsense reasoning" rather than true probabilities. However, no concrete evaluation of the tree quality is provided—how often do the Composer's selected trees match human-expert trees? The authors reference a human-expert correlation study in Appendix A.10 but the main text provides no summary statistics.

*Required fix:* Include at least one quantitative metric of tree quality (e.g., human-expert agreement rate, tree coverage score) in the main text, even if briefly.

**W7. Missing per-step cost decomposition (Minor).** The paper argues that PCE's higher per-step inference cost is offset by episode-length reduction. While this is plausible, no data is provided to decompose Usages into per-step cost and number of steps. Without this decomposition, the explanation cannot be verified.

*Required fix:* Add an appendix table showing average per-step token consumption and average episode length for PCE and each baseline, allowing readers to verify the trade-off mechanism. If this data exists in the appendix (A.4 referenced), cite it explicitly with key numbers in the main text.

**W8. Novelty verification is deferred (Note).** Due to retrieval being unavailable in this review run, all novelty claims—particularly the differentiation from tree-based reasoning methods and the claim that "no prior work has systematically examined whether uncertainty can be resolved by scaling LLMs"—could not be verified against the external literature. These comparisons should be manually verified before publication.

## Score
**Final Score: 6/10**

**Rationale:** The paper has a well-motivated and novel core idea—extracting and structuring implicit assumptions from LLM reasoning traces for uncertainty-aware planning. The PCE framework is cleanly designed, ablation studies convincingly demonstrate the necessity of each component, and the LLM scaling analysis provides evidence that structured uncertainty handling is complementary to model scaling—a finding of broader interest. Empirical results across two benchmarks and three LLM backbones consistently show PCE outperforming strong baselines in task completion.

However, three major methodological gaps prevent a higher score: (1) the complete absence of statistical uncertainty quantification (variance, confidence intervals, significance tests) makes it impossible to assess whether performance gains are robust; (2) the Evaluator's utility function contains a scale inconsistency that is not addressed; and (3) the token usage claim is over-broad relative to the reported data. The user study, while valuable, has methodological limitations that reduce its confirmatory value. Novelty claims could not be externally verified in this review run.

These weaknesses are addressable: adding variance reporting and significance tests is standard practice that should be feasible; fixing the utility normalization requires clarifying existing implementation choices; and toning down the token usage claim is a simple wording change. The core contribution is solid and would stand after these revisions. A revised version addressing W1 and W2 could achieve 7-8/10.