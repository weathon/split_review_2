## Summary

This paper establishes a formal equivalence between GPTQ (a popular post-training quantization algorithm) and Babai's nearest plane algorithm for the closest vector problem (CVP) on a lattice defined by a layer's Hessian matrix. Concretely, when executed back-to-front (last dimension to first), GPTQ is mathematically identical to Babai's algorithm without LLL basis reduction (Theorem 4). This equivalence yields two analytical consequences: (i) a geometric interpretation of GPTQ's error propagation, and (ii) a tight layer-wise error bound inherited from Babai's guarantee (Theorem 5), valid in the no-clipping regime. The paper further designs no-clipping quantization methods (SSQR, HPTQ) motivated by this theory and provides optimized GPU inference kernels.

## Strengths

- **A genuinely novel theoretical bridge.** The paper connects two previously disconnected literatures—numerical quantization and computational lattice theory—by proving that GPTQ (back-to-front) = Babai's nearest plane algorithm (Theorem 4). This is the first geometric interpretation of why GPTQ's greedy sequential updates work, which the original GPTQ paper left as an open question. The equivalence is nontrivial and is supported by both a geometric sketch (Theorem 2) and an algebraic proof in the appendix.

- **An actionable error bound follows from the equivalence.** Theorem 5 imports Babai's worst-case guarantee to produce a tight layer-wise bound under no-clipping:  
  \(\|\mathbf{X} \operatorname{diag}(\mathbf{s}_i) \mathbf{z}_i - \mathbf{X} \mathbf{w}_i\|^2 \leq \frac{1}{4} (\mathbf{T}^{-1} \mathbf{s}_i)^\top \mathbf{D} (\mathbf{T}^{-1} \mathbf{s}_i)\).  
  This is not merely a restatement of known results—it ties the quantization error to the LDL decomposition of the Hessian and the quantization scales in a specific quadratic form, opening a principled channel for analyzing quantization orders and scale choices.

- **The "ineffectiveness of composing algorithms" observation (Section 4.3) is a crisp theoretical check.** The paper proves that once Babai's projection has been executed, any further GPTQ-style correction vanishes. This shows the equivalence is tight rather than approximate, and it rules out a naive but natural attempted improvement.

- **Intellectual honesty about limitations.** The paper explicitly states that min-pivot's downstream accuracy gains are "modest" (line 219), and that future work is needed to extend the analysis to clipped grids. This candor strengthens trust in the theoretical claims.

## Weaknesses

### Fatal
None.

### Major

1. **Practical claims ("outperform the original GPTQ") are insufficiently supported by the evidence presented in the main paper.**  
   The main-paper experiments (Figure 4) are limited to WikiText-2 perplexity on Qwen3-8B. No zero-shot accuracy numbers (MMLU, ARC, HellaSwag) appear in the main paper; no results on Llama models—the standard benchmark in the quantization literature—are shown in the main paper; and no comparison to contemporary methods like QuIP# or AQLM is visible. Furthermore, the comparison is confounded: HPTQ uses Huffman coding (variable-rate) against GPTQ's fixed-rate representation. The included HRTN baseline partially addresses this, but an ablation isolating the effect of the no-clipping regime from the effect of Huffman encoding would be needed to attribute gains to the theoretical insight. The paper states that additional experiments are in Section E (appendix), but as presented in the main text, the evidence is too thin to support the strong framing in the abstract. This is a **scope mismatch** between the theoretical contribution (which is strong) and the inflated practical claims.

2. **The gap between the theory and the proposed practical methods is large and unbridged.**  
   Theorem 5's error bound applies only to the GPTQ quantization step itself under no-clipping (\(\mathbb{Z}_\dagger = \mathbb{Z}\)). The proposed methods (SSQR with sparse outlier storage, HPTQ with Huffman encoding) introduce substantial additional machinery whose error is not bounded by Theorem 5. While the theory motivates the principle of avoiding clipping, it does not directly constrain or guarantee the performance of these complex engineering constructions. The connection is plausible but loose, and the paper would benefit from a clearer statement about which parts of the system the theory does and does not cover.

### Minor

3. **No ablation comparing front-to-back vs. back-to-front GPTQ.**  
   Theorem 4 establishes equivalence under back-to-front order, but standard GPTQ runs front-to-back. The paper calls this a "superficial difference" (line 187), yet Section 4.5 demonstrates that quantization order significantly affects results. An empirical comparison of the two orderings on real LLMs would clarify whether the mathematical equivalence has practical consequences or whether floating-point and order effects produce numerically different outputs. This is especially relevant because the practical evaluation uses act-order, not back-to-front.

4. **The geometric proof sketch of Theorem 2 in the main text is too compressed for independent verification.**  
   Lines 163–173 present the core geometric derivation in roughly 10 lines of dense algebra, including a coordinate transform via the inverse basis \(N = B^{-T}\), a \(\cos\theta\) identity, and a ratio argument arriving at the OBQ error propagation coefficient. Several steps (the relation \(\|\text{Proj}_{\mathcal{OPP}}(b_j)\|\|n_j\| = 1/\cos(\frac{\pi}{2} - \theta)\), the connection to \((\mathbf{B}^\top \mathbf{B})^{-1}\) entries) are asserted without expansion. The full proof resides in the appendix, but the main-text sketch is so compressed that a reader cannot assess its correctness without reconstructing the omitted algebra.

5. **The kernel speedup comparison uses a software baseline.**  
   The SSQR kernel is benchmarked against PyTorch BF16 matmul, not against an optimized GPTQ kernel (e.g., Marlin or the original GPTQ CUDA kernel). An optimized GPTQ kernel would itself be significantly faster than PyTorch BF16, so the claimed "about \(2\times\) speedup" may partially reflect the gap between a naive baseline and any optimized implementation, not a specific advantage of the SSQR representation.

### Trivial

6. **Algorithm 1 uses \(\text{LDL}(\mathbf{H}^{-1})\) while standard GPTQ factorizes \(\mathbf{H}\) via Cholesky (or LDL) and inverts the factor.** The paper states the algorithm is "identical to the original GPTQ paper" except for blocking, but this structural difference in the pseudocode is not flagged. While mathematically related, a practitioner implementing from this pseudocode might obtain different numerical results if not careful.

7. **Figure captions are nearly identical to body text (Figures 2 and 3),** making them redundant rather than complementary.

## Nice-to-Haves

- **Computational overhead of Huffman decoding on GPUs.** Variable-rate codes are notoriously difficult to deploy efficiently on GPUs due to irregular memory access. A discussion (or empirical measurement) of the HPTQ inference-time overhead would strengthen the practical section.
- **Error bars or variance estimates** for the perplexity numbers in Figure 4 would help assess statistical reliability.
- **A direct comparison to an optimized GPTQ CUDA kernel** (rather than PyTorch BF16) for the SSQR kernel speedup would clarify the practical advantage.

## Removed Points

These points were raised in the input review but are removed for the reasons stated:

- *"Missing proof in appendix"* (Theorem 4 deferred to appendix): Removed per instructions—the parser strips appendix content from all papers; the full proof exists in the original submission.
- *"QuIP relationship not discussed in enough depth"*: Removed per instructions about missing related-work discussion; the paper cites QuIP and states its contribution; I cannot verify the reviewer's claim that QuIP has "clear connections to lattice theory" without external sources.
- *"Min-pivot gains are modest, undercutting practical significance"*: Removed because the paper honestly acknowledges this; self-awareness of a limitation is not a weakness.
- *"The error bound uses LDL of permuted Hessian vs standard GPTQ's Cholesky"*: Merged into Trivial point 6 (redundant with the LDL/H⁻¹ observation).

## Novel Insights

The input review does not surface genuinely novel insights beyond the paper's own contributions. The observation that the theory-practice gap is large is a standard critical assessment, not a novel synthesis. The structural tension between the paper's strong theoretical result and its thin practical validation is correctly identified but does not constitute a new research direction beyond what the paper's future-work section already outlines.

## Suggestions

1. **Calibrate the practical claims to match the evidence.** The theoretical contribution (GPTQ = Babai) is strong enough to carry the paper on its own. Either downscope the practical narrative to a brief demonstration consistent with the main-paper evidence, or substantially expand the experimental section with multiple models, zero-shot benchmarks, and proper ablations isolating the effect of the theoretical principle from the engineering choices (Huffman coding, outlier storage).

2. **Add an ablation comparing GPTQ front-to-back vs. back-to-front** on at least one real LLM. Even if the results are identical (as the mathematics predicts), showing this would directly validate the practical relevance of the equivalence.

3. **Expand the geometric proof sketch of Theorem 2** in the main text. Even a few additional sentences clarifying the key steps (especially the \(\|\text{Proj}_{\mathcal{OPP}}(b_j)\|\|n_j\| = 1/\cos(\frac{\pi}{2} - \theta)\) relation and how it connects to \((\mathbf{B}^\top\mathbf{B})^{-1}\)) would make the argument self-contained enough for a reader to follow without reconstructing the appendix proof.

4. **Benchmark the kernel against an optimized GPTQ kernel** (e.g., Marlin) in addition to PyTorch BF16.

## Score and Decision

**MY FINAL SCORE: <score>7.5</score>**  
**MY FINAL DECISION: <decision>Accept</decision>**