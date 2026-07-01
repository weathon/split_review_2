Now I'll write the final review.

## Summary

This paper integrates n-gram induction heads (from Akyürek et al. 2024) into the Algorithm Distillation (AD) framework for in-context reinforcement learning. The approach replaces a standard attention layer with an n-gram attention pattern that directly computes token co-occurrence statistics, providing an inductive bias for pattern matching. The authors claim three benefits: reduced data requirements for ICRL generalization, reduced hyperparameter sensitivity, and applicability to visual observation spaces via vector quantization. Experiments on grid-world (Dark Room, Key-to-Door) and pixel-based (Miniworld) environments show that the n-gram augmented model matches or outperforms standard AD, particularly in low-data regimes.

## Strengths

1. **Well-grounded motivation in ICL theory.** The paper correctly identifies that induction heads are central to in-context learning (Olsson et al. 2022) and that transformers exhibit a simplicity bias that can delay or prevent the emergence of higher-order induction heads (Edelman et al. 2024). Hardcoding this inductive bias via n-gram attention is a plausible architectural intervention, and the connection between n-gram patterns and the ICRL setting is clearly argued in Sections 2.2 and 2.3.

2. **Thoughtful evaluation protocol using Expected Maximum Performance (EMP).** By aggregating over random hyperparameter searches rather than cherry-picking the best run, the paper avoids a common form of overclaiming. The decision to fix batch size and limit gradient steps (Section 3.2) so that both methods process equal data per run is a reasonable control for fair comparison.

3. **Useful "no harm" sanity check (Section 4.5).** Showing that a permuted n-gram mask does not degrade performance below the baseline (Table 1(c): 0.51±0.03 vs 0.52±0.02) addresses the natural concern that the extra architectural machinery might hurt the model, and provides evidence that the n-gram layer can be safely added.

4. **VQ-based extension to pixel observations is creative.** Using a 4×4 matrix of VQ indices and requiring exact matches across all 16 indices is a reasonable discretization strategy for enabling n-gram matching in continuous visual spaces where exact pixel matching would fail.

## Weaknesses

### Fatal
None.

### Major

1. **VQ confound in pixel-domain experiments undermines the visual-domain claim.** In the Miniworld experiments (Section 4.3, Figures 5 and 6), the n-gram method uses a pretrained VQ encoder to discretize images before n-gram matching, while the baseline AD does not use VQ. The paper provides no control experiment where the baseline AD uses VQ encoding *without* n-gram heads. This means any performance gap could come from (a) the n-gram attention pattern, (b) the VQ encoding itself providing more useful input representations, or (c) the combination. This confound directly affects the paper's third claimed contribution — that n-gram heads "can be used in environments with visual observations" — because the experiment does not isolate the n-gram mechanism from the VQ preprocessing. An ablation with VQ + standard attention (no n-gram heads) is needed to support this claim.

2. **The headline 27× data efficiency claim is not adequately supported, and the comparison is confounded.** The claim (line 45: "reduce the total number of transitions in training data by a maximum of 27x") is stated three times in the paper (abstract, contributions list, Figure 4 caption, Section 4.2), with the computation deferred to Appendix B (stripped). More importantly, the experiment in Figure 4 fixes the number of goals (100) *and* the number of histories (500–1000) simultaneously, so the baseline's failure could be due to low total data volume rather than specifically low task diversity. The paper never tests whether the baseline AD would also work with 100 goals if given proportionally more histories per goal (e.g., 100 goals × 20 histories each = 2000 total histories). Without this control, the claim that n-gram heads specifically improve data efficiency (rather than the method simply benefiting from a different task-to-history ratio) is unsubstantiated.

### Minor

1. **Discrepancy between Table 1 and Figure 5 EMP values for Miniworld-Dark is unexplained.** Table 1(a,b) reports N-Gram EMP values of 0.67–0.76 for Miniworld-Dark, while Figure 5 (left) shows NGH reaching ~0.96 in the same environment. The paper does not specify the data regime (number of goals, number of histories) used in the Table 1 experiments. The baseline values are roughly consistent (0.51–0.52 in Table 1(c) vs. low EMP in Figure 5), but the large gap in n-gram method values across these two experiments needs clarification. If different data configurations were used, this should be explicitly stated.

2. **Model capacity is not controlled across architectural variants.** While the n-gram layer is described as a "drop-in replacement for the multi-head attention mechanism" (line 39) — meaning it replaces rather than adds to a standard layer — the n-gram attention mechanism uses a different parameterization (W₁, W₂ projections plus MLP) than standard MHA. An ablation comparing (a) baseline AD, (b) AD with n-gram layer, and (c) AD with a controlled architectural change of matched parameter count (e.g., different attention head configuration) would strengthen the attribution of benefits to the n-gram inductive bias specifically, rather than to any architectural modification.

3. **Figure 2 labels used before matching methods are defined.** Figure 2 (line 65) uses labels "states" and "[s,a,r]" for the two n-gram matching variants, but the distinction between state-matching and full-transition-matching is only explained in Section 2.3 (line 95), which appears *after* the figure. A brief forward-reference in the Figure 2 caption would help readers.

4. **Several figures lack confidence intervals.** Figure 6 includes shaded regions representing confidence intervals, but Figures 2, 4, and 5 show point estimates without any indication of variance. Given the known instability of ICRL training, reporting variance or multiple independent runs for all figures would improve interpretability.

### Trivial
None.

## Nice-to-Haves

- **Test the "transient ICL" motivation directly.** The paper motivates n-gram heads by arguing they address the transient nature of ICL ability (Singh et al. 2024), but no experiment measures whether the n-gram model maintains ICL behavior longer during training or avoids the "in-weights regime" transition. This would be a natural way to connect motivation to evidence.
- **Clarify the 27× computation directly in the main text** rather than deferring to an appendix, given that it is a headline claim.
- **Report EMP curves with confidence intervals or multiple seeds** for all figures.

## Removed Points

These points from the input review were removed with justification:

1. **"Appendix B is stripped so I cannot verify [the 27× claim]"** — Removed per instructions: the parser strips appendices from all papers; they exist in the original submission. The substantive concern about the confounded comparison is retained as Major weakness 2.

2. **"The n-gram model has strictly more parameters than the baseline"** — The paper states the n-gram layer is a "drop-in replacement for the multi-head attention mechanism" (line 39), meaning it replaces a standard layer rather than adding to the total parameter count. The retained Minor weakness 2 captures the residual concern about architectural control without the "strictly more parameters" framing.

3. **"Abstract framing is slightly imprecise"** — The framing of ICL for language vs. ICRL is a minor imprecision that does not affect the paper's technical contributions.

4. **"Off-by-one indexing in the n-gram formula"** — The reviewer acknowledged this is "not a flaw." The indices correctly match the inductive head pattern from the cited prior work.

5. **"Reliance on Q-learning oracle is a limitation"** — This is a known limitation of AD inherited by this paper, not introduced by it. The paper acknowledges it in passing (line 217 in Related Work).

6. **"The 'transient ICL' motivation is never directly tested"** — Moved to Nice-to-Haves. The paper's main claims are about data efficiency and hyperparameter sensitivity, not about explaining the mechanism of transient ICL.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a VQ-only control baseline for pixel experiments.** Train the baseline AD with the same VQ encoder (providing latent vectors as input) but without n-gram attention. This would isolate whether the improvement in Miniworld comes from VQ preprocessing, n-gram attention, or their combination.

2. **Run the baseline AD with 100 goals and varying numbers of histories (e.g., 1000, 2000, 4000) in Key-to-Door.** If AD still fails with more histories per goal, the "low task diversity" explanation is supported. If AD succeeds with enough histories, the 27× claim needs revision.

3. **Clarify the data configuration for Table 1.** State the number of goals and histories used in the n-gram length and position ablations to explain the gap between EMP values in Table 1 and Figure 5.

**Calibration Report**

Round-1 bracket: 4.0 – 6.0

Anchor papers retrieved and compared:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `Uj0h13lVrR.md` (GFlowNets) | 1.00 | 1 | Unrelated topic, much weaker paper |
| `5kMwiMnUip.md` (LLM jailbreak) | 1.40 | 1 | Unrelated topic |
| `Y8DClN5ODu.md` (Demonstration Distillation) | 3.40 | 1 | ICL paper but in NLP, not RL |
| `b5MCteb3w7.md` (Actions Speak Louder) | 4.75 | 1 | Directly comparable ICRL paper with similar weaknesses (experimental confounds). Our paper has a stronger architectural contribution but also has confounds. |
| `YW79lAHBUF.md` (LLMs Are ICRL) | 3.75 | 1 | Similar ICRL topic, weaker method, lower score |
| `uIKZSStON3.md` (In-context Exploration-Exploitation) | 7.25 | 1 | Cleaner ICRL paper with well-controlled experiments. Our paper has weaker experimental controls. |
| `Pj06mxCXPl.md` (Transformers Learn TD) | 6.67 | 1 | Strong theoretical ICRL paper. Our paper is more applied with weaker controls. |
| `EytBpUGB1Z.md` (Retrieval Head) | 8.00 | 1 | Strong mechanistic analysis paper, not directly comparable |
| `5iWim8KqBR.md` (Memory-Efficient AD) | 5.50 | 2 | Most directly comparable — improves AD for ICRL. Rejected due to limited novelty. Our paper has stronger novelty but weaker experimental evidence. |
| `PIHPmNNp7w.md` (Retrieval-Augmented DT) | 4.67 | 2 | Another AD variant. Got mixed reviews. |
| `aN4Jf6Cx69.md` (Mechanistic basis of ICL) | 4.50 | 2 | ICL mechanism paper, split reviews (1,1,8,8) |
| `iLUcsecZJp.md` (ICL vs Meta-Learners) | 5.75 | 2 | ICL analysis paper, broader scope |

**Narrowing to final score:** The most comparable papers are "Memory-Efficient AD" (5.50, Reject) and "Actions Speak Louder" (4.75, Reject). Both were rejected despite addressing important ICRL problems — one due to limited novelty, the other due to experimental confounds. Our paper has a more novel contribution (first application of n-gram induction heads to ICRL) but shares the problem of confounded experimental evidence. The VQ confound (Major weakness 1) and the unsupported 27× claim (Major weakness 2) are significant enough that the paper does not meet the bar for acceptance, but the core idea and discrete-environment results keep it above the strong-reject range. Final score: 4.5.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>