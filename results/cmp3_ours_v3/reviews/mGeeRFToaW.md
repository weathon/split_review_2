Now I have sufficient calibration context. Let me write the final consolidated review.

## Summary

This paper proposes QZO (Quantized Zeroth-Order Optimization), a method that enables ZO fine-tuning of quantized LLMs by perturbing the continuous quantization scale parameters rather than the discrete quantized weights. This sidesteps the fundamental incompatibility between ZO (which requires continuous perturbations) and quantization (which produces discrete weights). The paper also proposes Directional Derivative Clipping (DDC) for training stability. QZO is demonstrated with GPTQ (4-bit) and AQLM (2-bit) across several 7B and 13B models, achieving up to 18× memory reduction vs. full-precision AdamW fine-tuning.

## Strengths

1. **The core idea is genuinely creative and clean.** Instead of perturbing discrete quantized weights (infeasible for ZO), QZO perturbs the continuous quantization scale parameters while keeping quantized weights fixed (Section 3.2.1, Definition 3.3). This cleanly resolves the tension between ZO's need for continuous perturbations and quantization's discrete weights. This is the paper's strongest contribution.

2. **Orthogonal to diverse PTQ methods.** The paper demonstrates compatibility with both scalar-based quantization (GPTQ, 4-bit) and codebook-based quantization (AQLM, 2-bit) (Section 3.2.1, Section 4.2). This extensibility is non-trivial and makes the method practically relevant.

3. **Memory profiling is concrete and honestly measured.** Figure 1 and Table 1 provide clear per-method breakdowns. The 18× reduction vs. full AdamW fine-tuning is a real number, and the demonstration of fine-tuning Llama-2-13B on a single 24GB GPU at 2-bit precision is a useful empirical result.

## Weaknesses

### Major

1. **No variance reporting across multiple runs — comparative claims are unverifiable.** Every result in Tables 1 and 3 is a single number with no indication of variance, number of random seeds, or repeated trials. This is a structural evidential gap because: (a) ZO methods are known to have high gradient variance (the paper itself emphasizes this in Section 3.2.2); (b) the paper makes comparative claims like "QZO even beats MeZO with noticeable margins, e.g., 85.5 vs. 80.7 on SQuAD" (Section 4.2) — without variance estimates, this could be a single favorable seed against an unfavorable one. At minimum 3–5 random seeds per configuration with mean and standard deviation are needed.

2. **The DDC variance-reduction proof is not established by the derivation in the main text.** The derivation in Eqs. 7–8 contains a mathematical gap. To conclude Var[clipped] ≤ Var[unclipped], one needs (∇L)² ≤ E[||clipped||]² — i.e., the expected norm of the *clipped* estimate must be at least as large as the true gradient norm. But clipping reduces magnitude (d' ≤ d by Eq. 6), making the opposite inequality expected. The paper asserts the result "holds almost surely" (line 122) without bridging this gap. Since the appendix is not accessible in this review process, the main-text derivation does not, on its own, constitute a valid proof. (The empirical evidence in Figure 2 remains useful regardless — the theory should either be corrected or DDC presented as an empirical heuristic.)

3. **Missing empirical comparison against prior ZO+quantization methods.** Section 2 cites three prior works (Feng et al., 2024; Zhou et al., 2025; Bar & Giryes, 2025) that "enable the fine-tuning of quantized models" but provides no experimental comparison against any of them. The paper's claim that QZO is "inherently more efficient and flexible" (Section 2) is asserted without head-to-head evidence. Even a single comparison (one model, one dataset) would ground this claim.

4. **The FLOPs comparison in Table 2 is misleading and the "1%" claim is numerically inaccurate.** The FLOPs figures appear to count only parameter-update computation (perturbation + update of trainable parameters), not the forward passes. Since both MeZO and QZO perform two forward passes per step (the dominant cost), the reported 10,000× FLOPs difference grossly overstates the practical computational advantage. Furthermore, the claim "QZO uses only about 1% of the FLOPs of MeZO" (Section 4.2) is numerically wrong for the reported data: the actual ratios in Table 2 are 0.008% (OPT-6.7B), 2% (Llama-2-7B), and 7% (Llama-3.1-8B). "About 1%" does not characterize any of the three tested models.

### Minor

5. **Upper bound (fine-tuning) uses SGD, not AdamW.** The paper acknowledges this in a footnote ("Due to limited budget on computational resources, fine-tuning experiments are conducted with SGD optimizer unless otherwise specified"). Using SGD instead of AdamW substantially weakens the upper bound, since AdamW is the standard optimizer in practice. The gap between QZO and this upper bound is therefore less informative than claimed.

6. **The "on par with MeZO" claim is too broad given visible gaps.** Table 1 shows QZO lags MeZO on several configurations (e.g., OPT-6.7B SST-2: 87.6 vs. 93.0; Llama-3.1-8B CB: 69.6 vs. 91.1; Llama-3.1-8B BoolQ: 78.2 vs. 83.4). While the paper acknowledges this in passing, the summary claim of being "on par" (abstract, Section 5) overstates the consistency.

7. **Limited ablation of the clipping threshold C.** Only SST-2 with one model (Llama-2-7B) is tested (Figure 3). The paper mentions instability when C > 150 (line 279) but shows no quantitative data points above 150. Additionally, DDC's effect is only demonstrated on a single configuration (Figure 2) — it is unclear whether better-tuned hyperparameters could avoid collapse without clipping.

8. **2-bit experiments are limited.** Only one model (Llama-2-13B) and one quantization method (AQLM) are tested, with no comparison against MeZO or any other fine-tuning method.

### Trivial

9. The claimed "1% of the FLOPs of MeZO" is numerically inaccurate — the actual ratios in Table 2 are 0.008%, 2%, and 7% for the three models tested.

## Nice-to-Haves

- Analyze what kinds of task-specific adaptations are possible within the restricted space of scale-only fine-tuning (since only quantization scales are updated, not the discrete weight integers).
- Clarify what operations are counted in the "Total FLOPs" column of Table 2, and include an apples-to-apples comparison that accounts for forward-pass cost.
- Test DDC's sensitivity to C on more than one dataset.
- Ablate whether DDC is needed when hyperparameters (learning rate, ε) are carefully tuned, or whether it is always beneficial.

## Removed Points

The following points from the input review were removed per filtering rules:

- **"QZO's memory reduction over MeZO is essentially the quantization ratio"**: Removed because this misunderstands the contribution. The paper's claim is that QZO *enables* ZO fine-tuning on quantized models, thereby obtaining the quantization method's memory savings. This is the method working as designed, not a weakness.
- **Formatting/style nitpicks and section-by-section notes about what the paper "could" analyze**: Removed per filtering rules (generic scope-creep criticisms, minor presentation notes).
- **"The 18× reduction mixes multiple sources of savings"**: Not a weakness — the paper is clear that QZO combines ZO (eliminating gradients/optimizer states) with quantization (compressing weights). Combining orthogonal techniques is the point.
- **"Theorem 1 is biased because clipping introduces bias"**: The reviewer asserted this without seeing the appendix proof. The retained weakness focuses on the verifiable gap in Eqs. 7–8 of the main text, not on the appendix proof of Theorem 1.

## Novel Insights

The most valuable observation from the review process is the mathematical gap in the DDC variance-reduction derivation (Eqs. 7–8): the chain requires an inequality ((∇L)² ≤ E[||clipped||]²) that is neither justified nor obviously true given that clipping reduces magnitudes. The second novel finding is that the "1% of FLOPs" claim is not only misleading in what it counts but is numerically inconsistent with the paper's own Table 2 (ratios ranging from 0.008% to 7%).

## Suggestions

1. **Add multiple random seeds (at least 3) with mean and standard deviation to every configuration in Tables 1 and 3.** This is the single change that most affects whether the evidence stands.
2. **Fix the DDC variance-reduction proof or present DDC as an empirical heuristic.** The derivation in Eqs. 7–8 does not prove Var[clipped] ≤ Var[unclipped] as currently written. If the appendix proof is correct, present it clearly in the main text. If not, remove the theoretical claim and present DDC as empirically motivated (which Figure 2 already supports).
3. **Add an empirical comparison against at least one prior ZO+quantization method** (Feng et al., 2024; Zhou et al., 2025; or Bar & Giryes, 2025).
4. **Clarify what the "Total FLOPs" in Table 2 counts**, and add a forward-pass-inclusive comparison since that dominates runtime.
5. **Correct the "1% of the FLOPs" numerical claim** to match the actual ratios in Table 2.

## Score and Decision

**Round 1 bracket:** [4.0, 5.5].

**Anchor papers used for calibration:**

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| Zeroth-Order Fine-Tuning of LLMs with Transferable Static Sparsity (SensZOQ) | 5.80 (Accept) | R1 | Also combines ZO+quantization for LLMs; accepted despite missing baselines and single-seed concerns. QZO has a more novel core idea but additional evidential issues (theoretical gap, misleading FLOPs). |
| SubZero: Random Subspace ZO Optimization (SubZero) | 4.25 (Reject) | R2 | Similar ZO-for-LLM fine-tuning paper; rejected for limited novelty and missing baselines. QZO has stronger conceptual novelty but comparable evidential problems plus a theoretical gap. |
| Stochastic Two Points Method (S2P) | 5.25 (Reject) | R1 | ZO optimization method for deep models; rejected for missing baselines and limited evaluation. QZO has more practical grounding but similar baseline issues. |
| EfficientQAT | 3.00 (Reject) | R1 | Pure quantization paper, no ZO; not directly comparable but serves as lower anchor. |
| MeZO-A³dam | 4.75 (Reject) | R2 | ZO + adaptive method for LLMs; similar score band, similar evidential concerns. |

**Narrowing to final score:** QZO's core conceptual contribution (perturbing quantization scales rather than weights) is genuinely novel and stronger than SensZOQ's combination of standard ZO with sparsification. However, the paper has more evidential problems than SensZOQ (which was accepted at 5.80): a theoretical gap in the DDC derivation (Eqs. 7–8), a misleading FLOPs comparison with a numerical inaccuracy, and missing ZO+quantization baselines. These place QZO below SensZOQ but above SubZero (4.25), which lacked QZO's conceptual novelty. The paper sits in the borderline-reject range.

**Final score: 4.5 — borderline reject.** The paper has a genuinely clever idea with practical potential, but the experimental validation suffers from critical shortcomings (no variance estimates, flawed theoretical claim, missing baselines, misleading FLOPs comparison) that prevent acceptance in current form. Substantial revision could make this a strong paper.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>