##Summary

This paper introduces the Language Confusion Gate (LCG), a lightweight, plug-in decoding-time intervention that reduces unintended language mixing in multilingual LLMs. LCG uses a small two-layer MLP trained via norm-adjusted self-distillation on the frozen model's own debiased top-k/p predictions to predict which language families (CJ, Latin, Symbols, Low-Res) are permissible at each generation step, then dynamically masks inappropriate tokens. The method is motivated by three observations: language confusion is rare, correct-language tokens are usually among top predictions, and output token embedding norms bias sampling toward high-resource languages. Experiments across Qwen3, Llama3.1, Gemma3, and GPT-OSS show that LCG reduces confusion by an order of magnitude without degrading task performance or eliminating legitimate code-switching.

## Strengths

- **Practical and lightweight solution**: LCG is a small MLP that operates at decoding time without modifying the base LLM, adding only ~0.4% overhead. This makes it directly deployable in production systems, unlike methods requiring retraining or fine-tuning.
- **Strong empirical results**: Across multiple models (Qwen3-8B/30B, Llama3.1-8B, Gemma3-12B, GPT-OSS) and both thinking/no-think modes, LCG reduces CJ and Latin confusion by an order of magnitude (e.g., Qwen3-8B Latin% from 12.1% to 2.0%) while maintaining or slightly improving BLEU/accuracy scores.
- **Principled analysis of the problem**: The paper provides a clear mechanistic analysis of language confusion, including the token embedding norm bias (Table 1, Figure 2) and the finding that correct-language tokens appear in top-3 99.29% of the time. This analysis directly motivates the norm-adjusted self-distillation training approach.
- **Careful handling of code-switching**: The paper distinguishes between harmful confusion and legitimate code-switching, and evaluates LCG's impact on code-switching using the FLORES-WITH-LATIN subset and human-validated examples. LCG preserves 86.7% of natural code-switch points.
- **Comprehensive baselines**: Comparison with ICL, greedy decoding, ORPO, and an ablation without intervention rules (Figure 3) demonstrates that LCG outperforms these alternatives, especially in preserving task performance while reducing confusion.

## Weaknesses

### Fatal
None.

### Major
- **Script-level granularity limits applicability**: LCG groups tokens into only four broad families (CJ, Latin, Symbols, Low-Res), so it cannot distinguish between languages sharing the same script (e.g., English vs. Spanish, or two low-resource languages). The paper acknowledges this but does not evaluate how often such confusions occur or propose a path to finer-grained control. This is a fundamental limitation that may restrict practical usefulness in many multilingual scenarios.
- **Pseudo-target quality is not analyzed**: The gate is trained on pseudo-targets derived from the model's own norm-adjusted top-k/p predictions. While the paper argues that correct-language tokens are usually in top-5, there is no analysis of how often these pseudo-targets are incorrect (e.g., when the model is genuinely uncertain or when confusion is severe). Noisy pseudo-targets could lead to a poorly calibrated gate, and the paper does not report gate accuracy or confidence calibration.
- **Code-switching evaluation is limited**: The human-validated code-switch experiment (86.7% preservation) does not report the number of examples, inter-annotator agreement, or selection criteria. The FLORES-WITH-LATIN comparison (Table 5) uses ground-truth and Claude Sonnet 4 as references, but these are not necessarily optimal code-switch rates. The paper does not measure whether LCG over-suppresses code-switching in contexts where it is genuinely needed (e.g., technical terms in low-resource languages).

### Minor
- **Missing comparison with neuron suppression methods**: The related work mentions neuron suppression (Nie et al., 2025) and post-hoc smoothing (Ji et al., 2025) as alternative decoding-time interventions, but these are not included in the experimental comparison. Including them would strengthen the evaluation of LCG's relative effectiveness.
- **Table 4 title is incorrect**: The table is labeled "No-Think Models" but reports results on Humaneval-XL for thinking models. This is a minor but confusing error.
- **Efficiency measurement is narrow**: The 0.4% overhead is reported only for Qwen3-30B-A3B with specific settings (2000 input, 100 output, concurrency 8). Overhead may vary with model size, hardware, and generation length. The paper could provide more systematic latency profiling.
- **No error analysis**: The paper does not analyze cases where LCG fails (e.g., incorrectly masking correct tokens or failing to mask confusion tokens). Understanding failure modes would help practitioners assess risk.

### Trivial
- The paper states "language confusion occurs rarely" but then reports confusion rates of 1–12% in some models, which is not negligible. The statement is relative but could be clarified.

## Nice-to-Haves

- Evaluate LCG on a broader set of language pairs, especially those sharing the same script (e.g., Spanish/Portuguese, Hindi/Urdu) to understand the script-level limitation.
- Provide gate accuracy metrics (precision/recall for each language family) on a held-out validation set.
- Include a comparison with neuron suppression or other decoding-time interventions from the related work.
- Analyze the effect of different top-k/p thresholds used in pseudo-target generation on gate performance.

## Novel Insights

The key insight is that token embedding norm imbalance systematically biases LLMs toward high-resource languages, and that correcting for this bias during training (via norm-adjusted self-distillation) produces a more accurate language gate than using raw logits. The observation that correct-language tokens are almost always in the top-3 predictions (99.29%) justifies a masking-based intervention rather than more complex approaches. The paper also demonstrates that a lightweight, plug-in gate can be trained on the model's own debiased predictions, avoiding the need for external supervision or model modification.

## Suggestions

- Add an analysis of gate prediction accuracy (precision/recall per language family) on a validation set to quantify how often the gate makes correct/incorrect predictions.
- Include a comparison with at least one other decoding-time intervention (e.g., neuron suppression from Nie et al., 2025) to better contextualize LCG's performance.
- Clarify the code-switching evaluation: report the number of human-validated examples, inter-annotator agreement, and the distribution of code-switch types (e.g., technical terms, quotations, bilingual explanations).
- Discuss potential failure modes and how the intervention rules (Section 4.3) mitigate them, with concrete examples.

## Score and Decision

The paper addresses an important and practical problem with a well-motivated, lightweight solution. The empirical results are strong across multiple models and tasks, and the analysis of token embedding norm bias provides a principled foundation. The main limitations are the script-level granularity and the lack of analysis on pseudo-target quality and gate accuracy. Despite these, the paper makes a solid contribution that is likely to be useful to the community.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>