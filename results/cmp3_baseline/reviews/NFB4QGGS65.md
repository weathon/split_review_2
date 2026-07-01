## Summary

This paper establishes a novel theoretical connection between GPTQ (a standard post-training quantization method for LLMs) and Babai’s nearest plane algorithm for the closest vector problem (CVP). The authors show that, when run back-to-front, GPTQ is mathematically identical to Babai’s algorithm applied to the lattice defined by the Hessian of the layer’s inputs. This equivalence yields a tight worst-case error bound for GPTQ under no-clipping, and motivates two new quantization schemes (SSQR and HPTQ) that avoid clipping, together with efficient GPU inference kernels. The work provides a long-missing geometric interpretation of GPTQ and opens the door to importing lattice-reduction techniques into LLM quantization.

## Strengths

- **Novel theoretical insight**: The connection between GPTQ and Babai’s nearest plane algorithm is both surprising and elegant. It provides a clear geometric interpretation for GPTQ’s error propagation, which was previously described only as a sequence of algebraic updates. This is a genuine contribution to understanding a widely-used algorithm.
- **Rigorous formalization**: The paper carefully defines the quantization problem as an instance of CVP (Theorem 1), derives the equivalence step by step (Theorem 4), and provides a tight absolute error bound (Theorem 5) that inherits Babai’s guarantees. The reasoning is logically sound and well-documented.
- **Practical spin-off**: The theoretical analysis is not purely conceptual. It leads to the design of no-clipping quantization schemes (SSQR, HPTQ) that respect the bound and outperform original GPTQ on perplexity, as shown on Qwen3-8B. The accompanying CUDA kernel demonstrates practical speedups.
- **Clear exposition**: The paper is well-structured, with helpful figures (e.g., Figure 2) and a concise CVP–quantization dictionary (Table 1). Notation is consistent and the mathematical derivations are presented clearly.

## Weaknesses

### Fatal
None.

### Major
- **Insufficient experimental comparison with state-of-the-art**: The practical evaluation is limited to comparisons with RTN, GPTQ, and self-variants (SSQR, HPTQ). To support claims of “state-of-the-art” or practical value, the paper should compare against other leading PTQ methods such as QuIP, AWQ, or the latest SpQR variants, across multiple model families and tasks (e.g., zero-shot benchmarks). The current experiments (Wikitext-2 perplexity for Qwen3 only, plus some appendix results for LLaMA) are not enough to convincingly demonstrate superiority or generality.
- **Lack of empirical verification of the error bound**: Theorem 5 provides a tight theoretical upper bound for the per-layer quantization error under no-clipping. The paper does not measure this error empirically or verify how tight the bound is in practice. Such validation would strengthen the theoretical claims and give practitioners confidence in the bound’s usefulness.
- **Limited novelty of the proposed quantization methods**: SSQR is essentially SpQR with a binary search over scales to avoid clipping; HPTQ is Huffman encoding combined with GPTQ. While both are sensible applications of the theory, they exhibit limited algorithmic novelty beyond existing work (Dettmers et al., 2024; Choi et al., 2017). The paper would benefit from a more extensive ablation study isolating the contribution of the no-clipping constraint itself.

### Minor
- **Default GPTQ order is front-to-back**: The equivalence requires GPTQ to run from the last to the first dimension, which is a superficial change. The paper correctly notes this, but the practical methods still use the standard front-to-back order (act‑order). The theoretical connection is therefore slightly indirect for the typical usage.
- **Dependence on the no-clipping assumption**: The error bound (Theorem 5) and the core CVP equivalence (Theorem 1) assume no clipping ($\mathbb{Z}_\dagger = \mathbb{Z}$). While the paper acknowledges this and migitates it with new no-clipping methods, the direct applicability to clipped GPTQ (which is widely used) remains unaddressed.

### Trivial
- Some caption text is duplicated under figures (e.g., Figure 1), which is a minor presentation glitch.

## Nice-to-Haves

- A systematic comparison with LLL‑reduced basis quantization (even preliminary simulations) would strengthen the claim that importing lattice algorithms is useful.
- Including the actual layer‑wise error bound values from the model would help readers assess the tightness.
- Ablation: How much of the perplexity gain comes from avoiding clipping versus from the specific scale/search mechanism in SSQR/HPTQ?

## Novel Insights

Beyond the paper’s own contributions, the most striking insight is that the seemingly heuristic “optimal brain surgeon” style correction in GPTQ is, in fact, an exact implementation of a classical lattice‑algorithm projection step. This recasts weight quantization as a geometric search on a lattice defined by the Hessian, and explains why the greedy GPTQ order works well: it corresponds to Babai’s nearest‑plane heuristic, which is known to have bounded approximation error. The paper also notes that composing GPTQ with itself is redundant (Section C.4), which clarifies the limits of iterative refinement.

## Suggestions

- Expand the experimental evaluation to include at least 2–3 additional model families (e.g., LLaMA‑2/3, OPT) and a standard zero‑shot benchmark suite (e.g., MMLU, HellaSwag, ARC). Compare against QuIP, AWQ, and the original SpQR without the scale‑adjustment fix.
- Add a small empirical study that measures the actual per‑layer quantization error (in L2 norm) and compares it to the bound in Theorem 5. This would confirm that the bound is meaningful.
- Discuss the cost of the GPU kernel relative to standard integer kernels (e.g., bitsandbytes) rather than only against PyTorch BF16.

## Score and Decision

The paper’s theoretical contribution—the equivalence between GPTQ and Babai’s nearest plane algorithm—is original, well‑supported, and likely to influence future quantization research. The error bound and the geometric interpretation are genuine advances. However, the practical portion is not yet fully convincing: the experimental validation is too narrow to claim state‑of‑the‑art, and the proposed methods have limited novelty. Nevertheless, the core theoretical result is strong enough to merit acceptance at a top venue.

**Score**: 6  
**Decision**: Accept  

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>