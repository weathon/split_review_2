## Summary

This paper introduces three contributions for multimodal process reward modeling: (1) VisualPRM400K, a ~400K multimodal process-supervision dataset with step-wise correctness annotations (~2M steps); (2) VisualPRM, an 8B multimodal PRM trained on this dataset; and (3) VisualProcessBench, a human-annotated benchmark (2,866 samples, 26,950 step labels) for detecting step-level errors in multimodal reasoning. Experiments show that VisualPRM improves Best-of-N reasoning across 7 benchmarks, 4 model families, and 6 model scales, while the benchmark reveals that existing open-source MLLMs perform near chance at step-level error detection.

## Strengths

1. **First large-scale multimodal process-supervision dataset with thorough evaluation.** PRM800K and MathShepherd exist for text-only math, but extending process supervision to vision-language reasoning is a natural and practically important direction. The paper demonstrates consistent improvements across 7 benchmarks, 4 model families, 6 model scales (Table 2), with gains not limited to one family — MiniCPM-V2.6 (+8.0), Qwen2.5-VL-7B (+3.7), InternVL2.5-8B (+8.4), InternVL2.5-78B (+5.9). Ablations in Figure 4 further show PRM scaling better than ORM and Self-Consistency as N increases.

2. **Carefully constructed human-annotated benchmark.** VisualProcessBench has 2,866 samples with 26,950 human-annotated step labels from 13 annotators (39 person-days, 10% author review per split), sourced from 5 multimodal reasoning benchmarks (MMMU, MathVision, MathVerse, DynaMath, WeMath) and solutions from 5 different MLLMs (GPT-4o, Claude-3.5-Sonnet, Gemini-2.0-Flash, QvQ-72B-Preview, InternVL2.5-78B). The "skip-if-unsure" mechanism and the requirement to detect all erroneous steps (not just the first) are sensible design choices.

3. **Consistent evidence of generalization.** Table 5 shows the PRM improves text-only reasoning on GSM8K, MATH-500, and GPQA-Diamond, suggesting the model learned something about reasoning quality beyond visual patterns. The finding that open-source MLLMs cluster near random guessing (F1=50) on VisualProcessBench (Table 3), while the trained 8B VisualPRM outperforms GPT-4o (62.0 vs. 60.3), validates the core premise.

## Weaknesses

### Fatal

None.

### Major

1. **The automated data labeling pipeline uses an extremely permissive threshold (mc_i > 0) that likely introduces substantial label noise, and the paper provides no direct validation of label quality.**

   The paper labels a step as "correct" if at least 1 out of 16 Monte Carlo continuations from that step yields a correct final answer (lines 104, 118, 154). A genuinely wrong step with true expected accuracy of 3% would be labeled correct with probability ~38% (1 − (0.97)^16). The paper acknowledges noise as the reason advantage-based PRMs underperform (line 269: "We attribute this to the inherent noise in our training data"), yet does not provide direct evidence of label quality — e.g., a human evaluation of a random sample of automated labels. The consistent downstream improvements suggest useful signal is learned despite the noise, but the dataset's quality claims are weakened without this validation. The authors mention trying a stricter threshold (Section B, stripped by parser) but report it negatively impacted performance.

2. **The training data source is under-described, raising concerns about coverage and contamination.**

   VisualPRM400K relies entirely on MMLR v1.1 / MMRP v1.1 (Wang et al., 2024c) — a dataset not widely known or accessible in the same way as standard vision-language benchmarks. The paper does not describe: what domains/topics the questions cover, the number of unique image-question pairs, the difficulty distribution relative to evaluation benchmarks, or whether there is any overlap with the evaluation benchmarks (a contamination concern). Additionally, there is a naming inconsistency: the abstract (line 21) refers to "MMRP v1.1" while Section 3.1 (line 130) refers to "MMLR v1.1" for the same citation.

### Minor

3. **The PRM vs. ORM comparison conflates label definition with model architecture.** The ORM is described as using "nearly identical data except that all steps are concatenated into a single step, and step-wise correctness annotations are converted into a single correctness label for the outcome" (lines 242–267). It is unclear whether this "single correctness label" is based on final-answer correctness or step-aggregation (all steps correct → solution correct). An ORM trained on step-aggregated labels would be a cleaner comparison to isolate the benefit of step-wise supervision from the benefit of different label signals.

4. **No statistical significance or variance information.** All results are reported as point estimates. The gap between VisualPRM (62.0) and GPT-4o (60.3) on VisualProcessBench (Table 3) is modest and could reflect noise; bootstrap confidence intervals or error bars would strengthen the claim. This is a common omission in large-scale benchmark evaluations but worth noting given the narrow margins for some comparisons.

5. **Neutral step handling in VisualProcessBench metrics could be more transparent.** Neutral steps (2,674/26,950 = 9.9%) are excluded from F1 computation (line 236). It is unclear how models are evaluated on these steps — are they penalized for classifying a neutral step as correct or incorrect? The paper should clarify the metric's treatment of neutral steps during model evaluation.

### Trivial

- The paper uses both "MMRP v1.1" (abstract) and "MMLR v1.1" (Section 3.1) for the same citation. This naming inconsistency should be resolved.
- The computational cost of data construction (~36M model inferences) is not reported, which would be useful for practitioners assessing whether the pipeline is practical.
- The step-merging heuristic ("evenly merge the steps if the number exceeds the threshold") is described too briefly for exact reproducibility.

## Nice-to-Haves

- Add a human evaluation of a random sample (200–500 steps) of automated labels in VisualPRM400K to directly validate label quality and quantify agreement rates.
- Report benchmark contamination checks between VisualPRM400K training data and the seven evaluation benchmarks / VisualProcessBench.
- Clarify the ORM label definition (final-answer correctness vs. step aggregation) and optionally add a variant using step aggregation for a cleaner comparison.
- Report per-split variance or confidence intervals for VisualProcessBench results.
- Report the computational cost (GPU-hours) of data construction.

## Removed Points

These points from the input review have been filtered:

1. **"Figure 1 table numbers inconsistent with Table 2"** — Removed per Hard Rules (parser artifact from alt-text extraction, not author error).
2. **"Figure 4 caption mislabels two lines as VisualPRM-8B"** — Removed per Hard Rules (parser artifact from alt-text extraction; the rendered figure likely has correct labels).
3. **"Missing related work / references"** — Removed per Hard Rules (cannot confirm missing references without external sources).
4. **"MLLM-as-a-Judger comparison is apples-to-oranges"** — Removed because the paper's comparison between a prompted MLLM and a trained PRM is an informative benchmark evaluation, not a controlled ablation. The paper frames this as a demonstration of the benchmark's challenge, not a controlled comparison.
5. **"Step-merging heuristic too vague"** — Moved to Trivial.
6. **"The paper should report whether models are penalized for classifying neutral steps"** — This is partially addressed in Minor #5 (transparency request), but the original framing as a metric flaw is removed since the paper explicitly states neutral steps are excluded.

## Novel Insights

The most striking finding is that open-source MLLMs cluster near the random-guessing baseline (F1=50) on step-level error detection (Table 3), while the trained 8B VisualPRM outperforms GPT-4o (62.0 vs. 60.3) on this task. This validates the core premise that process-supervision data is critical for building effective multimodal critics. Also notable: the PRM's gains extend to text-only reasoning (Table 5), suggesting the model learns reasoning quality features that transfer across modalities — a finding that strengthens the case for multimodal process supervision as a general approach to reasoning enhancement.

## Suggestions

1. Add a human evaluation of automated labels in VisualPRM400K to directly quantify label quality and address the noise concern.
2. Add contamination analysis between VisualPRM400K training data and evaluation benchmarks.
3. Clarify the ORM label definition and, optionally, add a step-aggregation ORM variant.
4. Resolve the MMRP/MMLR naming inconsistency and provide more statistics about the training data source.
5. Add confidence intervals or error bars for key comparisons, especially on VisualProcessBench.

## Score and Decision

**Score: 6.5** — The paper sits between OpenPRM (avg 6.0, comparable PRM dataset/model paper with less thorough evaluation) and MMAD/VL-ICL Bench (avg 6.5, benchmark papers with similar evaluation breadth). The contributions are genuine (first large-scale multimodal PRM dataset + trained model + human-annotated benchmark) with consistent and extensive experimental validation. The main limitations — label noise in the automated pipeline and under-described training data source — are real but bounded: the consistent empirical results suggest useful signal is learned despite the noise, and the limitations are honestly acknowledged. The paper fills a genuine gap and the open release commitment maximizes community utility.

**Decision: Accept**

Calibration anchors used:
- OpenPRM (avg 6.0, Round 1+2) — text-only PRM data+model paper; less thorough evaluation
- MMAD (avg 6.5, Round 2) — benchmark+eval in niche domain; comparable scope
- MMMU-Pro (avg 5.8, Round 1+2) — benchmark-only; less contribution breadth
- ToolComp (avg 5.4, Round 1) — smaller-scale benchmark+PRM paper
- MEGA-Bench (avg 7.0, Round 2) — large-scale multimodal benchmark; different focus
- RM-Bench (avg 8.0, Round 1) — higher tier, different focus (style bias in RMs)
- OmniBench (avg 5.75, Round 2) — tri-modal benchmark; rejected
- VL-ICL Bench (avg 6.5, Round 1+2) — multimodal ICL benchmark

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>