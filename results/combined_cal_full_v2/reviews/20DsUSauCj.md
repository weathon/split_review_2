## Summary

This paper introduces *persona vectors* — linear directions in LLM activation space corresponding to personality traits such as evil, sycophancy, and hallucination. It contributes (1) an automated pipeline that extracts persona vectors from just a natural-language trait description, (2) a preventative steering method that steers *toward* an undesired direction during training to avoid trait shifts at inference, and (3) a pre-finetuning data screening technique that predicts post-finetuning trait expression from training data projections onto persona vectors. Experiments across Qwen2.5-7B and Llama-3.1-8B, 8+ datasets, and 3 traits show strong correlations between persona-vector shifts and behavioral changes.

## Strengths

- **Automated pipeline for extracting persona vectors (Section 2) is a genuine systematization.** Prior work required manually designed contrastive pairs for each concept. The authors' approach — using a single prompt template with a frontier LLM to generate contrastive system prompts, evaluation questions, and a rubric from just a trait name and description — makes the line of research more accessible and reproducible. This is the paper's strongest methodological contribution. [draft weight: 8.69]

- **Preventative steering is novel and empirically compelling (Section 5, Figures 5-6).** The idea of steering *toward* an undesirable direction during training (rather than against it at inference) to prevent the model from needing to learn that shift is counterintuitive. The fact-acquisition case study (Section 5.2, Figure 6) is particularly well-chosen: it demonstrates a concrete practical scenario where inference-time steering degrades the very capability being trained (new-fact accuracy), while preventative steering largely preserves it. This is the paper's most novel experimental finding. [draft weight: 10.49]

- **Pre-finetuning data screening via projection difference (Section 6, Figures 7-8) is practically useful.** The idea of comparing the training response's projection onto the persona vector against the model's own "natural" response projection is elegant, and the reported correlations (r=0.88–0.95) are striking. The ability to identify problematic individual samples (Figure 8) before training has real practical value for safety. [draft weight: 9.80]

- **Broad evaluation across 3 traits, 8+ datasets, and 2 model families.** This breadth, combined with the cross-trait baseline analysis (Appendix I.2), provides reasonable evidence that findings are not specific to a single model or trait. [draft weight: 8.36]

- **The paper is transparent about its limitations** — acknowledging that monitoring correlations "arise primarily from distinguishing between different prompt types" with more modest within-type correlations (Section 3.3), and noting that preventative steering at a single layer does not always fully prevent trait acquisition (Section 5.1). [draft weight: 7.38]

## Weaknesses

### Fatal
None.

### Major

- **LLM judge validation is deferred entirely to the appendix with no quantitative evidence in the main text (Section 2.1).** The paper states it "validate[s] [the LLM judge] by checking agreement between our LLM judge and human evaluators" and "verify that our evaluation questions can effectively capture behavioral tendencies by comparing against established external benchmarks" — both cited to Appendix D. The main text contains zero quantitative results from this validation: no agreement rate, no correlation with human judgments, no examples of where the judge fails. Since every single claim in Sections 3–6 rests on trait expression scores produced by this judge, the reader cannot assess the reliability of the central evaluation instrument from the main paper. This is fixable (the validation exists in the appendix), but as presented it is a significant evidential gap. [draft weight: -0.28]

- **No error bars, confidence intervals, or variance estimates for any experimental result.** Steering experiments (Figures 2, 5, 6) plot trait expression scores as single lines with no indication of variance across rollouts or random seeds. Finetuning scatter plots (Figures 4, 7) show each dataset as a single point with no replication. The paper reports correlation coefficients and p-values, but p-values only test against the null of zero correlation — they do not tell whether differences between methods (e.g., preventative vs. inference-time steering in Figure 5) are statistically significant. The main claim that preventative steering preserves capabilities better than inference-time steering is supported only by the visual pattern of the MMLU line without any statistical test. [draft weight: 0.70]

### Minor

- **The strong correlations in Figures 4 and 7 may be substantially inflated by the coarse three-level data structure (Normal, I, II).** Each scatter plot contains ~24 points (8 datasets × 3 types). Normal points all cluster at low values while Type II points cluster at high values, meaning the correlation is driven primarily by the separation between three coarse categories rather than fine-grained predictive power. The paper does not report within-type correlations (e.g., among Normal-only, Type-I-only, or Type-II-only subsets). As the authors themselves note for the monitoring setting (Section 3.3), within-type correlations are "more modest." For practitioners, this matters: if the correlation is driven by the Normal-vs-Type-II distinction, the method primarily tells you whether a dataset is overtly harmful, not whether it will cause subtle shifts among datasets within the same severity level. [draft weight: 4.77]

- **The preventative steering mechanism (Section 5.1) is underspecified.** The paper states that adding the persona vector during training "counteracts the finetuning objective's tendency to push the model along that direction," but does not analyze the gradient dynamics or ablate to confirm the interpretation. An ablation comparing (a) steering during forward pass only (no gradient effect), (b) steering with stop-gradient on the added direction, and (c) full steering as implemented would clarify whether the effect comes from gradient dynamics or another property. The method may work regardless of mechanistic understanding, but the lack of analysis makes it harder to predict when it will fail or generalize. [draft weight: 6.79]

- **Sample-level detection (Section 6.2, Figure 8) shows qualitative histogram separations but does not report quantitative classification metrics.** A practitioner needs to know: at a given projection threshold, what is the precision, recall, or AUC? How many good samples are discarded and how many bad samples are missed? [draft weight: 4.27]

- **The pipeline depends on two proprietary API-gated models (Claude 3.7 Sonnet for generation, GPT-4.1-mini for evaluation).** If either model changes its behavior or is deprecated, exact reproduction may not be possible. This is a practical limitation worth more explicit discussion. [draft weight: 7.33]

### Trivial
None.

## Nice-to-Haves

- Add a calibration/threshold analysis for the projection difference metric (Section 6) — what projection difference should flag a dataset, and what is the false-positive rate at that threshold?
- Report failure cases: are there traits for which the pipeline fails to extract useful persona vectors?
- Add the prompt template for artifact generation to the main text (or a shortened version).
- The claim from the abstract/bullets about flagging data that "would otherwise escape LLM-based data filtering" should have a summary result in the main text rather than being deferred to appendices.

## Removed Points

These points were raised in the input review but are removed per filtering policy:
1. "The prompt template is not in the main text" — appendices are stripped by the parser; the template exists in the original submission.
2. "Normal datasets may not be clean" — the paper acknowledges baseline trait levels (hallucination score 20.1); this is a minor concern that does not affect the core claims.
3. Various formatting/style nitpicks — removed per policy.
4. Criticisms framed as area-of-concern speculation without concrete paper anchors — removed per filtering discipline.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Move the LLM judge human-agreement results (agreement rate, correlation with human judgments) from Appendix D into the main text — even a single paragraph with key numbers would substantially strengthen credibility.
2. Add variance estimates to all line plots (Figures 2, 5, 6) — the monitoring experiments already generate 10 rollouts; report this variance. For finetuning experiments, run at least 2–3 random seeds.
3. Compute and report within-type correlations for Figures 4 and 7 to clarify whether the correlations reflect fine-grained predictive power or primarily the Normal-vs-Type-II distinction.
4. Add a gradient-dynamics ablation for preventative steering to clarify the mechanism.
5. Report precision/recall or AUC for the sample-level separation in Figure 8.

## Calibration Anchors

| Paper | Path | Avg Score | Round | Itemized | Comparison |
|-------|------|-----------|-------|----------|------------|
| Steering LMs w/ Activation Engineering | 2XBPdPIcFK.md | 5.00 | 1 | Yes | Similar topic. Paper under review has broader evaluation and more applications but shares validation concerns. |
| Personality Alignment of LLMs | 0DZEs8NpUH.md | 6.00 | 1 | Yes | Personality + activation intervention. Paper under review has wider application scope but similar validation gaps. |
| Neuron-based Personality Trait Induction | LYHEY783Np.md | 6.67 | 1 | Yes | Personality trait induction via neuron manipulation. Comparable quality; both rely on LLM-as-judge. |
| Improving Reasoning via RepE | IssPhpUsKt.md | 6.80 | 1 | Yes | Representation engineering for reasoning. Paper under review has broader empirical scope. |
| Programming Refusal w/ CAST | Oi47wc10sm.md | 7.33 | 2 | Yes | Conditional activation steering. Better experimental reporting; paper under review has wider contribution but weaker reporting. |
| Editing Personality for LLMs | cxt2Auexc3.md | 5.75 | 2 | Yes | Personality editing benchmark. Less novel methodology; paper under review has stronger technical contributions. |
| Measuring Effects of Steered Representation | z1yI8uoVU3.md | 3.00 | 1 | Yes | More limited scope; paper under review is substantially stronger. |
| What Makes Your Model Low-empathy | DXaUC7lBq1.md | 3.00 | 1 | Yes | Fundamental framing issues; paper under review is substantially stronger. |

**Round 1 bracket:** 5.5–7.5. **Round 2 narrowing:** Compared weighted items with anchors in 5.5–7.5 range. The paper shares heavy-weight strengths (automated pipeline weight 8.69, preventative steering weight 10.49) with the 6.67–7.33 anchors. Its lightest weakness weights (-0.28 for judge validation, 0.70 for error bars) are below the mid-range anchors' typical weakness weights. The primary gap vs. the 7.33 "Programming Refusal" anchor is in experimental reporting rigor (error bars, validation transparency). **Final score:** 6.5 — between the 6.00 and 6.67/6.80 anchors, reflecting that the contributions are substantive and the scope is broad, but two reporting gaps (judge validation in appendix, no variance estimates) prevent it from reaching the 7+ level.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>