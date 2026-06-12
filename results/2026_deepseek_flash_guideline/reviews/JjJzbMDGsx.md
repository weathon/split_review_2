Here is the final consolidated review.

## Summary

This paper introduces Language Confusion Gate (LCG), a lightweight, plug-in decoding-time intervention that reduces language confusion (unintended language mixing) in LLM outputs. LCG consists of a small 2-layer MLP trained via norm-adjusted self-distillation — using the model's own debiased top-k/p predictions as pseudo-targets for predicting allowed language families (CJ, Latin, Symbols, Low-Res). The method builds on a mechanistic analysis showing that output token embedding norms are systematically larger for high-resource languages, creating a logit bias. Evaluated across 5 models on 3 benchmarks, LCG reduces confusion rates by roughly an order of magnitude (e.g., Qwen3-8B CJ%: 4.5%→0.1%, Latin%: 12.1%→2.0%) with minimal overhead (0.4% inference time increase).

## Strengths

1. **Mechanistic discovery of embedding norm bias (Section 3.2, Table 1, Figure 2).** The paper provides a clean geometric decomposition (logit_i = ||h||·||e_i||·cos_sim) showing that output token embedding norms are systematically larger for high-resource languages. Table 1 quantifies this across 5 models — e.g., CJ tokens constitute 10.74% of the top-5%-norm group in Qwen3-8B while Low-Res tokens account for only 0.14%. This is a novel, well-evidenced mechanistic finding of independent interest.

2. **Controlled ablation isolating norm adjustment (Table 3: LCG-unadjusted vs. LCG-adjusted).** The paper directly compares training the gate with vs. without norm adjustment. Results consistently show that norm adjustment improves confusion reduction — e.g., Llama3.1-8B Latin% drops from 5.7% (unadjusted) to 2.9% (adjusted) — cleanly validating the norm-adjustment component of the training pipeline.

3. **Comprehensive multi-model, multi-task evaluation (Tables 3, 4, 5).** LCG is evaluated on 5 distinct models (standard and reasoning architectures) on 3 benchmarks, measuring both confusion reduction and task-performance preservation. Results show consistent reductions (e.g., Qwen3-8B Latin% 12.1%→2.0%) without degrading BLEU or accuracy, demonstrating generality across architectures.

4. **Empirically measured low computational overhead (Section 6).** Benchmarked on Qwen3-30B-A3B: 15.95ms/step without LCG vs. 15.99ms with LCG (0.4% increase), confirming practical deployability.

5. **Sparse intervention rate (Section 5.3).** LCG intervenes on only 0.38% of tokens (Qwen3-8B) and 0.33% (Llama3.1-8B), demonstrating precise targeting.

## Weaknesses

### Fatal

None.

### Major

1. **No variance or uncertainty reported for any result (Tables 3, 4, 5).** All confusion rates, BLEU scores, and accuracy numbers are reported as single values without standard deviations, confidence intervals, or run-to-run variability. For small percentages in the 0.0–0.4% range, a few tokens' difference can significantly change the reported rate. The "0.0%" values are particularly problematic — they mean "zero detected in the sample," not "zero in the population." Without error bars, it is impossible to assess whether differences like 0.1% vs. 0.0% (CJ% for Gemma3-12B, Table 3) or 71.55 vs. 70.83 (INCLUDE accuracy for Qwen3-30B) are meaningful. This is the single most impactful gap in an otherwise solid evaluation.

2. **Confusion-point analysis based on a single model and dataset (Section 3.1).** The key observation that "correct-language tokens appear within top-3 99.29% of the time at confusion points" — which motivates the entire masking approach — is derived from Qwen3-8B on FLORES-NO-LATIN only. Given that Table 1 reveals substantial differences in token embedding distributions across models (e.g., GPT-OSS has 0.00% CJ tokens in the top-5%-norm group), the generality of the 99.29% figure is unverified. This finding should be replicated for at least one additional model.

3. **Code-switch preservation analysis has selection bias (Section 5.3, Experiment 1).** The first code-switch experiment selects examples where the model (without LCG) already generated English tokens that human annotators deemed "natural code-switch." This selects for cases where the model's distribution already permits the code-switch — precisely where the gate would be most permissive. The reported 86.7% preservation rate may overestimate the method's selectivity. A stronger test would sample all confusion points during code-switch contexts and measure what fraction LCG preserves.

### Minor

1. **Comparison with the closest prior methods absent.** The paper discusses Nie et al. (2025) and Ji et al. (2025) in Related Work — both propose post-hoc interventions (neuron suppression and smoothing respectively) that, like LCG, do not require model retraining. Neither is included as a baseline in Figure 3. While reproducing these methods across 5 models is non-trivial (especially neuron suppression which requires per-model mechanistic analysis), their absence leaves the paper's positioning against the most directly related work empirically unsubstantiated.

2. **Pseudo-target quality at confusion points is not analyzed.** The gate is trained using norm-adjusted pseudo-targets, but the paper does not analyze what fraction of these pseudo-targets are correct specifically at confusion points (where they matter most). Section 3.2 acknowledges that norm adjustment "cannot fully explain language confusion," and Figure 2 shows that the post-adjustment top-k set still contains Latin tokens at a Hebrew confusion point. The paper's own evidence suggests the pseudo-targets can be noisy at confusion points, yet no analysis quantifies this noise or its effect on gate training. The empirical results show the method works despite this, but the mechanism by which the gate learns correct behavior from partially noisy signals is unexamined.

3. **No per-language breakdown.** The evaluation aggregates across languages within each family (e.g., Arabic, Hebrew, Korean, Thai for Low-Res). Confusion rates may vary substantially by language. A per-language breakdown would help identify where LCG works well vs. poorly.

4. **No sensitivity analysis for gate capacity or training data size.** The gate uses a fixed 2-layer MLP and 78K training samples. No ablation explores how performance depends on these choices.

### Trivial

- The figure caption for Figure 2 textually describes the post-adjustment top-10 as "mostly Latin tokens" but the table data shows a Hebrew token (נ״) at rank 1 after adjustment. The caption should be updated for accuracy.

## Nice-to-Haves

- Evaluate on LCB (Language Confusion Benchmark) as a common reference point, perhaps after filtering out queries that require code-switching (similar to how FLORES was partitioned).
- Provide bootstrap or binomial confidence intervals for the main confusion-rate results.
- Include an analysis of what fraction of pseudo-targets at confusion points are correct, to explicitly address the training-signal-noise concern.

## Removed Points

- **"The pseudo-target is systematically Latin=1, Low-Res=0 at confusion points"** (from Harsh Critic, Issue 1): REMOVED because it is factually incorrect. Figure 2's data table shows Rank 1 after norm adjustment is a Hebrew (Low-Res) token (נ״) with 43.75% probability. The pseudo-target at this step would include Low-Res=1 (correct). The critic appears to have misread "mostly Latin" as "all Latin."
- **"ICL and greedy baselines are too weak for LCG beating them to be informative"**: REMOVED. These are standard, well-motivated baselines: ICL tests whether prompting alone suffices, and greedy tests whether conservative sampling suffices. They establish the need for a learned intervention.
- **"The reasoning models claim is vague"**: REMOVED. It is a brief contextual observation, not a core claim.
- **"BLEU differences may be noise"**: REMOVED as it is subsumed by the broader variance concern.
- **Several Strength Finder claims about "comprehensive" comparison or general praise**: REMOVED where generic (e.g., "this paper addressed an important problem"). Concrete strengths (norm bias discovery, controlled ablation, multi-model evaluation, overhead numbers, intervention rate) are retained.

## Novel Insights

The critic's concern about pseudo-target quality at confusion points is directionally valid — the paper does not analyze this — but its severity is substantially reduced by the actual data in Figure 2 showing that the correct-language (Hebrew/Low-Res) token does surface to rank 1 after norm adjustment (43.75% probability). The more interesting takeaway from the reviews is the tension between the paper's genuine strengths (clean mechanistic analysis, practical method, broad multi-model evaluation) and the single most impactful gap: the complete absence of variance or uncertainty quantification. For a central claim framed around order-of-magnitude reductions in small percentages (0.1–12.1%), the lack of error bars is the clearest actionable weakness.

## Suggestions

1. Add confidence intervals (bootstrap or binomial) to all reported confusion rates and task-performance metrics.
2. Extend the confusion-point analysis (top-3 correct-language accuracy) to at least one additional model to verify generality.
3. Provide per-language breakdowns for the confusion reduction results.
4. Analyze what fraction of pseudo-targets at confusion points are correct, to directly address the training-signal-noise concern.

## Score and Decision

**Calibration anchors (all rounds):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Advancing Cross-Lingual Capabilities for Humanoid Robots | 1.00 | R1-strong-reject | Pseudo-science, unrelated |
| Llamas (mostly) think in English | 3.00 | R1-reject | Single task, single model; LCG is far stronger |
| MLLM can see? Dynamic Correction Decoding | 6.00 | R1-6.0-band | Most structurally similar: analysis → decoding intervention → multi-model eval. LCG has broader model/task coverage but same key gap (no variance) |
| Inference-time Alignment (Nudging) | 6.00 | R2-narrow | Another decoding-time intervention; LCG is comparable in rigor |
| Token-Aware Inference-Time Intervention | 6.00 | R2-narrow | Decoding-time ITI; comparable in rigor |
| Tool Decoding | 6.00 | R2-narrow | Plug-and-play decoding method; similar contribution type |
| The Same but Different (mechanistic interp) | 6.60 | R1-6.0-band | Multilingual mechanistic work; higher rigor but different contribution type |
| DEPT: Decoupled Embeddings | 8.00 | R1-strong-accept | Full pre-training framework, much broader contribution; LCG is not at this level |

**Round 1 bracket:** 5.5–7.0 (between "MLLM can see" at 6.0 and "The Same but Different" at 6.60 — LCG is closer to the former in structure and evaluation profile).

**Final score:** 6.0. The paper presents a genuine contribution: a novel mechanistic insight (norm bias), a practical method, and evaluation across 5 models and 3 benchmarks. However, the lack of variance reporting weakens all quantitative claims about "order-of-magnitude" reductions, and the confusion-point analysis is validated on only one model. These are substantive but addressable gaps. The score reflects a borderline accept — the method has clear value and the analysis is largely sound, but the evaluation rigor needs improvement to be a clear accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>