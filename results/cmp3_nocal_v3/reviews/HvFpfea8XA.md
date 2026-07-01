## Summary

This paper proposes AMADEUS, a training-free RAG framework for role-playing agents (RPAs), consisting of three components: Adaptive Context-aware Text Splitter (ACTS), Guided Selection (GS), and Attribute Extractor (AE). It also contributes CharacterRAG, a manually constructed dataset of persona documents for 15 fictional characters (976K written characters, 450 QA pairs). The key challenge addressed is maintaining persona consistency when RPAs receive queries that fall outside a character's explicitly documented knowledge.

## Strengths

1. **CharacterRAG dataset fills a genuine resource gap.** The manual construction of persona documents for 15 fictional characters (976K written characters) with 450 QA pairs annotated across six attributes is a concrete, non-trivial contribution that stands independently of the method. The reconstruction from the character's perspective (removing editor-speculated content) demonstrates careful annotation design. No prior dataset was designed explicitly for RAG-based role-playing, making this a first-of-its-kind resource.

2. **Training-free framework design is practical.** AMADEUS requires no additional training or fine-tuning, leveraging off-the-shelf embedding models and LLM inference. The three-stage pipeline (ACTS → GS → AE) is conceptually clean and deployment-friendly.

3. **Relatively broad evaluation setup for an under-explored area.** The paper tests across three LLMs (GPT-4.1, Gemma3-27B, Qwen3-32B), three embedding models, three RAG baselines (Naive RAG, CRAG, LightRAG), and two psychological assessment frameworks (MBTI and BFI). This breadth is appropriate for an initial investigation into RAG-based RPAs.

4. **Well-motivated problem with a verifiable phenomenon.** Figure 1 concretely demonstrates that naive RAG overuses irrelevant chunks when queries fall outside a character's explicit knowledge, providing a clear empirical motivation for the proposed approach.

## Weaknesses

### Fatal

None.

### Major

1. **No ablation study of the three-component architecture.** AMADEUS consists of three distinct components (ACTS, GS, AE), yet the paper contains no ablation isolating each component's contribution. Table 2 evaluates ACTS vs. other chunking methods on similarity-score distributions, but this is not the same as measuring ACTS's impact on final role-playing quality. Table 4 compares full AMADEUS against baselines, conflating the effects of all three components. Without an ablation comparing (i) Naive RAG, (ii) Naive RAG + ACTS, (iii) Naive RAG + ACTS + GS, and (iv) full AMADEUS, the paper cannot attribute its claimed improvements to the specific mechanisms it proposes. This is a structural gap in the evaluation design.

2. **Main evaluation of final response quality lacks human validation and significance testing.** The core results on CharacterRAG (Table 4) use ACC, ACC_L, and HS — LLM-based metrics with no reported confidence intervals, standard deviations, or significance tests. The margins over Naive RAG are very small (e.g., GPT-4.1: 92.67% vs. 91.33% ACC, a 1.34 pp gap; ACC_L: 9.26 vs. 9.23 on a 1–10 scale). The human evaluation (Table 3) validates only the intermediate GS+AE outputs, not the final role-playing responses. This means the central claim — that AMADEUS produces better role-playing responses — rests on LLM-as-judge metrics with slender margins and no variance estimates. With 450 QA pairs, a ~1.3% difference could easily fall within random variation.

3. **MBTI/BFI prediction methodology is critically underspecified.** The paper states that 60 MBTI and 120 BFI questions are asked to each character (Section 5.2) but never describes how the model's responses are converted into a predicted MBTI/BFI type (e.g., the 4-letter code and SLOAN type shown in Table 1). Is an LLM used to score responses against the standard scoring key? Is a separate classifier used? This is a fundamental gap in reproducibility. Additionally, the ground-truth personality types come from Personality Database (personality-database.com), a crowd-sourced fan-voting website (Section 5.2, footnote 4). The paper provides no justification for treating these as authoritative ground truth, nor does it discuss the inherent subjectivity of fan consensus on fictional characters' personality types. While these design choices follow prior work (Wang et al., 2024b; Park et al., 2025), they need to be transparently described and their limitations acknowledged.

4. **No statistical significance or variance reporting.** None of the main tables (1, 2, 4) report confidence intervals, standard deviations across runs, or significance tests. Table 2 reports within-chunk variance (σ²) for similarity scores, but this is not across-run variance of the final evaluation. The paper has no multi-run or bootstrap-based variance estimates, making it impossible to assess whether observed differences are meaningful.

### Minor

1. **Language mismatch between persona documents and evaluation questions.** The CharacterRAG dataset is sourced from Namuwiki and is Korean-language (footnote 2, ethics statement). The MBTI/BFI questions are presumably in English (the paper does not specify). The embedding models include BGE-M3 (multilingual) and mE5-large-instruct (English-focused), yet the paper provides no discussion of how this language asymmetry might affect retrieval quality or overall results.

2. **GS fallback frequency and design parameters not reported.** Algorithm 1 includes a fallback (lines 14–16): if no chunks pass the LLM filter, the top-K+1 chunks by similarity are returned. The paper never reports how often this fallback triggers, making it impossible to assess whether GS is actively selecting chunks or mostly falling back to naive ranking. The search parameters (N=30, M=2) are stated but not justified or ablated.

3. **AE extracts only two of six attributes without justification.** The Attribute Extractor considers only "Belief and Value" and "Psychological Traits" (Section 4.3, footnote 3), asserting that these "directly influence a character's behavior." No analysis is provided to support this claim or to show that discarding the other four attributes (Activity, Demographic Information, Skill and Expertise, Social Relationships) does not harm responses to queries about those attributes.

4. **Missing HS values and unaddressed baseline behavior.** In Table 4, w/o RAG and LightRAG have "-" entries for HS with no explanation. This makes it difficult to compare hallucination behavior across all methods.

5. **Table 2 evaluates chunking on similarity scores, not role-playing quality.** The analysis shows ACTS achieves higher mean similarity and lower variance than other chunkers. However, higher similarity to the query is not necessarily better for role-playing — optimal retrieval might involve diverse information rather than the most similar chunks. This analysis supports a necessary condition for good chunking but is not sufficient evidence that ACTS improves role-playing.

### Trivial

None.

## Nice-to-Haves

- **Ablation study**: Comparing Naive RAG → +ACTS → +GS → +AE would substantially strengthen the paper's ability to attribute improvements to its proposed mechanisms.
- **Human evaluation of final responses**: A blinded study comparing Naive RAG vs. AMADEUS on persona consistency and naturalness of full responses, rather than only on intermediate GS+AE outputs.
- **Statistical significance**: Bootstrapped confidence intervals or multi-run variance estimates for the main results in Tables 1 and 4.
- **Qualitative analysis**: Case studies or failure analysis showing where AMADEUS succeeds and where it still struggles.
- **Clarify MBTI/BFI conversion protocol**: Specify how LLM responses are mapped to 4-letter MBTI codes and SLOAN types, including the scoring mechanism.

## Removed Points

These points are flagged to be removed; treat them with caution.

- "ACC_L cannot be used for MBTI/BFI settings" — The paper does not use ACC_L for MBTI/BFI (Figure 5 uses only HS for those settings). This criticism misunderstands the evaluation design.
- "Table 1 notation is ambiguous" — The parenthetical notation and Accuracy calculation are clearly explained in the table caption and are straightforward to interpret.
- "Related work section is too short" — Instructions prohibit commenting on missing related work as the reviewer cannot confirm the existence of unmentioned works.
- "ACTS O(N) claim is trivial" — This is a presentation nitpick with no bearing on the paper's core claims.
- "Introduction framing about long-context models is tangential" — The paper uses RAG's efficiency advantage as motivation; this is a reasonable positioning choice.
- "ACTS chunk length could exceed embedding model limits" — Chunk length is set to the maximum paragraph length in the persona, which is bounded by the document's paragraph structure.
- "MBTI scientific validity" — While MBTI has known psychometric limitations, the paper follows established prior work in the role-playing community (Wang et al., 2024b; Park et al., 2025); this is a community-standard design choice, not a unique flaw of this paper.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the expected tension between the paper's claimed contribution and the strength of its evidence, but do not provide novel scientific insights beyond what the paper itself offers.

## Suggestions

1. Add an ablation study isolating the contribution of each AMADEUS component (ACTS, GS, AE) to the final role-playing quality.
2. Report confidence intervals (e.g., bootstrapped) for all main results in Tables 1 and 4.
3. Specify the MBTI/BFI prediction methodology in detail: how are LLM responses mapped to predicted types, and what scoring protocol is used?
4. Clarify the language setting: state explicitly whether MBTI/BFI questions are in English or Korean, and discuss the potential impact of language mismatch on cross-lingual retrieval.
5. Report how often the GS fallback triggers (Algorithm 1, line 14–16) and provide an ablation or justification for the N=30, M=2 parameters.
6. Explain the missing HS entries ("-") in Table 4 for w/o RAG and LightRAG.
7. Consider a human evaluation of the final role-playing responses (not just intermediate GS+AE outputs) to validate the central claim.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>