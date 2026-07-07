## Summary

This paper proposes integrating n-gram induction heads (borrowed from language modeling) into transformers for in-context reinforcement learning (ICRL). The approach hard-codes n-gram attention patterns into the architecture rather than relying on them to emerge during training, aiming to improve data efficiency and reduce hyperparameter sensitivity. Experiments on Dark Room, Key-to-Door (both discrete), and Miniworld (pixel-based) environments show consistent improvements over an Algorithm Distillation baseline.

## Strengths

- **Novel application of n-gram induction heads to ICRL.** The paper is the first to apply this architectural component from the language modeling literature (Akyürek et al.) in a decision-making setting (Section 2.2). The idea is sensible and non-obvious a priori.

- **Consistent positive signal across diverse environments.** The method outperforms its baseline on Dark Room (discrete MDP), Key-to-Door (discrete POMDP), and Miniworld (pixel-based), covering a reasonable diversity of observation types and task structures (Figures 2, 4, 5). The directional improvement is not an artifact of a single setting.

- **Clean diagnostic in the permuted-mask ablation.** Shuffling the n-gram attention matrix to simulate a broken layer and showing no degradation relative to the baseline (Table 1c, Section 4.5) provides reassurance that the layer does not introduce downside risk when matching fails.

- **Extension to pixel-based observations.** Using Vector Quantization to enable n-gram matching on images (Section 2.3) broadens the method's applicability beyond discrete observations, which is a nontrivial technical challenge.

## Weaknesses

### Fatal
None.

### Major

- **The headline 27× data-efficiency claim is based on an uncontrolled cross-paper comparison.** The paper states that its method (100 goals, Key-to-Door, Figure 4) matches AD's published performance and therefore needs "27× less data" compared to Laskin et al. (2048 goals). However, the paper never verifies that its own baseline implementation, when given 2048 goals, replicates AD's published performance. The controlled comparison (N-Gram vs. baseline at 100 goals, Figure 4) shows a real but unquantified advantage — baseline plateaus at ~1.3, N-Gram at ~1.9. But the 27× figure is drawn from an external published result, not a within-experiment measurement. This is the paper's most prominent quantitative claim (listed first in the bulleted contributions on page 1, line 45) and it is not supported by the evidence presented. *(Evidence: lines 45–46, 129, 179.)*

- **The ablation experiments (Table 1) report EMP values that are substantially lower than the main results, with no explanation.** The n-gram length and position ablations give EMP values of 0.67–0.76, and the permuted-mask ablation gives 0.51–0.52. These are far below the ~0.96 EMP reported for N-Gram on Miniworld-Dark in Figure 5. The paper never clarifies whether different experimental conditions (number of goals, histories) were used in the ablations. If the conditions are the same, the n-gram layer produces far lower performance than the main results claim; if different, the conditions are not stated. Either way, the ablations are difficult to interpret as presented. *(Evidence: Table 1, Figure 5, lines 200–213.)*

### Minor

- **No mechanistic analysis of what the n-gram layer actually learns.** In Key-to-Door, where the agent must remember whether it picked up the key, it is unclear why n-gram state-matching helps — the critical information concerns past actions, not state visitation patterns. The paper provides no attention visualizations, match-rate statistics, or probing diagnostics. This gap makes it harder to assess whether the improvements stem from the n-gram mechanism or from some confound (e.g., extra parameters, different gradient flow).

- **No single-run results at a well-tuned hyperparameter configuration.** All results are presented through EMP over random hyperparameter search. This prevents assessing the actual final performance of the best model each method can produce and makes it impossible to compare N-Gram and baseline at their respective optima.

- **The VQ-based n-gram matching for images uses a very strict criterion** (all 16 codebook indices must match), but no statistics are reported on match frequency, codebook size, codebook usage, or reconstruction quality (Section 2.3). Without these, it is difficult to assess whether the VQ approach produces a viable n-gram signal or whether matches are too sparse to be meaningful.

### Trivial
None.

## Nice-to-Haves

- A fuller conceptual motivation for why n-gram patterns in state-action-reward trajectories should be informative for RL (the paper's current explanation — "capturing sequential patterns within trajectories" — is intuitive but vague).
- An ablation that isolates the n-gram mechanism's effect more cleanly (e.g., does an n-gram head with access to only state information underperform one with access to full transitions?).

## Removed Points

These points were raised in the input reviews but removed per the filtering rules. They are listed here for completeness but should not be weighted in evaluation.

- **"Transitivity" typo (line 227):** Removed per formatting/typo rules — this is a parser issue, not an author error.
- **Missing comparison to more recent baselines:** Removed per rule — missing related works should not be mentioned without external confirmation.
- **Random seed control not reported:** Removed per reproducibility nitpick rule.
- **"The gap is suspiciously large" (Key-to-Door):** Removed — this is speculation without evidence of a specific confound, and the paper's results are consistent across multiple environments.
- **Criticism that n-gram motivation for RL is vague:** Demoted to nice-to-have — asking for a full theoretical account is outside the paper's stated empirical scope.

## Novel Insights

The most useful insight emerging from this review is the structural weakness in how the paper's evaluation framework interacts with its claims. The EMP metric conflates two distinct benefits (data efficiency and HP robustness), and the headline 27× figure turns out to be a cross-paper comparison rather than a controlled measurement — a pattern worth watching in ICRL papers generally. The unexplained gap between ablation EMP values (~0.67–0.76) and the main results (~0.96) is a genuine signal that the experimental conditions differ or that the method's advantage is more fragile than the main figures suggest.

## Suggestions

1. **Verify or retract the 27× claim.** Run your own baseline with 2048 goals to confirm it replicates AD's published performance, then directly compare N-Gram at 100 goals. Alternatively, drop the cross-paper 27× comparison and report the data multiplier visible in your own controlled experiments (Figure 1 suggests ~4–8× within your implementation), which is still a solid result.

2. **Clarify the ablation conditions.** State how many goals and histories were used in the ablations (Table 1) and explain why the EMP values (0.67–0.76) differ from the ~0.96 in Figure 5.

3. **Add a single-run comparison.** Train both methods at the best HP configuration found during random search and report final return with error bars.

4. **Add basic attention analysis and VQ statistics.** At minimum: what does the n-gram head attend to? How often does the VQ encoder produce matches? What is the codebook utilization rate?

## Score and Decision

**Calibration Anchors (all from deepreview_13k_calibration):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `b5MCteb3w7.md` (Actions Speak Louder Than States) | 4.75 | R1 | Yes | ICRL paper with a more fundamental flaw (conditioning on task invalidates ICRL claim, weight -6.03). Our paper lacks that flaw but also lacks the theoretical contribution. |
| `uIKZSStON3.md` (ICEE) | 7.25 | R1 | Yes | Stronger empirical story and clearer evaluation, but also heavy novelty questions (-7.84). Our paper is weaker empirically. |
| `p9OsTj0nMP.md` (XLand-100B) | 7.00 | R1 | Yes | Dataset paper, not directly comparable. Significantly stronger resource contribution. |
| `Pj06mxCXPl.md` (Transformers Learn TD) | 6.67 | R1 | Yes | Theoretical paper with rigorous proofs. Our paper lacks theoretical depth. |
| `2PKLRmU7ne.md` (ICL and Occam's Razor) | 5.60 | R1 | Yes | Stronger theoretical framing and more rigorous experiments. Our paper's evaluation is weaker. |
| `PIHPmNNp7w.md` (RA-DT) | 4.67 | R2 | Yes | Method shows inconsistent results across environments (-9.86 weight). Our paper's results are more consistently positive. |
| `Jwtpbhheoy.md` (ICL Uncertainty) | 5.00 | R2 | No | ICL theory paper, different domain. |
| `Af7CsWMUNI.md` (ICL at Representation Level) | 5.25 | R2 | No | ICL in NLP, different domain. |

**Bracket:** Round 1 bracket was 3.5–5.5. After itemizing the most similar anchors — particularly "Actions Speak Louder Than States" (4.75, shares an ICRL setting but has a more fundamental flaw) and "RA-DT" (4.67, weaker results) — the bracket narrows to 4.5–5.5.

**Weighted-item comparison:** Our draft's heaviest negative weight (-4.18 for the 27× claim) is substantially less damaging than the fundamental flaws in "Actions Speak" (-6.03, -7.74) or RA-DT (-9.86, -9.60), but our heaviest positive weights (+4.18–+4.62) are also lower than the strongest positives in higher-scoring papers like "ICL and Occam's Razor" (+5.74–+6.09) or ICEE (+5.45). The paper's weighted sum is slightly positive (~+5.7), consistent with a borderline score.

**Final score:** 5.0. The paper has a genuine novel contribution and consistently positive results, but the evaluation methodology has significant issues — particularly the unsupported 27× headline claim and the unexplained ablation inconsistency — that prevent it from being a clear accept. The core approach is promising and the weaknesses are fixable, but in its current form the evidence does not fully support the claims at the asserted strength.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>