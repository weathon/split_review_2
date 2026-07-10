Based on the favorability signals — where the core strengths (empirical finding, Qwen3 analysis, memorization check) all score at or near 1.00, and the weaknesses cluster around 0.44–0.64 (moderately negative but not fatal) — the paper's genuine contributions clearly outweigh its addressable limitations. I now produce the final consolidated review.

---

## Summary

This paper revisits the idea of using a prompted off-the-shelf LLM as a guardrail against prompt injection attacks. Prior work (Liu et al., 2024) had found prompting-based defenses largely ineffective, but those results were based on older, weaker LLMs. The paper shows that with modern reasoning-capable LLMs (GPT-4o, GPT-4.1), a carefully designed prompt achieves detection FPR and FNR both below 1% on the AgentDojo benchmark and end-to-end attack success rates approaching 0%. The paper also introduces a "detect and remove" pipeline (rather than simply discarding contaminated inputs) using fuzzy matching, evaluates across three benchmarks against seven baselines, and conducts informative ablations on model size and reasoning mode using the Qwen3 family. The core contribution is the empirical finding that this simple, easy-to-deploy approach now works far better than previously believed.

## Strengths

- **Clear, practically important empirical finding (Tables 1 and 2):** The paper convincingly demonstrates that prompting a modern off-the-shelf LLM (GPT-4o, GPT-4.1) to detect prompt injections achieves FPR and FNR both below 1% on AgentDojo and ASR of 0.00% for PromptArmor-GPT-4.1. This is a non-obvious finding because prior work using weaker LLMs had concluded prompting-based defenses were largely ineffective. Revisiting this with stronger models has real practical value for practitioners deciding what defense to deploy.

- **Informative model scaling analysis (Section 4.4, Figure 3):** The systematic variation of Qwen3 models across sizes (0.6B, 8B, 32B) and reasoning modes provides genuine insight. The finding that reasoning helps mid-sized models but cannot compensate for insufficient capacity in the 0.6B model is non-trivial and well-supported. The Qwen3-32B achieving near-perfect performance comparable to GPT-4.1 demonstrates that strong results do not require the largest proprietary models.

- **Responsible memorization check (Section 4.5):** The paper verifies that GPT-4.1 has not simply memorized benchmark inputs (average similarity 0.34, only 3.5% above the 0.6 threshold), ruling out a common concern with benchmark evaluations of LLMs and strengthening the credibility of the results.

- **Comprehensive evaluation design:** The paper evaluates across three benchmarks (AgentDojo, Open Prompt Injection, TensorTrust), compares against seven diverse baselines (Table 2), and measures both detection metrics (FPR, FNR) and end-to-end task metrics (UA, ASR) across multiple axes including reasoning mode, model size, and adaptive attacks.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Baseline comparisons are confounded by model scale.** The key baselines (Deberta, Llama Prompt Guard 2, DataSentinel) use much smaller models than PromptArmor's GPT-4.1 — e.g., DataSentinel uses Mistral-7B. Table 2 shows that even PromptArmor-GPT-3.5, despite using a much weaker model, still achieves lower ASR (6.84%) than Deberta (18.92%), Llama Prompt Guard 2 (34.66%), and DataSentinel (38.63%), suggesting the prompting approach has genuine advantages beyond model scale. However, a controlled comparison where the same base model serves both PromptArmor and a fine-tuned baseline would strengthen the claim that "prompting an off-the-shelf LLM should be regarded as a standard baseline." The Qwen3-32B results partially address this concern by showing strong prompting performance at a smaller scale, but the comparison is not direct.

- **Adaptive attack evaluation is limited in scope.** The paper tests only one automated red-teaming method (AgentVigil). The absence of human-crafted adaptive attacks or attacks targeting specific components of PromptArmor (e.g., the fuzzy matching mechanism) leaves the robustness claim less thoroughly tested than would be ideal for a proposed standard baseline. (Note: the concern that AgentVigil-Adaptive's reduced ASR against the undefended system indicates a weak search is a misunderstanding — attacks optimized to evade a specific defense are expected to behave differently against an undefended system — but the broader point about limited scope stands.)

- **Removal step (fuzzy matching) is not separately evaluated.** Section 3.1 describes the removal mechanism, but the paper never evaluates whether the guardrail LLM correctly extracts the injection text, whether fuzzy matching removes too much or too little, or how often the guardrail paraphrases rather than extracts the injection verbatim. The end-to-end ASR of 0.00% for GPT-4.1 implicitly validates the full pipeline, but decomposition of where failures occur would strengthen the analysis, especially since "detect and remove" (rather than "detect and discard") is a claimed advantage over prior work.

- **No discussion of computational cost or limitations.** The paper does not analyze the cost and latency implications of running a GPT-4.1-class guardrail LLM on every tool call. For practitioners evaluating whether to adopt this as a baseline, this information is relevant. The paper also lacks a dedicated limitations section discussing scenarios where PromptArmor might underperform.

### Trivial
None.

## Nice-to-Haves
- Include a controlled comparison using the same base model for both PromptArmor and a fine-tuned detection baseline.
- Decompose the removal step's accuracy (how often extraction succeeds, how often fuzzy matching causes collateral damage).
- Add a brief cost/latency analysis and a limitations paragraph.

## Removed Points
These points from the input review were removed (treated with caution):
- **Claim that PromptArmor with GPT-3.5 is "worse than several baselines on some metrics"** — removed because it is factually incorrect against the Deberta example given; Table 2 shows GPT-3.5 PromptArmor achieves BETTER (lower) ASR (6.84%) than Deberta (18.92%), Llama Prompt Guard 2 (34.66%), and DataSentinel (38.63%).
- **Claim that AgentVigil-Adaptive's 21.46% ASR against the undefended system indicates a weak search** — removed because it misunderstands the experimental setup; attacks optimized to evade a specific defense are expected to have different effectiveness against the undefended system.
- **Formatting/style nitpicks and speculation about missing appendix content** — removed per instructions.

## Novel Insights
None beyond the paper's own contributions. The reviews faithfully reflect the paper's content but do not surface any observation that the paper itself does not already make clear.

## Suggestions
1. Add a controlled comparison using the same base model for both PromptArmor and a fine-tuned detection baseline (e.g., fine-tune GPT-4o-mini or Qwen3-32B on a prompt injection detection dataset). This would separate the effect of prompting methodology from model capability.
2. Decompose the removal step's accuracy: evaluate how often the guardrail correctly extracts the injection text, characterize fuzzy matching failures, and report the fraction of end-to-end successes attributable to correct removal vs. correct detection alone.
3. Include a brief discussion of cost/latency tradeoffs and a limitations paragraph acknowledging scenarios where PromptArmor may underperform.
4. For the adaptive attack evaluation, consider testing against human-crafted attacks or an additional automated method to broaden the robustness analysis.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>