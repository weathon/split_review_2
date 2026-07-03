Now I have all the information I need. Let me produce the final consolidated review.

## Summary

AMADEUS proposes a training-free three-component framework (ACTS, GS, AE) for RAG-based role-playing agents, designed to maintain persona consistency especially for queries beyond a character's explicit knowledge. The paper also contributes CharacterRAG, a manually constructed dataset of 15 fictional character personas (976K written characters, 450 QA pairs) built explicitly for RAG-based RPA development and evaluation. Experiments across three LLMs and three embedding models show the full system outperforms Naive RAG, CRAG, and LightRAG on personality inference and QA tasks.

## Strengths

1. **Large and well-documented gains on out-of-knowledge personality inference (Table 1)**: AMADEUS achieves 85.00% MBTI accuracy (Σ|d|=9) and 81.33% BFI accuracy (Σ|d|=14), substantially outperforming the next-best baseline (CRAG at 68.33%/Σ|d|=19 for MBTI). This directly supports the paper's central claim of maintaining persona consistency on out-of-knowledge queries. The improvement is large enough that even accounting for evaluation concerns, the trend is clearly positive.

2. **First dedicated RAG-based role-playing dataset (Section 2)**: CharacterRAG fills a clearly documented gap — "no existing benchmark explicitly targets role-playing under RAG" — with 15 characters, 976K written characters, 450 QA pairs, and manual removal of non-character-perspective information by human annotators. This is a reusable community resource that will likely benefit future research.

3. **Robust performance across diverse backbones and embeddings (Tables 2, 4)**: AMADEUS achieves the best ACC, ACC_L, and HS across all three tested LLMs (GPT-4.1, Gemma3-27B, Qwen3-32B) on CharacterRAG QA, and ACTS outperforms existing chunking methods across all three embedding models (BGE-M3, Qwen3-0.6B, mE5-large-instruct). This confirms generality beyond a single model. The ACTS chunking results (Table 2) are particularly clean and well-evidenced.

4. **Human evaluation with high inter-rater reliability (Table 3)**: Fourteen human evaluators rated GS+AE outputs, with Cronbach's alpha values of 0.825 and 0.810 — well above the 0.8 threshold for high internal consistency. This provides independent human-grounded evidence that the attribute extraction pipeline produces reasonable output.

5. **Empirical validation of ACTS design choices (Figure 4)**: The paper validates the overlap coefficient α=2 by fitting log-normal density ridgelines, showing this setting maximizes sum of similarity scores while minimizing variance, grounding a key hyperparameter in data rather than arbitrary selection.

## Weaknesses

### Fatal
None.

### Major

1. **No component ablation (Structural)**: The paper proposes three novel components (ACTS, GS, AE) but never tests any subset (e.g., "Naive RAG + ACTS only," "Naive RAG + ACTS + GS," "Naive RAG + ACTS + AE"). Because baselines (Naive RAG, CRAG, LightRAG) differ from AMADEUS in *multiple* ways simultaneously — chunking strategy, LLM-based chunk filtering (GS), and LLM-based attribute extraction (AE) — the reported improvements cannot be attributed to any specific component or mechanism. The gap in Table 1 (85% vs. 68.33%) could plausibly be driven entirely by the extra GPT-4.1 reasoning stages in GS and AE that no baseline receives. An ablation study is necessary to support the paper's central claim that the three-component design collectively produces the benefit. The paper claims the components are "three substages" of a coherent framework, but the community needs to know which parts actually matter.

2. **MBTI/BFI evaluation pipeline is underspecified and Table 1 contains verifiable inconsistencies (Evidential)**: The paper never describes how predicted personality types are derived from the model's free-form responses — there is no automatic classifier, LLM judge prompt, or scoring rubric disclosed. Section 5.2 merely states "we instead conduct interview-based assessments (Wang et al., 2024b) for each character and compare the results to psychological test outcomes." This is the central methodology behind Table 1, which is the paper's strongest evidence. Without knowing the classification protocol, the headline results cannot be independently reproduced or evaluated for potential bias (especially since the LLM used for classification may also be GPT-4.1, creating a circular evaluation concern).

   Additionally, Table 1 has verifiable internal inconsistencies:
   - **Chika Fujiwara MBTI (Naive RAG)**: Predicted INFP (0) with GT=ENFP. INFP and ENFP differ by one dimension (I vs. E), so the parenthetical should be (-1), not (0).
   - **Naive RAG MBTI Σ|d|**: Reported as 21, but summing the absolute values of the individual parentheticals gives 24.
   - **Naive RAG BFI Σ|d|**: Reported as 21, but summing the absolute values gives 23.
   
   These issues undermine confidence in the table's accuracy and need to be corrected and explained.

3. **GS and AE are confounded with a stronger LLM**: Section 5.1 states: "We implement Guided Selection (GS) and Attribute Extractor (AE) using GPT-4.1." This means even when Gemma3-27B or Qwen3-32B is used as the response-generation backbone, the framework leverages GPT-4.1 (a frontier model) for its filtering and extraction stages — an advantage none of the baselines receive. The improvement may partly reflect applying a stronger LLM to the retrieval results rather than the framework's architectural innovation. A controlled comparison that gives baselines a comparable "LLM reasoning on retrieved chunks" stage (without the proposed architectural components) would be needed to disentangle these factors.

### Minor

4. **Modest gains on CharacterRAG QA (Table 4)**: ACC improvements over Naive RAG are 1.34 pp (GPT-4.1), 1.56 pp (Gemma3), and 0.45 pp (Qwen3-32B). HS improvements are similarly small (e.g., 3.13→2.89 for GPT-4.1). The paper's framing ("significantly enhance," "markedly improves") overstates these numbers relative to the evidence.

5. **CRAG sometimes achieves lower hallucination scores than AMADEUS (Figure 5)**: For Qwen3-32B on MBTI, CRAG achieves HS=1.80 vs. AMADEUS HS=2.04. On BFI, CRAG achieves HS=1.96 vs. AMADEUS HS=2.03. The paper does not discuss these counterexamples.

6. **Computational cost not reported**: GS iterates through chunks with LLM calls (up to N=30 iterations per query). The paper emphasizes that the framework is "training-free," but inference cost could be substantially higher than single-pass retrieval baselines. Reporting average LLM calls per query would contextualize the practical trade-off.

7. **Limited cultural/literary scope of CharacterRAG**: All 15 characters are from Japanese anime/manga, sourced from a single Korean wiki (Namuwiki). The paper does not discuss this as a limitation, though it constrains the dataset's generalizability to broader role-playing contexts.

8. **Human evaluation (Table 3) is a proxy**: The evaluation assesses whether GS-selected chunks and AE-extracted attributes *appear reasonable to humans*, not whether the *final generated responses* are better. This validates intermediate outputs but not end-to-end response quality.

### Trivial

9. **"w/o RAG" HS not reported in Table 4**: The "w/o RAG" row has no HS values, making it impossible to compare hallucination when the model guesses without retrieval.

## Nice-to-Haves

- Adding role-playing-specific baselines (e.g., fine-tuned RPA or prompt-based role-playing) would help contextualize performance relative to the broader role-playing literature, though the paper's RAG-specific scope makes this an extension rather than a necessity.
- Reporting the language used for model prompting (the QA pairs are Korean, but embedding models are English-pretrained) would aid reproducibility.
- Disclosing whether the LLM-based MBTI/BFI classifier is also GPT-4.1 (and discussing potential circularity if so) would strengthen the evaluation.

## Removed Points

These points were flagged by at least one reviewer but removed from the main review:
1. **Figure 1 caption being garbled** — Parser artifact. The original submission does not have this issue.
2. **Missing proofs in appendix / missing appendix content** — Parser strips these sections from all papers; they exist in the original submission.
3. **"No role-playing-specific baseline" as a major weakness** — The paper explicitly scopes itself to *RAG-based* RPAs. Criticizing the absence of fine-tuned or prompt-based RPAs is scope creep. Placed in Nice-to-Haves instead.
4. **Generic reproducibility concerns about hyperparameters not being disclosed** — The paper discloses most key hyperparameters (N=30, M=2, α=2 etc.) to a reasonable degree.
5. **Formatting and typo nitpicks** — Parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a perspective on the work that the authors themselves have not already stated or implied.

## Suggestions

1. **Add component ablations** on the MBTI/BFI task testing at minimum: (i) Naive RAG + ACTS, (ii) Naive RAG + ACTS + GS, (iii) Naive RAG + ACTS + AE, and (iv) full AMADEUS. This is the single most impactful improvement.
2. **Disclose the MBTI/BFI classification protocol** — provide the exact prompts used, describe how free-form responses are mapped to 4-letter MBTI types and 5-letter SLOAN types, and state which model/classifier performs this mapping.
3. **Correct the inconsistencies in Table 1** and verify all computed Σ|d| values.
4. **Control for LLM confound**: Add a baseline where GS and AE's GPT-4.1 reasoning steps are replaced with a simpler heuristic (e.g., using the same chunk similarity scoring without LLM calls) to isolate the value of the architectural design.
5. **Report computational cost**: Average number of LLM calls per query for the full AMADEUS pipeline vs. each baseline.
6. **Discuss counterexamples**: Explain why CRAG achieves lower HS on some Qwen3 settings and what this implies about AMADEUS's limitations.
7. **Acknowledge dataset scope limitations** regarding the cultural and linguistic homogeneity of the characters.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>