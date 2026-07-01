## Summary

This paper identifies that language confusion in LLMs stems partly from output token embedding norm imbalance (high-resource language tokens have larger norms). It proposes the Language Confusion Gate (LCG), a lightweight two-layer MLP trained via norm-adjusted self-distillation to predict permissible language families (CJ, Latin, Symbols, Low-Res) at each decoding step, masking disallowed tokens only when confusion is likely. The method reduces cross-script confusion by roughly an order of magnitude across Qwen3, Llama3.1, Gemma3, and GPT-OSS models with minimal overhead (~0.4%) and a sparse intervention rate (0.33–0.38%).

## Strengths

- **Novel mechanistic insight that is directly operationalized.** Section 3.2's identification of token embedding norm imbalance (Table 1) as a source of language confusion is the paper's strongest intellectual contribution. The decomposition of logits into norm × cosine similarity (Eq. 1) is basic algebra, but connecting it to the overrepresentation of high-resource language tokens in the top-5% of norms and then using norm-adjusted self-distillation to train the gate creates a tight analysis-to-method pipeline.

- **Genuinely practical and lightweight intervention.** A two-layer MLP trained by self-distillation with a 0.38% intervention rate and 0.4% generation overhead (Section 6) is deployable. The paper correctly positions this as the primary advantage over retraining-based approaches.

- **Broad and systematic model coverage.** Evaluation across Qwen3-8B, Qwen3-30B, Llama3.1-8B, Gemma3-12B, and GPT-OSS, in both thinking and non-thinking modes (Tables 3, 4), gives reasonable confidence the method generalizes across architectures and sizes.

- **Sparse intervention is concretely documented.** The paper reports exact intervention counts (e.g., 523 out of 139,354 tokens for Qwen3-8B), providing concrete evidence for the paper's framing of language confusion as a rare, correctable event.

## Weaknesses

### Fatal

None.

### Major

- **Training/evaluation overlap on FLORES+ (the primary benchmark).** The gate is trained on a composite dataset that explicitly includes **FLORES+** (Section 5.1). The primary no-think evaluation uses **FLORES-NO-LATIN** (Section 5.2), which is a subset of FLORES+. This means the gate was trained on prompts drawn from the same source it is evaluated on. While the self-distillation training objective (predicting language families from hidden states) makes standard supervised overfitting less likely, the concern is real: the gate may have learned FLORES+-distribution-specific patterns rather than general language-family prediction. The INCLUDE benchmark results (Table 3) provide clean, uncontaminated evidence and are consistent with the FLORES-NO-LATIN results, which limits the damage. However, the paper does not acknowledge this overlap, and the most dramatic headline numbers (e.g., CJ confusion 1.0%→0.0% on Qwen3-30B, Section 1) come from the potentially affected benchmark. The authors should retrain the gate without FLORES+ data and re-report, or at minimum discuss the potential impact.

### Minor

- **Binary response-level confusion metric is coarser than necessary.** The confusion rate is defined as "the percentage of model responses that contain at least one character from an unintended language script" (Section 5.2). This is per-response binary: a response with a single stray CJ character is counted the same as one that is half CJ characters. The paper reports intervention rate at the token level (0.38%) but confusion only at the response level. Token-level confusion rates would be strictly more informative and would align the two metrics.

- **Code-switch evaluation has blind spots.** The first experiment (Section 5.3) tests whether LCG blocks known-correct code-switches selected by human judges (86.7% preservation), which directly addresses the main concern. However, it does not measure whether LCG *changes* the model's code-switching behavior in ways other than blocking — e.g., whether it causes the model to choose different code-switch points. The second experiment partially addresses this by showing aggregate code-switch rate changes, but the drops are substantial (e.g., Qwen3-8B from 46.34% to 25.90%, nearly halved). The paper's argument that this is acceptable because the rate remains above Claude Sonnet 4 (23.29%) is reasonable but the magnitude of change deserves fuller discussion.

- **No variance or statistical significance for confusion rates.** None of the tables include standard deviations, confidence intervals, or significance tests. Since many comparisons involve very small percentages (0.0%, 0.1%, 0.06%), it is impossible to assess whether reported differences are meaningful or simply reflect finite-sample variation. The paper reports aggregate token counts for intervention rate but not sample sizes for each evaluation condition in the confusion rate tables.

- **The dismissal of LCB is not quantified.** Section 5.2 gives two reasonable reasons for not using the Language Confusion Benchmark, but neither is quantified (e.g., "X% of LCB queries involve code-switching" or "the detector has Y% false positive rate"). This makes the justification feel hand-wavy rather than rigorous.

- **Intervention rule thresholds appear uncalibrated.** Rule 2's thresholds (top-k=5, p=0.999 and top-k=20, p=0.95) are presented without sensitivity analysis or justification (Section 4.3). The "No Rule" ablation in Figure 3 shows that LCG works without the rules, so this is not a fatal gap, but the specific choices warrant some explanation.

- **The core mechanistic analysis (Section 3.1) is single-model, single-dataset.** The finding that language-consistent tokens appear within top-3 at 99.29% of confusion points is based only on Qwen3-8B on FLORES-NO-LATIN. This empirical foundation for the entire method should be replicated across at least one more model.

- **Method addresses cross-script confusion only.** By grouping tokens into four script-based families, the gate cannot distinguish between languages sharing a script (e.g., English vs. Spanish or Arabic vs. Hindi). The paper acknowledges this in Section 6 but the framing ("Language Confusion Gate") is broader than what the method handles, and same-script confusion may be more practically important than the cross-script cases tested.

### Trivial

- GPT-5-Chat's BLEU score of 10.66 on FLORES-NO-LATIN (Table 2) is surprisingly low and unexplained — some context about the difficulty or size of this subset would help the reader calibrate.

## Nice-to-Haves

- Report precision/recall of the gate's language-family predictions directly, rather than inferring gate quality only from downstream confusion rates. This would let readers assess where the gate errs and how often Rule 2 overrides it.
- Sensitivity analysis for the top-k/top-p thresholds used in both training (self-distillation) and inference (Rule 2).
- Token-level confusion rates to complement the response-level metric, providing a finer-grained view of improvement magnitude.
- Evaluate the gate on Low-Res language family confusion (one of the four predicted families) rather than only CJ and Latin confusion, to demonstrate coverage of all output categories.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Claim about reasoning models reintroducing problem is unsupported"** — The paper cites Guo et al. (2025) and Wang et al. (2025) in support (Section 1). Removing as strawman (misreads supported claim as unsupported).
- **"ORPO training details missing"** — The appendix (stripped by the parser) may contain these details. Removing per rule about missing appendix content.
- **"Figure 3 labeling issues"** — Formatting nitpick about figure readability in text-only form. Removing as formatting artifact.
- **"Unclear if top-3 finding holds across models"** — This is a valid point but very minor; merged into the Minor weakness about single-model analysis rather than kept as separate criticism.
- **Criticisms about missing standard deviations on BLEU/accuracy** — Already covered by the broader point about missing variance reporting; merged.

## Novel Insights

None beyond the paper's own contributions. The reviews identify useful methodological critiques (training/evaluation overlap, metric granularity, missing statistical rigor) but surface no novel synthesis that the paper itself does not provide.

## Suggestions

- Retrain the gate excluding FLORES+ data from the training set and re-report the FLORES-NO-LATIN results. If the results hold, the data leakage concern is resolved. If they degrade, the gap should be honestly reported and analyzed. This is the single highest-impact improvement the paper could make.
- Add token-level confusion rates alongside the existing response-level metric.
- Report confidence intervals or at minimum sample sizes for each evaluation condition.
- Replicate the Section 3.1 confusion-point analysis on at least one additional model (e.g., Llama3.1-8B).
- Add justification or sensitivity analysis for the Rule 2 thresholds.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>