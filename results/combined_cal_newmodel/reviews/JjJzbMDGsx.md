Here is my final consolidated review.

## Summary

This paper introduces the Language Confusion Gate (LCG), a lightweight MLP that operates at decoding time to filter tokens from unintended language families in multilingual LLM generation. The method is motivated by a mechanistic finding — output token embedding norms are systematically larger for high-resource languages, creating a bias — and trained via norm-adjusted self-distillation using the model's own debiased predictions as pseudo-targets. Evaluated across 5 base models (Qwen3-30B, Qwen3-8B, Llama3.1-8B, Gemma3-12B, GPT-OSS) on translation and reasoning benchmarks, LCG reduces language confusion by roughly an order of magnitude with 0.4% overhead and minimal impact on task metrics.

## Strengths

- **Clear mechanistic insight grounded in evidence (Section 3.2).** The finding that output token embedding norms are systematically larger for high-resource languages is concretely demonstrated in Table 1 (e.g., Qwen3-8B: 10.74% of CJ tokens vs. 0.14% of Low-Res tokens in the top 5% of embedding norms) and Figure 2 (norm-adjustment removes CJ tokens from top-10 logits at a Hebrew confusion point). This identifies a specific mechanism underlying language confusion.

- **Elegant training signal from the insight itself.** Norm-adjusted self-distillation (Section 4.2) uses the model's own debiased predictions as pseudo-targets, avoiding hand-labeling while being internally consistent with the analysis.

- **Genuinely lightweight intervention.** The 0.4% overhead (Section 6) and ~0.33–0.38% intervention rate (Section 5.3) are well-measured and make the method practical for deployment — a key advantage over retraining-based approaches.

- **Cross-model consistency.** LCG is evaluated on 5 different base models (Qwen3-30B, Qwen3-8B, Llama3.1-8B, Gemma3-12B, GPT-OSS) spanning both "thinking" and "no-think" architectures, with directionally consistent confusion reductions across all of them.

## Weaknesses

### Major

- **The ORPO baseline comparison is insufficiently documented to support the claimed advantage (Section 5.3, lines 298–312).** The paper states "we prepare a multilingual dataset, and synthesize samples with language confusion as rejected samples similar to Lee et al. (2025)" but provides no details on dataset size, quality of synthesized samples, ORPO hyperparameters (β, learning rate, epochs), or whether training was tuned to convergence. Since the paper claims ORPO degrades INCLUDE accuracy (Qwen3-8B: 61.4→57.3; Llama3.1-8B: 46.1→43.2) — a key selling point of LCG's advantage over training-based methods — the reader cannot distinguish whether this reflects a genuine limitation of ORPO or suboptimal implementation. This is an addressable weakness but, as presented, weakens the claim that LCG is superior to training-time alternatives.

### Minor

- **No variance or uncertainty reported for any result.** All confusion rates in Tables 3, 4, 5 are point estimates. For rates as small as 0.0–0.4%, a single confused response could move the metric substantially. The thinking-model evaluation (Section 5.2) mentions repeating each prompt 10 times, but no variance across repetitions is reported. Without confidence intervals or bootstrap estimates, the reliability of headline reductions (e.g., 0.0% CJ confusion on Qwen3-30B) cannot be assessed.

- **The BLEU scores on FLORES-NO-LATIN are partially confounded with confusion reduction.** Since FLORES-NO-LATIN references contain no Latin/CJ characters, any confused output containing such characters mechanically lowers BLEU, so when LCG removes them, BLEU could mechanically increase even if underlying translation quality is unchanged. The INCLUDE accuracy results (which are not subject to this confound, since it is QA not translation) partially mitigate this concern, and BLEU values do not decrease (they slightly increase or stay flat), which still supports the "no degradation" claim. However, the paper would be stronger with an explicit control — e.g., measuring BLEU on a confusion-free subset.

- **The gate training procedure is underspecified with respect to what the gate actually learns (Section 4.2).** The gate is trained on all ~78K tokens from the composite dataset, not just confusion points. At non-confusion steps, the pseudo-target trivially matches the token's actual language family. The gate may therefore learn general language identification from hidden states rather than confusion-specific detection. The paper does not report language-family prediction accuracy (precision/recall per family) to verify the gate is working as intended at confusion points specifically.

- **The persistence rule (Rule 3 in Section 4.3)** — always allowing the previous token's language family — could over-correct at legitimate language-switch boundaries (e.g., a bilingual response switching from a CJ explanation to a Latin technical term). The paper does not analyze how often this rule triggers when it should not.

### Trivial

- **Table 4 caption error.** The caption reads "Effectiveness of LCG Intervention on 'No-Think' Models" but the table evaluates thinking models on Humaneval-XL (Pass@1/Pass@10 metrics, reasoning token lengths). This is a copy-paste error.

## Nice-to-Haves

- Report Wilson confidence intervals or bootstrap estimates for the small confusion percentages, especially the 0.0% results.
- Evaluate on a confusion-free subset of FLORES to more cleanly disentangle confusion removal from task performance measurement.
- Provide full ORPO hyperparameters, dataset size, and training details, and consider running multiple seeds.
- Report the gate's language-family precision/recall per family to verify it distinguishes confusion from normal generation.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **[Code-switch evaluation has "fundamental methodological flaw"]** — REMOVED. The paper uses human annotators to judge whether the base model's code-switching is "natural and appropriate" (Section 5.3, line 284). This is an independent human judgment of legitimacy, not circular conditioning on the base model. The evaluation is not exhaustive of all legitimate code-switching scenarios, but it is not fundamentally flawed as the critic claimed.

- **[Section 3.2 norm analysis doesn't directly measure norm bias's causal contribution]** — REMOVED. The paper explicitly acknowledges this limitation: "Norm bias can account for a subset of such errors but cannot fully explain language confusion" (line 155). The analysis is presented as suggestive evidence motivating the method, not as a complete causal accounting.

- **[Script-level granularity cannot handle same-script confusion]** — REMOVED. The paper openly acknowledges this as a limitation (Section 6, line 320). Listing it as a weakness penalizes the paper for being honest about its scope.

- **[Section 3.1 analysis only on Qwen3-8B]** — REMOVED. While this is true, the method is validated across 5 models and the core finding (embedding norm imbalance) is shown across multiple models in Table 1. This is a reasonable initial analysis scope.

- **Generic/superficial strengths from input** — REMOVED (e.g., "the paper addresses an important problem" — this is generic without specific evidence tying the paper's execution to that importance).

## Novel Insights

The harsh critic's most insightful observation is that the BLEU metric on FLORES-NO-LATIN is partially confounded because removing confused characters from the output mechanically brings it closer to the reference, independent of translation quality changes. This nuance is worth the authors' attention, though the INCLUDE accuracy results and the fact that BLEU does not decrease already provide meaningful evidence for the "no degradation" claim. The critic's concern about what the gate actually learns (language ID vs. confusion detection) is also a thoughtful point that the authors could address with a targeted analysis.

## Suggestions

- Provide full details of the ORPO training setup (dataset size, hyperparameters, convergence verification). Running multiple seeds would also help establish the robustness of the observed accuracy degradation.
- Report confidence intervals or bootstrap estimates for the small confusion percentages (particularly the 0.0% results reported for Qwen3-30B CJ confusion).
- Add a control experiment: evaluate BLEU on a confusion-free subset of FLORES to decouple confusion removal from translation quality changes.
- Report the gate's language-family prediction accuracy on confusion points specifically, to verify it learns confusion detection rather than general language identification.

---

## Calibration Report

All anchors retrieved from `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/`:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Llamas (mostly) think in English | fSbPwHjdDG.md | 3.00 | 1 | Yes | Narrower scope (1 task, 1 model), poorly organized. Our paper has broader evaluation and a practical method. |
| Babel Tower (multilingual code LLM) | eznTVIM3bs.md | 5.25 | 1 | Yes | Similar analytical contribution but narrower scope (code only). Our paper has comparable strengths but a more practical contribution. |
| Crosslingual Knowledge Barriers | BCyAlMoyx5.md | 5.67 | 1 | Yes | Analysis-only paper without a practical method contribution. Our paper is stronger due to the LCG method. |
| Language Models Implicitly Learn a Unified Representation Space | FrFQpAgnGE.md | 7.00 | 1 | Yes | Stronger contribution with multimodal scope and thorough causal evidence. Our paper is more narrowly focused. |
| Constrained Decoding for Cross-lingual Label Projection | DayPQKXaQk.md | 7.00 | 2 | Yes | Cleaner experimental design and more rigorous comparisons, but narrower task scope. Comparable structure. |
| MLLM Dynamic Correction Decoding | 4z3IguA4Zg.md | 6.00 | 2 | Yes | Most directly comparable: empirical insight → lightweight decoding intervention. Similar strengths (insight, efficiency, cross-model eval) and weaknesses (empirical tuning, limited theoretical grounding). |
| Mexa | hsMkpzr9Oy.md | 5.40 | 1 | No | Evaluation-only paper without a method. |
| Scaling Laws for Multilingual LMs | T2h2V7Rx7q.md | 5.25 | 1 | No | Theoretical scaling law paper, different contribution type. |

**Bracket determination (Round 1):** The most relevant anchor range is 3.00 (Llamas think in English) to 7.00 (Constrained Decoding / Unified Representation Space). Our paper clearly exceeds the 3.00 anchor (more models, practical method, better presentation). It is below the 7.00 anchors which have stronger causal evidence or cleaner experimental design. The MLLM Dynamic Correction Decoding anchor at 6.00 is the closest structural match.

**Narrowing (Round 2):** Comparing item-level favorability ratings: the 6.00 anchor's weaknesses (favorability as low as -0.39) are comparable in severity to our strongest negative (-0.06). The 7.00 anchors have more negative-rated weaknesses (as low as -3.62 for Constrained Decoding). Our paper has slightly weaker evaluation rigor (no variance, partial BLEU confound) than the 6.00 anchor, which ran standard benchmarks. Balanced against this, our paper has a cleaner mechanistic insight and broader model coverage (5 models vs 4). The 6.00 anchor's contribution was rated as having limitations in generalizability and ad-hoc design choices — similar concerns apply here. **Final score: 6.0.**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>