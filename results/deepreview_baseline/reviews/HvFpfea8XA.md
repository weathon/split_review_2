## Summary

This paper proposes AMADEUS, a training-free framework for retrieval-augmented generation (RAG) based role-playing agents (RPAs). AMADEUS consists of three components: Adaptive Context-aware Text Splitter (ACTS) for persona chunking with hierarchical context, Guided Selection (GS) for relevant chunk retrieval, and Attribute Extractor (AE) for inferring character attributes. The authors also manually construct CharacterRAG, a role-playing dataset comprising persona documents for 15 fictional characters (976K characters) and 450 QA pairs. Experiments using psychological questionnaires (MBTI, BFI) and knowledge-based QA demonstrate that AMADEUS improves persona consistency compared to Naive RAG, CRAG, and LightRAG baselines.

## Strengths

- **Addresses an important and under-explored problem**: The paper tackles the practical challenge of RAG-based role-playing, particularly handling queries beyond explicit character knowledge—a realistic scenario in deployed RPAs that has received little prior attention.
- **Comprehensive evaluation approach**: The use of psychological questionnaires (MBTI and BFI with 60+120 questions) to evaluate persona consistency for out-of-knowledge queries is creative and appropriate, moving beyond simple QA accuracy metrics.
- **Human evaluation with reliability metrics**: The human evaluation of attribute extraction includes Cronbach's alpha (0.825 and 0.810), demonstrating acceptable inter-annotator reliability and strengthening claims about the method's plausibility.
- **Empirical validation of design choices**: The analysis of chunk overlap coefficients (Figure 4) and the ablation on chunking strategies (Table 2) provide concrete evidence supporting the specific design decisions in ACTS.

## Weaknesses

### Fatal

No fatal errors were identified.

### Major

- **GS algorithm's reliance on LLM-as-judge is poorly characterized**: The Guided Selection algorithm (Algorithm 1) uses an LLM to determine whether a chunk "contains information from which the character's attributes can be inferred" (lines 8-10). This is a central component of the method, yet the paper provides no analysis of this LLM-based judgment's accuracy, failure modes, or the prompt used. The entire method's success hinges on this step, making it a critical unvalidated component.

- **Contradictory results in Table 1 undermine claimed superiority**: For the MBTI task, AMADEUS achieves 85.00% accuracy vs. 68.33% for CRAG. However, looking at individual characters, CRAG actually predicts the correct type for more characters than AMADEUS: CRAG gets 4 correct (Chika, Frieren, Saitama, Tanjiro—4 out of 15, with the rest having at least one mismatch) while AMADEUS gets only 3 fully correct (Frieren, Hitori, Saitama). The accuracy metric appears to be computed in a way that dilutes these individual successes. This discrepancy between the aggregate metric and per-character results is unexplained.

- **Missing analysis of GS's out-of-knowledge detection capability**: The paper's core challenge is handling queries beyond character knowledge. GS's role is to identify relevant chunks or fall back to top-K similarity. However, the paper never evaluates how well GS distinguishes between queries that CAN be answered from persona vs. those that CANNOT. This is essential for understanding the method's behavior.

- **CharacterRAG dataset is Korean, but all models are English-centric**: The persona documents are from Namuwiki (Korean wiki), yet the experiments use GPT-4.1, Gemma3, and Qwen3—all primarily English-trained models. The paper does not discuss how cross-lingual transfer affects the results or whether observed improvements are confounded by translation effects.

### Minor

- **No statistical significance testing**: All comparisons are reported as point estimates without confidence intervals or significance tests. Given the small number of characters (15) and the variability in results (e.g., Light Yagami's MBTI prediction is the same for CRAG, LightRAG, and AMADEUS), statistical testing would help distinguish signal from noise.

- **Limited baselines**: The paper includes only three RAG baselines (Naive RAG, CRAG, LightRAG). Missing are methods specifically designed for RAG-based role-playing or character-consistent generation, such as prompt engineering approaches or the RAG system used in CharacterGLM or similar works.

- **ACTS overlap coefficient selection is empirically motivated but not theoretically justified**: The choice of l_max/2 is validated only on one overlap coefficient analysis (Figure 4), and the improvement over ATS (without hierarchy) in Table 2 is marginal for some embedding models (e.g., mE5: 12.3240 vs 12.2336).

### Trivial

- Figure 1's caption has a duplicated paragraph, but this is a parser artifact.

## Nice-to-Haves

- An ablation study isolating the contribution of each AMADEUS component (ACTS, GS, AE) on the MBTI/BFI tasks would strengthen the paper.
- Analysis of computational cost (latency, token usage) since GS involves iterative LLM calls.
- Error analysis showing which types of queries fail under each method.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Validate the GS judgment step**: Report accuracy of the LLM's binary decision (can attributes be inferred?) against human judgments on a held-out set, and include the prompt template used for this step.
2. **Clarify the MBTI accuracy calculation in Table 1**: Explain why the per-character results and aggregate accuracy appear inconsistent, and consider reporting both strict-match accuracy and a softer metric (e.g., average number of letter mismatches).
3. **Add statistical significance**: Use bootstrap or permutation tests to compare AMADEUS against baselines on the key metrics.
4. **Include a monolingual control experiment**: If possible, translate a subset of CharacterRAG to English and re-run experiments to assess cross-lingual effects.

## Score and Decision

The paper addresses a genuine and underexplored problem with a creative approach and reasonable experimental design. The main claims are supported by multiple evaluation settings (MBTI, BFI, QA), and the new dataset is a potential contribution. However, the major weaknesses—particularly the unvalidated LLM-based judgment in GS and the inconsistency in the MBTI accuracy reporting—prevent a stronger recommendation. The method's novelty is incremental (combining adaptive chunking with attribute extraction), and the empirical gains, while positive, are sometimes modest.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>