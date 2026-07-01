Now I have a clear picture. Let me write the final consolidated review.

## Summary

This paper proposes Quantized Zeroth-order Optimization (QZO), a method that enables zeroth-order fine-tuning of quantized LLMs by perturbing the continuous quantization scale parameter Δ rather than the discrete quantized weights. This bypasses the discreteness problem that prevents direct application of ZO to quantized weights, eliminating the need for de-quantization/re-quantization loops. QZO achieves an ~18× memory reduction vs. 16-bit AdamW fine-tuning (Figure 1), fitting Llama-2-13B in a single 24GB GPU, and performs competitively with MeZO despite using 4-bit weights. A directional derivative clipping (DDC) mechanism stabilizes training.

## Strengths

1. **Genuinely novel and elegant core idea.** The insight of perturbing the quantization scale Δ (Eq. 5, Definition 3.3) rather than the discrete quantized weights θ̄ is conceptually simple yet sidesteps the de-quantization/re-quantization overhead of prior ZO-for-quantized-models work (Feng et al., 2024; Zhou et al., 2025; Bar & Giryes, 2025). This is a substantive conceptual advance.

2. **Dramatic and practically meaningful memory reduction.** QZO enables fine-tuning Llama-2-13B within a single 24GB GPU — something neither full-parameter ZO (MeZO needs ~53GB for 13B) nor 16-bit fine-tuning can do. The 18× memory reduction vs. AdamW (Figure 1, Table 1) moves the capability boundary and is the paper's strongest empirical result.

3. **Orthogonality to existing PTQ methods.** QZO works with both scalar-based (GPTQ, 4-bit) and codebook-based (AQLM, 2-bit) quantization without modification (Section 3.2.1, Table 3), meaning it can benefit from future improvements in PTQ.

4. **Computation efficiency.** QZO fine-tunes only ~0.75% of parameters (5×10⁷ vs. 6.7×10⁹) with correspondingly lower FLOPs (Table 2) — this is not just a memory story but genuine computation savings.

## Weaknesses

### Fatal
None.

### Major

1. **Missing the most relevant practical baseline: QLoRA.** QLoRA (Dettmers et al., 2023) — cited but never used as a baseline — is the standard method for fine-tuning quantized LLMs. The paper's framing ("pushing the limits of memory-efficient training") invites exactly this comparison. A practitioner choosing between QZO and QLoRA needs to know whether QZO's additional memory savings (from eliminating adapters and gradients) come at a meaningful performance cost. Similarly, LoRA (on un-quantized models) would contextualize QZO's savings against a standard parameter-efficient baseline. Without these comparisons, the conclusions about QZO's practical value are broader than the evidence supports.

   *Verification:* The paper compares against Fine-tuning (SGD), Zero-Shot, Zero-Shot-Q, and MeZO only (Section 4.1). QLoRA is in the references but never evaluated.

2. **Theoretical analysis of DDC contains a mathematical error.** Equation 8 (lines 120–122) defines the variance of the clipped gradient estimate as:

   Var[∇̂' L] = E[||∇̂' L||²] **− E[||∇̂' L||]²**

   For a vector-valued estimator, the correct definition is:

   Var[∇̂' L] = E[||∇̂' L||²] **− ||E[∇̂' L]||²**

   The quantities E[||X||]² and ||E[X]||² are not equal in general. The subsequent derivation that Var[∇̂' L] ≤ Var[∇̂ L] relies on this substitution, so the claimed variance-reduction proof does not follow from the algebra presented. The empirical evidence for DDC (Figure 2) remains convincing; this error undermines the *theoretical justification*, not the method itself.

   *Verification:* Equation 8 in the paper (lines 120–122) uses E[||∇̂' L||]² where the correct formula requires ||E[∇̂' L]||².

### Minor

3. **Theorem 1's unbiasedness claim is unqualified.** Theorem 1 (line 112) states that the clipped gradient estimate is "an unbiased estimate of the full gradient of loss w.r.t quantization scales." The two-point SPSA estimator itself carries an O(ε²) bias for smooth functions, and clipping the directional derivative (which Figure 2 shows is active since d routinely exceeds |d| > 100) introduces additional bias whenever probability mass lies outside [-C, C]. The claim as stated (without qualification of "asymptotically" or "approximately") is theoretically suspect. The proof is deferred to the appendix; this is a framing issue in the main text.

4. **No statistical significance or variance reporting.** Tables 1 and 3 report single-run results without error bars, confidence intervals, or multiple-seed runs. For a ZO method acknowledged to have high gradient variance (the paper's own Figure 2 shows directional derivatives ranging from −200 to 300), this is a significant gap. Claims like "QZO beats MeZO with noticeable margins" (85.5 vs. 80.7 on SQuAD) and the large gap on Llama-3.1-8B CB (69.6 vs. 91.1) cannot be assessed for reliability. Single-run reporting is common in this subfield, but it weakens the evidence for comparative claims.

5. **"Upper bound" uses SGD, not AdamW.** The paper labels "Fine-tuning (with SGD)" as the upper bound (Table 1, line 186, footnote 2). SGD fine-tuning of LLMs typically underperforms AdamW fine-tuning by a meaningful margin. The memory comparison (Figure 1) separately lists "Fine-tune w/ AdamW (16-bit)" for memory but not for performance. This inconsistency means the gap between QZO and a true practical upper bound is likely larger than reported. The authors transparently acknowledge the budget constraint, but the "upper bound" framing is misleading.

### Trivial
None.

## Nice-to-Haves

- **Compare against QLoRA on 2–3 representative datasets** (e.g., SST-2, SQuAD) with 1–2 models. This is the single highest-leverage addition to contextualize QZO's practical value.
- **Report results with 3–5 random seeds** including standard deviations, at least for the main claims.
- **Reframe the DDC theoretical analysis**: drop the unqualified unbiasedness claim and present the variance argument as empirical motivation rather than formal proof. The practitioner value of DDC is already demonstrated by Figure 2.

## Removed Points

These points from the input review are flagged for removal; treat them with caution.

- *"Theorem 1's unbiasedness claim is theoretically suspect because the proof is in the appendix (not visible)."* — Removed per the hard rule that parser-stripped appendix sections cannot be criticized as missing. The mathematical concern about the unqualified claim is retained in Weakness #3 above.
- *"The paper does not discuss the inductive bias of fine-tuning only scales."* — This is a speculation about interpretation, not a specific problem with the paper's claims. QZO's parameter efficiency is already quantified in Table 2.
- *"The activation memory is not explicitly measured for QZO."* — The paper mentions this as an advantage (line 130) but does not promise specific numbers; this is a minor omission that does not affect the core claims.
- *Various formatting/style nitpicks and claims about "missing related works."* — Removed per hard rules.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm that the core idea (perturbing quantization scales) is genuinely novel, and surface that the theoretical analysis of DDC contains a verifiable mathematical error (Eq. 8) that the paper's own framing does not acknowledge.

## Suggestions

1. Add QLoRA as a baseline on at least 2–3 datasets (e.g., SST-2, RTE, SQuAD) with Llama-2-7B to contextualize the performance-memory tradeoff.
2. Correct Eq. 8: replace E[||∇̂' L||]² with ||E[∇̂' L]||², and either re-derive the variance reduction or honestly reframe the DDC analysis as empirical motivation.
3. Qualify Theorem 1 to state "approximately unbiased" or specify the conditions under which unbiasedness holds.
4. Report results with 3–5 random seeds including standard deviations for at least the main configuration (Llama-2-7B, 4-bit).

## Score and Decision

Let me round to .5 or .0.

Based on calibration:

**Round 1 bracket:** The paper sits between SensZOQ (5.80, Accepted) which also combines ZO + quantization but with limited novelty, and LOZO (7.00, Accepted) which has cleaner theory. The paper's core idea is more novel than SensZOQ, but the theoretical errors (Eq. 8) are more problematic than any weakness in SensZOQ.

**Round 2 narrowing:** Comparing with the 5.0–6.5 band:
- SensZOQ (5.80, Accepted): Combines sparse ZO + quantization. Criticized for limited novelty but accepted. QZO has more novelty but worse theoretical hygiene.
- Sparse MeZO (5.50, Rejected): Incremental contribution. QZO is more novel.
- Efficient Fine-Tuning of Quantized LLMs via Three-Stage (5.40, Rejected): Directly relevant. QZO has a cleaner core idea.

QZO's core contribution is genuinely novel and the memory savings are impressive. But the Eq. 8 error is a real mathematical mistake, and the missing QLoRA baseline is a notable gap. The paper is stronger than Sparse MeZO (5.50, Rejected) and comparable to SensZOQ (5.80, Accepted) — but the theoretical error prevents me from placing it above SensZOQ.

**Final score: 5.5** — The paper has a genuinely novel idea and practically significant memory savings, but is held back by a verifiable mathematical error in the theoretical analysis (Eq. 8) and the omission of the most relevant practical baseline (QLoRA). These are addressable; the core contribution is solid.

---

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| FK6T0U4Mg1 (SubZero) | 4.25 | R1, Q3 | Random subspace ZO for LLMs; rejected. QZO has more novel core idea. |
| 9BiVepgmWW (LOZO) | 7.00 | R1, Q4 | Low-rank ZO with cleaner theory; accepted. QZO has less rigorous theory. |
| myYzr50xBh (SensZOQ) | 5.80 | R1, Q4; R2,Q1-2 | Sparse ZO + quantization; accepted. QZO has more novelty but worse theory. |
| QhxjQOMdDF (Addax) | 6.00 | R1, Q4; R2,Q2 | Hybrid ZO+SGD; accepted. QZO is comparable in contribution strength. |
| bEqI61iBue (HiZOO) | 5.67 | R1, Q4; R2,Q2 | Hessian-informed ZO; accepted. Comparable paper quality. |
| 4Kw4KAoVnx (Sparse MeZO) | 5.50 | R2, Q1 | Sparse ZO; rejected. QZO has more novelty. |
| wO8WbhsjNG (Bilevel ZOFO) | 5.50 | R2, Q1 | PEFT+ZO; rejected. Similar tier. |
| zcx6rIMbbR (Three-Stage Quant) | 5.40 | R1, Q3; R2,Q1 | Quantized LLM fine-tuning; rejected. QZO is cleaner. |
| xw29VvOMmU (LQ-LoRA) | 6.75 | R2, Q2 | Low-rank + quantized decomposition; accepted. Stronger empirical package. |
| bAFVlpFQvT (CoLM) | 6.75 | R1, Q4; R2,Q2 | Memory-efficient LLM training; accepted. Cleaner but different focus. |

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>