## Summary

This paper introduces "persona vectors" — linear directions in LLM activation space that correspond to personality traits such as evil, sycophancy, and hallucination. It presents an automated pipeline for extracting these vectors from natural-language trait descriptions and demonstrates four applications: steering behavior at inference time, monitoring prompt-induced shifts, mitigating finetuning-induced shifts via preventative steering during training, and pre-screening training data for problematic samples. The core contributions are (a) showing that a single linear direction predicts finetuning-induced behavioral changes across diverse datasets, and (b) a novel preventative steering method that preserves general capabilities better than post-hoc inference-time steering.

## Strengths

1. **Unified framework across multiple distinct applications.** The paper extracts one vector per trait and validates it across four substantially different tasks (steering, monitoring, preventative mitigation, and data screening). The finding that the same vector predicts finetuning shifts and can screen data before training is the paper's most impressive and distinctive result (Sections 4 and 6, Figures 4 and 7).

2. **Preventative steering is a novel and practically motivated idea.** Steering the model *toward* an undesirable trait during training (to absorb the drift) rather than correcting afterward is clever and non-obvious. The fact-acquisition case study (Section 5.2, Figure 6) concretely demonstrates why this matters: inference-time steering destroys newly learned facts, while preventative steering preserves them. This is the paper's strongest standalone contribution.

3. **High and consistent correlations across models.** The correlations between finetuning shift and trait expression (r=0.76–0.97, Figure 4) and between data projection difference and post-finetuning trait expression (r=0.88–0.95, Figure 7) replicate across Qwen2.5-7B and Llama-3.1-8B, with within-trait correlations consistently higher than cross-trait baselines.

4. **Transparent reporting of limitations.** The paper honestly reports that monitoring correlations come primarily from coarse prompt-type differences rather than fine-grained detection (Section 3.3), that single-layer preventative steering does not always fully prevent trait acquisition (Section 5.1), and that cross-trait correlations exist (footnote 6). This candor is commendable.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or uncertainty estimates for key comparisons.** The main paper contains no error bars, standard deviations, confidence intervals, or mention of random seeds. The steering plots (Figure 2) show line plots without uncertainty despite aggregating over multiple rollouts. More critically, the central comparisons between preventative and inference-time steering (Figures 5 and 6) show MMLU accuracy as single lines with no variance, making it impossible to assess whether the observed differences are statistically meaningful. While p-values are reported for the correlation analyses (Figures 4, 7), the steering experiments that ground the paper's strongest comparative claim lack any such quantification.

### Minor

1. **Preventative vs. inference-time steering comparison could be framed more carefully.** The paper compares (a) steering *toward* the undesirable trait during training vs. (b) steering *against* it at inference after standard training. These are inherently different interventions applied at different stages — the comparison is practically meaningful (these are two real alternatives a practitioner might choose) but the claimed advantage partially conflates the "preventative vs. post-hoc" axis with the "training-time vs. inference-time" axis. The finding that training under intervention preserves capabilities better than applying intervention cold post-training is genuine and interesting; the framing as a head-to-head method comparison is slightly oversold. This interacts with the variance concern above: without error bars, the magnitude of the claimed advantage is unclear.

2. **Monitoring claim in the abstract is stronger than the evidence supports.** The abstract states that persona vectors "can be used to monitor fluctuations in the Assistant's personality at deployment time" without qualification. The body (Section 3.3) reveals that the reported correlations (r=0.75–0.83) come primarily from distinguishing trait-encouraging vs. trait-discouraging system prompts, with "more modest correlations when controlling for prompt type." The practical utility for detecting *subtle* persona drift — the more realistic deployment scenario — is substantially limited. The headline should more clearly reflect this scope.

### Trivial
None.

## Nice-to-Haves

- **Quantify sample-level detection performance.** Figure 8 shows visually clear separation, but reporting AUC, F1, or precision-recall in the main text would make the data-screening claim concrete rather than visual.
- **Discuss the potential valence confound.** The paper notes (footnote 6) that negative traits (and humor) shift together opposite to optimism, suggesting the vectors may partially capture a general valence/positivity dimension. A brief discussion of whether the effects are trait-specific beyond what a simple valence detector would predict would strengthen the paper.
- **Report computational cost.** The pipeline's cost (Claude generations, multiple forward passes, layer extraction) would be useful for adoption decisions.

## Removed Points

The following points from the input review were removed per the filtering rules:
- **Criticism about human validation being "relegated to an appendix."** The paper explicitly states that human-LLM judge agreement is validated in Appendix D. The parser strips appendices; this content exists in the original submission. Per the hard rules, weaknesses about missing appendix content are removed.
- **Criticism about LLM judge bias potentially inflating correlations.** While a legitimate concern in principle, the paper addresses it by validating against human evaluators (details in the full submission's appendix). The criticism as phrased relied on the absence of information that is present in the full paper.
- **Typo note about "sycomancy."** This is a formatting artifact from PDF parsing; per the hard rules such nitpicks are removed.
- **Suggestion to compare against training with "expectation of later steering" (variant iii).** This is speculative and not a standard practice; the existing comparison between two practical alternatives is appropriate for the paper's scope.
- **General speculation about sycophancy vs. agreeableness.** Not backed by specific evidence that can be verified from the paper.

## Novel Insights

The reviews surface an important calibration point: the paper's strongest contributions are not the steering or monitoring (which extend existing work) but rather (a) the finding that a single linear direction extracted from contrastive prompts predicts training outcomes, and (b) the preventative steering method. The monitoring application is weaker than the abstract implies — detecting explicit pro-trait vs. anti-trait prompts is a coarse capability compared to the subtle drift detection needed in practice. The main methodological gap is the absence of uncertainty quantification for the central comparative claims, which would substantially increase confidence in the results.

## Suggestions

1. Add error bars (standard deviation across multiple seeds/rollouts) to the steering plots (Figures 2, 5, 6), particularly for the MMLU comparisons in the preventative vs. inference-time steering figures.
2. Reframe the preventative steering comparison to accurately characterize it as a comparison between two inherently different intervention strategies (training-time steering vs. post-hoc steering), which is still a practically valuable comparison.
3. Temper the monitoring claim in the abstract to reflect that the method is effective for detecting coarse, explicit prompt-induced shifts but has limited sensitivity for subtle behavioral changes.
4. Report AUC or similar metrics for the sample-level data screening (Figure 8) in the main text.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>