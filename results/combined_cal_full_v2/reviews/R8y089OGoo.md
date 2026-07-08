Now let me write the final consolidated review.

## Summary

This paper proposes DIPOLE, a reinforcement learning algorithm for diffusion policy optimization that decomposes the optimal policy into two dichotomous components (positive/reward-maximizing and negative/reward-minimizing) via a greedified KL-regularized RL objective. The resulting score combination at inference time mirrors classifier-free guidance, enabling controllable greediness. The paper evaluates on 39 offline RL tasks across ExORL and OGBench, offline-to-online settings, and a large-scale autonomous driving benchmark (NAVSIM) with a 1B-parameter VLA model.

## Strengths

- **Mathematically elegant decomposition (weight=9.37).** Factoring the optimal policy into positive and negative components via the sigmoid identity (Eq. 7→10) is genuinely clever. The resulting linear score combination directly mirrors classifier-free guidance, providing a clean theoretical bridge between KL-regularized RL and CFG that prior work (CFGRL) only approximated with heuristic indicator functions.

- **Strong empirical results on ExORL (weight=10.70).** DIPOLE consistently outperforms baselines on the Walker, Quadruped, Cheetah, and Jaco domains, often with sizable margins (e.g., Walker walk: 910 vs. next-best 844 for IFQL; Walker run: 442 vs. 406). The "DIPOLE w/o rs" variant also generally exceeds CFGRL, confirming the improvement is not just from rejection sampling.

- **Principled solution to an acknowledged problem (weight=8.70).** The instability of exp-weighted regression for diffusion policies (Section 3.1) is a real issue addressed with ad hoc fixes (clipping, small β). DIPOLE replaces unbounded exp weights with bounded sigmoid weights, which is a more principled alternative.

- **Breadth of evaluation (weight=6.93).** The paper evaluates on 39 offline RL tasks, offline-to-online settings, and a large-scale autonomous driving benchmark with a 1B-parameter VLA model, demonstrating scalability to complex real-world problems.

## Weaknesses

### Major

- **NAVSIM navtest results are presented in a potentially misleading way.** The paper reports a 6.5-point PDMS improvement (88.3 → 94.8) from RL fine-tuning on the navtest (test) split, but the 88.3 baseline (DP-VLA) is trained on navtrain, making this an apples-to-oranges comparison. The paper does state that "we provide a variant of our model trained on the test split" (line 211–213) and labels table rows, but the text still highlights the navtest-vs-navtrain comparison as the headline result without caveat. The fair navtrain-only improvement is 1.4 points (88.3 → 89.7). Additionally, DPPO is only evaluated on navtest (89.0), making it impossible to compare DIPOLE and DPPO on the same navtrain split. The navtest results (94.8 vs. DPPO 89.0) are legitimate and show strong improvement, but the presentation should clearly separate these or add explicit caveats about the distribution shift.

### Minor

- **OGBench results are more mixed than the paper's framing suggests.** On humanoidmaze-large-navigate, DIPOLE (6±2) is *worse* than IFQL (11±2). On antsoccer-arena-navigate, DIPOLE (57±7) is within noise of FQL (60±2). On cube-single-play, DIPOLE (97±2) is essentially tied with FQL (96±1). The paper's claim of "best or near-best performance" is technically accurate but elides these cases where the advantage is marginal or reversed, especially on the hardest long-horizon tasks. The paper should discuss these limitations more candidly.

- **Compute and memory cost are not discussed.** DIPOLE requires training two separate diffusion models (positive and negative) and combining them at inference, which doubles parameter count and compute relative to single-model approaches like FQL. The paper does not address this trade-off, especially on tasks where the gains over FQL are marginal.

- **The greedified objective (Eq. 5) is an engineered surrogate, not a standard KL-regularized RL objective.** The reference policy in Eq. (5) is μ·σ(βG)/Z, which depends on the same value function G being optimized. While the paper acknowledges this "shares a similar spirit with some offline RL methods" (line 85), it does not discuss what relationship this surrogate bears to the actual expected return. This is a clear design choice (common in RL) but should be acknowledged more explicitly.

### Trivial

None.

## Nice-to-Haves

- A direct comparison with clipped exp-weighted regression would test whether the dichotomous machinery provides benefit over a simpler fix.
- DPPO should be evaluated on the navtrain split for a fair comparison with DIPOLE on navtrain.
- Hyperparameter sensitivity analysis for β and ω would strengthen the paper's practical utility.

## Removed Points

These points from the input review were removed after cross-verification against the paper:

1. **Circular dependency of G and π (Issue 3).** The critic claimed Theorem 1 treats G as fixed while G = A^π depends on the current policy. This is a standard approximation made by all actor-critic methods; it is not specific to DIPOLE. In the offline setting, G is estimated from the static dataset, which avoids the circularity. This does not constitute a unique weakness of this paper.

2. **Missing implementation details (Issue 5).** Complaints about β/ω values missing from the main text and how μ is obtained from behavior policies were standard details relegated to the appendix (referenced as Appendix C and D). Per review guidelines, criticisms about appendix-deferred content that the parser has stripped are not held against the paper.

3. **"Theoretical analysis treats G as fixed" concerns.** These apply to essentially all actor-critic algorithms and are not a paper-specific flaw.

4. **Strengths about general problem importance.** Generic strengths about the problem being "important" were removed as lacking specific anchoring to the paper's content.

## Novel Insights

The most striking insight from the review is how the dichotomous decomposition via the sigmoid identity transforms an inherently unstable exponential weighting scheme into two stable bounded-weight policies, while the resulting score combination formula directly and unexpectedly mirrors classifier-free guidance. This provides a principled RL foundation for what CFGRL previously approximated with heuristics. The review does not surface additional novel insights beyond what the paper itself contributes.

## Suggestions

1. Add an explicit caveat in the NAVSIM results section that the navtest variant trains on test-split data and should be compared primarily against DPPO on the same split, not against the navtrain baseline.
2. Report DPPO results on the navtrain split for a fair comparison.
3. Discuss the compute cost trade-off (dual models vs. single-model baselines) explicitly.
4. Add a comparison with clipped exp-weighted regression to validate that the dichotomous machinery provides benefit over simpler fixes.
5. Include a sensitivity analysis or range summary for β and ω in the main text.

## Score and Decision

**Calibration Report.**

*Round 1 bracket anchors (by score band):*

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| BDQL | gEdg9JvO8X.md | 3.67 | R1 | Yes | Weaker paper — limited novelty, unconvincing empirical results, minor improvement over baselines. Unlike DIPOLE, it lacks a strong theoretical contribution and the experiments do not show clear dominance. |
| EFM (QIPO) | HA0oLUvuGI.md | 6.25 | R2 | Yes | Also uses weighted regression for offline RL with diffusion. Novelty was questioned and results were mixed (scores 5,8,6,6). DIPOLE's dichotomous decomposition is more novel and its evaluation is broader. |
| SRPO | xCRr9DrolJ.md | 6.25 | R1 | Yes | Mixed reception (8,3,8,6). Novel idea (score regularization) but novelty questioned and results marginal. DIPOLE has stronger experiments and cleaner theory. |
| DAC | ldVkAO09Km.md | 6.50 | R1 | Yes | Most similar paper. Formulates KL-constrained policy iteration as diffusion noise regression. Strong theoretical contribution and clean experiments on D4RL. DIPOLE has broader evaluation and comparable theoretical novelty, but the NAVSIM presentation issue is a weakness DAC doesn't share. |

*Weighted-item comparison:*

DIPOLE's strengths (weights 6.93–10.70) align closely with DAC's (8.33–10.05) and EFM's (8.69–9.23). DIPOLE's highest-weight weakness (OGBench mixed results, weight 6.62) is moderate, and its major NAVSIM weakness has weight 2.80 — less severe than DAC's missing-baseline concerns (weight 7.58) or EFM's novelty concerns (weight −2.59). The ExORL results (weight 10.70) are the strongest positive signal, comparable to the strongest items in DAC and EFM.

*Score placement:*

The paper sits above BDQL (3.67) and comparably to DAC (6.50) and EFM (6.25). The methodological contribution (dichotomous decomposition, CFG connection) is novel and well-executed. The ExORL empirical results are strong. The NAVSIM presentation issue is the primary weakness — it is addressable and does not invalidate the core contribution, but the current framing is misleading. The OGBench results are more mixed than ideally one would like. On balance, the paper is a borderline accept: its core contribution is solid, but the evaluation presentation needs cleanup.

*Final score: **6.0** — borderline accept.*

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>