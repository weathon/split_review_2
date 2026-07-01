## Summary

The paper introduces MermaidFlow, a framework that represents agentic workflows as declarative, typed graphs using the Mermaid markup language. This representation enables static verification of structural and semantic properties before execution. Building on this, the authors propose a safety-constrained evolutionary programming (EP) approach with correctness-preserving operators (node substitution, addition, deletion, edge rewiring, subgraph mutation, crossover) that operate directly on the Mermaid graph space. Experiments on math reasoning (GSM8K, MATH) and code generation (HumanEval, MBPP) benchmarks show consistent improvements over strong baselines including AFlow and MaAS, with better search efficiency and higher success rates in generating valid executable code.

## Strengths

- **Novel and well-motivated representation**: Using Mermaid as a structured, human-readable, and statically verifiable intermediate representation for agentic workflows is a clean idea. It cleanly separates planning from execution, enabling pre-execution validation and structured manipulation that prior code-centric approaches lack.
- **Principled evolutionary operators**: The constraint-preserving EP operators (node substitution, addition, deletion, edge rewiring, subgraph mutation, crossover) are formally defined with type-compatibility conditions, and Lemma 1 shows the search space is closed under these operators. This provides a theoretical foundation for safe exploration.
- **Strong empirical results**: MermaidFlow outperforms 13 baselines across all four benchmarks, with an average score of 80.75% vs. 79.35% for the best baseline (MaAS). The improvements are consistent and particularly notable on harder benchmarks (MATH: +2.61% over AFlow).
- **Informative ablation studies**: The paper provides useful analyses of evolution efficiency (learning curves, token cost), impact of optimization LLM scale, and optimal stopping points, which support the claim that the structured representation enables more stable and efficient search.
- **Clear case study**: Figure 4 concretely illustrates how crossover combines beneficial subgraphs from parent workflows and how the Mermaid graph translates to executable Python code, demonstrating the practical composability of the approach.

## Weaknesses

### Major

- **Overclaim on static correctness guarantee**: The paper states it is "the first agentic workflow framework to guarantee static graph-level correctness across the entire generation process." However, the guarantee relies on the LLM correctly applying the EP operators. The paper acknowledges that LLM-generated Mermaid code may violate constraints and uses a checker to regenerate. Thus, the guarantee is not absolute but rather a best-effort property of the search space under correct operator application. This overclaim should be tempered.

### Minor

- **LLM-as-judge reliability not validated**: The selection of candidate workflows uses an LLM-as-judge to score candidates without full rollout. The paper does not provide any analysis of the judge's accuracy or compare it to alternatives (e.g., random selection, direct rollout on a subset). If the judge is noisy or biased, the search could be misled. While the final evaluation uses actual execution, the search quality depends on the judge.
- **Missing systematic comparison of generation success rates**: The paper claims MermaidFlow achieves >90% success rate in producing valid Python code vs. ~50% for AFlow, but this is only mentioned in the ablation text without a dedicated table or statistical comparison. A quantitative comparison of generation validity rates across iterations would strengthen this claim.
- **Fairness of MaAS MBPP comparison**: The MBPP result for MaAS is taken from the original paper (marked with *), which may use a different LLM or evaluation setup. While MermaidFlow outperforms MaAS on other datasets where both are run under the same conditions, this single data point is less reliable.

### Trivial

- The paper uses "agentive" (Section 3.2) where "agentic" is standard; this is a minor stylistic issue.

## Nice-to-Haves

- An analysis of the computational cost (total API calls, runtime) of the full evolutionary search compared to baselines would help practitioners assess trade-offs.
- A study of how the predefined node types and roles limit expressiveness on novel or out-of-distribution tasks would clarify the generality of the approach.
- An ablation comparing the LLM-as-judge selection with direct rollout-based selection (on a small subset) would validate the judge's effectiveness.

## Novel Insights

Beyond the paper's own contributions, the key insight is that representing agentic workflows in a declarative, typed graph language (Mermaid) transforms the search problem from unstructured code mutation to structured graph evolution. This shift enables static verification, type-safe composition, and reliable translation to executable code, which together make evolutionary search more efficient and robust. The paper demonstrates that the representation itself—not just the search algorithm—is a critical factor in workflow generation quality.

## Suggestions

- Tone down the claim about "guaranteeing static correctness" to reflect that the guarantee holds under correct application of operators, with a fallback regeneration mechanism for LLM errors.
- Add a table or figure showing the success rate of generating valid Python code for MermaidFlow vs. AFlow across iterations, to substantiate the >90% vs. 50% claim.
- Validate the LLM-as-judge by comparing its rankings with actual execution scores on a held-out set, or at least discuss potential biases.

## Score and Decision

**Score**: 6

**Decision**: Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>