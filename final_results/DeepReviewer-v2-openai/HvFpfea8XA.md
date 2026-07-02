## Summary
# Final Review Report

## Summary

This paper presents AMADEUS, a training-free framework for retrieval-augmented generation (RAG) based role-playing agents (RPAs), along with CharacterRAG, a manually constructed dataset of 15 fictional characters (976K written characters, 450 QA pairs). AMADEUS consists of three components: Adaptive Context-aware Text Splitter (ACTS), which uses adaptive chunk sizing with hierarchical context; Guided Selection (GS), which uses up to 30 LLM calls per query to select chunks from which character attributes can be inferred; and Attribute Extractor (AE), which extracts belief/value and psychological trait attributes from selected chunks.

The paper addresses a genuine and under-explored problem — maintaining persona consistency when RPAs receive queries outside a character's documented knowledge. The CharacterRAG dataset is a useful resource for the community. However, the experimental evaluation has several critical weaknesses: (1) AMADEUS achieves only marginal improvement over Naive RAG (+1.34% ACC) without statistical significance testing; (2) no comparison against fine-tuned RPAs or full-context prompting baselines; (3) LLM-based evaluation metrics are not validated against human judgments; (4) ground-truth personality labels come from crowd-sourced voting rather than verified annotation. Additional methodological concerns include the high computational cost of GS (up to 30 LLM calls/query), arbitrary design choices in ACTS (max paragraph length as chunk size), and insufficient justification for AE's 2-attribute focus. These weaknesses substantially limit the strength of the claimed contributions.

## Strengths
**1. Well-motivated problem definition.** The paper identifies a genuine and practical gap: existing RPA methods assume personas are short and knowledge-complete, while real-world role-playing interactions frequently involve out-of-knowledge queries. The observation that Naive RAG overuses irrelevant chunks under such conditions (Figure 1) is a useful empirical finding that motivates the work.

**2. CharacterRAG dataset fills a gap.** The manual construction of persona documents from the character's perspective (removing extradiegetic information) is a thoughtful design choice. At 976K written characters and 450 QA pairs across 15 characters, CharacterRAG is the first dataset specifically designed for evaluating RAG-based RPAs with out-of-knowledge queries. The attribute taxonomy (6 attributes) provides a structured evaluation framework that can be extended by future work.

**3. Comprehensive evaluation scope.** The experiments span 3 LLMs (GPT-4.1, Gemma3-27B, Qwen3-32B), 3 embedding models, 4 RAG methods, and two psychological inventories (MBTI, BFI). This breadth provides a useful empirical landscape of RAG-based RPA performance. The finding that graph-based RAG (LightRAG) and web-search RAG (CRAG) are poorly suited for role-playing is a practically relevant insight.

**4. Training-free approach has practical appeal.** By avoiding fine-tuning, AMADEUS can be applied to new characters without per-character model updates. This is a meaningful advantage for deployment scenarios requiring rapid character switching or where computational resources for fine-tuning are unavailable.

## Weaknesses
### W1. Marginal improvement over Naive RAG without statistical significance
The central claim is that AMADEUS "significantly enhances persona consistency." However, on the primary CharacterRAG benchmark (Table 4, GPT-4.1), AMADEUS achieves 92.67% ACC vs 91.33% for Naive RAG — a mere +1.34% improvement. The ACC_L scores are virtually identical (9.26 vs 9.23). No variance estimates, confidence intervals, or statistical significance tests are reported across any experiment. Without multi-seed runs or significance testing, readers cannot determine whether this improvement is reliable or within noise range. The hallucination score (HS) shows a more meaningful reduction (2.89 vs 3.13), but this improvement is not decomposed across components.
- **Severity:** Critical. This weakens the core contribution claim.
- **Required action:** (a) Report results over ≥3 random seeds with mean±std. (b) Add bootstrapped confidence intervals or paired significance tests for AMADEUS vs Naive RAG. (c) Qualify claims: replace "significantly enhances" with "marginally improves" unless testing supports the stronger wording.

### W2. Missing critical baselines — no comparison against fine-tuned RPAs or full-context prompting
The paper compares only against RAG methods (Naive RAG, CRAG, LightRAG). The most relevant baselines for RPAs are conspicuously absent: (a) fine-tuned RPAs (Park et al., 2025; Lu et al., 2024), which represent the dominant approach in the field, and (b) a "full-context prompt" baseline where the entire persona is included in the LLM prompt without RAG. Without these, the practical significance of AMADEUS is unclear — if fine-tuned methods achieve 95%+ ACC, AMADEUS's 92.67% is not competitive; if they achieve lower, the training-free advantage is meaningful.
- **Severity:** Critical. Without these baselines, the contribution's value cannot be properly assessed.
- **Required action:** Add at least one fine-tuned RPA baseline and a full-context prompt baseline to Table 4.

### W3. Evaluation metrics lack human validation and suffer from confound
Three LLM-based metrics (ACC, ACC_L, HS) are used as primary evaluation instruments, but: (a) No human correlation study is reported for these metrics on the CharacterRAG QA task. The human evaluation (Table 3) only validates the GS+AE component (attribute extraction), not the main RPA performance. (b) The same LLM (GPT-4.1) is used for generation, GS selection, AE extraction, and presumably evaluation — creating a systematic self-consistency bias. (c) No inter-rater reliability is reported for the LLM-as-judge metrics.
- **Severity:** Major. The entire ranking of methods depends on these unvalidated metrics.
- **Required action:** (a) Correlate LLM-based scores with human judgments on a held-out subset. (b) Use a different LLM for evaluation than for generation. (c) Report test-retest reliability across multiple evaluation runs.

### W4. Ground-truth personality labels are crowd-sourced and unverified
The MBTI and BFI evaluation (Table 1) uses ground-truth labels from personality-database.com, a crowd-sourced voting platform. Character personality interpretation is inherently subjective — different viewers may interpret the same character differently. The paper reports 85.00% MBTI accuracy, but if the ground truth is noisy, this number may reflect agreement with popular consensus rather than genuine persona fidelity.
- **Severity:** Major. The paper's secondary contribution (maintaining persona consistency for out-of-knowledge queries) rests heavily on this evaluation.
- **Required action:** (a) Add a caveat about ground-truth reliability. (b) Report vote counts per character to indicate label confidence. (c) Consider expert annotation for a subset of characters as validation.

### W5. High computational cost of Guided Selection (GS) without cost-benefit analysis
GS (Algorithm 1) makes up to N=30 LLM calls per query just for chunk selection, yet only outputs M=2 chunks. The paper does not report: (a) the average number of LLM calls actually used per query, (b) the percentage of queries where the fallback mechanism (Top-K+1) is triggered, (c) end-to-end latency compared to baselines, or (d) cost per query. For a method targeting practical RPAs, this is a significant omission.
- **Severity:** Major. The practical deployability of AMADEUS depends on this cost being justified.
- **Required action:** Report average LLM calls per query, fallback rate, and a latency/cost comparison table. Add an ablation with N=5, N=10, N=20 to show the cost-accuracy trade-off.

### W6. ACTS design choices are arbitrary and under-justified
The Adaptive Context-aware Text Splitter uses the maximum paragraph length as chunk size ($l_{max} = \max(p_i)$) and overlap as $l_{max}/2$. These choices are critical to the method but are justified only by a vague claim about "minimizing information loss." Using max rather than mean, median, or a percentile is not justified. The overlap coefficient ($\alpha=2$) is validated using log-density ridgelines under normality assumptions (Figure 4), but this indirect validation does not directly measure retrieval quality improvements. Additionally, the length-calculating function $\varphi$ is never specified (characters? words? tokens?).
- **Severity:** Major. ACTS is a core contribution; its design must be reproducible and principled.
- **Required action:** (a) Specify $\varphi$ (recommend character count for language-agnostic reproducibility). (b) Justify max vs alternative statistics with data distribution analysis. (c) Replace the indirect overlap validation with direct retrieval quality metrics (e.g., recall@K).

### W7. AE covers only 2 of 6 attributes with circular justification
The Attribute Extractor selects only "Belief and Value" and "Psychological Traits" from the 6 defined attributes, with the footnote claiming these "directly influence behavior." This is circular: all six attributes influence behavior. No ablation tests whether using 2 vs 4 vs 6 attributes changes performance. The extraction method itself (prompt template, LLM call format) is not disclosed.
- **Severity:** Major. Without ablation or justification, readers cannot attribute gains to AE rather than other components.
- **Required action:** (a) Add an ablation: AE with 2, 4, and 6 attributes. (b) Provide the exact AE prompt template. (c) Provide empirical justification for the 2-attribute choice.

### W8. No component ablation for the full system
AMADEUS has three components (ACTS, GS, AE), but no ablation study isolates their contributions. Readers cannot determine which component drives the observed improvement. The comparison of ACTS vs ATS in Table 2 (similarity scores) is informative but does not directly measure end-to-end RPA performance.
- **Severity:** Major. The paper cannot claim that all three components are necessary without ablation.
- **Required action:** Add an ablation study: (a) Naive RAG, (b) +ACTS, (c) +ACTS+GS, (d) +ACTS+GS+AE (full AMADEUS), reporting ACC, ACC_L, and HS.

### W9. CharacterRAG dataset limitations bound generalizability
The dataset has several constraints that limit the scope of conclusions: (a) Single source (Namuwiki, Korean-language). (b) Only 15 characters from Japanese anime/manga (narrow cultural/genre diversity). (c) No inter-annotator agreement statistics. (d) Only 30 QA pairs per character — modest for rigorous evaluation.
- **Severity:** Moderate. While the dataset is a useful contribution, these limitations must be acknowledged.
- **Required action:** Add inter-annotator agreement metrics, acknowledge limitations in the paper, and discuss plans for multilingual/cross-genre expansion.

### W10. Conclusion lacks limitations and introduces unsupported claims
The conclusion claims "robust and consistent simulation" without empirical support for robustness (no stress tests, no OOD evaluation, no perturbation analysis). No limitations are acknowledged. The closing statement about future prospects is vague and promotional.
- **Severity:** Moderate. The conclusion should reflect what was actually demonstrated, not aspirational claims.
- **Required action:** Restructure conclusion into: validated findings → bounded limitations → specific next steps.

## Score
**Final Score: 5/10**

**Scoring rationale:** This score prioritizes novelty + research value as primary dimensions, consistent with the review guidelines. The paper addresses a genuine and under-explored problem (RAG-based RPAs with out-of-knowledge queries) and contributes a useful dataset (CharacterRAG). However, several critical weaknesses substantially limit confidence in the claimed contributions:

- **Novelty assessment (deferred):** Due to Retrieval-Disabled Mode in this run, external literature verification was unavailable. The paper's core novelty (training-free adaptive chunking + guided selection for RPAs) cannot be fully verified against the state of the art without external comparison. The marginal improvement over Naive RAG (W1) raises questions about how much practical novelty the method provides over standard RAG.

- **Research value: Moderate.** The CharacterRAG dataset and the empirical findings (e.g., graph-based RAG unsuitability for RPAs, LLM thinking mode ineffectiveness) are useful contributions. However, the AMADEUS framework's benefits over Naive RAG are incremental, and the missing baselines against fine-tuned RPAs (W2) make it difficult to assess the framework's practical value.

- **Validity risk: High.** The evaluation is undermined by unvalidated LLM-based metrics (W3), crowd-sourced ground truth (W4), and the absence of statistical significance testing (W1). These issues mean the reported performance numbers may not be reliable indicators of true persona consistency.

- **Reproducibility: Moderate.** Key design choices (ACTS chunking, AE extraction) are underspecified, and the LLM-as-judge metrics are not fully described. The promise of code/dataset release will partially address this.

The score of 5/10 reflects a paper with a worthwhile motivation and useful resources, but whose central methodological claims are not yet convincingly supported by the evidence presented. The identified issues are fixable with additional experiments and analysis, particularly adding proper baselines, statistical testing, evaluation validation, and component ablations.