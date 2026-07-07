Now I have enough calibration data. Let me compile the final review.

## Summary of Anchor Comparison

| Anchor | Score | Round | Itemized | Comparison |
|--------|-------|-------|----------|------------|
| PPU unlearning (Xagys9QD3T) | 3.00 | R1 | Yes | Worse written, more fundamental issues; our paper is stronger |
| Auditing Privacy Protection (Uv7bWrIucU) | 4.20 | R1 | Yes | Similar evaluation rigor issues but less novel contribution |
| Label-Agnostic Forgetting (SIZWiya7FE) | 6.00 | R1 | Yes | Stronger evaluation, minor weaknesses only; our paper has more significant gaps |
| Oblivious Unlearning (wAemQcyWqq) | 5.67 | R1 | Yes | Mixed; similar evaluation breadth but more practical concerns |
| UGradSL (hwXUmwJAq5) | 3.00 | R2 | Yes | Has fundamental misunderstandings about unlearning; our paper does not |
| Decoupling Class Label (OHOmpkGiYK) | 5.75 | R2 | Yes | Better evaluation, clearer framing; our paper worse on rigor |

**Round 1 bracket**: [4, 5.5] — narrowed from comparing against anchors. The paper has genuine novelty (first FF unlearning) placing it above 3.0, but evaluation gaps (missing baseline, no error bars) push it below 5.5.

**Weighted comparison**: My draft's strongest negative items are the missing baseline (-6.04) and no statistical rigor (-4.05). The 6.00-scoring Label-Agnostic Forgetting anchor's strongest negatives are much milder (-4.83, -4.32) and its positives are stronger. Conversely, the 3.00-scoring anchors have negatives in the -7 to -10 range from fundamental misunderstandings or editing problems, which our paper doesn't have. This places our paper firmly between these bands.

**Final score**: 4.5

---

## Summary

This paper introduces FF-Erase, the first machine unlearning method specifically designed for Forward-Forward (FF) neural networks, together with G-MIA, a goodness-based membership inference attack for black-box unlearning verification. The core idea is to use a guidance model to provide a stable target goodness distribution, steering the original model's layer-wise goodness scores away from forgetting data via KL-divergence minimization, while periodically recovering utility on remaining data. The paper identifies genuine challenges in adapting gradient-based unlearning to FF models, including sensitivity to parameter tuning and layer-wise independence.

## Strengths

- **Genuine problem novelty.** The paper correctly identifies that machine unlearning for FF models is unexplored and articulates specific challenges (sensitivity to parameter tuning, layer-wise independence) that distinguish the setting from BP-based unlearning (§1, lines 38–41). This is a legitimate gap.

- **Core design idea is well-motivated.** Using a guidance model to provide a target goodness distribution during "forgetting forward" (Eq. 5, KL-divergence objective) is a principled response to the instability problem — more sophisticated than naively minimizing or maximizing goodness (§4.1). The two strategies for generating the guidance model (mini-retrained and fast-distilled) add practical flexibility.

- **G-MIA naturally exploits the FF architecture.** Leveraging layer-wise goodness vectors for membership inference is a clean architectural adaptation. The method is black-box (requires only goodness outputs) and is well-aligned with how FF models represent information (§5). G-MIA consistently outperforms the final-layer black-box baseline across all tested settings (Figure 3).

- **Broad evaluation scope.** Experiments span 4 image benchmarks (CIFAR-10/100, MNIST, Fashion-MNIST) and 3 FF architectures (TinyCNN, AlexNet, VGG13) with state-of-the-art FF algorithms (CwComp, Deeperforward), providing reasonable breadth (§6).

## Weaknesses

### Major

- **Missing critical baseline (finetuning on remaining data).** The paper claims "existing machine unlearning methods are not feasible for FF models" (line 17) but tests only gradient ascent (GA) as a representative approximate method. The simplest baseline in the unlearning literature — continued FF training on the remaining data *D_remain* only (finetuning) — is absent. This baseline is trivially implementable, requires no guidance model, and its inclusion or exclusion would directly test whether the guidance-model framework is necessary. Without it, the reader cannot determine whether the core contribution (guidance-model-based unlearning) is essential or whether a much simpler approach suffices.

- **No statistical rigor.** No confidence intervals, standard deviations, or repeated runs are reported for any experimental result (Table 1, Figures 3–5). This is especially problematic because G-MIA ACC values in the unlearning evaluation cluster at 0.52–0.59 — differences as small as 0.02–0.04 between methods (e.g., FF-Erase(D) 0.5245 vs RE 0.5320 in Figure 4c) cannot be assessed for significance. Accuracy numbers reported to two decimal places (e.g., 81.58 vs 80.76 in Table 1) likewise lack variance estimates, which is insufficient given typical neural network training stochasticity.

### Minor

- **Only one forgetting proportion tested.** All unlearning experiments use β = 20% forgetting data (line 240). Unlearning performance can vary substantially with the fraction removed, and the paper provides no analysis of how FF-Erase behaves with smaller (e.g., 5%) or larger (e.g., 50%) forget sets.

- **Fast-distilled guidance model may leak forgetting data.** The paper claims the guidance model is "ignorant of the forgetting data" (line 121). However, the fast-distilled strategy (Eq. 8) trains the guidance model by minimizing KL-divergence to the original model θ_o, which **was** trained on D_forget ∪ D_remain. Knowledge distillation can transfer information about training data through the teacher's output distribution. The paper does not analyze or even acknowledge this potential leakage, calling into question whether the fast-distilled variant truly separates the guidance model from forgetting data.

- **No ablation of key hyperparameters K (recovery frequency) and λ (recovery weight).** The ablation study (§6.4) only varies guidance model generation parameters (α₁, α₂). Two important algorithmic hyperparameters — recovery frequency K (Algorithm 1, line 138) and recovery weight λ (Eq. 6) — are neither varied nor analyzed, leaving the method's sensitivity to these choices unknown. An ablation removing the recovering forward entirely (K = ∞) would be particularly informative.

- **Synthetic data generation for G-MIA is underspecified.** The method assumes the attacker "can synthesize data that has a similar distribution to the training data" (line 200), citing model inversion techniques. The paper does not specify how synthetic data is generated in practice for the experiments, leaving a key precondition of the attack unclear.

### Trivial

None.

## Nice-to-Haves

- Memory overhead analysis: FF-Erase requires holding both θ_o and θ_g in memory during unlearning, doubling the memory requirement relative to simple finetuning. For the edge-computing scenario mentioned in the introduction, this is a practical concern.
- The paper would benefit from a brief discussion of its limitations and scope (only image classification tested; no analysis of other modalities or FF architectures).

## Removed Points

These points are flagged to be removed, treated with caution:
- Claim that "existing methods fail" framing is unsupported — this is a standard narrative structure partially supported by §6.3. Not a substantive weakness.
- Mixed gradient scenario in Algorithm 1 — the layer-wise sequential update is consistent with how FF models operate; the criticism misunderstands the architecture. Removed as factually incorrect.
- Notation inconsistency (L_H vs L_ff) — L_H likely refers to the same cross-entropy formulation. Trivial.
- G-MIA vs white-box claim unsupported — Figure 3 and the paper's text support this claim for VGG13/CIFAR-100; the reviewer's criticism was inaccurate. Removed.
- "1.9-3.1× faster" misleading — the paper pairs the speed claim with accuracy degradation (abstract, line 9). The trade-off is disclosed, though the G-MIA differences warrant more emphasis. Weakened substantially.
- Missing limitations section — presentation preference, not a substantive flaw.
- Only VGG13/CIFAR-10 in main text — standard space management with appendix results.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add continued FF training on D_remain as a baseline.** This is the simplest possible approach; its success or failure directly tests whether the guidance model is necessary. Either result (success → simpler alternative exists; failure → stronger motivation for the proposed method) would substantially strengthen the paper.
2. **Report all quantitative results with confidence intervals or standard deviations across at least 3–5 random seeds.** This is essential given that G-MIA values often differ by only 0.02–0.04 between methods.
3. **Test at least two additional forgetting proportions** (e.g., β = 5%, 50%) to assess generality.
4. **Analyze potential information leakage in the fast-distilled guidance model.** Measure G-MIA success rate against the distilled model on D_forget vs D_remain to check whether membership information is preserved.
5. **Include an ablation varying K and λ**, or removing the recovering forward entirely (K = ∞), to clarify each component's role in the quality-speed trade-off.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>