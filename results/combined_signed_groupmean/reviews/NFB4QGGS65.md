Now I have sufficient calibration data. Let me write the final consolidated review.

**Calibration Summary:**
- **Round 1 bracket (all bands searched):** The most relevant anchors were DiscQuant (4.50, theory→algorithm, weak baselines), SPFQ (4.25, theory-heavy, weak experiments), PVQ for LLMs (5.00, theory+practice, mixed reviews), and RIQ (5.25, theory+experiments, questioned novelty). 
- **Round 2 (4.0-6.0 narrow search):** Confirmed DiscQuant (4.50), SPFQ (4.25), RIQ (5.25) as closest peers.
- **Placing the paper:** The current paper has a more novel theoretical insight than DiscQuant or RIQ (the Babai connection is genuinely surprising and non-obvious). However, it has a larger gap between theory and experiments: DiscQuant at least empirically tests its assumptions (low-rank gradients), whereas this paper runs no experiment that validates the theoretical predictions (no order comparison, no bound verification, no clipping ablation). The paper's strengths align with DiscQuant's (genuinely novel theoretical framing), and its weaknesses are worse than DiscQuant's on theory-experiment alignment. Thus the paper sits between DiscQuant (4.50) and the stronger PVQ/RIQ papers (~5.0-5.25), at **5.0**.

**Final score: 5.0, Decision: Reject**

Now writing the review.

---

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses
### Fatal
None.

### Major
- weakness 1
- weakness 2

### Minor
- weakness 1

### Trivial
None.

## Nice-to-Haves
- suggestion

## Removed Points
...

## Novel Insights
...

## Suggestions
...

## Score and Decision
MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>## Summary

This paper establishes a formal connection between GPTQ (a popular LLM post-training quantization algorithm) and Babai's nearest plane algorithm for the closest vector problem (CVP) on a lattice defined by the Hessian. It shows that GPTQ executed back-to-front is mathematically identical to Babai's algorithm without LLL reduction, and derives an error bound from Babai's bound. The paper then proposes practical no-clipping quantization methods (SSQR, HPTQ) motivated by this theory, together with efficient GPU inference kernels.

## Strengths

- **A genuinely novel cross-field connection** (Theorem 4, Table 1). Identifying GPTQ's error propagation with Babai's nearest plane heuristic is non-obvious and opens a two-way channel between quantization and lattice algorithms. This is the paper's real contribution and it is meaningful.

- **Clear geometric interpretation of the error propagation step** (Section 4.2, Theorem 2). The paper explains *why* the GPTQ update formula (Eq. 2) is a projection onto a hyperplane, with inverse Hessian entries giving the geometry. This is a genuine pedagogical advance over the original GPTQ paper.

- **The error bound (Theorem 5) is a well-structured consequence** of the equivalence. The bound's expression in terms of the LDL diagonal matrix D and scales s_i is clean, and the observation that expected error under uniform weights is 1/3 of the worst-case (Section D.2) adds useful nuance.

- **The min-pivot ordering heuristic** (Algorithm 3) and its geometric interpretation (Gram-Schmidt always taking the shortest residual) are principled contributions derived from the theory.

## Weaknesses

### Major

- **The equivalence covers a differently ordered variant, not the algorithm as used in practice.** Theorem 4 requires GPTQ to run back-to-front (last to first dimension), while standard GPTQ runs front-to-back (Algorithm 1, line 5: `j ← 1 to c`). The paper calls this a "superficial difference" (line 187) but Section 4.5 shows that quantization order materially affects the error bound — the bound is sensitive to the LDL pivot order. Without any empirical comparison of GPTQ front-to-back vs. back-to-front across models and bitwidths, the theory's relevance to the practically-used algorithm is unvalidated. The paper's claim to explain "why a local greedy rule works so well globally" (line 15) for standard GPTQ is not directly supported.

- **The error bound (Theorem 5) assumes no clipping (ℤ† = ℤ), which standard GPTQ violates.** The bound's derivation uses per-coordinate rounding error ≤ 1/2, which fails when rounded values are clipped. The paper acknowledges this (line 247) and proposes methods that avoid clipping. However, the proposed methods (SSQR, HPTQ) differ from GPTQ in multiple ways — Huffman coding, sparse outlier storage, binary scale search — so performance gains cannot be cleanly attributed to the theoretical insight about avoiding clipping. The HRTN baseline partially controls for the Huffman component, but there is no ablation that isolates clipping vs. no-clipping while holding bit allocation, grouping, and scale selection constant.

- **Experiments do not directly validate the theoretical predictions.** The experimental section (Section 5) compares SSQR and HPTQ against GPTQ and RTN on WikiText-2 perplexity. None of the following sanity checks appear in the main text: (a) a comparison of GPTQ front-to-back vs. back-to-front to test whether order matters; (b) an empirical evaluation of whether the Theorem 5 bound holds or how loose it is; (c) an ablation isolating clipping vs. no-clipping. The paper's claim that the results "tie our theoretical findings to practical quantization" (line 245) is not supported by the experimental design.

### Minor

- **Insufficient differentiation from prior work (QuIP/LDLQ).** The related work (line 27) mentions that QuIP (Chee et al., 2023) "proves an error guarantee for GPTQ and proposes the LDLQ method as an equivalent variant of GPTQ" — using the same LDL decomposition this paper relies on. The paper does not explain how its error bound differs from QuIP's, whether it is tighter, or what the Babai interpretation adds beyond LDLQ's analysis. A reader familiar with QuIP is left uncertain about the additional contribution.

- **The main text is thin on experiments.** Only one dataset (WikiText-2) and one figure (Figure 4) appear. Zero-shot accuracy, Llama-family results, and ablation studies are deferred to the appendix, making it hard to assess robustness from the main text alone.

### Trivial

None.

## Nice-to-Haves

- Add an experiment comparing GPTQ front-to-back vs. back-to-front across several models and bitwidths to directly test the order assumption.
- Provide an ablation isolating clipping vs. no-clipping while holding all else constant.
- Empirically evaluate the Theorem 5 bound by computing actual error vs. bound ratio per layer.
- Compare the paper's error bound to QuIP's bound explicitly.
- State clearly whether the GPTQ baseline in experiments runs front-to-back or back-to-front.

## Removed Points

These points from the harsh critic are removed with brief justification:

- *"The paper never justifies that the difference is superficial"* — removed because the paper does provide an algebraic proof (deferred to Appendix C, as stated on line 193). The deeper concern (lack of *empirical* validation) is retained in Major weaknesses.
- *"Standard GPTQ uses INT4 grid {-8,...,7}"* — this is information stated in the paper itself (§3.1), not a criticism.
- *"Missing appendix content"* — the parser strips appendices from all papers; the appendix exists in the original submission. The concern about thin main-text experiments is retained in Minor weaknesses since it is about presentation, not missing content.
- *"No experiment comparing GPTQ front-to-back vs. back-to-front"* — this is retained as a Major weakness.
- The harsh critic's strength about "important problem" is removed as generic/superficial. Retained strengths are concrete and grounded in specific paper content.
- The claim that "the bound has a factor √(c+1) ≈ 64 — a loose bound" is demoted to Nice-to-Have: it is a known property of Babai's bound (not specific to this paper) and does not constitute a methodological flaw.

## Novel Insights

The harsh critic insightfully notes a tension the paper does not resolve: the claim that the order difference is "superficial" (line 187) coexists uneasily with Section 4.5's detailed analysis of how order affects the error bound. This suggests the paper would benefit from explicitly distinguishing between the algebraic equivalence proof (which works for matched orders) and the practical question of whether front-to-back vs. back-to-front GPTQ produce similar outcomes (which is untested). A second observation: the paper's flow (Theorem 4: equivalence → Theorem 5: bound from Babai → Section 5: design no-clipping methods) is logically coherent, but the experimental section tests the final link in this chain without verifying the earlier links, making the claimed support circular.

## Suggestions

1. Add a comparison experiment of GPTQ front-to-back vs. back-to-front across multiple models (e.g., Llama-2/3, Qwen2/3) and bitwidths to ground the "superficial difference" claim empirically.
2. Add an ablation that isolates clipping vs. no-clipping while holding scale selection, grouping, and bit allocation fixed.
3. Empirically evaluate the Theorem 5 bound by computing the ratio of actual error to the bound for each layer; report whether the bound is tight or loose and under what conditions.
4. Include QuIP/LDLQ as an explicit baseline in the experiments and compare error bounds analytically in the main text.
5. Tone down the framing in the abstract and introduction: the theory explains a variant of GPTQ (back-to-front) under a specific condition (no-clipping), and the paper should acknowledge the scope gap to standard GPTQ upfront rather than claiming to "place GPTQ on a firm theoretical footing."

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| DiscQuant (vJmpg0exYA.md) | 4.50 | R1+R2 | Yes | Similar structure (theory→algorithm), but DiscQuant empirically tests its assumptions while this paper does not. This paper has more novel theory. |
| SPFQ (vmiV4Z99lK.md) | 4.25 | R1+R2 | Yes | Theory-heavy, experiments on small networks only. This paper has better experiments (real LLMs) and more novel theory. |
| PVQ for LLMs (ZBlfjXubgG.md) | 5.00 | R1+R2 | Yes | Mixed reviews (1-8). Similar theory-practice gap. Comparable quality. |
| RIQ (CXjz7p4qha.md) | 5.25 | R2 | Yes | Stronger theory-experiment alignment but less novel theory. |
| LL-VQ-VAE (sfTsvy05MX.md) | 4.75 | R1 | Yes | Related lattice VQ method for different domain. |

**Round 1 bracket:** 4.0–5.5 (below DiscQuant/SPFQ on theory-experiment alignment, but above them on theoretical novelty).

**Narrowing:** Comparison with DiscQuant (4.50) shows DiscQuant's impact profile has strong theory items (+9.8 to +10.0) paired with experiments that at least validate assumptions (+9.9). This paper's theory items are equally strong (+10.0 for novel connection), but the corresponding experimental-validation weaknesses are decisively negative (-9.99 for order issue, -9.85 for no-clipping bound, -9.55 for confounded experiments). DiscQuant received a 4.50 despite having a less novel theoretical insight but stronger validation. This paper's theoretical novelty is greater, pushing it above DiscQuant, but its validation gap is wider, keeping it below 5.5. The closest comparators (PVQ at 5.00, RIQ at 5.25) have similar trade-offs.

**Final placement:** 5.0 — the paper has a genuinely novel theoretical contribution that is worth publishing in principle, but the overclaiming, the lack of experimental validation of the theory, and the insufficient differentiation from QuIP mean the current submission does not meet the bar for acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>