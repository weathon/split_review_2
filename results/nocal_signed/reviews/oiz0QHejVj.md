Now let me compose the final review.

## Summary

This paper proposes CLIP-Map, a parameter-efficient CLIP compression framework that replaces the conventional select-based pruning paradigm with a learnable mapping-based approach. Instead of measuring parameter importance and dropping low-ranking weights, CLIP-Map learns linear transformations (structured via Kronecker factorization) that combine original weights into a smaller representation. A Diagonal Inheritance Initialization scheme addresses optimization challenges from the Kronecker product's multiplicative variance. The method is evaluated on zero-shot image-text retrieval and classification benchmarks at various compression ratios.

## Strengths

- **Genuinely novel paradigm for CLIP compression.** Replacing weight selection (pruning) with learned linear mappings that *combine* original weights rather than dropping them is a real alternative to existing approaches, not an incremental modification. The paper correctly identifies that pruning methods (TinyCLIP, MoPE-CLIP) all operate on the same importance-ranking-then-dropping principle.

- **Kronecker factorization of the mapping matrix is technically clean and well-motivated (Sec. 3.2.2).** The mapping from ℝ^{D₁²} to ℝ^{D₂²} would require a dense matrix with O(D₁²D₂²) parameters. The Kronecker-structured mapping R = F^{in} ⊗ F^{out} reduces this to O(D₁D₂), and Eq. 4 (W' = F^{out} W F^{inT}) makes the semantics as input/output dimension transformations explicit.

- **Variance analysis motivating Diagonal Inheritance Initialization (Eq. 5–8) is mathematically sound.** The multiplicative variance of Kronecker products (Var(R) = σ_A² · σ_B²) is a genuine optimization challenge, and initializing diagonally to preserve identity-like behavior is a principled solution.

- **Results at extreme compression (1.0% in Table 1) are genuinely strong.** CLIP-Map_base at 0.84M params achieves 15.8 TR@1 on MSCOCO vs TinyCLIP's 10.5 (non-progressive) and 12.5 (progressive, 75 epochs) — a relative improvement of ~26–50% in the regime where pruning causes the most information loss.

## Weaknesses

### Major

- **Paper claims "consistently improved" but Table 4 shows a non-monotonic relationship.** The paper states (Sec. 4.3): "as the mapping stage is extended, the performance of the final compressed model is consistently improved." This is factually incorrect. Table 4 shows Manual Drop (0 mapping epochs) achieves 41.1% on IN-1K, while 0.28 epochs (39.7%) and 1 epoch (39.6%) are *worse*, and 7 epochs (40.8%) again underperforms Manual Drop. The mapping stage can actively hurt performance before becoming beneficial, and the effective operating window is narrow (3–5 epochs). The paper acknowledges degradation with "excessively long" mapping but does not reconcile this with the "consistently improved" claim.

- **Missing SVD/low-rank approximation baseline.** The method compresses weight matrices via W' = F^{out} W F^{inT} — a bilinear projection. SVD truncation of W to rank D₂ is the natural algebraic baseline for this type of transformation. Without it, readers cannot distinguish how much of the gain comes from the *learned optimization* of the F matrices versus the *linear transformation structure* itself. This baseline is conspicuously absent and would directly test the value added by learning.

- **Overclaiming at moderate compression.** The abstract and introduction claim the method "outperforms select-based frameworks across various compression ratios." At 50% compression (Table 1), CLIP-Map and TinyCLIP are essentially tied on MSCOCO (55.1 vs 54.9 TR@1), and TinyCLIP is notably better on several Flickr30K metrics (84.6 vs 81.9 TR@1, 96.7 vs 96.2 TR@5). The paper's language should be calibrated to acknowledge that the method's advantage is largest at extreme compression (≤10%) and diminishes at moderate ratios.

### Minor

- **The initialization ablation (Table 5) reports mapping-stage-only performance, not post-retraining.** Diagonal Init achieves 28.9% IN-1K vs Kaiming's 4.4% after the mapping stage — but this largely reflects that the identity-like initialization preserves usable weights while random init produces garbage. A post-retraining comparison across all initialization methods would isolate whether *optimizing* the F matrices adds value beyond the *initialization* strategy itself. Table 4 partially addresses this (Manual Drop + retraining vs. learned mapping + retraining) but the gain is modest (~1 point on IN-1K).

- **Large per-dataset performance swings in Table 2 are unexplained.** At the base scale (39+19M), CLIP-Map substantially outperforms TinyCLIP on Stanford Cars (69.2 vs 51.7) and FCVC Aircraft (50.8 vs 15.7), but is dramatically worse on VOC2007 (22.2 vs 76.0). The paper presents these without analysis, making it unclear whether the method's behavior is consistent or uneven across domains.

- **The Meta-CLIP variant at 10% compression (Table 1) achieves 34.3 TR@1 — substantially below the OpenCLIP variant's 38.4.** The paper reports this without discussion, leaving questions about sensitivity to the base model's training data distribution.

### Trivial

- **Off-diagonal initialization is ambiguous.** The text says "set the off-diagonal elements to zero *or* small random values," but Eq. 9 specifies exactly zero. This affects initial gradient behavior.

- **The "fewer training epochs" claim (Sec. 4.2, Conclusion) is accurate against progressive TinyCLIP but incomplete.** Against non-progressive TinyCLIP (25 epochs), CLIP-Map uses the same 25 total epochs. Additionally, each mapping-stage epoch processes the full uncompressed model, so per-epoch FLOP cost differs from training a compressed model. A total FLOP comparison would be more informative.

## Nice-to-Haves

- Compare diagonal init (without optimization) → full retraining vs. learned mapping → full retraining to directly isolate the value of optimization.
- Discuss the non-monotonic behavior in Table 4 — why short mapping durations hurt and whether this reflects a convergence phenomenon where optimization temporarily destroys the good initialization.
- Analyze the Meta-CLIP degradation and large per-dataset swings.

## Removed Points

These points were removed per filtering rules:
- "CLIP (Wu et al., 2023) row appears twice in Table 1": Factually misidentified — the duplicate entries are CLIP (Radford et al., 2021), not CLIP (Wu et al., 2023). May reflect different evaluation protocols. Removed.
- "λ hyperparameter not reported in main text": Value is in the appendix, which the parser strips. Per rule: appendix-deferred details are not paper errors.
- "No inference-time FLOP or latency analysis": Scope creep for a parameter-reduction paper. Removed.
- Various generic presentation nitpicks and speculative confound concerns: Removed per filtering discipline.

## Novel Insights

The harsh critic's observation that the ablation study reveals non-monotonic behavior (short mapping hurts, moderate helps, too much hurts) is worth emphasizing beyond what the paper itself articulates. This is an informative empirical finding about the optimization landscape of Kronecker-structured mappings — the optimization temporarily destroys the good diagonal initialization before converging to a better solution, which reveals something about the loss geometry. The paper could strengthen itself by analyzing this phenomenon rather than glossing over it with the inaccurate "consistently improved" claim.

## Suggestions

1. Fix the "consistently improved" claim to honestly describe the non-monotonic relationship in Table 4.
2. Add SVD truncation as a baseline to isolate whether learning adds value over algebraic compression.
3. Add a post-retraining comparison across all initialization methods (Random, Kaiming, Xavier, Diagonal).
4. Calibrate claims to match evidence: the method's advantage is clearest at extreme compression (≤10%), not uniformly across all ratios.
5. Analyze large per-dataset swings (VOC2007, Aircraft) and the Meta-CLIP degradation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>