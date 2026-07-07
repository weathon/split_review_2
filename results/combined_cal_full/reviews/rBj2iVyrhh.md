Now I have a clear calibration picture. Let me write the final review.

## Final Review

## Summary

This paper proposes Classifier-Constrained Alternating Training (CCAT), a two-stage framework for multimodal learning that addresses modality imbalance. The key idea is that alternating training methods (like MLA) reduce encoder-level gradient interference but fail to prevent the classifier from developing structural bias toward the faster-converging modality. CCAT addresses this by: (1) pretraining a shared classifier with a regularization term that penalizes large disparities in modality contribution scores; (2) freezing this classifier during alternating training with modality-specific LoRA adapters; and (3) performing secondary gradient updates on samples where one modality's contribution falls below a threshold. The method achieves SOTA results on CREMA-D (+1.35% over LFM), Kinetic-Sound (+6.76% over LFM), and MVSA (+1.92% over MMPareto).

## Strengths

- **Clear diagnosis of a real limitation in alternating training (Section 1, Figure 1).** The paper correctly identifies that existing alternating training methods reduce encoder-level gradient interference but fail to address classifier-level bias — the classifier learns a structural preference for the faster-converging modality early on, and this persists. This is a legitimate gap that the paper isolates well.

- **Strong headline results on Kinetic-Sound (Table 1).** The +6.76% gain over LFM (79.29% vs 72.53%) is substantial, not incremental. Improvements on CREMA-D (+1.35% over LFM from 83.62% to 85.89%) and MVSA (+1.92% over MMPareto from 78.81% to 80.73%) are positive, though more modest.

- **Clean ablation structure (Table 2).** Each component (classifier freezing, alternating training, secondary updates, LoRA) is removed systematically, and each removal degrades performance, confirming that all four components contribute to the final result. The ablation shows internal consistency.

- **The high-level architecture is well-motivated by the diagnosed problem.** If classifier bias is the core issue, then: pretrain an unbiased classifier → freeze it → use LoRA to adapt it per modality → fix the most imbalanced samples. This sequence follows logically from the problem framing.

## Weaknesses

### Fatal
None.

### Major

- **Overclaimed theoretical contribution (Contribution i, Section 3.1).** The paper claims a "profound theoretical isomorphism" and "new theoretical framework" bridging class and modality imbalance, and states it "provides a proof of their underlying similar" (line 59). What is actually presented is a qualitative analogy: both class and modality imbalance involve gradient suppression of one group during early training. There are no shared equations connecting the two phenomena, no bounds, no reduction of one to the other, and no theoretically derived design principle that follows from the analogy. The gradient analysis (Eqs. 2-3) describes each phenomenon separately without formally connecting them. This level of analysis is a useful intuition, not a theoretical framework or isomorphism. The paper would be better served by honestly framing this as motivation/inspiration rather than a theoretical contribution.

- **The unimodal accuracy results create a tension with the "balanced representations" framing.** In every dataset, the dominant modality's unimodal accuracy improves more in absolute terms than the weaker modality, widening the gap (CREMA-D: 4.84→7.80; KS: 3.64→7.90; MVSA: 19.85→22.16). The paper partially addresses this (Section 4.2, point iii: "transcending relative performance differences"), arguing that it prioritizes "liberating weak modalities' representational potential" over closing the gap. However, the abstract and title still claim "mitigating modality imbalance" and "learning balanced, robust multimodal representations" without clarifying that "balance" refers to contribution scores (which do converge, Figure 1), not unimodal accuracy gaps. This disconnect between the paper's framing and its data needs to be resolved.

- **Missing comparison with a closely related baseline.** SMLV (Zhou et al., 2025b) is cited in the related work (line 51) and provides the MI-based contribution estimation formula (Eq. 5) used in this paper. Since SMLV also addresses sample-level modality imbalance and uses the same contribution estimation approach, its exclusion from the baseline comparison (Table 1) is a notable gap.

- **The secondary update mechanism is confounded with hard-sample mining (Algorithm 1, lines 10-15).** Samples with low contribution scores receive extra gradient updates, meaning some samples get more training iterations per epoch than others. The ablation shows this component helps (Table 2: 83.06 → 85.89 on CREMA-D), but any method that gives extra training iterations to difficult samples would likely improve accuracy regardless of modality considerations. A proper control would compare modality-aware selection vs. random selection of equal size from the same modality. Without this control, the claimed modality-balancing mechanism for the sample-level improvement cannot be isolated from the confound of additional training on hard-to-classify samples.

### Minor

- **The MI-based contribution estimator (Eq. 5) is referenced from Zhou et al. (2025b) but not independently validated within this paper.** The regularization (Eq. 7) penalizes disparities in this specific quantity, and the secondary update selection mechanism depends on it. The paper does not examine whether this MI estimate correlates with genuine modality importance (e.g., by verifying with controlled degradation of one modality or showing the relationship between contribution scores and accuracy).

- **No standard deviations or error bars in the main results (Table 1, Table 2).** The paper reports "average test accuracy of three random seeds" but with no variance. Without this information, it is difficult to assess whether the improvements (especially the modest +1.35% on CREMA-D and the component-wise degradations in the ablation) are statistically significant.

### Trivial
None.

## Nice-to-Haves

- The paper could directly report contribution scores (c₁, c₂) on the evaluation datasets (not just the synthetic Figure 1) to ground the modality balancing claim.
- A controlled experiment testing CCAT's robustness when the weaker modality is intentionally degraded would strengthen the claim of modality rebalancing.
- Reporting wall-clock time or parameter counts would help practitioners assess the computational overhead of the secondary update mechanism.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"The gradient derivation for class imbalance (Eq. 2) assumes the conclusion."** Removed: The reviewer claims that assuming ŷⱼ ≈ 0 for minority classes is circular. However, this is a standard characterization of class imbalance dynamics — when minority class samples are scarce, the model's predictions are indeed near zero for those classes. This is a known phenomenon, not an assumed conclusion.

- **"The paper does not quantify distribution mismatch" between classifier pretraining and alternating training.** Removed: The paper identifies a conceptual challenge and addresses it via LoRA; quantifying the mismatch precisely is a nice-to-have, not a requirement.

- **Criticisms about the bidirectional cross-attention being "described by reference to the appendix."** Removed per instruction: appendix content is stripped by the parser from all papers; it exists in the original submission.

- **"Code release," "computational cost," "energy/efficiency."** Removed per reproducibility nitpick rules. These are standard omissions for method papers unless efficiency is a claimed contribution.

- **Criticism about "Figure 2 is described by reference to appendix."** Removed: parser artifact.

## Novel Insights

The most salient insight that emerges from cross-referencing the reviews is that the paper uses two different notions of "balance" — contribution scores (which converge toward 0.65/0.35, showing balancing) and unimodal accuracy (where the gap widens, showing the opposite). The paper is aware of this distinction (Section 4.2, point iii) and explicitly argues against equating "reduced unimodal gaps" with "balance," but the abstract and title do not reflect this nuance. This disconnect is the core tension that the paper does not adequately resolve. Beyond this, the reviews do not surface novel insights beyond the paper's own contributions.

## Suggestions

1. **Tone down the theoretical claims.** Reframe Section 3.1 as an "intuition" or "qualitative analogy" rather than a "profound theoretical isomorphism" or "proof." Drop the "theoretical framework" language for Contribution (i) unless a genuine formal connection is developed.

2. **Clarify what "balanced" means.** Either (a) explicitly state that CCAT balances contribution scores, not unimodal accuracies, and explain why this distinction matters, or (b) provide evidence that the widened accuracy gap is consistent with genuine modality rebalancing (e.g., by showing that contribution score balance correlates with better multimodal fusion).

3. **Control for the hard-sample mining confound.** Add an experiment comparing modality-aware selection (low cᵢᵐ) against random selection of equal size from the same modality for the secondary updates.

4. **Add SMLV as a baseline.** Since SMLV uses the same contribution estimator and targets sample-level imbalance, it is the most directly comparable prior work.

5. **Report standard deviations** in all result tables.

6. **Validate the MI contribution estimator** by showing its correlation with ground-truth modality importance (e.g., via controlled modality degradation experiments).

## Score and Decision

**Calibration summary:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| A Theory of Unimodal Bias | ul1cjLB98Y.md | 5.25 | 1,2 | Yes | Similar level — both have strengths and significant weaknesses. That paper had stronger theoretical framing but weaker experimental validation. |
| Towards Holistic Multimodal Interaction | BZWssJoYEv.md | 5.50 | 1,2 | Yes | Similar level — theoretical overclaim and limited baselines. CCAT has stronger accuracy gains. |
| Test-time Adaptation (Reliability Bias) | TPZRq4FALB.md | 8.00 | 1 | Yes | Much stronger — no major weaknesses, extensive benchmarks, well-supported claims. |
| Gramian Multimodal Repr Learning | ftGnpZrW7P.md | 7.00 | 1 | Yes | Stronger — cleaner theoretical framing, more thorough evaluation. |
| One Modality Synergize Training | 5BXWhVbHAK.md | 6.33 | 2 | Yes | Stronger — has rigorous theoretical proofs and broader modality validation. CCAT's theory is weaker. |
| Improving Multi-modal LLM (Arcana) | 0yTf37PXcH.md | 5.40 | 2 | Yes | Similar level — both have novel components but some overclaim. |
| Robust Multimodal Learning w/ Missing Modalities | XTwwtlEfTF.md | 4.50 | 2 | Yes | Weaker — lower novelty, missing comparisons. CCAT has stronger empirical contributions. |

Round-1 bracket: 4.0–6.0. The paper's weighted items show clean empirical contributions (ablation +4.70, results +4.01) weighed against heavy theoretical overclaim (−6.50) and several moderate weaknesses (−2 to −3 range). The final score of 5.0 places this paper between the rejected anchors at ~5.25–5.50 and above clearly weaker papers at ~4.50. The primary factors keeping it from 6+ are: the oversold theoretical framing (the heaviest negative weight at −6.50, roughly double any other weakness), the missing baseline comparison with SMLV (−2.09), and the unresolved framing tension between "balance" as contribution scores vs. unimodal accuracy (−2.91). These are correctable weaknesses, but in their current form they prevent the paper from meeting the bar for acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>