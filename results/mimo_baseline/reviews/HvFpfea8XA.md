## Summary

This paper proposes AMADEUS, a training-free RAG-based framework for role-playing agents (RPAs) that enhances persona consistency when responding to queries outside a character's explicit knowledge. The framework comprises three components—Adaptive Context-aware Text Splitter (ACTS), Guided Selection (GS), and Attribute Extractor (AE)—and is evaluated on a newly constructed CharacterRAG dataset of 15 fictional characters with 450 QA pairs, as well as MBTI/BFI psychological questionnaire-based assessments.

## Strengths

- **Relevant and underexplored research direction.** Applying RAG to role-playing agents is a practical gap in the literature. The paper clearly motivates the problem of hallucination when persona documents lack direct knowledge for a query (Figure 1 shows concrete chunk duplication behavior).

- **CharacterRAG dataset contribution.** The manually constructed dataset of 15 fictional characters with hierarchical persona documents and attribute-tagged QA pairs fills a genuine gap. The construction methodology—filtering out non-character-perspective information—demonstrates careful design.

- **Well-designed human evaluation.** Table 3 evaluates the reliability of GS+AE outputs via 14 human evaluators using a 5-point Likert scale, reporting Cronbach's alpha (0.825, 0.810), which exceeds the 0.8 threshold for high internal consistency. This strengthens the credibility of the attribute extraction pipeline.

- **Comprehensive experimental breadth.** The paper tests 3 LLMs (GPT-4.1, Gemma3-27B, Qwen3-32B), 3 embedding models (BGE-M3, Qwen3-0.6B, mE5-large-instruct), multiple RAG baselines (Naive RAG, CRAG, LightRAG), and multiple evaluation protocols (CharacterRAG QA, MBTI, BFI).

- **Strong MBTI/BFI results.** On the out-of-knowledge psychological assessment (Table 1), AMADEUS achieves sum|d|=9 for MBTI versus 19–21 for baselines, and accuracy of 85% versus 65–68%. This demonstrates the framework's core value proposition for persona-consistent responses to novel queries.

## Weaknesses

### Fatal
None.

### Major

- **No ablation study.** The paper does not isolate the individual contribution of each component (ACTS, GS, AE). Without ablation experiments such as ACTS-only, ACTS+GS, and ACTS+GS+AE, it is impossible to determine what drives the improvements. This is a critical omission for a method paper proposing three distinct components.

- **Very marginal improvements on the primary CharacterRAG benchmark.** Table 4 shows that over Naive RAG, AMADEUS improves ACC by only 1.34% (GPT-4.1), 1.56% (Gemma3-27B), and 0.45% (Qwen3-32B). These gains are within typical noise ranges and are not supported by confidence intervals or statistical significance tests. The hallucination score improvements are similarly small (e.g., 3.13→2.89 for GPT-4.1). The paper's strongest results are on MBTI/BFI, but these use a different set of characters (Table 1: Anya Forger, Chika Fujiwara, etc.) than CharacterRAG (Table 4: Tanjiro Kamado, Nezuko Kamado, etc.), and the connection between the two evaluations is not clearly explained.

- **High computational cost of GS not discussed.** GS invokes an LLM (GPT-4.1) up to 30 times per query to filter chunks. The paper does not report latency, cost per query, or compare against simpler alternatives (e.g., TopK with re-ranking). For a training-free method that relies heavily on LLM API calls at inference, this is a significant omission that affects practical utility.

- **Inconsistent use of character sets across experiments.** The CharacterRAG dataset contains characters like Tanjiro Kamado and Muzan Kibutsuji, while the MBTI/BFI experiments (Table 1) use characters like Anya Forger and Edward Elric. The paper does not clarify where the persona documents for the Table 1 characters come from, whether they are also in CharacterRAG, or why different character sets are used for different evaluations. This undermines the coherence of the experimental narrative.

### Minor

- **LLM evaluator details missing.** The paper states metrics are "LLM-based" but does not specify which LLM serves as the judge, what prompt is used, or how evaluator reliability is validated against human judgments.

- **Small dataset scale.** 15 characters and 450 QA pairs is limited, though the authors acknowledge this. The MBTI/BFI evaluation relies on ground truth from crowd-sourced personality assessments of fictional characters (personality-database.com), which is an inherently noisy signal.

- **Overlap coefficient selection is empirical.** The choice of α=2 (overlap = l_max/2) is supported only by a single ridgeline plot (Figure 4) comparing four values. A more rigorous analysis of how chunk overlap affects downstream role-playing quality would strengthen the contribution.

- **Qwen3-32B thinking mode shows no benefit.** While the paper reports this finding, it is only briefly mentioned with a single sentence. Understanding why chain-of-thought reasoning fails to help in role-playing would be a valuable contribution if analyzed more deeply.

### Trivial
None.

## Nice-to-Haves

- A cost/latency comparison showing GS overhead versus simpler re-ranking methods, to justify the additional LLM calls.
- Per-character breakdowns of performance to identify where AMADEUS helps most and where it does not.
- Exploration of whether the attribute extraction from GS could be done with smaller/cheaper models while maintaining quality.

## Novel Insights

The key insight—that RAG-based RPAs overuse irrelevant chunks when queries fall outside a character's knowledge base, and that extracting general character attributes (beliefs, psychological traits) from contextually relevant chunks provides a more robust signal than direct knowledge retrieval—is genuinely interesting and practically relevant. The observation that graph-based RAG (LightRAG) and web-search RAG (CRAG) are poorly suited for role-playing due to entity ambiguity and persona inconsistency is also a useful empirical finding for the community.

## Suggestions

- Add a full ablation table (ACTS only, ACTS+GS, ACTS+GS+AE) on both CharacterRAG and MBTI/BFI to clarify component contributions.
- Report per-query cost and latency for GS versus baselines.
- Clarify the relationship between the two character sets used in experiments and unify the experimental setup.
- Specify the LLM judge model and prompt used for metric computation, and validate against human ratings.
- Report confidence intervals or perform bootstrap significance testing for all metrics.

## Score and Decision

The paper addresses a relevant problem and provides a new dataset, but the core methodological improvements are very small on the primary benchmark (CharacterRAG), there is no ablation to understand what drives results, and the high inference cost of GS goes unexamined. The stronger MBTI/BFI results use a different character set, weakening the overall experimental coherence. The contributions are incremental rather than transformative.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject