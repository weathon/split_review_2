Now I have everything I need. Let me compile the final authoritative review.

## Summary

This paper proposes PKA (Patch-wise and Keyword-Aware Attention), a framework for efficient multi-condition control in Diffusion Transformers. It replaces the "concatenate-and-attend" strategy with two specialized modules: Position-Aligned Attention (PAA) for spatial-aligned conditions and Keyword-Scoped Attention (KSA) for subject-driven conditions. Combined with a Condition Cache and an early-timestep sampling strategy for training, PKA achieves up to 10× inference speedup and 5.12× VRAM reduction in the attention module.

## Strengths

1. **Well-motivated problem with diagnostic evidence.** The paper provides empirical analysis (Figures 2, 3) showing that attention in multi-condition DiTs is sparse in predictable ways — diagonally concentrated for spatial conditions and locally concentrated for subject conditions. This grounds the method design in observed properties of the system, not arbitrary heuristics.

2. **Substantial and well-documented efficiency gains.** The efficiency results (Figures 7, 8) are the paper's strongest contribution. The 3.90×–10× speedup and 2.46×–5.12× VRAM reduction with clean scaling trends across 1–16 conditions are operationally meaningful. The internal ablation (Figure 9: PAA vs. Sliding Window Attention vs. full attention) confirms the architectural benefit within a controlled setting, showing PAA achieves 13.63s/237MB vs. 15.38s/308MB for full attention.

3. **Clean conceptual decomposition.** Separating conditions into spatial-aligned (handled by PAA) and subject-driven (handled by KSA) follows naturally from the observed sparsity patterns. The two-module design is intuitive and clearly communicated (Figure 4).

## Weaknesses

### Major

1. **Baseline fine-tuning status is unspecified, undermining quality comparisons.** Section 4.1 states: "To ensure a fair comparison, we fine-tune the FLUX.1 model using LoRA." This sentence describes what the authors did for their own model. The paper does **not** state whether OminiControl2 and UniCombine were also fine-tuned on the same Subject200K subset with the same LoRA procedure, or whether they were used from released checkpoints without in-domain adaptation. If the latter, every quality metric in Table 1 (FID, SSIM, CLIP-I, DINOv2) is confounded: the FID improvements — e.g., 52.99 vs. 61.03 on Subject-Canny — could partly reflect training distribution mismatch rather than architectural superiority. The efficiency comparisons are unaffected, but the claim that PKA "maintains or improves generative quality" depends on a fair quality evaluation. The authors must clarify this in rebuttal.

2. **PAA's mathematical formulation does not perform attention — the Softmax of a single scalar degenerates to a no-op.** Equation (2) defines PAA([X; SP])[i] = Softmax(Q_{X,i} K_{SP,i}^⊤ / √d) V_{SP,i}, where Q_{X,i} is a single query vector and K_{SP,i} is a single key vector. Their dot product is a scalar; softmax of a single scalar is always 1, regardless of the input. Therefore PAA does not perform token mixing, selection, or weighting — it directly copies V_{SP,i} to the output at position i. This is functionally equivalent to a feature pass-through, not attention. The paper calls it "one-to-one attention computation" and claims it "enables highly localized control," which mischaracterizes the operation. The O(N²)→O(N) complexity reduction claim is technically correct but the "attention" being replaced is already a degenerate case. This does not necessarily mean the method is ineffective (the value injection may still work), but the formalism is misleading and should be corrected.

### Minor

3. **Quality evaluation is limited to 2-condition tasks, while efficiency claims scale to 16 conditions.** Table 1 evaluates three tasks (Subject-Canny, Subject-Depth, Canny-Depth), each with exactly two conditions. The efficiency plots (Figures 7, 8) go up to 16 conditions, and the abstract claims quality is "maintained or improved" in multi-condition settings. Without quality measurements at higher condition counts (e.g., 4, 8, or 16 conditions), it is unknown whether the sparse approximations in PAA and KSA accumulate errors or cause condition conflicts as conditions increase. This creates a gap between the efficiency and quality claims.

4. **Early-timestep sampling contribution lacks quantitative validation.** Figure 11 provides a qualitative comparison across different (μ, δ) settings, but no quantitative metric (FID, CLIP-I, SSIM, or any metric from Table 1) is reported to support the claimed benefits. The specific μ and δ values used in experiments are also not reported (only "μ > 0, δ > 1" is stated). This is a secondary contribution, but the absence of numbers weakens it.

5. **Condition Cache is not ablated separately.** The paper describes a caching mechanism (Section 3.2) where condition tokens' K/V projections are computed once and reused across all denoising steps. This is a substantial source of speedup. Yet the ablations (Figures 9, 10) always include the cache alongside PAA/KSA, making it impossible to attribute the speedup between architectural sparsity (PAA/KSA) and the caching strategy. Since caching is an orthogonal engineering optimization unrelated to the paper's core insight about sparsity, this breakdown would meaningfully clarify the contribution.

6. **Mischaracterization of the F1 gap on Subject-Canny.** The paper describes the F1 score (0.414 vs. UniCombine's 0.551, a ~25% relative drop) as "a narrow margin" (line 249). This understates the controllability gap for edge conditions. While our method leads on all other metrics for this task (FID, SSIM, CLIP-I, DINOv2), the F1 drop should be acknowledged more candidly.

### Trivial

7. No statistical significance or variance is reported for any metric in Table 1, which matters given the modest dataset size.
8. The image resolution, number of denoising steps, and exact training/testing split sizes are not reported in Section 4.1.
9. The paper does not discuss scenarios with multiple conditions of the same type (e.g., two subject conditions or two spatial conditions).

## Nice-to-Haves

- Quantify quality at 4- and 8-condition settings to directly test whether sparse approximations degrade as conditions accumulate.
- Ablate the Condition Cache separately (report speedup/VRAM of full attention, PAA+KSA without cache, and PAA+KSA with cache).
- Report the specific μ and δ values used for the early-timestep sampling.
- Provide quantitative controllability metrics (F1, MSE) for the KSA ε threshold ablation across values.

## Removed Points

These points were considered but removed from the main review (and should be treated with caution):

- *"PAA tested only on dense spatial conditions (canny, depth) but not on sparse/semantic conditions (bounding boxes, segmentation maps)"* — The paper scopes itself to dense spatial conditions and the two evaluated types are standard in this domain. This is scope-appropriate, not a weakness.
- *"No analysis of when KSA's temporal consistency approximation fails"* — A reasonable suggestion for strengthening but not a core weakness; the paper cites prior work on temporal consistency.
- *"Speedup comparison conflates implementation differences"* — The internal ablation (Figure 9) validates efficiency within a controlled setting, mitigating this concern.
- *"FID values are unusually high (52–80)"* — This is an observation without clear baseline reference; comparison is relative and consistent across methods.
- *"Missing related work on token merging/pruning"* — The paper already discusses OminiControl2 (dynamic token pruning) and other efficient mechanisms.
- *"The paper does not discuss what happens when multiple conditions of same type are used"* — This falls outside the paper's stated scope.
- *"Reproducibility concerns about undisclosed hyperparameters"* — Most key details are provided; the specific μ/δ values are a minor omission noted in the review.

## Novel Insights

None beyond the paper's own contributions. The review's observation about PAA's softmax-of-scalar degeneracy is a mathematical correction to the paper's framing rather than a novel scientific insight. The baseline-comparison fairness concern is a standard evaluation verification point.

## Suggestions

- In the rebuttal, explicitly clarify whether OminiControl2 and UniCombine were fine-tuned on the same Subject200K subset under identical LoRA conditions, or used from pre-trained checkpoints. If the latter, clearly discuss this limitation and present the quality results as preliminary.
- Rewrite Equation (2) to accurately describe PAA as aligned value injection rather than attention, or reformulate to include a local neighborhood of key positions per query (e.g., a 3×3 window) so that the softmax is non-degenerate.
- Add quality evaluation at higher condition counts (4, 8, 16) for at least one task to close the efficiency-quality scope gap.
- Add an ablation separating the Condition Cache contribution from PAA/KSA's architectural contribution.
- Report variance/confidence intervals for Table 1 metrics.

## Calibration Anchors

The following anchors from the human-review corpus were used to calibrate this score:

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| D2as3jDmRA (LinFusion) | 6.25 | 1 | Yes | Proposes linear attention for diffusion efficiency. Stronger experimental validation across multiple models/resolutions. PKA is weaker due to baseline comparison uncertainty and PAA formalism issue. |
| lTrrnNdkOX (PT-DiT) | 6.40 | 1 | Yes | Proxy-tokenized attention for DiT. Tests across T2I, T2V, T2MV; called "incremental" by one reviewer. PKA has cleaner motivation but less comprehensive evaluation. |
| Jt1gGIumJo (Highlight Diffusion) | 3.00 | 1 | Yes | Attention-guided acceleration for T2I. Only 1.52× speedup; narrow applicability. PKA clearly stronger (10× speedup, better motivation). |
| taHwqSrbrb (DyDiT) | 5.50 | 2 | Yes | Dynamic computation in DiT. Extensive experiments. PKA has cleaner conceptual contribution but weaker experiments. |
| leBbjaUxut (MDiT) | 5.00 | 2 | Yes | Multi-scale DiT with training speedup. Mixed reviews (3,3,6,8); called "incremental engineering." Similar profile to PKA. |
| uJqKf24HGN (UniCon) | 7.00 | 2 | Yes | Unidirectional flow for DiT control adapters. Cleaner, more comprehensive evaluation. PKA is substantially weaker. |

**Bracket rationale (Round 1):** PKA is clearly above the 3.00-level (Highlight Diffusion) due to 10× speedup, better motivation, and cleaner design. It is below the 6.0+ level (LinFusion, PT-DiT) due to the baseline comparison uncertainty, PAA formalism issue, and narrower experimental validation. This places PKA in the 4.0–5.5 range.

**Narrowing (Round 2):** Compared to DyDiT (5.50) and MDiT (5.00), PKA has a cleaner conceptual decomposition but weaker experimental rigor. The baseline comparison concern and PAA mischaracterization are heavier weaknesses than those found in DyDiT. PKA sits closest to MDiT (5.00) in overall quality — both have genuine contributions undermined by incomplete experimental validation.

Shared heavy-weight items (positive): Substantial efficiency gains (+3 in LinFusion, +4 in DyDiT); clear motivation (+2 in DyDiT). Missing heavy-weight items (negative): PKA lacks the "extensive experiments and thorough ablation" (+3 in DyDiT) and "sufficient ablation studies" (+4 in DyDiT) that lifted those papers. PKA uniquely carries the baseline-comparison uncertainty and PAA formalism issue.

**Final score: 4.5** — The paper has a genuine efficiency contribution (10× speedup is impressive) and a clean conceptual decomposition, but the baseline comparison uncertainty and the misleading PAA formalism are significant concerns that prevent acceptance at the current level of experimental rigor. With major revisions addressing these issues, the paper could be a 6+.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>