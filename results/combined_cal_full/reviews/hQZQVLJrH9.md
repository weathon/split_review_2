Now I have all the information I need. Here is my final consolidated review.

---

## Summary

This paper proves that activation steering and influence functions are, to first order, mathematically equivalent: any steering vector can be represented as an influence weighting over training data, and vice versa. The framework yields an Influence-Aligned Steering (IAS) vector construction, a geometric diagnostic (γ) that quantifies when steering can reproduce weight-space effects, generalization bounds for low-rank steering, and a spectral optimality result for steering directions. The core contribution is a clean theoretical unification of two previously disconnected strands of interpretability research.

## Strengths

- **The core theoretical insight — that activation steering and influence functions are first-order duals governed by subspace alignment — is a genuinely novel unification of two previously disconnected literatures.** The paper identifies a real gap and provides a clean mathematical framework connecting them. This alone makes the paper worth engaging with.

- **The γ diagnostic (the cosine of the smallest principal angle between Jacobian subspaces) is a principled, computable quantity with a clear geometric interpretation.** It provides a practical answer to when steering can reproduce weight-space updates, backed by a no-free-lunch bound when alignment is poor. This is the paper's strongest theoretical contribution.

- **The computational primitives for the IAS construction are honestly scoped: given a target logit displacement, computing the optimal steering vector requires only Jacobian-vector products and a rank-d pseudoinverse (two backward passes).** The paper is transparent about what the steering-side computation costs.

## Weaknesses

### Major

1. **The paper's most practically impactful claim — that ρₛ maps steering vectors back to causal training examples (Corollary 1) — is never empirically validated.** The paper states "see Section 7" for this validation, but Section 7 contains no experiment demonstrating that ρₛ identifies meaningful training examples, that the attribution outperforms simpler baselines (e.g., gradient-based attribution, TracIn), or that the top-weighted examples are causally relevant. This is a critical gap between claimed contribution and provided evidence. The theoretical construction is sound, but the paper presents this as a headline practical contribution without any supporting experiment.

2. **IAS underperforms the baseline CAA on the paper's own main task (detoxification).** Table 1 shows IAS achieves worse toxicity (0.0164 vs. 0.0150) and worse perplexity (13701 vs. 13291) than Contrastive Activation Addition, under identical ℓ₂ magnitude and layer. No error bars, confidence intervals, or significance tests are reported, making the comparison uninterpretable. While the theoretical contribution does not require beating baselines, the empirical case for using IAS rather than existing methods is absent.

3. **The cost model systematically understates the computational burden of the full steer→trace→edit workflow.** The "two backward passes" claim covers only computing the IAS vector from a given parameter perturbation Δθ. However, obtaining Δθ itself requires solving Δθ_ε = −ε 𝐇_θ⁻¹ ∇_θ ℓ(z, θ), which involves inverting or approximating the P×P empirical Hessian (or its Gauss-Newton surrogate). For models with hundreds of millions of parameters, this is the dominant cost, yet it is not counted in the paper's advertised complexity. The paper mentions damped Gauss-Newton surrogates and Tikhonov regularization, but does not acknowledge that the influence-function side inherits the well-documented computational and numerical difficulties of Hessian-based methods (Basu et al., 2021). This undermines the claimed "practical workflow" where one would "steer first, trace provenance, edit only when needed."

### Minor

4. **The first-order linearity experiment (Section 7.2, Figure 1) shows a systematic bias: the fitted slope is 1.50, not 1.0.** The actual logit shift is 50% larger than the first-order prediction. While the high cosine (0.978) confirms directional alignment, the magnitude discrepancy is substantial and the paper does not attempt to explain it beyond calling it "consistent with the expected linear regime." For a paper whose central claim is first-order equivalence, this warrants analysis or at least discussion.

5. **The proof sketch for Corollary 1 (minimal ℓ₁ measure) is unconvincing as stated.** The argument claims that if another measure ν had smaller ℓ₁ norm, "one could scale ρₛ down and still match the shift, contradicting the definition of α as the steering magnitude." Scaling ρₛ down would change the logit shift proportionally, so it would no longer match the target shift. The argument as written does not establish minimality.

6. **Equation (2) in Section 3.2 contains a mathematical error.** The expression Δh* = 𝐉_{h→y}ᵀ 𝐉_{θ→y} Δθ is missing the pseudoinverse factor (𝐉_{h→y}𝐉_{h→y}ᵀ)†. The correct expression is 𝐉_{h→y}† 𝐉_{θ→y} Δθ, which is correctly given later in Theorem 5.2. While a careful reader can infer the intended formula, the inconsistency in the paper's central derivational equation undermines confidence.

7. **The spectral optimality experiment (Section 7.4, ResNet-50 on ImageNet) demonstrates that the spectral direction is statistically significant vs. random directions (p=0.005), but does not report what the steering direction actually accomplishes** — e.g., how much the horse logit changes, at what cost to other classes, or how it compares to existing steering methods like CAA or activation maximization. The random-direction null is a weak baseline.

## Nice-to-Haves

- Adding a small-scale validation experiment for ρₛ (e.g., on a synthetic dataset with known ground-truth influence, or testing whether the most-weighted examples are causally connected to the steering behavior) would substantially strengthen the paper's practical claims.
- Providing error bars or significance tests for Table 1.
- An ablation of the rank parameter k in the generalization bound (Theorem 6.1), despite its stated importance.
- Experiments on larger models (e.g., LLaMA-7B) would better support the paper's claims about scalability to "billion-parameter models."

## Removed Points

- **"Wrong sign" claim in Eq. (2):** The sign is consistent across the derivation and Theorem 5.2; the actual error is the missing pseudoinverse factor, not the sign.
- **"Does not acknowledge" the slope 1.50:** The paper directly reports slope 1.50 in both text and figure, so it is acknowledged. The valid criticism is that it is not *explained*.
- **"Optimal-control perspective is standard Lagrangian dual":** This is a framing preference, not a substantive error. The paper does not claim novelty in the optimization technique itself.
- **Missing experiments on LLaMA/Mistral-7B:** GPT-2 Medium (350M params) is a standard model for interpretability research; scaling to larger models is a reasonable future direction but not a required experiment.
- **Various section-by-section presentation notes** (notation overloading, Theorem 6.2 being "essentially a restatement"): These are presentation-level observations that do not undermine the paper's contributions.
- **Missing rank-k ablation:** A reasonable suggestion but not a core weakness given the paper's main contributions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a small-scale validation experiment for ρₛ — even on a synthetic dataset or controlled setting with known ground-truth influence.
2. Acknowledge the full cost of Hessian-based computation when the workflow involves the influence→steering direction, and clarify which operations the "two backward passes" cost model covers.
3. Provide error bars or significance tests for Table 1.
4. Analyze or at least discuss the slope 1.50 discrepancy in Figure 1 — is it due to second-order effects, specific layer choice, or the linear approximation breaking systematically?
5. Fix the error in Eq. (2) to match the correct expression in Theorem 5.2 and fix the proof sketch of Corollary 1.

---

## Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `9wjGUN65tY.md` — "From Steering Vectors to Conceptors and Beyond" | 5.00 | R1 | Yes | Similar topic (steering theory), stronger empirical validation (baseline comparisons, error bars on some metrics), but also has incremental-advantage concerns. Our paper has stronger theoretical novelty (unification of two fields) but weaker empirics. |
| `2XBPdPIcFK.md` — "Steering Language Models with Activation Engineering" | 5.00 | R1 | Yes | The original CAA paper; stronger experimental validation across multiple models/tasks but less theoretical depth. Our paper makes a different type of contribution. |
| `z1yI8uoVU3.md` — "Measuring Effects of Steered Representation in LLMs" | 3.00 | R1 | No | About evaluating steering effects, narrower contribution than our paper. |
| `wozhdnRCtw.md` — "Improving Instruction-Following through Activation Steering" | 7.00 | R1 | Yes | Comprehensive experiments, clear practical value, but less theoretical depth. A stronger empirical paper. |
| `uHLgDEgiS5.md` — "Capturing Temporal Dependence of Training Data Influence" | 8.00 | R1 | Yes | Strong influence-function theory paper with thorough empirical validation; sets the bar for what a theory+empirics paper in this area should achieve. |
| `Gl4AsqInti.md` — "How Hessian structure explains mysteries in sharpness regularization" | 4.75 | R2 | No | Theory-heavy paper with similar score; our paper's empirical gaps are more significant. |
| `KjBG4JNOc2.md` — "Enhancing Training Robustness through Influence Measure" | 6.20 | R2 | No | Influence-function paper with comprehensive empirical validation; our paper lacks this level of support. |

**Round-1 bracket:** [4.0, 5.5] — comparable to the conceptor paper (5.00) but pulled down by heavier negative-weighted items (ρₛ unvalidated at -5.65, IAS vs CAA at -6.60). Our draft's strongest positive items (+4.56, +4.50, +3.90) are competitive, but the two heaviest negatives have no positive counterweight of comparable magnitude. The conceptor paper's weighted items net out near zero; ours net out clearly negative, placing this paper below 5.00 but not as low as 3.00-range papers (which lack the theoretical novelty).

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>