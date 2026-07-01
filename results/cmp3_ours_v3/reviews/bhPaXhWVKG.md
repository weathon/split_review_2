## Summary

MermaidFlow proposes a declarative, typed graph representation using the Mermaid markup language for agentic workflows, combined with safety-constrained evolutionary programming (EP) operators that preserve type correctness. The system is evaluated on four benchmarks (GSM8K, MATH, HumanEval, MBPP) against 13 baselines and reports consistent improvements.

## Strengths

- **Well-motivated representation choice (Sections 1, 3).** The paper correctly identifies that existing agentic workflow systems entangle planning and execution in code-centric formats that resist static verification, and responds with a principled declarative intermediate representation. The contrast with collapsed Python-code or JSON-tree representations is well-drawn and supported by cited evidence (Cemri et al., 2025).

- **Clean formalization of the search space (Section 3.2, Equations 1–3).** The formal definition of workflows as typed declarative graphs with explicit type-consistency preconditions for each EP operator (Section 4.1) is a genuine step forward. Lemma 1 (transformation invariance) provides a formal guarantee that prior work in this area has not offered.

- **Consistent empirical wins across all four benchmarks (Table 1).** MermaidFlow achieves the best score on GSM8K, MATH, HumanEval, and MBPP against 13 baselines. The average improvement over the strongest baseline (MaAS) is 1.40 points, with the largest margin on the harder benchmark (MATH: +2.61 over AFlow).

## Weaknesses

### Fatal
None.

### Major

1. **LLM-as-Judge used as selection bottleneck without validation against actual task performance (Section 4.2).** The paper states: "To avoid expensive rollout-based evaluation over the full population, we adopt an *LLM-as-judge* model that scores each candidate based on semantic fit, structure, and task relevance" (line 152). The highest-scoring candidate is selected for execution while all others are discarded (line 156). The paper provides no evidence — no correlation study, ablation, or qualitative analysis — that the judge's scores are predictive of actual solve rates. If the judge's scoring is noisy or misaligned, the search could systematically discard high-performing candidates or promote low-performing ones, making the reported improvements uninterpretable. This is not a missing peripheral experiment: the judge shapes the entire search trajectory, and without validation the reader cannot trust that the reported results reflect genuine pipeline quality rather than artifacts of the judge's preferences.

2. **No standard deviations or confidence intervals reported (Table 1).** The caption states "results averaged over three runs" but no variance is shown. Several margins are small (e.g., +0.14 on MBPP, +0.92 on GSM8K) and could fall within run-to-run noise. Additionally, the MBPP value for the strongest baseline (MaAS) is marked with an asterisk: "Result reported in the MaAS paper, as the corresponding implementation for this dataset is not available in their code" — meaning this comparison is against a number from a different evaluation protocol, further weakening the evidence.

3. **The experimental comparison conflates representation choice with search algorithm (Section 5).** MermaidFlow uses EP over Mermaid graphs, while the primary baseline AFlow uses MCTS over Python code. The two differ in both representation *and* search algorithm. The paper attributes improvements to the declarative representation but the experiments cannot distinguish the effect of the representation from the effect of the search strategy. A controlled comparison (e.g., MCTS over Mermaid workflows, or EP applied to Python-code workflows with type-checking heuristics) would be needed to support the causal claim that the representation is the source of improvement.

### Minor

4. **The "static graph-level correctness" guarantee is narrower than suggested (Sections 3–4).** The paper claims to "guarantee static graph-level correctness across the entire generation process" (line 30) and that "all candidates in MermaidFlow are valid by construction" (line 102). The guarantee applies to Mermaid syntax and type-checking at the graph level. However, the translation from Mermaid to executable Python code is performed by gpt-4o-mini (line 279) and is not proven correct-by-construction. The paper acknowledges a >90% success rate in Python generation (line 201), confirming that ~10% of valid Mermaid graphs produce non-functional Python code. The claims should be qualified to reflect this gap.

5. **Initial population generation is not described (Section 4).** The induction argument (line 134) requires an initial graph G₀ ∈ S, but the paper does not specify how this initial workflow is created (LLM-generated from a task description? hand-crafted? parsed from existing workflows?). This is needed for reproducibility.

6. **Temperature 0 for all LLM calls (line 168).** While parent-sampling randomness provides some diversity, deterministic LLM outputs from identical inputs could restrict the diversity of generated candidates. The paper does not discuss this design choice.

7. **No sensitivity analysis for hyperparameters λ and α (line 142).** These control exploration-exploitation balance in the parent sampling distribution, but no ablation or sensitivity study is provided.

### Trivial
None.

## Nice-to-Haves

- A correlation study between the LLM judge's scores and actual execution performance would substantially strengthen confidence in the evaluation pipeline.
- An ablation that controls for search algorithm (e.g., MCTS on Mermaid workflows) would help isolate the effect of the representation.
- Standard deviations or confidence intervals for all reported results.
- Specification of the initial population generation procedure.

## Removed Points

- The critic's claim that "Excluding MBPP, the average margin is smaller" is **factually wrong**. Without MBPP the margin is ~1.61 (from three datasets) vs. 1.40 (with MBPP). The MBPP value actually *reduces* the average margin. Removed as factually incorrect.
- Criticisms about code quality in the case study (nested `await`, unbalanced parentheses) are parser artifacts from PDF text extraction, not paper issues. Removed per the formatting-artifact rule.
- Criticisms about implementation details deferred to the appendix (crossover interface matching, type system specifics, algorithmic pseudocode) are removed per policy — the appendix is stripped by the parser and exists in the original submission.
- The critic's speculation that the LLM judge confounds the stopping point analysis (Issue 6) without evidence of judge-score drift over time is removed as speculative; it is subsumed by the validated-judge concern (Weakness #1).
- Concerns about the type system not being concrete enough in Section 3.2 are removed since the paper explicitly defers to Appendix A.1, which was stripped by the parser.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Validate the LLM-as-Judge against actual execution scores via a correlation study (e.g., for one dataset, run full evaluation on all candidates across several rounds and compute rank correlation).
2. Report standard deviations or confidence intervals for all main results.
3. Include at least one controlled experimental condition that isolates the representation from the search algorithm.
4. Specify the initial population generation procedure.
5. Qualify the "static correctness" claim to acknowledge the Mermaid-to-Python translation step.

---

**Calibration anchors used:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `...deepreview_13k_calibration/Uj0h13lVrR.md` | 1.00 | R1 | Unrelated paper (GFlowNets) — far lower quality |
| `...deepreview_13k_calibration/5kMwiMnUip.md` | 1.40 | R1 | Unrelated paper (LLM jailbreaking) — far lower quality |
| `...deepreview_13k_calibration/EHYbqCDRtM.md` | 2.00 | R1 | Graph+LLM paper — less rigorous evaluation |
| `...deepreview_13k_calibration/P8IBvXLAVk.md` | 4.00 | R1 | Self-Evolving Agents — similar topic, weaker formalization and evaluation |
| `...deepreview_13k_calibration/PfYg3eRrNi.md` | 4.80 | R1 | Agent Workflow Memory — similar topic, weaker empirical support |
| `...deepreview_13k_calibration/r1cbFEH0Df.md` | 5.50 | R2 | Semantic Backpropagation — comparable rigor, similar evaluation gap concerns |
| `...deepreview_13k_calibration/b8eEutZlPb.md` | 5.75 | R2 | AgentGym — broader scope but similar methodological concerns |
| `...deepreview_13k_calibration/Kvdh12wGC0.md` | 6.00 | R2 | CycleQD — stronger ablation study, more thorough evaluation |
| `...deepreview_13k_calibration/sLKDbuyq99.md` | 6.25 | R1/R2 | Dynamic Workflow Updating — accepted; similar topic but with less rigorous benchmarking |
| `...deepreview_13k_calibration/3Hy00Wvabi.md` | 6.25 | R2 | WorkflowLLM — accepted; data-construction focused, different evaluation paradigm |

**Round 1 bracket:** 4.0–6.0. MermaidFlow is stronger than the 4.00–4.80 papers (Self-Evolving Agents, Agent Workflow Memory) due to cleaner formalization and more comprehensive benchmarking, but weaker than the 6.00–6.25 papers (CycleQD, Dynamic Workflow Updating) due to the unvalidated LLM judge, missing variance estimates, and confounded attribution claims.

**Round 2 narrow:** The 5.50–6.00 band confirms MermaidFlow sits near the lower end. Comparison with the 5.50 Semantic Backpropagation paper (rejected for theoretical rigor concerns) and the 6.00 CycleQD paper (accepted with thorough ablations) supports a score of 5.0.

**Final score anchored:** 5.0 — the paper has a genuinely interesting core idea and clean formalization, but the evaluation gaps (unvalidated judge, no variance estimates, confounded attribution) are significant enough that the evidence does not yet support the causal claims the paper makes.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>