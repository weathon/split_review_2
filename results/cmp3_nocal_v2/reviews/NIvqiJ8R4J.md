## Summary

PELICAN proposes a two-stage adaptive tutoring framework: (1) a collaborative cognitive diagnosis stage that uses a successor-first strategy with an expert-assistant-verifier pipeline to assess a student's knowledge state, and (2) an adaptive tutoring stage that selects teaching strategies via a dual-system-inspired fast/slow thinking mechanism (including a simulated teaching tree for slow thinking). The framework is evaluated on the Gaokao dataset with simulated students and in a real deployment with 169 high school students.

## Strengths

- **Concrete, well-motivated problem framing.** Figures 1 and 2 ground the core failure mode concretely: a single correct LLM response that is simultaneously too hard for a weak student and too basic for a strong one, followed by three distinct tutoring trajectories at different cognitive levels. This clearly illustrates why cognitive-state-aware tutoring matters.

- **Real human evaluation at nontrivial scale.** The deployment with 169 high school students and 1,335 tutoring reports (Section 4.6, Table 6) provides genuine practical validation that goes well beyond the simulated experiments. Many papers in this space evaluate only with LLM-simulated students, making this a meaningful differentiator.

- **Strategy distribution analysis (Figure 4).** The breakdown of teaching strategies used for each cognitive level shows that decomposition and analogies are used more for low-level students while questioning is preferred for high-level students. This adaptive behavior is exactly what the framework is designed to produce, and demonstrating it with data is a meaningful sanity check.

## Weaknesses

### Fatal
None.

### Major

- **Abstract makes quantitative claims unsupported in the paper body.** The abstract reports *"significant improvements in critical thinking stimulation (+18.7%) and task completion rates (+22.4%) compared to baseline models."* These two numbers appear **nowhere** in the paper's experimental sections. Table 2 (simulated GPT-based metrics) shows PELICAN Inspiration = 4.21 vs. Free-Prompt = 2.42—a relative increase of ~74%, not 18.7%. Table 6 (human evaluation) shows PELICAN success rate = 86.8% vs. Free-Prompt = 85.2%—a 1.6 percentage-point difference, not 22.4%. No table, metric definition, or experiment description in the body supports the abstract figures. Even if these numbers are located in the stripped appendix, placing headline quantitative results in the abstract that cannot be identified or verified from the main paper is a serious framing failure.

- **Unexplained ~17.5-point discrepancy in PELICAN's own R_coverage between main results and ablation.** Table 2 (main results) reports PELICAN's R_coverage = 72.36 (±4.69). Table 3 (ablation) reports PELICAN's R_coverage = 54.84. The same method differs by ~17.5 points on the same metric with no explanation. For context, this gap is larger than the advantage PELICAN claims over any baseline. The paper states the ablation is on "stage-1 and slow-thinking" but does not clarify whether different data, question subsets, or experimental conditions were used. This inconsistency undermines confidence in the experimental methodology.

- **GPT-based evaluation circularity and suspiciously tight standard deviations.** The base LLM for PELICAN is GPT-4o, and the "GPT-based assessments" (Suitability, Logic, Inspiration, Reliability, Overall) are also conducted by a GPT-family model (the paper does not specify which model). This places the same model family in the roles of both the tutor and the judge of tutoring quality. The reported standard deviations in Table 2 are suspiciously tight (e.g., ±0.003 for Overall, ±0.002 for Inspiration, ±0.006 for Reliability)—orders of magnitude smaller than the R_coverage SDs (±4.69, ±3.42). This pattern is consistent with a judge that gives near-identical scores across runs, raising doubts about whether these metrics have the discriminative power to support fine-grained comparisons between methods.

### Minor

- **Main experimental results are from simulated, not real, students.** The Gaokao dataset experiments (Tables 1–5) use LLM-simulated students whose cognitive levels are initialized programmatically (Section 4.4: "for each math question … we initialize three different cognitive levels for the students"). Simulated students never get distracted, bored, or frustrated, and they respond deterministically to scripted knowledge states. The human evaluation (Table 6) provides real-world validation, but the effect sizes are smaller and the metrics do not directly replicate the simulated findings. The paper's strongest comparative claims rest on simulation data.

- **In the ablation (Table 3), the "w/o. Diagnosis & slow" condition achieves the highest Inspiration score (4.56 vs. 4.30 for full PELICAN).** Removing both cognitive diagnosis and slow thinking should theoretically produce less inspiring responses. The paper notes this result but does not explain it, which suggests either noise in the GPT-based evaluation or a systematic bias in the judge that is not accounted for.

- **Qwen-max outperforms GPT-4o-based PELICAN on R_coverage (64.41 vs. 54.84) in Table 4.** The paper claims "all models perform well" but does not explain why a weaker-on-paper model substantially outperforms GPT-4o on a key strict metric. This may indicate that R_coverage is sensitive to model-specific generation styles rather than the framework's diagnostic/tutoring capability.

- **Human evaluation (Table 6) lacks statistical significance reporting.** The headline comparison (PELICAN 86.8% vs. Free-Prompt 85.2%) is a 1.6pp difference. No confidence intervals, p-values, or standard deviations are reported for this table, unlike the simulated experiments (Table 2). Given that this is the only direct evidence of real-world effectiveness, variance or significance information would substantially strengthen the claims.

### Trivial

- **The slow-thinking activation threshold is set to M=1** (Section 4.1), meaning slow thinking activates after a single round of fast thinking on any sub-task. This largely eliminates the "fast" path and contradicts the paper's narrative that slow thinking is reserved for "persistent cognitive obstacles." This is a minor implementation/parameterization choice that deserves clarification but does not affect the core contribution.

## Nice-to-Haves

- **Report token/session usage for all baselines** (not just for PELICAN alone). The paper notes that slow thinking consumes ~230k tokens (~40% of total) but does not compare this against baseline methods, making cost-effectiveness assessment impossible.

- **Discuss failure cases and limitations.** The conclusion is uniformly positive. The paper would benefit from acknowledging when and why the system fails—e.g., whether very low-knowledge students still benefit, or whether the simulated teaching tree ever selects poor strategies.

## Removed Points

These points were flagged for removal but are listed here for completeness:

- **"Diagnostic accuracy not evaluated on real students"** — Removed because real students lack ground-truth knowledge states, making this an unreasonable requirement.
- **"No head-to-head comparison of slow-thinking tree search cost"** — Moved to Nice-to-Haves above; it is not a weakness but a missing analysis.
- **"No discussion of failure cases"** — Moved to Nice-to-Haves; common in papers and not a decisive weakness.
- **"Simulated students are fundamentally different from real students" framed as a fatal/critical issue** — The paper already includes a real human evaluation (Section 4.6), which partially addresses this concern, so it is downgraded to Minor rather than treated as structural.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a clear pattern: the paper's content is stronger than its presentation. The framework design and human evaluation are genuine contributions, but the unsupported abstract numbers and unexplained experimental inconsistency (R_coverage gap between Tables 2 and 3) are presentation/analysis errors that the reviews correctly identify without introducing new synthetic insights.

## Suggestions

1. **Ground the abstract claims.** Either delete the +18.7% and +22.4% numbers from the abstract or explicitly identify which table/metric/baseline they correspond to in the paper body.
2. **Explain the R_coverage discrepancy between Tables 2 and 3.** If the ablation was run on a different data subset, state this explicitly and, ideally, re-run the ablation under conditions comparable to Table 2.
3. **Validate the GPT-based judge.** Provide evidence of calibration against human annotations (e.g., inter-annotator agreement), or use a held-out judge from a different model family, or report how scores correlate with the human evaluation results already collected.
4. **Add significance tests or confidence intervals to the human evaluation (Table 6).** The 1.6pp success-rate advantage over Free-Prompt needs statistical characterization to support the claimed superiority.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>