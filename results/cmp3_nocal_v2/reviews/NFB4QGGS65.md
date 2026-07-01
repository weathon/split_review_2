## Summary

This paper establishes that GPTQ, when executed back-to-front (last dimension to first), is mathematically identical to Babai's nearest plane algorithm on a lattice defined by the layer's Hessian matrix. This connection yields a tight, layer-wise error bound (Theorem 5) under the no-clipping assumption. The paper also proposes two no-clipping PTQ methods (SSQR and HPTQ) with GPU inference kernels. The core theoretical contribution — the geometric interpretation and the Babai equivalence — is genuinely novel and non-obvious.

## Strengths

1. **A genuinely insightful theoretical connection.** Theorem 4 — that GPTQ run back-to-front is identical to Babai's nearest plane algorithm — is well-motivated, clearly argued, and non-trivial. Sections 4.1–4.3 build this case carefully: first showing the quantization objective is a CVP (Sec 4.1), then interpreting OBQ's error propagation as a nearest-hyperplane projection (Theorem 2, Sec 4.2), and finally establishing the algorithmic equivalence (Theorem 4, Sec 4.3). This is the first geometric interpretation for GPTQ that I am aware of.

2. **A concrete, tight error bound.** Theorem 5 (Sec 4.4) translates Babai's classical guarantee into a layer-wise bound on GPTQ's quantization error in the no-clipping regime. The bound is tight (Babai's original bound is tight), and a relative approximation guarantee is also imported. This goes beyond generic LDLQ guarantees from prior work.

3. **Honest about limitations.** The paper transparently reports that min-pivot yields only "modest" downstream accuracy gains despite consistently reducing tr(D) (Sec 4.5). It also acknowledges concurrent work (Birnick, 2025) and correctly situates itself relative to QuIP/LDLQ. This candor is valuable.

4. **Ineffectiveness of composition result (Sec 4.3).** The observation that once Babai's projection is executed, any further GPTQ-style correction is algebraically redundant is a clean structural result that confirms the equivalence is tight.

## Weaknesses

### Major

1. **The equivalence is for back-to-front GPTQ; the paper's broader claims about explaining "why GPTQ works" outpace what is proven.** The paper states that GPTQ's inner workings are obscure and asks "why does a local greedy rule work so well globally?" (line 15). The answer provided — the Babai equivalence — holds for GPTQ executed from the *last* dimension to the *first* (Theorem 4), whereas standard GPTQ runs front-to-back (first to last). The paper calls this reversal "the only (superficial) difference" (line 187) but offers no analysis to justify calling it superficial. Section 4.5 discusses how quantization order affects the bound but never answers: what does the standard front-to-back GPTQ correspond to in the Babai/lattice framework? Does it implement a different CVP algorithm? Does the error bound in Theorem 5 apply to it? Without this analysis, the claim of placing "GPTQ on a firm theoretical footing" (abstract) overreaches — the footing is firm for a variant, and the gap to the actual algorithm is unaddressed. **Why this matters:** This is the paper's central narrative, and the scope of the theoretical contribution is narrower than the framing suggests.

### Minor

2. **The practical claims ("outperform the original GPTQ") are supported by thin evidence in the main paper.** The abstract claims the proposed methods "outperform the original GPTQ," but the main paper's experimental support consists of Figure 4(a) showing one model (Qwen3-8B) on one dataset (WikiText-2) with one metric (perplexity), presented without error bars or a table of exact numerical values. Additional results are deferred to the appendix. While it is common to defer detailed evaluations, the strength of the claim in the abstract is mismatched with the evidence present in the main text. A single table in the main paper would significantly strengthen credibility.

3. **The two proposed methods (SSQR, HPTQ) are heuristic bridges to the no-clipping regime, not methods derived from the bound.** The paper states it is "Leveraging this bound" (abstract) to design methods, but SSQR is essentially SpQR with a scale-tuning binary search loop (line 251–252) and HPTQ uses Huffman encoding with an entropy-guided scale search (line 253). Neither method uses Theorem 5's bound to guide its design in a nontrivial way — the bound motivates *that* clipping should be avoided, but doesn't inform *how*. The theory-practice bridge is via heuristics rather than derivation from the bound itself. The paper is candid about the challenge ("enforcing no-clipping by simply increasing scales is counterproductive," line 249), but the gap remains.

4. **SSQR is not compared against the original SpQR, which it directly modifies.** SSQR "discard[s] SpQR's second-level quantization for the scales" (line 251), a significant simplification. The main paper does not compare SSQR to the original SpQR to assess the impact of this change, making it difficult to evaluate whether the modification is beneficial.

5. **Huffman decoding overhead on GPUs is not discussed for HPTQ.** HPTQ uses Huffman-encoded integers with variable-length codewords. The paper does not discuss the implications of variable-length decoding during inference on GPUs, where irregular memory access patterns can introduce significant overhead. The CUDA kernel is only implemented for SSQR (line 269), not HPTQ, leaving the practical feasibility of HPTQ for deployment unclear.

### Trivial

None.

## Nice-to-Haves

- Analyze what standard front-to-back GPTQ corresponds to in the Babai/lattice framework, or explicitly acknowledge the limitation and its implications.
- Investigate why act-order (a simple diagonal heuristic) captures "most of the benefit" relative to the principled min-pivot order, which would deepen the theoretical contribution.
- Add a table with exact perplexity numbers in the main paper for key comparisons.
- Compare SSQR against the original SpQR to validate the simplifications made.

## Removed Points

These points were flagged during review but are excluded here for the following reasons:

- **Criticism about Theorem 4 proof being deferred to appendix / Theorem 2 proof being "not self-contained":** These are complaints about proofs being in the appendix, which is a standard formatting choice; the parser strips appendix content from all papers. Per guidelines, such criticisms are removed.
- **"No numerical results in the main paper":** Factually inaccurate — Figure 4 does contain numerical axes and results. The concern about lack of a table with exact numbers is captured in Weakness #2 above.
- **"CVP hardness discussion is tangential":** This is background context in the Related Work section, not a flaw in the paper's contributions.
- **"Missing related works":** Cannot be verified externally.
- **"The paper would be strongest if reframed as a theoretical paper":** This is a recommendation, not a weakness of the presented work.

## Novel Insights

Beyond the paper's own contributions, the review surfaces a subtle tension: the paper's strongest point (the Babai equivalence) and its main weakness (the front-to-back gap) stem from the same source. The paper identifies that GPTQ's order is the *only* difference from Babai and calls it superficial, but never validates this empirically or theoretically. This creates an opportunity: either the order reversal truly is superficial (which would be worth proving), or standard GPTQ corresponds to a different lattice algorithm with its own properties (which would be worth characterizing). Either direction would strengthen the paper more than adding heuristic no-clipping methods.

## Suggestions

1. **Tighten the framing.** Reframe the abstract and introduction to precisely reflect the scope of the theoretical contribution: "we show that back-to-front GPTQ is Babai's algorithm, yielding a tight error bound and geometric interpretation. We analyze the role of quantization order via this lens, and we propose no-clipping variants that avoid violating the bound's preconditions." This aligns the claims with the evidence.
2. **Consider whether the order reversal is truly superficial.** Add a brief analysis or experiment showing how front-to-back GPTQ relates to the Babai framework — even a negative result ("front-to-back is not obviously Babai on any simple transformation") would clarify the contribution's scope.
3. **Add one table with exact perplexity numbers** to the main paper for the key comparison (HPTQ vs GPTQ at matched bitwidths).
4. **Compare SSQR against the original SpQR** to validate the simplifications.

## Score and Decision

**Score:** 6

**Decision:** Borderline Accept

The theoretical contribution (the GPTQ↔Babai equivalence and the geometric interpretation) is genuinely novel, well-articulated, and worth publishing. The paper's primary weakness is a mismatch between the scope of the claims — about "GPTQ" broadly and about "outperforming" it — and what is actually proven and shown. The core theory is solid; the overclaiming can be addressed by tightening the narrative and either strengthening or tempering the practical evidence. I lean toward acceptance with the expectation that the authors will clarify the scope of their theoretical claims.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>