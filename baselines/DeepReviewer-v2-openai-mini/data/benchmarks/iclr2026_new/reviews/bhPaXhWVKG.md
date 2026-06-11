## Summary
# Final Review Report

## Summary

This paper introduces MermaidFlow, a framework that represents agentic workflows as typed, declarative graphs using the Mermaid markup language. The key idea is to separate workflow planning from execution code by using a statically verifiable graph representation, then applying evolutionary programming (EP) operators — substitution, addition, deletion, rewiring, and crossover — that preserve type and role consistency while exploring the workflow space. The approach is evaluated on four benchmarks (GSM8K, MATH, HumanEval, MBPP) against 13 baselines including non-agentic prompting methods, hand-crafted multi-agent systems, and autonomous workflow generation systems (AFlow, ADAS, MaAS).

The paper targets a real and important problem: current LLM-based agentic workflows are often encoded as imperative code where validity can only be checked at runtime, leading to fragile and hard-to-reuse systems. MermaidFlow's core technical contribution — using a typed graph language as an intermediate representation with correctness-preserving mutation operators — is well-motivated and practically relevant. The experimental results show consistent improvements, with an average score of 80.75% across benchmarks versus 79.35% for the best baseline (MaAS), and the authors demonstrate better token efficiency and higher valid-generation rates compared to AFlow.

However, the paper has several notable weaknesses: (1) the "first" and "guarantee" claims in the introduction are unsupported and contradicted by the paper's own admission of reject-sampling; (2) statistical significance is not established — Table 1 reports averages over three runs without standard deviations or significance tests, while some margins are as small as 0.14 points; (3) the LLM-as-Judge selection mechanism lacks validation against actual task performance; (4) the 50% failure rate claimed for AFlow is unsubstantiated; and (5) the conclusion's limitations are generic rather than specific to the method's observed failure modes. Additionally, the mathematical formalism contains notational errors (Eq. 3 has unbalanced parentheses) and the "inductive closure" argument is not fully proven for composed operators. Novelty and literature-positioning conclusions are deferred due to external retrieval being unavailable in this run.

## Strengths
**S1. Well-motivated problem and principled approach.** The paper correctly identifies a key limitation in current agentic workflow systems: the entanglement of planning and execution logic leads to brittle, hard-to-verify workflows. Proposing a typed declarative graph representation (Mermaid) as an intermediate layer is a clean, principled design choice that cleanly separates planning from implementation.

**S2. Novel combination of declarative representation with evolutionary search.** While declarative graphs and evolutionary search each exist in the literature, the paper's contribution of correctness-preserving EP operators (substitution, addition, deletion, rewiring, subgraph mutation, crossover) operating directly on typed Mermaid graphs is technically novel. The operators are clearly defined with type-compatibility preconditions, and Lemma 1 (transformation invariance) provides a formal basis for the claim that valid workflows remain valid under these operators.

**S3. Strong empirical results on multiple benchmarks.** The experimental evaluation is comprehensive (13 baselines, 4 benchmarks across 2 domains). MermaidFlow achieves the best average performance (80.75%) and shows consistent improvements over the strongest baselines (AFlow, MaAS). The ablation study on optimization LLM scale (Table 2) provides useful insight: stronger optimization LLMs lead to better workflows, suggesting the search space is well-structured.

**S4. Token efficiency analysis.** The comparison of token consumption (2.7e4 vs 6.9e4 at matching performance on MATH) is a practically relevant contribution. Demonstrating that the declarative representation is not only more reliable but also more token-efficient adds engineering value beyond the core scientific contribution.

**S5. Clear writing and good organization.** The paper is generally well-structured, with a logical flow from motivation (Introduction) → related work → representation formalism → search framework → experiments → case study. The figures (Figure 1 lifecycle, Figure 2 framework overview, Figure 4 case study) effectively communicate the core ideas.

## Weaknesses
**W1. Unsupported "first" and "guarantee" claims (Severity: Major).** Page 1 - Introduction (lines 70-71) states: "To our knowledge, this is the first agentic workflow framework to **guarantee static graph-level correctness across the entire generation process**." This claim is problematic for two reasons. First, the "first" claim cannot be verified without exhaustive literature comparison; even within the paper's own related work, EvoFlow (Zhang et al., 2025a) and DebFlow (Su et al., 2025) also perform constrained search over workflow spaces. Second, the paper's own mechanism (Section 4.1, last paragraph) admits that LLM-generated Mermaid code may violate constraints and requires a checker with regeneration — this is reject-sampling, not "guarantee by construction." The word "guarantee" should be replaced with "enforce through validation" and the "first" claim should be scoped or removed.

**W2. Missing statistical significance and variance reporting (Severity: Major).** Page 7 - Table 1 reports results "averaged over three runs" but provides no standard deviations, confidence intervals, or significance tests. Several margins are extremely small — MermaidFlow's MBPP score (82.31) vs MaAS (82.17) is a 0.14% difference, which could easily fall within run-to-run noise. Without variance information, the central claim of "consistent improvements" is not statistically grounded. This is a mandatory revision: report mean ± std over ≥3 seeds and add paired significance tests against the strongest baseline for each metric.

**W3. LLM-as-Judge mechanism lacks validation (Severity: Major).** Page 6 (lines 131-134) introduces an LLM-as-Judge to score candidates "based on semantic fit, structure, and task relevance," but provides no evidence that the judge's scores correlate with actual task performance. The judge model, prompt template, and calibration are not disclosed. If the judge is unreliable, the entire selection mechanism and the efficiency claims built upon it are compromised. The authors must report Spearman correlation between judge scores and validation accuracy, and compare workflow quality when selecting by judge vs by random sampling.

**W4. Unsubstantiated 50% failure rate for AFlow (Severity: Major).** Page 7 - Evolution Efficiency paragraph claims AFlow has "only a 50% success rate in generating executable code." This number is presented without citation or experimental evidence. Given that this comparison is central to the paper's efficiency narrative, the authors must either cite the AFlow paper's own statistics or report a carefully controlled replication with the exact same experimental setup.

**W5. Confusing duplication and missing evidence in ablation section (Severity: Major).** Page 7 (lines 163-168) contains a duplicated text block: the sentence "**consistently yielding >90% success rate in producing valid Python code.** This reliability enables..." appears twice (once in the evolution efficiency paragraph and once after the figure). This appears to be a copy-paste artifact. Additionally, the "Optimal Stopping Point Analysis" (lines 176-183) uses later iteration indices as evidence of stability, but this is a flawed interpretation — later discovery could simply reflect slower exploration, not more stable search. The analysis needs additional metrics (fraction of improving iterations, variance across trajectory, invalid generation rate) to support the stability claim.

**W6. Conclusion contains generic limitations (Severity: Minor).** Page 9 - Conclusion states only one vague limitation: "integration with real-world multi-agent systems and user-in-the-loop workflows introduces nuances that merit further exploration." This does not inform readers about actual failure modes observed during experiments. Specific limitations (e.g., static type system prevents dynamic agent creation, ~8% translation errors from Mermaid to Python, sensitivity to optimization LLM quality) should be stated with concrete estimates.

**W7. Notational error in Eq. (3) (Severity: Minor).** Page 4 - Section 3.2, Eq. (3): the set-builder notation has unbalanced parentheses. The expression "{(m, p(τ,α), f(τ) | m ∈ M, p ∈ P, f ∈ F)}" is missing a closing parenthesis after "f(τ)". The correct form is "{(m, p(τ,α), f(τ)) | m ∈ M, p ∈ P, f ∈ F}". While this is a minor formatting issue, it undermines the paper's mathematical precision.

**W8. Overstated claims about static verification of imperative code (Severity: Minor).** Page 1 - Introduction (line 9) states that in Python-based workflows, "validity can only be assessed at runtime." This is an overstatement: Python has mature static analysis tools (linters, type checkers, abstract interpretation) that can detect many errors before execution. The paper should clarify that while general static analysis exists, *domain-specific* workflow properties (role consistency, agent type compatibility) are not verifiable with general-purpose tools.

**W9. Inductive closure claim not fully proven (Severity: Minor).** Page 4 (line 104) claims the search space S is "inductively closed" under composition of subgraphs. Lemma 1 (page 5) proves closure for individual atomic operators, but the paper never extends this proof to compositions or to the crossover operator that combines subgraphs from different parent graphs. While the induction over sequential steps (lines 122) covers single-operator steps, the argument for crossover requires showing that the combined graph's interface node satisfies both parent type constraints simultaneously — this is asserted but not proven.

**Novelty and Literature-Positioning Note.** Due to external paper search being unavailable in this run (Retrieval-Disabled Mode), novelty and literature-positioning conclusions are deferred. The claims about being "first" (W1) require external verification that cannot be performed here. The related work section appears to cover relevant baselines adequately from a listing perspective, but whether critical comparisons are missing cannot be determined without external search.

## Score
**Final Score: 6/10**

**Rationale.** This score prioritizes research value and novelty as primary dimensions, followed by validity and reproducibility. The paper addresses a genuine and important problem (fragile agentic workflows) with a principled approach (typed declarative graph + constrained evolutionary search) that has practical potential. The experimental coverage (4 benchmarks, 13 baselines) is commendable, and the token efficiency analysis adds practical value.

However, the score is constrained by several major rigor issues: (1) unsupported "first" and "guarantee" claims that overstate the contribution and are inconsistent with the paper's own mechanism description; (2) complete absence of statistical significance testing and variance reporting, making it impossible to assess whether the reported improvements are reliable; (3) an LLM-as-Judge component that is central to the method's efficiency claims but completely unvalidated; (4) a key comparison number (50% AFlow failure rate) presented without evidence; and (5) a duplicated text artifact suggesting hasty preparation. Additionally, novelty claims cannot be independently verified due to the lack of external retrieval in this run.

These weaknesses are fixable with a careful revision. If the authors add variance reporting, validate the judge, substantiate comparison claims, and tone down unsupported "first"/"guarantee" language, a revised version could reasonably target a 7-8/10.

**Post-Revision Target: [7, 8]/10**

*Conditions for reaching 7:*
- Add standard deviations and significance tests to Table 1
- Remove "first" / "guarantee" or replace with accurately scoped language
- Validate LLM-as-Judge with correlation analysis
- Substantiate or remove the 50% AFlow claim

*Conditions for reaching 8 (in addition to the above):*
- Add missing stability metrics for search trajectory
- Provide specific, quantified limitations in the conclusion
- Fix Eq. (3) notation and strengthen the inductive closure proof for composed operators
- Add a clear description of failure cases (when does MermaidFlow fail?)