## Summary

This paper argues that biomolecular sequences should not be fed directly to Scientific LLMs (as tokens or embeddings) but instead should be processed through established bioinformatics tools (InterProScan, BLASTp, ProTrek) to generate structured textual context, which the LLM then reasons over. Through experiments across multiple Sci-LLMs and general-purpose LLMs, the authors show that context-only input dramatically outperforms sequence-only and sequence+context inputs, and that raw sequences act as informational noise that degrades performance even when context is available.

## Strengths

- **Comprehensive multi-model evaluation**: The paper tests its hypothesis across three specialized Sci-LLMs (Intern-S1, Evolla, NatureLM) and four general-purpose LLMs (DeepSeek-V3, Gemini2.5 Pro, GPT-5, Qwen3-235B), each under three input configurations (sequence-only, context-only, sequence+context). This breadth lends credibility to the core finding.

- **The sequence+context degradation finding is genuinely surprising and well-documented**: Across all seven models evaluated, adding raw sequence to context consistently degrades performance (e.g., Intern-S1: 86.15→84.03, Evolla: 74.02→70.53, NatureLM: 39.50→38.86). This is a striking empirical finding that warrants careful discussion.

- **Temporal robustness analysis (Section 5.4)**: Analyzing performance as a function of a protein's first publication year provides valuable insight into generalization and training data contamination. The steep degradation for Evolla versus the graceful degradation for the context approach is informative.

- **Wet-lab validation on truly unpublished sequences (Section 5.6)**: Testing on sequences absent from major databases provides strong evidence for real-world applicability and helps address concerns about test set leakage.

- **Computational cost analysis**: The paper provides a practical comparison showing the context approach is substantially cheaper and faster than end-to-end specialized models (Table 2), which is valuable for practitioners.

## Weaknesses

### Fatal

None.

### Major

- **Information leakage / fairness of comparison is the central concern**: The comparison is fundamentally asymmetric in a way the paper does not fully address. The "context-only" approach provides the LLM with domain-derived functional annotations (GO terms from homologs, Pfam domain descriptions) that are extremely close proxies for the ground-truth answers. The prompt template essentially asks "What is the function?" while providing "Here are the GO terms associated with homologs." This is far closer to information retrieval than reasoning. The sequence-only models, by contrast, must extract all information from raw amino acid letters. The authors' anti-leakage arguments in Section 4 (intrinsic analysis, homology-based inference) are necessary but not sufficient—they explain *why* direct label leakage is avoided but do not address the structural advantage of providing near-answer-level textual evidence. The real question is not "can the LLM retrieve the right answer from structured context?" but "what does this tell us about Sci-LLM capabilities?" The comparison would be more informative if it included a retrieval baseline without LLM reasoning to disentangle the contributions.

- **Scope of claims vs. scope of evidence**: The paper's title and framing claim broad implications for "biomolecular understanding in Scientific LLMs," but the empirical evaluation covers only protein function, pathway, and subcellular localization QA tasks—essentially annotation retrieval. Many important biomolecular tasks (structure prediction, variant effect prediction, protein design, evolutionary analysis) are entirely omitted. The sweeping conclusion that Sci-LLMs should be "reframed not as sequence decoders, but as powerful reasoning engines over expert knowledge" is not warranted by this narrow evaluation scope. The paper's own limitation section acknowledges this but the framing does not appropriately temper the claims.

- **LLM-as-judge evaluation protocol**: Using a general-purpose LLM to score answers raises concerns of circularity and calibration. The evaluation metric "LLM-Score" is not validated against human annotations, and the judge model's biases could systematically favor longer, more information-rich context-derived answers over concise or differently phrased ones. Without inter-annotator agreement statistics or comparison with human evaluation, the reliability of these scores is uncertain.

### Minor

- **The benchmark dataset construction details are deferred to appendices**: The paper states that "a question was only included if its corresponding annotation field was explicitly present in the source database entry," but the test set size, filtering criteria, and diversity characteristics are not discussed in the main text. This makes it difficult to assess potential biases.

- **Context generation has implicit assumptions and costs**: The hierarchical fallback strategy (InterProScan → BLASTp → ProTrek) introduces its own failure modes. The paper acknowledges degradation for "truly novel orphan proteins" but does not quantify how frequently the fallback to ProTrek is triggered or how ProTrek's context quality compares to the primary tools.

- **Figure 6 caption says 5% accuracy for Evolla on Rhodopsin, but body text says 80%**: This appears contradictory (the figure shows 1 correct / 19 incorrect = 5%, while Section 5.6 states "Evolla attains a reasonable 80.0% accuracy on Rhodopsin"). This discrepancy needs clarification.

### Trivial

- The "paradigm" framing (sequence-as-language, sequence-as-modality, context-driven) is useful but could be more precisely mapped to existing terminology in the retrieval-augmented generation (RAG) literature, which the context-driven approach closely resembles.

## Nice-to-Haves

- A retrieval-only baseline (no LLM reasoning, just matching context to answers) would help disentangle whether the LLM is genuinely "reasoning" or simply performing high-quality retrieval.
- Evaluation on tasks beyond annotation retrieval (e.g., variant effect prediction, homology inference, or protein design instructions) would substantially strengthen the paper's broad claims.
- Human evaluation or validated automatic metrics would increase confidence in the reported scores.
- Analysis of when sequence information *does* help (the paper notes context-only wins but doesn't explore marginal cases or task types where sequence might be beneficial).

## Novel Insights

The paper's most genuinely novel finding is the consistent performance degradation when raw sequences are added to already-informative context—a result replicated across seven different models. This "sequence as noise" phenomenon, if it holds across a broader range of tasks and benchmarks, would be a significant observation for the field. The layer-wise analysis of Evolla's representational degradation through the alignment module (Section 5.3) also provides useful mechanistic insight into the semantic misalignment problem. However, the broader reframing of Sci-LLMs as "reasoning engines over expert knowledge" rather than sequence decoders is essentially a reformulation of retrieval-augmented generation applied to bioinformatics, and the paper would benefit from acknowledging this lineage.

## Suggestions

- Include a retrieval-only baseline that uses the same bioinformatics tools and context but maps annotations to answers without LLM reasoning, to quantify how much performance comes from retrieval versus reasoning.
- Expand evaluation to at least one task that requires genuine biological reasoning beyond annotation retrieval (e.g., predicting the effect of a mutation, inferring evolutionary relationships, or answering "why" questions about protein function).
- Resolve the Rhodopsin accuracy discrepancy between the body text (80%) and Figure 6 (5%) for Evolla.
- Validate the LLM-as-judge evaluation against a human-annotated subset to establish reliability.
- Explicitly discuss connections to retrieval-augmented generation (RAG) and position the contribution within that well-established framework rather than presenting it as entirely novel.

## Score and Decision

The paper presents an interesting and well-executed empirical finding—context-only outperforms both sequence-only and sequence+context across multiple models—and supports it with temporal analysis, efficiency comparisons, and wet-lab validation. However, the central comparison is asymmetric in ways the paper does not adequately address (context provides near-answer-level information while sequence models must reason from scratch), the evaluation tasks are limited to annotation retrieval despite broad claims, and the evaluation protocol lacks human validation. The results are thought-provoking but the conclusions drawn from them are overreaching relative to the evidence presented.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>