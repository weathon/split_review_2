Here is the final consolidated review.

---

## Summary

HASTE proposes a modular pipeline (AST-aware chunking, hybrid BM25+semantic retrieval, call-graph expansion, token-budget filtering) for compressing code context before feeding it to LLMs. The paper is motivated by a real tension — structure-aware methods preserve syntactic validity but can miss relevant code, while relevance-focused methods retrieve pertinent snippets but sever structural dependencies.

## Strengths

- **Well-motivated problem (Section 1).** The paper correctly identifies and articulates the structure-vs-relevance trade-off in code context engineering, which is a genuine and underexplored challenge. This grounding gives the work clear purpose.

- **Sensible architectural design (Section 3).** The modular pipeline is internally coherent: AST-aware chunking ensures structurally valid units, hybrid retrieval (BM25 + semantic via RRF) balances precision and recall, call-graph expansion recovers dependencies, and token-budget filtering enforces context limits. Each module targets a specific aspect of the stated problem.

- **One instructive case study (Section 5.1, test3.py).** The paper shows HASTE achieving 6.8× compression (85.3% reduction) on a 306-line file with a Judge Score of 90, and provides a qualitative explanation: graph expansion included a dependent class definition that enabled the LLM to generate a correct complex type hint. This serves as an existence proof that the approach can work.

## Weaknesses

### Fatal
None.

### Major

- **Baseline comparisons defined but entirely missing from results.** Section 4.1.3 defines three baselines (IR-only, AST-only, Naïve truncation), and RQ1 (line 124) explicitly asks about performance *"compared to baseline methods."* Yet Section 5 reports only HASTE's performance — Table 2, Figure 2, and Figure 3 contain zero baseline data. Without this comparison, the paper's central claim — that HASTE "resolves the trade-off" between structure and relevance — cannot be evaluated. The paper asserts (line 209) that "structure-agnostic pruning would likely lead to a catastrophic drop in performance at similar compression levels," but provides no experimental support for this claim.

- **AST Fidelity and Hallucination Rate defined but never reported.** Sections 4.2.2 and 4.2.3 define these two metrics, which are the ones most directly tied to the paper's core differentiators. The abstract claims HASTE "maintain[s] high structural fidelity" and "reduc[es] model-generated hallucinations," but the results section contains no data for either metric. The paper makes two specific empirical claims without supporting evidence.

- **LLM-as-Judge is neither identified nor validated.** Section 4.2.1 describes the judge only as "a general-purpose LLM" without naming which model. No validation against human raters or inter-rater reliability is reported. The judge scores cluster near the ceiling (five of six curated files score 98–100), producing a range too narrow to discriminate between methods — which is precisely why baseline comparisons and metric validation are essential. This also makes the results non-reproducible.

### Minor

- **Evaluation scale is too small for the claims made.** The curated dataset contains 6 files with 6 tasks, and the SWE-PolyBench evaluation covers 12 instances (7 of which are NOOP non-functional change tasks). Claims about "generalizability" and "robustness" are not supported by this sample size.

- **Compression-quality correlation analysis is not meaningful.** The reported Pearson's r = −0.97 is computed across only 6 data points and is driven almost entirely by a single outlier (test3.py at 6.8× compression). The paper itself notes this point "was also the one with the lowest score." Without baselines showing how other methods behave at comparable compression, this does not constitute evidence that HASTE "effectively navigates" the trade-off.

- **Unsubstantiated claim about prior work (Section 2.2).** The paper states that "Our replication of these approaches on software engineering tasks... revealed a critical flaw" in token-level pruning, but provides no experimental details, data, or results for this replication.

- **Only Python is evaluated.** The paper acknowledges Tree-sitter for multi-language support but tests only Python, limiting the generality of the claims.

### Trivial

- Call-graph expansion depth and token budget values are not specified (Section 3.3, line 110).
- The number of SWE-PolyBench instances excluded due to processing errors is not stated (Section 5.3, line 213).

## Nice-to-Haves

- Validate the LLM-as-Judge against human raters.
- Scale up the evaluation to more files, tasks, and programming languages.
- Specify the call-graph depth and token budget hyperparameters for reproducibility.

## Removed Points

None. All weaknesses listed above were verified against the paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The single highest-priority improvement is to **run the three baselines already defined** (IR-only, AST-only, Naïve truncation) and report comparative results. This is the experiment the paper's own research question (RQ1) calls for, and without it the central claim is unsubstantiated. Second, **report AST Fidelity and Hallucination Rate** — these are the metrics designed to measure the paper's claimed advantages, and their absence leaves the abstraction-level claims unsupported. Third, **identify and validate the judge LLM** for reproducibility and credibility.

## Score and Decision

The paper has a well-motivated problem and a sensible architecture, which are genuine strengths. However, the evaluation is fundamentally incomplete in ways that prevent assessing the central claims: baseline comparisons are defined but not run, two of three evaluation metrics are defined but not reported, and the sole evaluation instrument (LLM-as-Judge) is neither identified nor validated. The paper cannot be accepted in its current form because its core comparative claims lack supporting evidence. A substantially strengthened evaluation could make this a viable contribution.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>