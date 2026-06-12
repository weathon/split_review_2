## Summary

DRE-Bench proposes a dynamic reasoning evaluation benchmark for LLMs, organized around a four-level cognitive hierarchy (Attribute → Spatial → Sequential → Conceptual) grounded in psychology (Primi, 2001). The benchmark uses a code-based generator/solver pipeline to dynamically produce abstract reasoning test instances with varying complexity, addressing data contamination concerns in static benchmarks. The paper evaluates 11 LLMs and finds that while models perform reasonably at lower cognitive levels, performance degrades sharply at higher levels, especially for tasks requiring conceptual/physics knowledge.

## Strengths

1. **Psychology-grounded task hierarchy with human validation.** The four-level cognitive framework is explicitly mapped to Primi (2001), which is a principled move beyond ad-hoc benchmark design. The human study (Section 4.2, ~400 cases, 40 annotators) provides supporting evidence that the hierarchy reflects genuine difficulty ordering — human accuracy declines across levels as expected (77.5% → 70.4% → 65.0% → 47.3%). This validation is uncommon in benchmark papers.

2. **Code-based generator/solver pipeline for dynamic evaluation.** The human-agent collaboration pipeline (Section 3.2) produces parameterized code functions enabling dynamic data generation, verifiability through test-time consistency checks, and scalability to new rules. This is a genuine engineering contribution that addresses the data contamination problem that plagues static benchmarks.

3. **Interesting behavioral findings.** The analysis of spatial orientation biases (Section 4.5, Table 3) — showing that models perform better on vertical than horizontal movement and on horizontal than vertical symmetry — is a genuinely non-obvious result that the benchmark design enables. Similarly, the finding that visual information does not meaningfully help (Table 2) and that inference-time scaling has diminishing returns at higher cognitive levels (Figure 7) are nontrivial observations.

## Weaknesses

### Fatal
None.

### Major

1. **Duplicate model entry and unexplained averages in Table 1 erode data integrity.** The table lists "o3-mini" twice (lines 148–149) with wildly different results — one row shows Avg-2 (Spatial) = 91.78 with all Level-4 scores at 0.00, while the other shows Avg-2 = 23.13 with Mechanics = 31.75 and Avg-4 = 10.58. These cannot both be correct for the same model under the same evaluation procedure. The second row almost certainly corresponds to a different model (o1-mini, which appears in Figure 4 and Table 3 but is absent from Table 1 proper) but is mislabeled. Additionally, the "Avg" columns do not correspond to simple arithmetic means of the three task scores within each level (e.g., Claude-3.7 Level-1: (65.22+63.14+13.33)/3 = 47.23, but the table reports Avg-1 = 58.76; Level-3: (54.44+2.50+54.44)/3 = 37.13, but Avg-3 = 44.05). If the averages are weighted or computed differently, the scheme must be explained. As presented, these issues undermine trust in the reported results and must be corrected.

2. **Level-4 tasks conflate fluid and crystallized intelligence, creating a framing gap.** The paper's title and abstract foreground "fluid intelligence" (the ability to reason in novel situations independently of acquired knowledge). However, Level-4 tasks (Gravity, Reflection, Expansion) require application of specific physics knowledge that models may have memorized during training — this draws on crystallized rather than fluid intelligence. The paper acknowledges this implicitly (line 121: "requires not only high-level abstract reasoning but also the application of conceptual knowledge") but does not address how to disentangle the two. This framing gap between what the benchmark measures and what it claims to measure is a structural limitation.

### Minor

1. **The "Shape" task within Level-1 is a severe outlier left undiscussed.** In Table 1, the "Shape" task produces accuracy of 8–18% for nearly all models (exceptions: o1 at 58.33% and one o3-mini row at 71.67%), while the other two Level-1 tasks (Size, Count) produce 40–80% accuracy. If Level-1 represents the simplest cognitive tier, a task where almost all models score below 20% is inconsistent with that framing and should be discussed. This within-level variance weakens the claim that the four levels constitute a clean hierarchy.

2. **Column label inconsistency in Table 1.** The Level-4 columns are labeled "Optics," "Mechanics," "Thermal," while Section 3.1 and Figure 2 describe these tasks as "Gravity," "Reflection," "Expansion." The relationship between these naming conventions is not explained.

3. **Overstated ICL claim relative to evidence.** The paper claims "increasing the number of in-context samples helps models better capture underlying rules" (line 214), but Figure 6 shows only marginal improvements (e.g., Level-2: ~60% → ~62%). A 2-point gain does not strongly support the "helps models better capture rules" framing.

4. **Visual information analysis is based on only 2 models.** Table 2 tests auxiliary visual information only on GPT-4o and Claude-3.7, yet the conclusion generalizes to "current models" broadly.

5. **Human study lacks inter-annotator agreement metrics.** With 40 annotators handling ~10 cases each, per-annotator variance could be significant, but no inter-annotator agreement (e.g., Krippendorff's alpha) is reported.

6. **"First dynamic evaluation for abstract reasoning" claim is too strong.** Line 93 states "we are the first to introduce a dynamic evaluation paradigm for abstract reasoning tasks." The contribution is significant enough without this framing, which risks being inaccurate given prior community efforts around procedural generation for abstract reasoning.

### Trivial
None.

## Nice-to-Haves
- Address the fluid/crystallized confound in Level-4 by either reframing the benchmark's scope or adding a control condition with fictional physical rules to isolate abstract reasoning from knowledge application.
- Discuss what distinguishes easy vs. hard tasks within a level (especially the "Shape" outlier), which would deepen the cognitive analysis.
- Report error bars alongside point estimates in Table 1 for improved transparency.

## Removed Points
- Weakness about "36 tasks claim not supported by paper" — Removed because the paper states "approximately three tasks for each rule" (line 125) and gives explicit examples (Move has 5 directional sub-tasks), which supports the abstract's claim.
- Weakness about no error bars — Demoted to Nice-to-Have because variance is shown separately in Figure 5 for top models, and single-run reporting without confidence intervals is standard for many LLM benchmarks.
- Weakness about data contamination claims not being tested — Removed because testing contamination resistance would require a separate dedicated study beyond the benchmark's scope.
- Weakness about missing model parameter counts — Removed because several models are API-based where parameters are not publicly disclosed.
- Various section-by-section presentation nitpicks that are too granular or subsumed by points above.

## Novel Insights
The spatial orientation bias finding (vertical > horizontal movement; horizontal > vertical symmetry) is the most novel insight — it reveals a systematic divergence between LLM and human spatial processing that the benchmark is uniquely positioned to detect. The finding that inference-time scaling shows diminishing returns specifically at higher cognitive levels (planning tasks plateau despite increased compute) is also a non-obvious result worth highlighting, as it suggests architectural limits beyond what test-time compute alone can address.

## Suggestions
1. Fix the duplicate "o3-mini" row — relabel the second entry to its actual model name (likely o1-mini, which appears elsewhere in the paper).
2. Explain the averaging scheme used for the "Avg" columns in Table 1, or recompute them as simple arithmetic means.
3. Clarify the relationship between "Optics/Mechanics/Thermal" and "Gravity/Reflection/Expansion" column labels.
4. Add a discussion of the "Shape" outlier within Level-1 and what it implies about within-level difficulty variance.
5. Revise the framing of Level-4 tasks to clarify the relationship between fluid and crystallized intelligence, or add a control experiment with fictional physical rules.
6. Tone down the "first" claim to avoid unnecessary controversy.

## Score and Decision

**Calibration anchors used (all rounds):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Large Language Models Are Not Strong Abstract Reasoners | 5.33 (Reject) | R1 | Most directly comparable — also introduces an abstract reasoning benchmark for LLMs. DRE-Bench has stronger novelty (dynamic pipeline, cognitive hierarchy, human validation) but weaker data transparency (duplicate row, unexplained averages). |
| KOR-Bench | 7.00 (Accept) | R1 | Knowledge-orthogonal reasoning benchmark. Cleaner execution and better framing than DRE-Bench, which has more principled cognitive grounding but worse presentation. |
| Alice in Wonderland | 5.20 (Reject) | R1 | Narrow single-question reasoning study. DRE-Bench is broader and more systematic, but the Alice paper has cleaner data. |
| TurtleBench | 3.80 (Reject) | R1 | Dynamic evaluation benchmark for reasoning. DRE-Bench has better methodology and more thorough validation. |
| ActionReasoningBench | 6.75 (Accept) | R1 | Well-executed reasoning benchmark. DRE-Bench's cognitive hierarchy and human validation are distinct strengths, but its data issues are more serious. |
| ReCogLab | 5.00 (Accept) | R2 | Cognition-inspired reasoning framework. Similar in ambition; DRE-Bench has more tasks but less polished presentation. |
| LiveCodeBench | 6.25 (Accept) | R2 | Dynamic contamination-free code benchmark. Better execution quality in a different domain. |
| M3GIA | 4.33 (Reject) | R2 | Cognition-inspired multimodal benchmark. DRE-Bench is stronger on both methodology and validation. |

**Round 1 bracket:** 4.0 – 5.5

**Round 2 narrowing:** The closest comparator is "Large Language Models Are Not Strong Abstract Reasoners" (5.33, Reject). DRE-Bench has stronger technical contributions (dynamic generation, human-validated hierarchy) but also has more serious data presentation flaws. KOR-Bench at 7.00 (Accept) sets an upper bound — DRE-Bench lacks that paper's clarity and polish. The data integrity concerns (duplicate row, unexplained averages) are significant enough to prevent acceptance in the current form, but the core contributions are genuine and fixable.

**Final score:** 5.0

**Final decision:** Reject — The paper makes real contributions (cognitively grounded hierarchy, dynamic generation pipeline, interesting behavioral findings) that I would like to see in the community. However, the duplicate model entry and unexplained averaging scheme in Table 1 significantly undermine confidence in the reported results, and the Level-4 framing gap creates a mismatch between what the benchmark measures and what it claims. These issues are fixable, and a carefully revised version could be strong.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>