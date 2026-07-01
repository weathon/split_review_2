## Summary

This paper identifies a critical failure mode in gradient-ascent-based LLM unlearning: the *squeezing effect*, where suppressing target responses merely redistributes probability mass to semantically related alternatives, causing *spurious unlearning*. The authors propose a **bootstrapping framework** that incorporates the model’s own high-confidence predictions (its *model beliefs*) as additional forgetting targets. Two instantiations are presented: **BS-T** (token-level) suppresses top-\(k\) high-probability tokens alongside the target, and **BS-S** (sequence-level) augments the forget set with sampled high-confidence continuations. Theoretical analysis within the AKG learning dynamics framework shows how BS-T reshapes the residual to spread forgetting pressure over the belief neighborhood. Experiments on TOFU, MUSE, and WMDP with Llama-3 and Zephyr models demonstrate consistent improvements over strong baselines like NPO and RMU, yielding a better balance between forgetting and retention.

## Strengths

- **Novel identification of a genuine failure mode.** The paper clearly reveals the squeezing effect and demonstrates that GA/NPO-based methods often produce only superficial forgetting—a problem that existing metrics (ROUGE, perplexity) fail to capture. The use of LLM-as-judge to expose spurious unlearning is a valuable methodological contribution.
- **Principled and intuitive solution.** The bootstrapping idea—using the model’s own high-confidence outputs as additional unlearning signals—directly addresses the probability redistribution mechanism. BS-T and BS-S are conceptually clean, theoretically justified, and compatible with existing unlearning losses.
- **Theoretical support.** The analysis within the AKG framework (Lemma 5.1, Theorems 5.2 and 5.3) provides a formal understanding of why BS-T mitigates the squeezing effect by reshaping the residual term, and how BS-S aggregates residuals across belief-aligned sequences. This distinguishes the paper from purely empirical work.
- **Comprehensive empirical evaluation.** Experiments span three benchmarks (TOFU, MUSE, WMDP) and multiple model families (Llama 3.2 1B/3B, Llama 3.1 8B, Zephyr-7B, Llama 2 7B) with five strong baselines. Results consistently show BS-S achieving the best aggregate scores.
- **Flexibility and practicality.** BS-T and BS-S can be combined with various base losses (GA, NPO, WGA) and retain regularizations (GradDiff), making the framework easy to adopt in existing pipelines.

## Weaknesses

### Fatal
None.

### Major
- **Incremental gains over state-of-the-art in some settings.** While BS-S often achieves the best aggregate score, the improvement over NPO is sometimes modest (e.g., TOFU 10% Llama 3B: BS-S 0.63 vs. NPO 0.62; TOFU 5% Llama 3B: BS-S 0.60 vs. NPO 0.57). In the 1% setting, the gap is similarly small. The gains are consistent but not dramatic across all configurations, which slightly weakens the claim of a major breakthrough.
- **Theoretical assumptions limit rigor.** The AKG analysis relies on the lazy eNTK regime and first-order expansion, which may not hold for deep, non-linear models during multi-epoch training. The paper acknowledges this limitation but does not provide experiments validating that the dynamics match the theory (e.g., measuring the NTK). The theoretical contribution is suggestive rather than fully rigorous.
- **LLM-as-judge reliability is underexplored.** The Laaj evaluation (§3.1, Fig. 4c) uses Gemini 2.5 Flash as the judge, but no human correlation study, inter-rater reliability analysis, or calibration check is provided. Given that the paper’s core claim of spurious unlearning rests on this evaluation, a stronger validation of the judge is expected. The prompt design is deferred to the appendix, and potential judge bias or inconsistency is not discussed.

### Minor
- **Computational cost of BS-S not thoroughly discussed.** BS-S requires sampling \(N\) high-confidence generations per forget prompt, and possibly doing so multiple times (on-policy variant). The appendix reports training time, but the main text does not quantify the overhead or provide guidance on practical trade-offs between BS-T (cheaper) and BS-S (more thorough).
- **Hyperparameter sensitivity not fully explored in main text.** The choice of \(k\) for top-\(k\) in BS-T, \(\lambda_{\text{BST}}\), \(\lambda_{\text{BSS}}\), and \(N\) are critical. While ablation studies appear in the appendix, the main results do not include error bars or a sensitivity analysis, making it hard to assess robustness.
- **Definition of “model beliefs” is slightly informal.** The paper defines beliefs as high-probability tokens/sequences from the model’s own distribution, but the threshold (top-\(k\) for BS-T, temperature for BS-S) is arbitrary. The connection to the theoretical residual is clear, but a more principled characterization (e.g., based on uncertainty or epistemic vs. aleatoric) would strengthen the framing.

### Trivial
- The term “bootstrapping” is used differently from its common meaning in RL/statistics; the paper defines it explicitly, but a brief note distinguishing it from other uses (e.g., Yarowsky) would help readers.

## Nice-to-Haves

- A small human evaluation of the Laaj judgments (e.g., 50 samples rated by experts) would significantly strengthen the evidence for spurious unlearning and the success of BS methods.
- Sensitivity plots for key hyperparameters (\(k\), \(\lambda_{\text{BST}}\), \(\lambda_{\text{BSS}}\), \(N\)) in the main text, even if as a small figure, would improve reproducibility and practical guidance.
- A comparison with a simple baseline that just augments the forget set with paraphrases from a generic paraphraser (rather than model beliefs) would isolate the benefit of using the model’s own distribution.

## Novel Insights

The key insight is that the root cause of spurious unlearning is not an optimization failure but a fundamental consequence of softmax normalization: lowering the probability of a target token *forces* probability mass to flow elsewhere, and it naturally flows to regions that the model already believes are plausible—i.e., its own high-confidence predictions. This perspective reframes unlearning from a simple parameter-erasure task to a more nuanced problem of reshaping the model’s belief landscape. The bootstrapping idea—harnessing the model’s own predictions as forgetting targets—is a natural and elegant consequence of this reframing. This insight is genuinely novel and could inspire future work on “belief-aware” safety and alignment techniques beyond unlearning.

## Suggestions

1. Provide a brief human-validation study for the LLM-as-judge evaluation, or at least report agreement statistics with human raters on a sample.
2. Include a small figure in the main text showing how the aggregate score varies with \(k\) or \(\lambda_{\text{BST}}\) for a representative setting (e.g., TOFU 10% with Llama 3B).
3. Clarify the practical recommendation for when to use BS-T vs. BS-S based on computational budget and forgetting requirements.
4. Acknowledge more explicitly the theoretical limitations (lazy NTK, first-order) and suggest extensions (e.g., measuring NTK evolution during training) as future work.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>