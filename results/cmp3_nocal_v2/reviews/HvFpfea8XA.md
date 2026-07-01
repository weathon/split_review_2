## Summary

This paper proposes AMADEUS, a training-free RAG framework for role-playing agents, consisting of three components: Adaptive Context-aware Text Splitter (ACTS), Guided Selection (GS), and Attribute Extractor (AE). It also introduces CharacterRAG, a manually constructed dataset with persona documents for 15 fictional characters (976K characters) and 450 QA pairs. The paper evaluates AMADEUS on in-knowledge QA and out-of-knowledge personality inference (MBTI/BFI) across multiple LLMs.

## Strengths

1. **CharacterRAG dataset is a concrete and carefully constructed resource.** The methodology — manually removing extraneous information and writing persona documents from the character's perspective (Section 2.1) — addresses a genuine gap in existing role-playing datasets. At 976K characters across 15 characters with 450 manually constructed QA pairs and persona lengths ranging from 32K to 145K characters, it provides a meaningful testbed for RAG-based role-playing that did not previously exist.

2. **Human evaluation of the GS+AE pipeline provides real evidence of reliability.** The paper evaluates attribute extraction quality with 14 human evaluators scoring 60 samples each, reporting Cronbach's alpha values of 0.825 (BFI) and 0.810 (MBTI), both exceeding the 0.8 threshold for high internal consistency (Table 3). This grounds the claim that the attribute extraction pipeline produces reasonable outputs in human judgment.

3. **The paper correctly identifies a genuine gap.** Existing RAG methods for role-playing use uniform chunking strategies that do not account for the hierarchical, narrative structure of persona documents (Section 4.2). The observation that standard RAG produces uninformative responses when questions exceed a character's explicit knowledge is a well-motivated problem.

## Weaknesses

### Fatal
None.

### Major

1. **The LLM used to compute ACC, ACC_L, and HS is never specified.** The paper states "We design three LLM-based metrics" (line 295) but never reveals which LLM serves as the evaluator. If it is GPT-4.1 — the same model used to implement GS and AE and one of the generation backbones — the evaluation suffers from potential self-enhancement bias: the judge may prefer responses that match its own reasoning patterns. If it is a different model, the paper must say so. This omission makes the headline quantitative results in Tables 4 and 5 impossible to interpret rigorously as presented.

2. **No ablation study isolating the three components.** AMADEUS = ACTS + GS + AE, but the paper never evaluates the progression: Naive RAG → +ACTS → +ACTS+GS → +ACTS+GS+AE on any role-playing task. Table 2 evaluates ACTS against other chunkers on similarity scores (a proxy metric), and Table 4 compares full AMADEUS against baselines. Without an ablation, it is impossible to determine which component drives the gains, or whether the full pipeline improves over ACTS alone. This is the most basic experimental design question for a multi-component system.

3. **MBTI/BFI accuracy results (the strongest evidence for the out-of-knowledge claim) are only reported under GPT-4.1 as both the generation backbone and the model implementing GS/AE.** Table 1's caption explicitly states "The experiments are conducted using GPT-4.1 setting." While Figure 5 does report MBTI/BFI *hallucination scores* on Gemma3-27B and Qwen3-32B, the accuracy/type-prediction results — which are the paper's headline evidence for maintaining personality consistency "even when responding to queries beyond explicit knowledge" — are not replicated on any other LLM. This creates a confound: it is unclear whether the advantage reflects genuinely better retrieval and attribute extraction, or GPT-4.1's ability to better follow its own sophisticated prompt chain.

4. **The procedure for converting character responses into predicted MBTI/BFI types is not described.** The paper mentions "interview-based assessments" (line 252) and compares against ground truth from Personality-Database.com, but does not specify how the raw responses are aggregated or mapped to MBTI/BFI type labels. This is a reproducibility gap for the out-of-knowledge evaluation.

### Minor

5. **Gains on the in-knowledge task (CharacterRAG QA) are modest.** AMADEUS improves ACC over the strongest baseline by +1.34 pp (GPT-4.1), +1.56 pp (Gemma3-27B), and +0.45 pp (Qwen3-32B) in Table 4. These margins are small and are reported without any measure of variance, confidence intervals, or statistical significance. The jump from "w/o RAG" to "Naive RAG" (~40 pp) dwarfs the jump from Naive RAG to AMADEUS (~1 pp). The paper frames this as a major improvement, but the evidence shows that Naive RAG already handles most in-knowledge questions well.

6. **The MBTI/BFI ground truth is inherently noisy.** The ground-truth personality types come from "thousands of actual participants' votes" on Personality-Database.com (line 252). Fictional characters do not have ground-truth personality types; this is fan consensus, not a validated psychometric assessment. While this follows prior work conventions (Wang et al. 2024b, Park et al. 2025), the reported "accuracy" of 85% must be interpreted with this caveat.

7. **The Guided Selection component's cost is not discussed.** The GS loop (Algorithm 1) makes up to 30 LLM calls per query (N=30), plus the attribute extraction call and the final generation call, compared to 1 retrieval + 1 generation for Naive RAG. A ~30× increase in LLM calls for a ~1% ACC gain on the in-knowledge task needs justification, particularly for a method described as "training-free" but computationally expensive at inference time.

### Trivial

8. **The φ function in Equation 4 is described only as a "length-calculating function."** The surrounding text (line 128) clarifies that it computes the maximum paragraph length, but the notation itself is underspecified and could be tightened.

## Nice-to-Haves

- An ablation study (Naive RAG → +ACTS → +ACTS+GS → +ACTS+GS+AE) on both the in-knowledge and out-of-knowledge tasks would greatly strengthen the paper.
- Specifying the evaluation LLM, and ideally using a different model than the GS/AE implementation model, would remove the evaluator confound.
- MBTI/BFI type-prediction accuracy on at least one non-GPT-4.1 backbone would demonstrate generality.
- Reporting variance or significance tests for the small-margin improvements in Table 4 would help the reader assess whether they are meaningful.
- A brief cost or latency analysis comparing the 30-iteration GS loop against standard RAG would contextualize the trade-off.

## Removed Points

Several points from the input review were removed for the following reasons:

- **LightRAG misconfiguration speculation** (the critic suggested LightRAG's poor performance "suggests possible misconfiguration"): This is speculative and not verifiable from the paper as written. The paper attributes LightRAG's low scores to known issues with graph-based methods for role-playing.
- **Figure 1 rendering complaint** (the critic notes "duplicated personality labels, suggesting a rendering issue"): The label duplication is a PDF parsing artifact, not an author error.
- **"No statistical significance or variance reported" elevated to fatal/major**: While notable, this concern is already covered under Weakness #5 (modest gains) and is better framed as a minor issue given that single-run evaluation on large-scale benchmarks is common practice in this sub-area.
- **Reproducibility complaint about prompts not being provided**: The paper states it will release code and supplementary materials (line 383). This is standard practice and not a mark against the paper as submitted.
- **Inter-annotator agreement for dataset cleaning**: The critic asks about this but the paper does not claim inter-annotator statistics; this is a reasonable request but not a required methodology for dataset construction, and is speculative.

## Novel Insights

None beyond the paper's own contributions. The review surfaces that the paper's strongest claimed results (MBTI/BFI accuracy, Table 1) and the evaluator for its main metrics (ACC/ACC_L/HS) both depend on unspecified or confounded LLM choices, which the paper's own narrative does not acknowledge as limitations. This is not a novel observation but a factual cross-check of the experimental design.

## Suggestions

1. Specify which LLM computes ACC, ACC_L, and HS. If it is GPT-4.1, replicate the evaluation with a different judge model (e.g., Gemini, Claude) to disentangle the evaluator confound.
2. Add an ablation study that progressively adds ACTS, GS, and AE to Naive RAG and reports results on both the in-knowledge and out-of-knowledge tasks.
3. Report MBTI/BFI type-prediction accuracy (not just HS) for at least one non-GPT-4.1 backbone, ideally using the same GS/AE pipeline implemented with GPT-4.1 but with a different generation model.
4. Include confidence intervals, statistical significance, or variance estimates for the quantitative comparisons in Tables 4 and 5.
5. Describe the MBTI/BFI type-inference procedure in detail (how are raw responses mapped to a predicted type?) to enable reproduction.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>