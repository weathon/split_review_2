## Summary

This paper introduces **persona vectors** — linear directions in a language model's activation space that correspond to specific character traits (evil, sycophancy, hallucination). It presents an automated pipeline that, given only a natural-language trait description, generates contrastive prompts, extracts a layer-specific vector, and validates it. The paper then demonstrates four applications of a single persona vector: (1) monitoring prompt-induced behavioral shifts via projection, (2) steering behavior at inference time, (3) a novel **preventative steering** method that adds the persona vector during finetuning (rather than subtracting it at inference) to limit unwanted trait acquisition while better preserving general capabilities, and (4) pre-finetuning data screening by projecting training samples onto persona vectors to predict which data will cause trait shifts. The preventative steering result — particularly the hallucination/fact-acquisition case study (Figure 6) — is the paper's strongest and most distinctive contribution.

---

## Strengths

1. **Novel preventative steering application with compelling evidence.** The idea of steering *toward* an undesirable trait during finetuning (rather than *against* it at inference) is conceptually interesting and practically relevant. The hallucination/fact-acquisition case study (Figure 6, Section 5.2) cleanly shows that inference-time steering degrades both MMLU and new-fact accuracy, while preventative steering suppresses hallucinations to baseline while largely preserving both — a result that is striking and not easily explained by confounders.

2. **Broad and practical application scope from a single vector.** The paper demonstrates a single persona vector being used for monitoring (Section 3.3), inference-time steering (Section 3.2), preventative steering during finetuning (Section 5), and pre-finetuning data screening (Section 6). Most representation engineering papers stop at steering; the breadth here makes the contribution practically grounded.

3. **Automated extraction pipeline.** Given only a trait name and description, the pipeline (Section 2) uses a frontier LLM to generate contrastive system prompts, evaluation questions, and a rubric, then extracts a layer-specific persona vector. Prior work required manually constructed contrastive pairs or hand-crafted datasets (though the paper acknowledges that Wu et al. 2025 also developed an automated pipeline). The systematization is non-trivial.

4. **Candid about limitations.** The paper explicitly notes that monitoring correlations (r=0.75–0.83) arise primarily from distinguishing between different prompt types, with "more modest correlations when controlling for prompt type" (Appendix E.2, referenced in Section 3.3). It acknowledges that single-layer preventative steering does not always fully prevent trait acquisition (Section 5.1). This candor lends credibility.

---

## Weaknesses

### Fatal
None.

### Major

1. **No variance or uncertainty estimates reported anywhere in the main text.** The paper reports correlation coefficients (r=0.75–0.97) and p-values across six figures, but no standard deviations, confidence intervals, or error bars appear on any figure. No mention of multiple finetuning seeds. This matters concretely:
   - **Finetuning experiments (Figure 4):** Each point is a single finetuning run on one dataset × version. With ~24 data points per plot, a single outlier seed could shift the correlation meaningfully.
   - **Preventative vs. inference-time steering (Figures 5–6):** MMLU accuracy and trait expression curves are single lines without variance estimates. The central claim — that preventative steering better preserves capabilities — rests on the separation between these curves, but the reader cannot assess whether the gap is significant relative to run-to-run variation.
   - **Projection difference predictions (Figure 7):** Same issue — r=0.88–0.95 with no uncertainty quantification.
   
   This is an evidential weakness (the conclusions may be correct, but reliability cannot be assessed from the reported data). The authors should report standard deviations across multiple finetuning seeds and include error bars or shaded regions.

2. **Central evaluation metric relies on a single LLM judge (GPT-4.1-mini), with its validation deferred entirely to the appendix.** Every empirical claim — steering effectiveness, monitoring correlations, finetuning shift correlations, preventative steering comparisons — rests on a single automated evaluation producing a "trait expression score" from 0 to 100. The paper states that the judge is validated "by checking agreement between our LLM judge and human evaluators... (see Appendix D)" (line 66–67), but no agreement statistics (Cohen's κ, Spearman ρ, accuracy) appear in the main text. Given that the judge model itself is a black box that may share training data or biases with the evaluated models, and that LLM-as-judge for hallucination has known failure modes, the main text should report at minimum the human–LLM agreement numbers. Without them, the reader cannot assess whether the reported correlations reflect genuine behavioral traits or systematic biases in a single evaluation model.

### Minor

3. **Cross-trait correlations are high enough to partially undermine the trait-specificity framing.** The paper reports cross-trait correlations of r=0.34–0.86 (Section 4.2, line 164). Notably, the upper end (r=0.86) exceeds the same-trait correlation for sycophancy on the Qwen model (r=0.769, Figure 4). The paper acknowledges this in a footnote (fn. 6: "negative traits... tend to shift together") but the central narrative treats evil, sycophancy, and hallucination as separate traits with separate vectors. The data screening and preventative steering applications depend on *distinguishing* which trait a dataset induces; if the vectors largely capture a common "undesirable behavior" factor, the methods may work mainly by detecting and suppressing a general undesirability direction. This deserves more prominent analysis than a footnote.

4. **The "mediated by" framing in Section 4.2 implies a causal account unsupported by the evidence.** The section opens with "Are behavioral shifts during finetuning mediated by persona vectors?" (line 138) and the surrounding text repeatedly uses causal language. However, the evidence is correlational: finetuning shift along a persona vector correlates with trait expression. It could equally be that finetuning changes behavior through other mechanisms, and both the activation shift and behavioral change are downstream effects of a common cause. The paper does not establish that the persona vector is the *mediator* rather than a correlate.

5. **The claim about "escaping LLM filters" appears in the contribution list without main-text support.** The abstract and introduction state that the data screening method identifies problematic data "including some which would otherwise escape LLM-based data filtering" (line 54). The supporting evidence is entirely in Appendix N, with the main text only referencing this appendix (line 261). If this claim is substantive enough for the contribution list, a representative example or quantitative comparison belongs in the main text.

### Trivial

6. **The base model's pre-existing hallucination score (20.1) is notably high.** The Figure 5 caption reports that the base model's hallucination score is 20.1 on a 0–100 scale before any finetuning or steering. This is a substantial baseline for an "aligned" model and conditions the interpretability of the preventative steering results (which reduce hallucinations to baseline). The paper does not discuss why this baseline is so high or what it implies about the model's default behavior.

---

## Nice-to-Haves

- **Report variance estimates** (multiple finetuning seeds, error bars on line plots). This is the single highest-leverage improvement the paper could make.
- **Bring LLM judge validation statistics to the main text** — a single sentence with human–LLM agreement (e.g., "Spearman ρ = 0.XX on N samples") would address the most immediate concern.
- **Surface the cross-trait correlation analysis more prominently** — a dedicated paragraph or subsection analyzing vector geometry (cosine similarities between vectors, factor analysis) would clarify whether the applications require trait-specificity or work equally well with a generic vector.
- **Include a main-text quantitative comparison for the "escapes LLM filters" claim**, rather than deferring entirely to the appendix.
- **Ablate inference-time steering with all layers** for a fairer comparison with the strongest preventative steering result (which uses all-layer steering in the fact-acquisition case study, Section 5.2).
- **Discuss the high baseline hallucination score** (20.1) and its implications.

---

## Removed Points

These points were raised in the input review but are removed per the filtering rules. They are flagged for traceability but should be treated with caution:

- **Closed-source model dependency (Claude 3.7 Sonnet, GPT-4.1-mini) as a reproducibility concern** — Removed per hard rule: the paper cites these models, and questioning their availability/release status is prohibited.
- **Finetuning hyperparameters (LoRA vs. full FT, learning rate, epochs) absent from main text** — Removed per hard rule: nitpicks about undisclosed hyperparameters are not permitted.
- **Potential selection bias from filtering step discarding refusals** — Removed as speculative; the reviewer acknowledges it "could" introduce bias without evidence it actually does.
- **Concern that the strength about automated pipeline overstates novelty relative to Wu et al. (2025)** — The paper's footnote 1 acknowledges that Wu et al. also developed an automated pipeline, so the strength is slightly overstated; removed to avoid conflating reviewer claim with paper claim.

---

## Novel Insights

None beyond the paper's own contributions. The most novel insight from reviewing is the observation that the **preventative steering result** (Figure 6) is considerably more compelling than the monitoring correlations or data screening claims, and that it does not depend on trait-specificity — it would work if the vectors capture only a general "undesirability" direction. This suggests the paper's strongest contribution may be independent of its weaker ones.

---

## Suggestions

1. **Add variance reporting.** Finetune with at least 3 random seeds and report standard deviations or confidence intervals on all key numbers. Add error bars or shaded regions to Figures 5 and 6 (the preventative steering comparison). This single change would substantially strengthen the paper.
2. **Move the LLM judge validation into the main text.** Report the human–LLM agreement statistic in Section 2.1 (e.g., "Spearman ρ = 0.XX, p < 0.001 across N samples").
3. **Add a short subsection or paragraph analyzing what distinguishes the persona vectors from each other** (cosine similarities, variance explained by a common factor). Acknowledge explicitly whether the applications require trait-specificity or would work as well with a generic vector.
4. **For the data screening claim about escaping LLM filters**, include at least one qualitative example or a brief quantitative comparison in Section 6.

---

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>