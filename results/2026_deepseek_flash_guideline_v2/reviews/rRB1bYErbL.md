## Summary

R-HORIZON proposes a query-composition method that chains single problems into multi-step interdependent reasoning tasks. This method is used to construct a benchmark spanning 6 datasets (math, code, agent tasks) and to generate training data for RLVR. Evaluation of 26 LRMs shows consistent, severe performance degradation as the number of composed queries increases. RLVR training on R1-Qwen-7B with composed data improves both multi-horizon and single-problem performance (e.g., +7.5 on AIME24).

## Strengths

- **Systematic evaluation across diverse models and tasks** — 26 LRMs from 1.5B to 235B+ (including API models like o4-mini, Gemini-2.5-Pro, Claude-Sonnet-4) tested on 6 datasets covering math, code, and agent tasks. The consistent degradation pattern across this range strengthens the claim that the limitation is structural and not an artifact of a single model family or task type. For instance, DeepSeek-R1 drops from 87.3% to 24.6% on AIME25 from n=1 to n=5 (Figure 3).

- **Training with composed data improves both multi-horizon and single-horizon accuracy simultaneously** — Table 1 shows that R1-Qwen-7B trained on n=2 composed queries improves AIME24 from 48.3→65.4 (single-problem) and from 16.4→34.1 (multi-horizon). Many augmentation techniques trade off performance on one distribution for another; R-HORIZON training data improves both.

- **Quantified effective-reasoning-length boundaries** — Section 5.1 identifies concrete token-range thresholds where models begin to fail: 4–6k tokens for 7B models and 8–10k for 32B models on MATH500 (Figure 6). This is a measurable bottleneck for future research.

- **Rollout efficiency gains during RL training** — Figure 10 shows that training with composed data (n=4) increases the proportion of effective training samples by ~20 percentage points compared to n=1 data by step 600, a practical efficiency benefit for the training pipeline itself.

- **Error-type taxonomy with quantitative decomposition** — Figure 5 breaks failures into four categories (Problem Reasoning Error, Dependency Reasoning Error, Early Stop, Output Truncation) and tracks how their proportions shift as the horizon grows, providing diagnostic insight beyond aggregate scores.

- **Clear distinction from prior multi-problem benchmarks** — Section 2.2 explicitly differentiates R-HORIZON from NEST (independent concatenation) and GSM-Infinite (long-context input), positioning it in the short-input/long-output setting with meaningful inter-problem dependencies.

## Weaknesses

### Fatal

None.

### Major

- **Duplicate model entries and an impossible accuracy value in the main evaluation table (Figure 3).** Two distinct rows are both labeled "Qwen3-32B" (lines 157 and 162) with substantially different values. The row at line 157 reports **127.6%** accuracy on MATH500 at n=4 — a physically impossible value for an accuracy metric capped at 100%. In the corresponding second half of the table (AMC23 onward, line 186), only one "Qwen3-32B" appears along with a separate "Qwen3-8B" entry (line 191), suggesting a labeling or data corruption issue. The authors must clarify which model each row corresponds to, whether the 127.6 is a typo or a corrupted data point, and whether any other entries are similarly affected. While the overall degradation trend is so strong and consistent across the remaining 25 model entries that this single corrupted row does not invalidate the paper's core finding, it undermines confidence in the tabulated results and must be fully resolved.

- **RL training experiments conducted on a single base model (R1-Qwen-7B) with no evidence of generalization.** All training results (Table 1, Figures 4, 9, 10) use R1-Qwen-7B as the sole substrate. The degradation analysis (Section 4.2) itself shows that 7B models behave qualitatively differently from larger models (e.g., 7B models hit 0% at n=16 while 32B+ models retain measurable signal). Without at least one additional experiment on a larger model (e.g., R1-Qwen-32B) or a different 7B-family model, the claim that "training with R-HORIZON data is a highly efficient training approach" remains a suggestive case study rather than a demonstrated general finding.

### Minor

- **The "expected accuracy" metric (Eq. 4) uses a product of independent pass rates that conflates multiple sources of degradation.** The gap between actual accuracy and ∏p_i is interpreted as evidence of "limited effective reasoning length," but the composition introduces additional task demands (increased cognitive load from managing multiple sub-problems, error propagation through output formatting, etc.) that are not specifically about reasoning length. This does not invalidate the benchmark, but it weakens the precise mechanistic interpretation of the gap.

- **No variance or uncertainty reporting in the main evaluation table (Figure 3).** Point estimates are reported without confidence intervals or standard deviations. Given the all-or-nothing scoring (Eq. 3), which can produce high variance at larger n, this limits assessment of the reliability of individual entries.

- **The key variable verification model M (Eq. 2) is not specified or analyzed for accuracy.** The paper uses an unspecified model M to determine whether an integer is a "key variable" whose removal would make a problem unsolvable. The accuracy of this verification is not discussed, nor is the choice of M reported. If M has low precision, composed problems may be trivially solvable without using the intended dependency, undermining the benchmark.

- **Training data filtering by expected accuracy > 0.25 creates a distribution mismatch.** Section 4.3 notes that training data consists of relatively easy combinations (Acc_expected > 0.25), while the evaluation benchmark includes much harder combinations (e.g., AIME with n=5 where even strong models score ~25%). This mismatch between training and evaluation distributions is not discussed.

- **"Efficient reasoning" claim (Section 5.2) partially undersupported.** The paper shows that models trained with composed data generate shorter responses and equates this with "efficient reasoning." Shorter responses could also reflect corner-cutting that happens to improve accuracy on these particular benchmarks. A finer-grained analysis (e.g., examining whether shorter responses skip valid reasoning steps) would strengthen this claim.

### Trivial

None.

## Nice-to-Haves

- Run RL training on at least one larger model (e.g., R1-Qwen-32B or Qwen3-32B) or a different architecture to demonstrate generalization of the training benefit.
- Include confidence intervals or error bars in the main evaluation table.
- Report the computational cost of constructing the composed datasets and running RL training (to substantiate the "low-cost" claim).
- Add a brief sketch of how composition works for non-math tasks in the main text, even if full details remain in the appendix.

## Removed Points

These points raised by reviewers were filtered and moved here. Treat them with caution — they should not be treated as confirmed weaknesses.

- **"Code/agent composition not described in main text"** — The paper explicitly states "For code and agentic tasks, we provide the construction process in Appendix A." The appendix was stripped by the parser; the authors properly scoped this content. Not a valid weakness.
- **"Human evaluation/sanity check not reported"** — Asking authors to manually verify hundreds of composed problems is excessive and not standard for benchmark papers of this type.
- **"Thinking budget framing could be adaptive strategy, not limitation"** — The alternative interpretation is reasonable but the paper's framing (models favor early problems) is defensible and supported by the data.
- **"Computational cost not reported despite low-cost claim"** — Partially valid but minor; the claim refers to the method avoiding human annotation, not a precise dollar figure.
- **"Overthinking claim needs more justification"** — The paper provides supporting evidence (Figure 9b, response length analysis) that is commensurate with the claim.

## Novel Insights

The most interesting observation emerging from combining the evaluation and training results is the asymmetry: the benchmark shows that LRMs severely fail at multi-horizon reasoning, yet the same model family (R1-Qwen-7B) can learn to handle composed problems through RLVR with composed training data, and this transfer *improves* single-problem performance. This suggests that the failure on long-horizon reasoning is substantially a training-data distribution issue — models have simply not seen multi-step interdependent problems during training — rather than a fundamental architectural limitation. The rollout efficiency analysis further suggests that composed data provides a denser reward signal, which may explain why it accelerates learning even for single-problem tasks.

## Suggestions

1. **Fix the duplicate Qwen3-32B entries** — Clarify whether one row corresponds to a different model variant (e.g., Qwen3-32B-Instruct vs. Qwen3-32B) and correct or explain the 127.6% value. If possible, re-verify all entries in the table.
2. **Add at least one generalization experiment for RL training** — Even showing the benefit holds on a different 7B model or on R1-Qwen-32B would significantly strengthen the training contribution.
3. **Specify model M used for key variable verification** (Eq. 2) and report its accuracy or a human-verified precision rate.
4. **Add variance or confidence intervals** to the main evaluation table.
5. **Acknowledge the training/evaluation distribution mismatch** from the Acc_expected > 0.25 filter and discuss how this affects interpretation of the training results.

## Score and Decision

The calibration tool was unavailable (index corruption), so I calibrate based on my expertise against typical ICLR papers.

The paper makes a genuine, timely contribution: a simple method for creating multi-step interdependent reasoning problems, a large-scale evaluation showing consistent degradation across 26 models, and preliminary evidence that training on composed data improves both multi-horizon and single-horizon performance. The evaluation breadth (25+ models, 6 datasets, 3 task types) is a strength, and the degradation trends are robust and clearly documented.

The major weaknesses are: (1) a data integrity issue in the main evaluation table (duplicate rows with an impossible 127.6% value) that needs full clarification, and (2) RL training on a single 7B model without generalization evidence. Neither invalidates the core contribution — the table issue does not affect the overall degradation pattern visible across all other models, and the RL result is presented as exploratory — but both need to be addressed.

Typical ICLR "strong accept" papers (score 8+) would have tighter experimental methodology. Typical "reject" papers (score 3-4) lack a clear contribution or have fatal flaws. This paper sits between these: the contribution is real and well-supported at the benchmark level, but the experimental rigor has gaps.

**Score: 6.5** — borderline accept. The benchmark contribution is solid and the training results are promising but preliminary. The paper would be strengthened by resolving the table issue and adding generalization experiments.

**Decision: Accept.**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>