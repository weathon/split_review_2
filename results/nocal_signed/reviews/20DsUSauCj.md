## Summary

This paper presents an automated pipeline for extracting linear "persona vectors" from LLM activation spaces given only a natural-language trait description. It demonstrates four applications: monitoring prompt-induced persona shifts, predicting finetuning-induced trait changes, a novel "preventative steering" method that proactively limits unwanted persona drift during training, and pre-finetuning data screening to flag problematic training samples. The method is validated across two open-source models (Qwen2.5-7B, Llama-3.1-8B) and multiple datasets for three traits (evil, sycophancy, hallucination).

## Strengths

- **Preventative steering is a genuinely novel and well-evaluated contribution (Section 5).** Steering *toward* an undesired trait during training, then removing the steering at inference, is counterintuitive and practically valuable. The fact-acquisition case study (Section 5.2, Figure 6) is particularly compelling: inference-time steering destroys MMLU and new-fact accuracy while preventative steering preserves them, reducing hallucinations to baseline without capability degradation. This is a clean, impactful result.

- **Pre-finetuning data screening (Section 6) is a practical tool with clear utility.** The projection difference metric is simple and interpretable. The finding that it identifies problematic samples that "escape LLM filters" (Appendix N) addresses a real deployment problem. Figure 8's histograms provide visually convincing separation between trait-inducing and control samples.

- **Strong, consistent correlational evidence across two models and multiple dataset types.** Figures 4 and 7 show r-values in the 0.76–0.97 range for Qwen2.5-7B and Llama-3.1-8B, for three distinct traits, with correlations holding across both intentionally trait-eliciting and "emergent misalignment-like" datasets spanning medical, code, math, and opinion domains.

- **Automated pipeline from natural language to activation vector (Section 2).** Prior activation-steering work required manual curation of contrastive data. Showing that a frontier LLM can generate the necessary artifacts (contrastive system prompts, evaluation questions, rubrics) from just a trait name and description lowers the practical barrier to applying the method, which is a real contribution.

- **Honest treatment of limitations in the monitoring section (Section 3.3).** The paper explicitly acknowledges that the high correlations (r=0.75–0.83) arise "primarily from distinguishing between different prompt types" and that controlling for prompt type yields "more modest correlations," noting the method "may be less reliable for more subtle behavioral changes in deployment settings." This self-critical transparency is commendable.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Reliance on a single LLM judge (GPT-4.1-mini) for both extraction filtering and evaluation.** The same model (GPT-4.1-mini) scores which responses to retain for extraction (Section 2.2: retaining responses where trait score > 50 for positive prompts) and then evaluates all downstream results (Sections 3–6). This creates a risk of circularity: the persona vectors may be learning to align with GPT-4.1-mini's internal labeling preferences rather than with objective behavioral properties. While the paper mentions human evaluator validation and external benchmark comparisons (Appendix D), the main text provides no quantitative agreement statistics. The concern is partially mitigated by the convincing qualitative examples (Figure 2), the convergent evidence from objective metrics in the fact-acquisition case study (New Facts Accuracy, MMLU in Figure 6), and the grounding of the data-screening method in model activations rather than LLM judgments — but including human-agreement numbers in the main text would substantially strengthen confidence.

- **Framing "propensity to hallucinate" as a personality trait parallel to "evil" and "sycophancy" is conceptually strained.** Evil and sycophancy are motivational/behavioral dispositions, while hallucination is fundamentally a capability failure (generating factually incorrect content). The methodology demonstrably works for all three — this is a valid empirical finding — but labeling all three uniformly as "persona traits" conflates qualitatively different phenomena. The paper would benefit from explicitly acknowledging this distinction rather than treating them as interchangeable.

- **The correlation evidence in Section 4 does not establish causation.** The question "Are behavioral shifts during finetuning mediated by persona vectors?" is investigated using correlational evidence alone: both the finetuning shift (projection of activation change onto a persona vector) and the trait expression score (LLM-judged behavioral measure) could be driven by a common third factor — the overall change in model representations induced by finetuning. The paper appropriately uses "predicts" in the main heading and provides separate causal evidence via steering interventions in Section 5, but the "mediated by" framing and the abstract's "underlying" slightly overstate what the correlational evidence alone supports.

- **Data-point independence in the correlation analyses (Figures 4 and 7) is not addressed.** Each figure contains multiple dataset variants (Normal, I, II) drawn from the same dataset families (Evil, Sycophancy, Hallucination, Medical, Code, GSM8K, MATH, Opinions). Within-family data points may not be independent observations, and within-family correlations could inflate the reported overall r-values. The paper should clarify whether points are treated as independent and ideally report within-dataset-type correlations.

- **No confidence intervals on correlation coefficients.** Figures 4 and 7 report r and p-values but no confidence intervals. Given the relatively small number of data points (~20–24 per plot), confidence intervals would help assess the precision of the estimates beyond the reported p-values.

### Trivial
None.

## Nice-to-Haves
- The marginal contribution relative to Wu et al. (2025), who also developed an automated pipeline from concept descriptions to linear directions, could be stated more sharply in the main text.
- The dependence on proprietary APIs (Claude 3.7 Sonnet for generation, GPT-4.1-mini for evaluation) could be discussed as a limitation, and exploring open-weight alternatives would strengthen reproducibility.
- A discussion of scaling behavior to larger models (>10B) would improve the paper's completeness.

## Removed Points
These points from the input review were removed with justification:
1. **"The section heading says 'mediated by'"** — The actual heading reads "ACTIVATION SHIFT ALONG PERSONA VECTOR PREDICTS TRAIT EXPRESSION"; the word "mediated" appears only in a rhetorical question in the body text. The reviewer's characterization is imprecise.
2. **"Wu et al. marginal contribution not sharply stated"** — A reasonable suggestion but not a weakness; moved to Nice-to-Haves.
3. **"Only small models tested"** — A scope observation, not a flaw. The paper does not claim scalability and both tested models are standard choices.
4. **"Dependence on proprietary APIs not discussed"** — A valid reproducibility note but the paper already discusses limitations (Appendix B, stripped by parser); moved to Nice-to-Haves.
5. **"Evaluate one key result with objective metric"** — The paper already does this (Figure 6 shows New Facts Accuracy and MMLU as objective metrics).
6. **"Circularity is a critical/fatal issue"** — Demoted from the reviewer's "Critical" to Minor because the paper (a) mentions human validation, (b) provides objective metrics in the fact-acquisition case study, (c) shows convincing qualitative examples, and (d) grounds part of the analysis (data screening) in model activations rather than LLM judgments.

## Novel Insights
Beyond the paper's own contributions, the review surfaces the observation that persona-vector-based data filtering and LLM-judge-based filtering appear to have complementary strengths for identifying problematic training data — an insight the authors partially address in Appendix M (stripped by parser) but could be elevated to the main text. Otherwise, no genuinely novel insight emerges beyond what the paper demonstrates.

## Suggestions
- Report human-evaluation agreement statistics (Cohen's κ or Pearson r) for the LLM judge in the main text, alongside the current brief mention.
- Add a brief discussion of data-point independence in the correlation analyses and report within-dataset-type correlations.
- Reframe the hallucination results to acknowledge the conceptual distinction from personality traits.
- Add confidence intervals to reported correlation coefficients.

## Score and Decision

This is a solid, well-executed paper with genuine contributions. The preventative steering method is the standout contribution — novel, counterintuitive, and convincingly demonstrated with practical impact (the fact-acquisition case study). The automated pipeline and data-screening tool are useful additions. The weaknesses are all minor and addressable: they concern framing, statistical presentation, and the depth of evaluation validation rather than any fundamental flaw. The balance of strengths strongly outweighs the weaknesses.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>