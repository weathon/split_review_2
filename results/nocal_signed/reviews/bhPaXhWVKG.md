## Summary

MermaidFlow proposes using Mermaid (a declarative graph markup language) as a structured intermediate representation for agentic workflows, combined with evolutionary programming (EP) operators that operate directly on this graph representation. The core idea is that representing workflows as typed, compiler-verifiable graphs (rather than unstructured Python code) enables static validation, safe mutation, and more efficient search. The paper formalizes the search space with closure properties, defines type-preserving EP operators (crossover, mutation, insertion, deletion), and demonstrates consistent improvements over 13 baselines across 4 benchmarks.

## Strengths

- **Clear problem identification (Sections 1, paragraphs 2–3).** The paper correctly identifies a genuine limitation: existing workflow representations entangle planning decisions with low-level code or unstructured prompts, making verification, reuse, and search difficult. The motivation is well-supported by references to recent failure analyses (Cemri et al., 2025; Zhang et al., 2024a, 2025c).

- **Novel representation choice (Section 3.1).** Using Mermaid graph markup language as the workflow representation is a genuinely clever design decision. Mermaid is human-readable, has a real parser/compiler, supports typed nodes and labeled edges, and can be rendered visually. The clean separation between declarative planning (Mermaid graphs) and executable code (Python) is a principled architectural choice that enables static verification using existing infrastructure.

- **Formalized search space with closure properties (Section 3.2 & Lemma 1).** The paper formally defines the search space S and proves that the EP operators preserve membership in S. The inductively closed property—that type-compatible subgraphs compose without revalidation—is a genuinely desirable property that prior code-based representations lack. The formalization is clean and mathematically well-specified.

- **Consistent empirical results (Table 1).** MermaidFlow outperforms all 13 baselines on all 4 benchmarks. The margins over the strongest prior method (MaAS) average 1.40%, and the consistency across diverse tasks (math reasoning and code generation) supports the claim that the representation itself confers an advantage. The ablation on generation success rate (>90% vs. ~50%) and token efficiency (2.7e4 vs. 6.9e4 tokens) provides concrete evidence for the practical benefits of the representation.

## Weaknesses

### Fatal
None.

### Major

- **LLM-as-judge scoring mechanism is underspecified and unevaluated (Section 4.2).** The paper replaces expensive rollout-based evaluation with an LLM-as-judge that scores candidates "based on semantic fit, structure, and task relevance" and uses these scores to select which candidate gets rolled out, thereby shaping the entire search trajectory. The paper provides: no description of the judge prompt, no calibration or accuracy evaluation against actual rollout performance, no analysis of whether the judge's rankings correlate with true task performance, and no ablation comparing LLM-as-judge selection against rollout-based selection or random selection. If the judge is unreliable, the search could converge toward workflows that look good according to the judge's unspecified criteria but do not actually improve task performance. This is a significant methodological gap because the efficiency advantage over AFlow (which uses rollout-based evaluation) could partly come from a cheaper but potentially less reliable selection mechanism, and this confound is not disentangled.

- **"Experience accumulation and reuse" claim is unsupported by evidence (Section 1, last paragraph of introduction).** The paper claims that "historical workflows generated during search accumulate as structured experience, enabling efficient reuse and adaptation across tasks" and lists this as a contribution (Section 1, contribution 2). However, the experiments only evaluate MermaidFlow on individual tasks in isolation. There is no cross-task transfer experiment, no demonstration that accumulated workflows from one task benefit another, and no analysis of the history buffer's contribution. This claim should be either substantiated with cross-task experiments or removed/reframed to match what is actually evaluated.

### Minor

- **Non-standard use of "safety-constrained" terminology.** The title, abstract, and body repeatedly use "safety-constrained" and "safety-aware" (appearing 10+ times throughout) to describe what the paper actually enforces: type safety, structural validity, and syntactic correctness (Definition 1: "workflow structure, well-typed I/O, role validity, and full connectivity"). In the AI conference community, "safety" overwhelmingly refers to alignment, harmlessness, bias mitigation, or robustness—none of which this paper addresses. While the paper defines its usage via the constraint set C_static, the terminology is confusing and sets misleading expectations given the current salience of AI safety as a technical concept.

- **No statistical significance or variance reporting (Table 1).** Results are reported as averages over three runs with no variance, confidence intervals, or significance tests. The reported improvements over the strongest baselines are modest (1.40% average over MaAS). Given that GPT-4o-mini exhibits non-deterministic API behavior even at temperature 0, variance information is needed to assess whether the observed differences are meaningful given run-to-run variability.

### Trivial
None.

## Nice-to-Haves

- Validate the LLM-as-judge by comparing its top-1 selection against actual rollout performance on a held-out set of candidates, and report agreement rates. This would substantially strengthen confidence in the search process.
- Consider an ablation that isolates the representation advantage: run AFlow's search with the same EP operators and LLM-as-judge but operating on Python code vs. Mermaid graphs, to directly measure whether the declarative representation itself drives the gains.
- Replace "safety-constrained" with more precise terminology (e.g., "structurally constrained," "type-constrained") to avoid misleading expectations about what the framework provides.

## Removed Points

- **Code formatting issue in case study (Section 5.4).** Removed as a parser artifact, not an author error.
- **AFlow 50% success rate lacking citation.** Removed; this appears to be the authors' own measurement from their runs, which is standard practice in comparative evaluations.
- **Optimal stopping point alternative interpretation (slower convergence).** Removed as speculative; the paper's interpretation is equally valid given the data.
- **Missing limitations section.** Removed as a generic concern; the paper acknowledges one limitation in the conclusion, and the remaining issues are covered in the Major/Minor weaknesses above.
- **Various section-by-section notes (e.g., "AFlow comparison underspecified").** These are subsumed into the weaknesses above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Validate the LLM-as-judge by reporting accuracy/agreement against actual rollout evaluation on a held-out candidate set.
2. Either add a cross-task transfer experiment substantiating the "experience accumulation" claim, or remove it from the contributions and reframe more modestly.
3. Add variance bars, confidence intervals, or significance tests to Table 1.
4. Run a controlled ablation keeping search algorithm and judge fixed while varying only the representation (Mermaid vs. Python code) to directly attribute the advantage.
5. Adopt more precise terminology than "safety-constrained" (e.g., "structurally constrained," "type-constrained") throughout the paper.

## Score and Decision

The core technical contribution—using Mermaid as a typed, declarative graph representation for agentic workflows with structured evolutionary search—is genuinely novel and well-executed. The formalization is clean, and the results are consistently positive across all benchmarks. However, the paper has two significant methodological gaps (unevaluated LLM-as-judge, unsupported "experience accumulation" claim) that prevent it from being a strong accept. These issues are addressable and do not invalidate the core contribution. The paper would be strengthened by validating the judge mechanism and either substantiating or removing the cross-task claim.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>