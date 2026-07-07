## Summary

HARA proposes a unified framework that replaces all non-linear operators in Transformers (GELU, SiLU, Softmax, LayerNorm, RMSNorm) with a single canonical architecture built from arithmetic primitives and a shallow ReLU network. The key algorithmic contribution is a DP-based parameter initialization pipeline that systematically derives near-optimal PWL breakpoints before converting them to ReLU network weights, outperforming naive direct training by orders of magnitude. The paper evaluates on BERT, Swin, LLaMA, and DiT, reporting <0.1% performance change and projecting >60% area savings from hardware synthesis estimation.

## Strengths

- **The DP-based initialization convincingly outperforms naive direct training across all eight tested operators, with MSE improvements of several orders of magnitude (Table 4).** This is a genuine, clearly-demonstrated algorithmic improvement that is likely reproducible. The gap between "Naive" (MSE 1.38e-03 for GELU) and "DP w/ FT" (MSE 1.89e-07) is so large that it cannot be explained by hyperparameter tuning alone.

- **The symmetry-based decomposition for infinite-domain activation functions (Section 3.3.1, Table 1) is mathematically clean and principled.** Expressing GELU/SiLU/Sigmoid/Tanh/Softplus as ReLU(x) plus an even decaying correction, then approximating only the correction on a finite domain, transforms an unbounded problem into a bounded one in a way that guarantees correct asymptotic behavior (f(x)→0 as x→-∞). This prevents the catastrophic extrapolation failures that Figure 3 illustrates for naive ReLU Net training.

- **The end-to-end evaluation spans four architecturally diverse models (BERT, Swin, LLaMA, DiT) across NLU, vision, language generation, and text-to-image domains.** This breadth demonstrates that the approach generalizes across model families, not just a single architecture.

- **The core research question — whether all non-linear operators in Transformers can be replaced with a single canonical ReLU network — is well-motivated and timely.** The paper correctly identifies that existing methods are both function-specific (causing hardware bloat) and heuristic (leading to suboptimal accuracy).

## Weaknesses

### Major

- **End-to-end results lack variance or confidence intervals, and two of six metrics improve after approximation, indicating that the reported deltas are within measurement noise rather than signal.** Table 6 shows Swin Top-5 improving from 95.516→95.538 and DiT HPSv2 from 0.2724→0.2731 after replacing exact operators with approximations. Without standard deviations, confidence intervals, or multiple seeds, the reader cannot distinguish between "HARA preserves accuracy to machine precision" and "HARA causes a 0.05% degradation within the run-to-run variance." The headline claim of "< 0.1% change" may be true but is vacuous if 0.1% is simply the noise floor of these evaluations. This is the single most consequential problem — it undermines the paper's most important quantitative claim.

- **No end-to-end comparison against the operator-level baselines (NN-LUT, RI-LUT).** Table 3 shows HARA achieves 2–7 orders of magnitude lower MSE than NN-LUT and RI-LUT on individual operators (e.g., GELU at HD=16: HARA MSE 3.20e-08 vs. NN-LUT 2.07e-06). However, the paper never checks whether those baselines cause any measurable end-to-end degradation. If NN-LUT's GELU approximation (MSE ≈ 2e-6 at HD=16) also yields <0.1% accuracy change in BERT, then the operator-level MSE advantage is irrelevant for the use case. The paper needs to show that the less accurate baselines actually harm model performance to support the claim that HARA's systematic optimization "is crucial for high-fidelity function approximation."

- **The baseline for the 8-bit quantization claim is ambiguous.** The text states HARA-approximated models use "standard 8-bit post-training quantization" and Table 6's column header reads "Baseline" vs. "HARA (8,8,8)." It is unclear whether the Baseline column reflects a full-precision model or an equivalently quantized one. These are very different comparisons: if the baseline is full-precision and HARA is quantized, the near-identical results are actually impressive — but if the baseline is also quantized, the results say something different. The paper should report both "Baseline (FP)" and "Baseline (INT8)" to clarify this.

### Minor

- **The number of linear segments N in the DP algorithm (Algorithm 1) is never reported for any experiment.** N directly determines the trade-off between approximation quality and hardware cost, and the results cannot be reproduced without it. The paper mentions HD=8 for the URN hardware configuration, but N (number of PWL segments) and HD (hidden dimension of the ReLU network) are distinct parameters.

- **The "Naive" direct training baseline in the ablation study (Table 4) is not specified** — no information about number of epochs, learning rate, initialization scheme, or whether any hyperparameter tuning was attempted. While the order-of-magnitude gap between Naive and DP makes it unlikely that better tuning would erase it entirely, the omission hurts reproducibility and opens the comparison to fair methodological scrutiny.

- **No analysis of how approximation errors propagate through chained operators for Softmax and LayerNorm.** Section 3.3.2 decomposes these into Pow2 and Log2 primitives, each approximated separately, then recombined with arithmetic operations. The combined error of this pipeline is not characterized. A worst-case or statistical error bound would strengthen the paper — currently the reader must assume individual Pow2/Log2 MSEs translate linearly through the computation.

- **The hardware savings claim (62.3% area, 51.7% power) is projected against a baseline of three separate specialized units (Softmax LUT + LayerNorm LUT + GELU LUT).** While the paper is transparent about this baseline, a single reconfigurable piecewise-linear unit or time-multiplexed LUT is a more obvious alternative to HARA's URN than three parallel specialized units. The savings relative to such alternatives would likely be smaller. The paper should either add this comparison or explicitly discuss the expected savings against a single reconfigurable unit.

### Trivial

None.

## Nice-to-Haves

- An analysis of the DP algorithm's computational complexity (runtime as a function of sample points and N).
- Throughput/latency analysis to confirm the URN can process all operators at required rates without becoming a bottleneck.
- Extension of the symmetry decomposition approach to cover more activation functions (e.g., Swish variants).

## Removed Points

These points were identified in the source reviews but are removed for the reasons stated:

1. "No mention of polynomial approximation methods (Chebyshev/minimax)" — Removed per hard rule: do not flag missing related works.
2. "The literature review is adequate but somewhat thin" — Removed: general negativity without specific anchor to the paper.
3. "DiT evaluation uses HPSv2 not FID/CLIP" — Removed: the paper can choose appropriate metrics for its evaluation; this is scope creep.
4. "Figure captions off-center" / "typos" — Removed per hard rule: formatting artifacts from PDF parsing.
5. "NN-LUT/RI-LUT not described as relying on heuristics" — Removed: the paper frames them as representative baselines, which is standard practice.

## Novel Insights

The harsh critic's review surfaces one genuinely insightful observation beyond the paper's own contributions: the fact that two of six end-to-end metrics *improve* after replacing exact operators with approximations is a clear symptom that the reported differences are within measurement noise. This is a stronger argument than a generic request for "add error bars" — it directly shows that the presented data cannot support the precision claimed. The reviewer's framing of this as the "single most consequential problem" is correct: it is not merely a presentation preference but a structural gap in the evidence for the paper's headline claim.

## Suggestions

1. **Add variance to end-to-end results.** Run each model with at least 3 random seeds and report mean ± std for all metrics in Table 6. This alone would either validate or undermine the paper's most important claim.
2. **Report NN-LUT and RI-LUT end-to-end** on at least one model (e.g., BERT on SQuAD) to demonstrate that their higher operator MSE translates to measurable performance degradation.
3. **Clarify the quantization baseline.** Add a "Baseline (INT8)" column to Table 6, or explicitly state whether the reported baseline is full-precision or quantized.
4. **Report N (number of DP segments)** for each operator configuration used, and detail the Naive training protocol (epochs, LR, initialization).
5. **Add a fairer hardware baseline:** compare against a single reconfigurable PWL/LUT unit (not three separate specialized units) and report savings.

## Score and Decision

**Score: 4.5**

**Decision: Reject**

**Reasoning:** HARA makes genuine contributions — the DP-based initialization and symmetry decomposition are technically solid and the unified architecture idea is well-motivated. However, the paper's core quantitative claims are not adequately supported by the evidence presented. The end-to-end accuracy preservation claim rests on a table with no variance measures where some metrics *improve* after approximation, making the reported differences uninterpretable. The operator-level accuracy advantage over NN-LUT/RI-LUT is never validated end-to-end, so the reader cannot assess whether HARA's MSE advantage actually matters. The quantization claim is ambiguous about the baseline. These are fixable issues, but in their current form they leave the paper's strongest claims insufficiently demonstrated.

**Calibration Anchors (all retrieved across rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/.../LlE61BEYpB.md (FLARE) | 4.00 | R1 | Yes | Similar theme (ReLU for transformer efficiency), similar weaknesses (incomplete evaluation, novelty concerns). HARA has stronger algorithmic contribution but similar evidential gaps. |
| /home/.../S4wo3MnlTr.md (trainable manifold) | 4.25 | R1 | Yes | Similar theme (ReLU approximation via principled initialization). HARA has broader practical validation but weaker statistical rigor. |
| /home/.../Mhu9iNGKqP.md (DP polynomial approx) | 4.50 | R2 | Yes | Most methodologically similar (DP for function approximation). HARA matches on technical depth but has broader end-to-end validation. Strongest anchor. |
| /home/.../nXV3C8aKxZ.md (L-Mul) | 4.50 | R1 | Yes | Similar profile: interesting idea + estimated hardware savings + insufficient hardware validation. HARA's negatives are less severe in magnitude. |
| /home/.../I8pdQLfR77.md (IMLP) | 4.75 | R1 | No | Similar (activation function improvement for transformers). HARA has broader scope. |
| /home/.../osoWxY8q2E.md (ReLU Strikes Back) | 7.33 | R1 | Yes | Related topic (ReLU for LLM efficiency) but much stronger empirical evaluation. HARA is not at this quality level. |
| /home/.../YFxfcQMLWX.md (PADRe) | 6.75 | R2 | No | Stronger framework paper. HARA has comparable architectural ambition but lags in evaluation rigor. |
| /home/.../CPBdBmnkA5.md (AERO) | 6.00 | R2 | No | Similar theme (removing non-linearities). HARA's approach is more general, but AERO's evaluation is more complete. |

**Initial bracket:** After comparing HARA's weighted items against anchors, I estimated 4.0–5.5. HARA's strongest negatives (missing variance: -5.95, missing baseline comparison: -4.64) are comparable to those in papers scoring 4.0–4.75, while its strongest positives (DP initialization: +5.74, symmetry decomposition: +5.28) suggest it has real technical substance. The final score of 4.5 is anchored by Mhu9iNGKqP (4.50, most methodologically similar) and nXV3C8aKxZ (4.50, similar profile of estimated hardware savings with incomplete validation). HARA does not reach the 6+ range because its main empirical claim lacks basic statistical support — this puts it decisively below papers like PADRe (6.75) and AERO (6.00) that have comparable ambitions but more rigorous evidence.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>