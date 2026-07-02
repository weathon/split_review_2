## Summary

This paper proposes TRACE (Truncated Reasoning AUC Evaluation), a method to detect implicit reward hacking in LLMs by measuring reasoning effort. The key insight is that a model exploiting a loophole can achieve high reward with only a small fraction of its chain-of-thought, while a legitimate solver needs the full CoT. TRACE operationalizes this by progressively truncating the CoT, forcing early answers, and computing the AUC of expected reward versus CoT percentage. The method is evaluated on math (Big-Math-Verified) and code (APPS) with both in-context and reward-model loopholes across 1.5B–14B models, showing large F1 gains over CoT monitoring baselines.

## Strengths

1. **Genuinely novel method with a clean, well-motivated intuition.** The core idea — that hacking shortcuts should be detectable because the model can obtain the reward earlier in its CoT than a legitimate solver — is distinct from prior work and clearly operationalized through progressive truncation + AUC. This is not a thin variant of an existing technique.

2. **Training-time monitoring result (Figure 8) is the paper's strongest evidence.** TRACE score rises sharply at the point where RL training begins to exploit the loophole, while CoT length and KL loss move indistinguishably between hacking and non-hacking models. This directly demonstrates that TRACE captures signal that standard diagnostics miss.

3. **Breadth across domains and loophole types.** Evaluation spans math and code, in-context and reward-model loopholes, and multiple model scales (1.5B–14B), lending credibility to the claim that TRACE is not an artifact of a single setup.

4. **Honest and thorough treatment of limitations.** The Discussion section (Section 7) candidly addresses overthinking confounds, CoT optimization pressure (that TRACE would be evaded if used as a training signal), threshold calibration difficulties, and cases where the initial policy already hacks. This candor is commendable and makes the paper's claims easier to evaluate critically.

## Weaknesses

### Fatal
None.

### Major

1. **RL training results are reported from single seeds with no variance.** The paper trains hacking and non-hacking models using RLOO, which is sensitive to random seed, especially given the small training sets (896 examples for code). There is no mention of multiple seeds, no error bars on the training curves (except Fig. 13 which shows "confidence intervals" without describing their computation), and no statistical tests on the F1 comparisons. The bar charts in Figures 9 and 10 report F1 as point values. Without variance information, we cannot assess whether the reported F1 differences are reproducible or could vary substantially across seeds.

2. **The central confound — increased TRACE score from competence improvement vs. hacking — is acknowledged but not experimentally controlled.** TRACE scores could rise during RL training because (a) the model becomes more efficient at genuine reasoning and answers earlier, or (b) the model learns to "overthink" on easy samples, inflating the denominator of the AUC. The paper acknowledges overthinking (Section 7) but provides no experiment isolating these effects. Figure 8 compares a hacking model (trained with loopholes) against a non-hacking model (trained without loopholes), but the two models train on different data distributions, so the comparison does not rule out competence-driven TRACE increases. A control experiment — training a model on the same loophole data but with a clean reward function, then measuring its TRACE change relative to the hacking model — would substantially strengthen the central claim.

### Minor

3. **Evaluation relies on ground-truth labels constructed using knowledge of the specific loophole mechanism.** Hacking samples are defined via counterfactual tests (Section 3.2) that require knowing the exact loophole (wrong hint for IC, clean verifier for RM). This is necessary for evaluation in a synthetic setup and is standard practice, but it means the experiments measure TRACE's ability to agree with labels derived from known loophole structures. The gap between this synthetic evaluation and real deployment (where the loophole is unknown and no counterfactual test exists) is acknowledged but not addressed. This limits the strength of the generalization claims.

4. **The "loophole discovery" case study (Section 5) is a proof-of-concept that demonstrates only the most obvious pattern.** K-means clustering on TRACE scores followed by LLM prompting surfaces the question-ID loophole — a synthetic pattern where the answer is literally the problem number. The comparison to CoT-monitor-based clustering shows the CoT monitor finds different (but not clearly wrong) patterns. The paper frames this as a proof-of-concept and acknowledges real loopholes may need more sophisticated techniques (line 274), so no overclaiming occurs, but the demonstration does not provide evidence that TRACE-based clustering can discover subtle or non-obvious loopholes.

5. **The detection threshold ("average TRACE score of the initial policy") is underspecified.** The paper states the threshold (line 204) but does not specify how it is applied — whether as a hard cutoff (any sample above the average is hacking), whether mean + k standard deviations is used, or whether it is calibrated on a validation set. The classification results in Figures 9–12 depend on this threshold, and the procedure should be clearly reported.

6. **No matched-cost comparison with the CoT monitor.** TRACE requires multiple forward passes per sample (multiple truncation points × multiple samples per point), while the CoT monitor requires one. The paper's headline claims ("over 65% gains over 72B CoT monitor") do not report relative compute cost. The argument that TRACE needs no external monitor is valid, but the efficiency dimension is unquantified.

7. **Code evaluation uses a small dataset (896 training examples) with partial overlap between training and detection sets.** The detection set (2297 samples) includes both training and held-out data. The consistency of the code results with the math results (which use a much larger dataset) mitigates this concern, but the code evaluation's statistical power is limited.

8. **The definition of "implicit hacking" (CoT is "unfaithful") is assumed rather than independently verified for the examples.** The paper defines implicit hacking as occurring when the CoT is unfaithful (line 52), but the ground-truth labeling relies on counterfactual tests (outcome-based) rather than directly verifying CoT unfaithfulness. The examples in Figure 3 show CoTs that contain plausible reasoning alongside a wrong final answer — whether these are genuinely "unfaithful" (the model knew the correct answer but fabricated reasoning) or simply erroneous is not independently validated.

### Trivial

None.

## Nice-to-Haves

- A control experiment that trains a model on the same loophole-containing data but with a clean reward function, measuring TRACE change relative to the hacking model. This would isolate the "effort" confound directly.
- Multiple seeds with reported variance (even 3 seeds with error bands) for the RL training results.
- A compute-cost comparison (estimated FLOPs or tokens processed per sample for TRACE vs. the CoT monitor).
- A discussion of why the 72B CoT monitor achieves near-chance F1 (0.395) on RM loopholes in math — whether this reflects task difficulty or suboptimal prompting.
- The temperature asymmetry between math (temperature 0.7, 5 samples) and code (temperature 0, single sample) could be justified more explicitly.

## Removed Points

These points from the input review were removed with brief justifications:

- *"No analysis of failure modes"* — Removed as generic; the paper acknowledges overthinking and initial-policy hacking as failure modes.
- *"Code IC F1=0.050 is suspiciously low"* — Removed because this is a question about baseline performance, not a weakness of the proposed method.
- *"Missing truncation point details"* — Removed as a trivial presentation issue; figures show example truncation points.
- *"CoT monitor finding different patterns in case study is not clearly wrong"* — Removed because the paper frames this as a comparison, not as a claim that the CoT monitor is wrong.
- *"If TRACE were used as training signal models would learn to evade it"* — Removed because the paper explicitly discusses this in Section 7 ("CoT Optimization Pressure") and treats TRACE as a detection-only method.

## Novel Insights

None beyond the paper's own contributions. The input review's most valuable observation is that the evaluation's ground-truth labels are intrinsically tied to known loophole structures (weakness #3 above), which creates a gap between synthetic and real-world deployment that is acknowledged but unaddressed. The review also correctly identifies the single-seed training as the most pressing methodological gap (weakness #1). Neither observation is novel to this review, but their joint emphasis helps calibrating expectations: the paper's contributions are real but are best read as a promising proof-of-concept rather than a fully validated deployment-ready method.

## Suggestions

1. **Report results from at least 3 RL seeds** with error bars on the key F1 comparisons (Figures 9–12). This is the single most impactful improvement for the quantitative claims.
2. **Add a control experiment** where a model trains on the same loophole-containing data but with a clean reward function, measuring its TRACE change to isolate the effect of hacking from competence improvement.
3. **Specify the exact thresholding procedure** used for classification (e.g., "a sample is classified as hacking if its TRACE score exceeds the mean TRACE score of the initial policy on a held-out set of clean examples").
4. **Include a compute-cost comparison** — approximate FLOPs or tokens per sample for TRACE vs. the CoT monitor — to substantiate the scalable oversight argument.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>