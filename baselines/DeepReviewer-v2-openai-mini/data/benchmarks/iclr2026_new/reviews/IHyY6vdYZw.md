## Summary
# Final Review Report

## Summary

This paper introduces VisualPRM400K, a dataset of approximately 400K multimodal process supervision samples with step-level correctness annotations, and VisualPRM, an 8B multimodal Process Reward Model (PRM) trained on this dataset. The authors also construct VisualProcessBench, a benchmark with 2,866 samples and 26,950 human-annotated step-wise correctness labels for evaluating step error detection in multimodal reasoning. Under Best-of-N (BoN) evaluation, VisualPRM improves reasoning performance across seven benchmarks for four MLLM families (MiniCPM-V2.6, QwenVL2.5-7B, InternVL2.5-8B/78B) by 3.7–8.4 points, and consistently outperforms Outcome Reward Models and Self-Consistency. The paper makes three contributions: (C1) the first large-scale multimodal process supervision dataset with an automatic Monte Carlo labeling pipeline, (C2) a benchmark for step-wise error detection, and (C3) empirical evidence that PRMs serve as effective critics for multimodal test-time scaling.

**Strengths**: The dataset scale (400K samples, 2M steps) and automatic labeling pipeline are practically valuable for the MLLM community. The benchmark addresses a real gap (lack of multimodal process evaluation) with careful human annotation and a well-motivated all-errors detection design. BoN experiments cover multiple model families and scales, demonstrating generality.

**Key Issues Identified**: (1) No statistical significance or variance reporting for BoN results. (2) Potential confirmation bias in automatic labeling (same model family for generation and scoring). (3) ORM comparison may be unfair due to label construction asymmetry. (4) Training-inference mismatch in PRM scoring. (5) Generic limitations section missing concrete failure modes.

**Novelty Note**: External literature verification is unavailable in this run (Retrieval-Disabled Mode). Novelty and comparison claims are deferred for manual verification. The claim of being "the first multimodal process supervision dataset" should be carefully scoped and verified by authors against concurrent work.

## Strengths
1. **Large-scale multimodal process supervision dataset**: VisualPRM400K with ~400K samples and ~2M steps is, to the authors' knowledge, the first multimodal dataset specifically designed for training process reward models. The scale and the automatic Monte Carlo labeling pipeline (sampling 16 continuations per step) make this a practically useful resource for the community. The release of data, model, and benchmark is a significant positive for reproducibility and future research.

2. **Well-designed benchmark with careful human annotation**: VisualProcessBench (2,866 samples, 26,950 step labels) addresses a clear gap in multimodal critic evaluation. The all-errors detection design (rather than only first erroneous step) is well motivated by recent advances in model reflection, and the use of multiple solution sources (GPT-4o, Claude, Gemini, QvQ, InternVL) ensures diversity. The 39 person-days of human annotation with quality review (10% per split) represents a substantial annotation effort.

3. **Comprehensive BoN evaluation across model families and scales**: The paper evaluates VisualPRM on four different MLLM families (MiniCPM-V, Qwen-VL, InternVL2.5 at 8B/26B/38B/78B) across seven reasoning benchmarks. This breadth demonstrates that the PRM-based approach is not tailored to a specific model family and provides useful empirical evidence for the effectiveness of test-time scaling for MLLMs.

4. **Empirical comparison against ORM and Self-Consistency**: The ablation study (Figure 4, Table 4) provides a head-to-head comparison of different critic strategies under the same BoN framework, showing that PRM consistently outperforms both ORM and SC across different N values. The analysis of why ORM performance saturates at larger N is informative.

5. **Multi-turn training formulation**: Formulating PRM training as a multi-turn chat task that leverages the generation ability of MLLMs is a clean and implementable design. The inference-time efficiency advantage (single forward pass via '+' placeholder logit probability) over autoregressive MLLM judges is a practical contribution.

## Weaknesses
### Major Weaknesses

**W1. Missing statistical significance and variance reporting (Validity Risk)**

All BoN results in Table 2 are reported as point estimates without standard deviations, confidence intervals, or significance tests. Since the BoN procedure involves sampling N=8 reasoning paths with temperature 0.7, the selection process has inherent stochasticity. Without multi-seed reporting (minimum 3 independent runs), readers cannot assess whether the reported gains (e.g., +0.7 on MMMU for InternVL2.5-78B, or +1.3 on MathVision for MiniCPM-V2.6) are statistically reliable or within noise. This is especially concerning given that some per-benchmark gains are small (<2 points) while the paper makes strong claims ("greatly enhances," "consistently outperforms"). *Impact*: The core empirical conclusion that VisualPRM significantly improves MLLM reasoning is weakened. *Fix*: Report all BoN results as mean ± std over ≥3 independent sampling runs, and include a paired significance test (e.g., Wilcoxon signed-rank) across benchmarks for each policy model. (See Page 6 - Section 4.1 Results paragraph.)

**W2. Potential confirmation bias in automatic labeling pipeline (Methodological Soundness)**

The Monte Carlo pipeline for step correctness estimation uses the same model family (InternVL2.5) for both generating solutions and estimating step correctness via continuations. This creates a risk of confirmation bias: if the model makes systematic reasoning errors (e.g., consistently misinterpreting certain geometry configurations), the continuations will likely propagate the same error, inflating mc_i values for incorrect but internally consistent steps. The paper reports only ~10% incorrect steps — this low proportion may partly reflect labeling bias rather than genuine solution quality. The paper does not provide a human validation study comparing automatic labels against human judgments on a random subset. *Impact*: The training data quality is unverified, and the PRM may learn to predict step correctness based on internally consistent but factually incorrect reasoning. *Fix*: (1) Conduct a small-scale human validation study (e.g., 200 samples, dual annotation) and report inter-labeler agreement (Cohen's kappa) between automatic and human labels. (2) Discuss the confirmation bias concern explicitly and consider using a different model for the Monte Carlo estimation. (See Page 4 - Process Supervision Generation subsection.)

**W3. Unfair ORM comparison (Fairness of Baselines)**

The ORM is constructed by collapsing step-level labels into a single outcome label, which inherently discards the step-wise signal. While the paper notes data is "nearly identical," this construction creates an asymmetric comparison: PRM is trained with richer supervision. The paper does not report ORM performance on VisualProcessBench, making it impossible to assess whether ORM's lower BoN performance is due to weaker step-level understanding or simply the label construction. Furthermore, ORM's performance degradation beyond N=64 (Best-of-128 < Best-of-64) is noted but not analyzed. *Impact*: The claim "PRMs consistently outperform ORMs" may be overstated — a fairer comparison would use an ORM trained with step-level logit averaging rather than outcome-level collapse. *Fix*: (1) Report ORM F1 scores on VisualProcessBench. (2) Add an ORM variant trained by averaging step-level logits. (3) Analyze why ORM saturates at large N and discuss implications. (See Page 7 - Section 4.3 Effects of BoN.)

**W4. Training-inference distribution mismatch in PRM scoring (Methodological Rigor)**

During training, VisualPRM is formulated as a multi-turn chat where the model autoregressively generates correctness tokens (+, -) after each step. During inference, however, the model computes step scores in a single forward pass by interpreting the logit probability of '+' as the step score, without actually generating the token. This creates a distribution mismatch: the model was trained to generate correctness tokens as continuations, but during inference it uses pre-generation logits. The paper does not verify whether the logit-based scoring preserves the same ranking as autoregressive token generation. *Impact*: The effectiveness of the inference-time shortcut is assumed but not validated, and it may not correspond to the training objective. *Fix*: (1) Add a calibration study showing high correlation (Spearman ρ) between logit-based scores and autoregressive token predictions on a validation set. (2) Consider using a binary classification head on the final hidden state during training to align with the inference procedure. (See Page 4 - VisualPRM Overview and Inference subsections.)

**W5. Generic and non-actionable limitations section (Completeness)**

The Limitations paragraph is a single generic statement acknowledging "limited exploration of training and modeling strategies" without specifying which concrete strategies remain unexplored, what the practical failure modes of VisualPRM are, or under what conditions the approach may underperform. Important unaddressed limitations include: (a) potential confirmation bias in labeling (W2), (b) only 8B scale explored, (c) benchmark limited to math/logic reasoning, (d) no OOD robustness evaluation. *Impact*: The limitations do not usefully guide future research and read as a placeholder. *Fix*: Replace with 3-4 concrete, bullet-scoped limitations as described in the Conclusion annotation. (See Page 8 - Conclusion Limitations paragraph.)

### Minor Weaknesses

**W6. Abstract lacks structured logical flow.** The current abstract is a single dense paragraph that mixes problem, solution, results, and filler. It does not cleanly separate the specific gap addressed (lack of multimodal PRMs) from the contributions. Recommended: adopt a 4-5 sentence structure (problem → gap → method → key result → bounded implication). (See Page 0 - Abstract.)

**W7. Overclaim on "first multimodal process supervision dataset."** The phrase "first" (used in Related Work) is a strong novelty claim that cannot be verified in Retrieval-Disabled Mode. The authors should qualify with "to our knowledge" and clarify the boundary between VisualPRM400K and existing multimodal preference/reasoning datasets with step annotations. (See Page 3 - Process Reward Models paragraph.)

**W8. Step score aggregation by simple averaging is not well justified.** The ablation shows averaging > min/max, but does not explore position-aware weighting (despite evidence that errors concentrate in the middle of solutions). The phrase "Without further explanation" dismissively under-motivates this design choice. (See Page 4 - Inference stage paragraph.)

**W9. MLLM-as-a-Judger comparison lacks controlled size baseline.** The comparison pits VisualPRM-8B against much larger models (InternVL2.5-78B) without a same-size prompted MLLM baseline. The efficiency advantage is also not contextualized against the training cost required to obtain VisualPRM. (See Page 8 - MLLM-as-a-Judger paragraph.)

**W10. Class imbalance not analyzed.** Only ~10% of steps are incorrect, but no analysis is provided on how this affects PRM training — e.g., whether the model simply learns to predict '+' for most steps (as the MLLMs it criticizes do). A per-class precision/recall analysis on a held-out set is needed. (See Page 4 - Statistics subsection.)

## Score
**Final Score: 6/10**

**Scoring Rationale (Research Value + Novelty as Primary Dimensions):**

The paper makes a practically useful contribution by providing the first large-scale multimodal process supervision dataset (VisualPRM400K) and a dedicated evaluation benchmark (VisualProcessBench), both of which fill genuine gaps in the MLLM ecosystem. The empirical finding that PRMs can serve as effective critics for multimodal test-time scaling is consistent with the text-only PRM literature and extends it to the multimodal domain. The multi-turn training formulation and efficient single-forward-pass inference are technically sound.

However, the score is moderated by the following factors:

1. **Research value/novelty (moderate)**: The core methodology (Monte Carlo-based automatic process supervision, value/advantage-based PRM formulations) is adapted from existing text-only PRM work (MathShepherd, OmegaPRM) without significant multimodal-specific innovation. The main novelty is the scale and modality, which is valuable but incremental. The "first multimodal process supervision dataset" claim requires external verification.

2. **Validity concerns (several major issues identified)**: Missing statistical significance testing (W1), potential confirmation bias in labeling (W2), unfair ORM comparison (W3), and training-inference mismatch (W4) collectively reduce confidence in the reported results. These issues are fixable but currently weaken the empirical contribution.

3. **Empirical evidence (good breadth, limited depth)**: The evaluation covers multiple model families and scales, which is a strength. However, the lack of variance reporting, limited analysis of failure cases, and absence of OOD evaluation limit the depth of empirical validation.

4. **Reproducibility (promising)**: The commitment to open-source data, model, and benchmark is commendable. The method description is generally clear, though the training-inference mismatch needs clarification.

The identified major weaknesses are fixable with additional experiments and analysis (variance reporting, human validation study, fairer ORM baselines). With these addressed, the manuscript could reach 7-8/10.