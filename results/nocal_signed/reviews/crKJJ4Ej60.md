## Summary

This paper proposes Copy-Paste, a generation paradigm for RAG that maximizes lexical reuse from provided context to reduce hallucinations. The authors instantiate this through a two-stage pipeline: (1) three Copy-Paste prompting methods (CP-Order, CP-Link, CP-Refine) generate high-copying responses, and (2) CopyPasteLLM internalizes these as DPO preference targets. On FaithEval (a counterfactual benchmark), CopyPasteLLM achieves 12.2–24.5% improvements over baselines using only 365 training samples (1/50th of prior methods). The paper also contributes a mechanistic analysis (Context-Parameter Copying Capturing) revealing that CopyPasteLLM suppresses parametric knowledge rather than enhancing contextual representations.

## Strengths

- **Data efficiency is genuinely impressive.** CopyPasteLLM achieves strong counterfactual results with only 365 query-context pairs (~1,825 preference pairs), compared to 18,000 for Context-DPO, 10,000 for Canoe, and 32,580 for ParamMute. This is well-documented in Table 1 and is a meaningful practical contribution.

- **The mechanistic analysis (Section 4.2) provides non-trivial insight.** The Context-Parameter Copying Capturing algorithm extends Knowledge Token Capturing to full Chain-of-Thought trajectories. The finding (Figure 4) that CopyPasteLLM's parametric knowledge representations shift while its contextual representations remain similar to the base model is specific, non-obvious, and backed by evidence — suggesting the mechanism is suppression of internal parametric knowledge rather than enhancement of context processing.

- **The three prompting methods (CP-Order, CP-Link, CP-Refine) form a coherent design space** from strict extraction to soft iterative refinement. Their trade-offs are documented with consistency across four model families (Mistral-7B, Llama-3.1-8B, Qwen2.5-72B, DeepSeek-V3), lending credibility to the empirical patterns.

- **The automated preference construction pipeline** (multi-criteria filtering → Elo tournament → answer stamping → preference pairs) is a well-engineered solution for generating preference data without human annotation, and is a genuine enabling contribution.

## Weaknesses

### Fatal
None.

### Major

- **Missing comparison against other fine-tuned baselines on non-counterfactual settings.** Table 3 compares CopyPasteLLM only against its own base model on PubMedQA and ConFiQA original contexts. While CopyPasteLLM shows clear improvements over the base model, it is impossible to tell whether these gains would also be achieved by Context-DPO, Canoe, or ParamMute in non-counterfactual scenarios. Without these comparisons, claims of generalizable improvement over prior methods are not fully supported.

- **Evaluation scope is predominantly counterfactual/knowledge-conflict benchmarks.** FaithEval is a counterfactual benchmark where the context contradicts parametric knowledge and the correct answer is to reproduce the context — an ideal setting for a method designed to maximize copying. ConFiQA's MR/MC subsets are also built around knowledge conflicts. While the paper also evaluates on PubMedQA (a non-counterfactual setting), it does not include standard RAG benchmarks with noisy, partially relevant, or distractor-containing contexts where blind copying could be harmful. This limits the generality of the claimed paradigm. (Note: this does *not* invalidate the results on the evaluated benchmarks; prior methods trained on the same counterfactual data still underperform by 12–24%, so the results are not tautological.)

### Minor

- **Training data composition is incompletely specified.** The paper states 241 of the 365 query-context pairs come from FaithEval (removed from the test set) but does not specify the source of the remaining ~124 samples. The paper also does not explicitly state whether any ConFiQA samples are included in the training data, which is relevant to the "unseen" claims for that dataset (though Table 3 does state PubMedQA samples are not used).

- **The motivating correlation (Section 2.2) is reported only qualitatively** via kernel density estimation without a quantitative correlation coefficient (e.g., Spearman's r). The abstract's language ("suggesting higher copying degrees *reduce* hallucinations") implies a causal direction that the observational analysis alone cannot support. The subsequent experimental results do provide causal evidence, so this is a framing issue rather than a technical flaw.

- **The "Twist" and "Causal" hallucination metrics in Table 2 are not defined in the main text.** Readers cannot interpret whether values in the 1300–1650 range are good or bad without consulting the appendix.

- **The CP-Refine "composite copy score" threshold is mentioned but not specified** in the main text, affecting reproducibility of the prompting method.

- **The logits power analysis (Figure 3) filters out samples where CopyPasteLLM responses exceed base response lengths.** The paper acknowledges this filtering but does not discuss potential selection bias — this may preferentially remove cases where copying is most effective.

### Trivial

- Table 1 does not report variance, confidence intervals, or statistical significance for any results.

## Nice-to-Haves

- Include comparisons against Context-DPO, Canoe, and ParamMute on non-counterfactual settings (PubMedQA and ConFiQA original contexts).
- Evaluate on a standard RAG benchmark with noisy or partially relevant retrieved passages to test whether copying remains beneficial when blind copying could be harmful.
- Report a quantitative correlation coefficient (Spearman's r) for the RAGTruth motivating analysis, controlling for question difficulty.
- Define the Twist and Causal hallucination metrics briefly in the main text.
- Specify the composite copy score threshold value used for CP-Refine.
- Add a brief discussion of potential selection bias from the logits power filtering.
- Include failure case analysis for the ~7% of FaithEval samples where CopyPasteLLM does not succeed.

## Removed Points

- **Correlation/causation as a fatal flaw:** The critic argued the paper treats correlation as causation without evidence. Demoted to Minor. The paper uses hedged language ("suggesting," "hypothesize") and the causal direction is subsequently tested experimentally (Section 4.1.2). The correlation is motivation; the experiments provide the causal evidence.
- **Evaluation on counterfactual benchmarks as "tautological":** Removed in severity. Prior methods trained on the same counterfactual data underperform by 12–24%, so success is not automatic. The point about limited evaluation scope is retained as Major.
- **"Generation paradigm" claim overstated:** Removed. The paper explicitly distinguishes Copy-Paste from extractive summarization (Section 2.1). The contribution lies primarily in the training pipeline and mechanistic analysis, which the paper accurately presents.
- **Non-sequitur about Chen & Shu citation:** Removed. A minor aside in the introduction that does not affect the technical contribution.
- **Task formulation eliminates reasoning:** The paper explicitly states "our focus in this work is a specialized task" — this is already acknowledged.
- **Answer stamping under-description:** The main text description is adequate for understanding; implementation details belong in the appendix.
- **Criticisms of missing appendix content:** The appendix was stripped by the parser; these criticisms cannot be verified and are removed per hard rules.

## Novel Insights

Beyond the paper's own contributions, the reviews surface one genuinely novel perspective: the finding that CopyPasteLLM works by suppressing parametric knowledge confidence rather than enhancing contextual representations (Section 4.2) is the most interesting and least expected result. Most prior work implicitly assumes the model needs to be taught to "pay more attention to context"; this paper suggests an alternative mechanism of "trusting context by distrusting your own knowledge." The UMAP visualization (Figure 4) showing that contextual representations remain nearly identical between base and CopyPasteLLM, while parametric representations shift substantially, is crisp evidence for this mechanism.

## Suggestions

- Add comparisons against Context-DPO, Canoe, and ParamMute on non-counterfactual settings (PubMedQA and ConFiQA original contexts) to substantiate claims of generalizable improvement.
- Include at least one standard RAG benchmark with noisy/distractor contexts to test whether the copying strategy remains beneficial when blind copying could be harmful.
- Specify the source of the remaining ~124 training samples (beyond the 241 from FaithEval) and explicitly state whether any ConFiQA samples are included in the training data.
- Define the Twist and Causal hallucination metrics briefly in the main text to make Table 2 self-contained.
- Report the composite copy score threshold value used for CP-Refine.
- Add a brief discussion of potential selection bias from the logits power filtering in Section 4.2.
- Re-frame the motivating correlation to emphasize it as a motivating observation rather than causal evidence, reserving the causal claim for the experimental results.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>