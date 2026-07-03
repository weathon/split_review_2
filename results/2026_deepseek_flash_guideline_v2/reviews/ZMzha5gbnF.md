The calibration tool is unavailable due to an infrastructure issue. I'll proceed with my best judgment based on the paper content and the established ICLR scoring guidelines.

Let me now produce the final consolidated review.

## Summary

This paper identifies, characterizes, and mitigates the "priming vulnerability" in Masked Diffusion Language Models (MDLMs): if an affirmative token endorsing a harmful query appears at an intermediate denoising step, subsequent generation is steered toward harm even in safety-aligned models, because standard alignment trains only from fully masked initial states. The paper contributes **(1)** a controlled characterization via the anchoring attack, **(2)** First-Step GCG, an optimization-based attack exploiting a theoretical lower bound (Theorem 4.1) that achieves ~20× speedup and up to 4× higher ASR over Monte Carlo GCG, and **(3)** Recovery Alignment (RA), a defense that trains models via RLHF to generate safe responses from contaminated intermediate states. RA reduces ASR from 44.0% to 1.3% at t_inter=4 on LLaDA Instruct, preserves general capability across 11 benchmarks, and generalizes to conventional jailbreak attacks (PAIR, ReNeLLM, Crescendo).

## Strengths

1. **First-Step GCG provides a tractable, theoretically grounded attack with strong empirical results.** Theorem 4.1 derives a lower bound relating the full-denoising log-likelihood to the first-step mask-predictor log-likelihood, making GCG differentiable and avoiding high-variance Monte Carlo estimation. Table 1 shows ~20× speedup and up to 4× ASR improvement (20% → 58% on LLaDA Instruct). This is a non-trivial contribution because the iterative stochastic re-masking in MDLMs otherwise makes gradients intractable.

2. **RA achieves dramatic ASR reductions with strong mechanistic evidence from the ablation.** Table 2 shows RA brings ASR from 44.0% to 1.3% at t_inter=4 and from 68.7% to 3.0% at t_inter=8 on LLaDA Instruct, dramatically outperforming SFT, DPO, MOSA, and the RA w/o inter ablation. Critically, RA w/o inter (trained without contaminated intermediate states) still shows >20% ASR at t_inter=4, confirming that conditioning on contaminated intermediate states — not just the RLHF objective — is the essential mechanism. This ablation cleanly isolates the paper's core design insight.

3. **General capability is preserved across 11 diverse benchmarks with negligible average change.** Table 4 reports results on ARC-C, CEval, CMMLU, GPQA, HellaSwag, HumanEval, MBPP, MMLU, PIQA, TruthfulQA, and Winogrande. Average accuracy for LLaDA stays at 52.2% (original) vs. 52.6% (RA), and for LLaDA 1.5 at 52.7% vs. 52.8%. This addresses a common concern with safety alignment methods — capability degradation — and is one of the paper's strongest pieces of evidence for practical viability.

4. **The anchoring attack provides a systematic, controlled characterization beyond heuristic concurrent work.** Section 4.1 varies the intervention step t_inter and measures ASR at each step, revealing a clean monotonic trend. This contrasts with the heuristic approaches in concurrent work (PAD, DiJA) which the paper discusses in Section 2.2, and enables precise quantitative measurement rather than binary vulnerability assessment.

5. **Ablation studies quantitatively validate the method's design choices.** Figure 3b shows linear scheduling of t_inter consistently outperforms uniform and constant scheduling across all three models, with constant scheduling failing entirely (remaining at ~80–90% ASR). Figure 3a shows the impact of varying t_max on robustness. These ablations provide concrete evidence supporting the design rationale rather than merely claiming the method works.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Numerical inconsistency in a headline result.** In Section 4.1 (and the Introduction), the paper states: "For example, ASR increases from 2% to 21% with LLaDA Instruct" under the anchoring attack at intervention step 1. However, the data table in Figure 2 shows LLaDA Instruct ASR at step 1/128 as **40%**, not 21%. The "2%" comes from Table 1's "No Attack" baseline (a different condition), while the anchoring attack at step 0 in Figure 2 shows 0%. The correct anchoring-attack ASR at step 1 for LLaDA Instruct is 40% per the paper's own table. This inconsistency — while the correct value (40%) actually *strengthens* the paper's argument — undermines trust in the reported numbers and must be corrected. The authors should verify which number is correct and update the text or table accordingly.

2. **Partial circularity between RA's training procedure and the anchoring attack evaluation.** RA is trained by contaminating intermediate states with a harmful response at step t_inter and optimizing the model to recover safe responses from those states. The anchoring attack — the primary attack used to evaluate RA in Table 2 — operates by the same mechanism: injecting the same harmful response at the same t_inter and measuring whether the model continues toward harm. That RA achieves 0.0% ASR on anchoring at low t_inter values is therefore partly expected, as the model is tested on the distribution it was trained on. This concern is *partially* mitigated by (a) RA's generalization to different intervention attacks (PAD, DiJA) and to non-intervention attacks (PAIR, First-Step GCG), and (b) the ablation RA w/o inter confirms that training from contaminated states is necessary. However, the paper does not explicitly acknowledge this circularity or delineate which results reflect genuine generalization vs. training-test overlap. Adding this discussion would strengthen the paper's case.

### Trivial

- **Theorem 4.1's bound is acknowledged to be loose but not empirically characterized.** The lower bound contains a 1/T factor (1/128 in experiments), meaning the first-step log-likelihood must be scaled by 128 before it relates to true generation probability. The paper acknowledges this looseness and relies on the empirical observation that the attack still works. An empirical characterization of how tight the bound is across queries (e.g., measuring log p(r_T=r) / (1/T) log π_θ(r̃_1=r) for a sample) would strengthen the theoretical narrative, though the strong attack results already validate the practical utility.

## Nice-to-Haves

- Evaluate RA against intervention attacks where the injected tokens are not harmful target responses but other steering tokens (e.g., generic affirmative tokens) to more directly test generalization of the recovery capability beyond the training distribution.
- Report RA's ASR broken down by whether harmful responses in the evaluation set were seen during training (BeaverTails) vs. unseen, to clarify whether the defense memorizes specific query–response pairs or learns a general recovery policy.
- Consider adding a brief limitations paragraph explicitly acknowledging that RA's anchoring-attack results reflect partly the training-test distribution overlap, and that the stronger evidence for generalization comes from the non-intervention and different-intervention attack results.

## Removed Points

These points were flagged by the reviewers but removed from the main weaknesses after verification against the paper:

- **"MMaDA MixCoT is unaligned, conflating alignment and robustness"**: The paper is transparent about this — MMaDA is explicitly labeled "(unaligned)" in Figure 2 and Table 1. Results are reported per-model, allowing readers to distinguish alignment from robustness. This is a correct observation about the paper's scope but not a weakness, as the paper does not misrepresent the MMaDA results.
- **"LLaMA/LLaDA naming inconsistency in Tables 2 and 3"**: The row labels in the tables read "LLaMA" while the rest of the paper uses "LLaDA". This is consistent with a PDF parser misreading the character "D" (the model is LLaDA, as cited in the references). Removed per the formatting-artifact rule.
- **"Missing discussion about t_min/t_max default values"**: The paper states these details are in Appendix D, which is stripped by the parser. Not a weakness in the submission.
- **"Theorem 4.1 is too loose to support the attack method"**: This mischaracterizes the paper's treatment — the paper explicitly acknowledges the looseness and argues that the priming vulnerability "helps compensate" (Section 4.2), with strong empirical validation. The bound is presented as a pragmatic surrogate, not a tight theoretical guarantee.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface any perspective on the work that goes beyond what the paper itself articulates.

## Suggestions

1. **Correct the numerical inconsistency**: In Section 4.1 (and the Introduction), verify whether the anchoring-attack ASR for LLaDA Instruct at t_inter=1 is 21% or 40%. If Figure 2's table is correct (40%), update the text. If the text is correct (21%), update the figure/table.
2. **Add an explicit paragraph on the RA–anchoring circularity**: In Section 5 or 6.2, briefly note that RA is trained on the same intervention mechanism that the anchoring attack uses, and clarify that the generalization evidence (PAD, DiJA, PAIR, First-Step GCG, the RA w/o inter ablation) is what most convincingly supports the claim of learning a general recovery capability.
3. **Consider a brief empirical characterization of Theorem 4.1's bound** as a supplement (e.g., in Appendix C), showing the ratio of the two quantities across a sample of queries.

## Score and Decision

Based on the paper content and the severity of identified weaknesses:

- The core contribution is clear and well-motivated: identifying a genuinely MDLM-specific vulnerability that does not transfer from ARM findings.
- The empirical evaluation is comprehensive: 3 MDLMs, 2 datasets, 3 evaluators, multiple attack types, ablations, and 11 general-capability benchmarks.
- The single verified concrete error (21% vs. 40%) is minor — it actually understates the vulnerability and does not weaken any claim.
- The circularity concern is partially mitigated by existing evidence and would be fully addressed with an explicit discussion.
- No fatal or major weaknesses threaten the paper's core claims.

This is a strong paper. It contributes a new vulnerability analysis, a theoretically grounded attack, a practical defense, and thorough empirical validation. The issues are minor and addressable.

**Score: 7.5**

**Decision: Accept**

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>