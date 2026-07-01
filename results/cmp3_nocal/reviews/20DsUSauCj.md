## Summary

This paper presents an automated pipeline for extracting "persona vectors"—linear directions in activation space corresponding to personality traits like evil, sycophancy, and hallucination—from natural-language descriptions. It then demonstrates several applications: monitoring prompt-induced and finetuning-induced persona shifts via activation projection, mitigating unwanted shifts through inference-time steering, proactively preventing shifts during finetuning via a novel "preventative steering" method (steering *toward* the undesirable trait during training), and pre-finetuning data screening using a projection-difference metric. Experiments across Qwen2.5-7B and Llama-3.1-8B show strong correlations between persona vector projections and behavioral changes, and that preventative steering preserves general capabilities better than inference-time steering.

## Strengths

1. **Genuinely automated pipeline (Section 2).** The system takes only a natural-language trait description and returns a persona vector, using Claude 3.7 Sonnet to generate contrastive system prompts, evaluation questions, and a rubric. This is a meaningful operational advance over prior work requiring hand-crafted contrastive pairs (e.g., Zou et al. 2025, Wu et al. 2025), enabling application to arbitrary traits with minimal human effort.

2. **Preventative steering is a novel and well-motivated intervention (Section 5).** Steering *toward* an undesirable persona direction during finetuning (rather than against it at inference) is counterintuitive and evidently effective. The fact-acquisition case study (Section 5.2, Figure 6) is the cleanest result: both methods reduce hallucinations to baseline, but inference-time steering degrades MMLU and new-fact accuracy substantially while preventative steering preserves both. This is a concrete, practically relevant finding.

3. **Pre-finetuning data screening (Section 6) is a natural extension with strong empirical support.** The projection-difference metric is well motivated, and the correlations in Figure 7 (r = 0.88–0.95, all p < 0.001) across both models and three traits are compelling. The sample-level detection (Figure 8) further demonstrates practical utility.

4. **Cross-trait and cross-model consistency.** The correlations in Figures 4 and 7 hold across two model families (Qwen2.5-7B, Llama-3.1-8B) and three distinct traits, with consistently high r values. The paper also honestly acknowledges when cross-trait correlations are non-trivial (Footnote 6, Appendix I.2) rather than sweeping them under the rug.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or uncertainty reported for any quantitative result.** The experimental section lacks standard deviations, confidence intervals, or error bars on all steering results (Figures 2, 5, 6) and all correlation estimates (Figures 3, 4, 7). Each point in the correlation plots represents one finetuned model checkpoint—one per dataset × severity level, with no replication. The steering plots show lines without any indication of run-to-run variability. This is a genuine evidential gap: without variance estimates, the reader cannot reliably assess whether the difference between inference-time and preventative steering (Figure 5) is statistically robust, whether the apparent MMLU preservation of preventative steering is within noise, or whether correlation coefficients of 0.88 vs 0.95 differ meaningfully. While single-seed finetuning is common in this subfield, the paper makes strong comparative claims that require stronger evidential support. **Impact:** Undermines confidence in the central quantitative comparison; fixable with multiple seeds and error bars.

2. **The comparison between preventative steering and inference-time steering is uncalibrated (Section 5).** Preventative steering adds the vector *during training* (changing weights through gradient descent), while inference-time steering subtracts the vector *at inference* (a purely activation-level intervention on a separately finetuned model). These operate through fundamentally different mechanisms, and the x-axis in Figures 5 and 6 is the same scalar α for both—but there is no guarantee that α=1.0 has the same effective strength in both settings. The paper's central claim that preventative steering "better preserves general capabilities" may well be true, but the evidence does not fully rule out the possibility that the comparison operates at different effective strengths of the two interventions. **Mitigating factor:** The fact-acquisition case study (Figure 6) shows the qualitative pattern holds across several α values, including small α where inference-time steering already degrades MMLU, and multi-layer steering (Appendix L.3) further corroborates the finding. Nevertheless, the main single-layer comparison remains ambiguous without explicit calibration or discussion.

### Minor

1. **LLM-as-judge validation details are deferred to the appendix.** The paper states that the judge (GPT-4.1-mini) is validated against human evaluators (Appendix D), but the main text does not report the agreement level (correlation or Cohen's κ) or discuss potential systematic biases. Since *every* quantitative result in the paper depends on this judge, a one-sentence summary of the validation in the main text would substantially increase reader confidence.

2. **Filtering statistics for persona vector extraction not reported (Section 2.2).** The pipeline retains responses with trait scores >50 for positive prompts and <50 for negative prompts, discarding refusals. The paper does not report what proportion of responses are filtered out. If a large fraction is discarded, the resulting contrastive set may be biased toward extreme cases, and the persona vectors may not capture more subtle manifestations of the trait.

3. **Mechanism of preventative steering is under-explained (Section 5.1).** The paper states that adding the persona vector "counteracts the finetuning objective's tendency to push the model along that direction," but this is an intuitive characterization without mechanistic verification. Alternative hypotheses (e.g., that it changes how the model memorizes training data) are not explored. This does not invalidate the empirical results, but deeper analysis would strengthen the contribution.

### Trivial
None.

## Nice-to-Haves
- A causal experiment connecting Sections 4 and 5: take a finetuned model, apply inference-time steering *against* the persona vector, and verify that trait expression reverses. This would directly show that the shift along the persona vector *causes* the behavioral change rather than merely correlating with it.
- Practical guidance for choosing the steering coefficient α in deployment settings.
- A brief note in Section 6 on efficient approximations of the projection-difference metric (Appendix K) to help practitioners assess feasibility.

## Removed Points
These points from the original review are flagged as removed; treat them with caution:
- Concern about the "escape LLM filters" claim being relegated to an appendix: standard practice; the paper references Appendix N. Removed per policy against penalizing appendix-deferred content.
- Criticism about projection-difference computational cost not discussed: the paper *does* mention it in Section 6.1 ("computing projection difference is somewhat expensive") and references Appendix K. Removed as already addressed.
- Any criticism about existence/availability of cited models, tools, or datasets. Removed per policy.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Run all finetuning experiments with at least 3 random seeds and report error bars on all steering curves and correlation estimates. This is the single highest-priority improvement.
2. Calibrate the preventative vs. inference-time steering comparison: find the α for each method that produces equal trait suppression, then compare MMLU cost at those matched points. If the pattern holds, the claim is airtight.
3. Include a one-sentence summary of the human-judge agreement level (e.g., "Pearson r = X on Y samples") in the main text.
4. Report the filtering rate for Section 2.2's response selection step.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>