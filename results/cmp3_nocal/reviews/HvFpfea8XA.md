## Summary

This paper proposes AMADEUS, a training-free framework for RAG-based role-playing agents (RPAs), consisting of three components: ACTS (adaptive chunking with hierarchical context), GS (LLM-based chunk selection), and AE (attribute extraction). The authors also construct CharacterRAG, a manually curated dataset of persona documents for 15 fictional characters (~976K characters) with 450 QA pairs. The framework is evaluated on knowledge-grounded QA (CharacterRAG) and on out-of-knowledge personality inference using MBTI/BFI questionnaires, where AMADEUS achieves 85% MBTI dimensional accuracy vs. 65% for Naive RAG.

## Strengths

- **CharacterRAG dataset is a concrete, reusable resource.** The manual construction of persona documents (976K written characters across 15 characters) with editorial meta-information removed and documents written from the character's perspective, plus 450 QA pairs tied to six defined attributes, fills a genuine gap — no existing dataset was designed specifically for RAG-based role-playing evaluation.
- **The MBTI/BFI interview-based evaluation is a creative approach to measuring out-of-knowledge consistency.** Using standardized psychological questionnaires as probes for whether a model has internalized character traits goes beyond simple fact-retrieval evaluation. The results (85.00% MBTI accuracy vs. 65.00% for Naive RAG) show substantial improvement on this challenging task.
- **The paper identifies a real, underexplored problem.** The observation that persona documents are too long for naive LLM context windows and that standard chunking breaks the narrative continuity needed for consistent role-playing is well-motivated, and the paper demonstrates this concretely with chunk duplication frequency analysis (Figure 1).

## Weaknesses

### Fatal
None.

### Major

- **No ablation study.** AMADEUS has three distinct components (ACTS, GS, AE), but the paper never evaluates which component drives the improvements. Table 2 compares ACTS with other chunkers on a proxy metric (similarity scores), not on downstream role-playing. Without ablations (e.g., ACTS alone + Naive RAG, ACTS+GS without AE, etc.), readers cannot attribute the gains to the proposed architecture. This is a standard experimental requirement for a multi-component method paper.

- **No statistical significance or variance reporting.** All main results (Table 4, Table 1, Figure 5) are reported from single runs with no standard deviations, confidence intervals, or significance tests. This is especially critical because the CharacterRAG QA improvements (Table 4) are very small — AMADEUS vs. Naive RAG: 92.67% vs. 91.33% with GPT-4.1 (+1.34%), 88.00% vs. 86.44% with Gemma3 (+1.56%), 78.89% vs. 78.44% with Qwen3 (+0.45%). Differences this small cannot be assumed reliable without variance estimates.

- **No long-context baseline.** The paper's central motivation is that persona documents are too long to feed directly into an LLM. Yet the experiments never test the simplest alternative: feeding the full persona document as context to a long-context model (GPT-4.1-128K, Gemini 1M, etc.). This baseline would directly test whether RAG is needed at all for this setting.

- **Overclaim: "best performance across all three LLMs."** The paper states (line 347) that "our framework achieves the best performance across all three LLMs" in a paragraph discussing both Table 4 and Figure 5. However, for Qwen3-32B on the MBTI/BFI HS metric, CRAG outperforms AMADEUS (MBTI HS: CRAG 1.80 vs. AMADEUS 2.04; BFI HS: CRAG 1.96 vs. AMADEUS 2.03). The claim is technically true for Table 4 but ambiguous in context, and Figure 5 shows AMADEUS is not uniformly best.

### Minor

- **LLM-as-evaluator transparency.** The evaluation metrics (ACC, ACC_L, HS) are computed by an unspecified LLM ("LLM-based metrics, similar to prior studies"). The paper does not state which model is used as the evaluator. Since GS and AE use GPT-4.1 (Section 5.1), and the evaluator could plausibly be the same model family, there is a risk of systematic bias toward the method's outputs. The paper should explicitly report which LLM judges the metrics and, ideally, include independent human evaluation of final responses rather than only of intermediate GS/AE outputs (Table 3).

- **MBTI/BFI ground truth is crowd-sourced and unvalidated.** The ground-truth personality types come from personality-database.com, where "thousands of actual participants' votes" determine each character's type. These labels are inherently subjective (e.g., Mikoto Misaka: GT=ENTJ, AMADEUS=INFJ, |d|=2). The paper follows prior work (Wang et al., 2024b) in using this source, but it does not report inter-annotator agreement or any reliability measure for the ground-truth labels themselves. Given only 15 characters, the reported 85% accuracy could shift with different characters or voting populations.

- **GS's LLM-in-the-loop conflates chunk selection with additional reasoning.** GS iterates through up to N=30 chunks, calling an LLM for each to determine whether it "contains information from which the character's attributes can be inferred regarding [the query]." This gives the LLM an extra pass over the chunks before final response generation. The paper does not disentangle whether GS helps via better chunk selection or simply by providing an additional reasoning opportunity. A simpler baseline — taking top-K chunks and prompting the LLM to reason over them — would clarify this.

- **Human evaluation validates intermediate outputs, not final responses.** Table 3 shows that human raters find GS/AE outputs reasonable (~4/5 Likert). This does not validate that the *final generated responses* are better than baselines. The connection between "GS/AE outputs are reasonable" and "AMADEUS produces better role-playing" is an unvalidated step in the chain of evidence.

- **No cost/latency analysis of GS's iterative LLM calls.** GS calls an LLM for each chunk (up to N=30 iterations), adding substantial overhead compared to a single-pass retriever. The paper does not report this cost or justify whether the improvement justifies the expense.

- **Dataset language mismatch.** The persona documents are in Korean (footnote 2), but evaluation is conducted with English LLMs and English MBTI/BFI questions. The paper does not clarify whether documents were translated or used in their original Korean for the RAG pipeline, which affects reproducibility and the interpretation of retrieval quality.

### Trivial
- The claim that setting overlap to half the max paragraph length "minimizes information loss" (Section 4.1) is asserted without evidence. The empirical validation in Figure 4 shows this choice maximizes similarity score sum, but the theoretical claim is overstated.
- Several characters in Table 1 show large per-character discrepancies (e.g., Mikoto Misaka: GT=ENTJ, AMADEUS=INFJ, |d|=2; Edward Elric: GT=ENTP, AMADEUS=INFP, |d|=2). A per-character confusion matrix or breakdown would be more informative than the aggregate 85% figure.

## Nice-to-Haves
- An ablation study isolating ACTS, GS, and AE on the main evaluation tasks.
- Variance estimates from multiple runs (at least 3–5) for the main results.
- A long-context baseline feeding the full persona document into a 128K-context model.
- Human evaluation comparing final AMADEUS responses vs. baseline responses on out-of-knowledge questions.
- Reporting of the computational overhead (latency, cost) of GS's iterative LLM calls.

## Removed Points
These points are flagged to be removed; treat them with caution.
- "Missing role-playing-specific baselines (character fine-tuning)": The paper scopes itself to *RAG-based* RPAs; fine-tuning is a different paradigm and not a required comparison. (Scope creep — Soft Rule.)
- "Table 5 referenced but missing from main text": The parser strips appendices; Table 5 exists in the original submission. (Hard Rule: parser artifact.)
- "No discussion of limitations": Not a structured gap in the evidence — many papers present contributions without a separate Limitations section.
- "Paper claims 'little research on RAG-based RPAs'; reviewer acknowledges this is probably true": Not a weakness.
- "ACTS is simple": The simplicity of a method is not itself a weakness if it works; this is a characterization, not a flaw.
- "The dataset is sourced from Namuwiki (Korean wiki) introducing cultural skew": Acknowledged by the paper in footnote 2; this is a scope boundary rather than a flaw.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add an ablation study removing one component at a time (ACTS only, ACTS+GS, ACTS+AE) on both CharacterRAG QA and MBTI/BFI tasks. This is the single highest-impact addition.
2. Repeat main experiments 3–5 times with different random seeds and report mean ± std. Given the small margins in Table 4, this is essential to establish reliability.
3. Add a long-context baseline: feed the full persona document as a single context window to a model with ≥128K capacity.
4. Explicitly state which LLM is used for metric evaluation and, ideally, add a human evaluation of final responses (not just intermediate GS/AE outputs).
5. Clarify whether Korean persona documents were translated for use with English LLMs and, if so, how.
6. Report the average number of GS iterations and the associated latency/cost.
7. Rephrase the "best across all three LLMs" claim to specify it refers to Table 4 (CharacterRAG QA) and acknowledge the Qwen3 HS results in Figure 5.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>