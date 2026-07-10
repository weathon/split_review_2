Now let me compile the final review.

## Summary

This paper proposes DIPOLE, an RL algorithm for fine-tuning diffusion policies. The core idea is to decompose the optimal policy (from a greedified KL-regularized objective) into a pair of dichotomous policies — one weighted by σ(β·G(s,a)) for reward maximization, the other by (1−σ(β·G(s,a))) for minimization. During inference, the score functions of the two learned diffusion models are combined linearly (Eq. 10), resembling classifier-free guidance and providing controllable greediness via a hyperparameter ω. Experiments span 39 tasks on ExORL and OGBench (offline + offline-to-online), plus a 1B-parameter VLA model for autonomous driving on NAVSIM.

## Strengths

1. **Elegant theoretical derivation.** The decomposition of the optimal policy into sigmoid-weighted dichotomous components (Eqs. 7–9) is mathematically clean and well-motivated. The connection to classifier-free guidance (Eq. 10) is insightful and provides a natural inference-time control mechanism via ω. [favorability=11.08]

2. **Broad empirical evaluation.** The paper tests DIPOLE across standard offline RL benchmarks (39 tasks on ExORL and OGBench), offline-to-online fine-tuning, and a large 1B-parameter VLA model for real-world autonomous driving on NAVSIM. This breadth is genuinely impressive and demonstrates practical ambition. [favorability=8.97]

3. **Clear problem motivation.** Section 3.1 correctly identifies the fragility of exp-weighted regression for diffusion policies — exploding loss under large β and training dominated by high-return samples — which is a genuine limitation not adequately addressed in prior work. [favorability=8.88]

## Weaknesses

### Fatal
None.

### Major

1. **Missing baseline that directly tests the central claim.** The paper's main motivation (Section 3.1) is that the exp-weighted regression scheme (Eq. 4) suffers from optimality-stability trade-offs and inefficient learning, and DIPOLE is proposed to solve these problems. Yet none of the baselines (IQL, ReBRAC, IDQL, IFQL, FQL, CFGRL) implement a diffusion policy trained with Eq. (4). Without comparing against a simple exp-weighted diffusion regression baseline using the same architecture, critic, and data, the reader cannot verify whether the dichotomous formulation actually solves the problems it claims to solve, or whether the apparent advantages come from unrelated design choices. This is the most significant gap in the experimental evaluation. [favorability=-0.99]

2. **Strong ExORL results are substantially driven by rejection sampling, an orthogonal technique.** The paper reports both "DIPOLE w/o rs" and "DIPOLE" (with rejection sampling) on ExORL. The gap is large and often decisive (e.g., Walker walk: 679→910, Cheetah run: 194→274, Jaco reach-top-right: 84→117). Crucially, **DIPOLE w/o rs is worse than IFQL (which also uses rejection sampling) on all 9 ExORL tasks** (e.g., Walker walk: 679 vs 844; Cheetah run: 194 vs 269). The paper does not report rejection-sampling-free results for IDQL or IFQL, making it impossible to determine how much of DIPOLE's advantage comes from the dichotomous policy learning itself versus the rejection sampling mechanism shared with baselines. The headline "state-of-the-art" claim on ExORL primarily reflects the combination of DIPOLE + rejection sampling, not the core method alone. [favorability=2.06]

### Minor

3. **Computational cost not discussed.** The paper trains two separate diffusion models (π⁺ and π⁻, Eq. 9), roughly doubling the compute of single-model baselines, yet provides no analysis of training time, wall-clock time, or FLOPs. This omission matters for practical adoption, especially given that on OGBench DIPOLE leads in 4/6 categories but trails on 2/6. [favorability=5.24]

4. **Imprecise statement about exp-weighted regression adoption.** Line 72 claims "we do not observe the adoption of this scheme in many recent diffusion-based RL methods," but the paper's own preceding discussion (lines 58–59) cites Kang et al. (2023) and Zheng et al. (2024) as works that use exactly this scheme. The statement is at best imprecise. [favorability=2.76]

5. **Statistical significance is unclear in several results.** Several reported results have large standard deviations that overlap substantially with the second-best method (e.g., Quadruped walk: 928 ± 55 vs IFQL 883 ± 12; humanoidmaze-large-navigate: 6 ± 2 vs IFQL 11 ± 2). Explicit significance testing or effect-size reporting would strengthen the claims. [favorability=4.30]

### Trivial
None.

## Nice-to-Haves

- An ablation study on the greediness factor ω and temperature β would substantiate the claim of "controllable generation" and guide practitioners.
- Reporting DIPOLE w/o rs on OGBench would clarify how much of the performance on that benchmark is attributable to rejection sampling vs. the core method.
- A comparison of training wall-clock time or FLOPs for DIPOLE vs. single-model baselines would help assess the practical cost of training two diffusion models.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Advantage function estimator underspecification**: The critic argued the main paper does not specify how the advantage function is learned. The paper explicitly states "The algorithm pseudocode and additional implementation details are provided in Appendix C and D" (line 123), which is standard practice. The parser strips appendices from all papers. Per the hard rule, weaknesses about missing appendix content are removed.
- **Claim that Eq. (5) is reverse-engineered for algebraic convenience**: This is a speculative motivational criticism. The paper provides a clear rationale (addressing exp-weighted regression limitations, using bounded sigmoid for stability, adding ω for controllability). Removed as speculative/unverifiable.
- **Autonomous driving results being too modest**: The 1.4-point improvement on navtrain is a genuine positive result atop an already SOTA imitation baseline. The 6.5-point improvement on navtest is acknowledged as a non-standard scenario. These are observations, not flaws.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add an exp-weighted diffusion regression baseline (Eq. 4)** using the same architecture and critic as DIPOLE. This is the single most important addition — it directly tests whether the dichotomous formulation addresses the problems it claims to solve.
2. **Report rejection-sampling-free results for IFQL and IDQL** on ExORL, or otherwise present "DIPOLE w/o rs" as the primary result and treat rejection sampling as an optional add-on, so readers can assess the core method's contribution independently.
3. **Provide a sensitivity analysis for ω and β** to substantiate the controllability claims.

## Score and Decision

**Round 1 (Bracketing):** Based on the favorability comparison between the draft's items and anchors from similar-scored papers (DAC: 6.50, SRPO: 6.25, EFM: 6.25, ContraDiff: 5.67, BDQL: 3.67), I bracket the paper between **6.0 and 7.5**. The theoretical contribution (favorability 11.08) is exceptional and the evaluation breadth is strong, but the two Major weaknesses — particularly the missing exp-weighted regression baseline and the rejection sampling confound — prevent it from reaching the upper end of the bracket.

**Round 2 (Narrowing):** Comparing against the closest anchors:
- **DAC (6.50)**: Shares a similarly clean theoretical formulation + a comparably severe missing-comparison weakness (Q-ensemble confound at -1.51 vs this paper's missing baseline at -0.99). DAC's strengths (9.12, 8.44, 9.28, 10.05) are comparable to this paper's (11.08, 8.97, 8.88). This paper's evaluation is broader.
- **EFM (6.25)**: Had lower-favorability weaknesses (-2.59 for novelty concerns vs this paper's -0.99) and weaker experimental differentiation (0.31). This paper is stronger.
- **ContraDiff (5.67)**: Had marginal gains (-0.76) and unclear theoretical justification. This paper has much stronger theory and clearer gains.

The paper's single most negative item (-0.99) is comparable to DAC's weakest (-1.51) and less negative than EFM's (-2.59), placing it above EFM and around or slightly above DAC given the broader evaluation. **Final score: 6.5**.

**Anchors used across rounds:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| cXxfVkRCHJ (CFDG) | 3.00 | R1 | Yes | Much weaker; limited novelty, small gains |
| gEdg9JvO8X (BDQL) | 3.67 | R1 | Yes | Similar topic but rejected due to unconvincing performance |
| xCRr9DrolJ (SRPO) | 6.25 | R1, R2 | Yes | Similar topic, accepted; narrower evaluation |
| ldVkAO09Km (DAC) | 6.50 | R1, R2 | Yes | Most similar in contribution type; slightly stronger theory here |
| HA0oLUvuGI (EFM) | 6.25 | R2 | Yes | Similar weighting-scheme approach; this paper has broader eval |
| XMOaOigOQo (ContraDiff) | 5.67 | R2 | Yes | Also uses both high/low return data; weaker theory than here |
| TeeyHEi25C (Value function...) | 6.25 | R2 | No | Less directly comparable |
| tGQirjzddO (Latent Diffusion...) | 6.33 | R2 | No | Less directly comparable |

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>