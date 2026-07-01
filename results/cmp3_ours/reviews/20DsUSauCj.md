## Summary

This paper presents an automated pipeline for extracting linear directions in LLM activation spaces ("persona vectors") from natural-language trait descriptions, and demonstrates their use for monitoring, controlling, and predicting personality shifts during finetuning. Key contributions: (1) an automated pipeline that uses an LLM to generate contrastive prompts, evaluation questions, and rubrics, reducing a significant labor bottleneck; (2) validation that persona vectors can monitor both prompt-induced and finetuning-induced personality shifts; (3) a novel preventative steering method that adds the persona vector during training (rather than subtracting it at inference) to limit unwanted trait shifts while preserving capabilities; and (4) a pre-finetuning data screening metric that predicts post-finetuning trait expression from training data alone, with correlations of r=0.88–0.95.

## Strengths

1. **Novel preventative steering technique (Section 5).** The approach of steering *toward* an undesired trait during training to prevent its emergence is counterintuitive and well-supported. The fact-acquisition case study (Figure 6) provides a clean head-to-head comparison where preventative steering preserves both MMLU and new-fact accuracy while inference-time steering degrades both. The comparison to CAFT (which works for evil/sycophancy but not hallucination) further demonstrates the method's distinctive value. This is a genuine practical contribution beyond prior work.

2. **Pre-finetuning data screening (Section 6).** The projection-difference metric computed *before* finetuning correlates with post-finetuning trait expression at r=0.88–0.95 (Figure 7). The metric requires only forward passes through the base model, not full finetuning runs. Sample-level detection (Figure 8) showing clear separability between trait-inducing and control samples adds a finer-grained capability that could be practically useful for data filtering.

3. **Automated, generalizable pipeline (Section 2).** Given only a natural-language trait description, the pipeline generates contrastive system prompts, evaluation questions, and an evaluation rubric using Claude 3.7 Sonnet. Prior work required hand-crafted contrastive pairs or manual rubric design. The method is validated on two model families (Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct) and multiple traits (three main + four additional in appendix), providing reasonable evidence of generality.

4. **Intellectual honesty about limitations.** The paper candidly notes that monitoring correlations "arise primarily from distinguishing between different prompt types" (Section 3.3), that cross-trait correlations complicate specificity (Footnote 6), and that single-layer preventative steering does not fully prevent trait acquisition for strongly engineered datasets (Section 5). This transparency strengthens credibility.

## Weaknesses

### Fatal
None.

### Major

1. **The evaluation pipeline's LLM judge creates a dependency that the paper does not fully address in the main text.** The evaluation chain is: (a) Claude 3.7 Sonnet generates the evaluation rubric; (b) GPT-4.1-mini uses that rubric to assign trait expression scores; (c) the same scores filter responses used to extract persona vectors (Section 2.2: retain responses with scores >50 for positive prompts, <50 for negative); (d) the same scores serve as the y-axis metric in essentially every figure (Figures 2–8). This creates a plausible alternative explanation: the LLM judge may be detecting superficial linguistic markers that are easy for the persona vector to correlate with because both are optimized against the same judge, rather than reflecting genuine personality traits.

   The paper states that the LLM judge is validated against human evaluators and external benchmarks (Appendix D), but the main text provides no summary statistics (e.g., inter-rater agreement, which benchmarks, correlation strength). A reader cannot assess whether the metric is trustworthy without consulting the appendix, which is stripped by the review system. **At minimum, the main text should state the inter-rater agreement statistic and list which external benchmarks were used.** The causal steering experiments (Section 3.2) partially mitigate this concern by showing that persona vectors causally influence behavior, but the core correlation results in Figures 4 and 7 would be substantially more convincing if at least one key finding were replicated with an independent evaluation method (human evaluation or established behavioral benchmark).

### Minor

2. **The correlation analyses in Figures 4 and 7 rely on ~24 data points per plot, with non-independent observations.** Each subplot contains finetuned models from 8 dataset types × 3 severity levels (Normal/I/II) ≈ 24 points. The Normal/I/II variants of the same dataset share the same prompts (only target responses differ), so they are not independent observations. The paper reports p-values but not confidence intervals for the correlations, and does not account for the clustered data structure. Reporting confidence intervals or using a mixed-effects model would give a more accurate picture of estimate precision. The very high observed correlations (r=0.76–0.97) likely survive these corrections, but the analysis would be more rigorous with them.

3. **The number of finetuning runs per dataset configuration is not stated.** Section 4 describes measuring activation shifts but does not say how many finetuning seeds or runs were used per condition. Without this, the reader cannot assess whether observed variation reflects genuine dataset differences or random seed variation.

4. **A duplicated paragraph appears in Section 5** (lines 194 and 196 both begin "We compared preventative steering against alternative training interventions..."). This appears to be a formatting/editing artifact that should be cleaned up.

### Trivial
None.

## Nice-to-Haves

- **Confidence intervals for key correlations** would strengthen the statistical presentation (point 2 above could be elevated here if authors address it).
- **Explanation of why all-layer steering was necessary for the fact-acquisition case study (Section 5.2)** while single-layer steering was sufficient in other settings would help readers understand when to use which approach.
- **Independent replication of one key finding** (e.g., Figure 4 or 7) with a non-LLM-based evaluation metric (human evaluation or established benchmark like TruthfulQA) would substantially strengthen the paper's core claims, though the causal steering experiments already provide partial validation.

## Removed Points

- **Criticism about the prompt template not being in the main text**: Removed because conference papers routinely relegate full prompt templates to the appendix. The main text clearly references Appendix C.
- **Criticism about cross-trait correlations potentially not being statistically significant**: Removed because with r values of 0.76–0.97 and N≈24, even the most conservative CI bounds would still indicate significant effects. The concern about clustered data is kept as Minor.
- **Criticism that the "persona vectors" concept is not novel**: Removed because the paper correctly frames the contribution as the *automated pipeline* and its applications, not the concept itself. The abstract and introduction are clear about this.
- **Strength claiming the paper addresses an "important problem"**: Removed as generic. The three kept strengths are all concrete and evidence-grounded.

## Novel Insights

The review reveals that the paper's strongest finding is not explicitly highlighted as such: the pre-finetuning data screening metric (Section 6) and the preventative steering method (Section 5) are conceptually linked through the paper's core thesis that persona shifts are mediated by linear directions. The fact that a metric computed *before* training (projection difference) can predict post-finetuning outcomes with r≈0.9 is a surprisingly strong validation of the linear-mediation hypothesis. The contrast between CAFT (effective for evil/sycophancy but not hallucination) and preventative steering (effective for all three) is also more informative than the paper foregrounds — it suggests that different traits may have different mechanistic underpinnings (zero-ablation works for some, additive steering for others), which could be a fruitful direction for future work.

## Suggestions

- **Summarize the LLM judge validation in the main text.** At minimum, report the inter-rater agreement (e.g., Cohen's κ or Spearman correlation with human evaluators) and list which external benchmarks were used for validation. This single change would substantially address the main weakness.
- **Report confidence intervals for the correlations in Figures 4 and 7**, and note whether the Normal/I/II clustering affects the results.
- **State the number of finetuning seeds/runs** used per configuration.
- **Remove the duplicated paragraph** in Section 5.
- **Consider replicating one key finding** with an independent evaluation method (e.g., TruthfulQA for hallucination) to break the pipeline dependency, though this is a strengthening suggestion rather than a requirement.

## Score and Decision

**Calibration methodology.** I performed a bracketing search over the human-review corpus using queries related to "activation steering concept directions representation engineering LLM," retrieving papers across six score bands. I read full reviews for five anchor papers:
- **Steering Language Models with Activation Engineering** (avg 5.00, Reject): had baseline comparison issues, outdated models, and incomplete experiments — substantially weaker than the reviewed paper.
- **From Steering Vectors to Conceptors and Beyond** (avg 5.00, Reject): had unclear methodology and limited experiments — weaker in both execution and contribution.
- **Improving Instruction-Following in Language Models through Activation Steering** (avg 7.00, Accept): similar activation-steering methodology with clear experiments but narrower scope; the reviewed paper has more applications and a genuinely novel method (preventative steering).
- **Beyond Single Concept Vector: Gaussian Concept Subspace** (avg 6.75, Accept): similar concerns about LLM-based evaluation, but the reviewed paper is more comprehensive in its contributions.
- **Programming Refusal with Conditional Activation Steering** (avg 7.33, Accept): selective activation steering with good empirical validation; the reviewed paper has a comparable validation level but a wider range of demonstrated applications.

**Round 1 bracket:** Based on these anchors, I initially bracketed the paper between 6.5 and 8.5. The paper is clearly stronger than the 5.0 papers (which had methodological flaws the reviewed paper avoids) and comparable to the 7.0–7.33 accepted papers. The preventative steering method and pre-finetuning data screening go beyond what those papers demonstrated.

**Final score:** After narrowing against the 7.0–7.33 anchors, I assign **7.5**. This reflects that the paper has genuinely novel contributions and thorough experiments across two model families, but the LLM-judge dependency in the evaluation pipeline is a real concern that the main text does not fully address (the validation details are deferred to an appendix that review systems strip). This is fixable and not structural, but it prevents the paper from reaching the 8+ tier.

**Decision: Accept.** The contributions are significant and the issues are addressable through presentation improvements without changing the method or conclusions.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>