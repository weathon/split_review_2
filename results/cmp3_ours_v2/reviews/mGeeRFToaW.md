Now I have a clear calibration picture. Let me produce the final review.

## Summary

This paper proposes Quantized Zeroth-order Optimization (QZO), combining zeroth-order optimization with model quantization for memory-efficient LLM fine-tuning. The key innovation is perturbing the continuous quantization scale Δ (rather than discrete quantized weights) for gradient estimation via a modified SPSA estimator (Q-SPSA), alongside a directional derivative clipping (DDC) mechanism to stabilize training. Experiments on OPT, Llama-2, and Llama-3.1 models across five NLP benchmarks demonstrate substantial memory reduction (e.g., 4.8 GB vs. 14.8 GB for MeZO on OPT-6.7B) while maintaining competitive performance, including a 2-bit Llama-2-13B result on a single 24 GB GPU.

## Strengths

- **Clean and genuinely novel core idea.** Perturbing the continuous quantization scale Δ rather than the discrete quantized weights θ̄ is a creative decomposition that cleanly sidesteps the precision mismatch between ZO and quantized parameters. This is fundamentally different from prior ZO-for-quantized-models work (Feng et al., Zhou et al., Bar & Giryes) which quantizes perturbation noise and applies sign-based updates to discrete weights. The approach is also orthogonal to both scalar-based (GPTQ, 4-bit) and codebook-based (AQLM, 2-bit) PTQ families, as demonstrated in experiments.

- **Concrete and compelling memory savings.** The memory numbers are clearly demonstrated (Figure 1, Table 1): QZO achieves 4.8 GB vs. 14.8 GB for MeZO and 26.8 GB for SGD fine-tuning on OPT-6.7B. The 2-bit Llama-2-13B result (5.78 GB on a single 24 GB GPU, Table 3) is a genuine technical achievement in extreme memory reduction.

- **Competitive performance despite 3× memory reduction.** QZO (4-bit) performs on par with or sometimes exceeds MeZO (16-bit) across multiple tasks (e.g., 85.5 vs. 80.7 F1 on SQuAD with Llama-2-7B), despite using quantized weights. This is a non-trivial result.

## Weaknesses

### Major

- **Missing QLoRA comparison and prior ZO-quantized method comparisons.** QLoRA (Dettmers et al., 2023) — cited in the paper's references — is the canonical method for memory-efficient fine-tuning of quantized LLMs and operates in the same 4-bit regime. QZO's central claim is enabling fine-tuning of quantized models, but the most directly relevant competitor is never empirically compared. Without this comparison, a reader cannot assess whether QZO provides a practical advantage over an existing widely-used method or merely replicates its capabilities. Separately, prior ZO-quantized methods (Feng et al., Zhou et al., Bar & Giryes) are acknowledged in Related Work and claimed to be "inherently more efficient and flexible" (line 52), but no empirical or quantitative comparison is provided. These gaps make it difficult to evaluate the paper's main contribution relative to the state of the art.

- **Theoretical derivation for DDC variance reduction contains a mathematical error.** The critical step in Eq. 8 (line 120) substitutes \( \mathbb{E}[\|\hat{\nabla}\|]^2 = (\nabla_\Delta \mathcal{L})^2 \), equating the squared expected norm of the gradient estimate with the squared norm of the true gradient. For any estimator with non-zero variance, Jensen's inequality gives \( \mathbb{E}[\|X\|] \ge \|\mathbb{E}[X]\| \), so \( \mathbb{E}[\|\hat{\nabla}\|]^2 > \|\nabla_\Delta \mathcal{L}\|^2 \) in general. The conclusion \( \text{Var}[\nabla'] \le \text{Var}[\nabla] \) does not follow from the derivation as presented. The simpler argument in Eq. 7 (second-moment reduction) is valid, but the paper overclaims by framing it as a variance reduction proof. The empirical evidence for DDC (Figure 2) is visually convincing and can stand independently, but the theoretical framing needs correction. Theorem 1 (unbiasedness of the clipped estimator) is also stated without sufficient justification in the main text; the proof is relegated to a stripped appendix.

- **FLOPs numbers in Table 2 appear inconsistent with the method's computation profile.** QZO's reported FLOPs for OPT-6.7B is \( 8.19 \times 10^{13} \) compared to MeZO's \( 9.91 \times 10^{17} \) — a ~12,000× difference. Both methods perform two forward passes through the same model per optimization step, so the dominant compute cost should be similar. The FLOPs for the other two models (Llama-2-7B: \( 2.26 \times 10^{16} \); Llama-3.1-8B: \( 7.9 \times 10^{16} \)) are also inconsistent with each other. The paper states "QZO uses only about 1% of the FLOPs of MeZO" (line 251), but the actual ratio for OPT-6.7B is ~0.008% while for Llama-2-7B it is ~2%. The calculation methodology is not explained, making it impossible to verify.

### Minor

- **No variance reporting across any result.** ZO methods are acknowledged to have high gradient variance (line 104), yet none of the tables report standard deviations, confidence intervals, or results over multiple seeds. Given the stochastic nature of the method (random perturbations \( z \sim \mathcal{N}(0,\mathbf{I}) \)), single-run results cannot rule out the possibility that observed differences (e.g., QZO 90.0 vs. MeZO 83.5 on Llama-2-7B SST-2) are within the noise. This is a standard concern in ZO literature and is addressable.

- **2-bit results (Table 3) only compare against Zero-Shot-Q**, with no other fine-tuning baseline. While this is understandable given the technical challenge of applying other ZO methods at 2-bit, it limits the evaluation to a feasibility demonstration rather than a competitive comparison.

- **The 18× headline memory claim warrants clarification.** The 18× number (Figure 1, abstract) is computed against AdamW fine-tuning at 16 bits (87.6 GB → 4.8 GB). However, the experimental upper-bound throughout the paper is SGD fine-tuning (26.8 GB → 4.8 GB, ~5.6×). Both comparisons are disclosed in the figure, but the paper defaults to the largest possible number in the abstract and introduction without noting that the experimental comparisons use a different baseline.

### Trivial

- Minor imprecision in line 36: "approximates the gradients of quantized weights" — QZO actually approximates gradients of the quantization scales \( \Delta \) with respect to the loss, not gradients of the quantized weights themselves. The distinction matters because QZO updates only ~50M scale parameters out of ~7B total.

## Nice-to-Haves

- An analysis of the learned scale values \( \Delta \) after training (e.g., do they increase or decrease? does the method effectively learn a per-group learning rate?) would deepen understanding of what QZO actually does.
- A discussion of the constrained optimization aspect (Algorithm 1, line 158: \( \Delta_i \leftarrow \max(\Delta_i - \eta_t \cdot d' \cdot z, 0) \)) and its effect on convergence guarantees would be useful.
- Convergence speed / wall-clock time comparison with baselines (beyond FLOPs) would strengthen the practical evaluation.

## Removed Points

These points were flagged in the input review but are removed with justification:

1. **"Missing the most relevant baselines — prior ZO-quantized methods are not compared"** → Kept but downgraded. The prior ZO-quantized methods are acknowledged as related work, and the paper's core comparison is against MeZO (the ZO baseline). The missing QLoRA comparison is the more consequential gap and is retained as Major.

2. **"The variance-reduction argument contains a mathematical error" — "Theorem 1 claims the clipped gradient estimate is unbiased — not generally true"** → Kept. The Eq. 8 derivation error is verifiable from the main text and is retained as Major. The Theorem 1 concern is noted but the proof is in the stripped appendix, so I focus on the verifiable derivation error.

3. **"No error bars or variance reporting across any result"** → Retained as Minor. Valid concern but common practice in this subfield (MeZO also reported single runs).

4. **"The 18× memory claim mixes incompatible comparisons"** → Retained as Minor. Disclosed but worth noting.

5. **"FLOPs comparison in Table 2 appears inconsistent"** → Retained as Major. Verifiable inconsistency.

6. **"the claim that QZO 'approximates the gradients of quantized weights' (line 36) is imprecise"** → Retained as Trivial.

7. **"Constrained ZO can affect convergence guarantees"** → Moved to Nice-to-Haves. Valid observation but not a flaw — it's part of the algorithm design.

8. **"Small dataset sizes"** → Removed. Follows MeZO convention and is a common practice in this literature.

9. **"Figure 3 shows standard gradient clipping behavior"** → Removed. The paper already frames this as an empirical observation; the criticism doesn't identify a specific error.

10. **"No comparison to QLoRA"** → Retained as Major. This is the single most important weakness.

## Novel Insights

The input review's most valuable observation is that QZO's perturbation mechanism effectively applies a *multiplicative* perturbation to all quantized weights in a group via the shared scale \( \Delta \). This is structurally different from perturbing individual weights and means QZO is learning per-group step sizes rather than per-weight updates. This insight frames QZO as closer to a learnable scaling mechanism than to traditional weight-space optimization. The observation that the optimization is inherently constrained (\( \Delta \ge 0 \)) — visible in Algorithm 1 but not discussed in the paper — is a genuine nuance that would merit analysis in a revision.

## Suggestions

1. **Add QLoRA as a baseline.** Even a single-task comparison (SST-2) at 4-bit would substantially improve the paper's practical relevance. Report memory usage, accuracy, and training time.

2. **Fix or reframe the DDC theoretical claims.** The second-moment reduction (Eq. 7) is valid; the variance reduction argument (Eq. 8) is not. Either provide a correct derivation of variance reduction under specific assumptions, or reframe DDC as a practical heuristic with empirical support (which Figure 2 already provides convincingly).

3. **Clarify the FLOPs calculation methodology** in Table 2. Explain what operations are counted (forward passes? perturbations? both?) and why the ratios differ so dramatically across model sizes.

4. **Report results over at least 3 random seeds** with mean and standard deviation, especially given the stochastic nature of ZO gradient estimation.

## Score and Decision

### Calibration Anchors

| Paper | Avg Score | Decision | Round | Comparison |
|-------|-----------|----------|-------|------------|
| Zeroth-Order Fine-Tuning of LLMs with Transferable Static Sparsity | 5.80 | Accept | R2 | Similar ZO+quantization scope; stronger experimental coverage but less novel core idea |
| SubZero: Random Subspace ZO | 4.25 | Reject | R1/R2 | ZO method with theory; rejected partly due to missing baselines — similar issue |
| Sparse MeZO | 5.50 | Reject | R2 | ZO sparsity method; solid results but limited novelty |
| Efficient Fine-Tuning of Quantized LLMs via Three-Stage Optimization | 5.40 | Reject | R2 | Quantized LLM fine-tuning; mixed reviews |
| HiZOO: Hessian Informed ZO | 5.67 | Accept | R2 | ZO with theory; accepted despite theoretical concerns |
| Simultaneous Computation and Memory Efficient ZO | 4.00 | Reject | R2 | ZO for LLMs; limited scope |

**Round 1 bracket:** 4.0 – 6.0 (based on similarity to ZO+quantization papers scoring 4.0–5.8)

**Round 2 narrowing:** The most comparable anchor (Transferable Static Sparsity, 5.80, Accept) has similar memory-efficiency goals but stronger experimental breadth. SubZero (4.25, Reject) and Sparse MeZO (5.50, Reject) show the scoring floor for ZO fine-tuning papers with evidential gaps. The QZO paper has a more novel core idea than any of these, but the missing QLoRA baseline, theoretical derivation error, and unclear FLOPs numbers are significant gaps that bring it below the accept threshold. The paper's contribution is real and fixable, warranting a score closer to the borderline than a strong reject.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>