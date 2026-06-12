## Summary

This paper shows that GPTQ, when executed in the reverse dimensional order (last to first), is mathematically identical to Babai’s nearest plane algorithm for the closest vector problem (CVP) on a lattice defined by the Hessian matrix of the layer’s inputs. This equivalence provides a geometric interpretation of GPTQ’s error propagation and yields a tight layer-wise error bound in the no-clipping setting. Leveraging this insight, the authors propose two no-clipping quantization methods (SSQR and HPTQ) and provide efficient GPU inference kernels.

## Strengths

- **Clear and original theoretical contribution.** The paper establishes for the first time a direct equivalence between GPTQ and a well-known lattice algorithm (Babai’s nearest plane) with a geometric interpretation. This brings a principled perspective to a widely used method.
- **Rigorous derivation of an error bound.** Theorem 5 provides a tight, layer-wise absolute error bound for GPTQ in the no-clipping regime, importing decades of lattice-algorithm theory into LLM quantization.
- **Well-structured exposition.** The correspondence is built step by step, with helpful figures and a dictionary table linking quantization and CVP concepts, making the material accessible.

## Weaknesses

### Fatal

None.

### Major

1. **Limited experimental support.** The evaluation reports only perplexity on WikiText‑2. No zero-shot downstream accuracy, no comparisons with state-of-the-art PTQ methods (e.g., QuIP#, AQLM, GPTVQ, or recent uniform‑vs‑non‑uniform quantizers). Without broader validation, the claimed practical superiority of SSQR/HPTQ remains unconvincing.
2. **Theory vs. practice gap.** The error bound (Theorem 5) and the equivalence proof assume no clipping ($\mathbb{Z}_\dagger = \mathbb{Z}$), but standard GPTQ (and the proposed SSQR/HPTQ) involve finite integer grids. The paper argues that the equivalence holds “independently of clipping,” yet the proof in Section 4.3 implicitly relies on unbounded rounding. The practical relevance of the bound when clipping is used is not clearly established.
3. **Modest novelty of the proposed methods.** SSQR is a small modification of SpQR (outlier–inlier separation with scale adjustment), and HPTQ combines Huffman coding with GPTQ. Neither method deeply exploits the new lattice perspective (e.g., no basis reduction, no use of the derived bound to guide scale selection). The gains over GPTQ seem attributable mainly to variable-bitrate allocation rather than the geometric insight.
4. **GPU kernel evaluation is weak.** Only end‑to‑end speedup vs. PyTorch BF16 is shown (Fig. 4(c)). There is no comparison with other optimized quantized kernels (e.g., bitsandbytes, GPTQ’s kernel, Marlin), and no detailed breakdown of latency, memory footprint, or throughput across outlier rates.

### Minor

- The paper claims to be “first” while noting concurrent work (Birnick 2025). The novelty claim is defensible but should be toned down.
- The relative bound in Theorem 5 is presented without derivation or reference to the original Babai bound, making it hard to verify its tightness in the context of the specific LDL factorization.

### Trivial

- Figure 3 is cited but not referred to in the main text in a way that clarifies its role.

## Nice-to-Haves

- Extend perplexity experiments to additional tasks (e.g., ARC, HellaSwag, MMLU) and compare with modern PTQ methods such as QuIP#, AQLM, and the original GPTQ with the same bitwidths.
- Discuss whether LLL basis reduction could be incorporated into GPTQ and whether it would improve accuracy—a natural next step suggested by the lattice framing.

## Novel Insights

Beyond the paper’s own contributions, the most valuable insight is that a heuristic, widely‑used LLM quantization algorithm (GPTQ) is exactly a classic CVP approximator. This opens a concrete path to transplant lattice‑reduction techniques (LLL, BKZ) into LLM compression, potentially leading to algorithms with provably better worst‑case error. Conversely, the massive‑scale linear layers in LLMs might motivate new, faster lattice heuristics.

## Suggestions

1. Expand the experimental section to include downstream task accuracy and comparisons with at least two recent PTQ baselines (e.g., QuIP# and AQLM) at comparable bitwidths.
2. Clarify the precise conditions under which the equivalence holds when clipping is present, and discuss how the derived bound relates to the clipped setting.
3. Provide at least one experiment that uses the error bound to guide quantization (e.g., choosing the order to minimize the bound) and measure the effect on accuracy.

## Score and Decision

**Score:** 6  
**Decision:** Accept  

**MY FINAL SCORE:** <score>6</score>  
**MY FINAL DECISION:** <decision>Accept</decision>