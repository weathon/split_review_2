## Summary

This paper introduces the Language Confusion Gate (LCG), a lightweight, plug-in decoding intervention that uses a small MLP to predict permissible language families (CJ, Latin, Symbols, Low-Res) and dynamically mask disallowed tokens during generation. The gate is trained via norm-adjusted self-distillation, using the model's own debiased logits as pseudo-targets to avoid any labeled data. Across 4 no-think and 3 thinking models, LCG reduces cross-script language confusion by roughly an order of magnitude (e.g., Qwen3-30B: CJ confusion 1.0%→0.0%, Latin confusion 4.4%→0.4%) with only 0.4% latency overhead, while maintaining task performance and largely preserving legitimate code-switching.

## Strengths

- **Clean mechanistic motivation.** Section 3.2 identifies output token embedding norm imbalance as a source of systematic bias toward high-resource languages, with a clear geometric decomposition of the logit (`logit = ‖h‖ · ‖e_i‖ · cos_sim(h, e_i)`). Table 1 shows that CJ tokens occupy 10.74% of top-5% norms in Qwen3-8B vs. 0.14% for Low-Res tokens — a directly actionable finding.

- **Norm-adjusted self-distillation is a clever, label-free training signal.** Section 4.2 uses the model's own norm-debiased logits to generate pseudo-targets for the gate. The ablation in Table 3 convincingly shows that norm adjustment matters: e.g., Llama3.1-8B Latin confusion drops from 5.7% (LCG-unadjusted) to 2.9% (LCG-adjusted).

- **Strong and consistent empirical results across diverse models and tasks.** Improvements hold across 4 no-think models (Qwen3, Llama3.1, Gemma3, GPT-OSS) on FLORES-NO-LATIN and the held-out INCLUDE benchmark, and across 3 thinking models on Humaneval-XL (Table 4) without degrading Pass@1.

- **Practical efficiency.** The ~0.4% latency increase (Section 6) and ~0.35% intervention rate (Section 5.3) are genuine practical advantages over retraining-based approaches.

- **Careful treatment of the code-switch problem.** The FLORES-WITH-LATIN / FLORES-NO-LATIN split and explicit evaluation of code-switch preservation (Table 5, the 86.7% human evaluation) directly address the core difficulty of distinguishing confusion from legitimate mixing.

## Weaknesses

### Fatal
None.

### Major

- **Training/evaluation data overlap on FLORES.** The gate is trained on a dataset that includes FLORES+ (Section 5.1), and the primary evaluation benchmark FLORES-NO-LATIN is a subset of FLORES+ (Section 5.2). While the gate is a small 4-class classifier unlikely to memorize answers, the FLORES+ translation task creates a predictable context that the gate could learn to exploit. This is substantially mitigated by two facts: (i) the INCLUDE benchmark (not in the training data) shows similarly strong gains, and (ii) thinking-model results on Humaneval-XL (also held out) are consistent. The authors should clarify whether any specific FLORES+ sentences appear in both training and evaluation, and ideally provide a version trained without any FLORES data.

- **Missing comparison to the most directly related methods.** The paper cites Nie et al. (2025) (neuron suppression for language switching) and Ji et al. (2025) (post-hoc token filtering for CJ intrusion) in the Related Work but does not include either as an experimental baseline. Given that these are the closest prior methods for decoding-time language confusion mitigation, their absence weakens the empirical positioning.

### Minor

- **Code-switch human evaluation is underspecified.** The 86.7% preservation rate (Section 5.3) rests on human annotations with no information about number of annotators, qualifications, or inter-annotator agreement. The Table 5 evidence (code-switch rates before/after intervention) is more robust and should be foregrounded; the human evaluation as reported is difficult to interpret.

- **Script-level granularity limits scope (acknowledged but under-emphasized).** The gate operates over 4 coarse families and cannot handle intra-script confusion (e.g., English vs. French, Mandarin vs. Japanese). The paper acknowledges this in Section 6, but the abstract's claim that "LCG decreases language confusion significantly" — without qualification — could mislead readers about the scope. The evaluation measures only cross-script confusion (CJ and Latin intrusion into non-matching scripts), which is exactly what the method targets.

- **No confidence intervals or significance tests.** Confusion rates are often small percentages (0.0–5%), and some reported improvements could be within noise (e.g., Gemma3-12B CJ from 0.2%→0.1%). Variance estimates would strengthen confidence in the claims.

- **Norm bias contribution is not quantified.** The paper states norm bias "can account for a subset of such errors but cannot fully explain language confusion" (Section 3.2) but does not estimate what fraction of observed confusion points are norm-driven versus caused by other factors. A simple analysis on a sample of confusion points would clarify the method's foundation.

- **No per-language breakdown.** Results aggregate across Arabic, Hebrew, Korean, Thai (FLORES) and Arabic, Hebrew, Greek, Russian, Vietnamese (INCLUDE). Some languages may benefit more than others, and this heterogeneity would inform understanding of the method's limitations.

- **Intervention rules not individually ablated.** The "No Rule" condition (Figure 3) removes all three rules together. Individual ablation of Rules 1–3 (Section 4.3) — especially Rule 3, persistence of the previous token's language — would show what the learned gate contributes versus the heuristic overrides.

### Trivial
None.

## Nice-to-Haves

- Analysis of how often Rule 2 (contradiction safeguard) triggers, to assess whether the gate's predictions are reliable or lean heavily on the override.
- Evaluation on an additional held-out benchmark that shares no data source with the training set, to further address the FLORES overlap concern.

## Removed Points

These points from the input review are flagged for removal (treated with caution):

- **"The claim that norm bias 'can account for a subset' is stated but not quantified"** — Kept in Minor (not removed).
- **"Section-by-Section Notes: No mention of how often Rule 2 triggers"** — Merged into Minor weaknesses (rule ablation point) rather than listed separately.
- **"No comparison with Nie et al. (2025) or Ji et al. (2025)"** — Kept in Major (not removed); this is a valid experimental gap, not a missing-related-work citation.
- **The reviewer's Strengths are all grounded in specific paper content; none removed.**
- **The reviewer's suggestion to "separate the FLORES+ evaluation from the FLORES+ training data"** — This is a suggestion, moved to Nice-to-Haves / Suggestions.

No points were removed for being factually wrong, formatting nitpicks, reproducibility nitpicks, or strawman misreadings.

## Novel Insights

The most notable observation to emerge from this review is the tension between the paper's two contributions: the norm-adjusted self-distillation training signal (Section 4.2) and the inference-time intervention rules (Section 4.3). Rule 3 (persistence of previous token's language) effectively reduces the gate to a one-shot decision per language switch — it fires once and then the previous token's language is locked in. The "No Rule" ablation shows LCG still works without rules but worse. A clean individual ablation would reveal whether the gate's learned predictions are genuinely useful or whether the rules are doing most of the work. This matters because if the rules are the primary driver, the self-distillation training may be less critical than the paper suggests. Conversely, if the gate alone (without Rule 3) makes sensible predictions, that is strong evidence for the self-distillation approach.

## Suggestions

1. Clarify and resolve the FLORES train/eval overlap — train a version without any FLORES data and report whether results hold.
2. Include Nie et al. (2025) or a comparable neuron-level intervention as a baseline.
3. Add bootstrap-based confidence intervals for confusion rates.
4. Ablate each intervention rule individually (especially Rule 3) to quantify the gate's independent contribution.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>