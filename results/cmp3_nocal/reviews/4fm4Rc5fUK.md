## Summary

This paper proposes ATF (Autoformalizer with Tool Feedback), a training framework that integrates Lean 4 compiler feedback and a multi-LLM consistency judge as tools into the autoformalization process. The pipeline has three phases: cold-start distillation from Claude-4 to teach tool-use format, expert iteration with real tool feedback, and DPO to reduce ineffective revision attempts. ATF-32B achieves substantial gains over existing formalizers across three benchmarks (e.g., +29.13% consistency on CombiBench vs Goedel-V2-Formalizer-32B), and ATF-8B-Distilled outperforms all 32B baselines. Human evaluation corroborates the relative rankings.

## Strengths

1. **Well-motivated problem framing with concrete failure modes.** The paper identifies two specific issues—syntactic errors from limited formal knowledge and subtle semantic misalignments from unreliable consistency checking—and grounds them in concrete examples (Figure 1's birthday-paradox case with quantifier confusion and modulo errors). This is specific rather than generic.

2. **Thoughtful three-phase training design.** The cold-start → expert iteration → DPO pipeline has clear motivation behind each stage, and the ablation study (Table 4) confirms that each phase contributes cumulatively. The DPO phase targeting repeated identical errors addresses a genuine failure pattern observed during development.

3. **Large and consistent empirical margins.** ATF-32B's gains over Goedel-V2-Formalizer-32B are substantial across all three benchmarks: +9.1%, +10.08%, and +29.13% on consistency Pass@1. ATF-8B-Distilled outperforms all 32B baselines on every metric at every Pass@k level. These margins are large enough that a real effect is clearly present even accounting for evaluation artifacts.

4. **Human evaluation confirms the relative ranking.** Although limited to 100 samples per benchmark, the human evaluation shows the same ordering as the automated metric (ATF-32B > Goedel-V2-32B > others), and the reported Pearson correlation of 0.746 between tool-based and human judgments supports the tool's utility as a ranking signal.

5. **Inference scaling analysis (Section 5.1).** ATF's performance continues to improve with more revision attempts beyond its training limit of 8, suggesting the model has learned revision strategies that generalize—a non-trivial property.

## Weaknesses

### Fatal

None.

### Major

1. **The consistency check tool is used both for training data filtering and as the primary evaluation metric, creating a circularity.** The multi-LLM-as-judge ensemble (QWQ-32B + Qwen3-32B) is used to (a) filter successful trajectories during expert iteration training data collection, and (b) compute the CC metric in Table 3. Because ATF is explicitly trained to produce statements this specific judge finds consistent, while baselines were not, a gap in CC scores could partially reflect learned conformity to the judge's preferences rather than genuine semantic superiority. This is acknowledged only briefly ("Considering the limitations of LLMs-as-judge... we further conduct human evaluation"). The human evaluation on 100 samples/benchmark mitigates this but does not fully resolve it—a held-out judge that never appeared in training would provide cleaner evidence. (See Table 3 for the CC metric; Section 4.1 for the acknowledgment; Section 3.2 for how training uses the check.)

2. **The 8B distillation process is never described.** ATF-8B-Distilled outperforms all 32B baselines on every metric—a striking result—but the paper only states "we also train an ATF-8B-Distilled using the same data" (Section 4.1). It is unclear whether this uses the same three-phase pipeline on a Qwen3-8B base, whether it distills ATF-32B's outputs, or what architectural/training differences exist. This is a significant reproducibility gap for the paper's most surprising efficiency claim.

### Minor

1. **The consistency check tool's ~40% false negative rate is not analyzed for its impact on training.** Table 1 reports Ensemble Vote FNR = 0.4033. This means roughly 40% of semantically consistent formalizations are discarded during expert iteration training, biasing the training distribution toward statements that match the specific preferences of QWQ-32B and Qwen3-32B. The paper acknowledges the tool is strict but does not quantify how many valid trajectories are discarded or what effect this has on the learned policy.

2. **The decontamination procedure is underspecified.** Section 4.1 mentions "similarity-based decontamination" but does not report the similarity metric, threshold, or number of training examples removed per evaluation set. Since the training data (NuminaMath-1.5) and evaluation sets (e.g., AIME problems in FormalMath-Lite) share mathematical sources, this matters for interpreting results.

3. **No statistical uncertainty is reported for Table 3.** The main results lack confidence intervals or bootstrap estimates, making it difficult to assess whether the large margins are statistically reliable, especially for the smaller human evaluation (n=100).

### Trivial

None.

## Nice-to-Haves

- **Add a tool-augmented baseline.** Comparing ATF against a strong baseline (e.g., Goedel-V2-Formalizer-32B) that receives the same inference-time tool access (syntax + consistency feedback with iterative refinement) but without ATF-specific training would isolate how much of ATF's gains come from the training pipeline versus the general availability of tools.
- **Use a held-out judge for evaluation.** Employing a different judge model (e.g., Gemini-2.5-Pro or Claude-4) exclusively for evaluation, never seen during training, would break the circularity concern cleanly.
- **Quantify the FNR impact on training data.** Estimate how many valid formalizations are discarded per iteration and show that models trained on data filtered by a lower-FNR judge perform similarly.

## Removed Points

These points from the input review were removed with justification:

- "The 63%/37% failure rate is presented as though it's a known fact" — The Figure 1 caption explicitly attributes this to Kimina-Autoformalizer operation. It is an empirical observation, not a false claim. The duplication of captions (lines 47-51) is a PDF parser artifact, not an author error.
- "Why use weaker open-source judges rather than Claude-4 or Gemini?" — The paper benchmarks QWQ-32B and Qwen3-32B, finds the ensemble effective, and explains the choice. Questioning it is a subjective preference, not a flaw.
- "Cold-start should be described as distillation, not teaching" — Semantics; the paper describes the process transparently. Not a substantive weakness.
- "The DPO uses the check as a reward signal" (framing in input) — The paper's DPO selects positive/negative pairs based on revision attempt count difference (both trajectories passed the check), not on passing vs failing. The reviewer's framing was somewhat inaccurate.
- "The larger tool-human gap for ATF on CombiBench suggests overfitting to the judge" — The differential gap is only 2.13 points on one of three benchmarks; on FormalMath-Lite and ProverBench the pattern does not hold. The evidence is too weak to support the inference.
- "The OOD claim needs qualification since CombiBench overlaps with olympiad training data" — The paper acknowledges the relative nature by calling it "out-of-distribution scenarios" and noting CombiBench "contains diverse combinatorial mathematics problems" that differ from the training distribution. This is sufficiently qualified.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. In the final version, add a section describing the ATF-8B-Distilled training procedure (base model, pipeline stages, data) to support the striking efficiency result.
2. Explicitly acknowledge the evaluation circularity in the limitations section and, if possible, report results against a held-out judge that was never used during training.
3. Report the decontamination threshold, similarity metric, and counts of removed examples.
4. Add confidence intervals (e.g., bootstrapped 95% CIs) to the main results in Table 3.
5. Include a tool-augmented baseline ablation to disambiguate training effects from tool-access effects.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>