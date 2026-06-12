Now I have a thorough understanding of the calibration landscape. Let me finalize my review.

**Round 1 Bracket**: Based on the retrieved anchors:
- **Self-Taught Evaluators** (5.40, rejected): Very similar iterative bootstrapping approach for training evaluators, but text-only. Concerns about limited model testing and simple synthetic data generation.
- **JudgeLM** (5.25, rejected): Fine-tunes LLMs as judges, simpler methodology than VideoJudge.
- **Auto-J / Generative Judge** (5.33, accepted): 13B judge trained on GPT-4 data. Less novel methodology.
- **VideoNIAH** (5.75, accepted): Synthetic evaluator for video MLLMs, more limited in scope.
- **"Is Your Video Language Model a Reliable Judge?"** (6.50, accepted): Related but different approach.
- **"Limits to scalable evaluation"** (6.50, accepted): More theoretical.

**Bracket**: 5.5–6.5. VideoJudge has more novel methodology than the rejected papers (Self-Taught, JudgeLM), and more ambitious contributions than accepted papers at 5.33–5.75, but has real evaluation issues that prevent it from reaching 6.5+ territory. The bootstrapping methodology and rubric generation are genuine innovations, and the resource contribution is significant. The circular evaluation is partially mitigated by external benchmarks. The calibration failure is real but acknowledged.

**Final score: 6.0**

---

## Summary
VideoJudge introduces a bootstrapping framework for training MLLM-based evaluators (3B/7B) for video understanding. An iterative generator-evaluator pipeline synthesizes ~104K training examples across a 1–5 rating scale without human annotation, which are used to fine-tune Qwen2.5-VL models into pointwise and pairwise judges. The paper also trains a rubric-generating variant (VideoJudgeR-3B), constructs meta-evaluation benchmarks, and evaluates across four pointwise and three pairwise benchmarks.

## Strengths
- **Novel bootstrapping methodology with formal iterative refinement**: The generator-evaluator pipeline (§3.1, Eqs 1–4) is cleanly formalized with an explicit acceptance criterion (Δ ≤ α) and iterative refinement using evaluator feedback. This produces over 100K training examples from 25K seeds without human annotation, validated by monotonic BERTScore/BLEU degradation across rating levels (Figure 2).
- **Instance-specific rubric generation as a distinctive contribution**: Training models to generate per-instance rubrics before scoring (§6.1, Table 2) is genuinely novel. VideoJudgeR-3B reduces MAE from 1.15 to 0.59 compared to the base 3B model, achieving performance comparable to 32B/72B models. Human evaluation (Figure 3) shows rubrics preferred over GPT-4o-mini (53.4%) and Qwen-72B (63.9%).
- **Human evaluation validates bootstrapped data quality**: The pairwise data quality study (§5.2) reports 94.8% annotator agreement (Cohen's κ = 89.5) and >92% correctness relative to gold preferences on the hardest 2-vs-3 rating boundary — validating the reliability of the synthetic supervision signal.
- **Robustness to decoding temperature**: Figure 4 shows VideoJudge maintains correlation at high temperatures (0.73 at T=1.0) while the base model degrades (0.42 at T=1.0), demonstrating that training confers practical robustness important for real-world deployment.
- **Transparent error analysis and useful negative findings**: The paper openly reports the overestimation bias (§6.2), and Table 1 shows that unimodal Qwen3 models underperform multimodal Qwen2.5-VL models while "thinking mode" does not reliably help — providing actionable guidance.
- **Significant resource contribution**: The paper releases trained models (3B/7B pointwise and pairwise), meta-evaluation benchmarks, bootstrapped datasets, and rubric-generation models — supporting reproducible research.

## Weaknesses

### Fatal
None.

### Major
- **Circular evaluation inflates headline results on self-constructed benchmarks**: Two of four pointwise benchmarks (VideoJudgeLLaVA-MetaEval and VideoJudgeVCG-MetaEval) are constructed using the same generator-evaluator pipeline (Algorithm 1) as the training data. §4.2 explicitly states seed data is sourced from LLaVA-Video/VideoChatGPT then "generating additional responses via our bootstrapping pipeline (Algorithm 1) with threshold 0." This means the distribution of "what a rating-3 response looks like" in these benchmarks closely mirrors the training distribution. On these benchmarks, VideoJudge-3B achieves its strongest results (Spearman/Pearson 0.82 on VideoJudgeLLaVA). On external benchmarks, results are notably weaker: on VATEX, VideoJudge-3B's PSUP (0.61) is well below Qwen2.5-VL-32B (0.73) and 72B (0.71); on pairwise VideoAutoArena, VideoJudge-7B (85.49) trails Qwen2.5-VL-72B (89.80). The paper acknowledges "partial closed-loop effects" in §7, but this is more serious than framed — self-constructed benchmarks account for half the pointwise evaluation and all pairwise VJ results (94–98.6% accuracy).

- **Severe overestimation bias undermines core utility as a judge**: The error analysis (§6.2) reveals 81.3% of rating-4 responses are incorrectly scored as 5, and 46.6% of rating-3 responses are inflated to 5. Only 36.9% of rating-3 responses receive the correct score. The model overestimates by ≥2 points 14.8% of the time but underestimates by the same margin only 1.5%. For a model whose purpose is assigning accurate ratings, this calibration failure is fundamental. Critically, the correlation metrics (Spearman, Pearson) reported in the main results can remain high with this bias since they measure ordering, not calibration — meaning headline metrics may be masking the problem. The paper defers this to future work rather than engaging with what it means for the current contribution.

### Minor
- **Generator and evaluator models not identified in main text**: The paper refers to "a generator model G" and "an evaluator model E" throughout but never identifies them in the main text, deferring to §A.2 (appendix). This matters because the ceiling of bootstrapped data quality is bounded by the evaluator model — if the evaluator is one of the larger Qwen2.5-VL variants, then VideoJudge models are effectively distilling from that model, and "outperforming" it on self-constructed benchmarks would be unsurprising.
- **No ablation of bootstrapping components**: The paper does not isolate the contribution of the iterative refinement loop vs. simple one-shot generation, nor does it ablate the acceptance threshold α or the choice of generator/evaluator model. This makes it difficult to understand what drives the improvements.
- **Missing comparison with straightforward fine-tuning baselines**: No comparison with fine-tuning on existing human preference data (e.g., from VideoAutoArena) or simple augmentations (e.g., randomly degrading gold responses). Without these, it is unclear whether the bootstrapping machinery is necessary or whether any supervised fine-tuning on the base Qwen2.5-VL models would yield similar gains.
- **Use of dense video descriptions as proxy for raw video**: §3.1 notes the pipeline uses dense video descriptions ṽ instead of raw video during bootstrapping, introducing a dependency on description quality. Any biases or information loss in descriptions propagate into the entire training corpus. This design choice deserves more explicit discussion.

## Nice-to-Haves
- Center evaluation on external, human-annotated benchmarks (VATEX, LongVideoBench, VideoAutoArena) and treat self-constructed benchmarks as supplementary.
- Even a simple calibration post-processing step (temperature scaling, isotonic regression) or training with a loss that penalizes score inflation would show engagement with the overestimation problem rather than deferring it.
- Ablate the feedback/refinement loop contribution vs. one-shot generation, and the effect of acceptance threshold α.
- Discuss the gap between correlation metrics (which look good) and calibration (which is poor), since it means the model preserves ordering but not magnitude — a judge that consistently inflates scores would pass a correlation test while being misleading in practice.

## Removed Points
These points are flagged to be removed, treat them with caution.

- "Several models excluded due to instruction-following failures could indicate fragile prompt format" — The paper explicitly notes these models failed to follow instructions under the same setup. Excluding non-functional baselines is standard practice. (Removed: speculative concern.)
- "Human evaluation limited to 250 pairs at 2-vs-3 boundary" — The evaluation targets the hardest cases and achieves strong results (94.8% agreement, κ=89.5). (Removed: the evaluation is reasonable for its stated purpose.)
- "BERTScore/BLEU degradation is a low bar" — The paper uses this appropriately as a sanity check, not a primary claim. (Removed: not a substantive weakness.)
- "Abstract claim 'on par' is doing a lot of work" — The abstract claims "three out of four" benchmarks, which is reasonably supported. (Removed: the claim is appropriately hedged.)
- "Comparison between fine-tuned and zero-shot models on rubric generation is confounded" — The comparison setup is standard; both models are evaluated on the same benchmarks. (Removed: standard experimental design.)

## Novel Insights
The paper makes a genuine methodological contribution by showing that an iterative generator-evaluator bootstrapping pipeline can produce sufficient training signal for small MLLMs to perform competitively as video understanding judges. The instance-specific rubric generation approach is novel and particularly promising — enabling a 3B model to produce rubrics preferred by humans over those from 72B models. The negative findings about LLM vs. MLLM judges and chain-of-thought reasoning are also valuable for the community.

## Suggestions
- Identify the generator and evaluator models prominently in the main text (§3.1 or §4).
- Relegate self-constructed benchmarks to supplementary and center external benchmark results.
- Address the calibration/overestimation problem directly, even with a simple post-hoc correction.
- Add ablation studies on the bootstrapping loop iterations, acceptance threshold, and generator/evaluator model choice.

## Calibration Report

**Anchor papers retrieved across rounds:**

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| Systematic Review of LLMs | 1.00 | 1 | Far below — survey with no novelty |
| NEMESIS Jailbreaking LLMs | 1.40 | 1 | Far below — weak jailbreak survey |
| Multimodal Instruction Tuning w/ HSM | 3.40 | 1 | Below — multimodal but limited scope |
| Explainable Rewards in RLHF | 3.00 | 1 | Below — circular LLM-as-judge evaluation, weak experiments |
| LVBench | 4.50 | 1 | Below — benchmark paper with limited novelty |
| SynthCLIP | 4.75 | 2 | Below — fully synthetic training for CLIP, limited analysis |
| JudgeLM | 5.25 | 1 | Below — simpler judge fine-tuning, rejected |
| Self-Taught Evaluators | 5.40 | 2 | Close below — very similar bootstrapping approach for text, rejected |
| Auto-J / Generative Judge | 5.33 | 1 | Close below — judge training with less novel methodology, accepted |
| VideoGLUE | 5.50 | 2 | Close below — video evaluation benchmark, limited contribution |
| VideoNIAH | 5.75 | 1 | Close — synthetic video evaluator, less ambitious |
| Neptune | 5.33 | 2 | Below — long video benchmark, limited scope |
| Collapse or Thrive (Synthetic Data) | 5.75 | 2 | Close — synthetic data analysis, different focus |
| Genie (Achieving Human Parity) | 5.33 | 2 | Below — synthetic data generation, less novel |
| "Is Your VLM a Reliable Judge?" | 6.50 | 1 | Close above — related topic, different approach, less ambitious |
| "Limits to Scalable Evaluation" | 6.50 | 1 | Close above — theoretical, more focused contribution |
| MMIE | 8.00 | 1 | Above — large-scale benchmark, well-executed |
| Training on the Test Task | 8.00 | 1 | Above — fundamental evaluation insight |

**Bracket and reasoning:**
- **Round 1 bracket**: 5.5–6.5. VideoJudge has more novel methodology than rejected papers at 5.25–5.40 (JudgeLM, Self-Taught Evaluators) and more ambitious contributions than accepted papers at 5.33–5.75 (Auto-J, VideoNIAH). The bootstrapping pipeline, rubric generation, and resource contribution are genuine innovations. However, the circular evaluation on self-constructed benchmarks and severe calibration failure prevent it from reaching the 6.5+ tier of papers like "Is Your VLM a Reliable Judge?" (6.50) which had fewer evaluation concerns.
- **Final score: 6.0**. The paper is a clear accept with meaningful methodological and resource contributions, but the evaluation issues (circularity, calibration) are significant enough to prevent a higher score. It sits between the rejected evaluator-training papers (5.25–5.40) and the stronger accepted evaluation papers (6.50).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>