## Summary

MermaidFlow introduces a declarative graph representation for agentic workflows using the Mermaid markup language, enabling static verification of workflow structure and type safety. It couples this representation with a safety-constrained evolutionary programming (EP) framework—featuring type-preserving crossover, mutation, insertion, and deletion operators—that explores the valid workflow space while guaranteeing structural correctness by construction. Evaluated on GSM8K, MATH, HumanEval, and MBPP with gpt-4o-mini, MermaidFlow consistently outperforms 13 baselines, achieving an average score of 80.75% (1.40% above the next-best MaAS at 79.35%).

## Strengths

- **Well-motivated problem and clear formulation.** The paper convincingly argues that brittle, code-bound workflow representations are a primary failure source in multi-agent systems, and the three-layer lifecycle (planning, code realization, runtime) provides a useful conceptual framework. The formalization of workflows as typed declarative graphs (Eq. 1–3) is clean and well-structured.

- **Consistent empirical improvements across all four benchmarks.** MermaidFlow outperforms all 13 baselines on every benchmark, with notable gains on MATH (+2.61% over AFlow) and HumanEval (+1.30% over MaAS). The ablation showing 2.5× better token efficiency than AFlow at comparable performance is a practical strength.

- **Meaningful ablation studies.** The paper provides several useful ablations: (1) learning curves showing faster and more stable convergence (Figure 3), (2) the impact of optimization LLM scale (Table 2), and (3) optimal stopping point analysis (Table 3) demonstrating that MermaidFlow's search remains productive at later iterations, suggesting more stable exploration.

- **Good case study and visualization.** Figure 4's illustration of crossover-based evolution from Mermaid graphs to executable Python code makes the framework tangible and demonstrates the practical workflow lifecycle clearly.

## Weaknesses

### Fatal
None.

### Major

- **"Static verification" claim is overstated.** The paper repeatedly emphasizes "static graph-level correctness" and "safety," but what is actually verified is syntactic validity and type compatibility of the Mermaid representation—not semantic correctness of the workflow. A workflow that parses and type-checks in Mermaid can still produce incorrect outputs or have coordination failures. The paper should more carefully distinguish between structural validity and behavioral correctness. Lemma 1's "Transformation Invariance" guarantees closure in the syntactically valid space, but this is a weaker guarantee than the "safety" framing implies.

- **Modest improvements and unclear statistical significance.** The average improvement over the best baseline is 1.40%, with the MBPP gain being only +0.14% over MaAS. Results are averaged over only 3 runs with no standard deviations reported. At these margins, the differences may not be statistically significant, especially given the inherent variance in LLM-based evaluations. The paper would benefit from significance tests or confidence intervals.

- **Limited evaluation scope.** Only 4 benchmarks are used, all in math reasoning and code generation with relatively simple task structures. No evaluation on more complex multi-step tasks (e.g., web browsing, tool use, or open-ended planning) is provided, limiting the generalizability claims.

### Minor

- **Crossover instability is poorly explained.** The paper applies crossover at only 10% probability "to ensure experimental stability" but never explains what instability occurs at higher rates or quantifies the failure mode. This raises questions about how robust the type-safety guarantees actually are in practice.

- **LLM-as-Judge as evaluation proxy.** The paper uses LLM-as-Judge for candidate selection during optimization rather than executing workflows. The correlation between judge scores and actual task performance is not analyzed, and potential biases in this proxy evaluation are not discussed.

- **Mermaid choice not strongly justified.** The paper does not compare Mermaid against other structured graph languages (e.g., DOT/Graphviz, PlantUML, custom DSLs). Without this comparison, it's unclear whether the benefits stem from Mermaid specifically or from any structured graph representation.

### Trivial

- Some figures have overlapping caption text and figure content descriptions (likely OCR artifacts).

## Nice-to-Haves

- Report standard deviations and run significance tests on the benchmark results.
- Evaluate on at least one more complex agentic benchmark (e.g., GAIA, WebArena) to test generalization.
- Analyze the correlation between LLM-as-Judge scores and actual execution outcomes.
- Provide a comparison of different graph representations to justify the Mermaid choice.
- Quantify the Mermaid code generation failure rate and the cost of regeneration.

## Novel Insights

The paper's genuinely novel observation is that LLMs are significantly better at generating and manipulating structured markup languages (Mermaid) than raw Python code, achieving >90% valid code generation versus ~50% for code-based approaches. This empirical finding—that the choice of intermediate representation dramatically affects the reliability of LLM-based workflow optimization—is practically valuable and suggests a broader design principle: structured, constrained representations can amplify the capabilities of even modest LLMs in optimization settings.

## Suggestions

- Add a "static verification vs. semantic correctness" section that honestly characterizes what guarantees Mermaid provides and what remains to be validated at runtime.
- Report mean ± std over 3 runs and consider paired statistical tests against the strongest baseline.
- Analyze the correlation between LLM-as-Judge scores and actual benchmark performance to validate the proxy evaluation.
- Include failure mode analysis: how often do generated Mermaid graphs fail validation, and what patterns characterize these failures?
- Consider testing with a stronger execution LLM (GPT-4o) to separate the contribution of the framework from the ceiling imposed by gpt-4o-mini.

## Score and Decision

The paper presents a clear, well-motivated idea with solid execution and consistent (if modest) improvements. The declarative graph representation is a genuine contribution that enables better LLM-based workflow generation. However, the improvements are marginal, the safety claims are overstated relative to what is actually verified, and the evaluation scope is limited. The contribution is incremental but valuable—bringing the community closer to principled workflow optimization.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept