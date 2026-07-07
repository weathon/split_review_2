Now let me write the final consolidated review.

## Summary

DIPOLE proposes a new RL algorithm for diffusion policy optimization that replaces the unstable exponential weighting in KL-regularized RL with a dichotomous decomposition. The key idea: the optimal policy factorizes into a "positive" policy (sigmoid-weighted for reward maximization) and a "negative" policy (complement-weighted for reward minimization), trained with bounded sigmoid weights. Inference uses a CFG-style linear combination of both policies' scores, enabling controllable greediness via a hyperparameter ω. Evaluations span ExORL (9 tasks), OGBench (30 tasks), and NAVSIM autonomous driving with a 1B-parameter VLA model.

## Strengths

- **Principled theoretical derivation.** The chain from the greedified KL-regularized objective (Eq. 5) → closed-form solution (Theorem 1, Eq. 6) → dichotomous decomposition (Eqs. 7–8) → CFG-style inference (Eq. 10) is coherent and mathematically sound. This is the paper's genuine intellectual contribution, and the reasoning is clearly laid out in the main text.

- **Sigmoid weighting genuinely addresses the instability of exp-weighted regression.** The observation that σ(βG) ∈ (0,1) while exp(βG) can explode for large β is correct and directly addresses the limitation of methods like Kang et al. (2023) and Zheng et al. (2024). The bounded training losses in Eq. (9) are a real practical improvement.

- **Large-scale validation with a 1B-parameter VLA model.** Training a vision-language-action diffusion policy on NAVSIM is non-trivial engineering. The qualitative trajectory correction examples in Figure 2 are visually compelling, and the offline-to-online fine-tuning results (Table 3) show clear improvement over initial pre-trained performance (e.g., humanoidmaze-medium: 61→97).

## Weaknesses

### Major

- **The base dichotomously-trained policy without rejection sampling underperforms IFQL on ExORL, undermining the claim that the dichotomous training objective itself resolves the limitations of exp-weighted regression.** On every ExORL task, DIPOLE w/o rs is worse than IFQL (which uses rejection sampling): e.g., Walker walk 679 vs 844 (−165), Jaco reach-top-right 84 vs 193 (−109). The full DIPOLE (with rejection sampling) then beats IFQL, meaning the performance gains are substantially driven by the CFG-style inference combination + rejection sampling, not the training objective in isolation. The paper claims the method "resolves the issue of being dominated by high-return samples" (Section 3.2), but if the trained policies alone are worse than IFQL's, this claim is not supported. DIPOLE w/o rs is also not reported on OGBench (Table 2), so its standalone performance cannot be assessed on that benchmark.

- **The NAVSIM navtest comparison (94.8 vs 88.3 baseline) is misleading.** The paper's Table 4 shows "DP-VLA w/ DIPOLE navtest" at 94.8 PDMS — a 6.5-point improvement — but this model was trained on test-split data, while all baselines (including the 88.3 baseline) were trained only on navtrain. The paper acknowledges this distinction in the table header but frames the 6.5-point gain as headline result without sufficient caveat. The only fair navtest-to-navtest comparison is against DPPO navtest (89.0), where the gap is 5.8 points rather than 6.5. The honest navtrain-to-navtrain comparison is +1.4 PDMS (88.3→89.7), which is modest. The paper should present the navtrain result as primary and the navtest result as a secondary, qualified variant.

- **How the advantage function is estimated is not described in the main text.** For a claimed RL method, the critic (value/advantage) learning is a core component. Section 3.3 states "we can set G(s,a) as the advantage function A(s,a)" but never specifies how A(s,a) is computed — whether through expectile regression (as in IQL/IFQL), TD-learning, or another method. The architecture, loss function, and interaction with diffusion policy training are all deferred to the (parsing-stripped) appendix. This makes the method incompletely specified from the main paper.

### Minor

- **No sensitivity analysis for the key hyperparameter ω.** The paper's selling point is "controllable greediness" via ω, yet no experiment shows the effect of varying ω on a representative task. Since ω is the primary new hyperparameter (replacing the role of β in standard KL-regularized RL), the absence of any empirical study of its effect is a gap.

- **Two diffusion policies from scratch doubles compute vs single-policy methods, with no acknowledgment.** For the RL benchmarks (ExORL, OGBench), the paper trains two independent diffusion models from scratch (Eq. 9). This doubles the policy parameter count and training cost relative to methods like IFQL or FQL that train a single policy. The 1B-parameter VLA case uses LoRA (lower cost), but the RL benchmark cost is not discussed.

- **DIPOLE underperforms on some OGBench categories without discussion.** On ant-soccer-arena-navigate, DIPOLE (57±7) is worse than FQL (60±2). On humanoidmaze-large-navigate, DIPOLE (6±2) is worse than IFQL (11±2). The paper's claim "achieves better performance in most task categories" (Section 4.1) is technically true but the exceptions should be acknowledged.

### Trivial

- Several ExORL improvements are within one standard deviation (e.g., Cheetah run: DIPOLE 274±12 vs IFQL 269±16). The paper does not discuss statistical significance.

## Nice-to-Haves

- Report DIPOLE w/o rs on OGBench to allow assessment of the base dichotomous decomposition's standalone effect.
- Compare DIPOLE w/o rs against IFQL/FQL w/o rs (where both use single-policy inference without rejection sampling), which would be a fairer ablation of the training objective.
- Provide a compute cost comparison (training time, inference time) between DIPOLE and single-policy baselines.
- Add an experiment varying ω on a representative ExORL or OGBench task to demonstrate the claimed "controllable greediness."

## Removed Points

These points were flagged by the harsh critic but are removed with justification:

1. **"The claim of resolving the optimality-stability trade-off is overstated because inference uses unbounded (1+ω)ϵ⁺−ωϵ⁻."** Removed. The paper's claim is about training stability (bounded sigmoid weights in Eq. 9), not inference. The reviewer conflated training and inference. The training loss IS bounded, which is the genuine improvement.

2. **"Hyperparameter tuning fairness concern — DIPOLE's hyperparameters may have been tuned per task while baselines used defaults."** Removed as speculative. No evidence is provided that DIPOLE was tuned per task differently from baselines.

3. **"The paper says 'we do not observe the adoption of this scheme in many recent diffusion-based RL methods' which is odd because the paper cites methods that use it."** Removed. The paper's claim is nuanced — it observes that most methods don't use the exp-weighted scheme directly (they clip or use small β), which is accurate.

4. **"The connection to CFG is presented as a separate discovery rather than a direct consequence."** Removed. The paper derives CFG as a consequence of the decomposition; this is accurate.

5. **"Missing related works."** Removed per policy — related work coverage is adequate, and the reviewer cannot verify missing references.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's main novel insight — that the DIPOLE w/o rs underperformance relative to IFQL suggests the real gains come from the CFG inference rather than the training objective — is a valid critique of the paper's framing, not an additional discovery about the method itself.

## Suggestions

1. **Add a paragraph in Section 3.3 describing how the advantage function is estimated** (architecture, loss, training procedure). This is a methodological necessity, not a nice-to-have.

2. **Reframe the NAVSIM results:** present the navtrain comparison as the primary result, and clearly label the navtest variant as an additional demonstration of how the method can leverage distribution-matched rollouts.

3. **Add a simple ω-sweep experiment** on a single task (e.g., Walker walk or a representative OGBench task) to demonstrate the claimed controllability of greediness.

4. **Discuss the DIPOLE w/o rs results more honestly.** Acknowledge that the base dichotomous policies alone underperform IFQL on ExORL, and explain that the full method's advantage comes from the CFG-style combination during inference.

5. **Add a brief note on computational cost** — at minimum, acknowledge that two diffusion models are trained and explain why this cost is justified by the performance gains.

## Score and Decision

**Calibration:** I compared DIPOLE against relevant calibration anchors:

| Anchor | Score | Comparison |
|--------|-------|------------|
| DAC (ldVkAO09Km) — Diffusion Actor-Critic | 6.50 | Cleaner theory than DAC, but weaker empirical evidence (DIPOLE w/o rs < IFQL is a significant gap DAC doesn't have). DAC's weaknesses are about missing ablations; DIPOLE's are about core evidential support. Below DAC. |
| SRPO (xCRr9DrolJ) — Score Regularized Policy Optimization | 6.25 | DIPOLE's theory is cleaner and better presented than SRPO's. But SRPO's main weakness is marginal empirical benefit, which DIPOLE shares (on navtrain). Comparable or slightly below. |
| EFM (HA0oLUvuGI) — Energy-Weighted Flow Matching | 6.25 | Both have similar-level theoretical contributions. EFM was criticized for overclaiming novelty; DIPOLE is more honest. But DIPOLE has the base-method-underperforms issue. Slightly below. |
| CFDG (cXxfVkRCHJ) — Offline-to-Online CFDG | 3.00 | DIPOLE has much stronger theory and better empirical framework. Clearly above. |
| BDQL (gEdg9JvO8X) | 3.67 | DIPOLE is better motivated and has more comprehensive evaluation. Clearly above. |

**Round-1 bracket:** [3.5, 6.5]. **Final score:** 5.0.

The weighted-item comparison shows DIPOLE shares DAC's "strong theoretical contribution" (+4 weight) but lacks DAC's "strong empirical results" (+3 weight) — DIPOLE's empirical evidence is undercut by the DIPOLE w/o rs < IFQL finding and the NAVSIM navtest framing. DIPOLE sits between the 3.5–5.5 and 5.5–7.5 anchors: above CFDG/BDQL (which lack theoretical depth) but below DAC/SRPO (which have cleaner empirical support). Score 5.0 reflects a borderline paper with a solid theoretical contribution whose experimental evidence needs shoring up.

**MY FINAL SCORE:** <score>5.0</score>
**MY FINAL DECISION:** <decision>Reject</decision>