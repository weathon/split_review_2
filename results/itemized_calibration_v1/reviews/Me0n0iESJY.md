## Summary

This paper introduces a benchmark for evaluating model merging methods on Multimodal LLMs (MLLMs), covering five capability categories (VQA, Geometry, Chart, OCR, Grounding) and a modality-merging track (vision+audio+video). It evaluates 10 merging algorithms on both full-fine-tuned (InternVL2.5) and LoRA-tuned (Qwen2-VL) models, and proposes OptMerge—a method combining low-rank SVD denoising with improved task vector optimization. The paper also provides a theoretical bound linking fine-tuning intensity to merging quality.

## Strengths

- **First comprehensive benchmark for MLLM model merging.** The benchmark fills a genuine gap with 5 capability categories, ≥100k samples per category, both full fine-tuning and LoRA scenarios, expert model weights and code publicly released, and a modality-merging track. Prior work (AdaMMS, UQ-Merge) had narrower scope.

- **Theoretical analysis connecting fine-tuning to merging quality.** Theorem 3.1 provides an upper bound on merging loss decomposed into residual, cross-task interference, and curvature terms, giving a principled explanation for why over-trained models (e.g., Qwen2.5-Math/Coder) merge poorly. While the analysis uses standard assumptions (L-smoothness + PL condition), the explicit connection to model merging is new and practically useful.

- **Comprehensive baseline evaluation.** 10 merging algorithms across 4 categories are systematically evaluated on two architectures with consistent hyperparameter search. The analysis of *why* different methods succeed or fail in each setting (e.g., Iso-C fails on LoRA because LoRA task vectors are already low-rank) is informative and goes beyond reporting numbers.

- **Emergent capabilities on general benchmarks (Table 10).** The merged model (InternVL2.5-1B) substantially outperforms individual experts on general multimodal QA benchmarks (MMMU, DocVQA, ScienceQA, AI2D, InfographicVQA) with an average improvement of 10.85%. This is one of the paper's strongest empirical findings—demonstrating that merging can yield emergent integrated capabilities that no single expert possesses.

- **Real-world validation on Hugging Face checkpoints (Table 6).** Merging models actually uploaded by the community (GRPO-tuned, Pokemon, OCR, Vietnamese) demonstrates practical applicability beyond idealized lab settings.

## Weaknesses

### Fatal
None.

### Major

- **Numerical inconsistencies in Table 3 undermine data integrity.** I verified every average in Tables 2, 5, and 6—most are within rounding error (≤0.1). However, Table 3 (Qwen2-VL, LoRA) has two clear errors:
  - **WUDI Merging**: Individual scores sum to 599.72 (mean 59.97), but the table reports **63.65** — a discrepancy of **3.68 points**.
  - **TSV Merging**: Individual scores sum to 627.92 (mean 62.79), but the table reports **60.63** — a discrepancy of **2.16 points**.
  - Other rows in the same table check out (e.g., OptMerge computed≈63.36 vs reported 63.30), so the individual scores are likely correct but the averages for WUDI and TSV are wrong. This directly affects the paper's central comparison because the Qwen2-VL setting is where the reported superiority of OptMerge over WUDI (63.30 vs. 63.65) is contradicted by the paper's own data—correcting WUDI's average to 59.97 would reverse the ranking. The paper cannot make trustworthy claims about relative method performance on this architecture until these numbers are corrected.

- **Improvements over the strongest baselines are marginal and inconsistent across settings.** Even taking the reported numbers at face value:
  - **InternVL2.5 (Table 2):** OptMerge (57.44) improves over WUDI (57.00) by only **+0.44 points**, and **Mixture Training (57.66) beats OptMerge**. The abstract's claim that "model merging surpasses mixture training" is directly contradicted by this table.
  - **Qwen2-VL (Table 3):** If the reported averages are taken at face value, OptMerge (63.30) loses to WUDI (63.65). (Correcting the WUDI error reverses this, but the point stands that even the paper's own data does not show clear dominance.)
  - **Modality merging (Table 5):** OptMerge (67.00) is second to TSV (67.34).
  - **Hugging Face (Table 6):** OptMerge (66.70) beats the next best (TIES w/ DARE, 66.58) by **+0.12 points**.
  No single experiment shows OptMerge as clearly dominant, and the margins are consistently well under 1% against the strongest competitor. The **2.48% average gain** claimed in the abstract refers to the ablation study (WUDI → OptMerge), not to improvement over the best prior method—this framing is misleading.

- **No variance or statistical significance reported.** All experiments are single runs with no standard deviations, confidence intervals, or multiple seeds. Given that margins between methods are frequently <1% and MLLM evaluation has known run-to-run variance from decoding stochasticity, it is impossible to determine whether the observed differences are meaningful. This is critical when the paper's central claim rests on very small margins.

- **Mixture training comparison is not controlled for Qwen2-VL.** For InternVL2.5, the authors perform controlled mixture training on the same task data—a fair comparison. But for Qwen2-VL-Base, they use **Qwen2-VL-Instruct** as the "mixture training upper bound," which was trained on different (potentially proprietary) data with different procedures. This conflates two questions: (1) whether merging can match multitask training, and (2) whether a separately trained instruction-tuned model is a fair baseline. The claim that merging "surpasses mixture training" on Qwen2-VL is not supported by an apples-to-apples comparison.

### Minor

- **OptMerge's novelty is modest.** The method combines existing ideas: WUDI's optimization loss, SVD denoising (from TSV/Iso-C), SGD instead of Adam, and mean initialization of the merged vector. The ablation (Table 4) shows the largest gain comes from mean initialization (+4.43% on Qwen2-VL), not from the low-rank approximation (+0.22%). The method is better described as a well-engineered combination of known components than as a novel algorithmic contribution.

- **Only linear layers are optimized (footnote 1); all other layers use simple averaging.** The paper does not analyze whether this restriction helps or hurts, nor whether applying SVD/optimization to non-linear layers would change results.

- **The rank-size ablation (Table 8) is evaluated only on InternVL2.5.** It is not shown whether the k/rank heuristic generalizes to Qwen2-VL or the modality merging setting.

### Trivial
None.

## Nice-to-Haves

- The finding in Table 10 (10.85% improvement on general QA benchmarks via emergent capabilities) is arguably one of the paper's most striking results but receives minimal discussion in the abstract and conclusion. Highlighting and analyzing why merging yields synergistic benefits would strengthen the paper.
- A limitations section discussing failure cases (e.g., why OptMerge underperforms mixture training on OCR in Table 2, or when the method might underperform simple averaging) would improve the paper's completeness.

## Removed Points

The following points from the input review were removed:

- *"No statistical significance or variance"* — merged into Major weakness above with the acknowledgment that this is partially standard for the field but critical given the small margins.
- *"Data-free claim needs qualification about λ search"* — removed; the paper acknowledges λ is tuned on a validation set, which is standard practice and does not violate the "data-free" characterization of the core optimization.
- *"Reproducibility details are thin"* — removed per filtering rules; hyperparameter disclosure beyond what is provided (λ range, optimizers, iterations) is not required for review.
- *"No limitations section"* — demoted to Nice-to-Haves; not having a limitations section is not a flaw per se.
- *"Weak modality merging baselines (audio-only 37.75)"* — removed; the critic acknowledged this is expected since audio-only models cannot solve visual QA tasks.
- *"Overstates prior work gap in intro"* — removed; the paper acknowledges AdaMMS and UQ-Merge in Section 2, and the intro's claim is about a benchmark that "clearly divides tasks," which is distinct from those works.
- *"Missing related works"* — removed per rules (risk of speculation without external sources).

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis confirms the paper's main findings (benchmark is valuable, method improvements are marginal) but does not surface any unanticipated pattern or contradiction beyond the numerical errors in Table 3.

## Suggestions

1. **Correct the numerical errors in Table 3** for WUDI and TSV averages (and verify all other rows). Provide corrected numbers.
2. **Add variance estimates** or multiple-run statistics for the key comparison experiments, especially where margins are <1%.
3. **Recalibrate claims:**
   - "Model merging surpasses mixture training" is not supported on InternVL2.5 (Table 2 shows mixture training at 57.66 beats OptMerge at 57.44). Either qualify this claim or remove it.
   - Clearly attribute the 2.48% gain to the ablation study (WUDI → OptMerge), not to comparison against the strongest baseline.
4. **Either perform a controlled mixture training experiment on Qwen2-VL** (using the same task data as the experts) or clearly qualify that the Instruct model comparison is not apples-to-apples.
5. **Give more prominence to the emergent capabilities result (Table 10)** in the abstract and conclusion, as this is a stronger and more interesting finding than the marginal method improvements.
6. Consider repositioning the paper primarily around the benchmark contribution, presenting OptMerge as a well-engineered method that works well on this benchmark rather than claiming it as a novel algorithmic contribution.

## Score and Decision

**Calibration anchors (all retrieved across rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| fvUVe2gJh0.md ("What Matters for Model Merging at Scale?") | 5.33 | R1 | Yes | Rejected evaluation paper; comprehensive but criticized for unfair comparisons and limited scope. Our paper has data errors this anchor lacks. |
| Bq3fEAGXUL.md ("Realistic Evaluation of Model Merging") | 5.33 | R1 | Yes | Rejected; unclear trends, insufficient insights, no error bars. Our paper has clearer comparative results but also verifiable data errors. |
| lNtio1tdbL.md ("ATM: Alternating Tuning and Merging") | 3.00 | R1 | Yes | Rejected; method fundamentally misrepresented as merging, unfair baselines. Our paper does not have this misrepresentation issue. |
| gNoqEdT2wO.md ("Multimodal Class-Incremental Learning benchmark") | 2.33 | R1 | Yes | Rejected; weak benchmark, limited datasets, poor motivation. Our benchmark is substantially stronger. |
| 2rWbKbmOuM.md ("MEGA-Bench") | 7.00 | R1 | Yes | Accepted; large-scale evaluation benchmark (500+ tasks). Significantly larger scale than our paper. |
| HfJxXbXlYJ.md ("LLM2CLIP") | 3.00 | R1 | No | CLIP extension paper, less relevant. |
| 5kMwiMnUip.md, 8QTpYC4smR.md, etc. | 0.5-1.4 | R1 | No | Strong reject anchors; clearly irrelevant (surveys, jailbreaking, unrelated topics). |

**Bracket reasoning (R1):** The paper's benchmark is clearly stronger than the 2.33 anchor's, and it lacks the fundamental misrepresentation of the 3.00 ATM paper. However, the Table 3 data errors and overstated claims are weaknesses the 5.33 papers do not share. The paper sits between these bands. **Initial bracket: 3.5–5.0.**

**Narrowing to final score:** Against the 5.33 anchors, this paper has a stronger benchmark contribution but introduces data integrity concerns those papers avoid. The WUDI average error (Δ=3.68) and TSV average error (Δ=2.16) are verifiable from the printed numbers and are not small rounding issues. Combined with the mixture training comparison being uncontrolled for Qwen2-VL and the claim that merging "surpasses mixture training" being contradicted by Table 2, these issues prevent the paper from reaching even the borderline-rejected evaluation papers' level. The paper needs substantive corrections and claim recalibration before it can be accepted.

**Final calibrated score: 4.0** — The benchmark contribution is genuine and fills a gap, but the data errors, unqualified claims, and marginal method improvements prevent acceptance in the current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>