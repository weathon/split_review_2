## Summary

This paper establishes that GPTQ, when run back-to-front, is mathematically identical to Babai's nearest plane algorithm on a lattice defined by the Hessian matrix of a linear layer. It derives a tight layer-wise error bound (Theorem 5) in the no-clipping regime, proposes a min-pivot ordering heuristic, and presents two no-clipping quantization methods (SSQR, HPTQ) with GPU inference kernels.

## Strengths

- **The GPTQ–Babai equivalence (Theorem 4) is a genuine, non-obvious theoretical connection between LLM quantization and computational lattice theory.** The paper provides both a geometric argument and an algebraic proof, making the connection precise. This is a genuinely illuminating result that clarifies why a greedy per-dimensional rounding procedure can work well globally.

- **Theorem 5 gives a nontrivial, tight layer-wise error bound for GPTQ in the no-clipping regime**, correctly derived from Babai's framework and specific to the Hessian-defined lattice. The bound is not merely a restatement of Babai's bound; it reflects the structure of the quantization problem.

- **The paper is unusually honest about its limitations.** It explicitly states the back-to-front ordering requirement, that the bound assumes no clipping, that min-pivot gains are modest, and discloses concurrent work (Birnick 2025). This candor makes the remaining claims more credible.

## Weaknesses

### Major

- **The core equivalence (Theorem 4) is established for back-to-front GPTQ, not the standard front-to-back version used in practice.** The paper acknowledges this difference and calls it "superficial" (line 187: "This is the only (superficial) difference"), but the ordering determines the error-propagation direction: in standard front-to-back GPTQ, earlier-quantized rows are updated by later rows of the lower-triangular factor L, while back-to-front reverses this flow. The paper provides no experimental characterization of how much the two orderings differ in practice, nor a symmetry argument relating them. This limits the direct applicability of the paper's central theoretical result to a sibling procedure rather than the exact algorithm practitioners deploy.

- **The error bound (Theorem 5) requires no clipping (ℤ† = ℤ), which is not the regime where standard GPTQ is deployed.** The paper acknowledges this and provides a forward-looking justification (modern micro-scaled floating-point formats like MXFP4/NVFP4 are effectively no-clipping). This is reasonable for future applicability, but as a backward-looking account of *why GPTQ works so well* in its standard INT4 clipped setting, the bound has limited explanatory power.

### Minor

- **The main-text experimental evidence is thin for the practical claims made.** Section 5 presents exactly one figure (Figure 4) with perplexity on one model (Qwen3-8B). Downstream zero-shot accuracy, Llama-family results, and comparisons with additional methods are deferred entirely to the appendix. For a paper whose abstract claims its practical methods "outperform the original GPTQ," the main body does not provide sufficient evidence to independently substantiate this claim. At minimum, one downstream accuracy table should appear in the main text.

- **QuIP/LDLQ is acknowledged in the related work (line 27) as proving an error guarantee for GPTQ and proposing an equivalent GPTQ variant, but is not included as an experimental baseline.** Given the clear overlap in aims, this omission weakens the case that the proposed methods provide added value relative to the closest prior work.

- **The min-pivot ordering's improvement is stated only qualitatively.** The paper says it "consistently reduces tr(D)" and "downstream accuracy gains are modest" (line 219) without quantifying either claim in the main text (e.g., "tr(D) reduced by X% on average").

### Trivial

None.

## Nice-to-Haves

- A small-scale numerical verification that back-to-front GPTQ and Babai (without LLL) produce identical quantized weights in finite-precision arithmetic would directly confirm Theorem 4 and substantially increase confidence.
- An empirical plot of actual layer-wise quantization error against the Theorem 5 bound across layers of a real model would validate whether the bound is informative or loose.
- Showing that the scale-selection procedures in SSQR/HPTQ approximately minimize the bound in Theorem 5 under a fixed bit-budget would tighten the theory-practice link.

## Removed Points

- **"SSQR/HPTQ are loosely connected to the theory"** — The paper positions these as applications that operate in the no-clipping regime (where the bound applies), not as consequences of the bound. The specific designs being heuristic is a reasonable engineering choice; the theory provides motivation but need not dictate implementation details. Moved to nice-to-have.
- **"No numerical verification of the equivalence"** — The paper provides an algebraic proof, which is rigorous for the formal claim. Moved to nice-to-have.
- **"Typo in equation (2)"** — Parser artifact; removed per hard rules.
- **"Abstract phrasing of 'inherits' could mislead"** — Speculative and minor; removed.
- **"Only one metric in the main text"** — Already covered in the main weaknesses as "thin experimental evidence."

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a small-scale numerical verification that back-to-front GPTQ and Babai (without LLL) produce identical results on at least one real layer.
2. Move at least one downstream zero-shot accuracy table (ARC, HellaSwag, WinoGrande) from the appendix into the main text.
3. Include QuIP/LDLQ as a baseline in the experimental comparison.
4. Quantify the min-pivot improvement numerically (e.g., "tr(D) reduced by X% on average, but perplexity improved by < 0.1").
5. Consider reframing the practical methods section as "methods enabled by the no-clipping regime" rather than "methods derived from the bound" to better reflect the actual relationship between theory and practice.

---

## Calibration Report

**Round-1 bracket:** 4.5 – 6.0 (based on comparison to anchors)

**Anchors retrieved (all rounds):**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| DiscQuant (vJmpg0exYA) | 4.50 | R1 | Similar theory-heavy quantization paper with thin experiments; our paper has more novel theory and is more honest about limitations |
| SPFQ (vmiV4Z99lK) | 4.25 | R1 | Similar error-bound quantization theory paper with weak experiments; our paper has stronger practical relevance |
| Pyramid VQ for LLMs (ZBlfjXubgG) | 5.00 | R1 | Mixed theory/practice, polarized reviews; our paper is better written and more coherent |
| OSTQuant (rAcgDBdKnP) | 6.20 | R1 | Strong experiments and practical method; our paper has stronger theory but much thinner experiments |
| Catalyst Framework (XaARrKTNh3) | 5.25 | R2 | Theoretical paper with limited experiments; comparable structure |
| Equivariant QGNN (KbvKjpqYQR) | 6.00 | R2 | Less comparable topic |

**Narrowing:** After reading DiscQuant (4.50) and SPFQ (4.25) in full, the paper under review is clearly stronger in theoretical novelty and presentation quality, placing it above the 4.25–4.50 range. But it falls short of OSTQuant (6.20) in experimental thoroughness. The final score of 5.0 reflects a paper with a genuinely novel theoretical core that is not sufficiently substantiated by the experimental evidence provided in the main text, and whose central result has scope limitations that are acknowledged but not explored.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>