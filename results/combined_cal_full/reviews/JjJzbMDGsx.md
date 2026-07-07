Now I'll write the final consolidated review.

## Summary

This paper introduces the Language Confusion Gate (LCG), a lightweight plug-in decoding intervention for LLMs that dynamically masks tokens from disallowed language families to reduce language confusion (unintended language mixing) during text generation. LCG is a small two-layer MLP trained via norm-adjusted self-distillation: the frozen LLM's own norm-debiased logits provide pseudo-targets for which language families (CJ, Latin, Symbols, Low-Res) are permissible at each step. The method is motivated by three findings: language confusion is rare, correct-language tokens usually rank among top predictions, and output token embedding norms are biased toward high-resource languages. Evaluated across Qwen3, Llama3.1, Gemma3, and GPT-OSS on translation, knowledge/reasoning, and code generation tasks, LCG substantially reduces confusion rates (e.g., Qwen3-30B CJ confusion from 1.0% to 0.0%) with minimal overhead (0.4% latency increase).

## Strengths

- **Mechanistic insight into embedding norm bias (Section 3.2, Table 1, Figure 2):** The analysis showing that high-resource language tokens disproportionately dominate top embedding norms (e.g., CJ 10.74% vs. Low-Res 0.14% for Qwen3-8B) and that norm-adjustment surfaces correct-language tokens is genuinely informative and concretely demonstrates why norm imbalance causes language confusion. This is the strongest empirical foundation for the method.

- **Lightweight and practical intervention (Section 5.3, lines 265, 318):** The 0.33–0.38% intervention rate and 0.4% latency overhead, combined with the plug-in design (no base model modification) and compatibility with speculative decoding (Appendix F), make this a deployable solution compared to retraining-based approaches like ORPO.

- **Broad evaluation across model families and modalities (Tables 3, 4):** Testing on Qwen3 (multiple sizes), Llama3.1, Gemma3, and GPT-OSS across translation (FLORES), knowledge/reasoning (INCLUDE), and code generation (Humaneval-XL) in both standard and thinking modes provides reasonable evidence of generality beyond single-model or single-task evaluations common in prior work.

- **Thoughtful handling of the code-switching confound (Section 3.3, Table 5):** The paper explicitly acknowledges that hard language-consistency constraints would break legitimate multilingual behavior, and attempts to measure impact on code-switching rather than assuming it away. This framing is more responsible than typical work on language confusion.

## Weaknesses

### Fatal

None.

### Major

- **FLORES training-evaluation overlap (lines 221, 227, 231):** The LCG gate is trained on a composite dataset that includes the FLORES+ Dataset (used "to generate translation pairs for low-resource languages") and evaluated on FLORES-NO-LATIN, which is directly derived from the same FLORES+ benchmark. The paper does not acknowledge this overlap, discuss whether any FLORES-NO-LATIN items appear in the training data, or clarify what fraction of the 78k training samples comes from FLORES+. The headline results in Table 3 (e.g., CJ confusion from 1.0% to 0.0% on FLORES-NO-LATIN) may therefore be inflated. The INCLUDE results in the same table partially mitigate this concern since INCLUDE is a separate benchmark not used in training, but the overlap must be addressed explicitly.

### Minor

- **No variance reporting for main experiments (Table 3):** The paper reports confusion rates as low as 0.0%, 0.07%, and 0.11% but provides no standard deviations, confidence intervals, number of runs, or random seeds. Without this information, it is impossible to assess whether these low rates are stable or artifacts of a single stochastic draw. This is especially important for the headline 0.0% numbers and for the near-zero rates on INCLUDE.

- **Code-switch preservation analysis is under-specified (line 284):** The 86.7% token-level preservation figure relies on human annotation, but no details are given about the number of annotators, their qualifications, inter-annotator agreement, or how examples were selected for annotation. The claim that LCG "preserves" code-switching is further weakened by Table 5, which shows a 44% relative reduction in code-switch rate for Qwen3-8B (from 46.34% to 25.90%); the paper calls this "not much lower" than the ground-truth answer rate (38.36%), but a 12 percentage-point gap is meaningful and no utility metric or user study is provided to assess practical impact.

- **Pseudo-target quality is not characterized (Section 4.2):** The gate is trained on pseudo-targets derived from the frozen model's own norm-adjusted logits. The paper acknowledges that norm-adjustment "cannot fully explain language confusion" (line 155), yet does not analyze how often the pseudo-targets mislabel the permissible language family. Without analyzing pseudo-target accuracy (e.g., against ground-truth language labels on a held-out set), it is unclear whether the gate is learning a reliable signal or amplifying the model's own confusion patterns.

### Trivial

- **Slightly overstated abstract claim (line 9):** The abstract says LCG reduces confusion "often by an order of magnitude." While this holds for many model-task combinations (e.g., Qwen3-8B CJ: 4.5%→0.1%, a 45× reduction), it does not for others (e.g., Gemma3-12B CJ: 0.2%→0.1%, a 2× reduction). The qualifier "often" provides some cover, but the phrasing is imprecise.

## Nice-to-Haves

- Run the main FLORES experiments with at least 3 random seeds and report mean and standard deviation for confusion rates, especially for near-zero figures.
- Disentangle FLORES training and evaluation sets by reporting whether any FLORES-NO-LATIN items overlap with the 78k training samples, or run a held-out evaluation.
- Provide details on the human annotation study: number of annotators, qualifications, inter-annotator agreement, and example selection criteria.
- Analyze pseudo-target accuracy against ground-truth language labels on a small annotated set to characterize the quality of the self-distillation signal.
- Ablate the individual intervention rules (Section 4.3) to show which rule contributes most.

## Removed Points

- "The ORPO baseline comparison is asymmetric" — Removed. The asymmetry (ORPO retrains the model, LCG does not) is inherent to the methods being compared and the paper does not claim a controlled comparison; it shows that LCG achieves comparable or better results without retraining costs, which is a valid comparison framing.
- "The BLEU scores on FLORES-NO-LATIN are very low across the board" — Removed. This is an observation about the evaluation setup, not a flaw in the method. The BLEU scores are stable before and after intervention, so low absolute values do not undermine the paper's claims.
- "The ablation of 'No Rule' in Figure 3 cannot distinguish which rule contributes most" — Removed. Ablating the full rule set vs. no rules is a standard ablation strategy; disentangling individual rules is a refinement, not a gap.
- "Section-by-section notes" about abstract references, GPT-5 BLEU scores, and other observational comments — Removed. These are observations, not weaknesses.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observations largely echo the paper's own framing and do not surface any insight that the paper itself does not already articulate.

## Suggestions

1. Disentangle the FLORES training-evaluation setup: report whether any FLORES-NO-LATIN items overlap with the gate training data, or hold out a clean subset for evaluation.
2. Add variance reporting (standard deviation over multiple seeds) to all main confusion-rate tables.
3. Provide full details on the human annotation for the code-switch study.
4. Characterize pseudo-target quality by comparing against ground-truth language labels on a small annotated sample.

## Score and Decision

**Calibration Anchors:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Llamas (mostly) think in English | fSbPwHjdDG.md | 3.00 | R1 | Yes | This paper is substantially stronger — the anchor had severe presentation/experimental flaws (-9.77, -6.91) and limited scope (one task, one model). |
| The Rise and Down of Babel Tower | eznTVIM3bs.md | 5.25 | R1 | Yes | This paper is slightly stronger — comparable positive weights (+4.90 vs +4.86) but milder negatives (-3.30 vs -4.59). The anchor was limited to code LLMs with methodology concerns. |
| Crosslingual Capabilities & Knowledge Barriers | BCyAlMoyx5.md | 5.67 | R1 | Yes | This paper is clearly stronger — the anchor had severe originality (-8.25) and experimental (-10.69, -6.77) concerns that this paper does not share. |
| The Same but Different | NCrFA7dq8T.md | 6.60 | R1 | Yes | This paper is weaker — the anchor had much stronger positive weights (+5.82 to +7.09 vs +2.82 to +4.90) and milder negatives (-2.64 vs -3.30). |

**Bracket:** Round 1 placed the paper between 5.67 and 6.60, closer to the lower end of this range. The weighted-item comparison confirms this: this paper shares the strongest positive items (mechanistic insight, broad evaluation) with the 5.25–5.67 anchors but the code-switch underspecification (-3.30) and missing variance (-1.87) are heavier negatives than the 6.60 anchor's criticisms. The weakest negatives (+0.39 for FLORES overlap, +0.40 for pseudo-target quality) have near-zero weight, indicating the model sees them as addressable rather than damaging.

**Final Score:** 6.0 — The paper presents a novel, practical, and well-motivated method with broad evaluation. The core contribution is sound. However, the FLORES training-evaluation overlap, missing variance reporting, and under-specified code-switch analysis prevent full confidence in the results as presented. These are all fixable issues that do not invalidate the contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>