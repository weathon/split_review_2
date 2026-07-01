Now I have all the information I need. Let me compile the final review.

```
## Summary
The paper proposes AMADEUS, a training-free RAG framework for role-playing agents (RPAs) that addresses the problem of out-of-knowledge questions. It consists of three components — Adaptive Context-aware Text Splitter (ACTS), Guided Selection (GS), and Attribute Extractor (AE) — plus a manually curated dataset (CharacterRAG, 15 characters, 450 QA pairs). Evaluations show substantial improvements on MBTI/BFI personality assessments but marginal gains on in-knowledge QA, with a critical absence of ablation experiments.

## Strengths

1. **Well-motivated problem.** Out-of-knowledge queries are a genuine limitation of RAG-based role-playing that prior work has largely overlooked. The paper clearly identifies and demonstrates this gap (Figure 1).

2. **CharacterRAG dataset is carefully constructed.** The manual removal of omniscient-narrator framing and character-popularity information (Section 2.1) goes beyond what typical role-playing datasets do. This is a genuine community resource.

3. **Strong MBTI/BFI results.** 85.00% MBTI accuracy vs. 65.00–68.33% for baselines and 81.33% BFI accuracy vs. 72.00–76.00% (Table 1). These are large, non-noise gaps.

4. **Well-conducted human evaluation.** Fourteen evaluators, Cronbach's alpha > 0.8 for both settings (Table 3), clear 5-point Likert protocol. Exceeds typical NLP standards.

## Weaknesses

### Fatal
None.

### Major

1. **No ablation study (structural gap).** AMADEUS has three components (ACTS, GS, AE) but no experiment isolates their individual contributions. The reader cannot tell which component drives the gains. Specifically: (a) AE extracts Belief/Value and Psychological Traits — the MBTI/BFI evaluation tests exactly these constructs, so AE alone might explain most of the improvement; (b) GS is a learned filter using the same LLM that generates the response, making its effect hard to separate from the generator; (c) ACTS is evaluated only on similarity scores (Table 2), a proxy metric, never on downstream response quality. Without ablations, the paper's central claim — that the *combination* of all three components is responsible — is unsupported. This is the most consequential omission.

2. **AE-MBTI/BFI evaluation coupling (evidential concern).** The pipeline explicitly extracts "Psychological Traits" and "Belief and Value" (AE's output) from persona chunks and then tests whether responses match expected MBTI/BFI types. This is a partial closed loop: the LLM receives the very information needed to pass the test. The MBTI/BFI results therefore primarily measure AE's ability to extract personality attributes from persona documents, not whether the RPA "maintains persona consistency" in the broader sense of naturally behaving like the character across diverse out-of-knowledge queries. Following prior work (Wang et al., 2024b; Park et al., 2025) mitigates but does not eliminate this concern; the paper oversells what these results demonstrate.

3. **Marginal and unqualified improvement on in-knowledge QA (Table 4).** On the CharacterRAG QA benchmark, AMADEUS improves over Naive RAG by only 1.34pp (GPT-4.1), 1.56pp (Gemma3), and 0.45pp (Qwen3). No confidence intervals, significance tests, or variance estimates are reported. With 450 questions, these gaps could easily arise from chance. The hallucination score improvements are similarly small (e.g., 2.89 vs 3.13 for GPT-4.1). The paper claims "best performance across all three LLMs" without acknowledging the weakness of this evidence.

### Minor

1. **ACTS novelty is modest.** Computing max paragraph length and using it as chunk size with overlap = half that length, plus hierarchical context via section headers, is a reasonable heuristic that builds on standard recursive text splitting. It is presented as a novel algorithmic contribution without sufficient differentiation.

2. **GS context window is narrow.** Slot size M=2 means at most 2 chunks are used for attribute inference. This narrow window should be discussed or ablated.

3. **Limited cultural and domain diversity in CharacterRAG.** All 15 characters are from anime/manga sourced from a single Korean wiki (Namuwiki). The paper claims "rigorous evaluation" without discussing this limitation.

4. **Similarity score evaluation (Table 2) is a proxy.** ACTS is evaluated only on embedding similarity rather than end-task persona consistency. This is informative for chunking quality but does not demonstrate downstream benefit.

### Trivial
- Table 1 has minor formatting inconsistencies in parenthetical counts.
- Figure 4's axis labels ("log 100%") need clarification.

## Nice-to-Haves
- Ablation study isolating ACTS, GS, and AE contributions on end-task metrics.
- A "Naive RAG + attribute prompting" baseline to test whether structured AE adds value over a simple prompt instruction.
- Error analysis categorizing failure modes across the 15 characters.
- Confidence intervals or bootstrap significance tests for Table 4.

## Removed Points
- **Missing prompts for GS/AE:** The paper states it will release code and supplementary materials. The appendix is stripped by the parser, so prompts may exist there. Removed per hard rule about missing appendix content.
- **CRAG/LightRAG are not informative baselines:** The paper's primary comparison is against Naive RAG (which is present). CRAG and LightRAG are supplementary explorations. Not a substantive weakness.
- **Figure 1 data provenance complaint:** Reflects a misreading — the 3×5 grid shows 15 per-character CDF plots (15 characters × 60 MBTI questions = 900 queries). The description is correct.
- **MBTI ground truth reliability:** The paper follows prior work (Wang et al., 2024b; Sang et al., 2022) in using personality-database.com. Field-standard limitation, not unique to this paper.
- **Dataset size (15 characters) criticized as too small:** The paper's contribution is the *careful curation*, not scale. The limitation is implicit from the reported numbers.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add an ablation study isolating each component's contribution — this is the single highest-leverage improvement and is necessary to support the paper's central claim.
2. Include a "Naive RAG + attribute prompting" baseline to test whether structured AE adds value over a simple prompt.
3. Report confidence intervals or bootstrap p-values for Table 4.
4. Explicitly discuss the limited domain diversity of CharacterRAG.
5. Clarify Figure 4's "log 100%" notation.

## Score and Decision
**Round 1 (Bracketing):** Compared against 30 retrieved papers across six score bands. Closest topical anchors: "Tell Me What You Don't Know: Enhancing Refusal Capabilities of Role-Playing Agents" (5.20, rejected — similar RPA benchmark+method with methodological rigor concerns), "MMRole" (6.50, accepted — larger-scale multimodal RPA framework), "BIG5-CHAT" (5.25, rejected — personality evaluation with similar circularity concerns), "PersonaEval" (4.00, rejected — RPA benchmark only), "KARPA" (4.60, rejected — training-free RAG framework).

**Initial bracket:** 4.0–5.5.

**Narrowing:** The missing ablation is a structural gap that prevents validation of the paper's core claim about multi-component interaction. The dataset and MBTI/BFI results are genuine contributions, but the evidence does not currently support the claim that all three components together are responsible for the improvement. The paper sits below acceptance threshold at a top venue.

**Final Score: 4.0**

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>
```