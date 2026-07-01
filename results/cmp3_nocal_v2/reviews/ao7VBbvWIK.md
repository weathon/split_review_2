## Summary

HASTE is a pipeline for compressing code context for LLM-based code editing by combining AST-aware chunking, hybrid retrieval (BM25 + semantic), call-graph expansion, and token-budget filtering. The paper claims this hybrid approach resolves the trade-off between structural coherence and semantic relevance in context selection for code LLMs.

## Strengths

- **Pipeline design is well-motivated and modular.** The architecture (§3) cleanly decomposes the problem into AST-aware chunking, hybrid indexing (lexical + semantic), RRF fusion, call-graph expansion, and budget-constrained selection. Each module targets a specific failure mode identified in prior work — broken syntax from token-level pruning, irrelevant results from structure-only methods, missing dependencies — and this decomposition is clearly presented.

## Weaknesses

### Fatal

- **No baseline comparison despite defining it as the primary research question.** §4.1.3 defines three baselines (IR-only retrieval, AST-only retrieval, naïve truncation). §4.1 states RQ1 as: "To what extent can HASTE's AST-guided context compression enable LLMs to perform correct, localized code edits **compared to baseline methods**?" Yet zero baseline results appear anywhere. Table 2, Figure 2, and Figure 3 report HASTE-only numbers on every metric. The paper's central claim — that HASTE "resolves" the trade-off between structure-aware and relevance-focused methods (abstract, §1) — cannot be evaluated without showing how the individual components that define each side of that trade-off perform. Without this comparison, the paper is a pipeline description with a demo, not a validated method. This is a structural flaw: the evidence required to support the core claim was designed (the baselines) but never collected or reported.

### Major

- **Curated dataset is far too small to support the conclusions drawn.** The entire RQ2 analysis rests on **6 files** (Table 1, 52–1317 LOC). The Pearson correlation r = −0.97 (Figure 2c) is entirely driven by a single file (test3.py, 6.8× compression, score 90); the remaining 5 points cluster at compression ratios of 1.2–2.7× with scores of 98–100 — essentially flat. The paper simultaneously reports r = −0.97 (compression ratio) and r = −0.81 (reduction percentage) for the same 6 data points, which signals instability — reduction percentage is a monotonic transform of compression ratio, so the two r-values should be consistent. The headline "up to 85% compression" is a single-file result; median compression is roughly 1.5× (33% reduction). No confidence intervals or standard deviations are reported despite stating that each task was run three times and averaged (§4.1.4).

- **AST Fidelity and Hallucination Rate are defined but never reported.** §4.2 defines two objective, non-LLM-dependent metrics — AST Fidelity (§4.2.2) and Hallucination Rate (§4.2.3) — yet neither appears anywhere in §5 Results. The paper claims HASTE "maintains high structural fidelity" and "reduces model-generated hallucinations" (Abstract), but provides zero quantitative support. The entire evaluation rests on a single LLM-as-Judge score with no calibration or human agreement study. The absence of these metrics is particularly concerning because the paper's motivation (§2.4) highlights code-specific hallucinations (invalid syntax, broken imports) as a key failure mode that HASTE addresses, making these the most directly relevant quantitative measures.

- **SWE-PolyBench evaluation is thin and lacks transparency.** The evaluation covers only 12 instances (Figure 3), of which 7 are "POLYBENCH-NOOP" tasks (non-functional changes such as adding comments). §5.3 states the analysis "excludes instances that resulted in processing errors" without specifying how many were excluded or on what criteria. No baseline comparison is provided on this benchmark either. The failure cases (scores of 0, 5, 10) are attributed to "misinterpretation" or "fundamentally incorrect suggestions" — attributions that a controlled comparison with baselines could contextualize.

### Minor

- **Single-LLM evaluation.** All experiments use Gemini 1.5 Flash (§4.1.4). The paper's claims about HASTE's value for "LLMs" broadly cannot be supported by results from one model. The LLM-as-Judge metric also uses the same model family, with no human agreement study or discussion of known judge biases.

- **Map from research questions to experiments is inconsistent.** RQ1 (§4.1) asks about comparison to baselines, but §4.1.1 maps it to SWE-PolyBench (which also lacks baselines), while §5.1 is labeled "Analysis of Performance on Curated Data (RQ1)" but reports only HASTE scores. The paper's own mapping between questions, datasets, and experiments is confused.

### Trivial

- One reference (Zhang et al., 2025) is explicitly marked as "Placeholder citation for illustrative purposes," which should be replaced with a real citation or removed.

## Nice-to-Haves

- Multi-LLM evaluation (beyond Gemini 1.5 Flash) to support generalizability claims.
- Human evaluation or calibration study for the LLM-as-Judge metric.
- Reporting of per-run variance (standard deviations) for the 3-run averaged scores.
- Specification of the embedding model and retrieval depth / token budget parameters.
- Clarification of SWE-PolyBench instance selection criteria and the number/fate of excluded instances.

## Removed Points

These points from the input review were removed per filtering rules:
- "The problem is real and well-motivated" — generic strength about problem importance, not paper-specific.
- Criticisms about undisclosed hyperparameters (embedding model, prompt templates) — the rules instruct to remove nitpicks about reproducibility details.
- "Data availability / PyPI but no open-source code during review" — the paper explicitly states this is due to double-anonymous review, standard practice.
- "References are to arXiv preprints" and the placeholder citation note — citing preprints is not a weakness, and the placeholder concern is kept as trivial above but the broader reference critique is removed.
- "The novelty claim rests on combined off-the-shelf components" — this is an observation about contribution type, not a concrete weakness.
- "Section-by-section notes" about framing, related work, architecture clarity — editorial observations, not concrete weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run and report the three defined baselines** (IR-only, AST-only, naïve truncation) on all metrics (Judge Score, AST Fidelity, Hallucination Rate). This is the single most important missing piece: without it, none of the comparative claims can be assessed.
2. **Report AST Fidelity and Hallucination Rate** — these objective metrics are defined but completely absent from the results, leaving two of the paper's three evaluation dimensions unmeasured.
3. **Scale the curated evaluation substantially beyond 6 files**, or clearly reframe it as a preliminary case study rather than a conclusive evaluation.
4. **Report the full SWE-PolyBench evaluation** with transparent exclusion criteria and baseline comparisons.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>