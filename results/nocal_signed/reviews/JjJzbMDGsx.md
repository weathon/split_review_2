Now let me compile the final review.

## Summary

This paper proposes Language Confusion Gate (LCG), a lightweight plug-in MLP that filters tokens during decoding to mitigate language confusion in LLMs. Trained via norm-adjusted self-distillation using the model's own predictions as pseudo-targets, LCG predicts permissible language families (CJ, Latin, Symbols, Low-Res) at each generation step and masks disallowed tokens. Experiments across Qwen3, Llama3.1, Gemma3, and GPT-OSS show consistent reductions in confusion rates without degrading task performance or eliminating legitimate code-switching, with only 0.33–0.38% token-level intervention.

## Strengths

- **Token embedding norm imbalance analysis (Section 3.2) is a genuine mechanistic finding.** Table 1 shows CJ and Latin tokens disproportionately occupy top embedding norms while low-resource tokens are severely underrepresented (e.g., 0.07% for Qwen3-30B Low-Res vs. 6.52% CJ). Figure 2 concretely demonstrates norm-adjustment promotes correct-language tokens from outside the top-10 to the top position. This analysis is both novel and directly actionable — it motivates the norm-adjusted training procedure.

- **The method is well-motivated by three specific observations (Section 3.1):** (a) confusion is rare → sparse intervention is sufficient, (b) correct-language tokens are in top-k → logit masking can work, and (c) norm bias inflates high-resource logits → training targets should be norm-adjusted. The internal coherence between analysis and method is strong.

- **Careful handling of the confusion vs. code-switching distinction.** The paper explicitly acknowledges language mixing is not always erroneous (Section 3.3), creates FLORES-WITH-LATIN / FLORES-NO-LATIN splits to separate evaluation contexts, and measures impact on legitimate code-switching separately (Section 5.3, Table 5). This is more thoughtful than most prior work.

- **The intervention is genuinely lightweight** — 0.33–0.38% token-level intervention rate, 0.4% overhead per generation step (Section 6) — making it practically deployable as claimed.

## Weaknesses

### Fatal
None.

### Major

- **No uncertainty quantification for low base-rate metrics.** Confusion rates are reported as point estimates with no confidence intervals or standard deviations. With base rates as low as 0.0% vs. 0.2% (e.g., Gemma3-12B CJ confusion: No LCG 0.2% vs. LCG 0.1%; Qwen3-30B CJ: LCG-unadjusted 0.2% vs. LCG-adjusted 0.0%), differences may fall within noise. This is especially important since the paper's strongest claims rely on these small absolute numbers. Bootstrap confidence intervals or multiple seeds would substantially increase confidence in the findings.

- **Response-level confusion metric is coarse and conflates distinct phenomena.** The paper defines confusion as "percentage of model responses that contain at least one character from an unintended language script" (line 229), aggregating at the response level while the paper's own analysis (Section 3.1) operates at the token level. A single stray CJ character flags the entire response. The low BLEU scores (10–17) suggest models struggle with these translation directions, so some "Latin confusion" may reflect fallback behavior when the model does not know the correct translation — a different failure mode from the Chinese-into-Hebrew archetype the method targets. Token-level rates would better align the metric with the paper's own analysis.

### Minor

- **The code-switching preservation framing overstates the findings.** The 86.7% preservation figure comes from evaluating LCG on human-selected "natural" code-switches drawn from the model's *own* outputs — the easiest possible cases. Meanwhile, Table 5 shows code-switch rates drop substantially (e.g., Qwen3-8B: 46.34% → 25.90%, a 44% relative reduction). The paper is transparent about both measurements, but framing "preserves code-switch ability" based on the 86.7% figure while the actual behavioral change is large understates the trade-off.

- **The ORPO baseline comparison is under-specified.** No training hyperparameters are reported (learning rate, epochs, LoRA rank, dataset size). The observed accuracy degradation (Qwen3-8B: 61.4→57.3; Llama3.1-8B: 46.1→43.2) may reflect suboptimal tuning rather than a fundamental limitation of ORPO. This weakens the claim that LCG "outperforms training-based methods."

- **Self-referential training signal limits demonstrable scope.** The gate learns from norm-adjusted versions of the model's own top-k predictions. As the paper acknowledges (line 155), norm bias "cannot fully explain language confusion" — it cannot address English-vs-Chinese (both high-norm) or LowRes-vs-LowRes (both low-norm) confusions. The paper does not evaluate LCG on confusions arising from other mechanisms, so the method's broader generalization is untested. The limitation is discussed in principle but its boundaries are not probed.

- **The "No Rule" ablation lacks quantitative reporting.** The paper states the ablation "can still reduce language confusion without the additional rules" (line 312) but reports only visual results in Figure 3 rather than providing exact numbers alongside Table 3.

### Trivial

- **Table 4 caption incorrectly labels thinking models as "No-Think" Models** (line 273), a copy-paste error since the section and table content clearly discuss thinking models.
- **Training hyperparameters for the gate itself** (epochs, learning rate, optimizer, train/validation split) are not reported, which would aid reproducibility.
- **Commercial model evaluations (Table 2)** do not specify the sampling parameters (temperature, top-k, top-p) used, which can affect confusion rates.

## Nice-to-Haves

- Evaluate LCG on at least one confusion type not mediated by norm bias (e.g., English-Chinese) to clarify the method's scope.
- Report token-level confusion rates alongside response-level rates to align evaluation with the paper's own token-level analysis.
- Analyze residual confusions (e.g., the 2.9% Latin confusion remaining in Llama3.1-8B) to understand gate failure modes.
- Provide quantitative evidence for the claimed issues with the Language Confusion Benchmark (LCB) that motivated not using it.

## Removed Points

These points were raised in the input review but are removed after cross-checking against the paper:
- *Criticism about missing appendix content / proofs:* The parser strips appendix and reference sections from all papers; they exist in the original submission.
- *Criticism about causal language in Section 3.2 ("creates a systemic bias"):* The paper demonstrates the imbalance exists via the logit decomposition; this is a presentation-style point that does not affect the paper's validity.
- *Criticism about the heuristic language-family classification:* The paper acknowledges this limitation explicitly in Section 6 (line 320) as a scope limitation.
- *Criticism about LCB rationale lacking evidence:* This is a reasonable methodological justification, not a core weakness.
- *Criticism about the abstract's "order of magnitude" claim:* The claim is qualified with "often" and holds for most reported cases (e.g., CJ confusion in Qwen3-8B: 4.5%→0.1% is 45×).

## Novel Insights

None beyond the paper's own contributions — the norm imbalance finding and LCG method are the paper's own novel contributions, and the reviews did not surface additional novel perspectives beyond what the paper already presents.

## Suggestions

- Add bootstrap confidence intervals or standard deviations to the main results (Table 3), especially for the low base-rate confusion metrics where point estimates alone are unreliable.
- Strengthen or de-emphasize the ORPO comparison: either report a reasonable hyperparameter search demonstrating adequate tuning, or reframe the comparison as illustrative rather than competitive.
- Report the "No Rule" ablation numbers in a supplementary table.
- Fix the Table 4 caption error.
- Report token-level confusion rates alongside the current response-level rates.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>