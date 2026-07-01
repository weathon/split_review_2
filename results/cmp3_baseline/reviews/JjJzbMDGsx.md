## Summary

The paper introduces the Language Confusion gate (LCG), a plug-in intervention that reduces language mixing errors in large language models without requiring model retraining. The method uses norm-adjustment self-distilation to predict permissible language families and mask disallowed logits at confusion points. Evaluations across multiple models show LGC reduces confusion by an order of magnitude while maintaining task performance.

## strengths

1. **Novel approach**: LGC is a light-weight, plug-in solution that operates at confusion points without base model modification. This avoids the trade-offs common in retraining-based methods.
2. **Well motivated analysis**: The paper provides three key observations (confusion is rare, correct language is among top predictions, token norm bias favors high-resource languages) that ground the method.
3. **Strong experimental results**: LGC reduces confusion significantly across multiple models (Qwen3, Llama3.1, gemma3, gpt-oss) on both no-think and thinking tasks, with minimal impact on task performance (bleu, accuracy, pass rates).
4. **Ablation and comparison**: The norm-adjustment ablation shows LGC-adjust consistently improves results, and comparison with baseline methods (icl, greedy, orpo) demonstrates LGC's effectiveness.

## weakness

### Fatal
None. The paper's core claims are well supported.

### Major
1. **Script-level granularity limitation**: The gate operates at broad language family level (CJ, Latin, Symbols, LowRes) and cannot resolve confusion between languages sharing the same script (e.g., Spanish vs English) or between two low-resource languages. This is a fundamental limitation.
2. **Code-switch impact**: While LGC reduces legitimate code-switch rates (table 5 shows reduction from 46.34 to 25.90 for Qwen3-8B), the post intervention rates remain above the baseline (claud sonnet 4 23.29) and not much below ground truth answer rate (38.36). This suggests the gate may be too conservative for some contexts.

### minor
1. **Training data scope**: The gate is trained on ~78k samples covering 200 languages, but the distribution across language families may not fully represent low-resource languages (table 1 shows low-res% as 0.07 for Qwen3-30B, 0.14 for Qwen3-8B). This could affect prediction accuracy for those languages.
2. **Evaluation dataset choice**: The paper uses FLores-NO-Latin and INclude instead of LCB, but the reasoning for not using LCB is not fully explained (the LCB may require natural code-switch and its detector may produce false positives). This could weaken the evaluation comparability.

### Trivia
1. **Overhead measurement**: The production system timing shows only 0.4% increase (15.95ms vs 15.99ms), but this is measured for 100 token output with 2000 input length and 8 concurrence. The overhead may vary for longer outputs or higher concurrence.
2. **Intervention rate**: The measured intervention rates (0.38% for Qwen3-8B, 0.33% for Llama3.1-8B) are low, but the paper does not report rates for other models or tasks.

## nice-to-haves
- **Fine-grained language gate**: Future work could develop more granular language-specific gating to handle same-script confusion.
- **Dynamic threshold**: The gate could adapt its masking threshold based on context (e.g., code-switch likelihood) to better balance legitimate mixing.
- **Cross-model validation**: Extending evaluation to more commercial models (e.g., DeepSeek-v3.1, gemini-2.5-pro) would strengthen general claims.

## novel insights
The paper's key novel insight is that token output norm bias favors high-resource languages, which contributes to language confusion. This is a mechanistic observation that leads to norm-adjustment self-distilation. The gate trained on the model's own debiased top-k/p predictions is a practical, efficient intervention that avoids retrading. The analysis that confusion is rare and correct language is among top predictions also provides a foundation for the method.

## suggestions
1. **Develop language-specific gating**: Extend the gate to finer granularity (e.g., per language pairs) to handle same-script confusion.
2. **Validate on more commercial models**: Test on DeepSeek-v3.1, gemini-2.5-pro, and others to confirm general effectiveness.
3. **Provide more code-switch analysis**: Show how the gate preserves legitimate mixing in diverse contexts (e.g., coding, language study) with examples.

## score and decision
The paper is a solid contribution with strong evidence and practical value. The main limitation (script-level granularity) is a major weakness but not fatal. The experimental results are compelling and the method is clearly motivated. Overall, the paper meets high standards for ICLR.

Score: 8

Decision: accept

My final score: 8
My final decision: accept