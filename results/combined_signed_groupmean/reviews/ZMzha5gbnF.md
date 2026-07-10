Based on the calibration analysis, I can now produce the final consolidated review.

**Calibration Summary:**
- Round 1 bracket: 6.0–8.0 (identified through comparison with Backtracking at 8.0, Catastrophic Jailbreak at 7.0, Q-Misalign at 6.0, and Safe RLHF at 7.5)
- Comparison with Backtracking (8.0): Reviewed paper has comparable strength impact (+9.86–+10.00 vs +6.69–+10.00) and substantially lower-magnitude weaknesses (max -0.11 vs -7.98). However, scope is narrower (MDLMs only vs all LLMs).
- Comparison with Catastrophic Jailbreak (7.0): Reviewed paper has stronger strengths and weaker weaknesses.
- Comparison with Q-Misalign (6.0): Reviewed paper is substantially stronger in all dimensions.
- Final placement: 7.5 — a clear accept with strong contributions, slightly below the broadest-impact top-tier papers due to MDLM-specific scope.

---

## Summary

This paper identifies the **priming vulnerability** in Masked Diffusion Language Models (MDLMs): affirmative tokens appearing at intermediate denoising steps can steer generation toward harmful responses even in safety-aligned models. The paper demonstrates this through both a controlled anchoring attack (Section 4.1) and a practical optimization-based attack, First-Step GCG (Section 4.2, Theorem 4.1). It then proposes **Recovery Alignment (RA)**, an RLHF-style method that trains models to generate safe responses from contaminated intermediate states. Experiments across three MDLMs show RA reduces ASR to near zero for most attacks with minimal capability degradation across 11 benchmarks.

## Strengths

- **Novel vulnerability finding with clean isolation.** The priming vulnerability is genuinely MDLM-specific and clearly distinguished from ARM prefilling attacks (Section 1, lines 15–33). The anchoring attack isolates the mechanism precisely: a single affirmative token at step 1 raises ASR from 2% to 21% on LLaDA Instruct (Figure 2). [impact: +10.00]

- **First-Step GCG is practically effective and well-motivated.** Table 1 shows 20× speedup and 3–4× ASR improvement over Monte Carlo GCG across all three models. Theorem 4.1 provides formal motivation, and the paper openly acknowledges the bound's looseness (line 136), letting the empirical results stand on their own. [impact: +10.00]

- **Recovery Alignment achieves strong and consistent results.** Across three models and multiple attacks (Anchoring, PAD, DiJA, First-Step GCG), RA consistently outperforms all baselines (SFT, DPO, MOSA). The RA w/o inter ablation is the critical control: at t_inter=4 on LLaDA Instruct, RA achieves 1.3% ASR vs RA w/o inter 22.0%, confirming that training on contaminated states — not more alignment data — is the active ingredient. [impact: +9.99]

- **Well-designed ablations.** The t_max sweep (Figure 3a) shows expected monotonic robustness improvement and honestly reports reward hacking at large t_max. The linear/uniform/constant scheduling comparison (Figure 3b) directly validates the curriculum design. [impact: +9.99]

- **Thorough capability evaluation.** 11 benchmarks (Table 4) with honest reporting of decreases (PIQA) and plausible explanations for improvements (TruthfulQA). Average degradation is negligible (+0.4 on LLaDA). [impact: +9.86]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Reward model is underspecified.** Section 6.1 states: "As the reward model, we directly employ DeBERTaV3 (He et al., 2021; Köpf et al., 2023) without additional fine-tuning." A vanilla DeBERTaV3 produces contextual embeddings, not scalar safety scores. The citation to Köpf et al. (2023, OpenAssistant) suggests a specific reward checkpoint, but the exact model ID and how scores are produced are not specified in the main text. Since the entire RA pipeline depends on this reward signal, this must be clarified for reproducibility. [impact: -0.11]

- **Abstract claim about conventional attacks is overstated.** The Abstract claims RA "improves robustness against conventional jailbreak attacks" without qualification. In Table 3, MMaDA's ReNeLLM ASR increases from 79.3% (Original) to 81.7% (RA). While RA does improve on PAIR and Crescendo, the ReNeLLM counterexample should be noted. [impact: -0.08]

- **Residual ASR against First-Step GCG after RA is not discussed.** After RA, First-Step GCG still achieves 11.3% ASR (LLaDA Instruct), 15.0% (LLaDA 1.5), and 45.7% (MMaDA) (Table 2, last column). Since the paper claims RA targets exactly the vulnerability that First-Step GCG exploits, the residual warrants analysis — e.g., whether the successful attacks use suffixes that bypass reward model detection. [impact: -0.00]

- **Training budget for baselines and statistical significance not reported.** The paper specifies RA uses 2,500 GRPO steps but does not report comparable budgets for SFT, DPO, and MOSA. Additionally, some comparisons have overlapping error bars (e.g., ReNeLLM on LLaDA: RA 72.3±8.0 vs RA w/o inter 75.7±3.8) that should be noted. [impact: -0.01]

### Trivial
None.

## Nice-to-Haves

- Provide qualitative traces of the denoising trajectory before and after RA to visually confirm the "recovery" mechanism.
- Analyze whether the reward model's scores correlate with human judgments of safety for MDLM-generated outputs specifically.
- Conduct an analysis of what PAIR/ReNeLLM outputs look like to explain why RA's effectiveness varies across attack types.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Section 3 integral notation (Eq. 1):** Integral-over-discrete is a standard convention in probability theory papers; this is a style nitpick.
- **Monotonicity assumption validation:** The paper states empirical validation in Appendix C.2 (line 130). The concern references a stripped appendix and cannot be evaluated from what is on the page.
- **Objective (7) notation garbled:** Parser artifact — the original submission does not have this issue.
- **PAD/DiJA description sparse:** Paper states details are in Appendix D.5, stripped by the parser.
- **Table 2 vs Table 3 consistency for MMaDA:** The paper provides a plausible mechanism (lines 243–244) and explicitly acknowledges RA "remains imperfect" (line 299). This is discussed.
- **Theorem 4.1 bound looseness framing:** The paper explicitly acknowledges the looseness (line 136) and presents the theorem as motivation, not a tight bound.
- **Section 7 Limitations clarity:** Presentation nuance about "data-construction cost" framing; does not affect validity.

## Novel Insights

The harsh critic insightfully isolates the RA w/o inter ablation as the key causal test: it directly separates the effect of training on contaminated intermediates from simply having more alignment training (GRPO vs SFT/DPO). The large gap (e.g., 1.3% vs 22.0% at t_inter=4 on LLaDA Instruct) cleanly confirms the paper's claimed mechanism. This causal decomposition is the paper's strongest structural feature and should be emphasized — it answers the most natural skeptical question before it is asked.

## Suggestions

1. Specify the exact reward model checkpoint (HuggingFace model ID), how it produces scalar safety scores, and whether any calibration was performed for MDLM outputs.
2. Qualify the Abstract claim about conventional attacks, noting the ReNeLLM case on MMaDA.
3. Add a paragraph analyzing the residual ASR against First-Step GCG after RA, with qualitative examples.
4. Report training steps/compute for all baselines, and note where ASR differences are not statistically significant.

## Score and Decision

**Score calibration:** Round 1 bracket was 6.0–8.0. The closest anchor is Backtracking (8.0), which has comparable strength impact (+6.69–+10.00) but a substantially more severe weakness profile (max -7.98 vs max -0.11). The reviewed paper's MDLM-specific scope is narrower, which prevents it from matching the broad-impact top tier (9+). Catastrophic Jailbreak (7.0) has weaker strengths and more severe weaknesses. Safe RLHF (7.5) is the natural comparison point. The paper sits between 7.0 and 8.0 — clearly above 7.0 due to cleaner execution, but below 8.0 due to narrower scope and the reward model reproducibility gap. Final score: **7.5**.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>