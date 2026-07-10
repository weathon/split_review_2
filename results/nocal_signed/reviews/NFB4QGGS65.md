Now let me finalize the review based on these scores. The theoretical strength is very high (+9.9, +9.3), but the QuIP relationship issue (-9.7) and thin experimental evaluation (-8.9 for missing zero-shot, -7.7 for no QuIP comparison) are significant. The back-to-front/no-clipping limitation is noticeable but much less severe (-3.4, -2.2). The balance suggests a paper with a genuinely strong theoretical core that needs better positioning and broader validation.

## Summary

This paper establishes that GPTQ, when executed back-to-front, is mathematically identical to Babai's nearest plane algorithm for the closest vector problem on a lattice defined by the Hessian matrix. This equivalence yields a geometric interpretation of GPTQ's error propagation and a provable layer-wise error bound (under no-clipping). The paper also proposes no-clipping practical methods (SSQR, HPTQ) derived from this theory, with GPU inference kernels.

## Strengths

- **A genuinely non-obvious theoretical bridge**: The identification that GPTQ's error propagation step (Eq. 2) is algebraically identical to Babai's nearest plane projection (Algorithm 2) is a concrete and non-superficial connection between LLM quantization and lattice algorithms. The mapping in Table 1 and the formal equivalence in Theorem 4 are clean and theoretically grounded. This is the paper's strongest contribution.

- **A provable layer-wise error bound (Theorem 5)**: Importing Babai's guarantee to GPTQ yields an absolute error bound expressed in terms of the diagonal matrix **D** of the LDL decomposition and the scales **s**ᵢ. The bound is tight in the worst case. Even under the no-clipping assumption, this is a genuine theoretical property not previously stated in this form for GPTQ.

## Weaknesses

### Major

- **Relationship to QuIP (Chee et al., 2023) is inadequately addressed, undermining the novelty framing.** The Related Work states that QuIP "proves an error guarantee for GPTQ and proposes the LDLQ method as an equivalent variant," yet the Introduction claims that "Current literature does not answer" why GPTQ works and that this paper is "the first to provide a geometric interpretation." The paper never clarifies: whether Theorem 5's bound differs from, improves upon, or is equivalent to QuIP's bound; whether the LDL decomposition connection is already present in QuIP's LDLQ; or what the lattice/Babai framing adds that QuIP's analysis does not already provide. Without this clarification, a reader familiar with QuIP cannot determine what is genuinely new. This is the most critical issue because it directly affects how the paper's central contribution should be understood.

- **Experimental evaluation in the main paper is too narrow to support the broader claims.** The main paper presents results on one model family (Qwen3, 0.6B–14B) using one metric (WikiText-2 perplexity), with zero-shot task results deferred entirely to the appendix. Critically, there is no experimental comparison to QuIP (the closest theoretical baseline) or to SpQR (from which SSQR is derived). The claimed 2× speedup of the SSQR kernel is measured against PyTorch BF16, not against an optimized quantized kernel (e.g., the GPTQ kernel or bitsandbytes). These gaps mean the claim that SSQR and HPTQ "outperform the original GPTQ" is suggestive but not broadly demonstrated.

### Minor

- **The core theoretical results apply to a variant of GPTQ, not the standard algorithm.** The equivalence (Theorem 4) requires running GPTQ back-to-front (from last to first dimension), whereas standard GPTQ runs front-to-back. The error bound (Theorem 5) requires no-clipping (ℤ† = ℤ), whereas standard GPTQ uses clipped INT4 quantization. The paper is fully transparent about both constraints, and Section 5 designs methods around the no-clipping requirement. Nevertheless, these gaps limit the explanatory power of the theory for understanding the standard GPTQ algorithm as deployed in practice. The paper acknowledges this (e.g., by treating order as a design parameter in Section 4.5 and mentioning clipped grids as future work), but does not resolve the tension.

## Nice-to-Haves

- Provide a direct comparison between Theorem 5's bound and QuIP's bound, clarifying whether they differ, are tighter, or are equivalent.
- Analyze whether the front-to-back ordering of standard GPTQ also admits a lattice interpretation, or explicitly state why this is open.
- Measure actual quantization error against Theorem 5's bound across layers to show tightness empirically.
- Compare the SSQR kernel's speedup against other optimized quantized inference kernels, not just PyTorch BF16.
- Summarize zero-shot evaluation results from the appendix in the main paper.

## Removed Points

- The criticism that the abstract "conflates lack of geometric meaning with lack of worst-case guarantees": the abstract says GPTQ's description "obscure[s] geometric meaning **or** worst-case guarantees" — this is about the original GPTQ presentation, not a literature claim. REMOVED as a misreading.
- The criticism about the H⁻¹/Gram-Schmidt connection not being explicit enough: a presentation preference. REMOVED.
- The "section-by-section" notes about proof density: presentation preferences. REMOVED.
- The criticism that SSQR/HPTQ are "incremental modifications of existing methods": incremental practical methods are fine when presented honestly. REMOVED.
- The request for AWQ/SmoothQuant comparisons: these are activation-aware methods with different scope. REMOVED.

## Novel Insights

The paper's core insight — that GPTQ's error propagation is geometrically Babai's nearest plane projection when the dimensional order is reversed — is a genuinely non-obvious bridge between LLM quantization and lattice algorithms. This goes deeper than a notational equivalence: it follows from the specific structure of the LDL decomposition used in GPTQ and the Gram-Schmidt orthogonalization underlying Babai's algorithm. The practical consequence (Section 5) that no-clipping methods can be derived from the theory is also valuable. However, the unresolved relationship to QuIP means the novelty claims cannot be fully assessed as written.

## Suggestions

The paper would be significantly strengthened by: (1) explicitly differentiating its theoretical results from QuIP's (is the bound new? tighter? is the geometric interpretation new?); (2) broadening the experimental evaluation in the main paper to include multiple model families, zero-shot tasks, and comparison against QuIP; and (3) either addressing the front-to-back ordering or clearly stating it as an open question for future work.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>