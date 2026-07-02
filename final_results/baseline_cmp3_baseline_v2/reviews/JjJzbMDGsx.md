## Summary

This paper introduces the **Language Confusion Gate (LCG)**, a lightweight, plug-in decoding-time intervention that reduces language confusion (unintended language mixing) in multilingual LLMs without modifying the base model. The method trains a small two-layer MLP via norm-adjusted self-distillation on the frozen model’s own debiased predictions to dynamically mask tokens from disallowed language families. Evaluated across Qwen3, Llama3.1, Gemma3, and GPT-OSS in both standard and reasoning modes, LCG reduces confusion rates by an order of magnitude while preserving task performance and legitimate code-switching, with minimal computational overhead (~0.4%).

## Strengths

- **Practical and lightweight solution**: LCG requires no model retraining, adds only ~0.4% computational overhead, and is compatible with speculative decoding, making it directly deployable in production systems.
- **Well-motivated by mechanistic analysis**: The paper provides clear evidence that language confusion stems from token embedding norm imbalance biasing high-resource languages, and that correct-language tokens typically rank within top-5 predictions. These insights motivate both the norm-adjusted self-distillation and the logit-masking approach.
- **Comprehensive evaluation across diverse settings**: Experiments span multiple model families (Qwen3, Llama3.1, Gemma3, GPT-OSS), both thinking and no-think modes, and multiple benchmarks (FLORES, INCLUDE, Humaneval-XL). The paper also evaluates impact on legitimate code-switching, which is a critical consideration often overlooked in prior work.
- **Strong empirical results**: LCG consistently reduces CJ and Latin confusion by large margins (e.g., Qwen3-8B CJ confusion from 4.5% to 0.1%, Latin from 12.1% to 2.0%) while maintaining or slightly improving BLEU/accuracy scores. Ablations confirm that norm adjustment and the intervention rules both contribute positively.
- **Open-source datasets**: The paper commits to releasing specialized training and evaluation datasets covering 200+ languages, which would benefit the community.

## Weaknesses

### Fatal

None.

### Major

- **Coarse language family granularity**: The four-family grouping (CJ, Latin, Symbols, Low-Res) cannot distinguish between different Latin-script languages (e.g., Spanish vs. English) or between different low-resource languages. The authors acknowledge this, but it limits the method’s applicability in settings where more fine-grained control is needed. This is not fatal but is a significant practical limitation.

### Minor

- **Definition of confusion rate at response level**: The metric reports the percentage of *responses* containing at least one erroneous character. A single confused token in a long response flags the entire response, which may overstate the problem. Per-token confusion rates would provide a complementary view. That said, the authors do report token-level intervention rates (0.33-0.38%), partially addressing this.
- **Ambiguity about “GPT-OSS”**: The paper evaluates on a model called “GPT-OSS” cited as “OpenAI, 2025”, but this appears to be a non-standard or hypothetical model. Its architecture and availability are unclear, which weakens reproducibility claims for that specific experiment. The paper’s conclusions do not rely on this model alone, but clarity is needed.
- **Comparison with ORPO may be incomplete**: The ORPO baseline is implemented by synthesizing confusion data specifically for this task, which may not be the most competitive or well-tuned application of ORPO. A more standard baseline (e.g., language-consistent prompting with strong in-context examples) or an additional post-hoc smoothing baseline (Ji et al., 2025) would strengthen the comparison.
- **No statistical significance or confidence intervals**: Results are reported as point estimates without variance measures. Given the stochasticity of sampling, confidence intervals or multiple-seed runs would increase confidence in the reported reductions.

### Trivial

- Table 4 title says “No-Think Models” but the section describes it as “Thinking Model Intervention” — minor labeling inconsistency.

## Nice-to-Haves

- Analyze whether LCG’s performance degrades on languages where the model has minimal training data (e.g., truly low-resource languages beyond the “Low-Res” category).
- Study the effect of different gate architectures (e.g., deeper MLP, linear probe) on the trade-off between confusion reduction and code-switch preservation.
- Provide per-language breakdowns of confusion reduction (e.g., Arabic vs. Hebrew vs. Thai) to show the method’s uniformity across target languages.

## Novel Insights

The key insight is that token embedding norm imbalance systematically biases LLMs toward high-resource language tokens, and that norm-adjusted logits (dividing by token embedding norm) reveal the model’s genuine language preference even at confusion points. This observation directly leads to a training signal (norm-adjusted self-distillation) that is cleaner than raw logits. The paper also makes the practical observation that confusion is rare (~0.3% of tokens) but harmful, motivating a lightweight intervention that fires only when needed.

## Suggestions

- Clarify what “GPT-OSS” refers to and provide a public model identifier or explain its provenance to improve reproducibility.
- Add per-token confusion rates alongside per-response rates for a finer-grained evaluation.
- Report results with confidence intervals (e.g., bootstrap resampling) to quantify the reliability of the observed reductions.

## Score and Decision

This paper tackles an important and practical problem with a well-motivated, lightweight, and empirically effective solution. The contributions are solid: a novel gating mechanism trained via norm-adjusted self-distillation, thorough evaluation across diverse models and settings, and careful handling of the confusion-vs-code-switch trade-off. The weaknesses are minor and do not invalidate the core claims.

MY FINAL SCORE: 7.0

MY FINAL DECISION: Accept