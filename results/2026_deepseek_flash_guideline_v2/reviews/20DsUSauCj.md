Since the calibration data is not accessible, I will score based on my thorough reading of the paper and knowledge of ICLR standards. Let me finalize the review.

Here is my final consolidated review:

---

## Summary

This paper introduces "persona vectors" — linear directions in LLM activation space corresponding to personality traits (evil, sycophancy, hallucination) — extracted via an automated pipeline from natural-language descriptions. It demonstrates four applications: monitoring deployment-time persona shifts, controlling traits via steering, preventing unwanted personality drift during finetuning via a novel "preventative steering" method, and screening training data before finetuning using projection differences.

## Strengths

- **Preventative steering preserves capabilities better than inference-time steering.** The fact-acquisition case study (Section 5.2, Figure 6) provides the cleanest causal evidence in the paper: under inference-time steering, reducing hallucinations to baseline degrades both MMLU accuracy and new-fact accuracy, whereas preventative steering achieves the same hallucination reduction while preserving MMLU and only slightly reducing new-fact accuracy. This demonstrates that the core methodological novelty — steering *toward* an undesirable trait during training — is practically useful in a realistic scenario and cannot be replicated by post-hoc intervention.

- **Pre-finetuning projection difference predicts post-finetuning trait expression with high correlation across two model families.** Figure 7 reports r=0.88–0.95 (all p<0.001) between a metric computed on training data alone and the actual trait expression after finetuning. This holds for Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct, across three traits, and for both explicitly trait-eliciting and EM-like datasets. The metric is principled (difference between training-response and base-model natural-response projections, Equation in Section 6.1).

- **Finetuning-induced persona shifts correlate strongly and specifically with activation shifts along persona vectors.** Figure 4 reports within-trait correlations of r=0.76–0.97 that are systematically higher than cross-trait baselines (r=0.34–0.86, Appendix I.2), supporting the claim that persona vectors capture trait-specific signal rather than a generic "badness" direction. The paper also honestly reports that negative traits (and humor) tend to shift together (footnote 6).

- **Honest reporting of limitations throughout.** The paper explicitly notes that monitoring correlations are driven primarily by distinguishing between different prompt types, with more modest correlations when controlling for prompt type (Section 3.3, Appendix E.2); that single-layer preventative steering does not fully prevent trait acquisition on challenging datasets (Section 5.1); and that persona shifts are correlated between seemingly different traits (footnote 6). This transparency strengthens rather than weakens the paper's claims.

- **Comparisons against multiple alternative methods.** Preventative steering is compared against inference-time steering (Figures 5, 6), simple regularization penalties (found ineffective, Appendix L.5), and CAFT (Casademunt et al., 2025) — which works for evil and sycophancy but fails for hallucinations (Appendix L.4). Persona-vector-based data filtering is compared against LLM judge-based filtering and shown to have complementary strengths (Appendix M).

## Weaknesses

### Fatal
None.

### Major

1. **Complete absence of variance/uncertainty reporting.** None of the paper's key figures (Figures 2, 4, 5, 6, 7) report error bars, confidence intervals, or any measure of dispersion. There is no mention of random seeds, number of finetuning runs with different initializations, or stability of correlations under resampling. This is problematic because some conclusions depend on fine-grained comparisons — e.g., Figure 5 compares preventative and inference-time steering across steering coefficient values, and Figure 6 shows a differential impact on MMLU/new-fact accuracy between the two methods. Without variance estimates, the reader cannot assess whether the observed differences are meaningful or within experimental noise. Given that the paper already uses 10 rollouts per configuration for many experiments (Section 3.3), bootstrap-estimated confidence intervals should be straightforward to compute.

2. **Near-total reliance on a single LLM-as-judge evaluation pipeline with only appendix-deferred validation.** Every quantitative result in the paper uses GPT-4.1-mini as the judge to assign trait expression scores (0–100). The paper mentions in Section 2.1 that the judge is validated "by checking agreement between our LLM judge and human evaluators" and by "comparing against established external benchmarks" (Appendix D), but the main text provides no summary of this validation. If the LLM judge has systematic biases — e.g., conflating verbosity or certain writing styles with trait expression — those biases propagate through the entire pipeline: response filtering during extraction, steering evaluation, monitoring correlations, finetuning shift correlations, and data screening evaluation. While the paper does perform human validation (deferred to Appendix D), the absence of even a summary statistic (e.g., "human-LLM agreement: r=X on N samples") in the main text weakens the reader's ability to assess result credibility.

### Minor

3. **"Mediation" framing overstates what the evidence supports.** Section 4.2 asks "Are behavioral shifts during finetuning *mediated* by persona vectors?" but the evidence is purely correlational: both the finetuning shift (x-axis) and the trait expression score (y-axis) measure different consequences of the same finetuning process. The section title correctly uses "predicts" ("Activation shift along persona vector predicts trait expression"), and the paper presents the evidence as correlations, but the "mediated" language implies a causal pathway that the evidence does not establish. This is a framing issue; replacing "mediated" with "predicted by" or "correlated with" would be more accurate.

4. **Dataset-level correlations may be partially inflated by clustering.** The scatter plots in Figures 4 and 7 include data from two qualitatively different dataset types: explicitly trait-eliciting datasets (Evil II, Sycophancy II, Hallucination II) which naturally produce extreme projection values, and EM-like datasets (Medical, Code, GSM8K, MATH, Opinions) with more modest values. This bimodal structure can inflate Pearson correlations. The reported cross-trait baselines (r=0.34–0.86, Appendix I.2) and the inclusion of Normal/I/II severity levels within each dataset type provide partial reassurance, but the paper does not report whether the within-trait correlations remain strong when restricted to the EM-like datasets alone. A within-cluster analysis would strengthen the claim.

### Trivial

5. **The paper splits 40 questions into extraction set (20) and evaluation set (20) for layer selection, but does not explicitly confirm these sets are disjoint from the downstream evaluation.** The design suggests they are (the split is described in Section 2.1), but explicitly stating that the sets used for layer selection and downstream validation are non-overlapping would preempt a potential information leakage concern.

## Nice-to-Haves

- A brief summary of human-LLM judge agreement in the main text (one sentence with correlation and sample size).
- Within-cluster correlation analyses for Figures 4 and 7 (restricted to EM-like datasets).
- A brief limitations paragraph in the main text rather than deferring entirely to Appendix B.
- A brief note on the computational budget (API calls, GPU hours) for the full pipeline.

## Removed Points

The following points from the inputs were removed as they do not reflect genuine weaknesses in the paper:

- **"The LLM judge concern is fatal/evidential"** — The paper explicitly validates the judge against human evaluators and external benchmarks (Section 2.1, Appendix D). The criticism about not seeing those results is a parser artifact (stripped appendix), not an author omission. The remaining concern about insufficient main-text visibility is kept as a Major weakness.
- **"No discussion of computational cost"** — Moved to Nice-to-Haves; not a core weakness.
- **"Finetuning setup is underspecified in main text"** — Standard practice to defer training hyperparameters to an appendix.
- **"Preventative vs inference-time steering comparison is unfair"** — The paper compares methods at matched steering coefficient values, which is a standard and reasonable approach. The critic's suggested alternative (adjust coefficients to match post-steering trait scores, then compare MMLU) would be complementary but the current comparison is not unfair.
- **"Layer selection overlap concern (framed as major)"** — The paper describes a 20/20 split of 40 questions into extraction/evaluation sets, making them disjoint by design. Downgraded to trivial because the paper should confirm this explicitly.
- **"Missing related works"** — Rule prohibits this criticism.
- **All formatting/style nitpicks, speculation-based claims, and generic area-of-concern sweeps** — Removed per filtering rules.
- **Strengths about generic "importance of the problem" or lacking specific evidence** — Removed per filtering rules.

## Novel Insights

The synthesis reveals an interesting asymmetry: the paper's strongest and most novel contribution (preventative steering, demonstrated in Figure 6) is also the one least affected by the evaluation methodology concerns. The fact-acquisition case study compares two steering methods applied to the same model on the same task — both methods use the same LLM judge, so any judge bias affects both arms equally, and the differential impact on MMLU and new-fact accuracy is a model-internal comparison. This means the paper's most important claim is robust even to the LLM-judge concern. The more vulnerable claims (monitoring correlations, data screening) are also the ones for which the paper is more transparent about limitations, creating a consistent pattern where the strength of evidence is proportional to the novelty of the claim.

## Suggestions

1. **Add error bars or confidence intervals to all figures** — at minimum, Figures 2, 5, and 6. Bootstrap-estimated CIs from the existing rollouts (10 per configuration) would substantially improve credibility.
2. **Include a one-sentence summary of human-LLM judge agreement in the main text** (e.g., "Our LLM judge agrees with human evaluators with a Pearson correlation of r=X on N samples").
3. **Replace "mediated" with "predicted by" or "correlated with" in Section 4.2** to avoid overclaiming causal interpretation.
4. **Add within-cluster correlation analyses** for Figures 4 and 7, restricted to EM-like datasets only, to show the relationship is not driven purely by the bimodal structure.
5. **Explicitly state** that the layer selection evaluation set and downstream validation set are disjoint.

## Score and Decision

Based on my thorough reading of the paper:

The paper makes genuine contributions: the automated extraction pipeline is a practical improvement over manual approaches, and the preventative steering method is genuinely novel and well-demonstrated. The experiments are extensive (2 model families, 3 main + 4 additional traits, multiple dataset types, comparisons against multiple baselines). The paper is well-written, clearly motivated, and honestly reports limitations.

The weaknesses are real but bounded: (1) the absence of error bars throughout is the most significant gap and would need to be addressed in a revision, but the qualitative trends and effect sizes are large enough that they would likely survive proper variance estimation; (2) the single-judge evaluation is a concern mitigated by the paper's own validation (appendix-deferred) and by the fact that the most important claim (preventative steering) compares two methods using the same judge, making it robust to judge biases; (3) the remaining issues are minor framing and presentation concerns.

This is a clear accept at ICLR. The contributions are concrete, the evaluation is extensive if imperfect, and the paper would benefit the community. I assign a score of **7**, reflecting that the paper has solid contributions with fixable methodological gaps, placing it in the "good paper" range for a top venue.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>