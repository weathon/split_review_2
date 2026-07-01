Good, I have my calibration anchors. Let me write the final review.

**Round 1 bracket**: 5.5–6.5 (based on 6 calibration queries across all bands; papers below 3.5 are clearly weaker, 8.0 band is clearly stronger, and the 5.5–7.5 band contained the most topically similar accepted papers).

**Narrowing**: Within this band, the most comparable paper, "How to Correctly Do Semantic Backpropagation on Language-based Agentic Systems" (5.50), was rejected, while "Agent Skill Acquisition via CycleQD" (6.00), "Dynamic Workflow Updating" (6.25), and "WorkflowLLM" (6.25) were accepted. MermaidFlow has a genuinely novel representation-level contribution that is stronger than some of these, but has evaluation gaps (unvalidated LLM-as-Judge, no variance reporting) that prevent it from reaching the 6.25+ level.

**Final score**: 6.0.

Here is the final review:

---

## Summary

MermaidFlow introduces a typed, declarative graph representation (using the Mermaid markup language) for agentic workflow generation, combined with safety-constrained evolutionary programming operators that preserve structural validity during search. The core insight is that representing workflows as structured Mermaid graphs enables static verification of type safety and connectivity before translation to executable Python code, dramatically reducing the rate of invalid candidates that plagues code-level search. The paper reports consistent improvements over baselines on GSM8K, MATH, HumanEval, and MBPP.

## Strengths

- **Novel representation-level contribution.** Using Mermaid (a typed, declarative graph language) as an intermediate representation that can be statically checked for structural validity and then translated to code is a genuinely novel idea. The formalization of workflow graphs as \(G(\mathcal{V}_{[\tau,\alpha]}, \mathcal{E}_{[\rho]})\) with typed nodes and role-labeled edges (Section 3.1) provides a clean separation between planning and execution that prior code-level representations (Python, JSON trees) lack.

- **Well-specified EP operators with formal correctness properties.** The six operators in Section 4.1 (Node Substitution, Node Addition, Edge Rewiring, Node Deletion, Subgraph Mutation, Crossover) are each defined with explicit type-consistency preconditions, and Lemma 1 states a formal invariance property (the search space is closed under valid EP operations). This level of formal specification is uncommon in the agentic workflow literature and adds rigor.

- **Consistent empirical gains across all four benchmarks.** In Table 1, MermaidFlow achieves the best average accuracy on every benchmark (80.75% vs. 79.35% for the best baseline, MaAS). The >90% valid code generation rate (vs. ~50% for AFlow, reported in Section 5.3) provides concrete evidence for the representation's practical advantage in maintaining search-space validity.

## Weaknesses

### Major

- **LLM-as-Judge used for candidate selection without any validation.** Section 4.2 describes selecting which candidate workflow to execute based on an LLM-as-Judge score ("semantic fit, structure, and task relevance"), with only the highest-scoring candidate being actually validated and added to the history buffer. The paper provides zero evidence that this judge's rankings correlate with actual execution performance. Since the search trajectory is partly determined by this proxy scorer, it is impossible to attribute the empirical gains to the Mermaid representation versus the judge's unvalidated preferences. An ablation comparing LLM-judge-based selection against execution-feedback-based selection (or random selection) is necessary to isolate the source of improvement.

- **No variance reporting despite small margins.** Table 1 reports results "averaged over three runs" with no standard deviations, confidence intervals, or individual run values. The average improvement over the best baseline is 1.40% absolute (80.75% vs. 79.35%), and individual benchmark margins range from 0.14% (MBPP: 82.31 vs. 82.17) to 2.61% (MATH: 55.42 vs. 52.81). Without variance estimates, it is impossible to assess whether these differences are statistically significant or within run-to-run noise.

- **Non-uniform comparison on one benchmark.** The MBPP result for MaAS (82.17) is marked with * as "reported in the MaAS paper" rather than re-run under the same conditions. This creates a non-uniform comparison—the MaAS value may come from a different setup—and since the MBPP margin over MaAS is only 0.14%, this undermines the claimed improvement on that dataset.

### Minor

- **Multi-agent framing not reflected in evaluation.** The paper motivates the problem with multi-agent coordination failures (Cemri et al., 2025; Zhang et al., 2024a; 2025c), but evaluates on GSM8K, MATH, HumanEval, and MBPP—benchmarks where workflows are primarily single-agent prompt chains and ensembles. While these are the standard benchmarks used by all baselines (AFlow, MaAS, etc.), the evaluation would better substantiate the stated motivation if it included tasks requiring role specialization or inter-agent coordination.

- **"Static graph-level correctness" claim is overstated.** The paper claims to "guarantee static graph-level correctness across the entire generation process" (Abstract, Section 1). What is actually statically verified is syntactic well-formedness and type consistency of the Mermaid graph; semantic correctness of the resulting Python execution is not guaranteed (the paper itself reports >90% valid Python, not 100%). The detailed sections are more precise, but the high-level framing could mislead.

- **No analysis of expressiveness trade-offs.** The paper acknowledges the search space is "intentionally bounded" (Section 3.2) but provides no analysis of what fraction of workflows discoverable by prior methods (AFlow, ADAS) can be expressed in MermaidFlow's constrained space. This makes it difficult to assess whether improved search validity comes at the cost of excluding potentially high-performing workflows.

- **Hyperparameter values for selection distribution not reported.** The parent selection formula in Section 4.2 includes parameters α (score influence) and λ (exploration-exploitation balance), but their specific values are not given.

- **Crossover operator's practical applicability unclear.** Crossover requires workflows that "share a common interface node" and is applied with only 10% probability. The paper does not report how often this precondition is satisfied, making it unclear whether crossover contributes meaningfully to search.

- **Optimization LLM ablation is one-sided.** Table 2 varies the optimization LLM for MermaidFlow only. A two-sided ablation (varying the optimization LLM for both MermaidFlow and AFlow) would be more informative about how the representation interacts with LLM capability.

### Trivial

None.

## Nice-to-Haves

- An expressiveness analysis: inspecting workflows found by AFlow or another baseline and reporting what fraction can be represented in MermaidFlow's typed graph formalism.
- Analysis of the 5–10% of cases where Mermaid-to-Python translation fails—whether these correlate with certain workflow structures.
- Clarifying that the optimal stopping point analysis (Table 3) is retrospective and not how the system would be used in practice.

## Removed Points

- *Open-source model evaluation would strengthen generality.* REMOVED: Scope creep. The paper uses the same execution LLM as all baselines; this goes beyond standard practice in this literature.
- *"Safety-constrained" is misleading about AI safety.* REMOVED: The paper consistently uses "safety-constrained" in the constrained optimization sense (structural validity), not AI safety. The usage is standard.
- *Static verification conflates syntactic with semantic correctness (as fatal).* DEMOTED TO MINOR: The paper is precise in detailed sections about what is verified. The high-level claim is somewhat overstated but not fundamentally incorrect—it does guarantee graph-level structural correctness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Provide a correlation analysis between LLM-as-Judge scores and ground-truth execution scores on a held-out set of workflows, or run an ablation with random candidate selection as a control to isolate the representation's contribution.
2. Add standard deviations or confidence intervals to Table 1.
3. Re-run MaAS on MBPP (or remove the asterisk-marked comparison) to ensure uniform evaluation on all benchmarks.
4. Reframe the contribution as addressing general workflow representation brittleness (rather than specifically multi-agent coordination), or add evaluation on genuinely multi-agent tasks.
5. Report the numerical values of α and λ used in the parent selection distribution.

## Score and Decision

| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| Semantic Backpropagation on Agentic Systems | 5.50 | 2 | Rejected; similar topic (agentic system optimization via graphs), comparable evaluation concerns but MermaidFlow has stronger representation novelty |
| CycleQD for Agent Skill Acquisition | 6.00 | 2 | Accepted; comparable contribution level, cleaner evaluation |
| Dynamic Workflow Updating (Multi-Agent) | 6.25 | 1, 2 | Accepted; similar scope (multi-agent workflows), MermaidFlow has stronger formalization but weaker evaluation reporting |
| WorkflowLLM | 6.25 | 1, 2 | Accepted; data-centric approach, different methodology |
| EvoPrompt (LLM+EA) | 6.50 | 1 | Accepted; LLM+EA combination, stronger empirical breadth (31 datasets) |
| FlowAgent (PDL workflow) | 4.50 | 1 | Rejected; similar idea (new workflow language), but weaker evaluation and unfair comparisons |

**Round 1 bracket**: 5.5–6.5. **Round 2 narrowing**: anchored at 5.5 (semantic backpropagation, rejected) and 6.0–6.25 (accepted papers with similar limitations). MermaidFlow's representation-level novelty is stronger than most papers in this band, but the unvalidated LLM-as-Judge and missing variance are meaningful gaps that prevent a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>