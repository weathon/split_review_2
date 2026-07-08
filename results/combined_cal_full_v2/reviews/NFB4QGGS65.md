Now I'll compose the final consolidated review.

## Summary

This paper establishes a novel theoretical connection: GPTQ, when executed back-to-front (from the last to first dimension), is mathematically identical to Babai's nearest plane algorithm on a lattice defined by the factorized Hessian (Theorem 4). This provides a geometric interpretation for GPTQ's error propagation, and imports Babai's tight error bound as a layer-wise guarantee for GPTQ in the no-clipping regime (Theorem 5). The paper also proposes no-clipping practical variants (SSQR, HPTQ) and provides GPU inference kernels.

## Strengths

- **Genuinely novel theoretical connection.** The GPTQ–Babai equivalence (Theorem 4, Section 4.3) is a nontrivial insight that gives geometric meaning to what was previously described as a sequence of greedy algebraic updates. The paper provides both a geometric proof via hyperplane projection (Theorem 2) and an algebraic proof (appendix), and correctly acknowledges concurrent work. This is the paper's primary contribution and is solid.

- **Imported error bound with analytic consequences.** Theorem 5 imports Babai's tight error bound to GPTQ under the no-clipping assumption, expressed in terms of the LDL decomposition of the Hessian. The bound is tight (equality at the hyper-cuboid corner) and provides a principled explanation for why GPTQ outperforms round-to-nearest. The visualization in Figure 1 clearly illustrates the geometric difference in rounding boundaries.

- **Thoughtful quantization-order analysis (Section 4.5).** The observation that the error bound depends on how scaling factors align with the diagonal entries of the LDL decomposition is well-motivated. The min-pivot ordering (Algorithm 3) is a principled heuristic, and the paper honestly reports that accuracy gains are modest.

## Weaknesses

### Major

- **Theory–experiment mismatch on the central equivalence claim.** Theorem 4 requires GPTQ to run **back-to-front** (dimension c to 1) to be equivalent to Babai's algorithm. Theorem 5's error bound additionally assumes **no clipping** ($\mathbb{Z}_\dagger = \mathbb{Z}$). Yet every experiment in Section 5 uses the original **front-to-back** GPTQ order (act-order, line 255: "The quantization order is act-order for all methods"). The paper never runs back-to-front GPTQ to validate the equivalence empirically. This means the theoretical guarantee (Theorem 5) does not apply to any algorithm actually tested. The headline equivalence is about back-to-front GPTQ, but the experiments only test front-to-back GPTQ, severing the evidence chain from theory to practice. The proposed methods (SSQR, HPTQ) are motivated by satisfying the no-clipping assumption, but since they run front-to-back, the Babai bound does not apply to them either. Fixing this requires either (a) running back-to-front GPTQ experiments to validate the theory, or (b) scaling back the practical claims and presenting the paper as a pure theory result.

- **Weak connection between theory and proposed practical methods.** SSQR and HPTQ are engineering heuristics (scale-adjustment with outlier storage; Huffman encoding with a scalar scale) that happen to avoid clipping, but the paper does not show they improve *because* they satisfy the Babai bound, as opposed to other factors (extra outlier storage budget, variable-rate encoding). A proper ablation would compare front-to-back GPTQ with clipping vs. back-to-front GPTQ without clipping (pure Babai) vs. SSQR/HPTQ to attribute improvements to the bound.

- **Experimental evaluation is thin relative to the practical claims.** The main paper contains exactly one experimental figure (Figure 4): one dataset (WikiText-2) on one model (Qwen3-8B) for method comparison, scaling across model sizes on one dataset, and speedup measurements on one GPU at batch size 1. No error bars or variance information is reported. Standard practice in LLM quantization includes multiple datasets (WikiText-2, C4, PTB), zero-shot accuracy on multiple tasks, and comparisons against baselines like AWQ, QuIP, SmoothQuant — none appear. The paper claims HPTQ produces "Pareto optimal" 3.125-bit results and SSQR achieves "about 2× speedup," but these claims are uncalibrated without proper baselines or variance.

### Minor

- **SSQR kernel speedup compared against the wrong baseline.** The speedup in Figure 4(c) compares SSQR against PyTorch BF16 matmul, not against a quantized baseline (e.g., INT4 GPTQ inference via the Marlin kernel). A 2× speedup over BF16 is expected for 4-bit quantization; the relevant question is whether SSQR's sparse outlier overhead negates gains relative to other quantized systems.

- **No error bars or variance.** Perplexity varies with random seeds and calibration data. Single-run measurements provide no confidence in the claimed improvements.

- **Min-pivot complexity not fully clarified.** The paper states min-pivot has "cubic time complexity and does not increase the overall time complexity of quantization" (line 219). Since GPTQ's preprocessing is already O(c³) due to LDL decomposition, if min-pivot runs a separate O(c³) loop the total constant-factor work could double. The paper should clarify whether min-pivot can be folded into the existing LDL factorization.

### Trivial

None.

## Nice-to-Haves
- Run back-to-front GPTQ and compare directly to front-to-back GPTQ at multiple bitwidths to empirically test whether the equivalence matters for accuracy.
- Compute the Theorem 5 error bound for back-to-front GPTQ (no clipping) and compare against empirical error to validate the bound directly.
- Include at least one additional evaluation dataset (C4 or PTB) and zero-shot task results in the main paper.
- Compare SSQR kernel speedup against a quantized inference baseline (e.g., INT4 GPTQ via Marlin), not just BF16.
- Add error bars or variance information for all perplexity measurements.

## Removed Points

These points are flagged to be removed; treat them with caution.
- **"Typo in Equation (2)":** Parser/formatting artifact (missing bracket). Not an author error. REMOVED per formatting rule.
- **"Theorem 2 proof is too compressed":** Presentation style preference about exposition density. Not a substantive weakness. REMOVED.
- **"Ineffectiveness of composing algorithms lacks experimental demonstration":** This is a theoretical result whose proof is in the appendix, correctly scoped as algebraic. REMOVED.
- **"Missing appendix content":** The parser strips appendix sections; they exist in the original submission. REMOVED.
- **"No experiment validating the core equivalence claim (back-to-front GPTQ = Babai)":** Already covered under the theory–experiment mismatch Major weakness. REMOVED as duplicate.
- **"The paper should clarify how it differs from QuIP's error guarantee":** The paper does acknowledge QuIP in related work (line 27). This is a scope-creep request that is addressed. REMOVED.

## Novel Insights

The most insightful observation from the review is that the paper's structural weakness is not merely a matter of experimental thinness but a fundamental misalignment between what the theory proves and what the experiments test. The theory (Theorems 4–5) concerns back-to-front GPTQ without clipping, but every experiment uses front-to-back GPTQ. This is not an incremental gap that more experiments would trivially fill — it is a logical disconnect in the paper's narrative. The reviewer's suggestion to either run back-to-front GPTQ or reframe as a theory paper correctly diagnoses the core issue and provides a clear path to resolution. Beyond this, no genuinely novel insight emerges from the reviews beyond the paper's own contributions.

## Suggestions

1. **Run back-to-front GPTQ** and compare it directly to front-to-back GPTQ. Report whether the order matters empirically — either outcome is informative.
2. **Validate the error bound directly**: compute the Theorem 5 bound for back-to-front GPTQ (no clipping) and compare against empirical error.
3. **Ablate the no-clipping assumption**: compare GPTQ with and without clipping in both front-to-back and back-to-front orders to measure how clipping degrades the bound.
4. If the above experiments are infeasible, **reframe the paper as a theoretical contribution** with illustrative demonstrations and scale back the practical claims about SSQR/HPTQ.
5. Add error bars and at least one additional evaluation dataset to the experiments.
6. Compare SSQR kernel speedup against a quantized inference baseline, not just BF16.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Itemized | Comparison |
|-------|------|-----------|-------|----------|------------|
| CVXQ | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0T8vCKa7yu.md | 3.00 | 1 | Yes | LLM quantization theory paper; less novel theory, similar experiment gaps. Our paper has stronger theoretical contribution. |
| DiscQuant | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/vJmpg0exYA.md | 4.50 | 1,2,3 | Yes | Theory-heavy quantization (discrepancy theory); rejected due to missing baselines and computational concerns. Comparable theory depth but our paper has a structural theory-experiment gap. |
| SPFQ | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/vmiV4Z99lK.md | 4.25 | 2,3 | Yes | Quantization theory with error bounds; rejected due to theory-experiment disconnect and missing baselines. Similar structure to our paper but our theoretical contribution is more clearly novel. |
| PVQ for LLMs | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ZBlfjXubgG.md | 5.00 | 1,3 | Yes | Lattice quantization; mixed reception (scores: 8,6,1,5). Poor presentation, missing baselines. |
| LeanQuant | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ISqx8giekS.md | 5.17 | 2 | Yes | Practical LLM quantization with good experiments; accepted. Stronger empirically, weaker theoretically than our paper. |
| OSTQuant | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rAcgDBdKnP.md | 6.20 | 1 | Yes | Practical LLM quantization with comprehensive experiments; accepted. Our theory is more novel but experiments are much weaker. |
| Lattice Transform Coding | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Tv36j85SqR.md | 7.20 | 1 | Yes | High-quality theory+experiments about lattice quantization; accepted. Stronger in both theory and experiments. |

### Weighted-Item Comparison

My draft's three strengths (weights: 10.97, 9.94, 7.91) are strong positive signals, comparable to DiscQuant's theory strengths (11.00, 9.31) and SPFQ's (13.64, 11.14). However, my draft's three Major weaknesses (weights: -1.55, -0.83, -2.32) have a cumulative negative impact. The theory–experiment gap (weight=-1.55) and thin experiments (weight=-2.32) are the main drags.

DiscQuant's strongest weaknesses had weights around -2.14 (missing lattice comparisons) and SPFQ's around -6.33 (poor ICLR fit). My paper's weaknesses are less severe individually than SPFQ's worst, but the structural nature of the theory-experiment gap makes it more fundamental than DiscQuant's missing-baselines issue.

The approach of running back-to-front GPTQ and verifying the claim directly would resolve the structural gap, which is fixable — this is not a fatal flaw in the theory itself. This places the paper above SPFQ (4.25) where the theory-experiment disconnect was more severe (bounds not validated, experiments in appendix), but below PVQ (5.00) where despite presentation issues, the experiments at least matched the method described.

### Final Score and Decision

**Round 1 bracket**: 3.5 – 5.5  
**Round 2 narrowing**: 4.0 – 5.0  
**Final score**: 4.5

The paper has a genuine theoretical contribution that is novel and rigorous. However, the structural gap between the theory (back-to-front GPTQ) and experiments (front-to-back GPTQ) undermines the evidence chain, and the practical claims are not well-supported by the thin experimental evaluation. With significant revision — particularly running back-to-front experiments or reframing as pure theory — this could become a substantially stronger paper.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>