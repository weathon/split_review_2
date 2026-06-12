## Summary
This paper introduces the Language Confusion Gate (LCG), a lightweight two-layer MLP that predicts permissible language families at each decoding step and masks tokens from disallowed scripts, addressing language confusion in multilingual LLMs without modifying the base model. The gate is trained via norm-adjusted self-distillation, leveraging the mechanistic insight that output token embedding norms are systematically biased toward high-resource languages. Experiments across Qwen3, Llama3.1, Gemma3, and GPT-OSS show order-of-magnitude reductions in confusion rates while preserving task performance.

## Strengths
- **Well-motivated empirical analysis of the problem.** The paper provides solid evidence that language confusion is pervasive across both open-source and SOTA commercial models (Table 2), demonstrates that the confusion token is the top-1 candidate 56.74% of the time (making greedy decoding insufficient), and that correct-language tokens appear in the top-3 99.29% of the time—motivating a logit-level intervention. The embedding norm analysis (Table 1, Figure 2) provides a clean mechanistic explanation for a subset of confusion errors.

- **Practical, efficient, and well-engineered method.** LCG adds only 0.4% latency overhead, does not modify the base model, is compatible with speculative decoding, and achieves order-of-magnitude reductions in confusion (e.g., CJ confusion from 4.5% to 0.1% on Qwen3-8B). The intervention rate is impressively sparse (~0.3-0.4% of generated tokens), and the authors compare against five meaningful baselines (greedy decoding, ICL, ORPO, LCG without rules, LCG-unadjusted) across multiple models and benchmarks.

- **Thoughtful handling of code-switching.** The authors explicitly address the key concern that suppressing confusion could eliminate legitimate code-switching, conducting both token-level analysis (86.7% of human-validated code-switch points preserved) and output-level analysis (Table 5). The FLORES-NO-LATIN / FLORES-WITH-LATIN partitioning is a well-designed evaluation strategy.

## Weaknesses
### Fatal
None.

### Major
- **Aggressive suppression of legitimate code-switching.** While the authors frame the code-switching results positively, the numbers tell a more concerning story. For Qwen3-8B, the code-switch rate drops from 46.34% to 25.90%, which is substantially *below* the ground-truth answer rate of 38.36%. This means LCG is not merely moderating but actively suppressing legitimate multilingual behavior below what should be expected. The authors acknowledge this but frame it as "more cautious" rather than as a substantive limitation. This trade-off between confusion reduction and code-switching suppression deserves deeper analysis—is the gate too conservative, and what downstream effects does this have on multilingual task quality?

- **Coarse granularity limits practical impact.** The four-family classification (CJ, Latin, Symbols, Low-Res) means LCG cannot address confusion between languages sharing the same script (English/Spanish, Arabic/Hebrew, Hindi/Bengali, etc.) or between different low-resource languages. The "Low-Res" category groups together Arabic, Hebrew, Korean, Thai, Russian, Vietnamese, Greek, and dozens of other scripts. Since the evaluated benchmarks focus on CJ-vs-other and Latin-vs-other confusion, the paper's results represent the best case for the method's granularity. The authors acknowledge this limitation in the discussion but it significantly bounds the contribution's generality.

### Minor
- **Potential label inconsistency in Table 3.** The table header says "Effectiveness of LCG Intervention on 'No-Think' Models" but includes Qwen3-30B-A3B-Thinking-2507 and GPT-OSS-20B models, while the description in the experimental setup indicates these are thinking models. Table 4 then appears to repeat evaluation for thinking models on a different benchmark. If the table captions are swapped, this should be corrected; if not, the paper needs to clarify which models are being evaluated where.

- **No analysis of error cascading from masking decisions.** The intervention rule in Section 4.3 that "always allows the language family of the immediately preceding non-symbol token" could be exploited: if a confusion token slips through, subsequent tokens in that same language would be allowed by this rule. The paper does not analyze whether masking at one step can cause generation quality degradation at subsequent steps (e.g., producing a semantically wrong but script-correct token).

- **Narrow evaluation scope.** All translation evaluations are from English to target languages. The paper does not test non-English source languages, multi-turn conversations, or scenarios where code-switching is central to the task (e.g., bilingual customer service). The INCLUDE benchmark tests general knowledge but doesn't specifically stress-test multilingual reasoning scenarios.

### Trivial
- Table 4 is titled "Effectiveness of LCG Intervention on 'No-Think' Models" but the surrounding text discusses "thinking model intervention"—likely a typo in the table caption.

## Nice-to-Haves
- A deeper analysis of *why* certain legitimate code-switch instances are suppressed by LCG (are they systematically associated with specific language families or contexts?) would strengthen the understanding of failure modes.
- Evaluation on confusion between languages of the same script family (e.g., Arabic and Hebrew, which share many characters) to better quantify the boundaries of the approach.
- Analysis of whether LCG's intervention rules could be learned rather than hand-designed, potentially improving their precision.

## Novel Insights
The paper's most novel and practically valuable observation is that output token embedding norms create a systematic bias favoring high-resource language tokens, and that dividing logits by embedding norms (removing the norm factor from the dot product decomposition) can recover correct-language tokens that were otherwise ranked below confusion tokens. This is a clean, theoretically grounded insight (Equation 2) that goes beyond just describing the problem—it identifies a specific geometric mechanism in the model's output layer. The demonstration that this norm adjustment meaningfully improves gate training accuracy (LCG-adjusted vs. LCG-unadjusted consistently better across all models and benchmarks) validates this insight.

## Suggestions
- Add a detailed error analysis of cases where LCG fails—either missing confusion or suppressing legitimate code-switching. Understanding the failure modes would be more valuable than aggregate metrics alone.
- Include a confidence calibration analysis: when the gate decides to intervene, how confident is it, and does calibration quality correlate with intervention accuracy?
- Consider a more fine-grained token classification (e.g., splitting Low-Res into script-based subgroups) and analyze how this affects both the confusion reduction and code-switching preservation.

## Score and Decision
The paper presents a clean, well-motivated, and practical method for a real and demonstrably widespread problem. The mechanistic insight about embedding norm bias is genuinely interesting, the empirical evaluation is extensive across multiple models and benchmarks, and the method is computationally lightweight. However, the coarse language family granularity limits generality, the aggressive suppression of legitimate code-switching (below ground-truth rates) is a notable limitation that the paper under-acknowledges, and the evaluation focuses on the most favorable confusion types (cross-script). These factors place it in borderline accept territory—the contribution is solid and useful, but not yet comprehensive enough to be a definitive solution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <score>Accept</score>