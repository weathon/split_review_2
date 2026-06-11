## Summary
# Final Review Report

## Summary

This paper presents PLAGUE, a plug-and-play framework for generating multi-turn jailbreak attacks against Large Language Models. The framework decomposes the attack lifecycle into three phases — Planner (strategy generation and retrieval), Primer (adversarial context building), and Finisher (goal-driven exploitation) — supported by a lifelong learning component that stores successful attack strategies in a vector memory bank for future retrieval. Evaluated on the HarmBench benchmark (200 goals) across 5 frontier models (OpenAI o3, o1, Deepseek-R1, Claude Opus 4.1, Llama 3.3-70B), PLAGUE achieves strong Attack Success Rates (SRE) of 81.4% on o3 and 97.8% on Deepseek-R1 under a 6-turn budget.

**Strengths:** The plug-and-play design is practically motivated; the ablation study systematically disentangles the contribution of backtracing, reflection, planning, and strategy retrieval; the paper evaluates across multiple state-of-the-art models using consistent evaluation protocols.

**Key weaknesses:** (1) No variance or significance reporting for main results — critical for stochastic LLM-based attacks; (2) Baseline modifications are unquantified, making "apples-to-apples" comparison claims unverifiable; (3) The lifelong learning claim is not supported by longitudinal experiments showing improvement over successive attack goals; (4) The paper overclaims in multiple places (GPT-4o results not in tables, "robustness" framing in conclusion); (5) Reproducibility is limited by undisclosed strategy library contents and removed appendix content; (6) Novelty cannot be independently verified due to Retrieval-Disabled Mode.

**Note on novelty verification:** External literature search was unavailable in this run (API token missing). All novelty/comparison conclusions are marked as deferred and require manual literature verification before acceptance decisions.

## Strengths
1. **Practically motivated plug-and-play design.** The three-phase decomposition (Planner, Primer, Finisher) is a sensible modularization of the multi-turn attack process. Separating plan generation, context construction, and exploitation allows independent optimization of each phase. The demonstrated ability to swap Finisher modules (GOAT vs. Crescendo) to improve performance on different target models (e.g., Crescendo works better on Claude Opus 4.1) provides direct evidence that modularity has practical utility for red-teaming operations.

2. **Comprehensive ablation study.** Table 3 provides a clean, additive ablation that isolates the contribution of backtracing (BT), reflection (R), planning (P), and strategy retrieval (RSS) — a rare and valuable feature for multi-turn attack literature. The observation that different components dominate for different models (reflection for o3, backtracking for Claude) is an actionable insight for safety researchers. The paper correctly identifies that component importance varies by target model, which has practical implications for attack design.

3. **Broad and consistent evaluation.** Evaluating across 5 frontier models (o3, o1, Deepseek-R1, Claude Opus 4.1, Llama 3.3-70B) under a unified evaluation protocol with two complementary metrics (SRE and Bin-ASR) provides a reasonably comprehensive picture. The budget-controlled evaluation (6-turn cap) and ASR@K reporting are sensible methodological choices.

4. **Efficiency analysis.** Table 5 provides useful information about the computational cost of different attacks, breaking down Target LLM calls, Evaluator calls, and Planner calls. The finding that PLAGUE's total call count is comparable to Crescendo while delivering higher performance is a concrete efficiency advantage.

5. **Clear positioning against existing work.** Table 1 systematically compares existing multi-turn methods across 6 dimensions (lifelong learning, planning, reflection, open source, backtracking, external knowledge base), making it easy to see where PLAGUE differs from prior approaches.

## Weaknesses
### Critical

1. **Missing variance and statistical reliability.** The paper reports mean scores over 3 runs but provides no standard deviations, confidence intervals, or significance tests. Given the high stochasticity of LLM-based attacks (different model responses, varying backtracking paths, ASR@K selection), the reported differences between PLAGUE and baselines cannot be assessed for statistical reliability. For example, on Deepseek-R1, both PLAGUE and GOAT achieve 0.978 SRE — the score is identical, yet the paper claims superiority. On Llama 3.3-70B, PLAGUE achieves 0.958 vs. GOAT 0.95 — a 0.8 percentage point difference that falls well within typical LLM output variance. Without variance estimates, readers cannot determine which comparisons reflect genuine improvement and which are noise. *(See annotation: Page 1 - Section 5.1 Attack Performance)*

2. **Unquantified baseline modifications.** The paper modifies baseline implementations (GOAT with per-round scoring, ActorBreaker limited to K=2) but does not quantify the impact of these changes. The claim of "apples-to-apples comparison" is unverifiable without showing original-vs-modified performance for each baseline. If the modified baselines underperform their original configurations, PLAGUE's relative gains may be inflated. *(See annotation: Page 1 - Section 4 Experimental Setup)*

### Major

3. **Lifelong learning claim not substantiated by longitudinal evidence.** The paper states PLAGUE "is the first multi-turn attack to feature a lifelong-learning component," but the only evidence provided is an ablation showing that adding strategy retrieval (RSS) to the full system improves ASR. This is a static comparison, not a demonstration of learning over time. To support lifelong learning, the paper must show that ASR improves as the system accumulates experience across successive attack goals — for example, comparing performance on the first 50 vs. last 50 HarmBench goals, or showing ASR growth as the strategy library expands. Without such evidence, the claim reduces to "retrieving similar past strategies helps," which is already known from single-turn work (AutoDAN-Turbo) and is not a demonstration of lifelong learning. *(See annotation: Page 1 - Section 3.5 Lifelong Learning)*

4. **Overclaiming and unsupported statements.** Several claims in the paper are not supported by the presented evidence:
   - The abstract and introduction claim "GPT-4o" as a target model, but Table 2 does not include GPT-4o results, making this claim unverifiable.
   - The abstract states "improving ASR by more than 30% across leading models," but Table 2 shows this only holds for specific comparisons (o3 vs. ActorBreaker, Opus 4.1 vs. Crescendo) — many models show much smaller gains (Deepseek-R1: 0.978 vs. 0.978).
   - The conclusion claims PLAGUE "advance[s] the frontiers of building robust LLM systems," but the paper only demonstrates breaking systems, not building robust ones.
   - "Factor of 32.14%" uses "factor" to mean relative percentage improvement, which is misleading (a factor typically implies multiplicative scaling: 1.32x, not 32% relative). *(See annotations: Page 1 - Abstract; Page 1 - Introduction Paragraph 4; Page 1 - Conclusion)*

5. **Rubric scorer decision criteria not fully specified.** The mapping from rubric scores (Compliance 2pt, Practicality 2pt, Level of Detail 2pt, Relevance 4pt) to backtracking thresholds (7/10 Primer, 3/10 Finisher) and success criteria (8/10) is not fully defined. Key questions: Can an attack be "successful" with Compliance=0? How are ties broken? Were these thresholds tuned on the same HarmBench data used for reporting? The paper should provide a complete rubric-to-decision matrix. *(See annotation: Page 1 - Section 3.2 Rubric Scorer)*

6. **Strategy library initialization is a potential confound.** The paper initializes the strategy library with "two strategies adapted from examples in Crescendo" but does not disclose what these strategies are. Given the authors' own observation that in AutoDAN-Turbo "only human-generated strategies appended during initialization seem to yield a discernible improvement" — a pattern that could apply to PLAGUE as well — the initial strategies should be fully disclosed. An empty-library ablation would clarify whether gains come from the initial curated strategies or from the retrieval/lifelong learning mechanism. *(See annotation: Page 1 - Section 3.3 Planner Phase)*

7. **Premature conclusive language on semantic drift.** The introduction claims PLAGUE avoids "common pitfalls such as semantic drifts in the generated context," but no explicit measurement of semantic drift is reported in the experiments. The Primer phase's design rationale (anchoring to intermediate plan steps) is promising, but the paper should present evidence that PLAGUE-generated context indeed exhibits less drift than Crescendo or GOAT — for example, by measuring cosine similarity between consecutive queries or computing semantic relevance scores to the original goal. *(See annotation: Page 1 - Introduction Paragraph 3)*

8. **ASR formula conflates attack execution with evaluation.** The defined ASR$(\mathbb{J})$ takes the form $\frac{1}{P}\sum \mathbb{J}(p_i, \text{MT}_i)$, which passes the full multi-turn attack as input to the evaluator. However, the paper states that for successful attacks, only the final query is evaluated. This discrepancy should be resolved. Additionally, the notation $\mathbb{R}^{(+)}$ for the memory bank conflicts with $\mathbb{R}$ for the Rubric Scorer. *(See annotation: Page 1 - Section 3.2 Attack Setup)*

### Minor

9. **Related work reads as a sequential list.** The multi-turn red-teaming paragraph catalogs methods one after another without organizing around comparative axes (e.g., planning-based vs. feedback-based, static vs. adaptive strategies). A restructured comparison would better position PLAGUE's contribution. *(See annotation: Page 1 - Section 2.2)*

10. **Primer backtracking frequency unreported.** The paper defines a 7/10 threshold for backtracking but does not report how often backtracking occurs in practice. Since backtracking removes turns from the target's history while keeping them in the attacker's history, its effect on conversation coherence and budget usage should be analyzed. *(See annotation: Page 1 - Section 3.4 Primer Phase)*

11. **"Frozen context" underspecified.** The description of context freezing between Primer and Finisher phases is ambiguous about exactly what is preserved and how the Finisher uses the accumulated context. This is a reproducibility concern for practitioners trying to implement the framework. *(See annotation: Page 1 - Section 3.1 Attack Overview)*

12. **Novelty cannot be verified in this run.** Due to Retrieval-Disabled Mode (external paper search not available), all novelty claims — including the claim of being "the first multi-turn attack to feature a lifelong-learning component" — must be treated as deferred for manual verification. The landscape of multi-turn jailbreak attacks is rapidly evolving (AutoRedTeamer, concurrent works), and independent verification against the latest literature is essential before accepting these claims.

### Defect Ranking Board (Top 5 by Severity)

| Rank | Defect | Severity | Validity Risk | Fixability | Confidence |
|------|--------|----------|---------------|------------|------------|
| 1 | Missing variance/statistics for main results | Critical | High — undermines all quantitative claims | Easy — report std over seeds | High |
| 2 | Baseline modifications unquantified | Critical | High — may inflate relative gains | Medium — add comparison table | High |
| 3 | Lifelong learning lacks longitudinal evidence | Major | High — core novelty claim unsupported | Medium — add sequential block experiment | High |
| 4 | Overclaiming (GPT-4o, "robustness", "factor") | Major | Medium — affects credibility, not validity | Easy — correct wording | High |
| 5 | Rubric scorer criteria underspecified | Major | Medium — affects reproducibility | Easy — add decision matrix | Medium |

### Page Coverage Audit

The paper is rendered as a single physical page (Page 1) with logical sections separated by horizontal rules. All 16 annotations cover this logical page. Coverage across logical sections:
- Abstract: 1 annotation
- Introduction (paragraphs 1-5): 5 annotations
- Related Work (Sections 2.1-2.3): 1 annotation
- Method (Sections 3.1-3.5): 4 annotations
- Experimental Setup (Section 4): 1 annotation
- Results and Discussion (Sections 5.1-5.2): 1 annotation
- Conclusion (Section 6): 1 annotation
- Additional (notation/clarity): 2 annotations

All substantive paragraphs in Abstract, Introduction, Method, Experiments (Setup + Results), and Conclusion are covered by at least one annotation.

## Score
**Final Score: 5.5/10**

**Rationale:** The paper addresses an important and timely problem (multi-turn LLM jailbreak attacks) with a modular framework design that is practically motivated. The plug-and-play architecture and systematic ablation are genuine strengths. However, the evaluation has critical gaps that prevent higher scoring: absence of variance/statistical reporting undermines confidence in the quantitative claims; baseline modifications are not validated against original implementations; the core novelty claim of "lifelong learning" lacks longitudinal evidence; and multiple instances of overclaiming (GPT-4o, "robustness" framing) reduce the paper's scientific defensibility. The paper's value is primarily in its framework design and ablation insights rather than in the absolute ASR numbers reported. Novelty verification is deferred due to unavailable literature access.

**Research value assessment:** The plug-and-play framework concept has practical value for red-teaming operations. The component-level analysis (which module helps which model) provides actionable guidance. However, the claimed "lifelong learning" advance is not yet demonstrated, and several strong empirical claims require additional statistical support.

**External literature verification:** Unavailable in this run (paper_search API token not provided). All novelty/comparison conclusions are intentionally deferred for manual verification.