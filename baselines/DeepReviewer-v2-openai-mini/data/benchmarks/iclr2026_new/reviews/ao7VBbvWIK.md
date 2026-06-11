## Summary
# Final Review Report

## Summary

This paper presents HASTE (Hybrid AST-guided Selection with Token-bounded Extraction), a framework for context selection in LLM-based code editing. HASTE combines Abstract Syntax Tree (AST)-aware chunking, hybrid lexical + semantic retrieval, call-graph expansion, and token-budget filtering to produce structurally coherent, compact code contexts for LLM prompts. The paper defines three evaluation metrics (LLM-as-Judge scores, AST Fidelity, Hallucination Rate) and reports Judge Scores on a curated benchmark of 6 Python files (average 97.3/100) and 12 SWE-PolyBench instances.

**Core strengths:** The problem is well-motivated — context selection for LLM code editing is practically important. The pipeline architecture is clearly explained and combines several reasonable design choices. The qualitative analysis in Section 5.3 (e.g., the test3.py example where call-graph expansion enabled correct type hint generation) provides useful insight into when AST-aware context helps.

**Core weaknesses (critical):** The evaluation has fundamental gaps: (1) three baselines are defined but none are compared against — the entire results section reports only HASTE's absolute scores, invalidating RQ1; (2) two of three promised metrics (AST Fidelity, Hallucination Rate) are never reported, so claims about structural fidelity and hallucination reduction are unsubstantiated; (3) the LLM-as-Judge metric lacks model specification, human validation, and inter-rater reliability analysis; (4) the Pearson r=-0.97 correlation is based on 6 data points with one outlier; (5) the curated dataset is very small (6 files, half from Pydantic). Novelty and comparison conclusions are deferred due to external literature verification being unavailable in this run.

## Strengths
1. **Well-motivated problem.** The core challenge — selecting a minimal, structurally coherent code context for LLMs under tight token budgets — is practically important and timely. The paper clearly articulates the tension between structure-aware and relevance-focused retrieval.

2. **Clean modular architecture.** The HASTE pipeline (Scanner → Chunker → Identifier Extraction → Payload Builder → Embedding & Indexing → Retrieval Pipeline → Export) is logically organized and the data flow is easy to follow. The separation of concerns makes the system understandable and extensible.

3. **Hybrid design that addresses a real gap.** Combining AST-bounded pruning with hybrid lexical/semantic retrieval is a reasonable approach to ensuring both relevance and structural coherence. The use of Reciprocal Rank Fusion for integrating BM25 and dense retrieval signals is standard but appropriate.

4. **Informative qualitative analysis.** The discussion of specific cases — the test3.py example (6.8× compression with correct complex type hint thanks to call-graph expansion) and the SWE-PolyBench failure analysis (scores of 10, 5, 0 due to ambiguous suggestions) — provides genuine insight into when HASTE works and where its limitations lie.

5. **Commitment to open science.** The authors state that HASTE is available as an open-source Python package (HasteContext on PyPI) and commit to releasing experimental data and scripts upon acceptance, which supports reproducibility.

6. **Clear writing structure.** The paper is well-organized, with a clear separation of related work into four thematic threads, detailed architecture descriptions, and explicit research questions guiding the evaluation.

## Weaknesses
### W1 [CRITICAL] — No baseline comparison results
- **Page 5 - Baseline Conditions / Page 6-7 - Results.** Three baselines are defined (IR-only, AST-only, Naïve truncation) but their results are never reported anywhere. RQ1 explicitly asks "compared to baseline methods," yet the entire Results section presents only HASTE's absolute scores. The abstract, introduction, and conclusion claim superiority over alternatives without a single comparative data point.
- **Impact:** The paper's central empirical contribution is incomplete. No comparative evidence supports the claimed advantage.
- **Fix (Must):** Run all baselines and report results side-by-side, or reposition as a non-comparative system description with scoped claims.

### W2 [CRITICAL] — Two of three evaluation metrics never reported
- **Page 6 - Section 4.2.** AST Fidelity and Hallucination Rate are defined in Section 4.2 but never presented in Section 5 (Results). The abstract states HASTE "reducing model-generated hallucinations" and "maintaining high structural fidelity" — neither claim has any supporting data.
- **Impact:** The paper's headline claims are unsubstantiated. A reader cannot verify the core advertised benefits.
- **Fix (Must):** Report both metrics with full results, or remove all corresponding claims from abstract, introduction, and conclusion. If the metrics were measured, include them; if not, remove the metric definitions.

### W3 [MAJOR] — LLM-as-Judge evaluation lacks essential validation
- **Page 6 - Section 4.2.1.** The primary evaluation uses an LLM-as-Judge framework, but: (a) the judge model is not specified (name, version); (b) no human validation or calibration is reported; (c) no inter-rater reliability assessment; (d) potential bias if the judge and editor LLMs belong to the same family.
- **Impact:** The evaluation's central metric (Judge Score) is unvalidated. Entire results section rests on this unverified metric.
- **Fix (Must):** Specify the judge model, report human correlation on a sampled subset, and discuss potential bias.

### W4 [MAJOR] — Correlation analysis based on 6 data points with one outlier
- **Page 7 - Section 5.2.** Pearson r = -0.97 is reported for compression ratio vs. Judge Score based on only 6 data points. Visual inspection shows the correlation is driven almost entirely by a single point (test3.py). No confidence interval, p-value, or robust correlation (e.g., Spearman ρ) is reported.
- **Impact:** The conclusion that HASTE "navigates the compression-quality frontier" is overstated relative to the statistical evidence.
- **Fix (Must):** Report confidence intervals, use robust correlation, and explicitly acknowledge the outlier-driven nature of the result.

### W5 [MAJOR] — Very small evaluation scale
- **Page 5 - Datasets / Page 7 - SWE-PolyBench.** The curated dataset has only 6 Python files (three from Pydantic). The SWE-PolyBench evaluation uses only 12 instances with unexplained exclusions. Neither sample size supports the paper's claims about "robustness and generalizability."
- **Impact:** Claims about general performance cannot be reliably assessed from this data.
- **Fix (Must):** Expand evaluation or explicitly bound claims to the specific tested files and note that larger-scale validation is needed.

### W6 [MAJOR] — Missing reproducibility details in method section
- **Page 3-4 - Method.** The embedding model is described only as "state-of-the-art transformer-based encoders" with no name, dimension, or training details. The Index Builder mentions FAISS/Annoy/HNSW but does not specify which was used. The Suggestion Generator used for task creation is a black box.
- **Impact:** The method cannot be reproduced or fairly compared against.
- **Fix (Must):** Specify exact model names, index configuration, and provide the suggestion generator prompt template.

### W7 [MAJOR] — Overclaimed contribution statements
- **Page 1 - Abstract and Introduction.** Claims of "novel pipeline" are not substantiated by explicit differentiation from prior component-level work. The "85% compression" headline is a single outlier (test3.py); median compression is 1.5×. "Dramatically improving" success rates has no comparative evidence.
- **Impact:** Reviewers may perceive hype, reducing credibility.
- **Fix (Must):** Qualify contribution claims: report median alongside maximum, compare against prior work components, and replace subjective intensifiers with metric-grounded statements.

### W8 [MAJOR] — Unverifiable replication claim in Related Work
- **Page 2 - Section 2.2.** The paper states "Our replication of these approaches... revealed a critical flaw" without providing replication details, quantitative results, or methodology.
- **Impact:** A central motivation for HASTE's design is based on an unverifiable claim.
- **Fix (Must):** Provide replication summary or soften to hypothesis.

### W9 [MAJOR] — False dichotomy in Introduction framing
- **Page 1 - Introduction paragraph 2.** The paper frames structure-aware and relevance-focused approaches as "two distinct schools of thought" that have not been combined, ignoring existing hybrid approaches. This oversimplifies the landscape.
- **Impact:** Weakens the perceived novelty and may mislead readers about the state of prior art.
- **Fix (Must):** Acknowledge existing hybrid methods and articulate the specific gap more precisely.

### W10 [MAJOR] — RRF parameter selection not justified
- **Page 4 - Retrieval Pipeline.** The RRF formula uses k=60, which is at the high end of typical values. No sensitivity analysis, ablation, or justification is provided. At k=60, the fusion scores become nearly uniform, potentially defeating the purpose of rank fusion.
- **Impact:** The core ranking mechanism may be operating suboptimally, and readers cannot assess this.
- **Fix (Must):** Provide k sensitivity analysis or ablation against alternative fusion strategies.

## Score
**Final Score: 4/10**

**Rationale:** The paper addresses a well-motivated problem with a clean architectural design. However, the evaluation has fundamental gaps that prevent validation of the core claims: (1) defined baselines are never compared against, invalidating the comparative research question; (2) two of three evaluation metrics (AST Fidelity, Hallucination Rate) are never reported, leaving headline claims about structural fidelity and hallucination reduction unsupported; (3) the primary metric (LLM-as-Judge) lacks specification, validation, and reliability assessment; (4) the correlation analysis is statistically misleading (6 points, one outlier); (5) the evaluation scale (6 files + 12 instances) is too small to support generalizability claims; and (6) critical reproducibility details (embedding model, index configuration, task generation) are missing.

The paper has genuine potential — the idea is sound, the architecture is well-structured, and the qualitative analysis provides useful insights. However, in its current form, the empirical contribution does not meet the standard for a methods paper claiming superiority over alternatives. A major revision addressing the evaluation gaps (especially adding baseline comparisons and reporting the missing metrics) is essential.

**Novelty verdict:** Deferred — external literature verification was unavailable in this run. Based on the paper's own description, the combination of hybrid retrieval + AST-bounded pruning + budget-aware filtering appears to have elements of novelty, but this cannot be confirmed without literature comparison.

*Notes: Scoring follows the required policy prioritizing research value + novelty. The score reflects that the core research value cannot be assessed due to missing comparative evaluation and unsubstantiated central claims. The architectural contribution is visible and potentially valuable, meriting a non-zero score even in the current incomplete state.*