## Summary
This paper challenges the prevailing view that topical relevance is the primary driver of benign relearning (the phenomenon where forgotten information resurfaces after fine-tuning on benign data). Through controlled experiments on the TOFU benchmark and re-analyses of the BLUR benchmark, the authors demonstrate that syntactic similarity—surface-level structural overlap between forget and relearn sets—is a stronger and more consistent predictor of relearning. They propose "syntactic diversification," which paraphrases forget queries into diverse structures before unlearning, showing it suppresses benign relearning, accelerates forgetting, and improves the utility-robustness trade-off.

## Strengths
- **Well-motivated and clearly articulated core insight.** The paper provides a crisp, testable hypothesis: syntactic similarity drives benign relearning more than topical relevance. This is a meaningful reframing that shifts attention from content-level to structure-level analysis in unlearning robustness.

- **Careful experimental design with controlled comparisons.** The construction of topically relevant vs. syntactically similar relearn sets on TOFU (Section 5.2) is well-designed to isolate the variable of interest. The authors also provide a valid critique of BLUR's evaluation protocol (confounded dataset sizes and fixed-step evaluation), proposing a fairer max-over-steps comparison (Section 4, Figure 3).

- **Multiple complementary analyses supporting the core claim.** Beyond the main relearning experiments (Figure 4), the authors provide representation and gradient similarity analysis (Figure 5), a template vs. keyword loss ratio analysis (Figure 6) that explains *why* syntactic patterns are more vulnerable, and a revisit of BLUR's benchmarks with syntactic similarity measurements (Table 1). This triangulation strengthens the central thesis.

- **Practical and effective mitigation strategy.** Syntactic diversification is simple to implement (using LLM-based paraphrasing), demonstrates clear empirical benefits on TOFU (Figures 8–9, Table 2), and the authors show it addresses the root cause (loss ratio converging to 1, indicating balanced template/keyword suppression).

- **Broader implications are well-articulated.** The discussion in Section 8 on regulatory risks, safety training limitations, and LoRA-based relearning vulnerabilities adds practical value and raises important deployment considerations.

## Weaknesses
### Fatal
None.

### Major
- **Limited diversity of experimental settings.** The primary experimental evidence for the core syntactic similarity claim comes from the TOFU benchmark (synthetic fictitious author biographies with highly templated QA pairs). This is a setting where syntactic structure is particularly rigid and prominent by construction. The re-analysis of BLUR benchmarks (WMDP, WHP, RWKU) in Section 5.4 provides supporting evidence, but the syntactic diversification intervention (Section 7) is only evaluated on TOFU. The question of whether this finding and intervention generalizes to more naturalistic, less templated datasets (e.g., real copyrighted text, real personal data) remains substantially open. The paper acknowledges additional experiments in appendices, but the main body does not provide sufficient evidence of generalizability.

- **Single model evaluation for the main experiments.** The core TOFU experiments (Sections 5–7) use only Llama-2-7b-chat (with a brief mention of Phi in Appendix B.3). The degree to which the phenomenon is model-specific vs. general is not well-established in the main paper.

- **Syntactic diversification relies on GPT-4o for paraphrasing.** This creates a dependency on a commercial API, raises reproducibility concerns, and the quality/diversity of generated paraphrases could vary. The filtering procedure is deferred to the appendix, and a more rigorous analysis of how paraphrase quality and diversity affect the intervention's efficacy would strengthen the contribution.

### Minor
- **Levenshtein distance as the primary syntactic similarity metric.** While simple and interpretable, normalized Levenshtein distance captures character-level edit distance, which may not faithfully reflect structural/syntactic similarity in the linguistically meaningful sense (e.g., parse tree distance). The authors mention alternatives in Appendix I, but the main text could benefit from briefly discussing limitations of this choice.

- **The template vs. keyword analysis (Section 6) assumes a specific decomposition of answer tokens.** The categorization into template and keyword tokens, while illustrative, is applied to a single example and the loss ratio analysis does not fully demonstrate that this decomposition is robust across different queries or datasets.

- **Table 2 shows mixed results for World Facts.** While Real Authors and Retain set metrics improve, World Facts metrics are comparable or slightly worse (e.g., Probability and Truth Ratio decrease slightly). This nuance is worth acknowledging.

### Trivial
None.

## Nice-to-Haves
- An analysis of how the number of paraphrases per query in the diversified forget set affects the trade-off between unlearning efficacy and computational cost.
- Evaluation on more diverse unlearning benchmarks beyond TOFU, WMDP, WHP, and RWKU to strengthen generalizability claims.
- A comparison of syntactic diversification against other data augmentation strategies for unlearning (e.g., random perturbation, semantic paraphrasing without structural variation) to isolate the contribution of syntactic diversity specifically.

## Novel Insights
The paper's most novel insight is the decomposition of benign relearning into a syntactic vs. topical component, with controlled experiments showing that syntactic similarity is the dominant driver. The template vs. keyword loss ratio analysis provides a mechanistic explanation: unlearning disproportionately suppresses rigid syntactic patterns (template tokens) rather than the actual sensitive content (keyword tokens), and syntactically similar relearn data provides a shortcut to restore those suppressed templates, which in turn enables keyword recovery. This reframing—from content-level to structure-level vulnerability—is a genuinely useful conceptual contribution to the unlearning literature and suggests that prior work attributing relearning to topical relevance may have been confounded by correlated syntactic similarity.

## Suggestions
- Expand the syntactic diversification experiments to at least one additional benchmark (e.g., WMDP or RWKU) and a second model family beyond Llama-2 to demonstrate generalizability of the intervention.
- Include a brief ablation on the number of paraphrase variants per query to understand the sensitivity of the approach to this hyperparameter.
- Consider comparing against simpler diversification baselines (e.g., random word shuffling, synonym replacement) to establish that it is specifically syntactic variation rather than generic noise that drives the improvement.

## Score and Decision
This paper presents a clear, well-motivated hypothesis with strong experimental support on the TOFU benchmark and corroborating evidence from BLUR benchmarks. The core insight—syntactic similarity as a driver of benign relearning—is novel and practically important. The proposed mitigation is effective and well-analyzed. However, the generalizability concerns (single primary benchmark, single primary model, reliance on GPT-4o for the intervention) are significant for a contribution that claims broad importance. The paper is above the borderline but not yet at the level of a strong accept given the limited scope of the main experimental validation.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>