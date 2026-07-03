Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proposes **Language Confusion Gate (LCG)**, a lightweight two-layer MLP inserted at decoding time that predicts permissible language families per step and masks disallowed tokens. It is trained via **norm-adjusted self-distillation** — using the frozen LLM's own norm-adjusted predictions as pseudo-targets — turning a known mechanistic bias (token embedding norms favoring high-resource languages) into a training signal. The method is evaluated across five open-source models (Qwen3-8B/30B, Llama3.1-8B, Gemma3-12B, GPT-OSS) on translation (FLORES+) and reasoning (INCLUDE, Humaneval-XL) benchmarks, showing substantial confusion reduction with negligible overhead (~0.4% latency) and no degradation in task performance. A careful analysis of legitimate code-switching preservation (86.7% token-level retention of human-validated switches) directly addresses the hardest part of the problem.

## Strengths

- **Mechanistically grounded training signal**: The paper identifies that output token embedding norms are systematically skewed toward high-resource languages (Table 1: Qwen3-8B has 10.74% CJ tokens vs. 0.14% Low-Res tokens in the top 5% of norms) and shows that norm-adjusted logits reveal the correct language family (Figure 2). Training the gate on norm-adjusted self-distillation turns this bias into a useful signal. The ablation confirms norm adjustment is essential — e.g., Latin confusion on Llama3.1-8B drops from 5.7% (LCG-unadjusted) to 2.9% (LCG-adjusted).

- **Quantitative evidence that legitimate code-switching is preserved**: The paper directly tackles the hardest part of the problem — distinguishing erroneous confusion from valid code-switching. It reports that LCG allows English tokens at 86.7% of human-validated code-switch points (Section 5.3) and that post-intervention code-switch rates on FLORES-WITH-LATIN remain near or above the Claude Sonnet 4 reference baseline (Table 5: Qwen3-8B drops from 46.34% to 25.90% vs. 23.29% reference).

- **Sparse, empirically validated intervention minimizing side effects**: The intervention rate is only 0.38% for Qwen3-8B (523/139,354 tokens) and 0.33% for Llama3.1-8B (545/162,846 tokens) on FLORES-NO-LATIN, and latency overhead is 0.4% (15.95ms → 15.99ms per step, Section 6). This directly confirms the method is lightweight.

- **Comprehensive multi-model evaluation**: Five models spanning diverse architectures, sizes (8B–30B), and reasoning paradigms (thinking/no-think modes) consistently show confusion reduction — e.g., CJ confusion on INCLUDE drops from 2.21% to 0.11% for Qwen3-30B (Table 3), demonstrating model-agnostic effectiveness.

- **Ablation of both norm adjustment and intervention rules**: The paper ablates norm adjustment (LCG-adjusted vs. LCG-unadjusted, Table 3) and the intervention rules ("No Rule" in Figure 3), providing evidence for the necessity of each design choice.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **ORPO baseline not fully specified**: The ORPO implementation is described in one sentence: "prepare a multilingual dataset, and synthesize samples with language confusion as rejected samples similar to Lee et al. (2025)" with no training hyperparameters, data size, or validation setup. The observed accuracy degradation (61.4→57.3 on Qwen3-8B INCLUDE, 46.1→43.2 on Llama3.1-8B) could partially reflect suboptimal ORPO tuning rather than an intrinsic limitation of ORPO for this task. Since the paper uses this comparison to argue LCG's advantage over retraining approaches, more rigor — reporting hyperparameters and discussing whether the degradation was robust to tuning — would strengthen the claim.

- **No statistical uncertainty reported**: All results are presented as point estimates without confidence intervals, standard deviations, or mention of number of runs/seeds. This is especially relevant for very small confusion rates (e.g., CJ% dropping "from 0.12% to 0.00%" on Qwen3-30B thinking, Table 4), where a single seed's difference of a few examples could change the measured rate significantly. The thinking-model evaluation repeats each prompt 10 times (which is good), but the no-think evaluations (FLORES+, INCLUDE, Tables 3 and 5) do not report repetition or variance.

- **Potential FLORES+ overlap between training and evaluation**: The gate is trained on a composite dataset that includes FLORES+ (Section 5.1), and FLORES-NO-LATIN — a primary evaluation benchmark — is derived from FLORES+ (Section 5.2). The paper does not explicitly address whether specific sentences appear in both sets. That said, since the gate is a 2-layer MLP operating on hidden states (not a lookup table), memorization of individual sentences is highly unlikely, and the main results are corroborated by INCLUDE and Humaneval-XL, which provide independent evidence. An explicit statement on overlap (and ideally, results on a non-overlapping subset) would resolve the concern cleanly.

### Trivial

- The "order of magnitude" claim in the abstract is supported for the strongest cases (e.g., Qwen3-30B CJ% 1.0→0.0, Qwen3-8B CJ% 4.5→0.1) but is weaker for Gemma3-12B (CJ% 0.2→0.1, ~2×; Latin% 1.0→0.5, ~2×). The paper uses "often" to qualify this, but more precise quantification of the improvement range across models would be helpful.

## Nice-to-Haves

- Reporting intervention rates and token-level code-switch preservation (already done for one analysis: 86.7%) more broadly across all models would strengthen the preservation claim.
- A comparison with the neuron-suppression method of Nie et al. (2025) on at least one model/dataset would be informative, though the paper's related work section notes this approach and the scope choice is reasonable.

## Removed Points

- **"Missing ablation: intervention rules alone without the gate"** — Removed. Rules 1 and 2 are constraints defined in terms of the gate's predictions (Rule 2: "if the gate's prediction is contradicted by high-confidence model output") and cannot function as standalone interventions. Rule 3 (persistence) alone would prevent all language switching, including legitimate code-switching. The reverse ablation ("No Rule" in Figure 3, which tests the gate without rules) is the informative direction and is already included. The requested ablation is not well-defined and was removed as a misunderstanding of the rules' role.

- **"LCB benchmark not used"** — Removed. The paper provides a clear, reasonable rationale (natural code-switching in LCB queries, unreliable language detector). This is a methodological choice, not a weakness.

- **"Low-Res category is never masked"** — Removed. The paper acknowledges this limitation in Section 6 ("the current approach is limited by its script-level granularity"). This is a known design constraint and honestly stated.

- **"No comparison with neuron-suppression method"** — Removed. It would be a nice addition but is not a weakness given the paper's scope and the existing baseline set (ICL, greedy, ORPO).

## Novel Insights

None beyond the paper's own contributions. The paper itself already provides the key novel insights: (1) that embedding norm bias can be leveraged as a self-supervised signal via norm-adjusted self-distillation, and (2) that an extremely lightweight gate (2-layer MLP, 0.4% overhead) with sparse intervention (~0.35% of tokens) can effectively suppress language confusion while preserving legitimate code-switching. The harsh critic's observations are refinements, not novel findings.

## Suggestions

1. **Report ORPO hyperparameters and tuning**: Provide learning rate, batch size, number of epochs, data size, and validation selection for the ORPO baseline. Discuss whether additional tuning could close the accuracy gap with LCG.

2. **Add variance estimates**: Run the no-think evaluations (Tables 3, 5) with at least 3 seeds and report means with standard deviations or confidence intervals. This would significantly strengthen confidence in the small confusion rate reductions.

3. **Clarify FLORES+ overlap**: State explicitly whether any FLORES+ sentences used in evaluation also appear in the gate's training data. If overlap exists, report results on the non-overlapping subset separately.

4. **Qualify the "order of magnitude" claim**: Provide the range of improvement factors across all models/configurations rather than highlighting only the best case.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>