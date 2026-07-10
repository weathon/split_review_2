Now let me write the final consolidated review.

## Summary

This paper identifies and names the "underthinking" phenomenon in LongCoT reasoning models — where models prematurely switch between reasoning thoughts without sufficient exploration. It proposes SmartSwitch, a training-free, plug-and-play inference framework that detects premature thought-switching via linguistic cues, evaluates the potential of abandoned thoughts using an off-the-shelf Process Reward Model (PRM), and intervenes by backtracking and injecting a "deepen prompt" to encourage deeper exploration. Experiments across five mathematical reasoning benchmarks (AIME24, AIME25, AMC23, MATH-500, GaoKao2023en) and five model scales (1.5B–32B) show substantial accuracy gains alongside counterintuitive reductions in response length and inference time.

## Strengths

- **Clear problem identification with empirical grounding (Section 3).** The paper provides both qualitative (Figure 1a) and quantitative evidence (Figures 1b, 2) for underthinking, showing it correlates with problem difficulty and incorrect answers. The Underthinking Frequency metric, while heuristic, enables systematic cross-model comparison.
- **Elegant and practical method design (Section 4).** SmartSwitch is training-free, model-agnostic, and uses off-the-shelf components (linguistic cues, a PRM). The two-stage perception-intervention loop is conceptually clean, and the plug-and-play nature is a genuine practical advantage over alternatives requiring model modification.
- **Strong and consistent empirical results (Table 1).** Gains are substantial across all model sizes and benchmarks. Examples: DeepSeek-R1-Distill-Qwen-1.5B on AIME24 improves 28.9% → 40.0% (+11.1 points); QwQ-32B on AIME25 improves 63.3% → 73.3% (+10.0 points). Larger improvements on harder benchmarks are consistent with the underthinking hypothesis.
- **Counterintuitive efficiency improvements (Tables 2-3).** SmartSwitch reduces both response length and wall-clock inference time despite PRM overhead (e.g., 33.7% time reduction for the 1.5B model on AIME24), suggesting it prunes wasteful shallow thought-switching rather than simply adding computation.
- **Comprehensive ablation study (Tables 4-8).** The paper systematically ablates PRM choice, process division strategy, score mapping, and threshold sensitivity. The "Always Intervene" baseline (Table 4) degrading performance to 18.9% cleanly demonstrates that selective PRM-guided intervention is critical.

## Weaknesses

### Fatal

None.

### Major

- **Undisclosed threshold selection procedure combined with extreme sensitivity (Table 8).** The paper does not state whether the τ=0.70 threshold was selected on a held-out validation set or directly on the test benchmarks. The sensitivity is extreme — e.g., for DeepSeek-R1-Distill-Qwen-7B on AIME24, τ=0.69 gives 43.3% (worse than vanilla at 55.5%), τ=0.70 gives 66.7%, τ=0.71 drops to 43.3%. The phrasing "selecting the optimal value, such as 0.70 in this case, is crucial" (Section 5.5) reads as post-hoc selection. If the threshold was chosen by examining test-set accuracy, the main results (Table 1) are not unbiased estimates. The authors should clarify this and, ideally, report performance under a principled selection procedure (e.g., a held-out validation split). *(Note: the fact that τ=0.70 is the peak for all five model scales with no per-model tuning is also consistent with genuine robustness — this needs clarification from the authors.)*

### Minor

- **No confidence intervals or variance estimates for any reported metric.** The paper reports pass@1 accuracy averaged over 32 responses but provides no confidence intervals, standard deviations, or any measure of variance. This is particularly salient for the small 30-problem AIME benchmarks, where a 10-point swing corresponds to roughly 3 problems changing status. Without error bars, the statistical reliability of the claimed improvements cannot be assessed. The same issue applies to the response length and inference time comparisons (Tables 2-3).
- **Limited comparison to the most directly relevant prior method (TIP).** The comparison to TIP (Wang et al., 2025) is conducted on only one model (1.5B) and one benchmark (AIME24). While the paper's main claim — that SmartSwitch improves over vanilla inference — is thoroughly validated, the narrower claim that it "outperforms existing underthinking mitigation methods" needs broader support. Extending the TIP comparison to additional models and benchmarks would substantiate this.
- **The Underthinking Frequency metric is a heuristic based purely on token length (Eq. 1), conflating "short" with "prematurely abandoned."** A correct solution that efficiently uses a short reasoning step would be flagged. The paper acknowledges this as a heuristic and uses it only for aggregate analysis, but a small validation study (e.g., human annotation of whether short thoughts are genuinely abandoned prematurely) would strengthen the foundation.
- **No analysis of failure modes where SmartSwitch hurts performance.** Even at the optimal threshold, the paper does not analyze cases where the deepening intervention causes the model to waste time on genuinely unpromising paths or derails correct reasoning. A qualitative analysis of such cases would provide a more balanced picture.

### Trivial

None.

## Nice-to-Haves

- Separately report the overhead of PRM scoring vs. the base model's generation in the wall-clock times (Table 3) to help practitioners budget compute.
- Discuss the practical feasibility of deploying SmartSwitch with closed-source API-based models that do not expose generation state for backtracking.
- The "deepen prompt" is fixed; exploring context-aware dynamic prompts could further improve results.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **Speculative fatal claim**: The critic's suggestion that test-set overfitting *definitely* inflated results. The paper does not state how the threshold was selected, making this a legitimate question, but the consistent peak at 0.70 across all 5 model scales is equally consistent with genuine robustness. The concern is retained as MAJOR (not fatal) with the appropriate caveats.
- **Request for Best-of-N / majority voting / self-consistency / Tree-of-Thoughts baselines**: These are answer-aggregation or prompting-paradigm methods orthogonal to underthinking mitigation; they are not direct competitors and demanding them is scope creep.
- **Concern about DeepSeek-V3 segmentation variability**: The paper mentions this segmentation step. This is a standard delegation to an LLM, not a meaningful gap.
- **Concern about closed-source API support**: The paper evaluates on open-source models where backtracking is feasible; demanding closed-source support is beyond stated scope.
- **Generic strength/superlative content** (e.g., "problem is important") removed to keep strengths concrete and evidence-grounded.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Report the exact validation procedure used for threshold selection. If no validation split was used, re-evaluate the main results under a principled selection procedure (e.g., cross-validation or a reported held-out set).
- Add bootstrap confidence intervals for all main accuracy results (especially AIME24 and AIME25 with 30-problem sizes).
- Extend the TIP comparison to at least one additional model and one additional benchmark.
- Provide qualitative failure-mode analysis showing cases where SmartSwitch's deepening intervention is unhelpful.

## Score and Decision

The paper identifies a genuine and practical problem, offers a clean training-free solution, and validates it across multiple model scales and benchmarks with consistent gains. The main weaknesses — the undisclosed threshold selection procedure and the absence of variance estimates — are real but addressable; they do not invalidate the core contribution. The method's surprising efficiency improvements further strengthen the case. This is a solid empirical contribution that will be useful to the community.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>