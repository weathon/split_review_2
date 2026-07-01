## Summary

This paper introduces a benchmark for model merging in Multimodal LLMs (MLLMs), organized into 5 fine-grained capability areas (VQA, Geometry, Chart, OCR, Grounding) with ≥100k training samples per task, covering both full fine-tuning (InternVL2.5) and LoRA (Qwen2-VL) paradigms. It benchmarks 10 merging algorithms and proposes OptMerge, which applies low-rank denoising and improved optimization to task vectors. It also explores a novel modality merging direction (vision/audio/video) and validates merging on real Hugging Face checkpoints. The benchmark, code, and checkpoints are publicly released.

## Strengths

1. **First fine-grained capability benchmark for MLLM model merging.** Defines five distinct capability areas with dedicated training data (≥100k samples each) and corresponding evaluation benchmarks. Prior work (AdaMMS, UQ-Merge) either merges two models at a time or treats each fine-tuning dataset as a separate task without capability-level categorization. This fills a real gap for the model merging community.

2. **Two training paradigms with public checkpoints.** Both full fine-tuning (InternVL2.5) and LoRA (Qwen2-VL) are covered, exposing the different behaviors of task vectors under each regime. The visualization of magnitude distributions (Fig. 2) supports the method's design choices.

3. **Modality merging direction is novel and well-motivated.** Merging vision-language, audio-language, and video-language models into a single model (Table 5) is a genuinely underexplored application of model merging, and the results (67.00 average across two benchmarks) demonstrate the complementary nature of modal information.

4. **Validated on real Hugging Face checkpoints (Table 6).** The experiment with community-contributed models (GRPO-tuned math, Pokemon, OCR, Vietnamese VQA) provides practical evidence that the approach works with off-the-shelf models from open-source communities, not just the authors' own fine-tuned ones.

5. **Computational efficiency clearly demonstrated (Table 7).** OptMerge achieves dramatic efficiency gains: 0.22h/2.62GB for InternVL2.5-1B vs 25.38h/240GB for mixture training — a ~115× reduction in time and ~90× reduction in GPU memory. This is a genuine practical advantage of the merging approach.

## Weaknesses

### Major

1. **The central claim that "model merging can outperform mixture training" is not supported by the controlled experiment, and the uncontrolled comparison is invalid.**

   The paper's headline claim (abstract, introduction, conclusion) rests on two cases:
   - **InternVL2.5 (Table 2):** Actual mixture training is performed by combining all task-specific data for SFT. Result: Mixture Training **57.66**, OptMerge **57.44** — OptMerge is *lower*, not higher. The paper says "closely match or even surpass" (line 224), but in the one controlled case it does not surpass.
   - **Qwen2-VL (Table 3):** No mixture training is performed. The paper uses Qwen2-VL-Instruct as a proxy, calling it "the upper bound for mixture training, given its extensive prior SFT with diverse datasets" (line 224). This is not a valid comparison — Qwen2-VL-Instruct was trained on an entirely different (undisclosed) dataset with different training objectives. OptMerge (63.30) vs Qwen2-VL-Instruct (62.23) is an apples-to-oranges comparison.

   The claim that "model merging can outperform mixture training" thus rests entirely on an invalid comparison. In the one controlled experiment, the merged model underperforms mixture training. The paper qualifies this with "potentially" (conclusion) and "can" (abstract), but the overall framing is misleading. This is the most significant weakness and requires either removing the claim or conducting the missing controlled experiment on Qwen2-VL-Base.

2. **The average column in Tables 2 and 3 aggregates over different numbers of benchmarks per row, making cross-row average comparisons invalid.**

   In Table 2, Individual VQA has "-" entries for the three RefCOCO grounding benchmarks. Its average (41.80) is computed over 7 benchmarks where it has scores, while OptMerge's average (57.44) is computed over all 10 benchmarks. The same issue affects Individual Chart (missing RefCOCOs) and indeed all individual models. Any comparison of average scores between individual and merged models conflates genuine improvement with different evaluation coverage. The paper uses the average column extensively in its claims without noting this discrepancy, which systematically inflates the apparent gap between individual and merged models.

3. **Ablation study (Table 4) reveals the novel technical component contributes very little.**

   For Qwen2-VL: WUDI (58.65) → +SGD (48.88, −9.77%) → +Mean Init (63.08, +4.43%) → +Low-rank (63.30, +4.65%). The low-rank denoising step — presented as the primary novel contribution of OptMerge — adds only **+0.22%** (the difference between +Mean Init and +Low-rank). For Vicuna-7B: WUDI (64.65) → +SGD (66.91, +2.26%) → +Mean Init (67.07, +2.42%) → +Low-rank (67.00, −0.07%). Here low-rank denoising *hurts* performance. The main gain comes from mean initialization, a simple technique (initializing τ_m as the mean of task vectors). The paper frames OptMerge as having a strong novel technical contribution, but the data show it is primarily a practical recipe combining existing elements with a small low-rank tweak. This weakens the claimed technical contribution substantially.

### Minor

4. **No variance or statistical significance reported.** All tables report single numbers without confidence intervals or multiple runs. Given small margins (e.g., OptMerge 57.44 vs WUDI 57.00 on InternVL2.5, or 67.00 vs 64.65 on modality merging), it is impossible to assess whether these differences are meaningful. For a paper that makes comparative claims across 10+ tables, this is a methodological gap.

5. **The "2.48% average improvement" claim is not clearly traceable.** The abstract and contribution list state "an average performance gain of 2.48%." Individual tables report 0.44% (Table 2, InternVL2.5), 1.9% (Table 6, HF checkpoints), 4.65% (Table 4, Qwen2-VL), and 2.35% (Table 4, Vicuna-7B). The paper does not specify which experiments are averaged to produce 2.48%, making this claim unverifiable from the presented data.

### Trivial

6. **The claim "requires no hyperparameter search" (line 54) is contradicted by the λ search procedure.** The paper states it "requires no hyperparameter search" while all methods (including OptMerge) tune λ over [0.1, 0.3, 0.5, 0.7, 1.0, 1.5] using validation data (Section 5.1). The λ search is standard for all merging methods and the claim is comparing to AdaMMS's more expensive search, but the absolute statement is inaccurate.

## Nice-to-Haves

- Conduct actual mixture training on Qwen2-VL-Base with the same task data, enabling a controlled comparison.
- Report variance estimates over at least 3 runs.
- Clarify the 2.48% figure by stating which experiments are averaged.
- Disentangle the average column issue: report two sets of averages (full suite vs. task-covered subset) or rely on per-task breakdowns.
- Reframe OptMerge honestly: the effective component is mean initialization, not low-rank denoising.
- Discuss the rank size k sensitivity more thoroughly; Table 8 shows average dropping from 57.43 (20%) to 52.98 (50%), which is a meaningful sensitivity.

## Removed Points

These points from the input reviews are flagged for removal; treat them with caution:

1. *"Theoretical analysis (Theorem 3.1) — While not directly driving the method design, it formalizes the known empirical observation..."* — Listed as a strength in the harsh critic's input. Retained in a diluted form. The theorem is presented as a strength but it's a fairly standard bound and not connected to the method design. This was moved from the Strengths list to not be a core strength.

2. *"The method only optimizes linear layers, with remaining layers merged by averaging. The impact of this design choice is not analyzed."* — From harsh critic's "Missing Parts." This is a fair point but very minor and not central to any claim. Moved to removed.

3. *"Section 3.2: Theorem 3.1 is presented without specifying the assumptions needed for the bound to hold (relegated to Appendix A)."* — The paper states assumptions are in Appendix A. Since appendices are stripped by the parser, this cannot be verified and is removed per hard rules.

4. *"The remark about 'Qwen2.5-Math and Qwen2.5-Coder yielding poor merging due to excessive post-training' is interesting but unsupported — no experiment is shown."* — This remark is an example, not a claim requiring experimental support. It's a reasonable observation from existing knowledge. Removed.

5. *Various formatting/style nitpicks and grammar complaints* — Removed per hard rules (parser artifacts, not author errors).

## Novel Insights

The most valuable insight from the input reviews is the identification of a structural evidential gap: the paper's headline claim ("model merging can outperform mixture training") is contradicted by its own controlled experiment (InternVL2.5) and supported only by an invalid comparison (Qwen2-VL-Instruct as a proxy). The ablation analysis revealing that low-rank denoising — the claimed novel contribution — contributes at most 0.22% (and can hurt) is a second critical observation that recontextualizes the method's contribution. The average-column inconsistency is a methodological oversight that inflates apparent gains.

## Suggestions

1. **Fix the central evidential gap** — either perform controlled mixture training on Qwen2-VL-Base, or honestly reframe the claim to "model merging closely matches mixture training while being dramatically more efficient" (which the data does support).

2. **Revise the method framing** — present OptMerge as a practical recipe (mean initialization + careful optimization) rather than claiming low-rank denoising as the primary innovation.

3. **Make the average column transparent** — either compute all averages over the same benchmark set, or explicitly note which benchmarks are included per row.

4. **Add variance estimates** over at least 3 runs, particularly for close comparisons.

5. **Clarify the 2.48% figure** by stating which experiments contribute to the average.

## Score and Decision

**Bracket (Round 1):** 4.5 – 5.5 (based on comparison to UQ-Merge at 5.50, Realistic Evaluation at 5.33, and What Matters at 5.33 — all judged by human reviewers as borderline reject for comparable contributions and issues).

**Final determination:** The paper has a solid benchmark contribution and a genuinely novel modality merging direction. However, the headline claim is not supported by the controlled experiment; the method's novel component contributes negligibly; and the average evaluation metric is inconsistently computed. These issues are significant enough that the paper cannot be accepted as written, but they are addressable with major revisions.

**Score:** 5.0  
**Decision:** Reject

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>