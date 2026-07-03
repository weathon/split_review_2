Now I have everything I need. Let me produce the final consolidated review.

---

## Summary

This paper integrates hardcoded n-gram induction heads (from Akyürek et al. 2024) into transformers for in-context reinforcement learning (ICRL), building on Algorithm Distillation (AD). The central idea is that n-gram attention layers provide an inductive bias that makes ICRL models more data-efficient and less sensitive to hyperparameters, while being adaptable to pixel-based observations via vector quantization. Experiments on Dark Room, Key-to-Door, and Miniworld environments show that the n-gram method consistently outperforms AD, especially in low-data regimes.

## Strengths

1. **First application of hardcoded n-gram induction heads to ICRL.** The paper explicitly notes (Section 5, line 223) that it is "the first to apply these findings in a decision-making setting." Prior work studied n-gram induction heads in language or synthetic settings; transferring this to RL's state-action-reward structure is a non-trivial and sensible extension. The two matching variants tested (full transitions and just states) represent a genuine adaptation effort.

2. **Clear evidence of reduced hyperparameter sensitivity.** Figure 2 shows that on Dark Room with 1K learning histories, the n-gram model finds optimal hyperparameters in ~20 random assignments versus over 400 for AD — an order-of-magnitude reduction (Section 4.1, line 171). This is a concrete, well-documented engineering benefit supported by the EMP evaluation protocol.

3. **Consistent performance advantage across diverse environments.** The n-gram method outperforms AD in discrete (Dark Room, Key-to-Door) and pixel-based (Miniworld) environments. For example, Figure 4 shows the method achieving near-optimal return (~1.9) where AD plateaus at ~1.3 with limited task diversity. Figure 5 shows similar advantages in pixel-based settings. The advantage is most pronounced in low-data conditions, which is precisely where the paper claims improvement.

4. **Principled evaluation protocol.** The use of Expected Maximum Performance (EMP) with random hyperparameter search, equal batch sizes, and fixed 10K gradient steps (Section 3.2, line 139) avoids cherry-picking and provides a fair comparison of method robustness rather than best-case performance.

5. **Informative ablations.** Table 1(a,b) shows that performance is largely insensitive to n-gram length (1- to 3-gram all within 0.71–0.76 EMP) and layer position (all within 0.67–0.69). Table 1(c) shows that a deliberately broken (permuted) n-gram mask (0.51±0.03) does not hurt performance relative to baseline (0.52±0.02) — a useful negative result confirming the method does no harm when its mechanism is ineffective.

## Weaknesses

### Major

- **The headline 27× data reduction claim is not fully supported by controlled evidence.** The paper states (Section 4.2, line 179; Figure 4 caption, line 129) that their method needs "27x less data" compared to AD. This figure is derived by comparing the n-gram model at 100 goals to the original AD paper's [17] reported requirement of 2048 goals. While the paper does run AD at 2048 goals in Figure 1 (baseline return 1.7 vs ngram 2.0), the specific 27× computation is deferred to Appendix B (stripped from this review), and the comparison in Figure 4 relies on citing [17] for the baseline's 2048-goal requirement rather than demonstrating it within the same experimental pipeline. The controlled comparison in Figure 4 (100 goals, 500–1000 histories) cleanly shows n-gram outperforming AD, and the qualitative claim of improved data efficiency is well-supported. However, the precise quantitative claim of a 27× reduction requires verifying that the baseline implementation reproduces the original AD results at the 2048-goal scale under identical data generation and evaluation conditions.

### Minor

- **Figure 6 compares methods on different training set sizes.** In the Miniworld-Dark hyperparameter sensitivity experiment (Figure 6, left), the caption states (line 195) that the n-gram model is trained on 50 goals while the baseline uses 60 goals. Although the performance gap is large enough that this is unlikely to reverse the qualitative conclusion, this confound should be removed in a proper controlled comparison. The Miniworld-Key-to-Door panel (right) correctly uses equal sizes (2K goals for both).

- **Ambiguity in how n-gram matching operates on RL sequences.** The paper states (Section 2.3, line 95) that the input sequence is (s₀, a₀, r₀, …, sₙ, aₙ, rₙ) and tests two matching approaches — comparing full transitions (a_{i-1}, r_{i-1}, s_i) or just states (s_i = s_j). However, it does not specify how the n-gram length n (from Equation 1) interacts with the interleaved action/reward tokens when matching "just states." For n > 1, does the n-gram pattern check consecutive state positions (skipping a/r tokens) or consecutive sequence positions (which would mix states, actions, and rewards)? The mechanism is understandable in broad strokes, but the token-level mechanics could be specified more precisely for reproducibility.

- **Experimental conditions for Table 1 ablations are not specified.** The EMP values in Table 1 range from 0.51–0.76, far below the near-optimal ~0.96 reported in Figure 5 for Miniworld-Dark. The paper states the ablations are in "Miniworld-Dark" (Section 4.4, line 203) but does not state the number of goals, learning histories, or other data configuration used. This makes it unclear whether these results reflect a different, harder setting or the same setting as Figure 5.

### Trivial

None.

## Nice-to-Haves

- Show confidence intervals or variance across seeds for EMP curves in Figures 2, 4, and 5 (Figure 6 already includes shaded regions).
- Report the actual number or proportion of n-gram matches found in each environment to deepen understanding of when the mechanism is effective.

## Removed Points

These points were raised by reviewers but are removed from the main weakness list with justification:

- **"Authors never run AD with 2048 goals in their own implementation"** — Factually incorrect. Figure 1 clearly shows AD baseline at 2048 goals with return 1.7. This claim is removed.
- **Hyperparameters not listed for random search** — Section 3.2 (line 143) references Appendix C for exact setups; appendix is stripped by the parser. Removed per hard rules.
- **Data generation details (Q-Learning hyperparameters, noise schedule specifics)** — These are reproducibility nitpicks about trivial implementation details standard for the field. Removed per hard rules.
- **Missing related works / missing appendix content** — Removed per hard rules (parser strips appendices; related works claims are unverifiable without external sources).
- **Formatting or style nitpicks** — Removed per hard rules (parser artifacts, not author errors).
- **Strength Finder generic claims about importance of the problem** — Removed as superficial or not anchored to specific paper content.

## Novel Insights

The most interesting observation from reviewing this paper is that the n-gram method's benefits are concentrated in **low-data / low-diversity regimes** (few goals, few learning histories). When data is abundant (e.g., Figure 1 at 2048 goals), both methods perform well, with n-gram still marginally ahead. This suggests the mechanism functions primarily as a **data-efficiency regularizer** rather than a universal performance booster. The paper's framing as "reducing data requirements" is accurate, but this also implies that in settings where large datasets are available (e.g., massive multi-task datasets like XLand-100B), the advantage may be minimal. This contextualizes the contribution more precisely than the paper's own broad claims.

## Suggestions

1. Run a fully controlled experiment where *both* methods are evaluated at the same data scales used for the 27× claim (e.g., 2048 goals and 100 goals within the same codebase and evaluation pipeline), so the data efficiency ratio is measured directly rather than via cross-paper comparison.
2. Equalize training goal counts in the Figure 6 left panel (use 50 goals for both methods, not 50 vs 60).
3. Specify in Section 2.3 how the n-gram length interacts with the interleaved action/reward tokens for the "states" matching variant — i.e., whether the comparison skips non-state positions or whether the sequence is restructured.
4. State the experimental configuration (number of goals, learning histories) used for the Table 1 ablations explicitly.

## Score and Decision

Due to a technical issue with the calibration retrieval tool, I could not retrieve anchor papers for direct comparison. I instead calibrated my score against the ICLR scoring guidelines and my assessment of the paper's strengths and weaknesses relative to typical conference submissions in this area.

The paper makes a solid, clearly-motivated contribution — the first application of hardcoded n-gram induction heads to ICRL — with consistent empirical evidence across three environments, a principled evaluation protocol, and informative ablations. The weaknesses are real but addressable: the 27× claim is over-extrapolated from a cross-paper comparison, and there are minor methodological issues (Figure 6 training size mismatch, underspecified matching mechanics, unclear Table 1 conditions). None of these invalidate the core finding that n-gram heads improve data efficiency and reduce hyperparameter sensitivity in ICRL.

The paper is on the accept side of borderline. With revisions to temper the precise quantitative claim and fix the comparison fairness issue, the contribution would be credible and useful to the ICRL community.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>