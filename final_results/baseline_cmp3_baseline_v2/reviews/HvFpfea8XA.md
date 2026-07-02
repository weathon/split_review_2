## Summary
This paper introduces AMADEUS, a training-free framework for retrieval-augmented generation (RAG) based role-playing agents (RPAs). The framework consists of three components: Adaptive Context-aware Text Splitter (ACTS) for optimal persona chunking with hierarchical context, Guided Selection (GS) for retrieving relevant chunks, and Attribute Extractor (AE) for inferring character attributes. The authors also construct CharacterRAG, a manually curated dataset of 15 fictional characters with 976K characters of persona documents and 450 QA pairs. Experiments show that AMADEUS improves persona consistency, particularly for out-of-knowledge questions, achieving 85.00% MBTI accuracy and 81.33% BFI accuracy compared to baselines.

## Strengths
- **Novel problem framing**: The paper identifies and addresses a genuine gap in RAG-based role-playing—handling queries beyond a character's explicit knowledge—which is a practical and important challenge for deploying RPAs in real-world applications.
- **Comprehensive evaluation framework**: The use of psychological assessments (MBTI, BFI) as evaluation tools for out-of-knowledge questions is creative and well-motivated, providing a rigorous way to measure persona consistency beyond simple QA accuracy.
- **Strong empirical results**: The proposed method consistently outperforms baselines across multiple LLMs (GPT-4.1, Gemma3-27B, Qwen3-32B) and embedding models, with particularly notable improvements in MBTI accuracy (85.00% vs. 65.00-68.33% for baselines) and BFI accuracy (81.33% vs. 34.67-76.00%).
- **Human evaluation validation**: The human evaluation (Table 3) with 14 evaluators and high Cronbach's alpha values (0.825, 0.810) provides strong evidence that the GS and AE components produce reasonable and reliable attribute extraction.

## Weaknesses
### Major
- **Limited novelty of individual components**: While the combination is novel, each component (adaptive chunking, guided retrieval, attribute extraction) builds on existing techniques. ACTS is essentially adaptive chunking with hierarchical context, GS is a filtering mechanism using LLM judgments, and AE extracts two specific attributes. The paper would benefit from clearer articulation of what is fundamentally new versus an engineering integration.
- **Insufficient ablation studies**: The paper lacks a systematic ablation study that isolates the contribution of each component (ACTS, GS, AE). Table 2 shows ACTS vs. other chunking methods, but there is no experiment showing, for example, "ACTS only" vs. "ACTS + GS" vs. "ACTS + GS + AE" on the main evaluation tasks. This makes it difficult to attribute improvements to specific components.
- **Limited baseline diversity for the core RAG comparison**: The main comparison (Table 4) uses only three RAG baselines (Naive RAG, CRAG, LightRAG). Given that the paper claims to address fundamental RAG limitations for role-playing, comparisons with more recent or specialized RAG methods (e.g., Self-RAG, Corrective RAG, or other adaptive retrieval methods) would strengthen the claims.

### Minor
- **Dataset scope**: CharacterRAG contains only 15 characters from a single cultural context (Korean wiki data), and all characters appear to be from anime/manga. This limits generalizability claims about the framework's effectiveness across diverse character types and cultural backgrounds.
- **Computational cost of GS**: The Guided Selection component requires iterative LLM calls (up to N=30 iterations) to evaluate each chunk, which could be computationally expensive. The paper does not discuss runtime or cost comparisons with baselines.
- **The MBTI/BFI evaluation methodology**: While creative, using psychological tests to evaluate RPAs has inherent limitations—characters are fictional constructs, and their "ground truth" personality types come from crowd-sourced votes (personality-database.com), which may not be reliable or consistent.

### Trivial
- The paper mentions "15 distinct fictional characters" but the table in Figure 2 shows 15 characters with some names that appear to be OCR errors (e.g., "Sanpō", "Tsuzaki", "Aoi Fuyuki", "Chika Kadobayashi", "Maki Hashizaki", "Suzuhito", "Shinobu", "Enma Eto").

## Nice-to-Haves
- An analysis of when GS fails (i.e., when the slot remains empty and falls back to top-K chunks) would provide insight into the method's limitations.
- Discussion of how the framework handles characters with very different persona document lengths or structures would be valuable.
- A comparison with fine-tuning-based RPAs (even if the paper focuses on training-free methods) would help contextualize the trade-offs.

## Novel Insights
None beyond the paper's own contributions. The key insight—that adaptive chunking with hierarchical context and attribute extraction can improve RAG-based role-playing for out-of-knowledge queries—is well-demonstrated but does not reveal a fundamentally new principle beyond the specific technical contributions.

## Suggestions
- Add a full ablation study showing the contribution of each component (ACTS, GS, AE) on the main evaluation metrics (MBTI accuracy, BFI accuracy, CharacterRAG accuracy).
- Include runtime/computational cost comparisons to help practitioners understand the trade-offs of the proposed method.
- Expand the baseline set to include more recent RAG variants (e.g., Self-RAG, Corrective RAG) to better contextualize the improvements.

## Score and Decision
The paper addresses a well-motivated problem with a sound technical approach and strong empirical validation. The main limitations are the lack of ablation studies and the somewhat incremental nature of the individual components. However, the overall contribution—a practical, training-free framework that demonstrably improves RAG-based role-playing—is valuable to the community.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>