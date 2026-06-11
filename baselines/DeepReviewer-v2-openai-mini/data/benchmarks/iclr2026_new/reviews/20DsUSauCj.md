## Summary
# Final Review Report

## Summary

This paper presents a systematic framework for extracting "persona vectors" — linear directions in the activation space of LLMs that correspond to specific personality traits (evil, sycophancy, hallucination) — and demonstrates four applications: monitoring prompt-induced persona shifts via activation projection, detecting finetuning-induced shifts along these directions, a novel "preventative steering" method applied during finetuning to limit unwanted persona drift, and pre-finetuning data screening at dataset and sample levels. The extraction pipeline takes a natural-language trait description as input and produces a corresponding direction using contrastive LLM-generated artifacts.

**Core claims (C1-C4):**
- C1: An automated pipeline can extract trait-specific persona vectors from natural-language descriptions.
- C2: Finetuning-induced persona shifts strongly correlate with activation changes along corresponding persona vectors (r = 0.76–0.97).
- C3: Preventative steering (adding the persona vector during training) reduces unwanted persona drift while better preserving general capabilities than inference-time steering.
- C4: Training data projection differences predict post-finetuning trait expression, enabling data screening.

The paper makes a genuine contribution to the alignment and representation engineering literature by connecting activation-based monitoring with practical safety interventions during training. However, several methodological concerns (reliance on LLM-based evaluation, limited sensitivity to subtle shifts, confounded correlation metrics) and the significant overlap of the extraction pipeline with prior work (Wu et al., 2025) temper the overall impact. The preventative steering and data screening innovations are the strongest contributions but require further validation with independent evaluation protocols.

## Strengths
**S1 — Practical relevance and timely application.** The paper addresses a concrete and urgent problem: unexpected persona shifts in deployed LLMs. The choice of three traits with documented real-world incidents (evil, sycophancy, hallucination) grounds the work in practical safety concerns rather than toy settings. The fact-acquisition case study (Section 5.2) is particularly well-motivated, as it mirrors a real scenario where finetuning on new knowledge introduces hallucination side-effects. This practical orientation increases the paper's potential impact.

**S2 — Preventative steering is a clear methodological contribution.** The idea of adding the persona vector *during* training (rather than subtracting it at inference) to proactively counteract unwanted drift is conceptually novel and well-motivated. The empirical comparison showing that it better preserves MMLU and new-fact accuracy than inference-time steering (Figures 5 and 6) provides evidence for its practical advantage. This is likely the paper's strongest original contribution, and the comparison with CAFT (Casademunt et al., 2025) helps establish its positioning.

**S3 — Pre-finetuning data screening is a compelling extension.** Using projection differences to predict post-finetuning behavior *before* training occurs (Section 6, Figure 7) is a practically valuable capability. The observation that this method works at both dataset and sample levels, and can detect samples that escape LLM-based filters (Section 6.2, Appendix N), demonstrates a real advantage over existing approaches. The correlation values (r > 0.88 across settings) are impressive, though they come with caveats discussed below.

**S4 — Generally clear experimental methodology.** The paper reports correlations with p-values across multiple datasets and two model families (Qwen2.5-7B, Llama-3.1-8B). The construction of multiple dataset types (trait-eliciting and EM-like) with severity levels (Normal/I/II) is thoughtful. The inclusion of cross-trait baselines (Appendix I.2) and comparison with alternative methods (CAFT, regularization) strengthens the empirical evaluation.

**S5 — Automated extraction pipeline is useful but incremental.** While the pipeline's novelty is limited relative to Wu et al. (2025), its automation and generality (any trait from a natural-language description) are practically useful. The ability to generate evaluation questions and rubrics automatically makes the method more accessible to non-specialist practitioners.

## Weaknesses
**W1 — Novelty of extraction pipeline is overstated; insufficient differentiation from prior work. [Severity: Major]**

Evidence: Page 1, Section 1: "In this work, we systematize the process of identifying such directions, which we refer to as persona vectors." The footnote on Page 2 acknowledges that Wu et al. (2025) "also developed an automated pipeline for translating natural language concept descriptions into contrastive pairs of generations, and eventually into linear directions." The paper does not clearly articulate what is added beyond Wu et al.'s pipeline.

Impact: Readers familiar with the activation steering literature will recognize that the core extraction technique (contrastive pairs → activation difference → linear direction) is well-established. The claimed "automated pipeline" contribution is therefore incremental, not foundational. This does not invalidate the paper, but it requires de-emphasizing the pipeline novelty and foregrounding the applications (preventative steering, data screening) which are genuinely new.

Recommendation: 
- Move the explicit comparison with Wu et al. (2025) to the main text (Section 2), clearly stating what is shared and what is added.
- Reorder the contribution list to put preventative steering first and the pipeline last.
- Use bounded language: "Building on prior concept-extraction methods, we develop an automated pipeline that extends them with [specific additions: response filtering, automated rubric generation, layer selection]."

**W2 — Core correlations may be inflated by shared measurement methodology. [Severity: Major]**

Evidence: Page 5, Section 4.2 and Figure 4. The finetuning shift (x-axis) is computed as projection onto the persona vector, which was itself extracted using the same LLM judge that produces the trait expression score (y-axis). The correlation thus has a shared-method confound. Similarly, the projection difference (Section 6.1) uses the same persona vector and the same LLM judge.

Impact: The reported correlations (r = 0.76–0.97 for finetuning shift, r = 0.88–0.95 for projection difference) may be inflated by this shared methodology. If the LLM judge has a systematic bias (e.g., it interprets certain activation patterns as trait-relevant due to its own training), both x and y measures would reflect that bias. The cross-trait baselines (r = 0.34–0.86) are provided, but these are also computed using the same judge, so they don't fully resolve the concern.

Recommendation:
1. Add an independent evaluation for at least one trait using established behavioral benchmarks (e.g., TruthfulQA for hallucination).
2. For the data screening results (Figure 7), report the correlation when the y-axis uses an independently-validated trait measure rather than the LLM judge.
3. Explicitly discuss this shared-method confound in a limitations paragraph.

**W3 — Monitoring capability is limited to explicit prompt shifts, not subtle deployment drift. [Severity: Major]**

Evidence: Page 3-4, Section 3.3: "These correlations arise primarily from distinguishing between different prompt types... with more modest correlations when controlling for prompt type (Appendix E.2). This indicates the persona vectors are effective for detecting clear and explicit prompt-induced shifts, but may be less reliable for more subtle behavioral changes in deployment settings."

Impact: The abstract claims persona vectors "can be used to monitor fluctuations in the Assistant's personality at deployment time," which implies sensitivity to subtle changes. The actual evidence shows they mainly distinguish between explicitly different system prompts. Real-world harmful persona shifts are often gradual and contextual (e.g., slow sycophancy creep across conversations), and the current method would likely miss these.

Recommendation:
1. Qualify the monitoring claim in the abstract: "can monitor explicit prompt-induced persona shifts."
2. Add the within-prompt-type correlation to the main text to give readers an accurate picture of the method's sensitivity.
3. Discuss what types of deployment monitoring are and are not supported (e.g., detecting malicious system prompt changes is supported; detecting gradual conversation-level drift is not).

**W4 — Duplicate paragraph in Section 5.1 indicates editorial incompleteness. [Severity: Major]**

Evidence: Page 6, lines 106 and 107. The exact same comparison (preventative steering vs. CAFT vs. regularization) appears twice with slightly different wording. This is clearly an editing artifact.

Impact: This error reduces confidence in the manuscript's preparation quality. For a paper making strong empirical claims, such oversights may lead reviewers to question the rigor of the underlying experiments.

Recommendation: Delete the first occurrence (line 106) and keep the more complete second version (line 107). Add a sentence about the prompt-based baselines and domain-specific skills from the second version.

**W5 — Heavy reliance on LLM-based evaluation without sufficient human validation reported in main text. [Severity: Major]**

Evidence: Page 2, Section 2.1: "Since our results rely heavily on this LLM-based evaluation, we validate it by checking agreement between our LLM judge and human evaluators... (see Appendix D)." The main text does not report the agreement level. Appendix D details are not available in the reviewed manuscript (the appendix was removed).

Impact: The entire empirical chain — from persona vector extraction through steering effectiveness to finetuning shift correlations — depends on a single LLM judge (GPT-4.1-mini) assigning trait expression scores. Without knowing the human-judge agreement, readers cannot assess whether the method measures actual personality traits or artifacts of the judge model. The filtering threshold (score > 50) is presented without sensitivity analysis.

Recommendation:
1. Report the human-judge agreement metric and value in the main text, not only in the appendix.
2. Add a robustness check: compare persona vectors extracted using different judge models (e.g., Claude, GPT-4).
3. Test different filtering thresholds (e.g., 40/60, 30/70) and report whether the main results change.

**W6 — Finetuning protocol details are insufficient for reproducibility. [Severity: Minor]**

Evidence: Page 4, Section 4.1. The dataset construction is described, but key details are missing: number of samples per dataset, training hyperparameters (learning rate, epochs, LoRA rank, batch size), number of seeds, and whether full finetuning or LoRA was used.

Impact: Without these details, the finetuning experiments cannot be reproduced or compared with future work. The magnitude of persona shift is known to depend heavily on training hyperparameters.

Recommendation: Add a table summarizing dataset sizes and training hyperparameters in the main text or a dedicated appendix section.

**W7 — Conclusion is too brief, defers limitations to appendix. [Severity: Minor]**

Evidence: Page 9, Conclusion (lines 148-150). Two sentences summarize the work, then "Our work also has several limitations, which we discuss in Appendix B." The appendix is not available in the reviewed manuscript.

Impact: A strong conclusion should synthesize validated findings and bounded limitations in the main text. Deferring limitations entirely to an appendix that may not be read by all reviewers/practitioners weakens the paper's scientific communication.

Recommendation: Add a main-text limitations paragraph covering: (1) reliance on LLM judge, (2) limited sensitivity to subtle shifts, (3) two-model validation only, (4) synthetic dataset constraints, and (5) the shared-method confound in correlation measures.

## Score
**Final Score: 6.5/10**

**Rationale:** The paper addresses a practically important problem (monitoring and controlling LLM persona shifts) with a systematic framework. The preventative steering method (adding persona vectors during training) and pre-finetuning data screening via projection differences are genuine contributions with practical value. However, several factors prevent a higher rating:

1. **Novelty concern (primary):** The core extraction pipeline has substantial overlap with Wu et al. (2025), and this is only acknowledged in a footnote. The paper's stated contribution of "systematizing" the process is not sufficiently differentiated from prior work. The strongest novel contributions (preventative steering, data screening) are valuable but are built on this incremental foundation.

2. **Validity concern (primary):** The reported correlations (r = 0.76–0.97) likely contain shared-method inflation since both the x-axis (finetuning shift / projection difference) and y-axis (trait expression score) derive from the same LLM judge and persona vector. The heavy reliance on a single LLM judge (GPT-4.1-mini) without main-text human validation further weakens confidence.

3. **Claim-precision gap:** The abstract and introduction claim "monitoring" capability broadly, but the method primarily detects coarse prompt-type differences. Subtle deployment drift — the more dangerous scenario — is not reliably captured.

4. **Presentation:** The duplicate paragraph in Section 5.1 and the deferral of all limitations to an appendix (removed from review) reduce confidence.

**What would raise the score:** (i) Independent validation of trait expression using established behavioral benchmarks (e.g., TruthfulQA) to decouple the shared-method confound; (ii) Main-text reporting of human-judge agreement and within-prompt-type correlations; (iii) Clear differentiation from Wu et al. (2025) in the main text, with the pipeline novelty downgraded and applications foregrounded; (iv) A substantive main-text limitations paragraph. With these fixes, the paper could be a strong 7.5–8/10 submission.

---

**External Literature Note:** Novelty and comparison conclusions in this review are deferred due to Retrieval-Disabled Mode (paper_search unavailable). A comprehensive literature verification should be conducted before final assessment of the paper's novelty relative to the full body of activation steering and representation engineering literature. The strong overlap acknowledged with Wu et al. (2025) is based on the paper's own footnote; a full literature search may reveal additional overlapping works that could further affect the novelty assessment.