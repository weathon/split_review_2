Now let me read the remaining sections more carefully to check a few specific claims:Now I have a thorough understanding of the paper. Let me draft the post-filtering review.Now let me run calibration Round 1 — Bracketing:Let me read the most relevant anchor papers to calibrate:Now let me read the most directly comparable RPA paper more carefully:Now I have sufficient information to form my bracket and write the final review. 

**Round 1 Bracket: 4.0–5.5**

The paper sits above pure evaluation benchmarks like PersonaEval (4.00, rejected) due to its combined dataset+method contribution and substantial MBTI/BFI improvements, but below the more comprehensive MMRole framework (6.50, accepted) which has larger scale, a novel paradigm shift, and broader evaluation. The three major experimental gaps (no ablation, no long-context baseline, no cost analysis) prevent it from reaching the level of "Tell Me What You Don't Know" (5.20, rejected), which had stronger analytical contributions despite similar LLM-as-judge concerns.

Now let me write the final consolidated review:

---

## Summary
This paper introduces AMADEUS, a training-free RAG framework for role-playing agents (RPAs) consisting of three components: Adaptive Context-aware Text Splitter (ACTS), Guided Selection (GS), and Attribute Extractor (AE). The framework targets the under-explored problem of maintaining persona consistency when RPAs face queries outside a character's explicit knowledge. The paper also contributes CharacterRAG, a manually curated dataset of 15 fictional characters with persona documents totaling 976K characters and 450 QA pairs. Evaluation covers in-knowledge QA (CharacterRAG) and out-of-knowledge personality-type inference (MBTI/BFI).

## Strengths

- **Concrete problem identification with empirical evidence.** The observation that naive RAG over-concentrates on a small set of chunks for out-of-knowledge queries is well-illustrated. Figure 1 quantifies this: chunk usage rate increases from 34.93% to 43.84% with AMADEUS, and the CDF distributions become more uniform across all 15 characters. This is a specific, actionable observation rather than a vague claim.

- **Substantial improvement on out-of-knowledge tasks.** Table 1 shows AMADEUS achieving 85.00% MBTI accuracy vs. 65.00% for Naive RAG (Σ|d| drops from 21→9), and 81.33% BFI accuracy vs. 72.00% (Σ|d| 21→14) with GPT-4.1. Individual character results are detailed, making the improvement pattern transparent—e.g., Anya Forger goes from ISFP(-2) to ENFP(0), and Tobio Kageyama from ENFJ(-3) to ISTJ(0).

- **CharacterRAG is a useful artifact.** 15 manually curated persona documents totaling 976K characters, with editorial noise removed (popularity polls, editor speculation). The six-attribute taxonomy (Section 2.2) and the careful construction process from a character's perspective are well-motivated. The decision to strip meta-information that could contaminate persona consistency is thoughtful.

- **Human evaluation with internal consistency reporting.** Table 3 reports human evaluation of GS+AE outputs with Cronbach's alpha of 0.810–0.825 across 14 evaluators, exceeding the 0.8 threshold for high internal consistency. This is a meaningful validation that the intermediate pipeline produces outputs humans find reasonable.

- **ACTS's hierarchical context preservation is well-grounded.** Table 2 demonstrates that ACTS consistently achieves higher mean similarity scores and lower variance than four alternative chunking strategies across three embedding models (BGE-M3, Qwen3-0.6B, mE5-large-instruct).

## Weaknesses

### Fatal
None

### Major

- **No ablation study isolating components on downstream tasks.** The paper proposes three components (ACTS, GS, AE) but never tests them in isolation or pairwise on the primary evaluation tasks (MBTI/BFI accuracy in Table 1; ACC/ACC_L/HS in Table 4). Table 2 compares chunking strategies (ATS vs. ACTS) but only on embedding similarity scores—a proxy metric—not on actual role-playing performance. The reader cannot determine whether the 65%→85% MBTI accuracy improvement comes primarily from better chunking (ACTS), smarter retrieval (GS), attribute extraction (AE), or their combination. For a multi-component framework, this is a significant gap: if one component drives most of the gain, the others may not be pulling their weight.

- **Missing long-context baseline.** The introduction explicitly motivates RAG as an alternative to long-context models (Section 1), yet the paper never compares against simply providing the full persona document to a long-context LLM. Persona documents range from ~32K to ~145K characters (Figure 2a), well within GPT-4.1's 1M token context window. The "w/o RAG" baseline in Table 4 tests the model with *no persona at all* (49.56% ACC), which is a fundamentally different and much weaker comparison. If providing the full persona achieves comparable consistency, the entire RAG-based framework becomes unnecessary at this data scale.

- **Undiscussed computational cost.** Algorithm 1 iterates through up to N=30 chunks, making an individual LLM call for each to determine attribute relevance. With slot size M=2, early termination is possible after finding 2 suitable chunks, but worst-case is 30 GPT-4.1 calls for GS alone, plus AE and final generation calls. For a framework targeting interactive dialogue, this inference-time cost is non-trivial. The paper mentions benchmarking on an H100 NVL GPU (Section 5.1) but reports no latency, throughput, or API cost figures. Even basic statistics (e.g., average GS iterations before termination) would help assess practical viability.

### Minor

- **Marginal in-knowledge improvement with overclaimed framing.** On CharacterRAG QA (Table 4), AMADEUS achieves 92.67% vs. Naive RAG's 91.33% ACC (+1.34pp) and 9.26 vs. 9.23 ACC_L with GPT-4.1. While gains on Gemma3-27B and Qwen3-32B are slightly larger, these are modest. The abstract's claim that AMADEUS "significantly enhances persona consistency" is not qualified to distinguish the marginal in-knowledge setting from the more substantial out-of-knowledge improvements.

- **LLM-as-judge overlap.** GPT-4.1 is used for both GS/AE implementation (Section 5.1) and as the evaluation judge for ACC, ACC_L, and HS (Section 5.2). This creates a potential self-evaluation bias. The human evaluation in Table 3 partially mitigates this for the GS+AE step, and the MBTI/BFI evaluation in Table 1 is based on personality-type matching rather than LLM scoring, so the circularity concern is more narrowly about the CharacterRAG QA metrics.

- **Language and generalizability underspecified.** CharacterRAG is sourced from Namuwiki (Korean), confirmed by footnote 2 and the ethics statement ("The Korean-language dataset was used solely for academic research"). However, the paper does not clearly specify whether experiments were conducted in Korean, whether translation was involved, or how this affects generalizability. All 15 characters are from anime/manga, which further narrows the domain.

- **Overgeneralized claims about alternative RAG architectures.** The bolded section header "Graph-Based RAG and Web Search-Based RAG Are Unsuitable for Role-Playing" is too strong given the evidence. The experiments test LightRAG and CRAG on 15 anime characters with Korean-language data. The paper itself acknowledges the GraphRAG comparison is indirect: "While we did not perform a direct comparison, we observed that GraphRAG suffers from similar problems" (Section 5.3). The poor performance could stem from configuration choices or domain mismatch rather than fundamental unsuitability.

- **AE restricted to two attributes with thin justification.** Footnote 3 states Belief/Value and Psychological Traits "directly influence a character's behavior," but Activities, Social Relationships, and Skills (defined in Section 2.2) also influence behavior. The selection of only two attributes for AE appears somewhat ad hoc; a brief ablation over attribute subsets would strengthen this design choice.

### Trivial
None

## Nice-to-Haves

- A complete ablation study across component combinations (ACTS only, ACTS+GS, ACTS+GS+AE) on all downstream tasks would be the single most impactful addition.
- Computational cost reporting: average GS iterations before early termination, latency per query, and API cost estimates.
- Testing on characters from non-anime/manga domains and non-Korean sources to establish generalizability.
- Using a different model family (e.g., Claude or Gemini) as the evaluation judge to explicitly rule out self-evaluation bias on CharacterRAG QA metrics.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **GS prompt not provided in main text (removed).** The exact prompt for the LLM call in Algorithm 1 line 8 is not shown in the main text, but may be in the appendix which was stripped by the parser. Removed per rules about missing appendix content.
- **ACTS overlap validation only on proxy metric (removed).** Figure 4 validates the overlap coefficient on similarity score distributions, not downstream performance. This concern is subsumed by the broader ablation weakness already retained.
- **Noisy crowd-sourced labels framed as a fatal concern (demoted).** The reviewer characterized personality-database.com labels as fundamentally unreliable, but the paper follows established conventions from prior work (Wang et al., 2024b; Park et al., 2025; Sang et al., 2022). Using crowd-sourced personality labels is standard practice in the RPA evaluation literature. The concern is retained as Minor rather than structural.
- **Missing limitations section (removed).** The paper's conclusion is brief and optimistic, but this is a presentation preference, not a substantive flaw.
- **Binary yes/no in GS discards degree of relevance (removed).** The reviewer noted GS treats weakly and strongly relevant chunks identically. This is a design choice rather than a demonstrated flaw; the human evaluation in Table 3 (mean ~4/5) suggests the binary approach works adequately in practice.

## Novel Insights
The paper's core observation—that naive RAG for role-playing concentrates on a small set of irrelevant chunks when handling out-of-knowledge queries, and that this can be addressed by reframing retrieval as attribute inference rather than direct answer retrieval—is a genuinely novel and useful framing. The idea of using retrieved chunks not to find a direct answer but to infer character attributes (beliefs, personality traits) that then guide generation represents a meaningful conceptual shift in how RAG can be applied to persona-based dialogue systems.

## Suggestions
- **Priority 1:** Conduct a full ablation study: ACTS-only, ACTS+GS, ACTS+GS+AE on both MBTI/BFI and CharacterRAG QA tasks across at least one LLM.
- **Priority 2:** Add the long-context baseline: feed the full persona document to GPT-4.1 without any retrieval, and compare on all metrics.
- **Priority 3:** Report average number of GS iterations before slot fills, wall-clock latency per query, and approximate API cost.
- Qualify the abstract's "significantly enhances" claim to distinguish in-knowledge (marginal) from out-of-knowledge (substantial) improvements.
- Soften the "unsuitable for role-playing" claim about graph/web RAG to "performed poorly in our setting."

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| NEMESIS: Jailbreaking LLMs | 5kMwiMnUip | 1.40 | R1 | Fundamentally flawed; AMADEUS is far stronger |
| Scaling In-the-Wild Training (IC-Light) | u1cQYxRI1H | 10.00 | R1 | Top-tier accepted work; AMADEUS not at this level |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.00 | R1 | Not a real contribution; AMADEUS clearly above |
| Time-dependent Scientific Discourse | P49gSPmrvN | 1.00 | R1 | Not a real contribution; AMADEUS clearly above |
| Reward-RAG | oqRe1KvD17 | 3.00 | R1 | Weak experimental setup and unfair comparisons; AMADEUS has stronger dataset contribution and clearer problem |
| Multimodal RAG QA | fMaEbeJGpp | 2.50 | R1 | Limited novelty; AMADEUS contributes more |
| EDU-RAG | a2rSx6t4EV | 2.33 | R1 | Benchmark-only with limited analysis; AMADEUS has both method and dataset |
| LLM Anti-Social Behavior | acDwoHrwZ8 | 3.00 | R1 | Different domain, limited depth; AMADEUS comparable in rigor |
| Personas as Truthfulness | rKMQhP6iAv | 4.25 | R1 | Interesting hypothesis but limited validation; AMADEUS has more extensive experiments |
| Tell Me What You Don't Know (RPA refusal) | 87DtYFaH2d | 5.20 | R1 | Stronger analytical contribution (representation analysis) with RPA benchmark; AMADEUS has weaker experimental validation |
| PersonaEval | wZbkQStAXj | 4.00 | R1 | Benchmark-only, limited scope; AMADEUS has broader contribution (method + dataset) |
| No Free Lunch: RAG Fairness | cphaRg46jD | 4.50 | R1 | Different focus, similar experimental gaps |
| MMRole | FGSgsefE0Y | 6.50 | R1 | Comprehensive multimodal RPA framework with large-scale dataset; AMADEUS is narrower and less thoroughly validated |
| Bias Runs Deep: Persona-Assigned LLMs | kGteeZ18Ir | 5.75 | R1 | Extensive study with clear findings; AMADEUS has comparable breadth but weaker experimental completeness |
| RAG-DDR | Pnktu2PBXD | 6.00 | R1 | Clean method with thorough ablations; AMADEUS lacks this experimental rigor |
| InstructRAG | P1qhkp8gQT | 7.00 | R1 | Strong RAG method with clear ablations; AMADEUS doesn't reach this level of validation |
| Trustworthiness in RAG | Iyrtb9EJBp | 8.00 | R1 | Comprehensive evaluation and method; well above AMADEUS's validation level |
| Synthetic Continued Pretraining | 07yvxWDSla | 8.00 | R1 | Novel paradigm with strong theoretical grounding; well above AMADEUS |
| EQA-MX | 7gUrYE50Rb | 8.00 | R1 | Large-scale novel contribution; well above AMADEUS |
| Retrieval Head Mechanistically | EytBpUGB1Z | 8.00 | R1 | Deep mechanistic analysis; different category entirely |

### Scoring Rationale

**Round 1 bracket: 4.0–5.5.** The paper has genuine contributions (CharacterRAG dataset, novel attribute-inference framing for RAG-based RPAs, substantial MBTI/BFI improvements) that place it above reject-range RAG papers like Reward-RAG (3.00) and EDU-RAG (2.33). However, three compounding major gaps—no ablation study, no long-context baseline, and no cost analysis—prevent the paper from reaching the level of accepted RPA papers like MMRole (6.50) or accepted RAG papers like RAG-DDR (6.00) and InstructRAG (7.00), all of which feature cleaner experimental validation.

Comparing within the bracket: AMADEUS contributes more than PersonaEval (4.00, benchmark only) and Personas as Truthfulness (4.25, limited validation), but falls below "Tell Me What You Don't Know" (5.20) which offers deeper analysis despite similar scale. The missing long-context baseline is particularly impactful because it questions the fundamental necessity of the RAG framework at this data scale. The marginal in-knowledge improvement (92.67% vs 91.33%) further weakens confidence, though the out-of-knowledge results are genuinely strong.

The paper occupies the borderline-reject zone: real contributions exist but the evidence is insufficient to support the claims with confidence. The three major gaps are all addressable in revision, suggesting the work has potential but is not ready in its current form.

**Final score: 4.5**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>