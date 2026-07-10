Now let me write the final consolidated review.

## Summary

This paper presents the first large-scale (400,000+ GPU-hours) empirical study of reinforcement learning scaling for LLMs. It fits sigmoidal compute-performance curves to RL training trajectories and validates that extrapolations from partial runs accurately predict extended training, demonstrated on a flagship 100,000 GPU-hour run. Through systematic ablations at the 8B parameter scale, the paper develops SCALERL, a recipe combining existing methods (PipelineRL, CISPO loss, FP32 precision fix, prompt-level loss averaging, etc.) that achieves predictable scaling and state-of-the-art performance compared to DeepSeek GRPO, Qwen DAPO, Magistral, and MiniMax-M1. The leave-one-out ablation study (16,000 GPU-hours per variant) reveals that most individual components primarily affect compute efficiency (B-parameter) rather than asymptotic performance (A-parameter), while their cumulative effect produces a robust recipe.

## Strengths

- **Unprecedented empirical scale.** The paper reports over 400,000 GPU-hours of experiments, with individual LOO runs at 16,000 GPU-hours and a flagship 100,000 GPU-hour single run — 6× the compute of ProRL. At this scale, the experiments are genuinely informative in a regime where most academic work cannot operate.

- **Extrapolation validated, not just asserted.** The paper consistently fits curves on the first half of each run's compute budget and verifies against extended training points. This is done across LOO experiments (8k→16k), the 100k-hour run (50k→100k), the MoE run (16k→45k), and the cross-recipe comparison (Figure 2). The visual alignment between extrapolated and observed points is convincing.

- **Leave-one-out ablation at meaningful scale.** Each LOO variant runs for 16,000 GPU-hours — not at toy scale where all methods look similar. The finding that most components affect efficiency (B) more than the asymptote (A), while the cumulative effect produces a robust recipe, is a genuinely informative empirical result that goes beyond prior work.

- **Cross-recipe scaling comparison.** The paper compares SCALERL against four recently reported recipes (DeepSeek GRPO, Qwen DAPO, Magistral, MiniMax-M1) and compares not just final numbers but the full scaling trajectories (A and B parameters), which is more informative than single-point comparisons.

- **Multi-axis scaling validation.** Section 5 investigates model scale (8B dense → 17B×16 MoE), sequence length (14k→32k), batch size, and generations per prompt, showing the framework holds across these variations.

## Weaknesses

### Major

**No statistical uncertainty on any result.** All scaling curves present point estimates of A, B, and C_mid with no confidence intervals, error bars, or replication. The validation pass rate is measured on 1,000 held-out prompts with 16 generations each — this has sampling variance that is never quantified. The curve-fitting procedure (non-linear least squares on a 4-parameter sigmoid) propagates this noise into uncertainty on the fitted parameters. Every experiment — including the flagship 100,000 GPU-hour run — is a single trajectory with no seed variation. For a paper that frames itself as establishing a "scientific framework" and "principled understanding" (Abstract), the absence of any statistical quantification is a significant gap. Bootstrapping over prompts or generations would produce confidence intervals at negligible additional compute cost and would immediately strengthen every comparison in the paper.

**GPU-hours as the compute measure conflates algorithmic, systems, and hardware efficiency.** The x-axis in all scaling curves is GPU-hours, which conflates (a) algorithmic data efficiency, (b) implementation efficiency, and (c) hardware utilization. The paper explicitly acknowledges this for the PipelineRL comparison (line 136: "PipelineRL reduces the amount of idle time in the training process"), but does not discuss it as a general limitation of the framework. For the LOO ablations (all within the same codebase), this confound is minimal. However, for the cross-recipe comparison in Figure 2, differences in implementation quality or pipeline efficiency could masquerade as algorithmic scaling advantages. The paper would be stronger with a clear statement of whether its goal is *algorithmic* scaling (requiring tokens or gradient steps as the x-axis) or *practical* scaling (where GPU-hours as a mixed metric is acceptable but should be explicitly scoped).

### Minor

**Re-fitting LOO curves with fixed A may exaggerate efficiency differences.** In the LOO analysis, the paper averages A across all runs and re-fits with this fixed value to highlight B differences. The original fits show A varying from 0.590 to 0.610 (Figure 5 table). Fixing A assumes these differences are noise rather than signal, which could inflate the apparent B differences that become the headline finding for the LOO study (that most components affect B, not A). The paper should justify this assumption or report results both ways.

**No seed variation for any experiment.** While the paper validates extrapolation across many settings (8 LOO runs, MoE, scaling axes, cross-recipe comparisons), each is a single trajectory. Without knowing trajectory-to-trajectory variance, readers cannot assess how reliable the extrapolation would be under different random seeds or data splits. Even 2–3 seeds for one or two key comparisons at moderate scale would substantially strengthen the evidential weight.

**Excluding the early low-compute regime.** The paper excludes the first ~1,500 GPU-hours for curve fitting (line 104), meaning the "predictability" claim does not cover the beginning of training. The paper references Appendix A.7 (stripped by the parser) for robustness analysis, so sensitivity to this cutoff is not assessable from the main text.

**Null result lacks statistical grounding.** The finding that "generations per prompt leaves fitted scaling curves essentially unchanged" (line 220) is stated without statistical power analysis. With single-run data, the paper cannot distinguish between "no effect" and "an effect too small to detect in one trajectory."

**Framing as "first large-scale systematic study" (line 9) is somewhat overstated.** ProRL (Liu et al., 2025a) and LitePPO (Liu et al., 2025c) study RL scaling, and the paper cites them. The novelty lies in the predictive framework and scale, which is a defensible distinction, but the "first" claim should be qualified.

## Nice-to-Haves

- Add uncertainty quantification (bootstrapped confidence intervals on A, B, C_mid) using the existing validation data.
- Normalize compute by tokens processed or gradient steps, or explicitly frame the work as studying practical (not purely algorithmic) scaling and acknowledge the confound as a limitation.
- Run 2–3 seeds for one or two key comparisons at moderate scale.
- Discuss whether iid validation scaling correlates with out-of-distribution generalization scaling as compute increases, since the paper notes some algorithmic choices help generalization more.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Comparison with other methods is unverifiable without Appendix A.17"** — Removed per policy: the parser strips appendix sections from all papers; they exist in the original submission. The description of how comparison methods were configured is in Appendix A.17.
- **"Equation (1) is not conceptually novel"** — The paper explicitly cites prior work (Ruan et al., 2024; Srivastava et al., 2022) for this form and positions its contribution as the empirical application and validation at scale, not the mathematical form itself.
- **"Speculative concern about interruption mechanism creating distributional mismatch"** — No evidence provided for this concern; the paper explicitly addresses the mechanism and compares it against length-penalty (Section 4, LOO-length-penalty).
- **"SCALERL combines existing components"** — The paper is transparent about this (line 66); it is a factual description, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add confidence intervals to all fitted scaling parameters (A, B, C_mid) via bootstrapping over validation prompts — this is the single highest-leverage improvement and requires no additional experiments.
- Explicitly acknowledge the GPU-hours confound as a limitation in the main text, and clarify whether the framework is intended for algorithmic scaling or practical scaling.
- Provide per-task breakdown for downstream evaluations (AIME-24) to quantify the variance.
- Include a brief analysis of how sensitive the fitted parameters are to the early-regime cutoff point.

## Score and Decision

### Calibration Anchors

**Round 1 (Bracketing):**
- `8QTpYC4smR` avg=1.00, Reject — Systematic review paper; not comparable to this empirical study. [not itemized]
- `Uj0h13lVrR` avg=1.00, Reject — GFlowNets paper; domain mismatch. [not itemized]
- `5kMwiMnUip` avg=1.40, Reject — Jailbreaking paper; domain mismatch. [not itemized]
- `gwZ90hFSL2` avg=1.00, Reject — Cross-lingual robotics; domain mismatch. [not itemized]
- `zEhTnQZB3D` avg=2.33, Reject — Continual RL; domain mismatch. [not itemized]
- `jOuHjFw71C` avg=3.00, Reject — LRM planning evaluation; domain mismatch. [not itemized]
- `2HN97iDvHz` avg=3.00, Reject — Data center scheduling; domain mismatch. [not itemized]
- `RiDtvlNiqp` avg=3.00, Reject — Foundation models for exploration; domain mismatch. [not itemized]
- `D0XpSucS3l` avg=4.50, Reject — Scaling laws for pre-training agents/world models (itemized). Weaker than this paper: single simulation environment, no extrapolation validation, no practical recipe. Our paper is clearly stronger.
- `xGM5shdGJD` avg=5.20, Reject — Scaling law estimation methodology (itemized). Methodologically similar but focused on pre-training LM scaling laws, not RL. Our paper has stronger empirical scale and demonstrated extrapolation.
- `iIGNrDwDuP` avg=5.25, Reject — Scaling laws for DiT; different domain (image generation). [not itemized]
- `BDisxnHzRL` avg=4.25, Reject — Scaling laws for downstream performance prediction. Narrower scope, less empirical scale. [not itemized]
- `LYS3RhIYCq` avg=6.20, Reject — Scaling laws for IL in games (itemized). Comparable quality but its forecasted agent underperformed predictions, while our extrapolations validate accurately. Our paper is somewhat stronger.
- `VNckp7JEHn` avg=5.75, Accept — Inference scaling laws; different setting (inference vs training). [not itemized]
- `iZeQBqJamf` avg=6.50, Accept — Language models scale reliably with over-training (itemized). Most comparable anchor: similar methodology (scaling law fitting + validation), similar attention to practical relevance. Our paper is slightly stronger empirically (larger scale, RL domain, validated extrapolation) but weaker on uncertainty quantification.
- `gjC3QvVh1U` avg=6.25, Reject — AlphaZero neural scaling. Different RL setting (AlphaZero vs LLM RL). [not itemized]
- `wg1PCg3CUP` avg=8.00, Accept — Scaling laws for precision; different focus (numerical precision). [not itemized]
- `pISLZG7ktL` avg=8.00, Accept — Data scaling laws in IL for robotics (itemized). Stronger overall execution: real-world validation, cleaner methodology, more rigorous. Our paper has larger compute scale but less experimental control.
- `Tzh6xAJSll` avg=7.60, Accept — Associative memory scaling; theoretical, not empirical. [not itemized]
- `rfdblE10qm` avg=8.00, Accept — Reward modeling theory; not about scaling. [not itemized]

**Round 2 (Narrowing within 5.5–7.5):**
- `Eo7kv0sllr` avg=6.50, Accept — Emulator for fine-tuning LLMs. Different approach (emulation vs direct scaling). [not itemized]
- `lDbjooxLkD` avg=6.00, Accept — Predicting emergent abilities via infinite resolution evaluation. Different framing but similar validation paradigm. [not itemized]
- `xI71dsS3o4` avg=5.75, Accept — Survey of scaling law fitting techniques. Methodologically adjacent. [not itemized]
- `o9YC0B6P2m` avg=6.75, Reject — Scaling law with LR annealing. Strong mathematical formulation but rejected (possibly due to novelty concerns). [not itemized]

**Score Placement.** The round-1 bracket placed this paper between the 4.5-level papers (weaker: single environment, no extrapolation validation) and the 6.5–8.0-level papers (stronger: cleaner methodology, uncertainty quantification, or real-world validation). The round-2 narrowing within 5.5–7.5 confirmed that this paper sits above the 5.75–6.0 level papers (Inference Scaling Laws, Emergent Abilities prediction) on empirical contribution and below the 8.0-level papers (Data Scaling Laws in IL for Robotics, Scaling Laws for Precision) on methodological rigor.

Compared to the closest anchor — "Language models scale reliably with over-training" (6.50, Accept) — our paper shares strong strengths in empirical validation (both have favorability ~15.5 for strong experiment results) but has a significantly more damaging weakness (favorability=-1.18 for no uncertainty quantification vs that paper's worst items around 2.0–3.5). This weakness places our paper slightly below that anchor.

**Final score: 6.0** — a genuine empirical contribution at unprecedented scale, with convincing extrapolation validation, held back from a higher score by the complete absence of uncertainty quantification (a significant gap for its "scientific framework" framing) and the GPU-hours confound in cross-recipe comparisons. These issues are fixable. Recommend acceptance.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>