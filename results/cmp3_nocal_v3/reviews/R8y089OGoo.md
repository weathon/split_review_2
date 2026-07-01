## Summary

This paper proposes DIPOLE, an RL algorithm for diffusion policy optimization that addresses the instability of exponential-weighted regression approaches. The key idea is a greedified KL-regularized objective that decomposes the optimal policy into a pair of "dichotomous" policies — one maximizing return, one minimizing return — whose scores are linearly combined at inference time (analogous to classifier-free guidance). The method is evaluated on ExORL (9 tasks), OGBench (30 tasks), and a 1-billion-parameter VLA driving model on NAVSIM.

## Strengths

- **Theoretically clean and novel decomposition.** The derivation from the greedified KL-regularized objective (Eq. 5) through Theorem 1 (Eq. 6) to the sigmoid-based dichotomous policies (Eqs. 7–8) is mathematically sound and genuinely novel. The weights `σ(βG)` and `1−σ(βG)` are bounded, directly addressing the instability caused by unbounded exponential weights in prior weighted-regression methods. The connection to classifier-free guidance (Eq. 10) is insightful and turns two-model training into a controllable inference mechanism.

- **Broad empirical scope.** The paper evaluates across standard RL benchmarks (39 tasks across ExORL and OGBench) and a large-scale real-world autonomous driving benchmark (NAVSIM with a 1B-parameter VLA model). This breadth is unusual and meaningfully demonstrates scalability beyond small-scale tasks.

- **Honest disclosure of key variants.** The paper reports a "DIPOLE w/o rs" variant on ExORL (Table 1) and explicitly separates navtrain/navtest results on NAVSIM (Table 4), providing some ability to assess the method's intrinsic contribution versus inference-time rejection sampling.

- **Strong offline-to-online results.** Table 3 shows substantial fine-tuning gains (e.g., humanoidmaze-m: 61→97, antsoccer-arena: 43→90) that go well beyond what imitation learning alone provides, and these results use the proper training-split protocol.

## Weaknesses

### Fatal

None.

### Major

1. **The method's contribution is confounded by rejection sampling, and the w/o rs ablation is missing on the more challenging benchmark.** On ExORL (Table 1), the gap between DIPOLE w/o rs and DIPOLE with rs is large and uneven (e.g., Walker "stand": 793→953; Walker "walk": 679→910). The w/o rs variant substantially underperforms FQL on Jaco tasks (84 vs. 224 on reach-top-right). Yet on OGBench (Table 2) — where the method's strongest results appear (e.g., cube-double-play 44 vs. FQL's 29) — the w/o rs variant is not reported at all. The paper claims DIPOLE *"completely resolv[es] the issue of being dominated by high-return samples"* (Section 3.2, line 105), but the reader cannot determine how much of the improvement comes from the dichotomous training objective versus the rejection sampling applied at inference. This is the single most consequential gap in the evaluation.

2. **The NAVSIM "navtest" result (94.8 PDMS) is presented in the main comparison table alongside methods trained on the training split, creating a structurally misleading comparison.** The paper states (line 211) that this model is *"trained on the test split"* and the table caption notes the data-split difference. However, the 94.8 value appears as a row in the same Table 4 as UniAD, Transfuser, and Hydra-MDP — all trained on the standard training split — without any visual separation (e.g., a horizontal divider or separate sub-table). The primary fair comparison (navtrain: 89.7 PDMS, a 1.4-point gain) is a solid but modest result. The paper's most striking headline number comes from a non-standard evaluation protocol, and the table's layout invites an apples-to-oranges comparison that the text does not adequately counter.

### Minor

3. **DPPO — the most directly related prior method — is absent from the main RL benchmark comparisons.** The paper includes DPPO on NAVSIM (Table 4) and criticizes policy-gradient approaches (Black et al., 2024b; Ren et al., 2025) for Gaussian approximation issues in the introduction. Yet DPPO is absent from the offline-to-online results (Table 3), where a comparison would be most natural. While DPPO is an online method and may not apply to pure offline RL (Tables 1–2), its absence from the fine-tuning experiments leaves the reader without a direct point of reference on standard benchmarks.

4. **No discussion of DIPOLE's own computational cost.** DIPOLE trains two diffusion models (ϵ⁺ and ϵ⁻) or two LoRA modules. All baselines (IQL, ReBRAC, IDQL, IFQL, FQL, CFGRL) train a single policy. The paper criticizes prior methods (direct backprop, DPPO) for being *"extremely costly"* and *"prolonged"* (Section 1) but provides no runtime, parameter-count, or FLOP comparison for its own two-model design. This is a notable omission for a paper that motivates its approach partly on computational grounds.

### Trivial

None.

## Nice-to-Haves

- An ablation of the greediness factor ω on at least one domain would help readers calibrate sensitivity. The paper notes ω as a key hyperparameter providing *"flexible control over the level of greediness"* (Section 3.2) but does not report which values were used or how they were chosen. (The paper states that Appendix D.4 contains ablation studies, which were stripped by the parser, so this concern may be partially addressed there.)

- Reporting DIPOLE w/o rs on OGBench (especially cube-double-play) would directly address the primary confound concern and substantially strengthen the paper's core claim.

## Removed Points

These points from the input review were removed with justification:

- **Missing ω/β ablation in main text, missing appendix content, negative policy collapse speculation, "per-state optimization assumption" presentation nitpick, "not observed" claim being overstated, missing related works, framing of π⁻ as "slightly slippery":** These are either (a) addressed in the appendix (which is stripped by the parser and therefore cannot be verified as missing), (b) speculative and not grounded in paper evidence, (c) minor presentation nitpicks that do not affect the paper's validity, or (d) factually questionable without external verification. See the filtering rules in the merger instructions.

## Novel Insights

The most important insight from the reviews is the extent to which rejection sampling drives the reported improvements. While the paper provides a w/o rs ablation on ExORL showing that the dichotomous method itself provides some benefit (outperforming CFGRL on all ExORL tasks), the gap between w/o rs and with-rs is large, and the absence of this ablation on OGBench means the paper's most compelling results (cube-double-play: 44 vs. FQL 29) cannot be attributed to the dichotomous training alone. This is a concrete, addressable gap rather than a fundamental flaw.

## Suggestions

1. Report DIPOLE w/o rs on OGBench (Table 2). If the w/o rs variant still outperforms FQL and IFQL on cube-double-play, the paper's core claim is substantially strengthened.
2. In Table 4, separate the navtest row from the main comparison (e.g., with a horizontal line or a separate panel) and clearly label it as a non-standard evaluation split.
3. Add a brief computational cost comparison (training time per iteration or parameter count) relative to at least the single-policy baselines.
4. Add DPPO to the offline-to-online results (Table 3) if feasible, or explicitly discuss why direct comparison is not meaningful in the offline setting.

## Score and Decision

**MY FINAL SCORE:** <score>7</score>
**MY FINAL DECISION:** <decision>Accept</decision>