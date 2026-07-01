## Summary

This paper addresses the challenge of building retrieval-augmented generation (RAG) based role-playing agents (RPAs) that maintain persona consistency even when users ask questions beyond the character's explicit knowledge. The authors propose a training-free framework called AMADEUS, consisting of an Adaptive Context-aware Text Splitter (ACTS) for optimal persona chunking with hierarchical context, a Guided Selection (GS) module that retrieves chunks from which character attributes can be inferred, and an Attribute Extractor (AE) that extracts beliefs and psychological traits to guide responses. They also introduce CharacterRAG, a manually constructed dataset of 15 fictional characters (976K characters of persona text and 450 QA pairs). Experiments using multiple LLMs and embedding models show improvements over Naive RAG, CRAG, and LightRAG on both in-knowledge QA tasks and out-of-knowledge personality inference (MBTI and BFI).

## Strengths

- **Novel application area:** The paper identifies an important gap—RAG-based role-playing agents that handle out-of-knowledge queries—and proposes a structured framework tailored to this challenge, which has received little prior attention.
- **Training-free and modular design:** AMADEUS does not require additional fine-tuning, making it practical for deployment. The three components (ACTS, GS, AE) are clearly motivated and address specific failure modes of naive RAG in role-playing.
- **Comprehensive experimental scope:** The evaluation spans three LLMs (GPT-4.1, Gemma3-27B, Qwen3-32B), three embedding models, and three baselines, covering both in-knowledge tasks (CharacterRAG QA) and out-of-knowledge tasks (MBTI/BFI personality inference). The inclusion of human evaluation for the GS+AE component with acceptable inter-rater reliability (Cronbach's alpha > 0.8) is a positive step.
- **Dataset contribution:** CharacterRAG is a manually reconstructed persona dataset designed specifically for RAG-based role-playing, removing extraneous information that could break persona consistency. This fills a gap in existing resources.

## Weaknesses

### Fatal
None.

### Major

- **No ablation study isolating each proposed component:** The paper does not report results for ACTS alone, GS alone, or AE alone. Without an ablation, it is unclear how much each component contributes to the overall improvements, and whether simpler alternatives (e.g., better chunking alone) could achieve similar gains. This is a significant gap for a method paper.
- **Evaluation of out-of-knowledge capability is indirect and incompletely specified:** The main evidence for handling out-of-knowledge queries comes from matching predicted MBTI/BFI types to ground-truth labels from a community voting site. The reliability of these ground-truth labels is not discussed. More critically, the process for deriving predicted personality types from the model's responses is not described—is an LLM used to classify responses? What prompt? This lack of detail undermines reproducibility and makes it impossible to assess potential evaluation biases.
- **The Attribute Extractor is underspecified.** The paper states that AE extracts "Belief and Value" and "Psychological Traits" from chunks selected by GS, but provides no algorithm, prompt template, or even a high-level description of how this extraction is performed. Given that AE is a core novelty, this omission is a major weakness.
- **Marginal gains on in-knowledge tasks diminish the overall impact.** On the CharacterRAG QA benchmark (Table 4), AMADEUS improves over Naive RAG by only ~1–2 percentage points in accuracy across LLMs, with somewhat larger gains in hallucination scores. The primary claimed advantage is for out-of-knowledge queries, but the indirect personality-test evaluation makes it hard to gauge real-world significance.

### Minor

- **Dataset size is limited:** 15 characters and 450 QA pairs is a modest resource. While manual reconstruction justifies the scale, broader coverage would strengthen the conclusions.
- **Human evaluation only covers a sub-component.** The Likert-scale ratings assess whether GS+AE produce reasonable attribute extractions, but do not evaluate the end-to-end response quality or persona consistency of the full AMADEUS pipeline.
- **Chunk duplication frequency analysis (Figure 1) is unclear.** The figure shows 15 CDF plots with repeated MBTI labels, and it is not explained how "chunk duplication frequency" is computed or why it is measured per MBTI type rather than per character. The connection between this metric and downstream performance is asserted but not rigorously justified.
- **The claim about graph-based and web-search RAG unsuitability is overstated.** The paper evaluates only LightRAG and CRAG, and the poor performance of LightRAG may be due to implementation-specific issues rather than a fundamental incompatibility. The statement that "GraphRAG suffers from similar problems" without direct comparison is speculative.

### Trivial

None.

## Nice-to-Haves

- An ablation study that reports performance with and without each of the three components (ACTS, GS, AE).
- A clear description of how MBTI/BFI types are predicted from model responses, including the exact prompt or classifier used.
- Example prompts for the Guided Selection LLM call and the Attribute Extractor.
- A more thorough analysis of why LightRAG fails (e.g., entity ambiguity examples, graph construction statistics) to support the general claim about graph-based RAG unsuitability.
- Evaluation on additional role-playing datasets (e.g., existing character QA datasets) to show generalization beyond CharacterRAG.

## Novel Insights

Beyond the paper's own contributions, the key insight is that persona consistency in RAG-based role-playing requires not only retrieving relevant factual chunks but also inferring implicit attributes (beliefs, personality) from the narrative context, especially when the query has no explicit match in the persona. The observation that naive RAG over-uses irrelevant chunks for out-of-knowledge queries, and that this can be mitigated by an LLM-based guided selection step, is practically useful. However, this insight aligns with existing literature on multi-hop reasoning and attribute inference in dialogue systems.

## Suggestions

- Run an ablation study where ACTS, GS, and AE are removed one at a time, reporting results on both CharacterRAG QA and the MBTI/BFI tasks. This would clarify the individual contribution of each module.
- Provide the exact prompt templates used for (a) the Guided Selection LLM call (b) the Attribute Extractor, and (c) the final response generation. This is essential for reproducibility.
- For the MBTI/BFI evaluation, explicitly state how ground-truth personality types were validated and how the model responses were classified (including prompt or classification method). Consider using multiple independent classifiers to reduce bias.
- Discuss the limitations of using personality tests as a proxy for persona consistency, and consider adding a human evaluation of end-to-end response persona consistency for out-of-knowledge queries.

## Score and Decision

The paper addresses a relevant problem with a modular, training-free framework and contributes a new dataset. However, the lack of an ablation study and the underspecification of key components (AE, personality-type classification) substantially weaken the evidence for the framework's efficacy. The reported gains on in-knowledge tasks are modest, and the out-of-knowledge evaluation relies on an indirect metric whose computation is not fully described. These issues prevent me from recommending acceptance.

MY FINAL SCORE: 4.0

MY FINAL DECISION: Reject