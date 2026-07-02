## Summary

This paper introduces VideoJudge, a bootstrapping framework for training small MLLM-based evaluators (3B and 7B) specialized for video understanding tasks. The key idea is a generator–evaluator pipeline that iteratively produces candidate responses across a 1–5 rating scale, validates them via an evaluator, and refines mismatched examples—yielding over 100K training examples without manual annotation. The trained judge models are evaluated across four pointwise and three pairwise benchmarks, including independent human-annotated ones, and shown to be competitive with much larger models (Qwen2.5-VL 32B/72B). The paper also introduces instance-specific rubric generation at test time for improved interpretability.

## Strengths

1. **Practical and well-motivated pipeline.** The bootstrapping approach (generator–evaluator loop with iterative refinement) directly addresses the scarcity of human-annotated evaluation data for video understanding. The process produces 103K training examples from 25K seed pairs without manual annotation, which is a tangible engineering contribution (Sections 3.1, 4).

2. **Broad and largely fair experimental design.** Evaluation covers four pointwise benchmarks (including two independent, human-annotated ones: VATEx and LongVideoBench) and three pairwise benchmarks (including VideoAutoArena and a human-annotated subset VJ-H with 200+ pairs, 94.8% inter-annotator agreement, κ=89.5). The inclusion of independent external benchmarks guards against pure closed-loop overfitting (Sections 4.2, 5.2, Table 1, Table 3).

3. **Transparent error analysis.** Section 6.2 candidly reports that 14.8% of evaluations overestimate by ≥2 points, only 36.9% of rating-3 responses are correct, and 81.3% of rating-4 responses are incorrectly scored as 5. The paper does not hide these flaws, which enables readers to calibrate their trust in the model appropriately.

4. **Instance-specific rubric generation (VideoJudgeR-3B).** Having the judge produce explicit evaluation criteria before scoring is a thoughtful addition for interpretability, and Table 2 shows meaningful gains over the base 3B model (MAE 0.59 vs. 1.15, correlations above 73 vs. 38).

## Weaknesses

### Fatal

None.

### Major

1. **Systematic overestimation bias severely limits fine-grained reliability.** The error analysis (Section 6.2) shows that VideoJudge systematically inflates mid-to-high scores: 81.3% of rating-4 responses are incorrectly scored as 5, and only 36.9% of rating-3 responses receive the correct score (46.6% are inflated to 5). For a model whose entire purpose is evaluation, this degree of miscalibration in the range where most real evaluation would occur is a significant practical limitation. While the paper acknowledges this, it defers the solution to future work rather than offering any mitigation. The correlation numbers (Spearman, Pearson) may partly reflect the model's ability to separate extreme ratings (1 vs. 5) rather than meaningful fine-grained discrimination.

2. **Two of four pointwise benchmarks share methodology with the training pipeline.** The VideoJudgeLLaVA and VideoJudgeVCG benchmarks are constructed using the same generator–evaluator bootstrapping pipeline (Algorithm 1) used to create the training data. Although the seed instruction sources differ from the training sources, the ground-truth ratings rely on the same pipeline rather than human judgments. The paper acknowledges this "partial closed-loop effect" (Section 7), but the strongest correlational results (VideoJudge-3B achieving S=0.82/P=0.82 on VideoJudgeLLaVA) come from these benchmarks. On the two independent pointwise benchmarks (VATEx, LongVideoBench), VideoJudge is competitive but does not clearly surpass larger models—performance depends on which metric is prioritized. This tempers the headline claim.

### Minor

3. **Claim framing is slightly broader than the evidence supports.** The abstract states that VideoJudge-7B "outperforms or is on par with larger MLLM judge baselines such as Qwen2.5-VL (32B and 72B) across three out of four meta-evaluation benchmarks." Looking at Table 1, the pattern is more mixed: on VATEx, VideoJudge-7B's PSUP (0.66) is below Qwen-32B (0.73) and Qwen-72B (0.71), though its ECE (0.64) is best; on LongVideoBench, VideoJudge-7B has the best Δ(C-D) (1.16) but PSUP (0.66) is again below the larger models. The claim is defensible when selecting the most favorable metric per benchmark, but the overall picture is one of *competitive* performance with selective advantages rather than clear superiority. The contribution—that fine-tuned 7B judges can match larger models—is still valuable and does not require the stronger framing.

4. **Rubric quality evidence is weaker than claimed.** The human evaluation (Figure 3) shows VideoJudgeR-3B achieving a 53.4% unanimous win rate against GPT-4o-mini's rubrics—barely above chance, yet described as "substantially higher-quality rubrics." Against Qwen-72B (63.9%) and smaller models the results are stronger. The LLM-as-Judge evaluation (92.7% vs. GPT-4o-mini) is impressive but introduces circularity concerns (GPT-4o-mini judging rubrics). The numbers are presented honestly, but the framing should be more measured.

5. **Acceptance threshold α for training data is not specified.** The methodology (Section 3.1) defines the acceptance criterion |r - r̂| ≤ α, and the meta-evaluation benchmarks use threshold 0 (Section 4.2). However, the value of α used during training data generation is never stated. This matters because a stricter α yields higher-quality but fewer examples.

6. **Weight decay of 0 with full fine-tuning is an unusual choice.** The experimental setup (Section 4.2) specifies weight decay of 0 without discussion. Given the relatively small training set (103K examples) and full fine-tuning, this choice risks overfitting and warrants at least a brief justification.

### Trivial

None.

## Nice-to-Haves

- Training on harder negatives or adding calibration-aware training could directly address the overestimation bias, rather than deferring it entirely.
- Reliability diagrams (calibration curves) would be more informative than the aggregate ECE metric, given the known miscalibration pattern.
- A head-to-head human evaluation of VideoJudge's scoring (not just rubric generation) against human raters on a held-out set would strengthen the claim of alignment with human judgment.

## Removed Points

These points are flagged to be removed; treat them with caution.
- **Generator/evaluator model identity not stated in main paper (Issue 4 from the harsh critic).** Removed per the rule that appendix content was stripped by the parser; the original submission references §A.2 for these details.
- **"First bootstrapped framework" claim is too strong.** Removed because the qualifier "bootstrapped" and "across diverse video understanding tasks" distinguishes this from prior work on narrower settings (text-to-image, text-to-video).
- **BERTScore/BLEU degradation as weak evidence.** Removed because the paper presents these as a sanity check (Section 5.1), not as strong evidence of quality.
- **Various section-by-section formatting and presentation notes.** Removed per filtering rules on style nitpicks and parser artifacts.

## Novel Insights

The harsh critic does not identify genuinely novel observations beyond the paper's own contributions. One interesting cross-cutting observation is the tension between the paper's transparent error reporting (a strength) and its optimistic claim framing (a weakness): the same section (6.2) that reveals 81.3% inflation of rating-4→5 is used to support a narrative of "matching or surpassing" much larger models. This disconnect—honest data paired with optimistic framing—is itself instructive about the gap between aggregate correlation metrics and per-rating reliability in learned evaluators.

## Suggestions

1. **Recalibrate the narrative.** Replace "match or surpass" with "are competitive with" or "achieve comparable performance to" when describing results against 32B–72B models. The paper is stronger when it accurately reflects the mixed evidence.
2. **Address the overestimation bias directly** rather than deferring it. A targeted experiment (e.g., upweighting mid-range training examples, adding a calibration loss, or analyzing whether the bias stems from label imbalance in the bootstrapped data) would substantially strengthen the paper.
3. **Specify the training acceptance threshold α** and the generator/evaluator model identities in the main text for reproducibility.

## Score and Decision

This paper tackles an important problem (scalable video understanding evaluation) with a sensible methodology and a thorough experimental design that includes independent human-annotated benchmarks. The bootstrapping pipeline is a practical contribution, and the honest error analysis is commendable.

However, the paper has two significant weaknesses. First, the systematic overestimation bias (81.3% of rating-4 responses scored as 5) undermines the model's reliability for fine-grained evaluation—the very task it is designed for. Second, the headline claims of "matching or surpassing" much larger models are slightly over-framed; the evidence shows competitive performance with selective metric-dependent advantages, and the strongest results occur on closed-loop benchmarks. These issues do not invalidate the contribution but do narrow its scope.

The paper would be a solid contribution with revision: recalibrating the claims, adding a targeted analysis of the overestimation bias, and providing the missing reproducibility details. In its current form, the gap between the strongest claims and the supporting evidence warrants a borderline accept.

**MY FINAL SCORE: <score>6</score>**
**MY FINAL DECISION: <decision>Accept</decision>**