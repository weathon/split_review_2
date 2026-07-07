Based on my reading of the paper and calibration, I now have enough to write the final review. The initial bracket is **5–6.5**, with QZO sitting slightly above the ~5.8 anchor (`myYzr50xBh`) due to a cleaner core idea and broader evaluation, but below the 6.75 anchor due to missing comparisons with directly related prior work.

---

## Summary
QZO (Quantized Zeroth-Order Optimization) proposes fine-tuning quantized LLMs by perturbing continuous quantization scales rather than discrete integer weights, enabling gradient-free updates on 4-bit and 2-bit models. A Directional Derivative Clipping (DDC) module is introduced to stabilize training and is theoretically motivated as reducing gradient estimate variance. The method achieves ~18× memory reduction over 16-bit AdamW fine-tuning and performs comparably to MeZO while using 3× less GPU memory.

## Strengths
- **Elegant and principled core idea**: Decomposing θ = Δ ⊙ θ̄ and perturbing only the continuous scale Δ (Eq. 5) cleanly sidesteps the precision gap without de-quantization/re-quantization, and extends naturally to any PTQ method that exposes its scales.
- **Broad compatibility demonstrated**: QZO is applied successfully to both scalar-based GPTQ (4-bit) and codebook-based AQLM (2-bit), across OPT-6.7B, Llama-2-7B, Llama-3.1-8B, and Llama-2-13B—covering three families and two quantization paradigms.
- **Memory efficiency is concrete and large**: Figure 1 and Tables 1–3 show 4.8–6.3 GB peak memory vs. 14.8–20.5 GB for MeZO on 7–8B models; enabling Llama-2-13B on a single 24 GB GPU via 2-bit quantization.
- **DDC ablation is rigorous**: Figure 2 demonstrates training collapse (NaN at step 22) without DDC; Figure 3 shows robustness to C over a wide range (75–150), validating the design choice empirically.
- **Variance reduction analysis**: The derivation in Eq. 7–8 showing that clipping reduces the second moment of the gradient estimate is a meaningful theoretical contribution, conditional on Theorem 1 being correct.

## Weaknesses

### Fatal
None.

### Major
- **Missing experimental comparison with directly related methods**: The related work (Section 2) explicitly cites Feng et al. (2024), Zhou et al. (2025), and Bar & Giryes (2025) as sharing the same paradigm of combining ZO with quantization. QZO's claimed advantages over these works—"inherently more efficient and flexible," "does not require quantization of perturbation noises or re-quantization at each iteration"—are described qualitatively but never measured. An empirical comparison on at least one dataset/model is necessary to substantiate these claims.

- **Theorem 1 (unbiasedness of clipped estimate) appears incorrect without additional assumptions**: The paper states: "Clipped gradient estimate is an unbiased estimate of the full gradient" (p. 4). Standard gradient clipping truncates the distribution and *does* introduce bias. The paper defers the proof to Appendix A; without the proof inline, this claim cannot be verified, and the entire variance-reduction argument in Eq. 7–8 rests on it. If Theorem 1 requires special assumptions (e.g., symmetry of d, specific distributional properties), these must be stated explicitly in the main text.

### Minor
- **Table 3 (2-bit Llama-2-13B) lacks MeZO baseline**: Only Zero-Shot-Q is compared, offering no context for whether the gains come from fine-tuning or model strength. Even an out-of-memory note with a single-GPU MeZO run or a CPU-offloading baseline would help.
- **Inconsistent FLOPs across models in Table 2 are unexplained**: OPT-6.7B shows QZO using ~12,000× fewer FLOPs than MeZO (8.19×10¹³ vs 9.91×10¹⁷), while Llama-2-7B shows only ~50× fewer and Llama-3.1-8B shows QZO using *more* FLOPs than full fine-tuning (7.9×10¹⁶ vs 2.48×10¹⁶). No explanation is given; this likely reflects different training-step counts, but the paper does not clarify.
- **Upper-bound "Fine-tuning" uses SGD, not AdamW** (Footnote 2: "limited budget"). Since AdamW is standard for LLM fine-tuning and would yield notably higher accuracy, the reported gap between QZO and fine-tuning is underestimated, weakening the claim that QZO is "on par" with the upper bound.

### Trivial
None.

## Nice-to-Haves
- A wall-clock time comparison between QZO and MeZO per training step would complement FLOPs, since the two-forward-pass structure of QZO is the same as MeZO but may differ due to quantization kernel overhead.
- A comparison with QLoRA (Dettmers et al., 2023) would help practitioners understand where ZO-based methods sit relative to gradient-based PEFT on quantized models.
- Training convergence curves (accuracy vs. steps) would illustrate how the reduced parameter space (scales only, ~1% of weights) affects convergence speed compared to MeZO.

## Removed Points
*These points are flagged to be removed; treat them with caution.*
- **Reproducibility concerns about model availability or missing hyperparameters**: Not applicable per review policy; models and code are cited as publicly available.
- **Missing appendix proofs**: The proof of Theorem 1 is in Appendix A, which is stripped by the parser. Per policy, this is not a flaw.
- **Formatting issues**: Not applicable; parser artifacts only.
- **Generic strengths about the importance of memory-efficient training**: Removed as insufficiently specific.

## Novel Insights
The key insight is that post-training quantization methods already expose a continuous intermediate—the quantization scale Δ—that participates in the forward pass via de-quantization (w = Δ · w̄). This makes Δ a natural target for ZO perturbation without requiring any de-quantization/re-quantization cycle, and is compatible with any PTQ method as a drop-in enhancement. This observation, while simple in hindsight, opens a plug-and-play avenue for gradient-free fine-tuning across the entire PTQ ecosystem.

## Suggestions
1. Add at least one quantitative comparison with Feng et al. (2024), Zhou et al. (2025), or Bar & Giryes (2025) to substantiate the efficiency and flexibility claims.
2. Either present the proof of Theorem 1 inline or clearly state the distributional assumptions required for the unbiasedness claim—e.g., via the symmetry of the ZO perturbation direction z.
3. Standardize training steps or explain the FLOPs discrepancy in Table 2 across model families.
4. Include a MeZO or fine-tuning baseline for Llama-2-13B in Table 3, even if achieved via multi-GPU or CPU offloading.

## Score and Decision

**Anchor papers (all rounds):**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `myYzr50xBh.md` | 5.80 | R1 | ZO+quantization, most similar topic; accepted; QZO has cleaner idea, broader quantization coverage, more model families |
| `zcx6rIMbbR.md` | 5.40 | R1 | Quantized LLM fine-tuning, 3-stage optimization; rejected; weaker core contribution than QZO |
| `FK6T0U4Mg1.md` | 4.25 | R1 | SubZero ZO optimization without quantization integration; rejected; less relevant |
| `euZD4YTXKu.md` | 3.75 | R1 | ZO offloading, weaker evaluation and motivation; rejected |
| `xw29VvOMmU.md` | 6.75 | R1 | LQ-LoRA: quantized fine-tuning with first-order methods; accepted; stronger baseline comparisons |
| `1MHgMGoqsH.md` | 3.00 | R1 | Forward-forward/ZO unification; rejected; weaker contribution |
| `E4Fk3YuG56.md` | 8.50 | R1 | Cut Cross-Entropy; accepted; much stronger systems contribution |
| `7X65yoKl3Y.md` | 3.33 | R1 | ALLoRA; rejected; different topic |
| `wg1PCg3CUP.md` | 8.00 | R1 | Scaling laws for precision; accepted; different contribution type |

**Round 1 bracket**: 5–6.5, anchored against `myYzr50xBh` (5.80, most topically similar, accepted). QZO has a cleaner and more general core idea, covers more model families, and demonstrates broader quantization compatibility. However, it shares the missing-comparison weakness and has the additional Theorem 1 concern. Score converges to **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>