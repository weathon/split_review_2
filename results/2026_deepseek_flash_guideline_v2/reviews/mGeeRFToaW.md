The calibration search is not working due to a path issue. I'll proceed based on my own analysis, carefully weighing the paper's merits against the verified weaknesses.

Let me now produce the final consolidated review.

## Summary
The paper proposes Quantized Zeroth-order Optimization (QZO), which enables fine-tuning of quantized LLMs by applying zeroth-order optimization to the continuous quantization scale parameters (Δ) rather than to discrete quantized weights. The core technical contribution is Q-SPSA (Definition 3.3), which perturbs Δ while keeping discrete weights fixed, and Directional Derivative Clipping (DDC) for training stability. The paper demonstrates an 18× memory reduction over 16-bit full fine-tuning and shows that QZO can fine-tune 4-bit LLMs on par with MeZO (which uses 16-bit un-quantized models) while using ~3× less memory.

## Strengths
1. **Clean technical solution to a non-trivial problem.** Perturbing the continuous quantization scale Δ (Q-SPSA, Definition 3.3) instead of discrete quantized weights elegantly avoids the de-quantization/re-quantization overhead required by prior ZO-for-quantized-models approaches that perturb discrete weights directly (Section 2). This is a simple, well-motivated, and novel modification of SPSA.

2. **Substantial and well-measured memory reduction.** Per-model profiling (Figure 1/Table 1) shows consistent ~18× memory reduction across three model sizes: OPT-6.7B (4.8GB vs 87.6GB), Llama-2-7B (5.0GB vs 92.2GB), and Llama-3.1-8B (6.2GB vs 113.7GB). These concrete numbers directly and reliably substantiate the paper's central claim.

3. **Empirical evidence that DDC is necessary for training stability.** Figure 2 convincingly shows that without DDC, training collapses to NaN at step 22, while with DDC it remains stable over 1,000 steps. Figure 3 shows robustness across a range of clipping thresholds (C=75–150), providing practical guidance for the hyperparameter.

4. **Generality across quantization paradigms.** QZO works with both scalar-based (GPTQ, 4-bit) and codebook-based (AQLM, 2-bit) quantization methods, including the challenging 2-bit setting on Llama-2-13B within a single 24GB GPU (Table 3). This demonstrates applicability beyond the typical 4-bit setting.

## Weaknesses

### Fatal
None.

### Major

1. **Theorem 1 (unbiasedness of the clipped gradient estimate) is not credible as stated, which undermines the theoretical justification for DDC.** Theorem 1 claims that the clipped gradient estimate ∇̂' = d'·z (where d' = clip(d, -C, C)) is unbiased. Since d ≈ z^T ∇_Δ L, the directional derivative d and the random vector z are correlated. Clipping d to [-C, C] therefore changes the expectation of their product in a way that generally introduces bias (e.g., in the 1D case, E[clip(gz, -C, C)·z] ≠ E[gz²] = g for any finite C). The variance reduction derivation in Eq. 7–8 depends on this unbiasedness to replace E[‖∇̂'‖]² with ‖∇L‖²; without it, the derivation is invalid. The paper's proof is relegated to the appendix (which is stripped by the PDF parser and thus not accessible in the review), so it is impossible to verify whether some non-obvious assumption rescues the claim. The strong empirical evidence for DDC (Figure 2) stands on its own, but the theoretical framing must be corrected or removed.

2. **Missing comparison to QLoRA (Dettmers et al., 2023), the most widely used method for fine-tuning quantized LLMs.** QLoRA is cited in the references but never mentioned in the experimental design or compared against. The paper claims to address "fine-tuning quantized neural networks," yet a reader cannot assess whether QZO's trade-off (eliminating gradients/optimizer states entirely vs. using LoRA adapters with backprop) is practically competitive at similar memory budgets. Even if a strict apples-to-apples memory comparison is non-trivial (QLoRA uses backprop, QZO uses ZO), the absence of any comparison is a significant gap in evaluation.

3. **No empirical comparison to prior ZO-for-quantized-models methods** (Feng et al., 2024; Zhou et al., 2025; Bar & Giryes, 2025) described in Section 2. The paper asserts QZO is "inherently more efficient and flexible" than these approaches but provides no experimental evidence. Without this comparison, the claimed advantage over prior work in this specific sub-area is an assertion, not a finding.

### Minor

1. **FLOPs comparison in Table 2 lacks methodological transparency.** The ratio of QZO FLOPs to MeZO FLOPs varies dramatically across models: from ~0.008% (OPT-6.7B, a 12,000× gap) to ~7% (Llama-3.1-8B, a 14× gap). Since both methods perform two forward passes per optimization step through the same model architecture (for OPT and Llama-2-7B both are 7B-class models), the forward-pass FLOPs should dominate and be similar. The paper does not explain how FLOPs are calculated, making the numbers difficult to interpret or trust.

2. **Asymmetric baselines: performance comparison uses SGD, memory comparison uses AdamW.** The headline 18× memory reduction (Figure 1) compares QZO (4-bit) against AdamW fine-tuning (16-bit). However, the performance "upper bound" in Table 1 uses SGD (Footnote 2: "Due to limited budget on computational resources, fine-tuning experiments are conducted with SGD optimizer"). Since AdamW is known to outperform SGD for LLM fine-tuning, the true gap between QZO and a properly-tuned upper bound is likely larger than reported. This asymmetry inflates the apparent competitiveness of QZO.

3. **Weights quantized to zero are effectively unfine-tunable via QZO, a limitation not acknowledged.** By the chain rule applied to w = Δ·w̄, we have ∂L/∂Δ = w̄·∂L/∂w. When w̄ = 0 (which is common in GPTQ for weights near zero), the gradient w.r.t. Δ is zero regardless of the true gradient, making those parameters unfine-tunable. Since QZO estimates ∇_Δ L via SPSA on Δ, the same issue applies: perturbing Δ_i does not change the output when w̄_i = 0.

4. **No statistical significance or variance information.** All results appear to be single runs without standard errors or confidence intervals. Given the stochastic nature of ZO methods, this makes it difficult to assess whether reported differences (e.g., QZO's 69.6 vs MeZO's 91.1 on CB with Llama-3.1-8B) are meaningful or within noise.

5. **The 2-bit experiment (Table 3) has no fine-tuning baseline** (neither MeZO nor SGD fine-tuning on Llama-2-13B), so the only comparison is against the zero-shot quantized model. While the improvement from 57.6% → 80.5% on SST-2 is notable, it is unclear how this compares to even a minimal fine-tuning baseline.

### Trivial
None.

## Nice-to-Haves
- Wall-clock time comparison with MeZO and QLoRA to assess the practical trade-off beyond memory.
- An ablation study randomizing Δ updates (e.g., using random perturbations) to confirm that improvements come from task-specific adaptation rather than general calibration effects.
- Memory profiling during full training (not just the first 100 steps).

## Removed Points
The following points raised by reviewers were removed as they do not meet the threshold for inclusion:

- **Harsh Critic's claim that the paper "cannot be accepted because we do not know whether QZO actually advances the state of the art"**: Overly strong framing. The paper does advance the state of the art relative to MeZO (same paradigm, lower memory) even without QLoRA comparison. The missing comparison is a weakness but not fatal.
- **Harsh Critic's point about the chain-rule gradient dependence on w̄ being a "subtle issue" in the methodology section**: Kept as Minor weakness 3 (zero-weight limitation) but reformulated more precisely.
- **Strength Finder's claim that DDC is "theoretically grounded"**: This conflicts with the verified weakness about Theorem 1. The empirical support is strong, but the theory is flawed. Removed the "theoretically grounded" characterization.
- **Strength Finder's claim about "dramatically lower computation cost"**: Overstated given the FLOPs transparency issue (Minor weakness 1). Modified to focus on memory savings only.
- **Harsh Critic's criticism about statistical significance**: Kept as Minor weakness 4, though this is a common issue in LLM fine-tuning papers.

## Novel Insights
None beyond the paper's own contributions. The core insight of perturbing quantization scales rather than discrete weights is already clearly articulated by the authors.

## Suggestions
1. Correct or remove Theorem 1. The empirical DDC results are compelling on their own and do not need a questionable theoretical scaffold. If a corrected proof exists in the appendix, state the necessary assumptions explicitly in the main text.
2. Add at least one comparison to QLoRA at a similar memory budget to establish practical relevance.
3. Add experimental comparison to at least one prior ZO-for-quantized-models method (Feng et al., 2024; Bar & Giryes, 2025) on a subset of tasks.
4. Provide a clear methodology for FLOPs calculation in Table 2, or report forward-pass and update FLOPs separately.
5. Acknowledge the zero-weight limitation explicitly in Section 5 (Limitations).
6. Report results with variance estimates (multiple seeds or bootstrap confidence intervals) for key comparisons.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>