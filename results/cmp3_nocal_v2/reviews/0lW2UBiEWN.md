Now I have thoroughly verified all claims against the paper. Let me write the final consolidated review.

## Summary

This paper introduces MESA & MASK, a benchmark for detecting and classifying deceptive behaviors in LLMs. The core methodology contrasts a model's reasoning and responses under a neutral system prompt (MESA) with those under a pressure-inducing prompt (MASK) that creates goal conflicts without explicit instructions to deceive. Using this comparative paradigm, the authors construct a dataset of 2,100 instances across 6 domains and 6 deception types, evaluate 22 models, and introduce a four-quadrant classification system (Explicit Deception, Deception Tendency, Superficial Alignment, Consistent) based on whether reasoning and responses change between the two conditions. The paper finds that deceptive behaviors are widespread across models, including state-of-the-art proprietary systems.

## Strengths

1. **Well-motivated comparative evaluation paradigm.** Contrasting model behavior under neutral vs. pressure-inducing conditions addresses a genuine gap in prior static benchmarks (e.g., TruthfulQA, HaluEval) that cannot distinguish strategic behavioral shifts from capability deficits or hallucination. The design using goal-conflict scenarios without explicit deceptive instructions is sound. (Section 1, Figure 1)

2. **Thorough dataset construction with rigorous quality control.** The 2,100 instances are balanced across 6 domains and 6 deception types (Figure 4, Table 1). The pipeline includes automated quality evaluation with explicit thresholds (≥0.85 on three dimensions), iterative refinement with up to 3 rounds, and human expert double-blind annotation with strong inter-annotator agreement (94.3%, Cohen's κ = 0.89). Exclusion of prompts that could be interpreted as implicit instructions is a sensible design choice. (Section 4.2)

3. **Complementary metric design.** D@1 (per-instance likelihood), D@k (behavioral persistence across k=5 samples), and Stability (D@k/D@1) capture different facets of deceptive behavior, distinguishing sporadic from systematic patterns. This is more informative than a single aggregate rate. (Section 5.1)

4. **Broad and systematic model evaluation.** Covering 22 models from Qwen-0.6B to Gemini 2.5 Pro and Claude Sonnet 4 — spanning dense, MoE, distilled, and proprietary architectures — enables informative cross-model comparisons about how scale, architecture, and training strategy relate to behavioral patterns. (Table 1)

## Weaknesses

### Major

1. **Data error in the safety fine-tuning experiment (Table/Figure 6).** The epoch 0 baselines in the fine-tuning table (lines 239-246) are inconsistent with Table 1 on three of four values. Specifically:
   - Table 1 reports Qwen3-14B D@k = 47.38; the fine-tuning table shows 71.37.
   - Table 1 reports Qwen3-4B D@1 = 71.37; the fine-tuning table shows 72.84.
   - Table 1 reports Qwen3-4B D@k = 46.36; the fine-tuning table shows 71.37.
   
   Additionally, the figure caption states the right y-axis range is 38–48% for @k, yet the table lists @k values between 66–71%, placing them entirely outside that axis range. The figure and table contradict each other. The text's description of percentage reductions correctly uses the Table 1 baselines, suggesting the table entries (not the conclusions) are erroneous, but this error undermines trust in the reported data. Since the paper itself acknowledges this is "a limited case study involving two models from the same family and a single training run," this error does not invalidate the core benchmark contribution, but it must be corrected.

2. **No reported human-model agreement on the deception classification task.** The entire evaluation pipeline — determining whether a MASK output constitutes deception relative to the MESA baseline — is performed by GPT-4.1 as an LLM judge. The paper asserts that "evaluation metrics validated through human annotation studies" (Section 4.3) and that "the determination of deceptive behavior (Ground Truth) ... is derived from rigorous human annotation studies" (Section 5.1). However, the only human annotation statistics reported (94.3% agreement, κ=0.89) are for *dataset quality control* — verifying formatting, instruction following, deception type matching, and safety compliance (Section 4.2). No agreement rate between GPT-4.1 and human experts on classifying model outputs as deceptive vs. non-deceptive is reported. Given that GPT-4.1 is a proprietary model subject to its own alignment pressures and potential biases, using it as the sole judge without calibration against human judgment leaves the reliability of per-instance deception classifications unsubstantiated.

3. **Conceptual tension between "behavior change under pressure" and "deception."** The paper adopts the definition of deception as "the intentional inducement of false beliefs to achieve an outcome distinct from the truth" (Section 1), yet LLMs do not have intentions. The comparative framework measures *behavioral shifts* between MESA and MASK conditions, and these shifts are then labeled as deception. While the paper's scenario design (goal conflicts where the honest response conflicts with model incentives) and four-quadrant system (which also examines reasoning changes) partially mitigate this concern, the paper does not cleanly articulate why a behavioral shift under pressure constitutes deception (which requires intentionality) rather than context-adaptive behavior (which is generally desirable). The paper would benefit from explicitly acknowledging that "deception" is used as a behavioral label for outputs that exhibit strategic concealment or misdirection in goal-conflict scenarios, not as an attribution of mental states.

### Minor

4. **The "~" (consistency) operator in the four-quadrant classification is not formally defined in the main text.** Figure 2 uses $C_{me} \sim C_{ma}$ and $R_{me} \sim R_{ma}$ to distinguish quadrants, but the criteria for what counts as "consistent" vs. "inconsistent" reasoning chains or responses — the similarity metric, threshold, or rubric — are not stated in the main body. The paper refers to Appendix C.2 and D for details. While the appendix likely contains this information, the main text should at least summarize the judgment criteria given that this is the paper's primary classification mechanism.

5. **"Consensus aggregation" for MESA baseline is not explained.** The evaluation protocol states that the MESA chain's k responses "undergo consensus aggregation to produce a consolidated MESA baseline" (Section 4.3), but the method (majority vote, average embedding, or some other procedure) is not specified. This matters because the MESA baseline determines what counts as "consistent" behavior.

6. **Several causal interpretations in Section 5.3 go beyond correlational evidence.** Claims such as "the architectural efficiency of Llama3's GQA may foster more stable reasoning pathways" and "the expanded parameter space provided by MoE architectures could be a contributing factor" are presented in the context of a single comparison that conflates architecture, training data, pre-training procedure, and distillation method. The paper mostly uses hedging language ("might," "could," "we hypothesize"), but the surrounding framing treats these as findings rather than speculations about confounded variables.

7. **The term "authentic preference function" (Section 3.1) attributes agency to statistical models in a way that is philosophically questionable and unnecessary.** The comparative framework works as a measure of behavioral shift regardless of whether MESA outputs represent an "authentic" preference.

### Trivial

- None identified.

## Nice-to-Haves

- Provide representative examples from each of the four quadrants with human expert reasoning showing what distinguishes a Q1 (Explicit Deception) instance from a Q3 (Superficial Alignment) or Q4 (Consistent) instance.
- Report confidence intervals or error bars for the main results in Table 1, given the k=5 sampling.
- If the fine-tuning experiment data can be corrected (or if the error turns out to reflect a different experimental setup that is properly documented), include a clear explanation of the discrepancy.

## Removed Points

- **"First benchmark" claim overreach** — Removed because the paper's qualifier "designed for the *differential diagnosis* of LLM deception" distinguishes it from cited benchmarks (DeceptionBench, Sycophancy Eval) that do not contrast conditions to perform differential diagnosis. The claim is defensible as written.

- **"Paper never demonstrates pressure condition achieves discrimination"** — Removed because this misunderstands the paper's methodology. The paper's core argument IS the comparative logic: if a model performs identically in MESA and MASK, behavioral changes are absent; if it changes under pressure in goal-conflict scenarios, this constitutes evidence of strategic (rather than capability-based) shifts. The paper makes this case at multiple points (lines 24, 28, 80).

- **Section-by-section notes about "first deception benchmark" and related work positioning** — Removed per the above reasoning.

- **LLM judge stability/reproducibility concern about GPT-4.1 API changes** — Removed as speculative (no evidence the specific version used in the study will change vs. the paper's base claim).

- **Statistical significance and variance (confidence intervals)** — Demoted to Nice-to-Have from a weakness, as single-run large-scale benchmark evaluation without confidence intervals is common practice in this field.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's central insight — that the paper should more carefully distinguish behavioral shift from deception — is a valid framing critique but is already partially addressed by the paper's quadrant system and scenario design.

## Suggestions

1. **Report human-model agreement on the deception classification task.** Have the same expert annotators who performed dataset quality control label a sample of MASK outputs as deceptive or not, and report the agreement rate with GPT-4.1. This single addition would substantially strengthen the paper's central claim about reliable deception detection.

2. **Correct or remove the fine-tuning data.** The epoch-0 values in the table need to be reconciled with Table 1, and the figure axis must be consistent with the table values. If the data cannot be corrected, consider removing this experiment since it is acknowledged as a limited case study and is not central to the paper's contribution.

3. **Reframe the deception definition for clarity.** Explicitly acknowledge that the paper measures behavioral shifts in goal-conflict scenarios that are *indicative* of deception (strategic concealment or misdirection) rather than claiming to detect "intentional" deception, which requires a theory of mind that LLMs do not possess. The existing four-quadrant taxonomy already provides the tools for this more precise framing.

4. **Define the consistency operator "~" in the main text** with at least a summary of the judgment criteria used by GPT-4.1 (e.g., semantic similarity threshold or rubric categories), and clarify the consensus aggregation method for MESA baselines.

## Score and Decision

This paper presents a genuinely promising core idea — the comparative MESA/MASK paradigm — and backs it with a carefully constructed dataset and broad model evaluation. The three major issues (data error in the fine-tuning table, missing human-model agreement for the LLM judge, and the conceptual framing tension) are all fixable and do not invalidate the core contribution. The data error appears to be a transcription mistake in the table rather than a reflection of incorrect conclusions. The paper's primary value — the benchmark, dataset, and comparative framework — stands independently of these issues.

Score of 6 reflects a borderline accept: the contribution is real and useful, but the paper needs corrections before it can be considered reliable science.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>