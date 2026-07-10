Now I have enough information for calibration. Let me compile the final review.

**Calibration Summary:**

**Round 1 bracket:** 5.5 – 7.5

**Anchors examined:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| 2XBPdPIcFK (ActAdd) | 5.00 | R1 | Yes | Worse: outdated models, inconsistent baselines, experiment clarity issues. Our paper has stronger empirical design. |
| gYa9R2Pmp8 (Jailbreak via Persona) | 4.00 | R1 | No | Worse: narrower scope, black-box only. |
| 0DZEs8NpUH (Personality Alignment) | 6.00 | R1 | Yes | Comparable: dataset contribution vs. methodological breadth; both have evaluation concerns. |
| rKMQhP6iAv (Personas/Truthfulness) | 4.25 | R1 | No | Worse: less comprehensive. |
| Oi47wc10sm (CAST) | 7.33 | R1+R2 | Yes | Better: cleaner comparison design, no asymmetric evaluation issue. Our paper has more breadth but weaker comparison. |
| wozhdnRCtw (Instr.-Following Steering) | 7.00 | R2 | Yes | Better: solid experiments, weaker novelty. Our paper has more applications but weaker comparison. |
| tTPHgb0EtV (Booster) | 8.00 | R2 | Yes | Better: all-8s, clean experiments. Our paper has broader scope but methodological concern. |

**Round 2 narrowing:** The paper is clearly above 5.00 (ActAdd) but below 7.33 (CAST) due to the asymmetric comparison issue.

**Final score: 6.0** — Grounded in favorability comparison: our strengths (9.80–14.56) match the 7.00–8.00 anchors, but our Major weakness (favorability 1.49) is more severe than the corresponding worst items in those anchors (CAST's lowest was 1.31 for a minor scalability skepticism; Booster's lowest were ~-2 but from a single harsh reviewer where other reviewers disagreed). The asymmetry in the Section 5 comparison is a genuine methodological concern that the 7+ papers do not share. The 6.0 decision reflects a paper with real contributions and strong evidence for most claims, but whose strongest comparative claim requires clarification.

---

## Summary

This paper introduces *persona vectors* — linear directions in LLM activation space extracted via an automated contrastive-generation pipeline — and demonstrates four applications: monitoring persona shifts at deployment, correlating finetuning-induced behavioral changes with activation shifts, preventing unwanted shifts via a novel preventative steering method, and pre-screening training data for potential persona impacts. The paper is evaluated on Qwen2.5-7B and Llama-3.1-8B across three traits (evil, sycophancy, hallucination) with additional traits in the appendix.

## Strengths

- **Comprehensive evaluation across multiple axes.** The paper validates persona vectors for four distinct applications (steering, monitoring, preventative mitigation, data screening) across two model families (Qwen2.5-7B, Llama-3.1-8B) and three major traits (evil, sycophancy, hallucination), plus additional traits in the appendix. This breadth makes the findings harder to dismiss as artifacts of a single setup. **[favorability=12.48]**

- **Strong and consistent correlational evidence.** The correlations between finetuning shift and trait expression (r = 0.76–0.97 across 12 model-trait pairs, Figure 4) and between projection difference and post-finetuning trait expression (r = 0.88–0.95, Figure 7) are unusually high for this type of mechanistic analysis, suggesting a genuinely tight correspondence between activation geometry and behavior. **[favorability=13.93]**

- **The pre-finetuning data screening idea is novel and practically useful.** Section 6's ability to predict which datasets or individual samples will cause persona shifts *before training* is a genuinely useful application that falls out naturally from the persona-vector framing, and goes beyond what existing LLM-based filtering alone can achieve. **[favorability=14.56]**

- **Well-motivated with real-world grounding.** The paper grounds its work in specific incidents (Bing chatbot, Grok praising Hitler, GPT-4o sycophancy in 2025) that are clearly instances of unintended persona drift. **[favorability=9.80]**

## Weaknesses

### Major

- **Asymmetric comparison design for preventative vs. inference-time steering (Section 5, Figures 5–6).** For inference-time steering, the model is finetuned normally, then steering *against* the trait is applied *during* the MMLU evaluation — so accuracy is measured with the steering intervention actively modifying hidden states. For preventative steering, the model is steered *toward* the trait during training, then evaluated *without* any steering intervention. The paper concludes that preventative steering "better preserves the model's general capabilities than inference-time steering," but this comparison conflates method advantage with the cost of active steering during MMLU evaluation. A control experiment — measuring MMLU of the inference-time finetuned model *without* the steering intervention — would isolate the cost of the steering operation itself from any genuine capability preservation difference. The preventative steering method still stands as a useful contribution on its own, but the comparative claim is weakened. **[favorability=1.49]**

### Minor

- **Heavy reliance on a single LLM judge (GPT-4.1-mini) for the primary trait expression metric.** All quantitative results (correlations, steering comparisons, data screening) ultimately depend on this one judge assigning 0–100 scores. The paper acknowledges this and references validation in Appendix D (agreement with human evaluators, external benchmarks), but no quantitative human agreement score appears in the main text, and there is no main-text analysis of whether the judge confounds trait expression with response length, refusal patterns, or other surface features. Some triangulation exists (MMLU, New Facts Accuracy for hallucination in Section 5.2), but the core trait-expression scores lack main-text corroboration. **[favorability=1.85]**

- **Framing of pipeline novelty relative to prior work.** The paper acknowledges (footnote 1) that Wu et al. (2025) "also developed an automated pipeline for translating natural language concept descriptions into contrastive pairs of generations, and eventually into linear directions," which describes essentially the same pipeline. The paper's genuine novelty lies in the applications (preventative steering, data screening), but the abstract and introduction present the automated pipeline as a primary contribution ("Our method for extracting persona vectors is automated and can be applied to any personality trait"). The applications are genuinely novel, so this is a framing issue rather than a substantive one. **[favorability=4.62]**

### Trivial

None.

## Nice-to-Haves

- **Confidence intervals on correlations.** Figures 4 and 7 report r and p-values but not confidence intervals. For n≈20 data points per plot, the uncertainty on r = 0.76 is substantially larger than on r = 0.96. Reporting 95% CIs would improve interpretability.
- **Quantification of projection-difference cost.** Section 6 notes that computing projection difference requires generating base-model responses for all training samples. A brief cost estimate (e.g., "roughly 2× the inference cost of processing the training data") would help practitioners gauge feasibility.
- **Token-position rationale.** Extraction uses response-token averaged activations while monitoring uses the last prompt token. The paper notes (footnote 2) that response tokens yield better steering directions, but a brief empirical note on why prompt-token projections work for monitoring would be helpful.
- **Broader monitoring caveat in abstract.** The paper honestly discloses (line 112) that monitoring correlations are driven by distinguishing prompt types, with more modest correlations controlling for prompt type. This bounds practical utility and could usefully appear in the conclusion.

## Removed Points

These points were flagged by the reviewer but are removed after verification against the paper:

- **CAFT finding relegated to appendix** — REMOVED. The finding that CAFT is effective for evil/sycophancy but ineffective for hallucinations IS in the main text (lines 194–196). Only the *explanatory discussion* of *why* is in the appendix, which is a reasonable division of content.
- **Monitoring caveat about explicit vs. subtle shifts** — REMOVED. The paper itself honestly discloses this limitation (line 112: "more modest correlations when controlling for prompt type").
- **Token-position mismatch not discussed** — REMOVED. The paper notes in footnote 2 that response tokens yield better steering, and the monitoring experiments successfully use prompt-token projections. The empirical choice works and is documented.
- **Small n for correlations (Figure 4)** — DEMOTED to Nice-to-have. Reporting r and p-values is standard practice. Confidence intervals would improve interpretability but this is not a weakness.
- **LLM judge lack of alternative metrics** — PARTIALLY REMOVED. The paper does use MMLU and New Facts Accuracy as alternative metrics for hallucination (Section 5.2). The concern is narrowed to the lack of main-text human-agreement numbers.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add the control experiment: measure MMLU of the inference-time-steered model *without* the steering intervention to separate finetuning-induced degradation from steering-operation cost. This would either strengthen the comparative claim (if the gap persists) or clarify the degree to which the reported advantage is an evaluation artifact.
2. Include at least one main-text quantitative human-agreement metric for the LLM judge (e.g., Spearman correlation) and an analysis of potential confounds (response length, refusal patterns).
3. Reframe the contribution statement to more precisely scope the pipeline as building on prior work (Wu et al., 2025) while emphasizing the novel applications.
4. Add confidence intervals to correlation plots (Figures 4, 7).

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>