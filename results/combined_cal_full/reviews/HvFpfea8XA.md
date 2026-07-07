Here is my final consolidated review.

## Summary

This paper proposes AMADEUS, a training-free framework for RAG-based role-playing agents that combines adaptive chunking (ACTS), guided chunk selection (GS), and attribute extraction (AE) to maintain persona consistency even for queries beyond a character's explicit knowledge. It also introduces CharacterRAG, a manually constructed dataset of 976K-character persona documents for 15 fictional characters with 450 QA pairs. Experiments compare AMADEUS against Naive RAG, CRAG, and LightRAG on both in-knowledge QA and out-of-knowledge MBTI/BFI personality assessments.

## Strengths

- **CharacterRAG dataset fills a genuine gap.** No existing dataset was designed specifically for RAG-based role-playing. Manually constructing 976K-character persona documents from Namuwiki for 15 characters and producing 450 QA pairs with six attribute categories is a non-trivial annotation effort that can be reused by the community. (Weight: +3.36)

- **ACTS chunking strategy shows clear improvement in retrieval quality.** Table 2 demonstrates that ACTS achieves higher mean similarity scores (∑μ) and lower variance (∑σ²) across three embedding models (BGE-M3, Qwen3-0.6B, mE5-large-instruct) compared to standard chunkers (RCTS, MHTS, SC, ATS), with the addition of hierarchical context providing further gains over adaptive sizing alone. (Weight: +4.07)

- **Well-motivated problem with concrete diagnosis.** The paper identifies a genuine failure mode for RAG-based role-playing: when queries go beyond explicit persona knowledge, existing RAG methods overuse less-relevant chunks. Figure 1 provides a concrete illustration of this chunk duplication problem, and the paper's overall framing of the gap is clear. (Weight: +2.99)

## Weaknesses

### Major

- **MBTI/BFI evaluation missing w/o RAG control — confound with parametric knowledge.** The paper's primary evidence for handling out-of-knowledge questions (Table 1) does not include a no-RAG baseline. Characters like Son Goku, Light Yagami, Edward Elric, and Tanjiro Kamado are among the most widely discussed fictional characters online; LLMs almost certainly have substantial parametric knowledge of their personalities from training data. The paper acknowledges this confound for CharacterRAG QA (Table 4 includes a w/o RAG column showing 18–49% accuracy across LLMs) but provides no comparable control for MBTI/BFI. Without this, we cannot determine how much of AMADEUS's 85% MBTI accuracy reflects effective RAG-based inference vs. the LLM's prior knowledge of popular characters. (Weight: -3.37)

- **MBTI/BFI evaluation protocol critically under-specified.** The paper states it follows "interview-based assessments" but does not specify: (a) how free-form RPA responses are converted to 4-letter MBTI types or 5-letter SLOAN types (by an LLM judge, rule-based mapping, or human evaluators?); (b) what the SLOAN typology represents — it is never defined anywhere in the paper, yet it is used for all Big Five results; (c) how Accuracy and Avg F1-Score in Table 1 are computed from per-character letter-level predictions. These gaps make the evaluation difficult to assess or reproduce. (Weight: -4.11)

- **No end-to-end ablation of the full AMADEUS pipeline.** The paper ablates ACTS alone (Table 2: chunking strategies) and evaluates GS+AE output quality via human evaluation (Table 3), but never ablates the complete system. We do not know how much of the MBTI/BFI improvement comes from ACTS (better chunking, applicable to any RAG system) vs. GS (guided selection) vs. AE (attribute extraction). Without this, improvements cannot be attributed to the proposed components. (Weight: -3.06)

### Minor

- **CharacterRAG QA gains are very small with no significance testing.** In Table 4, AMADEUS improves ACC over Naive RAG by only 0.45–1.56% across the three LLMs (GPT-4.1: 92.67% vs. 91.33%; Gemma3-27B: 88.00% vs. 86.44%; Qwen3-32B: 78.89% vs. 78.44%). With 450 QA pairs and no confidence intervals or significance tests, these differences could fall within evaluation noise — especially since the metrics themselves are LLM-based, introducing additional variance. (Weight: -3.89)

- **LightRAG/CRAG conclusions may overgeneralize.** The paper concludes that graph-based and web-search-based RAG are "unsuitable for role-playing." However, LightRAG (designed for entity-centric knowledge graphs) and CRAG (designed for factoid QA with web correction) are applied to narrative persona documents and personality inference — a substantial domain mismatch. The strong dismissive framing goes beyond what the experimental setup supports. (Weight: -2.36)

- **Human annotator details omitted.** The paper mentions "human annotators" for dataset construction and 14 evaluators for the human evaluation (Table 3), but provides no information on annotator qualifications, number of annotators (for dataset construction), or inter-annotator agreement for the QA construction task. (Weight: -1.47)

- **Dataset language gap not addressed.** Line 100 states the persona documents are "based on Korean data" from Namuwiki, while the MBTI/BFI questions and evaluation appear to be in English. The paper does not discuss whether translation was needed or how language mismatch interacts with the role-playing evaluation, affecting reproducibility. (Weight: -0.44)

- **GS computational cost not discussed.** Algorithm 1 makes up to N=30 LLM calls per query (iterating over chunks). Across 60 MBTI + 120 BFI questions × 15 characters, this could be tens of thousands of LLM calls. The paper does not acknowledge or compare this cost to baselines. (Weight: -0.87)

- **Same-model evaluation concern.** GS and AE use GPT-4.1, and the three LLM-based metrics (ACC, ACC_L, HS) do not specify which model serves as judge. If GPT-4.1 is used for both the pipeline and evaluation, there is a risk of bias favoring the method's outputs. (Weight: +0.40 — the model-weighted item is near-zero, indicating this is a minor concern)

### Trivial

- "Chunk duplication frequency" in Figure 1 is mentioned but never formally defined as a metric. (Weight: -4.48)
- HS is reported as "-" for w/o RAG and LightRAG in Table 4 without explanation. (Weight: -2.76)

## Nice-to-Haves

- Add a w/o-RAG baseline to the MBTI/BFI evaluation (Table 1) to control for the parametric knowledge confound.
- Add a full-pipeline ablation (AMADEUS vs. ACTS-only, ACTS+GS, ACTS+AE) to isolate each component's contribution.
- Report confidence intervals or bootstrap significance tests for the small CharacterRAG QA improvements.
- Disclose the complete MBTI/BFI prediction protocol: how responses map to personality types, evaluator identity, SLOAN definition, and metric computation formulas.
- Discuss the computational cost of GS (N=30 LLM calls per query) relative to baselines.
- Clarify how the Korean-language persona documents interact with English-language questions and evaluation.

## Removed Points

- Criticism about character names ("Sanpō," "Tsuzaki," "Mao Mao") being potentially non-standard or misspelled — speculative; the reviewer lacks source material knowledge to verify.
- Criticism about Equation (1) being a "high-level abstraction" — this is a reasonable simplification, not a weakness.
- Criticism about Table 5 being referenced but not present — the appendix section is stripped by the parser; it exists in the original submission.
- Criticism about only 2 of 6 attributes being used in AE — the paper justifies this choice (line 204: "Unlike other attributes, Belief and Value and Psychological Traits directly influence a character's behavior").
- Criticism about overlap coefficient α=2 being only empirically motivated — a minor design choice, not a substantive weakness.
- Criticism about "thinking mode" results not being reported quantitatively — the paper mentions the finding qualitatively; incorporated into Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis surfaces the key evidential gaps (missing w/o RAG control, under-specified protocol, missing ablation) but does not identify any novel perspective that the authors themselves did not recognize.

## Suggestions

1. Add a w/o-RAG column to Table 1 to control for LLMs' parametric knowledge of popular fictional characters' personalities.
2. Ablate the full AMADEUS pipeline: compare ACTS-only, ACTS+GS, ACTS+AE, and full AMADEUS on the MBTI/BFI task.
3. Report bootstrap confidence intervals for Table 4's CharacterRAG QA improvements.
4. Specify the MBTI/SLOAN prediction mechanism (who or what maps responses to types, and how metrics are computed).
5. Define the SLOAN typology (or replace it with the more standard OCEAN labels for Big Five).

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/87DtYFaH2d.md (Tell Me What You Don't Know: Enhancing Refusal Capabilities of RPAs) | 5.20 | R1 | Yes | Shares concerns about evaluation rigor and same-model bias; but 87DtYFaH2d has stronger strengths (+6.74, +7.02) and a higher net item weight. This paper is slightly weaker. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FGSgsefE0Y.md (MMRole: Multimodal RPAs) | 6.50 | R1 | Yes | More comprehensive dataset (85 characters, 11K images) and stronger evaluation framework. This paper's evaluation gaps are more significant. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wZbkQStAXj.md (PersonaEval: Role-Playing Evaluation) | 4.00 | R1 | Yes | Both have evaluation validity concerns, but this paper has a concrete dataset and method, whereas PersonaEval's central premise is questioned. This paper is slightly stronger. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BCP5nAHXqs.md (Human Simulacra) | 5.60 | R2 | Yes | Shares "no ablation" and "limited evaluation" weaknesses, but Human Simulacra has stronger methodological rigor in dataset construction and psychology grounding. This paper is somewhat below. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rKMQhP6iAv.md (Personas as Truthfulness) | 4.25 | R1 | No | Both involve persona-based evaluation, but less topically similar. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/kGteeZ18Ir.md (Bias Runs Deep) | 5.75 | R1 | No | About persona-induced reasoning biases — different contribution type. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/cphaRg46jD.md (No Free Lunch: RAG Undermines Fairness) | 4.50 | R2 | No | About RAG's negative side effects; evaluation concerns but different topic. |

**Round 1 bracket:** 4.0–6.5 (based on initial calibration query results and similarity to anchors 4.00–6.50).

**Narrowing:** Round 2 confirmed the bracket, with the most similar topical anchors scoring 4.00 (PersonaEval), 5.20 (Tell Me What You Don't Know), and 5.60 (Human Simulacra). This paper lies between PersonaEval and the RPA refusal paper: it has a more concrete contribution than PersonaEval but weaker evaluation support than the refusal paper.

**Final score grounding:** The paper's weighted items show strengths totaling +10.42 and meaningful weaknesses totaling approximately -14.43 (majors + most significant minors), yielding a net negative. Compared to 87DtYFaH2d (5.20, net positive ~+17 from weighted items), this paper has less compelling strengths relative to its weaknesses. The paper's dataset and ACTS method are real contributions, but the evaluation gaps (missing w/o RAG control, under-specified protocol, missing ablation) prevent full confidence in the central claims, placing it in the borderline reject range.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>