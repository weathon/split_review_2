## Summary

This paper establishes that GPTQ, a widely-used post-training quantization method, is mathematically equivalent to Babai's nearest plane algorithm (without LLL basis reduction) when run in the reversed dimensional order. The equivalence is grounded in showing that the GPTQ optimization problem is an instance of the Closest Vector Problem on a lattice defined by the Hessian matrix, and that GPTQ's error propagation step coincides with Babai's hyperplane projection. From this connection, the paper imports Babai's error bound to obtain a layer-wise guarantee for GPTQ in the no-clipping setting (Theorem 5), and proposes two practical no-clipping variants (SSQR and HPTQ) with a CUDA inference kernel achieving ~2× speedup over PyTorch BF16.

## Strengths

- **Novel theoretical connection (Sections 4.1–4.4).** The core contribution — identifying GPTQ as Babai's nearest plane algorithm on the lattice defined by a Hessian factor — is genuinely non-obvious and intellectually interesting. The paper goes beyond prior high-level connections (QuIP/LDLQ) by pinpointing the exact algorithmic identity: GPTQ's error propagation corresponds to sequential hyperplane projection, and the L matrix from LDL decomposition encodes the Gram-Schmidt coefficients. Theorem 4 (GPTQ = Babai without basis reduction, when run in the same order) provides a clarifying geometric perspective on a widely-used algorithm and is the paper's strongest claim. [favorability=15.80]

- **Error bound with tightness guarantee (Theorem 5).** By importing Babai's bound, the paper obtains a layer-wise error guarantee for GPTQ in the no-clipping regime, stated as an explicit function of D from LDL decomposition and quantization scales. The bound is noted to be tight (attainable). Having a rigorous bound for GPTQ-type updates, even if limited to the no-clipping setting, is a theoretical improvement over purely empirical understanding. [favorability=13.24]

- **Principled design of no-clipping methods (Section 5).** SSQR and HPTQ are grounded in the theoretical analysis: they avoid clipping to inherit the error bound, and handle outliers through orthogonal mechanisms (sparse outlier storage for SSQR, Huffman coding for HPTQ). The CUDA kernel achieving ~2× speedup over PyTorch BF16 on the A6000 GPU (Figure 4c) is a practical contribution. [favorability=14.78]

- **Honest presentation of limitations.** The paper transparently acknowledges that the bound is without LLL reduction (Theorem 5), that min-pivot order yields only modest accuracy gains (Section 4.5), and that extending to clipped grids and basis reduction are future work (Section 6). This intellectual honesty is commendable. [favorability=13.13]

## Weaknesses

### Fatal
None.

### Major

- **Limited main-text experimental evidence.** The experimental section (Section 5, Figure 4) evaluates only one model family (Qwen3) on one dataset (WikiText-2). While additional results are deferred to the appendix, the main-text claims that the proposed methods "outperform the original GPTQ" rest on thin evidence. Perplexity values at low bitwidths (50–80) are far above the BF16 baseline (~11), and the zoomed inset makes margins at usable bitwidths hard to assess. For a paper that presents practical methods as part of its contribution and titles a section "Applications," the main-text validation is insufficient to fully support the practical claims. [favorability=-2.84]

### Minor

- **Practical force of the error bound is unclear.** The bound (Theorem 5) is imported from Babai's algorithm *without* LLL basis reduction. As the paper acknowledges, this bound can be exponentially large in the dimension for ill-conditioned Hessians, so it does not carry a practically meaningful approximation guarantee in general. The paper does not empirically investigate whether the bound is informative for real LLM layers (e.g., by computing the bound's right-hand side and comparing to empirical error). This limits the practical relevance of what is otherwise a clean theoretical result. [favorability=0.72]

- **The no-clipping methods conflate the theoretical contribution with engineering choices.** HPTQ combines GPTQ without clipping with Huffman encoding; SSQR combines it with sparse outlier storage. The comparison against standard (clipped) GPTQ cannot disentangle whether the gains come from the theoretically motivated no-clipping design or from the variable-length coding / outlier-handling mechanisms. While HRTN (Huffman + RTN) partially controls for Huffman, a cleaner ablation holding the representation scheme fixed would strengthen the paper. [favorability=4.12]

- **Some results are less substantive than presented.** (a) The "ineffectiveness of composing algorithms" (Section 4.3) follows trivially from Theorem 4: if GPTQ = Babai, then once Babai is done, GPTQ is done, so composition is identity. (b) The min-pivot order reduces tr(D) but accuracy gains are "modest," somewhat undermining its value as a proposed contribution. (c) Theorem 1 is a basic observation (inner products preserved under orthogonal transformation) presented as a theorem. [favorability=4.12–5.26]

### Trivial
None.

## Nice-to-Haves

1. An empirical investigation of whether the Babai bound (Theorem 5) has explanatory power on real LLM layers by computing its RHS and comparing to empirical error.
2. An ablation that holds the representation fixed (e.g., fixed 4-bit) and compares GPTQ with clipping vs. GPTQ without clipping under the same scale selection.
3. Reporting overhead analysis of Huffman decoding for HPTQ.
4. Moving key results from the appendix (zero-shot benchmarks, Llama results) to the main text.

## Removed Points

These points from the input review were evaluated and removed:
- "HPTQ vs GPTQ comparison structurally imbalanced" — removed because HPTQ beats both GPTQ (same rounding, different encoding) and HRTN (same encoding, different rounding), which together isolate both factors. The proposed baseline of "GPTQ without clipping + fixed-length coding" would require impractically large bitwidths and is not a meaningful comparison.
- "No error bars" — removed because single-run perplexity evaluation on fixed benchmarks is standard for LLM quantization.
- "Missing comparison with QuIP/QuIP#/AQLM in main text" — the paper cites QuIP in related work and the appendix covers these; the main text's scope is appropriately defined.
- Formatting/presentation nitpicks that are parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Move at least one additional model family (e.g., Llama) and one zero-shot benchmark result from the appendix into the main text to strengthen the practical claims.
2. Run a controlled experiment: compare GPTQ with clipping vs. GPTQ without clipping under identical representation (e.g., both with fixed 4-bit encoding) to isolate the effect of avoiding clipping.
3. Compute the Babai bound's RHS on real LLM layers and report whether it correlates with empirical quantization error — this would turn a theoretical curiosity into a practically informative result.

## Calibration Report

**All anchors retrieved (across rounds):**

| Path | Avg Score | Round | Itemized? | Comparison to this paper |
|------|-----------|-------|-----------|--------------------------|
| DiscQuant (`vJmpg0exYA.md`) | 4.50 | R1 | Yes | Closest match — theoretical connection (discrepancy theory) + practical method. Rejected due to assumption concerns and limited baselines. Our paper has cleaner theory (exact equivalence, no debatable assumptions) and no computational cost issues, justifying a higher score. |
| Pyramid VQ (`ZBlfjXubgG.md`) | 5.00 | R1 | Yes | Theoretical connection (spherical geometry) for quantization. Rejected on novelty/baseline concerns. Our paper's theoretical result is more concretely an exact algorithmic equivalence. |
| OSTQuant (`rAcgDBdKnP.md`) | 6.20 | R1 | Yes | Practical PTQ with theoretical metric (QSUR). Strong empirical validation across models. Our paper has weaker experiments but stronger theoretical novelty. |
| OmniQuant (`8Wuvhh0LYW.md`) | 6.40 | R1 | Yes | Practical learnable PTQ. Strong empirical results across settings. Our paper's theory is more novel but experiments are thinner. |
| PrefixQuant (`vw0NurJ7UX.md`) | 3.00 | R1 | Yes | Practical quantization paper. Rejected (all 3s) on novelty concerns. Our paper is substantially stronger. |
| CVXQ (`0T8vCKa7yu.md`) | 3.00 | R1 | Yes | Theoretical quantization approach. Rejected on practicality concerns. Our paper's theory is more solid. |

**Bracketing:** Round 1 bracketing placed the paper between 3.5 and 7.5. Removing the strong-reject band (all 1–1.4, papers with fatal flaws) and the top band (no papers in 8.5+), the paper's closest peers sat in the 4.5–6.4 range. Round 2 and 3 narrowed by comparing item-level favorability: our strengths (13–16) are stronger than DiscQuant's (8.7–14.4), but our major weakness (limited experiments, favorability -2.84) is a real drag that accepted practical papers (OSTQuant, OmniQuant) do not share. The paper thus sits above DiscQuant (4.50) but below the empirically strong accept papers (6.2–6.4).

**Final score: 6.0**. The theoretical insight (GPTQ = Babai) is the core contribution and is strong enough to warrant publication. However, the thin main-text experimental evidence and the unreduced-Babai bound's limited practical force prevent a higher score.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>