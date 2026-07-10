Now let me produce the final review.

## Summary

This paper introduces VideoJudge, a framework that bootstraps training data for MLLM-based video evaluators via a generator–evaluator pipeline, eliminating the need for costly human annotation. The trained 3B and 7B judge models are evaluated on both auto-constructed and independent human-annotated benchmarks (pointwise and pairwise), and are shown to match or exceed much larger models (e.g., Qwen2.5-VL-72B) on several metrics. The paper also demonstrates rubric-generation capabilities where a 3B model produces instance-specific rubrics preferred by humans over those from 72B models.

## Strengths

- **A genuinely useful methodological contribution.** The generator–evaluator bootstrapping pipeline (Section 3.1) is a principled, scalable approach for generating training data for video evaluators without requiring human annotation at scale. The iterative refinement loop with the deviation threshold is clean and reusable beyond video understanding.

- **Strong and consistent results on independent human-annotated benchmarks.** On LongVideoBench, VideoJudge-7B achieves Δ(C-D) of 1.16, outperforming Qwen2.5-VL-72B (1.06) — a model roughly 10× larger. On VATEx, VideoJudge-3B achieves the best ECE (0.63) and RMSE (1.33). In pairwise evaluation, VideoJudge-7B reaches 93.67 on VJ-H, essentially on par with Qwen2.5-VL-72B (94.51). These results on independently-annotated benchmarks provide credible evidence that the bootstrapped training transfers beyond the pipeline's own outputs.

- **Honest error analysis.** Section 6.2 reports a consistent overestimation bias (14.8% overestimate by ≥2 points vs. 1.5% underestimate) and poor calibration in the mid-to-high range (only 36.9% of rating-3 responses correct, with 46.6% inflated to 5). This self-critical analysis is rare and valuable — it tells the community exactly where to target improvements.

- **Rubric generation capability.** Training a 3B model to produce instance-specific rubrics (VideoJudgeR-3B) and showing these rubrics are preferred by human annotators over those from much larger models (63.9% win rate vs. Qwen-72B) is a solid secondary contribution. The rubric-first-then-score generation pipeline adds interpretability.

- **Rigorous human evaluation of training data quality.** The pairwise human evaluation (Section 5.2) with two annotators achieving 94.8% agreement and Cohen's κ of 89.5 is well-documented and directly validates that the bootstrapped pairwise data is reliable even in the hardest rating region (2 vs. 3).

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Overclaimed "outperforming" statement (Table 1, line 155).** The paper claims that on VideoJudgeLLaVA and VideoJudgeVCG, both VideoJudge-3B and -7B "outperform… LLaVA-NeXT, OneVision, and Video-R1." On VideoJudgeVCG, however, VideoJudge-3B (Spearman 0.59) underperforms both LLaVA-NeXT (0.70) and LLaVA-OneVision (0.77), and VideoJudge-7B (0.74) underperforms LLaVA-OneVision (0.77). The claim holds on VideoJudgeLLaVA but is partially inaccurate when the two benchmarks are grouped. This should be qualified.

- **"Gold response = rating 5" assumption may contribute to the documented overestimation bias.** Seed data responses from instruction-tuning datasets (of variable quality) are assigned rating 5 by default, implying they represent the quality ceiling. The paper's own error analysis shows 81.3% of rating-4 responses are scored as 5 and 46.6% of rating-3 responses are inflated to 5 — a pattern consistent with the model learning "high rating = the gold training response" rather than learning fine-grained distinctions near the top. The paper identifies the calibration gap (Section 6.2) but does not connect it to this structural design choice. Acknowledging this link would strengthen the paper's self-critique.

- **Two of four pointwise benchmarks are auto-constructed with the same pipeline used for training.** The paper acknowledges this closed-loop effect (Section 7), and the independent benchmarks (VATEx, LongVideoBench) corroborate the findings. Still, the abstract's "three out of four" framing would be more precise if it noted which two benchmarks are auto-constructed, as a reader relying solely on the abstract could overestimate the evidence base.

- **Generator/evaluator model identities stated only in the appendix (§A.2).** While the appendix exists in the original submission, the main text should state whether the generator and evaluator are from the same model family as the student (Qwen2.5-VL), since this matters for assessing independence between teacher and student. A one-sentence statement in Section 3.1 would resolve this.

- **Training data acceptance threshold α is never specified.** The parameter α is defined in Equation 3 and used throughout the acceptance criterion, but only the evaluation benchmarks use a concretely stated threshold ("threshold 0" in Section 4.2). The α used during training data generation is absent.

- **"w/ FB" vs "w/o FB" distinction in Table 3 is ambiguous.** For prompted baselines like Qwen2.5-VL, it is unclear what "with feedback" means — whether the prompt includes additional feedback from the bootstrapping loop, or whether the distinction only applies to the fine-tuned VideoJudge models. The caption defines the abbreviation but does not explain the operational difference for non-fine-tuned models.

- **Generator's "progressively degrading" prompt mechanism is not described.** The paper states that the generator is prompted to produce responses conditioned on a target rating by "progressively degrading the quality" (Section 5.1) but does not explain how controlled degradation is achieved in the prompt, which is a nontrivial part of the method.

### Trivial
None.

## Nice-to-Haves

- Report the acceptance/rejection rate in the bootstrapping pipeline to give a sense of the refinement loop's efficiency.
- Add confidence intervals or variance estimates for key results (Tables 1 and 3) where margins between models are small.
- Evaluate rubric-guided scoring on the independent human-annotated benchmarks (VATEx, LongVideoBench) rather than only on auto-constructed benchmarks.

## Removed Points

These points were flagged for removal; treat them with caution:

- **Closed-loop as a fatal concern**: Downgraded to Minor. The paper acknowledges this (Section 7), and the independent benchmarks corroborate the main findings.
- **Generator/evaluator models not in main text as a fatal reproducibility gap**: Downgraded to Minor. The information exists in §A.2; a one-sentence addition would resolve it.
- **Missing confidence intervals**: Moved to Nice-to-Have. Single-run evaluations without CIs are standard practice for large-scale benchmarks in this field.
- **Failure rate of excluded models**: Moved to Nice-to-Have. The paper reports which models were excluded and why, which is sufficient.
- **Rejection rate**: Moved to Nice-to-Have. Useful efficiency detail but not a core flaw.
- **"Outperforming" claim removed as a Major weakness**: Downgraded to Minor. The claim is partially true (holds on VideoJudgeLLaVA) and only overstated on one specific benchmark combination.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify the generator/evaluator models and α threshold in the main text.** Even a brief sentence in Section 3.1 would suffice: "We use [model X] as G and [model Y] as E, and set α = [value] during training."
2. **Clarify what "feedback" means for prompted baselines in Table 3.** If it means prompting with the evaluator's reasoning from the bootstrapping loop, state this explicitly; if it only applies to fine-tuned VideoJudge models, say so.
3. **Qualify the abstract's "three out of four" to note that two benchmarks are auto-constructed.** E.g., "Across three out of four benchmarks (including two human-annotated ones)…"
4. **Connect the overestimation bias to the "gold = rating 5" design choice.** Add a sentence in Section 6.2 or 7 discussing whether assigning rating 5 unconditionally to seed responses may inflate training targets.
5. **Tone down the "outperforming" claim on VideoJudgeVCG** or specify which benchmarks the claim applies to.

## Score and Decision

The paper makes a solid methodological contribution with a well-designed bootstrapping pipeline, rigorous evaluation (including human annotation for data validation), and convincing results on independent human-annotated benchmarks where a 7B model competes with a 72B model. All identified weaknesses are minor and addressable; none threaten the core claims. The paper should be accepted.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>