## Summary

VideoJudge introduces a bootstrapping framework for training MLLM-based evaluators specialized for video understanding. The method uses a generator-evaluator iterative loop to produce 103,825 training examples from 25K seed video-instruction pairs without human annotation, covering both pointwise (1–5 rating) and pairwise (preference) evaluation settings. Fine-tuned 3B and 7B judge models (based on Qwen2.5-VL) are evaluated across a suite of benchmarks and can additionally generate instance-specific rubrics at test time. The paper provides released models, bootstrapped datasets, and meta-evaluation benchmarks.

## Strengths

1. **Bootstrapped data quality is validated through both automatic metrics and human evaluation**: Section 5.1 shows monotonic BERTScore/BLEU degradation across rating gaps (BERTScore 91.1→86.9 from rating 5–4 to 5–1, BLEU 11.0→3.0), confirmed by VQAScore in the appendix. Section 5.2 reports 94.8% annotator agreement (Cohen's κ=89.5) and >92% correctness relative to gold preference on the hardest 2-vs-3 rating pairs — directly supporting the claim that the pipeline yields reliable supervision without costly annotation.

2. **Small trained models match or outperform models 10× larger on multiple benchmarks**: In Table 1, VideoJudge-3B achieves Spearman 0.82 on VideoJudgeLLaVA vs Qwen2.5-VL-32B (0.80) and 72B (0.80). On LongVideoBench, VideoJudge-7B achieves the highest Δ(C-D)=1.16 (vs 72B's 1.06). In Table 3 (pairwise), VideoJudge-3B achieves 94.0 on VJ matching Qwen-72B, and VideoJudge-7B achieves 98.6 on VJ (w/o FB), the highest score across all models.

3. **Instance-specific rubric generation enables a 3B model to rival much larger models**: Table 2 shows VideoJudgeR-3B achieves MAE 0.59 and Pearson 73.96, comparable to Qwen2.5-VL-32B (0.59, 78.59) and 72B (0.54, 78.10), while dramatically improving over the base 3B (MAE 1.15, correlation 37.85). Human evaluations (Fig. 3) show VideoJudgeR-3B's rubrics preferred over GPT-4o-mini (53.4% win rate) and Qwen-72B (63.9%).

4. **Systematic ablation isolates the effect of temporal context and decoding temperature on judgment reliability**: The maxframes analysis (Section 6.2) shows training benefits from up to ~240 frames while evaluation saturates at ~120 frames, providing practical guidance. The temperature analysis (Fig. 4) shows VideoJudge's Spearman improves from 0.66 to 0.73 as temperature increases, while the base model degrades from 0.56 to 0.42 — demonstrating training confers robustness to stochastic decoding.

5. **Controlled comparison isolates the role of video input for video evaluation**: The paper systematically compares unimodal LLM judges (Qwen3, text-only) against MLLM judges (Qwen2.5-VL, with video), finding LLM judges consistently underperform and long chain-of-thought reasoning does not close the gap. This provides concrete evidence that video input is crucial for video understanding evaluation.

6. **Honest error analysis quantifies specific failure modes**: Section 6.2 reports that VideoJudge overestimates scores by ≥2 points in 14.8% of cases but underestimates by the same margin in only 1.5%, and only 36.9% of rating-3 responses receive the correct score (with 46.6% inflated to 5). This diagnostic detail directly informs the limitations section and is valuable for future work.

## Weaknesses

### Major

1. **Closed-loop evaluation inflates the headline model-size comparisons**: Two of four pointwise benchmarks (VideoJudgeLLaVA-MetaEval, VideoJudgeVCG-MetaEval) are constructed via the same bootstrapping pipeline used to generate training data — the ground-truth ratings are determined by the evaluator's own preferences. One of three pairwise benchmarks (VideoJudge-Pairwise/VJ) is similarly derived from bootstrapped pointwise data. On the truly independent benchmarks (VateX-Eval, LongVideoBench, VideoAutoArena, VJ-H), the results are more modest: VideoJudge-7B trails Qwen2.5-VL-72B on VAA (85.49 vs. 89.80) and on VateX PSUP (0.66 vs. 0.71), though it leads on LongVideoBench Δ(C-D) (1.16 vs. 1.06) and VJ-H (93.67 vs. 94.51). The paper acknowledges "partial closed-loop effects" in the limitations but does not separate closed-loop and independent evaluations in the main results presentation, making it easy for readers to over-interpret the claim that a 7B model "matches or surpasses models 10× its size." The strongest support for this claim comes from benchmarks where the training and evaluation signals originate from the same pipeline.

2. **The generator and evaluator models (G and E) used in bootstrapping are never identified**: Section 3.1 describes the iterative refinement loop with a generator G and evaluator E, but the paper never specifies which models play these roles. Whether G and E are Qwen2.5-VL-72B, GPT-4o, or something else fundamentally affects understanding of what is being distilled and the reproducibility of the method. The appendix reference about "strong vision-language models" (§A.2) concerns dense video descriptions, not the G and E models themselves. This is a basic methodological detail whose absence is a barrier to replication.

3. **The acceptance threshold α used during training data construction is never reported**: Section 3.1 defines the acceptance criterion $|r - \hat{r}| \leq \alpha$, but only discloses that α=0 for meta-evaluation benchmarks (line 108). The value of α during training data generation is never stated. This affects the size, difficulty composition, and quality of the training set, leaving the pipeline incompletely specified.

### Minor

1. **The rubric-generation comparison is asymmetric**: VideoJudgeR-3B is fine-tuned to generate rubrics on 10% of the bootstrapped data, while the baselines (Qwen2.5-VL-3B/7B/32B/72B) are evaluated zero-shot — they were never trained to generate rubrics. The strong win rates (92.7% vs. GPT-4o-mini, 71.3% vs. Qwen-72B in LLM-as-Judge evaluation) therefore do not demonstrate that the 3B model has fundamentally better rubric-generation capability; they primarily show that fine-tuning helps over zero-shot prompting for this task. A fairer comparison would fine-tune baselines on the same rubric training data.

2. **No error bars or statistical significance**: None of the tables report confidence intervals or significance tests. For pointwise metrics (RMSE, MAE, correlation), these can vary across data splits. For pairwise accuracy (Table 3), some differences between models are small enough that significance testing would clarify whether they are meaningful.

3. **Excluded baselines limit the "video model" category**: Four models (VideoLLaMA3-7B, VideoChat-Flash, Keye-VL, SmolVLM2) are excluded because they "failed to follow instructions or produce valid scores under the same evaluation setup" (line 102). While disclosed, reporting what fraction of outputs were invalid and why would clarify whether the evaluation protocol is biased toward certain model characteristics.

4. **The automatic data quality evaluation relies primarily on BERTScore/BLEU**: The monotonic degradation trend is informative, but BERTScore decreasing from 91.1 to 86.9 and BLEU from 11.0 to 3.0 primarily reflects decreasing lexical overlap with the gold response — not necessarily semantic degradation. VQAScore results in the appendix address this partially, but the main-text figures rely on lexical metrics.

### Trivial

None.

## Nice-to-Haves

- Report bootstrapping efficiency metrics: average number of refinement iterations (T), rejection rate, and how much of the 25K seed data was discarded.
- Train the rubric-generation model on the full dataset rather than 10% to strengthen that experiment.
- Include calibration plots or reliability diagrams alongside the ECE metric.

## Removed Points

- **Harsh critic's point about the "no comprehensive datasets" claim being overstated**: The paper specifically says "no comprehensive datasets with human preference signals" (emphasis on human preference signals). VateX-Eval and LongVideoBench are acknowledged and used as independent evaluations. This is a misreading of the paper's claim.
- **Harsh critic's point about Figure 1 caption/text discrepancy (MAD vs. Δ)**: The figure caption mentions MAD (mean absolute deviation) aggregated across responses, while the text uses per-response deviation Δ. This is a minor inconsistency in the figure description but the math (Eq. 3) clearly defines Δ, and the overall logic is consistent. Not a substantive weakness.
- **Strength Finder generic strengths** (e.g., "addressed an important problem"): Removed per filtering rules as generic/superficial.
- **Harsh critic critique that BERTScore/BLEU "does not independently validate semantic degradation"**: This ignores that the paper also uses VQAScore (appendix) and human evaluation (Section 5.2). The automatic metrics are presented as a proxy check, not the primary validation. Demoted from a claimed major issue to a minor note.
- **Formatting nitpicks, garbled table formatting observations**: Parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Restructure the results to explicitly separate closed-loop and independent benchmarks**: Present a clear partition in Table 1 (and the surrounding discussion) indicating which benchmarks share the evaluation pipeline with training data and which are fully independent human-annotated evaluations. This would let readers directly assess what generalizes to human judgment vs. what reflects pipeline preference alignment.

2. **Specify the G and E model identities and the training α threshold** in the main text to enable reproducibility and clarify whether the bootstrapping is self-distillation or distillation from a stronger teacher.

3. **Add error bars or confidence intervals** to key metrics, especially for pairwise accuracy where model rankings are close (e.g., VJ-H results in Table 3).

4. **For the rubric-generation experiment**, consider fine-tuning the larger baseline models on the same rubric training data to provide an apples-to-apples comparison, or at minimum acknowledge the asymmetry more explicitly.

5. **Report the disqualification rate for excluded baselines** to clarify whether the evaluation protocol systematically disadvantages certain model architectures.

---

**Calibration note**: The calibration search tool was unavailable during this review due to a filesystem error, so anchor-based score calibration could not be performed. The score assigned below reflects a direct assessment of the paper's contributions, evidence quality, and presentation.

---

**Score and Decision**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>