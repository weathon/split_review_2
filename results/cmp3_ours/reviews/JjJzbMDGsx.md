Now I have a thorough understanding of the calibration landscape. Let me write the final review.

## Summary

The paper introduces the Language Confusion Gate (LCG), a lightweight two-layer MLP that intercepts the base LLM's hidden state during decoding, predicts which of four language families (CJ, Latin, Symbols, Low-Res) are permissible at each step, and masks tokens from disallowed families. The gate is trained via norm-adjusted self-distillation — using the frozen LLM's own top-k/p predictions after debiasing by token embedding norms. Evaluated across Qwen3 (two sizes), Llama3.1-8B, Gemma3-12B, and GPT-OSS in both thinking and no-think modes, LCG reduces confusion rates substantially (e.g., Qwen3-8B Latin confusion from 12.1% to 2.0%) while adding only 0.4% latency overhead. The paper also evaluates impact on legitimate code-switching, finding that LCG largely preserves it.

## Strengths

1. **Well-motivated problem grounded in mechanistic analysis.** The paper identifies a genuine issue in multilingual LLMs (language confusion) and supports its solution with three concrete observations: confusion is rare at the token level, correct-language tokens are usually in the top-k/p candidates, and output token embedding norms are biased toward high-resource languages (Section 3.2, Table 1, Figure 2). The norm-bias analysis is particularly insightful and feels like a real find.

2. **Practical, deployment-ready design with measured overhead.** LCG intervenes on only ~0.33–0.38% of tokens (Section 5.3) and adds 0.4% latency overhead in a production benchmark with 8-sample concurrency (Section 6). These are measured, not just claimed — meaningful for practical adoption.

3. **Norm-adjusted self-distillation is well-motivated and cleanly ablated.** The comparison between LCG-adjusted and LCG-unadjusted (Table 3) directly demonstrates the value of the norm-adjustment component. For Llama3.1-8B, Latin confusion drops from 5.7% to 2.9% by adding norm adjustment.

4. **Explicitly evaluates code-switching preservation.** The paper does not only report confusion reduction — it checks whether legitimate code-switching is preserved (Table 5), including a human-validated analysis showing 86.7% token-level preservation at confusion points. This is the right thing to check and most prior work does not do it.

5. **Consistent results across model families and modes.** Results hold across Qwen3 (two sizes), Llama3.1, Gemma3, and GPT-OSS, spanning both thinking and no-think modes — making the findings more robust than a single-model evaluation.

## Weaknesses

### Fatal
None.

### Major

1. **No "persistence-only" baseline to isolate the learned gate's contribution.** The paper's Rule 3 ("always allow the previous token's language family") is a simple heuristic that, applied as a standalone rule (always allow the previous token's family + symbols + Low-Res, without the learned gate), could potentially capture most of the improvement without any learned component. The "No Rule" ablation (Figure 3) removes all three intervention rules simultaneously, so it does not isolate Rule 3 alone. Without a persistence-only baseline, we cannot tell whether the bulk of the gain comes from LCG or from this simple heuristic. The paper claims LCG as a learned solution, but a large fraction of the improvement might be attributable to the persistence rule alone. *Verifiable from Section 4.3 (Rule 3) and Figure 3 ("No Rule" removes all rules).*

2. **The gate's binary decision threshold for masking is unspecified.** The gate is trained with BCE loss on sigmoid outputs (Section 4.2), but the paper never states the threshold or decision rule used to convert the continuous per-family predictions (ℝ⁴) into the binary "allow/mask" action during inference. Section 4.1 states "mask tokens in banned language" without specifying how "banned" is determined from the gate's output. This is a reproducibility gap. *Verifiable from Section 4: lines 183, 205–206 describe training but no inference threshold.*

### Minor

3. **Token-level confusion metrics are not reported.** The confusion rate is defined as "the percentage of model responses that contain at least one character from an unintended language script" (Section 5.2) — a response-level metric that treats a single confused character the same as a mostly-confused response. When base rates are low (e.g., Qwen3-30B CJ% at 1.0% → 0.0%), the response-level framing is the only perspective available. Without token-level metrics or confidence intervals, it is unclear whether small reductions (e.g., 0.22% → 0.11% on INCLUDE) are meaningful. The main high-confusion results (Qwen3-8B: 12.1% → 2.0%) are clearly significant regardless, so this does not threaten the paper's core claims. *Verifiable from Section 5.2, line 229.*

4. **FLORES train/eval split not clarified.** The training data (Section 5.1) includes FLORES+ to generate translation pairs, and the evaluation datasets (FLORES-NO-LATIN, FLORES-WITH-LATIN) are derived from FLORES+. The paper does not state whether these sets are disjoint. Since the gate predicts language families (not memorizing translations), any contamination would affect results only indirectly, but the split should still be clarified. *Verifiable from lines 221 and 227.*

5. **Self-distillation pseudo-target accuracy not measured across models.** The key observation that "correct-language tokens appear within top-3 99.29% of the time" is from Qwen3-8B only (Section 3.1). The accuracy of the norm-adjusted top-k/p pseudo-targets — what fraction actually contain the correct language family — is never reported or broken down by model. The ablation shows norm-adjustment helps, but the potential upper bound on gate performance from pseudo-target errors is uncharacterized. *Verifiable from line 96 and Section 4.2.*

6. **Human annotation for code-switch validation lacks methodological detail.** The paper reports 86.7% token-level preservation based on "human annotators" (Section 5.3) but does not specify the number of annotators, number of examples annotated, or inter-annotator agreement. This is a key supporting result and its reliability is opaque. *Verifiable from line 284.*

### Trivial

7. No confidence intervals or variance estimates are reported for any confusion rates, many of which are small (0.0–5.0%) with finite samples where uncertainty is non-negligible.

## Nice-to-Haves

- Report token-level confusion metrics alongside response-level metrics for at least one representative condition (e.g., Qwen3-8B on FLORES-NO-LATIN) to validate that the response-level metric does not distort conclusions.
- Add confidence intervals or binomial confidence bounds for confusion rate estimates.
- Analyze failure modes: cases where LCG makes false positives (blocking legitimate tokens) or false negatives (allowing confused tokens), beyond aggregate rates.

## Removed Points

These points are flagged to be removed; treat them with caution.

None — all weaknesses from the harsh critic were verified against the paper and retained. Some were demoted in severity after verification:
- The response-level metric concern (originally "Evidential") was downgraded to **Minor** because the main high-confusion results are clearly meaningful at either level, and the core claims do not depend on small-magnitude differences.
- The FLORES train/eval overlap concern (originally "Evidential") was downgraded to **Minor** because the gate predicts language families (not translation outputs), making contamination indirect.
- The pseudo-target accuracy concern (originally "Evidential") was downgraded to **Minor** because the ablation already indirectly validates the component's value.
- The human annotation detail concern was moved from the body of the critic's review into a dedicated minor weakness.

## Novel Insights

The harsh critic's most valuable observation is the "persistence-only baseline" gap: the paper's evaluation conflates the learned gate with Rule 3, a simple heuristic that may do much of the work. This is a concrete experimental fix that would cleanly separate LCG's contribution from its scaffolding rules. The paper's other oversight — not specifying the gate's inference threshold — is a straightforward reproducibility fix. Together these point to an otherwise solid paper that would benefit from targeted tightening rather than a major rewrite.

## Suggestions

1. **Add a "persistence-only" baseline**: disable the learned gate entirely and apply only Rule 3 (always allow the previous token's language family + symbols + Low-Res). If this baseline already captures most of the gain, LCG is over-engineering; if it does not, it cleanly validates the learned component.
2. **Specify the gate's inference threshold**: state the threshold or decision rule used to convert sigmoid outputs to binary allow/mask decisions for each language family.
3. **Report token-level confusion rates** for at least the main results (Table 3) to validate that the response-level metric is not masking meaningful patterns.
4. **Clarify the FLORES train/eval split**: state explicitly whether the FLORES+ data used for training is disjoint from the evaluation subsets.
5. **Provide human annotation details**: annotator count, example count, and inter-annotator agreement for the code-switch validation.
6. **Report pseudo-target accuracy across models**: show what fraction of norm-adjusted top-k/p candidate sets contain the correct language family, to characterize the upper bound on gate performance.

## Score and Decision

**Calibration process**: I retrieved anchor papers from six score bands and read several in full.

**Round 1 (bracketing)** retrieved anchors across all bands:

| Band | Sample Anchor | Avg Score | Round | Comparison to LCG Paper |
|------|--------------|-----------|-------|------------------------|
| Strong reject (≤1.5) | "Advancing Cross-Lingual..." | 1.00 | 1 | Trivial or broken papers; LCG is far beyond this. |
| Weak reject (1.5–3.5) | "Llamas (mostly) think in English" | 3.00 | 1 | Single task, poor presentation, questionable methodology. LCG is clearly stronger. |
| Borderline reject (3.5–5.5) | "XTransplant" | 4.75 | 1 | Data contamination concerns, unfair upper-bound reporting. LCG has better eval hygiene. |
| Weak accept (5.5–7.5) | "Self-Detoxifiers (SASA)" | 6.00 | 1 | Similar lightweight decoding intervention with broader evaluation; LCG comparably strong. |
| Weak accept (5.5–7.5) | "The Same but Different" | 6.60 | 1 | Strong mechanistic analysis but limited to 2 languages. Different type of contribution. |
| Accept (7.5–8.5) | "Better Instruction-Following Through MBR" | 7.33 | 1 | Very clean evaluation, no major weaknesses. LCG has more gaps. |

**Round 2 (narrowing)** retrieved papers in the 5.5–7.5 range, confirming that 6.0–6.5 is the appropriate band. The paper's contributions (clear mechanistic grounding, practical latency measurement, explicit code-switching evaluation, multi-model breadth) put it above the 3.0–5.0 papers, but the missing persistence-only baseline and unspecified gate threshold prevent it from reaching the 7+ tier.

**Final score**: 6.5. The paper makes a genuine contribution with a practical, well-motivated method and solid evaluation across diverse models. The weaknesses are real but addressable — the most significant (persistence-only baseline, unspecified threshold) have clear fixes that would substantially strengthen the paper.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>