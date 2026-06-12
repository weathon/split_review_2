## Summary

This paper introduces PCE, a Planner-Composer-Evaluator framework that extracts implicit assumptions from LLM reasoning traces and organizes them into a decision tree for uncertainty-aware action selection in embodied multi-agent settings. The key contribution is reducing reliance on inter-agent communication by treating environmental assumptions as first-class decision variables, scoring each scenario by likelihood, conditional gain, and execution cost to guide rational action without heavy dialogue. Experiments across two benchmarks and three LLM backbones demonstrate consistent improvements over communication-centric baselines.

## Strengths

- **Well-motivated and clearly articulated problem.** The paper identifies a genuine limitation in current LLM-based embodied agents: their dependence on frequent communication to resolve uncertainty under partial observability, which incurs token/time costs and disrupts human workflows. The motivation is grounded in concrete observations about LLM reasoning traces containing implicit but unstructured assumptions.

- **Novel structural approach to uncertainty handling.** The Composer's decision tree over environmental assumptions (rather than reasoning steps or joint action spaces) is a meaningful conceptual distinction from prior tree-based frameworks like ToT and CoTS. Treating communication as an atomic action evaluated alongside physical actions within the tree is a principled design choice that enables adaptive communication.

- **Comprehensive and consistent experimental evaluation.** The paper evaluates across 2 benchmarks (C-WAH, TDW-MAT), 3 diverse LLM backbones (GPT-4o mini, Gemma3:4B, GPT-OSS:20B), includes component ablations, LLM scaling analyses, MCTS comparisons, and a human user study. PCE consistently achieves the best task performance across all settings while using substantially fewer communication actions (e.g., 1.7–3.0 vs. 4–110 for baselines on C-WAH).

- **Compelling scaling ablation.** Figure 3 demonstrates that increasing model capacity (Gemma3:4B→12B→27B) or reasoning depth (Low→Medium→High) yields only modest gains for the Planner-only baseline, while PCE consistently maintains a performance advantage. This provides meaningful evidence that structured uncertainty handling complements rather than overlaps with scaling.

## Weaknesses

### Fatal
None.

### Major

- **No statistical significance tests or confidence intervals.** C-WAH has only 10 episodes and TDW-MAT has 24 episodes. With such small sample sizes, it is impossible to determine whether the differences between PCE and strong baselines like REVECA (e.g., 42.76 vs. 46.80 steps on C-WAH with GPT-4o mini) are statistically significant. Error bars or bootstrap confidence intervals would substantially strengthen the claims. The paper's central argument — that PCE consistently outperforms baselines — is undermined without this rigor.

- **Token usage claims are mixed.** The abstract claims "comparable token usage," but the results paint a more nuanced picture. On TDW-MAT with GPT-4o mini, PCE uses 197K tokens vs. 113K for CoELA (75% more). On C-WAH with Gemma3:4B, PCE uses 51K vs. 44.6K for REVECA. The paper should more carefully acknowledge that PCE's three-module pipeline can increase per-episode token cost, even though task efficiency improves.

- **DEC-POMDP formulation is disconnected from the method.** Section 3 formally defines a DEC-POMDP, but the actual PCE method does not solve or approximate this formulation. The Composer and Evaluator rely on LLM-based heuristic estimation rather than any principled probability or value computation tied to the DEC-POMDP. This creates a misleading theoretical framing — the formalism suggests rigor that the method does not deliver.

### Minor

- **The Evaluator's scoring reliability is not deeply examined.** Scenario likelihood, conditional gain, and cost are all estimated by LLMs. While Appendix A.10 and A.11 mention correlation studies with human experts, the main paper does not report how accurate these estimates are or how sensitive the final action selection is to estimation errors. Given that the entire action selection hinges on these three scores, more transparency is warranted.

- **User study is small (12 participants).** While the qualitative findings align with the system's design rationale, 12 participants is insufficient for robust statistical conclusions about human perception. The paper appropriately uses this as supplementary evidence rather than a core claim, but future work should include larger-scale studies.

- **Communication metric interpretation.** The paper treats *Comm* as descriptive rather than a success metric, which is reasonable. However, the narrative sometimes implies fewer communications is inherently better (e.g., "suppresses unnecessary communication-driven planning cycles"), while acknowledging that communication can be valuable. A more explicit framework for when communication is and isn't beneficial would strengthen the contribution.

### Trivial
None.

## Nice-to-Haves

- A table or analysis showing when PCE chooses communication vs. physical actions and how this correlates with environment state would provide deeper insight into the mechanism.
- Reporting the variance across episodes/runs would help assess reliability beyond mean performance.
- A comparison of PCE's planning latency per step vs. baselines would complete the efficiency picture.

## Novel Insights

The paper's central insight — that LLM reasoning traces contain latent environmental assumptions that can be extracted, structured, and jointly evaluated as decision variables — offers a genuinely new perspective on uncertainty handling in embodied multi-agent systems. Prior work has treated uncertainty either through communication (exchanging information) or through reasoning augmentation (deeper chains, tree search over reasoning steps), but PCE uniquely identifies that the *content* of assumptions about the environment is itself a valuable structured representation. The finding that scaling model capacity or reasoning depth without explicit uncertainty handling yields diminishing returns (Figure 3) while PCE maintains consistent gains is a noteworthy empirical contribution suggesting that structural approaches to uncertainty and model scaling address complementary dimensions of the planning problem.

## Suggestions

- Add confidence intervals and statistical tests (e.g., Wilcoxon signed-rank across episodes) for all reported metrics, particularly for C-WAH where only 10 episodes exist.
- Include a breakdown of PCE's per-step latency to demonstrate that the three-module pipeline does not introduce prohibitive computational overhead.
- Soften or qualify the DEC-POMDP framing in Section 3 to more accurately reflect that PCE is a heuristic approach inspired by rather than solving the formal DEC-POMDP.

## Score and Decision

The paper presents a clear, well-motivated contribution with a novel mechanism for structuring latent assumptions in LLM reasoning into actionable decision trees. The experimental design is thorough and results are consistently positive across settings. However, the lack of statistical significance testing on small benchmark instances, some overstatements regarding token efficiency, and a disconnect between the formal DEC-POMDP framing and the heuristic method temper the contribution. These issues are addressable and do not invalidate the core claims, but they weaken the evidentiary foundation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>