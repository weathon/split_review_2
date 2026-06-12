## Summary

HASTE is a framework for code context compression that combines Abstract Syntax Tree (AST)-aware chunking, hybrid lexical/semantic retrieval, call graph expansion, and token-budget filtering to produce compact but structurally coherent code snippets for LLM prompts. The paper evaluates HASTE on six curated Python files and twelve SWE-PolyBench tasks, reporting high judge scores and compression ratios up to 85%.

## Strengths

*   **Well-motivated problem.** The tension between syntactic coherence and semantic relevance in code retrieval is a genuine obstacle for LLM-based software engineering, and the paper articulates this trade-off clearly.
*   **Clean, modular architecture.** The pipeline is decomposed into logical stages (ingestion, embedding, retrieval, observability), making the design easy to understand and potentially reproducible.

## Weaknesses

### Fatal

*   **No experimental comparison against any baseline.** The paper introduces three baselines (IR-only retrieval, AST-only retrieval, naïve truncation) but reports zero results for them. The central claim that HASTE resolves the structure-relevance trade-off cannot be evaluated without showing that HASTE outperforms these methods. The evaluation is essentially a self-case-study.

### Major

*   **Evaluation is far too small and lacks rigor.**  
    * The curated dataset contains only 6 files; the SWE-PolyBench analysis covers just 12 instances, many of which are trivial “no-op” tasks.  
    * No confidence intervals, error bars, or statistical tests are presented despite the LLM-as-judge setup having high stochasticity (only 3 runs averaged).  
    * Metrics promised in Section 4.2 (AST Fidelity, Hallucination Rate) are never reported in the results.  
    * The correlation analysis (Figure 2c–d, r = –0.97 and –0.81) is performed on 6 data points; such small-sample correlations are not meaningful and should not be used to support claims about a compression-quality frontier.  
    * The LLM-as-judge scoring criteria (correctness, readability, instruction alignment) are described but no aggregation formula or validation of the judge’s reliability is provided.

*   **Limited novelty.** The components are largely off-the-shelf: AST chunking, BM25, embedding-based retrieval, Reciprocal Rank Fusion. The contribution is a system integration without a new algorithm or theoretical insight. An ICLR paper needs a stronger algorithmic or empirical contribution.

### Minor

*   The paper claims HASTE “reduces model-generated hallucinations” but provides no hallucination measurements, only an indirect argument about coherent context.
*   The SWE-PolyBench failure cases are attributed to poor suggestions, which is reasonable but does not demonstrate that HASTE’s context was superior to what an alternative method would provide.
*   Some abstractions (e.g., “Identifier Extraction”, “Payload Builder”) are described in detail but their actual impact on performance is not tested via ablation.

### Trivial

*   Figure 3’s x-axis labels are truncated and hard to read.

## Nice-to-Haves

*   Ablation studies isolating each pipeline component (e.g., disabling call graph expansion, using only BM25, using only AST) would greatly strengthen the paper.
*   A larger-scale evaluation on standard code completion or bug-fixing benchmarks (e.g., HumanEval, SWE-bench) with multiple LLMs would improve generalizability.
*   A validation study of the LLM-as-judge (e.g., correlation with human ratings or pass@k) would increase confidence in the reported scores.

## Novel Insights

None beyond the paper’s own contributions. The observation that high compression is negatively correlated with quality is intuitive and not deeply analyzed; no new understanding of code retrieval or LLM behavior emerges.

## Suggestions

*   **Run baselines and report their results.** Without this, the paper cannot support its core thesis.
*   **Report all three promised metrics** (Judge Score, AST Fidelity, Hallucination Rate) across all conditions.
*   **Increase the evaluation scale** (at least hundreds of edits) and include standard code generation benchmarks.
*   **Include error bars and significance tests** for all reported numbers.
*   **Consider submitting to a software engineering conference** (e.g., ICSE, ASE, FSE) where system-tool papers with smaller-scale evaluation are more common, rather than a venue like ICLR that expects stronger empirical or theoretical novelty.

## Score and Decision

**Score**: 3  
**Decision**: Reject

The paper addresses an important problem and presents a sensible design, but the evaluation is critically incomplete—lacking any baseline comparison, being too small, and omitting promised metrics. Without addressing these issues, the claims are unsubstantiated and the paper does not meet ICLR’s standards for contribution and rigor.

MY FINAL SCORE: <score>3</score>  
MY FINAL DECISION: <decision>Reject</decision>